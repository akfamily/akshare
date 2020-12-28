# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/11/30 13:14
Desc: 网站的经济政策不确定性指数
http://www.policyuncertainty.com/index.html
"""
import pandas as pd


def article_epu_index(index: str = "China") -> pd.DataFrame:
    """
    网站的经济政策不确定性指数
    :param index: 指定的国家名称, e.g. “China”
    :type index: str
    :return: 指定 index 的数据
    :rtype: pandas.DataFrame
    """
    if index == "China New":
        index = "China"
    if index == "USA":
        index = "US"
    if index == "Hong Kong":
        index = "HK"
        epu_df = pd.read_excel(
            f"http://www.policyuncertainty.com/media/{index}_EPU_Data_Annotated.xlsx",
            engine="openpyxl"
        )
        return epu_df
    if index in ["Germany", "France", "Italy"]:  # 欧洲
        index = "Europe"
    if index == "South Korea":
        index = "Korea"
    if index == "Spain New":
        index = "Spain"
    if index in ["Ireland", "Chile", "Colombia", "Netherlands", "Singapore", "Sweden"]:
        epu_df = pd.read_excel(
            f"http://www.policyuncertainty.com/media/{index}_Policy_Uncertainty_Data.xlsx",
            engine="openpyxl"
        )
        return epu_df
    if index == "Greece":
        epu_df = pd.read_excel(
            f"http://www.policyuncertainty.com/media/FKT_{index}_Policy_Uncertainty_Data.xlsx",
            engine="openpyxl"
        )
        return epu_df
    url = f"http://www.policyuncertainty.com/media/{index}_Policy_Uncertainty_Data.csv"
    epu_df = pd.read_csv(url)
    return epu_df


if __name__ == "__main__":
    article_epu_index_df = article_epu_index(index="Greece")
    print(article_epu_index_df)
