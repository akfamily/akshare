# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/6 20:37
Desc:
商品期货指数
农产品期货指数
商品期货指数
工业品期货指数
商品综合指数
http://index.cfmmc.com/index/views/index.html
"""
import requests
import pandas as pd
from io import BytesIO


def futures_index_cfmmc(index_name="商品综合指数", start_date="2010-01-01", end_date="2020-04-06"):
    """
    中国期货市场监控中心
    http://index.cfmmc.com/index/views/index.html
    :param index_name: 指数名称 大类 {"商品期货指数", "农产品期货指数", "商品期货指数", "工业品期货指数", "商品综合指数"}
    :type index_name: str
    :param start_date: default "2010-01-01"
    :type start_date: str
    :param end_date: default "2020-04-06"
    :type end_date: str
    :return: index data frame
    :rtype: pandas.DataFrame
    """
    url = "http://index.cfmmc.com/servlet/indexAction"
    params = {
        "function": "DowladIndex",
        "start": start_date,
        "end": end_date,
        "code": "CCFI",
        "codeName": index_name,
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_excel(BytesIO(r.content))
    return temp_df


if __name__ == '__main__':
    futures_index_cfmmc_df = futures_index_cfmmc(index_name="商品综合指数", start_date="2010-01-01", end_date="2020-04-06")
    print(futures_index_cfmmc_df)
