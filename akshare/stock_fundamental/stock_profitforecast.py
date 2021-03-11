# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/3/10 19:12
Desc: 
"""
import requests
import pandas as pd
from tqdm import tqdm

url = "http://reportapi.eastmoney.com/report/predic"
params = {
    'dyCode': '*',
    'pageNo': '1',
    'pageSize': '100',
    'fields': '',
    'beginTime': '2019-03-10',
    'endTime': '2021-03-10',
    'hyCode': '*',
    'gnCode': '*',
    'marketCode': '*',
    'sort': 'count,desc',
    'p': '1',
    'pageNum': '1',
    '_': '1615374649216',
}
r = requests.get(url, params=params)
data_json = r.json()
page_num = data_json['TotalPage']
big_df = pd.DataFrame()
for page in tqdm(range(1, page_num+1)):
    params = {
        'dyCode': '*',
        'pageNo': page,
        'pageSize': '100',
        'fields': '',
        'beginTime': '2019-03-10',
        'endTime': '2021-03-10',
        'hyCode': '*',
        'gnCode': '*',
        'marketCode': '*',
        'sort': 'count,desc',
        'p': page,
        'pageNum': page,
        '_': '1615374649216',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data'])
    big_df = big_df.append(temp_df, ignore_index=True)
big_df.reset_index(inplace=True)
big_df['index'] = range(1, len(big_df)+1)
big_df.columns = [
    '序号',
    '名称',
    '代码',
    '研报数',
    '机构投资评级(近六个月)-买入',
    '机构投资评级(近六个月)-增持',
    '机构投资评级(近六个月)-中性',
    '机构投资评级(近六个月)-减持',
    '机构投资评级(近六个月)-卖出',
    '_',
    '_',
    '_',
    '_',
]
