# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/7/21 14:22
Desc: 郑州商品交易所-交易数据-历史行情下载-期权历史行情下载
http://www.czce.com.cn/cn/jysj/lshqxz/H770319index_1.htm
自 20200101 起，成交量、空盘量、成交额、行权量均为单边计算
郑州商品交易所-期权上市时间表
"SR": "20170419"
"CF": "20190410"
"TA": "20191216"
"MA": "20191217"
"RM": "20200116"
"ZC": "20200630"
"""
from io import StringIO
import warnings

import pandas as pd
import requests
from bs4 import BeautifulSoup


def option_czce_hist(symbol: str = "SR", year: str = "2021") -> pd.DataFrame:
    """
    郑州商品交易所-交易数据-历史行情下载-期权历史行情下载
    http://www.czce.com.cn/cn/jysj/lshqxz/H770319index_1.htm
    :param symbol: choice of {"白糖": "SR", "棉花": "CF", "PTA": "TA", "甲醇": "MA", "菜籽粕": "RM", "动力煤": "ZC"}
    :type symbol: str
    :param year: 需要获取数据的年份, 注意品种的上市时间
    :type year: str
    :return: 指定年份的日频期权数据
    :rtype: pandas.DataFrame
    """
    symbol_year_dict = {
        "SR": "2017",
        "CF": "2019",
        "TA": "2019",
        "MA": "2019",
        "RM": "2020",
        "ZC": "2020",
    }
    if int(symbol_year_dict[symbol]) > int(year):
        warnings.warn(f"{year} year, symbol {symbol} is not on trade")
        return None
    warnings.warn("正在下载中, 请稍等")
    url = f'http://www.czce.com.cn/cn/DFSStaticFiles/Option/2021/OptionDataAllHistory/{symbol}OPTIONS{year}.txt'
    r = requests.get(url)
    option_df = pd.read_table(StringIO(r.text), skiprows=1, sep="|", low_memory=False)
    return option_df


if __name__ == "__main__":
    option_czce_hist_df = option_czce_hist(symbol="ZC", year="2021")
    print(option_czce_hist_df.info())
