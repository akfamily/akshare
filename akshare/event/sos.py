# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/1/23 9:07
contact: jindaxiang@163.com
desc: 新增-事件接口
新增-事件接口新型冠状病毒-网易
新增-事件接口新型冠状病毒-丁香园
"""
import json
import time

import requests
import pandas as pd
from bs4 import BeautifulSoup


def epidemic_163():
    url = "https://news.163.com/special/epidemic/?spssid=93326430940df93a37229666dfbc4b96&spsw=4&spss=other&"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")

    province_list = [item.get_text() for item in soup.find("ul").find_all("strong")]
    desc_list = [item.get_text() for item in soup.find("ul").find_all("li")]
    temp_df = pd.DataFrame([province_list, desc_list],
                           index=["地区", f"数据-{soup.find(attrs={'class': 'tit'}).find('span').get_text()}"]).T
    return temp_df


def epidemic_dxy(indicator="data"):
    url = "https://3g.dxy.cn/newh5/view/pneumonia"
    params = {
        "scene": "2",
        "clicktime": int(time.time()),
        "enterid": int(time.time()),
        "from": "groupmessage",
        "isappinstalled": "0",
    }
    res = requests.get(url, params=params)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "lxml")
    text_data_news = str(soup.find_all("script", attrs={"id": "getTimelineService"}))
    temp_json = text_data_news[text_data_news.find("= {") + 2: text_data_news.rfind("}catch")]
    json_data = pd.DataFrame(json.loads(temp_json)["result"])
    desc_data = json_data[["title", "summary", "infoSource", "provinceName", "sourceUrl"]]

    text_data_news = str(soup.find_all("script", attrs={"id": "getListByCountryTypeService1"}))
    temp_json = text_data_news[text_data_news.find("= [{") + 2: text_data_news.rfind("catch") - 1]
    json_data = pd.DataFrame(json.loads(temp_json))
    data = json_data[['tags', 'provinceShortName']]
    dig_data = data[['provinceShortName', 'tags']]

    # text_data_news = str(soup.find_all("script")[6])
    # temp_json = text_data_news[text_data_news.find("= {") + 2: text_data_news.rfind("}catch")]
    # info_data = pd.DataFrame(json.loads(temp_json), index=[0]).T
    if indicator == "data":
        return dig_data
    else:
        return desc_data


if __name__ == '__main__':
    epidemic_dxy_df = epidemic_dxy(indicator="data")
    print(epidemic_dxy_df)
    epidemic_163_df = epidemic_163()
    print(epidemic_163_df)
