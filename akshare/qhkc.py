# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
contact: jindaxiang@163.com
desc: 
"""
import pandas as pd
import requests

from akshare.cons import QHKC_URL


def get_qhkc_data(name, url=QHKC_URL):
    """
    获得奇货可查的指数数据: '奇货黑链', '奇货商品', '奇货谷物', '奇货贵金属', '奇货饲料', '奇货软商品', '奇货化工', '奇货有色', '奇货股指', '奇货铁合金', '奇货油脂'
    :param url: 网址
    :param name None
    :return: pd.DataFrame

    """
    name_id_dict = {}
    qhkc_index_url = "https://qhkch.com/ajax/official_indexes.php"
    r = requests.post(qhkc_index_url)
    display_name = [item["name"] for item in r.json()["data"]]
    index_id = [item["id"] for item in r.json()["data"]]
    for item in range(len(display_name)):
        name_id_dict[display_name[item]] = index_id[item]
    payload_id = {
        "id": name_id_dict[name]
    }
    r = requests.post(url, data=payload_id)
    print(name, "数据获取成功")
    json_data = r.json()
    date = json_data["data"]["date"]
    price = json_data["data"]["price"]
    df_temp = pd.DataFrame([date, price]).T
    df_temp.columns = ["date", "price"]
    return df_temp


if __name__ == "__main__":
    data = get_qhkc_data("奇货谷物")
    print(data)