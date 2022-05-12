# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/5/12 16:53
Desc: 百度股市通-经济数据
https://gushitong.baidu.com/calendar
"""
import pandas as pd
import requests


def news_economic_baidu(date: str = "20220502") -> pd.DataFrame:
    """
    百度股市通-经济数据
    https://gushitong.baidu.com/calendar
    :param date: 开始日期
    :type date: str
    :return: 经济数据
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([date[:4], date[4:6], date[6:]])
    end_date = "-".join([date[:4], date[4:6], date[6:]])
    url = "https://finance.pae.baidu.com/api/financecalendar"
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "market": "",
        "cate": "economic_data",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    big_df = pd.DataFrame()
    for item in data_json["Result"]:
        if not item["list"] == []:
            temp_df = pd.DataFrame(item["list"])
            temp_df.columns = [
                "日期",
                "时间",
                "-",
                "事件",
                "重要性",
                "前值",
                "预期",
                "公布",
                "-",
                "-",
                "地区",
                "-",
            ]
            temp_df = temp_df[
                [
                    "日期",
                    "时间",
                    "地区",
                    "事件",
                    "公布",
                    "预期",
                    "前值",
                    "重要性",
                ]
            ]
            temp_df["公布"] = pd.to_numeric(temp_df["公布"], errors="coerce")
            temp_df["预期"] = pd.to_numeric(temp_df["预期"], errors="coerce")
            temp_df["前值"] = pd.to_numeric(temp_df["前值"], errors="coerce")
            temp_df["重要性"] = pd.to_numeric(temp_df["重要性"], errors="coerce")
            temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date

            big_df = pd.concat([big_df, temp_df], ignore_index=True)
        else:
            continue
    return big_df


if __name__ == "__main__":
    news_economic_baidu_df = news_economic_baidu(date="20220512")
    print(news_economic_baidu_df.info())
