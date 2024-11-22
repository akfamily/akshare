#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/11/22 14:00
Desc: 新浪财经-基金行情
https://vip.stock.finance.sina.com.cn/fund_center/index.html#jjhqetf
"""

import pandas as pd
import py_mini_racer
import requests

from akshare.stock.cons import hk_js_decode
from akshare.utils import demjson


def fund_etf_category_sina(symbol: str = "LOF基金") -> pd.DataFrame:
    """
    新浪财经-基金列表
    https://vip.stock.finance.sina.com.cn/fund_center/index.html#jjhqetf
    :param symbol: choice of {"封闭式基金", "ETF基金", "LOF基金"}
    :type symbol: str
    :return: 指定 symbol 的基金列表
    :rtype: pandas.DataFrame
    """
    fund_map = {
        "封闭式基金": "close_fund",
        "ETF基金": "etf_hq_fund",
        "LOF基金": "lof_hq_fund",
    }
    url = (
        "https://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/"
        "IO.XSRV2.CallbackList['da_yPT46_Ll7K6WD']/Market_Center.getHQNodeDataSimple"
    )
    params = {
        "page": "1",
        "num": "5000",
        "sort": "symbol",
        "asc": "0",
        "node": fund_map[symbol],
        "[object HTMLDivElement]": "qvvne",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("([") + 1 : -2])
    temp_df = pd.DataFrame(data_json)
    if symbol == "封闭式基金":
        temp_df.columns = [
            "代码",
            "名称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "买入",
            "卖出",
            "昨收",
            "今开",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "_",
            "_",
        ]
    else:
        temp_df.columns = [
            "代码",
            "名称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "买入",
            "卖出",
            "昨收",
            "今开",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "_",
            "_",
            "_",
            "_",
        ]
    temp_df = temp_df[
        [
            "代码",
            "名称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "买入",
            "卖出",
            "昨收",
            "今开",
            "最高",
            "最低",
            "成交量",
            "成交额",
        ]
    ]
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["买入"] = pd.to_numeric(temp_df["买入"], errors="coerce")
    temp_df["卖出"] = pd.to_numeric(temp_df["卖出"], errors="coerce")
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    return temp_df


def fund_etf_hist_sina(symbol: str = "sh510050") -> pd.DataFrame:
    """
    新浪财经-基金-ETF 基金-日行情数据
    https://finance.sina.com.cn/fund/quotes/159996/bc.shtml
    :param symbol: 基金名称, 可以通过 ak.fund_etf_category_sina() 函数获取
    :type symbol: str
    :return: 日行情数据
    :rtype: pandas.DataFrame
    """
    url = f"https://finance.sina.com.cn/realstock/company/{symbol}/hisdata/klc_kl.js"
    r = requests.get(url)
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(hk_js_decode)
    dict_list = js_code.call(
        "d", r.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    temp_df = pd.DataFrame(dict_list)
    if temp_df.empty:  # 处理获取数据为空的问题
        return pd.DataFrame()
    temp_df["date"] = pd.to_datetime(temp_df["date"], errors="coerce").dt.date
    temp_df["open"] = pd.to_numeric(temp_df["open"], errors="coerce")
    temp_df["high"] = pd.to_numeric(temp_df["high"], errors="coerce")
    temp_df["low"] = pd.to_numeric(temp_df["low"], errors="coerce")
    temp_df["close"] = pd.to_numeric(temp_df["close"], errors="coerce")
    temp_df["volume"] = pd.to_numeric(temp_df["volume"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    fund_etf_category_sina_df = fund_etf_category_sina(symbol="封闭式基金")
    print(fund_etf_category_sina_df)

    fund_etf_category_sina_df = fund_etf_category_sina(symbol="ETF基金")
    print(fund_etf_category_sina_df)

    fund_etf_category_sina_df = fund_etf_category_sina(symbol="LOF基金")
    print(fund_etf_category_sina_df)

    fund_etf_hist_sina_df = fund_etf_hist_sina(symbol="sh510050")
    print(fund_etf_hist_sina_df)

    fund_etf_hist_sina_df = fund_etf_hist_sina(symbol="sh510300")
    print(fund_etf_hist_sina_df)
