#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/3/18 20:03
Desc: 谷歌指数, 必须使用代理, 获得的数据是小时频率的, 所以获取时间周期太长会很慢
"""
from akshare.index.request import TrendReq
import pandas as pd


def google_index(
    symbol: str = "python",
    start_date: str = "20191201",
    end_date: str = "20191204",
):
    """
    谷歌指数
    :param symbol: 关键词
    :type symbol: str
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :return: 谷歌指数
    :rtype: pandas
    """

    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    pytrends = TrendReq(hl="en-US", tz=360)
    kw_list = [symbol]
    pytrends.build_payload(
        kw_list, cat=0, timeframe=start_date + " " + end_date, geo="", gprop=""
    )
    search_df = pytrends.interest_over_time()
    search_se = search_df[symbol]
    search_df = pd.DataFrame(search_se)
    search_df.reset_index(inplace=True)
    if "T" not in start_date:
        search_df['date'] = pd.to_datetime(search_df['date']).dt.date
    return search_df


if __name__ == "__main__":
    google_index_df = google_index(symbol="bitcoin", start_date="20000101", end_date="20220303")
    print(google_index_df)

    google_index_df = google_index(symbol="python", start_date='20040101', end_date='20191201')
    print(google_index_df)

    google_index_df = df = google_index(symbol="AI", start_date="20191210T10", end_date="20191210T23")
    print(google_index_df)
