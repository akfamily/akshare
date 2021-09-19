# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2020/10/10 13:42
Desc: 国债期货可交割券相关指标
http://www.csindex.com.cn/zh-CN/bond-valuation/bond-futures-deliverable-coupons-related-indicators?date=2020-09-22
"""
import pandas as pd
import requests


def bond_futures_deliverable_coupons(trade_date: str = "20200923") -> pd.DataFrame:
    """
    国债期货可交割券相关指标
    http://www.csindex.com.cn/zh-CN/bond-valuation/bond-futures-deliverable-coupons-related-indicators
    :param trade_date: 交易日
    :type trade_date: str
    :return: 国债期货可交割券相关指标
    :rtype: pandas.DataFrame
    """
    trade_date = '-'.join([trade_date[:4], trade_date[4:6], trade_date[6:]])
    url = "http://www.csindex.com.cn/zh-CN/bond-valuation/bond-futures-deliverable-coupons-related-indicators"
    params = {
        "date": trade_date
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Host': 'www.csindex.com.cn',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': f'http://www.csindex.com.cn/zh-CN/bond-valuation/bond-futures-deliverable-coupons-related-indicators?date={trade_date}',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }
    r = requests.get(url, params=params, headers=headers)
    temp_df = pd.read_html(r.text)[0]
    temp_df['日期'] = temp_df['日期'].astype(str)
    temp_df['银行间代码'] = temp_df['银行间代码'].astype(str)
    temp_df['上交所代码'] = temp_df['上交所代码'].astype(str)
    temp_df['深交所代码'] = temp_df['深交所代码'].astype(str)
    temp_df.rename({"中证估值(净价)": "中证估值", "隐含回购利率(%)": "隐含回购利率"}, inplace=True, axis=1)
    return temp_df


if __name__ == '__main__':
    bond_futures_deliverable_coupons_df = bond_futures_deliverable_coupons(trade_date="20210823")
    print(bond_futures_deliverable_coupons_df)
