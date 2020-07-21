# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/17 21:34
Desc: 新浪财经-国内期货-实时数据获取
http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_3
P.S. 注意抓取速度, 容易封 IP 地址
"""
import time
import json

import demjson
import pandas as pd
import requests

from akshare.futures.cons import (zh_subscribe_exchange_symbol_url,
                                  zh_match_main_contract_url,
                                  zh_match_main_contract_payload)


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
            main_contract = data_df[data_df.iloc[:, 3:].duplicated()]
            print(main_contract["symbol"].values[0])
            subscribe_cffex_list.append(main_contract["symbol"].values[0])
        except:
            print(item, "无主力合约")
            continue
    print("主力合约获取成功")
    return ','.join(["nf_" + item for item in subscribe_cffex_list])


def futures_zh_spot(
        subscribe_list="nf_IF1912,nf_TF1912,nf_IH1912,nf_IC1912",
        market="CF"):
    url = f"https://hq.sinajs.cn/rn={round(time.time() * 1000)}&list={subscribe_list}"
    res = requests.get(url)
    data_df = pd.DataFrame([item.strip().split("=")[1].split(
        ",") for item in res.text.split(";") if item.strip() != ""])
    data_df.iloc[:, 0] = data_df.iloc[:, 0].str.replace('"', "")
    data_df.iloc[:, -1] = data_df.iloc[:, -1].str.replace('"', "")
    if market == "CF":
        data_df.columns = [
            "symbol",
            "time",
            "open",
            "high",
            "low",
            "last_close",
            "bid_price",
            "ask_price",
            "current_price",
            "avg_price",
            "last_settle_price",
            "buy_vol",
            "sell_vol",
            "hold",
            "volume",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_"]
        return data_df[["symbol",
                        "time",
                        "open",
                        "high",
                        "low",
                        "current_price",
                        "bid_price",
                        "ask_price",
                        "buy_vol",
                        "sell_vol",
                        "hold",
                        "volume",
                        "avg_price",
                        "last_close",
                        "last_settle_price",
                        ]]
    else:
        data_df.columns = [
            "open",
            "high",
            "low",
            "current_price",
            "volume",
            "amount",
            "hold",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_"
            "_",
            "time",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "symbol"]
        return data_df[["symbol",
                        "time",
                        "open",
                        "high",
                        "low",
                        "current_price",
                        "hold",
                        "volume",
                        "amount"
                        ]]


def futures_zh_minute_sina(symbol: str = "IF2008", period: str = "5") -> pd.DataFrame:
    """
    中国各品种期货分钟频率数据
    http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_3
    :param symbol: 可以通过 match_main_contract(exchange="cffex") 获取, 或者访问网页获取
    :type symbol: str
    :param period: choice of {"1": "1分钟", "5": "5分钟", "15": "15分钟", "30": "30分钟", "60": "60分钟"}
    :type period: str
    :return: 指定 symbol 和 period 的数据
    :rtype: pandas.DataFrame
    """
    url = 'https://stock2.finance.sina.com.cn/futures/api/jsonp.php/=/InnerFuturesNewService.getFewMinLine'
    params = {
        "symbol": symbol,
        "type": period,
    }
    r = requests.get(url, params=params)
    temp_df = pd.DataFrame(json.loads(r.text.split('=(')[1].split(");")[0]))
    temp_df.columns = ["date", "open", "high", "low", "close", "volume", "hold"]
    return temp_df


if __name__ == "__main__":
    futures_zh_minute_sina_df = futures_zh_minute_sina(symbol="TF2009", period="1")
    print(futures_zh_minute_sina_df)
    print("开始接收实时行情, 每秒刷新一次")
    dce_text = match_main_contract(exchange="dce")
    czce_text = match_main_contract(exchange="czce")
    shfe_text = match_main_contract(exchange="shfe")
    while True:
        time.sleep(3)
        data = futures_zh_spot(
            subscribe_list=",".join([dce_text, czce_text, shfe_text]),
            market="CF")
        print(data)

    # 金融期货单独订阅
    cffex_text = match_main_contract(exchange="cffex")

    while True:
        time.sleep(3)
        data = futures_zh_spot(subscribe_list=cffex_text, market="FF")
        print(data)
