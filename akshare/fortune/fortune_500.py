# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/12/10 21:55
Desc: 历年世界 500 强榜单数据
http://www.fortunechina.com/fortune500/index.htm
特殊情况说明：
2010年由于网页端没有公布公司所属的国家, 故 2010 年数据没有国家这列
"""
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.fortune.cons import *


def fortune_rank(year="2015"):
    """
    财富500强公司从1996年开始的排行榜
    http://www.fortunechina.com/fortune500/index.htm
    :param year: str 年份
    :return: pandas.DataFrame
    """
    if int(year) in [item for item in range(2014, 2020)] + [item for item in range(1996, 2007)]:
        if year in ["2006", "2007"]:
            res = requests.get(eval("url_" + year))
            res.encoding = "utf-8"
            df = pd.read_html(res.text)[0].iloc[1:, 2:]
            df.columns = pd.read_html(res.text)[0].iloc[0, 2:].tolist()
            return df
        elif year in ["1996", "1997", "1998", "1999", "2000", "2001", "2003", "2004", "2005"]:
            res = requests.get(eval("url_" + year))
            res.encoding = "utf-8"
            df = pd.read_html(res.text)[0].iloc[1:-1, 1:]
            df.columns = pd.read_html(res.text)[0].iloc[0, 1:].tolist()
            return df
        elif year in ["2002"]:
            res = requests.get(eval("url_" + year))
            res.encoding = "utf-8"
            df = pd.read_html(res.text)[0].iloc[1:, 1:]
            df.columns = pd.read_html(res.text)[0].iloc[0, 1:].tolist()
            return df
        else:
            res = requests.get(eval("url_" + year))
            res.encoding = "utf-8"
            df = pd.read_html(res.text)[0].iloc[:, 2:]
            return df
    elif int(year) in [item for item in range(2010, 2014)]:
        if int(year) == 2011:
            res = requests.get(eval(f"url_{2011}"))
            res.encoding = "utf-8"
            df = pd.read_html(res.text)[0].iloc[:, 2:]
            temp_df = df
            for page in range(2, 6):
                # page = 1
                res = requests.get(eval(f"url_{2011}").rsplit(".", maxsplit=1)[0] + "_" + str(page) + ".htm")
                res.encoding = "utf-8"
                df = pd.read_html(res.text)[0].iloc[:, 2:]
                temp_df = temp_df.append(df, ignore_index=True)
            temp_df.columns = ["公司名称", "营业收入百万美元", "利润百万美元", "国家地区"]
            return temp_df
        res = requests.get(eval(f"url_{year}"))
        res.encoding = "utf-8"
        df = pd.read_html(res.text)[0].iloc[:, 2:]
        temp_df = df
        for page in range(2, 6):
            # page = 1
            res = requests.get(eval(f"url_{year}").rsplit(".", maxsplit=1)[0] + "_" + str(page) + ".htm")
            res.encoding = "utf-8"
            df = pd.read_html(res.text)[0].iloc[:, 2:]
            temp_df = temp_df.append(df, ignore_index=True)
        df = temp_df
        return df
    elif int(year) in [item for item in range(2008, 2010)]:
        res = requests.get(eval(f"url_{year}"))
        res.encoding = "utf-8"
        df = pd.read_html(res.text)[0].iloc[1:, 2:]
        df.columns = pd.read_html(res.text)[0].iloc[0, 2:].tolist()
        temp_df = df
        for page in range(2, 11):
            # page = 1
            res = requests.get(eval(f"url_{year}").rsplit(".", maxsplit=1)[0] + "_" + str(page) + ".htm")
            res.encoding = "utf-8"
            text_df = pd.read_html(res.text)[0]
            df = text_df.iloc[1:, 2:]
            df.columns = text_df.iloc[0, 2:]
            temp_df = temp_df.append(df, ignore_index=True)
        df = temp_df
        return df
    elif int(year) == 2007:
        res = requests.get(eval(f"url_{year}"))
        res.encoding = "utf-8"
        df = pd.read_html(res.text)[0].iloc[1:, 1:]
        df.columns = pd.read_html(res.text)[0].iloc[0, 1:].tolist()
        temp_df = df
        for page in range(2, 11):
            # page = 1
            res = requests.get(eval(f"url_{year}").rsplit(".", maxsplit=1)[0] + "_" + str(page) + ".htm")
            res.encoding = "utf-8"
            text_df = pd.read_html(res.text)[0]
            df = text_df.iloc[1:, 1:]
            df.columns = text_df.iloc[0, 1:]
            temp_df = temp_df.append(df, ignore_index=True)
        df = temp_df
        return df


def fortune_rank_eng(year="1995"):
    """
    注意你的网速
    https://fortune.com/global500/
    https://fortune.com/global500/2012/search/
    :param year: "1995"
    :type year: str
    :return:
    :rtype: pandas.DataFrame
    """
    url = f"https://fortune.com/global500/{year}/search/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    code = json.loads(soup.find("script", attrs={"type": "application/ld+json"}).get_text())["identifier"]
    url = f"https://content.fortune.com/wp-json/irving/v1/data/franchise-search-results?list_id={code}"
    res = requests.get(url)
    big_df = pd.DataFrame()
    for i in range(len(res.json()[1]["items"][0]['fields'])):
        temp_df = pd.DataFrame([item["fields"][i] for item in res.json()[1]["items"]])
        big_df[temp_df["key"].values[0]] = temp_df["value"]
    big_df["rank"] = big_df["rank"].astype(int)
    big_df.sort_values("rank", inplace=True)
    big_df.reset_index(drop=True, inplace=True)
    return big_df


if __name__ == '__main__':
    fortune_rank_df = fortune_rank(year=2011)  # 2010 不一样
    print(fortune_rank_df)
    for year in range(1995, 2020):
        print(year)
        fortune_eng_df = fortune_rank_eng(year=year)
        print(fortune_eng_df)
