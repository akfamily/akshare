#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/1/7 14:00
Desc: 国泰君安期货-交易日历数据表
https://www.gtjaqh.com/pc/calendar.html
"""
import pandas as pd
import requests


def futures_rule(date: str = "20220106") -> pd.DataFrame:
    """
    国泰君安期货-交易日历数据表
    https://www.gtjaqh.com/pc/calendar.html
    :param date: 需要指定为交易日, 且是近期的日期
    :type date: str
    :return: 交易日历数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.gtjaqh.com/do/4600.128"
    params = {"base_date": f"{date}"}
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df = temp_df[temp_df["tradingday"] == date]
    if not temp_df["events"].values[0]:
        return f"{date} 查询时间过早或者不是交易日"
    else:
        big_df = pd.read_html(temp_df["events"].values[0][0]["content"], header=1)[0]
        big_df['交易保证金比例'] = big_df['交易保证金比例'].str.strip("%")
        big_df['交易保证金比例'] = pd.to_numeric(big_df['交易保证金比例'], errors="coerce")

        big_df['涨跌停板幅度'] = big_df['涨跌停板幅度'].str.strip("%")
        big_df['涨跌停板幅度'] = pd.to_numeric(big_df['涨跌停板幅度'], errors="coerce")

        big_df['合约乘数'] = pd.to_numeric(big_df['合约乘数'], errors="coerce")
        big_df['最小变动价位'] = pd.to_numeric(big_df['最小变动价位'], errors="coerce")
        big_df['限价单每笔最大下单手数'] = pd.to_numeric(big_df['限价单每笔最大下单手数'], errors="coerce")
        return big_df


if __name__ == '__main__':
    futures_rule_df = futures_rule(date="20220106")
    print(futures_rule_df)
