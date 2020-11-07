# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/11/7 13:04
Desc: 胡润排行榜
http://www.hurun.net/CN/HuList/Index?num=3YwKs889SRIm
"""
import numpy as np
import pandas as pd
import requests


def hurun_rank(indicator: str = "百富榜", year: str = "2020") -> pd.DataFrame:
    """
    胡润排行榜
    http://www.hurun.net/CN/HuList/Index?num=3YwKs889SRIm
    :param indicator: choice of {"百富榜", "富豪榜", "至尚优品"}
    :type indicator: str
    :param year: 指定年份; {"百富榜": "2015至今", "富豪榜": "2015至今", "至尚优品": "2017至今"}
    :type year: str
    :return: 指定 indicator 和 year 的数据
    :rtype: pandas.DataFrame
    """
    if indicator == "百富榜":
        symbol_map = {
            "2015": "5",
            "2016": "1",
            "2017": "11",
            "2018": "15",
            "2019": "19",
            "2020": "22",
        }
    elif indicator == "全球榜":
        symbol_map = {
            "2015": "6",
            "2016": "4",
            "2017": "2",
            "2018": "14",
            "2019": "18",
            "2020": "20",
        }
    elif indicator == "至尚优品":
        symbol_map = {
            "2017": "10",
            "2018": "13",
            "2019": "17",
            "2020": "21",
        }
        url = f"http://www.hurun.net/CN/HuList/BobListJson/{symbol_map[year]}"
        payload = {"order": "asc", "search": ""}
        r = requests.post(url, json=payload)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = [
            "_",
            "_",
            "_",
            "类别",
            "_",
            "_",
            "奖项",
            "_",
            "排名",
            "品牌",
            "_",
            "_",
        ]
        temp_df = temp_df[
            [
                "类别",
                "奖项",
                "排名",
                "品牌",
            ]
        ]
        temp_df["类别"].replace("", np.nan, inplace=True)
        temp_df.fillna(method="ffill", inplace=True)
        return temp_df
    url = f"http://www.hurun.net/CN/HuList/ListJson/{symbol_map[year]}"
    payload = {"order": "asc", "search": ""}
    r = requests.post(url, json=payload)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    temp_df.columns = [
        "_",
        "排名",
        "姓名",
        "财富",
        "出生日期",
        "关联企业",
        "主营行业",
    ]
    temp_df = temp_df[
        [
            "排名",
            "姓名",
            "财富",
            "出生日期",
            "关联企业",
            "主营行业",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    hurun_rank_df = hurun_rank(indicator="至尚优品", year="2020")
    print(hurun_rank_df)
