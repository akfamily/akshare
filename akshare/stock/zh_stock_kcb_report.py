# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/11/22 19:00
Desc: 科创板报告
http://data.eastmoney.com/notices/kcb.html
"""
import json

import pandas as pd
import requests
from tqdm import tqdm


def _zh_stock_kcb_report_page() -> int:
    """
    科创板报告的页数
    http://data.eastmoney.com/notices/kcb.html
    :return: 科创板报告的页数
    :rtype: int
    """
    url = "http://data.eastmoney.com/notices/getdata.ashx"
    params = {
        'StockCode': '',
        'FirstNodeType': '0',
        'CodeType': 'KCB',
        'PageIndex': '1',
        'PageSize': '5000',
        'jsObj': 'vblwauPF',
        'SecNodeType': '0',
        'Time': '',
        'rt': '53534758',
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find('{'):-1])
    return data_json['pages']


def zh_stock_kcb_report() -> pd.DataFrame:
    """
    科创板报告内容
    http://data.eastmoney.com/notices/kcb.html
    :return: 科创板报告内容
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    url = "http://data.eastmoney.com/notices/getdata.ashx"
    pages = _zh_stock_kcb_report_page()
    for i in tqdm(range(1, pages+1)):
        params = {
            'StockCode': '',
            'FirstNodeType': '0',
            'CodeType': 'KCB',
            'PageIndex': str(i),
            'PageSize': '5000',
            'jsObj': 'vblwauPF',
            'SecNodeType': '0',
            'Time': '',
            'rt': '53534758',
        }
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = json.loads(data_text[data_text.find('{'):-1])
        temp_df = pd.DataFrame([
            [item['codes'][0]['stock_code'] for item in data_json['data']],
            [item['codes'][0]['short_name'] for item in data_json['data']],
            [item['title'] for item in data_json['data']],
            [item['columns'][0]['column_name'] for item in data_json['data']],
            [item['notice_date'] for item in data_json['data']],
            [item['art_code'] for item in data_json['data']],
        ]).T
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [
        '代码',
        '名称',
        '公告标题',
        '公告类型',
        '公告日期',
        '公告代码',
    ]
    return big_df


if __name__ == '__main__':
    zh_stock_kcb_report_df = zh_stock_kcb_report()
    print(zh_stock_kcb_report_df)
