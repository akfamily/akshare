#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/3/21 17:40
Desc: 天天基金网-基金档案-投资组合
http://fundf10.eastmoney.com/ccmx_000001.html
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.utils import demjson


def fund_portfolio_hold_em(symbol: str = "162411", date: str = "2020") -> pd.DataFrame:
    """
    天天基金网-基金档案-投资组合-基金持仓
    http://fundf10.eastmoney.com/ccmx_000001.html
    :param symbol: 基金代码
    :type symbol: str
    :param date: 查询年份
    :type date: str
    :return: 基金持仓
    :rtype: pandas.DataFrame
    """
    url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx"
    params = {
        "type": "jjcc",
        "code": symbol,
        "topline": "200",
        "year": date,
        "month": "",
        "rt": "0.913877030254846",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    soup = BeautifulSoup(data_json["content"], "lxml")
    item_label = [
        item.text.split("\xa0\xa0")[1]
        for item in soup.find_all("h4", attrs={"class": "t"})
    ]
    big_df = pd.DataFrame()
    for item in range(len(item_label)):
        temp_df = pd.read_html(data_json["content"], converters={"股票代码": str})[item]
        del temp_df["相关资讯"]
        temp_df["占净值比例"] = temp_df["占净值比例"].str.split("%", expand=True).iloc[:, 0]
        temp_df.rename(columns={"持股数（万股）": "持股数", "持仓市值（万元）": "持仓市值"}, inplace=True)
        temp_df.rename(columns={"持股数（万股）": "持股数", "持仓市值（万元人民币）": "持仓市值"}, inplace=True)
        temp_df["季度"] = item_label[item]
        temp_df = temp_df[
            [
                "序号",
                "股票代码",
                "股票名称",
                "占净值比例",
                "持股数",
                "持仓市值",
                "季度",
            ]
        ]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df["占净值比例"] = pd.to_numeric(big_df["占净值比例"], errors="coerce")
    big_df["持股数"] = pd.to_numeric(big_df["持股数"], errors="coerce")
    big_df["持仓市值"] = pd.to_numeric(big_df["持仓市值"], errors="coerce")
    big_df["序号"] = range(1, len(big_df) + 1)
    return big_df


def fund_portfolio_change_em(
    symbol: str = "003567", indicator: str = "累计买入", date: str = "2020"
) -> pd.DataFrame:
    """
    天天基金网-基金档案-投资组合-重大变动
    http://fundf10.eastmoney.com/ccbd_000001.html
    :param symbol: 基金代码
    :type symbol: str
    :param indicator: choice of {"累计买入", "累计卖出"}
    :type indicator: str
    :param date: 查询年份
    :type date: str
    :return: 重大变动
    :rtype: pandas.DataFrame
    """
    indicator_map = {
        "累计买入": "1",
        "累计卖出": "2",
    }
    url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx"
    params = {
        "type": "zdbd",
        "code": symbol,
        "zdbd": indicator_map[indicator],
        "year": date,
        "rt": "0.913877030254846",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    soup = BeautifulSoup(data_json["content"], "lxml")
    item_label = [
        item.text.split("\xa0\xa0")[1]
        for item in soup.find_all("h4", attrs={"class": "t"})
    ]
    big_df = pd.DataFrame()
    for item in range(len(item_label)):
        temp_df = pd.read_html(data_json["content"], converters={"股票代码": str})[item]
        del temp_df["相关资讯"]
        temp_df["占期初基金资产净值比例（%）"] = (
            temp_df["占期初基金资产净值比例（%）"].str.split("%", expand=True).iloc[:, 0]
        )
        temp_df["季度"] = item_label[item]
        temp_df.columns = [
            "序号",
            "股票代码",
            "股票名称",
            "本期累计买入金额",
            "占期初基金资产净值比例",
            "季度",
        ]
        temp_df = temp_df[
            [
                "序号",
                "股票代码",
                "股票名称",
                "本期累计买入金额",
                "占期初基金资产净值比例",
                "季度",
            ]
        ]
        big_df = big_df.append(temp_df, ignore_index=True)
    del big_df["序号"]
    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.rename(columns={"index": "序号"}, inplace=True)

    big_df["本期累计买入金额"] = pd.to_numeric(big_df["本期累计买入金额"], errors="coerce")
    big_df["占期初基金资产净值比例"] = pd.to_numeric(big_df["占期初基金资产净值比例"], errors="coerce")
    return big_df


if __name__ == "__main__":
    fund_portfolio_hold_em_df = fund_portfolio_hold_em(symbol="162411", date="2020")
    print(fund_portfolio_hold_em_df)

    fund_portfolio_change_em_df = fund_portfolio_change_em(
        symbol="003567", indicator="累计买入", date="2020"
    )
    print(fund_portfolio_change_em_df)

    fund_portfolio_change_em_df = fund_portfolio_change_em(
        symbol="003567", indicator="累计卖出", date="2020"
    )
    print(fund_portfolio_change_em_df)
