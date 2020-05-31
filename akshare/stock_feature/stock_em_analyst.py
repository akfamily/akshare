# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/3/22 15:39
Desc: 东方财富网-数据中心-研究报告-东方财富分析师指数
http://data.eastmoney.com/invest/invest/list.html
"""
import requests
import pandas as pd
import json


def stock_em_analyst_rank():
    """
    东方财富网-数据中心-研究报告-东方财富分析师指数-东方财富分析师指数2020最新排行
    :return: 东方财富分析师指数2020最新排行
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    url = "http://data.eastmoney.com/invest/invest/ajax.aspx"
    params = {
        "st": "0",
        "sr": "-1",
        "p": "1",
        "ps": "500",
        "js": "nPqXnjcx",
        "type": "all",
        "name": "",
        "rt": "52828756",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = json.loads(r.text.strip("var nPqXnjcx ="))["data"]
    data_df = pd.DataFrame(data_json)
    result_df = data_df[
        [
            "LastYearIndex",
            "LastYearSyl",
            "StockName",
            "FxsName",
            "Ssjg",
            "NewIndex",
            "Earnings_3",
            "Earnings_6",
            "Earnings_12",
            "NewGgpj",
            "Jyrq",
            "JyrqStr",
            "FxsCode",
            "CfgGs",
            "stockcount",
            "Industrycode",
        ]
    ]
    return result_df


def stock_em_analyst_detail(
    analyst_id: str = "11000257131", indicator: str = "最新跟踪成分股"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-研究报告-东方财富分析师指数-东方财富分析师指数2020最新排行-分析师详情
    :param analyst_id: 分析师ID, 从 stock_em_analyst_rank 获取
    :type analyst_id: str
    :param indicator: ["最新跟踪成分股", "历史跟踪成分股", "历史指数"]
    :type indicator: str
    :return: 具体指标的数据
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    url = f"http://data.eastmoney.com/invest/invest/{analyst_id}.html"
    r = requests.get(url, headers=headers)
    current_stock_df = pd.read_html(r.text)[0]
    history_stock_df = pd.read_html(r.text)[1]
    if indicator == "最新跟踪成分股":
        return current_stock_df
    elif indicator == "历史跟踪成分股":
        return history_stock_df
    elif indicator == "历史指数":
        url = "http://data.eastmoney.com/DataCenter_V3/chart/AnalystsIndex.ashx"
        params = {
            "code": f"{analyst_id}",
            "r": "0.5281549337680276",
            "isxml": "false",
        }
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        data_df = pd.DataFrame(
            [data_json["X"].split(","), data_json["Y"][0].split(",")],
            index=["date", "value"],
        ).T
        return data_df


if __name__ == "__main__":
    stock_em_analyst_rank_df = stock_em_analyst_rank()
    print(stock_em_analyst_rank_df)
    stock_em_analyst_detail_current_stock_df = stock_em_analyst_detail(
        analyst_id="11000257131", indicator="最新跟踪成分股"
    )
    print(stock_em_analyst_detail_current_stock_df)
    stock_em_analyst_detail_history_stock_df = stock_em_analyst_detail(
        analyst_id="11000257131", indicator="历史跟踪成分股"
    )
    print(stock_em_analyst_detail_history_stock_df)
    stock_em_analyst_detail_index_df = stock_em_analyst_detail(
        analyst_id="11000257131", indicator="历史指数"
    )
    print(stock_em_analyst_detail_index_df)
