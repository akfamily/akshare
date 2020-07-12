# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/12 21:51
Desc: 国泰君安期货-交易日历数据表
https://www.gtjaqh.com/pc/calendar.html
"""
import pandas as pd
import requests


def futures_rule(trade_date: str = "20200712") -> pd.DataFrame:
    """
    国泰君安期货-交易日历数据表
    https://www.gtjaqh.com/pc/calendar.html
    :return: 交易日历数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.gtjaqh.com/fn/128"
    params = {"base_date": f"{trade_date}"}
    r = requests.post(url, json=params)
    temp_df = pd.DataFrame(r.json()["data"])
    temp_df = temp_df[temp_df["tradingday"] == trade_date]
    if not temp_df["events"].values[0]:
        return f"{trade_date} 查询时间过早或者不是交易日"
    else:
        table_df = pd.read_html(temp_df["events"].values[0][0]["content"], header=1)[0]
        table_df.dropna(axis=1, how="all", inplace=True)
    return table_df


if __name__ == '__main__':
    futures_rule_df = futures_rule(trade_date="20200713")
    print(futures_rule_df)
