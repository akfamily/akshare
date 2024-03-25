#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/3/25 17:27
Desc: openctp 期货交易费用参照表
http://openctp.cn/fees.html
"""

from io import BytesIO

import pandas as pd
import requests


def futures_fees_info() -> pd.DataFrame:
    """
    openctp 期货交易费用参照表
    http://openctp.cn/fees.html
    :return: 期货交易费用参照表
    :rtype: pandas.DataFrame
    """
    url = "http://openctp.cn/fees.csv"
    r = requests.get(url)
    temp_df = pd.read_csv(BytesIO(r.content))
    return temp_df


if __name__ == "__main__":
    futures_fees_info_df = futures_fees_info()
    print(futures_fees_info_df)
