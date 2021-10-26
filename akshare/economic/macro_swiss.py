#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/7/23 16:50
Desc: 东方财富-经济数据-瑞士
http://data.eastmoney.com/cjsj/foreign_2_0.html
"""
import pandas as pd
import requests
from akshare.utils import demjson


# SVME采购经理人指数
def macro_swiss_svme():
    """
    东方财富-经济数据-瑞士-SVME采购经理人指数
    http://data.eastmoney.com/cjsj/foreign_2_0.html
    :return: SVME采购经理人指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "2",
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


# 贸易帐
def macro_swiss_trade():
    """
    东方财富-经济数据-瑞士-贸易帐
    http://data.eastmoney.com/cjsj/foreign_2_1.html
    :return: 贸易帐
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "2",
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


# 消费者物价指数年率
def macro_swiss_cpi_yearly():
    """
    东方财富-经济数据-瑞士-消费者物价指数年率
    http://data.eastmoney.com/cjsj/foreign_2_2.html
    :return: 消费者物价指数年率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "2",
        "stat": "2",
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


# GDP季率
def macro_swiss_gdp_quarterly():
    """
    东方财富-经济数据-瑞士-GDP季率
    http://data.eastmoney.com/cjsj/foreign_2_3.html
    :return: GDP季率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "2",
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


# GDP年率
def macro_swiss_gbd_yearly():
    """
    东方财富-经济数据-瑞士-GDP 年率
    http://data.eastmoney.com/cjsj/foreign_2_4.html
    :return: GDP年率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "2",
        "stat": "4",
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


# 央行公布利率决议
def macro_swiss_gbd_bank_rate():
    """
    东方财富-经济数据-瑞士-央行公布利率决议
    http://data.eastmoney.com/cjsj/foreign_2_5.html
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
        "mkt": "2",
        "stat": "5",
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
    macro_swiss_svme_df = macro_swiss_svme()
    print(macro_swiss_svme_df)

    macro_swiss_trade_df = macro_swiss_trade()
    print(macro_swiss_trade_df)

    macro_swiss_cpi_yearly_df = macro_swiss_cpi_yearly()
    print(macro_swiss_cpi_yearly_df)

    macro_swiss_gdp_quarterly_df = macro_swiss_gdp_quarterly()
    print(macro_swiss_gdp_quarterly_df)

    macro_swiss_gbd_yearly_df = macro_swiss_gbd_yearly()
    print(macro_swiss_gbd_yearly_df)

    macro_swiss_gbd_bank_rate_df = macro_swiss_gbd_bank_rate()
    print(macro_swiss_gbd_bank_rate_df)
