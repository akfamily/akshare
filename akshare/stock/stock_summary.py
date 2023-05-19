#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/5/3 17:00
Desc: 股票数据-总貌-市场总貌
股票数据-总貌-成交概括
https://www.szse.cn/market/overview/index.html
https://www.sse.com.cn/market/stockdata/statistic/
"""
import warnings
from io import BytesIO

import pandas as pd
import requests
from bs4 import BeautifulSoup


def stock_szse_summary(date: str = "20200619") -> pd.DataFrame:
    """
    深证证券交易所-总貌-证券类别统计
    https://www.szse.cn/market/overview/index.html
    :param date: 最近结束交易日
    :type date: str
    :return: 证券类别统计
    :rtype: pandas.DataFrame
    """
    url = "http://www.szse.cn/api/report/ShowReport"
    params = {
        "SHOWTYPE": "xlsx",
        "CATALOGID": "1803_sczm",
        "TABKEY": "tab1",
        "txtQueryDate": "-".join([date[:4], date[4:6], date[6:]]),
        "random": "0.39339437497296137",
    }
    r = requests.get(url, params=params)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        temp_df = pd.read_excel(BytesIO(r.content), engine="openpyxl")
    temp_df["证券类别"] = temp_df["证券类别"].str.strip()
    temp_df.iloc[:, 2:] = temp_df.iloc[:, 2:].applymap(lambda x: x.replace(",", ""))
    temp_df.columns = ["证券类别", "数量", "成交金额", "总市值", "流通市值"]
    temp_df["数量"] = pd.to_numeric(temp_df["数量"])
    temp_df["成交金额"] = pd.to_numeric(temp_df["成交金额"])
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
    temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
    return temp_df


def stock_szse_area_summary(date: str = "202203") -> pd.DataFrame:
    """
    深证证券交易所-总貌-地区交易排序
    https://www.szse.cn/market/overview/index.html
    :param date: 最近结束交易日
    :type date: str
    :return: 地区交易排序
    :rtype: pandas.DataFrame
    """
    url = "http://www.szse.cn/api/report/ShowReport"
    params = {
        "SHOWTYPE": "xlsx",
        "CATALOGID": "1803_sczm",
        "TABKEY": "tab2",
        "DATETIME": "-".join([date[:4], date[4:6]]),
        "random": "0.39339437497296137",
    }
    r = requests.get(url, params=params)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        temp_df = pd.read_excel(BytesIO(r.content), engine="openpyxl")
    temp_df.columns = ["序号", "地区", "总交易额", "占市场", "股票交易额", "基金交易额", "债券交易额"]
    temp_df["总交易额"] = temp_df["总交易额"].str.replace(",", "")
    temp_df["总交易额"] = pd.to_numeric(temp_df["总交易额"])
    temp_df["占市场"] = pd.to_numeric(temp_df["占市场"])
    temp_df["股票交易额"] = temp_df["股票交易额"].str.replace(",", "")
    temp_df["股票交易额"] = pd.to_numeric(temp_df["股票交易额"], errors="coerce")
    temp_df["基金交易额"] = temp_df["基金交易额"].str.replace(",", "")
    temp_df["基金交易额"] = pd.to_numeric(temp_df["基金交易额"], errors="coerce")
    temp_df["债券交易额"] = temp_df["债券交易额"].str.replace(",", "")
    temp_df["债券交易额"] = pd.to_numeric(temp_df["债券交易额"], errors="coerce")
    return temp_df


def stock_szse_sector_summary(symbol: str = "当月", date: str = "202303") -> pd.DataFrame:
    """
    深圳证券交易所-统计资料-股票行业成交数据
    https://docs.static.szse.cn/www/market/periodical/month/W020220511355248518608.html
    :param symbol: choice of {"当月", "当年"}
    :type symbol: str
    :param date: 交易年月
    :type date: str
    :return: 股票行业成交数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.szse.cn/market/periodical/month/index.html"
    r = requests.get(url)
    r.encoding = "utf8"
    soup = BeautifulSoup(r.text, "lxml")
    tags_list = soup.find_all("div", attrs={"class": "g-container"})[1].find_all(
        "script"
    )
    tags_dict = [
        eval(
            item.string[item.string.find("{") : item.string.find("}") + 1]
            .replace("\n", "")
            .replace(" ", "")
            .replace("value", "'value'")
            .replace("text", "'text'")
        )
        for item in tags_list
    ]
    date_url_dict = dict(
        zip(
            [item["text"] for item in tags_dict],
            [item["value"][2:] for item in tags_dict],
        )
    )
    date_format = "-".join([date[:4], date[4:]])
    url = f"http://www.szse.cn/market/periodical/month/{date_url_dict[date_format]}"
    r = requests.get(url)
    r.encoding = "utf8"
    soup = BeautifulSoup(r.text, "lxml")
    url = [item for item in soup.find_all("a") if item.get_text() == "股票行业成交数据"][0]["href"]

    if symbol == "当月":
        temp_df = pd.read_html(url, encoding="gbk")[0]
        temp_df.columns = [
            "项目名称",
            "项目名称-英文",
            "交易天数",
            "成交金额-人民币元",
            "成交金额-占总计",
            "成交股数-股数",
            "成交股数-占总计",
            "成交笔数-笔",
            "成交笔数-占总计",
        ]
    else:
        temp_df = pd.read_html(url, encoding="gbk")[1]
        temp_df.columns = [
            "项目名称",
            "项目名称-英文",
            "交易天数",
            "成交金额-人民币元",
            "成交金额-占总计",
            "成交股数-股数",
            "成交股数-占总计",
            "成交笔数-笔",
            "成交笔数-占总计",
        ]

    temp_df["交易天数"] = pd.to_numeric(temp_df["交易天数"], errors="coerce")
    temp_df["成交金额-人民币元"] = pd.to_numeric(temp_df["成交金额-人民币元"], errors="coerce")
    temp_df["成交金额-占总计"] = pd.to_numeric(temp_df["成交金额-占总计"], errors="coerce")
    temp_df["成交股数-股数"] = pd.to_numeric(temp_df["成交股数-股数"], errors="coerce")
    temp_df["成交股数-占总计"] = pd.to_numeric(temp_df["成交股数-占总计"], errors="coerce")
    temp_df["成交笔数-笔"] = pd.to_numeric(temp_df["成交笔数-笔"], errors="coerce")
    temp_df["成交笔数-占总计"] = pd.to_numeric(temp_df["成交笔数-占总计"], errors="coerce")
    return temp_df


def stock_sse_summary() -> pd.DataFrame:
    """
    上海证券交易所-总貌
    https://www.sse.com.cn/market/stockdata/statistic/
    :return: 上海证券交易所-总貌
    :rtype: pandas.DataFrame
    """
    url = "http://query.sse.com.cn/commonQuery.do"
    params = {
        "sqlId": "COMMON_SSE_SJ_GPSJ_GPSJZM_TJSJ_L",
        "PRODUCT_NAME": "股票,主板,科创板",
        "type": "inParams",
        "_": "1640855495128",
    }
    headers = {
        "Referer": "http://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]).T
    temp_df.reset_index(inplace=True)
    temp_df["index"] = [
        "流通股本",
        "总市值",
        "平均市盈率",
        "上市公司",
        "上市股票",
        "流通市值",
        "报告时间",
        "-",
        "总股本",
        "项目",
    ]
    temp_df = temp_df[temp_df["index"] != "-"].iloc[:-1, :]
    temp_df.columns = [
        "项目",
        "股票",
        "主板",
        "科创板",
    ]
    return temp_df


def stock_sse_deal_daily(date: str = "20180117") -> pd.DataFrame:
    """
    上海证券交易所-数据-股票数据-成交概况-股票成交概况-每日股票情况
    http://www.sse.com.cn/market/stockdata/overview/day/
    :return: 每日股票情况
    :rtype: pandas.DataFrame
    """
    if int(date) <= 20181231:
        url = "http://query.sse.com.cn/commonQuery.do"
        params = {
            "searchDate": "-".join([date[:4], date[4:6], date[6:]]),
            "sqlId": "COMMON_SSE_SJ_GPSJ_CJGK_DAYCJGK_C",
            "stockType": "90",
            "_": "1616744620492",
        }
        headers = {
            "Referer": "http://www.sse.com.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"])
        temp_df = temp_df.T
        temp_df.reset_index(inplace=True)
        temp_df.columns = [
            "单日情况",
            "主板A",
            "-",
            "主板B",
        ]
        temp_df = temp_df[
            [
                "单日情况",
                "主板A",
                "主板B",
            ]
        ]
        temp_df["单日情况"] = [
            "流通市值",
            "流通换手率",
            "平均市盈率",
            "_",
            "市价总值",
            "_",
            "换手率",
            "_",
            "挂牌数",
            "_",
            "_",
            "_",
            "_",
            "_",
            "成交笔数",
            "成交金额",
            "成交量",
            "次新股换手率",
            "_",
            "_",
        ]
        temp_df = temp_df[temp_df["单日情况"] != "_"]
        temp_df["单日情况"] = temp_df["单日情况"].astype("category")
        list_custom_new = [
            "挂牌数",
            "市价总值",
            "流通市值",
            "成交金额",
            "成交量",
            "成交笔数",
            "平均市盈率",
            "换手率",
            "次新股换手率",
            "流通换手率",
        ]
        temp_df["单日情况"].cat.set_categories(list_custom_new)
        temp_df.sort_values("单日情况", ascending=True, inplace=True)
        temp_df.reset_index(drop=True, inplace=True)
        # 构建空
        temp_df['股票'] = "-"
        temp_df['科创板'] = "-"
        temp_df['股票回购'] = "-"
        temp_df["股票"] = pd.to_numeric(temp_df["股票"], errors="coerce")
        temp_df["主板A"] = pd.to_numeric(temp_df["主板A"], errors="coerce")
        temp_df["主板B"] = pd.to_numeric(temp_df["主板B"], errors="coerce")
        temp_df["科创板"] = pd.to_numeric("-", errors="coerce")  # 默认位空
        temp_df["股票回购"] = pd.to_numeric(temp_df["股票回购"], errors="coerce")
        temp_df = temp_df[
            [
                "单日情况",
                "股票",
                "主板A",
                "主板B",
                "科创板",
                "股票回购",
            ]
        ]
        return temp_df
    if int(date) <= 20211224:
        url = "http://query.sse.com.cn/commonQuery.do"
        params = {
            "searchDate": "-".join([date[:4], date[4:6], date[6:]]),
            "sqlId": "COMMON_SSE_SJ_GPSJ_CJGK_DAYCJGK_C",
            "stockType": "90",
            "_": "1616744620492",
        }
        headers = {
            "Referer": "http://www.sse.com.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"])
        temp_df = temp_df.T
        temp_df.reset_index(inplace=True)
        if len(temp_df.columns) == 6:
            temp_df.columns = [
                "单日情况",
                "-",
                "股票",
                "主板B",
                "主板A",
                "股票回购",
            ]
            temp_df = temp_df[
                [
                    "单日情况",
                    "股票",
                    "主板A",
                    "主板B",
                    "股票回购",
                ]
            ]
            temp_df["单日情况"] = [
                "流通市值",
                "流通换手率",
                "平均市盈率",
                "_",
                "市价总值",
                "_",
                "换手率",
                "_",
                "挂牌数",
                "_",
                "_",
                "_",
                "_",
                "_",
                "成交笔数",
                "成交金额",
                "成交量",
                "次新股换手率",
                "_",
                "_",
            ]
            temp_df = temp_df[temp_df["单日情况"] != "_"]
            temp_df["单日情况"] = temp_df["单日情况"].astype("category")
            list_custom_new = [
                "挂牌数",
                "市价总值",
                "流通市值",
                "成交金额",
                "成交量",
                "成交笔数",
                "平均市盈率",
                "换手率",
                "次新股换手率",
                "流通换手率",
            ]
            temp_df["单日情况"].cat.set_categories(list_custom_new)
            temp_df.sort_values("单日情况", ascending=True, inplace=True)
            temp_df.reset_index(drop=True, inplace=True)
            temp_df["股票"] = pd.to_numeric(temp_df["股票"], errors="coerce")
            temp_df["主板A"] = pd.to_numeric(temp_df["主板A"], errors="coerce")
            temp_df["主板B"] = pd.to_numeric(temp_df["主板B"], errors="coerce")
            temp_df["科创板"] = pd.to_numeric("-", errors="coerce")  # 默认位空
            temp_df["股票回购"] = pd.to_numeric(temp_df["股票回购"], errors="coerce")
            temp_df = temp_df[
                [
                    "单日情况",
                    "股票",
                    "主板A",
                    "主板B",
                    "科创板",
                    "股票回购",
                ]
            ]
            return temp_df
        else:
            temp_df.columns = [
                "单日情况",
                "主板A",
                "股票",
                "主板B",
                "_",
                "股票回购",
                "科创板",
            ]
            temp_df = temp_df[
                [
                    "单日情况",
                    "股票",
                    "主板A",
                    "主板B",
                    "科创板",
                    "股票回购",
                ]
            ]
            temp_df["单日情况"] = [
                "流通市值",
                "流通换手率",
                "平均市盈率",
                "_",
                "市价总值",
                "_",
                "换手率",
                "_",
                "挂牌数",
                "_",
                "_",
                "_",
                "_",
                "_",
                "成交笔数",
                "成交金额",
                "成交量",
                "次新股换手率",
                "_",
                "_",
            ]
            temp_df = temp_df[temp_df["单日情况"] != "_"]
            temp_df["单日情况"] = temp_df["单日情况"].astype("category")
            list_custom_new = [
                "挂牌数",
                "市价总值",
                "流通市值",
                "成交金额",
                "成交量",
                "成交笔数",
                "平均市盈率",
                "换手率",
                "次新股换手率",
                "流通换手率",
            ]
            temp_df["单日情况"].cat.set_categories(list_custom_new)
            temp_df.sort_values("单日情况", ascending=True, inplace=True)
            temp_df.reset_index(drop=True, inplace=True)
            temp_df["股票"] = pd.to_numeric(temp_df["股票"], errors="coerce")
            temp_df["主板A"] = pd.to_numeric(temp_df["主板A"], errors="coerce")
            temp_df["主板B"] = pd.to_numeric(temp_df["主板B"], errors="coerce")
            temp_df["科创板"] = pd.to_numeric(temp_df["科创板"], errors="coerce")
            temp_df["股票回购"] = pd.to_numeric(temp_df["股票回购"], errors="coerce")
            return temp_df
    elif int(date) <= 20220224:
        url = "http://query.sse.com.cn/commonQuery.do"
        params = {
            "sqlId": "COMMON_SSE_SJ_GPSJ_CJGK_MRGK_C",
            "SEARCH_DATE": "-".join([date[:4], date[4:6], date[6:]]),
            "_": "1640836561673",
        }
        headers = {
            "Referer": "http://www.sse.com.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"])
        temp_df = temp_df.T
        temp_df.reset_index(inplace=True)
        temp_df.columns = [
            "单日情况",
            "主板A",
            "主板B",
            "科创板",
            "-",
            "-",
            "-",
            "-",
            "-",
        ]
        temp_df = temp_df[
            [
                "单日情况",
                "主板A",
                "主板B",
                "科创板",
            ]
        ]
        temp_df["单日情况"] = [
            "市价总值",
            "成交量",
            "平均市盈率",
            "换手率",
            "成交金额",
            "-",
            "流通市值",
            "流通换手率",
            "报告日期",
            "挂牌数",
            "-",
        ]
        temp_df = temp_df[temp_df["单日情况"] != "-"]
        temp_df["单日情况"] = temp_df["单日情况"].astype("category")
        list_custom_new = [
            "挂牌数",
            "市价总值",
            "流通市值",
            "成交金额",
            "成交量",
            "平均市盈率",
            "换手率",
            "流通换手率",
        ]
        temp_df["单日情况"].cat.set_categories(list_custom_new)
        temp_df.sort_values("单日情况", ascending=True, inplace=True)
        temp_df.reset_index(inplace=True, drop=True)
        temp_df["主板A"] = pd.to_numeric(temp_df["主板A"], errors="coerce")
        temp_df["主板B"] = pd.to_numeric(temp_df["主板B"], errors="coerce")
        temp_df["科创板"] = pd.to_numeric(temp_df["科创板"], errors="coerce")
        return temp_df
    else:
        url = "http://query.sse.com.cn/commonQuery.do"
        params = {
            "sqlId": "COMMON_SSE_SJ_GPSJ_CJGK_MRGK_C",
            "PRODUCT_CODE": "01,02,03,11,17",
            "type": "inParams",
            "SEARCH_DATE": "-".join([date[:4], date[4:6], date[6:]]),
            "_": "1640836561673",
        }
        headers = {
            "Referer": "http://www.sse.com.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"])
        temp_df = temp_df.T
        temp_df.reset_index(inplace=True)
        if len(temp_df.T) == 5:
            temp_df.columns = [
                "单日情况",
                "主板A",
                "主板B",
                "科创板",
                "股票",
            ]
            temp_df["股票回购"] = "-"
        else:
            temp_df.columns = [
                "单日情况",
                "主板A",
                "主板B",
                "科创板",
                "股票回购",
                "股票",
            ]
        temp_df = temp_df[
            [
                "单日情况",
                "股票",
                "主板A",
                "主板B",
                "科创板",
                "股票回购",
            ]
        ]
        temp_df["单日情况"] = [
            "市价总值",
            "成交量",
            "平均市盈率",
            "换手率",
            "成交金额",
            "-",
            "流通市值",
            "流通换手率",
            "报告日期",
            "挂牌数",
            "-",
        ]
        temp_df = temp_df[temp_df["单日情况"] != "-"]
        temp_df["单日情况"] = temp_df["单日情况"].astype("category")
        list_custom_new = [
            "挂牌数",
            "市价总值",
            "流通市值",
            "成交金额",
            "成交量",
            "平均市盈率",
            "换手率",
            "流通换手率",
        ]
        temp_df["单日情况"].cat.set_categories(list_custom_new)
        temp_df.sort_values("单日情况", ascending=True, inplace=True)
        temp_df.reset_index(inplace=True, drop=True)
        temp_df["主板A"] = pd.to_numeric(temp_df["主板A"], errors="coerce")
        temp_df["主板B"] = pd.to_numeric(temp_df["主板B"], errors="coerce")
        temp_df["科创板"] = pd.to_numeric(temp_df["科创板"], errors="coerce")
        temp_df["股票"] = pd.to_numeric(temp_df["股票"], errors="coerce")
        temp_df["股票回购"] = pd.to_numeric(temp_df["股票回购"], errors="coerce")
        return temp_df


if __name__ == "__main__":
    stock_szse_summary_df = stock_szse_summary(date="20070511")
    print(stock_szse_summary_df)

    stock_szse_area_summary_df = stock_szse_area_summary(date="202203")
    print(stock_szse_area_summary_df)

    stock_szse_sector_summary_df = stock_szse_sector_summary(symbol="当月", date="202303")
    print(stock_szse_sector_summary_df)

    stock_sse_summary_df = stock_sse_summary()
    print(stock_sse_summary_df)

    stock_sse_deal_daily_df = stock_sse_deal_daily(date="20211221")
    print(stock_sse_deal_daily_df)

    stock_sse_deal_daily_df = stock_sse_deal_daily(date="20211227")
    print(stock_sse_deal_daily_df)

    stock_sse_deal_daily_df = stock_sse_deal_daily(date="20190613")
    print(stock_sse_deal_daily_df)

    stock_sse_deal_daily_df = stock_sse_deal_daily(date="20080131")
    print(stock_sse_deal_daily_df)
