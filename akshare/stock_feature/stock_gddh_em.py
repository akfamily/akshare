#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/19 13:32
Desc: 乐咕乐股-创新高、新低的股票数量
https://www.legulegu.com/stockdata/high-low-statistics
"""
import pandas as pd
import requests


def stock_a_high_low_statistics(symbol: str = "all") -> pd.DataFrame:
    """
    乐咕乐股-创新高、新低的股票数量
    https://www.legulegu.com/stockdata/high-low-statistics
    :param symbol: choice of {"all", "sz50", "hs300", "zz500"}
    :type symbol: str
    :return: 创新高、新低的股票数量
    :rtype: pandas.DataFrame
    """
    if symbol == "all":
        url = f"https://www.legulegu.com/stockdata/member-ship/get-high-low-statistics/{symbol}"
    elif symbol == "sz50":
        url = f"https://www.legulegu.com/stockdata/member-ship/get-high-low-statistics/{symbol}"
    elif symbol == "hs300":
        url = f"https://www.legulegu.com/stockdata/member-ship/get-high-low-statistics/{symbol}"
    elif symbol == "zz500":
        url = f"https://www.legulegu.com/stockdata/member-ship/get-high-low-statistics/{symbol}"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    temp_df["date"] = pd.to_datetime(temp_df["date"], unit="ms").dt.date
    del temp_df["indexCode"]
    temp_df.sort_values(['date'], inplace=True, ignore_index=True)
    return temp_df


if __name__ == '__main__':
    stock_a_high_low_statistics_df = stock_a_high_low_statistics(symbol="all")
    print(stock_a_high_low_statistics_df)

    stock_a_high_low_statistics_df = stock_a_high_low_statistics(symbol="sz50")
    print(stock_a_high_low_statistics_df)

    stock_a_high_low_statistics_df = stock_a_high_low_statistics(symbol="hs300")
    print(stock_a_high_low_statistics_df)

    stock_a_high_low_statistics_df = stock_a_high_low_statistics(symbol="zz500")
    print(stock_a_high_low_statistics_df)
