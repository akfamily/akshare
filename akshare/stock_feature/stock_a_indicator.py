# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/13 22:32
Desc: 市盈率, 市净率和股息率查询
https://www.legulegu.com/stocklist
https://www.legulegu.com/s/000001
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup


def stock_a_lg_indicator(stock: str = "688388") -> pd.DataFrame:
    """
    市盈率, 市净率, 股息率数据接口
    :param stock: 通过 stock_a_indicator(stock="all") 来获取所有股票的代码
    :type stock: str
    :return: 市盈率, 市净率, 股息率查询
    :rtype: pandas.DataFrame
    """
    if stock == "all":
        url = "https://www.legulegu.com/stocklist"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        node_list = soup.find_all(attrs={"class": "col-xs-6"})
        href_list = [item.find("a")["href"] for item in node_list]
        title_list = [item.find("a")["title"] for item in node_list]
        temp_df = pd.DataFrame([title_list, href_list]).T
        temp_df.columns = ["stock_name", "short_url"]
        temp_df["code"] = temp_df["short_url"].str.split("/", expand=True).iloc[:, -1]
        del temp_df["short_url"]
        temp_df = temp_df[["code", "stock_name"]]
        return temp_df
    else:
        url = f"https://www.legulegu.com/s/base-info/{stock}"
        r = requests.get(url)
        temp_json = r.json()
        temp_df = pd.DataFrame(temp_json["data"]["items"], columns=temp_json["data"]["fields"])
        temp_df["trade_date"] = pd.to_datetime(temp_df["trade_date"])
        temp_df.iloc[:, 1:] = temp_df.iloc[:, 1:].astype(float)
        return temp_df


if __name__ == '__main__':
    stock_a_lg_indicator_all_df = stock_a_lg_indicator(stock="all")
    print(stock_a_lg_indicator_all_df)
    stock_a_lg_indicator_df = stock_a_lg_indicator(stock="000001")
    print(stock_a_lg_indicator_df)
