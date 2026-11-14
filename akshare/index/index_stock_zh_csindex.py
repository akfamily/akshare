# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2024/12/23 17:00
Desc: 中证指数-所有指数-历史行情数据
https://www.csindex.com.cn/zh-CN/indices/index-detail/H30374#/indices/family/list?index_series=1
"""

import pandas as pd

from akshare.utils import http


def index_hist_csindex(
    symbol: str = "000928",
    start_date: str = "20180526",
    end_date: str = "20261111",
) -> pd.DataFrame:
    """
    中证指数-具体指数-历史行情数据
    P.S. 只有收盘价，正常情况下不应使用该接口，除非指数只有中证网站有
    https://www.csindex.com.cn/zh-CN/indices/index-detail/H30374#/indices/family/detail?indexCode=H30374
    :param symbol: 指数代码；e.g., H30374
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 包含日期和收盘价的指数数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.csindex.com.cn/csindex-home/perf/index-perf"
    params = {
        "indexCode": symbol,
        "startDate": start_date,
        "endDate": end_date,
    }
    r = http.get(url, params=params)
    data_json = r.json()
    columns = {
        "tradeDate": "日期",
        "indexCode": "指数代码",
        "indexNameCnAll": "指数中文全称",
        "indexNameCn": "指数中文简称",
        "indexNameEnAll": "指数英文全称",
        "indexNameEn": "指数英文简称",
        "open": "开盘",
        "high": "最高",
        "low": "最低",
        "close": "收盘",
        "change": "涨跌",
        "changePct": "涨跌幅",
        "tradingVol": "成交量",
        "tradingValue": "成交金额",
        "consNumber": "样本数量",
        "peg": "滚动市盈率",
    }
    if not data_json["data"]:
        # 查询区间内没有数据：非交易日，或中证指数网站尚未发布（通常滞后一到两个交易日）
        return pd.DataFrame(columns=list(columns.values()))
    temp_df = pd.DataFrame(data_json["data"]).rename(columns=columns)
    temp_df = temp_df[list(columns.values())]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
    temp_df["涨跌"] = pd.to_numeric(temp_df["涨跌"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交金额"] = pd.to_numeric(temp_df["成交金额"], errors="coerce")
    temp_df["样本数量"] = pd.to_numeric(temp_df["样本数量"], errors="coerce")
    temp_df["滚动市盈率"] = pd.to_numeric(temp_df["滚动市盈率"], errors="coerce")
    return temp_df


def index_value_csindex(symbol: str = "H30374") -> pd.DataFrame:
    """
    中证指数-指数估值数据
    https://www.csindex.com.cn/zh-CN/indices/index-detail/H30374#/indices/family/detail?indexCode=H30374
    :param symbol: 指数代码；e.g., H30374
    :type symbol: str
    :return: 指数估值数据
    :rtype: pandas.DataFrame
    """
    url = (
        f"https://oss-ch.csindex.com.cn/static/"
        f"html/csindex/public/uploads/file/autofile/indicator/{symbol}indicator.xls"
    )
    temp_df = pd.read_excel(http.get_buffer(url))
    temp_df.columns = [
        "日期",
        "指数代码",
        "指数中文全称",
        "指数中文简称",
        "指数英文全称",
        "指数英文简称",
        "市盈率1",
        "市盈率2",
        "股息率1",
        "股息率2",
    ]
    temp_df["日期"] = pd.to_datetime(
        temp_df["日期"], format="%Y%m%d", errors="coerce"
    ).dt.date
    temp_df["市盈率1"] = pd.to_numeric(temp_df["市盈率1"], errors="coerce")
    temp_df["市盈率2"] = pd.to_numeric(temp_df["市盈率2"], errors="coerce")
    temp_df["股息率1"] = pd.to_numeric(temp_df["股息率1"], errors="coerce")
    temp_df["股息率2"] = pd.to_numeric(temp_df["股息率2"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    index_hist_csindex_df = index_hist_csindex(
        symbol="000928", start_date="20100101", end_date="20240604"
    )
    print(index_hist_csindex_df)

    index_value_csindex_df = index_value_csindex(symbol="H30374")
    print(index_value_csindex_df)
