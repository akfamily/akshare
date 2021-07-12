# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/7/12 15:47
Desc: 
"""
import requests
import pandas as pd


def stock_board_concept_em() -> pd.DataFrame:
    """

    :return:
    :rtype:
    """
    url = 'http://79.push2.eastmoney.com/api/qt/clist/get'
    params = {
        'pn': '1',
        'pz': '2000',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:90 t:3 f:!50',
        'fields': 'f2,f3,f4,f8,f12,f14,f15,f16,f17,f18,f20,f21,f24,f25,f22,f33,f11,f62,f128,f124,f107,f104,f105,f136',
        '_': '1626075887768'
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data']['diff'])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.columns = [
        '排名',
        '最新价',
        '涨跌幅',
        '涨跌额',
        '换手率',
        '_',
        '板块代码',
        '板块名称',
        '_',
        '_',
        '_',
        '_',
        '总市值',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '上涨家数',
        '下跌家数',
        '_',
        '_',
        '领涨股票',
        '_',
        '_',
        '领涨股票-涨跌幅',
    ]
    temp_df = temp_df[[
        '排名',
        '板块名称',
        '板块代码',
        '最新价',
        '涨跌额',
        '涨跌幅',
        '总市值',
        '换手率',
        '上涨家数',
        '下跌家数',
        '领涨股票',
        '领涨股票-涨跌幅'
    ]]
    return temp_df


def stock_board_concept_hist_em(symbol: str = "数字货币", adjust: str = "") -> pd.DataFrame:

    stock_board_concept_em_map = stock_board_concept_em()
    stock_board_code = stock_board_concept_em_map[stock_board_concept_em_map['板块名称'] == symbol]['板块代码'].values[0]
    adjust_map = {
        "": "0",
        "qfq": "1",
        "hfq": "2"
    }
    url = 'http://91.push2his.eastmoney.com/api/qt/stock/kline/get'
    params = {
        'secid': f'90.{stock_board_code}',
        'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
        'fields1': 'f1,f2,f3,f4,f5,f6',
        'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
        'klt': '101',
        'fqt': adjust_map[adjust],
        'beg': '0',
        'end': '20500101',
        'smplmt': '10000',
        'lmt': '1000000',
        '_': '1626079488673',
    }
    r = requests.get(url, params=params)
    data_json = r.json()

    temp_df = pd.DataFrame([item.split(",") for item in data_json['data']['klines']])
    temp_df.columns = [
        '日期',
        '开盘',
        '收盘',
        '最高',
        '最低',
        '成交量',
        '成交额',
        '振幅',
        '涨跌幅',
        '涨跌额',
        '换手率',
    ]
    temp_df = temp_df[[
        '日期',
        '开盘',
        '收盘',
        '最高',
        '最低',
        '涨跌幅',
        '涨跌额',
        '成交量',
        '成交额',
        '振幅',
        '换手率',
    ]]
    return temp_df


def stock_board_concept_cons_em(symbol: str = "车联网") -> pd.DataFrame:

    stock_board_concept_em_map = stock_board_concept_em()
    stock_board_code = stock_board_concept_em_map[stock_board_concept_em_map['板块名称'] == symbol]['板块代码'].values[0]
    url = 'http://29.push2.eastmoney.com/api/qt/clist/get'
    params = {
        'pn': '1',
        'pz': '20',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': f'b:{stock_board_code} f:!50',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f45',
        '_': '1626081702127',
    }
    r = requests.get(url, params=params)
    data_json = r.json()

    temp_df = pd.DataFrame(data_json['data']['diff'])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.columns = [
        '序号',
        '_',
        '最新价',
        '涨跌幅',
        '涨跌额',
        '成交量',
        '成交额',
        '振幅',
        '换手率',
        '市盈率-动态',
        '_',
        '_',
        '代码',
        '_',
        '名称',
        '最高',
        '最低',
        '今开',
        '昨收',
        '_',
        '_',
        '_',
        '市净率',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
    ]
    temp_df = temp_df[[
        '序号',
        '代码',
        '名称',
        '最新价',
        '涨跌幅',
        '涨跌额',
        '成交量',
        '成交额',
        '振幅',
        '最高',
        '最低',
        '今开',
        '昨收',
        '换手率',
        '市盈率-动态',
        '市净率',
    ]]
    return temp_df


if __name__ == '__main__':
    stock_board_concept_em_df = stock_board_concept_em()
    print(stock_board_concept_em_df)

    stock_board_concept_hist_em_df = stock_board_concept_hist_em(symbol="车联网", adjust="")
    print(stock_board_concept_hist_em_df)

    stock_board_concept_cons_em_df = stock_board_concept_cons_em(symbol="车联网")
    print(stock_board_concept_cons_em_df)
