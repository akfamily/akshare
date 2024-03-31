#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/3/30 14:00
Desc: 乘联会
https://data.cpcaauto.com/FuelMarket
汽车行业制造企业数据库
http://i.gasgoo.com/data/ranking
"""

import pandas as pd
import requests

from akshare.utils import demjson


def car_market_total_cpca(
    symbol: str = "狭义乘用车", indicator: str = "产量"
) -> pd.DataFrame:
    """
    乘联会-统计数据-总体市场
    http://data.cpcaauto.com/TotalMarket
    :param symbol: choice of {"狭义乘用车", "广义乘用车"}
    :type symbol: str
    :param indicator: choice of {"产量", "批发", "零售", "出口"}
    :type indicator: str
    :return: 统计数据-总体市场
    :rtype: pandas.DataFrame
    """
    url = "http://data.cpcaauto.com/api/chartlist"
    params = {"charttype": "1"}
    r = requests.get(url, params=params)
    data_json = r.json()
    big_df = pd.DataFrame()
    if symbol == "狭义乘用车":
        temp_df = pd.DataFrame(data_json[0]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[0]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[2]])
            try:
                temp_current_year_list.append(item[temp_df.columns[1]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        if indicator == "产量":
            big_df = pd.DataFrame(
                [temp_current_year_df.iloc[:, 0], temp_previous_year_df.iloc[:, 0]]
            ).T
            big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
            big_df["月份"] = temp_df["month"]
            big_df = big_df[
                [
                    "月份",
                    temp_df.columns[2],
                    temp_df.columns[1],
                ]
            ]
        elif indicator == "批发":
            big_df = pd.DataFrame(
                [temp_current_year_df.iloc[:, 1], temp_previous_year_df.iloc[:, 1]]
            ).T
            big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
            big_df["月份"] = temp_df["month"]
            big_df = big_df[
                [
                    "月份",
                    temp_df.columns[2],
                    temp_df.columns[1],
                ]
            ]
        elif indicator == "零售":
            big_df = pd.DataFrame(
                [temp_current_year_df.iloc[:, 2], temp_previous_year_df.iloc[:, 2]]
            ).T
            big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
            big_df["月份"] = temp_df["month"]
            big_df = big_df[
                [
                    "月份",
                    temp_df.columns[2],
                    temp_df.columns[1],
                ]
            ]
        elif indicator == "出口":
            big_df = pd.DataFrame(
                [temp_current_year_df.iloc[:, 3], temp_previous_year_df.iloc[:, 3]]
            ).T
            big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
            big_df["月份"] = temp_df["month"]
            big_df = big_df[
                [
                    "月份",
                    temp_df.columns[2],
                    temp_df.columns[1],
                ]
            ]
    else:
        temp_df = pd.DataFrame(data_json[1]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[1]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[2]])
            try:
                temp_current_year_list.append(item[temp_df.columns[1]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        if indicator == "产量":
            big_df = pd.DataFrame(
                [temp_current_year_df.iloc[:, 0], temp_previous_year_df.iloc[:, 0]]
            ).T
            big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
            big_df["月份"] = temp_df["month"]
            big_df = big_df[
                [
                    "月份",
                    temp_df.columns[2],
                    temp_df.columns[1],
                ]
            ]
        elif indicator == "批发":
            big_df = pd.DataFrame(
                [temp_current_year_df.iloc[:, 1], temp_previous_year_df.iloc[:, 1]]
            ).T
            big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
            big_df["月份"] = temp_df["month"]
            big_df = big_df[
                [
                    "月份",
                    temp_df.columns[2],
                    temp_df.columns[1],
                ]
            ]
        elif indicator == "零售":
            big_df = pd.DataFrame(
                [temp_current_year_df.iloc[:, 2], temp_previous_year_df.iloc[:, 2]]
            ).T
            big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
            big_df["月份"] = temp_df["month"]
            big_df = big_df[
                [
                    "月份",
                    temp_df.columns[2],
                    temp_df.columns[1],
                ]
            ]
        elif indicator == "出口":
            big_df = pd.DataFrame(
                [temp_current_year_df.iloc[:, 3], temp_previous_year_df.iloc[:, 3]]
            ).T
            big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
            big_df["月份"] = temp_df["month"]
            big_df = big_df[
                [
                    "月份",
                    temp_df.columns[2],
                    temp_df.columns[1],
                ]
            ]

    return big_df


def __car_market_man_rank_cpca_pifa(symbol: str = "狭义乘用车-累计") -> pd.DataFrame:
    """
    乘联会-统计数据-厂商排名
    http://data.cpcaauto.com/ManRank
    :param symbol: choice of {"狭义乘用车-单月", "狭义乘用车-累计", "广义乘用车-单月", "广义乘用车-累计"}
    :type symbol: str
    :return: 统计数据-厂商排名
    :rtype: pandas.DataFrame
    """
    url = "http://data.cpcaauto.com/api/chartlist"
    params = {"charttype": "2"}
    r = requests.get(url, params=params)
    data_json = r.json()
    big_df = pd.DataFrame()
    if symbol == "狭义乘用车-累计":
        temp_df = pd.DataFrame(data_json[0]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[0]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[2]])
            try:
                temp_current_year_list.append(item[temp_df.columns[1]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 0], temp_previous_year_df.iloc[:, 0]]
        ).T
        big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
        big_df["厂商"] = temp_df["厂商"]
        big_df = big_df[
            [
                "厂商",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    elif symbol == "狭义乘用车-单月":
        temp_df = pd.DataFrame(data_json[1]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[1]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[2]])
            try:
                temp_current_year_list.append(item[temp_df.columns[1]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 0], temp_previous_year_df.iloc[:, 0]]
        ).T
        big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
        big_df["厂商"] = temp_df["厂商"]
        big_df = big_df[
            [
                "厂商",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    elif symbol == "广义乘用车-累计":
        temp_df = pd.DataFrame(data_json[2]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[2]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[2]])
            try:
                temp_current_year_list.append(item[temp_df.columns[1]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 0], temp_previous_year_df.iloc[:, 0]]
        ).T
        big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
        big_df["厂商"] = temp_df["厂商"]
        big_df = big_df[
            [
                "厂商",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    elif symbol == "广义乘用车-单月":
        temp_df = pd.DataFrame(data_json[3]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[3]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[2]])
            try:
                temp_current_year_list.append(item[temp_df.columns[1]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 0], temp_previous_year_df.iloc[:, 0]]
        ).T
        big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
        big_df["厂商"] = temp_df["厂商"]
        big_df = big_df[
            [
                "厂商",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    return big_df


def __car_market_man_rank_cpca_lingshou(
    symbol: str = "狭义乘用车-累计",
) -> pd.DataFrame:
    """
    乘联会-统计数据-厂商排名
    http://data.cpcaauto.com/ManRank
    :param symbol: choice of {"狭义乘用车-单月", "狭义乘用车-累计", "广义乘用车-单月", "广义乘用车-累计"}
    :type symbol: str
    :return: 统计数据-厂商排名
    :rtype: pandas.DataFrame
    """
    url = "http://data.cpcaauto.com/api/chartlist_2"
    params = {"charttype": "2"}
    r = requests.get(url, params=params)
    data_json = r.json()
    big_df = pd.DataFrame()
    if symbol == "狭义乘用车-累计":
        temp_df = pd.DataFrame(data_json[0]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[0]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[2]])
            try:
                temp_current_year_list.append(item[temp_df.columns[1]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 1], temp_previous_year_df.iloc[:, 1]]
        ).T
        big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
        big_df["厂商"] = temp_df["厂商"]
        big_df = big_df[
            [
                "厂商",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    elif symbol == "狭义乘用车-单月":
        temp_df = pd.DataFrame(data_json[1]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[1]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[2]])
            try:
                temp_current_year_list.append(item[temp_df.columns[1]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 1], temp_previous_year_df.iloc[:, 1]]
        ).T
        big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
        big_df["厂商"] = temp_df["厂商"]
        big_df = big_df[
            [
                "厂商",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    elif symbol == "广义乘用车-累计":
        temp_df = pd.DataFrame(data_json[2]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[2]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[2]])
            try:
                temp_current_year_list.append(item[temp_df.columns[1]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 1], temp_previous_year_df.iloc[:, 1]]
        ).T
        big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
        big_df["厂商"] = temp_df["厂商"]
        big_df = big_df[
            [
                "厂商",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    elif symbol == "广义乘用车-单月":
        temp_df = pd.DataFrame(data_json[3]["dataList"])
        temp_current_year_list = []
        temp_previous_year_list = []
        for item in data_json[3]["dataList"]:
            temp_previous_year_list.append(item[temp_df.columns[2]])
            try:
                temp_current_year_list.append(item[temp_df.columns[1]])
            except:  # noqa: E722
                continue
        temp_current_year_df = pd.DataFrame(temp_current_year_list)
        temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
        big_df = pd.DataFrame(
            [temp_current_year_df.iloc[:, 1], temp_previous_year_df.iloc[:, 1]]
        ).T
        big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
        big_df["厂商"] = temp_df["厂商"]
        big_df = big_df[
            [
                "厂商",
                temp_df.columns[2],
                temp_df.columns[1],
            ]
        ]
    return big_df


def car_market_man_rank_cpca(
    symbol: str = "狭义乘用车-单月", indicator: str = "批发"
) -> pd.DataFrame:
    """
    乘联会-统计数据-厂商排名
    http://data.cpcaauto.com/ManRank
    :param symbol: choice of {"狭义乘用车-单月", "狭义乘用车-累计", "广义乘用车-单月", "广义乘用车-累计"}
    :type symbol: str
    :param indicator: choice of {"批发", "零售"}
    :type indicator: str
    :return: 统计数据-厂商排名
    :rtype: pandas.DataFrame
    """
    if indicator == "批发":
        temp_df = __car_market_man_rank_cpca_pifa(symbol=symbol)
        return temp_df
    else:
        temp_df = __car_market_man_rank_cpca_lingshou(symbol=symbol)
        return temp_df


def car_energy_sale_cpca() -> pd.DataFrame:
    """
    乘联会-新能源细分市场-整体市场
    https://data.cpcaauto.com/FuelMarket
    :return: 新能源细分市场-整体市场
    :rtype: pandas.DataFrame
    """
    url = "http://data.cpcaauto.com/api/chartlist"
    params = {"charttype": "6"}
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json[0]["dataList"])
    temp_current_year_list = []
    temp_previous_year_list = []
    for item in data_json[0]["dataList"]:
        temp_previous_year_list.append(item[temp_df.columns[2]])
        try:
            temp_current_year_list.append(item[temp_df.columns[1]])
        except:  # noqa: E722
            continue
    temp_current_year_df = pd.DataFrame(temp_current_year_list)
    temp_previous_year_df = pd.DataFrame(temp_previous_year_list)
    big_df = pd.DataFrame(
        [temp_current_year_df.iloc[:, 2], temp_previous_year_df.iloc[:, 2]]
    ).T
    big_df.columns = [temp_df.columns[1], temp_df.columns[2]]
    big_df["月份"] = temp_df["month"]
    big_df = big_df[
        [
            "月份",
            temp_df.columns[2],
            temp_df.columns[1],
        ]
    ]
    return big_df


def car_gasgoo_sale_rank(symbol: str = "车企榜", date: str = "202109") -> pd.DataFrame:
    """
    盖世汽车-汽车行业制造企业数据库-销量数据
    https://i.gasgoo.com/data/ranking
    :param symbol: choice of {"车企榜", "品牌榜", "车型榜"}
    :type symbol: str
    :param date: 查询的年份和月份
    :type date: str
    :return: 销量数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "车型榜": "M",
        "车企榜": "F",
        "品牌榜": "B",
    }
    url = "https://i.gasgoo.com/data/sales/AutoModelSalesRank.aspx/GetSalesRank"
    payload = {
        "countryID": "",
        "endM": str(int(date[4:6])),
        "endY": date[:4],
        "energy": "",
        "modelGradeID": "",
        "modelTypeID": "",
        "orderBy": f"{date[:4]}-{str(int(date[4:6]))}",
        "queryDate": f"{date[:4]}-{str(int(date[4:6]))}",
        "rankType": symbol_map[symbol],
        "startY": date[:4],
        "startM": str(int(date[4:6])),
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "195",
        "Content-Type": "application/json; charset=UTF-8",
        "Cookie": "Hm_lvt_8e90480b1bf68ede548c407057660718=1636981448; _ga=GA1.2.858318653.1636981449; "
        "_gid=GA1.2.1448165285.1636981449; _gat=1; Hm_lpvt_8e90480b1bf68ede548c407057660718=1636982578",
        "Host": "i.gasgoo.com",
        "Origin": "https://i.gasgoo.com",
        "Pragma": "no-cache",
        "Referer": "https://i.gasgoo.com/data/sales/AutoModelSalesRank.aspx/GetSalesRank",
        "sec-ch-ua": '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/95.0.4638.69 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.post(url, json=payload, headers=headers)
    data_json = r.json()
    data_json = demjson.decode(data_json["d"])
    temp_df = pd.DataFrame(data_json)
    return temp_df


if __name__ == "__main__":
    car_market_total_cpca_df = car_market_total_cpca(
        symbol="狭义乘用车", indicator="产量"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="广义乘用车", indicator="产量"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="狭义乘用车", indicator="批发"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="广义乘用车", indicator="批发"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="狭义乘用车", indicator="零售"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="广义乘用车", indicator="零售"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="狭义乘用车", indicator="出口"
    )
    print(car_market_total_cpca_df)

    car_market_total_cpca_df = car_market_total_cpca(
        symbol="广义乘用车", indicator="出口"
    )
    print(car_market_total_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="狭义乘用车-单月", indicator="批发"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="狭义乘用车-累计", indicator="批发"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="广义乘用车-单月", indicator="批发"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="广义乘用车-累计", indicator="批发"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="狭义乘用车-单月", indicator="零售"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="狭义乘用车-累计", indicator="零售"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="广义乘用车-单月", indicator="零售"
    )
    print(car_market_man_rank_cpca_df)

    car_market_man_rank_cpca_df = car_market_man_rank_cpca(
        symbol="广义乘用车-累计", indicator="零售"
    )
    print(car_market_man_rank_cpca_df)

    car_energy_sale_cpca_df = car_energy_sale_cpca()
    print(car_energy_sale_cpca_df)

    car_gasgoo_sale_rank_df = car_gasgoo_sale_rank(symbol="品牌榜", date="202311")
    print(car_gasgoo_sale_rank_df)

    car_gasgoo_sale_rank_df = car_gasgoo_sale_rank(symbol="车型榜", date="202311")
    print(car_gasgoo_sale_rank_df)

    car_gasgoo_sale_rank_df = car_gasgoo_sale_rank(symbol="车企榜", date="202311")
    print(car_gasgoo_sale_rank_df)
