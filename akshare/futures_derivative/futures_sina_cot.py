# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/6/6 18:14
Desc: 新浪财经-商品期货-成交持仓
http://vip.stock.finance.sina.com.cn/q/view/vCffex_Positions_cjcc.php?symbol=IC2106&date=2021-06-03
"""
import requests
import pandas as pd


def futures_sina_hold_pos(
    symbol: str = "成交量", contract: str = "IC2106", date: str = "2021-06-03"
) -> pd.DataFrame:
    """
    新浪财经-商品期货-成交持仓
    http://vip.stock.finance.sina.com.cn/q/view/vCffex_Positions_cjcc.php?symbol=IC2106&date=2021-06-03
    :param symbol: choice of {"成交量", "多单持仓", "空单持仓"}
    :type symbol: str
    :param contract: 期货合约
    :type contract: str
    :param date: 查询日期
    :type date: str
    :return: 成交持仓
    :rtype: pandas.DataFrame
    """
    url = "http://vip.stock.finance.sina.com.cn/q/view/vCffex_Positions_cjcc.php"
    params = {"symbol": contract, "date": date}
    r = requests.get(url, params=params)
    if symbol == "成交量":
        return pd.read_html(r.text)[2]
    elif symbol == "多单持仓":
        return pd.read_html(r.text)[3]
    elif symbol == "空单持仓":
        return pd.read_html(r.text)[4]


if __name__ == "__main__":
    futures_sina_hold_pos_df = futures_sina_hold_pos(
        symbol="成交量", contract="IC2106", date="2021-06-03"
    )
    print(futures_sina_hold_pos_df)
