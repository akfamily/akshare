#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/14 20:00
Desc: 金十数据-沪深融资融券报告
https://datacenter.jin10.com/market
"""

import time
import pandas as pd
from akshare.utils import http


def stock_margin_szse_js() -> pd.DataFrame:
    """
    深圳融资融券报告，数据区间从20100331-至今
    https://datacenter.jin10.com/reportType/dc_market_margin_sz
    :return: pandas.DataFrame
    """
    t = time.time()
    params = {"_": t}
    res = http.get(
        url="https://cdn.jin10.com/data_center/reports/fs_2.json", params=params
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df.columns = [
        "融资买入额",
        "融资余额",
        "融券卖出量",
        "融券余量",
        "融券余额",
        "融资融券余额",
    ]
    temp_df = temp_df.sort_index()
    temp_df.index = pd.to_datetime(temp_df.index)
    temp_df = temp_df.astype("float")
    temp_df = temp_df.reset_index()
    temp_df = temp_df.rename(columns={"index": "日期"})
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    return temp_df


def stock_margin_sse_js() -> pd.DataFrame:
    """
    上海融资融券报告，数据区间从 20100331-至今
    https://datacenter.jin10.com/reportType/dc_market_margin_sse
    :return: pandas.DataFrame
    """
    url = "https://cdn.jin10.com/data_center/reports/fs_1.json"
    t = time.time()
    params = {"_": t}
    r = http.get(url, params=params)
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df = temp_df.reset_index()
    temp_df.columns = [
        "日期",
        "融资买入额",
        "融资余额",
        "融券卖出量",
        "融券余量",
        "融券余额",
        "融资融券余额",
    ]
    temp_df = temp_df.sort_values(by=["日期"], ignore_index=True)
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    temp_df["融资买入额"] = pd.to_numeric(temp_df["融资买入额"], errors="coerce")
    temp_df["融资余额"] = pd.to_numeric(temp_df["融资余额"], errors="coerce")
    temp_df["融券卖出量"] = pd.to_numeric(temp_df["融券卖出量"], errors="coerce")
    temp_df["融券余量"] = pd.to_numeric(temp_df["融券余量"], errors="coerce")
    temp_df["融券余额"] = pd.to_numeric(temp_df["融券余额"], errors="coerce")
    temp_df["融资融券余额"] = pd.to_numeric(temp_df["融资融券余额"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    stock_margin_szse_js_df = stock_margin_szse_js()
    print(stock_margin_szse_js_df)

    stock_margin_sse_js_df = stock_margin_sse_js()
    print(stock_margin_sse_js_df)
