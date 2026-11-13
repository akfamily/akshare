#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/13 17:00
Desc: 美股目标价 or 港股目标价
https://www.ushknews.com/report.html
"""

import pandas as pd

from akshare.utils import http


def stock_target_price_js(symbol: str = "us") -> pd.DataFrame:
    """
    美股目标价 or 港股目标价
    https://www.ushknews.com/report.html
    :param symbol: choice of {"us", "hk"}
    :type symbol: str
    :return: 美股目标价 or 港股目标价
    :rtype: pandas.DataFrame
    """
    url = "https://calendar-api.ushknews.com/getWebTargetPriceList"
    params = {
        "limit": "20",
        "category": symbol,
    }
    # 不声明 accept-encoding: br：未安装 brotli 时 requests 无法解压，会报 JSONDecodeError
    headers = {
        "accept": "application/json, text/plain, */*",
        "origin": "https://www.ushknews.com",
        "referer": "https://www.ushknews.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "x-app-id": "BNsiR9uq7yfW0LVz",
        "x-version": "1.0.0",
    }
    r = http.get(url, params=params, headers=headers)
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["data"]["list"])
    temp_df = temp_df.rename(
        columns={
            "pub_time": "日期",
            "name": "个股名称",
            "latest_rating": "评级",
            "previous_target_price": "先前目标价",
            "latest_target_price": "最新目标价",
            "institution": "机构名称",
        }
    )
    temp_df = temp_df[
        [
            "日期",
            "个股名称",
            "评级",
            "先前目标价",
            "最新目标价",
            "机构名称",
        ]
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["先前目标价"] = pd.to_numeric(
        temp_df["先前目标价"], errors="coerce"
    ).astype(float)
    temp_df["最新目标价"] = pd.to_numeric(
        temp_df["最新目标价"], errors="coerce"
    ).astype(float)
    return temp_df


if __name__ == "__main__":
    stock_target_price_js_df = stock_target_price_js(symbol="us")
    print(stock_target_price_js_df)

    stock_target_price_js_df = stock_target_price_js(symbol="hk")
    print(stock_target_price_js_df)
