# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/10 21:55
contact: jindaxiang@163.com
desc: 历年世界500强榜单数据
http://www.fortunechina.com/fortune500/index.htm
特殊情况说明：
2010年由于网页端没有公布公司所属的国家, 故 2010 年数据没有国家这列
"""
import requests
import pandas as pd

from akshare.fortune.cons import (
    url_1996,
    url_1997,
    url_1998,
    url_1999,
    url_2000,
    url_2001,
    url_2002,
    url_2003,
    url_2004,
    url_2005,
    url_2006,
    url_2007,
    url_2008,
    url_2009,
    url_2010,
    url_2011,
    url_2012,
    url_2013,
    url_2014,
    url_2015,
    url_2016,
    url_2017,
    url_2018,
    url_2019,
)


def fortune_rank(year="2015"):
    """
    获取财富500强公司从1996年开始的排行榜
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


if __name__ == '__main__':
    df = fortune_rank(year=2011)  # 2010 不一样
    print(df)
