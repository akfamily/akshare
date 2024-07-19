#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/7/19
Desc: 新浪财经-日内分时数据
"""

import pandas as pd
import requests
from akshare.utils.tqdm import get_tqdm


def stock_intraday_sina(symbol: str = "sz000001", date: str = "20240719") -> pd.DataFrame:
    """
    新浪财经-日内分时数据
    :param symbol: 股票代码
    :type symbol: str
    :param date: 交易日
    :type date: str
    :return: 分时数据
    :rtype: pandas.DataFrame
    """
    base_url = "https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList"
    params = {
        "symbol": symbol,
        "num": "60",
        "page": "1",
        "sort": "ticktime",
        "asc": "0",
        "volume": "0",
        "amount": "0",
        "type": "0",
        "day": "-".join([date[:4], date[4:6], date[6:]]),
    }
    headers = {
        "Referer": f"https://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill.php?symbol={symbol}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/126.0.0.0 Safari/537.36",
    }
    big_df = pd.DataFrame()
    page = 1
    tqdm = get_tqdm()

    # 假设最多有100页数据，可以根据实际情况调整
    max_pages = 100
    for page in tqdm(range(1, max_pages + 1), desc="Fetching data", leave=False):
        params.update({"page": page})
        response = requests.get(url=base_url, params=params, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code} on page {page}")

        data_json = response.json()
        if not data_json:
            break

        temp_df = pd.DataFrame(data_json)
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)

        if len(temp_df) < 60:
            break

    if big_df.empty or 'ticktime' not in big_df.columns:
        print("The expected 'ticktime' column is missing from the data.")
        return pd.DataFrame()

    big_df.sort_values(by=["ticktime"], inplace=True, ignore_index=True)
    big_df["price"] = pd.to_numeric(big_df["price"], errors="coerce")
    big_df["volume"] = pd.to_numeric(big_df["volume"], errors="coerce")
    big_df["prev_price"] = pd.to_numeric(big_df["prev_price"], errors="coerce")
    return big_df


if __name__ == "__main__":
    stock_intraday_sina_df = stock_intraday_sina(symbol="sz000001", date="20240719")
    if not stock_intraday_sina_df.empty:
        print(stock_intraday_sina_df)
    else:
        print("No intraday data available.")
