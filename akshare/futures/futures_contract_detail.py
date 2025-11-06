#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/30 17:00
Desc: 查询期货合约当前时刻的详情
https://finance.sina.com.cn/futures/quotes/V2101.shtml
"""

from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup


def futures_contract_detail(symbol: str = "AP2101") -> pd.DataFrame:
    """
    查询期货合约详情
    https://finance.sina.com.cn/futures/quotes/V2101.shtml
    :param symbol: 合约
    :type symbol: str
    :return: 期货合约详情
    :rtype: pandas.DataFrame
    """
    url = f"https://finance.sina.com.cn/futures/quotes/{symbol}.shtml"
    r = requests.get(url)
    r.encoding = "gb2312"
    temp_df = pd.read_html(StringIO(r.text))[6]
    data_one = temp_df.iloc[:, :2]
    data_one.columns = ["item", "value"]
    data_two = temp_df.iloc[:, 2:4]
    data_two.columns = ["item", "value"]
    data_three = temp_df.iloc[:, 4:]
    data_three.columns = ["item", "value"]
    temp_df = pd.concat(
        objs=[data_one, data_two, data_three], axis=0, ignore_index=True
    )
    return temp_df


def futures_contract_detail_em(symbol: str = "v2602F") -> pd.DataFrame:
    """
    查询期货合约详情
    https://quote.eastmoney.com/qihuo/v2602F.html
    :param symbol: 合约
    :type symbol: str
    :return: 期货合约详情
    :rtype: pandas.DataFrame
    """
    url = f"https://quote.eastmoney.com/qihuo/{symbol}.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")
    url_text = \
        soup.find(name="div", attrs={"class": "sidertabbox_tsplit"}).find(name="div", attrs={"class": "onet"}).find(
            "a")[
            'href']
    inner_symbol = url_text.split("#")[-1].strip("futures_")
    url = f"https://futsse-static.eastmoney.com/redis?msgid={inner_symbol}_info"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame.from_dict(data_json, orient="index")
    column_mapping = {
        'vname': '交易品种',
        'vcode': '交易代码',
        'jydw': '交易单位',
        'bjdw': '报价单位',
        'market': '上市交易所',
        'zxbddw': '最小变动价格',
        'zdtbfd': '跌涨停板幅度',
        'hyjgyf': '合约交割月份',
        'jysj': '交易时间',
        'zhjyr': '最后交易日',
        'zhjgr': '最后交割日',
        'jgpj': '交割品级',
        'zcjybzj': '最初交易保证金',
        'jgfs': '交割方式'
    }
    temp_df.rename(index=column_mapping, inplace=True)
    temp_df.reset_index(drop=False, inplace=True)
    temp_df.columns = ['item', 'value']
    return temp_df


if __name__ == "__main__":
    futures_contract_detail_df = futures_contract_detail(symbol="V2101")
    print(futures_contract_detail_df)

    futures_contract_detail_em_df = futures_contract_detail_em(symbol="l2602F")
    print(futures_contract_detail_em_df)
