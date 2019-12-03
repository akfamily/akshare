# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/2 22:24
contact: jindaxiang@163.com
desc: 获取微博指数
"""
import re
import datetime

import pandas as pd
import requests
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 显示中文标签

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Referer": "http://data.weibo.com/index/newindex",
    "Accept": "application/json",
    "Origin": "https://data.weibo.com",
}


def _get_items(word="股票"):
    url = "https://data.weibo.com/index/ajax/newindex/searchword"
    payload = {"word": word}
    res = requests.post(url, data=payload, headers=headers)
    return {word: re.findall(r"\d+", res.json()["html"])[0]}


def _get_index_data(wid, time_type):
    url = "http://data.weibo.com/index/ajax/newindex/getchartdata"
    data = {
        "wid": wid,
        "dateGroup": time_type,
    }
    res = requests.get(url, params=data, headers=headers)
    json_df = res.json()
    data = {
        "index": json_df["data"][0]["trend"]["x"],
        "value": json_df["data"][0]["trend"]["s"],
    }
    df = pd.DataFrame(data)
    return df


def _process_index(index):
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


def weibo_index(word, time_type):
    """
    :param word: str
    :param time_type: str 1hour, 1day, 1month, 3month
    :return:
    """
    dict_keyword = _get_items(word)
    df_list = []
    for keyword, wid in dict_keyword.items():
        df = _get_index_data(wid, time_type)
        if df is not None:
            df.columns = ["index", keyword]
            df["index"] = df["index"].apply(lambda x: _process_index(x))
            df.set_index("index", inplace=True)
            df_list.append(df)
    if len(df_list) > 0:
        df = pd.concat(df_list, axis=1)
        df.index = pd.to_datetime(df.index, format="%Y%m%d")
        return df


if __name__ == "__main__":
    df_index = weibo_index(word="螺纹钢", time_type="3month")
    print(df_index)
    df_index.plot()
    plt.show()
