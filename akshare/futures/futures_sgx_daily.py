#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2020/3/14 0:25
Desc: Futures data from Singapore Exchange
https://www.sgx.com/zh-hans/research-education/derivatives
https://links.sgx.com/1.0.0/derivatives-daily/5888/FUTURE.zip
"""
import zipfile
from io import BytesIO
from io import StringIO

import pandas as pd
import requests
from tqdm import tqdm

from akshare.index.index_investing import index_investing_global


def futures_sgx_daily(trade_date: str = "20200306", recent_day: str = "3") -> pd.DataFrame:
    """
    Futures daily data from sgx
    P.S. it will be slowly if you do not use VPN
    :param trade_date: it means the specific trade day you want to fetch
    :type trade_date: str e.g., "2020/03/06"
    :param recent_day: the data range near the specific trade day
    :type recent_day: str e.g. "3" means 3 day before specific trade day
    :return: data contains from (trade_date - recent_day) to trade_day
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    index_df = index_investing_global(country="新加坡", index_name="FTSE Singapore", start_date="20200101", end_date=trade_date)
    index_df.sort_index(inplace=True)
    index_df.reset_index(inplace=True)
    index_df.reset_index(inplace=True)
    index_df.index = index_df["index"] + 5840
    date_start = index_df.index[-1] + 1 - int(recent_day)
    date_end = index_df.index[-1] + 1
    for page in tqdm(range(date_start, date_end)):
        # page = 5883
        url = f"https://links.sgx.com/1.0.0/derivatives-daily/{page}/FUTURE.zip"
        r = requests.get(url)
        with zipfile.ZipFile(BytesIO(r.content)) as file:
            with file.open(file.namelist()[0]) as my_file:
                data = my_file.read().decode()
                if file.namelist()[0].endswith("txt"):
                    data_df = pd.read_table(StringIO(data))
                else:
                    data_df = pd.read_csv(StringIO(data))
        big_df = big_df.append(data_df)
    return big_df


if __name__ == '__main__':
    futures_sgx_daily_df = futures_sgx_daily(trade_date="20211118", recent_day="2")
    print(futures_sgx_daily_df)
