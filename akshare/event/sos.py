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

pd.set_option('display.max_columns', None)


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


def epidemic_dxy(indicator="浙江省"):
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
    data_df.columns = ["地区", "地区简称", "确诊", "疑似", "治愈", "死亡", "备注", "区域ID", "区域"]
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
            sub_area.columns = ["区域", "确诊人数", "疑似人数", "治愈人数", "死亡人数", "区域ID"]
            sub_area[["区域", "确诊人数", "疑似人数", "治愈人数", "死亡人数"]]
            return sub_area
        except IndexError as e:
            print("请输入省/市的全称, 如: 浙江省/上海市 等")


def epidemic_baidu(indicator="浙江"):
    """
    百度-新型冠状病毒肺炎-疫情实时大数据报告
    https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1
    :param indicator: 看说明文档
    :type indicator: str
    :return: 指定 indicator 的数据
    :rtype: pandas.DataFrame
    """
    url = "https://huiyan.baidu.com/openapi/v1/migration/rank"
    params = {
        "type": "move",
        "ak": "kgD2HiDnLdUhwzd3CLuG5AWNfX3fhLYe",
        "adminType": "country",
        "name": "全国",
    }
    res = requests.get(url, params=params)
    move_in_df = pd.DataFrame(res.json()["result"]["moveInList"])
    move_out_df = pd.DataFrame(res.json()["result"]["moveOutList"])
    url = "https://opendata.baidu.com/api.php"
    params = {
        "query": "全国",
        "resource_id": "39258",
        "tn": "wisetpl",
        "format": "json",
        "cb": "jsonp_1580470773343_11183",
    }
    res = requests.get(url, params=params)
    json_data = json.loads(res.text[res.text.find("({")+1:res.text.rfind(");")])
    today_df = pd.DataFrame(json_data["data"][0]["list"][0]["item"])
    protect_df = pd.DataFrame(json_data["data"][0]["list"][1]["item"])
    rumor_df = pd.DataFrame(json_data["data"][0]["list"][2]["item"])

    url = "https://opendata.baidu.com/data/inner"
    params = {
        "tn": "reserved_all_res_tn",
        "dspName": "iphone",
        "from_sf": "1",
        "dsp": "iphone",
        "resource_id": "28565",
        "alr": "1",
        "query": "肺炎",
        "cb": "jsonp_1580470773344_83572",
    }
    res = requests.get(url, params=params)
    json_data = json.loads(res.text[res.text.find("({") + 1:res.text.rfind(");")])
    spot_report = pd.DataFrame(json_data["Result"][0]["DisplayData"]["result"]["items"])

    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/"
    params = {
        "from": "osari_pc_1",
    }
    res = requests.get(url, params=params)
    json_data = json.loads(res.text[res.text.find("V.conf = ")+9: res.text.find("V.bsData")-1])
    temp_df = pd.DataFrame()
    temp_df[json_data["component"][0]["trend"]["list"][0]["name"]] = json_data["component"][0]["trend"]["list"][0]["data"]
    temp_df[json_data["component"][0]["trend"]["list"][1]["name"]] = json_data["component"][0]["trend"]["list"][1]["data"]
    temp_df[json_data["component"][0]["trend"]["list"][2]["name"]] = json_data["component"][0]["trend"]["list"][2]["data"]
    temp_df[json_data["component"][0]["trend"]["list"][3]["name"]] = json_data["component"][0]["trend"]["list"][3]["data"]
    temp_df.index = json_data["component"][0]["trend"]["updateDate"]

    temp_dict = {}
    for item in json_data["component"][0]["caseList"]:
        temp_dict[item["area"]] = item["subList"]

    domestic_df = pd.DataFrame.from_dict(json_data["component"][0]["summaryDataIn"], orient="index")
    domestic_df.columns = [json_data["component"][0]["mapLastUpdatedTime"]]
    out_df = pd.DataFrame.from_dict(json_data["component"][0]["summaryDataOut"], orient="index")
    out_df.columns = [json_data["component"][0]["foreignLastUpdatedTime"]]

    if indicator == "热门迁入地":
        return move_in_df
    elif indicator == "热门迁出地":
        return move_out_df
    elif indicator == "今日疫情热搜":
        return today_df
    elif indicator == "防疫知识热搜":
        return protect_df
    elif indicator == "热搜谣言粉碎":
        return rumor_df
    elif indicator == "实时播报":
        return spot_report
    elif indicator == "历史":
        return temp_df
    elif indicator == "国内":
        return domestic_df
    elif indicator == "国外":
        return out_df
    else:
        return pd.DataFrame(temp_dict[indicator])


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
    # baidu
    epidemic_baidu_rmqrd_df = epidemic_baidu(indicator="热门迁入地")
    print(epidemic_baidu_rmqrd_df)
    epidemic_baidu_rmqcd_df = epidemic_baidu(indicator="热门迁出地")
    print(epidemic_baidu_rmqcd_df)
    epidemic_baidu_jryqrs_df = epidemic_baidu(indicator="今日疫情热搜")
    print(epidemic_baidu_jryqrs_df)
    epidemic_baidu_fyzsrs_df = epidemic_baidu(indicator="防疫知识热搜")
    print(epidemic_baidu_fyzsrs_df)
    epidemic_baidu_rsyyfs_df = epidemic_baidu(indicator="热搜谣言粉碎")
    print(epidemic_baidu_rsyyfs_df)
    epidemic_baidu_ssbb_df = epidemic_baidu(indicator="实时播报")
    print(epidemic_baidu_ssbb_df.columns)
    epidemic_baidu_ls_df = epidemic_baidu(indicator="历史")
    print(epidemic_baidu_ls_df)
    epidemic_baidu_gn_df = epidemic_baidu(indicator="国内")
    print(epidemic_baidu_gn_df)
    epidemic_baidu_gw_df = epidemic_baidu(indicator="国外")
    print(epidemic_baidu_gw_df)
    epidemic_baidu_zj_df = epidemic_baidu(indicator="浙江")
    print(epidemic_baidu_zj_df)

