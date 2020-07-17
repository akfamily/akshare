# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/12/4 15:49
Desc: 获取谷歌指数, 必须使用代理, 获得的数据是小时频率的, 所以获取时间周期太长会很慢
"""
from akshare.index.request import TrendReq
import matplotlib.pyplot as plt


def google_index(
    word="python", start_date="2019-12-01", end_date="2019-12-04", plot=True
):
    """
    返回指定区间的谷歌指数
    """
    pytrends = TrendReq(hl="en-US", tz=360)
    kw_list = [word]
    pytrends.build_payload(
        kw_list, cat=0, timeframe=start_date + " " + end_date, geo="", gprop=""
    )
    search_df = pytrends.interest_over_time()
    if plot:
        search_df[word].plot()
        plt.legend()
        plt.show()
        return search_df[word]
    return search_df[word]


if __name__ == "__main__":
    google_index_df = google_index(
        word="AI", start_date="2019-12-10T10", end_date="2019-12-10T23", plot=True
    )
    print(google_index_df)
