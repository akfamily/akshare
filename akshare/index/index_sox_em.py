#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/14 20:00
Desc: 东方财富-数据中心-经济数据-费城半导体指数
https://data.eastmoney.com/cjsj/hyzs_list_EMI00055562.html
"""

import pandas as pd
from akshare.utils import http
from akshare.utils.tqdm import get_tqdm


def index_us_sox_em() -> pd.DataFrame:
    """
    费城半导体指数
    https://data.eastmoney.com/cjsj/hyzs_list_EMI00055562.html
    :return: 费城半导体指数
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,"
        "CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00055562")',
        "source": "WEB",
        "client": "WEB",
    }
    r = http.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    tqdm = get_tqdm()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = http.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df = big_df.drop_duplicates()
    big_df = big_df.rename(
        columns={
            "REPORT_DATE": "日期",
            "INDICATOR_VALUE": "最新值",
            "CHANGE_RATE": "涨跌幅",
            "CHANGERATE_3M": "近3月涨跌幅",
            "CHANGERATE_6M": "近6月涨跌幅",
            "CHANGERATE_1Y": "近1年涨跌幅",
            "CHANGERATE_2Y": "近2年涨跌幅",
            "CHANGERATE_3Y": "近3年涨跌幅",
        }
    )
    big_df = big_df[
        [
            "日期",
            "最新值",
            "涨跌幅",
            "近3月涨跌幅",
            "近6月涨跌幅",
            "近1年涨跌幅",
            "近2年涨跌幅",
            "近3年涨跌幅",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df = big_df.sort_values(["日期"])
    big_df = big_df.reset_index(drop=True)
    return big_df


if __name__ == "__main__":
    index_us_sox_em_df = index_us_sox_em()
    print(index_us_sox_em_df)
