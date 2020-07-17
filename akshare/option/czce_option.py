# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/1/19 14:44
Desc: 郑州商品交易所-交易数据-历史行情下载-期权历史行情下载
http://www.czce.com.cn/cn/jysj/lshqxz/H770319index_1.htm
自 20200101 起，成交量、空盘量、成交额、行权量均为单边计算
郑州商品交易所-期权上市时间表
"SR": "20170419"
"CF": "20190410"
"TA": "20191216"
"MA": "20191217"
"RM": "20200116"
"""
from io import StringIO
import warnings

import pandas as pd
import requests
from bs4 import BeautifulSoup


def option_czce_hist(symbol="SR", year="2019"):
    """
    郑州商品交易所-交易数据-历史行情下载-期权历史行情下载
    http://www.czce.com.cn/cn/jysj/lshqxz/H770319index_1.htm
    :param symbol: {"白糖": "SR", "棉花": "CF", "PTA": "TA", "甲醇": "MA", "菜籽粕": "RM"}
    :type symbol: str
    :param year: 需要获取数据的年份, 注意品种的上市时间
    :type year: str
    :return: 制定年份的日频期权数据
    :rtype: pandas.DataFrame
    """
    symbol_year_dict = {
        "SR": "2017",
        "CF": "2019",
        "TA": "2019",
        "MA": "2019",
        "RM": "2020",
    }
    if int(symbol_year_dict[symbol]) > int(year):
        warnings.warn(f"{year} year, symbol {symbol} is not on trade")
        return
    url = "http://app.czce.com.cn/cms/cmsface/czce/newcms/calendarnewAll.jsp"
    payload = {
        "dataType": "HISTORY",
        "radio": "options",
        "curpath": "/cn/jysj/lshqxz/H770319index_1.htm",
        "curpath1": "",
        "pubDate": f"{year}-01-01",
        "commodity": symbol,
        "fileType": "txt",
        "download": "下载",
        "operate": "download",
    }
    res = requests.post(url, data=payload)
    soup = BeautifulSoup(res.text, "lxml")
    # 获取 url 地址
    url = soup.get_text()[
        soup.get_text().find("'") + 1: soup.get_text().rfind("'")
    ].split(",")[0][:-1]
    res = requests.get(url)
    option_df = pd.read_table(StringIO(res.text), skiprows=1, sep="|", low_memory=False)
    return option_df


if __name__ == "__main__":
    option_czce_hist_df = option_czce_hist(symbol="MA", year="2019")
    print(option_czce_hist_df)
