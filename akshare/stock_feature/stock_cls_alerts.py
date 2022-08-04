#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/8/4 14:20
Desc: 财联社-今日快讯
https://www.cls.cn/searchPage?keyword=%E5%BF%AB%E8%AE%AF&type=all
财联社-电报
https://www.cls.cn/telegraph
"""
import base64
import hashlib
import time
import warnings

import pandas as pd
import requests
from Cryptodome.Cipher import AES


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


def pkcs7_padding(data: bytes) -> bytes:
    """

    :param data:
    :type data:
    :return:
    :rtype:
    """
    if not isinstance(data, bytes):
        data = data.encode()
    pad_len = 8 - (len(data) % 8)
    data += bytes([pad_len] * pad_len)
    return data


def encrypt(key, iv, text):
    text = pkcs7_padding(text.encode("utf-8"))
    cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    return base64.b64encode(cipher.encrypt(text)).decode()


def stock_zh_a_alerts_cls() -> pd.DataFrame:
    """
    财联社-今日快讯
    https://www.cls.cn/searchPage?keyword=%E5%BF%AB%E8%AE%AF&type=all
    :return: 财联社-今日快讯
    :rtype: pandas.DataFrame
    """
    warnings.warn(
        "该接口将被移除，请使用 ak.stock_telegraph_cls() 接口替代", DeprecationWarning
    )
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
    session = requests.session()
    url = "https://m.cls.cn/telegraph"
    session.get(url)  # 获取 cookies
    params = {
        "refresh_type": "1",
        "rn": "10",
        "last_time": "",
        "app": "CailianpressWap",
        "sv": "1",
    }
    ts = pd.Timestamp(pd.Timestamp.now())
    current_time = int(ts.timestamp())
    params.update({"last_time": current_time})
    url = "https://m.cls.cn/nodeapi/telegraphs"
    r = session.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["roll_data"])
    next_time = temp_df["modified_time"].values[-1]
    n = 1
    big_df = temp_df.copy()
    while n < 15:
        params.update({"last_time": next_time})
        r = session.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["roll_data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
        next_time = temp_df["modified_time"].values[-1]
        n += 1
    big_df = big_df[["title", "content", "ctime"]]
    big_df["ctime"] = pd.to_datetime(
        big_df["ctime"], unit="s", utc=True
    ).dt.tz_convert("Asia/Shanghai")
    big_df.columns = ["标题", "内容", "发布时间"]
    big_df.sort_values(["发布时间"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    big_df["发布日期"] = big_df["发布时间"].dt.date
    big_df["发布时间"] = big_df["发布时间"].dt.time
    return big_df


if __name__ == "__main__":
    stock_zh_a_alerts_cls_df = stock_zh_a_alerts_cls()
    print(stock_zh_a_alerts_cls_df)

    stock_telegraph_cls_df = stock_telegraph_cls()
    print(stock_telegraph_cls_df)
