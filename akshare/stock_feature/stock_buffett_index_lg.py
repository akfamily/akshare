#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/10/15 16:16
Desc: 乐估乐股-底部研究-巴菲特指标
https://legulegu.com/stockdata/marketcap-gdp
"""
import pandas as pd
import requests


def stock_buffett_index_lg() -> pd.DataFrame:
    """
    乐估乐股-底部研究-巴菲特指标
    https://legulegu.com/stockdata/marketcap-gdp
    :return: 巴菲特指标
    :rtype: pandas.DataFrame
    """
    url = "https://legulegu.com/api/stockdata/marketcap-gdp/get-marketcap-gdp"
    params = {"token": "a44658d8b4705f9370174ddea8d5ce50"}
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.rename(
        columns={
            "marketCap": "总市值",
            "gdp": "GDP",
            "close": "收盘价",
            "date": "日期",
            "quantileInAllHistory": "总历史分位数",
            "quantileInRecent10Years": "近十年分位数",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "日期",
            "收盘价",
            "总市值",
            "GDP",
            "近十年分位数",
            "总历史分位数",
        ]
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], unit="ms").dt.date
    return temp_df


if __name__ == "__main__":
    stock_buffett_index_lg_df = stock_buffett_index_lg()
    print(stock_buffett_index_lg_df)
