# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/1/23 9:07
contact: jindaxiang@163.com
desc: 新增-事件接口
新增-事件接口新型冠状病毒-网易
新增-事件接口新型冠状病毒-丁香园
新增-事件接口新型冠状病毒-百度
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


# pd.set_option('display.max_columns', None)  # just for debug


def epidemic_163(indicator="实时"):
    """
    网易网页端-新冠状病毒-实时人数统计情况
    国内和海外
    https://news.163.com/special/epidemic/?spssid=93326430940df93a37229666dfbc4b96&spsw=4&spss=other&#map_block
    https://news.163.com/special/epidemic/?spssid=93326430940df93a37229666dfbc4b96&spsw=4&spss=other&
    :return: 返回国内各地区和海外地区情况
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

    url = "https://news.163.com/special/epidemic/"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    data_info_df = pd.DataFrame([item.text.strip().split(".")[1] for item in
                                 soup.find("div", attrs={"class": "data_tip_pop_text"}).find_all("p")])

    hist_today_df = pd.DataFrame([item["today"] for item in data_json["data"]["chinaDayList"]],
                                 index=[item["date"] for item in data_json["data"]["chinaDayList"]])
    hist_total_df = pd.DataFrame([item["total"] for item in data_json["data"]["chinaDayList"]],
                                 index=[item["date"] for item in data_json["data"]["chinaDayList"]])

    current_df = pd.DataFrame.from_dict(data_json["data"]["chinaTotal"])

    outside_today_df = pd.DataFrame([item["today"] for item in data_json["data"]["areaTree"]],
                                    index=[item["name"] for item in data_json["data"]["areaTree"]])
    outside_hist_df = pd.DataFrame([item["total"] for item in data_json["data"]["areaTree"]],
                                   index=[item["name"] for item in data_json["data"]["areaTree"]])

    province_hist_df = pd.DataFrame([item["total"] for item in data_json["data"]["areaTree"][0]["children"]],
                                    index=[item["name"] for item in data_json["data"]["areaTree"][0]["children"]])

    if indicator == "实时":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return current_df
    if indicator == "数据说明":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return data_info_df
    if indicator == "省份":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return province_hist_df
    elif indicator == "历史":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return hist_total_df
    elif indicator == "国家":
        print(f"数据更新时间: {data_json['data']['lastUpdateTime']}")
        return outside_hist_df


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
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    # news
    text_data_news = str(soup.find_all("script", attrs={"id": "getTimelineService"}))
    temp_json = text_data_news[
                text_data_news.find("= [{") + 2: text_data_news.rfind("}catch")
                ]
    json_data = pd.DataFrame(json.loads(temp_json))
    desc_data = json_data[
        ["title", "summary", "infoSource", "provinceName", "sourceUrl"]
    ]
    # data-domestic
    data_text = str(soup.find("script", attrs={"id": "getAreaStat"}))
    data_text_json = json.loads(
        data_text[data_text.find("= [{") + 2: data_text.rfind("catch") - 1]
    )
    data_df = pd.DataFrame(data_text_json).iloc[:, :7]
    data_df.columns = ["地区", "地区简称", "现存确诊", "累计确诊", "-", "治愈", "死亡"]
    country_df = data_df[["地区", "地区简称", "现存确诊", "累计确诊", "治愈", "死亡"]]
    # data-global
    data_text = str(soup.find("script", attrs={"id": "getListByCountryTypeService2"}))
    data_text_json = json.loads(
        data_text[data_text.find("= [{") + 2: data_text.rfind("catch") - 1]
    )
    global_df = pd.DataFrame(data_text_json)
    # info
    dxy_static = soup.find(attrs={"id": "getStatisticsService"}).get_text()
    data_json = json.loads(dxy_static[dxy_static.find("= {") + 2: dxy_static.rfind("}c")])
    info_df = pd.DataFrame([time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_json["modifyTime"] / 1000)),
                            data_json["currentConfirmedCount"],
                            data_json["confirmedCount"],
                            data_json["suspectedCount"],
                            data_json["curedCount"],
                            data_json["deadCount"],
                            data_json["seriousCount"],
                            ], index=["数据发布时间", "现存确诊", "累计确诊", "现存疑似", "治愈", "死亡", "现存重症"])
    # hospital
    url = (
        "https://assets.dxycdn.com/gitrepo/tod-assets/output/default/pneumonia/index.js"
    )
    payload = {"t": str(int(time.time()))}
    r = requests.get(url, params=payload)
    hospital_df = pd.read_html(r.text)[0].iloc[:, :-1]
    if indicator == "全国":
        return country_df
    elif indicator == "global":
        return global_df
    elif indicator == "info":
        return info_df
    elif indicator == "hospital":
        return hospital_df
    elif indicator == "全国-疫情新增趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["quanguoTrendChart"][0]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "全国-疫情疑似-确诊趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["quanguoTrendChart"][1]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "全国-疫情死亡-治愈病例趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["quanguoTrendChart"][2]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "全国-疫情病死率-治愈率趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["quanguoTrendChart"][3]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "湖北-疫情新增确诊病例趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["hbFeiHbTrendChart"][0]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "湖北-疫情确诊趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["hbFeiHbTrendChart"][1]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "湖北-疫情死亡-治愈病例趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["hbFeiHbTrendChart"][2]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "湖北-疫情病死率趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["hbFeiHbTrendChart"][3]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "湖北-疫情治愈率趋势图":
        img_file = Image.open(
            BytesIO(requests.get(data_json["hbFeiHbTrendChart"][4]["imgUrl"]).content)
        )
        img_file.show()
    elif indicator == "疫情地图":
        # img
        img_url = pd.read_json(
            dxy_static[dxy_static.find("= {") + 2: dxy_static.rfind("}catch")],
            orient="index",
        ).T
        img_file = Image.open(
            BytesIO(requests.get(img_url["imgUrl"].values[0]).content)
        )
        img_file.show()
    elif indicator == "news":
        return desc_data
    else:
        try:
            data_text = str(soup.find("script", attrs={"id": "getAreaStat"}))
            data_text_json = json.loads(
                data_text[data_text.find("= [{") + 2: data_text.rfind("catch") - 1]
            )
            data_df = pd.DataFrame(data_text_json)
            sub_area = pd.DataFrame(data_df[data_df["provinceName"] == indicator]["cities"].values[0])
            if sub_area.empty:
                return print("暂无分区域数据")
            sub_area.columns = ["区域", "现在确诊人数", "确诊人数", "疑似人数", "治愈人数", "死亡人数", "id"]
            sub_area = sub_area[["区域", "现在确诊人数", "确诊人数", "疑似人数", "治愈人数", "死亡人数"]]
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
    json_data_news = json.loads(text_data.strip("/**/jsonp_1580470773343_11183(").rstrip(");"))

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
    json_data = json.loads(r.text[r.text.find("({") + 1:r.text.rfind(");")])
    spot_report = pd.DataFrame(json_data["Result"][0]["DisplayData"]["result"]["items"])

    url = "https://mss0.bdstatic.com/se/static/act/captain/bundles/458/a6dc3abe.65e7e794.js"
    r = requests.get(url)
    text_data = r.text
    json_data = demjson.decode(text_data[text_data.find('type:"object"') - 1: text_data.find('t.default=r') - 2])
    domestic_df = pd.DataFrame.from_dict(json_data["properties"]["summaryDataIn"]["properties"], orient="index")
    spot_df = pd.DataFrame.from_dict(json_data["properties"]["summaryDataIn"]["default"], orient="index")
    domestic_df = pd.DataFrame.from_dict(json_data["properties"]["caseList"]["default"])
    out_df = pd.DataFrame.from_dict(json_data["properties"]["caseOutsideList"]["default"])

    temp_df = pd.DataFrame([pd.DataFrame.from_dict(json_data["properties"]["trend"]["default"]["list"])["data"][0],
                            pd.DataFrame.from_dict(json_data["properties"]["trend"]["default"]["list"])["data"][1],
                            pd.DataFrame.from_dict(json_data["properties"]["trend"]["default"]["list"])["data"][2],
                            pd.DataFrame.from_dict(json_data["properties"]["trend"]["default"]["list"])["data"][3],
                            pd.DataFrame.from_dict(json_data["properties"]["trend"]["default"]["list"])["data"][4],
                            pd.DataFrame.from_dict(json_data["properties"]["trend"]["default"]["list"])["data"][5]],
                           index=pd.DataFrame.from_dict(json_data["properties"]["trend"]["default"]["list"])[
                               "name"].to_list(),
                           columns=json_data["properties"]["trend"]["default"]["updateDate"])

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
    elif indicator == "实时播报":
        return spot_report
    elif indicator == "实时":
        return spot_df
    elif indicator == "历史":
        return temp_df
    elif indicator == "国内":
        return domestic_df
    elif indicator == "国外":
        return out_df
    else:
        return pd.DataFrame(domestic_df[domestic_df.area == indicator]["subList"].to_list()[0])


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
    json_data = json.loads(r.text[r.text.find("({") + 1:r.text.rfind(");")])
    return pd.DataFrame(json_data["data"]["list"])


def migration_scale_baidu(area="乌鲁木齐市", indicator="move_out", start_date="20190112", end_date="20200201"):
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
    json_data = json.loads(r.text[r.text.find("({") + 1:r.text.rfind(");")])
    temp_df = pd.DataFrame.from_dict(json_data["data"]["list"], orient="index")
    temp_df.index = pd.to_datetime(temp_df.index)
    temp_df.columns = ["迁徙规模指数"]
    return temp_df


def epidemic_area_search(province="四川省", city="成都市", district="高新区"):
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
    return temp_df[["province", "city", "district", "show_address", "full_address", "cnt_sum_certain"]]


def epidemic_area_all():
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
            temp.extend(list(zip([p] * len(list(area[p][c].keys())[1:]), [c] * len(list(area[p][c].keys())[1:]),
                                 list(area[p][c].keys())[1:])))
    return pd.DataFrame(temp, columns=["province", "city", "district"])


def epidemic_area_detail():
    """
    细化到每个小区的确诊人数
    需要遍历每个页面, 如非必要, 请勿运行
    https://ncov.html5.qq.com/community?channelid=1&from=singlemessage&isappinstalled=0
    :return: 全国每个小区的确诊人数
    :rtype: pandas.DataFrame
    """
    temp_df = pd.DataFrame()
    area_df = epidemic_area_all()
    for item in area_df.iterrows():
        print(f"一共{area_df.shape[0]}, 正在下载第{item[0] + 1}页")
        small_df = epidemic_area_search(province=item[1][0], city=item[1][1], district=item[1][2])
        temp_df = temp_df.append(small_df, ignore_index=True)
    return temp_df


def epidemic_trip():
    """
    新型肺炎确诊患者-相同行程查询工具
    https://rl.inews.qq.com/h5/trip?from=newsapp&ADTAG=tgi.wx.share.message
    :return: 新型肺炎确诊患者-相同行程查询工具的所有历史数据
    :rtype: pandas.DataFrame
    """
    url = "https://rl.inews.qq.com/taf/travelFront"
    r = requests.get(url)
    return pd.DataFrame(r.json()["data"]["list"])


def epidemic_hist_all() -> pd.DataFrame:
    """
    返回丁香园的数据
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


def epidemic_hist_city(city: str = "武汉市") -> pd.DataFrame:
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


def epidemic_hist_province(province: str = "湖北省") -> pd.DataFrame:
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
    return data_df[data_df["province"] == province]


def epidemic_history() -> pd.DataFrame:
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
    epidemic_current_163_df = epidemic_163(indicator="实时")
    print(epidemic_current_163_df)
    epidemic_info_163_df = epidemic_163(indicator="数据说明")
    print(epidemic_info_163_df)
    epidemic_hist_163_df = epidemic_163(indicator="省份")
    print(epidemic_hist_163_df)
    epidemic_area_163_df = epidemic_163(indicator="历史")
    print(epidemic_area_163_df)
    epidemic_outside_163_df = epidemic_163(indicator="国家")
    print(epidemic_outside_163_df)
    # dxy
    epidemic_dxy_country_df = epidemic_dxy(indicator="全国")
    print(epidemic_dxy_country_df)
    epidemic_dxy_global_df = epidemic_dxy(indicator="global")
    print(epidemic_dxy_global_df)
    epidemic_dxy_province_df = epidemic_dxy(indicator="浙江省")
    print(epidemic_dxy_province_df)
    epidemic_dxy_info_df = epidemic_dxy(indicator="info")
    print(epidemic_dxy_info_df)
    epidemic_dxy_hospital_df = epidemic_dxy(indicator="hospital")
    print(epidemic_dxy_hospital_df)
    epidemic_dxy_news_df = epidemic_dxy(indicator="news")
    print(epidemic_dxy_news_df)
    epidemic_dxy(indicator="全国-疫情新增趋势图")
    epidemic_dxy(indicator="全国-疫情疑似-确诊趋势图")
    epidemic_dxy(indicator="全国-疫情新增死亡-治愈病例趋势图")
    epidemic_dxy(indicator="全国-疫情死亡-治愈病例趋势图")
    epidemic_dxy(indicator="全国-疫情病死率-治愈率趋势图")
    epidemic_dxy(indicator="湖北-疫情新增确诊病例趋势图")
    epidemic_dxy(indicator="湖北-疫情确诊趋势图")
    epidemic_dxy(indicator="湖北-疫情死亡-治愈病例趋势图")
    epidemic_dxy(indicator="湖北-疫情病死率趋势图")
    epidemic_dxy(indicator="湖北-疫情治愈率趋势图")
    epidemic_dxy(indicator="疫情地图")
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
    migration_area_baidu_df = migration_area_baidu(area="上海市", indicator="move_in", date="20200212")
    # print(migration_area_baidu_df.to_csv("迁入上海市来源地-20200218.csv", encoding="gb2312"))
    print(migration_area_baidu_df)
    migration_scale_baidu_df = migration_scale_baidu(area="上海市", indicator="move_in", start_date="20190113",
                                                     end_date="20200212")
    # print(migration_scale_baidu_df.to_csv("迁入上海市2019-2020统计-20200218.csv", encoding="gb2312"))
    print(migration_scale_baidu_df)
    # 小区
    epidemic_area_search_df = epidemic_area_search(province="四川省", city="成都市", district="高新区")
    print(epidemic_area_search_df)
    epidemic_area_all_df = epidemic_area_all()
    print(epidemic_area_all_df)
    # epidemic_area_detail_df = epidemic_area_detail()
    # print(epidemic_area_detail_df)
    # print(epidemic_area_detail_df.to_csv("所有疫情地点-20200218.csv", encoding="gbk"))
    # 行程
    epidemic_trip_df = epidemic_trip()
    print(epidemic_trip_df)
    # 历史数据
    epidemic_hist_all_df = epidemic_hist_all()
    print(epidemic_hist_all_df)
    epidemic_hist_city_df = epidemic_hist_city(city="武汉市")
    print(epidemic_hist_city_df)
    epidemic_hist_province_df = epidemic_hist_province(province="湖北省")
    print(epidemic_hist_province_df)
    # 详细历史数据
    epidemic_history_df = epidemic_history()
    print(epidemic_history_df)
