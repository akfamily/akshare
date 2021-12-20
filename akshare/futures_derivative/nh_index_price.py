#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/20 14:52
Desc: 南华期货-商品指数历史走势-价格指数-数值
http://www.nanhua.net/nhzc/varietytrend.html
1000 点开始, 用收益率累计
http://www.nanhua.net/ianalysis/varietyindex/price/A.json?t=1574932974280
"""
import time

import requests
import pandas as pd


def futures_nh_index_symbol_table() -> pd.DataFrame:
    """
    南华期货-南华指数所有品种一览表
    http://www.nanhua.net/ianalysis/varietyindex/price/A.json?t=1574932974280
    :return: 南华指数所有品种一览表
    :rtype: pandas.DataFrame
    """
    url = "http://www.nanhua.net/ianalysis/plate-variety.json"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    temp_df['firstday'] = pd.to_datetime(temp_df['firstday']).dt.date
    return temp_df


def futures_nh_price_index(symbol: str = "A") -> pd.DataFrame:
    """
    南华期货-南华指数单品种-价格-所有历史数据
    http://www.nanhua.net/ianalysis/varietyindex/price/A.json?t=1574932974280
    :param symbol: 通过 ak.futures_nh_index_symbol_table() 获取
    :type symbol: str
    :return: 南华期货-南华指数单品种-价格-所有历史数据
    :rtype: pandas.Series
    """
    symbol_df = futures_nh_index_symbol_table()
    if symbol in symbol_df["code"].tolist():
        t = time.time()
        url = f"http://www.nanhua.net/ianalysis/varietyindex/price/{symbol}.json?t={int(round(t * 1000))}"
        r = requests.get(url)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["date", "value"]
        temp_df['date'] = pd.to_datetime(temp_df["date"], unit='ms').dt.date
        return temp_df


if __name__ == "__main__":
    futures_nh_index_symbol_table_df = futures_nh_index_symbol_table()
    print(futures_nh_index_symbol_table_df)

    futures_nh_price_index_df = futures_nh_price_index(symbol="NHAI")
    print(futures_nh_price_index_df)
