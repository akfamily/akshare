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
from io import BytesIO

import demjson
import pandas as pd
import requests
from PIL import Image
from bs4 import BeautifulSoup


def epidemic_163(indicator="实时"):
    """
    网易网页端-新冠状病毒-实时人数统计情况
    国内和海外
    https://news.163.com/special/epidemic/?spssid=93326430940df93a37229666dfbc4b96&spsw=4&spss=other&#map_block
    :return: 返回国内各地区和海外地区情况
    :rtype: pandas.DataFrame
    """
    url = "https://spider.ws.126.net/disease_map_data"
    res = requests.get(url)
    temp = res.text[res.text.find("({") + 1: res.text.rfind("})") + 1]
    current_df = pd.DataFrame(
        demjson.decode(json.loads(temp)["data1"].replace("\n", ""))
    )
    hist_df = pd.DataFrame(demjson.decode(json.loads(temp)["data2"].replace("\n", "")))
    if indicator == "实时":
        return current_df
    else:
        return hist_df


def epidemic_dxy(indicator="info"):
    """
    丁香园-全国统计-info
    丁香园-分地区统计-data
    丁香园-全国发热门诊一览表-hospital
    丁香园-全国新闻-news
    :param indicator: ["info", "data", "hospital", "news"]
    :type indicator: str
    :return: 返回指定 indicator 的数据
    :rtype: pandas.DataFrame
    """
    url = "https://3g.dxy.cn/newh5/view/pneumonia"
    res = requests.get(url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "lxml")
    # news
    text_data_news = str(soup.find_all("script", attrs={"id": "getTimelineService"}))
    temp_json = text_data_news[
                text_data_news.find("= [{") + 2: text_data_news.rfind("}catch")
                ]
    json_data = pd.DataFrame(json.loads(temp_json))
    desc_data = json_data[
        ["title", "summary", "infoSource", "provinceName", "sourceUrl"]
    ]
    # data-new
    data_text = str(soup.find("script", attrs={"id": "getAreaStat"}))
    data_text_json = json.loads(
        data_text[data_text.find("= [{") + 2: data_text.rfind("catch") - 1]
    )
    data_df = pd.DataFrame(data_text_json)
    data_df.columns = ["地区", "地区简称", "确诊", "疑似", "治愈", "死亡", "备注", "区域"]
    country_df = data_df[["地区", "地区简称", "确诊", "疑似", "治愈", "死亡", "备注"]]
    # info
    dxy_static = soup.find(attrs={"id": "getStatisticsService"}).get_text()
    # hospital
    url = (
        "https://assets.dxycdn.com/gitrepo/tod-assets/output/default/pneumonia/index.js"
    )
    params = {"t": str(int(time.time()))}
    res = requests.get(url, params=params)
    hospital_df = pd.read_html(res.text)[0].iloc[:, :-1]
    if indicator == "全国":
        return country_df
    elif indicator == "info":
        return pd.read_json(
            dxy_static[dxy_static.find("= {") + 2: dxy_static.rfind("}catch")],
            orient="index",
        )
    elif indicator == "hospital":
        return hospital_df
    elif indicator == "plot":
        # img
        img_url = pd.read_json(
            dxy_static[dxy_static.find("= {") + 2: dxy_static.rfind("}catch")],
            orient="index",
        ).T
        img_file = Image.open(
            BytesIO(requests.get(img_url["dailyPic"].values[0]).content)
        )
        img_file.show()
    elif indicator == "news":
        return desc_data
    else:
        try:
            sub_area = pd.DataFrame(data_df[data_df["地区"] == indicator]["区域"].values[0])
            sub_area.columns = ["区域", "确诊人数", "疑似人数", "治愈人数", "死亡人数"]
            return sub_area
        except IndexError as e:
            print("请输入省/市的全称, 如: 浙江省/上海市 等")


if __name__ == "__main__":
    # 163
    epidemic_current_163_df = epidemic_163(indicator="实时")
    print(epidemic_current_163_df)
    epidemic_hist_163_df = epidemic_163(indicator="历史")
    print(epidemic_hist_163_df)
    # dxy
    epidemic_dxy_country_df = epidemic_dxy(indicator="全国")
    print(epidemic_dxy_country_df)
    epidemic_dxy_province_df = epidemic_dxy(indicator="湖北省")
    print(epidemic_dxy_province_df)
    epidemic_dxy_info_df = epidemic_dxy(indicator="info")
    print(epidemic_dxy_info_df)
    epidemic_dxy_hospital_df = epidemic_dxy(indicator="hospital")
    print(epidemic_dxy_hospital_df)
    epidemic_dxy_news_df = epidemic_dxy(indicator="news")
    print(epidemic_dxy_news_df)
    epidemic_dxy(indicator="plot")

