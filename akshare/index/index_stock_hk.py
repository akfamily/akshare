#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/5/10 18:00
Desc: 股票指数数据-新浪-东财
所有指数-实时行情数据和历史行情数据
https://finance.sina.com.cn/realstock/company/sz399552/nc.shtml
"""
import re

import pandas as pd
import requests
from py_mini_racer import py_mini_racer

from akshare.index.cons import (
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


def get_hk_index_page_count() -> int:
    """
    指数的总页数
    https://vip.stock.finance.sina.com.cn/mkt/#zs_hk
    :return: 需要抓取的指数的总页数
    :rtype: int
    """
    res = requests.get("https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getNameCount?node=zs_hk")
    page_count = int(re.findall(re.compile(r"\d+"), res.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1


def stock_hk_index_spot() -> pd.DataFrame:
    """
    新浪财经-行情中心首页-港股-分类-所有指数
    大量采集会被目标网站服务器封禁 IP, 如果被封禁 IP, 请 10 分钟后再试
    https://vip.stock.finance.sina.com.cn/mkt/#zs_hk
    :return: 所有指数的实时行情数据
    :rtype: pandas.DataFrame
    """
    url = "https://hq.sinajs.cn/rn=mtf2t&list=hkCES100,hkCES120,hkCES280,hkCES300,hkCESA80,hkCESG10,hkCESHKM,hkCSCMC,hkCSHK100,hkCSHKDIV,hkCSHKLC,hkCSHKLRE,hkCSHKMCS,hkCSHKME,hkCSHKPE,hkCSHKSE,hkCSI300,hkCSRHK50,hkGEM,hkHKL,hkHSCCI,hkHSCEI,hkHSI,hkHSMBI,hkHSMOGI,hkHSMPI,hkHSTECH,hkSSE180,hkSSE180GV,hkSSE380,hkSSE50,hkSSECEQT,hkSSECOMP,hkSSEDIV,hkSSEITOP,hkSSEMCAP,hkSSEMEGA,hkVHSI"
    headers = {
        "Referer": "https://vip.stock.finance.sina.com.cn/"
    }
    r = requests.get(url, headers=headers)
    data_text = r.text
    data_list = [item.split('"')[1].split(",") for item in data_text.split("\n") if len(item.split('"')) > 1]
    temp_df = pd.DataFrame(data_list)
    temp_df.columns = [
        "代码",
        "名称",
        "今开",
        "昨收",
        "最高",
        "最低",
        "最新价",
        "涨跌额",
        "涨跌幅",
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
    temp_df = temp_df[
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
        ]
    ]
    temp_df['最新价'] = pd.to_numeric(temp_df['最新价'], errors="coerce")
    temp_df['涨跌额'] = pd.to_numeric(temp_df['涨跌额'], errors="coerce")
    temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'], errors="coerce")
    temp_df['昨收'] = pd.to_numeric(temp_df['昨收'], errors="coerce")
    temp_df['今开'] = pd.to_numeric(temp_df['今开'], errors="coerce")
    temp_df['最高'] = pd.to_numeric(temp_df['最高'], errors="coerce")
    temp_df['最低'] = pd.to_numeric(temp_df['最低'], errors="coerce")
    return temp_df


def stock_hk_index_daily(symbol: str = "sh000922") -> pd.DataFrame:
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


def stock_hk_index_daily_em(symbol: str = "sh000913") -> pd.DataFrame:
    """
    东方财富网-股票指数数据
    https://quote.eastmoney.com/center/hszs.html
    :param symbol: 带市场标识的指数代码
    :type symbol: str
    :return: 指数数据
    :rtype: pandas.DataFrame
    """
    market_map = {"sz": "0", "sh": "1"}
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "cb": "jQuery1124033485574041163946_1596700547000",
        "secid": f"{market_map[symbol[:2]]}.{symbol[2:]}",
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
        "klt": "101",  # 日频率
        "fqt": "0",
        "beg": "19900101",
        "end": "20320101",
        "_": "1596700547039",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -2])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
    temp_df.columns = ["date", "open", "close", "high", "low", "volume", "amount", "_"]
    temp_df = temp_df[["date", "open", "close", "high", "low", "volume", "amount"]]

    temp_df["open"] = pd.to_numeric(temp_df["open"])
    temp_df["close"] = pd.to_numeric(temp_df["close"])
    temp_df["high"] = pd.to_numeric(temp_df["high"])
    temp_df["low"] = pd.to_numeric(temp_df["low"])
    temp_df["volume"] = pd.to_numeric(temp_df["volume"])
    temp_df["amount"] = pd.to_numeric(temp_df["amount"])
    return temp_df


if __name__ == "__main__":
    stock_zh_index_daily_df = stock_hk_index_daily(symbol="sz399905")
    print(stock_zh_index_daily_df)

    stock_zh_index_spot_df = stock_hk_index_spot()
    print(stock_zh_index_spot_df)

    stock_zh_index_daily_em_df = stock_hk_index_daily_em(symbol="sz399812")
    print(stock_zh_index_daily_em_df)
