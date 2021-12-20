#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/20 15:41
Desc: 新浪财经-期货的主力合约数据
https://finance.sina.com.cn/futuremarket/index.shtml
"""
import pandas as pd
import requests

from akshare.futures.cons import (
    zh_subscribe_exchange_symbol_url,
    zh_match_main_contract_url,
    zh_match_main_contract_payload,
)
from akshare.utils import demjson


def zh_subscribe_exchange_symbol(exchange: str = "dce") -> pd.DataFrame:
    """
    订阅指定交易所品种的代码
    :param exchange: choice of {"dce", "czce", "shfe", "cffex"}
    :type exchange: str
    :return: 订阅指定交易所品种的代码
    :rtype: pandas.DataFrame
    """
    r = requests.get(zh_subscribe_exchange_symbol_url)
    r.encoding = 'gb2312'
    data_json = demjson.decode(r.text[r.text.find("{"): r.text.find("};") + 1])
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


def match_main_contract(exchange: str = "shfe") -> pd.DataFrame:
    """
    指定交易所的所有可以提供数据的合约
    :param exchange: choice of {"dce", "czce", "shfe", "cffex"}
    :type exchange: str
    :return: 指定交易所的所有可以提供数据的合约
    :rtype: pandas.DataFrame
    """
    subscribe_list = []
    exchange_symbol_list = zh_subscribe_exchange_symbol(exchange).iloc[:, 1].tolist()
    for item in exchange_symbol_list:
        zh_match_main_contract_payload.update({"node": item})
        res = requests.get(
            zh_match_main_contract_url, params=zh_match_main_contract_payload
        )
        data_json = demjson.decode(res.text)
        data_df = pd.DataFrame(data_json)
        try:
            main_contract = data_df[data_df['name'].str.contains("连续") & data_df['symbol'].str.extract(r'([\w])(\d)').iloc[:, 1].str.contains("0")].iloc[0, :3]
            subscribe_list.append(main_contract)
        except:
            # print(item, "无主力连续合约")
            continue
    # print("主力连续合约获取成功")
    return pd.DataFrame(subscribe_list)


def futures_display_main_sina() -> pd.DataFrame:
    """
    新浪主力连续合约
    :return: 新浪主力连续合约
    :rtype: pandas.DataFrame
    """
    temp_df = pd.DataFrame()
    for item in ["dce", "czce", "shfe", "cffex"]:
        temp_df = temp_df.append(match_main_contract(exchange=item))
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


def futures_main_sina(symbol: str = "V0", trade_date: str = "20210817") -> pd.DataFrame:
    """
    新浪财经-期货-主力连续日数据
    http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1
    :param symbol: 通过 futures_display_main_sina 函数获取 symbol
    :type symbol: str
    :param trade_date: 交易日
    :type trade_date: str
    :return: 主力连续日数据
    :rtype: pandas.DataFrame
    """
    trade_date = trade_date[:4] + "_" + trade_date[4:6] + "_" + trade_date[6:]
    url = f"https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_{symbol}{trade_date}=/InnerFuturesNewService.getDailyKLine?symbol={symbol}&_={trade_date}"
    resp = requests.get(url)
    data_json = resp.text[resp.text.find("([") + 1: resp.text.rfind("])") + 1]
    data_df = pd.read_json(data_json)
    data_df.columns = ["日期", "开盘价", "最高价", "最低价", "收盘价", "成交量", "持仓量", "动态结算价"]
    return data_df


if __name__ == "__main__":
    futures_display_main_sina_df = futures_display_main_sina()
    print(futures_display_main_sina_df)

    futures_main_sina_hist = futures_main_sina(symbol="V0", trade_date="20210817")
    print(futures_main_sina_hist)
