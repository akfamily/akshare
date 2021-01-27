# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/1/26 12:47
Desc: 金十数据 websocket 实时数据接口-新闻
https://www.jin10.com/
wss://wss-flash-1.jin10.com/
# TODO 此接口在 Ubuntu 18.04 里面有问题
"""
import pandas as pd
import requests


def js_news(indicator: str = '最新资讯') -> pd.DataFrame:
    """
    金十数据-最新资讯
    https://www.jin10.com/
    :param indicator: choice of {'最新资讯', '最新数据'}
    :type indicator: str
    :return: 最新资讯
    :rtype: pandas.DataFrame
    """
    url = 'https://m.jin10.com/flash'
    r = requests.get(url)
    text_data = r.json()
    text_data = [item.strip() for item in text_data]
    big_df = pd.DataFrame()
    try:
        temp_df_part_one = pd.DataFrame([item.split("#") for item in text_data if item.startswith('0#1#')]).iloc[:, [2, 3]]
    except IndexError:
        temp_df_part_one = pd.DataFrame()
    try:
        temp_df_part_two = pd.DataFrame([item.split('#') for item in text_data if item.startswith('0#0#')]).iloc[:, [2, 3]]
    except IndexError:
        temp_df_part_two = pd.DataFrame()
    try:
        temp_df_part_three = pd.DataFrame([item.split('#') for item in text_data if item.startswith('1#')]).iloc[:, [8, 2, 3, 5]]
    except IndexError:
        temp_df_part_three = pd.DataFrame()
    big_df = big_df.append(temp_df_part_one, ignore_index=True)
    big_df = big_df.append(temp_df_part_two, ignore_index=True)
    big_df.columns = [
        'datetime',
        'content',
    ]
    big_df['datetime'] = pd.to_datetime(big_df['datetime'])
    big_df.sort_values('datetime', ascending=False, inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    if not temp_df_part_three.empty:
        temp_df_part_three.columns = [
            'datetime',
            'content',
            'before',
            'now',
        ]
    if indicator == '最新资讯':
        return big_df
    else:
        return temp_df_part_three


if __name__ == '__main__':
    js_news_df = js_news(indicator='最新资讯')
    print(js_news_df)
