#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/28
Desc: 财富中文网-历年《财富》世界 500 强榜单
https://www.fortunechina.com/fortune500/index.htm
各年份网页的表格格式不同，返回结果统一为固定的列，网页未公布的字段为空值，
例如 2010 年没有国家，2020 年起没有上年排名，2009 年以前才有资产与雇员人数
"""

from functools import lru_cache
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.exceptions import InvalidParameterError
from akshare.utils.tqdm import get_tqdm

FORTUNE_COLUMNS = [
    "排名",
    "上年排名",
    "公司名称",
    "国家",
    "营业收入",
    "利润",
    "资产",
    "股东权益",
    "雇员人数",
]


@lru_cache()
def _fortune_rank_year_url_map() -> dict:
    """
    年份和网址映射
    https://www.fortunechina.com/fortune500/index.htm
    :return: 年份和网址映射
    :rtype: dict
    """
    url = "https://www.fortunechina.com/fortune500/index.htm"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")
    url_2023 = "https://www.fortunechina.com/fortune500/c/2023-08/02/content_436874.htm"
    node_list = soup.find_all(name="div", attrs={"class": "swiper-slide"})
    url_list = [item.find("a")["href"] for item in node_list]
    year_list = [item.find("a").text for item in node_list]
    year_url_map = dict(zip(year_list, url_list))
    year_url_map["2023"] = url_2023
    return year_url_map


def _fortune_rename(columns: list) -> dict:
    """
    把各年份网页表头统一为 FORTUNE_COLUMNS 中的名称。
    第一列总是当年排名；第二列为年份或含“排名”时是上年排名。
    :param columns: 原始表头
    :type columns: list
    :return: 原始表头到统一名称的映射
    :rtype: dict
    """
    keywords = [
        ("上年排名", "上年排名"),
        ("公司", "公司名称"),
        ("国家", "国家"),
        ("营业收入", "营业收入"),
        ("利润", "利润"),
        ("资产", "资产"),
        ("股东权益", "股东权益"),
        ("雇员", "雇员人数"),
    ]
    rename = {columns[0]: "排名"}
    for position, column in enumerate(columns[1:], start=1):
        text = str(column)
        if position == 1 and (text.split(".")[0].isdigit() or "排名" in text):
            rename[column] = "上年排名"
            continue
        for keyword, name in keywords:
            if keyword in text:
                rename[column] = name
                break
    return rename


def _fortune_read_table(html: str, header_in_first_row: bool) -> pd.DataFrame:
    """
    读取榜单页面中的表格。
    :param html: 页面内容
    :type html: str
    :param header_in_first_row: 表头是否在表格第一行（2009 年以前的页面）
    :type header_in_first_row: bool
    :return: 表格
    :rtype: pandas.DataFrame
    """
    table = pd.read_html(StringIO(html))[0]
    if header_in_first_row:
        table.columns = table.iloc[0, :].tolist()
        table = table.iloc[1:, :]
    return table


def fortune_rank(year: str = "2025") -> pd.DataFrame:
    """
    财富中文网-历年《财富》世界 500 强榜单
    https://www.fortunechina.com/fortune500/index.htm
    :param year: 年份，1996 年至今
    :type year: str
    :return: 世界 500 强榜单，金额单位为百万美元
    :rtype: pandas.DataFrame
    """
    year_url_map = _fortune_rank_year_url_map()
    if year not in year_url_map:
        raise InvalidParameterError(
            f"year 可选 {min(year_url_map)} 至 {max(year_url_map)}，收到 {year}"
        )
    url = year_url_map[year]
    r = requests.get(url, timeout=15)
    r.encoding = "utf-8"
    if int(year) < 2007:
        # 最后一行是页面的说明文字
        temp_df = _fortune_read_table(r.text, header_in_first_row=True).iloc[:-1, :]
    elif int(year) < 2010:
        # 分 10 页，后续页面地址为 xxx_2.htm 至 xxx_10.htm
        temp_df = _fortune_read_table(r.text, header_in_first_row=True)
        tqdm = get_tqdm()
        for page in tqdm(range(2, 11), leave=False):
            page_url = url.rsplit(".", maxsplit=1)[0] + "_" + str(page) + ".htm"
            r = requests.get(page_url, timeout=15)
            r.encoding = "utf-8"
            page_df = _fortune_read_table(r.text, header_in_first_row=True)
            temp_df = pd.concat(objs=[temp_df, page_df], ignore_index=True)
    else:
        temp_df = _fortune_read_table(r.text, header_in_first_row=False)
    temp_df = temp_df.rename(columns=_fortune_rename(list(temp_df.columns)))
    temp_df = temp_df.reindex(columns=FORTUNE_COLUMNS).reset_index(drop=True)
    for column in [
        "排名",
        "上年排名",
        "营业收入",
        "利润",
        "资产",
        "股东权益",
        "雇员人数",
    ]:
        temp_df[column] = pd.to_numeric(
            temp_df[column].astype(str).str.replace(",", "", regex=False),
            errors="coerce",
        )
    temp_df["排名"] = temp_df["排名"].astype("Int64")
    temp_df["上年排名"] = temp_df["上年排名"].astype("Int64")
    return temp_df


if __name__ == "__main__":
    fortune_rank_df = fortune_rank(year="2025")
    print(fortune_rank_df)

    fortune_rank_df = fortune_rank(year="2005")
    print(fortune_rank_df)
