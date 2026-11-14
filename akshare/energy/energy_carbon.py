#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/6/25 15:00
Desc: 碳排放交易
北京市碳排放权电子交易平台-北京市碳排放权公开交易行情
https://www.bjets.com.cn/article/jyxx/

深圳碳排放交易所-国内碳情
http://www.cerx.cn/dailynewsCN/index.htm

深圳碳排放交易所-国际碳情
http://www.cerx.cn/dailynewsOuter/index.htm

湖北碳排放权交易中心-现货交易数据-配额-每日概况
http://www.cerx.cn/dailynewsOuter/index.htm

广州碳排放权交易中心-行情信息
http://www.cnemission.com/article/hqxx/
"""

from io import StringIO

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

from akshare.utils import jsonish
from akshare.utils import http
from akshare.utils.cons import headers


def energy_carbon_bj() -> pd.DataFrame:
    """
    北京市碳排放权电子交易平台-北京市碳排放权公开交易行情
    https://www.bjets.com.cn/article/jyxx/
    :return: 北京市碳排放权公开交易行情
    :rtype: pandas.DataFrame
    """
    url = "https://www.bjets.com.cn/article/jyxx/"
    r = http.get(url, headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")
    total_page = (
        soup.find("table")
        .find("script")
        .string.split("=")[-1]
        .strip()
        .strip(";")
        .strip('"')
    )
    temp_df = pd.DataFrame()
    for i in tqdm(
        range(1, int(total_page) + 1),
        desc="Please wait for a moment",
        leave=False,
    ):
        if i == 1:
            i = ""
        url = f"https://www.bjets.com.cn/article/jyxx/?{i}"
        r = http.get(url, headers=headers)
        r.encoding = "utf-8"
        df = pd.read_html(StringIO(r.text))[0]
        temp_df = pd.concat(objs=[temp_df, df], ignore_index=True)
    temp_df.columns = ["日期", "成交量", "成交均价", "成交额"]
    temp_df["成交单位"] = (
        temp_df["成交额"]
        .str.split("(", expand=True)
        .iloc[:, 1]
        .str.split("）", expand=True)
        .iloc[:, 0]
        .str.split(")", expand=True)
        .iloc[:, 0]
    )
    temp_df["成交额"] = (
        temp_df["成交额"]
        .str.split("(", expand=True)
        .iloc[:, 0]
        .str.split("（", expand=True)
        .iloc[:, 0]
    )
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交均价"] = pd.to_numeric(temp_df["成交均价"], errors="coerce")
    temp_df["成交额"] = temp_df["成交额"].str.replace(",", "")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    temp_df = temp_df.sort_values(by="日期")
    temp_df = temp_df.reset_index(drop=True)
    return temp_df


def energy_carbon_hb() -> pd.DataFrame:
    """
    湖北碳排放权交易中心-现货交易数据-配额-每日概况
    http://www.hbets.cn/list/13.html?page=42
    :return: 现货交易数据-配额-每日概况行情数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.hbets.cn/"
    r = http.get(url, headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")
    data_text = (
        soup.find(name="div", attrs={"class": "threeLeft"}).find_all("script")[1].text
    )
    start_pos = data_text.find("cjj = '[") + 7  # 找到 JSON 数组开始的位置
    end_pos = data_text.rfind("cjj =") - 31  # 找到 JSON 数组结束的位置
    data_json = jsonish.loads(data_text[start_pos:end_pos])
    temp_df = pd.DataFrame.from_dict(data_json)
    temp_df = temp_df.rename(
        columns={
            "riqi": "日期",
            "cjj": "成交价",
            "cjl": "成交量",
            "zx": "最新",
            "zd": "涨跌",
        },
    )
    temp_df = temp_df[
        [
            "日期",
            "成交价",
            "成交量",
            "最新",
            "涨跌",
        ]
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    temp_df["成交价"] = pd.to_numeric(temp_df["成交价"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["最新"] = pd.to_numeric(temp_df["最新"], errors="coerce")
    temp_df["涨跌"] = pd.to_numeric(temp_df["涨跌"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    energy_carbon_bj_df = energy_carbon_bj()
    print(energy_carbon_bj_df)

    energy_carbon_hb_df = energy_carbon_hb()
    print(energy_carbon_hb_df)
