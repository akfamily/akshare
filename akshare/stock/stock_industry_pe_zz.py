# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/9/14 16:29
Desc: 巨潮资讯-数据中心-行业分析-行业市盈率
http://webapi.cninfo.com.cn/#/thematicStatistics?name=%E6%8A%95%E8%B5%84%E8%AF%84%E7%BA%A7
"""
import time
from py_mini_racer import py_mini_racer
import requests
import pandas as pd


trade_date = '20210910'
url = "http://www.csindex.com.cn/zh-CN/downloads/industry-price-earnings-ratio"
trade_date = '-'.join([trade_date[:4], trade_date[4:6], trade_date[6:]])
params = {
    "type": "zjh1",
    "date": trade_date,
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Host': 'www.csindex.com.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': f'http://www.csindex.com.cn/zh-CN/downloads/industry-price-earnings-ratio?type=zjh2&date={trade_date}',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
}
r = requests.get(url, params=params, headers=headers)
temp_df = pd.read_html(r.text)[0]