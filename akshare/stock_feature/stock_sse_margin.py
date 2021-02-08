# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/2/8 16:40
Desc: 上海证券交易所-融资融券数据
http://www.sse.com.cn/market/othersdata/margin/sum/
"""
import pandas as pd
import requests


def stock_margin_sse(
    start_date: str = "20010106", end_date: str = "20210208"
) -> pd.DataFrame:
    """
    上海证券交易所-融资融券数据-融资融券汇总
    http://www.sse.com.cn/market/othersdata/margin/sum/
    :param start_date: 交易开始日期
    :type start_date: str
    :param end_date: 交易结束日期
    :type end_date: str
    :return: 融资融券汇总
    :rtype: pandas.DataFrame
    """
    url = "http://query.sse.com.cn/marketdata/tradedata/queryMargin.do"
    params = {
        "isPagination": "true",
        "beginDate": start_date,
        "endDate": end_date,
        "tabType": "",
        "stockCode": "",
        "pageHelp.pageSize": "5000",
        "pageHelp.pageNo": "1",
        "pageHelp.beginPage": "1",
        "pageHelp.cacheSize": "1",
        "pageHelp.endPage": "5",
        "_": "1612773448860",
    }
    headers = {
        "Referer": "http://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"])
    temp_df.columns = [
        "_",
        "信用交易日期",
        "_",
        "融券卖出量",
        "融券余量",
        "融券余量金额",
        "_",
        "_",
        "融资买入额",
        "融资融券余额",
        "融资余额",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "信用交易日期",
            "融资余额",
            "融资买入额",
            "融券余量",
            "融券余量金额",
            "融券卖出量",
            "融资融券余额",
        ]
    ]
    return temp_df


def stock_margin_detail_sse(date: str = "20210205") -> pd.DataFrame:
    """
    上海证券交易所-融资融券数据-融资融券明细
    http://www.sse.com.cn/market/othersdata/margin/detail/
    :param date: 交易日期
    :type date: str
    :return: 融资融券明细
    :rtype: pandas.DataFrame
    """
    url = "http://query.sse.com.cn/marketdata/tradedata/queryMargin.do"
    params = {
        "isPagination": "true",
        "tabType": "mxtype",
        "detailsDate": date,
        "stockCode": "",
        "beginDate": "",
        "endDate": "",
        "pageHelp.pageSize": "5000",
        "pageHelp.pageCount": "50",
        "pageHelp.pageNo": "1",
        "pageHelp.beginPage": "1",
        "pageHelp.cacheSize": "1",
        "pageHelp.endPage": "21",
        "_": "1612773448860",
    }
    headers = {
        "Referer": "http://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"])
    temp_df.columns = [
        "_",
        "信用交易日期",
        "融券偿还量",
        "融券卖出量",
        "融券余量",
        "_",
        "_",
        "融资偿还额",
        "融资买入额",
        "_",
        "融资余额",
        "标的证券简称",
        "标的证券代码",
    ]
    temp_df = temp_df[
        [
            "信用交易日期",
            "标的证券代码",
            "标的证券简称",
            "融资余额",
            "融资买入额",
            "融资偿还额",
            "融券余量",
            "融券卖出量",
            "融券偿还量",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    stock_margin_sse_df = stock_margin_sse(start_date="20010106", end_date="20210208")
    print(stock_margin_sse_df)

    stock_margin_detail_sse_df = stock_margin_detail_sse(date="20210201")
    print(stock_margin_detail_sse_df)
