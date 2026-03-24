#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/3/24 11:30
Desc: 乐咕乐股-创新高、新低的股票数量
https://www.legulegu.com/stockdata/high-low-statistics
"""

from datetime import date

import pandas as pd
import requests

from akshare.utils.cons import headers


def stock_a_high_low_statistics(symbol: str = "all") -> pd.DataFrame:
    """
    乐咕乐股-创新高、新低的股票数量
    https://www.legulegu.com/stockdata/high-low-statistics
    :param symbol: choice of {"all", "sz50", "hs300", "zz500"}
    :type symbol: str
    :return: 创新高、新低的股票数量
    :rtype: pandas.DataFrame
    """
    url = f"https://www.legulegu.com/stockdata/member-ship/get-high-low-statistics/{symbol}"
    r = requests.get(url, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    del temp_df["indexCode"]
    temp_df['date'] = temp_df['date'].apply(lambda x: pd.Timestamp(date(x[0], x[1], x[2])))
    temp_df["date"] = pd.to_datetime(temp_df["date"], errors="coerce").dt.date
    temp_df["close"] = pd.to_numeric(temp_df["close"], errors="coerce")
    temp_df["high20"] = pd.to_numeric(temp_df["high20"], errors="coerce")
    temp_df["low20"] = pd.to_numeric(temp_df["low20"], errors="coerce")
    temp_df["high60"] = pd.to_numeric(temp_df["high60"], errors="coerce")
    temp_df["low60"] = pd.to_numeric(temp_df["low60"], errors="coerce")
    temp_df["high120"] = pd.to_numeric(temp_df["high120"], errors="coerce")
    temp_df["low120"] = pd.to_numeric(temp_df["low120"], errors="coerce")
    temp_df.sort_values(by=["date"], inplace=True, ignore_index=True)
    return temp_df


if __name__ == "__main__":
    stock_a_high_low_statistics_df = stock_a_high_low_statistics(symbol="all")
    print(stock_a_high_low_statistics_df)

    stock_a_high_low_statistics_df = stock_a_high_low_statistics(symbol="sz50")
    print(stock_a_high_low_statistics_df)

    stock_a_high_low_statistics_df = stock_a_high_low_statistics(symbol="hs300")
    print(stock_a_high_low_statistics_df)

    stock_a_high_low_statistics_df = stock_a_high_low_statistics(symbol="zz500")
    print(stock_a_high_low_statistics_df)
