# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/12/27 15:34
Desc: 
"""
import requests
import pandas as pd


def index_sugar_msweet() -> pd.DataFrame:
    """
    沐甜科技数据中心-中国食糖指数
    http://www.msweet.com.cn/mtkj/sjzx13/index.html
    :return: 中国食糖指数
    :rtype: pandas.DataFrame
    """
    url = "http://www.msweet.com.cn/eportal/ui"
    params = {
        'struts.portlet.action': '/portlet/price!getSTZSJson.action',
        'moduleId': 'cb752447cfe24b44b18c7a7e9abab048',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.concat([pd.DataFrame(data_json['category']), pd.DataFrame(data_json['data'])], axis=1)
    temp_df.columns = ["日期", "综合价格", "原糖价格", "现货价格"]
    temp_df.loc[3226, ['原糖价格']] = 12.88  # 数据源错误
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["综合价格"] = pd.to_numeric(temp_df["综合价格"])
    temp_df["原糖价格"] = pd.to_numeric(temp_df["原糖价格"])
    temp_df["现货价格"] = pd.to_numeric(temp_df["现货价格"])
    return temp_df


if __name__ == '__main__':
    index_sugar_msweet_df = index_sugar_msweet()
    print(index_sugar_msweet_df)
