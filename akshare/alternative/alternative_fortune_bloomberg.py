#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/4/10 18:24
Desc: 彭博亿万富豪指数
https://www.bloomberg.com/billionaires/
"""

import pandas as pd
from bs4 import BeautifulSoup

from akshare.utils import http


def alternative_billionaires_hist_bloomberg(year: str = "2021") -> pd.DataFrame:
    """
    Bloomberg Billionaires Index
    https://stats.areppim.com/stats/links_billionairexlists.htm
    :param year: choice of {"2021", "2019", "2018", ...}
    :type year: str
    :return: 彭博亿万富豪指数历史数据
    :rtype: pandas.DataFrame
    """
    url = f"https://stats.areppim.com/listes/list_billionairesx{year[-2:]}xwor.htm"
    # areppim 对不带浏览器 User-Agent 的请求返回“Access denied by security policy”
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    r = http.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    trs = soup.findAll("table")[0].findAll("tr")
    heads = trs[1]
    if "Rank" not in heads.text:
        heads = trs[0]
    dic_keys = []
    dic = {}
    for head in heads:
        head = head.text
        dic_keys.append(head)
    for dic_key in dic_keys:
        dic[dic_key] = []

    for ll in trs:
        item = ll.findAll("td")
        for i in range(len(item)):
            v = item[i].text
            if i == 0 and not v.isdigit():
                break
            dic[dic_keys[i]].append(v)

    temp_df = pd.DataFrame(dic)
    temp_df = temp_df.rename(
        {
            "Rank": "rank",
            "Name": "name",
            "Age": "age",
            "Citizenship": "country",
            "Country": "country",
            "Net Worth(bil US$)": "total_net_worth",
            "Total net worth$Billion": "total_net_worth",
            "$ Last change": "last_change",
            "$ YTD change": "ytd_change",
            "Industry": "industry",
        },
        axis=1,
    )
    return temp_df


if __name__ == "__main__":
    alternative_billionaires_hist_bloomberg_df = (
        alternative_billionaires_hist_bloomberg(year="2021")
    )
    print(alternative_billionaires_hist_bloomberg_df)
