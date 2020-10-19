# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/10/18 20:29
Desc: 电影票房数据
https://www.endata.com.cn/BoxOffice/BO/RealTime/reTimeBO.html
"""
import datetime
import json
import os

import pandas as pd
import requests
from py_mini_racer import py_mini_racer


def _get_js_path(name, module_file):
    """
    获取 JS 文件的路径(从模块所在目录查找)
    :param name: 文件名
    :param module_file: filename
    :return: str json_file_path
    """
    module_folder = os.path.abspath(os.path.dirname(os.path.dirname(module_file)))
    module_json_path = os.path.join(module_folder, "movie", name)
    return module_json_path


def _get_file_content(file_name="jm.js"):
    """
    读取文件内容
    :return: str
    """
    setting_file_name = file_name
    setting_file_path = _get_js_path(setting_file_name, __file__)
    with open(setting_file_path) as f:
        file_data = f.read()
    return file_data


def get_current_week(date="20201019"):
    """
    当前周的周一
    :return: 当前周的周一
    :rtype: datetime.date
    """
    monday = datetime.datetime.strptime(date, "%Y%m%d").date()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    return monday


def decrypt(origin_data):
    """
    解密
    :param origin_data:
    :type origin_data:
    :return:
    :rtype:
    """
    file_data = _get_file_content(file_name="jm.js")
    ctx = py_mini_racer.MiniRacer()
    ctx.eval(file_data)
    data = ctx.call("webInstace.shell", origin_data)
    return data


def movie_boxoffice(date: str = "20201019", indicator: str = "实时票房") -> pd.DataFrame:
    """
    电影票房数据
    https://www.endata.com.cn/BoxOffice/BO/RealTime/reTimeBO.html
    :param date: 指定日期
    :type date: str
    :param indicator: choice of ["实时票房", "单日票房", "单周票房", "单月票房", "年度票房", "影院票房"]
    :type indicator: str
    :return: 电影票房数据
    :rtype: pandas.DataFrame
    """
    last_date = datetime.datetime.strptime(date, "%Y%m%d") - datetime.timedelta(days=1)
    last_date = last_date.strftime("%Y%m%d")
    url = "https://www.endata.com.cn/API/GetData.ashx"
    if indicator == "实时票房":
        payload = {
            "showDate": "",
            "tdate": f"{date[:4]}-{date[4:6]}-{date[6:]}",
            "MethodName": "BoxOffice_GetHourBoxOffice",
        }
        r = requests.post(url, data=payload)
        r.encoding = "utf8"
        data_json = json.loads(decrypt(r.text))
        temp_df = pd.DataFrame(data_json["Data"]["Table1"])
        temp_df = temp_df.iloc[:, :7]
        temp_df.columns = ["排序", "_", "影片名称", "实时票房", "累计票房", "上映天数", "票房占比"]
        temp_df = temp_df[["排序", "影片名称", "实时票房", "票房占比", "上映天数", "累计票房"]]
        return temp_df
    elif indicator == "单日票房":
        payload = {
            "sdate": f"{date[:4]}-{date[4:6]}-{date[6:]}",
            "edate": f"{last_date[:4]}-{last_date[4:6]}-{last_date[6:]}",
            "MethodName": "BoxOffice_GetDayBoxOffice",
        }
        r = requests.post(url, data=payload)
        r.encoding = "utf8"
        data_json = json.loads(decrypt(r.text))
        temp_df = pd.DataFrame(data_json["Data"]["Table"])
        temp_df.columns = ["排序", "_", "影片名称", "_", "累计票房", "平均票价", "上映天数", "场均人次", "_", "_", "_", "_", "_", "单日票房", "环比变化", "_", "口碑指数"]
        temp_df = temp_df[["排序", "影片名称", "环比变化", "单日票房", "累计票房", "平均票价", "场均人次", "口碑指数", "上映天数"]]
        return temp_df
    elif indicator == "单周票房":
        payload = {
            "sdate": get_current_week(date="20201010").strftime("%Y-%m-%d"),
            "MethodName": "BoxOffice_GetWeekInfoData",
        }
        r = requests.post(url, data=payload)
        r.encoding = "utf8"
        data_json = json.loads(decrypt(r.text))
        temp_df = pd.DataFrame(data_json["Data"]["Table"])
        temp_df.columns = ["排序", "_", "影片名称", "单周票房", "累计票房", "_", "上映天数", "平均票价", "场均人次", "环比变化", "_", "_", "_", "排名变化", "口碑指数"]
        temp_df = temp_df[["排序", "影片名称", "排名变化", "单周票房", "环比变化", "累计票房", "平均票价", "场均人次", "口碑指数", "上映天数"]]
        return temp_df
    elif indicator == "单月票房":
        payload = {
            "startTime": f"{date[:4]}-{date[4:6]}-01",
            "MethodName": "BoxOffice_GetMonthBox",
        }
        r = requests.post(url, data=payload)
        r.encoding = "utf8"
        data_json = json.loads(decrypt(r.text))
        temp_df = pd.DataFrame(data_json["Data"]["Table"])
        temp_df.columns = ["排序", "_", "影片名称", "月内天数", "单月票房", "平均票价", "场均人次", "月度占比", "上映日期", "_", "口碑指数"]
        temp_df = temp_df[["排序", "影片名称", "单月票房", "月度占比", "平均票价", "场均人次", "上映日期", "口碑指数", "月内天数"]]
        return temp_df
    elif indicator == "年度票房":
        payload = {
            "year": f"{date[:4]}",
            "MethodName": "BoxOffice_GetYearInfoData",
        }
        r = requests.post(url, data=payload)
        r.encoding = "utf8"
        data_json = json.loads(decrypt(r.text))
        temp_df = pd.DataFrame(data_json["Data"]["Table"])
        temp_df.reset_index(inplace=True)
        temp_df.columns = ["排序", "_", "影片名称", "类型", "总票房", "平均票价", "场均人次", "国家及地区", "上映日期", "_"]
        temp_df = temp_df[["影片名称", "类型", "总票房", "平均票价", "场均人次", "国家及地区", "上映日期"]]
        return temp_df
    elif indicator == "影院票房":
        payload = {
            "rowNum1": "1",
            "rowNum2": "100",
            "date": "2020-10-17",
            "MethodName": "BoxOffice_GetCinemaDayBoxOffice",
        }
    r = requests.post(url, data=payload)
    r.encoding = "utf8"
    data_json = json.loads(decrypt(r.text))
    temp_df = pd.DataFrame(data_json["Data"]["Table"])
    temp_df.columns = ["排序", "_", "影院名称", "单日票房", "单日场次", "_", "_", "场均票价", "场均人次", "上座率"]
    temp_df = temp_df[["排序", "影院名称", "单日票房", "单日场次", "场均人次", "场均票价", "上座率"]]
    return temp_df


if __name__ == "__main__":
    movie_boxoffice_df = movie_boxoffice(date="20201019", indicator="实时票房")
    print(movie_boxoffice_df)

    movie_boxoffice_df = movie_boxoffice(date="20201018", indicator="单日票房")
    print(movie_boxoffice_df)

    movie_boxoffice_df = movie_boxoffice(date="20201010", indicator="单周票房")
    print(movie_boxoffice_df)

    movie_boxoffice_df = movie_boxoffice(date="20201010", indicator="单月票房")
    print(movie_boxoffice_df)

    movie_boxoffice_df = movie_boxoffice(date="20201010", indicator="年度票房")
    print(movie_boxoffice_df)

    movie_boxoffice_df = movie_boxoffice(indicator="影院票房")
    print(movie_boxoffice_df)
