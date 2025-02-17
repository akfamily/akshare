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
    :param symbol: choice of {"全部", "A股", "港股", "美股"}
    :type symbol: str
    :param date: 日期
    :type date: str
    :param time: time="今日"；choice of {"今日", "1小时"}
    :type time: str
    :return: 股东人数及持股集中度
    :rtype: pandas.DataFrame
    """
    hour_str = datetime.now().hour
    symbol_map = {
        "全部": "all",
        "A股": "ab",
        "港股": "hk",
        "美股": "us",
    }
    url = "https://finance.pae.baidu.com/vapi/v1/hotrank"
    params = {
        "tn": "wisexmlnew",
        "dsp": "iphone",
        "product": "stock",
        "day": date,
        "hour": hour_str,
        "pn": "0",
        "rn": "1000",
        "market": symbol_map[symbol],
        "type": "day" if time == "今日" else "hour",
        "finClientType": "pc",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(
        data_json["Result"]["body"], columns=data_json["Result"]["header"]
    )
    temp_df["现价"] = pd.to_numeric(temp_df["现价"], errors="coerce")
    temp_df["排名变化"] = pd.to_numeric(temp_df["排名变化"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    stock_hot_search_baidu_df = stock_hot_search_baidu(
        symbol="A股", date="20240929", time="今日"
    )
    print(stock_hot_search_baidu_df)
