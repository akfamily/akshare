#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/29 10:54
Desc: 东方财富网-行情中心-期权市场
http://quote.eastmoney.com/center
"""
import json

import pandas as pd
import requests


def option_current_em() -> pd.DataFrame:
    """
    东方财富网-行情中心-期权市场
    http://quote.eastmoney.com/center
    :return: 期权价格
    :rtype: pandas.DataFrame
    """
    url = 'http://23.push2.eastmoney.com/api/qt/clist/get'
    params = {
        'cb': 'jQuery112409395946290628259_1606225274048',
        'pn': '1',
        'pz': '200000',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:10,m:140,m:141,m:151',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f28,f11,f62,f128,f136,f115,f152,f133,f108,f163,f161,f162',
        '_': '1606225274063',
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find('{'):-2])
    temp_df = pd.DataFrame(data_json['data']['diff'])
    temp_df.columns = [
        '_',
        '最新价',
        '涨跌幅',
        '涨跌额',
        '成交量',
        '成交额',
        '_',
        '_',
        '_',
        '_',
        '_',
        '代码',
        '_',
        '名称',
        '_',
        '_',
        '今开',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '昨结',
        '_',
        '持仓量',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '行权价',
        '剩余日',
        '日增'
    ]
    temp_df = temp_df[[
        '代码',
        '名称',
        '最新价',
        '涨跌额',
        '涨跌幅',
        '成交量',
        '成交额',
        '持仓量',
        '行权价',
        '剩余日',
        '日增',
        '昨结',
        '今开'
    ]]
    temp_df['最新价'] = pd.to_numeric(temp_df['最新价'], errors='coerce')
    temp_df['涨跌额'] = pd.to_numeric(temp_df['涨跌额'], errors='coerce')
    temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'], errors='coerce')
    temp_df['成交量'] = pd.to_numeric(temp_df['成交量'], errors='coerce')
    temp_df['成交额'] = pd.to_numeric(temp_df['成交额'], errors='coerce')
    temp_df['持仓量'] = pd.to_numeric(temp_df['持仓量'], errors='coerce')
    temp_df['行权价'] = pd.to_numeric(temp_df['行权价'], errors='coerce')
    temp_df['剩余日'] = pd.to_numeric(temp_df['剩余日'], errors='coerce')
    temp_df['日增'] = pd.to_numeric(temp_df['日增'], errors='coerce')
    temp_df['昨结'] = pd.to_numeric(temp_df['昨结'], errors='coerce')
    temp_df['今开'] = pd.to_numeric(temp_df['今开'], errors='coerce')
    return temp_df


if __name__ == '__main__':
    option_daily_hist_em_df = option_current_em()
    print(option_daily_hist_em_df)
