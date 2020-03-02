# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/29 15:20
contact: jindaxiang@163.com
desc: 获取腾讯财经-A+H股数据, 实时行情数据和历史行情数据(后复权)
"""
import random

import requests
import pandas as pd
import demjson
from tqdm import tqdm

from akshare.stock.cons import (hk_url,
                                hk_headers,
                                hk_payload,
                                hk_stock_url,
                                hk_stock_headers,
                                hk_stock_payload)


def get_zh_stock_ah_page_count() -> int:
    hk_payload_copy = hk_payload.copy()
    hk_payload_copy.update({"reqPage": 1})
    res = requests.get(hk_url, params=hk_payload_copy, headers=hk_headers)
    data_json = demjson.decode(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    page_count = data_json["data"]["page_count"]
    return page_count


def stock_zh_ah_spot():
    big_df = pd.DataFrame()
    page_count = get_zh_stock_ah_page_count() + 1
    for i in tqdm(range(1, page_count)):
        hk_payload.update({"reqPage": i})
        res = requests.get(hk_url, params=hk_payload, headers=hk_headers)
        data_json = demjson.decode(res.text[res.text.find("{"): res.text.rfind("}") + 1])
        big_df = big_df.append(pd.DataFrame(data_json["data"]["page_data"]).iloc[:, 0].str.split("~", expand=True), ignore_index=True)
    big_df.columns = ["代码", "名称", "最新价", "涨跌幅", "涨跌额", "买入", "卖出", "成交量", "成交额", "今开", "昨收", "最高", "最低"]
    return big_df


def stock_zh_ah_name():
    big_df = pd.DataFrame()
    page_count = get_zh_stock_ah_page_count() + 1
    for i in tqdm(range(1, page_count)):
        hk_payload.update({"reqPage": i})
        res = requests.get(hk_url, params=hk_payload, headers=hk_headers)
        data_json = demjson.decode(res.text[res.text.find("{"): res.text.rfind("}") + 1])
        big_df = big_df.append(pd.DataFrame(data_json["data"]["page_data"]).iloc[:, 0].str.split("~", expand=True), ignore_index=True)
    big_df.columns = ["代码", "名称", "最新价", "涨跌幅", "涨跌额", "买入", "卖出", "成交量", "成交额", "今开", "昨收", "最高", "最低"]
    code_name_dict = dict(zip(big_df["代码"], big_df["名称"]))
    return code_name_dict


def stock_zh_ah_daily(symbol="02318", start_year="2000", end_year="2019"):
    big_df = pd.DataFrame()
    for year in tqdm(range(int(start_year), int(end_year))):
        hk_stock_payload_copy = hk_stock_payload.copy()
        hk_stock_payload_copy.update({"_var": f"kline_dayhfq{year}"})
        hk_stock_payload_copy.update({"param": f"hk{symbol},day,{year}-01-01,{int(year) + 1}-12-31,640,hfq"})
        hk_stock_payload_copy.update({"r": random.random()})
        res = requests.get(hk_stock_url, params=hk_stock_payload_copy, headers=hk_stock_headers)
        data_json = demjson.decode(res.text[res.text.find("{"): res.text.rfind("}") + 1])
        try:
            temp_df = pd.DataFrame(data_json["data"][f"hk{symbol}"]["hfqday"])
        except:
            continue
        temp_df.columns = ["日期", "开盘", "收盘", "最高", "最低", "成交量", "_", "_", "_"]
        temp_df = temp_df[["日期", "开盘", "收盘", "最高", "最低", "成交量"]]
        # print("正在采集{}第{}年的数据".format(symbol, year))
        big_df = big_df.append(temp_df, ignore_index=True)
    return big_df


if __name__ == "__main__":
    stock_zh_ah_spot()
    big_dict = stock_zh_ah_name()
    for item in big_dict.keys():
        df = stock_zh_ah_daily(symbol=item, start_year="2000", end_year="2019")
        print(df)
        # temp_df.to_csv(f"{item}.csv")
        print(f"{item}完成")
