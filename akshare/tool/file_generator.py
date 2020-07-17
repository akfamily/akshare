# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/11/14 14:38
Desc:
"""
import requests
from bs4 import BeautifulSoup
url = "https://suulnnka.github.io/BullshitGenerator/index.html"
payload = {
    "主题": "一带一路",
    "随机中立": 409467
}
res = requests.get(url, params=payload)
soup = BeautifulSoup(res.text, "lxml")
soup.find("一带一路")
