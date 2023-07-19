#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/7/7 19:28
Desc: 新浪财经-ESG评级中心
https://finance.sina.com.cn/esg/
"""
import math

import pandas as pd
import requests
from tqdm import tqdm


def stock_esg_rate_sina() -> pd.DataFrame:
    """
    新浪财经-ESG评级中心-ESG评级-ESG评级数据
    https://finance.sina.com.cn/esg/grade.shtml
    :return: ESG评级数据
    :rtype: pandas.DataFrame
    """
    url = "https://global.finance.sina.com.cn/api/openapi.php/EsgService.getEsgStocks?page=1&num=200"
    r = requests.get(url)
    data_json = r.json()
    page_num = math.ceil(data_json["result"]["data"]["info"]["total"] / 200)
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1), leave=False):
        url = f"https://global.finance.sina.com.cn/api/openapi.php/EsgService.getEsgStocks?page={page}&num=200"
        r = requests.get(url)
        data_json = r.json()
        stock_num = len(data_json["result"]["data"]["info"]["stocks"])
        for num in range(stock_num):
            temp_df = pd.DataFrame(
                data_json["result"]["data"]["info"]["stocks"][num]["esg_info"]
            )
            temp_df["symbol"] = data_json["result"]["data"]["info"]["stocks"][num][
                "symbol"
            ]
            temp_df["market"] = data_json["result"]["data"]["info"]["stocks"][num][
                "market"
            ]
            big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.rename(
        columns={
            "symbol": "成分股代码",
            "agency_name": "评级机构",
            "esg_score": "评级",
            "esg_dt": "评级季度",
            "remark": "标识",
            "market": "交易市场",
        },
        inplace=True,
    )
    big_df = big_df[
        [
            "成分股代码",
            "评级机构",
            "评级",
            "评级季度",
            "标识",
            "交易市场",
        ]
    ]
    return big_df


def stock_esg_hz_sina() -> pd.DataFrame:
    """
    新浪财经-ESG评级中心-ESG评级-华证指数
    https://finance.sina.com.cn/esg/grade.shtml
    :return: 华证指数
    :rtype: pandas.DataFrame
    """
    url = "https://global.finance.sina.com.cn/api/openapi.php/EsgService.getHzEsgStocks?p=1&num=20000"
    r = requests.get(url)
    data_json = r.json()
    big_df = pd.DataFrame(data_json["result"]["data"]["data"])
    big_df.rename(
        columns={
            "date": "日期",
            "symbol": "股票代码",
            "market": "交易市场",
            "name": "股票名称",
            "esg_score": "ESG评分",
            "esg_score_grade": "ESG等级",
            "e_score": "环境",
            "e_score_grade": "环境等级",
            "s_score": "社会",
            "s_score_grade": "社会等级",
            "g_score": "公司治理",
            "g_score_grade": "公司治理等级",
        },
        inplace=True,
    )
    big_df = big_df[
        [
            "日期",
            "股票代码",
            "交易市场",
            "股票名称",
            "ESG评分",
            "ESG等级",
            "环境",
            "环境等级",
            "社会",
            "社会等级",
            "公司治理",
            "公司治理等级",
        ]
    ]
    big_df['日期'] = pd.to_datetime(big_df['日期'], errors="coerce").dt.date
    big_df['ESG评分'] = pd.to_numeric(big_df['ESG评分'], errors="coerce")
    big_df['环境'] = pd.to_numeric(big_df['环境'], errors="coerce")
    big_df['社会'] = pd.to_numeric(big_df['社会'], errors="coerce")
    big_df['公司治理'] = pd.to_numeric(big_df['公司治理'], errors="coerce")
    return big_df


if __name__ == "__main__":
    stock_esg_rate_sina_df = stock_esg_rate_sina()
    print(stock_esg_rate_sina_df)

    stock_esg_hz_sina_df = stock_esg_hz_sina()
    print(stock_esg_hz_sina_df)
