# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/18 10:24
contact: jindaxiang@163.com
desc: 
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

from akshare.index.cons import short_headers


url = "http://www.chinamoney.com.cn/ags/ms/cm-u-md-bond/CbMktMakQuot?flag=1&lang=cn&abdAssetEncdShrtDesc=&emaEntyEncdShrtDesc="
payload = {
    "flag": "1",
    "lang": "cn",
    "abdAssetEncdShrtDesc": "",
    "emaEntyEncdShrtDesc": "",
}
res = requests.post(url, data=payload, headers=short_headers)
df = res.json()["records"]
pd.DataFrame(df)
