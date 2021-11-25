# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/11/25 15:37
Desc: 中证商品指数
http://www.cscidx.com/index.html
"""
import pandas as pd
import requests


def futures_index_cscidx(symbol: str = "中证监控油脂油料期货指数") -> pd.DataFrame:
    """
    中证商品指数-商品指数-分时数据
    http://www.cscidx.com/index.html
    :param symbol: choice of {"中证监控软商品期货指数", "中证监控油脂油料期货指数", "中证监控饲料期货指数", "中证监控能化期货指数", "中证监控钢铁期货指数", "中证监控建材期货指数"}
    :type symbol: str
    :return: 商品指数-分时数据
    :rtype: pandas.DataFrame
    """
    futures_index_map = {
        '中证监控软商品期货指数': ['606008.CCI', '0'],
        '中证监控油脂油料期货指数': ['606005.CCI', '1'],
        '中证监控饲料期货指数': ['606004.CCI', '2'],
        '中证监控能化期货指数': ['606010.CCI', '3'],
        '中证监控钢铁期货指数': ['606011.CCI', '4'],
        '中证监控建材期货指数': ['606012.CCI', '5'],
    }
    url = "http://www.cscidx.com/cscidx/csciAction/loadTimeData"
    params = {
        'r': '0.08644997232349438'
    }
    payload = {
        'indexCode': futures_index_map[symbol][0],
        'indexType': futures_index_map[symbol][1],
        'pointer': 'all',
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Content-Length': '44',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.cscidx.com',
        'Origin': 'http://www.cscidx.com',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.cscidx.com/cscidx/quote1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    r = requests.post(url, params=params, data=payload, headers=headers)
    data_json = r.json()
    # TODO
    return data_json


if __name__ == "__main__":
    futures_index_cscidx_df = futures_index_cscidx(symbol='中证监控油脂油料期货指数')
    print(futures_index_cscidx_df)
