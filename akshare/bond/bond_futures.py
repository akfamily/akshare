# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/9/24 13:42
Desc: 国债期货可交割券相关指标
http://www.csindex.com.cn/zh-CN/bond-valuation/bond-futures-deliverable-coupons-related-indicators?date=2020-09-22
"""
import pandas as pd
import requests


def bond_futures_deliverable_coupons(trade_date="2020-09-23"):
    """
    国债期货可交割券相关指标
    http://www.csindex.com.cn/zh-CN/bond-valuation/bond-futures-deliverable-coupons-related-indicators
    :param trade_date: 交易日
    :type trade_date: str
    :return: 国债期货可交割券相关指标
    :rtype: pandas.DataFrame
    """
    url = "http://www.csindex.com.cn/zh-CN/bond-valuation/bond-futures-deliverable-coupons-related-indicators"
    params = {
        "date": trade_date
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_html(r.text)[0]
    return temp_df


if __name__ == '__main__':
    bond_futures_deliverable_coupons_df = bond_futures_deliverable_coupons(trade_date="2020-09-22")
    print(bond_futures_deliverable_coupons_df)
