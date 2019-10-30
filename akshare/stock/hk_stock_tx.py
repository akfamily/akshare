# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/29 15:20
contact: jindaxiang@163.com
desc: 
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import demjson
import random

from akshare.stock.cons import (hk_headers,
                                hk_url,
                                hk_payload)


def get_ah_current():
    big_df = pd.DataFrame()
    for i in range(1, 7):
        hk_payload.update({"reqPage": i})
        res = requests.get(hk_url, params=hk_payload, headers=hk_headers)
        data_json = demjson.decode(res.text[res.text.find("{"): res.text.rfind("}") + 1])
        big_df = big_df.append(pd.DataFrame(data_json["data"]["page_data"]).iloc[:, 0].str.split("~", expand=True), ignore_index=True)
    big_df.columns = ["代码", "名称", "最新价", "涨跌幅", "涨跌额", "买入", "卖出", "成交量", "成交额", "今开", "昨收", "最高", "最低"]
    return big_df


def get_a_plus_h_stock_dict():
    big_df = pd.DataFrame()
    for i in range(1, 7):
        hk_payload.update({"reqPage": i})
        res = requests.get(hk_url, params=hk_payload, headers=hk_headers)
        data_json = demjson.decode(res.text[res.text.find("{"): res.text.rfind("}") + 1])
        big_df = big_df.append(pd.DataFrame(data_json["data"]["page_data"]).iloc[:, 0].str.split("~", expand=True), ignore_index=True)
    big_df.columns = ["代码", "名称", "最新价", "涨跌幅", "涨跌额", "买入", "卖出", "成交量", "成交额", "今开", "昨收", "最高", "最低"]
    big_dict = dict(zip(big_df["代码"], big_df["名称"]))
    return big_dict


def get_ah_his_data(symbol="02318", start_year="2000", end_year="2019"):
    big_df = pd.DataFrame()
    for year in range(int(start_year), int(end_year)):
        year = year
        url = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get"
        headers = {
            "Referer": "http://gu.qq.com/hk00168/gp",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        }
        payload = {
            "_var": f"kline_dayhfq{year}",
            "param": f"hk{symbol},day,{year}-01-01,{int(year)+1}-12-31,640,hfq",
            "r": random.random()
        }
        res = requests.get(url, params=payload, headers=headers)
        data_json = demjson.decode(res.text[res.text.find("{"): res.text.rfind("}") + 1])
        try:
            temp_df = pd.DataFrame(data_json["data"][f"hk{symbol}"]["hfqday"])
        except:
            continue
        temp_df.columns = ["日期", "开盘", "收盘", "最高", "最低", "成交量", "_", "_", "_"]
        temp_df = temp_df[["日期", "开盘", "收盘", "最高", "最低", "成交量"]]
        print("正在采集{}第{}年的数据".format(symbol, year))
        big_df = big_df.append(temp_df, ignore_index=True)
    return big_df


if __name__ == "__main__":
    big_dict = get_a_plus_h_stock_dict()
    for item in big_dict.keys():
        temp_df = get_ah_his_data(symbol=item, start_year="2000", end_year="2019")
        temp_df.to_csv(f"{item}.csv")
        print(f"{item}完成")
