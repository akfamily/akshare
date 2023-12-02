#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/12/2 18:00
Desc: 财联社-今日快讯
https://www.cls.cn/searchPage?keyword=%E5%BF%AB%E8%AE%AF&type=all
财联社-电报
https://www.cls.cn/telegraph
"""
import pandas as pd
import requests


def stock_telegraph_cls(symbol: str = "全部") -> pd.DataFrame:
    """
    财联社-电报
    https://www.cls.cn/telegraph
    :param symbol: choice of {"全部", "重点"}
    :type symbol: str
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
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
        next_time = temp_df["modified_time"].values[-1]
        n += 1
    big_df = big_df[["title", "content", "ctime", "level"]]
    big_df["ctime"] = pd.to_datetime(
        big_df["ctime"], unit="s", utc=True
    ).dt.tz_convert("Asia/Shanghai")
    big_df.columns = ["标题", "内容", "发布时间", "等级"]
    big_df.sort_values(["发布时间"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    big_df["发布日期"] = big_df["发布时间"].dt.date
    big_df["发布时间"] = big_df["发布时间"].dt.time

    if symbol == "重点":
        big_df = big_df[(big_df['等级'] == 'B') | (big_df['等级'] == 'A')]
        big_df.reset_index(inplace=True, drop=True)
        big_df = big_df[["标题", "内容", "发布日期", "发布时间"]]
        return big_df
    else:
        big_df = big_df[["标题", "内容", "发布日期", "发布时间"]]
        return big_df


if __name__ == "__main__":
    stock_telegraph_cls_df = stock_telegraph_cls(symbol="全部")
    print(stock_telegraph_cls_df)
