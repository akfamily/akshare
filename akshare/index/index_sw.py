#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/1/24 15:00
Desc: 申万宏源研究-申万指数-指数发布
乐咕乐股网
https://legulegu.com/stockdata/index-composition?industryCode=851921.SI
"""

import re
from io import StringIO
from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.utils.cons import headers


def _clean_legulegu_table_headers(columns: List[str]) -> List[str]:
    """
    清洗乐咕乐股表头中的 JSON-LD 噪声内容。

    :param columns: 原始表头序列
    :type columns: List[str]
    :return: 清洗后的表头列表
    :rtype: List[str]
    """
    cleaned_columns: List[str] = []
    for column in columns:
        column_name = re.sub(r"\s*\{.*", "", str(column), flags=re.S).strip()
        column_name = column_name.replace("市值（亿元）", "市值")
        cleaned_columns.append(column_name)
    return cleaned_columns


def sw_index_first_info() -> pd.DataFrame:
    """
    乐咕乐股-申万一级-分类
    https://legulegu.com/stockdata/sw-industry-overview#level1
    :return: 分类
    :rtype: pandas.DataFrame
    """
    url = "https://legulegu.com/stockdata/sw-industry-overview"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")
    code_raw = soup.find(name="div", attrs={"id": "level1Items"}).find_all(
        name="div", attrs={"class": "lg-industries-item-chinese-title"}
    )
    name_raw = soup.find(name="div", attrs={"id": "level1Items"}).find_all(
        name="div", attrs={"class": "lg-industries-item-number"}
    )
    value_raw = soup.find(name="div", attrs={"id": "level1Items"}).find_all(
        name="div", attrs={"class": "lg-sw-industries-item-value"}
    )
    code = [item.get_text() for item in code_raw]
    name = [item.get_text().split("(")[0] for item in name_raw]
    num = [item.get_text().split("(")[1].split(")")[0] for item in name_raw]
    num_1 = [
        item.find_all("span", attrs={"class": "value"})[0].get_text().strip()
        for item in value_raw
    ]
    num_2 = [
        item.find_all("span", attrs={"class": "value"})[1].get_text().strip()
        for item in value_raw
    ]
    num_3 = [
        item.find_all("span", attrs={"class": "value"})[2].get_text().strip()
        for item in value_raw
    ]
    num_4 = [
        item.find_all("span", attrs={"class": "value"})[3].get_text().strip()
        for item in value_raw
    ]
    temp_df = pd.DataFrame([code, name, num, num_1, num_2, num_3, num_4]).T
    temp_df.columns = [
        "行业代码",
        "行业名称",
        "成份个数",
        "静态市盈率",
        "TTM(滚动)市盈率",
        "市净率",
        "静态股息率",
    ]
    temp_df["成份个数"] = pd.to_numeric(temp_df["成份个数"], errors="coerce")
    temp_df["静态市盈率"] = pd.to_numeric(temp_df["静态市盈率"], errors="coerce")
    temp_df["TTM(滚动)市盈率"] = pd.to_numeric(
        temp_df["TTM(滚动)市盈率"], errors="coerce"
    )
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["静态股息率"] = pd.to_numeric(temp_df["静态股息率"], errors="coerce")
    return temp_df


def sw_index_second_info() -> pd.DataFrame:
    """
    乐咕乐股-申万二级-分类
    https://legulegu.com/stockdata/sw-industry-overview#level1
    :return: 分类
    :rtype: pandas.DataFrame
    """
    url = "https://legulegu.com/stockdata/sw-industry-overview"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")
    code_raw = soup.find(name="div", attrs={"id": "level2Items"}).find_all(
        name="div", attrs={"class": "lg-industries-item-chinese-title"}
    )
    name_raw = soup.find(name="div", attrs={"id": "level2Items"}).find_all(
        name="div", attrs={"class": "lg-industries-item-number"}
    )
    value_raw = soup.find(name="div", attrs={"id": "level2Items"}).find_all(
        name="div", attrs={"class": "lg-sw-industries-item-value"}
    )
    code = [item.get_text() for item in code_raw]
    name = [item.get_text().split("(")[0] for item in name_raw]
    parent_name = [
        item.find("span").get_text().split("(")[0][1:-1] for item in name_raw
    ]
    num = [item.get_text().split("(")[1].split(")")[0] for item in name_raw]
    num_1 = [
        item.find_all("span", attrs={"class": "value"})[0].get_text().strip()
        for item in value_raw
    ]
    num_2 = [
        item.find_all("span", attrs={"class": "value"})[1].get_text().strip()
        for item in value_raw
    ]
    num_3 = [
        item.find_all("span", attrs={"class": "value"})[2].get_text().strip()
        for item in value_raw
    ]
    num_4 = [
        item.find_all("span", attrs={"class": "value"})[3].get_text().strip()
        for item in value_raw
    ]
    temp_df = pd.DataFrame([code, name, parent_name, num, num_1, num_2, num_3, num_4]).T
    temp_df.columns = [
        "行业代码",
        "行业名称",
        "上级行业",
        "成份个数",
        "静态市盈率",
        "TTM(滚动)市盈率",
        "市净率",
        "静态股息率",
    ]
    temp_df["成份个数"] = pd.to_numeric(temp_df["成份个数"], errors="coerce")
    temp_df["静态市盈率"] = pd.to_numeric(temp_df["静态市盈率"], errors="coerce")
    temp_df["TTM(滚动)市盈率"] = pd.to_numeric(
        temp_df["TTM(滚动)市盈率"], errors="coerce"
    )
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["静态股息率"] = pd.to_numeric(temp_df["静态股息率"], errors="coerce")
    return temp_df


def sw_index_third_info() -> pd.DataFrame:
    """
    乐咕乐股-申万三级-分类
    https://legulegu.com/stockdata/sw-industry-overview#level1
    :return: 分类
    :rtype: pandas.DataFrame
    """
    url = "https://legulegu.com/stockdata/sw-industry-overview"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")
    code_raw = soup.find(name="div", attrs={"id": "level3Items"}).find_all(
        name="div", attrs={"class": "lg-industries-item-chinese-title"}
    )
    name_raw = soup.find(name="div", attrs={"id": "level3Items"}).find_all(
        name="div", attrs={"class": "lg-industries-item-number"}
    )
    value_raw = soup.find(name="div", attrs={"id": "level3Items"}).find_all(
        name="div", attrs={"class": "lg-sw-industries-item-value"}
    )
    code = [item.get_text() for item in code_raw]
    name = [item.get_text().split("(")[0] for item in name_raw]
    parent_name = [
        item.find("span").get_text().split("(")[0][1:-1] for item in name_raw
    ]
    num = [item.get_text().split("(")[1].split(")")[0] for item in name_raw]
    num_1 = [
        item.find_all("span", attrs={"class": "value"})[0].get_text().strip()
        for item in value_raw
    ]
    num_2 = [
        item.find_all("span", attrs={"class": "value"})[1].get_text().strip()
        for item in value_raw
    ]
    num_3 = [
        item.find_all("span", attrs={"class": "value"})[2].get_text().strip()
        for item in value_raw
    ]
    num_4 = [
        item.find_all("span", attrs={"class": "value"})[3].get_text().strip()
        for item in value_raw
    ]
    temp_df = pd.DataFrame([code, name, parent_name, num, num_1, num_2, num_3, num_4]).T
    temp_df.columns = [
        "行业代码",
        "行业名称",
        "上级行业",
        "成份个数",
        "静态市盈率",
        "TTM(滚动)市盈率",
        "市净率",
        "静态股息率",
    ]
    temp_df["成份个数"] = pd.to_numeric(temp_df["成份个数"], errors="coerce")
    temp_df["静态市盈率"] = pd.to_numeric(temp_df["静态市盈率"], errors="coerce")
    temp_df["TTM(滚动)市盈率"] = pd.to_numeric(
        temp_df["TTM(滚动)市盈率"], errors="coerce"
    )
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["静态股息率"] = pd.to_numeric(temp_df["静态股息率"], errors="coerce")
    return temp_df


def sw_index_third_cons(symbol: str = "801120.SI") -> pd.DataFrame:
    """
    乐咕乐股-申万三级-行业成份
    https://legulegu.com/stockdata/index-composition?industryCode=801120.SI
    :param symbol: 三级行业的行业代码
    :type symbol: str
    :return: 行业成份
    :rtype: pandas.DataFrame
    """
    url = f"https://legulegu.com/stockdata/index-composition?industryCode={symbol}"
    r = requests.get(url, headers=headers)
    temp_df = pd.read_html(StringIO(r.text))[0]
    temp_df.columns = _clean_legulegu_table_headers(temp_df.columns.tolist())
    temp_df["序号"] = pd.to_numeric(temp_df["序号"], errors="coerce")
    temp_df["价格"] = pd.to_numeric(temp_df["价格"], errors="coerce")
    temp_df["市盈率"] = pd.to_numeric(temp_df["市盈率"], errors="coerce")
    temp_df["市盈率ttm"] = pd.to_numeric(temp_df["市盈率ttm"], errors="coerce")
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["市值"] = pd.to_numeric(temp_df["市值"], errors="coerce")
    for column in temp_df.columns:
        if column in {"股息率", "ROE(%)"} or "涨幅" in column or "(%)" in column:
            temp_df[column] = pd.to_numeric(
                temp_df[column].astype(str).str.strip("%"), errors="coerce"
            )
    return temp_df


if __name__ == "__main__":
    sw_index_first_info_df = sw_index_first_info()
    print(sw_index_first_info_df)

    sw_index_second_info_df = sw_index_second_info()
    print(sw_index_second_info_df)

    sw_index_third_info_df = sw_index_third_info()
    print(sw_index_third_info_df)

    sw_index_third_cons_df = sw_index_third_cons(symbol="850111.SI")
    print(sw_index_third_cons_df)
