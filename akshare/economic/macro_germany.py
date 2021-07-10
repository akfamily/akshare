# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/7/9 14:05
Desc: 东方财富-德国-经济数据
"""
import demjson
import pandas as pd
import requests


# 东方财富-德国-经济数据-IFO商业景气指数
def macro_germany_ifo() -> pd.DataFrame:
    """
    IFO商业景气指数
    http://data.eastmoney.com/cjsj/foreign_1_0.html
    :return: IFO商业景气指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "1",
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


# 东方财富-德国-经济数据-消费者物价指数月率终值
def macro_germany_cpi_monthly() -> pd.DataFrame:
    """
    消费者物价指数月率终值
    http://data.eastmoney.com/cjsj/foreign_1_1.html
    :return: 消费者物价指数月率终值
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "1",
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


# 东方财富-德国-经济数据-消费者物价指数年率终值
def macro_germany_cpi_yearly() -> pd.DataFrame:
    """
    消费者物价指数年率终值
    http://data.eastmoney.com/cjsj/foreign_1_2.html
    :return: 消费者物价指数年率终值
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "1",
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


# 东方财富-德国-经济数据-贸易帐(季调后)
def macro_germany_trade_adjusted() -> pd.DataFrame:
    """
    贸易帐(季调后)
    http://data.eastmoney.com/cjsj/foreign_1_3.html
    :return: 贸易帐(季调后)
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "1",
        "stat": "3",
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
    temp_df["前值"] = pd.to_numeric(temp_df["前值"]) * 10
    temp_df["现值"] = pd.to_numeric(temp_df["现值"]) * 10
    return temp_df


# 东方财富-德国-经济数据-GDP
def macro_germany_gdp() -> pd.DataFrame:
    """
    GDP
    http://data.eastmoney.com/cjsj/foreign_1_4.html
    :return: GDP
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "1",
        "stat": "4",
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


# 东方财富-德国-经济数据-实际零售销售月率
def macro_germany_retail_sale_monthly() -> pd.DataFrame:
    """
    实际零售销售月率
    http://data.eastmoney.com/cjsj/foreign_1_5.html
    :return: 实际零售销售月率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "1",
        "stat": "5",
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


# 东方财富-德国-经济数据-实际零售销售年率
def macro_germany_retail_sale_yearly() -> pd.DataFrame:
    """
    实际零售销售年率
    http://data.eastmoney.com/cjsj/foreign_1_6.html
    :return: 实际零售销售年率
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "1",
        "stat": "6",
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


# 东方财富-德国-经济数据-ZEW 经济景气指数
def macro_germany_zew() -> pd.DataFrame:
    """
    ZEW 经济景气指数
    http://data.eastmoney.com/cjsj/foreign_1_7.html
    :return: ZEW 经济景气指数
    :rtype: pandas.DataFrame
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "1",
        "stat": "7",
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


if __name__ == "__main__":
    macro_germany_ifo_df = macro_germany_ifo()
    print(macro_germany_ifo_df)

    macro_germany_cpi_monthly_df = macro_germany_cpi_monthly()
    print(macro_germany_cpi_monthly_df)

    macro_germany_cpi_yearly_df = macro_germany_cpi_yearly()
    print(macro_germany_cpi_yearly_df)

    macro_germany_trade_adjusted_df = macro_germany_trade_adjusted()
    print(macro_germany_trade_adjusted_df)

    macro_germany_gdp_df = macro_germany_gdp()
    print(macro_germany_gdp_df)

    macro_germany_retail_sale_monthly_df = macro_germany_retail_sale_monthly()
    print(macro_germany_retail_sale_monthly_df)

    macro_germany_retail_sale_yearly_df = macro_germany_retail_sale_yearly()
    print(macro_germany_retail_sale_yearly_df)

    macro_germany_zew_df = macro_germany_zew()
    print(macro_germany_zew_df)
