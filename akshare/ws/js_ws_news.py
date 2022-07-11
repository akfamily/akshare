#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/4/25 17:47
Desc: 金十数据-市场快讯
https://www.jin10.com/
"""
import pandas as pd
import requests


def js_news(timestamp: str = "2021-06-05 20:50:18") -> pd.DataFrame:
    """
    金十数据-市场快讯
    https://www.jin10.com/
    :param timestamp: choice of {'最新资讯', '最新数据'}
    :type timestamp: str
    :return: 市场快讯
    :rtype: pandas.DataFrame
    """
    url = "https://flash-api.jin10.com/get_flash_list"
    params = {
        "channel": "-8200",
        "vip": "1",
        "t": "1625623640730",
        "max_time": timestamp,
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "handleerror": "true",
        "origin": "https://www.jin10.com",
        "pragma": "no-cache",
        "referer": "https://www.jin10.com/",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "x-app-id": "bVBF4FyRTn5NJF5n",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_list = []
    for item in temp_df["data"]:
        if "content" in item.keys():
            temp_list.append(item["content"])
        elif "pic" in item.keys():
            temp_list.append(item["pic"])
        else:
            temp_list.append("-")
    temp_df = pd.DataFrame([temp_df["time"].to_list(), temp_list]).T
    temp_df.columns = ["datetime", "content"]
    temp_df.sort_values(['datetime'], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


if __name__ == "__main__":
    js_news_df = js_news(timestamp="2022-04-25 17:57:18")
    print(js_news_df)
