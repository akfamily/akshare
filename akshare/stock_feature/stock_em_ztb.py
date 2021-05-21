# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/5/21 17:50
Desc: 首页-行情中心-涨停板行情-涨停股池
http://quote.eastmoney.com/ztb/detail#type=ztgc
"""
import pandas as pd
import requests


def stock_em_zt_pool(date: str = '20210521') -> pd.DataFrame:
    """
    首页-行情中心-涨停板行情-涨停股池
    http://quote.eastmoney.com/ztb/detail#type=ztgc
    :return: 涨停股池
    :rtype: pandas.DataFrame
    """
    url = 'http://push2ex.eastmoney.com/getTopicZTPool'
    params = {
        'ut': '7eea3edcaed734bea9cbfc24409ed989',
        'dpt': 'wz.ztzt',
        'Pageindex': '0',
        'pagesize': '320',
        'sort': 'fbt:asc',
        'date': date,
        '_': '1621590489736',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data']['pool'])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.columns = [
        '序号',
        '代码',
        '_',
        '名称',
        '最新价',
        '涨跌幅',
        '成交额',
        '流通市值',
        '总市值',
        '换手率',
        '连板数',
        '首次封板时间',
        '最后封板时间',
        '封板资金',
        '炸板次数',
        '所属行业',
        '涨停统计',
    ]
    temp_df['涨停统计'] = temp_df['涨停统计'].apply(lambda x: dict(x)['days']).astype(str) + "/" + temp_df['涨停统计'].apply(lambda x: dict(x)['ct']).astype(str)
    temp_df = temp_df[[
        '序号',
        '代码',
        '名称',
        '涨跌幅',
        '最新价',
        '成交额',
        '流通市值',
        '总市值',
        '换手率',
        '封板资金',
        '首次封板时间',
        '最后封板时间',
        '炸板次数',
        '涨停统计',
        '连板数',
        '所属行业',
    ]]
    return temp_df


def stock_em_zt_pool_previous(date: str = '20210521') -> pd.DataFrame:
    """
    首页-行情中心-涨停板行情-昨日涨停股池
    http://quote.eastmoney.com/ztb/detail#type=zrzt
    :return: 昨日涨停股池
    :rtype: pandas.DataFrame
    """
    url = 'http://push2ex.eastmoney.com/getYesterdayZTPool'
    params = {
        'ut': '7eea3edcaed734bea9cbfc24409ed989',
        'dpt': 'wz.ztzt',
        'Pageindex': '0',
        'pagesize': '170',
        'sort': 'zs:desc',
        'date': date,
        '_': '1621590489736',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data']['pool'])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.columns = [
        '序号',
        '代码',
        '_',
        '名称',
        '最新价',
        '涨停价',
        '涨跌幅',
        '成交额',
        '流通市值',
        '总市值',
        '换手率',
        '振幅',
        '涨速',
        '昨日封板时间',
        '昨日连板数',
        '所属行业',
        '涨停统计',
    ]
    temp_df['涨停统计'] = temp_df['涨停统计'].apply(lambda x: dict(x)['days']).astype(str) + "/" + temp_df['涨停统计'].apply(lambda x: dict(x)['ct']).astype(str)
    temp_df = temp_df[[
        '序号',
        '代码',
        '名称',
        '涨跌幅',
        '最新价',
        '涨停价',
        '成交额',
        '流通市值',
        '总市值',
        '换手率',
        '涨速',
        '振幅',
        '昨日封板时间',
        '昨日连板数',
        '涨停统计',
        '所属行业',
    ]]
    return temp_df


if __name__ == '__main__':
    stock_em_zt_pool_df = stock_em_zt_pool(date='20210521')
    print(stock_em_zt_pool_df)

    stock_em_zt_pool_previous_df = stock_em_zt_pool_previous(date='20210521')
    print(stock_em_zt_pool_previous_df)


