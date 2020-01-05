# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/11/26 16:33
contact: jindaxiang@163.com
desc: 河北的空气质量数据
"""
import datetime

import pandas as pd
import requests


def air_hebei(city=""):
    url = f"http://110.249.223.67/publishNewServer/api/CityPublishInfo/GetProvinceAndCityPublishData?publishDate={datetime.datetime.today().strftime('%Y-%m-%d')}%2016:00:00"
    res = requests.get(url)
    json_data = res.json()

    city_list = pd.DataFrame.from_dict(json_data["cityPublishDatas"], orient="columns")["CityName"].tolist()
    city_1 = pd.DataFrame.from_dict([item["Date1"] for item in json_data["cityPublishDatas"]], orient="columns")
    city_2 = pd.DataFrame.from_dict([item["Date2"] for item in json_data["cityPublishDatas"]], orient="columns")
    city_3 = pd.DataFrame.from_dict([item["Date3"] for item in json_data["cityPublishDatas"]], orient="columns")
    city_4 = pd.DataFrame.from_dict([item["Date4"] for item in json_data["cityPublishDatas"]], orient="columns")
    city_5 = pd.DataFrame.from_dict([item["Date5"] for item in json_data["cityPublishDatas"]], orient="columns")
    city_6 = pd.DataFrame.from_dict([item["Date6"] for item in json_data["cityPublishDatas"]], orient="columns")

    city_1.index = city_list
    city_2.index = city_list
    city_3.index = city_list
    city_4.index = city_list
    city_5.index = city_list
    city_6.index = city_list

    big_df = pd.concat([city_1, city_2, city_3, city_4, city_5, city_6])
    if city == "":
        return big_df
    else:
        return big_df[big_df.index == city]


if __name__ == "__main__":
    temp_df = air_hebei(city="")
    print(temp_df[temp_df.index == "石家庄市"])
