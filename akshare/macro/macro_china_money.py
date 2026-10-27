#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/28
Desc: 中国外汇交易中心-利率互换曲线与债券发行
https://www.chinamoney.com.cn/chinese/bkcurvfxhis/?cfgItemType=72&curveType=FR007
"""

import pandas as pd
import requests
from akshare.utils.tqdm import get_tqdm
from akshare.bond.bond_china_money import bond_china_close_return_map


def macro_china_swap_rate(
    start_date: str = "20231101", end_date: str = "20231204"
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
    bond_china_close_return_map()
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "https://www.chinamoney.com.cn/ags/ms/cm-u-bk-shibor/IfccHis"
    params = {
        "cfgItemType": "72",
        "interestRateType": "0",
        "startDate": start_date,
        "endDate": end_date,
        "bidAskType": "",
        "lang": "CN",
        "quoteTime": "全部",
        "pageSize": "5000",
        "pageNum": "1",
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Host": "www.chinamoney.com.cn",
        "Origin": "https://www.chinamoney.com.cn",
        "Pragma": "no-cache",
        "Referer": "https://www.chinamoney.com.cn/chinese/bkcurvfxhis/?cfgItemType=72&curveType=FR007",
        "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/107.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.post(url, data=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.columns = [
        "日期",
        "_",
        "_",
        "时刻",
        "_",
        "_",
        "_",
        "_",
        "_",
        "价格类型",
        "_",
        "曲线名称",
        "_",
        "_",
        "_",
        "_",
        "data",
    ]
    price_df = pd.DataFrame([item for item in temp_df["data"]])
    price_df.columns = [
        "1M",
        "3M",
        "6M",
        "9M",
        "1Y",
        "2Y",
        "3Y",
        "4Y",
        "5Y",
        "7Y",
        "10Y",
    ]
    big_df = pd.concat(objs=[temp_df, price_df], axis=1)
    big_df = big_df[
        [
            "日期",
            "曲线名称",
            "时刻",
            "价格类型",
            "1M",
            "3M",
            "6M",
            "9M",
            "1Y",
            "2Y",
            "3Y",
            "4Y",
            "5Y",
            "7Y",
            "10Y",
        ]
    ]
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
    big_df.sort_values(["日期"], inplace=True, ignore_index=True)
    return big_df


def macro_china_bond_public() -> pd.DataFrame:
    """
    中国-债券信息披露-债券发行
    https://www.chinamoney.com.cn/chinese/xzjfx/
    :return: 债券发行
    :rtype: pandas.DataFrame
    """
    bond_china_close_return_map()
    url = "https://www.chinamoney.com.cn/ags/ms/cm-u-bond-an/bnBondEmit"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/107.0.0.0 Safari/537.36",
    }
    payload = {
        "enty": "",
        "bondType": "",
        "bondNameCode": "",
        "leadUnderwriter": "",
        "pageNo": "1",
        "pageSize": "10",
        "limit": "1",
    }
    r = requests.post(url, data=payload, headers=headers)
    data_json = r.json()
    total_page = int(data_json["data"]["pageTotalSize"]) + 1
    big_df = pd.DataFrame()
    tqdm = get_tqdm()
    for page in tqdm(range(1, total_page), leave=False):
        payload.update({"pageNo": page})
        r = requests.post(url, data=payload, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["records"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
    big_df.columns = [
        "债券全称",
        "债券类型",
        "-",
        "发行日期",
        "-",
        "计息方式",
        "-",
        "债券期限",
        "-",
        "债券评级",
        "-",
        "价格",
        "计划发行量",
    ]
    big_df = big_df[
        [
            "债券全称",
            "债券类型",
            "发行日期",
            "计息方式",
            "价格",
            "债券期限",
            "计划发行量",
            "债券评级",
        ]
    ]
    big_df["价格"] = pd.to_numeric(big_df["价格"], errors="coerce")
    big_df["计划发行量"] = pd.to_numeric(big_df["计划发行量"], errors="coerce")
    return big_df


if __name__ == "__main__":
    macro_china_swap_rate_df = macro_china_swap_rate(
        start_date="20251010", end_date="20251208"
    )
    print(macro_china_swap_rate_df)

    macro_china_bond_public_df = macro_china_bond_public()
    print(macro_china_bond_public_df)
