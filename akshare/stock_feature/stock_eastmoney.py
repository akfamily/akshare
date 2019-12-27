# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/27 18:02
contact: jindaxiang@163.com
desc: 
"""
import json

import requests
import pandas as pd


def _get_page_num():
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


def stock_em_jgdy():
    url = "http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx"
    page_num = _get_page_num()
    temp_df = pd.DataFrame()
    for page in range(1, page_num+1):
        print(page)
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


if __name__ == '__main__':
    df = stock_em_jgdy()
    print(df)
