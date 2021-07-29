# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/7/29 22:03
Desc: 猪肉信息
https://zhujia.zhuwang.cc/
"""
import requests
import pandas as pd


def futures_pig_info(symbol: str = "猪肉批发价") -> pd.DataFrame:
    """
    猪肉信息
    https://zhujia.zhuwang.cc/
    :param symbol: choice of {"猪肉批发价", "仔猪价格", "生猪期货指数", "二元母猪价格"}
    :type symbol: str
    :return: 猪肉信息
    :rtype: pandas.DataFrame
    """
    if symbol == "猪肉批发价":
        url = "https://zhujia.zhuwang.cc/new_map/zhujiapork/chart1.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.columns = ["date", "item", "value"]
        del temp_df["item"]
        return temp_df
    elif symbol == "仔猪价格":
        url = "https://zt.zhuwang.cc/new_map/zhizhu/chart2.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["date", "value"]
        temp_df["date"] = pd.to_datetime(temp_df["date"], format="%Y年%m月%d日").dt.date
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    elif symbol == "生猪期货指数":
        url = "https://zhujia.zhuwang.cc/new_map/shengzhuqihuo/chart1.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        return temp_df
    elif symbol == "二元母猪价格":
        url = "https://zt.zhuwang.cc/new_map/eryuanpig/chart2.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["date", "value"]
        temp_df["date"] = pd.to_datetime(temp_df["date"], format="%Y年%m月%d日").dt.date
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df
    elif symbol == "生猪产能数据":
        url = "https://zt.zhuwang.cc/new_map/shengzhuchanneng/chart1.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["time", "能繁母猪存栏", "猪肉产量", "生猪存栏", "生猪出栏"]
        temp_df["能繁母猪存栏"] = pd.to_numeric(temp_df["能繁母猪存栏"], errors="coerce")
        temp_df["猪肉产量"] = pd.to_numeric(temp_df["猪肉产量"], errors="coerce")
        temp_df["生猪存栏"] = pd.to_numeric(temp_df["生猪存栏"], errors="coerce")
        temp_df["生猪出栏"] = pd.to_numeric(temp_df["生猪出栏"], errors="coerce")
        return temp_df
    elif symbol == "饲料原料数据":
        url = "https://zt.zhuwang.cc/new_map/pigfeed/chart1.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["time", "大豆进口金额", "大豆播种面积", "玉米进口金额", "玉米播种面积"]
        temp_df["time"] = temp_df["time"].astype(int).astype(str)
        temp_df["大豆进口金额"] = pd.to_numeric(temp_df["大豆进口金额"], errors="coerce")
        temp_df["大豆播种面积"] = pd.to_numeric(temp_df["大豆播种面积"], errors="coerce")
        temp_df["玉米进口金额"] = pd.to_numeric(temp_df["玉米进口金额"], errors="coerce")
        temp_df["玉米播种面积"] = pd.to_numeric(temp_df["玉米播种面积"], errors="coerce")
        return temp_df
    elif symbol == "中央储备冻猪肉":
        url = "https://zt.zhuwang.cc/new_map/chubeidongzhurou/chart2.json"
        params = {"timestamp": "1627567846422"}
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json).T
        temp_df.columns = ["date", "value"]
        temp_df["date"] = pd.to_datetime(temp_df["date"], format="%Y年%m月%d日").dt.date
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df


if __name__ == "__main__":
    futures_pig_info_df = futures_pig_info(symbol="猪肉批发价")
    print(futures_pig_info_df)
