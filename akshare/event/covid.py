#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/2/22 14:07
Desc: COVID-19、COVID-19-网易、COVID-19-丁香园、COVID-19-百度、COVID-19-GitHub
"""
import json
import time

import jsonpath
import pandas as pd
import py_mini_racer
import requests
from bs4 import BeautifulSoup

from akshare.datasets import get_covid_js
from akshare.event.cons import province_dict, city_dict
from akshare.utils import demjson


def _get_file_content(file: str = "covid.js") -> str:
    """
    获取 JS 文件的内容
    :param file:  JS 文件名
    :type file: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_path = get_covid_js(file)
    with open(setting_file_path) as f:
        file_data = f.read()
    return file_data


def covid_19_risk_area(symbol: str = "高风险等级地区") -> pd.DataFrame:
    """
    卫生健康委-疫情风险等级查询
    http://bmfw.www.gov.cn/yqfxdjcx/risk.html
    :param symbol: choice of {"高风险等级地区", "中风险等级地区"}
    :type symbol: str
    :return: 疫情风险等级查询
    :rtype: pandas.DataFrame
    """
    file_data = _get_file_content(file="covid.js")
    ctx = py_mini_racer.MiniRacer()
    ctx.eval(file_data)
    decode_ajax_dict = ctx.call("generateAjaxParmas", "xxx")
    decode_header_dict = ctx.call("generateHeaderParmas", "xxx")
    url = "http://103.66.32.242:8005/zwfwMovePortal/interface/interfaceJson"
    payload = {
        "appId": "NcApplication",
        "key": "3C502C97ABDA40D0A60FBEE50FAAD1DA",
        "nonceHeader": "123456789abcdefg",
        "paasHeader": "zdww",
        "signatureHeader": eval(decode_ajax_dict)["signatureHeader"],
        "timestampHeader": eval(decode_ajax_dict)["timestampHeader"],
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "235",
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "103.66.32.242:8005",
        "Origin": "http://bmfw.www.gov.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://bmfw.www.gov.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "x-wif-nonce": "QkjjtiLM2dCratiA",
        "x-wif-paasid": "smt-application",
        "x-wif-signature": eval(decode_header_dict)["signatureHeader"],
        "x-wif-timestamp": eval(decode_header_dict)["timestampHeader"],
    }
    r = requests.post(url, json=payload, headers=headers)
    data_json = r.json()
    if symbol == "高风险等级地区":
        temp_df = pd.DataFrame(data_json["data"]["highlist"])
        temp_df = temp_df.explode(["communitys"])
        del temp_df["type"]
        temp_df["grade"] = "高风险"
        temp_df["report_date"] = data_json["data"]["end_update_time"]
        temp_df["number"] = data_json["data"]["hcount"]
        return temp_df
    else:
        temp_df = pd.DataFrame(data_json["data"]["middlelist"])
        temp_df = temp_df.explode(["communitys"])
        del temp_df["type"]
        temp_df["grade"] = "高风险"
        temp_df["report_date"] = data_json["data"]["end_update_time"]
        temp_df["number"] = data_json["data"]["mcount"]
        return temp_df


def covid_19_163(indicator: str = "实时") -> pd.DataFrame:
    """
    网易-新型冠状病毒
    https://news.163.com/special/epidemic/?spssid=93326430940df93a37229666dfbc4b96&spsw=4&spss=other&#map_block
    https://news.163.com/special/epidemic/?spssid=93326430940df93a37229666dfbc4b96&spsw=4&spss=other&
    :param indicator: 参数
    :type indicator: str
    :return: 返回指定 indicator 的数据
    :rtype: pandas.DataFrame
    """
    url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    }
    payload = {
        "t": int(time.time() * 1000),
    }
    r = requests.get(url, params=payload, headers=headers)
    data_json = r.json()

    # data info
    url = "https://news.163.com/special/epidemic/"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    data_info_df = pd.DataFrame(
        [
            item.text.strip().split(".")[1]
            for item in soup.find("div", attrs={"class": "data_tip_pop_text"}).find_all(
                "p"
            )
        ]
    )
    data_info_df.columns = ["info"]

    # 中国历史时点数据
    hist_today_df = pd.DataFrame(
        [item["today"] for item in data_json["data"]["chinaDayList"]],
        index=[item["date"] for item in data_json["data"]["chinaDayList"]],
    )

    # 中国历史累计数据
    hist_total_df = pd.DataFrame(
        [item["total"] for item in data_json["data"]["chinaDayList"]],
        index=[item["date"] for item in data_json["data"]["chinaDayList"]],
    )

    # 中国实时数据
    current_df = pd.DataFrame.from_dict(data_json["data"]["chinaTotal"])

    # 世界历史时点数据
    outside_today_df = pd.DataFrame(
        [item["today"] for item in data_json["data"]["areaTree"]],
        index=[item["name"] for item in data_json["data"]["areaTree"]],
    )

    # 世界历史累计数据
    outside_total_df = pd.DataFrame(
        [item["total"] for item in data_json["data"]["areaTree"]],
        index=[item["name"] for item in data_json["data"]["areaTree"]],
    )

    # 全球所有国家及地区时点数据
    all_world_today_df = pd.DataFrame(
        jsonpath.jsonpath(data_json["data"]["areaTree"], "$..today"),
        index=jsonpath.jsonpath(data_json["data"]["areaTree"], "$..name"),
    )

    # 全球所有国家及地区累计数据
    all_world_total_df = pd.DataFrame(
        jsonpath.jsonpath(data_json["data"]["areaTree"], "$..total"),
        index=jsonpath.jsonpath(data_json["data"]["areaTree"], "$..name"),
    )

    # 中国各地区累计数据
    area_total_df = pd.DataFrame(
        [item["total"] for item in data_json["data"]["areaTree"][2]["children"]],
        index=[item["name"] for item in data_json["data"]["areaTree"][2]["children"]],
    )

    # 中国各地区时点数据
    area_today_df = pd.DataFrame(
        [item["today"] for item in data_json["data"]["areaTree"][2]["children"]],
        index=[item["name"] for item in data_json["data"]["areaTree"][2]["children"]],
    )

    # 疫情学术进展
    url_article = "https://vip.open.163.com/api/cms/topic/list"
    payload_article = {
        "topicid": "00019NGQ",
        "listnum": "1000",
        "liststart": "0",
        "pointstart": "0",
        "pointend": "255",
        "useproperty": "true",
    }
    r_article = requests.get(url_article, params=payload_article)
    article_df = pd.DataFrame(r_article.json()["data"]).iloc[:, 1:]

    # 资讯
    url_info = "https://ent.163.com/special/00035080/virus_report_data.js"
    payload_info = {
        "_": int(time.time() * 1000),
        "callback": "callback",
    }
    r_info = requests.get(url_info, params=payload_info, headers=headers)
    data_info_text = r_info.text
    data_info_json = demjson.decode(data_info_text.strip(" callback(")[:-1])

    if indicator == "数据说明":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return data_info_df

    if indicator == "中国实时数据":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return current_df

    if indicator == "中国历史时点数据":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return hist_today_df

    if indicator == "中国历史累计数据":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return hist_total_df

    if indicator == "世界历史时点数据":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return outside_today_df

    if indicator == "世界历史累计数据":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return outside_total_df

    if indicator == "全球所有国家及地区时点数据":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return all_world_today_df

    elif indicator == "全球所有国家及地区累计数据":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return all_world_total_df

    elif indicator == "中国各地区时点数据":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return area_today_df

    elif indicator == "中国各地区累计数据":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return area_total_df

    elif indicator == "疫情学术进展":
        return article_df

    elif indicator == "实时资讯新闻播报":
        return pd.DataFrame(data_info_json["list"])

    elif indicator == "实时医院新闻播报":
        return pd.DataFrame(data_info_json["hospital"])

    elif indicator == "前沿知识":
        return pd.DataFrame(data_info_json["papers"])

    elif indicator == "权威发布":
        return pd.DataFrame(data_info_json["power"])

    elif indicator == "境外输入疫情趋势":
        url = "https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code"
        params = {"areaCode": "66", "t": round(int(time.time() * 1000))}
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["list"])
        today_list = [item.get("input", 0) for item in temp_df["today"]]
        total_list = [item.get("input", 0) for item in temp_df["total"]]
        result_df = pd.DataFrame([today_list, total_list]).T
        result_df.columns = ["境外输入新增确诊", "境外输入累计确诊"]
        result_df.index = pd.to_datetime(temp_df.date)
        return result_df

    elif indicator == "境外输入确诊病例来源":
        url = "https://c.m.163.com/ug/api/wuhan/app/index/input-data-list"
        params = {"t": round(int(time.time() * 1000))}
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["list"])
        del temp_df["page"]
        return temp_df


def covid_19_dxy(indicator: str = "浙江省") -> pd.DataFrame:
    """
    20200315-丁香园接口更新分为国内和国外
    https://ncov.dxy.cn/ncovh5/view/pneumonia
    丁香园-全国统计-info
    丁香园-分地区统计-data
    丁香园-全国发热门诊一览表-hospital
    丁香园-全国新闻-news
    :param indicator: choice of {"info", "data", "hospital", "news"}
    :type indicator: str
    :return: 返回指定 indicator 的数据
    :rtype: pandas.DataFrame
    """
    url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    # news-china
    text_data_news = str(soup.find("script", attrs={"id": "getTimelineService1"}))
    temp_json = text_data_news[
        text_data_news.find("= [{") + 2 : text_data_news.rfind("}catch")
    ]
    json_data = pd.DataFrame(json.loads(temp_json))
    chinese_news = json_data[
        [
            "id",
            "pubDate",
            "pubDateStr",
            "title",
            "summary",
            "infoSource",
            "sourceUrl",
            "provinceId",
        ]
    ]

    # data-domestic
    data_text = str(soup.find("script", attrs={"id": "getAreaStat"}))
    data_text_json = json.loads(
        data_text[data_text.find("= [{") + 2 : data_text.rfind("catch") - 1]
    )
    big_df = pd.DataFrame()
    for i, p in enumerate(jsonpath.jsonpath(data_text_json, "$..provinceName")):
        temp_df = pd.DataFrame(jsonpath.jsonpath(data_text_json, "$..cities")[i])
        temp_df["province"] = p
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    domestic_city_df = big_df
    data_df = pd.DataFrame(data_text_json).iloc[:, :7]
    data_df.columns = ["地区", "地区简称", "现存确诊", "累计确诊", "-", "治愈", "死亡"]
    domestic_province_df = data_df[["地区", "地区简称", "现存确诊", "累计确诊", "治愈", "死亡"]]

    # data-global
    data_text = str(
        soup.find("script", attrs={"id": "getListByCountryTypeService2true"})
    )
    data_text_json = json.loads(
        data_text[data_text.find("= [{") + 2 : data_text.rfind("catch") - 1]
    )
    global_df = pd.DataFrame(data_text_json)

    # info
    dxy_static = str(soup.find("script", attrs={"id": "getStatisticsService"}))
    data_json = json.loads(
        dxy_static[dxy_static.find("= {") + 2 : dxy_static.rfind("}c")]
    )
    china_statistics = pd.DataFrame(
        [
            time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(data_json["modifyTime"] / 1000)
            ),
            data_json["currentConfirmedCount"],
            data_json["confirmedCount"],
            data_json["suspectedCount"],
            data_json["curedCount"],
            data_json["deadCount"],
            data_json["seriousCount"],
        ],
        index=[
            "数据发布时间",
            "现存确诊",
            "累计确诊",
            "境外输入",
            "累计治愈",
            "累计死亡",
            "现存重症",
        ],
        columns=["info"],
    )
    foreign_statistics = pd.DataFrame.from_dict(
        data_json["foreignStatistics"], orient="index"
    )
    global_statistics = pd.DataFrame.from_dict(
        data_json["globalStatistics"], orient="index"
    )

    # hospital
    url = (
        "https://assets.dxycdn.com/gitrepo/tod-assets/output/default/pneumonia/index.js"
    )
    payload = {"t": str(int(time.time()))}
    r = requests.get(url, params=payload)
    hospital_df = pd.read_html(r.text)[0].iloc[:, :-1]

    if indicator == "中国疫情分省统计详情":
        return domestic_province_df
    if indicator == "中国疫情分市统计详情":
        return domestic_city_df
    elif indicator == "全球疫情分国家统计详情":
        return global_df
    elif indicator == "中国疫情实时统计":
        return china_statistics
    elif indicator == "国外疫情实时统计":
        return foreign_statistics
    elif indicator == "全球疫情实时统计":
        return global_statistics
    elif indicator == "中国疫情防控医院":
        return hospital_df
    elif indicator == "国内新闻":
        return chinese_news
    else:
        try:
            data_text = str(soup.find("script", attrs={"id": "getAreaStat"}))
            data_text_json = json.loads(
                data_text[data_text.find("= [{") + 2 : data_text.rfind("catch") - 1]
            )
            data_df = pd.DataFrame(data_text_json)
            # indicator = "浙江省"
            sub_area = pd.DataFrame(
                data_df[data_df["provinceName"] == indicator]["cities"].values[0]
            )
            if sub_area.empty:
                return
            if sub_area.shape[1] != 10:
                sub_area.columns = [
                    "区域",
                    "现在确诊人数",
                    "确诊人数",
                    "疑似人数",
                    "治愈人数",
                    "死亡人数",
                    "高危人数",
                    "中危人数",
                    "id",
                    "_",
                    "_",
                ]
                sub_area = sub_area[
                    [
                        "区域",
                        "现在确诊人数",
                        "确诊人数",
                        "疑似人数",
                        "治愈人数",
                        "死亡人数",
                        "高危人数",
                        "中危人数",
                    ]
                ]
            else:
                sub_area.columns = [
                    "区域",
                    "现在确诊人数",
                    "确诊人数",
                    "疑似人数",
                    "治愈人数",
                    "死亡人数",
                    "高危人数",
                    "中危人数",
                    "id",
                    "_",
                ]
                sub_area = sub_area[
                    [
                        "区域",
                        "现在确诊人数",
                        "确诊人数",
                        "疑似人数",
                        "治愈人数",
                        "死亡人数",
                        "高危人数",
                        "中危人数",
                    ]
                ]
            return sub_area
        except IndexError:
            print("请输入省/市的全称, 如: 浙江省/上海市 等")


def covid_19_baidu(indicator: str = "浙江") -> pd.DataFrame:
    """
    百度-新型冠状病毒肺炎-疫情实时大数据报告
    https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1
    百度迁徙
    https://qianxi.baidu.com/
    :param indicator: 看说明文档
    :type indicator: str
    :return: 指定 indicator 的数据
    :rtype: pandas.DataFrame
    """
    # domestic-city
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    temp_soup = str(soup.find(attrs={"id": "captain-config"}))
    data_json = demjson.decode(
        temp_soup[temp_soup.find("{") : temp_soup.rfind("}") + 1]
    )
    big_df = pd.DataFrame()
    for i, p in enumerate(
        [item["area"] for item in data_json["component"][0]["caseList"]]
    ):
        temp_df = pd.DataFrame(
            jsonpath.jsonpath(data_json["component"][0]["caseList"][i], "$.subList")[0]
        )

        temp_df["province"] = p
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    domestic_city_df = big_df

    domestic_province_df = pd.DataFrame(data_json["component"][0]["caseList"]).iloc[
        :, :-2
    ]

    big_df = pd.DataFrame()
    for i, p in enumerate(
        jsonpath.jsonpath(data_json["component"][0]["caseOutsideList"], "$..area")
    ):
        temp_df = pd.DataFrame(
            jsonpath.jsonpath(
                data_json["component"][0]["caseOutsideList"], "$..subList"
            )[i]
        )
        temp_df["province"] = p
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    outside_city_df = big_df

    outside_country_df = pd.DataFrame(
        data_json["component"][0]["caseOutsideList"]
    ).iloc[:, :-1]

    big_df = pd.DataFrame()
    for i, p in enumerate(
        jsonpath.jsonpath(data_json["component"][0]["globalList"], "$..area")
    ):
        temp_df = pd.DataFrame(
            jsonpath.jsonpath(data_json["component"][0]["globalList"], "$..subList")[i]
        )
        temp_df["province"] = p

        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    global_country_df = big_df

    global_continent_df = pd.DataFrame(data_json["component"][0]["globalList"])[
        ["area", "died", "crued", "confirmed", "confirmedRelative"]
    ]

    url = "https://opendata.baidu.com/data/inner"
    params = {
        "tn": "reserved_all_res_tn",
        "dspName": "iphone",
        "from_sf": "1",
        "dsp": "iphone",
        "resource_id": "28565",
        "alr": "1",
        "query": "国内新型肺炎最新动态",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(
        data_json["Result"][0]["items_v2"][0]["aladdin_res"]["DisplayData"]["result"][
            "items"
        ]
    )
    temp_df.rename(
        {
            "bjh_na": "_",
            "eventDescription": "新闻",
            "eventTime": "时间",
            "eventUrl": "链接",
            "homepageUrl": "_",
            "item_avatar": "_",
            "siteName": "来源",
        },
        axis=1,
        inplace=True,
    )
    temp_df.set_index(pd.to_datetime(temp_df["时间"], unit="s", utc=True), inplace=True)
    temp_df.index = (
        pd.to_datetime(temp_df["时间"], unit="s", utc=True)
        .tz_convert("Asia/Shanghai")
        .index
    )
    del temp_df["时间"]
    temp_df.reset_index(inplace=True)
    temp_df["时间"] = (
        pd.to_datetime(temp_df["时间"])
        .dt.date.astype(str)
        .str.cat(pd.to_datetime(temp_df["时间"]).dt.time.astype(str), sep=" ")
    )
    temp_df = temp_df[
        [
            "新闻",
            "时间",
            "来源",
            "链接",
        ]
    ]
    domestic_news = temp_df

    params = {
        "tn": "reserved_all_res_tn",
        "dspName": "iphone",
        "from_sf": "1",
        "dsp": "iphone",
        "resource_id": "28565",
        "alr": "1",
        "query": "国外新型肺炎最新动态",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(
        data_json["Result"][0]["items_v2"][0]["aladdin_res"]["DisplayData"]["result"][
            "items"
        ]
    )
    temp_df.rename(
        {
            "bjh_na": "_",
            "eventDescription": "新闻",
            "eventTime": "时间",
            "eventUrl": "链接",
            "homepageUrl": "_",
            "item_avatar": "_",
            "siteName": "来源",
        },
        axis=1,
        inplace=True,
    )
    temp_df = temp_df[
        [
            "新闻",
            "时间",
            "来源",
            "链接",
        ]
    ]
    temp_df.set_index(pd.to_datetime(temp_df["时间"], unit="s", utc=True), inplace=True)
    temp_df.index = (
        pd.to_datetime(temp_df["时间"], unit="s", utc=True)
        .tz_convert("Asia/Shanghai")
        .index
    )
    del temp_df["时间"]
    temp_df.reset_index(inplace=True)
    temp_df["时间"] = (
        pd.to_datetime(temp_df["时间"])
        .dt.date.astype(str)
        .str.cat(pd.to_datetime(temp_df["时间"]).dt.time.astype(str), sep=" ")
    )
    temp_df = temp_df[
        [
            "新闻",
            "时间",
            "来源",
            "链接",
        ]
    ]
    foreign_news = temp_df

    if indicator == "中国分省份详情":
        return domestic_province_df
    elif indicator == "中国分城市详情":
        return domestic_city_df
    elif indicator == "国外分国详情":
        return outside_country_df
    elif indicator == "国外分城市详情":
        return outside_city_df
    elif indicator == "全球分洲详情":
        return global_continent_df
    elif indicator == "全球分洲国家详情":
        return global_country_df
    elif indicator == "国内新型肺炎最新动态":
        return domestic_news
    elif indicator == "国外新型肺炎最新动态":
        return foreign_news


def migration_area_baidu(
    area: str = "乌鲁木齐市", indicator: str = "move_out", date: str = "20200201"
) -> pd.DataFrame:
    """
    百度地图慧眼-百度迁徙-XXX迁入地详情
    百度地图慧眼-百度迁徙-XXX迁出地详情
    以上展示 top100 结果，如不够 100 则展示全部
    迁入来源地比例: 从 xx 地迁入到当前区域的人数与当前区域迁入总人口的比值
    迁出目的地比例: 从当前区域迁出到 xx 的人口与从当前区域迁出总人口的比值
    https://qianxi.baidu.com/?from=shoubai#city=0
    :param area: 可以输入 省份 或者 具体城市 但是需要用全称
    :type area: str
    :param indicator: move_in 迁入 move_out 迁出
    :type indicator: str
    :param date: 查询的日期 20200101 以后的时间
    :type date: str
    :return: 迁入地详情/迁出地详情的前 50 个
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
    r = requests.get(url, params=params)
    data_text = r.text[r.text.find("({") + 1 : r.text.rfind(");")]
    data_json = json.loads(data_text)
    temp_df = pd.DataFrame(data_json["data"]["list"])
    return temp_df


def migration_scale_baidu(
    area: str = "佛山市",
    indicator: str = "move_out",
    start_date: str = "20200110",
    end_date: str = "20200315",
) -> pd.DataFrame:
    """
    百度地图慧眼-百度迁徙-迁徙规模
    迁徙规模指数：反映迁入或迁出人口规模，城市间可横向对比城市迁徙边界采用该城市行政区划，包含该城市管辖的区、县、乡、村
    https://qianxi.baidu.com/?from=shoubai#city=0
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
    r = requests.get(url, params=params)
    json_data = json.loads(r.text[r.text.find("({") + 1 : r.text.rfind(");")])
    temp_df = pd.DataFrame.from_dict(json_data["data"]["list"], orient="index")
    temp_df.index = pd.to_datetime(temp_df.index)
    temp_df.columns = ["迁徙规模指数"]
    temp_df = temp_df[start_date:end_date]
    return temp_df


def covid_19_trip() -> pd.DataFrame:
    """
    新型肺炎确诊患者-同程查询
    https://rl.inews.qq.com/h5/trip?from=newsapp&ADTAG=tgi.wx.share.message
    :return: 新型肺炎确诊患者-相同行程查询工具的所有历史数据
    :rtype: pandas.DataFrame
    """
    url = "https://r.inews.qq.com/api/travelFront"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["list"])
    return temp_df


def covid_19_trace() -> pd.DataFrame:
    """
    腾讯新闻-疫情-病患轨迹
    https://news.qq.com/hdh5/hebeicomeon.htm#/?ADTAG=yqi
    :return: 病患轨迹
    :rtype: pandas.DataFrame
    """
    url = "https://r.inews.qq.com/api/trackmap/poilist"
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    r = requests.get(url, headers=headers)
    data_json = r.json()
    province_list = [item["fullname"] for item in data_json["result"]["list"]]
    big_df = pd.DataFrame()
    for province in province_list:
        url = "https://apis.map.qq.com/place_cloud/search/region"
        params = {
            "region": province,
            "page_size": "200",
            "table_id": "5ff7d526b34a3525c3169a0b",
            "key": "NFPBZ-D2N3P-T7FDV-VLBQ6-4DVM7-JQFCR",
            "fliter": "",
        }
        headers = {
            "Referer": "https://news.qq.com/",
            "Host": "apis.map.qq.com",
            "Origin": "https://news.qq.com",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        }
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        risk_level = [item["x"]["risk_level"] for item in data_json["result"]["data"]]
        count_time = [item["x"]["datetime"] for item in data_json["result"]["data"]]
        temp_df = pd.DataFrame(data_json["result"]["data"])
        del temp_df["location"]
        del temp_df["id"]
        del temp_df["polygon"]
        del temp_df["tel"]
        del temp_df["ud_id"]
        del temp_df["adcode"]
        del temp_df["x"]
        temp_df["update_time"] = pd.to_datetime(temp_df["update_time"], unit="s")
        temp_df["create_time"] = pd.to_datetime(temp_df["create_time"], unit="s")
        temp_df["risk_level"] = risk_level
        temp_df["count_time"] = count_time
        del temp_df["create_time"]
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.columns = [
        "地址",
        "城市",
        "区",
        "_",
        "省份",
        "标题",
        "更新时间",
        "风险等级",
        "统计时间",
    ]
    big_df = big_df[
        [
            "地址",
            "城市",
            "区",
            "省份",
            "标题",
            "更新时间",
            "风险等级",
            "统计时间",
        ]
    ]
    return big_df


def covid_19_hist_city(city: str = "武汉市") -> pd.DataFrame:
    """
    该接口最好用代理速度比较快, 2019-12-01开始
    https://github.com/canghailan/Wuhan-2019-nCoV
    :param city: 具体的城市
    :type city: str
    :return: COVID-19 具体城市的数据
    :rtype: pandas.DataFrame
    """
    url = "https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.json"
    r = requests.get(url)
    data_json = r.json()
    data_df = pd.DataFrame(data_json)
    return data_df[data_df["city"] == city]


def covid_19_hist_province(province: str = "湖北省") -> pd.DataFrame:
    """
    该接口最好用代理速度比较快, 2019-12-01开始
    https://github.com/canghailan/Wuhan-2019-nCoV
    :param province: 具体的省份
    :type province: str
    :return: COVID-19 具体城市的数据
    :rtype: pandas.DataFrame
    """
    url = "https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.json"
    r = requests.get(url)
    data_json = r.json()
    data_df = pd.DataFrame(data_json)
    return data_df[data_df["province"] == province]


def covid_19_csse_daily(date: str = "2020-04-06") -> pd.DataFrame:
    """
    2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE, 采集 GitHub csv 文件需要 raw 地址
    https://github.com/CSSEGISandData/COVID-19
    :param date: from 2020-01-22 to today
    :type date: str
    :return: CSSE data
    :rtype: pandas.DataFrame
    """
    url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date.split('-')[1]}-{date.split('-')[2]}-{date.split('-')[0]}.csv"
    temp_df = pd.read_table(url, sep=",")
    return temp_df


def covid_19_csse_us_confirmed() -> pd.DataFrame:
    """
    2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE
    https://github.com/CSSEGISandData/COVID-19
    :return: us confirmed data
    :rtype: pandas.DataFrame
    """
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
    temp_df = pd.read_table(url, sep=",")
    return temp_df


def covid_19_csse_global_confirmed() -> pd.DataFrame:
    """
    2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE
    https://github.com/CSSEGISandData/COVID-19
    :return: global data
    :rtype: pandas.DataFrame
    """
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    temp_df = pd.read_table(url, sep=",")
    return temp_df


def covid_19_csse_us_death() -> pd.DataFrame:
    """
    2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE
    https://github.com/CSSEGISandData/COVID-19
    :return: us death data
    :rtype: pandas.DataFrame
    """
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
    temp_df = pd.read_table(url, sep=",")
    return temp_df


def covid_19_csse_global_death() -> pd.DataFrame:
    """
    2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE
    https://github.com/CSSEGISandData/COVID-19
    :return: global death data
    :rtype: pandas.DataFrame
    """
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    temp_df = pd.read_table(url, sep=",")
    return temp_df


def covid_19_csse_global_recovered() -> pd.DataFrame:
    """
    2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE
    https://github.com/CSSEGISandData/COVID-19
    :return: recovered data
    :rtype: pandas.DataFrame
    """
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    temp_df = pd.read_table(url, sep=",")
    return temp_df


if __name__ == "__main__":
    covid_19_risk_area_df = covid_19_risk_area(symbol="高风险等级地区")
    print(covid_19_risk_area_df)

    covid_19_risk_area_df = covid_19_risk_area(symbol="中等风险等级地区")
    print(covid_19_risk_area_df)

    # 163
    indicator_list = [
        "数据说明",
        "中国实时数据",
        "中国历史时点数据",
        "中国历史累计数据",
        "世界历史时点数据",
        "世界历史累计数据",
        "全球所有国家及地区时点数据",
        "全球所有国家及地区累计数据",
        "中国各地区时点数据",
        "中国各地区累计数据",
        "疫情学术进展",
        "实时资讯新闻播报",
        "实时医院新闻播报",
        "前沿知识",
        "权威发布",
        "境外输入疫情趋势",
        "境外输入确诊病例来源",
    ]
    for item in indicator_list:
        print(item)
        covip_19_163_df = covid_19_163(indicator=item)
        print(covip_19_163_df)

    # dxy
    indicator_list = [
        "中国疫情分省统计详情",
        "中国疫情分市统计详情",
        "全球疫情分国家统计详情",
        "中国疫情实时统计",
        "国外疫情实时统计",
        "全球疫情实时统计",
        "中国疫情防控医院",
        "国内新闻",
        "浙江省",
    ]
    for item in indicator_list:
        # item = "国外新闻"
        print(item)
        covid_19_dxy_df = covid_19_dxy(indicator=item)
        print(covid_19_dxy_df)

    # baidu
    indicator_list = [
        "中国分省份详情",
        "中国分城市详情",
        "国外分国详情",
        "国外分城市详情",
        "全球分洲详情",
        "全球分洲国家详情",
        "国内新型肺炎最新动态",
        "国外新型肺炎最新动态",
    ]
    for item in indicator_list:
        print(item)
        covid_19_baidu_df = covid_19_baidu(indicator=item)
        print(covid_19_baidu_df)

    # 迁徙地图
    migration_area_baidu_df = migration_area_baidu(
        area="上海市", indicator="move_in", date="20201112"
    )
    print(migration_area_baidu_df)

    migration_scale_baidu_df = migration_scale_baidu(
        area="上海市", indicator="move_in", start_date="20200110", end_date="20200315"
    )
    print(migration_scale_baidu_df)

    # 同程查询
    epidemic_trip_df = covid_19_trip()
    print(epidemic_trip_df)

    # 病患轨迹
    covid_19_trace_df = covid_19_trace()
    print(covid_19_trace_df)

    # 历史数据
    epidemic_hist_city_df = covid_19_hist_city(city="武汉市")
    print(epidemic_hist_city_df)

    epidemic_hist_province_df = covid_19_hist_province(province="湖北省")
    print(epidemic_hist_province_df)

    # CSSE
    covid_19_csse_daily_df = covid_19_csse_daily(date="2020-04-13")
    print(covid_19_csse_daily_df)

    covid_19_csse_us_confirmed_df = covid_19_csse_us_confirmed()
    print(covid_19_csse_us_confirmed_df)

    covid_19_csse_global_confirmed_df = covid_19_csse_global_confirmed()
    print(covid_19_csse_global_confirmed_df)

    covid_19_csse_us_death_df = covid_19_csse_us_death()
    print(covid_19_csse_us_death_df)

    covid_19_csse_global_death_df = covid_19_csse_global_death()
    print(covid_19_csse_global_death_df)

    covid_19_csse_global_recovered_df = covid_19_csse_global_recovered()
    print(covid_19_csse_global_recovered_df)
