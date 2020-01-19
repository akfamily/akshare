# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/21 13:22
contact: jindaxiang@163.com
desc: 提供英为财情-利率国债-全球政府债券行情与收益率
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.index.cons import short_headers, long_headers


def get_sector_symbol_name_url():
    """
    获取期货所对应板块的 URL
    :return: dict
    {'能源': '/commodities/energy',
    '金属': '/commodities/metals',
    '农业': '/commodities/softs',
    '商品指数': '/indices/commodities-indices'}
    """
    url = "https://cn.investing.com/commodities/"
    res = requests.post(url, headers=short_headers)
    soup = BeautifulSoup(res.text, 'lxml')
    name_url_option_list = soup.find_all(attrs={"class": "linkTitle"})  # 去掉-所有国家及地区
    url_list = [item.find("a")["href"] for item in name_url_option_list]
    name_list = [item.get_text() for item in name_url_option_list]
    name_code_map_dict = {}
    name_code_map_dict.update(zip(name_list, url_list))
    return name_code_map_dict


def get_symbol_name_url(country="能源"):
    """
    参考网页: https://cn.investing.com/commodities/
    获取选择板块对应的: 具体期货品种的 url 地址
    :param country: str 板块, 对应 get_global_country_name_url 品种名称
    :return: dict
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
    url = f"https://cn.investing.com{name_url_dict[country]}"
    res = requests.post(url, headers=short_headers)
    soup = BeautifulSoup(res.text, 'lxml')
    url_list = [item.find("a")["href"]
                for item in soup.find_all(attrs={"class": "plusIconTd"})]
    name_list = [item.find("a").get_text()
                 for item in soup.find_all(attrs={"class": "plusIconTd"})]
    name_code_map_dict = {}
    name_code_map_dict.update(zip(name_list, url_list))
    return name_code_map_dict


def get_sector_futures(
        sector="能源",
        symbol="伦敦布伦特原油",
        start_date='2000/01/01',
        end_date='2019/10/17'):
    """
    具体国家的具体指数的从 start_date 到 end_date 期间的数据
    :param sector: str 对应函数中的国家名称
    :param symbol: str 对应函数中的指数名称
    :param start_date: str '2000/01/01', 注意格式
    :param end_date: str '2019/10/17', 注意格式
    :return: pandas.DataFrame
        0              收盘     开盘      高      低      涨跌幅
    日期
    2019-10-17  59.91  58.99  60.04  58.69  269.84K
    2019-10-16  59.42  58.90  59.75  58.36  257.88K
    2019-10-15  58.74  59.30  59.68  58.00  305.68K
    2019-10-14  59.35  60.69  60.73  58.50  283.07K
    2019-10-11  60.51  59.53  60.69  59.21  367.63K
               ...    ...    ...    ...      ...
    2005-01-10  42.92  43.20  44.85  42.90   27.65K
    2005-01-07  43.18  42.75  43.75  42.20   29.64K
    2005-01-06  42.85  40.43  43.20  39.82   51.63K
    2005-01-05  40.51  40.80  41.00  39.90   42.23K
    2005-01-04  41.04  39.40  41.25  38.81   40.10K
    """
    name_code_dict = get_symbol_name_url(sector)
    temp_url = f"https://cn.investing.com/{name_code_dict[symbol]}-historical-data"
    res = requests.post(temp_url, headers=short_headers)
    soup = BeautifulSoup(res.text, 'lxml')
    title = soup.find("h2", attrs={"class": "float_lang_base_1"}).get_text()
    res = requests.post(temp_url, headers=short_headers)
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.find_all(text=re.compile(
        'window.histDataExcessInfo'))[0].strip()
    para_data = re.findall(r'\d+', data)
    payload = {
        'curr_id': para_data[0],
        'smlID': para_data[1],
        'header': title,
        'st_date': start_date,
        'end_date': end_date,
        'interval_sec': 'Daily',
        'sort_col': 'date',
        'sort_ord': 'DESC',
        'action': 'historical_data'
    }
    url = 'https://cn.investing.com/instruments/HistoricalDataAjax'
    res = requests.post(url, data=payload, headers=long_headers)
    soup = BeautifulSoup(res.text, 'lxml')
    vest_list = [item.get_text().strip().split('\n')
                 for item in soup.find_all('tr')]

    list_date = list()
    for item in vest_list[:-1]:
        list_date.append(item[0])

    list_new = list()
    for item in vest_list[:-1]:
        list_new.append(item[1])

    list_open = list()
    for item in vest_list[:-1]:
        list_open.append(item[2])

    list_high = list()
    for item in vest_list[:-1]:
        list_high.append(item[3])

    list_low = list()
    for item in vest_list[:-1]:
        list_low.append(item[4])

    list_vol_per = list()
    for item in vest_list[:-1]:
        list_vol_per.append(item[5])

    list_vol = list()
    # list_per = list()
    for item in list_vol_per:
        list_vol.append(item.split(' ')[0])
        # list_per.append(item.split(' ')[1])

    list_date.append(vest_list[-1][0])
    list_new.append(vest_list[-1][1])
    list_open.append(vest_list[-1][2])
    list_high.append(vest_list[-1][3])
    list_low.append(vest_list[-1][4])

    df_data = pd.DataFrame(
        [list_date, list_new, list_open, list_high, list_low, list_vol]).T
    # df_data.iloc[0, :][5] = '涨跌幅'
    df_data.columns = df_data.iloc[0, :]
    df_data = df_data.iloc[1:, :]
    df_data = df_data[:-1]  # 去掉最后一行
    df_data = df_data.set_index(["日期"])
    df_data.index = pd.to_datetime(df_data.index, format="%Y年%m月%d日")
    df_data.index.name = "日期"
    df_data["收盘"] = df_data["收盘"].str.replace(",", "").astype(float)
    df_data["开盘"] = df_data["开盘"].str.replace(",", "").astype(float)
    df_data["高"] = df_data["高"].str.replace(",", "").astype(float)
    df_data["低"] = df_data["低"].str.replace(",", "").astype(float)
    df_data.name = title
    return df_data


if __name__ == "__main__":
    index_df = get_sector_futures(
        sector="能源",
        symbol="WTI原油",
        start_date='2019/02/01',
        end_date='2020/01/17')
    print(index_df.name)
    print(index_df)
