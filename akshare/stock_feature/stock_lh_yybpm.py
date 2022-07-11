#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/4/19 16:56
Desc: 同花顺-数据中心-营业部排名
http://data.10jqka.com.cn/market/longhu/
"""
import requests
import pandas as pd
from tqdm import tqdm


def stock_lh_yyb_most() -> pd.DataFrame:
    """
    同花顺-数据中心-营业部排名-上榜次数最多
    http://data.10jqka.com.cn/market/longhu/
    :return: 上榜次数最多
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    for page in tqdm(range(1, 11)):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
        url = f'http://data.10jqka.com.cn/ifmarket/lhbyyb/type/1/tab/sbcs/field/sbcs/sort/desc/page/{page}/'
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = big_df.append(temp_df)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def stock_lh_yyb_capital() -> pd.DataFrame:
    """
    同花顺-数据中心-营业部排名-资金实力最强
    http://data.10jqka.com.cn/market/longhu/
    :return: 资金实力最强
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    for page in tqdm(range(1, 11)):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
        url = f'http://data.10jqka.com.cn/ifmarket/lhbyyb/type/1/tab/zjsl/field/zgczje/sort/desc/page/{page}/'
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = big_df.append(temp_df)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def stock_lh_yyb_control() -> pd.DataFrame:
    """
    同花顺-数据中心-营业部排名-抱团操作实力
    http://data.10jqka.com.cn/market/longhu/
    :return: 抱团操作实力
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    for page in tqdm(range(1, 11)):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
        url = f'http://data.10jqka.com.cn/ifmarket/lhbyyb/type/1/tab/btcz/field/xsjs/sort/desc/page/{page}/'
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = big_df.append(temp_df)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


if __name__ == '__main__':
    stock_lh_yyb_most_df = stock_lh_yyb_most()
    print(stock_lh_yyb_most_df)

    stock_lh_yyb_capital_df = stock_lh_yyb_capital()
    print(stock_lh_yyb_capital_df)

    stock_lh_yyb_control_df = stock_lh_yyb_control()
    print(stock_lh_yyb_control_df)
