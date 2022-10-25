# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/10/25 19:20
Desc: 50ETF期权波动率指数QVIX
http://1.optbbs.com/s/vix.shtml?50ETF
"""
import pandas as pd


def option_50etf_qvix() -> pd.DataFrame:
    """
    50ETF 期权波动率指数 QVIX
    http://1.optbbs.com/s/vix.shtml?50ETF
    :return: 50ETF 期权波动率指数 QVIX
    :rtype: pandas.DataFrame
    """
    url = "http://1.optbbs.com/d/csv/d/k.csv"
    temp_df = pd.read_csv(url).iloc[:, :5]
    temp_df.columns = [
        "date",
        "open",
        "high",
        "low",
        "close",
    ]
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    return temp_df


if __name__ == "__main__":
    option_50etf_qvix_df = option_50etf_qvix()
    print(option_50etf_qvix_df)
