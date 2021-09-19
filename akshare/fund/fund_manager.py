# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/7/1 16:30
Desc: 基金经理大全
http://fund.eastmoney.com/manager/default.html
"""
from akshare.utils import demjson
import pandas as pd
import requests
from tqdm import tqdm


def fund_manager(explode: bool = False) -> pd.DataFrame:
    """
    天天基金网-基金数据-基金经理大全
    http://fund.eastmoney.com/manager/default.html
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
        temp_df.reset_index(inplace=True)
        temp_df["index"] = range(1, len(temp_df) + 1)
        temp_df.columns = [
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
        temp_df = temp_df[
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
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df["现任基金最佳回报"] = big_df["现任基金最佳回报"].str.split("%", expand=True).iloc[:, 0]
    big_df["现任基金资产总规模"] = big_df["现任基金资产总规模"].str.split("亿元", expand=True).iloc[:, 0]
    big_df['累计从业时间'] = pd.to_numeric(big_df['累计从业时间'], errors="coerce")
    big_df['现任基金最佳回报'] = pd.to_numeric(big_df['现任基金最佳回报'], errors="coerce")
    big_df['现任基金资产总规模'] = pd.to_numeric(big_df['现任基金资产总规模'], errors="coerce")
    if explode:
        big_df['现任基金'] = big_df['现任基金'].apply(lambda x: x.split(','))
        big_df = big_df.explode(column='现任基金')
        big_df.reset_index(drop=True, inplace=True)
        return big_df
    return big_df


if __name__ == "__main__":
    fund_manager_df = fund_manager(explode=False)
    print(fund_manager_df)
