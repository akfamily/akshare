#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/8/22 18:39
Desc: 东方财富网-数据中心-研究报告-东方财富分析师指数
http://data.eastmoney.com/invest/invest/list.html
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_analyst_rank_em(year: str = "2022") -> pd.DataFrame:
    """
    东方财富网-数据中心-研究报告-东方财富分析师指数-东方财富分析师指数
    http://data.eastmoney.com/invest/invest/list.html
    :param year: 从 2015 年至今
    :type year: str
    :return: 东方财富分析师指数
    :rtype: pandas.DataFrame
    """
    url = "https://data.eastmoney.com/dataapi/invest/list"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    params = {
        "sortColumns": "YEAR_YIELD",
        "sortTypes": "-1",
        "pageSize": "50",
        "pageNumber": "1",
        "reportName": "RPT_ANALYST_INDEX_RANK",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f'(YEAR="{year}")',
        "limit": "top100",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1)):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        data_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, data_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = list(range(1, len(big_df) + 1))
    big_df.columns = [
        "序号",
        "分析师ID",
        "分析师名称",
        "更新日期",
        "年度",
        "分析师单位",
        "_",
        "年度指数",
        f"{year}年收益率",
        "3个月收益率",
        "6个月收益率",
        "12个月收益率",
        "成分股个数",
        f"{year}最新个股评级-股票名称",
        "_",
        f"{year}最新个股评级-股票代码",
        "_",
        "行业代码",
        "行业",
    ]
    big_df = big_df[
        [
            "序号",
            "分析师名称",
            "分析师单位",
            "年度指数",
            f"{year}年收益率",
            "3个月收益率",
            "6个月收益率",
            "12个月收益率",
            "成分股个数",
            f"{year}最新个股评级-股票名称",
            f"{year}最新个股评级-股票代码",
            "分析师ID",
            "行业代码",
            "行业",
            "更新日期",
            "年度",
        ]
    ]
    big_df["更新日期"] = pd.to_datetime(big_df["更新日期"]).dt.date
    big_df["年度指数"] = pd.to_numeric(big_df["年度指数"])
    big_df[f"{year}年收益率"] = pd.to_numeric(big_df[f"{year}年收益率"])
    big_df["3个月收益率"] = pd.to_numeric(big_df["3个月收益率"])
    big_df["6个月收益率"] = pd.to_numeric(big_df["6个月收益率"])
    big_df["12个月收益率"] = pd.to_numeric(big_df["12个月收益率"])
    big_df["成分股个数"] = pd.to_numeric(big_df["成分股个数"])
    return big_df


def stock_analyst_detail_em(
    analyst_id: str = "11000200926", indicator: str = "最新跟踪成分股"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-研究报告-东方财富分析师指数-东方财富分析师指数2020最新排行-分析师详情
    http://data.eastmoney.com/invest/invest/11000200926.html
    :param analyst_id: 分析师 ID, 从 ak.stock_analyst_rank_em() 获取
    :type analyst_id: str
    :param indicator: ["最新跟踪成分股", "历史跟踪成分股", "历史指数"]
    :type indicator: str
    :return: 具体指标的数据
    :rtype: pandas.DataFrame
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    url = "http://data.eastmoney.com/dataapi/invest/other"
    if indicator == "最新跟踪成分股":
        params = {
            "href": "/api/Zgfxzs/json/AnalysisIndexNew.aspx",
            "paramsstr": f"index=1&size=100&code={analyst_id}",
        }
        r = requests.get(url, params=params, headers=headers)
        json_data = r.json()
        if len(json_data) == 0:
            return pd.DataFrame()
        temp_df = pd.DataFrame(json_data["re"])
        temp_df.reset_index(inplace=True)
        temp_df["index"] = list(range(1, len(temp_df) + 1))
        temp_df.columns = [
            "序号",
            "股票代码",
            "股票名称",
            "调入日期",
            "当前评级名称",
            "成交价格(前复权)",
            "最新价格",
            "最新评级日期",
            "_",
            "阶段涨跌幅",
        ]
        temp_df = temp_df[
            [
                "序号",
                "股票代码",
                "股票名称",
                "调入日期",
                "最新评级日期",
                "当前评级名称",
                "成交价格(前复权)",
                "最新价格",
                "阶段涨跌幅",
            ]
        ]
        temp_df["调入日期"] = pd.to_datetime(temp_df["调入日期"]).dt.date
        temp_df["最新评级日期"] = pd.to_datetime(temp_df["最新评级日期"]).dt.date
        temp_df["成交价格(前复权)"] = pd.to_numeric(temp_df["成交价格(前复权)"])
        temp_df["最新价格"] = pd.to_numeric(temp_df["最新价格"])
        temp_df["阶段涨跌幅"] = pd.to_numeric(temp_df["阶段涨跌幅"])
        return temp_df
    elif indicator == "历史跟踪成分股":
        params = {
            "href": "/api/Zgfxzs/json/AnalysisIndexls.aspx",
            "paramsstr": f"index=1&size=100&code={analyst_id}",
        }
        r = requests.get(url, params=params, headers=headers)
        json_data = r.json()
        temp_df = pd.DataFrame(json_data["re"])
        temp_df.reset_index(inplace=True)
        temp_df["index"] = list(range(1, len(temp_df) + 1))
        temp_df.columns = [
            "序号",
            "股票代码",
            "股票名称",
            "调入日期",
            "调出日期",
            "调入时评级名称",
            "调出原因",
            "_",
            "累计涨跌幅",
        ]
        temp_df = temp_df[
            [
                "序号",
                "股票代码",
                "股票名称",
                "调入日期",
                "调出日期",
                "调入时评级名称",
                "调出原因",
                "累计涨跌幅",
            ]
        ]
        temp_df["调入日期"] = pd.to_datetime(temp_df["调入日期"]).dt.date
        temp_df["调出日期"] = pd.to_datetime(temp_df["调出日期"]).dt.date
        temp_df["累计涨跌幅"] = pd.to_numeric(temp_df["累计涨跌幅"])
        return temp_df
    elif indicator == "历史指数":
        params = {
            "href": "/DataCenter_V3/chart/AnalystsIndex.ashx",
            "paramsstr": f"code={analyst_id}&d=&isxml=True",
        }
        r = requests.get(url, params=params, headers=headers)
        json_data = r.json()
        temp_df = pd.DataFrame(
            [json_data["X"].split(","), json_data["Y"][0].split(",")],
            index=["date", "value"],
        ).T
        temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
        temp_df["value"] = pd.to_numeric(temp_df["value"])
        return temp_df


if __name__ == "__main__":
    stock_analyst_rank_em_df = stock_analyst_rank_em(year="2022")
    print(stock_analyst_rank_em_df)

    stock_analyst_detail_em_df = stock_analyst_detail_em(
        analyst_id="11000200926", indicator="最新跟踪成分股"
    )
    print(stock_analyst_detail_em_df)

    stock_analyst_detail_em_df = stock_analyst_detail_em(
        analyst_id="11000200926", indicator="历史跟踪成分股"
    )
    print(stock_analyst_detail_em_df)

    stock_analyst_detail_em_df = stock_analyst_detail_em(
        analyst_id="11000200926", indicator="历史指数"
    )
    print(stock_analyst_detail_em_df)
