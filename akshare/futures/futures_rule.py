# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/30 21:51
contact: jindaxiang@163.com
desc: 国泰君安期货-交易日历数据表
http://www.gtjaqh.com/jyrl.html
"""
import pandas as pd

from akshare.futures.cons import futures_rule_url


def futures_rule() -> pd.DataFrame:
    """
    国泰君安期货-交易日历数据表, 必须在交易日运行
    http://www.gtjaqh.com/jyrl.html
    :return: 交易日历数据
    :rtype: pandas.DataFrame
    """
    temp_df = pd.read_html(futures_rule_url, header=0)[0]
    temp_df.dropna(subset=["品种"], inplace=True)
    return temp_df


if __name__ == '__main__':
    futures_rule_df = futures_rule()
    print(futures_rule_df)
