# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/4/30 22:11
Desc: 问财-热门 70 股票
http://www.iwencai.com/unifiedwap/home/index
"""
import requests
import pandas as pd


def stock_wc_hot_top() -> pd.DataFrame:
    """
    问财-热门 70 股票
    http://www.iwencai.com/unifiedwap/home/index
    :return: 热门 70 股票
    :rtype: pandas.DataFrame
    """
    url = 'http://www.iwencai.com/stockpick/cache'
    headers = {
        'hexin-v': 'A71zmAKegVB7viU8_TB5GQHTzBK0WvUe-4tVhH8H-BtCx9NER6oBfIveZV8M',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    params = {
        'token': '685028abd09621acfabc54dab635bba2',
        'p': '1',
        'perpage': '70',
        'changeperpage': '1',
        'showType': '["","","onTable","onTable","onTable","onTable","onTable","onTable"]'
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['result'])
    return temp_df


if __name__ == '__main__':
    stock_wc_hot_top_df = stock_wc_hot_top()
    print(stock_wc_hot_top_df)
