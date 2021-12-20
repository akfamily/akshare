#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/20 15:19
Desc: 南华期货-商品指数历史走势-收益率指数-波动率
http://www.nanhua.net/nhzc/varietytrend.html
1000 点开始, 用收益率累计
目标地址: http://www.nanhua.net/ianalysis/volatility/20/NHCI.json?t=1574932291399
"""
import time

import requests
import pandas as pd

from akshare.futures_derivative.nh_index_price import futures_nh_index_symbol_table


def futures_nh_volatility_index(symbol: str = "NHCI", period: str = '20') -> pd.DataFrame:
    """
    南华期货-南华指数单品种-波动率-所有历史数据
    http://www.nanhua.net/nhzc/varietytrend.html
    :param symbol: 通过 ak.futures_nh_index_symbol_table() 获取
    :type symbol: str
    :param period: 波动周期 choice of {'5', '20', '60', '120'}
    :type period: str
    :return: 波动率-所有历史数据
    :rtype: pandas.DataFrame
    """
    symbol_df = futures_nh_index_symbol_table()
    if symbol in symbol_df["code"].tolist():
        t = time.time()
        url = f"http://www.nanhua.net/ianalysis/volatility/{period}/{symbol}.json?t={int(round(t * 1000))}"
        r = requests.get(url)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["date", "value"]
        temp_df['date'] = pd.to_datetime(temp_df["date"], unit='ms').dt.date
        return temp_df


if __name__ == "__main__":
    futures_nh_volatility_index_df = futures_nh_volatility_index(symbol="SA", period='5')
    print(futures_nh_volatility_index_df)
