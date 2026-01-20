#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/12/25 16:46
Desc: 东方财富网-数据中心-新股申购-过会企业信息
https://data.eastmoney.com/xg/gh/default.html
"""

import json

import pandas as pd
import requests

from akshare.utils.cons import headers
from akshare.utils.tqdm import get_tqdm


def stock_ipo_review_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-新股申购-新股上会信息
    https://data.eastmoney.com/xg/gh/default.html
    :return: 新股上会信息
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REVIEW_DATE,ORG_CODE",
        "sortTypes": "-1,-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_IPO_REVIEW",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
    }

    def parse_jsonp(text: str):
        """安全解析 JSONP 响应"""
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError(f"无法找到 JSON 对象: {text[:200]}...")
        json_str = text[start : end + 1]
        return json.loads(json_str)

    # 首次请求获取总页数
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    data_json = parse_jsonp(r.text)

    if "result" not in data_json or "pages" not in data_json["result"]:
        raise ValueError("响应格式异常，未找到 result.pages")

    page_num = data_json["result"]["pages"]
    big_df = pd.DataFrame()

    tqdm = get_tqdm()
    for page in tqdm(range(1, page_num + 1), leave=False):
        params["pageNumber"] = str(page)
        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()
        try:
            data_json = parse_jsonp(r.text)
            temp_df = pd.DataFrame(data_json["result"]["data"])
            big_df = pd.concat([big_df, temp_df], ignore_index=True)
        except Exception as e:
            print(f"第 {page} 页解析失败: {e}")
            continue

    big_df.reset_index(drop=True, inplace=True)
    big_df.insert(0, "序号", big_df.index + 1)

    big_df.rename(
        columns={
            "ORG_NAME": "企业名称",
            "SECURITY_NAME_ABBR": "股票简称",
            "SECURITY_CODE": "股票代码",
            "TRADE_MARKET": "上市板块",
            "REVIEW_DATE": "上会日期",
            "REVIEW_STATE": "审核状态",
            "REVIEW_MEMBER": "发审委委员",
            "LEAD_UNDERWRITER": "主承销商",
            "ISSUE_NUM": "发行数量(股)",
            "FINANCE_AMT_UPPER": "拟融资额(元)",
            "NOTICE_DATE": "公告日期",
            "LISTING_DATE": "上市日期",
        },
        inplace=True,
    )

    big_df = big_df[
        [
            "序号",
            "企业名称",
            "股票简称",
            "股票代码",
            "上市板块",
            "上会日期",
            "审核状态",
            "发审委委员",
            "主承销商",
            "发行数量(股)",
            "拟融资额(元)",
            "公告日期",
            "上市日期",
        ]
    ]

    # 日期处理
    date_cols = ["上会日期", "公告日期", "上市日期"]
    for col in date_cols:
        if col in big_df.columns:
            big_df[col] = pd.to_datetime(big_df[col], errors="coerce").dt.date

    # 数值格式化（可选）
    if "发行数量(股)" in big_df.columns:
        big_df["发行数量(股)"] = pd.to_numeric(big_df["发行数量(股)"], errors="coerce")
    if "拟融资额(元)" in big_df.columns:
        big_df["拟融资额(元)"] = pd.to_numeric(big_df["拟融资额(元)"], errors="coerce")

    return big_df


if __name__ == "__main__":
    stock_ipo_review_em_df = stock_ipo_review_em()
    print(stock_ipo_review_em_df)
