#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/9/11 22:51
Desc: 财联社-今日快讯
https://www.cls.cn/searchPage?keyword=%E5%BF%AB%E8%AE%AF&type=all
"""
import pandas as pd
import requests


def stock_zh_a_alerts_cls() -> pd.DataFrame:
    """
    财联社-今日快讯
    https://www.cls.cn/searchPage?keyword=%E5%BF%AB%E8%AE%AF&type=all
    :return: 财联社-今日快讯
    :rtype: pandas.DataFrame
    """
    url = "https://www.cls.cn/api/sw"
    params = {"app": "CailianpressWeb", "os": "web", "sv": "7.5.5"}
    headers = {
        "Host": "www.cls.cn",
        "Connection": "keep-alive",
        "Content-Length": "112",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://www.cls.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    payload = {
        "type": "telegram",
        "keyword": "快讯",
        "page": 0,
        "rn": 10000,
        "os": "web",
        "sv": "7.2.2",
        "app": "CailianpressWeb",
    }
    r = requests.post(url, headers=headers, params=params, json=payload)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["telegram"]["data"])
    temp_df = temp_df[["descr", "time"]]
    temp_df["descr"] = temp_df["descr"].astype(str).str.replace("</em>", "")
    temp_df["descr"] = temp_df["descr"].str.replace("<em>", "")
    temp_df["time"] = pd.to_datetime(temp_df["time"], unit="s").dt.date
    temp_df.columns = ["快讯信息", "时间"]
    temp_df = temp_df[["时间", "快讯信息"]]
    return temp_df


if __name__ == "__main__":
    stock_zh_a_alerts_cls_df = stock_zh_a_alerts_cls()
    print(stock_zh_a_alerts_cls_df)
