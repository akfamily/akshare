# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/5/10 17:30
Desc: 东方财富网-数据中心-股票回购-股票回购数据
https://data.eastmoney.com/gphg/hglist.html
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_repurchase_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-股票回购-股票回购数据
    https://data.eastmoney.com/gphg/hglist.html
    :return: 股票回购数据
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/get"
    params = {
        "st": "dim_scode",
        "sr": "-1",
        "ps": "500",
        "p": "1",
        # "type": "RPTA_WEB_GETHGLIST",
        "type": "RPTA_WEB_GETHGLIST_NEW",
        "sty": "ALL",
        "source": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(total_page) + 1), leave=False):
        params.update({"p": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.rename(
        {
            "DIM_SCODE": "股票代码",
            "SECURITYSHORTNAME": "股票简称",
            "NEWPRICE": "最新价",
            "JHJG_VAG": "计划回购价格区间(元)",
            "JHSL_VAG": "计划回购数量区间(股)",
            "ZJSZBL": "占公告前一日总股本比例(%)",
            "JHJE_VAG": "计划回购金额区间(元)",
            "REPURSTARTDATE": "回购起始时间",
            "REPURPROGRESS": "实施进度",
            "HGJG_VAG": "已回购股份价格区间(元)",
            "REPURNUM": "已回购股份数量(股)",
            "REPURAMOUNT": "已回购金额(元)",
            "UPD": "最新公告日期"
        },
        axis="columns",
        inplace=True,
    )
    big_df = big_df[
        [
            "股票代码",
            "股票简称",
            "最新价",
            "计划回购价格区间(元)",
            "计划回购数量区间(股)",
            "占公告前一日总股本比例(%)",
            "计划回购金额区间(元)",
            "回购起始时间",
            "实施进度",
            "已回购股份价格区间(元)",
            "已回购股份数量(股)",
            "已回购金额(元)",
            "最新公告日期"
        ]
    ]
    big_df.reset_index(inplace=True)
    big_df.rename(
        {
            "index": "序号",
        },
        axis="columns",
        inplace=True,
    )
    big_df["序号"] = big_df.index + 1
    process_map = {
        "001": "董事会预案",
        "002": "股东大会通过",
        "003": "股东大会否决",
        "004": "实施中",
        "005": "停止实施",
        "006": "完成实施",
    }
    big_df["实施进度"] = big_df["实施进度"].map(process_map)
    big_df["回购起始时间"] = pd.to_datetime(big_df["回购起始时间"]).dt.date
    big_df["最新公告日期"] = pd.to_datetime(big_df["最新公告日期"]).dt.date
    return big_df


if __name__ == "__main__":
    stock_repurchase_em_df = stock_repurchase_em()
    print(stock_repurchase_em_df)
