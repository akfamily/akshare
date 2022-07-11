#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/2/9 12:22
Desc: 国家金融与发展实验室-中国宏观杠杆率数据
http://114.115.232.154:8080/
"""
import pandas as pd


def macro_cnbs() -> pd.DataFrame:
    """
    国家金融与发展实验室-中国宏观杠杆率数据
    http://114.115.232.154:8080/
    :return: 中国宏观杠杆率数据
    :rtype: pandas.DataFrame
    """
    url = "http://114.115.232.154:8080/handler/download.ashx"
    temp_df = pd.read_excel(
        url, sheet_name="Data", header=0, skiprows=1, engine="openpyxl"
    )
    temp_df["Period"] = pd.to_datetime(temp_df["Period"]).dt.strftime("%Y-%m")
    temp_df.dropna(axis=1, inplace=True)
    temp_df.columns = [
        "年份",
        "居民部门",
        "非金融企业部门",
        "政府部门",
        "中央政府",
        "地方政府",
        "实体经济部门",
        "金融部门资产方",
        "金融部门负债方",
    ]

    temp_df["居民部门"] = pd.to_numeric(temp_df["居民部门"])
    temp_df["非金融企业部门"] = pd.to_numeric(temp_df["非金融企业部门"])
    temp_df["政府部门"] = pd.to_numeric(temp_df["政府部门"])
    temp_df["中央政府"] = pd.to_numeric(temp_df["中央政府"])
    temp_df["地方政府"] = pd.to_numeric(temp_df["地方政府"])
    temp_df["实体经济部门"] = pd.to_numeric(temp_df["实体经济部门"])
    temp_df["金融部门资产方"] = pd.to_numeric(temp_df["金融部门资产方"])
    temp_df["金融部门负债方"] = pd.to_numeric(temp_df["金融部门负债方"])

    return temp_df


if __name__ == "__main__":
    macro_cnbs_df = macro_cnbs()
    print(macro_cnbs_df)
