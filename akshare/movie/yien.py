# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/10/18 23:29
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
    data = ctx.call('webInstace.shell', origin_data)
    return data


def movie_boxoffice(date="20201019", indicator="实时票房"):
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
        return temp_df.iloc[:, :5]
    elif indicator == "单日票房":
        payload = {
            "sdate": f"{date[:4]}-{date[4:6]}-{date[6:]}",
            "edate": f"{last_date[:4]}-{last_date[4:6]}-{last_date[6:]}",
            "MethodName": "BoxOffice_GetDayBoxOffice",
        }
    elif indicator == "单周票房":
        payload = {
            "sdate": get_current_week(date="20201010").strftime("%Y-%m-%d"),
            "MethodName": "BoxOffice_GetWeekInfoData"
        }
    elif indicator == "单月票房":
        payload = {
            "startTime": f"{date[:4]}-{date[4:6]}-01",
            "MethodName": "BoxOffice_GetMonthBox"
        }
    elif indicator == "年度票房":
        payload = {
            "year": f"{date[:4]}",
            "MethodName": "BoxOffice_GetYearInfoData",
        }
        r = requests.post(url, data=payload)
        r.encoding = "utf8"
        data_json = json.loads(decrypt(r.text))
        temp_df = pd.DataFrame(data_json["Data"]["Table"])
        return temp_df.iloc[:, :-1]
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
    return temp_df


if __name__ == '__main__':
    movie_boxoffice_df = movie_boxoffice(date="20201019", indicator="实时票房")
    print(movie_boxoffice_df)

    movie_boxoffice_df = movie_boxoffice(date="20201019", indicator="单日票房")
    print(movie_boxoffice_df)

    movie_boxoffice_df = movie_boxoffice(date="20201010", indicator="单周票房")
    print(movie_boxoffice_df)

    movie_boxoffice_df = movie_boxoffice(date="20201010", indicator="单月票房")
    print(movie_boxoffice_df)

    movie_boxoffice_df = movie_boxoffice(date="20201010", indicator="年度票房")
    print(movie_boxoffice_df)

    movie_boxoffice_df = movie_boxoffice(indicator="影院票房")
    print(movie_boxoffice_df)
