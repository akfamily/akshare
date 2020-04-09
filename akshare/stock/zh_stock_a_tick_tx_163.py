# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/11/16 20:39
contact: jindaxiang@163.com
desc: 腾讯-股票-实时行情-成交明细
下载成交明细-每个交易日16:00提供当日数据
该列表港股报价延时15分钟
"""
from io import StringIO, BytesIO

import pandas as pd
import requests


def stock_zh_a_tick_tx(code: str = "sh600848", trade_date: str = "20191011") -> pd.DataFrame:
    """
    http://gu.qq.com/sz000001/gp/detail
    成交明细-每个交易日16:00提供当日数据
    :param code: 带市场标识的股票代码
    :type code: str
    :param trade_date: 需要提取数据的日期
    :type trade_date: str
    :return: 返回当日股票成交明细的数据
    :rtype: pandas.DataFrame
    """
    url = "http://stock.gtimg.cn/data/index.php"
    params = {
        "appn": "detail",
        "action": "download",
        "c": code,
        "d": trade_date,
    }
    res = requests.get(url, params=params)
    res.encoding = "gbk"
    temp_df = pd.read_table(StringIO(res.text))
    return temp_df


def stock_zh_a_tick_163(code: str = "sh600848", trade_date: str = "20200408") -> pd.DataFrame:
    """
    成交明细-每个交易日16:00提供当日数据
    http://quotes.money.163.com/trade/cjmx_000001.html#01b05
    :param code: 带市场标识的股票代码
    :type code: str
    :param trade_date: 需要提取数据的日期
    :type trade_date: str
    :return: 返回当日股票成交明细的数据
    :rtype: pandas.DataFrame
    """
    name_code_map = {"sh": "0", "sz": 1}
    url = f"http://quotes.money.163.com/cjmx/{trade_date[:4]}/{trade_date}/{name_code_map[code[:2]]}{code[2:]}.xls"
    res = requests.get(url)
    res.encoding = "utf-8"
    temp_df = pd.read_excel(BytesIO(res.content))
    return temp_df


if __name__ == "__main__":
    date_list = pd.date_range(start="20190801", end="20191111").tolist()
    date_list = pd.date_range(start="20200401", end="20200408").tolist()
    date_list = [item.strftime("%Y%m%d") for item in date_list]
    for item in date_list:
        print(item)
        data = stock_zh_a_tick_tx(code="sz000001", trade_date=f"{item}")
        if not data.empty:
            print(data)
    stock_zh_a_tick_163_df = stock_zh_a_tick_163(code="sh600848", trade_date="20200408")
    print(stock_zh_a_tick_163_df)
