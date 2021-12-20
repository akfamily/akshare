#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/5/18 15:06
Desc: 增发和配股
东方财富网-数据中心-新股数据-增发-全部增发
http://data.eastmoney.com/other/gkzf.html
东方财富网-数据中心-新股数据-配股
http://data.eastmoney.com/xg/pg/
"""
import pandas as pd
import requests

from akshare.utils import demjson


def stock_em_qbzf():
    """
    东方财富网-数据中心-新股数据-增发-全部增发
    http://data.eastmoney.com/other/gkzf.html
    :return: 全部增发
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "st": "5",
        "sr": "-1",
        "ps": "5000",
        "p": "1",
        "type": "SR",
        "sty": "ZF",
        "js": '({"pages":(pc),"data":[(x)]})',
        "stat": "0",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "股票代码",
        "股票简称",
        "发行方式",
        "发行总数",
        "发行价格",
        "最新价",
        "发行日期",
        "增发上市日期",
        "_",
        "增发代码",
        "网上发行",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "股票代码",
            "股票简称",
            "增发代码",
            "发行方式",
            "发行总数",
            "网上发行",
            "发行价格",
            "最新价",
            "发行日期",
            "增发上市日期",
        ]
    ]
    temp_df["锁定期"] = "1-3年"
    return temp_df


def stock_em_pg():
    """
    东方财富网-数据中心-新股数据-配股
    http://data.eastmoney.com/xg/pg/
    :return: 配股
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "st": "6",
        "sr": "-1",
        "ps": "5000",
        "p": "1",
        "type": "NS",
        "sty": "NSA",
        "js": "({data:[(x)],pages:(pc)})",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "_",
        "_",
        "股票代码",
        "股票简称",
        "配售代码",
        "_",
        "配股比例",
        "配股价",
        "配股前总股本",
        "配股数量",
        "配股后总股本",
        "股权登记日",
        "缴款起始日期",
        "缴款截止日期",
        "上市日",
        "_",
        "_",
        "_",
        "_",
        "_",
        "最新价",
        "_",
    ]
    temp_df = temp_df[
        [
            "股票代码",
            "股票简称",
            "配售代码",
            "配股数量",
            "配股比例",
            "配股价",
            "最新价",
            "配股前总股本",
            "配股后总股本",
            "股权登记日",
            "缴款起始日期",
            "缴款截止日期",
            "上市日",
        ]
    ]
    temp_df["配股比例"] = "10配" + temp_df["配股比例"]
    return temp_df


if __name__ == "__main__":
    stock_em_qbzf_df = stock_em_qbzf()
    print(stock_em_qbzf_df)

    stock_em_pg_df = stock_em_pg()
    print(stock_em_pg_df)
