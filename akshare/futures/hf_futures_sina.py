# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/30 21:34
contact: jindaxiang@163.com
desc: 新浪财经-外盘期货-实时数据获取
"""
import time

import requests
import pandas as pd
import demjson

from akshare.futures.cons import (hf_subscribe_exchange_symbol_url,
                                  hf_subscribe_url,
                                  hf_subscribe_headers,
                                  hf_sina_spot_headers)


def hf_subscribe_exchange_symbol():
    res = requests.get(hf_subscribe_exchange_symbol_url, headers=hf_sina_spot_headers)
    res.encoding = "gb2312"
    data_json = demjson.decode(res.text[res.text.find("var oHF_1 = ") + 12: res.text.find("var oHF_2 = ") - 2])
    return list(data_json.keys())


def futures_hf_spot(subscribe_list=hf_subscribe_exchange_symbol()):
    payload = "&list=" + ",".join(["hf_" + item for item in subscribe_list])
    prefix = f"rn={round(time.time() * 1000)}"
    res = requests.get(hf_subscribe_url + prefix + payload, headers=hf_subscribe_headers)
    data_df = pd.DataFrame([item.strip().split("=")[1].split(
        ",") for item in res.text.split(";") if item.strip() != ""])
    data_df.iloc[:, 0] = data_df.iloc[:, 0].str.replace('"', "")
    data_df.iloc[:, -1] = data_df.iloc[:, -1].str.replace('"', "")
    data_df.columns = [
        "current_price",
        "-",
        "bid",
        "ask",
        "high",
        "low",
        "time",
        "last_settle_price",
        "open",
        "hold",
        "-",
        "-",
        "date",
        "symbol"]
    return data_df[["current_price",
                    "bid",
                    "ask",
                    "high",
                    "low",
                    "time",
                    "last_settle_price",
                    "open",
                    "hold",
                    "date",
                    "symbol"
                    ]]


if __name__ == "__main__":
    print("开始接收实时行情, 每秒刷新一次")
    while True:
        time.sleep(3)
        data = futures_hf_spot(subscribe_list=hf_subscribe_exchange_symbol())
        print(data)
