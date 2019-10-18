# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/18 9:04
contact: jindaxiang@163.com
desc: 获取指数目录, 由于目录太大, 不适合放在网站上, 终止！
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

from akshare.index.cons import short_headers

url = "https://cn.investing.com/indices/world-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on"
res = requests.get(url, headers=short_headers)
table_df = pd.read_html(res.text)
j = 0
for i in range(len(table_df[:-12])):
    j += len(table_df[i])
