# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/2 20:24
Desc: 东方财富-数据中心-中国油价
http://data.eastmoney.com/cjsj/oil_default.html
"""
import json

import pandas as pd
import requests


def energy_oil_hist() -> pd.DataFrame:
    """
    汽柴油历史调价信息
    http://data.eastmoney.com/cjsj/oil_default.html
    :return: 汽柴油历史调价数
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter.eastmoney.com/api/data/get"
    params = {
        "type": "RPTA_WEB_YJ_BD",
        "sty": "ALL",
        "source": "WEB",
        "p": "1",
        "ps": "5000",
        "st": "dim_date",
        "sr": "-1",
        "var": "OxGINxug",
        "rt": "52861006",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{"): -1])
    data_df = pd.DataFrame(data_json["result"]["data"])
    data_df.columns = ["日期", "汽油价格", "柴油价格", "汽油涨幅", "柴油涨幅"]
    return data_df


def energy_oil_detail(date: str = "2020-03-19") -> pd.DataFrame:
    """
    地区油价
    http://data.eastmoney.com/cjsj/oil_default.html
    :param date: call function: energy_oil_hist to get the date point
    :type date: str
    :return: oil price at specific date
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter.eastmoney.com/api/data/get"
    params = {
        "type": "RPTA_WEB_YJ_JH",
        "sty": "ALL",
        "source": "WEB",
        "p": "1",
        "ps": "5000",
        "st": "cityname",
        "sr": "1",
        "filter": f'(dim_date="{date}")',
        "var": "todayPriceData",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{"): -1])
    data_df = pd.DataFrame(data_json["result"]["data"]).iloc[:, 1:]
    return data_df


if __name__ == "__main__":
    energy_oil_hist_df = energy_oil_hist()
    print(energy_oil_hist_df)
    energy_oil_detail_df = energy_oil_detail(date="2020-09-19")
    print(energy_oil_detail_df)
