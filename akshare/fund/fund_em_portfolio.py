# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/2/2 17:54
Desc: 天天基金网-基金档案-投资组合-基金持仓
http://fundf10.eastmoney.com/ccmx_000001.html
"""
import demjson
import pandas as pd
import requests
from bs4 import BeautifulSoup


def fund_em_portfolio_hold(code: str = "162411", year: str = "2020") -> pd.DataFrame:
    """
    天天基金网-基金档案-投资组合-基金持仓
    http://fundf10.eastmoney.com/ccmx_000001.html
    :param code: 基金代码
    :type code: str
    :param year: 查询年份
    :type year: str
    :return: 基金持仓
    :rtype: pandas.DataFrame
    """
    url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx"
    params = {
        "type": "jjcc",
        "code": code,
        "topline": "200",
        "year": year,
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
        temp_df = pd.read_html(data_json["content"])[item]
        temp_df["股票代码"] = temp_df["股票代码"].astype(str).str.zfill(6)
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
    return big_df


if __name__ == "__main__":
    fund_em_portfolio_hold_df = fund_em_portfolio_hold(code="000001", year="2020")
    print(fund_em_portfolio_hold_df)
