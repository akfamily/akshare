#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/3/5 18:00
Desc: 外盘期货-历史行情数据-日频率
https://finance.sina.com.cn/money/future/hf.html
"""

from datetime import datetime
from io import StringIO

import pandas as pd

from akshare.futures.futures_hq_sina import (
    _futures_foreign_commodity_symbols,
)
from akshare.utils import http


def futures_foreign_hist_sina(symbol: str = "ZSD") -> pd.DataFrame:
    """
    外盘期货-历史行情数据-日频率
    https://finance.sina.com.cn/money/future/hf.html
    :param symbol: 外盘期货代码，可以通过 ak.futures_foreign_commodity_subscribe_exchange_symbol() 来获取所有品种代码
    :type symbol: str
    :return: 历史行情数据-日频率
    :rtype: pandas.DataFrame
    """
    today = f"{datetime.today().year}_{datetime.today().month}_{datetime.today().day}"
    url = (
        f"https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_S{today}=/"
        f"GlobalFuturesService.getGlobalFuturesDailyKLine"
    )
    params = {
        "symbol": symbol,
        "_": today,
        "source": "web",
    }
    r = http.get(url, params=params)
    data_text = r.text
    data_df = pd.read_json(StringIO(data_text[data_text.find("[") : -2]))
    return data_df


def futures_foreign_detail_sina(symbol: str = "ZSD") -> pd.DataFrame:
    """
    foreign futures contract detail data
    :param symbol: futures symbol, you can get it from ak.futures_hq_subscribe_exchange_symbol function
    :type symbol: str
    :return: contract detail, one row per item
    :rtype: pandas.DataFrame
    """
    url = f"https://finance.sina.com.cn/futures/quotes/{symbol}.shtml"
    r = http.get(url)
    r.encoding = "gbk"
    data_text = r.text
    # 页面上是每行三组“项目-内容”的表格，没有表头；整理成 item/value 两列
    raw_df = pd.read_html(StringIO(data_text))[6]
    pairs = [
        raw_df.iloc[:, [i, i + 1]].set_axis(["item", "value"], axis=1)
        for i in range(0, raw_df.shape[1] - 1, 2)
    ]
    data_df = pd.concat(pairs).sort_index(kind="stable").reset_index(drop=True)
    data_df = data_df.dropna(subset=["item"]).reset_index(drop=True)
    return data_df


if __name__ == "__main__":
    futures_foreign_hist_sina_df = futures_foreign_hist_sina(symbol="JY")
    print(futures_foreign_hist_sina_df)

    subscribes = _futures_foreign_commodity_symbols()

    for item in subscribes:
        futures_foreign_detail_sina_df = futures_foreign_detail_sina(symbol=item)
        print(futures_foreign_detail_sina_df)

    for item in subscribes:
        futures_foreign_hist_sina_df = futures_foreign_hist_sina(symbol=item)
        print(futures_foreign_hist_sina_df)
