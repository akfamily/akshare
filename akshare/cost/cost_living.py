# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/12/18 12:32
Desc: 获取世界各大城市生活成本数据
https://expatistan.com/cost-of-living/index
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.cost.cons import url, name_url_map


def _get_region():
    """
    获取主要板块, 一般不调用
    :return: dict
    """
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
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
    :param region: str ["europe", "north-america", "latin-america", "asia", "middle-east", "africa", "oceania", "world"]
    :return: pandas.DataFrame
    """
    object_url = f"https://www.expatistan.com{name_url_map[region]}"
    res = requests.get(object_url)
    temp_df = pd.read_html(res.text)[0]
    temp_df.columns = ["rank", "city", "index"]
    return temp_df


if __name__ == "__main__":
    cost_living_df = cost_living()
    print(cost_living_df)
