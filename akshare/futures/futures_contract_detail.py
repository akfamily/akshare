# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/1/6 12:52
Desc: 查询期货合约当前时刻的详情
https://finance.sina.com.cn/futures/quotes/V2101.shtml
"""
import pandas as pd
import requests


def futures_contract_detail(contract: str = 'AP2101') -> pd.DataFrame:
    """
    查询期货合约详情
    https://finance.sina.com.cn/futures/quotes/V2101.shtml
    :param contract: 合约
    :type contract: str
    :return: 期货合约详情
    :rtype: pandas.DataFrame
    """
    url = f"https://finance.sina.com.cn/futures/quotes/{contract}.shtml"
    r = requests.get(url)
    r.encoding = 'gb2312'
    temp_df = pd.read_html(r.text)[6]
    data_one = temp_df.iloc[:, :2]
    data_one.columns = ['item', 'value']
    data_two = temp_df.iloc[:, 2:4]
    data_two.columns = ['item', 'value']
    data_three = temp_df.iloc[:, 4:]
    data_three.columns = ['item', 'value']
    temp_df = pd.concat([data_one, data_two, data_three], axis=0, ignore_index=True)
    return temp_df


if __name__ == '__main__':
    futures_contract_detail_df = futures_contract_detail(contract='V1903')
    print(futures_contract_detail_df)
