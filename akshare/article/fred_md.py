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
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "s3.amazonaws.com",
        "Pragma": "no-cache",
        "Referer": "https://research.stlouisfed.org/econ/mccracken/fred-databases/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    temp_df = pd.read_csv(BytesIO(r.content))
    return temp_df


def fred_qd(date="2020-03"):
    url = f"https://s3.amazonaws.com/files.fred.stlouisfed.org/fred-md/quarterly/{date}.csv"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "s3.amazonaws.com",
        "Pragma": "no-cache",
        "Referer": "https://research.stlouisfed.org/econ/mccracken/fred-databases/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }
    temp_df = pd.read_csv(url)
    return temp_df


if __name__ == '__main__':
    fred_md_df = fred_md(date="2020-01")
    print(fred_md_df)
