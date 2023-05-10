#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/5/10 16:11
Desc: 问财-热门股票排名
https://www.iwencai.com/unifiedwap/home/index
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_hot_rank_wc(date: str = "20230316") -> pd.DataFrame:
    """
    问财-热门股票排名
    https://www.iwencai.com/unifiedwap/result?w=%E7%83%AD%E9%97%A85000%E8%82%A1%E7%A5%A8&querytype=stock&issugs&sign=1620126514335
    :param date: 查询日期
    :type date: str
    :return: 热门股票排名
    :rtype: pandas.DataFrame
    """
    url = "https://www.iwencai.com/gateway/urp/v7/landing/getDataList"
    params = {
        "query": f"{date}热门5000股票",
        "page": "1",
        "perpage": "100",
        "comp_id": "6734520",
        "uuid": "24087",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    big_df = pd.DataFrame()
    for page in tqdm(range(1, 51), leave=False):
        params.update(
            {
                "page": page,
            }
        )
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["answer"]["components"][0]["data"]["datas"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    try:
        rank_date_str = big_df.columns[1].split("[")[1].strip("]")
    except:
        try:
            rank_date_str = big_df.columns[2].split("[")[1].strip("]")
        except:
            rank_date_str = date
    big_df.rename(
        columns={
            "index": "序号",
            f"个股热度排名[{rank_date_str}]": "个股热度排名",
            f"个股热度[{rank_date_str}]": "个股热度",
            "code": "股票代码",
            "market_code": "_",
            "最新涨跌幅": "涨跌幅",
            "最新价": "现价",
            "股票代码": "_",
        },
        inplace=True,
    )
    big_df = big_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "现价",
            "涨跌幅",
            "个股热度",
            "个股热度排名",
        ]
    ]
    big_df["涨跌幅"] = big_df["涨跌幅"].astype(float).round(2)
    big_df["排名日期"] = rank_date_str
    big_df["现价"] = pd.to_numeric(big_df["现价"], errors="coerce")
    return big_df


if __name__ == "__main__":
    stock_hot_rank_wc_df = stock_hot_rank_wc(date="20230510")
    print(stock_hot_rank_wc_df)
