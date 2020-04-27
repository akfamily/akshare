# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/27 21:13
Desc: 真气网-空气质量
https://www.zq12369.com/environment.php
"""
import json

import demjson
import execjs
import pandas as pd
import requests


def air_quality_watch_point(city="杭州", start_date="2018-01-01", end_date="2020-04-27"):
    """

    :param city:
    :type city:
    :param start_date:
    :type start_date:
    :param end_date:
    :type end_date:
    :return:
    :rtype:
    """
    url = "https://www.zq12369.com/api/zhenqiapi.php"
    with open(r"akshare/air_new/crypto.js") as file:
        file_data = file.read()
    ctx = execjs.compile(file_data)
    method = "GETCITYPOINTAVG"
    ctx.call("encode_param", method)
    ctx.call("encode_param", start_date)
    ctx.call("encode_param", end_date)
    city_param = ctx.call("encode_param", city)
    ctx.call("encode_secret", method, city_param, start_date, end_date)
    payload = {
        "appId": "a01901d3caba1f362d69474674ce477f",
        "method": ctx.call("encode_param", method),
        "city": city_param,
        "startTime": ctx.call("encode_param", start_date),
        "endTime": ctx.call("encode_param", end_date),
        "secret": ctx.call("encode_secret", method, city_param, start_date, end_date),
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
    }
    r = requests.post(url, data=payload, headers=headers)
    data_text = r.text
    data_json = demjson.decode(ctx.call("decode_result", data_text))
    temp_df = pd.DataFrame(data_json["rows"])
    return temp_df


def air_quality_hist(
    city="杭州", period="day", start_date="2019-03-27", end_date="2020-04-27"
):
    url = "https://www.zq12369.com/api/newzhenqiapi.php"
    with open(r"akshare/air_new/outcrypto.js") as file:
        file_data = file.read()
    out = execjs.compile(file_data)
    appId = "4f0e3a273d547ce6b7147bfa7ceb4b6e"
    method = "CETCITYPERIOD"
    timestamp = execjs.eval("timestamp = new Date().getTime()")
    p_text = json.dumps(
        {
            "city": city,
            "endTime": f"{end_date} 23:45:39",
            "startTime": f"{start_date} 00:00:00",
            "type": period.upper(),
        },
        ensure_ascii=False,
        indent=None,
    ).replace(' "', '"')
    secret = out.call("hex_md5", appId + method + str(timestamp) + "WEB" + p_text)
    payload = {
        "appId": "4f0e3a273d547ce6b7147bfa7ceb4b6e",
        "method": "CETCITYPERIOD",
        "timestamp": int(timestamp),
        "clienttype": "WEB",
        "object": {
            "city": city,
            "type": period.upper(),
            "startTime": f"{start_date} 00:00:00",
            "endTime": f"{end_date} 23:45:39",
        },
        "secret": secret,
    }
    need = (
        json.dumps(payload, ensure_ascii=False, indent=None, sort_keys=False)
        .replace(' "', '"')
        .replace("\\", "")
        .replace('p": ', 'p":')
        .replace('t": ', 't":')
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
    }
    params = {"param": out.call("AES.encrypt", need)}
    r = requests.post(url, data=params, headers=headers)
    temp_text = out.call("decryptData", r.text)
    data_json = demjson.decode(out.call("b.decode", temp_text))
    temp_df = pd.DataFrame(data_json["result"]["data"]["rows"])
    return temp_df


# def _air_quality_rank(city="杭州", period="day", start_date="2019-03-27", end_date="2020-04-27"):
#     url = "https://www.zq12369.com/api/newzhenqiapi.php"
#     with open(r"akshare/air_new/outcrypto.js") as file:
#         file_data = file.read()
#     out = execjs.compile(file_data)
#     appId = "4f0e3a273d547ce6b7147bfa7ceb4b6e"
#     method = "GETCITYAQIRANK"
#     timestamp = execjs.eval("timestamp = new Date().getTime()")
#     p_text = json.dumps(
#         {
#             "order": "desc",
#         },
#         ensure_ascii=False,
#         indent=None,
#     ).replace(' "', '"')
#     secret = out.call("hex_md5", appId + method + str(timestamp) + "WEB" + p_text)
#     payload = {
#         "appId": "4f0e3a273d547ce6b7147bfa7ceb4b6e",
#         "method": method,
#         "timestamp": int(timestamp),
#         "clienttype": "WEB",
#         "object": {
#             "order": "desc",
#         },
#         "secret": secret,
#     }
#     need = (
#         json.dumps(payload, ensure_ascii=False, indent=None, sort_keys=False)
#         .replace(' "', '"')
#         .replace("\\", "")
#         .replace('p": ', 'p":')
#         .replace('t": ', 't":')
#     )
#
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
#     }
#     params = {"param": out.call("AES.encrypt", need)}
#     r = requests.post(url, data=params, headers=headers)
#     temp_text = out.call("decryptData", r.text)
#     data_json = demjson.decode(out.call("b.decode", temp_text))
#     temp_df = pd.DataFrame(data_json["result"]["data"]["rows"])
#     return temp_df


def air_quality_rank(date: str = "2020-03-12") -> pd.DataFrame:
    """
    真气网-168城市AQI排行榜
    https://www.zq12369.com/environment.php?date=2020-03-12&tab=rank&order=DESC&type=DAY#rank
    :param date:
    :type date:
    :return:
    :rtype: pandas.DataFrame
    """
    url = "https://www.zq12369.com/environment.php"

    if len(date.split("-")) == 3:
        params = {
            "date": date,
            "tab": "rank",
            "order": "DESC",
            "type": "DAY",
        }
        r = requests.get(url, params=params)
        return pd.read_html(r.text)[1].iloc[1:, :]
    elif len(date.split("-")) == 2:
        params = {
            "month": date,
            "tab": "rank",
            "order": "DESC",
            "type": "Month",
        }
        r = requests.get(url, params=params)
        return pd.read_html(r.text)[2].iloc[1:, :]
    elif len(date.split("-")) == 1:
        params = {
            "year": date,
            "tab": "rank",
            "order": "DESC",
            "type": "YEAR",
        }
        r = requests.get(url, params=params)
        return pd.read_html(r.text)[3].iloc[1:, :]
    if date == "实时":
        params = {
            "date": date,
            "tab": "rank",
            "order": "DESC",
            "type": "DAY",
        }
        r = requests.get(url, params=params)
        return pd.read_html(r.text)[0].iloc[1:, :]


if __name__ == "__main__":
    air_quality_spot_df = air_quality_watch_point(
        city="杭州", start_date="2018-01-01", end_date="2020-04-27"
    )
    print(air_quality_spot_df)
    air_quality_hist_df = air_quality_hist(
        city="北京", period="month", start_date="2019-03-27", end_date="2020-04-27"
    )
    print(air_quality_hist_df)
    air_quality_rank_df = air_quality_rank(date="2020-03-12")
    print(air_quality_rank_df)
