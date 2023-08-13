#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/8/13 01:23
Desc: 申万宏源研究-行业分类
https://www.swhyresearch.com/institute_sw/allIndex/downloadCenter/industryType
"""

import pandas as pd
import requests
from datetime import datetime
import io

def sw_stock_industry_classification_hist() -> pd.DataFrame:
    """
    申万宏源研究-行业分类-全部行业分类下载
    "https://www.swsresearch.com/swindex/pdf/SwClass2021/StockClassifyUse_stock.xls"
    :return: 个股行业分类变动历史
    :rtype: pandas.DataFrame
    """
    url = "https://www.swsresearch.com/swindex/pdf/SwClass2021/StockClassifyUse_stock.xls"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    temp_df = pd.read_excel(
        io.BytesIO(r.content), dtype={"股票代码": "str", "行业代码": "str"}
    )
    df = temp_df.rename(
        columns={
            "股票代码": "Symbol",
            "计入日期": "StartDate",
            "行业代码": "IndCode",
            "更新日期": "UpdateTime",
        }
    )
    df["StartDate"] = df["StartDate"].apply(lambda x: datetime.strftime(x.date(), "%Y-%m-%d"))
    df["UpdateTime"] = df["UpdateTime"].apply(lambda x: datetime.strftime(x.date(), "%Y-%m-%d"))
    return df


if __name__ == "__main__":
    sw_stock_industry_classification_hist_df = (
        sw_stock_industry_classification_hist()
    )
    print(sw_stock_industry_classification_hist_df)
