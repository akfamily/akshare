#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/7/20 20:20
Desc: 财联社-今日快讯
https://www.cls.cn/searchPage?keyword=%E5%BF%AB%E8%AE%AF&type=all
财联社-电报
https://www.cls.cn/telegraph
"""
import pandas as pd
import requests
import time
import hashlib


def __encrypts_cls(text: str) -> str:
    """
    财联社参数加密函数
    :param text: 文本
    :type text: str
    :return: 加密后的 sign 参数
    :rtype: str
    """
    if not isinstance(text, bytes):
        text = bytes(text, "utf-8")
    sha1 = hashlib.sha1(text).hexdigest()
    md5 = hashlib.md5(sha1.encode()).hexdigest()
    return md5


def stock_zh_a_alerts_cls() -> pd.DataFrame:
    """
    财联社-今日快讯
    https://www.cls.cn/searchPage?keyword=%E5%BF%AB%E8%AE%AF&type=all
    :return: 财联社-今日快讯
    :rtype: pandas.DataFrame
    """
    url = "https://www.cls.cn/api/sw"
    params = {
        "app": "CailianpressWeb",
        "os": "web",
        "sv": "7.7.5",
    }
    r = requests.get(url, params=params)
    code = __encrypts_cls(r.url.split("?")[1])
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
        "app": "CailianpressWeb",
        "keyword": "快讯",
        "os": "web",
        "page": 0,
        "rn": 10000,
        "sv": "7.7.5",
        "type": "telegram",
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
    temp_df.sort_values(["时间"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


def stock_telegraph_cls() -> pd.DataFrame:
    """
    财联社-电报
    https://www.cls.cn/telegraph
    :return: 财联社-电报
    :rtype: pandas.DataFrame
    """
    t = time.time()
    current_time = int(t)
    url = "https://www.cls.cn/nodeapi/telegraphList"
    params = {
        "app": "CailianpressWeb",
        "category": "",
        "lastTime": current_time,
        "last_time": current_time,
        "os": "web",
        "refresh_type": "1",
        "rn": "2000",
        "sv": "7.7.5",
    }
    r = requests.get(url, params=params)
    code = __encrypts_cls(r.url.split("?")[1])
    params = {
        "app": "CailianpressWeb",
        "category": "",
        "lastTime": current_time,
        "last_time": current_time,
        "os": "web",
        "refresh_type": "1",
        "rn": "2000",
        "sv": "7.7.5",
        "sign": code,
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=utf-8",
        "Host": "www.cls.cn",
        "Pragma": "no-cache",
        "Referer": "https://www.cls.cn/telegraph",
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }
    r = requests.get(url, headers=headers, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["roll_data"])
    temp_df = temp_df[["title", "content", "ctime"]]
    temp_df["ctime"] = pd.to_datetime(
        temp_df["ctime"], unit="s", utc=True
    ).dt.tz_convert("Asia/Shanghai")
    temp_df.columns = ["标题", "内容", "发布时间"]
    temp_df.sort_values(["发布时间"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    temp_df["发布日期"] = temp_df["发布时间"].dt.date
    temp_df["发布时间"] = temp_df["发布时间"].dt.time
    return temp_df


if __name__ == "__main__":
    stock_zh_a_alerts_cls_df = stock_zh_a_alerts_cls()
    print(stock_zh_a_alerts_cls_df)

    stock_telegraph_cls_df = stock_telegraph_cls()
    print(stock_telegraph_cls_df)
