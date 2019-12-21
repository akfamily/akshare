# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/21 15:22
contact: jindaxiang@163.com
desc: 
"""
import pandas as pd


def macro_cnbs():
    url = "http://114.115.232.154:8080/handler/download.ashx"
    excel_data = pd.read_excel(url, sheet_name="Data", header=0, skiprows=1)
    excel_data["Period"] = pd.to_datetime(excel_data["Period"]).dt.strftime("%Y-%m")
    excel_data.columns = [
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
    return excel_data
    # data_info = pd.read_excel(url, sheet_name="Contents", header=0, skiprows=4)
    # data_info.iloc[:, 2]


if __name__ == '__main__':
    cnbs_df = macro_cnbs()
    print(cnbs_df)
