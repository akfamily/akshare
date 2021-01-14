# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/1/13 17:16
Desc: 新浪财经-股票-行业分类

"""
import requests
import pandas as pd

url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes"
r = requests.get(url)
data_json = r.json()
temp_df = pd.DataFrame(data_json[1][0][1][0][1])
temp_df


