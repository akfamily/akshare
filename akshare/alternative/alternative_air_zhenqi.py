#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: 真气网-空气质量
https://www.zq12369.com/environment.php
空气质量在线监测分析平台的空气质量数据
https://www.aqistudy.cn/
"""

from akshare.datasets import get_data_file
import re
import warnings
from io import StringIO

import pandas as pd
from py_mini_racer import MiniRacer

from akshare.exceptions import APIError, DataParsingError
from akshare.utils import jsonish
from akshare.utils import http


def _get_js_path(name: str = None, module_file: str = None) -> str:
    """
    获取 JS 文件的路径（从模块所在目录查找）
    :param name: 文件名
    :type name: str
    :param module_file: 模块路径
    :type module_file: str
    :return: 路径
    :rtype: str
    """
    module_json_path = str(get_data_file(name))
    return module_json_path


def _get_file_content(file_name: str = "crypto.js") -> str:
    """
    获取 JS 文件的内容
    :param file_name:  JS 文件名
    :type file_name: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_name = file_name
    setting_file_path = _get_js_path(setting_file_name, __file__)
    with open(setting_file_path, encoding="utf-8") as f:
        file_data = f.read()
    return file_data


def has_month_data(href):
    """
    Deal with href node
    :param href: href
    :type href: str
    :return: href result
    :rtype: str
    """
    return href and re.compile("monthdata.php").search(href)


def air_city_table() -> pd.DataFrame:
    """
    真气网-空气质量历史数据查询-全部城市列表
    https://www.zq12369.com/environment.php?date=2019-06-05&tab=rank&order=DESC&type=DAY#rank
    :return: 城市映射
    :rtype: pandas.DataFrame
    """
    url = "https://www.zq12369.com/environment.php"
    date = "2020-05-01"
    temp_df = None
    if len(date.split("-")) == 3:
        params = {
            "date": date,
            "tab": "rank",
            "order": "DESC",
            "type": "DAY",
        }
        r = http.get(url, params=params)
        temp_df = pd.read_html(StringIO(r.text))[1].iloc[1:, :]
        del temp_df["降序"]
        temp_df = temp_df.reset_index()
        temp_df["index"] = temp_df.index + 1
        temp_df.columns = [
            "序号",
            "省份",
            "城市",
            "AQI",
            "空气质量",
            "PM2.5浓度",
            "首要污染物",
        ]
        temp_df["AQI"] = pd.to_numeric(temp_df["AQI"])
    return temp_df


def air_quality_watch_point(
    city: str = "杭州", start_date: str = "20220408", end_date: str = "20220409"
) -> pd.DataFrame:
    """
    真气网-监测点空气质量-细化到具体城市的每个监测点
    指定之间段之间的空气质量数据
    https://www.zq12369.com/
    :param city: 调用 ak.air_city_table() 接口获取
    :type city: str
    :param start_date: e.g., "20190327"
    :type start_date: str
    :param end_date: e.g., ""20200327""
    :type end_date: str
    :return: 指定城市指定日期区间的观测点空气质量
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "https://www.zq12369.com/api/zhenqiapi.php"
    file_data = _get_file_content(file_name="crypto.js")
    ctx = MiniRacer()
    ctx.eval(file_data)
    method = "GETCITYPOINTAVG"
    city_param = ctx.call("encode_param", city)
    payload = {
        "appId": "a01901d3caba1f362d69474674ce477f",
        "method": ctx.call("encode_param", method),
        "city": city_param,
        "startTime": ctx.call("encode_param", start_date),
        "endTime": ctx.call("encode_param", end_date),
        "secret": ctx.call("encode_secret", method, city_param, start_date, end_date),
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/81.0.4044.122 Safari/537.36"
    }
    r = http.post(url, data=payload, headers=headers)
    data_text = r.text
    data_json = jsonish.loads(ctx.call("decode_result", data_text))
    temp_df = pd.DataFrame(data_json["rows"])
    return temp_df


def _zhenqi_page_keys() -> dict:
    """
    读取真气网首页内联脚本中的加解密密钥 akb33、akb34、akb35、akb36、akb48
    站点会更换这些值，因此每次调用时读取，不写死在代码中
    :return: 变量名到值的映射
    :rtype: dict
    :raises DataParsingError: 页面中未找到密钥
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0.0.0 Safari/537.36",
    }
    r = http.get("https://www.zq12369.com/", headers=headers)
    keys = dict(re.findall(r'var (akb\d+)\s*=\s*"([^"]*)"', r.text))
    missing = {"akb33", "akb34", "akb35", "akb36", "akb48"} - keys.keys()
    if missing:
        raise DataParsingError(
            f"真气网首页中未找到加密密钥 {sorted(missing)}，上游可能已改版"
        )
    return keys


def air_quality_hist(
    city: str = "杭州",
    period: str = "day",
    start_date: str = "20260901",
    end_date: str = "20261028",
) -> pd.DataFrame:
    """
    真气网-空气历史数据
    https://www.zq12369.com/
    上游只提供最近约一年的数据，更早的日期返回空表
    :param city: 调用 ak.air_city_table() 接口获取所有城市列表
    :type city: str
    :param period: "hour": 每小时一个数据，由于数据量比较大，下载较慢；"day": 每天一个数据；"month": 每个月一个数据，上游目前返回其他城市的数据，会报错
    :type period: str
    :param start_date: e.g., "20260901"
    :type start_date: str
    :param end_date: e.g., "20261028"
    :type end_date: str
    :return: 指定城市和数据频率下在指定时间段内的空气质量数据
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    # 2026-10 起站点改为按 akb33 决定加密顺序、密钥写在页面里；原先内置的
    # encode_param 写死了旧顺序与旧密钥，服务端无法解密请求，返回的内容也解不开
    keys = _zhenqi_page_keys()
    ctx = MiniRacer()
    ctx.eval(_get_file_content(file_name="crypto.js"))
    ctx.eval("".join(f'var {k} = "{v}";\n' for k, v in keys.items()))
    ctx.eval("var b = new Base64();\n" + _get_file_content(file_name="outcrypto.js"))
    obj = {
        "city": city,
        "type": period.upper(),
        "startTime": f"{start_date} 00:00:00",
        "endTime": f"{end_date} 23:45:39",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.zq12369.com/",
    }
    r = http.post(
        "https://www.zq12369.com/api/newzhenqiapi.php",
        data={"param": ctx.call("getParam", "CETCITYPERIOD", obj)},
        headers=headers,
    )
    data_json = jsonish.loads(ctx.call("b.decode", ctx.call("decryptData", r.text)))
    if not data_json.get("success"):
        raise APIError(f"真气网返回错误：{data_json.get('errmsg')}")
    rows = data_json["result"]["data"]["rows"]
    if not rows:
        warnings.warn(
            "真气网未返回数据；上游只提供最近约一年的数据，请检查日期范围与城市名称"
        )
        return pd.DataFrame()
    temp_df = pd.DataFrame(rows)
    # 2026-10 实测月度数据无论请求哪个城市、哪个时段，都返回郑州 2021-08～2022-08，
    # 返回其他城市的数据比报错更糟，因此城市名不符时直接报错
    if "cityname" in temp_df.columns and not (temp_df["cityname"] == city).all():
        returned = "、".join(temp_df["cityname"].astype(str).unique()[:3])
        raise APIError(
            f"真气网返回的是{returned}的数据而非{city}，上游数据有误；"
            "月度数据可改用 period='day' 后自行按月汇总"
        )
    temp_df.index = temp_df["time"]
    del temp_df["time"]
    temp_df = temp_df.astype(float, errors="ignore")
    return temp_df


def air_quality_rank(date: str = "") -> pd.DataFrame:
    """
    真气网-168 城市 AQI 排行榜
    https://www.zq12369.com/environment.php?date=2020-03-12&tab=rank&order=DESC&type=DAY#rank
    :param date: "": 当前时刻空气质量排名；"20200312": 当日空气质量排名；"202003": 当月空气质量排名；"2019": 当年空气质量排名；
    :type date: str
    :return: 指定 date 类型的空气质量排名数据
    :rtype: pandas.DataFrame
    """
    if len(date) == 4:
        date = date
    elif len(date) == 6:
        date = "-".join([date[:4], date[4:6]])
    elif date == "":
        date = "实时"
    else:
        date = "-".join([date[:4], date[4:6], date[6:]])

    url = "https://www.zq12369.com/environment.php"

    if len(date.split("-")) == 3:
        params = {
            "date": date,
            "tab": "rank",
            "order": "DESC",
            "type": "DAY",
        }
        r = http.get(url, params=params)
        return pd.read_html(StringIO(r.text))[1].iloc[1:, :]
    elif len(date.split("-")) == 2:
        params = {
            "month": date,
            "tab": "rank",
            "order": "DESC",
            "type": "MONTH",
        }
        r = http.get(url, params=params)
        return pd.read_html(StringIO(r.text))[2].iloc[1:, :]
    elif len(date.split("-")) == 1 and date != "实时":
        params = {
            "year": date,
            "tab": "rank",
            "order": "DESC",
            "type": "YEAR",
        }
        r = http.get(url, params=params)
        return pd.read_html(StringIO(r.text))[3].iloc[1:, :]
    if date == "实时":
        params = {
            "tab": "rank",
            "order": "DESC",
            "type": "MONTH",
        }
        r = http.get(url, params=params)
        return pd.read_html(StringIO(r.text))[0].iloc[1:, :]


if __name__ == "__main__":
    air_city_table_df = air_city_table()
    print(air_city_table_df)

    air_quality_watch_point_df = air_quality_watch_point(
        city="杭州", start_date="20220408", end_date="20220409"
    )
    print(air_quality_watch_point_df)

    air_quality_hist_df = air_quality_hist(
        city="北京",
        period="day",
        start_date="20260901",
        end_date="20261028",
    )
    print(air_quality_hist_df)

    air_quality_rank_df = air_quality_rank()
    print(air_quality_rank_df)
