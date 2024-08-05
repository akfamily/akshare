#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/8/05 15:30
Desc: 财新网-财新数据通
https://cxdata.caixin.com/pc/
"""

import pandas as pd
import requests


def stock_news_main_cx() -> pd.DataFrame:
    """
    财新网-财新数据通
    https://cxdata.caixin.com/pc/
    :return: 特定时间表示的字典
    :rtype: pandas.DataFrame
    """
    url = "https://cxdata.caixin.com/api/dataplus/sjtPc/jxNews"
    params = {
        "pageNum": "1",
        "pageSize": "20000",
        "showLabels": "true",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["data"])
    temp_df = temp_df[["tag", "summary", "intervalTime", "pubTime", "url"]]
    temp_df.columns = ["tag", "summary", "interval_time", "pub_time", "url"]
    temp_df["pub_time"] = pd.to_datetime(
        temp_df["pub_time"], errors="coerce", unit="ms"
    ).astype(str)
    return temp_df


if __name__ == "__main__":
    stock_news_main_cx_df = stock_news_main_cx()
    print(stock_news_main_cx_df)
