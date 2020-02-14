# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/02/14 11:28
contact: jindaxiang@163.com
desc: 新浪财经-债券-沪深可转债-实时行情数据和历史行情数据
"""
import datetime
import re

import demjson
import execjs
import pandas as pd
import requests

from akshare.bond.cons import (
    zh_sina_bond_hs_cov_count_url,
    zh_sina_bond_hs_cov_payload,
    zh_sina_bond_hs_cov_url,
    zh_sina_bond_hs_cov_hist_url,
)
from akshare.stock.cons import hk_js_decode


def get_zh_bond_hs_cov_page_count():
    """
    行情中心首页-债券-沪深可转债的总页数
    http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
    :return: 总页数
    :rtype: int
    """
    params = {
        "node": "hskzz_z",
    }
    res = requests.get(zh_sina_bond_hs_cov_count_url, params=params)
    page_count = int(re.findall(re.compile(r"\d+"), res.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1


def bond_zh_hs_cov_spot():
    """
    新浪财经-债券-沪深可转债的实时行情数据, 大量抓取容易封IP
    http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
    :return: 所有沪深可转债在当前时刻的实时行情数据
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = get_zh_bond_hs_cov_page_count()
    zh_sina_bond_hs_payload_copy = zh_sina_bond_hs_cov_payload.copy()
    for page in range(1, page_count + 1):
        print(page)
        zh_sina_bond_hs_payload_copy.update({"page": page})
        res = requests.get(zh_sina_bond_hs_cov_url, params=zh_sina_bond_hs_payload_copy)
        data_json = demjson.decode(res.text)
        big_df = big_df.append(pd.DataFrame(data_json), ignore_index=True)
    return big_df


def bond_zh_hs_cov_daily(symbol="sh113542"):
    """
    新浪财经-债券-沪深可转债的的历史行情数据, 大量抓取容易封IP
    http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
    :param symbol: 沪深可转债代码; e.g., sh010107
    :type symbol: str
    :return: 指定沪深可转债代码的日 K 线数据
    :rtype: pandas.DataFrame
    """
    res = requests.get(
        zh_sina_bond_hs_cov_hist_url.format(
            symbol, datetime.datetime.now().strftime("%Y_%m_%d")
        )
    )
    js_code = execjs.compile(hk_js_decode)
    dict_list = js_code.call(
        "d", res.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df["date"] = data_df["date"].str.split("T", expand=True).iloc[:, 0]
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["date"]
    data_df.astype("float")
    return data_df


if __name__ == "__main__":
    bond_zh_hs_cov_daily_df = bond_zh_hs_cov_daily(symbol="sh113542")
    print(bond_zh_hs_cov_daily_df)
    bond_zh_hs_cov_spot_df = bond_zh_hs_cov_spot()
    print(bond_zh_hs_cov_spot_df)
