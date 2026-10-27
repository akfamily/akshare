#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/12/24 16:37
Desc: 东方财富网-数据中心-新股申购-辅导备案信息
https://data.eastmoney.com/xg/ipo/fd.html
"""

import json

import pandas as pd
import requests

from akshare.utils.cons import headers
from akshare.utils.tqdm import get_tqdm


def stock_ipo_tutor_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-新股数据-IPO辅导信息
    https://data.eastmoney.com/xg/ipo/fd.html
    :return: IPO辅导信息
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "RECORD_DATE,TUTOR_OBJECT",
        "sortTypes": "-1,-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_IPO_TUTRECORD",
        "columns": "TUTOR_OBJECT,ORG_CODE,TUTOR_ORG_CODE,TUTOR_ORG,TUTOR_PROCESS_STATE,REPORT_TYPE,"
        "DISPATCH_ORG,REPORT_TITLE,RECORD_DATE",
        "source": "WEB",
        "client": "WEB",
    }

    def parse_jsonp(text: str):
        """安全解析 JSONP 响应"""
        # 找到第一个 { 和最后一个 } 之间的内容
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError(f"无法找到 JSON 对象: {text[:100]}...")
        json_str = text[start : end + 1]
        return json.loads(json_str)

    # 首次请求获取总页数
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()  # 如果请求失败，抛出异常
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
            "TUTOR_OBJECT": "企业名称",
            "TUTOR_ORG": "辅导机构",
            "TUTOR_PROCESS_STATE": "辅导状态",
            "REPORT_TYPE": "报告类型",
            "DISPATCH_ORG": "派出机构",
            "REPORT_TITLE": "报告标题",
            "RECORD_DATE": "备案日期",
        },
        inplace=True,
    )

    big_df = big_df[
        [
            "序号",
            "企业名称",
            "辅导机构",
            "辅导状态",
            "报告类型",
            "派出机构",
            "报告标题",
            "备案日期",
        ]
    ]

    big_df["备案日期"] = pd.to_datetime(big_df["备案日期"], errors="coerce").dt.date

    return big_df


if __name__ == "__main__":
    stock_ipo_tutor_em_df = stock_ipo_tutor_em()
    print(stock_ipo_tutor_em_df)
