# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/6/29 16:32
Desc: 
"""
import pandas as pd
import requests


def fund_em_aum() -> pd.DataFrame:
    """
    东方财富-基金-基金公司排名列表
    http://fund.eastmoney.com/Company/lsgm.html
    :return: 基金公司排名列表
    :rtype: pandas.DataFrame
    """
    url = 'http://fund.eastmoney.com/Company/home/gspmlist'
    params = {
        'fundType': '0'
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_html(r.text)[0]
    del temp_df['相关链接']
    del temp_df['天相评级']
    temp_df.columns = ['序号', '基金公司', '成立时间', '全部管理规模', '全部基金数', '全部经理数']
    expanded_df = temp_df['全部管理规模'].str.split(' ', expand=True)
    temp_df['全部管理规模'] = expanded_df.iloc[:, 0].str.replace(",", "")
    temp_df['更新日期'] = expanded_df.iloc[:, 1]
    temp_df['全部管理规模'] = pd.to_numeric(temp_df['全部管理规模'], errors="coerce")
    temp_df['全部基金数'] = pd.to_numeric(temp_df['全部基金数'])
    temp_df['全部经理数'] = pd.to_numeric(temp_df['全部经理数'])
    return temp_df


def fund_em_aum_trend() -> pd.DataFrame:
    """
    东方财富-基金-基金市场管理规模走势图
    http://fund.eastmoney.com/Company/lsgm.html
    :return: 基金市场管理规模走势图
    :rtype: pandas.DataFrame
    """
    url = 'http://fund.eastmoney.com/Company/home/GetFundTotalScaleForChart'
    payload = {
        'fundType': '0'
    }
    r = requests.get(url, data=payload)
    data_json = r.json()
    temp_df = pd.DataFrame()
    temp_df['date'] = data_json['x']
    temp_df['value'] = data_json['y']
    return temp_df


if __name__ == '__main__':
    fund_em_aum_df = fund_em_aum()
    print(fund_em_aum_df)

    fund_em_aum_trend_df = fund_em_aum_trend()
    print(fund_em_aum_trend_df)
