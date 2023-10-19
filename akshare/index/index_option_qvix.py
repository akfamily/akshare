# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2023/10/19 16:00
Desc: 50 ETF 期权波动率指数 QVIX
300 ETF 期权波动率指数 QVIX
http://1.optbbs.com/s/vix.shtml?50ETF
http://1.optbbs.com/s/vix.shtml?300ETF
"""
import pandas as pd


def index_option_50etf_qvix() -> pd.DataFrame:
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
    temp_df["date"] = pd.to_datetime(temp_df["date"], errors="coerce").dt.date
    temp_df['open'] = pd.to_numeric(temp_df['open'], errors="coerce")
    temp_df['high'] = pd.to_numeric(temp_df['high'], errors="coerce")
    temp_df['low'] = pd.to_numeric(temp_df['low'], errors="coerce")
    temp_df['close'] = pd.to_numeric(temp_df['close'], errors="coerce")
    return temp_df


def index_option_50etf_min_qvix() -> pd.DataFrame:
    """
    50 ETF 期权波动率指数 QVIX
    http://1.optbbs.com/s/vix.shtml?50ETF
    :return: 50 ETF 期权波动率指数 QVIX
    :rtype: pandas.DataFrame
    """
    url = "http://1.optbbs.com/d/csv/d/vix50.csv"
    temp_df = pd.read_csv(url).iloc[:, :2]
    temp_df.columns = [
        "time",
        "qvix",
    ]
    temp_df['qvix'] = pd.to_numeric(temp_df['qvix'], errors="coerce")
    return temp_df


def index_option_300etf_qvix() -> pd.DataFrame:
    """
    300 ETF 期权波动率指数 QVIX
    http://1.optbbs.com/s/vix.shtml?300ETF
    :return: 300 ETF 期权波动率指数 QVIX
    :rtype: pandas.DataFrame
    """
    url = "http://1.optbbs.com/d/csv/d/k.csv"
    temp_df = pd.read_csv(url).iloc[:, [0, 9, 10, 11, 12]]
    temp_df.columns = [
        "date",
        "open",
        "high",
        "low",
        "close",
    ]
    temp_df["date"] = pd.to_datetime(temp_df["date"], errors="coerce").dt.date
    temp_df['open'] = pd.to_numeric(temp_df['open'], errors="coerce")
    temp_df['high'] = pd.to_numeric(temp_df['high'], errors="coerce")
    temp_df['low'] = pd.to_numeric(temp_df['low'], errors="coerce")
    temp_df['close'] = pd.to_numeric(temp_df['close'], errors="coerce")
    return temp_df


def index_option_300etf_min_qvix() -> pd.DataFrame:
    """
    300 ETF 期权波动率指数 QVIX-分时
    http://1.optbbs.com/s/vix.shtml?300ETF
    :return: 300 ETF 期权波动率指数 QVIX-分时
    :rtype: pandas.DataFrame
    """
    url = "http://1.optbbs.com/d/csv/d/vix300.csv"
    temp_df = pd.read_csv(url).iloc[:, :2]
    temp_df.columns = [
        "time",
        "qvix",
    ]
    temp_df['qvix'] = pd.to_numeric(temp_df['qvix'], errors="coerce")
    return temp_df


if __name__ == "__main__":
    index_option_50etf_qvix_df = index_option_50etf_qvix()
    print(index_option_50etf_qvix_df)

    index_option_50etf_min_qvix_df = index_option_50etf_min_qvix()
    print(index_option_50etf_min_qvix_df)

    index_option_300etf_qvix_df = index_option_300etf_qvix()
    print(index_option_300etf_qvix_df)

    index_option_300etf_min_qvix_df = index_option_300etf_min_qvix()
    print(index_option_300etf_min_qvix_df)
