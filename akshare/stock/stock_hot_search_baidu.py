#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/10/14 18:19
Desc: 百度股市通-热搜股票
https://gushitong.baidu.com/expressnews
"""
import pandas as pd
import requests


def stock_hot_search_baidu(symbol: str = "A股", date: str = "20221014", time: str = "0"):
    """
    百度股市通-热搜股票
    https://gushitong.baidu.com/expressnews
    :param symbol: choice of {"全部", "A股", "港股", "美股"}
    :type symbol: str
    :param date: 日期
    :type date: str
    :param time: 默认 time=0，则为当天的排行；如 time="16"，则为 date 的 16 点的热门股票排行
    :type time: str
    :return: 股东人数及持股集中度
    :rtype: pandas.DataFrame
    """
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
        "hour": time,
        "pn": "0",
        "rn": "1000",
        "market": symbol_map[symbol],
        "type": "day" if time == 0 else "hour",
        "finClientType": "pc",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(
        data_json["Result"]["body"], columns=data_json["Result"]["header"]
    )
    temp_df["综合热度"] = pd.to_numeric(temp_df["综合热度"])
    temp_df["排名变化"] = pd.to_numeric(temp_df["排名变化"])
    temp_df["是否连续上榜"] = pd.to_numeric(temp_df["是否连续上榜"])
    return temp_df


if __name__ == "__main__":
    stock_hot_search_baidu_df = stock_hot_search_baidu(
        symbol="A股", date="20221025", time="19"
    )
    print(stock_hot_search_baidu_df)
