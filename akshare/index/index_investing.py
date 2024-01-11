#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/8/8 19:53
Desc: 英为财情-股票指数-全球股指与期货指数数据接口
https://cn.investing.com/indices/volatility-s-p-500-historical-data
"""
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.index.cons import short_headers


def _get_global_index_area_name_code() -> dict:
    """
    全球指数-各国的全球指数数据
    https://cn.investing.com/indices/global-indices?majorIndices=on&primarySectors=on&bonds=on&additionalIndices=on&otherIndices=on&c_id=37
    :return: 国家和代码
    :rtype: dict
    """
    url = "https://cn.investing.com/indices/global-indices"
    params = {
        "majorIndices": "on",
        "primarySectors": "on",
        "bonds": "on",
        "additionalIndices": "on",
        "otherIndices": "on",
    }
    r = requests.get(url, params=params, headers=short_headers)
    data_text = r.text
    soup = BeautifulSoup(data_text, "lxml")
    name_url_option_list = soup.find_all("option")[1:]
    url_list = [
        item["value"]
        for item in name_url_option_list
        if "c_id" in item["value"]
    ]
    url_list_code = [
        item["value"].split("?")[1].split("=")[1]
        for item in name_url_option_list
        if "c_id" in item["value"]
    ]
    name_list = [item.get_text() for item in name_url_option_list][
        : len(url_list)
    ]
    _temp_df = pd.DataFrame([name_list, url_list_code]).T
    name_code_list = dict(zip(_temp_df.iloc[:, 0], _temp_df.iloc[:, 1]))
    return name_code_list


def _get_global_country_name_url() -> dict:
    """
    可获得指数数据国家对应的 URL
    https://cn.investing.com/indices/
    :return: 国家和 URL
    :rtype: dict
    """
    url = "https://cn.investing.com/indices/"
    res = requests.post(url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    name_url_option_list = soup.find(
        "select", attrs={"name": "country"}
    ).find_all("option")[
        1:
    ]  # 去掉-所有国家及地区
    url_list = [item["value"] for item in name_url_option_list]
    name_list = [item.get_text() for item in name_url_option_list]
    name_code_map_dict = {}
    name_code_map_dict.update(zip(name_list, url_list))
    return name_code_map_dict


def index_investing_global_area_index_name_code(area: str = "中国") -> dict:
    """
    指定 area 的所有指数和代码
    https://cn.investing.com/indices/
    :param area: 指定的国家或地区；ak._get_global_country_name_url() 函数返回的国家或地区的名称
    :type area: str
    :return: 指定 area 的所有指数和代码
    :rtype: dict
    """
    pd.set_option("mode.chained_assignment", None)
    name_url_dict = _get_global_country_name_url()
    url = f"https://cn.investing.com{name_url_dict[area]}?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    code_list = [
        item["data-id"]
        for item in soup.find_all("table")[1].find_all(
            "span", attrs={"class": "alertBellGrayPlus"}
        )
    ]
    name_list = [
        item.find("a").text
        for item in soup.find_all("td", attrs={"class": "plusIconTd"})
    ]
    name_code_map_dict = {}
    name_code_map_dict.update(zip(name_list, code_list))
    return name_code_map_dict


def index_investing_global_area_index_name_url(area: str = "中国") -> dict:
    """
    指定 area 的所有指数和 URL 地址
    https://cn.investing.com/indices/
    :param area: 指定的国家或地区；ak._get_global_country_name_url() 函数返回的国家或地区的名称
    :type area: str
    :return: 指定 area 的所有指数和 URL 地址
    :rtype: dict
    """
    pd.set_option("mode.chained_assignment", None)
    name_url_dict = _get_global_country_name_url()
    url = f"https://cn.investing.com{name_url_dict[area]}?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    code_list = [
        item.find("a")["href"]
        for item in soup.find_all("td", attrs={"class": "plusIconTd"})
    ]
    name_list = [
        item.find("a").text
        for item in soup.find_all("td", attrs={"class": "plusIconTd"})
    ]
    name_code_map_dict = {}
    name_code_map_dict.update(zip(name_list, code_list))
    return name_code_map_dict


def index_investing_global(
    area: str = "中国",
    symbol: str = "上证指数",
    period: str = "每日",
    start_date: str = "20100101",
    end_date: str = "20211031",
) -> pd.DataFrame:
    """
    具体国家或地区的从 start_date 到 end_date 期间的数据
    https://cn.investing.com/indices/ftse-epra-nareit-hong-kong-historical-data
    :param area: 对应函数中的国家或地区名称
    :type area: str
    :param symbol: 对应函数中的指数名称
    :type symbol: str
    :param period: choice of {"每日", "每周", "每月"}
    :type period: str
    :param start_date: '20000101', 注意格式
    :type start_date: str
    :param end_date: '20191017', 注意格式
    :type end_date: str
    :return: 指定参数的数据
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    period_map = {"每日": "Daily", "每周": "Weekly", "每月": "Monthly"}
    name_code_dict = index_investing_global_area_index_name_code(area)
    url = f"https://api.investing.com/api/financialdata/historical/{name_code_dict[symbol]}"
    params = {
        "start-date": start_date,
        "end-date": end_date,
        "time-frame": period_map[period],
        "add-missing-rows": "false",
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "domain-id": "cn",
        "origin": "https://cn.investing.com",
        "pragma": "no-cache",
        "referer": "https://cn.investing.com/",
        "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjM2NjQ1NzUsImp0aSI6IjIyODA4MDM5MSIsImlhdCI6MTY2MzY2MDk3NSwiaXNzIjoiaW52ZXN0aW5nLmNvbSIsInVzZXJfaWQiOjIyODA4MDM5MSwicHJpbWFyeV9kb21haW5faWQiOiIxIiwiQXV0aG5TeXN0ZW1Ub2tlbiI6IiIsIkF1dGhuU2Vzc2lvblRva2VuIjoiIiwiRGV2aWNlVG9rZW4iOiIiLCJVYXBpVG9rZW4iOiJObmclMkJmMlJyUHpjeWRtdHRaell5TW1JN1pUNWliV1prTURJMVB6czlNeVUySWpVN1lEYzNjV1ZxYWlSZ1kyVjVNamRsWWpRMFptWTFQMkk4TnpCdlBEWXlQbVJrWXo4M01tQnJaMmN3TW1aaU1HVm9ZbWRtWmpBNU5UWTdhRE0lMkJOalUxTW1Cdk56VmxPbW93WUR4bGJUSWdaWGswY0daM05XZGlNamQyYnlnMk9UNSUyRlpEUSUyRllESm1hMjluTURJeFlqRmxQV0l3Wmpjd1pUVXhPenN6S3paOSIsIkF1dGhuSWQiOiIiLCJJc0RvdWJsZUVuY3J5cHRlZCI6ZmFsc2UsIkRldmljZUlkIjoiIiwiUmVmcmVzaEV4cGlyZWRBdCI6MTY2NjE4MDk3NX0.uRLTP1IG3696uxHm3Qq0D8z4o3nfsD3CaIS9cZGjsV0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    r.encoding = "utf-8"
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    df_data = pd.DataFrame(data_json["data"])
    df_data.columns = [
        "-",
        "-",
        "-",
        "日期",
        "-",
        "-",
        "-",
        "-",
        "-",
        "交易量",
        "-",
        "收盘",
        "开盘",
        "高",
        "低",
        "涨跌幅",
    ]
    df_data = df_data[["日期", "收盘", "开盘", "高", "低", "交易量", "涨跌幅"]]
    df_data["日期"] = pd.to_datetime(df_data["日期"]).dt.date
    df_data["收盘"] = pd.to_numeric(df_data["收盘"])
    df_data["开盘"] = pd.to_numeric(df_data["开盘"])
    df_data["高"] = pd.to_numeric(df_data["高"])
    df_data["低"] = pd.to_numeric(df_data["低"])
    df_data["交易量"] = pd.to_numeric(df_data["交易量"])
    df_data["涨跌幅"] = pd.to_numeric(df_data["涨跌幅"])
    df_data.sort_values("日期", inplace=True)
    df_data.reset_index(inplace=True, drop=True)
    return df_data


if __name__ == "__main__":
    print(index_investing_global_area_index_name_url("香港"))

    print(index_investing_global_area_index_name_code("香港"))

    index_investing_global_df = index_investing_global(
        area="中国",
        symbol="富时中国A50指数",
        period="每日",
        start_date="20100101",
        end_date="20220808",
    )
    print(index_investing_global_df)
