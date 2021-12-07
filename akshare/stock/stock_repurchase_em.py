# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/12/2 15:48
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
        "type": "RPTA_WEB_GETHGLIST",
        "sty": "ALL",
        "source": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(total_page) + 1)):
        params.update({"p": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.rename(
        {
            "dim_scode": "股票代码",
            "securityshortname": "股票简称",
            "newprice": "最新价",
            "jhjg_vag": "计划回购价格区间",
            "jhsl_vag": "计划回购数量区间-平均",
            "zjszbl": "占公告前一日总股本比例-平均",
            "jhje_vag": "计划回购金额区间",
            "repurstartdate": "回购起始时间",
            "repurprogress": "实施进度",
            "hgjg_vag": "已回购股份价格区间-平均",
            "repurnum": "已回购股份数量",
            "repuramount": "已回购金额",
            "upd": "最新公告日期",
            "repurnumlower": "计划回购数量区间-下限",
            "repurnumcap": "计划回购数量区间-上限",
            "zszxx": "占公告前一日总股本比例-下限",
            "zszsx": "占公告前一日总股本比例-上限",
            "zdj": "已回购股份价格区间-下限",
            "zgj": "已回购股份价格区间-上限",
        },
        axis="columns",
        inplace=True,
    )
    big_df = big_df[
        [
            "股票代码",
            "股票简称",
            "最新价",
            "计划回购价格区间",
            "计划回购数量区间-下限",
            "计划回购数量区间-平均",
            "计划回购数量区间-上限",
            "占公告前一日总股本比例-下限",
            "占公告前一日总股本比例-平均",
            "占公告前一日总股本比例-上限",
            "计划回购金额区间",
            "回购起始时间",
            "实施进度",
            "已回购股份价格区间-下限",
            "已回购股份价格区间-平均",
            "已回购股份价格区间-上限",
            "已回购股份数量",
            "已回购金额",
            "最新公告日期",
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
