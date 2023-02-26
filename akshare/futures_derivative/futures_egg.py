#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/2/26 16:00
Desc: 鸡蛋价格
https://www.jidan7.com/trend/
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup


def futures_egg_price_yearly() -> pd.DataFrame:
    """
    各年度产区鸡蛋价格走势
    https://www.jidan7.com/trend/
    :return: 各年度产区鸡蛋价格走势
    :rtype: pandas.DataFrame
    """
    url = "https://www.jidan7.com/trend/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    js_text = soup.find_all("script")[8].string
    js_text_processed = js_text.replace("\r\n", "")
    js_text_processed = re.findall(r"(\[.*?])", js_text_processed)
    year_list = eval(js_text_processed[1])
    date_list = eval(js_text_processed[2])
    value_first_list = eval(js_text_processed[4])
    value_second_list = eval(js_text_processed[6])
    temp_df = pd.DataFrame(
        [
            date_list,
            value_first_list,
            value_second_list,
        ]
    ).T
    temp_df.columns = ["日期"] + year_list
    temp_df = temp_df[:-1]
    temp_df[temp_df.columns[1]] = pd.to_numeric(temp_df[temp_df.columns[1]], errors="coerce")
    temp_df[temp_df.columns[2]] = pd.to_numeric(temp_df[temp_df.columns[2]], errors="coerce")
    return temp_df


def futures_egg_price() -> pd.DataFrame:
    """
    2015年-至今的鸡蛋价格走势
    https://www.jidan7.com/trend/
    :return: 鸡蛋价格走势
    :rtype: pandas.DataFrame
    """
    url = "https://www.jidan7.com/trend/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    js_text = soup.find_all("script")[9].string
    js_text_processed = js_text.replace("\r\n", "")
    js_text_processed = re.findall(r"(\[.*?])", js_text_processed)
    date_list = eval(js_text_processed[0])
    value_list = eval(js_text_processed[1])
    temp_df = pd.DataFrame(
        [
            date_list,
            value_list,
        ]
    ).T
    temp_df.dropna(how="any", inplace=True)
    temp_df.columns = [
        "date",
        "price",
    ]
    temp_df["price"] = pd.to_numeric(temp_df["price"], errors="coerce")
    return temp_df


def futures_egg_price_area() -> pd.DataFrame:
    """
    各主产区鸡蛋均价
    https://www.jidan7.com/trend/
    :return: 各主产区鸡蛋均价
    :rtype: pandas.DataFrame
    """
    url = "https://www.jidan7.com/trend/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    js_text = soup.find_all("script")[10].string
    js_text_processed = js_text.replace("\r\n", "")
    js_area_text_processed = re.findall(r"data: (\[.*?])", js_text_processed)
    area_list = eval(js_area_text_processed[0])
    js_date_text_processed = re.findall(r"sldate = (\[.*?])", js_text_processed)
    date_list = eval(js_date_text_processed[0])
    js_shandong_text_processed = re.findall(r"shandong = (\[.*?])", js_text_processed)
    value_sd_list = eval(js_shandong_text_processed[0])

    js_henan_text_processed = re.findall(r"henan = (\[.*?])", js_text_processed)
    value_hn_list = eval(js_henan_text_processed[0])

    js_hebei_text_processed = re.findall(r"hebei = (\[.*?])", js_text_processed)
    value_hb_list = eval(js_hebei_text_processed[0])

    js_jiangsu_text_processed = re.findall(r"jiangsu = (\[.*?])", js_text_processed)
    value_js_list = eval(js_jiangsu_text_processed[0])

    js_liaoning_text_processed = re.findall(r"liaoning = (\[.*?])", js_text_processed)
    value_ln_list = eval(js_liaoning_text_processed[0])

    js_hubei_text_processed = re.findall(r"hubei = (\[.*?])", js_text_processed)
    value_hub_list = eval(js_hubei_text_processed[0])

    temp_df = pd.DataFrame(
        [
            date_list,
            value_sd_list,
            value_hn_list,
            value_hb_list,
            value_ln_list,
            value_js_list,
            value_hub_list,
        ]
    ).T
    temp_df.dropna(how="any", inplace=True)
    temp_df.columns = ["日期"] + area_list
    temp_df["山东均价"] = pd.to_numeric(temp_df["山东均价"], errors="coerce")
    temp_df["河南均价"] = pd.to_numeric(temp_df["河南均价"], errors="coerce")
    temp_df["河北均价"] = pd.to_numeric(temp_df["河北均价"], errors="coerce")
    temp_df["辽宁均价"] = pd.to_numeric(temp_df["辽宁均价"], errors="coerce")
    temp_df["江苏均价"] = pd.to_numeric(temp_df["江苏均价"], errors="coerce")
    temp_df["湖北均价"] = pd.to_numeric(temp_df["湖北均价"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    futures_egg_price_yearly_df = futures_egg_price_yearly()
    print(futures_egg_price_yearly_df)

    futures_egg_price_df = futures_egg_price()
    print(futures_egg_price_df)

    futures_egg_price_area_df = futures_egg_price_area()
    print(futures_egg_price_area_df)
