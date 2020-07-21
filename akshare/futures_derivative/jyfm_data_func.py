# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/12/6 0:17
Desc: 交易法门-数据

交易法门-数据-黑色系
交易法门-数据-黑色系-焦煤
交易法门-数据-黑色系-焦炭

交易法门-数据-农产品
交易法门-数据-农产品-美豆
交易法门-数据-农产品-豆粕
交易法门-数据-农产品-豆油
交易法门-数据-农产品-棕榈
交易法门-数据-农产品-白糖
"""
import requests
import pandas as pd

from akshare.futures_derivative.cons import (
    # 交易法门-数据-农产品
    jyfm_data_usa_bean_name_url_dict,  # 交易法门-数据-农产品-美豆
    jyfm_data_soybean_meal_name_url_dict,  # 交易法门-数据-农产品-豆粕
    jyfm_data_soybean_oil_name_url_dict,  # 交易法门-数据-农产品-豆油
    jyfm_data_palm_name_url_dict,  # 交易法门-数据-农产品-棕榈
    jyfm_data_sugar_name_url_dict,  # 交易法门-数据-农产品-白糖
    # 交易法门-数据-黑色系
    jyfm_data_cocking_coal_url_dict,  # 交易法门-数据-黑色系-焦煤
    jyfm_data_coke_url_dict,  # 交易法门-数据-黑色系-焦炭
)
from akshare.futures_derivative.jyfm_login_func import jyfm_login


# 农产品
def jyfm_data_usa_bean(indicator="美豆种植进度", headers=""):
    """
    交易法门-数据-农产品-美豆
    :param indicator: ["美豆种植进度", "美豆出苗率", "美豆开花率", "美豆优良率", "美豆收割进度", "美豆出口情况"]
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: result
    :rtype: pandas.DataFrame
    """
    res = requests.get(jyfm_data_usa_bean_name_url_dict[indicator], headers=headers,)
    return pd.DataFrame(res.json())


def jyfm_data_soybean_meal(indicator="豆粕月度产量", headers=""):
    """
    交易法门-数据-农产品-豆粕
    :param indicator: ["大豆月度进口", "大豆原料库存", "压榨开工率", "企业压榨利润",
    "豆粕月度产量", "豆粕每日成交", "豆粕周度库存", "豆粕平衡表"]
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: result
    :rtype: pandas.DataFrame
    """
    res = requests.get(
        jyfm_data_soybean_meal_name_url_dict[indicator], headers=headers,
    )
    return pd.DataFrame(res.json())


def jyfm_data_soybean_oil(indicator="豆油年度产能", headers=""):
    """
    交易法门-数据-农产品-豆油
    :param indicator: ["豆油年度产能", "压榨装置开工率", "油厂周度产量", "豆油现货成交",
    "豆油商业库存", "豆油毛利润", "豆油月度产量", "豆油月度进口", "豆油月度消费", "豆油月度出口", "豆油月度库存"]
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: result
    :rtype: pandas.DataFrame
    """
    res = requests.get(jyfm_data_soybean_oil_name_url_dict[indicator], headers=headers,)
    return pd.DataFrame(res.json())


def jyfm_data_palm(indicator="马棕种植面积", headers=""):
    """
    交易法门-数据-农产品-棕榈
    :param indicator: ["马棕种植面积", "马棕FFB单产", "马棕出油率", "马棕月度产量", "马棕月度库存", "马棕月度出口"]
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: result
    :rtype: pandas.DataFrame
    """
    res = requests.get(jyfm_data_palm_name_url_dict[indicator], headers=headers,)
    return pd.DataFrame(res.json())


def jyfm_data_sugar(indicator="白糖产区库存", headers=""):
    """
    交易法门-数据-农产品-白糖
    :param indicator: ["国内种植面积", "年度产糖率", "白糖年度产销", "白糖进出口量",
    "食糖产需缺口", "白糖月度产量", "白糖月度销量", "白糖月度进口", "食糖工业库存", "白糖产区库存"]
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: result
    :rtype: pandas.DataFrame
    """
    res = requests.get(jyfm_data_sugar_name_url_dict[indicator], headers=headers,)
    return pd.DataFrame(res.json())


# 黑色系
def jyfm_data_cocking_coal(indicator="焦煤总库存", headers=""):
    """
    交易法门-数据-黑色系-焦煤
    :param indicator: ["焦煤总库存", "焦煤焦企库存-焦煤焦企库存100", "焦煤焦企库存-焦煤焦企库存230", "焦煤钢厂库存", "焦煤港口库存"]
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: result
    :rtype: pandas.DataFrame
    """
    res = requests.get(jyfm_data_cocking_coal_url_dict[indicator], headers=headers,)
    # 由于返回的数据长度不一致，先补齐再转置
    return pd.read_json(res.text, orient="index").T


def jyfm_data_coke(indicator="焦炭总库存", headers=""):
    """
    交易法门-数据-黑色系-焦炭
    :param indicator: ["焦企产能利用率-100家独立焦企产能利用率", "焦企产能利用率-230家独立焦企产能利用率",
    "焦炭日均产量-100家独立焦企焦炭日均产量", "焦炭日均产量-230家独立焦企焦炭日均产量", "焦炭总库存",
    "焦炭焦企库存-100家独立焦企焦炭库存", "焦炭焦企库存-230家独立焦企焦炭库存", "焦炭钢厂库存", "焦炭港口库存", "焦企焦化利润"]
    :type indicator: str
    :param headers: headers with cookies
    :type headers: dict
    :return: result
    :rtype: pandas.DataFrame
    """
    res = requests.get(jyfm_data_coke_url_dict[indicator], headers=headers,)
    # 由于返回的数据长度不一致，先补齐再转置
    return pd.read_json(res.text, orient="index").T


if __name__ == "__main__":
    headers = jyfm_login(account="", password="")
    # 农产品
    # 农产品-美豆
    jyfm_data_usa_bean_df = jyfm_data_usa_bean(indicator="美豆优良率", headers=headers)
    print(jyfm_data_usa_bean_df)
    # 农产品-豆粕
    jyfm_data_soybean_meal_df = jyfm_data_soybean_meal(
        indicator="豆粕月度产量", headers=headers
    )
    print(jyfm_data_soybean_meal_df)
    # 农产品-豆油
    jyfm_data_soybean_oil_df = jyfm_data_soybean_oil(
        indicator="豆油年度产能", headers=headers
    )
    print(jyfm_data_soybean_oil_df)
    # 农产品-棕榈
    jyfm_data_palm_df = jyfm_data_palm(indicator="马棕月度出口", headers=headers)
    print(jyfm_data_palm_df)
    # 农产品-白糖
    jyfm_data_sugar_df = jyfm_data_sugar(indicator="白糖产区库存", headers=headers)
    print(jyfm_data_sugar_df)

    # 黑色系
    # 黑色系-焦煤
    jyfm_data_cocking_coal_df = jyfm_data_cocking_coal(
        indicator="焦煤总库存", headers=headers
    )
    print(jyfm_data_cocking_coal_df)
    # 黑色系-焦炭
    jyfm_data_coke_df = jyfm_data_coke(indicator="焦炭总库存", headers=headers)
    print(jyfm_data_coke_df)
