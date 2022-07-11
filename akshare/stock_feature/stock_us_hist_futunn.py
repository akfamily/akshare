#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/3/21 15:26
Desc: 富途牛牛-行情-美股-每日行情
https://www.futunn.com/stock/HON-US?seo_redirect=1&channel=1244&subchannel=2&from=BaiduAladdin&utm_source=alading_user&utm_medium=website_growth
"""
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def stock_us_code_table_fu() -> pd.DataFrame:
    """
    富途牛牛-行情-美股-美股代码表
    https://www.futunn.com/stock/HON-US
    :return: 美股代码表
    :rtype: pandas.DataFrame
    """
    url = "https://www.futunn.com/quote/list/us/1/694"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "futu-x-csrf-token": "FM5ZhxYFQsZM4k9rXk3TMA==-O4oTw/tuNRp5DlJNWo/TNEEfMt8=",
        "pragma": "no-cache",
        "referer": "https://www.futunn.com/stock/HON-US?seo_redirect=1&channel=1244&subchannel=2&from=BaiduAladdin&utm_source=alading_user&utm_medium=website_growth",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    data_text = r.text
    data_json = json.loads(
        data_text[data_text.find('{"prefetch') : data_text.find(",window._params")]
    )
    pd.DataFrame(data_json["prefetch"]["stockList"]["list"])
    total_page = data_json["prefetch"]["stockList"]["page"]["page_count"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        url = f"https://www.futunn.com/quote/list/us/1/{page}"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "futu-x-csrf-token": "FM5ZhxYFQsZM4k9rXk3TMA==-O4oTw/tuNRp5DlJNWo/TNEEfMt8=",
            "pragma": "no-cache",
            "referer": "https://www.futunn.com/stock/HON-US?seo_redirect=1&channel=1244&subchannel=2&from=BaiduAladdin&utm_source=alading_user&utm_medium=website_growth",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        }
        r = requests.get(url, headers=headers)
        data_text = r.text
        data_json = json.loads(
            data_text[data_text.find('{"prefetch') : data_text.find(",window._params")]
        )
        temp_df = pd.DataFrame(data_json["prefetch"]["stockList"]["list"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.columns = [
        "代码",
        "最新价",
        "成交额",
        "成交量",
        "换手率",
        "振幅",
        "涨跌额",
        "涨跌幅",
        "-",
        "股票名称",
        "股票简称",
        "-",
    ]
    big_df = big_df[
        [
            "代码",
            "股票名称",
            "股票简称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "成交量",
            "成交额",
            "换手率",
            "振幅",
        ]
    ]
    big_df["最新价"] = pd.to_numeric(big_df["最新价"])
    big_df["涨跌额"] = pd.to_numeric(big_df["涨跌额"])
    big_df["涨跌幅"] = big_df["涨跌幅"].str.strip("%")
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["换手率"] = big_df["换手率"].str.strip("%")
    big_df["换手率"] = pd.to_numeric(big_df["换手率"])
    big_df["振幅"] = big_df["振幅"].str.strip("%")
    big_df["振幅"] = pd.to_numeric(big_df["振幅"])
    return big_df


def stock_us_hist_fu(
    symbol: str = "202545",
    start_date: str = "19700101",
    end_date: str = "22220101",
) -> pd.DataFrame:
    """
    富途牛牛-行情-美股-每日行情
    https://www.futunn.com/stock/HON-US
    :param symbol: 股票代码; 此股票代码可以通过调用 ak.stock_us_code_table_fu() 的 `代码` 字段获取
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 每日行情
    :rtype: pandas.DataFrame
    """
    url = "https://www.futunn.com/stock/HON-US?seo_redirect=1&channel=1244&subchannel=2&from=BaiduAladdin&utm_source=alading_user&utm_medium=website_growth"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "futu-x-csrf-token": "FM5ZhxYFQsZM4k9rXk3TMA==-O4oTw/tuNRp5DlJNWo/TNEEfMt8=",
        "pragma": "no-cache",
        "referer": "https://www.futunn.com/stock/HON-US?seo_redirect=1&channel=1244&subchannel=2&from=BaiduAladdin&utm_source=alading_user&utm_medium=website_growth",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    }
    session_ = requests.session()
    r = session_.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    url = "https://www.futunn.com/quote-api/get-kline"
    params = {
        "stock_id": symbol,
        "market_type": "2",
        "type": "2",
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "futu-x-csrf-token": soup.find("meta")["content"],
        "pragma": "no-cache",
        "referer": "https://www.futunn.com/stock/HON-US?seo_redirect=1&channel=1244&subchannel=2&from=BaiduAladdin&utm_source=alading_user&utm_medium=website_growth",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    r = session_.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["list"])
    temp_df.columns = [
        "日期",
        "今开",
        "今收",
        "最高",
        "最低",
        "成交量",
        "成交额",
        "换手率",
        "-",
        "昨收",
    ]
    temp_df = temp_df[
        [
            "日期",
            "今开",
            "今收",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "换手率",
            "昨收",
        ]
    ]
    temp_df.index = pd.to_datetime(temp_df["日期"], unit="s")
    temp_df = temp_df[start_date:end_date]
    temp_df.reset_index(inplace=True, drop=True)
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], unit="s").dt.date
    temp_df["今开"] = pd.to_numeric(temp_df["今开"]) / 100
    temp_df["最高"] = pd.to_numeric(temp_df["最高"]) / 100
    temp_df["最低"] = pd.to_numeric(temp_df["最低"]) / 100
    temp_df["今收"] = pd.to_numeric(temp_df["今收"]) / 100
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"]) / 100
    return temp_df


if __name__ == "__main__":
    stock_us_hist_fu_df = stock_us_hist_fu(symbol="202545")
    print(stock_us_hist_fu_df)

    stock_us_code_table_fu_df = stock_us_code_table_fu()
    print(stock_us_code_table_fu_df)
