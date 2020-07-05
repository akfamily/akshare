# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/3/25 0:05
Desc: 东方财富网-数据中心-特色数据-停复牌信息
http://data.eastmoney.com/tfpxx/
"""
import demjson
import pandas as pd
import requests


def stock_em_tfp(trade_date: str = "2020-03-19") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-停复牌信息
    http://data.eastmoney.com/tfpxx/
    :param trade_date: specific date as "2020-03-19"
    :type trade_date: str
    :return: 停复牌信息表
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "FD",
        "sty": "SRB",
        "st": "0",
        "sr": "-1",
        "p": "1",
        "ps": "50",
        "js": "var BSkKafhD={pages:(pc),data:[(x)]}",
        "mkt": "1",
        "fd": trade_date,
        "rt": "52835529",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") :])
    temp_df = pd.DataFrame(data_json["data"]).iloc[:, 0].str.split(",", expand=True)
    temp_df.columns = [
        "代码",
        "名称",
        "停牌时间",
        "停牌截止时间",
        "停牌期限",
        "停牌原因",
        "所属市场",
        "-",
        "预计复牌时间",
    ]
    data_df = temp_df[["代码", "名称", "停牌时间", "停牌截止时间", "停牌期限", "停牌原因", "所属市场", "预计复牌时间"]]
    return data_df


if __name__ == "__main__":
    stock_em_tfp_df = stock_em_tfp(trade_date="2020-06-24")
    print(stock_em_tfp_df)
