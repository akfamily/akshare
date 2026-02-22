#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/2/20 10:00
Desc: 期货结算信息
期货交易所结算参数数据
- 中金所: 结算参数(保证金、手续费等) - 已实现
- 郑商所: 结算参数 - 已实现
- 上期所: 结算参数 - 已实现
- 广期所: 结算参数 - 已实现
- 上能中心: 结算参数 - 已实现
- 大商所: 待解决(网站反爬虫保护，所有接口返回412错误)
"""

import datetime

import pandas as pd
import requests
from io import StringIO

from akshare.futures import cons

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36",
}

gfex_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "http://www.gfex.com.cn",
    "Referer": "http://www.gfex.com.cn/gfex/rjycs/ywcs.shtml",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

# 统一的结算参数字段
SETTLE_OUTPUT_COLUMNS = [
    "date",
    "symbol",
    "variety",
    "settle_price",
    "long_margin_ratio",
    "short_margin_ratio",
    "spec_long_margin_ratio",
    "spec_short_margin_ratio",
    "hedge_long_margin_ratio",
    "hedge_short_margin_ratio",
    "trade_fee_ratio",
    "close_today_fee_ratio",
    "delivery_fee_ratio",
    "is_single_market",
    "single_market_days",
    "limit_ratio",
    "position_limit",
    "trade_limit",
    "rise_limit_rate",
    "fall_limit_rate",
]


def _normalize_settle_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    统一结算参数字段，将各交易所的字段映射到统一字段
    :param df: 原始DataFrame
    :type df: pandas.DataFrame
    :return: 统一格式的DataFrame
    :rtype: pandas.DataFrame
    """
    if df.empty:
        return pd.DataFrame(columns=SETTLE_OUTPUT_COLUMNS)

    # 字段映射关系
    field_mapping = {
        # 统一字段 -> 可能的来源字段
        "settle_price": ["settle_price", "SETTLEMENTPRICE", "当日结算价"],
        "long_margin_ratio": ["long_margin_ratio", "margin_ratio", "SPECLONGMARGINRATIO", "specBuyRate", "spec_buy_rate"],
        "short_margin_ratio": ["short_margin_ratio", "SPECSHORTMARGINRATIO", "hedgeBuyRate", "hedge_buy_rate"],
        "spec_long_margin_ratio": ["spec_long_margin_ratio", "SPECLONGMARGINRATIO", "spec_buy_rate"],
        "spec_short_margin_ratio": ["spec_short_margin_ratio", "SPECSHORTMARGINRATIO", "hedge_buy_rate"],
        "hedge_long_margin_ratio": ["hedge_long_margin_ratio", "HEDGLONGMARGINRATIO", "hedge_buy_rate"],
        "hedge_short_margin_ratio": ["hedge_short_margin_ratio", "HEDGSHORTMARGINRATIO", "spec_buy_rate"],
        "trade_fee_ratio": ["trade_fee_ratio", "TRADEFEERATIO", "交易手续费"],
        "close_today_fee_ratio": ["close_today_fee_ratio", "TTRADEFEERATIO", "日内平今仓交易手续费"],
        "delivery_fee_ratio": ["delivery_fee_ratio", "COMMODITYDELIVFEERATIO", "交割手续费"],
        "is_single_market": ["is_single_market", "是否单边市"],
        "single_market_days": ["single_market_days", "连续单边市天数"],
        "limit_ratio": ["limit_ratio", "涨跌停板(%)"],
        "position_limit": ["position_limit", "日持仓限额", "clientBuyPosiQuota", "client_buy_posi_quota"],
        "trade_limit": ["trade_limit", "交易限额"],
        "rise_limit_rate": ["rise_limit_rate", "riseLimitRate", "rise_limit_rate"],
        "fall_limit_rate": ["fall_limit_rate", "fallLimit", "fall_limit"],
    }

    # 确保必要的字段存在
    for col in ["date", "symbol", "variety"]:
        if col not in df.columns:
            if col == "variety" and "symbol" in df.columns:
                df["variety"] = df["symbol"].str.extract(r"([A-Za-z]+)", expand=False)
            else:
                df[col] = None

    # 映射字段
    for target_field, possible_sources in field_mapping.items():
        if target_field not in df.columns:
            for source in possible_sources:
                if source in df.columns:
                    df[target_field] = df[source]
                    break
            else:
                df[target_field] = None

    # 返回统一格式
    return df[SETTLE_OUTPUT_COLUMNS]


def _parse_pipe_data(text: str) -> pd.DataFrame:
    """
    解析管道符分隔的数据
    :param text: 原始文本数据
    :type text: str
    :return: 解析后的DataFrame
    :rtype: pandas.DataFrame
    """
    lines = text.strip().split("\n")
    if len(lines) < 2:
        return pd.DataFrame()
    columns = [col.strip() for col in lines[1].split("|")]
    data_lines = [line for line in lines[2:] if line.strip()]
    data_list = []
    for line in data_lines:
        row = [col.strip() for col in line.split("|")]
        if len(row) >= len(columns):
            data_list.append(row[:len(columns)])
    return pd.DataFrame(data_list, columns=columns)


def get_cffex_settle(date: str = "20260119") -> pd.DataFrame:
    """
    中国金融期货交易所-结算参数
    http://www.cffex.com.cn/jscs/
    :param date: 结算参数日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象，默认为当前交易日
    :type date: str or datetime.date
    :return: 结算参数数据
    :rtype: pandas.DataFrame
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    date = day.strftime("%Y%m%d")
    url = f"http://www.cffex.com.cn/sj/jscs/{date[:4]}{date[4:6]}/{date[6:8]}/{date}_1.csv"
    r = requests.get(url, headers=headers)
    r.encoding = "gbk"
    if r.status_code != 200:
        return pd.DataFrame()
    # 检查是否返回的是 HTML 页面（页面不存在或数据未发布）
    if r.text.strip().startswith("<") or "要查看的页面不存在" in r.text:
        return pd.DataFrame()
    try:
        data_df = pd.read_csv(StringIO(r.text), skiprows=1)
    except:  # noqa: E722
        return pd.DataFrame()
    if data_df.shape[0] < 5:
        return pd.DataFrame()
    data_df.columns = [
        "symbol",
        "long_margin_ratio",
        "short_margin_ratio",
        "trade_fee_ratio",
        "delivery_fee_ratio",
        "close_today_fee_ratio",
    ]
    data_df = data_df[data_df["symbol"].notna()]
    data_df = data_df[data_df["symbol"].str.contains(
        r"^[A-Z]+", na=False, regex=True)]
    data_df["variety"] = data_df["symbol"].str.extract(r"([A-Z]+)")
    data_df["date"] = date
    data_df = data_df[
        ["date", "symbol", "variety", "long_margin_ratio", "short_margin_ratio",
         "trade_fee_ratio", "delivery_fee_ratio", "close_today_fee_ratio"]
    ]
    return data_df


def get_czce_settle(date: str = "20260119") -> pd.DataFrame:
    """
    郑州商品交易所-结算参数
    http://www.czce.com.cn/cn/jysj/jscs/H077003003index_1.htm
    :param date: 结算参数日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象，默认为当前交易日
    :type date: str or datetime.date
    :return: 结算参数数据
    :rtype: pandas.DataFrame
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    date = day.strftime("%Y%m%d")
    url = f"http://www.czce.com.cn/cn/DFSStaticFiles/Future/{date[:4]}/{date}/FutureDataClearParams.txt"
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    if r.status_code != 200:
        return pd.DataFrame()
    try:
        data_df = _parse_pipe_data(r.text)
    except:  # noqa: E722
        return pd.DataFrame()
    if data_df.shape[0] < 5:
        return pd.DataFrame()
    data_df.columns = [
        "symbol", "settle_price", "is_single_market", "single_market_days",
        "margin_ratio", "limit_ratio", "trade_fee", "fee_type",
        "delivery_fee", "close_today_fee", "position_limit", "trade_limit"
    ]
    data_df = data_df[data_df["symbol"].notna()]
    data_df = data_df[~data_df["symbol"].str.contains("小计|合计|总计", na=False)]
    data_df["variety"] = data_df["symbol"].str.extract(r"([A-Za-z]+)")
    data_df["date"] = date
    data_df = data_df[
        ["date", "symbol", "variety", "settle_price", "is_single_market", "single_market_days",
         "margin_ratio", "limit_ratio", "trade_fee", "fee_type", "delivery_fee",
         "close_today_fee", "position_limit", "trade_limit"]
    ]
    return data_df


def get_gfex_settle(date: str = "20260119") -> pd.DataFrame:
    """
    广州期货交易所-结算参数
    http://www.gfex.com.cn/gfex/rjycs/ywcs.shtml
    :param date: 结算参数日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象，默认为当前交易日
    :type date: str or datetime.date
    :return: 结算参数数据
    :rtype: pandas.DataFrame
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    date = day.strftime("%Y%m%d")
    url = "http://www.gfex.com.cn/u/interfacesWebTtQueryTradPara/loadDayList"
    payload = {"trade_type": "0"}
    r = requests.post(url, data=payload, headers=gfex_headers)
    if r.status_code != 200:
        return pd.DataFrame()
    # 检查是否返回了反爬虫的 JavaScript 代码
    if r.text.strip().startswith("<script") or "function" in r.text[:100]:
        return pd.DataFrame()
    try:
        json_data = r.json()
        if json_data.get("code") != "0":
            return pd.DataFrame()
        data_list = json_data.get("data", [])
    except:  # noqa: E722
        return pd.DataFrame()
    if not data_list:
        return pd.DataFrame()
    # 过滤掉期权合约，只保留期货合约
    data_list = [
        item for item in data_list if "-" not in item.get("contractId", "")]
    if not data_list:
        return pd.DataFrame()
    data_df = pd.DataFrame(data_list)
    data_df.columns = [
        "symbol", "spec_buy_rate", "spec_buy", "hedge_buy_rate", "hedge_buy",
        "rise_limit_rate", "rise_limit", "fall_limit", "agent_tot_buy_posi_quota",
        "self_tot_buy_posi_quota", "client_buy_posi_quota", "self_tot_buy_ser_limit",
        "client_buy_ser_limit", "trade_type"
    ]
    data_df["variety"] = data_df["symbol"].str.extract(r"([A-Za-z]+)")
    data_df["date"] = date
    data_df = data_df[
        ["date", "symbol", "variety", "spec_buy_rate", "spec_buy", "hedge_buy_rate",
         "hedge_buy", "rise_limit_rate", "rise_limit", "fall_limit",
         "agent_tot_buy_posi_quota", "self_tot_buy_posi_quota", "client_buy_posi_quota"]
    ]
    return data_df


def get_shfe_settle(date: str = "20260119") -> pd.DataFrame:
    """
    上海期货交易所-结算参数
    https://www.shfe.com.cn/reports/tradedata/dailyandweeklydata/
    :param date: 结算参数日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象，默认为当前交易日
    :type date: str or datetime.date
    :return: 结算参数数据
    :rtype: pandas.DataFrame
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    date = day.strftime("%Y%m%d")
    url = f"https://www.shfe.com.cn/data/tradedata/future/dailydata/js{date}.dat"
    r = requests.get(url, headers=cons.shfe_headers)
    if r.status_code != 200:
        return pd.DataFrame()
    try:
        data_json = r.json()
        data_list = data_json.get("o_cursor", [])
    except:  # noqa: E722
        return pd.DataFrame()
    if not data_list:
        return pd.DataFrame()
    data_df = pd.DataFrame(data_list)
    data_df.columns = [
        "symbol", "trade_fee_ratio", "close_today_fee_ratio", "delivery_fee_unit",
        "spec_long_margin_ratio", "hedge_long_margin_ratio", "delivery_fee_ratio",
        "product_id", "product_name", "close_today_fee_unit", "trade_fee_unit",
        "hedge_short_margin_ratio", "settle_price", "uni_direction",
        "spec_short_margin_ratio", "is_close_today"
    ]
    data_df["variety"] = data_df["symbol"].str.extract(r"([A-Za-z]+)")
    data_df["date"] = date
    data_df = data_df[
        ["date", "symbol", "variety", "settle_price", "spec_long_margin_ratio",
         "hedge_long_margin_ratio", "spec_short_margin_ratio", "hedge_short_margin_ratio",
         "trade_fee_ratio", "close_today_fee_ratio", "is_close_today"]
    ]
    return data_df


def get_ine_settle(date: str = "20260119") -> pd.DataFrame:
    """
    上海国际能源交易中心-结算参数
    https://www.ine.cn/reports/businessdata/prmsummary/
    :param date: 结算参数日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象，默认为当前交易日
    :type date: str or datetime.date
    :return: 结算参数数据
    :rtype: pandas.DataFrame
    """
    day = cons.convert_date(date) if date is not None else datetime.date.today()
    date = day.strftime("%Y%m%d")
    url = f"https://www.ine.cn/data/tradedata/future/dailydata/js{date}.dat"
    r = requests.get(url, headers=cons.shfe_headers)
    if r.status_code != 200:
        return pd.DataFrame()
    try:
        data_json = r.json()
        data_list = data_json.get("o_cursor", [])
    except:  # noqa: E722
        return pd.DataFrame()
    if not data_list:
        return pd.DataFrame()
    data_df = pd.DataFrame(data_list)
    data_df.columns = [
        "symbol", "trade_fee_ratio", "close_today_fee_ratio", "delivery_fee_unit",
        "spec_long_margin_ratio", "hedge_long_margin_ratio", "delivery_fee_ratio",
        "product_id", "product_name", "close_today_fee_unit", "trade_fee_unit",
        "hedge_short_margin_ratio", "settle_price", "uni_direction",
        "spec_short_margin_ratio", "is_close_today"
    ]
    data_df["variety"] = data_df["symbol"].str.extract(r"([A-Za-z]+)")
    data_df["date"] = date
    data_df = data_df[
        ["date", "symbol", "variety", "settle_price", "spec_long_margin_ratio",
         "hedge_long_margin_ratio", "spec_short_margin_ratio", "hedge_short_margin_ratio",
         "trade_fee_ratio", "close_today_fee_ratio", "is_close_today"]
    ]
    return data_df


def get_futures_settle(date: str = "20260119", market: str = "CFFEX") -> pd.DataFrame:
    """
    期货交易所结算参数
    :param date: 结算日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象，默认为当前交易日
    :type date: str or datetime.date
    :param market: 交易所代码: CFFEX-中金所, CZCE-郑商所, SHFE-上期所, DCE-大商所, INE-上能中心, GFEX-广期所
    :type market: str
    :return: 结算参数数据（统一格式）
    :rtype: pandas.DataFrame
    """
    if market.upper() == "CFFEX":
        df = get_cffex_settle(date)
    elif market.upper() == "CZCE":
        df = get_czce_settle(date)
    elif market.upper() == "SHFE":
        df = get_shfe_settle(date)
    elif market.upper() == "GFEX":
        df = get_gfex_settle(date)
    elif market.upper() == "INE":
        df = get_ine_settle(date)
    else:
        print(f"Unsupported market: {market}")
        return pd.DataFrame(columns=SETTLE_OUTPUT_COLUMNS)
    return _normalize_settle_columns(df)


if __name__ == "__main__":
    get_cffex_settle_df = get_cffex_settle(date="20260119")
    print("=== 中金所结算参数 ===")
    print(get_cffex_settle_df)

    get_czce_settle_df = get_czce_settle(date="20260119")
    print("\n=== 郑商所结算参数 ===")
    print(get_czce_settle_df)

    get_shfe_settle_df = get_shfe_settle(date="20260119")
    print("\n=== 上期所结算参数 ===")
    print(get_shfe_settle_df)

    get_gfex_settle_df = get_gfex_settle(date="20260119")
    print("\n=== 广期所结算参数 ===")
    print(get_gfex_settle_df)

    get_ine_settle_df = get_ine_settle(date="20250117")
    print("\n=== 上能中心结算参数 ===")
    print(get_ine_settle_df)

    get_futures_settle_df = get_futures_settle(date="20260119", market="CFFEX")
    print("\n=== 通用接口-CFFEX ===")
    print(get_futures_settle_df)

    get_futures_settle_df = get_futures_settle(date="20260119", market="CZCE")
    print("\n=== 通用接口-CZCE ===")
    print(get_futures_settle_df)

    get_futures_settle_df = get_futures_settle(date="20260119", market="SHFE")
    print("\n=== 通用接口-SHFE ===")
    print(get_futures_settle_df)

    get_futures_settle_df = get_futures_settle(date="20260119", market="GFEX")
    print("\n=== 通用接口-GFEX ===")
    print(get_futures_settle_df)

    get_futures_settle_df = get_futures_settle(date="20260119", market="INE")
    print("\n=== 通用接口-INE ===")
    print(get_futures_settle_df)
