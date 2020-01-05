# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/11/25 19:58
contact: jindaxiang@163.com
desc: 日出和日落数据
"""
import pandas as pd
import pypinyin
import requests


def weather_city_df():
    url = "https://www.timeanddate.com/sun/china"
    res = requests.get(url)
    china_city_df = pd.read_html(res.text)[0]
    city_list = [item.lower() for item in china_city_df["Location Name"].tolist()]
    return city_list


def weather_daily(trade_date="20190801", city="北京"):
    if pypinyin.slug(city, separator='') in weather_city_df():
        year = trade_date[:4]
        month = trade_date[4:6]
        url = f"https://www.timeanddate.com/sun/china/{pypinyin.slug(city, separator='')}?month={month}&year={year}"
        res = requests.get(url)
        table = pd.read_html(res.text, header=2)[0]
        month_df = table.iloc[
            :-1,
        ]
        day_df = month_df[month_df.iloc[:, 0].astype(str).str.zfill(2) == trade_date[6:]]
        day_df.index = pd.to_datetime([trade_date]*len(day_df), format="%Y%m%d")
        return day_df
    else:
        return "不存在这个城市的数据"


def weather_monthly(trade_date="20190801", city="北京"):
    if pypinyin.slug(city, separator='') in weather_city_df():
        year = trade_date[:4]
        month = trade_date[4:6]
        url = f"https://www.timeanddate.com/sun/china/{pypinyin.slug(city, separator='')}?month={month}&year={year}"
        res = requests.get(url)
        table = pd.read_html(res.text, header=2)[0]
        month_df = table.iloc[
            :-1,
        ]
        month_df.index = pd.to_datetime([trade_date[:-2]]*len(month_df), format="%Y%m")
        return month_df
    else:
        return "不存在这个城市的数据"


if __name__ == "__main__":
    weather_day_df = weather_daily(trade_date="20190801", city="北京")
    weather_month_df = weather_monthly(trade_date="20190801", city="北京")
    print(weather_day_df)
    print(weather_month_df)
