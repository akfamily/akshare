#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/8/20 20:00
Desc: 东方财富网-数据中心-研究报告-个股研报
https://data.eastmoney.com/report/stock.jshtml
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_research_report_em(symbol: str = "000001") -> pd.DataFrame:
    """
    东方财富网-数据中心-研究报告-个股研报
    https://data.eastmoney.com/report/stock.jshtml
    :return: 个股研报
    :rtype: pandas.DataFrame
    """
    url = "https://reportapi.eastmoney.com/report/list"
    params = {
        "industryCode": "*",
        "pageSize": "5000",
        "industry": "*",
        "rating": "*",
        "ratingChange": "*",
        "beginTime": "2000-01-01",
        "endTime": "2025-01-01",
        "pageNo": "1",
        "fields": "",
        "qType": "0",
        "orgCode": "",
        "code": symbol,
        "rcode": "",
        "p": "1",
        "pageNum": "1",
        "pageNumber": "1",
        "_": "1692533168153",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["TotalPage"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update(
            {
                "pageNo": page,
                "p": page,
                "pageNum": page,
                "pageNumber": page,
            }
        )
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"])
        big_df = pd.concat([big_df, temp_df], axis=0, ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df["index"] = big_df["index"] + 1
    big_df.rename(
        columns={
            "index": "序号",
            "title": "报告名称",
            "stockName": "股票简称",
            "stockCode": "股票代码",
            "orgCode": "-",
            "orgName": "-",
            "orgSName": "机构",
            "publishDate": "日期",
            "infoCode": "-",
            "column": "-",
            "predictNextTwoYearEps": "-",
            "predictNextTwoYearPe": "-",
            "predictNextYearEps": "2024-盈利预测-收益",
            "predictNextYearPe": "2024-盈利预测-市盈率",
            "predictThisYearEps": "2023-盈利预测-收益",
            "predictThisYearPe": "2023-盈利预测-市盈率",
            "predictLastYearEps": "-",
            "predictLastYearPe": "-",
            "actualLastTwoYearEps": "-",
            "actualLastYearEps": "-",
            "industryCode": "-",
            "industryName": "-",
            "emIndustryCode": "-",
            "indvInduCode": "-",
            "indvInduName": "行业",
            "emRatingCode": "-",
            "emRatingValue": "-",
            "emRatingName": "东财评级",
            "lastEmRatingCode": "-",
            "lastEmRatingValue": "-",
            "lastEmRatingName": "-",
            "ratingChange": "-",
            "reportType": "-",
            "author": "-",
            "indvIsNew": "-",
            "researcher": "-",
            "newListingDate": "-",
            "newPurchaseDate": "-",
            "newIssuePrice": "-",
            "newPeIssueA": "-",
            "indvAimPriceT": "-",
            "indvAimPriceL": "-",
            "attachType": "-",
            "attachSize": "-",
            "attachPages": "-",
            "encodeUrl": "-",
            "sRatingName": "-",
            "sRatingCode": "-",
            "market": "-",
            "authorID": "-",
            "count": "近一月个股研报数",
            "orgType": "-",
        },
        inplace=True,
    )
    big_df = big_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "报告名称",
            "东财评级",
            "机构",
            "近一月个股研报数",
            "2023-盈利预测-收益",
            "2023-盈利预测-市盈率",
            "2024-盈利预测-收益",
            "2024-盈利预测-市盈率",
            "行业",
            "日期",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"], errors="coerce").dt.date
    big_df["近一月个股研报数"] = pd.to_numeric(big_df["近一月个股研报数"], errors="coerce")
    big_df["2023-盈利预测-收益"] = pd.to_numeric(big_df["2023-盈利预测-收益"], errors="coerce")
    big_df["2023-盈利预测-市盈率"] = pd.to_numeric(big_df["2023-盈利预测-市盈率"], errors="coerce")
    big_df["2024-盈利预测-收益"] = pd.to_numeric(big_df["2024-盈利预测-收益"], errors="coerce")
    big_df["2024-盈利预测-市盈率"] = pd.to_numeric(big_df["2024-盈利预测-市盈率"], errors="coerce")
    return big_df


if __name__ == "__main__":
    stock_research_report_em_df = stock_research_report_em(symbol="000001")
    print(stock_research_report_em_df)
