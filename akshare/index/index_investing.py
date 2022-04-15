#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/3/18 17:03
Desc: 英为财情-股票指数-全球股指与期货指数数据接口
https://cn.investing.com/indices/volatility-s-p-500-historical-data
"""
import re

import pandas as pd
from bs4 import BeautifulSoup

from akshare.index.cons import short_headers, long_headers
from akshare.utils.ak_session import session


def _get_global_index_country_name_url() -> dict:
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
    r = session.get(url, params=params, headers=short_headers)
    data_text = r.text
    soup = BeautifulSoup(data_text, "lxml")
    name_url_option_list = soup.find_all("option")[1:]
    url_list = [
        item["value"] for item in name_url_option_list if "c_id" in item["value"]
    ]
    url_list_code = [
        item["value"].split("?")[1].split("=")[1]
        for item in name_url_option_list
        if "c_id" in item["value"]
    ]
    name_list = [item.get_text() for item in name_url_option_list][: len(url_list)]
    _temp_df = pd.DataFrame([name_list, url_list_code]).T
    name_code_list = dict(zip(_temp_df.iloc[:, 0], _temp_df.iloc[:, 1]))
    return name_code_list


def _get_global_country_name_url() -> dict:
    """
    可获得指数数据国家对应的 URL
    :return: URL
    :rtype: dict
    """

    url = "https://cn.investing.com/indices/"
    res = session.post(url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    name_url_option_list = soup.find("select", attrs={"name": "country"}).find_all(
        "option"
    )[
        1:
    ]  # 去掉-所有国家及地区
    url_list = [item["value"] for item in name_url_option_list]
    name_list = [item.get_text() for item in name_url_option_list]
    name_code_map_dict = {}
    name_code_map_dict.update(zip(name_list, url_list))
    return name_code_map_dict


def index_investing_global_country_name_url(country: str = "中国") -> dict:
    """
    参考网页: https://cn.investing.com/indices/
    获取选择国家对应的: 主要指数, 主要行业, 附加指数, 其他指数
    :param country: str 中文国家名称, 对应 get_global_country_name_url 函数返回的国家名称
    :return: dict
    """
    pd.set_option("mode.chained_assignment", None)
    name_url_dict = _get_global_country_name_url()
    name_code_dict = _get_global_index_country_name_url()
    url = f"https://cn.investing.com{name_url_dict[country]}?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on"
    res = session.post(url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    url_list = [
        item.find("a")["href"] for item in soup.find_all(attrs={"class": "plusIconTd"})
    ]
    name_list = [
        item.find("a").get_text()
        for item in soup.find_all(attrs={"class": "plusIconTd"})
    ]
    name_code_map_dict = {}
    name_code_map_dict.update(zip(name_list, url_list))

    url = "https://cn.investing.com/indices/global-indices"
    params = {
        "majorIndices": "on",
        "primarySectors": "on",
        "bonds": "on",
        "additionalIndices": "on",
        "otherIndices": "on",
        "c_id": name_code_dict[country],
    }
    r = session.get(url, params=params, headers=short_headers)
    data_text = r.text
    soup = BeautifulSoup(data_text, "lxml")
    soup_list = soup.find("table", attrs={"id": "cr_12"}).find_all("a")
    global_index_url = [item["href"] for item in soup_list]
    global_index_name = [item["title"] for item in soup_list]
    name_code_map_dict.update(zip(global_index_name, global_index_url))
    return name_code_map_dict


def index_investing_global(
    country: str = "美国",
    index_name: str = "纳斯达克100",
    period: str = "每日",
    start_date: str = "20100101",
    end_date: str = "20211031",
) -> pd.DataFrame:
    """
    具体国家的具体指数的从 start_date 到 end_date 期间的数据
    :param country: 对应函数中的国家名称
    :type country: str
    :param index_name: 对应函数中的指数名称
    :type index_name: str
    :param period: choice of {"每日", "每周", "每月"}
    :type period: str
    :param start_date: '2000-01-01', 注意格式
    :type start_date: str
    :param end_date: '2019-10-17', 注意格式
    :type end_date: str
    :return: 指定参数的数据
    :rtype: pandas.DataFrame
    """
    start_date = "/".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "/".join([end_date[:4], end_date[4:6], end_date[6:]])
    period_map = {"每日": "Daily", "每周": "Weekly", "每月": "Monthly"}
    name_code_dict = index_investing_global_country_name_url(country)
    temp_url = f"https://cn.investing.com/{name_code_dict[index_name]}-historical-data"
    res = session.post(temp_url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find("h2", attrs={"class": "float_lang_base_1"}).get_text()
    res = session.post(temp_url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    data = soup.find_all(text=re.compile("window.histDataExcessInfo"))[0].strip()
    para_data = re.findall(r"\d+", data)
    payload = {
        "curr_id": para_data[0],
        "smlID": para_data[1],
        "header": title,
        "st_date": start_date,
        "end_date": end_date,
        "interval_sec": period_map[period],
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data",
    }
    url = "https://cn.investing.com/instruments/HistoricalDataAjax"
    res = session.post(url, data=payload, headers=long_headers)
    df_data = pd.read_html(res.text)[0]
    if period == "每月":
        df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月")
    else:
        df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月%d日")
    if any(df_data["交易量"].astype(str).str.contains("-")):
        df_data["交易量"][df_data["交易量"].str.contains("-")] = df_data["交易量"][
            df_data["交易量"].str.contains("-")
        ].replace("-", 0)
    if any(df_data["交易量"].astype(str).str.contains("B")):
        df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)]
            .str.replace("B", "")
            .str.replace(",", "")
            .astype(float)
            * 1000000000
        )
    if any(df_data["交易量"].astype(str).str.contains("M")):
        df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)]
            .str.replace("M", "")
            .str.replace(",", "")
            .astype(float)
            * 1000000
        )
    if any(df_data["交易量"].astype(str).str.contains("K")):
        df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)]
            .str.replace("K", "")
            .str.replace(",", "")
            .astype(float)
            * 1000
        )
    df_data["交易量"] = df_data["交易量"].astype(float)
    df_data = df_data[["收盘", "开盘", "高", "低", "交易量"]]
    df_data = df_data.astype(float)
    df_data.sort_index(inplace=True)
    df_data.reset_index(inplace=True)
    df_data["日期"] = pd.to_datetime(df_data["日期"]).dt.date
    return df_data


def index_investing_global_from_url(
    url: str = "https://www.investing.com/indices/ftse-epra-nareit-eurozone",
    period: str = "每日",
    start_date: str = "20000101",
    end_date: str = "20210909",
) -> pd.DataFrame:
    """
    获得具体指数的从 start_date 到 end_date 期间的数据
    https://www.investing.com/indices/ftse-epra-nareit-eurozone
    :param url: 具体数据链接
    :type url: str
    :param period: choice of {"每日", "每周", "每月"}
    :type period: str
    :param start_date: '2000-01-01', 注意格式
    :type start_date: str
    :param end_date: '2019-10-17', 注意格式
    :type end_date: str
    :return: 指定参数的数据
    :rtype: pandas.DataFrame
    """

    start_date = "/".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "/".join([end_date[:4], end_date[4:6], end_date[6:]])
    period_map = {"每日": "Daily", "每周": "Weekly", "每月": "Monthly"}
    url_name = url.split("/")[-1]
    temp_url = f"https://cn.investing.com/indices/{url_name}-historical-data"
    res = session.post(temp_url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find("h2", attrs={"class": "float_lang_base_1"}).get_text()
    res = session.post(temp_url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    data = soup.find_all(text=re.compile("window.histDataExcessInfo"))[0].strip()
    para_data = re.findall(r"\d+", data)
    payload = {
        "curr_id": para_data[0],
        "smlID": para_data[1],
        "header": title,
        "st_date": start_date,
        "end_date": end_date,
        "interval_sec": period_map[period],
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data",
    }
    url = "https://cn.investing.com/instruments/HistoricalDataAjax"
    res = session.post(url, data=payload, headers=long_headers)
    df_data = pd.read_html(res.text)[0]
    if period == "每月":
        df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月")
    else:
        df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月%d日")
    if any(df_data["交易量"].astype(str).str.contains("-")):
        df_data["交易量"][df_data["交易量"].str.contains("-")] = df_data["交易量"][
            df_data["交易量"].str.contains("-")
        ].replace("-", 0)
    if any(df_data["交易量"].astype(str).str.contains("B")):
        df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)]
            .str.replace("B", "")
            .str.replace(",", "")
            .astype(float)
            * 1000000000
        )
    if any(df_data["交易量"].astype(str).str.contains("M")):
        df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)]
            .str.replace("M", "")
            .str.replace(",", "")
            .astype(float)
            * 1000000
        )
    if any(df_data["交易量"].astype(str).str.contains("K")):
        df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)] = (
            df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)]
            .str.replace("K", "")
            .str.replace(",", "")
            .astype(float)
            * 1000
        )
    df_data["交易量"] = df_data["交易量"].astype(float)
    df_data = df_data[["收盘", "开盘", "高", "低", "交易量"]]
    df_data = df_data.astype(float)
    df_data.sort_index(inplace=True)
    df_data.reset_index(inplace=True)
    df_data["日期"] = pd.to_datetime(df_data["日期"]).dt.date
    return df_data


if __name__ == "__main__":
    index_investing_global_from_url_df = index_investing_global_from_url(
        url="https://www.investing.com/indices/ftse-epra-nareit-hong-kong",
        period="每日",
        start_date="19900101",
        end_date="20210909",
    )
    print(index_investing_global_from_url_df)

    index_investing_global_country_name_url_dict = (
        index_investing_global_country_name_url("美国")
    )

    index_investing_global_df = index_investing_global(
        country="香港",
        index_name="恒生指数",
        period="每日",
        start_date="20010101",
        end_date="20010316",
    )
    print(index_investing_global_df)
