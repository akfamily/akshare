# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/3/20 15:18
Desc: 
"""
import pandas as pd
import requests



url = "http://73.push2his.eastmoney.com/api/qt/stock/kline/get"
params = {
    'secid': '90.BK0936',
    'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
    'fields1': 'f1,f2,f3,f4,f5,f6',
    'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
    'klt': '5',
    'fqt': '1',
    'end': '20500101',
    'lmt': '1000000',
    '_': '1647760607065',
}
r = requests.get(url, params=params)
data_json = r.json()
temp_df = pd.DataFrame([item.split(',') for item in data_json['data']['klines']])
temp_df.columns = [
    "日期时间",
    "开盘",
    "收盘",
    "最高",
    "最低",
    "成交量",
    "成交额",
    "振幅",
    "涨跌幅",
    "涨跌额",
    "换手率",
]
temp_df['开盘'] = pd.to_numeric(temp_df['开盘'])
temp_df['收盘'] = pd.to_numeric(temp_df['收盘'])
temp_df['最高'] = pd.to_numeric(temp_df['最高'])
temp_df['最低'] = pd.to_numeric(temp_df['最低'])
temp_df['成交量'] = pd.to_numeric(temp_df['成交量'])
temp_df['成交额'] = pd.to_numeric(temp_df['成交额'])
temp_df['振幅'] = pd.to_numeric(temp_df['振幅'])
temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'])
temp_df['涨跌额'] = pd.to_numeric(temp_df['涨跌额'])
temp_df['换手率'] = pd.to_numeric(temp_df['换手率'])
