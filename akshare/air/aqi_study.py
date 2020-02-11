# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/7 15:55
contact: jindaxiang@163.com
desc: 获取空气质量在线监测分析平台的空气质量数据
https://www.aqistudy.cn/
此部分参考 https://github.com/PKUJohnson/OpenData/tree/master/opendatatools/aqi2
感谢 PKUJohnson 提供的加解密函数
"""
import json
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.air.aqi_utils import *


def air_hourly(city="上海", date="2019-12-05"):
    """

    :param city:
    :type city:
    :param date:
    :type date:
    :return:
    :rtype:
    """
    start_time = f"{date} 00:00:00"
    end_time = f"{date} 23:59:59"
    temp_df = get_server_data(city, "HOUR", start_time, end_time)
    return temp_df.transform(pd.to_numeric)


def air_daily(city="上海", start_date="2019-11-01", end_date="2019-12-01"):
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
    start_time = f"{start_date} 00:00:00"
    end_time = f"{end_date} 23:59:59"
    temp_df = get_server_data(city, "DAY", start_time, end_time)
    return temp_df.transform(pd.to_numeric)


def get_server_data(city, period_type, start_time, end_time):
    url = "https://www.aqistudy.cn/apinew/aqistudyapi.php"
    app_id = "a01901d3caba1f362d69474674ce477f"
    method = "GETDETAIL"
    timestamp = int(time.time() * 1000)
    client_type = "WEB"
    object_dict = {
        "city": city,
        "type": period_type,
        "startTime": start_time,
        "endTime": end_time,
    }
    secret_key = (
        app_id
        + method
        + str(timestamp)
        + client_type
        + '{"city":"%s","endTime":"%s","startTime":"%s","type":"%s"}'
        % (
            object_dict["city"],
            object_dict["endTime"],
            object_dict["startTime"],
            object_dict["type"],
        )
    )
    secret = hashlib.md5(secret_key.encode("utf8")).hexdigest()
    payload = {
        "appId": app_id,
        "method": method,
        "timestamp": timestamp,
        "clienttype": client_type,
        "object": object_dict,
        "secret": secret,
    }

    payload = base64.standard_b64encode(json.dumps(payload).encode("utf8")).decode()
    payload = aes_encrypt(real_aes_client_key, real_aes_client_iv, payload)

    response = requests.post(url, data={"d": payload})
    if response is None:
        return None, "获取数据失败"

    # data = base64.standard_b64decode(response.encode("utf8")).decode()
    data = decrypt_response(
        real_des_key,
        real_des_iv,
        real_aes_server_key,
        real_aes_server_iv,
        response.text,
    )

    json_obj = json.loads(data)
    success = json_obj["success"]
    errcode = json_obj["errcode"]
    errmsg = json_obj["errmsg"]

    if errcode != 0:
        return None, errmsg

    result_rows = json_obj["result"]["data"]["rows"]
    result_df = pd.DataFrame(result_rows)
    if len(result_df) > 0:
        result_df.set_index("time", inplace=True)
    return result_df


def air_all_city(period_type="HOUR", time_point="2019-12-01 20:00:00"):
    """
    # period_type : "DAY", "HOUR
    """
    url = "https://www.aqistudy.cn/apinew/aqistudyapi.php"
    app_id = "a01901d3caba1f362d69474674ce477f"
    method = "GETMAPDATA"
    timestamp = int(time.time() * 1000)
    client_type = "WEB"
    object_dict = {"type": period_type, "timepoint": time_point}
    secret_key = (
        app_id
        + method
        + str(timestamp)
        + client_type
        + '{"timepoint":"%s","type":"%s"}'
        % (object_dict["timepoint"], object_dict["type"])
    )
    secret = hashlib.md5(secret_key.encode("utf8")).hexdigest()
    payload = {
        "appId": app_id,
        "method": method,
        "timestamp": timestamp,
        "clienttype": client_type,
        "object": object_dict,
        "secret": secret,
    }

    payload = base64.standard_b64encode(json.dumps(payload).encode("utf8")).decode()
    payload = aes_encrypt(real_aes_client_key, real_aes_client_iv, payload)

    response = requests.post(url, data={"d": payload})
    if response is None:
        return None, "获取数据失败"

    # data = base64.standard_b64decode(response.encode("utf8")).decode()
    data = decrypt_response(
        real_des_key,
        real_des_iv,
        real_aes_server_key,
        real_aes_server_iv,
        response.text,
    )

    json_obj = json.loads(data)
    errcode = json_obj["errcode"]
    errmsg = json_obj["errmsg"]

    if errcode != 0:
        return None, errmsg

    result_rows = json_obj["result"]["data"]["rows"]
    result_df = pd.DataFrame(result_rows)
    if len(result_df) > 0:
        result_df.set_index("time", inplace=True)
    result_df = result_df.transform(pd.to_numeric, errors="ignore")
    return result_df


def air_city_list():
    """
    真气网-空气质量历史数据查询-全部城市列表
    https://www.aqistudy.cn/historydata/
    :return: 城市映射
    :rtype: dict
    """
    url = "https://www.aqistudy.cn/historydata/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    # 注意 href 的用法
    link_list = soup.find_all(href=has_month_data)
    city_list = [item.get_text() for item in link_list]
    return dict(zip(city_list, city_list))


if __name__ == "__main__":
    city_list = air_city_list()
    print(city_list)

    df_hourly = air_hourly("成都", "2019-12-10")
    print(df_hourly)

    df_daily = air_daily("成都", "2019-01-01", "2019-12-10")
    print(df_daily)

    df_all_city = air_all_city("HOUR", "2019-12-10 08:00:00")
    print(df_all_city)

    df_city = air_all_city("DAY", "2019-12-09")
    print(df_city)
