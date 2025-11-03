#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/10/30 15:00
Desc: 全部A股-等权重市盈率、中位数市盈率
https://www.legulegu.com/stockdata/a-ttm-lyr
"""
import pandas as pd
import requests

from akshare.stock_feature.stock_a_indicator import get_token_lg, get_cookie_csrf


def stock_a_ttm_lyr() -> pd.DataFrame:
    """
    全部 A 股-等权重市盈率、中位数市盈率
    :return: 全部A股-等权重市盈率、中位数市盈率
    :rtype: pandas.DataFrame
    """

    url = "https://legulegu.com/api/stock-data/market-ttm-lyr"
    params = {
        "marketId": "5",
        "token": get_token_lg(),
    }
    # 获取 cookie 和 headers
    csrf_data = get_cookie_csrf(url="https://www.legulegu.com/stockdata/a-ttm-lyr")
    # 使用返回的 headers（已经是副本）
    request_headers = csrf_data['headers'].copy()
    request_headers.update({
        "host": "www.legulegu.com",
        "referer": "https://www.legulegu.com/stockdata/a-ttm-lyr",
    })
    # 使用独立的 session
    session = requests.Session()
    r = session.get(
        url,
        params=params,
        cookies=csrf_data['cookies'],
        headers=request_headers,
    )
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df["date"] = pd.to_datetime(temp_df["date"], errors="coerce").dt.date
    # 关闭 session
    session.close()
    return temp_df


if __name__ == "__main__":
    stock_a_ttm_lyr_df = stock_a_ttm_lyr()
    print(stock_a_ttm_lyr_df)
