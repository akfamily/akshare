#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/4/21 14:19
Desc: 百度股市通-热搜股票
https://gushitong.baidu.com/expressnews
"""

import pandas as pd
import requests
from datetime import datetime


def stock_hot_search_baidu(
    symbol: str = "A股", date: str = "20240929", time: str = "今日"
):
    """
    百度股市通-热搜股票
    https://gushitong.baidu.com/expressnews
    https://gushitong.baidu.com/
    :param symbol: choice of {"全部", "A股", "港股", "美股"}
    :type symbol: str
    :param date: 日期
    :type date: str
    :param time: time="今日"；choice of {"今日", "1小时"}
    :type time: str
    :return: 热搜股票
    :rtype: pandas.DataFrame
    """
    hour_str = datetime.now().hour
    symbol_map = {
        "全市场": "all",
        "A股": "ab",
        "港股": "hk",
        "美股": "us",
    }
    url = "https://finance.pae.baidu.com/selfselect/listsugrecomm"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "PostmanRuntime-ApipostRuntime/1.1.0",
        "Connection": "keep-alive",
        "Cookie": "BAIDUID=27174CD808467DD509B95DF001F5D236%3AFG%3D1;BAIDUID=39D7691FB31E844E631F9FA97F6DC18E%3AFG%3D1",
        "Cache-Control": "no-cache",
        "Host": "finance.pae.baidu.com"
    }
    params = {
        "tn": "wisexmlnew",
        "dsp": "iphone",
        "product": "search",
        "style": "tablelist",
        "market": symbol_map[symbol],
        "type": "hour",
        "day": date,
        "hour": hour_str,
        "pn": "0",
        "rn": "12",
        "finClientType": "pc",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(
        data_json["Result"]['list']["body"], columns=data_json["Result"]['list']["header"]
    )
    temp_df["现价"] = pd.to_numeric(temp_df["现价"], errors="coerce")
    temp_df["排名变化"] = pd.to_numeric(temp_df["排名变化"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    stock_hot_search_baidu_df = stock_hot_search_baidu(
        symbol="A股", date="20250610", time="今日"
    )
    print(stock_hot_search_baidu_df)
