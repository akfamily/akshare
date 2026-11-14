#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/14 20:00
Desc: 金十数据-美国商品期货交易委员会 CFTC 持仓报告与芝加哥商业交易所贵金属成交量
https://datacenter.jin10.com/reportType/dc_cftc_nc_report
"""

import ast
import time
import pandas as pd
from akshare.utils import http


def futures_cftc_currency_noncommercial_holding_js() -> pd.DataFrame:
    """
    美国商品期货交易委员会CFTC外汇类非商业持仓报告，数据区间从 19830107-至今
    https://datacenter.jin10.com/reportType/dc_cftc_nc_report
    :return: 美国商品期货交易委员会CFTC外汇类非商业持仓报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {"_": str(int(round(t * 1000)))}
    r = http.get(
        url="https://cdn.jin10.com/data_center/reports/cftc_4.json", params=params
    )
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df = temp_df.fillna(value="[0, 0, 0]")
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(
                lambda x: ast.literal_eval(str(x))[i]
            )
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat(objs=[big_df, inner_temp_df], axis=1)
    big_df = big_df.astype("float")
    big_df = big_df.reset_index()
    big_df = big_df.rename(columns={"index": "日期"})
    big_df = big_df.sort_values(by=["日期"], ignore_index=True)
    return big_df


def futures_cftc_commodity_noncommercial_holding_js() -> pd.DataFrame:
    """
    美国商品期货交易委员会CFTC商品类非商业持仓报告，数据区间从 19830107-至今
    https://datacenter.jin10.com/reportType/dc_cftc_c_report
    :return: 美国商品期货交易委员会CFTC外汇类非商业持仓报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {"_": str(int(round(t * 1000)))}
    r = http.get(
        url="https://cdn.jin10.com/data_center/reports/cftc_2.json", params=params
    )
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df = temp_df.fillna(value="[0, 0, 0]")
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(
                lambda x: ast.literal_eval(str(x))[i]
            )
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat(objs=[big_df, inner_temp_df], axis=1)
    big_df = big_df.astype("float")
    big_df = big_df.reset_index()
    big_df = big_df.rename(columns={"index": "日期"})
    big_df = big_df.sort_values(by=["日期"], ignore_index=True)
    return big_df


def futures_cftc_currency_commercial_holding_js() -> pd.DataFrame:
    """
    美国商品期货交易委员会CFTC外汇类商业持仓报告，数据区间从 19860115-至今
    https://datacenter.jin10.com/reportType/dc_cftc_merchant_currency
    :return: 美国商品期货交易委员会CFTC外汇类商业持仓报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {"_": str(int(round(t * 1000)))}
    r = http.get(
        url="https://cdn.jin10.com/data_center/reports/cftc_3.json", params=params
    )
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df = temp_df.fillna(value="[0, 0, 0]")
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(
                lambda x: ast.literal_eval(str(x))[i]
            )
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat(objs=[big_df, inner_temp_df], axis=1)
    big_df = big_df.astype("float")
    big_df = big_df.reset_index()
    big_df = big_df.rename(columns={"index": "日期"})
    big_df = big_df.sort_values(by=["日期"], ignore_index=True)
    return big_df


def futures_cftc_commodity_commercial_holding_js() -> pd.DataFrame:
    """
    美国商品期货交易委员会CFTC商品类商业持仓报告，数据区间从 19860115-至今
    https://datacenter.jin10.com/reportType/dc_cftc_merchant_goods
    :return: 美国商品期货交易委员会CFTC商品类商业持仓报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {"_": str(int(round(t * 1000)))}
    r = http.get(
        url="https://cdn.jin10.com/data_center/reports/cftc_1.json", params=params
    )
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df = temp_df.fillna(value="[0, 0, 0]")
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(
                lambda x: ast.literal_eval(str(x))[i]
            )
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat(objs=[big_df, inner_temp_df], axis=1)
    big_df = big_df.astype("float")
    big_df = big_df.reset_index()
    big_df = big_df.rename(columns={"index": "日期"})
    big_df = big_df.sort_values(by=["日期"], ignore_index=True)
    return big_df


def futures_cme_metal_volume_js():
    """
    CME-贵金属，数据区间从 20180405-至今
    https://datacenter.jin10.com/org
    :return: CME-贵金属
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {"_": str(int(round(t * 1000)))}
    r = http.get(
        url="https://cdn.jin10.com/data_center/reports/cme_3.json", params=params
    )
    json_data = r.json()
    big_df = pd.DataFrame()
    for item in json_data["values"].keys():
        temp_df = pd.DataFrame(json_data["values"][item])
        temp_df["日期"] = item
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)

    big_df.columns = ["pz", "tc", "-", "-", "-", "成交量", "-", "-", "日期"]
    big_df["品种"] = big_df["pz"] + "-" + big_df["tc"]
    big_df = big_df[["日期", "品种", "成交量"]]
    big_df = big_df.sort_values(["日期"], ignore_index=True)
    return big_df


if __name__ == "__main__":
    futures_cftc_currency_noncommercial_holding_js_df = (
        futures_cftc_currency_noncommercial_holding_js()
    )
    print(futures_cftc_currency_noncommercial_holding_js_df)

    futures_cftc_commodity_noncommercial_holding_js_df = (
        futures_cftc_commodity_noncommercial_holding_js()
    )
    print(futures_cftc_commodity_noncommercial_holding_js_df)

    futures_cftc_currency_commercial_holding_js_df = (
        futures_cftc_currency_commercial_holding_js()
    )
    print(futures_cftc_currency_commercial_holding_js_df)

    futures_cftc_commodity_commercial_holding_js_df = (
        futures_cftc_commodity_commercial_holding_js()
    )
    print(futures_cftc_commodity_commercial_holding_js_df)

    futures_cme_metal_volume_js_df = futures_cme_metal_volume_js()
    print(futures_cme_metal_volume_js_df)
