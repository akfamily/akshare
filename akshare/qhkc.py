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

payload_id = {
    "id": "index0d5e051e-b262-bd7a-0fdc-89e2aab21ebb"
}


def get_qhkc_data(url=QHKC_URL, payload=payload_id):
    """
    获得齐货可查的指数数据
    :param url: 网址
    :param payload: 上传ID
    :return: pd.Dataframe
    """
    r = requests.post(url, data=payload)
    json_data = r.json()
    date = json_data["data"]["date"]
    price = json_data["data"]["price"]
    df_temp = pd.DataFrame([date, price]).T
    df_temp.columns = ["date", "price"]
    return df_temp


if __name__ == "__main__":
    df = get_qhkc_data()
    print(df)




