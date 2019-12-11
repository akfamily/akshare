# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/11 19:54
contact: jindaxiang@163.com
desc:
获取中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场做市报价
获取中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场成交行情
http://www.chinamoney.com.cn/chinese/mkdatabond/
"""
from operator import itemgetter

import requests
import pandas as pd
import numpy as np


def get_quote_data():
    """
    获取中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场做市报价
    """
    quote_url = "http://www.chinamoney.com.cn/ags/ms/cm-u-md-bond/CbMktMakQuot?"
    payload = {
        "flag": "1",
        "lang": "cn",
        "abdAssetEncdShrtDesc": "",
        "emaEntyEncdShrtDesc": "",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/78.0.3904.108 Safari/537.36",
    }
    res = requests.post(url=quote_url, data=payload, headers=headers)  # 请求数据
    res.encoding = "utf-8"
    json_df = res.json()
    return json_df


def get_deal_data():
    """
    获取中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场成交行情
    """
    deal_url = "http://www.chinamoney.com.cn/ags/ms/cm-u-md-bond/CbtPri?"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/78.0.3904.108 Safari/537.36",
    }
    payload = {
        "flag": "1",
        "lang": "cn",
        "bondName": "",
    }
    res = requests.post(url=deal_url, data=payload, headers=headers)  # 请求数据
    res.encoding = "utf-8"
    json_df = res.json()
    return json_df


def bond_spot_quote():
    """
    处理中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场做市报价
    """
    data = get_quote_data()
    need_data = data["records"]
    keys_list = [
        "abdAssetEncdShrtDesc",
        "emaEntyEncdShrtDesc",
        "tradeAmnt",
        "contraRate",
    ]  # 定义要取的 value 的 keys
    quote_data_out = pd.DataFrame()
    for i in range(len(need_data)):
        quote_data = itemgetter(*keys_list)(need_data[i])
        quote_data = pd.DataFrame(quote_data).T
        quote_data.columns = ["报价机构", "债券简称", "买入/卖出净价(元)", "买入/卖出收益率(%)"]
        quote_data_out = quote_data_out.append(quote_data, ignore_index=True)
    quote_data_out.replace("---", np.nan, inplace=True)
    return quote_data_out


def bond_spot_deal():
    """
    处理中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场成交行情
    """
    data = get_deal_data()
    need_data = data["records"]
    keys_list = [
        "abdAssetEncdFullDescByRmb",
        "dmiLatestRateLabel",
        "dmiLatestContraRateLabel",
        "bpNum",
        "dmiWghtdContraRateLabel",
        "dmiPrvsClsngContraRate",
    ]
    deal_data_out = pd.DataFrame()
    for j in range(len(need_data)):
        deal_data = itemgetter(*keys_list)(need_data[j])
        deal_data = pd.DataFrame(deal_data).T
        deal_data.columns = [
            "债券简称",
            "成交净价(元)",
            "最新收益率(%)",
            "涨跌(BP)",
            "加权收益率(%)",
            "交易量(亿)",
        ]
        deal_data_out = deal_data_out.append(deal_data, ignore_index=True)
    deal_data_out.replace("---", np.nan, inplace=True)
    return deal_data_out


if __name__ == "__main__":
    quote_df = bond_spot_quote()
    print(quote_df)
    deal_df = bond_spot_deal()
    print(deal_df)
