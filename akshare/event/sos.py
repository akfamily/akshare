# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/1/23 9:07
update_date: 2020/3/16 9:07
contact: jindaxiang@163.com
desc: COVID-19
COVID-19-网易
COVID-19-丁香园
COVID-19-百度
20200315 refactor the function
"""
import json
import time
from io import BytesIO

import demjson
import jsonpath
import pandas as pd
import requests
from PIL import Image
from bs4 import BeautifulSoup

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

    # 中国各地区时点数据
    area_total_df = pd.DataFrame(
        [item["total"] for item in data_json["data"]["areaTree"][0]["children"]],
        index=[item["name"] for item in data_json["data"]["areaTree"][0]["children"]],
    )

    # 中国各地区累计数据
    area_today_df = pd.DataFrame(
        [item["today"] for item in data_json["data"]["areaTree"][0]["children"]],
        index=[item["name"] for item in data_json["data"]["areaTree"][0]["children"]],
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

    elif indicator == "滚动新闻":
        return pd.DataFrame(data_info_json["scrollNews"])


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
        soup.find_all("script", attrs={"id": "getTimelineServiceundefined"})
    )
    temp_json = text_data_news[
        text_data_news.find("= [{") + 2 : text_data_news.rfind("}catch")
    ]
    json_data = pd.DataFrame(json.loads(temp_json))
    chinese_news = json_data[
        ["title", "summary", "infoSource", "provinceName", "sourceUrl"]
    ]

    # news-foreign
    text_data_news = str(soup.find_all("script", attrs={"id": "getTimelineService2"}))
    temp_json = text_data_news[
        text_data_news.find("= [{") + 2 : text_data_news.rfind("}catch")
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
        data_text[data_text.find("= [{") + 2 : data_text.rfind("catch") - 1]
    )
    global_df = pd.DataFrame(data_text_json)

    # info
    dxy_static = soup.find(attrs={"id": "getStatisticsService"}).get_text()
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
            data_json["suspectedIncr"],
            data_json["currentConfirmedIncr"],
            data_json["confirmedIncr"],
            data_json["curedIncr"],
            data_json["deadIncr"],
            data_json["seriousIncr"],
        ],
        index=[
            "数据发布时间",
            "现存确诊",
            "累计确诊",
            "境外输入",
            "累计治愈",
            "累计死亡",
            "现存重症",
            "境外输入较昨日",
            "现存确诊较昨日",
            "累计确诊较昨日",
            "累计治愈较昨日",
            "累计死亡较昨日",
            "现存重症较昨日",
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
    elif indicator == "实时播报":
        return chinese_news

    elif indicator == "中国-新增疑似-新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["quanguoTrendChart"][0]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "中国-现存确诊-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["quanguoTrendChart"][1]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "中国-现存疑似-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["quanguoTrendChart"][2]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "中国-治愈-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["quanguoTrendChart"][3]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "中国-死亡-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["quanguoTrendChart"][4]["imgUrl"]).content)
        )
        img_file.show()

    elif indicator == "中国-非湖北新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["hbFeiHbTrendChart"][0]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "中国-湖北新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["hbFeiHbTrendChart"][1]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "中国-湖北现存确诊-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["hbFeiHbTrendChart"][2]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "中国-非湖北现存确诊-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["hbFeiHbTrendChart"][3]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "中国-治愈-死亡-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["hbFeiHbTrendChart"][4]["imgUrl"]).content)
        )
        img_file.show()

    elif indicator == "国外-国外新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["foreignTrendChart"][0]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "国外-国外累计确诊-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["foreignTrendChart"][1]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "国外-国外死亡-趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["foreignTrendChart"][2]["imgUrl"]).content)
        )
        img_file.show()

    elif indicator == "国外-重点国家新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(
                requests.get(
                    data_json["importantForeignTrendChart"][0]["imgUrl"]
                ).content
            )
        )
        img_file.show()
    elif indicator == "国外-日本新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(
                requests.get(
                    data_json["importantForeignTrendChart"][1]["imgUrl"]
                ).content
            )
        )
        img_file.show()
    elif indicator == "国外-意大利新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(
                requests.get(
                    data_json["importantForeignTrendChart"][2]["imgUrl"]
                ).content
            )
        )
        img_file.show()
    elif indicator == "国外-伊朗新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(
                requests.get(
                    data_json["importantForeignTrendChart"][3]["imgUrl"]
                ).content
            )
        )
        img_file.show()
    elif indicator == "国外-美国新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(
                requests.get(
                    data_json["importantForeignTrendChart"][4]["imgUrl"]
                ).content
            )
        )
        img_file.show()
    elif indicator == "国外-法国新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(
                requests.get(
                    data_json["importantForeignTrendChart"][5]["imgUrl"]
                ).content
            )
        )
        img_file.show()
    elif indicator == "国外-德国新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(
                requests.get(
                    data_json["importantForeignTrendChart"][6]["imgUrl"]
                ).content
            )
        )
        img_file.show()
    elif indicator == "国外-西班牙新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(
                requests.get(
                    data_json["importantForeignTrendChart"][7]["imgUrl"]
                ).content
            )
        )
        img_file.show()
    elif indicator == "国外-韩国新增确诊-趋势图":
        img_file = Image.open(
            BytesIO(
                requests.get(
                    data_json["importantForeignTrendChart"][8]["imgUrl"]
                ).content
            )
        )
        img_file.show()
    else:
        try:
            data_text = str(soup.find("script", attrs={"id": "getAreaStat"}))
            data_text_json = json.loads(
                data_text[data_text.find("= [{") + 2 : data_text.rfind("catch") - 1]
            )
            data_df = pd.DataFrame(data_text_json)
            sub_area = pd.DataFrame(
                data_df[data_df["provinceName"] == indicator]["cities"].values[0]
            )
            if sub_area.empty:
                return print("暂无分区域数据")
            sub_area.columns = ["区域", "现在确诊人数", "确诊人数", "疑似人数", "治愈人数", "死亡人数", "id"]
            sub_area = sub_area[["区域", "现在确诊人数", "确诊人数", "疑似人数", "治愈人数", "死亡人数"]]
            return sub_area
        except IndexError as e:
            print("请输入省/市的全称, 如: 浙江省/上海市 等")


def covid_19_baidu(indicator="浙江"):
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

    url = "https://opendata.baidu.com/data/inner"
    payload = {
        "tn": "reserved_all_res_tn",
        "dspName": "iphone",
        "from_sf": "1",
        "dsp": "iphone",
        "resource_id": "28565",
        "alr": "1",
        "query": "肺炎",
        "cb": "jsonp_1580470773344_83572",
    }
    r = requests.get(url, params=payload)
    json_data = json.loads(r.text[r.text.find("({") + 1 : r.text.rfind(");")])
    spot_report = pd.DataFrame(json_data["Result"][0]["DisplayData"]["result"]["items"])

    # domestic-city
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    data_json = demjson.decode(soup.find(attrs={"id": "captain-config"}).text)

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
    elif indicator == "今日疫情热搜":
        return pd.DataFrame(json_data_news["data"][0]["list"][0]["item"])
    elif indicator == "防疫知识热搜":
        return pd.DataFrame(json_data_news["data"][0]["list"][1]["item"])
    elif indicator == "热搜谣言粉碎":
        return pd.DataFrame(json_data_news["data"][0]["list"][2]["item"])
    elif indicator == "复工复课热搜":
        return pd.DataFrame(json_data_news["data"][0]["list"][3]["item"])
    elif indicator == "热门人物榜":
        return pd.DataFrame(json_data_news["data"][0]["list"][4]["item"])
    elif indicator == "历史疫情热搜":
        return pd.DataFrame(json_data_news["data"][0]["list"][5]["item"])
    elif indicator == "搜索正能量榜":
        return pd.DataFrame(json_data_news["data"][0]["list"][6]["item"])
    elif indicator == "游戏榜":
        return pd.DataFrame(json_data_news["data"][0]["list"][7]["item"])
    elif indicator == "影视榜":
        return pd.DataFrame(json_data_news["data"][0]["list"][8]["item"])
    elif indicator == "小说榜":
        return pd.DataFrame(json_data_news["data"][0]["list"][9]["item"])
    elif indicator == "疫期飙升榜":
        return pd.DataFrame(json_data_news["data"][0]["list"][10]["item"])
    elif indicator == "实时播报":
        return spot_report
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


def migration_area_baidu(area="乌鲁木齐市", indicator="move_in", date="20200201"):
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
    payload = {
        "dt": dt_flag,
        "id": inner_dict[area],
        "type": indicator,
        "date": date,
    }
    r = requests.get(url, params=payload)
    json_data = json.loads(r.text[r.text.find("({") + 1 : r.text.rfind(");")])
    return pd.DataFrame(json_data["data"]["list"])


def migration_scale_baidu(
    area="乌鲁木齐市", indicator="move_out", start_date="20190112", end_date="20200201"
):
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
    json_data = json.loads(r.text[r.text.find("({") + 1 : r.text.rfind(");")])
    temp_df = pd.DataFrame.from_dict(json_data["data"]["list"], orient="index")
    temp_df.index = pd.to_datetime(temp_df.index)
    temp_df.columns = ["迁徙规模指数"]
    return temp_df


def covid_19_area_search(province="四川省", city="成都市", district="高新区"):
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


def covid_19_area_all():
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


def covid_19_area_detail():
    """
    细化到每个小区的确诊人数
    需要遍历每个页面, 如非必要, 请勿运行
    https://ncov.html5.qq.com/community?channelid=1&from=singlemessage&isappinstalled=0
    :return: 全国每个小区的确诊人数
    :rtype: pandas.DataFrame
    """
    temp_df = pd.DataFrame()
    area_df = covid_19_area_all()
    for item in area_df.iterrows():
        print(f"一共{area_df.shape[0]}, 正在下载第{item[0] + 1}页")
        small_df = covid_19_area_search(
            province=item[1][0], city=item[1][1], district=item[1][2]
        )
        temp_df = temp_df.append(small_df, ignore_index=True)
    return temp_df


def covid_19_trip():
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
    :return:
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
    :return: 具体省份的疫情数据
    :rtype: pandas.DataFrame
    """
    url = "https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.json"
    r = requests.get(url)
    data_json = r.json()
    data_df = pd.DataFrame(data_json)
    return data_df[data_df["province"] == province]


def covid_19_history() -> pd.DataFrame:
    """
    该接口最好用代理速度比较快
    https://github.com/canghailan/Wuhan-2019-nCoV
    2019-12-01开始
    :return:
    :rtype: pandas.DataFrame
    """
    url = "https://raw.githubusercontent.com/canghailan/Wuhan-2019-nCoV/master/Wuhan-2019-nCoV.json"
    r = requests.get(url)
    data_json = r.json()
    data_df = pd.DataFrame(data_json)
    return data_df


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
        "滚动新闻",
    ]
    for item in indicator_list:
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
        "实时播报",
        "中国-新增疑似-新增确诊-趋势图",
        "中国-现存确诊-趋势图",
        "中国-现存疑似-趋势图",
        "中国-治愈-趋势图",
        "中国-死亡-趋势图",
        "中国-非湖北新增确诊-趋势图",
        "中国-湖北新增确诊-趋势图",
        "中国-湖北现存确诊-趋势图",
        "中国-非湖北现存确诊-趋势图",
        "中国-治愈-死亡-趋势图",
        "国外-国外新增确诊-趋势图",
        "国外-国外累计确诊-趋势图",
        "国外-国外死亡-趋势图",
        "国外-重点国家新增确诊-趋势图",
        "国外-日本新增确诊-趋势图",
        "国外-意大利新增确诊-趋势图",
        "国外-伊朗新增确诊-趋势图",
        "国外-美国新增确诊-趋势图",
        "国外-法国新增确诊-趋势图",
        "国外-德国新增确诊-趋势图",
        "国外-西班牙新增确诊-趋势图",
        "国外-韩国新增确诊-趋势图",
        "浙江省",
    ]
    for item in indicator_list:
        covid_19_dxy_df = covid_19_dxy(indicator=item)
        print(covid_19_dxy_df)

    # baidu
    indicator_list = [
        "热门迁入地",
        "热门迁出地",
        "今日疫情热搜",
        "防疫知识热搜",
        "热搜谣言粉碎",
        "复工复课热搜",
        "热门人物榜",
        "历史疫情热搜",
        "搜索正能量榜",
        "游戏榜",
        "影视榜",
        "小说榜",
        "疫期飙升榜",
        "实时播报",
        "中国分省份详情",
        "中国分城市详情",
        "国外分国详情",
        "国外分城市详情",
        "全球分洲详情",
        "全球分洲国家详情",
    ]
    for item in indicator_list:
        covid_19_baidu_df = covid_19_baidu(indicator=item)
        print(covid_19_baidu_df)

    # 迁徙地图
    migration_area_baidu_df = migration_area_baidu(
        area="上海市", indicator="move_in", date="20200212"
    )
    # print(migration_area_baidu_df.to_csv("迁入上海市来源地-20200218.csv", encoding="gb2312"))
    print(migration_area_baidu_df)
    migration_scale_baidu_df = migration_scale_baidu(
        area="上海市", indicator="move_in", start_date="20190113", end_date="20200212"
    )
    # print(migration_scale_baidu_df.to_csv("迁入上海市2019-2020统计-20200218.csv", encoding="gb2312"))
    print(migration_scale_baidu_df)
    # 小区
    epidemic_area_search_df = covid_19_area_search(
        province="四川省", city="成都市", district="高新区"
    )
    print(epidemic_area_search_df)
    epidemic_area_all_df = covid_19_area_all()
    print(epidemic_area_all_df)
    # epidemic_area_detail_df = epidemic_area_detail()
    # print(epidemic_area_detail_df)
    # print(epidemic_area_detail_df.to_csv("所有疫情地点-20200218.csv", encoding="gbk"))
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
