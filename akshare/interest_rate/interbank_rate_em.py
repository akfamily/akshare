# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/1/10 17:13
contact: jindaxiang@163.com
desc: 东方财富网-经济数据-银行间拆借利率
http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99333&cu=sgd&type=009065&p=79
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.interest_rate.cons import market_symbol_indicator_dict


def _get_page_num(market="上海银行同业拆借市场", symbol="Shibor人民币", indicator="隔夜"):
    """
    获取具体市场具体品种具体指标的页面数量
    http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99333&cu=sgd&type=009065&p=79
    :param market: ["上海银行同业拆借市场", "中国银行同业拆借市场", "伦敦银行同业拆借市场", "欧洲银行同业拆借市场", "香港银行同业拆借市场", "新加坡银行同业拆借市场"]
    :type market: str
    :param symbol: ["Shibor人民币", ***]
    :type symbol: str
    :param indicator: str
    :type indicator: ["隔夜", "1周", "2周", ***]
    :return: 具体市场具体品种具体指标的页面数量
    :rtype: int
    """
    need_url = market_symbol_indicator_dict[market][symbol][indicator] + "&p=1"
    res = requests.get(need_url)
    soup = BeautifulSoup(res.text, "lxml")
    page_num = (
        soup.find("div", attrs={"class": "Page"})
        .find_all("a", attrs={"target": "_self"})[-1]["href"]
        .split("=")[-1]
    )
    return int(page_num)


def rate_interbank(market="上海银行同业拆借市场", symbol="Shibor人民币", indicator="隔夜"):
    """
    具体市场具体品种具体指标的拆借利率数据
    具体 market 和 symbol 参见: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99333&cu=sgd&type=009065&p=79
    :param market: ["上海银行同业拆借市场", "中国银行同业拆借市场", "伦敦银行同业拆借市场", "欧洲银行同业拆借市场", "香港银行同业拆借市场", "新加坡银行同业拆借市场"]
    :type market: str
    :param symbol: ["Shibor人民币", ***]
    :type symbol: str
    :param indicator: str
    :type indicator: ["隔夜", "1周", "2周", ***]
    :return: 具体市场具体品种具体指标的拆借利率数据
    :rtype: pandas.DataFrame
    """
    page_num = _get_page_num(market=market, symbol=symbol, indicator=indicator)
    temp_df = pd.DataFrame()
    for page in range(1, page_num + 1):
        need_url = (
            market_symbol_indicator_dict[market][symbol][indicator] + f"&p={page}"
        )
        res = requests.get(need_url)
        table = pd.read_html(res.text)[0]
        temp_df = temp_df.append(table, ignore_index=True)
    return temp_df


if __name__ == "__main__":
    rate_interbank_df = rate_interbank(
        market="中国银行同业拆借市场", symbol="Chibor人民币", indicator="3月"
    )
    print(rate_interbank_df)
    rate_interbank_df = rate_interbank(
        market="新加坡银行同业拆借市场", symbol="Sibor星元", indicator="1月"
    )
    print(rate_interbank_df)
