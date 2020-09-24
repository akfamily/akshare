# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/5/4 9:07
Desc: COVID-19
COVID-19-网易
COVID-19-丁香园
COVID-19-百度
COVID-19-GitHub
"""
import json
import time

import demjson
import jsonpath
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from akshare.event.cons import province_dict, city_dict


# pd.set_option('display.max_columns', None)  # just for debug


def covid_19_163(indicator: str = "实时") -> pd.DataFrame:
    """
    网易-新冠状病毒
    https://news.163.com/special/epidemic/?spssid=93326430940df93a37229666dfbc4b96&spsw=4&spss=other&#map_block
    https://news.163.com/special/epidemic/?spssid=93326430940df93a37229666dfbc4b96&spsw=4&spss=other&
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
        params = {
            "areaCode": "66",
            "t": round(int(time.time() * 1000))
        }
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
        params = {
            "t": round(int(time.time() * 1000))
        }
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["list"])
        del temp_df["page"]
        return temp_df


def covid_19_dxy(indicator: str = "西藏自治区") -> pd.DataFrame:
    """
    20200315-丁香园接口更新分为国内和国外
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
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    # news-china
    text_data_news = str(
        soup.find("script", attrs={"id": "getTimelineService1"})
    )
    temp_json = text_data_news[
        text_data_news.find("= [{") + 2: text_data_news.rfind("}catch")
    ]
    json_data = pd.DataFrame(json.loads(temp_json))
    chinese_news = json_data[
        ["id", "pubDate", "pubDateStr", "title", "summary", "infoSource", "sourceUrl", "provinceId"]
    ]

    # news-foreign
    text_data_news = str(soup.find_all("script", attrs={"id": "getTimelineService2"}))
    temp_json = text_data_news[
        text_data_news.find("= [{") + 2: text_data_news.rfind("}catch")
    ]
    json_data = pd.DataFrame(json.loads(temp_json))
    foreign_news = json_data

    # data-domestic
    data_text = str(soup.find("script", attrs={"id": "getAreaStat"}))
    data_text_json = json.loads(
        data_text[data_text.find("= [{") + 2 : data_text.rfind("catch") - 1]
    )
    big_df = pd.DataFrame()
    for i, p in enumerate(jsonpath.jsonpath(data_text_json, "$..provinceName")):
        temp_df = pd.DataFrame(jsonpath.jsonpath(data_text_json, "$..cities")[i])
        temp_df["province"] = p
        big_df = big_df.append(temp_df, ignore_index=True)
    domestic_city_df = big_df

    data_df = pd.DataFrame(data_text_json).iloc[:, :7]
    data_df.columns = ["地区", "地区简称", "现存确诊", "累计确诊", "-", "治愈", "死亡"]
    domestic_province_df = data_df[["地区", "地区简称", "现存确诊", "累计确诊", "治愈", "死亡"]]
    # data-global
    data_text = str(
        soup.find("script", attrs={"id": "getListByCountryTypeService2true"})
    )
    data_text_json = json.loads(
        data_text[data_text.find("= [{") + 2: data_text.rfind("catch") - 1]
    )
    global_df = pd.DataFrame(data_text_json)

    # info
    dxy_static = str(soup.find("script", attrs={"id": "getStatisticsService"}))
    data_json = json.loads(
        dxy_static[dxy_static.find("= {") + 2: dxy_static.rfind("}c")]
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
    elif indicator == "国外新闻":
        return foreign_news
    else:
        try:
            data_text = str(soup.find("script", attrs={"id": "getAreaStat"}))
            data_text_json = json.loads(
                data_text[data_text.find("= [{") + 2: data_text.rfind("catch") - 1]
            )
            data_df = pd.DataFrame(data_text_json)
            sub_area = pd.DataFrame(
                data_df[data_df["provinceName"] == indicator]["cities"].values[0]
            )
            if sub_area.empty:
                return None
            sub_area.columns = ["区域", "现在确诊人数", "确诊人数", "疑似人数", "治愈人数", "死亡人数", "id"]
            sub_area = sub_area[["区域", "现在确诊人数", "确诊人数", "疑似人数", "治愈人数", "死亡人数"]]
            return sub_area
        except IndexError as e:
            print("请输入省/市的全称, 如: 浙江省/上海市 等")


def covid_19_baidu(indicator: str = "浙江") -> pd.DataFrame:
    """
    百度-新型冠状病毒肺炎-疫情实时大数据报告
    https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1
    :param indicator: 看说明文档
    :type indicator: str
    :return: 指定 indicator 的数据
    :rtype: pandas.DataFrame
    """
    url = "https://huiyan.baidu.com/openapi/v1/migration/rank"
    payload = {
        "type": "move",
        "ak": "kgD2HiDnLdUhwzd3CLuG5AWNfX3fhLYe",
        "adminType": "country",
        "name": "全国",
    }
    r = requests.get(url, params=payload)
    move_in_df = pd.DataFrame(r.json()["result"]["moveInList"])
    move_out_df = pd.DataFrame(r.json()["result"]["moveOutList"])

    url = "https://opendata.baidu.com/api.php"
    payload = {
        "query": "全国",
        "resource_id": "39258",
        "tn": "wisetpl",
        "format": "json",
        "cb": "jsonp_1580470773343_11183",
    }
    r = requests.get(url, params=payload)
    text_data = r.text
    json_data_news = json.loads(
        text_data.strip("/**/jsonp_1580470773343_11183(").rstrip(");")
    )

    # domestic-city
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    temp_soup = str(soup.find(attrs={"id": "captain-config"}))
    data_json = demjson.decode(temp_soup[temp_soup.find("{"): temp_soup.rfind("}")+1])

    big_df = pd.DataFrame()
    for i, p in enumerate(
        jsonpath.jsonpath(data_json["component"][0]["caseList"], "$..area")
    ):
        temp_df = pd.DataFrame(
            jsonpath.jsonpath(data_json["component"][0]["caseList"], "$..subList")[i]
        )
        temp_df["province"] = p
        big_df = big_df.append(temp_df, ignore_index=True)
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
        big_df = big_df.append(temp_df, ignore_index=True)
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
        big_df = big_df.append(temp_df, ignore_index=True)
    global_country_df = big_df

    global_continent_df = pd.DataFrame(data_json["component"][0]["globalList"])[
        ["area", "died", "crued", "confirmed", "confirmedRelative"]
    ]

    if indicator == "热门迁入地":
        return move_in_df
    elif indicator == "热门迁出地":
        return move_out_df
    elif indicator == "中国分省份详情":
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


def migration_area_baidu(area: str = "乌鲁木齐市", indicator: str = "move_out", date: str = "20200201") -> pd.DataFrame:
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
    :param date: 查询的日期 20200101以后的时间
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
    payload = {
        "dt": dt_flag,
        "id": inner_dict[area],
        "type": indicator,
        "date": date,
    }
    r = requests.get(url, params=payload)
    json_data = json.loads(r.text[r.text.find("({") + 1: r.text.rfind(");")])
    return pd.DataFrame(json_data["data"]["list"])


def internal_flow_history(area: str = "北京市", date: str = "20200412") -> pd.DataFrame:
    """
    百度地图慧眼-百度迁徙-城内出行强度
    * 城内出行强度: 该城市有出行的人数与该城市居住人口比值的指数化结果.
    * 当前数据更新于可能有延迟, 具体延迟请看相关页面提示.
    * 2019年城内出行强度指数将于2020年3月15日停止更新.
    https://qianxi.baidu.com/
    :param area: 可以输入 "省份" 或者 "具体城市" 但是需要用全称, 如: 北京市
    :type area: str
    :param date: 查询的日期 20200101以后的时间
    :type date: str
    :return: 2019-2020 的城市出行强度数据
    :rtype: pandas.DataFrame
    """
    city_dict.update(province_dict)
    inner_dict = dict(zip(city_dict.values(), city_dict.keys()))
    url = "https://huiyan.baidu.com/migration/internalflowhistory.jsonp"
    payload = {
        "dt": "city",
        "id": inner_dict[area],
        "date": date,
    }
    r = requests.get(url, params=payload)
    json_data = json.loads(r.text[r.text.find("({") + 1 : r.text.rfind(");")])
    temp_df = pd.DataFrame.from_dict(json_data["data"]["list"], orient="index").sort_index()
    temp_df.columns = ["value"]
    return temp_df


def migration_scale_baidu(
    area: str = "乌鲁木齐市", indicator: str = "move_out", start_date: str = "20190112", end_date: str = "20200401"
) -> pd.DataFrame:
    """
    百度地图慧眼-百度迁徙-迁徙规模
    * 迁徙规模指数：反映迁入或迁出人口规模，城市间可横向对比
    * 城市迁徙边界采用该城市行政区划，包含该城市管辖的区、县、乡、村
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
    payload = {
        "dt": dt_flag,
        "id": inner_dict[area],
        "type": indicator,
        "startDate": start_date,
        "endDate": end_date,
    }
    r = requests.get(url, params=payload)
    json_data = json.loads(r.text[r.text.find("({") + 1: r.text.rfind(");")])
    temp_df = pd.DataFrame.from_dict(json_data["data"]["list"], orient="index")
    temp_df.index = pd.to_datetime(temp_df.index)
    temp_df.columns = ["迁徙规模指数"]
    return temp_df[start_date: end_date]


def covid_19_area_search(province: str = "四川省", city: str = "成都市", district: str = "高新区") -> pd.DataFrame:
    """
    省份-城市-区-数据查询
    https://ncov.html5.qq.com/community?channelid=1&from=singlemessage&isappinstalled=0
    :param province: 根据 epidemic_area_all 输入
    :type province: str
    :param city: 根据 epidemic_area_all 输入
    :type city: str
    :param district: 根据 epidemic_area_all 输入
    :type district: str
    :return: 全国所有省份-城市-区域数据
    :rtype: pandas.DataFrame
    """
    url = "https://ncov.html5.qq.com/api/getCommunity"
    payload = {
        "province": province,
        "city": city,
        "district": district,
        "lat": "30.26555",
        "lng": "120.1536",
    }
    r = requests.get(url, params=payload)
    temp_df = pd.DataFrame(r.json()["community"][province][city][district])
    return temp_df[
        [
            "province",
            "city",
            "district",
            "show_address",
            "full_address",
            "cnt_sum_certain",
        ]
    ]


def covid_19_area_all() -> pd.DataFrame:
    """
    可以获取数据的全国所有省份-城市-区域数据
    https://ncov.html5.qq.com/community?channelid=1&from=singlemessage&isappinstalled=0
    :return: 数据的全国所有省份-城市-区域数据
    :rtype: pandas.DataFrame
    """
    url = "https://ncov.html5.qq.com/api/getPosition"
    r = requests.get(url)
    area = r.json()["position"]
    province_list = list(area.keys())
    temp = []
    for p in province_list:
        for c in area[p].keys():
            temp.extend(
                list(
                    zip(
                        [p] * len(list(area[p][c].keys())[1:]),
                        [c] * len(list(area[p][c].keys())[1:]),
                        list(area[p][c].keys())[1:],
                    )
                )
            )
    return pd.DataFrame(temp, columns=["province", "city", "district"])


def covid_19_area_detail() -> pd.DataFrame:
    """
    细化到每个小区的确诊人数
    需要遍历每个页面, 如非必要, 请勿运行
    https://ncov.html5.qq.com/community?channelid=1&from=singlemessage&isappinstalled=0
    :return: 全国每个小区的确诊人数
    :rtype: pandas.DataFrame
    """
    temp_df = pd.DataFrame()
    area_df = covid_19_area_all()
    for item in tqdm(area_df.iterrows(), total=area_df.shape[0]):
        small_df = covid_19_area_search(
            province=item[1][0], city=item[1][1], district=item[1][2]
        )
        temp_df = temp_df.append(small_df, ignore_index=True)
    return temp_df


def covid_19_trip() -> pd.DataFrame:
    """
    新型肺炎确诊患者-相同行程查询工具
    https://rl.inews.qq.com/h5/trip?from=newsapp&ADTAG=tgi.wx.share.message
    :return: 新型肺炎确诊患者-相同行程查询工具的所有历史数据
    :rtype: pandas.DataFrame
    """
    url = "https://rl.inews.qq.com/taf/travelFront"
    r = requests.get(url)
    return pd.DataFrame(r.json()["data"]["list"])


def covid_19_hist_city(city: str = "武汉市") -> pd.DataFrame:
    """
    该接口最好用代理速度比较快
    https://github.com/canghailan/Wuhan-2019-nCoV
    2019-12-01开始
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
    该接口最好用代理速度比较快
    https://github.com/canghailan/Wuhan-2019-nCoV
    2019-12-01开始
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


def covid_19_history() -> pd.DataFrame:
    """
    接口最好用代理速度比较快
    https://github.com/canghailan/Wuhan-2019-nCoV
    2019-12-01开始
    :return: 疫情数据
    :rtype: pandas.DataFrame
    """
    url = "https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.json"
    r = requests.get(url)
    data_json = r.json()
    data_df = pd.DataFrame(data_json)
    return data_df


def covid_19_csse_daily(date: str = "2020-04-06") -> pd.DataFrame:
    """
    2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE
    https://github.com/CSSEGISandData/COVID-19
    采集 GitHub csv 文件需要 raw 地址
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
        "国外新闻",
        "浙江省",
    ]
    for item in indicator_list:
        # item = "国外新闻"
        print(item)
        covid_19_dxy_df = covid_19_dxy(indicator=item)
        print(covid_19_dxy_df)

    # baidu
    indicator_list = [
        "热门迁入地",
        "热门迁出地",
        "中国分省份详情",
        "中国分城市详情",
        "国外分国详情",
        "国外分城市详情",
        "全球分洲详情",
        "全球分洲国家详情",
    ]
    for item in indicator_list:
        print(item)
        covid_19_baidu_df = covid_19_baidu(indicator=item)
        print(covid_19_baidu_df)

    # 迁徙地图
    migration_area_baidu_df = migration_area_baidu(
        area="上海市", indicator="move_in", date="20200312"
    )
    print(migration_area_baidu_df)

    # internal_flow_history_df = internal_flow_history(area="北京市", date="20200405")
    # print(internal_flow_history_df)

    migration_scale_baidu_df = migration_scale_baidu(
        area="上海市", indicator="move_in", start_date="20190113", end_date="20200512"
    )
    print(migration_scale_baidu_df)
    # 小区
    epidemic_area_search_df = covid_19_area_search(
        province="四川省", city="成都市", district="高新区"
    )
    print(epidemic_area_search_df)
    epidemic_area_all_df = covid_19_area_all()
    print(epidemic_area_all_df)
    epidemic_area_detail_df = covid_19_area_detail()
    print(epidemic_area_detail_df)
    # 行程
    epidemic_trip_df = covid_19_trip()
    print(epidemic_trip_df)
    # 历史数据
    epidemic_hist_city_df = covid_19_hist_city(city="武汉市")
    print(epidemic_hist_city_df)
    epidemic_hist_province_df = covid_19_hist_province(province="湖北省")
    print(epidemic_hist_province_df)
    # 详细历史数据
    epidemic_history_df = covid_19_history()
    print(epidemic_history_df)

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
