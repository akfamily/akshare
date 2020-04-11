# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/10 19:58
Desc: 
"""
from io import BytesIO
import pandas as pd
import requests


def fred_md(date="2020-01"):
    url = f"https://s3.amazonaws.com/files.fred.stlouisfed.org/fred-md/monthly/{date}.csv"
    r = requests.get(url)
    temp_df = pd.read_csv(BytesIO(r.content))
    return temp_df


def fred_qd(date="2020-03"):
    url = f"https://s3.amazonaws.com/files.fred.stlouisfed.org/fred-md/quarterly/{date}.csv"
    temp_df = pd.read_csv(url)
    return temp_df


if __name__ == '__main__':
    fred_md_df = fred_md(date="2020-01")
    print(fred_md_df)
