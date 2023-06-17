#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/11/12 21:28
Desc: 股票指数数据-新浪-东财-腾讯
所有指数-实时行情数据和历史行情数据
https://finance.sina.com.cn/realstock/company/sz399552/nc.shtml
"""
import datetime
import re

import pandas as pd
import requests
from py_mini_racer import py_mini_racer
from tqdm import tqdm

from akshare.index.cons import (
    zh_sina_index_stock_payload,
    zh_sina_index_stock_url,
    zh_sina_index_stock_count_url,
    zh_sina_index_stock_hist_url,
)
from akshare.stock.cons import hk_js_decode
from akshare.utils import demjson


def _replace_comma(x):
    """
    去除单元格中的 ","
    :param x: 单元格元素
    :type x: str
    :return: 处理后的值或原值
    :rtype: str
    """
    if "," in str(x):
        return str(x).replace(",", "")
    else:
        return x


def get_zh_index_page_count() -> int:
    """
    指数的总页数
    http://vip.stock.finance.sina.com.cn/mkt/#hs_s
    :return: 需要抓取的指数的总页数
    :rtype: int
    """
    res = requests.get(zh_sina_index_stock_count_url)
    page_count = int(re.findall(re.compile(r"\d+"), res.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1


def stock_zh_index_spot() -> pd.DataFrame:
    """
    新浪财经-行情中心首页-A股-分类-所有指数
    大量采集会被目标网站服务器封禁 IP, 如果被封禁 IP, 请 10 分钟后再试
    http://vip.stock.finance.sina.com.cn/mkt/#hs_s
    :return: 所有指数的实时行情数据
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = get_zh_index_page_count()
    zh_sina_stock_payload_copy = zh_sina_index_stock_payload.copy()
    for page in tqdm(range(1, page_count + 1), leave=False):
        zh_sina_stock_payload_copy.update({"page": page})
        res = requests.get(zh_sina_index_stock_url, params=zh_sina_stock_payload_copy)
        data_json = demjson.decode(res.text)
        big_df = pd.concat([big_df, pd.DataFrame(data_json)], ignore_index=True)

    big_df = big_df.applymap(_replace_comma)
    big_df["trade"] = big_df["trade"].astype(float)
    big_df["pricechange"] = big_df["pricechange"].astype(float)
    big_df["changepercent"] = big_df["changepercent"].astype(float)
    big_df["buy"] = big_df["buy"].astype(float)
    big_df["sell"] = big_df["sell"].astype(float)
    big_df["settlement"] = big_df["settlement"].astype(float)
    big_df["open"] = big_df["open"].astype(float)
    big_df["high"] = big_df["high"].astype(float)
    big_df["low"] = big_df["low"].astype(float)
    big_df.columns = [
        "代码",
        "名称",
        "最新价",
        "涨跌额",
        "涨跌幅",
        "_",
        "_",
        "昨收",
        "今开",
        "最高",
        "最低",
        "成交量",
        "成交额",
        "_",
        "_",
    ]
    big_df = big_df[
        [
            "代码",
            "名称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "昨收",
            "今开",
            "最高",
            "最低",
            "成交量",
            "成交额",
        ]
    ]
    return big_df


def stock_zh_index_daily(symbol: str = "sh000922") -> pd.DataFrame:
    """
    新浪财经-指数-历史行情数据, 大量抓取容易封 IP
    https://finance.sina.com.cn/realstock/company/sh000909/nc.shtml
    :param symbol: sz399998, 指定指数代码
    :type symbol: str
    :return: 历史行情数据
    :rtype: pandas.DataFrame
    """
    params = {"d": "2020_2_4"}
    res = requests.get(zh_sina_index_stock_hist_url.format(symbol), params=params)
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(hk_js_decode)
    dict_list = js_code.call(
        "d", res.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    temp_df = pd.DataFrame(dict_list)
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df["open"] = pd.to_numeric(temp_df["open"])
    temp_df["close"] = pd.to_numeric(temp_df["close"])
    temp_df["high"] = pd.to_numeric(temp_df["high"])
    temp_df["low"] = pd.to_numeric(temp_df["low"])
    temp_df["volume"] = pd.to_numeric(temp_df["volume"])
    return temp_df


def _get_tx_start_year(symbol: str = "sh000919") -> pd.DataFrame:
    """
    腾讯证券-获取所有股票数据的第一天, 注意这个数据是腾讯证券的历史数据第一天
    http://gu.qq.com/sh000919/zs
    :param symbol: 带市场标识的股票代码
    :type symbol: str
    :return: 开始日期
    :rtype: pandas.DataFrame
    """
    url = "http://web.ifzq.gtimg.cn/other/klineweb/klineWeb/weekTrends"
    params = {
        "code": symbol,
        "type": "qfq",
        "_var": "trend_qfq",
        "r": "0.3506048543943414",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    if not demjson.decode(data_text[data_text.find("={") + 1 :])["data"]:
        url = "https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get"
        params = {
            "_var": "kline_dayqfq",
            "param": f"{symbol},day,,,320,qfq",
            "r": "0.751892490072597",
        }
        r = requests.get(url, params=params)
        data_text = r.text
        start_date = demjson.decode(data_text[data_text.find("={") + 1 :])["data"][
            symbol
        ]["day"][0][0]
        return start_date
    start_date = demjson.decode(data_text[data_text.find("={") + 1 :])["data"][0][0]
    return start_date


def stock_zh_index_daily_tx(symbol: str = "sz980017") -> pd.DataFrame:
    """
    腾讯证券-日频-股票或者指数历史数据
    作为 stock_zh_index_daily 的补充, 因为在新浪中有部分指数数据缺失
    注意都是: 前复权, 不同网站复权方式不同, 不可混用数据
    http://gu.qq.com/sh000919/zs
    :param symbol: 带市场标识的股票或者指数代码
    :type symbol: str
    :return: 前复权的股票和指数数据
    :rtype: pandas.DataFrame
    """
    start_date = _get_tx_start_year(symbol=symbol)
    url = "https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get"
    range_start = int(start_date.split("-")[0])
    range_end = datetime.date.today().year + 1
    temp_df = pd.DataFrame()
    for year in tqdm(range(range_start, range_end)):
        params = {
            "_var": "kline_dayqfq",
            "param": f"{symbol},day,{year}-01-01,{year + 1}-12-31,640,qfq",
            "r": "0.8205512681390605",
        }
        res = requests.get(url, params=params)
        text = res.text
        try:
            inner_temp_df = pd.DataFrame(
                demjson.decode(text[text.find("={") + 1 :])["data"][symbol]["day"]
            )
        except:
            inner_temp_df = pd.DataFrame(
                demjson.decode(text[text.find("={") + 1 :])["data"][symbol]["qfqday"]
            )
        temp_df = pd.concat([temp_df, inner_temp_df], ignore_index=True)
    if temp_df.shape[1] == 6:
        temp_df.columns = ["date", "open", "close", "high", "low", "amount"]
    else:
        temp_df = temp_df.iloc[:, :6]
        temp_df.columns = ["date", "open", "close", "high", "low", "amount"]
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df["open"] = pd.to_numeric(temp_df["open"])
    temp_df["close"] = pd.to_numeric(temp_df["close"])
    temp_df["high"] = pd.to_numeric(temp_df["high"])
    temp_df["low"] = pd.to_numeric(temp_df["low"])
    temp_df["amount"] = pd.to_numeric(temp_df["amount"])
    temp_df.drop_duplicates(inplace=True, ignore_index=True)
    return temp_df


def stock_zh_index_daily_em(
    symbol: str = "csi931151",
    start_date: str = "19900101",
    end_date: str = "20500101",
) -> pd.DataFrame:
    """
    东方财富网-股票指数数据
    https://quote.eastmoney.com/center/hszs.html
    :param symbol: 带市场标识的指数代码; sz: 深交所, sh: 上交所, csi: 中信指数 + id(000905)
    :type symbol: str
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :return: 指数数据
    :rtype: pandas.DataFrame
    """
    market_map = {"sz": "0", "sh": "1", "csi": "2"}
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    if symbol.find("sz") != -1:
        secid = "{}.{}".format(market_map["sz"], symbol.replace("sz", ""))
    elif symbol.find("sh") != -1:
        secid = "{}.{}".format(market_map["sh"], symbol.replace("sh", ""))
    elif symbol.find("csi") != -1:
        secid = "{}.{}".format(market_map["csi"], symbol.replace("csi", ""))
    else:
        return
    params = {
        "cb": "jQuery1124033485574041163946_1596700547000",
        "secid": secid,
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
        "klt": "101",  # 日频率
        "fqt": "0",
        "beg": start_date,
        "end": end_date,
        "_": "1596700547039",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -2])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
    temp_df.columns = ["date", "open", "close", "high", "low", "volume", "amount", "_"]
    temp_df = temp_df[["date", "open", "close", "high", "low", "volume", "amount"]]

    temp_df["open"] = pd.to_numeric(temp_df["open"], errors="coerce")
    temp_df["close"] = pd.to_numeric(temp_df["close"], errors="coerce")
    temp_df["high"] = pd.to_numeric(temp_df["high"], errors="coerce")
    temp_df["low"] = pd.to_numeric(temp_df["low"], errors="coerce")
    temp_df["volume"] = pd.to_numeric(temp_df["volume"], errors="coerce")
    temp_df["amount"] = pd.to_numeric(temp_df["amount"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    stock_zh_index_daily_df = stock_zh_index_daily(symbol="sz399905")
    print(stock_zh_index_daily_df)

    stock_zh_index_spot_df = stock_zh_index_spot()
    print(stock_zh_index_spot_df)

    stock_zh_index_daily_tx_df = stock_zh_index_daily_tx(symbol="sz000001")
    print(stock_zh_index_daily_tx_df)

    stock_zh_index_daily_em_df = stock_zh_index_daily_em(
        symbol="sz399812", start_date="20220101", end_date="20230606"
    )
    print(stock_zh_index_daily_em_df)
