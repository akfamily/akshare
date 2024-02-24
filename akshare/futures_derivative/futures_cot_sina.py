#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/2/24 15:30
Desc: 新浪财经-商品期货-成交持仓
https://vip.stock.finance.sina.com.cn/q/view/vFutures_Positions_cjcc.php
"""
from io import StringIO

import pandas as pd
import requests


def futures_hold_pos_sina(
        symbol: str = "成交量", contract: str = "IC2403", date: str = "20240223"
) -> pd.DataFrame:
    """
    新浪财经-商品期货-成交持仓
    https://vip.stock.finance.sina.com.cn/q/view/vFutures_Positions_cjcc.php
    :param symbol: choice of {"成交量", "多单持仓", "空单持仓"}
    :type symbol: str
    :param contract: 期货合约
    :type contract: str
    :param date: 查询日期
    :type date: str
    :return: 成交持仓
    :rtype: pandas.DataFrame
    """
    date = '-'.join([date[:4], date[4:6], date[6:]])
    url = "https://vip.stock.finance.sina.com.cn/q/view/vCffex_Positions_cjcc.php"
    params = {"symbol": contract, "date": date}
    r = requests.get(url, params=params)
    if symbol == "成交量":
        return pd.read_html(StringIO(r.text))[2]
    elif symbol == "多单持仓":
        return pd.read_html(StringIO(r.text))[3]
    elif symbol == "空单持仓":
        return pd.read_html(StringIO(r.text))[4]


if __name__ == "__main__":
    futures_hold_pos_sina_df = futures_hold_pos_sina(
        symbol="成交量", contract="IC2403", date="20240223"
    )
    print(futures_hold_pos_sina_df)
