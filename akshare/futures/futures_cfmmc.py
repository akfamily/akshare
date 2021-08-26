# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/8/26 15:37
Desc: 中证商品指数
http://www.cscidx.com/index.html
"""
from io import BytesIO

import pandas as pd
import requests


def futures_index_cscidx_map() -> dict:
    """
    name and code map
    :return: name to code
    :rtype: dict
    """
    url = 'http://www.cscidx.com/cscidx/csciAction/getCsciIndexMap'
    params = {
        'r': '0.08644997232349438'
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Content-Length': '45',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.cscidx.com',
        'Origin': 'http://www.cscidx.com',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.cscidx.com/cscidx/quote1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    r = requests.post(url, params=params, headers=headers)
    r.text

    url = "http://www.cscidx.com/cscidx/csciAction/loadTimeData"
    params = {
        'r': '0.08644997232349438'
    }
    payload = {
        'indexCode': '606004.CSCI',
        'indexType': '0',
        'pointer': 'all',
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Content-Length': '45',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.cscidx.com',
        'Origin': 'http://www.cscidx.com',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.cscidx.com/cscidx/quote1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    r = requests.post(url, params=params, json=payload, headers=headers)
    r.json()
    return None


def futures_index_cscidx(
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
    futures_index_map = futures_index_cscidx_map()
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
    futures_index_dict_temp = futures_index_cscidx_map()
    futures_index_df = pd.DataFrame.from_dict(
        futures_index_dict_temp, orient="index", columns=["index_code"]
    )
    print(futures_index_df)
    futures_index_cfmmc_df = futures_index_cscidx(
        index_name="林木综合指数", start_date="2010-01-01", end_date="2020-12-30"
    )
    print(futures_index_cfmmc_df)
