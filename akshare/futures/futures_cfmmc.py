# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/6 20:37
Desc: 中国期货市场监控中心-指数
http://index.cfmmc.com/index/views/index.html
"""
import requests
import pandas as pd
from io import BytesIO
from bs4 import BeautifulSoup


def futures_index_dict():
    """
    name and code map
    :return: name to code
    :rtype: dict
                 index_code
    商品期货指数         CCFI
    农产品期货指数        CAFI
    油脂油料期货指数       OOFI
    谷物期货指数         CRFI
    油脂期货指数         OIFI
    粮食期货指数         GRFI
    软商品期货指数        SOFI
    饲料期货指数         FEFI
    工业品期货指数        CIFI
    钢铁期货指数         STFI
    建材期货指数         BMFI
    能化期货指数         ECFI
    商品综合指数         CCCI
    林木综合指数         FWCI
    能化综合指数         ECCI
    金属综合指数         MECI
    农畜综合指数         ALCI
    """
    url = "http://index.cfmmc.com/index/views/index.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    name_list = [item.text.strip() for item in soup.find(attrs={"class": "down_box"}).find_all("b")[1:]]
    code_list = [item["indexcode"] for item in soup.find(attrs={"class": "down_box"}).find_all("b")[1:]]
    return dict(zip(name_list, code_list))


def futures_index_cfmmc(index_name="商品综合指数", start_date="2010-01-01", end_date="2020-04-06"):
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


if __name__ == '__main__':
    futures_index_dict_temp = futures_index_dict()
    futures_index_df = pd.DataFrame.from_dict(futures_index_dict_temp, orient="index", columns=["index_code"])
    print(futures_index_df)
    futures_index_cfmmc_df = futures_index_cfmmc(index_name="林木综合指数", start_date="2010-01-01", end_date="2020-04-06")
    print(futures_index_cfmmc_df)
