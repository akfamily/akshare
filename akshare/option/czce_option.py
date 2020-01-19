# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/1/19 14:44
contact: jindaxiang@163.com
desc: 郑州商品交易所-交易数据-历史行情下载-期权历史行情下载
http://www.czce.com.cn/cn/jysj/lshqxz/H770319index_1.htm
自 2020 年 1 月 1 日起，成交量、空盘量、成交额、行权量均为单边计算
SR  20170419
"""
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup


def option_czce_hist(symbol="SR", year="2019"):
    url = "http://app.czce.com.cn/cms/cmsface/czce/newcms/calendarnewAll.jsp"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "181",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "app.czce.com.cn",
        "Origin": "http://www.czce.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://www.czce.com.cn/cn/jysj/lshqxz/H770319index_1.htm",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
    }
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
    url = soup.get_text()[soup.get_text().find("'")+1:soup.get_text().rfind("'")].split(",")[0][:-1]
    res = requests.get(url)
    option_df = pd.read_table(StringIO(res.text), skiprows=1, sep="|", low_memory=False)
    return option_df


if __name__ == '__main__':
    option_czce_hist_df = option_czce_hist(symbol="SR", year="2018")
    print(option_czce_hist_df)
