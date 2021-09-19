# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/6/1 14:18
Desc: 东方财富网-数据中心-经济数据-中美国债收益率
http://data.eastmoney.com/cjsj/zmgzsyl.html
"""
import pandas as pd
import requests
from tqdm import tqdm


def bond_zh_us_rate() -> pd.DataFrame:
    """
    东方财富网-数据中心-经济数据-中美国债收益率
    http://data.eastmoney.com/cjsj/zmgzsyl.html
    :return: 中美国债收益率
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter.eastmoney.com/api/data/get"
    params = {
        "type": "RPTA_WEB_TREASURYYIELD",
        "sty": "ALL",
        "st": "SOLAR_DATE",
        "sr": "-1",
        "token": "894050c76af8597a853f5b408b759f5d",
        "p": "1",
        "ps": "500",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1615791534490",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1)):
        params = {
            "type": "RPTA_WEB_TREASURYYIELD",
            "sty": "ALL",
            "st": "SOLAR_DATE",
            "sr": "-1",
            "token": "894050c76af8597a853f5b408b759f5d",
            "p": page,
            "ps": "500",
            "pageNo": page,
            "pageNum": page,
            "_": "1615791534490",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.rename(
        columns={
            "SOLAR_DATE": "日期",
            "EMM00166462": "中国国债收益率5年",
            "EMM00166466": "中国国债收益率10年",
            "EMM00166469": "中国国债收益率30年",
            "EMM00588704": "中国国债收益率2年",
            "EMM01276014": "中国国债收益率10年-2年",
            "EMG00001306": "美国国债收益率2年",
            "EMG00001308": "美国国债收益率5年",
            "EMG00001310": "美国国债收益率10年",
            "EMG00001312": "美国国债收益率30年",
            "EMG01339436": "美国国债收益率10年-2年",
            "EMM00000024": "中国GDP年增率",
            "EMG00159635": "美国GDP年增率",
        },
        inplace=True,
    )
    big_df = big_df[
        [
            "日期",
            "中国国债收益率2年",
            "中国国债收益率5年",
            "中国国债收益率10年",
            "中国国债收益率30年",
            "中国国债收益率10年-2年",
            "中国GDP年增率",
            "美国国债收益率2年",
            "美国国债收益率5年",
            "美国国债收益率10年",
            "美国国债收益率30年",
            "美国国债收益率10年-2年",
            "美国GDP年增率",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    return big_df


if __name__ == "__main__":
    bond_zh_us_rate_df = bond_zh_us_rate()
    print(bond_zh_us_rate_df)
