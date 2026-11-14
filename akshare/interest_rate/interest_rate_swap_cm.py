#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/14 20:00
Desc: 中国外汇交易中心-FR007 利率互换曲线历史数据
https://www.chinamoney.com.cn/chinese/bkcurvfxhis/?cfgItemType=72&curveType=FR007
"""

import pandas as pd

from akshare.exceptions import APIError
from akshare.utils import http


def interest_rate_swap_cm(
    start_date: str = "20261101", end_date: str = "20261113"
) -> pd.DataFrame:
    """
    FR007 利率互换曲线历史数据；只能获取近一年的数据
    https://www.chinamoney.com.cn/chinese/bkcurvfxhis/?cfgItemType=72&curveType=FR007
    :param start_date: 开始日期，开始和结束日期不得超过一个月
    :type start_date: str
    :param end_date: 结束日期，开始和结束日期不得超过一个月
    :type end_date: str
    :return: FR007利率互换曲线历史数据
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "https://www.chinamoney.com.cn/ags/ms/cm-u-bk-shibor/IfccHis"
    # 上游不再接受 quoteTime="全部"（返回服务端异常），收盘曲线对应 16:30
    payload = {
        "cfgItemType": "72",
        "interestRateType": "0",
        "startDate": start_date,
        "endDate": end_date,
        "bidAskType": "",
        "lang": "CN",
        "quoteTime": "16:30",
        "pageSize": "5000",
        "pageNum": "1",
    }
    headers = {
        "Referer": "https://www.chinamoney.com.cn/chinese/bkcurvfxhis/?cfgItemType=72&curveType=FR007",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = http.post(url, data=payload, headers=headers)
    data_json = r.json()
    if data_json["head"]["rep_code"] != "200":
        raise APIError(
            f"中国外汇交易中心返回错误：{data_json['head']['rep_message']}，"
            "请检查日期范围，开始和结束日期不得超过一个月且只能查询近一年"
        )
    terms = data_json["data"]["bigthRowName"]
    columns = ["日期", "曲线名称", "时刻", "价格类型", *terms]
    if not data_json["records"]:
        return pd.DataFrame(columns=columns)
    temp_df = pd.DataFrame(data_json["records"]).rename(
        columns={
            "date": "日期",
            "bigthName": "曲线名称",
            "quoteTime": "时刻",
            "askBid": "价格类型",
        }
    )
    price_df = pd.DataFrame(temp_df["configPrice"].tolist(), columns=terms)
    big_df = pd.concat(objs=[temp_df, price_df], axis=1)[columns]
    big_df["日期"] = pd.to_datetime(big_df["日期"], errors="coerce").dt.date
    big_df["1M"] = pd.to_numeric(big_df["1M"], errors="coerce")
    big_df["3M"] = pd.to_numeric(big_df["3M"], errors="coerce")
    big_df["6M"] = pd.to_numeric(big_df["6M"], errors="coerce")
    big_df["9M"] = pd.to_numeric(big_df["9M"], errors="coerce")
    big_df["1Y"] = pd.to_numeric(big_df["1Y"], errors="coerce")
    big_df["2Y"] = pd.to_numeric(big_df["2Y"], errors="coerce")
    big_df["3Y"] = pd.to_numeric(big_df["3Y"], errors="coerce")
    big_df["4Y"] = pd.to_numeric(big_df["4Y"], errors="coerce")
    big_df["5Y"] = pd.to_numeric(big_df["5Y"], errors="coerce")
    big_df["7Y"] = pd.to_numeric(big_df["7Y"], errors="coerce")
    big_df["10Y"] = pd.to_numeric(big_df["10Y"], errors="coerce")
    big_df = big_df.sort_values(["日期"], ignore_index=True)
    return big_df


if __name__ == "__main__":
    interest_rate_swap_cm_df = interest_rate_swap_cm()
    print(interest_rate_swap_cm_df)
