#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/2 17:26
Desc: 富途牛牛-行情-美股-每日行情
https://www.futunn.com/stock/HON-US?seo_redirect=1&channel=1244&subchannel=2&from=BaiduAladdin&utm_source=alading_user&utm_medium=website_growth
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup


def stock_us_hist_fu(
    symbol: str = "202545",
    start_date: str = "19700101",
    end_date: str = "22220101",
) -> pd.DataFrame:
    """
    富途牛牛-行情-美股-每日行情
    https://www.futunn.com/stock/HON-US
    :param symbol: 股票代码; 此股票代码需要通过调用 ak.stock_us_spot_em 的 `代码` 字段获取
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 每日行情
    :rtype: pandas.DataFrame
    """
    raw_url = "https://www.futunn.com/stock/HON-US?seo_redirect=1&channel=1244&subchannel=2&from=BaiduAladdin&utm_source=alading_user&utm_medium=website_growth"
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
    session = requests.session()
    r = session.get(raw_url, headers=headers)
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
    r = session.get(url, params=params, headers=headers)
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
