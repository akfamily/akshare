#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/12/24 16:20
Desc: 东方财富网-数据中心-新股申购-首发申报信息-首发申报企业信息
https://data.eastmoney.com/xg/xg/sbqy.html
"""

import pandas as pd
import requests

from akshare.utils.cons import headers
from akshare.utils.tqdm import get_tqdm


def stock_ipo_declare_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-新股数据-首发申报企业信息
    https://data.eastmoney.com/xg/xg/sbqy.html
    :return: 首发申报企业信息
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "END_DATE,SECURITY_CODE",
        "sortTypes": "-1,-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_IPO_DECORGNEWEST",
        "columns": "DECLARE_ORG,STATE,REG_ADDRESS,RECOMMEND_ORG,LAW_FIRM,ACCOUNT_FIRM,IS_SUBMIT,"
        "PREDICT_LISTING_MARKET,END_DATE,INFO_CODE,SECURITY_CODE,ORG_CODE,IS_REGISTER,"
        "STATE_CODE,DERIVE_SECURITY_CODE,ORG_CODE_OLD,IS_STATE",
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    page_num = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    tqdm = get_tqdm()
    for page in tqdm(range(1, page_num + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1

    big_df.rename(
        columns={
            "index": "序号",
            "DECLARE_ORG": "企业名称",
            "STATE": "最新状态",
            "REG_ADDRESS": "注册地",
            "RECOMMEND_ORG": "保荐机构",
            "LAW_FIRM": "律师事务所",
            "ACCOUNT_FIRM": "会计师事务所",
            "PREDICT_LISTING_MARKET": "拟上市地点",
            "END_DATE": "更新日期",
            "INFO_CODE": "招股说明书",
        },
        inplace=True,
    )

    # 招股说明书链接处理（类似原有代码）
    if "招股说明书" in big_df.columns:
        big_df["招股说明书"] = [
            f"https://pdf.dfcfw.com/pdf/H2_{item}_1.pdf" if pd.notna(item) else ""
            for item in big_df["招股说明书"]
        ]

    big_df = big_df[
        [
            "序号",
            "企业名称",
            "最新状态",
            "注册地",
            "保荐机构",
            "律师事务所",
            "会计师事务所",
            "拟上市地点",
            "更新日期",
            # 可根据需要添加其他列，如 "IS_REGISTER" 等
            "招股说明书",
        ]
    ]

    # 日期处理
    big_df["更新日期"] = pd.to_datetime(
        big_df["更新日期"], errors="coerce", utc=True
    ).dt.date
    return big_df


if __name__ == "__main__":
    stock_ipo_declare_em_df = stock_ipo_declare_em()
    print(stock_ipo_declare_em_df)
