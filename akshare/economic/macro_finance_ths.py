#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/7/16 22:30
Desc: 同花顺-数据中心-宏观数据-股票筹资
https://data.10jqka.com.cn/macro/finance/
"""

from io import StringIO

import pandas as pd
import requests


def macro_stock_finance() -> pd.DataFrame:
    """
    同花顺-数据中心-宏观数据-股票筹资
    https://data.10jqka.com.cn/macro/finance/
    :return: 股票筹资
    :rtype: pandas.DataFrame
    """
    url = "https://data.10jqka.com.cn/macro/finance/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    temp_df = pd.read_html(StringIO(r.text))[0]
    temp_df.rename(
        columns={
            "月份": "月份",
            "募集资金(亿元)": "募集资金",
            "首发募集资金(亿元)": "首发募集资金",
            "增发募集资金(亿元)": "增发募集资金",
            "配股募集资金(亿元)": "配股募集资金",
        },
        inplace=True,
    )
    temp_df = temp_df[
        ["月份", "募集资金", "首发募集资金", "增发募集资金", "配股募集资金"]
    ]
    temp_df["募集资金"] = pd.to_numeric(temp_df["募集资金"], errors="coerce")
    temp_df["首发募集资金"] = pd.to_numeric(temp_df["首发募集资金"], errors="coerce")
    temp_df["增发募集资金"] = pd.to_numeric(temp_df["增发募集资金"], errors="coerce")
    temp_df["配股募集资金"] = pd.to_numeric(temp_df["配股募集资金"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    macro_stock_finance_df = macro_stock_finance()
    print(macro_stock_finance_df)
