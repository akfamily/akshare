# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/11/26 8:31
contact: jindaxiang@163.com
desc: 
"""
import pandas as pd

data = pd.read_excel(r'C:\Users\king\Desktop\sun\weather.xlsx', index_col=0, parse_dates=True)
city_list = list(set(data["area"]))
big_df = data[data["area"] == city_list[0]]
for city in city_list[1:]:
    temp_df = data[data["area"] == city]
    big_df = big_df.merge(temp_df, left_index=True, right_index=True)
big_df.to_excel("weather2.xlsx")