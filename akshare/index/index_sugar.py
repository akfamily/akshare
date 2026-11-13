# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2026/11/13 17:00
Desc: 沐甜科技数据中心-中国食糖指数
https://www.msweet.com.cn/mtkj/sjzx13/index.html
"""

import pandas as pd

from akshare.utils import http


def _msweet_frame(data_json: dict, columns: list) -> pd.DataFrame:
    """
    沐甜科技数据中心-把 {"category": [日期], "data": {指标名：[数值]}} 转为数据表
    上游的指标名即中文列名，按名称取列，不依赖上游返回的字段顺序
    :param data_json: 上游返回的 JSON
    :type data_json: dict
    :param columns: 需要返回的指标名，按输出顺序排列
    :type columns: list
    :return: 日期与各指标
    :rtype: pandas.DataFrame
    """
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.insert(0, "日期", data_json["category"])
    temp_df = temp_df[["日期", *columns]]
    temp_df["日期"] = pd.to_datetime(
        temp_df["日期"].str.replace("/", "-"), errors="coerce"
    ).dt.date
    for column in columns:
        # 上游个别数值带不换行空格或多打了小数点，如 "4045.2 "、"12..88"
        cleaned = (
            temp_df[column].astype(str).str.strip().str.replace("..", ".", regex=False)
        )
        temp_df[column] = pd.to_numeric(cleaned, errors="coerce").astype(float)
    return temp_df


def index_sugar_msweet() -> pd.DataFrame:
    """
    沐甜科技数据中心-中国食糖指数
    https://www.msweet.com.cn/mtkj/sjzx13/index.html
    :return: 中国食糖指数
    :rtype: pandas.DataFrame
    """
    url = "https://www.msweet.com.cn/eportal/ui"
    params = {
        "struts.portlet.action": "/portlet/price!getSTZSJson.action",
        "moduleId": "cb752447cfe24b44b18c7a7e9abab048",
    }
    r = http.get(url, params=params)
    return _msweet_frame(r.json(), ["综合价格", "原糖价格", "现货价格"])


def index_inner_quota_sugar_msweet() -> pd.DataFrame:
    """
    沐甜科技数据中心-配额内进口糖估算指数
    https://www.msweet.com.cn/mtkj/sjzx13/index.html
    :return: 配额内进口糖估算指数
    :rtype: pandas.DataFrame
    """
    url = "https://www.msweet.com.cn/datacenterapply/datacenter/json/JinKongTang.json"
    r = http.get(url)
    return _msweet_frame(
        r.json(),
        [
            "利润空间",
            "泰国糖",
            "泰国MA5",
            "巴西MA5",
            "利润MA5",
            "巴西MA10",
            "巴西糖",
            "柳州现货价",
            "广州现货价",
            "泰国MA10",
            "利润MA30",
            "利润MA10",
        ],
    )


def index_outer_quota_sugar_msweet() -> pd.DataFrame:
    """
    沐甜科技数据中心-配额外进口糖估算指数
    https://www.msweet.com.cn/mtkj/sjzx13/index.html
    :return: 配额外进口糖估算指数
    :rtype: pandas.DataFrame
    """
    url = "https://www.msweet.com.cn/datacenterapply/datacenter/json/Jkpewlr.json"
    r = http.get(url)
    return _msweet_frame(
        r.json(),
        [
            "巴西糖进口成本",
            "泰国糖进口利润空间",
            "巴西糖进口利润空间",
            "泰国糖进口成本",
            "日照现货价",
        ],
    )


if __name__ == "__main__":
    index_sugar_msweet_df = index_sugar_msweet()
    print(index_sugar_msweet_df)

    index_inner_quota_sugar_msweet_df = index_inner_quota_sugar_msweet()
    print(index_inner_quota_sugar_msweet_df)

    index_outer_quota_sugar_msweet_df = index_outer_quota_sugar_msweet()
    print(index_outer_quota_sugar_msweet_df)
