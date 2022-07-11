#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/7/6 18:58
Desc: 东方财富网-数据中心-期货库存数据
http://data.eastmoney.com/ifdata/kcsj.html
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.utils import demjson


def futures_inventory_em(
    exchange: str = "上海期货交易所", symbol: str = "沪铝"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-期货库存数据
    http://data.eastmoney.com/ifdata/kcsj.html
    :param exchange: choice of {"上海期货交易所", "郑州商品交易所", "大连商品交易所"}
    :type exchange: str
    :param symbol: http://data.eastmoney.com/ifdata/kcsj.html 对应的中文名称, 如: 沪铝
    :type symbol: str
    :return: 指定交易所和指定品种的库存数据
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/ifdata/kcsj.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    temp_soup = soup.find(attrs={"id": "select_jys"}).find_all("option")
    temp_key = [item.text for item in temp_soup]
    temp_value = [item.get("value") for item in temp_soup]
    exchange_dict = dict(zip(temp_key, temp_value))
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "QHKC",
        "sty": "QHKCSX",
        "_": "1618311930407",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame(data_json)
    temp_df = temp_df.iloc[:, 0].str.split(",", expand=True)
    symbol_dict = dict(zip(temp_df.iloc[:, 3], temp_df.iloc[:, 2]))
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "QHKC",
        "sty": "QHKCMX",
        "mkt": exchange_dict[exchange],
        "code": symbol_dict[symbol],
        "stat": "1",
        "_": "1587887394138",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame(data_json).iloc[:, 0].str.split(",", expand=True)
    temp_df.columns = ["日期", "库存", "增减"]
    temp_df.sort_values(["日期"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    temp_df["库存"] = pd.to_numeric(temp_df["库存"])
    temp_df["增减"] = pd.to_numeric(temp_df["增减"])
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    return temp_df


if __name__ == "__main__":
    futures_inventory_em_df = futures_inventory_em(
        exchange="大连商品交易所", symbol="豆一"
    )
    print(futures_inventory_em_df)
