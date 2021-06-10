# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/5/10 17:06
Desc: 提供英为财情-国际大宗商品期货
https://cn.investing.com/commodities/brent-oil-historical-data
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.index.cons import short_headers, long_headers


def get_sector_symbol_name_url() -> dict:
    """
    期货所对应板块的 URL
    :return: dict
    {'能源': '/commodities/energy',
    '金属': '/commodities/metals',
    '农业': '/commodities/softs',
    '商品指数': '/indices/commodities-indices'}
    """
    url = "https://cn.investing.com/commodities/"
    res = requests.get(url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    name_url_option_list = soup.find_all(attrs={"class": "linkTitle"})  # 去掉-所有国家及地区
    url_list = [item.find("a")["href"] for item in name_url_option_list]
    name_list = [item.get_text() for item in name_url_option_list]
    name_code_map_dict = {}
    name_code_map_dict.update(zip(name_list, url_list))
    return name_code_map_dict


def futures_global_commodity_name_url_map(sector: str = "能源") -> dict:
    """
    参考网页: https://cn.investing.com/commodities/
    获取选择板块对应的: 具体期货品种的 url 地址
    :param sector: 板块, 对应 get_global_country_name_url 品种名称
    :type sector: str
    :return: dict of name-url
    :rtype: dict
    {'伦敦布伦特原油': '/commodities/brent-oil',
    'WTI原油': '/commodities/crude-oil',
    '伦敦汽油': '/commodities/london-gas-oil',
    '天然气': '/commodities/natural-gas?cid=49787',
    '燃料油': '/commodities/heating-oil',
    '碳排放': '/commodities/carbon-emissions',
    'RBOB汽油': '/commodities/gasoline-rbob',
    '布伦特原油': '/commodities/brent-oil?cid=49769',
    '原油': '/commodities/crude-oil?cid=49774'}
    """
    name_url_dict = get_sector_symbol_name_url()
    url = f"https://cn.investing.com{name_url_dict[sector]}"
    res = requests.post(url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    url_list = [
        item.find("a")["href"].split("?")[0]
        for item in soup.find_all(attrs={"class": "plusIconTd"})
    ]
    name_list = [
        item.find("a").get_text()
        for item in soup.find_all(attrs={"class": "plusIconTd"})
    ]
    name_code_map_dict = {}
    name_code_map_dict.update(zip(name_list, url_list))
    return name_code_map_dict


def futures_global_commodity_hist(
    sector: str = "能源",
    symbol: str = "伦敦布伦特原油",
    start_date: str = "20000101",
    end_date: str = "20191017",
) -> pd.DataFrame:
    """
    国际大宗商品的历史量价数据
    https://cn.investing.com/commodities
    :param sector: 板块名称; 调用 futures_global_commodity_name_url_map 函数获取
    :type sector: str
    :param symbol: 品种名称; 通过访问网站查询
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 国际大宗商品的历史量价数据
    :rtype: pandas.DataFrame
    """
    start_date = "/".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "/".join([end_date[:4], end_date[4:6], end_date[6:]])
    name_code_dict = futures_global_commodity_name_url_map(sector)
    temp_url = f"https://cn.investing.com/{name_code_dict[symbol]}-historical-data"
    res = requests.post(temp_url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find("h2", attrs={"class": "float_lang_base_1"}).get_text()
    res = requests.post(temp_url, headers=short_headers)
    soup = BeautifulSoup(res.text, "lxml")
    data = soup.find_all(text=re.compile("window.histDataExcessInfo"))[0].strip()
    para_data = re.findall(r"\d+", data)
    payload = {
        "curr_id": para_data[0],
        "smlID": para_data[1],
        "header": title,
        "st_date": start_date,
        "end_date": end_date,
        "interval_sec": "Daily",
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data",
    }
    url = "https://cn.investing.com/instruments/HistoricalDataAjax"
    r = requests.post(url, data=payload, headers=long_headers)
    temp_df = pd.read_html(r.text)[0]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], format="%Y年%m月%d日")
    if any(temp_df["交易量"].astype(str).str.contains("-")):
        temp_df["交易量"][temp_df["交易量"].str.contains("-")] = temp_df["交易量"][
            temp_df["交易量"].str.contains("-")
        ].replace("-", 0)
    if any(temp_df["交易量"].astype(str).str.contains("B")):
        temp_df["交易量"][temp_df["交易量"].str.contains("B").fillna(False)] = (
            temp_df["交易量"][temp_df["交易量"].str.contains("B").fillna(False)]
            .str.replace("B", "")
            .astype(float)
            * 1000000000
        )
    if any(temp_df["交易量"].astype(str).str.contains("M")):
        temp_df["交易量"][temp_df["交易量"].str.contains("M").fillna(False)] = (
            temp_df["交易量"][temp_df["交易量"].str.contains("M").fillna(False)]
            .str.replace("M", "")
            .astype(float)
            * 1000000
        )
    if any(temp_df["交易量"].astype(str).str.contains("K")):
        temp_df["交易量"][temp_df["交易量"].str.contains("K").fillna(False)] = (
            temp_df["交易量"][temp_df["交易量"].str.contains("K").fillna(False)]
            .str.replace("K", "")
            .astype(float)
            * 1000
        )
    temp_df["交易量"] = temp_df["交易量"].astype(float)
    temp_df["涨跌幅"] = pd.DataFrame(
        round(temp_df["涨跌幅"].str.replace("%", "").astype(float) / 100, 6)
    )
    temp_df.name = title
    temp_df.columns.name = None
    temp_df.sort_values(["日期"], ascending=False, inplace=True)
    return temp_df


if __name__ == "__main__":
    temp_dict = futures_global_commodity_name_url_map(sector="能源")
    print(temp_dict)

    futures_global_commodity_hist_df = futures_global_commodity_hist(
        sector="能源", symbol="伦敦布伦特原油", start_date="19700101", end_date="20210510"
    )
    print(futures_global_commodity_hist_df)

    # futures_global_commodity_hist_df = futures_global_commodity_hist(
    #     sector="能源", symbol="伦敦布伦特原油", start_date="1970/01/01", end_date="2021/05/10"
    # )
    # print(futures_global_commodity_hist_df.to_csv("伦敦布伦特原油_19880627_20080319.csv", encoding="gb2312"))
    #
    # futures_global_commodity_hist_df = futures_global_commodity_hist(
    #     sector="能源", symbol="伦敦布伦特原油", start_date="2008/03/19", end_date="2021/05/10"
    # )
    # print(futures_global_commodity_hist_df.to_csv("伦敦布伦特原油_20080319_20210510.csv", encoding="gb2312"))
