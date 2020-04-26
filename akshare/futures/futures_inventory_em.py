# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/26 13:58
Desc: 东方财富网-数据中心-期货库存数据
http://data.eastmoney.com/ifdata/kcsj.html
"""
import demjson
import pandas as pd
import requests
from bs4 import BeautifulSoup


def futures_inventory_em(exchange: str = "上海期货交易所", symbol: str = "沪铝") -> pd.DataFrame:
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

    temp_text = soup.find_all("script", attrs={"type": "text/javascript"})[8].text
    temp_dict = demjson.decode(temp_text[temp_text.find('cv= ')+4:temp_text.rfind(';\r\n;')])
    temp_item = [item.get("data") for item in temp_dict if item.get("value") == exchange_dict[exchange]][0]
    symbol_dict = {item[1]: item[0] for item in temp_item}

    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "QHKC",
        "sty": "QHKCMX",
        "mkt": exchange_dict[exchange],
        "code": symbol_dict[symbol],
        "p": "1",
        "ps": "50",
        "js": "window.ret={pages:(pc),data:[(x)]}",
        "_": "1587887394138",
    }
    r = requests.get(url, params=params)
    data_text = r.text

    data_json = demjson.decode(data_text[data_text.find("{"):])
    temp_df = pd.DataFrame(data_json["data"]).iloc[:, 0].str.split(",", expand=True)
    temp_df.columns = ["日期", "库存", "增减"]
    return temp_df


if __name__ == "__main__":
    futures_inventory_em_df = futures_inventory_em(exchange="大连商品交易所", symbol="豆粕")
    print(futures_inventory_em_df)
