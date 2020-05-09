# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/5/9 22:34
Desc: 新浪财经-外盘期货-实时数据获取
"""
import time

import demjson
import pandas as pd
import requests

from akshare.futures.cons import (
    hf_subscribe_exchange_symbol_url,
    hf_subscribe_url,
    hf_subscribe_headers,
    # hf_sina_spot_headers,
)


def _get_real_name_list():
    """
    获取前端显示的名称列表
    ['NYBOT-棉花', 'LME镍3个月', 'LME铅3个月', 'LME锡3个月', 'LME锌3个月', 'LME铝3个月', 'LME铜3个月', 'CBOT-黄豆', 'CBOT-小麦', 'CBOT-玉米', 'CBOT-黄豆油', 'CBOT-黄豆粉', '日本橡胶', 'COMEX铜', 'NYMEX天然气', 'NYMEX原油', 'COMEX白银', 'COMEX黄金', 'CME-瘦肉猪', '布伦特原油', '伦敦金', '伦敦银', '伦敦铂金', '伦敦钯金']
    """
    url = "http://finance.sina.com.cn/money/future/hf.html"
    res = requests.get(url)
    res.encoding = "gb2312"
    dem_text = res.text[
        res.text.find("var oHF_1 = ") + 12 : res.text.find("var oHF_2") - 2
    ].replace("\n\t", "")
    json_data = demjson.decode(dem_text)
    name_list = [item[0].strip() for item in json_data.values()]
    return name_list


def hf_subscribe_exchange_symbol():
    """
    获取具体的量价数据
    """
    # res = requests.get(hf_subscribe_exchange_symbol_url, headers=hf_sina_spot_headers)
    res = requests.get(hf_subscribe_exchange_symbol_url)
    res.encoding = "gb2312"
    data_json = demjson.decode(
        res.text[res.text.find("var oHF_1 = ") + 12: res.text.find("var oHF_2 = ") - 2]
    )
    return list(data_json.keys())


def futures_hf_spot(subscribe_list=['CT', 'NID', 'PBD', 'SND', 'ZSD', 'AHD', 'CAD', 'S', 'W', 'C', 'BO', 'SM', 'TRB', 'HG', 'NG', 'CL', 'SI', 'GC', 'LHC', 'OIL', 'XAU', 'XAG', 'XPT', 'XPD']):
    """
    订阅数据处理
    """
    payload = "&list=" + ",".join(["hf_" + item for item in subscribe_list])
    prefix = f"rn={round(time.time() * 1000)}"
    res = requests.get(
        hf_subscribe_url + prefix + payload, headers=hf_subscribe_headers
    )
    data_df = pd.DataFrame(
        [
            item.strip().split("=")[1].split(",")
            for item in res.text.split(";")
            if item.strip() != ""
        ]
    )
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
        "symbol",
        "current_price_rmb",
    ]
    data_df["symbol"] = [
        "NYBOT-棉花",
        "LME镍3个月",
        "LME铅3个月",
        "LME锡3个月",
        "LME锌3个月",
        "LME铝3个月",
        "LME铜3个月",
        "CBOT-黄豆",
        "CBOT-小麦",
        "CBOT-玉米",
        "CBOT-黄豆油",
        "CBOT-黄豆粉",
        "日本橡胶",
        "COMEX铜",
        "NYMEX天然气",
        "NYMEX原油",
        "COMEX白银",
        "COMEX黄金",
        "CME-瘦肉猪",
        "布伦特原油",
        "伦敦金",
        "伦敦银",
        "伦敦铂金",
        "伦敦钯金",
    ]
    return data_df[
        [
            "current_price",
            "current_price_rmb",
            "bid",
            "ask",
            "high",
            "low",
            "time",
            "last_settle_price",
            "open",
            "hold",
            "date",
            "symbol",
        ]
    ]


if __name__ == "__main__":
    print("开始接收实时行情, 每秒刷新一次")
    subscribes = hf_subscribe_exchange_symbol()
    while True:
        data = futures_hf_spot(subscribe_list=subscribes)
        print(data)
        time.sleep(3)
