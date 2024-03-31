#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/3/31 19:00
Desc: 乘联会
https://data.cpcaauto.com/FuelMarket
汽车行业制造企业数据库
http://i.gasgoo.com/data/ranking
"""

import pandas as pd
import requests


def __car_market_cate_cpca_pifa(symbol: str = "MPV") -> pd.DataFrame:
    """
    乘联会-统计数据-车型大类
    http://data.cpcaauto.com/CategoryMarket
    :param symbol: choice of {"轿车", "MPV", "SUV", "占比"}
    :type symbol: str
    :return: 统计数据-车型大类
    :rtype: pandas.DataFrame
    """
    url = "http://data.cpcaauto.com/api/chartlist"
    params = {"charttype": "3"}
    r = requests.get(url, params=params)
    data_json = r.json()
    big_df = pd.DataFrame()
    if symbol == "MPV":
        temp_df = pd.DataFrame(data_json[0]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[0]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[1]])
            try:
                temp_current_year_list.append(item[temp_df.columns[2]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 1], temp_previous_year_df.iloc[:, 1]]
        ).T
        big_df.columns = [temp_df.columns[2], temp_df.columns[1]]
        big_df["月份"] = temp_df["month"]
        big_df = big_df[
            [
                "月份",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    elif symbol == "SUV":
        temp_df = pd.DataFrame(data_json[1]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[1]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[1]])
            try:
                temp_current_year_list.append(item[temp_df.columns[2]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 1], temp_previous_year_df.iloc[:, 1]]
        ).T
        big_df.columns = [temp_df.columns[2], temp_df.columns[1]]
        big_df["月份"] = temp_df["month"]
        big_df = big_df[
            [
                "月份",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    elif symbol == "轿车":
        temp_df = pd.DataFrame(data_json[2]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[2]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[1]])
            try:
                temp_current_year_list.append(item[temp_df.columns[2]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 1], temp_previous_year_df.iloc[:, 1]]
        ).T
        big_df.columns = [temp_df.columns[2], temp_df.columns[1]]
        big_df["月份"] = temp_df["month"]
        big_df = big_df[
            [
                "月份",
                temp_df.columns[1],
                temp_df.columns[2],
            ]
        ]
    elif symbol == "占比":
        temp_df = pd.DataFrame(data_json[3]["dataList"])
        temp_mpv_year_list = []
        temp_suv_year_list = []
        temp_jiaoche_year_list = []
        for item in data_json[3]["dataList"]:
            temp_mpv_year_list.append(item[temp_df.columns[1]])
            try:
                temp_suv_year_list.append(item[temp_df.columns[2]])
                temp_jiaoche_year_list.append(item[temp_df.columns[3]])
            except:  # noqa: E722
                continue
        temp_mpv_year_df = pd.DataFrame(temp_mpv_year_list)
        temp_suv_year_df = pd.DataFrame(temp_suv_year_list)
        temp_jiaoche_year_df = pd.DataFrame(temp_jiaoche_year_list)
        big_df = pd.DataFrame(
            [
                temp_mpv_year_df.iloc[:, 2],
                temp_suv_year_df.iloc[:, 2],
                temp_jiaoche_year_df.iloc[:, 2],
            ]
        ).T
        big_df.columns = [temp_df.columns[1], temp_df.columns[2], temp_df.columns[3]]
        big_df["月份"] = temp_df["月份"]
        big_df = big_df[
            ["月份", temp_df.columns[1], temp_df.columns[2], temp_df.columns[3]]
        ]
    return big_df


def __car_market_cate_cpca_lingshou(
    symbol: str = "狭义乘用车-累计",
) -> pd.DataFrame:
    """
    乘联会-统计数据-车型大类
    http://data.cpcaauto.com/CategoryMarket
    :param symbol: choice of {"轿车", "MPV", "SUV", "占比"}
    :type symbol: str
    :return: 统计数据-车型大类
    :rtype: pandas.DataFrame
    """
    url = "http://data.cpcaauto.com/api/chartlist"
    params = {"charttype": "3"}
    r = requests.get(url, params=params)
    data_json = r.json()
    big_df = pd.DataFrame()
    if symbol == "MPV":
        temp_df = pd.DataFrame(data_json[0]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[0]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[1]])
            try:
                temp_current_year_list.append(item[temp_df.columns[2]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 2], temp_previous_year_df.iloc[:, 2]]
        ).T
        big_df.columns = [temp_df.columns[2], temp_df.columns[1]]
        big_df["月份"] = temp_df["month"]
        big_df = big_df[
            [
                "月份",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    elif symbol == "SUV":
        temp_df = pd.DataFrame(data_json[1]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[1]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[1]])
            try:
                temp_current_year_list.append(item[temp_df.columns[2]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 2], temp_previous_year_df.iloc[:, 2]]
        ).T
        big_df.columns = [temp_df.columns[2], temp_df.columns[1]]
        big_df["月份"] = temp_df["month"]
        big_df = big_df[
            [
                "月份",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    elif symbol == "轿车":
        temp_df = pd.DataFrame(data_json[2]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[2]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[1]])
            try:
                temp_current_year_list.append(item[temp_df.columns[2]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 2], temp_previous_year_df.iloc[:, 2]]
        ).T
        big_df.columns = [temp_df.columns[2], temp_df.columns[1]]
        big_df["月份"] = temp_df["month"]
        big_df = big_df[
            [
                "月份",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    elif symbol == "占比":
        temp_df = pd.DataFrame(data_json[3]["dataList"])
        temp_mpv_year_list = []
        temp_suv_year_list = []
        temp_jiaoche_year_list = []
        for item in data_json[3]["dataList"]:
            temp_mpv_year_list.append(item[temp_df.columns[1]])
            try:
                temp_suv_year_list.append(item[temp_df.columns[2]])
                temp_jiaoche_year_list.append(item[temp_df.columns[3]])
            except:  # noqa: E722
                continue
        temp_mpv_year_df = pd.DataFrame(temp_mpv_year_list)
        temp_suv_year_df = pd.DataFrame(temp_suv_year_list)
        temp_jiaoche_year_df = pd.DataFrame(temp_jiaoche_year_list)
        big_df = pd.DataFrame(
            [
                temp_mpv_year_df.iloc[:, 3],
                temp_suv_year_df.iloc[:, 3],
                temp_jiaoche_year_df.iloc[:, 3],
            ]
        ).T
        big_df.columns = [temp_df.columns[1], temp_df.columns[2], temp_df.columns[3]]
        big_df["月份"] = temp_df["月份"]
        big_df = big_df[
            ["月份", temp_df.columns[1], temp_df.columns[2], temp_df.columns[3]]
        ]
    return big_df


def car_market_cate_cpca(symbol: str = "轿车", indicator: str = "批发") -> pd.DataFrame:
    """
    乘联会-统计数据-车型大类
    http://data.cpcaauto.com/CategoryMarket
    :param symbol: choice of {"轿车", "MPV", "SUV", "占比"}
    :type symbol: str
    :param indicator: choice of {"批发", "零售"}
    :type indicator: str
    :return: 统计数据-车型大类
    :rtype: pandas.DataFrame
    """
    if indicator == "批发":
        temp_df = __car_market_cate_cpca_pifa(symbol=symbol)
        return temp_df
    else:
        temp_df = __car_market_cate_cpca_lingshou(symbol=symbol)
        return temp_df


if __name__ == "__main__":
    car_market_cate_cpca_df = car_market_cate_cpca(symbol="轿车", indicator="批发")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="MPV", indicator="批发")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="SUV", indicator="批发")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="占比", indicator="批发")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="轿车", indicator="零售")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="MPV", indicator="零售")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="SUV", indicator="零售")
    print(car_market_cate_cpca_df)

    car_market_cate_cpca_df = car_market_cate_cpca(symbol="占比", indicator="零售")
    print(car_market_cate_cpca_df)
