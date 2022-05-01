#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/5/1 20:23
Desc: 东方财富网-数据中心-特色数据-高管持股
http://data.eastmoney.com/executive/gdzjc.html
"""
from tqdm import tqdm

import pandas as pd
import requests


def stock_ggcg_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-高管持股
    http://data.eastmoney.com/executive/gdzjc.html
    :return: 高管持股
    :rtype: pandas.DataFrame
    """
    url = 'https://datacenter-web.eastmoney.com/api/data/v1/get'
    params = {
        'sortColumns': 'END_DATE,SECURITY_CODE,EITIME',
        'sortTypes': '-1,-1,-1',
        'pageSize': '500',
        'pageNumber': '1',
        'reportName': 'RPT_SHARE_HOLDER_INCREASE',
        'quoteColumns': 'f2~01~SECURITY_CODE~NEWEST_PRICE,f3~01~SECURITY_CODE~CHANGE_RATE_QUOTES',
        'columns': 'ALL',
        'source': 'WEB',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json['result']['pages']
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page+1), leave=False):
        params.update({
            'pageNumber': page,
        })
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json['result']['data'])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.columns = [
        '持股变动信息-变动数量',
        '公告日',
        '代码',
        '股东名称',
        '持股变动信息-占总股本比例',
        '_',
        '-',
        '变动截止日',
        '-',
        '变动后持股情况-持股总数',
        '变动后持股情况-占总股本比例',
        '_',
        '变动后持股情况-占流通股比例',
        '变动后持股情况-持流通股数',
        '_',
        '名称',
        '持股变动信息-增减',
        '_',
        '持股变动信息-占流通股比例',
        '变动开始日',
        '_',
        '最新价',
        '涨跌幅',
        '_',
    ]

    big_df = big_df[[
        '代码',
        '名称',
        '最新价',
        '涨跌幅',
        '股东名称',
        '持股变动信息-增减',
        '持股变动信息-变动数量',
        '持股变动信息-占总股本比例',
        '持股变动信息-占流通股比例',
        '变动后持股情况-持股总数',
        '变动后持股情况-占总股本比例',
        '变动后持股情况-持流通股数',
        '变动后持股情况-占流通股比例',
        '变动开始日',
        '变动截止日',
        '公告日',
    ]]

    big_df['最新价'] = pd.to_numeric(big_df['最新价'], errors="coerce")
    big_df['涨跌幅'] = pd.to_numeric(big_df['涨跌幅'], errors="coerce")
    big_df['持股变动信息-变动数量'] = pd.to_numeric(big_df['持股变动信息-变动数量'])
    big_df['持股变动信息-占总股本比例'] = pd.to_numeric(big_df['持股变动信息-占总股本比例'])
    big_df['持股变动信息-占流通股比例'] = pd.to_numeric(big_df['持股变动信息-占流通股比例'])
    big_df['变动后持股情况-持股总数'] = pd.to_numeric(big_df['变动后持股情况-持股总数'])
    big_df['变动后持股情况-占总股本比例'] = pd.to_numeric(big_df['变动后持股情况-占总股本比例'])
    big_df['变动后持股情况-持流通股数'] = pd.to_numeric(big_df['变动后持股情况-持流通股数'])
    big_df['变动后持股情况-占流通股比例'] = pd.to_numeric(big_df['变动后持股情况-占流通股比例'])
    big_df['变动开始日'] = pd.to_datetime(big_df['变动开始日']).dt.date
    big_df['变动截止日'] = pd.to_datetime(big_df['变动截止日']).dt.date
    big_df['公告日'] = pd.to_datetime(big_df['公告日']).dt.date

    return big_df


if __name__ == '__main__':
    stock_ggcg_em_df = stock_ggcg_em()
    print(stock_ggcg_em_df)
