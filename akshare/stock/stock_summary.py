#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/30 11:31
Desc: 股票数据-总貌-市场总貌
股票数据-总貌-成交概括
http://www.szse.cn/market/overview/index.html
http://www.sse.com.cn/market/stockdata/statistic/
"""
import warnings
from io import BytesIO

from akshare.utils import demjson
import pandas as pd
import requests

warnings.filterwarnings('ignore')


def stock_szse_summary(date: str = "20200619") -> pd.DataFrame:
    """
    深证证券交易所-总貌
    http://www.szse.cn/market/overview/index.html
    :param date: 最近结束交易日
    :type date: str
    :return: 深证证券交易所-总貌
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
    temp_df = pd.read_excel(BytesIO(r.content))
    temp_df["证券类别"] = temp_df["证券类别"].str.strip()
    temp_df.iloc[:, 2:] = temp_df.iloc[:, 2:].applymap(lambda x: x.replace(",", ""))
    temp_df.columns = [
        '证券类别',
        '数量',
        '成交金额',
        '成交量',
        '总股本',
        '总市值',
        '流通股本',
        '流通市值']
    temp_df['数量'] = pd.to_numeric(temp_df['数量'])
    temp_df['成交金额'] = pd.to_numeric(temp_df['成交金额'])
    temp_df['成交量'] = pd.to_numeric(temp_df['成交量'])
    temp_df['总股本'] = pd.to_numeric(temp_df['总股本'], errors="coerce")
    temp_df['总市值'] = pd.to_numeric(temp_df['总市值'], errors="coerce")
    temp_df['流通股本'] = pd.to_numeric(temp_df['流通股本'], errors="coerce")
    temp_df['流通市值'] = pd.to_numeric(temp_df['流通市值'], errors="coerce")
    return temp_df


def stock_sse_summary() -> pd.DataFrame:
    """
    上海证券交易所-总貌
    http://www.sse.com.cn/market/stockdata/statistic/
    :return: 上海证券交易所-总貌
    :rtype: pandas.DataFrame
    """
    url = "http://query.sse.com.cn/commonQuery.do"
    params = {
        'sqlId': 'COMMON_SSE_SJ_GPSJ_GPSJZM_TJSJ_L',
        'PRODUCT_NAME': '股票,主板,科创板',
        'type': 'inParams',
        '_': '1640855495128',
    }
    headers = {
        "Referer": "http://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    data_json.keys()
    temp_df = pd.DataFrame(data_json['result']).T
    temp_df.reset_index(inplace=True)
    temp_df['index'] = [
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
    temp_df = temp_df[temp_df['index'] != '-'].iloc[:-1, :]
    temp_df.columns = [
        '项目',
        '股票',
        '科创板',
        '主板',
    ]
    return temp_df


def stock_sse_deal_daily(date: str = "20220331") -> pd.DataFrame:
    """
    上海证券交易所-数据-股票数据-成交概况-股票成交概况-每日股票情况
    http://www.sse.com.cn/market/stockdata/overview/day/
    :return: 每日股票情况
    :rtype: pandas.DataFrame
    """
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
        temp_df['股票'] = pd.to_numeric(temp_df['股票'], errors="coerce")
        temp_df['主板A'] = pd.to_numeric(temp_df['主板A'], errors="coerce")
        temp_df['主板B'] = pd.to_numeric(temp_df['主板B'], errors="coerce")
        temp_df['科创板'] = pd.to_numeric(temp_df['科创板'], errors="coerce")
        temp_df['股票回购'] = pd.to_numeric(temp_df['股票回购'], errors="coerce")
        return temp_df
    elif int(date) <= 20220224:
        url = "http://query.sse.com.cn/commonQuery.do"
        params = {
            'sqlId': 'COMMON_SSE_SJ_GPSJ_CJGK_MRGK_C',
            'SEARCH_DATE': "-".join([date[:4], date[4:6], date[6:]]),
            '_': '1640836561673',
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
        temp_df = temp_df[[
            "单日情况",
            "主板A",
            "主板B",
            "科创板",
        ]]
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
        temp_df['主板A'] = pd.to_numeric(temp_df['主板A'], errors="coerce")
        temp_df['主板B'] = pd.to_numeric(temp_df['主板B'], errors="coerce")
        temp_df['科创板'] = pd.to_numeric(temp_df['科创板'], errors="coerce")
        return temp_df
    else:
        url = "http://query.sse.com.cn/commonQuery.do"
        params = {
            'sqlId': 'COMMON_SSE_SJ_GPSJ_CJGK_MRGK_C',
            'PRODUCT_CODE': '01,02,03,11,17',
            'type': 'inParams',
            'SEARCH_DATE': "-".join([date[:4], date[4:6], date[6:]]),
            '_': '1640836561673',
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
            temp_df['股票回购'] = '-'
        else:
            temp_df.columns = [
                "单日情况",
                "主板A",
                "主板B",
                "科创板",
                "股票回购",
                "股票",
            ]
        temp_df = temp_df[[
            "单日情况",
            "股票",
            "主板A",
            "主板B",
            "科创板",
            "股票回购",
        ]]
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
        temp_df['主板A'] = pd.to_numeric(temp_df['主板A'], errors="coerce")
        temp_df['主板B'] = pd.to_numeric(temp_df['主板B'], errors="coerce")
        temp_df['科创板'] = pd.to_numeric(temp_df['科创板'], errors="coerce")
        temp_df['股票'] = pd.to_numeric(temp_df['股票'], errors="coerce")
        temp_df['股票回购'] = pd.to_numeric(temp_df['股票回购'], errors="coerce")
        return temp_df


if __name__ == "__main__":
    stock_szse_summary_df = stock_szse_summary(date="20211202")
    print(stock_szse_summary_df)

    stock_sse_summary_df = stock_sse_summary()
    print(stock_sse_summary_df)

    stock_sse_deal_daily_df = stock_sse_deal_daily(date="20211221")
    print(stock_sse_deal_daily_df)

    stock_sse_deal_daily_df = stock_sse_deal_daily(date="20211227")
    print(stock_sse_deal_daily_df)

    stock_sse_deal_daily_df = stock_sse_deal_daily(date="20220225")
    print(stock_sse_deal_daily_df)
