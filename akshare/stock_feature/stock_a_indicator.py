#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/4/3 20:50
Desc: 市盈率, 市净率和股息率查询
https://www.legulegu.com/stocklist
https://www.legulegu.com/s/000001
"""
from datetime import datetime
from hashlib import md5
from typing import Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_token_lg() -> str:
    """
    生成乐咕的 token
    https://legulegu.com/s/002488
    :return: token
    :rtype: str
    """
    current_date_str = datetime.now().date().isoformat()
    obj = md5()
    obj.update(current_date_str.encode("utf-8"))
    token = obj.hexdigest()
    return token


def stock_a_lg_indicator(symbol: str = "002174") -> pd.DataFrame:
    """
    市盈率, 市净率, 股息率数据接口
    https://legulegu.com/stocklist
    :param symbol: 通过 ak.stock_a_lg_indicator(symbol="all") 来获取所有股票的代码
    :type symbol: str
    :return: 市盈率, 市净率, 股息率查询
    :rtype: pandas.DataFrame
    """
    if symbol == "all":
        url = "https://legulegu.com/stocklist"
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
        from requests import Session
        session = Session()
        r = session.get(f"https://legulegu.com/s/{symbol}")
        soup = BeautifulSoup(r.text, "lxml")
        csrf_tag = soup.find("meta", attrs={"name": "_csrf"})
        csrf_token = csrf_tag.attrs["content"]
        session_id = r.cookies["JSESSIONID"]
        rdtkolg = r.cookies["rdtkolg"]
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "Content-Type": "application/json",
            "Host": "legulegu.com",
            "Origin": "https://legulegu.com",
            "Pragma": "no-cache",
            "Referer": "https://legulegu.com/s/002174",
            "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        headers.update({"Cookie": f"JSESSIONID={session_id}; rdtkolg={rdtkolg}", "X-CSRF-Token": csrf_token})
        url = "https://legulegu.com/api/s/base-info/"
        token = get_token_lg()
        params = {"token": token, "id": symbol}
        r = session.post(url, params=params, headers=headers)
        temp_json = r.json()
        temp_df = pd.DataFrame(
            temp_json["data"]["items"],
            columns=temp_json["data"]["fields"],
        )
        temp_df["trade_date"] = pd.to_datetime(temp_df["trade_date"]).dt.date
        temp_df[temp_df.columns[1:]] = temp_df[temp_df.columns[1:]].astype(float)
        temp_df.sort_values(["trade_date"], inplace=True, ignore_index=True)
        return temp_df


def stock_hk_eniu_indicator(
    symbol: str = "hk01093", indicator: str = "市盈率"
) -> pd.DataFrame:
    """
    亿牛网-港股指标
    https://eniu.com/gu/hk01093/roe
    :param symbol: 港股代码
    :type symbol: str
    :param indicator: 需要获取的指标, choice of {"港股", "市盈率", "市净率", "股息率", "ROE", "市值"}
    :type indicator: str
    :return: 指定 symbol 和 indicator 的数据
    :rtype: pandas.DataFrame
    """
    if indicator == "港股":
        url = "https://eniu.com/static/data/stock_list.json"
        r = requests.get(url)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        return temp_df[temp_df["stock_id"].str.contains("hk")]
    if indicator == "市盈率":
        url = f"https://eniu.com/chart/peh/{symbol}"
    elif indicator == "市净率":
        url = f"https://eniu.com/chart/pbh/{symbol}"
    elif indicator == "股息率":
        url = f"https://eniu.com/chart/dvh/{symbol}"
    elif indicator == "ROE":
        url = f"https://eniu.com/chart/roeh/{symbol}"
    elif indicator == "市值":
        url = f"https://eniu.com/chart/marketvalueh/{symbol}"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    return temp_df


if __name__ == "__main__":
    stock_a_lg_indicator_all_df = stock_a_lg_indicator(symbol="all")
    print(stock_a_lg_indicator_all_df)

    stock_a_lg_indicator_df = stock_a_lg_indicator(symbol="600030")
    print(stock_a_lg_indicator_df)

    stock_hk_eniu_indicator_df = stock_hk_eniu_indicator(
        symbol="hk01093", indicator="市净率"
    )
    print(stock_hk_eniu_indicator_df)
