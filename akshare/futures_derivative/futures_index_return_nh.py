#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/5/31 16:19
Desc: 南华期货-商品指数历史走势-收益率指数-数值
https://www.nanhua.net/nhzc/varietytrend.html
1000 点开始, 用收益率累计
https://www.nanhua.net/ianalysis/varietyindex/index/NHCI.json?t=1574932290494
"""
import time

import pandas as pd
import requests

from akshare.futures_derivative.futures_index_price_nh import (
    futures_index_symbol_table_nh,
)


def futures_return_index_nh(symbol: str = "Y") -> pd.DataFrame:
    """
    南华期货-南华指数单品种-收益率-所有历史数据
    https://www.nanhua.net/ianalysis/varietyindex/index/NHCI.json?t=1574932290494
    :param symbol: 通过 ak.futures_index_symbol_table_nh() 获取
    :type symbol: str
    :return: 南华指数单品种-收益率-所有历史数据
    :rtype: pandas.Series
    """
    symbol_df = futures_index_symbol_table_nh()
    symbol_list = symbol_df["code"].tolist()
    if symbol in symbol_list:
        t = time.time()
        url = f"https://www.nanhua.net/ianalysis/varietyindex/index/{symbol}.json?t={int(round(t * 1000))}"
        r = requests.get(url)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["date", "value"]
        temp_df["date"] = pd.to_datetime(temp_df["date"], unit="ms")
        temp_df["date"] = temp_df["date"].dt.tz_localize("UTC")
        temp_df["date"] = temp_df["date"].dt.tz_convert("Asia/Shanghai").dt.date
        temp_df["value"] = pd.to_numeric(temp_df["value"], errors="coerce")
        return temp_df


if __name__ == "__main__":
    futures_return_index_nh_df = futures_return_index_nh(symbol="NHCI")
    print(futures_return_index_nh_df)
