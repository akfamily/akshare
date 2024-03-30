#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/3/30 17:00
Desc: openctp 期货交易费用参照表
http://openctp.cn/fees.html
"""

import pandas as pd


def futures_fees_info() -> pd.DataFrame:
    """
    openctp 期货交易费用参照表
    http://openctp.cn/fees.html
    :return: 期货交易费用参照表
    :rtype: pandas.DataFrame
    """
    url = "http://openctp.cn/fees.html"
    temp_df = pd.read_html(url)[0]
    return temp_df


if __name__ == "__main__":
    futures_fees_info_df = futures_fees_info()
    print(futures_fees_info_df)
