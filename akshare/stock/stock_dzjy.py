# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/12/4 20:31
Desc: 东方财富网-数据中心-大宗交易-市场统计
http://data.eastmoney.com/dzjy/dzjy_sctj.aspx
"""
import demjson
import pandas as pd
import requests


def stock_dzjy_sctj() -> pd.DataFrame:
    """
    东方财富网-数据中心-大宗交易-市场统计
    http://data.eastmoney.com/dzjy/dzjy_sctj.aspx
    :return: 市场统计表
    :rtype: pandas.DataFrame
    """
    url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get'
    params = {
        'type': 'DZJYSCTJ',
        'token': '70f12f2f4f091e459a279469fe49eca5',
        'cmd': '',
        'st': 'TDATE',
        'sr': '-1',
        'p': '1',
        'ps': '50000',
        'js': 'var xoqCPdgn={pages:(tp),data:(x)}',
        'rt': '53569504',
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text.split('=')[1])
    temp_df = pd.DataFrame(data_json['data'])
    temp_df.columns = [
        '交易日期',
        '上证指数',
        '上证指数涨跌幅',
        '大宗交易成交总额',
        '溢价成交总额',
        '溢价成交总额占比',
        '折价成交总额',
        '折价成交总额占比',
    ]
    temp_df['交易日期'] = pd.to_datetime(temp_df['交易日期'])
    temp_df['上证指数'] = round(temp_df['上证指数'], 2)
    temp_df['上证指数涨跌幅'] = round(temp_df['上证指数涨跌幅'], 4)
    temp_df['大宗交易成交总额'] = round(temp_df['大宗交易成交总额'].astype(float), 2)
    temp_df['溢价成交总额'] = round(temp_df['溢价成交总额'].astype(float), 2)
    temp_df['溢价成交总额占比'] = round(temp_df['溢价成交总额占比'].astype(float), 4)
    temp_df['折价成交总额'] = round(temp_df['折价成交总额'].astype(float), 2)
    temp_df['折价成交总额占比'] = round(temp_df['折价成交总额占比'].astype(float), 4)
    return temp_df


if __name__ == '__main__':
    stock_dzjy_sctj_df = stock_dzjy_sctj()
    print(stock_dzjy_sctj_df)
