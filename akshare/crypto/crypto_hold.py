# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/6/22 15:08
Desc: 金十数据-比特币持仓报告
https://datacenter.jin10.com/dc_report?name=bitcoint
"""
import requests
import pandas as pd


def crypto_bitcoin_hold_report():
    """
    金十数据-比特币持仓报告
    https://datacenter.jin10.com/dc_report?name=bitcoint
    :return: 比特币持仓报告
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-api.jin10.com/bitcoin_treasuries/list"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-version": "1.0.0",
    }
    params = {"_": "1618902583006"}
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["values"])
    temp_df.columns = [
        '代码',
        '公司名称-英文',
        '国家/地区',
        '市值',
        '比特币占市值比重',
        '持仓成本',
        '持仓占比',
        '持仓量',
        '当日持仓市值',
        '查询日期',
        '公告链接',
        '_',
        '分类',
        '倍数',
        '_',
        '公司名称-中文',
    ]
    temp_df = temp_df[[
        '代码',
        '公司名称-英文',
        '公司名称-中文',
        '国家/地区',
        '市值',
        '比特币占市值比重',
        '持仓成本',
        '持仓占比',
        '持仓量',
        '当日持仓市值',
        '查询日期',
        '公告链接',
        '分类',
        '倍数',
    ]]
    return temp_df


def crypto_bitcoin_hold_report():
    """
    金十数据-比特币持仓报告
    https://datacenter.jin10.com/dc_report?name=bitcoint
    :return: 比特币持仓报告
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-api.jin10.com/bitcoin_treasuries/list"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-version": "1.0.0",
    }
    params = {"_": "1618902583006"}
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["values"])
    temp_df.columns = [
        '代码',
        '公司名称-英文',
        '国家/地区',
        '市值',
        '比特币占市值比重',
        '持仓成本',
        '持仓占比',
        '持仓量',
        '当日持仓市值',
        '查询日期',
        '公告链接',
        '_',
        '分类',
        '倍数',
        '_',
        '公司名称-中文',
    ]
    temp_df = temp_df[[
        '代码',
        '公司名称-英文',
        '公司名称-中文',
        '国家/地区',
        '市值',
        '比特币占市值比重',
        '持仓成本',
        '持仓占比',
        '持仓量',
        '当日持仓市值',
        '查询日期',
        '公告链接',
        '分类',
        '倍数',
    ]]
    return temp_df


if __name__ == '__main__':
    crypto_bitcoin_hold_report_df = crypto_bitcoin_hold_report()
    print(crypto_bitcoin_hold_report_df)
