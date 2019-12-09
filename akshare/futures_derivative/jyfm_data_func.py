# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/6 0:17
contact: jindaxiang@163.com
desc: 交易法门-数据-农产品-棕榈
"""
import requests
import pandas as pd

from akshare.futures_derivative.cons import (
    jyfm_data_palm_name_url_dict,
    jyfm_data_soybean_meal_name_url_dict,
    jyfm_data_sugar_name_url_dict,
    jyfm_data_usa_bean_name_url_dict,
)
from akshare.futures_derivative.jyfm_login_func import jyfm_login

# 农产品


def jyfm_data_palm(indicator="马棕种植面积", headers=""):
    res = requests.get(jyfm_data_palm_name_url_dict[indicator], headers=headers, )
    return pd.DataFrame(res.json())


def jyfm_data_soybean_meal(indicator="大豆月度进口", headers=""):
    res = requests.get(
        jyfm_data_soybean_meal_name_url_dict[indicator], headers=headers,
    )
    return pd.DataFrame(res.json())


def jyfm_data_sugar(indicator="白糖产区库存", headers=""):
    res = requests.get(
        jyfm_data_sugar_name_url_dict[indicator], headers=headers,
    )
    return pd.DataFrame(res.json())


def jyfm_data_usa_bean(indicator="白糖产区库存", headers=""):
    res = requests.get(
        jyfm_data_usa_bean_name_url_dict[indicator], headers=headers,
    )
    return pd.DataFrame(res.json())


if __name__ == "__main__":
    headers = jyfm_login(account="", password="")
    df = jyfm_data_palm(indicator="马棕月度出口", headers=headers)
    print(df)
    df = jyfm_data_soybean_meal(indicator="大豆月度进口", headers=headers)
    print(df)
    df = jyfm_data_sugar(indicator="白糖产区库存", headers=headers)
    print(df)
    df = jyfm_data_usa_bean(indicator="美豆优良率", headers=headers)
    print(df)
