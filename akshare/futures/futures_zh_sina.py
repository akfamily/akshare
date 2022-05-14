#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/31 13:20
Desc: 新浪财经-国内期货-实时数据获取
http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_3
P.S. 注意采集速度, 容易封禁 IP, 如果不能访问请稍后再试
"""
import json
import time

import pandas as pd
import requests

from akshare.futures.cons import (
    zh_subscribe_exchange_symbol_url,
    zh_match_main_contract_url,
    zh_match_main_contract_payload,
)
from akshare.futures.futures_contract_detail import futures_contract_detail
from akshare.utils import demjson


def zh_subscribe_exchange_symbol(symbol: str = "dce") -> dict:
    """
    交易所具体的可交易品种
    http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1
    :param symbol: choice of {'czce', 'dce', 'shfe', 'cffex'}
    :type symbol: str
    :return: 交易所具体的可交易品种
    :rtype: dict
    """
    r = requests.get(zh_subscribe_exchange_symbol_url)
    r.encoding = "gbk"
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): data_text.find("};") + 1])
    if symbol == "czce":
        data_json["czce"].remove("郑州商品交易所")
        return pd.DataFrame(data_json["czce"])
    if symbol == "dce":
        data_json["dce"].remove("大连商品交易所")
        return pd.DataFrame(data_json["dce"])
    if symbol == "shfe":
        data_json["shfe"].remove("上海期货交易所")
        return pd.DataFrame(data_json["shfe"])
    if symbol == "cffex":
        data_json["cffex"].remove("中国金融期货交易所")
        return pd.DataFrame(data_json["cffex"])


def match_main_contract(symbol: str = "cffex") -> str:
    """
    新浪财经-期货-主力合约
    http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1
    :param symbol: choice of {'czce', 'dce', 'shfe', 'cffex'}
    :type symbol: str
    :return: 主力合约的字符串
    :rtype: str
    """
    subscribe_exchange_list = []
    exchange_symbol_list = zh_subscribe_exchange_symbol(symbol).iloc[:, 1].tolist()
    for item in exchange_symbol_list:
        # item = 'sngz_qh'
        zh_match_main_contract_payload.update({"node": item})
        res = requests.get(
            zh_match_main_contract_url, params=zh_match_main_contract_payload
        )
        data_json = demjson.decode(res.text)
        data_df = pd.DataFrame(data_json)
        try:
            main_contract = data_df[data_df.iloc[:, 3:].duplicated()]
            print(main_contract["symbol"].values[0])
            subscribe_exchange_list.append(main_contract["symbol"].values[0])
        except:
            if len(data_df) == 1:
                subscribe_exchange_list.append(data_df["symbol"].values[0])
                print(data_df["symbol"].values[0])
            else:
                print(item, "无主力合约")
            continue
    print(f"{symbol}主力合约获取成功")
    return ",".join([item for item in subscribe_exchange_list])


def futures_zh_spot(
    symbol: str = 'V2205, P2205, B2201, M2205',
    market: str = "CF",
    adjust: str = '0',
) -> pd.DataFrame:
    """
    期货的实时行情数据
    http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1
    :param symbol: 合约名称的字符串组合
    :type symbol: str
    :param market: CF 为商品期货
    :type market: str
    :param adjust: '1' or '0'; 字符串的 0 或 1
    :type adjust: str
    :return: 期货的实时行情数据
    :rtype: pandas.DataFrame
    """
    subscribe_list = ','.join(['nf_' + item.strip() for item in symbol.split(',')])
    url = f"https://hq.sinajs.cn/rn={round(time.time() * 1000)}&list={subscribe_list}"
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Host': 'hq.sinajs.cn',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://vip.stock.finance.sina.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    data_df = pd.DataFrame(
        [
            item.strip().split("=")[1].split(",")
            for item in r.text.split(";")
            if item.strip() != ""
        ]
    )
    data_df.iloc[:, 0] = data_df.iloc[:, 0].str.replace('"', "")
    data_df.iloc[:, -1] = data_df.iloc[:, -1].str.replace('"', "")
    if adjust == '1':
        contract_name_list = [item.split("_")[1] for item in subscribe_list.split(",")]
        contract_min_list = []
        contract_exchange_list = []
        for contract_name in contract_name_list:
            # print(contract_name)
            # contract_name = 'AP2101'
            temp_df = futures_contract_detail(symbol=contract_name)
            exchange_name = temp_df[temp_df["item"] == "上市交易所"]["value"].values[0]
            contract_exchange_list.append(exchange_name)
            contract_min = temp_df[temp_df["item"] == "最小变动价位"]["value"].values[0]
            contract_min_list.append(contract_min)
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
                "_",
            ]
            data_df = data_df[
                [
                    "symbol",
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
                ]
            ]
            data_df["exchange"] = contract_exchange_list
            data_df["contract"] = contract_name_list
            data_df["contract_min_change"] = contract_min_list

            data_df['open'] = pd.to_numeric(data_df['open'])
            data_df['high'] = pd.to_numeric(data_df['high'])
            data_df['low'] = pd.to_numeric(data_df['low'])
            data_df['current_price'] = pd.to_numeric(data_df['current_price'])
            data_df['bid_price'] = pd.to_numeric(data_df['bid_price'])
            data_df['ask_price'] = pd.to_numeric(data_df['ask_price'])
            data_df['buy_vol'] = pd.to_numeric(data_df['buy_vol'])
            data_df['sell_vol'] = pd.to_numeric(data_df['sell_vol'])
            data_df['hold'] = pd.to_numeric(data_df['hold'])
            data_df['volume'] = pd.to_numeric(data_df['volume'])
            data_df['avg_price'] = pd.to_numeric(data_df['avg_price'])
            data_df['last_close'] = pd.to_numeric(data_df['last_close'])
            data_df['last_settle_price'] = pd.to_numeric(data_df['last_settle_price'])

            data_df.dropna(subset=['current_price'], inplace=True)
            return data_df
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
                "_" "_",
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
                "symbol",
            ]
            data_df = data_df[
                [
                    "symbol",
                    "time",
                    "open",
                    "high",
                    "low",
                    "current_price",
                    "hold",
                    "volume",
                    "amount",
                ]
            ]
            data_df["exchange"] = contract_exchange_list
            data_df["contract"] = contract_name_list
            data_df["contract_min_change"] = contract_min_list

            data_df['open'] = pd.to_numeric(data_df['open'])
            data_df['high'] = pd.to_numeric(data_df['high'])
            data_df['low'] = pd.to_numeric(data_df['low'])
            data_df['current_price'] = pd.to_numeric(data_df['current_price'])
            data_df['hold'] = pd.to_numeric(data_df['hold'])
            data_df['volume'] = pd.to_numeric(data_df['volume'])
            data_df['amount'] = pd.to_numeric(data_df['amount'])

            data_df.dropna(subset=['current_price'], inplace=True)
            return data_df
    else:
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
                "_",
            ]
            data_df = data_df[
                [
                    "symbol",
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
                ]
            ]

            data_df['open'] = pd.to_numeric(data_df['open'])
            data_df['high'] = pd.to_numeric(data_df['high'])
            data_df['low'] = pd.to_numeric(data_df['low'])
            data_df['current_price'] = pd.to_numeric(data_df['current_price'])
            data_df['bid_price'] = pd.to_numeric(data_df['bid_price'])
            data_df['ask_price'] = pd.to_numeric(data_df['ask_price'])
            data_df['buy_vol'] = pd.to_numeric(data_df['buy_vol'])
            data_df['sell_vol'] = pd.to_numeric(data_df['sell_vol'])
            data_df['hold'] = pd.to_numeric(data_df['hold'])
            data_df['volume'] = pd.to_numeric(data_df['volume'])
            data_df['avg_price'] = pd.to_numeric(data_df['avg_price'])
            data_df['last_close'] = pd.to_numeric(data_df['last_close'])
            data_df['last_settle_price'] = pd.to_numeric(data_df['last_settle_price'])

            data_df.dropna(subset=['current_price'], inplace=True)
            return data_df
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
                "_" "_",
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
                "symbol",
            ]
            data_df = data_df[
                [
                    "symbol",
                    "time",
                    "open",
                    "high",
                    "low",
                    "current_price",
                    "hold",
                    "volume",
                    "amount",
                ]
            ]
            data_df['open'] = pd.to_numeric(data_df['open'])
            data_df['high'] = pd.to_numeric(data_df['high'])
            data_df['low'] = pd.to_numeric(data_df['low'])
            data_df['current_price'] = pd.to_numeric(data_df['current_price'])
            data_df['hold'] = pd.to_numeric(data_df['hold'])
            data_df['volume'] = pd.to_numeric(data_df['volume'])
            data_df['amount'] = pd.to_numeric(data_df['amount'])

            data_df.dropna(subset=['current_price'], inplace=True)
            return data_df


def futures_zh_minute_sina(symbol: str = "IF2008", period: str = "5") -> pd.DataFrame:
    """
    中国各品种期货分钟频率数据
    http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_3
    :param symbol: 可以通过 match_main_contract(symbol="cffex") 获取, 或者访问网页获取
    :type symbol: str
    :param period: choice of {"1": "1分钟", "5": "5分钟", "15": "15分钟", "30": "30分钟", "60": "60分钟"}
    :type period: str
    :return: 指定 symbol 和 period 的数据
    :rtype: pandas.DataFrame
    """
    url = "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/=/InnerFuturesNewService.getFewMinLine"
    params = {
        "symbol": symbol,
        "type": period,
    }
    r = requests.get(url, params=params)
    temp_df = pd.DataFrame(json.loads(r.text.split("=(")[1].split(");")[0]))
    temp_df.columns = ["datetime", "open", "high", "low", "close", "volume", "hold"]
    temp_df['open'] = pd.to_numeric(temp_df['open'])
    temp_df['high'] = pd.to_numeric(temp_df['high'])
    temp_df['low'] = pd.to_numeric(temp_df['low'])
    temp_df['close'] = pd.to_numeric(temp_df['close'])
    temp_df['volume'] = pd.to_numeric(temp_df['volume'])
    temp_df['hold'] = pd.to_numeric(temp_df['hold'])
    return temp_df


def futures_zh_daily_sina(symbol: str = "V2105") -> pd.DataFrame:
    """
    中国各品种期货日频率数据
    https://finance.sina.com.cn/futures/quotes/V2105.shtml
    :param symbol: 可以通过 match_main_contract(symbol="cffex") 获取, 或者访问网页获取
    :type symbol: str
    :return: 指定 symbol 和 period 的数据
    :rtype: pandas.DataFrame
    """
    date = "20210412"
    url = "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_V21052021_4_12=/InnerFuturesNewService.getDailyKLine"
    params = {
        "symbol": symbol,
        "type": '_'.join([date[:4], date[4:6], date[6:]]),
    }
    r = requests.get(url, params=params)
    temp_df = pd.DataFrame(json.loads(r.text.split("=(")[1].split(");")[0]))
    temp_df.columns = ["date", "open", "high", "low", "close", "volume", "hold", "settle"]
    temp_df['open'] = pd.to_numeric(temp_df['open'])
    temp_df['high'] = pd.to_numeric(temp_df['high'])
    temp_df['low'] = pd.to_numeric(temp_df['low'])
    temp_df['close'] = pd.to_numeric(temp_df['close'])
    temp_df['volume'] = pd.to_numeric(temp_df['volume'])
    temp_df['hold'] = pd.to_numeric(temp_df['hold'])
    temp_df['settle'] = pd.to_numeric(temp_df['settle'])
    return temp_df


if __name__ == "__main__":
    futures_zh_minute_sina_df = futures_zh_minute_sina(symbol="V2201", period="5")
    print(futures_zh_minute_sina_df)

    futures_zh_daily_sina_df = futures_zh_daily_sina(symbol="IC2206")
    print(futures_zh_daily_sina_df)

    futures_zh_daily_sina_df = futures_zh_daily_sina(symbol="V2205")
    print(futures_zh_daily_sina_df)

    futures_zh_spot_df = futures_zh_spot(symbol='V2204', market="CF", adjust='0')
    print(futures_zh_spot_df)

    futures_zh_spot_df = futures_zh_spot(symbol='NR0', market="CF", adjust='0')
    print(futures_zh_spot_df)

    print("开始接收实时行情, 每秒刷新一次")
    dce_text = match_main_contract(symbol="dce")
    czce_text = match_main_contract(symbol="czce")
    shfe_text = match_main_contract(symbol="shfe")
    cffex_text = match_main_contract(symbol="cffex")

    while True:
        futures_zh_spot_df = futures_zh_spot(
            symbol=",".join([dce_text, czce_text, shfe_text]),
            market="CF",
            adjust='0',
        )
        print(futures_zh_spot_df)
        time.sleep(3)
