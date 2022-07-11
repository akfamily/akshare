#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/7/1 16:30
Desc: 基金经理大全
http://fund.eastmoney.com/manager/default.html
"""
import pandas as pd
import requests
from tqdm import tqdm

from akshare.utils import demjson


def fund_manager(adjust: str = '0') -> pd.DataFrame:
    """
    天天基金网-基金数据-基金经理大全
    http://fund.eastmoney.com/manager/default.html
    :param adjust: 默认 adjust='0', 返回目标地址相同格式; adjust='1', 返回根据 `现任基金` 打散后的数据
    :type adjust: str
    :return: 基金经理大全
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    url = "http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx"
    params = {
        "dt": "14",
        "mc": "returnjson",
        "ft": "all",
        "pn": "50",
        "pi": "1",
        "sc": "abbname",
        "st": "asc",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text.strip("var returnjson= "))
    total_page = data_json["pages"]
    for page in tqdm(range(1, total_page + 1), leave=False):
        url = "http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx"
        params = {
            "dt": "14",
            "mc": "returnjson",
            "ft": "all",
            "pn": "50",
            "pi": str(page),
            "sc": "abbname",
            "st": "asc",
        }
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text.strip("var returnjson= "))
        temp_df = pd.DataFrame(data_json["data"])

        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    big_df.columns = [
        "序号",
        "_",
        "姓名",
        "_",
        "所属公司",
        "_",
        "现任基金",
        "累计从业时间",
        "现任基金最佳回报",
        "_",
        "_",
        "现任基金资产总规模",
        "_",
    ]
    big_df = big_df[
        [
            "序号",
            "姓名",
            "所属公司",
            "现任基金",
            "累计从业时间",
            "现任基金资产总规模",
            "现任基金最佳回报",
        ]
    ]
    big_df["现任基金最佳回报"] = big_df["现任基金最佳回报"].str.split("%", expand=True).iloc[:, 0]
    big_df["现任基金资产总规模"] = big_df["现任基金资产总规模"].str.split("亿元", expand=True).iloc[:, 0]
    big_df['累计从业时间'] = pd.to_numeric(big_df['累计从业时间'], errors="coerce")
    big_df['现任基金最佳回报'] = pd.to_numeric(big_df['现任基金最佳回报'], errors="coerce")
    big_df['现任基金资产总规模'] = pd.to_numeric(big_df['现任基金资产总规模'], errors="coerce")
    if adjust == '1':
        big_df['现任基金'] = big_df['现任基金'].apply(lambda x: x.split(','))
        big_df = big_df.explode(column='现任基金')
        big_df.reset_index(drop=True, inplace=True)
        return big_df
    return big_df


if __name__ == "__main__":
    fund_manager_df = fund_manager(adjust='0')
    print(fund_manager_df)

    fund_manager_df = fund_manager(adjust='1')
    print(fund_manager_df)
