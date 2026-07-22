#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/4/20 16:00
Desc: 腾讯证券-沪深京-实时行情数据
https://stockapp.finance.qq.com/mstats/#mod=list&id=hs_hsj&module=hs&type=hsj&sort=2&page=1&max=20
"""

import math

import pandas as pd
import requests

from akshare.utils.tqdm import get_tqdm


def stock_zh_a_spot_tx() -> pd.DataFrame:
    """
    腾讯证券-沪深京-实时行情数据
    https://stockapp.finance.qq.com/mstats/#mod=list&id=hs_hsj&module=hs&type=hsj&sort=2&page=1&max=20
    :return: 所有股票的实时行情数据
    :rtype: pandas.DataFrame
    """
    url = "https://proxy.finance.qq.com/cgi/cgi-bin/rank/hs/getBoardRankList"
    page_size = 200
    params = {
        "_appver": "11.17.0",
        "board_code": "aStock",
        "sort_type": "price",
        "direct": "down",
        "offset": "0",
        "count": str(page_size),
    }
    r = requests.get(url, params=params, timeout=30)
    data_json = r.json()
    total = int(data_json["data"]["total"])
    total_page = math.ceil(total / page_size)
    temp_df = pd.DataFrame(data_json["data"]["rank_list"])
    tqdm = get_tqdm()
    for page in tqdm(range(1, total_page), leave=False):
        params.update({"offset": str(page * page_size)})
        r = requests.get(url, params=params, timeout=30)
        page_json = r.json()
        page_df = pd.DataFrame(page_json["data"]["rank_list"])
        temp_df = pd.concat([temp_df, page_df], ignore_index=True)
    temp_df.drop_duplicates(subset=["code"], inplace=True, ignore_index=True)
    return temp_df


if __name__ == "__main__":
    stock_zh_a_spot_tx_df = stock_zh_a_spot_tx()
    print(stock_zh_a_spot_tx_df)
