#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/3/15 15:46
Desc: 东方财富网-数据中心-年报季报-分红送配
http://data.eastmoney.com/yjfp/
"""
import pandas as pd
import requests


def stock_em_fhps(date: str = "20191231"):
    """
    东方财富网-数据中心-年报季报-分红送配
    http://data.eastmoney.com/yjfp/
    :param date: 分红送配报告期
    :type date: str
    :return: 分红送配
    :rtype: pandas.DataFrame
    """
    url = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get'
    params = {
        'st': 'YAGGR',
        'sr': '-1',
        'ps': '5000',
        'p': '1',
        'type': 'DCSOBS',
        'js': '{"data":(x),"pages":(tp)}',
        'token': '894050c76af8597a853f5b408b759f5d',
        'filter': f'(ReportingPeriod=^{"-".join([date[:4], date[4:6], date[6:]])}^)'
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data'])
    temp_df.columns = [
        '_',
        '代码',
        '名称',
        '送转股份-送转总比例',
        '送转股份-送转比例',
        '送转股份-转股比例',
        '现金分红-现金分红比例',
        '现金分红-股息率',
        '预案公告日',
        '_',
        '_',
        '股权登记日',
        '除权除息日',
        '_',
        '_',
        '总股本',
        '每股收益',
        '每股净资产',
        '每股公积金',
        '每股未分配利润',
        '净利润同比增长',
        '分红配送报告期',
        '_',
        '方案进度',
        '配送方案',
        '_',
        '_',
        '_',
        '最新公告日期',
        '_',
    ]
    temp_df = temp_df[[
        '代码',
        '名称',
        '送转股份-送转总比例',
        '送转股份-送转比例',
        '送转股份-转股比例',
        '现金分红-现金分红比例',
        '现金分红-股息率',
        '每股收益',
        '每股净资产',
        '每股公积金',
        '每股未分配利润',
        '净利润同比增长',
        '总股本',
        '预案公告日',
        '股权登记日',
        '除权除息日',
        '方案进度',
        '最新公告日期',
        '配送方案',
        '分红配送报告期',
    ]]
    return temp_df


if __name__ == '__main__':
    stock_em_fhps_df = stock_em_fhps(date="20201231")
    print(stock_em_fhps_df)
