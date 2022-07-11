#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/5/9 16:16
Desc: 浙江省排污权交易指数
https://zs.zjpwq.net/
"""
import requests
import pandas as pd


def index_eri() -> pd.DataFrame:
    """
    浙江省排污权交易指数
    https://zs.zjpwq.net
    :return: 浙江省排污权交易指数
    :rtype: pandas.DataFrame
    """
    url = "https://zs.zjpwq.net/zhe-jiang-pwq-webapi/indexData"
    params = {
        "indexId": "1",
        "areaCode": "330000",
        "cycle": "MONTH",
        "structCode": "01",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    del temp_df["id"]
    del temp_df["indexId"]
    del temp_df["stageId"]
    del temp_df["structCode"]
    del temp_df["areaCode"]
    del temp_df["rawValue"]
    temp_df.columns = [
        "value",
        "date",
    ]
    temp_df = temp_df[
        [
            "date",
            "value",
        ]
    ]
    big_df = temp_df
    url = "https://zs.zjpwq.net/zhe-jiang-pwq-webapi/rawValueStatistics"
    params = {
        "orderBy": "-date",
        "pageSize": "1000",
        "quotaType": "0",
        "index": "TOTAL_QUANTITY",
        "areaCode": "330000",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    del temp_df["id"]
    del temp_df["quotaType"]
    del temp_df["index"]
    temp_df.columns = [
        "date",
        "value",
        "update",
    ]
    big_df = big_df.merge(temp_df, on="date")
    big_df.columns = [
        "日期",
        "交易指数",
        "成交量",
        "更新时间",
    ]
    return big_df


if __name__ == "__main__":
    index_eri_df = index_eri()
    print(index_eri_df)
