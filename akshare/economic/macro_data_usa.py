# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/21 12:08
contact: jindaxiang@163.com
desc: 获取金十数据-数据中心-美国-宏观经济
后续修改为类 --> 去除冗余代码
"""
import json
import time

import pandas as pd
import requests

from akshare.economic.cons import (JS_USA_INTEREST_RATE_URL,
                                   JS_USA_NON_FARM_URL,
                                   JS_USA_UNEMPLOYMENT_RATE_URL,
                                   JS_USA_EIA_CRUDE_URL)


def get_usa_interest_rate():
    """
    获取美联储利率决议报告, 数据区间从19820927-至今
    :return: pandas.Series
    1982-09-27    10.25
    1982-10-01       10
    1982-10-07      9.5
    1982-11-19        9
    1982-12-14      8.5
                  ...
    2019-06-20      2.5
    2019-08-01     2.25
    2019-09-19        2
    2019-10-31        0
    2019-12-12        0
    """
    t = time.time()
    res = requests.get(JS_USA_INTEREST_RATE_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国利率决议"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "interest_rate"
    return temp_df


def get_usa_non_farm():
    """
    获取美国非农就业人数报告, 数据区间从19700102-至今
    :return: pandas.Series
    1970-01-02    15.3
    1970-02-06    -6.4
    1970-03-06    12.8
    1970-04-03    14.8
    1970-05-01   -10.4
                  ...
    2019-07-05    19.3
    2019-08-02    15.9
    2019-09-06    16.8
    2019-10-04    13.6
    2019-11-01       0
    """
    t = time.time()
    res = requests.get(JS_USA_NON_FARM_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国非农就业人数"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万人)"]
    temp_df.name = "non_farm"
    return temp_df


def get_usa_unemployment_rate():
    """
    获取美国失业率报告, 数据区间从19700101-至今
    :return: pandas.Series
    1970-01-01    3.5
    1970-02-01    3.9
    1970-03-01    4.2
    1970-04-01    4.4
    1970-05-01    4.6
                 ...
    2019-07-05    3.7
    2019-08-02    3.7
    2019-09-06    3.7
    2019-10-04    3.5
    2019-11-01      0
    """
    t = time.time()
    res = requests.get(JS_USA_UNEMPLOYMENT_RATE_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国失业率"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    temp_df.name = "unemployment_rate"
    return temp_df


def get_usa_eia_crude_rate():
    """
    获取美国EIA原油库存报告, 数据区间从19950801-至今
    :return: pandas.Series
    1982-09-01   -262.6
    1982-10-01       -8
    1982-11-01    -41.3
    1982-12-01    -87.6
    1983-01-01     51.3
                  ...
    2019-10-02      310
    2019-10-09    292.7
    2019-10-16        0
    2019-10-17    928.1
    2019-10-23        0
    """
    t = time.time()
    res = requests.get(JS_USA_EIA_CRUDE_URL.format(str(int(round(t * 1000))), str(int(round(t * 1000))+90)))
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}")+1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国EIA原油库存(万桶)"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万桶)"]
    temp_df.name = "eia_crude_rate"
    return temp_df


if __name__ == "__main__":
    df = get_usa_interest_rate()
    print(df)
    df = get_usa_non_farm()
    print(df)
    df = get_usa_unemployment_rate()
    print(df)
    df = get_usa_eia_crude_rate()
    print(df)


