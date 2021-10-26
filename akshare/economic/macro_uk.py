#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/7/27 15:14
Desc: 东方财富-经济数据-英国
http://data.eastmoney.com/cjsj/foreign_4_0.html
"""
import pandas as pd
import requests
from akshare.utils import demjson


# Halifax房价指数月率
def macro_uk_halifax_monthly():
    """
    东方财富-经济数据-英国-Halifax 房价指数月率
    http://data.eastmoney.com/cjsj/foreign_4_0.html
    :return: Halifax 房价指数月率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "4",
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


# Halifax 房价指数年率
def macro_uk_halifax_yearly():
    """
    东方财富-经济数据-英国-Halifax 房价指数年率
    http://data.eastmoney.com/cjsj/foreign_4_1.html
    :return: Halifax房价指数年率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "4",
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


# 贸易帐
def macro_uk_trade():
    """
    东方财富-经济数据-英国-贸易帐
    http://data.eastmoney.com/cjsj/foreign_4_2.html
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
        "mkt": "4",
        "stat": "2",
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


# 央行公布利率决议
def macro_uk_bank_rate():
    """
    东方财富-经济数据-英国-央行公布利率决议
    http://data.eastmoney.com/cjsj/foreign_4_3.html
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
        "mkt": "4",
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


# 核心消费者物价指数年率
def macro_uk_core_cpi_yearly():
    """
    东方财富-经济数据-英国-核心消费者物价指数年率
    http://data.eastmoney.com/cjsj/foreign_4_4.html
    :return: 核心消费者物价指数年率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "4",
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


# 核心消费者物价指数月率
def macro_uk_core_cpi_monthly():
    """
    东方财富-经济数据-英国-核心消费者物价指数月率
    http://data.eastmoney.com/cjsj/foreign_4_5.html
    :return: 核心消费者物价指数月率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "4",
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


# 消费者物价指数年率
def macro_uk_cpi_yearly():
    """
    东方财富-经济数据-英国-消费者物价指数年率
    http://data.eastmoney.com/cjsj/foreign_4_6.html
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
        "mkt": "4",
        "stat": "6",
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


# 消费者物价指数月率
def macro_uk_cpi_monthly():
    """
    东方财富-经济数据-英国-消费者物价指数月率
    http://data.eastmoney.com/cjsj/foreign_4_7.html
    :return: 消费者物价指数月率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "4",
        "stat": "7",
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


# 零售销售月率
def macro_uk_retail_monthly():
    """
    东方财富-经济数据-英国-零售销售月率
    http://data.eastmoney.com/cjsj/foreign_4_8.html
    :return: 零售销售月率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "4",
        "stat": "8",
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


# 零售销售年率
def macro_uk_retail_yearly():
    """
    东方财富-经济数据-英国-零售销售年率
    http://data.eastmoney.com/cjsj/foreign_4_9.html
    :return: 零售销售年率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "4",
        "stat": "9",
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


# Rightmove 房价指数年率
def macro_uk_rightmove_yearly():
    """
    东方财富-经济数据-英国-Rightmove 房价指数年率
    http://data.eastmoney.com/cjsj/foreign_4_10.html
    :return: Rightmove 房价指数年率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "4",
        "stat": "10",
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


# Rightmove 房价指数月率
def macro_uk_rightmove_monthly():
    """
    东方财富-经济数据-英国-Rightmove 房价指数月率
    http://data.eastmoney.com/cjsj/foreign_4_11.html
    :return: Rightmove 房价指数月率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "4",
        "stat": "11",
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


# GDP 季率初值
def macro_uk_gdp_quarterly():
    """
    东方财富-经济数据-英国-GDP 季率初值
    http://data.eastmoney.com/cjsj/foreign_4_12.html
    :return: GDP 季率初值
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "4",
        "stat": "12",
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


# GDP 年率初值
def macro_uk_gdp_yearly():
    """
    东方财富-经济数据-英国-GDP 年率初值
    http://data.eastmoney.com/cjsj/foreign_4_13.html
    :return: GDP 年率初值
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "4",
        "stat": "13",
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
def macro_uk_unemployment_rate():
    """
    东方财富-经济数据-英国-失业率
    http://data.eastmoney.com/cjsj/foreign_4_14.html
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
        "mkt": "4",
        "stat": "14",
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
    macro_uk_halifax_monthly_df = macro_uk_halifax_monthly()
    print(macro_uk_halifax_monthly_df)

    macro_uk_halifax_yearly_df = macro_uk_halifax_yearly()
    print(macro_uk_halifax_yearly_df)

    macro_uk_trade_df = macro_uk_trade()
    print(macro_uk_trade_df)

    macro_uk_bank_rate_df = macro_uk_bank_rate()
    print(macro_uk_bank_rate_df)

    macro_uk_core_cpi_yearly_df = macro_uk_core_cpi_yearly()
    print(macro_uk_core_cpi_yearly_df)

    macro_uk_core_cpi_monthly_df = macro_uk_core_cpi_monthly()
    print(macro_uk_core_cpi_monthly_df)

    macro_uk_cpi_yearly_df = macro_uk_cpi_yearly()
    print(macro_uk_cpi_yearly_df)

    macro_uk_cpi_monthly_df = macro_uk_cpi_monthly()
    print(macro_uk_cpi_monthly_df)

    macro_uk_retail_monthly_df = macro_uk_retail_monthly()
    print(macro_uk_retail_monthly_df)

    macro_uk_retail_yearly_df = macro_uk_retail_yearly()
    print(macro_uk_retail_yearly_df)

    macro_uk_rightmove_yearly_df = macro_uk_rightmove_yearly()
    print(macro_uk_rightmove_yearly_df)

    macro_uk_rightmove_monthly_df = macro_uk_rightmove_monthly()
    print(macro_uk_rightmove_monthly_df)

    macro_uk_gdp_quarterly_df = macro_uk_gdp_quarterly()
    print(macro_uk_gdp_quarterly_df)

    macro_uk_gdp_yearly_df = macro_uk_gdp_yearly()
    print(macro_uk_gdp_yearly_df)

    macro_uk_unemployment_rate_df = macro_uk_unemployment_rate()
    print(macro_uk_unemployment_rate_df)
