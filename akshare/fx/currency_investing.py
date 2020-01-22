# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/1/22 19:56
contact: jindaxiang@163.com
desc: 英为财情-外汇-货币对历史数据
https://cn.investing.com/currencies/
https://cn.investing.com/currencies/eur-usd-historical-data
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.index.cons import short_headers, long_headers


def currency_name_url():
    url = "https://cn.investing.com/currencies/"
    res = requests.post(url, headers=short_headers)
    data_table = pd.read_html(res.text)[0].iloc[:, 1:]  # 实时货币行情
    data_table.columns = ['中文名称', '英文名称', '最新', '最高', '最低', '涨跌额', '涨跌幅', '时间']
    name_code_dict = dict(zip(data_table["中文名称"].tolist(), [item.lower().replace("/", "-") for item in data_table["英文名称"].tolist()]))
    return name_code_dict


def currency_hist(index_name="欧元/美元", start_date="2005/01/01", end_date="2020/01/17"):
    """
    外汇历史数据获取, 注意获取数据区间的长短
    :param index_name: {'欧元/美元': 'eur-usd', '英镑/美元': 'gbp-usd', '美元/日元': 'usd-jpy', '澳大利亚元/美元': 'aud-usd', '美元/加拿大元': 'usd-cad', '澳大利亚元/港币': 'aud-hkd', '新西兰元/美元': 'nzd-usd', '美元/人民币': 'usd-cny', '澳大利亚元/人民币': 'aud-cny', '俄罗斯卢布/人民币': 'rub-cny'}
    :type index_name: str
    :param start_date: 日期
    :type start_date: str
    :param end_date: 日期
    :type end_date: str
    :return: 货币对历史数据
    :rtype: pandas.DataFrame
    """
    name_code_dict = currency_name_url()
    temp_url = f"https://cn.investing.com/currencies/{name_code_dict[index_name]}-historical-data"
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
    res = requests.post(url, data=payload, headers=long_headers)
    soup = BeautifulSoup(res.text, "lxml")
    vest_list = [item.get_text().strip().split("\n") for item in soup.find_all("tr")]
    raw_df = pd.DataFrame(vest_list)
    df_data = pd.DataFrame(vest_list, columns=raw_df.iloc[0, :].tolist()).iloc[1:-1, :]
    return df_data


if __name__ == '__main__':
    currency_hist_df = currency_hist(index_name="欧元/美元", start_date="2005/01/01", end_date="2020/01/17")
    print(currency_hist_df)
