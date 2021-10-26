#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/7/26 20:14
Desc: 东方财富-经济数据-日本
http://data.eastmoney.com/cjsj/foreign_3_0.html
"""
import pandas as pd
import requests
from akshare.utils import demjson


# 央行公布利率决议
def macro_japan_bank_rate():
    """
    东方财富-经济数据-日本-央行公布利率决议
    http://data.eastmoney.com/cjsj/foreign_3_0.html
    :return: 央行公布利率决议
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "3",
        "stat": "0",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1625474966006",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    return temp_df


# 全国消费者物价指数年率
def macro_japan_cpi_yearly():
    """
    东方财富-经济数据-日本-全国消费者物价指数年率
    http://data.eastmoney.com/cjsj/foreign_3_1.html
    :return: 全国消费者物价指数年率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "3",
        "stat": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1625474966006",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    return temp_df


# 全国核心消费者物价指数年率
def macro_japan_core_cpi_yearly():
    """
    东方财富-经济数据-日本-全国核心消费者物价指数年率
    http://data.eastmoney.com/cjsj/foreign_2_2.html
    :return: 全国核心消费者物价指数年率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "3",
        "stat": "2",
        'pageNo': '1',
        'pageNum': '1',
        "_": "1625474966006",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    return temp_df


# 失业率
def macro_japan_unemployment_rate():
    """
    东方财富-经济数据-日本-失业率
    http://data.eastmoney.com/cjsj/foreign_2_3.html
    :return: 失业率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "3",
        "stat": "3",
        'pageNo': '1',
        'pageNum': '1',
        "_": "1625474966006",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    return temp_df


# 领先指标终值
def macro_japan_head_indicator():
    """
    东方财富-经济数据-日本-领先指标终值
    http://data.eastmoney.com/cjsj/foreign_3_4.html
    :return: 领先指标终值
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "3",
        "stat": "4",
        'pageNo': '1',
        'pageNum': '1',
        "_": "1625474966006",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    return temp_df


if __name__ == '__main__':
    macro_japan_bank_rate_df = macro_japan_bank_rate()
    print(macro_japan_bank_rate_df)

    macro_japan_cpi_yearly_df = macro_japan_cpi_yearly()
    print(macro_japan_cpi_yearly_df)

    macro_japan_core_cpi_yearly_df = macro_japan_core_cpi_yearly()
    print(macro_japan_core_cpi_yearly_df)

    macro_japan_unemployment_rate_df = macro_japan_unemployment_rate()
    print(macro_japan_unemployment_rate_df)

    macro_japan_head_indicator_df = macro_japan_head_indicator()
    print(macro_japan_head_indicator_df)
