#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/8/14 16:20
Desc: 申万宏源研究-行业分类
https://www.swhyresearch.com/institute_sw/allIndex/downloadCenter/industryType
"""
import io
from datetime import datetime

import pandas as pd
import requests


def stock_industry_clf_hist_sw() -> pd.DataFrame:
    """
    申万宏源研究-行业分类-全部行业分类
    https://www.swsresearch.com/swindex/pdf/SwClass2021/StockClassifyUse_stock.xls
    :return: 个股行业分类变动历史
    :rtype: pandas.DataFrame
    """
    url = (
        "https://www.swsresearch.com/swindex/pdf/SwClass2021/StockClassifyUse_stock.xls"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    temp_df = pd.read_excel(io.BytesIO(r.content), dtype={"股票代码": "str", "行业代码": "str"})
    temp_df.rename(
        columns={
            "股票代码": "symbol",
            "计入日期": "start_date",
            "行业代码": "industry_code",
            "更新日期": "update_time",
        },
        inplace=True,
    )
    temp_df["start_date"] = pd.to_datetime(
        temp_df["start_date"], errors="coerce"
    ).dt.date
    temp_df["update_time"] = pd.to_datetime(
        temp_df["update_time"], errors="coerce"
    ).dt.date
    return temp_df


if __name__ == "__main__":
    stock_industry_clf_hist_sw_df = stock_industry_clf_hist_sw()
    print(stock_industry_clf_hist_sw_df)
