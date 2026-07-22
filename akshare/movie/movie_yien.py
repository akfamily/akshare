#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/2/20 14:00
Desc: 电影票房数据
https://ys.endata.cn/BoxOffice/Movie
"""

import datetime
import os
import random

import pandas as pd
import requests
import py_mini_racer

from akshare.exceptions import APIError


def _get_js_path(name: str = "", module_file: str = "") -> str:
    """
    get JS file path
    :param name: file name
    :type name: str
    :param module_file: filename
    :type module_file: str
    :return: 路径
    :rtype: str
    """
    module_folder = os.path.abspath(os.path.dirname(os.path.dirname(module_file)))
    module_json_path = os.path.join(module_folder, "movie", name)
    return module_json_path


def _get_file_content(file_name: str = "jm.js"):
    """
    read the file content
    :param file_name: filename
    :type file_name: str
    :return: file content
    :rtype: str
    """
    setting_file_name = file_name
    setting_file_path = _get_js_path(setting_file_name, __file__)
    with open(setting_file_path) as f:
        file_data = f.read()
    return file_data


def get_current_week(date: str = "20201019") -> datetime.date:
    """
    当前周的周一
    :param date: 具体的日期
    :type date: str
    :return: 当前周的周一
    :rtype: datetime.date
    """
    monday = datetime.datetime.strptime(date, "%Y%m%d").date()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    return monday


def decrypt(origin_data: str = "") -> str:
    """
    解密
    :param origin_data: 解密前的字符串
    :type origin_data: str
    :return: 解密后的字符串
    :rtype: str
    """
    file_data = _get_file_content(file_name="jm.js")
    ctx = py_mini_racer.MiniRacer()
    ctx.eval(file_data)
    data = ctx.call("webInstace.shell", origin_data)
    return data


def _get_endata_headers(referer_path: str) -> dict[str, str]:
    """
    获取艺恩新站接口请求头。

    :param referer_path: 请求对应的页面路径
    :type referer_path: str
    :return: 请求头
    :rtype: dict[str, str]
    """
    return {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://ys.endata.cn",
        "Referer": f"https://ys.endata.cn{referer_path}",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
    }


def _post_endata_json(
    url: str, payload: dict[str, object], referer_path: str
) -> dict[str, object]:
    """
    请求艺恩新站接口并返回 JSON 数据。

    :param url: 接口地址
    :type url: str
    :param payload: 表单请求参数
    :type payload: dict[str, object]
    :param referer_path: 请求页面路径
    :type referer_path: str
    :return: JSON 响应
    :rtype: dict[str, object]
    """
    response = requests.post(
        url,
        data=payload,
        headers=_get_endata_headers(referer_path=referer_path),
        timeout=30,
    )
    response.raise_for_status()
    data_json = response.json()
    if data_json.get("status") != 1:
        raise APIError(
            message=str(data_json.get("des", "艺恩接口返回异常")),
            status_code=data_json.get("status"),
        )
    return data_json


def _fetch_endata_list(
    url: str, payload: dict[str, object], referer_path: str
) -> pd.DataFrame:
    """
    获取艺恩新站分页列表数据。

    :param url: 接口地址
    :type url: str
    :param payload: 表单请求参数
    :type payload: dict[str, object]
    :param referer_path: 请求页面路径
    :type referer_path: str
    :return: 列表数据
    :rtype: pandas.DataFrame
    """
    data_json = _post_endata_json(url=url, payload=payload, referer_path=referer_path)
    temp_df = pd.DataFrame(data_json["data"].get("table1", []))
    total_page = int(
        data_json["data"].get("table2", [{"TotalPage": 1}])[0]["TotalPage"]
    )
    for page in range(2, total_page + 1):
        payload.update({"pageindex": page, "r": random.random()})
        page_json = _post_endata_json(
            url=url, payload=payload, referer_path=referer_path
        )
        page_df = pd.DataFrame(page_json["data"].get("table1", []))
        temp_df = pd.concat([temp_df, page_df], ignore_index=True)
    return temp_df


def _format_date(date: str) -> str:
    """
    格式化日期参数。

    :param date: 原始日期字符串
    :type date: str
    :return: YYYY-MM-DD 格式日期
    :rtype: str
    """
    return datetime.datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")


def _calc_first_week_days(value: object) -> object:
    """
    根据上映日期估算首周天数。

    :param value: 上映日期
    :type value: object
    :return: 首周天数
    :rtype: object
    """
    release_date = pd.to_datetime(value, errors="coerce")
    if pd.isna(release_date):
        return pd.NA
    return 7 - release_date.weekday()


def _raise_week_permission_error(interface_name: str) -> None:
    """
    抛出艺恩周榜权限异常。

    :param interface_name: 接口名称
    :type interface_name: str
    :raises APIError: 当周榜接口需要权限时抛出
    """
    raise APIError(
        message=(
            f"{interface_name} 上游艺恩公开周榜接口当前需要权限或直接返回系统错误, "
            "暂无法匿名获取"
        ),
        status_code=-1,
    )


def movie_boxoffice_realtime() -> pd.DataFrame:
    """
    电影票房-实时票房
    https://ys.endata.cn/BoxOffice/Movie
    :return: 实时票房数据
    :rtype: pandas.DataFrame
    """
    today = datetime.datetime.today().date().strftime("%Y-%m-%d")
    url = "https://ys.endata.cn/enlib-api/api/movie/getMovie_BoxOffice_Day_List.do"
    payload = {
        "r": random.random(),
        "datetype": "Day",
        "date": today,
        "sdate": today,
        "edate": today,
        "bserviceprice": "1",
        "columnslist": "100,102,103,119,105,107,109,106,112,129,142,143,163,164,165",
        "pageindex": 1,
        "pagesize": 20,
        "order": "103",
        "ordertype": "desc",
    }
    temp_df = _fetch_endata_list(
        url=url, payload=payload, referer_path="/BoxOffice/Movie"
    )

    temp_df = temp_df[
        [
            "Irank",
            "MovieName",
            "BoxOffice",
            "BoxOfficePercent",
            "ReleaseDay",
            "TotalBoxOffice",
        ]
    ]
    temp_df.columns = [
        "排序",
        "影片名称",
        "实时票房",
        "票房占比",
        "上映天数",
        "累计票房",
    ]
    temp_df["实时票房"] = pd.to_numeric(temp_df["实时票房"], errors="coerce") / 10000
    temp_df["累计票房"] = pd.to_numeric(temp_df["累计票房"], errors="coerce") / 10000
    temp_df["票房占比"] = pd.to_numeric(temp_df["票房占比"], errors="coerce")
    temp_df["上映天数"] = pd.to_numeric(temp_df["上映天数"], errors="coerce").astype(
        "Int64"
    )
    temp_df["排序"] = pd.to_numeric(temp_df["排序"], errors="coerce").astype("Int64")
    temp_df.sort_values(["排序"], inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df


def movie_boxoffice_daily(date: str = "20240219") -> pd.DataFrame:
    """
    电影票房-单日票房
    https://www.endata.com.cn/BoxOffice/BO/Day/index.html
    :param date: 只能设置当前日期的前一天的票房数据
    :type date: str
    :return: 每日票房
    :rtype: pandas.DataFrame
    """
    date_str = _format_date(date=date)
    url = "https://ys.endata.cn/enlib-api/api/movie/getMovie_BoxOffice_Day_List.do"
    payload = {
        "r": random.random(),
        "datetype": "Day",
        "date": date_str,
        "sdate": date_str,
        "edate": date_str,
        "bserviceprice": "1",
        "columnslist": "100,102,103,146,105,111,113,112,119",
        "pageindex": 1,
        "pagesize": 500,
        "order": "103",
        "ordertype": "desc",
    }
    temp_df = _fetch_endata_list(
        url=url, payload=payload, referer_path="/BoxOffice/Movie"
    )
    temp_df = temp_df[
        [
            "Irank",
            "MovieName",
            "BoxOffice",
            "BoxOfficeMoM",
            "TotalBoxOffice",
            "AvgBoxOffice",
            "AvgShowAudienceCount",
            "ReleaseDay",
        ]
    ]
    temp_df.columns = [
        "排序",
        "影片名称",
        "单日票房",
        "环比变化",
        "累计票房",
        "平均票价",
        "场均人次",
        "上映天数",
    ]
    temp_df["口碑指数"] = pd.NA
    temp_df = temp_df[
        [
            "排序",
            "影片名称",
            "单日票房",
            "环比变化",
            "累计票房",
            "平均票价",
            "场均人次",
            "口碑指数",
            "上映天数",
        ]
    ]
    temp_df["单日票房"] = pd.to_numeric(temp_df["单日票房"], errors="coerce") / 10000
    temp_df["环比变化"] = pd.to_numeric(temp_df["环比变化"], errors="coerce")
    temp_df["累计票房"] = pd.to_numeric(temp_df["累计票房"], errors="coerce") / 10000
    temp_df["平均票价"] = pd.to_numeric(temp_df["平均票价"], errors="coerce")
    temp_df["场均人次"] = pd.to_numeric(temp_df["场均人次"], errors="coerce")
    temp_df["上映天数"] = pd.to_numeric(temp_df["上映天数"], errors="coerce").astype(
        "Int64"
    )
    temp_df["排序"] = pd.to_numeric(temp_df["排序"], errors="coerce").astype("Int64")
    temp_df.sort_values(["排序"], inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df


def movie_boxoffice_weekly(date: str = "20240218") -> pd.DataFrame:
    """
    电影票房-单周票房
    https://www.endata.com.cn/BoxOffice/BO/Week/oneWeek.html
    :param date: 只能获取指定日期所在完整周的票房数据
    :type date: str
    :return: 单周票房
    :rtype: pandas.DataFrame
    """
    _ = date
    _raise_week_permission_error(interface_name="movie_boxoffice_weekly")


def movie_boxoffice_monthly(date: str = "20240218") -> pd.DataFrame:
    """
    电影票房-单月票房
    https://www.endata.com.cn/BoxOffice/BO/Month/oneMonth.html
    :param date: 指定日期所在月份的月度票房
    :type date: str
    :return: 单月票房
    :rtype: pandas.DataFrame
    """
    date_obj = datetime.datetime.strptime(date, "%Y%m%d")
    month_start = date_obj.replace(day=1).strftime("%Y-%m-%d")
    month_end = (
        (date_obj.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        - datetime.timedelta(days=1)
    ).strftime("%Y-%m-%d")
    url = "https://ys.endata.cn/enlib-api/api/movie/getMovie_BoxOffice_Month_List.do"
    month_id = date_obj.month + (date_obj.year - 2026) * 12 + 240
    payload = {
        "r": random.random(),
        "datetype": "Month",
        "date": f"{month_start},{month_end}",
        "sdate": month_start,
        "edate": month_end,
        "dateid": str(month_id),
        "sdateid": str(month_id),
        "edateid": str(month_id),
        "bserviceprice": "1",
        "columnslist": "100,101,102,105,109,110,130,131",
        "pageindex": 1,
        "pagesize": 500,
        "order": "102",
        "ordertype": "desc",
    }
    temp_df = _fetch_endata_list(
        url=url, payload=payload, referer_path="/BoxOffice/Movie"
    )
    temp_df = temp_df[
        [
            "Irank",
            "MovieName",
            "BoxOffice",
            "BoxOfficePercent",
            "AvgBoxOffice",
            "AvgShowAudienceCount",
            "ReleaseDate",
            "ReleaseDay",
        ]
    ]
    temp_df.columns = [
        "排序",
        "影片名称",
        "单月票房",
        "月度占比",
        "平均票价",
        "场均人次",
        "上映日期",
        "月内天数",
    ]
    temp_df["口碑指数"] = pd.NA
    temp_df = temp_df[
        [
            "排序",
            "影片名称",
            "单月票房",
            "月度占比",
            "平均票价",
            "场均人次",
            "上映日期",
            "口碑指数",
            "月内天数",
        ]
    ]
    temp_df["单月票房"] = pd.to_numeric(temp_df["单月票房"], errors="coerce") / 10000
    temp_df["月度占比"] = pd.to_numeric(temp_df["月度占比"], errors="coerce")
    temp_df["平均票价"] = pd.to_numeric(temp_df["平均票价"], errors="coerce")
    temp_df["场均人次"] = pd.to_numeric(temp_df["场均人次"], errors="coerce")
    temp_df["上映日期"] = pd.to_datetime(temp_df["上映日期"], errors="coerce").dt.date
    temp_df["月内天数"] = pd.to_numeric(temp_df["月内天数"], errors="coerce")
    temp_df["排序"] = pd.to_numeric(temp_df["排序"], errors="coerce").astype("Int64")
    temp_df.sort_values(["排序"], inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df


def movie_boxoffice_yearly(date: str = "20240218") -> pd.DataFrame:
    """
    电影票房-年度票房
    https://www.endata.com.cn/BoxOffice/BO/Year/index.html
    :param date: 当前日期所在年度的票房数据
    :type date: str
    :return: 年度票房
    :rtype: pandas.DataFrame
    """
    year = int(date[:4])
    url = "https://ys.endata.cn/enlib-api/api/movie/getMovie_BoxOffice_Year_List.do"
    payload = {
        "r": random.random(),
        "datetype": "Year",
        "date": f"{year}-01-01,{year}-12-31",
        "sdate": f"{year}-01-01",
        "edate": f"{year}-12-31",
        "dateid": str(year),
        "sdateid": str(year),
        "edateid": str(year),
        "bserviceprice": "1",
        "columnslist": "100,101,108,115,105,106,109,107",
        "pageindex": 1,
        "pagesize": 500,
        "order": "115",
        "ordertype": "desc",
    }
    temp_df = _fetch_endata_list(
        url=url, payload=payload, referer_path="/BoxOffice/Movie"
    )
    temp_df = temp_df[
        [
            "Irank",
            "MovieName",
            "GenreMain",
            "TotalBoxOffice",
            "AvgBoxOffice",
            "AvgShowAudienceCount",
            "Country",
            "ReleaseDate",
        ]
    ]
    temp_df.columns = [
        "排序",
        "影片名称",
        "类型",
        "总票房",
        "平均票价",
        "场均人次",
        "国家及地区",
        "上映日期",
    ]
    temp_df["总票房"] = pd.to_numeric(temp_df["总票房"], errors="coerce") / 10000
    temp_df["平均票价"] = pd.to_numeric(temp_df["平均票价"], errors="coerce")
    temp_df["场均人次"] = pd.to_numeric(temp_df["场均人次"], errors="coerce")
    temp_df["上映日期"] = pd.to_datetime(temp_df["上映日期"], errors="coerce").dt.date
    temp_df["排序"] = pd.to_numeric(temp_df["排序"], errors="coerce").astype("Int64")
    temp_df["国家及地区"] = (
        temp_df["国家及地区"].astype("string").str.replace(" ", "", regex=False)
    )
    temp_df.sort_values(["排序"], inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df


def movie_boxoffice_yearly_first_week(date: str = "20201018") -> pd.DataFrame:
    """
    电影票房-年度票房-年度首周票房
    https://www.endata.com.cn/BoxOffice/BO/Year/firstWeek.html
    :param date: 当前日期所在年度的年度首周票房票房数据
    :type date: str
    :return: 年度首周票房
    :rtype: pandas.DataFrame
    """
    year = int(date[:4])
    url = "https://ys.endata.cn/enlib-api/api/movie/getMovie_BoxOffice_Year_List.do"
    payload = {
        "r": random.random(),
        "datetype": "Year",
        "date": f"{year}-01-01,{year}-12-31",
        "sdate": f"{year}-01-01",
        "edate": f"{year}-12-31",
        "dateid": str(year),
        "sdateid": str(year),
        "edateid": str(year),
        "bserviceprice": "1",
        "columnslist": "100,101,108,118,119,106,109,107",
        "pageindex": 1,
        "pagesize": 500,
        "order": "118",
        "ordertype": "desc",
    }
    temp_df = _fetch_endata_list(
        url=url, payload=payload, referer_path="/BoxOffice/Movie"
    )
    temp_df = temp_df[
        [
            "Irank",
            "MovieName",
            "GenreMain",
            "WeekBoxOffice",
            "WeekBoxPercent",
            "AvgShowAudienceCount",
            "Country",
            "ReleaseDate",
        ]
    ]
    temp_df.columns = [
        "排序",
        "影片名称",
        "类型",
        "首周票房",
        "占总票房比重",
        "场均人次",
        "国家及地区",
        "上映日期",
    ]
    temp_df["首周天数"] = temp_df["上映日期"].map(_calc_first_week_days).astype("Int64")
    temp_df = temp_df[
        [
            "排序",
            "影片名称",
            "类型",
            "首周票房",
            "占总票房比重",
            "场均人次",
            "国家及地区",
            "上映日期",
            "首周天数",
        ]
    ]
    temp_df["首周票房"] = pd.to_numeric(temp_df["首周票房"], errors="coerce") / 10000
    temp_df["占总票房比重"] = pd.to_numeric(temp_df["占总票房比重"], errors="coerce")
    temp_df["场均人次"] = pd.to_numeric(temp_df["场均人次"], errors="coerce")
    temp_df["上映日期"] = pd.to_datetime(temp_df["上映日期"], errors="coerce").dt.date
    temp_df["排序"] = pd.to_numeric(temp_df["排序"], errors="coerce").astype("Int64")
    temp_df["国家及地区"] = (
        temp_df["国家及地区"].astype("string").str.replace(" ", "", regex=False)
    )
    temp_df.sort_values(["排序"], inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df


def movie_boxoffice_cinema_daily(date: str = "20240219") -> pd.DataFrame:
    """
    电影票房-影院票房-日票房排行
    https://www.endata.com.cn/BoxOffice/BO/Cinema/day.html
    :param date: 当前日期前一日的票房数据
    :type date: str
    :return: 影票房-影院票房-日票房排行
    :rtype: pandas.DataFrame
    """
    date_str = _format_date(date=date)
    url = "https://ys.endata.cn/enlib-api/api/cinema/getcinemaboxoffice_day_list.do"
    payload = {
        "r": random.random(),
        "bserviceprice": "0",
        "datetype": "Day",
        "date": date_str,
        "sdate": date_str,
        "edate": date_str,
        "citylevel": "",
        "lineid": "",
        "columnslist": "100,101,102,103,109,108,117",
        "pageindex": 1,
        "pagesize": 100,
        "order": "102",
        "ordertype": "desc",
    }
    temp_df = _post_endata_json(url=url, payload=payload, referer_path="/BoxOffice/Org")
    temp_df = pd.DataFrame(temp_df["data"].get("table1", []))
    temp_df = temp_df[
        [
            "Irank",
            "CinemaName",
            "BoxOffice",
            "ShowCount",
            "AvgShowAudienceCount",
            "AvgBoxOffice",
            "Attendance",
        ]
    ]
    temp_df.columns = [
        "排序",
        "影院名称",
        "单日票房",
        "单日场次",
        "场均人次",
        "场均票价",
        "上座率",
    ]
    temp_df["单日票房"] = pd.to_numeric(temp_df["单日票房"], errors="coerce")
    temp_df["单日场次"] = pd.to_numeric(temp_df["单日场次"], errors="coerce").astype(
        "Int64"
    )
    temp_df["场均人次"] = pd.to_numeric(temp_df["场均人次"], errors="coerce")
    temp_df["场均票价"] = pd.to_numeric(temp_df["场均票价"], errors="coerce")
    temp_df["上座率"] = pd.to_numeric(temp_df["上座率"], errors="coerce")
    temp_df["排序"] = pd.to_numeric(temp_df["排序"], errors="coerce").astype("Int64")
    temp_df.sort_values(["排序"], inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df


def movie_boxoffice_cinema_weekly(date: str = "20240219") -> pd.DataFrame:
    """
    电影票房-影院票房-周票房排行
    https://www.endata.com.cn/BoxOffice/BO/Cinema/week.html
    :param date: 当前日期前完整一周的票房数据
    :type date: str
    :return: 影票房-影院票房-轴票房排行
    :rtype: pandas.DataFrame
    """
    _ = date
    _raise_week_permission_error(interface_name="movie_boxoffice_cinema_weekly")


if __name__ == "__main__":
    movie_boxoffice_realtime_df = movie_boxoffice_realtime()
    print(movie_boxoffice_realtime_df)

    movie_boxoffice_daily_df = movie_boxoffice_daily(date="20240219")
    print(movie_boxoffice_daily_df)

    movie_boxoffice_weekly_df = movie_boxoffice_weekly(date="20240218")
    print(movie_boxoffice_weekly_df)

    movie_boxoffice_monthly_df = movie_boxoffice_monthly(date="20240218")
    print(movie_boxoffice_monthly_df)

    movie_boxoffice_yearly_df = movie_boxoffice_yearly(date="20240218")
    print(movie_boxoffice_yearly_df)

    movie_boxoffice_yearly_first_week_df = movie_boxoffice_yearly_first_week(
        date="20201018"
    )
    print(movie_boxoffice_yearly_first_week_df)

    movie_boxoffice_cinema_daily_df = movie_boxoffice_cinema_daily(date="20240219")
    print(movie_boxoffice_cinema_daily_df)

    movie_boxoffice_cinema_weekly_df = movie_boxoffice_cinema_weekly(date="20240219")
    print(movie_boxoffice_cinema_weekly_df)
