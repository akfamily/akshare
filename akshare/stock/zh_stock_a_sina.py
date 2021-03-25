# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/1/25 16:28
Desc: 新浪财经-A股-实时行情数据和历史行情数据(包含前复权和后复权因子)
https://finance.sina.com.cn/realstock/company/sh689009/nc.shtml
"""
import re
import json

import demjson
from py_mini_racer import py_mini_racer
import pandas as pd
import requests
from tqdm import tqdm

from akshare.stock.cons import (
    zh_sina_a_stock_payload,
    zh_sina_a_stock_url,
    zh_sina_a_stock_count_url,
    zh_sina_a_stock_hist_url,
    hk_js_decode,
    zh_sina_a_stock_hfq_url,
    zh_sina_a_stock_qfq_url,
    zh_sina_a_stock_amount_url,
)


def _get_zh_a_page_count() -> int:
    """
    所有股票的总页数
    http://vip.stock.finance.sina.com.cn/mkt/#hs_a
    :return: 需要抓取的股票总页数
    :rtype: int
    """
    res = requests.get(zh_sina_a_stock_count_url)
    page_count = int(re.findall(re.compile(r"\d+"), res.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1


def stock_zh_a_spot() -> pd.DataFrame:
    """
    新浪财经-A股获取所有A股的实时行情数据, 重复运行本函数会被新浪暂时封 IP
    http://vip.stock.finance.sina.com.cn/mkt/#qbgg_hk
    :return: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = _get_zh_a_page_count()
    zh_sina_stock_payload_copy = zh_sina_a_stock_payload.copy()
    for page in tqdm(range(1, page_count + 1), desc="Please wait for a moment"):
        zh_sina_stock_payload_copy.update({"page": page})
        r = requests.get(zh_sina_a_stock_url, params=zh_sina_stock_payload_copy)
        data_json = demjson.decode(r.text)
        big_df = big_df.append(pd.DataFrame(data_json), ignore_index=True)
    big_df = big_df.astype(
        {
            "trade": "float",
            "pricechange": "float",
            "changepercent": "float",
            "buy": "float",
            "sell": "float",
            "settlement": "float",
            "open": "float",
            "high": "float",
            "low": "float",
            "volume": "float",
            "amount": "float",
            "per": "float",
            "pb": "float",
            "mktcap": "float",
            "nmc": "float",
            "turnoverratio": "float",
        }
    )
    return big_df


def stock_zh_a_daily(
    symbol: str = "sz000001",
    start_date: str = "19900101",
    end_date: str = "21000118",
    adjust: str = "",
) -> pd.DataFrame:
    """
    新浪财经-A股-个股的历史行情数据, 大量抓取容易封 IP
    https://finance.sina.com.cn/realstock/company/sh689009/nc.shtml
    :param start_date: 20201103; 开始日期
    :type start_date: str
    :param end_date: 20201103; 结束日期
    :type end_date: str
    :param symbol: sh600000
    :type symbol: str
    :param adjust: 默认为空: 返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据; hfq-factor: 返回后复权因子; hfq-factor: 返回前复权因子
    :type adjust: str
    :return: specific data
    :rtype: pandas.DataFrame
    """
    def _fq_factor(method):
        if method == "hfq":
            res = requests.get(zh_sina_a_stock_hfq_url.format(symbol))
            hfq_factor_df = pd.DataFrame(
                eval(res.text.split("=")[1].split("\n")[0])["data"]
            )
            if hfq_factor_df.shape[0] == 0:
                raise ValueError("sina hfq factor not available")
            hfq_factor_df.columns = ["date", "hfq_factor"]
            hfq_factor_df.index = pd.to_datetime(hfq_factor_df.date)
            del hfq_factor_df["date"]
            return hfq_factor_df
        else:
            res = requests.get(zh_sina_a_stock_qfq_url.format(symbol))
            qfq_factor_df = pd.DataFrame(
                eval(res.text.split("=")[1].split("\n")[0])["data"]
            )
            if qfq_factor_df.shape[0] == 0:
                raise ValueError("sina hfq factor not available")
            qfq_factor_df.columns = ["date", "qfq_factor"]
            qfq_factor_df.index = pd.to_datetime(qfq_factor_df.date)
            del qfq_factor_df["date"]
            return qfq_factor_df

    if adjust in ("hfq-factor", "qfq-factor"):
        return _fq_factor(adjust.split("-")[0])

    res = requests.get(zh_sina_a_stock_hist_url.format(symbol))
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(hk_js_decode)
    dict_list = js_code.call(
        "d", res.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["date"]
    data_df = data_df.astype("float")
    r = requests.get(zh_sina_a_stock_amount_url.format(symbol, symbol))
    amount_data_json = demjson.decode(r.text[r.text.find("["): r.text.rfind("]") + 1])
    amount_data_df = pd.DataFrame(amount_data_json)
    amount_data_df.index = pd.to_datetime(amount_data_df.date)
    del amount_data_df["date"]
    temp_df = pd.merge(
        data_df, amount_data_df, left_index=True, right_index=True, how="outer"
    )
    temp_df.fillna(method="ffill", inplace=True)
    temp_df = temp_df.astype(float)
    temp_df["amount"] = temp_df["amount"] * 10000
    temp_df["turnover"] = temp_df["volume"] / temp_df["amount"]
    temp_df.columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "outstanding_share",
        "turnover",
    ]
    if adjust == "":
        temp_df = temp_df[start_date:end_date]
        temp_df.drop_duplicates(subset=["open", "high", "low", "close"], inplace=True)
        temp_df["open"] = round(temp_df["open"], 2)
        temp_df["high"] = round(temp_df["high"], 2)
        temp_df["low"] = round(temp_df["low"], 2)
        temp_df["close"] = round(temp_df["close"], 2)
        temp_df.dropna(inplace=True)
        temp_df.drop_duplicates(inplace=True)
        return temp_df
    if adjust == "hfq":
        res = requests.get(zh_sina_a_stock_hfq_url.format(symbol))
        hfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])["data"]
        )
        hfq_factor_df.columns = ["date", "hfq_factor"]
        hfq_factor_df.index = pd.to_datetime(hfq_factor_df.date)
        del hfq_factor_df["date"]
        temp_df = pd.merge(
            temp_df, hfq_factor_df, left_index=True, right_index=True, how="outer"
        )
        temp_df.fillna(method="ffill", inplace=True)
        temp_df = temp_df.astype(float)
        temp_df.dropna(inplace=True)
        temp_df.drop_duplicates(subset=["open", "high", "low", "close", "volume"], inplace=True)
        temp_df["open"] = temp_df["open"] * temp_df["hfq_factor"]
        temp_df["high"] = temp_df["high"] * temp_df["hfq_factor"]
        temp_df["close"] = temp_df["close"] * temp_df["hfq_factor"]
        temp_df["low"] = temp_df["low"] * temp_df["hfq_factor"]
        temp_df = temp_df.iloc[:, :-1]
        temp_df = temp_df[start_date:end_date]
        temp_df["open"] = round(temp_df["open"], 2)
        temp_df["high"] = round(temp_df["high"], 2)
        temp_df["low"] = round(temp_df["low"], 2)
        temp_df["close"] = round(temp_df["close"], 2)
        temp_df.dropna(inplace=True)
        return temp_df

    if adjust == "qfq":
        res = requests.get(zh_sina_a_stock_qfq_url.format(symbol))
        qfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])["data"]
        )
        qfq_factor_df.columns = ["date", "qfq_factor"]
        qfq_factor_df.index = pd.to_datetime(qfq_factor_df.date)
        del qfq_factor_df["date"]

        temp_df = pd.merge(
            temp_df, qfq_factor_df, left_index=True, right_index=True, how="outer"
        )
        temp_df.fillna(method="ffill", inplace=True)
        temp_df = temp_df.astype(float)
        temp_df.dropna(inplace=True)
        temp_df.drop_duplicates(subset=["open", "high", "low", "close", "volume"], inplace=True)
        temp_df["open"] = temp_df["open"] / temp_df["qfq_factor"]
        temp_df["high"] = temp_df["high"] / temp_df["qfq_factor"]
        temp_df["close"] = temp_df["close"] / temp_df["qfq_factor"]
        temp_df["low"] = temp_df["low"] / temp_df["qfq_factor"]
        temp_df = temp_df.iloc[:, :-1]
        temp_df = temp_df[start_date:end_date]
        temp_df["open"] = round(temp_df["open"], 2)
        temp_df["high"] = round(temp_df["high"], 2)
        temp_df["low"] = round(temp_df["low"], 2)
        temp_df["close"] = round(temp_df["close"], 2)
        temp_df.dropna(inplace=True)
        return temp_df


def stock_zh_a_cdr_daily(
    symbol: str = "sh689009", start_date: str = "19900101", end_date: str = "22201116"
) -> pd.DataFrame:
    """
    新浪财经-A股-CDR个股的历史行情数据, 大量抓取容易封 IP
    # TODO 观察复权情况
    https://finance.sina.com.cn/realstock/company/sh689009/nc.shtml
    :param start_date: 20201103; 开始日期
    :type start_date: str
    :param end_date: 20201103; 结束日期
    :type end_date: str
    :param symbol: sh689009
    :type symbol: str
    :return: specific data
    :rtype: pandas.DataFrame
    """
    res = requests.get(zh_sina_a_stock_hist_url.format(symbol))
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(hk_js_decode)
    dict_list = js_code.call(
        "d", res.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["date"]
    data_df = data_df.astype("float")
    temp_df = data_df[start_date:end_date]
    temp_df["open"] = round(temp_df["open"], 2)
    temp_df["high"] = round(temp_df["high"], 2)
    temp_df["low"] = round(temp_df["low"], 2)
    temp_df["close"] = round(temp_df["close"], 2)
    return temp_df


def stock_zh_a_minute(
    symbol: str = "sh600751", period: str = "5", adjust: str = ""
) -> pd.DataFrame:
    """
    股票及股票指数历史行情数据-分钟数据
    http://finance.sina.com.cn/realstock/company/sh600519/nc.shtml
    :param symbol: sh000300
    :type symbol: str
    :param period: 1, 5, 15, 30, 60 分钟的数据
    :type period: str
    :param adjust: 默认为空: 返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据;
    :type adjust: str
    :return: specific data
    :rtype: pandas.DataFrame
    """
    url = (
        "https://quotes.sina.cn/cn/api/jsonp_v2.php/=/CN_MarketDataService.getKLineData"
    )
    params = {
        "symbol": symbol,
        "scale": period,
        "datalen": "20000",
    }
    r = requests.get(url, params=params)
    temp_df = pd.DataFrame(json.loads(r.text.split("=(")[1].split(");")[0])).iloc[:, :6]

    if temp_df.empty:
        print(f"{symbol} 股票数据不存在，请检查是否已退市")
        return None

    try:
        stock_zh_a_daily(symbol=symbol, adjust="qfq")
    except:
        return temp_df

    if adjust == "":
        return temp_df

    if adjust == "qfq":
        temp_df[["date", "time"]] = temp_df["day"].str.split(" ", expand=True)
        need_df = temp_df[temp_df["time"] == "15:00:00"]
        need_df.index = pd.to_datetime(need_df["date"])
        stock_zh_a_daily_qfq_df = stock_zh_a_daily(symbol=symbol, adjust="qfq")
        result_df = stock_zh_a_daily_qfq_df.iloc[-len(need_df):, :]["close"].astype(float) / need_df["close"].astype(float)
        temp_df.index = pd.to_datetime(temp_df["date"])
        merged_df = pd.merge(temp_df, result_df, left_index=True, right_index=True)
        merged_df["open"] = merged_df["open"].astype(float) * merged_df["close_y"]
        merged_df["high"] = merged_df["high"].astype(float) * merged_df["close_y"]
        merged_df["low"] = merged_df["low"].astype(float) * merged_df["close_y"]
        merged_df["close"] = merged_df["close_x"].astype(float) * merged_df["close_y"]
        temp_df = merged_df[["day", "open", "high", "low", "close", "volume"]]
        temp_df.reset_index(drop=True, inplace=True)
        return temp_df
    if adjust == "hfq":
        temp_df[["date", "time"]] = temp_df["day"].str.split(" ", expand=True)
        need_df = temp_df[temp_df["time"] == "15:00:00"]
        need_df.index = pd.to_datetime(need_df["date"])
        stock_zh_a_daily_qfq_df = stock_zh_a_daily(symbol=symbol, adjust="hfq")
        result_df = stock_zh_a_daily_qfq_df.iloc[-len(need_df):, :]["close"].astype(
            float
        ) / need_df["close"].astype(float)
        temp_df.index = pd.to_datetime(temp_df["date"])
        merged_df = pd.merge(temp_df, result_df, left_index=True, right_index=True)
        merged_df["open"] = merged_df["open"].astype(float) * merged_df["close_y"]
        merged_df["high"] = merged_df["high"].astype(float) * merged_df["close_y"]
        merged_df["low"] = merged_df["low"].astype(float) * merged_df["close_y"]
        merged_df["close"] = merged_df["close_x"].astype(float) * merged_df["close_y"]
        temp_df = merged_df[["day", "open", "high", "low", "close", "volume"]]
        temp_df.reset_index(drop=True, inplace=True)
        return temp_df


if __name__ == "__main__":
    stock_zh_a_daily_hfq_df_one = stock_zh_a_daily(symbol="sz000592", start_date="20201106", end_date="20201110", adjust="qfq")
    print(stock_zh_a_daily_hfq_df_one)

    stock_zh_a_daily_hfq_df_three = stock_zh_a_daily(symbol="sz000001", start_date="19900103", end_date="20210118", adjust="qfq")
    print(stock_zh_a_daily_hfq_df_three)

    stock_zh_a_daily_hfq_df_two = stock_zh_a_daily(symbol="sz000001", start_date="19900103", end_date="20210118")
    print(stock_zh_a_daily_hfq_df_two)

    qfq_factor_df = stock_zh_a_daily(symbol="sz000001", adjust="hfq-factor")
    print(qfq_factor_df)

    stock_zh_a_daily_hfq_factor_df = stock_zh_a_daily(symbol="sz000002", adjust="hfq-factor")
    print(stock_zh_a_daily_hfq_factor_df)

    stock_zh_a_daily_df = stock_zh_a_daily(symbol="sh601939")
    print(stock_zh_a_daily_df)

    stock_zh_a_cdr_daily_df = stock_zh_a_cdr_daily(
        symbol="sh689009", start_date="20201103", end_date="20201116"
    )
    print(stock_zh_a_cdr_daily_df)

    stock_zh_a_spot_df = stock_zh_a_spot()
    print(stock_zh_a_spot_df)

    stock_zh_a_minute_df = stock_zh_a_minute(symbol="sh600751", period="1", adjust="qfq")
    print(stock_zh_a_minute_df)

    stock_zh_a_cdr_daily_df = stock_zh_a_cdr_daily(symbol="sh689009", start_date="19900101", end_date="22201116")
    print(stock_zh_a_cdr_daily_df)
