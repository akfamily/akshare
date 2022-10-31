#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/10/14 17:00
Desc: 百度股市通-期货-新闻
https://gushitong.baidu.com/futures/ab-CJ888
"""
import pandas as pd
import requests


def futures_news_baidu(symbol: str = "AL") -> pd.DataFrame:
    """
    百度股市通-期货-新闻
    https://gushitong.baidu.com/futures/ab-CJ888
    :param symbol: 期货品种代码；大写
    :type symbol: str
    :return: 新闻
    :rtype: pandas.DataFrame
    """
    url = "https://finance.pae.baidu.com/vapi/getfuturesnews"
    params = {"code": f"{symbol}888", "pn": "0", "rn": "2000", "finClientType": "pc"}
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["Result"])
    temp_df.rename(
        columns={
            "loc": "-",
            "provider": "-",
            "source": "-",
            "publish_time": "发布时间",
            "third_url": "新闻链接",
            "title": "标题",
            "is_self_build": "-",
            "news_id": "-",
            "locate_url": "-",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "标题",
            "发布时间",
            "新闻链接",
        ]
    ]
    temp_df["发布时间"] = pd.to_datetime(temp_df["发布时间"], unit="s").dt.date
    temp_df.sort_values(["发布时间"], inplace=True, ignore_index=True)
    return temp_df


if __name__ == "__main__":
    futures_news_baidu_df = futures_news_baidu(symbol="AL")
    print(futures_news_baidu_df)
