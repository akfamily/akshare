# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2024/9/1 22:20
Desc: 深圳证券交易所-期权子网-行情数据-当日合约
"""

import requests
import pandas as pd
from io import BytesIO
import warnings
warnings.filterwarnings('ignore', message="Workbook contains no default style")

def option_today_szse() -> pd.DataFrame:
    """
    深圳证券交易所-期权子网-行情数据-当日合约
    https://www.sse.org.cn/option/quotation/contract/daycontract/index.html
    :return: 深圳期权当日合约
    :rtype: pandas.DataFrame
    """
    url = "https://www.sse.org.cn/api/report/ShowReport"
    params = {
        "SHOWTYPE": "xlsx",
        "CATALOGID": "option_drhy",
        "TABKEY": "tab1",
        "random": "0.14023912951427653​",
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "query.sse.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/101.0.4951.67 Safari/537.36",
    }
    #r = requests.get(url, params=params, headers=headers)
    r = requests.get(url, params=params)
    temp_df = pd.read_excel(BytesIO(r.content))

    return temp_df


if __name__ == "__main__":
    option_today_df = option_today_szse()
    print(option_today_df)
