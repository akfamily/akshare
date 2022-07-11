#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2020/11/8 17:28
Desc: 新浪财经-债券-沪深债券-实时行情数据和历史行情数据
http://vip.stock.finance.sina.com.cn/mkt/#hs_z
"""
import datetime
import re

from akshare.utils import demjson
import pandas as pd
import requests
from py_mini_racer import py_mini_racer
from tqdm import tqdm

from akshare.bond.cons import (
    zh_sina_bond_hs_count_url,
    zh_sina_bond_hs_payload,
    zh_sina_bond_hs_url,
    zh_sina_bond_hs_hist_url,
)
from akshare.stock.cons import hk_js_decode


def get_zh_bond_hs_page_count() -> int:
    """
    行情中心首页-债券-沪深债券的总页数
    http://vip.stock.finance.sina.com.cn/mkt/#hs_z
    :return: 总页数
    :rtype: int
    """
    params = {
        "node": "hs_z",
    }
    res = requests.get(zh_sina_bond_hs_count_url, params=params)
    page_count = int(re.findall(re.compile(r"\d+"), res.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1


def bond_zh_hs_spot() -> pd.DataFrame:
    """
    新浪财经-债券-沪深债券-实时行情数据, 大量抓取容易封IP
    http://vip.stock.finance.sina.com.cn/mkt/#hs_z
    :return: 所有沪深债券在当前时刻的实时行情数据
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = get_zh_bond_hs_page_count()
    zh_sina_bond_hs_payload_copy = zh_sina_bond_hs_payload.copy()
    for page in tqdm(range(1, page_count + 1), leave=False):
        zh_sina_bond_hs_payload_copy.update({"page": page})
        res = requests.get(zh_sina_bond_hs_url, params=zh_sina_bond_hs_payload_copy)
        data_json = demjson.decode(res.text)
        big_df = big_df.append(pd.DataFrame(data_json), ignore_index=True)
    big_df.columns = [
        '代码',
        '-',
        '名称',
        '最新价',
        '涨跌额',
        '涨跌幅',
        '买入',
        '卖出',
        '昨收',
        '今开',
        '最高',
        '最低',
        '成交量',
        '成交额',
        '-',
        '-',
        '-',
        '-',
        '-',
        '-',
    ]
    big_df = big_df[[
        '代码',
        '名称',
        '最新价',
        '涨跌额',
        '涨跌幅',
        '买入',
        '卖出',
        '昨收',
        '今开',
        '最高',
        '最低',
        '成交量',
        '成交额',
    ]]
    big_df['最新价'] = pd.to_numeric(big_df['最新价'])
    big_df['买入'] = pd.to_numeric(big_df['买入'])
    big_df['卖出'] = pd.to_numeric(big_df['卖出'])
    big_df['昨收'] = pd.to_numeric(big_df['昨收'])
    big_df['今开'] = pd.to_numeric(big_df['今开'])
    big_df['最高'] = pd.to_numeric(big_df['最高'])
    big_df['最低'] = pd.to_numeric(big_df['最低'])
    return big_df


def bond_zh_hs_daily(symbol: str = "sh010107") -> pd.DataFrame:
    """
    新浪财经-债券-沪深债券-历史行情数据, 大量抓取容易封IP
    http://vip.stock.finance.sina.com.cn/mkt/#hs_z
    :param symbol: 沪深债券代码; e.g., sh010107
    :type symbol: str
    :return: 指定沪深债券代码的日 K 线数据
    :rtype: pandas.DataFrame
    """
    res = requests.get(
        zh_sina_bond_hs_hist_url.format(
            symbol, datetime.datetime.now().strftime("%Y_%m_%d")
        )
    )
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(hk_js_decode)
    dict_list = js_code.call(
        "d", res.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df["date"] = pd.to_datetime(data_df["date"]).dt.date
    data_df['open'] = pd.to_numeric(data_df['open'])
    data_df['high'] = pd.to_numeric(data_df['high'])
    data_df['low'] = pd.to_numeric(data_df['low'])
    data_df['close'] = pd.to_numeric(data_df['close'])
    return data_df


if __name__ == "__main__":
    bond_zh_hs_spot_df = bond_zh_hs_spot()
    print(bond_zh_hs_spot_df)

    bond_zh_hs_daily_df = bond_zh_hs_daily(symbol="sh110033")
    print(bond_zh_hs_daily_df)
