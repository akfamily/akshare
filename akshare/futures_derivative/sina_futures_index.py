# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/25 17:41
contact: jindaxiang@163.com
desc: 
"""
import requests
import pandas as pd
import demjson

pd.set_option('display.max_rows', 500)

from akshare.futures.cons import (zh_subscribe_exchange_symbol_url,
                                  zh_match_main_contract_url,
                                  zh_match_main_contract_payload,
                                  zh_sina_spot_headers)


def zh_subscribe_exchange_symbol(exchange="dce"):
    res = requests.get(zh_subscribe_exchange_symbol_url)
    data_json = demjson.decode(
        res.text[res.text.find("{"): res.text.find("};") + 1])
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
    exchange_symbol_list = zh_subscribe_exchange_symbol(
        exchange).iloc[:, 1].tolist()
    for item in exchange_symbol_list:
        zh_match_main_contract_payload.update({"node": item})
        res = requests.get(
            zh_match_main_contract_url,
            params=zh_match_main_contract_payload)
        data_json = demjson.decode(res.text)
        data_df = pd.DataFrame(data_json)
        try:
            main_contract = data_df.iloc[0, :3]
            # print(main_contract)
            subscribe_cffex_list.append(main_contract)
        except:
            print(item, "无主力连续合约")
            continue
    print("主力连续合约获取成功")
    return pd.DataFrame(subscribe_cffex_list)


def futures_display_main_sina():
    temp_df = pd.DataFrame()
    for item in ["dce", "czce", "shfe", "cffex"]:
        temp_df = temp_df.append(match_main_contract(exchange=item))
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


def futures_main_sina(symbol="V0", trade_date="20191225"):
    """
    获取新浪财经-期货-主力连续日数据
    :return:
    """
    trade_date = trade_date[:4] + "_" + trade_date[4:6] + "_" + trade_date[6:]
    url = f"https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_{symbol}{trade_date}=/InnerFuturesNewService.getDailyKLine?symbol={symbol}&_={trade_date}"
    resp = requests.get(url)
    data_json = resp.text[resp.text.find("([")+1:resp.text.rfind("])")+1]
    data_df = pd.read_json(data_json)
    data_df.columns = ["日期", "开盘价", "最高价", "最低价", "收盘价", "成交量", "持仓量"]
    return data_df


if __name__ == '__main__':
    display_main_df = futures_display_main_sina()
    print(display_main_df)

    futures_hist = futures_main_sina(symbol="IF0", trade_date="20181220")
    print(futures_hist)
