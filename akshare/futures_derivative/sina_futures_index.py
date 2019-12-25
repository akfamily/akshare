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


def futures_main_sina(symbol="TA0"):
    """
    获取新浪财经-期货-主力连续日数据
    :return:
    """
    url = f"https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_{symbol}2019_12_25=/InnerFuturesNewService.getDailyKLine?symbol={symbol}&_=2019_12_25"
    resp = requests.get(url)
    data_json = resp.text[resp.text.find("([")+1:resp.text.rfind("])")+1]
    data_df = pd.read_json(data_json)
    data_df.columns = ["日期", "开盘价", "最高价", "最低价", "收盘价", "成交量", "持仓量"]
    return data_df


if __name__ == '__main__':
    futures_hist = futures_main_sina(symbol="TA0")
    print(futures_hist)
