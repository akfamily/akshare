#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/8/4 14:00
Desc: 中证指数网站-指数列表
网站：https://www.csindex.com.cn/#/indices/family/list?index_series=1
"""
import warnings
from io import BytesIO

import pandas as pd
import requests


def index_csindex_all() -> pd.DataFrame:
    """
    中证指数网站-指数列表
    https://www.csindex.com.cn/#/indices/family/list?index_series=1
    Note: 但是不知道数据更新时间
    :return: 最新指数的列表,
    :rtype: pandas.DataFrame
    """
    warnings.filterwarnings("ignore", category=UserWarning, message="Workbook contains no default style")
    url = (
        f"https://www.csindex.com.cn/csindex-home/exportExcel/indexAll/CH"
    )

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
    }
    playloads = {
        "sorter": {
            "sortField": "null",
            "sortOrder": None
        },
        "pager": {
            "pageNum": 1,
            "pageSize": 10
        },
        "indexFilter": {
            "ifCustomized": None,
            "ifTracked": None,
            "ifWeightCapped": None,
            "indexCompliance": None,
            "hotSpot": None,
            "indexClassify": None,
            "currency": None,
            "region": None,
            "indexSeries": ["1"],
            "undefined": None
        }
    }
    r = requests.post(url, json=playloads, headers=headers)

    temp_df = pd.read_excel(BytesIO(r.content))
    temp_df["基日"] = pd.to_datetime(
        temp_df["基日"], format="%Y-%m-%d", errors="coerce"
    ).dt.date
    temp_df["发布时间"] = pd.to_datetime(
        temp_df["发布时间"], format="%Y-%m-%d", errors="coerce"
    ).dt.date
    temp_df["指数代码"] = temp_df["指数代码"].astype(str).str.zfill(6)
    return temp_df


if __name__ == "__main__":
    index_csindex_all_df = index_csindex_all()
    print(index_csindex_all_df)
