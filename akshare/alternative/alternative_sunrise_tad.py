#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/11/25 16:00
Desc: 日出和日落数据
https://www.timeanddate.com
"""

from io import StringIO

import pandas as pd

from akshare.exceptions import APIError, InvalidParameterError
from akshare.utils import http


def _get_html(url: str) -> str:
    """
    请求 timeanddate.com 的页面；被 Cloudflare 质询拦截时给出明确的报错
    :param url: 页面地址
    :type url: str
    :return: 页面源码
    :rtype: str
    """
    r = http.get(url)
    if r.status_code == 403 and "Just a moment" in r.text:
        raise APIError(
            "timeanddate.com 启用了 Cloudflare 人机验证，拒绝了本次程序访问，"
            "日出日落数据暂时无法获取；可更换网络或通过 ak.set_proxies 设置代理后重试",
            status_code=403,
        )
    return r.text


def sunrise_city_list() -> list:
    """
    查询日出与日落数据的城市列表
    https://www.timeanddate.com/astronomy/china
    :return: 所有可以获取的数据的城市列表
    :rtype: list
    """
    url = "https://www.timeanddate.com/astronomy/china"
    text = _get_html(url)
    city_list = []
    china_city_one_df = pd.read_html(StringIO(text))[1]
    china_city_two_df = pd.read_html(StringIO(text))[2]
    city_list.extend([item.lower() for item in china_city_one_df.iloc[:, 0].tolist()])
    city_list.extend([item.lower() for item in china_city_one_df.iloc[:, 3].tolist()])
    city_list.extend([item.lower() for item in china_city_one_df.iloc[:, 6].tolist()])
    city_list.extend([item.lower() for item in china_city_two_df.iloc[:, 0].tolist()])
    city_list.extend([item.lower() for item in china_city_two_df.iloc[:, 1].tolist()])
    city_list.extend([item.lower() for item in china_city_two_df.iloc[:, 2].tolist()])
    city_list.extend([item.lower() for item in china_city_two_df.iloc[:, 3].tolist()])
    city_list.extend(
        [item.lower() for item in china_city_two_df.iloc[:, 4].dropna().tolist()]
    )
    return city_list


def alternative_sunrise_daily_tad(
    date: str = "20240428", city: str = "beijing"
) -> pd.DataFrame:
    """
    每日日出日落数据
    https://www.timeanddate.com/astronomy/china/shaoxing
    :param date: 需要查询的日期，e.g., “20200428”
    :type date: str
    :param city: 需要查询的城市；注意输入的格式，e.g., "北京", "上海"
    :type city: str
    :return: 返回指定日期指定地区的日出日落数据
    :rtype: pandas.DataFrame
    """

    if city in sunrise_city_list():
        year = date[:4]
        month = date[4:6]
        url = f"https://www.timeanddate.com/sun/china/{city}?month={month}&year={year}"
        table = pd.read_html(StringIO(_get_html(url)), header=2)[1]
        month_df = table.iloc[:-1,]
        day_df = month_df[
            month_df.iloc[:, 0].astype(str).str.zfill(2) == date[6:]
        ].copy()
        day_df.index = pd.to_datetime([date] * len(day_df), format="%Y%m%d")
        day_df = day_df.reset_index()
        day_df = day_df.rename(columns={"index": "date"})
        day_df["date"] = pd.to_datetime(day_df["date"]).dt.date
        return day_df
    else:
        raise InvalidParameterError(
            f"没有城市 {city} 的日出日落数据，city 需为 timeanddate.com 上的英文小写"
            '城市名，如 "beijing"、"shanghai"'
        )


def alternative_sunrise_monthly_tad(
    date: str = "20240428", city: str = "beijing"
) -> pd.DataFrame:
    """
    每个指定 date 所在月份的每日日出日落数据，如果当前月份未到月底，则以预测值填充
    https://www.timeanddate.com/astronomy/china/shaoxing
    :param date: 需要查询的日期，这里用来指定 date 所在的月份；e.g., “20200428”
    :type date: str
    :param city: 需要查询的城市；注意输入的格式，e.g., "北京", "上海"
    :type city: str
    :return: 指定 date 所在月份的每日日出日落数据
    :rtype: pandas.DataFrame
    """

    if city in sunrise_city_list():
        year = date[:4]
        month = date[4:6]
        url = f"https://www.timeanddate.com/sun/china/{city}?month={month}&year={year}"
        table = pd.read_html(StringIO(_get_html(url)), header=2)[1]
        month_df = table.iloc[:-1,].copy()
        month_df.index = [date[:-2]] * len(month_df)
        month_df = month_df.reset_index()
        month_df = month_df.rename(
            columns={
                "index": "date",
            },
        )
        return month_df
    else:
        raise InvalidParameterError(
            f"没有城市 {city} 的日出日落数据，city 需为 timeanddate.com 上的英文小写"
            '城市名，如 "beijing"、"shanghai"'
        )


if __name__ == "__main__":
    alternative_sunrise_daily_tad_df = alternative_sunrise_daily_tad(
        date="20240428", city="beijing"
    )
    print(alternative_sunrise_daily_tad_df)

    alternative_sunrise_monthly_tad_df = alternative_sunrise_monthly_tad(
        date="20240428", city="beijing"
    )
    print(alternative_sunrise_monthly_tad_df)
