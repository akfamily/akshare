# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/12/11 19:54
Desc: 中国外汇交易中心暨全国银行间同业拆借中心
中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场做市报价
中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场成交行情
http://www.chinamoney.com.cn/chinese/mkdatabond/
"""
from operator import itemgetter

import numpy as np
import pandas as pd
import requests


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
        quote_data.columns = ["债券简称", "报价机构", "买入/卖出净价(元)", "买入/卖出收益率(%)"]
        quote_data_out = quote_data_out.append(quote_data, ignore_index=True)
    quote_data_out.replace("---", np.nan, inplace=True)
    return quote_data_out


def bond_spot_deal():
    """
    中国外汇交易中心暨全国银行间同业拆借中心-市场数据-债券市场行情-现券市场成交行情
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


def bond_china_yield(start_date="2019-02-04", end_date="2020-02-04"):
    """
    中国债券信息网-国债及其他债券收益率曲线
    https://www.chinabond.com.cn/
    http://yield.chinabond.com.cn/cbweb-pbc-web/pbc/historyQuery?startDate=2019-02-07&endDate=2020-02-04&gjqx=0&qxId=ycqx&locale=cn_ZH
    注意: end_date - start_date 应该小于一年
    :param start_date: 需要查询的日期, 返回在该日期之后一年内的数据
    :type start_date: str
    :param end_date: 需要查询的日期, 返回在该日期之前一年内的数据
    :type end_date: str
    :return: 返回在指定日期之间之前一年内的数据
    :rtype: pandas.DataFrame
    """
    url = "http://yield.chinabond.com.cn/cbweb-pbc-web/pbc/historyQuery"
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "gjqx": "0",
        "qxId": "ycqx",
        "locale": "cn_ZH",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    }
    res = requests.get(url, params=params, headers=headers)
    data_text = res.text.replace("&nbsp", "")
    data_df = pd.read_html(data_text, header=0)[1]
    return data_df


if __name__ == "__main__":
    bond_spot_quote_df = bond_spot_quote()
    print(bond_spot_quote_df)
    bond_spot_deal_df = bond_spot_deal()
    print(bond_spot_deal_df)
    bond_china_yield_df = bond_china_yield(start_date="2018-01-01", end_date="2019-01-01")
    print(bond_china_yield_df)
