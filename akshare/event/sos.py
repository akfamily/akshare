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

from akshare.event.cons import province_dict, city_dict

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


def epidemic_dxy(indicator="西藏自治区"):
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
            if sub_area.empty:
                return print("暂无分区域数据")
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


def migration_area_baidu(area="乌鲁木齐市", indicator="move_in", date="20200201"):
    """
    百度地图慧眼-百度迁徙-XXX迁入地详情
    百度地图慧眼-百度迁徙-XXX迁出地详情
    :param area: 可以输入 省份 或者 具体城市 但是需要用全称
    :type area: str
    :param indicator: move_in 迁入 move_out 迁出
    :type indicator: str
    :param date: 查询的日期 20200101以后的时间
    :type date: str
    :return: 迁入地详情/迁出地详情的前50个
    :rtype: pandas.DataFrame
    """
    city_dict.update(province_dict)
    inner_dict = dict(zip(city_dict.values(), city_dict.keys()))
    if inner_dict[area] in province_dict.keys():
        dt_flag = "province"
    else:
        dt_flag = "city"
    url = "https://huiyan.baidu.com/migration/cityrank.jsonp"
    params = {
        "dt": dt_flag,
        "id": inner_dict[area],
        "type": indicator,
        "date": date,
    }
    res = requests.get(url, params=params)
    json_data = json.loads(res.text[res.text.find("({")+1:res.text.rfind(");")])
    return pd.DataFrame(json_data["data"]["list"])


def migration_scale_baidu(area="乌鲁木齐市", indicator="move_out", start_date="20190112", end_date="20200201"):
    """
    百度地图慧眼-百度迁徙-迁徙规模
    * 迁徙规模指数：反映迁入或迁出人口规模，城市间可横向对比
    * 城市迁徙边界采用该城市行政区划，包含该城市管辖的区、县、乡、村
    :param area: 可以输入 省份 或者 具体城市 但是需要用全称
    :type area: str
    :param indicator: move_in 迁入 move_out 迁出
    :type indicator: str
    :param start_date: 开始查询的日期 默认就可以
    :type start_date: str
    :param end_date: 结束查询的日期 20200101 以后的时间
    :type end_date: str
    :return: 时间序列的迁徙规模指数
    :rtype: pandas.DataFrame
    """
    city_dict.update(province_dict)
    inner_dict = dict(zip(city_dict.values(), city_dict.keys()))
    if inner_dict[area] in province_dict.keys():
        dt_flag = "province"
    else:
        dt_flag = "city"
    url = "https://huiyan.baidu.com/migration/historycurve.jsonp"
    params = {
        "dt": dt_flag,
        "id": inner_dict[area],
        "type": indicator,
        "startDate": start_date,
        "endDate": end_date,
    }
    res = requests.get(url, params=params)
    json_data = json.loads(res.text[res.text.find("({") + 1:res.text.rfind(");")])
    temp_df = pd.DataFrame.from_dict(json_data["data"]["list"], orient="index")
    temp_df.index = pd.to_datetime(temp_df.index)
    temp_df.columns = ["迁徙规模指数"]
    return temp_df


if __name__ == "__main__":
    # 163
    epidemic_current_163_df = epidemic_163(indicator="实时")
    print(epidemic_current_163_df)
    epidemic_hist_163_df = epidemic_163(indicator="历史")
    print(epidemic_hist_163_df)
    # dxy
    epidemic_dxy_country_df = epidemic_dxy(indicator="全国")
    print(epidemic_dxy_country_df)
    epidemic_dxy_province_df = epidemic_dxy(indicator="西藏自治区")
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
    print(epidemic_baidu_ssbb_df)
    epidemic_baidu_ls_df = epidemic_baidu(indicator="历史")
    print(epidemic_baidu_ls_df)
    epidemic_baidu_gn_df = epidemic_baidu(indicator="国内")
    print(epidemic_baidu_gn_df)
    epidemic_baidu_gw_df = epidemic_baidu(indicator="国外")
    print(epidemic_baidu_gw_df)
    epidemic_baidu_zj_df = epidemic_baidu(indicator="浙江")
    print(epidemic_baidu_zj_df)
    # 迁徙地图
    migration_area_baidu_df = migration_area_baidu(area="浙江省", indicator="move_in", date="20200201")
    print(migration_area_baidu_df)
    migration_scale_baidu_df = migration_scale_baidu(area="浙江省", indicator="move_out", start_date="20190112", end_date="20200201")
    print(migration_scale_baidu_df)
