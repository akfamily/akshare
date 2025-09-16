#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/9/16 21:00
Desc: 天天基金-基金档案
https://fundf10.eastmoney.com/jbgk_015641.html
"""
from io import StringIO

import pandas as pd
import requests


def fund_overview_em(symbol: str = "015641") -> pd.DataFrame:
    """
    天天基金-基金档案-基本概况
    https://fundf10.eastmoney.com/jbgk_015641.html
    :param symbol: 基金代码
    :type symbol: str
    :return: 基本概况
    :rtype: pandas.DataFrame
    """
    url = f"https://fundf10.eastmoney.com/jbgk_{symbol}.html"
    r = requests.get(url)
    html_content = pd.read_html(StringIO(r.text))

    if len(html_content) == 0:
        temp_df = pd.DataFrame([])
    else:
        df_dict = {}
        # 最后一个表格的数据是我们想要的，按照Key-Value的形式存储
        for _, row in html_content[-1].iterrows():
            df_dict[row[0]] = row[1]
            df_dict[row[2]] = row[3]
        temp_df = pd.DataFrame([df_dict])

    return temp_df


if __name__ == "__main__":
    fund_overview_em_df = fund_overview_em(symbol="015641")
    print(fund_overview_em_df)
