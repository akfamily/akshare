# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/7/28 18:50
Desc: 东方财富-经济数据-澳大利亚
http://data.eastmoney.com/cjsj/foreign_5_0.html
"""
import pandas as pd
import requests
from akshare.utils import demjson


# 零售销售月率
def macro_australia_retail_rate_monthly():
    """
    东方财富-经济数据-澳大利亚-零售销售月率
    http://data.eastmoney.com/cjsj/foreign_5_0.html
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
        "mkt": "5",
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
def macro_australia_trade():
    """
    东方财富-经济数据-澳大利亚-贸易帐
    http://data.eastmoney.com/cjsj/foreign_5_1.html
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
        "mkt": "5",
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


# 失业率
def macro_australia_unemployment_rate():
    """
    东方财富-经济数据-澳大利亚-失业率
    http://data.eastmoney.com/cjsj/foreign_5_2.html
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
        "mkt": "5",
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


# 生产者物价指数季率
def macro_australia_ppi_quarterly():
    """
    东方财富-经济数据-澳大利亚-生产者物价指数季率
    http://data.eastmoney.com/cjsj/foreign_5_3.html
    :return: 生产者物价指数季率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "5",
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


# 消费者物价指数季率
def macro_australia_cpi_quarterly():
    """
    东方财富-经济数据-澳大利亚-消费者物价指数季率
    http://data.eastmoney.com/cjsj/foreign_5_4.html
    :return: 消费者物价指数季率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "5",
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


# 消费者物价指数年率
def macro_australia_cpi_yearly():
    """
    东方财富-经济数据-澳大利亚-消费者物价指数年率
    http://data.eastmoney.com/cjsj/foreign_5_5.html
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
        "mkt": "5",
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


# 央行公布利率决议
def macro_australia_bank_rate():
    """
    东方财富-经济数据-澳大利亚-央行公布利率决议
    http://data.eastmoney.com/cjsj/foreign_5_6.html
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
        "mkt": "5",
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


if __name__ == '__main__':
    macro_australia_retail_rate_monthly_df = macro_australia_retail_rate_monthly()
    print(macro_australia_retail_rate_monthly_df)

    macro_australia_trade_df = macro_australia_trade()
    print(macro_australia_trade_df)

    macro_australia_unemployment_rate_df = macro_australia_unemployment_rate()
    print(macro_australia_unemployment_rate_df)

    macro_australia_ppi_quarterly_df = macro_australia_ppi_quarterly()
    print(macro_australia_ppi_quarterly_df)

    macro_australia_cpi_quarterly_df = macro_australia_cpi_quarterly()
    print(macro_australia_cpi_quarterly_df)

    macro_australia_cpi_yearly_df = macro_australia_cpi_yearly()
    print(macro_australia_cpi_yearly_df)

    macro_australia_bank_rate_df = macro_australia_bank_rate()
    print(macro_australia_bank_rate_df)
