#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/6/4 15:19
Desc: 南华期货-商品指数历史走势-收益率指数-波动率
https://www.nanhua.net/nhzc/varietytrend.html
1000 点开始, 用收益率累计
目标地址: https://www.nanhua.net/ianalysis/volatility/20/NHCI.json?t=1574932291399
"""
import time

import pandas as pd
import requests

from akshare.futures_derivative.futures_index_price_nh import (
    futures_index_symbol_table_nh,
)


def futures_volatility_index_nh(
    symbol: str = "NHCI", period: str = "20"
) -> pd.DataFrame:
    """
    南华期货-南华指数单品种-波动率-所有历史数据
    https://www.nanhua.net/nhzc/varietytrend.html
    :param symbol: 通过 ak.futures_index_symbol_table_nh() 获取
    :type symbol: str
    :param period: 波动周期 choice of {'5', '20', '60', '120'}
    :type period: str
    :return: 波动率-所有历史数据
    :rtype: pandas.DataFrame
    """
    symbol_df = futures_index_symbol_table_nh()
    if symbol in symbol_df["code"].tolist():
        t = time.time()
        url = f"https://www.nanhua.net/ianalysis/volatility/{period}/{symbol}.json?t={int(round(t * 1000))}"
        r = requests.get(url)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["date", "value"]
        temp_df["date"] = pd.to_datetime(temp_df["date"], unit="ms")
        temp_df["date"] = temp_df["date"].dt.tz_localize("UTC")
        temp_df["date"] = temp_df["date"].dt.tz_convert("Asia/Shanghai").dt.date
        return temp_df


if __name__ == "__main__":
    futures_volatility_index_nh_df = futures_volatility_index_nh(
        symbol="SA", period="5"
    )
    print(futures_volatility_index_nh_df)
