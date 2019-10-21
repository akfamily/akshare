# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/21 12:08
contact: jindaxiang@163.com
desc: 获取金十数据-数据中心-中国-中国CPI年率报告
"""
import json
import time

import pandas as pd
import requests

from akshare.economic.cons import (JS_CHINA_CPI_YEARLY_URL,
                                   JS_CHINA_CPI_MONTHLY_URL,
                                   JS_CHINA_M2_YEARLY_URL)


def get_china_yearly_cpi():
    """
    获取中国年度CPI数据, 数据区间从19860201-至今
    :return: pandas.Series
    1986-02-01    7.1
    1986-03-01    7.1
    1986-04-01    7.1
    1986-05-01    7.1
    1986-06-01    7.1
                 ...
    2019-07-10    2.7
    2019-08-09    2.8
    2019-09-10    2.8
    2019-10-15      3
    2019-11-09      0
    """
    t = time.time()
    res = requests.get(JS_CHINA_CPI_YEARLY_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国CPI年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    cpi_df = value_df["今值(%)"]
    cpi_df.name = "cpi"
    return cpi_df


def get_china_monthly_cpi():
    """
    获取中国月度CPI数据, 数据区间从19960201-至今
    :return: pandas.Series
    1996-02-01     2.1
    1996-03-01     2.3
    1996-04-01     0.6
    1996-05-01     0.7
    1996-06-01    -0.5
                  ...
    2019-07-10    -0.1
    2019-08-09     0.4
    2019-09-10     0.7
    2019-10-15     0.9
    2019-11-09       0
    """
    t = time.time()
    res = requests.get(JS_CHINA_CPI_MONTHLY_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国CPI月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    cpi_df = value_df["今值(%)"]
    cpi_df.name = "cpi"
    return cpi_df


def get_china_yearly_m2():
    """
    获取中国年度M2数据, 数据区间从19980201-至今
    :return: pandas.Series
    1998-02-01    17.4
    1998-03-01    16.7
    1998-04-01    15.4
    1998-05-01    14.6
    1998-06-01    15.5
                  ...
    2019-09-11     8.2
    2019-09-13       0
    2019-10-14       0
    2019-10-15     8.4
    2019-10-17       0
    """
    t = time.time()
    res = requests.get(JS_CHINA_M2_YEARLY_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["中国M2货币供应年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    cpi_df = value_df["今值(%)"]
    cpi_df.name = "m2"
    return cpi_df


if __name__ == "__main__":
    df = get_china_yearly_cpi()
    print(df)
    df = get_china_monthly_cpi()
    print(df)
    df = get_china_yearly_m2()
    print(df)


