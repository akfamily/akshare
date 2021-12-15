#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/15 19:50
Desc: 东方财富-经济数据-加拿大
http://data.eastmoney.com/cjsj/foreign_5_0.html
"""
import pandas as pd
import requests

from akshare.utils import demjson


# 新屋开工
def macro_canada_new_house_rate() -> pd.DataFrame:
    """
    东方财富-经济数据-加拿大-新屋开工
    http://data.eastmoney.com/cjsj/foreign_7_0.html
    :return: 新屋开工
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "7",
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
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    return temp_df


# 失业率
def macro_canada_unemployment_rate() -> pd.DataFrame:
    """
    东方财富-经济数据-加拿大-失业率
    http://data.eastmoney.com/cjsj/foreign_7_1.html
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
        "mkt": "7",
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
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    return temp_df


# 贸易帐
def macro_canada_trade() -> pd.DataFrame:
    """
    东方财富-经济数据-加拿大-贸易帐
    http://data.eastmoney.com/cjsj/foreign_7_2.html
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
        "mkt": "7",
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
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    temp_df["前值"] = pd.to_numeric(temp_df["前值"]) / 100
    temp_df["现值"] = pd.to_numeric(temp_df["现值"]) / 100
    return temp_df


# 零售销售月率
def macro_canada_retail_rate_monthly() -> pd.DataFrame:
    """
    东方财富-经济数据-加拿大-零售销售月率
    http://data.eastmoney.com/cjsj/foreign_7_3.html
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
        "mkt": "7",
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
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    return temp_df


# 央行公布利率决议
def macro_canada_bank_rate() -> pd.DataFrame:
    """
    东方财富-经济数据-加拿大-央行公布利率决议
    http://data.eastmoney.com/cjsj/foreign_7_4.html
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
        "mkt": "7",
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
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    return temp_df


# 核心消费者物价指数年率
def macro_canada_core_cpi_yearly() -> pd.DataFrame:
    """
    东方财富-经济数据-加拿大-核心消费者物价指数年率
    http://data.eastmoney.com/cjsj/foreign_7_5.html
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
        "mkt": "7",
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
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    return temp_df


# 核心消费者物价指数月率
def macro_canada_core_cpi_monthly() -> pd.DataFrame:
    """
    东方财富-经济数据-加拿大-核心消费者物价指数月率
    http://data.eastmoney.com/cjsj/foreign_7_6.html
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
        "mkt": "7",
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
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    return temp_df


# 消费者物价指数年率
def macro_canada_cpi_yearly() -> pd.DataFrame:
    """
    东方财富-经济数据-加拿大-消费者物价指数年率
    http://data.eastmoney.com/cjsj/foreign_7_7.html
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
        "mkt": "7",
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
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    return temp_df


# 消费者物价指数月率
def macro_canada_cpi_monthly() -> pd.DataFrame:
    """
    东方财富-经济数据-加拿大-消费者物价指数月率
    http://data.eastmoney.com/cjsj/foreign_7_8.html
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
        "mkt": "7",
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
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    return temp_df


# GDP 月率
def macro_canada_gdp_monthly() -> pd.DataFrame:
    """
    东方财富-经济数据-加拿大-GDP 月率
    http://data.eastmoney.com/cjsj/foreign_7_9.html
    :return: GDP 月率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "7",
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
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    temp_df["前值"] = pd.to_numeric(temp_df["前值"])
    temp_df["现值"] = pd.to_numeric(temp_df["现值"])
    return temp_df


if __name__ == '__main__':
    macro_canada_new_house_rate_df = macro_canada_new_house_rate()
    print(macro_canada_new_house_rate_df)

    macro_canada_unemployment_rate_df = macro_canada_unemployment_rate()
    print(macro_canada_unemployment_rate_df)

    macro_canada_trade_df = macro_canada_trade()
    print(macro_canada_trade_df)

    macro_canada_retail_rate_monthly_df = macro_canada_retail_rate_monthly()
    print(macro_canada_retail_rate_monthly_df)

    macro_canada_bank_rate_df = macro_canada_bank_rate()
    print(macro_canada_bank_rate_df)

    macro_canada_core_cpi_yearly_df = macro_canada_core_cpi_yearly()
    print(macro_canada_core_cpi_yearly_df)

    macro_canada_core_cpi_monthly_df = macro_canada_core_cpi_monthly()
    print(macro_canada_core_cpi_monthly_df)

    macro_canada_cpi_yearly_df = macro_canada_cpi_yearly()
    print(macro_canada_cpi_yearly_df)

    macro_canada_cpi_monthly_df = macro_canada_cpi_monthly()
    print(macro_canada_cpi_monthly_df)

    macro_canada_gdp_monthly_df = macro_canada_gdp_monthly()
    print(macro_canada_gdp_monthly_df)
