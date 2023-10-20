#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/10/20 16:30
Desc: 微博指数
https://data.weibo.com/
"""
import datetime
import re

import pandas as pd
import requests

from akshare.index.cons import index_weibo_headers


def _get_items(symbol: str = "股票") -> dict:
    """
    新浪微博-名词编码
    https://data.weibo.com/
    :param symbol: 需要查询的名词
    :type symbol: str
    :return: 名词编码
    :rtype: dict
    """
    url = "https://data.weibo.com/index/ajax/newindex/searchword"
    payload = {"word": symbol}
    r = requests.post(url, data=payload, headers=index_weibo_headers)
    temp_dict = {symbol: re.findall(pattern=r"\d+", string=r.json()["html"])[0]}
    return temp_dict


def _get_index_data(wid: str = "", time_type: str = "") -> pd.DataFrame:
    """
    新浪微博-微博指数数据
    https://data.weibo.com/
    :param wid: 名词编码
    :type wid: str
    :param time_type: 时间区间
    :type time_type: str
    :return: 微博指数数据
    :rtype: pandas.DataFrame
    """
    url = "http://data.weibo.com/index/ajax/newindex/getchartdata"
    data = {
        "wid": wid,
        "dateGroup": time_type,
    }
    r = requests.get(url, params=data, headers=index_weibo_headers)
    data_json = r.json()
    data = {
        "index": data_json["data"][0]["trend"]["x"],
        "value": data_json["data"][0]["trend"]["s"],
    }
    temp_df = pd.DataFrame(data)
    return temp_df


def _process_index(index: str = "") -> str:
    """
    新浪微博-微博指数日期处理
    https://data.weibo.com/
    :param index: 日期数据
    :type index: str
    :return: 处理后的日期数据
    :rtype: str
    """
    now = datetime.datetime.now()
    curr_year = now.year
    curr_date = "%04d%02d%02d" % (now.year, now.month, now.day)
    if "月" in index:
        tmp = index.replace("日", "").split("月")
        date = "%04d%02d%02d" % (curr_year, int(tmp[0]), int(tmp[1]))
        if date > curr_date:
            date = "%04d%02d%02d" % (curr_year - 1, int(tmp[0]), int(tmp[1]))
        return date
    return index


def index_weibo_sina(symbol: str = "python", period: str = "3month") -> pd.DataFrame:
    """
    新浪微博-微博指数
    https://data.weibo.com/index/newindex
    :param symbol: 需要查询的名词
    :type symbol: str
    :param period: 时间段; choice of {'1hour', '1day', '1month', '3month'}
    :type period: str
    :return: 微博指数
    :rtype: pandas.DataFrame
    """
    dict_keyword = _get_items(symbol)
    df_list = []
    for keyword, wid in dict_keyword.items():
        df = _get_index_data(wid, period)
        if df is not None:
            df.columns = ["index", keyword]
            df["index"] = df["index"].apply(lambda x: _process_index(x))
            df.set_index("index", inplace=True)
            df_list.append(df)
    if len(df_list) > 0:
        df = pd.concat(df_list, axis=1)
        if period == "1hour" or "1day":
            df.index = pd.to_datetime(df.index, format="mixed")
        else:
            df.index = pd.to_datetime(df.index, format="mixed")
        df.reset_index(inplace=True)
        df.columns = ["datetime", "value"]
        df["datetime"] = df["datetime"].astype(str)
        return df


if __name__ == "__main__":
    index_weibo_sina_df = index_weibo_sina(symbol="股票", period="3month")
    print(index_weibo_sina_df)
