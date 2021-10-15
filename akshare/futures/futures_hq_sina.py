# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/7/21 14:34
Desc: 新浪财经-外盘期货-实时数据获取
http://finance.sina.com.cn/money/future/hf.html
"""
import time

from akshare.utils import demjson
import pandas as pd
import requests
from bs4 import BeautifulSoup


def _get_real_name_list() -> list:
    """
    新浪-外盘期货所有品种的中文名称
    :return: 外盘期货所有品种的中文名称
    :rtype: list
    """
    url = "http://finance.sina.com.cn/money/future/hf.html"
    r = requests.get(url)
    r.encoding = "gb2312"
    data_text = r.text
    need_text = data_text[
        data_text.find("var oHF_1 = ") + 12: data_text.find("var oHF_2") - 2
    ].replace("\n\t", "")
    data_json = demjson.decode(need_text)
    name_list = [item[0].strip() for item in data_json.values()]
    return name_list


def futures_foreign_commodity_subscribe_exchange_symbol() -> list:
    """
    需要订阅的行情的代码
    :return: 需要订阅的行情的代码
    :rtype: list
    """
    url = "http://finance.sina.com.cn/money/future/hf.html"
    r = requests.get(url)
    r.encoding = "gb2312"
    data_text = r.text
    data_json = demjson.decode(
        data_text[data_text.find("var oHF_1 = ") + 12: data_text.find("var oHF_2 = ") - 2]
    )
    code_list = list(data_json.keys())
    return code_list


def futures_foreign_commodity_realtime(subscribe_list: list) -> pd.DataFrame:
    """
    新浪-外盘期货-行情数据
    https://finance.sina.com.cn/money/future/hf.html
    :param subscribe_list: 通过调用 hq_subscribe_exchange_symbol 函数来获取
    :type subscribe_list: list
    :return: 行情数据
    :rtype: pandas.DataFrame
    """
    payload = "&list=" + ",".join(["hf_" + item for item in subscribe_list])
    prefix = f"rn={round(time.time() * 1000)}"
    url = "http://hq.sinajs.cn/" + prefix + payload
    r = requests.get(url)
    data_text = r.text
    data_df = pd.DataFrame(
        [
            item.strip().split("=")[1].split(",")
            for item in data_text.split(";")
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
        "马棕油",
    ]
    data_df = data_df[
        [
            "symbol",
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
        ]
    ]
    data_df.columns = [
        "名称",
        "最新价",
        "人民币报价",
        "买价",
        "卖价",
        "最高价",
        "最低价",
        "行情时间",
        "昨日结算价",
        "开盘价",
        "持仓量",
        "日期",
    ]
    data_df.dropna(how='all', inplace=True)
    data_df['最新价'] = pd.to_numeric(data_df['最新价'])
    data_df['人民币报价'] = pd.to_numeric(data_df['人民币报价'])
    data_df['买价'] = pd.to_numeric(data_df['买价'])
    data_df['卖价'] = pd.to_numeric(data_df['卖价'])
    data_df['最高价'] = pd.to_numeric(data_df['最高价'])
    data_df['最低价'] = pd.to_numeric(data_df['最低价'])
    data_df['昨日结算价'] = pd.to_numeric(data_df['昨日结算价'])
    data_df['开盘价'] = pd.to_numeric(data_df['开盘价'])
    data_df['持仓量'] = pd.to_numeric(data_df['持仓量'])
    data_df['涨跌额'] = data_df['最新价'] - data_df['昨日结算价']
    data_df['涨跌幅'] = (data_df['最新价'] - data_df['昨日结算价']) / data_df['昨日结算价'] * 100
    data_df = data_df[[
        "名称",
        "最新价",
        "人民币报价",
        "涨跌额",
        "涨跌幅",
        "开盘价",
        "最高价",
        "最低价",
        "昨日结算价",
        "持仓量",
        "买价",
        "卖价",
        "行情时间",
        "日期",
    ]]

    # 获取转换比例数据
    url = 'https://finance.sina.com.cn/money/future/hf.html'
    r = requests.get(url)
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, "lxml")
    data_text = soup.find_all("script", attrs={'type': 'text/javascript'})[-2].string.strip()
    raw_text = data_text[data_text.find("oHF_1 = "):data_text.find("oHF_2")]
    need_text = raw_text[raw_text.find("{"): raw_text.rfind("}")+1]
    data_json = demjson.decode(need_text)
    price_mul = pd.DataFrame([[item[0] for item in data_json.values()], [item[1][0] for item in data_json.values()]]).T
    price_mul.columns = ['symbol', 'price']

    # 获取汇率数据
    url = 'https://hq.sinajs.cn/?list=USDCNY'
    r = requests.get(url)
    data_text = r.text
    usd_rmb = float(data_text[data_text.find('"')+1:data_text.find(",美元人民币")].split(",")[-1])

    # 计算人民币报价
    data_df['人民币报价'] = data_df['最新价'] * price_mul['price'] * usd_rmb

    data_df.dropna(thresh=4, inplace=True)
    return data_df


if __name__ == "__main__":
    print("开始接收实时行情, 每秒刷新一次")
    subscribes = futures_foreign_commodity_subscribe_exchange_symbol()

    futures_foreign_commodity_realtime_df = futures_foreign_commodity_realtime(subscribe_list=subscribes)
    print(futures_foreign_commodity_realtime_df)

    while True:
        futures_foreign_commodity_realtime_df = futures_foreign_commodity_realtime(subscribe_list=subscribes)
        print(futures_foreign_commodity_realtime_df)
        time.sleep(3)
