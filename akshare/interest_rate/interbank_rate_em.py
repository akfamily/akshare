# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/6/22 16:13
Desc: 东方财富网-经济数据-银行间拆借利率
http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99333&cu=sgd&type=009065&p=79
Attention: 大量获取容易封 IP, 建议 20 分钟后再尝试或者切换 WIFI 为手机热点, 也可以修改本函数只更新增量
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from akshare.interest_rate.cons import market_symbol_indicator_dict, headers


class IPError(Exception):
    """
    Define IPError
    """

    pass


def _get_page_num(
    market: str = "上海银行同业拆借市场", symbol: str = "Shibor人民币", indicator: str = "隔夜"
) -> int:
    """
    具体市场具体品种具体指标的页面数量
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
    res = requests.get(need_url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    try:
        page_num = (
            soup.find("div", attrs={"class": "Page"})
            .find_all("a", attrs={"target": "_self"})[-1]["href"]
            .split("=")[-1]
        )
    except AttributeError as e:
        raise IPError("IP 被封了, 建议 20 分钟后再尝试或者切换 WIFI 为手机热点")
    return int(page_num)


def rate_interbank(
    market: str = "上海银行同业拆借市场",
    symbol: str = "Shibor人民币",
    indicator: str = "隔夜",
    need_page="",
) -> pd.DataFrame:
    """
    具体市场具体品种具体指标的拆借利率数据
    具体 market 和 symbol 参见: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99333&cu=sgd&type=009065&p=79
    :param market: choice of {"上海银行同业拆借市场", "中国银行同业拆借市场", "伦敦银行同业拆借市场", "欧洲银行同业拆借市场", "香港银行同业拆借市场", "新加坡银行同业拆借市场"}
    :type market: str
    :param symbol: choice of {"Shibor人民币", ***}
    :type symbol: str
    :param indicator: str
    :type indicator: choice of {"隔夜", "1周", "2周", ***}
    :param need_page: 返回前 need_page 页的数据; e.g., need_page="5", 则只返回前5页的数据, 此参数可以用于增量更新, 以免被封 IP
    :type need_page: str
    :return: 具体市场具体品种具体指标的拆借利率数据
    :rtype: pandas.DataFrame
    """
    page_num = _get_page_num(market=market, symbol=symbol, indicator=indicator)
    temp_df = pd.DataFrame()
    if need_page == "":
        for page in tqdm(range(1, page_num + 1), leave=False):
            need_url = (
                market_symbol_indicator_dict[market][symbol][indicator] + f"&p={page}"
            )
            res = requests.get(need_url, headers=headers)
            table = pd.read_html(res.text)[0]
            temp_df = temp_df.append(table, ignore_index=True)
        temp_df.columns = [
            "日期",
            "利率",
            "涨跌",
        ]
        return temp_df
    else:
        for page in tqdm(range(1, int(need_page) + 1)):
            need_url = (
                market_symbol_indicator_dict[market][symbol][indicator] + f"&p={page}"
            )
            res = requests.get(need_url, headers=headers)
            table = pd.read_html(res.text)[0]
            temp_df = temp_df.append(table, ignore_index=True)
        temp_df.columns = [
            "日期",
            "利率",
            "涨跌",
        ]
        return temp_df


if __name__ == "__main__":
    rate_interbank_shanghai_df = rate_interbank(
        market="上海银行同业拆借市场", symbol="Shibor人民币", indicator="3月", need_page="5"
    )
    print(rate_interbank_shanghai_df)

    rate_interbank_df = rate_interbank(
        market="新加坡银行同业拆借市场", symbol="Sibor星元", indicator="1月", need_page="2"
    )
    print(rate_interbank_df)
