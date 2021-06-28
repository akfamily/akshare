# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/3/26 19:10
Desc: foreign futures detail data
http://finance.sina.com.cn/money/future/hf.html
"""
from datetime import datetime

import pandas as pd
import requests

from akshare.futures.futures_hq_sina import futures_foreign_commodity_subscribe_exchange_symbol


def futures_foreign_hist(symbol: str = "ZSD") -> pd.DataFrame:
    """
    foreign futures historical data
    :param symbol: futures symbol, you can get it from futures_foreign_commodity_subscribe_exchange_symbol
    :type symbol: str
    :return: historical data from 2010
    :rtype: pandas.DataFrame
    """
    today = f'{datetime.today().year}_{datetime.today().month}_{datetime.today().day}'
    url = f"https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_S{today}=/GlobalFuturesService.getGlobalFuturesDailyKLine"
    params = {
        "symbol": symbol,
        "_": today,
        "source": "web",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_df = pd.read_json(data_text[data_text.find("["):-2])
    return data_df


def futures_foreign_detail(symbol: str = "ZSD") -> pd.DataFrame:
    """
    foreign futures contract detail data
    :param symbol: futures symbol, you can get it from hf_subscribe_exchange_symbol function
    :type symbol: str
    :return: contract detail
    :rtype: pandas.DataFrame
    """
    url = f"https://finance.sina.com.cn/futures/quotes/{symbol}.shtml"
    r = requests.get(url)
    r.encoding = "gbk"
    data_text = r.text
    data_df = pd.read_html(data_text)[6]
    return data_df


if __name__ == '__main__':
    subscribes = futures_foreign_commodity_subscribe_exchange_symbol()

    futures_foreign_hist_df = futures_foreign_hist(symbol="ZSD")
    print(futures_foreign_hist_df)

    for item in subscribes:
        futures_foreign_detail_df = futures_foreign_detail(symbol=item)
        print(futures_foreign_detail_df)
