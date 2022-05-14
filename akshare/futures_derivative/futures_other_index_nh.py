# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/4/14 15:24
Desc: 板块指数、品种指数和相关系数矩阵
南华期货-板块指数涨跌
http://www.nanhua.net/nhzc/platechange.html
南华期货-品种指数涨跌
http://www.nanhua.net/nhzc/varietychange.html
南华期货-相关系数矩阵
http://www.nanhua.net/nhzc/correltable.html
"""
import pandas as pd
import requests


def futures_board_index_nh(start_date: str = "20220104", end_date: str = "20220413") -> pd.DataFrame:
    """
    南华期货-市场涨跌-板块指数涨跌
    http://www.nanhua.net/nhzc/platechange.html
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :return: 板块指数涨跌
    :rtype: pandas.DataFrame
    """
    url = f"http://www.nanhua.net/ianalysis/plate/{start_date[:4]}/{start_date[4:6]}/{start_date}.json"
    params = {
        't': '1649920913503'
    }
    r = requests.get(url, params=params)
    start_df = pd.DataFrame(r.json())
    start_df.columns = [
        'name',
        'code',
        start_date,
    ]

    url = f"http://www.nanhua.net/ianalysis/plate/{end_date[:4]}/{end_date[4:6]}/{end_date}.json"
    params = {
        't': '1649920913503'
    }
    r = requests.get(url, params=params)
    end_df = pd.DataFrame(r.json())
    end_df.columns = [
        'name',
        'code',
        'end_date',
    ]

    start_df[end_date] = end_df['end_date']
    start_df['gap'] = start_df[end_date] - start_df[start_date]
    start_df['return'] = start_df['gap']/start_df[start_date]

    temp_df = start_df
    temp_df = temp_df[['name', 'return']]

    return temp_df


def futures_variety_index_nh(start_date: str = "20220104", end_date: str = "20220413") -> pd.DataFrame:
    """
    南华期货-市场涨跌-品种指数涨跌
    http://www.nanhua.net/nhzc/varietychange.html
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :return: 品种指数涨跌
    :rtype: pandas.DataFrame
    """
    url = f"http://www.nanhua.net/ianalysis/variety/{start_date[:4]}/{start_date[4:6]}/{start_date}.json"
    params = {
        't': '1649920913503'
    }
    r = requests.get(url, params=params)
    start_df = pd.DataFrame(r.json())
    start_df.columns = [
        'name',
        'code',
        start_date,
    ]

    url = f"http://www.nanhua.net/ianalysis/variety/{end_date[:4]}/{end_date[4:6]}/{end_date}.json"
    params = {
        't': '1649920913503'
    }
    r = requests.get(url, params=params)
    end_df = pd.DataFrame(r.json())
    end_df.columns = [
        'name',
        'code',
        'end_date',
    ]
    start_df[end_date] = end_df['end_date']

    start_df['gap'] = start_df[end_date] - start_df[start_date]
    start_df['return'] = start_df['gap']/start_df[start_date]

    temp_df = start_df
    temp_df = temp_df[['name', 'return']]
    return temp_df


def futures_correlation_nh(date: str = "20220104", period: str = "20") -> pd.DataFrame:
    """
    南华期货-统计监控-相关系数矩阵
    http://www.nanhua.net/nhzc/correltable.html
    :param date: 开始时间
    :type date: str
    :param period: 周期; choice of {"5", "20", "60", "120"}
    :type period: str
    :return: 相关系数矩阵
    :rtype: pandas.DataFrame
    """
    url = f"http://www.nanhua.net/ianalysis/correl/{period}/{date[:4]}/{date[4:6]}/{date}.json"
    params = {
        't': '1649920913503'
    }
    r = requests.get(url, params=params)
    temp_df = pd.DataFrame(r.json())
    temp_df.columns = [
        '品种代码1',
        '品种名称1',
        '品种代码2',
        '品种名称2',
        '相关系数',
    ]
    temp_df['相关系数'] = pd.to_numeric(temp_df['相关系数'])
    return temp_df


if __name__ == '__main__':
    futures_board_index_nh_df = futures_board_index_nh(start_date="20220104", end_date="20220413")
    print(futures_board_index_nh_df)

    futures_variety_index_nh_df = futures_variety_index_nh(start_date="20220104", end_date="20220413")
    print(futures_variety_index_nh_df)

    futures_correlation_nh_df = futures_correlation_nh(date="20220104", period="20")
    print(futures_correlation_nh_df)
