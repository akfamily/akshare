# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2020/10/14 16:52
Desc: 南华期货-商品指数历史走势-收益率指数-数值-http://www.nanhua.net/nhzc/varietytrend.html
1000 点开始, 用收益率累计
目标地址: http://www.nanhua.net/ianalysis/varietyindex/index/NHCI.json?t=1574932290494
"""
import time

import requests
import pandas as pd


def num_to_str_data(str_date: int) -> str:
    """
    num to str format
    :param str_date: time of int format
    :type str_date: int
    :return: format time
    :rtype: str
    """
    str_date = str_date / 1000
    str_date = time.localtime(str_date)
    strp_time = time.strftime("%Y-%m-%d %H:%M:%S", str_date)
    return strp_time


def get_nh_list_table() -> pd.DataFrame:
    """
    南华期货-南华指数所有品种一览表
    :return: 所有品种一览表
    :rtype: pandas.DataFrame
    """
    url_name = "http://www.nanhua.net/ianalysis/plate-variety.json"
    res = requests.get(url_name)
    futures_name = [item["name"] for item in res.json()]
    futures_code = [item["code"] for item in res.json()]
    futures_exchange = [item["exchange"] for item in res.json()]
    futures_first_day = [item["firstday"] for item in res.json()]
    futures_index_cat = [item["indexcategory"] for item in res.json()]
    futures_df = pd.DataFrame(
        [
            futures_code,
            futures_exchange,
            futures_first_day,
            futures_index_cat,
            futures_name,
        ]
    ).T
    futures_df.columns = ["code", "exchange", "start_date", "category", "name"]
    return futures_df


def nh_return_index(code: str = "Y") -> pd.DataFrame:
    """
    南华期货-南华指数单品种所有历史数据
    :param code: str 通过 get_nh_list 提供
    :return: pandas.Series
    """
    if code in get_nh_list_table()["code"].tolist():
        t = time.time()
        base_url = f"http://www.nanhua.net/ianalysis/varietyindex/index/{code}.json?t={int(round(t * 1000))}"
        r = requests.get(base_url)
        date = [num_to_str_data(item[0]).split(" ")[0] for item in r.json()]
        data = [item[1] for item in r.json()]
        df_all = pd.DataFrame([date, data]).T
        df_all.columns = ["date", "value"]
        df_all.index = pd.to_datetime(df_all["date"])
        del df_all["date"]
        return df_all


if __name__ == "__main__":
    nh_return_index_df = nh_return_index()
    print(nh_return_index_df)
