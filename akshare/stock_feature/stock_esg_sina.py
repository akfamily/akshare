#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/7/6 19:28
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


if __name__ == "__main__":
    stock_esg_rate_sina_df = stock_esg_rate_sina()
    print(stock_esg_rate_sina_df)
