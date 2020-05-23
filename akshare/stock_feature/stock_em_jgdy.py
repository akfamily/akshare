# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/27 18:02
contact: jindaxiang@163.com
desc: 东方财富网-数据中心-特色数据-机构调研
东方财富网-数据中心-特色数据-机构调研-机构调研统计: http://data.eastmoney.com/jgdy/tj.html
东方财富网-数据中心-特色数据-机构调研-机构调研详细: http://data.eastmoney.com/jgdy/xx.html
"""
import json

import pandas as pd
import requests
from tqdm import tqdm


# pd.set_option('display.max_columns', 500)


def _get_page_num_tj():
    """
    东方财富网-数据中心-特色数据-机构调研-机构调研统计
    http://data.eastmoney.com/jgdy/tj.html
    :return: int 获取 机构调研统计 的总页数
    """
    url = "http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx"
    params = {
        "pagesize": "5000",
        "page": "2",
        "js": "var sGrabtEb",
        "param": "",
        "sortRule": "-1",
        "sortType": "0",
        "rt": "52581365",
    }
    res = requests.get(url, params=params)
    data_json = json.loads(res.text[res.text.find("={")+1:])
    return data_json["pages"]


def _get_page_num_detail():
    """
    东方财富网-数据中心-特色数据-机构调研-机构调研详细
    http://data.eastmoney.com/jgdy/xx.html
    :return: int 获取 机构调研详细 的总页数
    """
    url = "http://data.eastmoney.com/DataCenter_V3/jgdy/xx.ashx"
    params = {
        "pagesize": "5000",
        "page": "1",
        "js": "var SZGpIhFb",
        "param": "",
        "sortRule": "-1",
        "sortType": "0",
        "rt": "52581407",
    }
    res = requests.get(url, params=params)
    data_json = json.loads(res.text[res.text.find("={")+1:])
    return data_json["pages"]


def stock_em_jgdy_tj():
    """
    东方财富网-数据中心-特色数据-机构调研-机构调研统计
    http://data.eastmoney.com/jgdy/tj.html
    :return: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx"
    page_num = _get_page_num_tj()
    temp_df = pd.DataFrame()
    for page in tqdm(range(1, page_num+1)):
        params = {
            "pagesize": "5000",
            "page": str(page),
            "js": "var sGrabtEb",
            "param": "",
            "sortRule": "-1",
            "sortType": "0",
            "rt": "52581365",
        }
        res = requests.get(url, params=params)
        data_json = json.loads(res.text[res.text.find("={")+1:])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    return temp_df


def stock_em_jgdy_detail():
    """
    东方财富网-数据中心-特色数据-机构调研-机构调研详细
    http://data.eastmoney.com/jgdy/xx.html
    :return: 机构调研详细
    :rtype: pandas.DataFrame
    """
    url = "http://data.eastmoney.com/DataCenter_V3/jgdy/xx.ashx"
    page_num = _get_page_num_detail()
    temp_df = pd.DataFrame()
    for page in tqdm(range(1, page_num+1)):
        params = {
            "pagesize": "5000",
            "page": str(page),
            "js": "var SZGpIhFb",
            "param": "",
            "sortRule": "-1",
            "sortType": "0",
            "rt": "52581407",
        }
        res = requests.get(url, params=params)
        data_json = json.loads(res.text[res.text.find("={")+1:])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    return temp_df


if __name__ == '__main__':
    stock_em_jgdy_tj_df = stock_em_jgdy_tj()
    print(stock_em_jgdy_tj_df)
    stock_em_jgdy_detail_df = stock_em_jgdy_detail()
    print(stock_em_jgdy_detail_df)
