# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/8/20 14:41
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
    js_text = soup.find_all("script")[7].string
    js_text_processed = js_text.replace("\r\n", "")
    js_text_processed = re.findall(r"(\[.*?])", js_text_processed)
    year_list = eval(js_text_processed[1])
    date_list = eval(js_text_processed[2])
    value_2015_list = eval(js_text_processed[4])
    value_2016_list = eval(js_text_processed[6])
    value_2017_list = eval(js_text_processed[8])
    value_2018_list = eval(js_text_processed[10])
    value_2019_list = eval(js_text_processed[12])
    value_2020_list = eval(js_text_processed[14])
    value_2021_list = eval(js_text_processed[16])
    temp_df = pd.DataFrame(
        [
            date_list,
            value_2015_list,
            value_2016_list,
            value_2017_list,
            value_2018_list,
            value_2019_list,
            value_2020_list,
            value_2021_list,
        ]
    ).T
    temp_df.columns = ["日期"] + year_list
    temp_df = temp_df[:-1]
    temp_df['2015年'] = pd.to_numeric(temp_df['2015年'])
    temp_df['2016年'] = pd.to_numeric(temp_df['2016年'])
    temp_df['2017年'] = pd.to_numeric(temp_df['2017年'])
    temp_df['2018年'] = pd.to_numeric(temp_df['2018年'])
    temp_df['2019年'] = pd.to_numeric(temp_df['2019年'])
    temp_df['2020年'] = pd.to_numeric(temp_df['2020年'])
    temp_df['2021年'] = pd.to_numeric(temp_df['2021年'])
    return temp_df


def futures_egg_price() -> pd.DataFrame:
    """
    2015-2021年鸡蛋价格走势
    https://www.jidan7.com/trend/
    :return: 2015-2021年鸡蛋价格走势
    :rtype: pandas.DataFrame
    """
    url = "https://www.jidan7.com/trend/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    js_text = soup.find_all("script")[8].string
    js_text_processed = js_text.replace("\r\n", "")
    re.findall(r"data: (.*)", js_text_processed)
    js_text_processed = re.findall(r"(\[.*?])", js_text_processed)
    date_list = eval(js_text_processed[2])
    value_2015_list = eval(re.findall(r"data: (\[.*?])", js_text_processed[3])[0])
    temp_df = pd.DataFrame(
        [
            date_list,
            value_2015_list,
        ]
    ).T
    temp_df.dropna(how="any", inplace=True)
    temp_df.columns = [
        "date",
        "price",
    ]
    temp_df['price'] = pd.to_numeric(temp_df['price'])
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
    js_text = soup.find_all("script")[9].string
    js_text_processed = js_text.replace("\r\n", "")
    js_text_processed = re.findall(r"data: (\[.*?])", js_text_processed)
    area_list = eval(js_text_processed[0])
    date_list = eval(js_text_processed[1])
    value_sd_list = eval(js_text_processed[2])
    value_hn_list = eval(js_text_processed[3])
    value_hb_list = eval(js_text_processed[4])
    value_ln_list = eval(js_text_processed[5])
    value_js_list = eval(js_text_processed[6])
    value_hub_list = eval(js_text_processed[7])
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
    temp_df['山东均价'] = pd.to_numeric(temp_df['山东均价'])
    temp_df['河南均价'] = pd.to_numeric(temp_df['河南均价'])
    temp_df['河北均价'] = pd.to_numeric(temp_df['河北均价'])
    temp_df['辽宁均价'] = pd.to_numeric(temp_df['辽宁均价'])
    temp_df['江苏均价'] = pd.to_numeric(temp_df['江苏均价'])
    temp_df['湖北均价'] = pd.to_numeric(temp_df['湖北均价'])
    return temp_df


if __name__ == "__main__":
    futures_egg_price_yearly_df = futures_egg_price_yearly()
    print(futures_egg_price_yearly_df)

    futures_egg_price_df = futures_egg_price()
    print(futures_egg_price_df)

    futures_egg_price_area_df = futures_egg_price_area()
    print(futures_egg_price_area_df)
