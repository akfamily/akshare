#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/2/27
Desc: 同花顺-新发基金
https://fund.10jqka.com.cn/datacenter/xfjj/
"""

import json
import re

import pandas as pd
import requests


def fund_new_found_ths(symbol: str = "全部") -> pd.DataFrame:
    """
    同花顺-基金数据-新发基金
    https://fund.10jqka.com.cn/datacenter/xfjj/
    :param symbol: 选择基金类型; choice of {"全部", "发行中", "将发行"}
    :type symbol: str
    :return: 新发基金数据
    :rtype: pandas.DataFrame
    """
    url = "https://fund.10jqka.com.cn/datacenter/xfjj/"
    r = requests.get(url, timeout=15)
    r.encoding = "utf-8"

    # 从页面中提取 jsonData
    # 找到 jsonData= 的位置
    start_idx = r.text.find("jsonData=")
    if start_idx == -1:
        raise ValueError("未找到 jsonData，可能页面结构已变化")

    # 找到第一个 {
    start_bracket = r.text.find("{", start_idx)
    if start_bracket == -1:
        raise ValueError("未找到 JSON 开始括号")

    # 通过计数括号找到完整的JSON对象
    count = 0
    end_idx = start_bracket
    for i in range(start_bracket, len(r.text)):
        if r.text[i] == "{":
            count += 1
        elif r.text[i] == "}":
            count -= 1
            if count == 0:
                end_idx = i + 1
                break

    if end_idx == start_bracket:
        raise ValueError("未找到完整的 JSON 对象")

    json_str = r.text[start_bracket:end_idx]
    data_json = json.loads(json_str)

    # 转换为 DataFrame
    temp_df = pd.DataFrame(data_json).T
    temp_df.reset_index(inplace=True, drop=True)

    # 根据 symbol 筛选数据
    if symbol == "发行中":
        # 发行中: zzfx=1
        temp_df = temp_df[temp_df["zzfx"] == 1]
    elif symbol == "将发行":
        # 将发行: zzfx != 1 (即 buy=0 且起始日在未来)
        temp_df = temp_df[temp_df["zzfx"] != 1]

    # 提取 manager 字段（可能是数组）
    if "manager" in temp_df.columns:
        temp_df["manager"] = temp_df["manager"].apply(
            lambda x: x[0] if isinstance(x, list) and len(x) > 0 else (x if pd.notna(x) else "")
        )

    # 重命名列
    temp_df.rename(
        columns={
            "code": "基金代码",
            "name": "基金名称",
            "type": "投资类型",
            "jjlx": "基金类型",
            "tzfg": "投资风格",
            "start": "募集起始日",
            "end": "募集终止日",
            "orgname": "管理人",
            "manager": "基金经理",
            "zgrgfl": "认购费率",
            "zdrg": "最低认购",
            "zdje": "认购金额",
            "zzfx": "发行中",
            "buy": "可购买",
        },
        inplace=True,
    )

    # 选择需要的列
    columns_order = [
        "基金代码",
        "基金名称",
        "投资类型",
        "募集起始日",
        "募集终止日",
        "管理人",
        "基金经理",
        "认购费率",
        "最低认购",
        "基金类型",
        "投资风格",
    ]

    # 只保留存在的列
    existing_columns = [col for col in columns_order if col in temp_df.columns]
    temp_df = temp_df[existing_columns]

    # 数据类型转换
    if "募集起始日" in temp_df.columns:
        temp_df["募集起始日"] = pd.to_datetime(temp_df["募集起始日"], errors="coerce").dt.date
    if "募集终止日" in temp_df.columns:
        temp_df["募集终止日"] = pd.to_datetime(temp_df["募集终止日"], errors="coerce").dt.date
    if "认购费率" in temp_df.columns:
        temp_df["认购费率"] = pd.to_numeric(temp_df["认购费率"], errors="coerce")
    if "最低认购" in temp_df.columns:
        temp_df["最低认购"] = pd.to_numeric(temp_df["最低认购"], errors="coerce")

    return temp_df


if __name__ == "__main__":
    # 测试获取全部新发基金
    fund_new_found_ths_df = fund_new_found_ths(symbol="全部")
    print(fund_new_found_ths_df)

    # 测试获取发行中的基金
    fund_new_found_ths_issue_df = fund_new_found_ths(symbol="发行中")
    print(fund_new_found_ths_issue_df)

    # 测试获取将发行的基金
    fund_new_found_ths_future_df = fund_new_found_ths(symbol="将发行")
    print(fund_new_found_ths_future_df)
