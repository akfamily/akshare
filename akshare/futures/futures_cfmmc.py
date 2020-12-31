# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/12/30 16:37
Desc: 中国期货市场监控中心-指数
http://index.cfmmc.com/index/views/index.html
"""
from io import BytesIO

import pandas as pd
import requests
from bs4 import BeautifulSoup


def futures_index_dict() -> dict:
    """
    name and code map
    :return: name to code
    :rtype: dict
    """
    url = "http://index.cfmmc.com/index/views/index.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    name_list = [
        item.text.strip()
        for item in soup.find(attrs={"class": "down_box"}).find_all("b")[1:]
    ]
    code_list = [
        item["indexcode"]
        for item in soup.find(attrs={"class": "down_box"}).find_all("b")[1:]
    ]
    return dict(zip(name_list, code_list))


def futures_index_cfmmc(
    index_name: str = "商品综合指数",
    start_date: str = "2010-01-01",
    end_date: str = "2020-04-06",
) -> pd.DataFrame:
    """
    中国期货市场监控中心-各类指数数据
    http://index.cfmmc.com/index/views/index.html
    :param index_name: 指数名称 大类 {"商品期货指数", "农产品期货指数", "商品期货指数", "工业品期货指数", "商品综合指数"}, refer futures_index_dict
    :type index_name: str
    :param start_date: default "2010-01-01"
    :type start_date: str
    :param end_date: default "2020-04-06"
    :type end_date: str
    :return: index data frame
    :rtype: pandas.DataFrame
    """
    futures_index_map = futures_index_dict()
    url = "http://index.cfmmc.com/servlet/indexAction"
    params = {
        "function": "DowladIndex",
        "start": start_date,
        "end": end_date,
        "code": futures_index_map[index_name],
        "codeName": index_name,
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_excel(BytesIO(r.content))
    return temp_df


if __name__ == "__main__":
    futures_index_dict_temp = futures_index_dict()
    futures_index_df = pd.DataFrame.from_dict(
        futures_index_dict_temp, orient="index", columns=["index_code"]
    )
    print(futures_index_df)
    futures_index_cfmmc_df = futures_index_cfmmc(
        index_name="林木综合指数", start_date="2010-01-01", end_date="2020-12-30"
    )
    print(futures_index_cfmmc_df)
