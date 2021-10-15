# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/5/6 18:32
Desc: 创新高、新低的股票数量
https://www.legulegu.com/stockdata/high-low-statistics
"""
import pandas as pd
import requests


def stock_a_high_low_statistics(market: str = "all") -> pd.DataFrame:
    """
    创新高、新低的股票数量
    https://www.legulegu.com/stockdata/high-low-statistics
    :param market: choice of {"all", "sz50", "hs300", "zz500"}
    :type market: str
    :return: 创新高、新低的股票数量
    :rtype: pandas.DataFrame
    """
    if market == "all":
        url = f"https://www.legulegu.com/stockdata/member-ship/get-high-low-statistics/{market}"
    elif market == "sz50":
        url = f"https://www.legulegu.com/stockdata/member-ship/get-high-low-statistics/{market}"
    elif market == "hs300":
        url = f"https://www.legulegu.com/stockdata/member-ship/get-high-low-statistics/{market}"
    elif market == "zz500":
        url = f"https://www.legulegu.com/stockdata/member-ship/get-high-low-statistics/{market}"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    temp_df["date"] = pd.to_datetime(temp_df["date"], unit="ms")
    del temp_df["id"]
    del temp_df["indexCode"]
    return temp_df


if __name__ == '__main__':
    stock_a_high_low_statistics_df = stock_a_high_low_statistics(market="all")
    print(stock_a_high_low_statistics_df)

    stock_a_high_low_statistics_df = stock_a_high_low_statistics(market="sz50")
    print(stock_a_high_low_statistics_df)

    stock_a_high_low_statistics_df = stock_a_high_low_statistics(market="hs300")
    print(stock_a_high_low_statistics_df)

    stock_a_high_low_statistics_df = stock_a_high_low_statistics(market="zz500")
    print(stock_a_high_low_statistics_df)
