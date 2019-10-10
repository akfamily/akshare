# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
contact: jindaxiang@163.com
desc: 
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.option.cons import DCE_OPTION_URL, DCE_PAYLOAD

def get_dce_option_daily_bar(date="20190910"):
    DCE_PAYLOAD.update({"year": "2019"})
    DCE_PAYLOAD.update({"month", "9"})  # 大连商品交易所少一个月, e.g. 9 表示 10 月
    DCE_PAYLOAD.update({"day", "09"})

    res = requests.post(DCE_OPTION_URL, data=DCE_PAYLOAD)
    dce_option_df = pd.read_html(res.text)[0]
    dce_option_df.columns
