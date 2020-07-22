# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/22 14:23
Desc: 东方财富网-数据中心-主力数据-基金持仓
http://data.eastmoney.com/zlsj/2020-06-30-1-2.html
"""
import demjson
import pandas as pd
import requests


def stock_report_fund_hold(symbol: str = "基金持仓", date: str = "20200630") -> pd.DataFrame:
    """
    东方财富网-数据中心-主力数据-基金持仓
    http://data.eastmoney.com/zlsj/2020-06-30-1-2.html
    :param symbol: choice of {"基金持仓", "QFII持仓", "社保持仓", "券商持仓", "保险持仓", "信托持仓"}
    :type symbol: str
    :param date: 财报发布日期, xxxx-03-31, xxxx-06-30, xxxx-09-30, xxxx-12-31
    :type date: str
    :return: 基金持仓数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "基金持仓": "1",
        "QFII持仓": "2",
        "社保持仓": "3",
        "券商持仓": "4",
        "保险持仓": "5",
        "信托持仓": "6",
    }
    date = "-".join([date[:4], date[4:6], date[6:]])
    url = "http://data.eastmoney.com/zlsj/zlsj_list.aspx"
    params = {
        "type": "ajax",
        "st": "2",
        "sr": "-1",
        "p": "1",
        "ps": "2000",
        "jsObj": "EKHDBOTH",
        "stat": symbol_map[symbol],
        "cmd": "1",
        "date": date,
        "rt": "53179965",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):])
    temp_df = pd.DataFrame(data_json["data"])
    temp_df["RDate"] = pd.to_datetime(
        temp_df["RDate"].str.strip("/Date(").str.strip(")"), unit="ms"
    )
    temp_df.columns = [
        "stock_code",
        "stock_name",
        "pub_date",
        "_",
        "_",
        "hold_num",
        "hold_change",
        "share_hold_num",
        "value_position",
        "_",
        "_",
        "hold_value_change",
        "hold_rate_change",
    ]
    temp_df = temp_df[[
        "stock_code",
        "stock_name",
        "pub_date",
        "hold_num",
        "hold_change",
        "share_hold_num",
        "value_position",
        "hold_value_change",
        "hold_rate_change",
    ]]
    return temp_df


if __name__ == "__main__":
    stock_report_fund_hold_df = stock_report_fund_hold(symbol="基金持仓", date="20200630")
    print(stock_report_fund_hold_df)
