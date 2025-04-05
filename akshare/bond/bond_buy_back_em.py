#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/4/5 17:30
Desc: 东方财富网-行情中心-债券市场-质押式回购
https://quote.eastmoney.com/center/gridlist.html#bond_sz_buyback
"""

import pandas as pd

import requests


def bond_sh_buy_back_em() -> pd.DataFrame:
    """
    东方财富网-行情中心-债券市场-上证质押式回购
    https://quote.eastmoney.com/center/gridlist.html#bond_sh_buyback
    :return: 上证质押式回购
    :rtype: pandas.DataFrame
    """
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "np": "1",
        "fltt": "1",
        "invt": "2",
        "fs": "m:1+b:MK0356",
        "fields": "f12,f13,f14,f1,f2,f4,f3,f152,f17,f18,f15,f16,f5,f6",
        "fid": "f6",
        "pn": "1",
        "pz": "20",
        "po": "1",
        "dect": "1",
        "wbp2u": "|0|0|0|web",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data']['diff'])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = temp_df['index'] + 1
    temp_df.rename(
        columns={
            "index": "序号",
            "f2": "最新价",
            "f3": "涨跌幅",
            "f4": "涨跌额",
            "f5": "成交量(手)",
            "f6": "成交额",
            "f12": "代码",
            "f14": "名称",
            "f15": "最高",
            "f16": "最低",
            "f17": "今开",
            "f18": "昨收",
        },
        inplace=True,
    )

    temp_df = temp_df[[
        "序号",
        "代码",
        "名称",
        "最新价",
        "涨跌额",
        "涨跌幅",
        "今开",
        "最高",
        "最低",
        "昨收",
        "成交量(手)",
        "成交额",
    ]]
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce") / 1000
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce") / 100
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce") / 1000
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce") / 1000
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce") / 1000
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce") / 1000
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce") / 1000
    temp_df["成交量(手)"] = pd.to_numeric(temp_df["成交量(手)"], errors="coerce") / 10000
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce") / 10000
    return temp_df


def bond_sz_buy_back_em() -> pd.DataFrame:
    """
    东方财富网-行情中心-债券市场-深证质押式回购
    https://quote.eastmoney.com/center/gridlist.html#bond_sz_buyback
    :return: 深证质押式回购
    :rtype: pandas.DataFrame
    """
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "np": "1",
        "fltt": "1",
        "invt": "2",
        "fs": "m:0+b:MK0356",
        "fields": "f12,f13,f14,f1,f2,f4,f3,f152,f17,f18,f15,f16,f5,f6",
        "fid": "f6",
        "pn": "1",
        "pz": "20",
        "po": "1",
        "dect": "1",
        "wbp2u": "|0|0|0|web",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data']['diff'])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = temp_df['index'] + 1
    temp_df.rename(
        columns={
            "index": "序号",
            "f2": "最新价",
            "f3": "涨跌幅",
            "f4": "涨跌额",
            "f5": "成交量(手)",
            "f6": "成交额",
            "f12": "代码",
            "f14": "名称",
            "f15": "最高",
            "f16": "最低",
            "f17": "今开",
            "f18": "昨收",
        },
        inplace=True,
    )

    temp_df = temp_df[[
        "序号",
        "代码",
        "名称",
        "最新价",
        "涨跌额",
        "涨跌幅",
        "今开",
        "最高",
        "最低",
        "昨收",
        "成交量(手)",
        "成交额",
    ]]
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce") / 1000
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce") / 100
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce") / 1000
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce") / 1000
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce") / 1000
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce") / 1000
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce") / 1000
    temp_df["成交量(手)"] = pd.to_numeric(temp_df["成交量(手)"], errors="coerce") / 10000
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce") / 10000
    return temp_df


if __name__ == "__main__":
    bond_sh_buy_back_em_df = bond_sh_buy_back_em()
    print(bond_sh_buy_back_em_df)

    bond_sz_buy_back_em_df = bond_sz_buy_back_em()
    print(bond_sz_buy_back_em_df)
