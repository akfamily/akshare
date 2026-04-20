#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/4/20 16:00
Desc: 腾讯证券-沪深京-实时行情数据
https://stockapp.finance.qq.com/mstats/#mod=list&id=hs_hsj&module=hs&type=hsj&sort=2&page=1&max=20
"""

import pandas as pd
import requests


def stock_zh_a_spot_tx() -> pd.DataFrame:
    """
    腾讯证券-沪深京-实时行情数据
    https://stockapp.finance.qq.com/mstats/#mod=list&id=hs_hsj&module=hs&type=hsj&sort=2&page=1&max=20
    :return: 所有股票的实时行情数据
    :rtype: pandas.DataFrame
    """
    url = "https://proxy.finance.qq.com/cgi/cgi-bin/rank/hs/getBoardRankList"
    params = {
        "_appver": "11.17.0",
        "board_code": "aStock",
        "sort_type": "price",
        "direct": "down",
        "offset": "0",
        "count": "200",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data']['rank_list'])
    return temp_df


if __name__ == '__main__':
    stock_zh_a_spot_tx_df = stock_zh_a_spot_tx()
    print(stock_zh_a_spot_tx_df)
