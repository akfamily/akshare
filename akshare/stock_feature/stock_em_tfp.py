#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/7/3 10:05
Desc: 东方财富网-数据中心-特色数据-停复牌信息
http://data.eastmoney.com/tfpxx/
"""
import pandas as pd
import requests

from akshare.utils import demjson


def stock_tfp_em(date: str = "20211026") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-停复牌信息
    http://data.eastmoney.com/tfpxx/
    :param date: specific date as "2020-03-19"
    :type date: str
    :return: 停复牌信息表
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "sr": "-1",
        "ps": "5000",
        "p": "1",
        "type": "FD",
        "sty": "SRB",
        "js": "({data:[(x)],pages:(pc)})",
        "fd": "-".join([date[:4], date[4:6], date[6:]]),
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame(data_json["data"]).iloc[:, 0].str.split(",", expand=True)
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.columns = [
        "序号",
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
    temp_df = temp_df[
        ["序号", "代码", "名称", "停牌时间", "停牌截止时间", "停牌期限", "停牌原因", "所属市场", "预计复牌时间"]
    ]
    temp_df['停牌时间'] = pd.to_datetime(temp_df['停牌时间']).dt.date
    temp_df['停牌截止时间'] = pd.to_datetime(temp_df['停牌截止时间']).dt.date
    temp_df['预计复牌时间'] = pd.to_datetime(temp_df['预计复牌时间']).dt.date
    return temp_df


if __name__ == "__main__":
    stock_tfp_em_df = stock_tfp_em(date="20211026")
    print(stock_tfp_em_df)
