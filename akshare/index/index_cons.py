# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2020/1/4 16:19
contact: jindaxiang@163.com
desc: 获取股票指数成份股数据, 新浪有两个接口, 这里使用老接口:
新接口：http://vip.stock.finance.sina.com.cn/mkt/#zhishu_000001
老接口：http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page=1&indexid=399639
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup


# def index_stock_cons(index="000905"):
#     """
#     新浪新版股票指数成份页面, 暂时不用
#     :param index:
#     :type index:
#     :return:
#     :rtype:
#     """
#     import demjson
#     if index == "000300":
#         temp_df = pd.DataFrame()
#         for page in range(1, 5):
#             url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
#             params = {
#                 "page": str(page),
#                 "num": "80",
#                 "sort": "symbol",
#                 "asc": "1",
#                 "node": "hs300",
#                 "symbol": "",
#                 "_s_r_a": "init",
#             }
#             r = requests.get(url, params=params)
#             temp_df = temp_df.append(pd.DataFrame(demjson.decode(r.text)), ignore_index=True)
#         return temp_df
#     url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple"
#     params = {
#         "page": "1",
#         "num": "3000",
#         "sort": "symbol",
#         "asc": "1",
#         "node": f"zhishu_{index}",
#         "_s_r_a": "setlen",
#     }
#     r = requests.get(url, params=params)
#     return pd.DataFrame(demjson.decode(r.text))


def index_stock_info() -> pd.DataFrame:
    """
    聚宽-指数数据-指数列表
    https://www.joinquant.com/data/dict/indexData
    :return: 指数信息的数据框
    :rtype: pandas.DataFrame
    """
    index_df = pd.read_html("https://www.joinquant.com/data/dict/indexData")[0]
    index_df["指数代码"] = index_df["指数代码"].str.split(".", expand=True)[0]
    index_df.columns = ["index_code", "display_name", "publish_date", "-", "-"]
    return index_df[["index_code", "display_name", "publish_date"]]


def index_stock_cons(index: str = "000031") -> pd.DataFrame:
    """
    最新股票指数的成份股目录
    http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page=1&indexid=399639
    :param index: 指数代码, 可以通过 index_stock_info 函数获取
    :type index: str
    :return: 最新股票指数的成份股目录
    :rtype: pandas.DataFrame
    """
    url = f"http://vip.stock.finance.sina.com.cn/corp/go.php/vII_NewestComponent/indexid/{index}.phtml"
    r = requests.get(url)
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, "lxml")
    page_num = (
        soup.find(attrs={"class": "table2"})
        .find("td")
        .find_all("a")[-1]["href"]
        .split("page=")[-1]
        .split("&")[0]
    )
    if page_num == "#":
        temp_df = pd.read_html(r.text, header=1)[3].iloc[:, :3]
        temp_df["品种代码"] = temp_df["品种代码"].astype(str).str.zfill(6)
        return temp_df

    temp_df = pd.DataFrame()
    for page in range(1, int(page_num) + 1):
        url = f"http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page={page}&indexid={index}"
        r = requests.get(url)
        r.encoding = "gb2312"
        temp_df = temp_df.append(pd.read_html(r.text, header=1)[3], ignore_index=True)
    temp_df = temp_df.iloc[:, :3]
    temp_df["品种代码"] = temp_df["品种代码"].astype(str).str.zfill(6)
    return temp_df


if __name__ == "__main__":
    index_list = index_stock_info()["index_code"].tolist()
    index_stock_cons_df = index_stock_cons(index="000312")
    print(index_stock_cons_df)
    for item in index_list:
        index_stock_cons_df = index_stock_cons(index=item)
        print(index_stock_cons_df)

