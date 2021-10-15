# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/10/15 15:49
Desc: 东方财富网-数据中心-公告大全-沪深 A 股公告
http://data.eastmoney.com/notices/hsa/5.html
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_notice_report(
    report_type: str = "财务报告", recent_page: str = "10"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-公告大全-沪深 A 股公告
    http://data.eastmoney.com/notices/hsa/5.html
    :param report_type: 报告类型; choice of {"财务报告", "融资公告", "风险提示", "信息变更", "重大事项", "资产重组", "持股变动"}
    :type report_type: str
    :param recent_page: 返回最近的页数
    :type recent_page: int
    :return: 沪深 A 股公告
    :rtype: pandas.DataFrame
    """
    url = "http://np-anotice-stock.eastmoney.com/api/security/ann"
    report_map = {
        "财务报告": "1",
        "融资公告": "2",
        "风险提示": "3",
        "信息变更": "4",
        "重大事项": "5",
        "资产重组": "6",
        "持股变动": "7",
    }
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(recent_page)+1), leave=False):
        params = {
            "sr": "-1",
            "page_size": "100",
            "page_index": page,
            "ann_type": "A",
            "client_source": "web",
            "f_node": report_map[report_type],
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
    big_df.rename(
        columns={
            "art_code": "_",
            "display_time": "-",
            "eiTime": "-",
            "notice_date": "公告日期",
            "title": "公告标题",
            "column_code": "-",
            "column_name": "公告类型",
            "ann_type": "-",
            "inner_code": "-",
            "market_code": "-",
            "short_name": "名称",
            "stock_code": "代码",
        },
        inplace=True,
    )
    big_df = big_df[
        [
            "代码",
            "名称",
            "公告标题",
            "公告类型",
            "公告日期",
        ]
    ]
    big_df['公告日期'] = pd.to_datetime(big_df['公告日期']).dt.date
    return big_df


if __name__ == "__main__":
    item_list = ["财务报告", "融资公告", "风险提示", "信息变更", "重大事项", "资产重组", "持股变动"]
    for temp_item in item_list:
        stock_notice_report_df = stock_notice_report(report_type=temp_item, recent_page="10")
        print(stock_notice_report_df)
        break
