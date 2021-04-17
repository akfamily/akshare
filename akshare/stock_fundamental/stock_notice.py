# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/4/17 14:49
Desc: 东方财富网-数据中心-公告大全-沪深 A 股公告
http://data.eastmoney.com/notices/hsa/5.html
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_notice_report() -> pd.DataFrame:
    """
    东方财富网-数据中心-公告大全-沪深 A 股公告
    :return: 沪深 A 股公告
    :rtype: pandas.DataFrame
    """
    url = "http://np-anotice-stock.eastmoney.com/api/security/ann"
    big_df = pd.DataFrame()
    for page in tqdm(range(1, 100)):
        params = {
            "sr": "-1",
            "page_size": "100",
            "page_index": page,
            "ann_type": "A",
            "client_source": "web",
            "f_node": "0",
            "s_node": "0",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["list"])
        temp_codes_df = pd.DataFrame(
            [item["codes"][0] for item in data_json["data"]["list"]]
        )
        try:
            temp_columns_df = pd.DataFrame(
                [item["columns"][0] for item in data_json["data"]["list"]]
            )
        except:
            continue
        del temp_df["codes"]
        del temp_df["columns"]
        temp_df = pd.concat([temp_df, temp_columns_df, temp_codes_df], axis=1)
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [
        "_",
        "_",
        "公告日期",
        "公告标题",
        "_",
        "公告类型",
        "_",
        "_",
        "名称",
        "代码",
    ]
    big_df = big_df[
        [
            "代码",
            "名称",
            "公告标题",
            "公告类型",
            "公告日期",
        ]
    ]
    return big_df


if __name__ == "__main__":
    stock_notice_report_df = stock_notice_report()
    print(stock_notice_report_df)
