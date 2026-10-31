#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/29
Desc: 沪深交易所 ETF 申购赎回清单与证券篮子市值占比
https://www.sse.com.cn/disclosure/fund/etflist/
https://www.szse.cn/disclosure/fund/currency/index.html
"""

import re
from datetime import datetime, timedelta, timezone
from xml.etree import ElementTree

import pandas as pd

from akshare.exceptions import DataParsingError, InvalidParameterError
from akshare.utils import http


def _parse_pcf(content: bytes, symbol: str, szse: bool) -> pd.DataFrame:
    """统一沪深 XML 字段，并保留证券代码的前导零。"""
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("gb18030")
    try:
        root = ElementTree.fromstring(text)
    except ElementTree.ParseError as err:
        raise DataParsingError("申购赎回清单应为 XML 文件") from err
    for node in root.iter():
        node.tag = node.tag.rsplit("}", 1)[-1]
    if root.findtext("SecurityID" if szse else "FundInstrumentID") != symbol:
        raise DataParsingError("申购赎回清单基金代码与请求代码不符")
    fields = {
        "证券代码": "UnderlyingSecurityID" if szse else "InstrumentID",
        "证券简称": "UnderlyingSymbol" if szse else "InstrumentName",
        "市场代码": "UnderlyingSecurityIDSource" if szse else "UnderlyingSecurityID",
        "证券数量": "ComponentShare" if szse else "Quantity",
        "现金替代标志": "SubstituteFlag" if szse else "SubstitutionFlag",
        "申购溢价比例": "PremiumRatio" if szse else "CreationPremiumRate",
        "赎回折价比例": "DiscountRatio" if szse else "RedemptionDiscountRate",
        "申购替代金额": "CreationCashSubstitute" if szse else "SubstitutionCashAmount",
        "赎回替代金额": "RedemptionCashSubstitute"
        if szse
        else "SubstitutionCashAmount",
    }
    path = "./Components/Component" if szse else "./ComponentList/Component"
    temp_df = pd.DataFrame(
        [
            {key: row.findtext(tag, "").strip() for key, tag in fields.items()}
            for row in root.findall(path)
        ],
        columns=list(fields),
    )
    if temp_df.empty or temp_df["证券代码"].eq("").any():
        raise DataParsingError("申购赎回清单证券明细缺失")
    for column in [
        "证券数量",
        "申购溢价比例",
        "赎回折价比例",
        "申购替代金额",
        "赎回替代金额",
    ]:
        temp_df[column] = pd.to_numeric(temp_df[column], errors="coerce").astype(float)
    if (
        temp_df["证券数量"].isna()
        | temp_df["证券数量"].lt(0)
        | temp_df["证券数量"].eq(float("inf"))
    ).any():
        raise DataParsingError("证券数量应为非负数")
    metadata = {
        "基金代码": symbol,
        "申赎单位": root.findtext("CreationRedemptionUnit"),
        "申赎单位净值": root.findtext("NAVperCU"),
        "现金差额": root.findtext("CashComponent" if szse else "PreCashComponent"),
        "预估现金差额": root.findtext(
            "EstimateCashComponent" if szse else "EstimatedCashComponent"
        ),
    }
    for key, value in reversed(list(metadata.items())):
        temp_df.insert(
            0,
            key,
            # 统一为浮点数：沪市清单写作 900000，深市写作 1000000.00，否则两市类型不一致
            value
            if key == "基金代码"
            else float(pd.to_numeric(value, errors="coerce")),
        )
    trading_day = pd.to_datetime(
        root.findtext("TradingDay", ""), format="%Y%m%d", errors="coerce"
    )
    if pd.isna(trading_day):
        raise DataParsingError("申购赎回清单交易日期缺失或格式错误")
    temp_df.insert(1, "交易日期", trading_day.date())
    temp_df["申赎现金"] = szse & temp_df["证券代码"].eq("159900")
    return temp_df


def fund_etf_pcf(symbol: str = "510300") -> pd.DataFrame:
    """
    沪深交易所 ETF 最新每日申购赎回清单（PCF）
    https://www.sse.com.cn/disclosure/fund/etflist/
    https://www.szse.cn/disclosure/fund/currency/index.html
    :param symbol: 六位 ETF 代码，如 "510300"、"159502"
    :type symbol: str
    :return: 每个最小申赎单位的证券明细及现金项目，金额单位为人民币元
    :rtype: pandas.DataFrame
    """
    if re.fullmatch(r"(?:5\d{5}|15\d{4})", symbol) is None:
        raise InvalidParameterError("请输入沪市 5 开头或深市 15 开头的六位 ETF 代码")
    szse = symbol.startswith("15")
    if szse:
        today = datetime.now(timezone(timedelta(hours=8))).date()
        r = http.get(
            "https://www.szse.cn/api/report/ShowReport/data",
            params={
                "SHOWTYPE": "JSON",
                "CATALOGID": "sgshqd",
                "TABKEY": "tab1",
                "txtJCorDH": symbol,
                "txtStart": (today - timedelta(days=365)).isoformat(),
                "txtEnd": today.isoformat(),
            },
            headers={"Referer": "https://www.szse.cn/"},
        )
        r.raise_for_status()
        # 公告索引覆盖休市日，选择最近公布的清单。
        dates = re.findall(rf"pcf_{symbol}_(\d{{8}})", str(r.json()))
        if not dates:
            raise DataParsingError(f"{symbol} 申购赎回清单公告缺失")
        r = http.get(
            f"https://reportdocs.static.szse.cn/files/text/ETFDown/pcf_{symbol}_{max(dates)}.xml",
        )
    else:
        r = http.get(
            "https://query.sse.com.cn/etfDownload/downloadETF2Bulletin.do",
            params={"fundCode": symbol},
            headers={"Referer": "https://www.sse.com.cn/"},
        )
    r.raise_for_status()
    return _parse_pcf(r.content, symbol, szse)


def _quote_prices(symbols: list) -> pd.Series:
    """分批请求腾讯行情，返回行情标识到最新价的映射。"""
    prices = {}
    symbols = list(dict.fromkeys(symbols))
    for offset in range(0, len(symbols), 50):
        r = http.get(
            "https://qt.gtimg.cn/q=" + ",".join(symbols[offset : offset + 50]),
        )
        r.raise_for_status()
        r.encoding = "gbk"
        for symbol, payload in re.findall(r'v_([A-Za-z0-9_]+)="(.*?)";', r.text, re.S):
            fields = payload.split("~")
            if len(fields) > 3:
                prices[symbol] = fields[3]
    return pd.to_numeric(pd.Series(prices, dtype="str"), errors="coerce").replace(
        [float("inf"), -float("inf")], float("nan")
    )


def fund_etf_holdings_tx(symbol: str = "510300") -> pd.DataFrame:
    """
    交易所 ETF 申赎篮子证券市值占比，使用腾讯最新价和人民币汇率估算
    https://www.sse.com.cn/disclosure/fund/etflist/
    https://gu.qq.com/
    :param symbol: 六位 ETF 代码，如 "510300"、"159502"
    :type symbol: str
    :return: 按市值占比降序排列的完整证券篮子，市值单位为人民币元，占比单位为 %
    :rtype: pandas.DataFrame
    """
    pcf = fund_etf_pcf(symbol)
    temp_df = pcf.loc[
        ~pcf["申赎现金"], ["证券代码", "证券简称", "市场代码", "证券数量"]
    ].copy()
    fixed = pcf.loc[temp_df.index, "现金替代标志"].eq("2")
    cash = pcf.loc[temp_df.index, "申购替代金额"].where(fixed)
    if (fixed & (cash.isna() | cash.lt(0) | cash.eq(float("inf")))).any():
        raise DataParsingError("必须现金替代证券的申购替代金额缺失或为负数")
    markets = {
        "101": "sh",
        "102": "sz",
        "103": "hk",
        "104": "bj",
        "106": "bj",
        "9999": "us",
    }
    prefixes = temp_df["市场代码"].map(markets)
    if prefixes.isna().any():
        raise DataParsingError("证券市场代码缺少对应的腾讯行情来源")
    if (
        prefixes.eq("us") & ~temp_df["证券代码"].str.fullmatch(r"[A-Z][A-Z0-9.]*")
    ).any():
        raise DataParsingError("境外证券代码需要对应的行情来源")
    codes = [
        code.replace(".", "_")
        if prefix == "us"
        else code.zfill(5 if prefix == "hk" else 6)
        for code, prefix in zip(temp_df["证券代码"], prefixes)
    ]
    quote_symbols = prefixes + codes
    temp_df["币种"] = prefixes.map(
        {"sh": "CNY", "sz": "CNY", "bj": "CNY", "hk": "HKD", "us": "USD"}
    )
    # 固定现金替代金额已为人民币，仅对按行情估值的证券请求汇率。
    quoted = ~fixed & temp_df["证券数量"].gt(0)
    prices = _quote_prices(quote_symbols.loc[quoted].tolist())
    temp_df["最新价"] = quote_symbols.map(prices).astype(float)
    if (quoted & (temp_df["最新价"].isna() | temp_df["最新价"].le(0))).any():
        missing = quote_symbols.loc[
            quoted & (temp_df["最新价"].isna() | temp_df["最新价"].le(0))
        ]
        raise DataParsingError(f"证券最新行情缺失：{', '.join(missing)}")
    currencies = sorted(set(temp_df.loc[quoted, "币种"]) - {"CNY"})
    fx = _quote_prices([f"wh{currency}CNY" for currency in currencies])
    rates = {"CNY": 1.0}
    for currency in currencies:
        rate = fx.get(f"wh{currency}CNY", float("nan"))
        if pd.isna(rate) or rate <= 0:
            raise DataParsingError(f"{currency}/CNY 汇率缺失")
        rates[currency] = rate
    temp_df["人民币汇率"] = temp_df["币种"].map(rates).astype(float)
    temp_df["市值"] = (
        temp_df["证券数量"]
        * temp_df["最新价"].fillna(0)
        * temp_df["人民币汇率"].fillna(1)
    ).where(~fixed, cash)
    temp_df["估值方式"] = fixed.map({True: "现金替代", False: "行情"})
    total = temp_df["市值"].sum()
    if total <= 0:
        raise DataParsingError("证券篮子总市值应大于零")
    temp_df["市值占比"] = temp_df["市值"] / total * 100
    return temp_df.sort_values("市值占比", ascending=False, kind="stable").reset_index(
        drop=True
    )


if __name__ == "__main__":
    print(fund_etf_pcf(symbol="510300"))
    print(fund_etf_holdings_tx(symbol="510300"))
