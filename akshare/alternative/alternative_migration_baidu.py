#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/5/12 22:30
Desc: 百度地图慧眼-百度迁徙数据
"""

import datetime
import json

import pandas as pd

from akshare.alternative.alternative_migration_cons import province_dict, city_dict
from akshare.exceptions import InvalidParameterError
from akshare.utils import http


def alternative_migration_area_baidu(
    area: str = "重庆市", indicator: str = "move_in", date: str = ""
) -> pd.DataFrame:
    """
    百度地图慧眼-百度迁徙-XXX迁入地详情
    百度地图慧眼-百度迁徙-XXX迁出地详情
    以上展示 top100 结果，如不够 100 则展示全部
    迁入来源地比例：从 xx 地迁入到当前区域的人数与当前区域迁入总人口的比值
    迁出目的地比例：从当前区域迁出到 xx 的人口与从当前区域迁出总人口的比值
    https://qianxi.baidu.com/?from=shoubai#city=0
    :param area: 可以输入 省份 或者 具体城市 但是需要用全称
    :type area: str
    :param indicator: move_in 迁入 move_out 迁出
    :type indicator: str
    :param date: 查询的日期，如 20261110；默认为空，取最近一个有数据的日期（百度通常滞后 2～3 天）
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
    if date:
        dates = [date]
    else:
        today = datetime.date.today()
        dates = [
            (today - datetime.timedelta(days=offset)).strftime("%Y%m%d")
            for offset in range(1, 8)
        ]
    for item in dates:
        params = {
            "dt": dt_flag,
            "id": inner_dict[area],
            "type": indicator,
            "date": item,
        }
        r = http.get(url, params=params)
        data_text = r.text[r.text.find("({") + 1 : r.text.rfind(");")]
        data_json = json.loads(data_text)
        if data_json["data"]["list"]:
            temp_df = pd.DataFrame(data_json["data"]["list"])
            temp_df["value"] = pd.to_numeric(temp_df["value"], errors="coerce")
            return temp_df
    raise InvalidParameterError(
        f"百度迁徙没有 {area} 在 {date or '最近 7 天'} 的数据；"
        "当天和前一两天的数据尚未发布，过早的日期也已不提供"
    )


def alternative_migration_scale_baidu(
    area: str = "广州市",
    indicator: str = "move_in",
) -> pd.DataFrame:
    """
    百度地图慧眼-百度迁徙-迁徙规模
    迁徙规模指数：反映迁入或迁出人口规模，城市间可横向对比城市迁徙边界采用该城市行政区划，包含该城市管辖的区、县、乡、村
    https://qianxi.baidu.com/?from=shoubai#city=0
    :param area: 可以输入 省份 或者 具体城市 但是需要用全称
    :type area: str
    :param indicator: move_in 迁入 move_out 迁出
    :type indicator: str
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
    }
    r = http.get(url, params=params)
    json_data = json.loads(r.text[r.text.find("({") + 1 : r.text.rfind(");")])
    temp_df = pd.DataFrame.from_dict(json_data["data"]["list"], orient="index")
    temp_df.index = pd.to_datetime(temp_df.index)
    temp_df = temp_df.reset_index()
    temp_df.columns = ["日期", "迁徙规模指数"]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    temp_df["迁徙规模指数"] = pd.to_numeric(temp_df["迁徙规模指数"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    alternative_migration_area_baidu_df = alternative_migration_area_baidu(
        area="杭州市", indicator="move_out", date="20240401"
    )
    print(alternative_migration_area_baidu_df)

    alternative_migration_scale_baidu_df = alternative_migration_scale_baidu(
        area="广州市",
        indicator="move_in",
    )
    print(alternative_migration_scale_baidu_df)
