#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/1/20 15:00
Desc: 上海证券交易所-ETF基金份额数据
https://www.sse.com.cn/assortment/fund/etf/list/scale/
"""

import pandas as pd
import requests


def fund_etf_scale_sse(date: str = "20250115") -> pd.DataFrame:
    """
    上海证券交易所-产品-基金产品-ETF产品-ETF产品列表-基金规模
    https://www.sse.com.cn/assortment/fund/etf/list/scale/
    :param date: 统计日期, 默认为空返回最新数据, 格式如 "20250115"
    :type date: str
    :return: ETF基金份额数据
    :rtype: pandas.DataFrame
    """
    data_str = "-".join([date[:4], date[4:6], date[6:]])
    url = "https://query.sse.com.cn/commonQuery.do"
    params = {
        "isPagination": "true",
        "pageHelp.pageSize": "10000",
        "pageHelp.pageNo": "1",
        "pageHelp.beginPage": "1",
        "pageHelp.cacheSize": "1",
        "pageHelp.endPage": "1",
        "sqlId": "COMMON_SSE_ZQPZ_ETFZL_XXPL_ETFGM_SEARCH_L",
        "STAT_DATE": data_str,
    }
    headers = {
        "Referer": "https://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/88.0.4324.150 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"])
    temp_df.rename(
        columns={
            "NUM": "序号",
            "SEC_CODE": "基金代码",
            "SEC_NAME": "基金简称",
            "ETF_TYPE": "ETF类型",
            "STAT_DATE": "统计日期",
            "TOT_VOL": "基金份额",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "序号",
            "基金代码",
            "基金简称",
            "ETF类型",
            "统计日期",
            "基金份额",
        ]
    ]
    temp_df["序号"] = pd.to_numeric(temp_df["序号"], errors="coerce")
    temp_df["统计日期"] = pd.to_datetime(temp_df["统计日期"], errors="coerce").dt.date
    temp_df["基金份额"] = pd.to_numeric(temp_df["基金份额"], errors="coerce") * 10000
    return temp_df


if __name__ == "__main__":
    fund_etf_scale_sse_df = fund_etf_scale_sse(date="20250115")
    print(fund_etf_scale_sse_df)
