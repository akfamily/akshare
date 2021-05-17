# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/5/17 20:06
Desc: 东方财富网-数据中心-新股数据-增发-全部增发
http://data.eastmoney.com/other/gkzf.html
"""
import requests
import pandas as pd
import demjson


def stock_em_qbzf():
    """
    东方财富网-数据中心-新股数据-增发-全部增发
    http://data.eastmoney.com/other/gkzf.html
    :return: 全部增发
    :rtype: pandas.DataFrame
    """
    url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx'
    params = {
        'st': '5',
        'sr': '-1',
        'ps': '5000',
        'p': '1',
        'type': 'SR',
        'sty': 'ZF',
        'js': '({"pages":(pc),"data":[(x)]})',
        'stat': '0'
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        '股票代码',
        '股票简称',
        '发行方式',
        '发行总数',
        '发行价格',
        '最新价',
        '发行日期',
        '增发上市日期',
        '_',
        '增发代码',
        '网上发行',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
    ]
    temp_df = temp_df[[
        '股票代码',
        '股票简称',
        '增发代码',
        '发行方式',
        '发行总数',
        '网上发行',
        '发行价格',
        '最新价',
        '发行日期',
        '增发上市日期',
    ]]
    temp_df['锁定期'] = '1-3年'
    return temp_df


if __name__ == '__main__':
    stock_em_qbzf_df = stock_em_qbzf()
    print(stock_em_qbzf_df)
