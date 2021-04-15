# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/2/1 13:50
Desc: 英为财情-利率国债-全球政府债券行情与收益率
https://hk.investing.com/rates-bonds/
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.index.cons import short_headers, long_headers


def _get_global_country_name_url() -> dict:
    """
    指数数据国家对应的 URL
    https://hk.investing.com/rates-bonds/
    :return: 指数数据国家对应的 URL
    :rtype: dict
    """
    url = "https://hk.investing.com/rates-bonds/"
    res = requests.get(url, headers=short_headers, timeout=30)
    soup = BeautifulSoup(res.text, "lxml")
    name_url_option_list = soup.find("select", attrs={"name": "country"}).find_all("option")[1:]
    url_list = [item["value"] for item in name_url_option_list]
    name_list = [item.get_text() for item in name_url_option_list]
    name_code_map_dict = {}
    name_code_map_dict.update(zip(name_list, url_list))
    return name_code_map_dict


def bond_investing_global_country_name_url(country: str = "中国") -> dict:
    """
    参考网页: https://hk.investing.com/rates-bonds/
    获取选择国家对应的: 主要指数, 主要行业, 附加指数, 其他指数
    :param country: str 中文国家名称, 对应 get_global_country_name_url 函数返回的国家名称
    :return: dict
    """
    name_url_dict = _get_global_country_name_url()
    from zhconv import convert
    country = convert(country, 'zh-hk')
    url = f"https://hk.investing.com{name_url_dict[country]}"
    res = requests.get(url, headers=short_headers, timeout=30)
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
    return name_code_map_dict


def bond_investing_global(
    country: str = "中国",
    index_name: str = "中国1年期国债",
    period: str = "每日",
    start_date: str = "2000-01-01",
    end_date: str = "2019-10-17",
) -> pd.DataFrame:
    """
    具体国家的具体指数的从 start_date 到 end_date 期间的数据
    https://hk.investing.com/rates-bonds/
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
    from zhconv import convert
    country = convert(country, 'zh-hk')
    index_name = convert(index_name, 'zh-hk')
    period = convert(period, 'zh-hk')
    start_date = start_date.replace("-", "/")
    end_date = end_date.replace("-", "/")
    period_map = {"每日": "Daily", "每周": "Weekly", "每月": "Monthly"}
    name_code_dict = bond_investing_global_country_name_url(country)
    temp_url = f"https://hk.investing.com/{name_code_dict[index_name]}-historical-data"
    res = requests.get(temp_url, headers=short_headers, timeout=30)
    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find("h2", attrs={"class": "float_lang_base_1"}).get_text()
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
    url = "https://hk.investing.com/instruments/HistoricalDataAjax"
    res = requests.post(url, data=payload, headers=long_headers, timeout=60)
    df_data = pd.read_html(res.text)[0]
    df_data.columns = [
        '日期',
        '收盘',
        '开盘',
        '高',
        '低',
        '涨跌幅',
    ]
    if period == "每月":
        df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月")
    else:
        df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月%d日")
    df_data = df_data[["收盘", "开盘", "高", "低", "涨跌幅"]]
    df_data["涨跌幅"] = df_data["涨跌幅"].str.replace("%", "")
    df_data["涨跌幅"] = df_data["涨跌幅"].str.replace(",", "")
    df_data = df_data.astype(float)
    return df_data


if __name__ == "__main__":
    bond_investing_global_country_name_url("中国")
    bond_investing_global_df = bond_investing_global(
        country="中国",
        index_name="中国10年期国债",
        period="每日",
        start_date="2010-01-01",
        end_date="2021-03-14",
    )
    print(bond_investing_global_df)
