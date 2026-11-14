#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/12 14:00
Desc: 新浪财经-国内期货-实时数据获取
https://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_3
P.S. 注意采集速度，容易封禁 IP，如果不能访问请稍后再试
"""

import json
import time
from functools import lru_cache
import warnings

import pandas as pd
import py_mini_racer

from akshare.futures.cons import (
    zh_subscribe_exchange_symbol_url,
    zh_match_main_contract_url,
    zh_match_main_contract_payload,
)
from akshare.exceptions import InvalidParameterError
from akshare.futures.futures_contract_detail import futures_contract_detail
from akshare.utils import jsonish
from akshare.utils import http


@lru_cache()
def futures_symbol_mark() -> pd.DataFrame:
    """
    期货的品种和代码映射
    https://vip.stock.finance.sina.com.cn/quotes_service/view/js/qihuohangqing.js
    :return: 期货的品种和代码映射
    :rtype: pandas.DataFrame
    """
    url = (
        "https://vip.stock.finance.sina.com.cn/quotes_service/view/js/qihuohangqing.js"
    )
    r = http.get(url)
    r.encoding = "gb2312"
    data_text = r.text
    raw_json = data_text[data_text.find("{") : data_text.find("}") + 1]
    data_json = jsonish.loads(raw_json)
    czce_mark_list = [item[1] for item in data_json["czce"][1:]]
    dce_mark_list = [item[1] for item in data_json["dce"][1:]]
    shfe_mark_list = [item[1] for item in data_json["shfe"][1:]]
    cffex_mark_list = [item[1] for item in data_json["cffex"][1:]]
    gfex_mark_list = [item[1] for item in data_json["gfex"][1:]]
    all_mark_list = (
        czce_mark_list
        + dce_mark_list
        + shfe_mark_list
        + cffex_mark_list
        + gfex_mark_list
    )

    czce_market_name_list = [data_json["czce"][0]] * len(czce_mark_list)
    dce_market_name_list = [data_json["dce"][0]] * len(dce_mark_list)
    shfe_market_name_list = [data_json["shfe"][0]] * len(shfe_mark_list)
    cffex_market_name_list = [data_json["cffex"][0]] * len(cffex_mark_list)
    gfex_market_name_list = [data_json["gfex"][0]] * len(gfex_mark_list)
    all_market_name_list = (
        czce_market_name_list
        + dce_market_name_list
        + shfe_market_name_list
        + cffex_market_name_list
        + gfex_market_name_list
    )

    czce_symbol_list = [item[0] for item in data_json["czce"][1:]]
    dce_symbol_list = [item[0] for item in data_json["dce"][1:]]
    shfe_symbol_list = [item[0] for item in data_json["shfe"][1:]]
    cffex_symbol_list = [item[0] for item in data_json["cffex"][1:]]
    gfex_symbol_list = [item[0] for item in data_json["gfex"][1:]]
    all_symbol_list = (
        czce_symbol_list
        + dce_symbol_list
        + shfe_symbol_list
        + cffex_symbol_list
        + gfex_symbol_list
    )

    temp_df = pd.DataFrame([all_market_name_list, all_symbol_list, all_mark_list]).T
    temp_df.columns = [
        "exchange",
        "symbol",
        "mark",
    ]
    return temp_df


def futures_zh_realtime_sina(symbol: str = "PTA") -> pd.DataFrame:
    """
    期货品种当前时刻所有可交易的合约实时数据
    https://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1
    :param symbol: 品种名称；可以通过 ak.futures_symbol_mark() 获取所有品种命名表
    :type symbol: str
    :return: 期货品种当前时刻所有可交易的合约实时数据
    :rtype: pandas.DataFrame
    """
    _futures_symbol_mark_df = futures_symbol_mark()
    symbol_mark_map = dict(
        zip(_futures_symbol_mark_df["symbol"], _futures_symbol_mark_df["mark"])
    )
    url = "https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQFuturesData"
    params = {
        "page": "1",
        "sort": "position",
        "asc": "0",
        "node": symbol_mark_map[symbol],
        "base": "futures",
    }
    r = http.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)

    temp_df["trade"] = pd.to_numeric(temp_df["trade"], errors="coerce")
    temp_df["settlement"] = pd.to_numeric(temp_df["settlement"], errors="coerce")
    temp_df["presettlement"] = pd.to_numeric(temp_df["presettlement"], errors="coerce")
    temp_df["open"] = pd.to_numeric(temp_df["open"], errors="coerce")
    temp_df["high"] = pd.to_numeric(temp_df["high"], errors="coerce")
    temp_df["low"] = pd.to_numeric(temp_df["low"], errors="coerce")
    temp_df["close"] = pd.to_numeric(temp_df["close"], errors="coerce")
    temp_df["bidprice1"] = pd.to_numeric(temp_df["bidprice1"], errors="coerce")
    temp_df["askprice1"] = pd.to_numeric(temp_df["askprice1"], errors="coerce")
    temp_df["bidvol1"] = pd.to_numeric(temp_df["bidvol1"], errors="coerce")
    temp_df["askvol1"] = pd.to_numeric(temp_df["askvol1"], errors="coerce")
    temp_df["volume"] = pd.to_numeric(temp_df["volume"], errors="coerce")
    temp_df["position"] = pd.to_numeric(temp_df["position"], errors="coerce")
    temp_df["preclose"] = pd.to_numeric(temp_df["preclose"], errors="coerce")
    temp_df["changepercent"] = pd.to_numeric(temp_df["changepercent"], errors="coerce")
    temp_df["bid"] = pd.to_numeric(temp_df["bid"], errors="coerce")
    temp_df["ask"] = pd.to_numeric(temp_df["ask"], errors="coerce")
    temp_df["prevsettlement"] = pd.to_numeric(
        temp_df["prevsettlement"], errors="coerce"
    )
    return temp_df


def zh_subscribe_exchange_symbol(symbol: str = "cffex") -> pd.DataFrame:
    """
    交易所具体的可交易品种
    https://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1
    :param symbol: choice of {'czce', 'dce', 'shfe', 'cffex', 'gfex'}
    :type symbol: str
    :return: 交易所具体的可交易品种
    :rtype: dict
    """
    r = http.get(zh_subscribe_exchange_symbol_url)
    r.encoding = "gbk"
    data_text = r.text
    data_json = jsonish.loads(data_text[data_text.find("{") : data_text.find("};") + 1])
    # 各交易所的首个元素是交易所名称；部分品种多一个字段，按最长的行补齐
    row_list = [item for item in data_json[symbol] if isinstance(item, list)]
    width = max(len(item) for item in row_list)
    return pd.DataFrame([item + [None] * (width - len(item)) for item in row_list])


def _pick_main_contract(data_df: pd.DataFrame) -> str | None:
    """
    从某个品种的合约行情中选出主力合约
    新浪以“连续”行（如 PS0）镜像主力合约，取与其字段一致最多的真实合约；
    没有“连续”行的品种（如 10 年期国债期货）取持仓量最大的合约
    :param data_df: 某个品种的合约行情，已剔除停止交易的合约
    :type data_df: pandas.DataFrame
    :return: 主力合约代码，没有真实合约时返回 None
    :rtype: str | None
    """
    is_continuous = data_df["symbol"].str.fullmatch(r"[A-Za-z]+0")
    real_df = data_df[~is_continuous]
    if real_df.empty:
        return None
    if is_continuous.any():
        continuous = data_df[is_continuous].iloc[0]
        field_list = [
            item
            for item in data_df.columns
            if item not in ("symbol", "exchange", "name")
        ]
        score = real_df[field_list].eq(continuous[field_list]).sum(axis=1)
        return real_df.loc[score.idxmax(), "symbol"]
    position = pd.to_numeric(real_df["position"], errors="coerce").fillna(0)
    return real_df.loc[position.idxmax(), "symbol"]


def futures_main_contract_sina(symbol: str = "cffex") -> str:
    """
    新浪财经-期货-主力合约
    https://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1
    :param symbol: choice of {'czce', 'dce', 'shfe', 'cffex', 'gfex'}
    :type symbol: str
    :return: 主力合约的字符串
    :rtype: str
    """
    exchange_symbol_list = zh_subscribe_exchange_symbol(symbol).iloc[:, 1].tolist()
    data_dict = {}
    for item in exchange_symbol_list:
        payload = {**zh_match_main_contract_payload, "node": item}
        res = http.get(zh_match_main_contract_url, params=payload)
        data_df = pd.DataFrame(jsonish.loads(res.text))
        if data_df.empty or "symbol" not in data_df.columns:
            warnings.warn(f"{item} 无主力合约")
            continue
        data_df["tradedate"] = pd.to_datetime(data_df["tradedate"], errors="coerce")
        data_dict[item] = data_df
    if not data_dict:
        return ""
    # 已停止交易的品种（如动力煤、强麦）仍会返回数年前的行情，按交易日期剔除
    latest_date = max(item["tradedate"].max() for item in data_dict.values())
    subscribe_exchange_list = []
    for item, data_df in data_dict.items():
        data_df = data_df[data_df["tradedate"] >= latest_date - pd.Timedelta(days=30)]
        if data_df.empty:
            continue
        main_contract = _pick_main_contract(data_df)
        if main_contract is None:
            warnings.warn(f"{item} 无主力合约")
            continue
        subscribe_exchange_list.append(main_contract)
    return ",".join(subscribe_exchange_list)


def futures_zh_contract_realtime_sina(
    symbol: str = "V2701",
    market: str = "CF",
    adjust: str = "0",
) -> pd.DataFrame:
    """
    期货的实时行情数据
    https://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1
    :param symbol: 合约名称的字符串组合
    :type symbol: str
    :param market: CF 为商品期货
    :type market: str
    :param adjust: '1' or '0'；字符串的 0 或 1；返回合约、交易所和最小变动单位的实时数据，返回数据会变慢
    :type adjust: str
    :return: 期货的实时行情数据
    :rtype: pandas.DataFrame
    """
    file_data = "Math.round(Math.random() * 2147483648).toString(16)"
    ctx = py_mini_racer.MiniRacer()
    rn_code = ctx.eval(file_data)
    subscribe_list = ",".join(["nf_" + item.strip() for item in symbol.split(",")])
    url = f"https://hq.sinajs.cn/rn={rn_code}&list={subscribe_list}"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Host": "hq.sinajs.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "https://vip.stock.finance.sina.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/97.0.4692.71 Safari/537.36",
    }
    r = http.get(url, headers=headers)
    data_df = pd.DataFrame(
        [
            item.strip().split("=")[1].split(",")
            for item in r.text.split(";")
            if item.strip() != ""
        ]
    )
    if data_df.shape[1] <= 1:
        # 新浪对无效或已到期的合约返回空字符串，此时只解析出一列
        raise InvalidParameterError(
            f"新浪没有返回合约 {symbol} 的行情，请检查合约代码是否有效、是否已到期"
        )
    data_df.iloc[:, 0] = data_df.iloc[:, 0].str.replace('"', "")
    data_df.iloc[:, -1] = data_df.iloc[:, -1].str.replace('"', "")
    if adjust == "1":
        contract_name_list = [item.split("_")[1] for item in subscribe_list.split(",")]
        contract_min_list = []
        contract_exchange_list = []
        for contract_name in contract_name_list:
            temp_df = futures_contract_detail(symbol=contract_name)
            exchange_name = temp_df[temp_df["item"] == "上市交易所"]["value"].values[0]
            contract_exchange_list.append(exchange_name)
            contract_min = temp_df[temp_df["item"] == "最小变动价位"]["value"].values[0]
            contract_min_list.append(contract_min)
        if market == "CF":
            data_df.columns = [
                "symbol",
                "time",
                "open",
                "high",
                "low",
                "last_close",
                "bid_price",
                "ask_price",
                "current_price",
                "avg_price",
                "last_settle_price",
                "buy_vol",
                "sell_vol",
                "hold",
                "volume",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
            ]
            data_df = data_df[
                [
                    "symbol",
                    "time",
                    "open",
                    "high",
                    "low",
                    "current_price",
                    "bid_price",
                    "ask_price",
                    "buy_vol",
                    "sell_vol",
                    "hold",
                    "volume",
                    "avg_price",
                    "last_close",
                    "last_settle_price",
                ]
            ]
            data_df["exchange"] = contract_exchange_list
            data_df["contract"] = contract_name_list
            data_df["contract_min_change"] = contract_min_list

            data_df["open"] = pd.to_numeric(data_df["open"], errors="coerce")
            data_df["high"] = pd.to_numeric(data_df["high"], errors="coerce")
            data_df["low"] = pd.to_numeric(data_df["low"], errors="coerce")
            data_df["current_price"] = pd.to_numeric(
                data_df["current_price"], errors="coerce"
            )
            data_df["bid_price"] = pd.to_numeric(data_df["bid_price"], errors="coerce")
            data_df["ask_price"] = pd.to_numeric(data_df["ask_price"], errors="coerce")
            data_df["buy_vol"] = pd.to_numeric(data_df["buy_vol"], errors="coerce")
            data_df["sell_vol"] = pd.to_numeric(data_df["sell_vol"], errors="coerce")
            data_df["hold"] = pd.to_numeric(data_df["hold"], errors="coerce")
            data_df["volume"] = pd.to_numeric(data_df["volume"], errors="coerce")
            data_df["avg_price"] = pd.to_numeric(data_df["avg_price"], errors="coerce")
            data_df["last_close"] = pd.to_numeric(
                data_df["last_close"], errors="coerce"
            )
            data_df["last_settle_price"] = pd.to_numeric(
                data_df["last_settle_price"], errors="coerce"
            )
            data_df = data_df.dropna(subset=["current_price"], ignore_index=True)
            return data_df
        else:
            data_df.columns = [
                "open",
                "high",
                "low",
                "current_price",
                "volume",
                "amount",
                "hold",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "__",
                "time",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "symbol",
            ]
            data_df = data_df[
                [
                    "symbol",
                    "time",
                    "open",
                    "high",
                    "low",
                    "current_price",
                    "hold",
                    "volume",
                    "amount",
                ]
            ]
            data_df["exchange"] = contract_exchange_list
            data_df["contract"] = contract_name_list
            data_df["contract_min_change"] = contract_min_list
            data_df["open"] = pd.to_numeric(data_df["open"], errors="coerce")
            data_df["high"] = pd.to_numeric(data_df["high"], errors="coerce")
            data_df["low"] = pd.to_numeric(data_df["low"], errors="coerce")
            data_df["current_price"] = pd.to_numeric(
                data_df["current_price"], errors="coerce"
            )
            data_df["hold"] = pd.to_numeric(data_df["hold"], errors="coerce")
            data_df["volume"] = pd.to_numeric(data_df["volume"], errors="coerce")
            data_df["amount"] = pd.to_numeric(data_df["amount"], errors="coerce")
            data_df = data_df.dropna(subset=["current_price"], ignore_index=True)
            return data_df
    else:
        if market == "CF":
            # 此处由于 20220601 接口变动，增加了字段，此处增加异常判断，except 后为新代码
            try:
                data_df.columns = [
                    "symbol",
                    "time",
                    "open",
                    "high",
                    "low",
                    "last_close",
                    "bid_price",
                    "ask_price",
                    "current_price",
                    "avg_price",
                    "last_settle_price",
                    "buy_vol",
                    "sell_vol",
                    "hold",
                    "volume",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                ]
            except Exception:
                data_df.columns = [
                    "symbol",
                    "time",
                    "open",
                    "high",
                    "low",
                    "last_close",
                    "bid_price",
                    "ask_price",
                    "current_price",
                    "avg_price",
                    "last_settle_price",
                    "buy_vol",
                    "sell_vol",
                    "hold",
                    "volume",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                    "_",
                ]
            data_df = data_df[
                [
                    "symbol",
                    "time",
                    "open",
                    "high",
                    "low",
                    "current_price",
                    "bid_price",
                    "ask_price",
                    "buy_vol",
                    "sell_vol",
                    "hold",
                    "volume",
                    "avg_price",
                    "last_close",
                    "last_settle_price",
                ]
            ]

            data_df["open"] = pd.to_numeric(data_df["open"], errors="coerce")
            data_df["high"] = pd.to_numeric(data_df["high"], errors="coerce")
            data_df["low"] = pd.to_numeric(data_df["low"], errors="coerce")
            data_df["current_price"] = pd.to_numeric(
                data_df["current_price"], errors="coerce"
            )
            data_df["bid_price"] = pd.to_numeric(data_df["bid_price"], errors="coerce")
            data_df["ask_price"] = pd.to_numeric(data_df["ask_price"], errors="coerce")
            data_df["buy_vol"] = pd.to_numeric(data_df["buy_vol"], errors="coerce")
            data_df["sell_vol"] = pd.to_numeric(data_df["sell_vol"], errors="coerce")
            data_df["hold"] = pd.to_numeric(data_df["hold"], errors="coerce")
            data_df["volume"] = pd.to_numeric(data_df["volume"], errors="coerce")
            data_df["avg_price"] = pd.to_numeric(data_df["avg_price"], errors="coerce")
            data_df["last_close"] = pd.to_numeric(
                data_df["last_close"], errors="coerce"
            )
            data_df["last_settle_price"] = pd.to_numeric(
                data_df["last_settle_price"], errors="coerce"
            )
            data_df = data_df.dropna(subset=["current_price"], ignore_index=True)
            return data_df
        else:
            data_df.columns = [
                "open",
                "high",
                "low",
                "current_price",
                "volume",
                "amount",
                "hold",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "__",
                "time",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "symbol",
            ]
            data_df = data_df[
                [
                    "symbol",
                    "time",
                    "open",
                    "high",
                    "low",
                    "current_price",
                    "hold",
                    "volume",
                    "amount",
                ]
            ]
            data_df["open"] = pd.to_numeric(data_df["open"], errors="coerce")
            data_df["high"] = pd.to_numeric(data_df["high"], errors="coerce")
            data_df["low"] = pd.to_numeric(data_df["low"], errors="coerce")
            data_df["current_price"] = pd.to_numeric(
                data_df["current_price"], errors="coerce"
            )
            data_df["hold"] = pd.to_numeric(data_df["hold"], errors="coerce")
            data_df["volume"] = pd.to_numeric(data_df["volume"], errors="coerce")
            data_df["amount"] = pd.to_numeric(data_df["amount"], errors="coerce")
            data_df = data_df.dropna(subset=["current_price"], ignore_index=True)
            return data_df


def futures_zh_min_sina(symbol: str = "IF2008", period: str = "1") -> pd.DataFrame:
    """
    中国各品种期货分钟频率数据
    https://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_3
    :param symbol: 可以通过 futures_main_contract_sina(symbol="cffex") 获取，或者访问网页获取
    :type symbol: str
    :param period: choice of {"1": "1分钟", "5": "5分钟", "15": "15分钟", "30": "30分钟", "60": "60分钟"}
    :type period: str
    :return: 指定 symbol 和 period 的数据
    :rtype: pandas.DataFrame
    """
    url = "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/=/InnerFuturesNewService.getFewMinLine"
    params = {
        "symbol": symbol,
        "type": period,
    }
    r = http.get(url, params=params)
    temp_df = pd.DataFrame(json.loads(r.text.split("=(")[1].split(");")[0]))
    temp_df = temp_df.rename(
        columns={
            "d": "datetime",
            "o": "open",
            "h": "high",
            "l": "low",
            "c": "close",
            "v": "volume",
            "p": "hold",
        }
    )
    temp_df = temp_df[["datetime", "open", "high", "low", "close", "volume", "hold"]]
    temp_df["open"] = pd.to_numeric(temp_df["open"], errors="coerce")
    temp_df["high"] = pd.to_numeric(temp_df["high"], errors="coerce")
    temp_df["low"] = pd.to_numeric(temp_df["low"], errors="coerce")
    temp_df["close"] = pd.to_numeric(temp_df["close"], errors="coerce")
    temp_df["volume"] = pd.to_numeric(temp_df["volume"], errors="coerce")
    temp_df["hold"] = pd.to_numeric(temp_df["hold"], errors="coerce")
    return temp_df


def futures_zh_daily_sina(symbol: str = "RB0") -> pd.DataFrame:
    """
    中国各品种期货日频率数据
    https://finance.sina.com.cn/futures/quotes/V2105.shtml
    :param symbol: 可以通过 futures_main_contract_sina(symbol="cffex") 获取，或者访问网页获取
    :type symbol: str
    :return: 指定 symbol 的数据
    :rtype: pandas.DataFrame
    """
    date = "20210412"
    url = (
        "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_V21052021_4_12="
        "/InnerFuturesNewService.getDailyKLine"
    )
    params = {
        "symbol": symbol,
        "type": "_".join([date[:4], date[4:6], date[6:]]),
    }
    r = http.get(url, params=params)
    temp_df = pd.DataFrame(json.loads(r.text.split("=(")[1].split(");")[0]))
    temp_df = temp_df.rename(
        columns={
            "d": "date",
            "o": "open",
            "h": "high",
            "l": "low",
            "c": "close",
            "v": "volume",
            "p": "hold",
            "s": "settle",
        }
    )
    temp_df = temp_df[
        ["date", "open", "high", "low", "close", "volume", "hold", "settle"]
    ]
    temp_df["open"] = pd.to_numeric(temp_df["open"], errors="coerce")
    temp_df["high"] = pd.to_numeric(temp_df["high"], errors="coerce")
    temp_df["low"] = pd.to_numeric(temp_df["low"], errors="coerce")
    temp_df["close"] = pd.to_numeric(temp_df["close"], errors="coerce")
    temp_df["volume"] = pd.to_numeric(temp_df["volume"], errors="coerce")
    temp_df["hold"] = pd.to_numeric(temp_df["hold"], errors="coerce")
    temp_df["settle"] = pd.to_numeric(temp_df["settle"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    futures_main_contract_sina_df = futures_main_contract_sina(symbol="gfex")
    print(futures_main_contract_sina_df)

    futures_zh_contract_realtime_sina_df = futures_zh_contract_realtime_sina(
        symbol="V2701,V2705", market="CF", adjust="0"
    )
    print(futures_zh_contract_realtime_sina_df)

    futures_zh_contract_realtime_sina_df = futures_zh_contract_realtime_sina(
        symbol="V2701", market="CF", adjust="0"
    )
    print(futures_zh_contract_realtime_sina_df)

    futures_symbol_mark_df = futures_symbol_mark()
    print(futures_symbol_mark_df)

    futures_zh_realtime_sina_df = futures_zh_realtime_sina(symbol="工业硅")
    print(futures_zh_realtime_sina_df)

    futures_zh_min_sina_df = futures_zh_min_sina(symbol="RB0", period="1")
    print(futures_zh_min_sina_df)

    futures_zh_daily_sina_df = futures_zh_daily_sina(symbol="RB0")
    print(futures_zh_daily_sina_df)

    futures_zh_daily_sina_df = futures_zh_daily_sina(symbol="RB2410")
    print(futures_zh_daily_sina_df)

    dce_text = futures_main_contract_sina(symbol="dce")
    czce_text = futures_main_contract_sina(symbol="czce")
    shfe_text = futures_main_contract_sina(symbol="shfe")
    gfex_text = futures_main_contract_sina(symbol="gfex")

    while True:
        time.sleep(3)
        futures_zh_contract_realtime_sina_df = futures_zh_contract_realtime_sina(
            symbol=",".join([dce_text, czce_text, shfe_text, gfex_text]),
            market="CF",
            adjust="0",
        )
        print(futures_zh_contract_realtime_sina_df)
