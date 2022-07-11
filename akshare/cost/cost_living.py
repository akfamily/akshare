#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/5/25 20:32
Desc: 世界各大城市生活成本数据
https://expatistan.com/cost-of-living/index
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup


def _get_region() -> dict:
    """
    获取主要板块, 一般不调用
    :return: 主要板块
    :rtype: dict
    """
    url = "https://www.expatistan.com/cost-of-living/index"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    half_url_list = [
        item["href"]
        for item in soup.find("ul", attrs={"class": "regions"}).find_all("a")
    ]
    name_list = [
        item["href"].split("/")[-1]
        for item in soup.find("ul", attrs={"class": "regions"}).find_all("a")
    ]
    name_url_dict = dict(zip(name_list, half_url_list))
    name_url_dict["world"] = "/cost-of-living/index"
    return name_url_dict


def cost_living(region: str = "world") -> pd.DataFrame:
    """
    国家或地区生活成本数据
    https://expatistan.com/cost-of-living/index
    :param region: choice of {"europe", "north-america", "latin-america", "asia", "middle-east", "africa", "oceania", "world"}
    :type region: str
    :return: 国家或地区生活成本数据
    :rtype: pandas.DataFrame
    """
    name_url_map = {
        "europe": "/cost-of-living/index/europe",
        "north-america": "/cost-of-living/index/north-america",
        "latin-america": "/cost-of-living/index/latin-america",
        "asia": "/cost-of-living/index/asia",
        "middle-east": "/cost-of-living/index/middle-east",
        "africa": "/cost-of-living/index/africa",
        "oceania": "/cost-of-living/index/oceania",
        "world": "/cost-of-living/index",
    }
    url = f"https://www.expatistan.com{name_url_map[region]}"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[0]
    temp_df.columns = ["rank", "city", "index"]
    return temp_df


if __name__ == "__main__":
    cost_living_df = cost_living()
    print(cost_living_df)
