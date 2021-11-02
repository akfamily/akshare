# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/11/2 17:43
Desc: 
"""
# import time
#
# import requests
# import pandas as pd
# import time
# from bs4 import BeautifulSoup
#
# url = "http://stock.finance.sina.com.cn/stock/go.php/vPerformancePrediction/kind/eps/index.phtml"
# big_df = pd.DataFrame()
# page = 1
# while 1:
#     params = {
#         'num': '500',
#         'p': page,
#     }
#     print(page)
#     r = requests.get(url, params=params)
#     try:
#         temp_df = pd.read_html(r.text)[0]
#         big_df = big_df.append(temp_df, ignore_index=True)
#         page += 1
#         time.sleep(5)
#     except:
#         break
# big_df
