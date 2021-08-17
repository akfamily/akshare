# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/8/17 17:59
Desc: 
"""
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from py_mini_racer import py_mini_racer

url = 'https://www.jidan7.com/trend/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
js_text = soup.find_all("script")[7]
js_code = py_mini_racer.MiniRacer()
