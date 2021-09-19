# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2020/4/21 15:34
Desc: 高频数据-标普 500 指数
https://github.com/FutureSharks/financial-data
long history data for S&P 500 index daily
http://www.econ.yale.edu/~shiller/data.htm
"""
import pandas as pd


def hf_sp_500(year: str = "2017") -> pd.DataFrame:
    """
    S&P 500 minute data from 2012-2018
    :param year: from 2012-2018
    :type year: str
    :return: specific year dataframe
    :rtype: pandas.DataFrame
    """
    url = f"https://github.com/FutureSharks/financial-data/raw/master/pyfinancialdata/data/stocks/histdata/SPXUSD/DAT_ASCII_SPXUSD_M1_{year}.csv"
    temp_df = pd.read_table(url, header=None, sep=";")
    temp_df.columns = ["date", "open", "high", "low", "close", "price"]
    temp_df.index = pd.to_datetime(temp_df.date)
    del temp_df["date"]
    return temp_df.iloc[:, :-1]


if __name__ == '__main__':
    hf_sp_500_df = hf_sp_500(year="2017")
    print(hf_sp_500_df)
