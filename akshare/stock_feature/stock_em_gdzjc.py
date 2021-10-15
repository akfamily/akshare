# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/4/26 14:57
Desc: 东方财富网-数据中心-特色数据-高管持股
http://data.eastmoney.com/executive/gdzjc.html
"""
import warnings

import pandas as pd
import requests


def stock_em_ggcg():
    """
    东方财富网-数据中心-特色数据-高管持股
    http://data.eastmoney.com/executive/gdzjc.html
    :return: 高管持股
    :rtype: pandas.DataFrame
    """
    warnings.warn("正在下载数据，请稍等")
    url = 'http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/GDZC/GetGDZC'
    params = {
        'pageSize': '5000000',
        'pageNum': '1',
        'tkn': 'eastmoney',
        'cfg': 'gdzc',
        'secucode': '',
        'fx': '',
        'sharehdname': '',
        'sortFields': 'BDJZ',
        'sortDirec': '1',
        'startDate': '',
        'endDate': '',
        'p': '1',
        'pageNo': '1',
        '_': '1619420305426',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    data_str_list = data_json['Data'][0]['Data']
    temp_df = pd.DataFrame([item.split('|') for item in data_str_list])
    temp_df.columns = [
        '_',
        '_',
        '代码',
        '最新价',
        '涨跌幅',
        '名称',
        '股东名称',
        '持股变动信息-增减',
        '持股变动信息-变动数量',
        '持股变动信息-占流通股比例',
        '持股变动信息-占总股本比例',
        '_',
        '变动后持股情况-持股总数',
        '变动后持股情况-占总股本比例',
        '变动后持股情况-持流通股数',
        '变动后持股情况-占流通股比例',
        '变动开始日',
        '变动截止日',
        '公告日',
    ]
    temp_df = temp_df[[
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
    return temp_df


if __name__ == '__main__':
    stock_em_ggcg_df = stock_em_ggcg()
    print(stock_em_ggcg_df)
