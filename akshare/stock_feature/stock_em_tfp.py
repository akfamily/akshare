# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/7/3 10:05
Desc: 东方财富网-数据中心-特色数据-停复牌信息
http://data.eastmoney.com/tfpxx/
"""
import demjson
import pandas as pd
import requests


def stock_em_tfp(date: str = "20200319") -> pd.DataFrame:
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
    temp_df['index'] = range(1, len(temp_df)+1)
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
    return temp_df


if __name__ == "__main__":
    stock_em_tfp_df = stock_em_tfp(date="20201209")
    print(stock_em_tfp_df)
