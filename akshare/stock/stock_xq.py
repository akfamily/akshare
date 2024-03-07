# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/3/7 22:30
Desc: 雪球-行情中心-个股
https://xueqiu.com/S/SH513520
"""
import re

import pandas as pd
import requests


def stock_individual_spot_xq(
        symbol: str = "SH600000",
        timeout: float = None,
) -> pd.DataFrame:
    """
    雪球-行情中心-个股
    https://xueqiu.com/S/SH600000
    :param symbol: 证券代码，可以是 A 股代码，A 股场内基金代码，A 股指数，美股代码, 美股指数
    :type symbol: str
    :param timeout: choice of None or a positive float number
    :type timeout: float
    :return: 证券最新行情
    :rtype: pandas.DataFrame
    """
    url = f"https://stock.xueqiu.com/v5/stock/quote.json?symbol={symbol}&extend=detail"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "80.0.3987.149 Safari/537.36",
        "Cookie": "xqat=52dfb79aed5f2cdd1e7c2cfc56054ac1f5b77fc3",
    }
    r = requests.get(url, headers=headers, timeout=timeout)
    column_name_map = {
        "acc_unit_nav": "累计净值",
        "amount": "成交额",
        "amplitude": "振幅",
        "avg_price": "均价",
        "chg": "涨跌",
        "currency": "货币",
        "current": "现价",
        "current_year_percent": "今年以来涨幅",
        "dividend": "股息(TTM)",
        "dividend_yield": "股息率(TTM)",
        "eps": "每股收益",
        "exchange": "交易所",
        "float_market_capital": "流通值",
        "float_shares": "流通股",
        "found_date": "成立日期",
        "goodwill_in_net_assets": "净资产中的商誉",
        "high": "最高",
        "high52w": "52周最高",
        "iopv": "参考净值",
        "issue_date": "发行日期",
        "last_close": "昨收",
        "limit_down": "跌停",
        "limit_up": "涨停",
        "lot_size": "最小交易单位",
        "low": "最低",
        "low52w": "52周最低",
        "market_capital": "资产净值/总市值",
        "name": "名称",
        "nav_date": "净值日期",
        "navps": "每股净资产",
        "open": "今开",
        "pb": "市净率",
        "pe_forecast": "市盈率(动)",
        "pe_lyr": "市盈率(静)",
        "pe_ttm": "市盈率(TTM)",
        "percent": "涨幅",
        "premium_rate": "溢价率",
        "psr": "市销率",
        "symbol": "代码",
        "total_shares": "基金份额/总股本",
        "turnover_rate": "周转率",
        "unit_nav": "单位净值",
        "volume": "成交量",
    }
    json_data = r.json()["data"]["quote"]
    temp_df = pd.json_normalize(json_data)
    temp_df.columns = [
        *map(
            lambda x: column_name_map[x] if x in column_name_map.keys() else x,
            temp_df.columns,
        )  # 由于传入的symbol可能是个股，可能是指数，也可能是基金，所以这里取列的最大公约数，没有数据的列内容为None
    ]
    temp_df = temp_df[
        list(
            filter(
                lambda x: re.search(r"[\u4e00-\u9fa5]", x), temp_df.columns
            )  # 过滤temp_df，留下包含汉字的列
        )
    ]
    temp_df = temp_df.T.reset_index()
    temp_df.columns = ["item", "value"]
    return temp_df


if __name__ == "__main__":
    stock_individual_spot_xq_df = stock_individual_spot_xq(symbol="SH600000")
    print(stock_individual_spot_xq_df)

    stock_individual_spot_xq_df = stock_individual_spot_xq(symbol="SH000001")
    print(stock_individual_spot_xq_df)

    stock_individual_spot_xq_df = stock_individual_spot_xq(symbol="SPY")
    print(stock_individual_spot_xq_df)

    stock_individual_spot_xq_df = stock_individual_spot_xq(symbol=".INX")
    print(stock_individual_spot_xq_df)
