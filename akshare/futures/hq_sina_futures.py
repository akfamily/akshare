# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/30 21:34
contact: jindaxiang@163.com
desc: 新浪财经-国内期货-实时数据获取
"""
import time

import requests
import pandas as pd
import demjson

from akshare.futures.cons import (subscribe_exchange_symbol_url,
                                  match_main_contract_url,
                                  match_main_contract_payload)


def subscribe_exchange_symbol(exchange="dce"):
    res = requests.get(subscribe_exchange_symbol_url)
    data_json = demjson.decode(res.text[res.text.find("{"): res.text.find("};") + 1])
    if exchange == "czce":
        data_json["czce"].remove("郑州商品交易所")
        return pd.DataFrame(data_json["czce"])
    if exchange == "dce":
        data_json["dce"].remove("大连商品交易所")
        return pd.DataFrame(data_json["dce"])
    if exchange == "shfe":
        data_json["shfe"].remove("上海期货交易所")
        return pd.DataFrame(data_json["shfe"])
    if exchange == "cffex":
        data_json["cffex"].remove("中国金融期货交易所")
        return pd.DataFrame(data_json["cffex"])


def match_main_contract(exchange="dce"):
    subscribe_cffex_list = []
    exchange_symbol_list = subscribe_exchange_symbol(exchange).iloc[:, 1].tolist()
    for item in exchange_symbol_list:
        match_main_contract_payload.update({"node": item})
        res = requests.get(match_main_contract_url, params=match_main_contract_payload)
        data_json = demjson.decode(res.text)
        data_df = pd.DataFrame(data_json)
        try:
            main_contract = data_df[data_df.iloc[:, 3:].duplicated()]
            print(main_contract["symbol"].values[0])
            subscribe_cffex_list.append(main_contract["symbol"].values[0])
        except:
            print(item, "无主力合约")
            continue
    print("主力合约获取成功")
    return subscribe_cffex_list


def subscribe_exchange_tick():
    url = f"https://hq.sinajs.cn/rn={round(time.time() * 1000)}&list={sub_str}"
    res = requests.get(url)
    data_df = pd.DataFrame(
        [item.strip().split("=")[1].split(",") for item in res.text.split(";") if item.strip() != ""])
    data_df.iloc[:, 0] = data_df.iloc[:, 0].str.replace('"', "")
    data_df.iloc[:, -1] = data_df.iloc[:, -1].str.replace('"', "")
    data_df.columns = ["symbol", "time", "open", "high", "low", "pre_settle", "_", "_", "_", "_", "buy_vol", "sell_vol", "hold", "volume", "_", "_", "_""_", "_", "_", "_""_", "_", "_", "_""_", "_", "_", "_", "_", "_"]
    return data_df[["symbol", "time", "open", "high", "low", "pre_settle", "buy_vol", "sell_vol", "hold", "volume"]]


if __name__ == "__main__":
    subscribe_cffex_list = match_main_contract(exchange="dce")
    print("开始接收实时行情, 每秒刷新一次")
    sub_str = ','.join(["nf_" + item for item in subscribe_cffex_list])
    while True:
        time.sleep(1)
        data = subscribe_exchange_tick()
        print(data)
