#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2020/5/27 19:57
Desc: 新浪财经-股票-机构持股
http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml
"""
from akshare.utils import demjson
import pandas as pd
import requests


def stock_institute_hold(quarter: str = "20051") -> pd.DataFrame:
    """
    新浪财经-股票-机构持股一览表
    http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml
    :param quarter: 从 2005 年开始, {"一季报":1, "中报":2 "三季报":3 "年报":4}, e.g., "20191", 其中的 1 表示一季报; "20193", 其中的 3 表示三季报;
    :type quarter: str
    :return: 机构持股一览表
    :rtype: pandas.DataFrame
    """
    url = "http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml?symbol=%D6%A4%C8%AF%BC%F2%B3%C6%BB%F2%B4%FA%C2%EB"
    params = {
        "p": "1",
        "num": "5000",
        "reportdate": quarter[:-1],
        "quarter": quarter[-1],
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_html(r.text)[0]
    temp_df["证券代码"] = temp_df["证券代码"].astype(str).str.zfill(6)
    del temp_df["明细"]
    temp_df.columns = ['证券代码', '证券简称', '机构数', '机构数变化', '持股比例', '持股比例增幅', '占流通股比例', '占流通股比例增幅']
    return temp_df


def stock_institute_hold_detail(stock: str = "600433", quarter: str = "20201") -> pd.DataFrame:
    """
    新浪财经-股票-机构持股详情
    http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml
    :param stock: 股票代码
    :type stock: str
    :param quarter: 从 2005 年开始, {"一季报":1, "中报":2 "三季报":3 "年报":4}, e.g., "20191", 其中的 1 表示一季报; "20193", 其中的 3 表示三季报;
    :type quarter: str
    :return: 指定股票和财报时间的机构持股数据
    :rtype: pandas.DataFrame
    """
    url = "http://vip.stock.finance.sina.com.cn/q/api/jsonp.php/var%20details=/ComStockHoldService.getJGCGDetail"
    params = {
        "symbol": stock,
        "quarter": quarter,
        }
    r = requests.get(url, params=params)
    text_data = r.text
    json_data = demjson.decode(text_data[text_data.find("{"):-2])
    big_df = pd.DataFrame()
    for item in json_data["data"].keys():
        inner_temp_df = pd.DataFrame(json_data["data"][item]).T.iloc[:-1, :]
        inner_temp_df.reset_index(inplace=True)
        big_df = big_df.append(inner_temp_df, ignore_index=True)
    if not big_df.empty:
        big_df["index"] = big_df["index"].str.split("_", expand=True)[0]
        big_df.rename(columns={"index": "institute"}, inplace=True)
        big_df = big_df.iloc[:, :12]
        big_df.columns = ["持股机构类型",
                          "持股机构代码",
                          "持股机构简称",
                          "持股机构全称",
                          "持股数",
                          "最新持股数",
                          "持股比例",
                          "最新持股比例",
                          "占流通股比例",
                          "最新占流通股比例",
                          "持股比例增幅",
                          "占流通股比例增幅",
                          ]
        big_df["持股机构类型"] = big_df["持股机构类型"].str.replace("fund", "基金")
        big_df["持股机构类型"] = big_df["持股机构类型"].str.replace("socialSecurity", "全国社保")
        big_df["持股机构类型"] = big_df["持股机构类型"].str.replace("qfii", "QFII")
        return big_df
    else:
        return None


if __name__ == '__main__':
    stock_institute_hold_df = stock_institute_hold(quarter="20201")
    print(stock_institute_hold_df)

    stock_institute_hold_detail_df = stock_institute_hold_detail(stock="300003", quarter="20201")
    print(stock_institute_hold_detail_df)
