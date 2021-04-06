# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/4/6 15:19
Desc: 东方财富网-数据中心-新股数据-注册制审核
http://data.eastmoney.com/kcb/?type=nsb
"""
import pandas as pd
import requests


def stock_register_kcb() -> pd.DataFrame:
    """
    东方财富网-数据中心-新股数据-注册制审核-科创板
    http://data.eastmoney.com/kcb/?type=nsb
    :return: 科创板注册制审核结果
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/get"
    params = {
        'st': 'UPDATE_DATE',
        'sr': '-1',
        'ps': '5000',
        'p': '1',
        'type': 'RPT_REGISTERED_INFO',
        'sty': 'ORG_CODE,ORG_CODE_OLD,ISSUER_NAME,CHECK_STATUS,CHECK_STATUS_CODE,REG_ADDRESS,CSRC_INDUSTRY,RECOMMEND_ORG,LAW_FIRM,ACCOUNT_FIRM,UPDATE_DATE,ACCEPT_DATE,TOLIST_MARKET,SECURITY_CODE',
        'token': '894050c76af8597a853f5b408b759f5d',
        'client': 'WEB',
        'filter': '(TOLIST_MARKET="科创板")',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    page_num = data_json['result']['pages']
    big_df = pd.DataFrame()
    for page in range(1, page_num+1):
        params = {
            'st': 'UPDATE_DATE',
            'sr': '-1',
            'ps': '5000',
            'p': page,
            'type': 'RPT_REGISTERED_INFO',
            'sty': 'ORG_CODE,ORG_CODE_OLD,ISSUER_NAME,CHECK_STATUS,CHECK_STATUS_CODE,REG_ADDRESS,CSRC_INDUSTRY,RECOMMEND_ORG,LAW_FIRM,ACCOUNT_FIRM,UPDATE_DATE,ACCEPT_DATE,TOLIST_MARKET,SECURITY_CODE',
            'token': '894050c76af8597a853f5b408b759f5d',
            'client': 'WEB',
            'filter': '(TOLIST_MARKET="科创板")',
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        }
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json['result']["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df['index'] = range(1, len(big_df) + 1)
    big_df.columns = [
        "序号",
        "_",
        "_",
        "发行人全称",
        "审核状态",
        "_",
        "注册地",
        "证监会行业",
        "保荐机构",
        "律师事务所",
        "会计师事务所",
        "更新日期",
        "受理日期",
        "拟上市地点",
        "_",
    ]
    big_df = big_df[
        [
            "序号",
            "发行人全称",
            "审核状态",
            "注册地",
            "证监会行业",
            "保荐机构",
            "律师事务所",
            "会计师事务所",
            "更新日期",
            "受理日期",
            "拟上市地点",
        ]
    ]
    return big_df


def stock_register_cyb() -> pd.DataFrame:
    """
    东方财富网-数据中心-新股数据-注册制审核-创业板
    http://data.eastmoney.com/xg/cyb/
    :return: 创业板注册制审核结果
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter.eastmoney.com/securities/api/data/get"
    params = {
        'st': 'UPDATE_DATE',
        'sr': '-1',
        'ps': '5000',
        'p': '1',
        'type': 'RPT_REGISTERED_INFO',
        'sty': 'ORG_CODE,ORG_CODE_OLD,ISSUER_NAME,CHECK_STATUS,CHECK_STATUS_CODE,REG_ADDRESS,CSRC_INDUSTRY,RECOMMEND_ORG,LAW_FIRM,ACCOUNT_FIRM,UPDATE_DATE,ACCEPT_DATE,TOLIST_MARKET,SECURITY_CODE',
        'token': '894050c76af8597a853f5b408b759f5d',
        'client': 'WEB',
        'filter': '(TOLIST_MARKET="创业板")',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    page_num = data_json['result']['pages']
    big_df = pd.DataFrame()
    for page in range(1, page_num+1):
        params = {
            'st': 'UPDATE_DATE',
            'sr': '-1',
            'ps': '5000',
            'p': page,
            'type': 'RPT_REGISTERED_INFO',
            'sty': 'ORG_CODE,ORG_CODE_OLD,ISSUER_NAME,CHECK_STATUS,CHECK_STATUS_CODE,REG_ADDRESS,CSRC_INDUSTRY,RECOMMEND_ORG,LAW_FIRM,ACCOUNT_FIRM,UPDATE_DATE,ACCEPT_DATE,TOLIST_MARKET,SECURITY_CODE',
            'token': '894050c76af8597a853f5b408b759f5d',
            'client': 'WEB',
            'filter': '(TOLIST_MARKET="创业板")',
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        }
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json['result']["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df['index'] = range(1, len(big_df) + 1)
    big_df.columns = [
        "序号",
        "_",
        "_",
        "发行人全称",
        "审核状态",
        "_",
        "注册地",
        "证监会行业",
        "保荐机构",
        "律师事务所",
        "会计师事务所",
        "更新日期",
        "受理日期",
        "拟上市地点",
        "_",
    ]
    big_df = big_df[
        [
            "序号",
            "发行人全称",
            "审核状态",
            "注册地",
            "证监会行业",
            "保荐机构",
            "律师事务所",
            "会计师事务所",
            "更新日期",
            "受理日期",
            "拟上市地点",
        ]
    ]
    return big_df


if __name__ == "__main__":
    stock_register_kcb_df = stock_register_kcb()
    print(stock_register_kcb_df)

    stock_register_cyb_df = stock_register_cyb()
    print(stock_register_cyb_df)
