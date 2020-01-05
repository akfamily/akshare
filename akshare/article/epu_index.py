# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/11/30 13:14
contact: jindaxiang@163.com
desc: 获取 http://www.policyuncertainty.com/index.html 网站的经济政策不确定性指数
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.article.cons import epu_home_url

res = requests.get(epu_home_url)
soup = BeautifulSoup(res.text, "lxml")
html_left_list = soup.find(attrs={"class": "sidebar_container"}).find_all("p", attrs={"class": "alignleft"})
html_right_list = soup.find(attrs={"class": "sidebar_container"}).find_all("p", attrs={"class": "alignright"})

index_left_list = [item.get_text() for item in html_left_list][4:]
index_right_list = [item.get_text() for item in html_right_list]
index_list = index_left_list + index_right_list


def article_epu_index(index="China"):
    if index == "China New":
        index = "China"
    if index == "USA":
        index = "US"
    if index == "Hong Kong":
        index = "HK"
        epu_df = pd.read_excel(f"http://www.policyuncertainty.com/media/{index}_EPU_Data_Annotated.xlsx")
        return epu_df
    if index in ["Germany", "France", "Italy"]:  # 欧洲
        index = "Europe"
    if index == "South Korea":
        index = "Korea"
    if index == "Spain New":
        index = "Spain"
    if index in ["Ireland", "Chile", "Colombia", "Netherlands", "Singapore", "Sweden"]:
        epu_df = pd.read_excel(f"http://www.policyuncertainty.com/media/{index}_Policy_Uncertainty_Data.xlsx")
        return epu_df
    if index == "Greece":
        epu_df = pd.read_excel(f"http://www.policyuncertainty.com/media/FKT_{index}_Policy_Uncertainty_Data.xlsx")
        return epu_df
    url = f"http://www.policyuncertainty.com/media/{index}_Policy_Uncertainty_Data.csv"
    epu_df = pd.read_csv(url)
    return epu_df


if __name__ == "__main__":
    epu_index_df = article_epu_index(index="China")
    print(epu_index_df)
