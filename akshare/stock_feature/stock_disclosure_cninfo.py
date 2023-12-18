#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/12/18 17:00
Desc: 巨潮资讯-首页-公告查询-信息披露
http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search
"""
import math
from functools import lru_cache

import pandas as pd
import requests

from akshare.utils.tqdm import get_tqdm


@lru_cache()
def __get_stock_json(symbol: str = "沪深京") -> dict:
    url = "http://www.cninfo.com.cn/new/data/szse_stock.json"
    if symbol == "沪深京":
        url = "http://www.cninfo.com.cn/new/data/szse_stock.json"
    elif symbol == "港股":
        url = "http://www.cninfo.com.cn/new/data/hke_stock.json"
    elif symbol == "三板":
        url = "http://www.cninfo.com.cn/new/data/gfzr_stock.json"
    elif symbol == "基金":
        url = "http://www.cninfo.com.cn/new/data/fund_stock.json"
    elif symbol == "债券":
        url = "http://www.cninfo.com.cn/new/data/bond_stock.json"
    r = requests.get(url)
    text_json = r.json()
    temp_df = pd.DataFrame([item for item in text_json['stockList']])
    return dict(zip(temp_df['code'], temp_df['orgId']))


def stock_zh_a_disclosure_report_cninfo(
        symbol: str = "000001", market: str = "沪深京", start_date: str = "20230618", end_date: str = "20231219"
) -> pd.DataFrame:
    """
    巨潮资讯-首页-公告查询-信息披露公告
    http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search
    :param symbol: 股票代码
    :type symbol: str
    :param market: choice of {"沪深京", "港股", "三板", "基金", "债券", "监管", "预披露"}
    :type market: str
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 开始时间
    :type end_date: str
    :return: 指定 symbol 的数据
    :rtype: pandas.DataFrame
    """
    column_map = {
        "沪深京": "szse",
        "港股": "hke",
        "三板": "third",
        "基金": "fund",
        "债券": "bond",
        "监管": "regulator",
        "预披露": "pre_disclosure",
    }
    if market == "沪深京":
        stock_id_map = __get_stock_json(symbol)
    url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    payload = {
        'pageNum': '1',
        'pageSize': '30',
        'column': column_map[market],
        'tabName': 'fulltext',
        'plate': '',
        'stock': f'{symbol},{stock_id_map[symbol]}',
        'searchkey': '',
        'secid': '',
        'category': '',
        'trade': '',
        'seDate': f'{"-".join([start_date[:4], start_date[4:6], start_date[6:]])}~{"-".join([end_date[:4], end_date[4:6], end_date[6:]])}',
        'sortName': '',
        'sortType': '',
        'isHLtitle': 'true'
    }
    r = requests.post(url, data=payload)
    text_json = r.json()
    page_num = math.ceil(int(text_json['totalAnnouncement']) / 30)
    big_df = pd.DataFrame()
    tqdm = get_tqdm()
    for page in tqdm(range(1, page_num + 1), leave=False):
        payload.update({"pageNum": page})
        r = requests.post(url, data=payload)
        text_json = r.json()
        temp_df = pd.DataFrame(text_json["announcements"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.rename(columns={
        "secCode": "代码",
        "secName": "简称",
        "announcementTitle": "公告标题",
        "announcementTime": "公告时间",
        "adjunctUrl": "公告链接",
    }, inplace=True)
    big_df = big_df[["代码", "简称", "公告标题", "公告时间", "公告链接"]]
    big_df['公告时间'] = pd.to_datetime(big_df['公告时间'], unit="ms", utc=True, errors="coerce")
    big_df['公告时间'] = big_df['公告时间'].dt.tz_convert('Asia/Shanghai').dt.date
    return big_df


def stock_zh_a_disclosure_relation_cninfo(
        symbol: str = "000001", market: str = "沪深京", start_date: str = "20230618", end_date: str = "20231219"
) -> pd.DataFrame:
    """
    巨潮资讯-首页-数据-预约披露调研
    http://www.cninfo.com.cn/new/commonUrl?url=data/yypl
    :param symbol: 股票代码
    :type symbol: str
    :param market: choice of {"沪深京", "港股", "三板", "基金", "债券", "监管", "预披露"}
    :type market: str
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 开始时间
    :type end_date: str
    :return: 指定 symbol 的数据
    :rtype: pandas.DataFrame
    """
    column_map = {
        "沪深京": "szse",
        "港股": "hke",
        "三板": "third",
        "基金": "fund",
        "债券": "bond",
        "监管": "regulator",
        "预披露": "pre_disclosure",
    }
    if market == "沪深京":
        stock_id_map = __get_stock_json(symbol)
    url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    payload = {
        'pageNum': '1',
        'pageSize': '30',
        'column': column_map[market],
        'tabName': 'relation',
        'plate': '',
        'stock': f'{symbol},{stock_id_map[symbol]}',
        'searchkey': '',
        'secid': '',
        'category': '',
        'trade': '',
        'seDate': f'{"-".join([start_date[:4], start_date[4:6], start_date[6:]])}~{"-".join([end_date[:4], end_date[4:6], end_date[6:]])}',
        'sortName': '',
        'sortType': '',
        'isHLtitle': 'true'
    }
    r = requests.post(url, data=payload)
    text_json = r.json()
    page_num = math.ceil(int(text_json['totalAnnouncement']) / 30)
    big_df = pd.DataFrame()
    tqdm = get_tqdm()
    for page in tqdm(range(1, page_num + 1), leave=False):
        payload.update({"pageNum": page})
        r = requests.post(url, data=payload)
        text_json = r.json()
        temp_df = pd.DataFrame(text_json["announcements"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.rename(columns={
        "secCode": "代码",
        "secName": "简称",
        "announcementTitle": "公告标题",
        "announcementTime": "公告时间",
        "adjunctUrl": "公告链接",
    }, inplace=True)
    big_df = big_df[["代码", "简称", "公告标题", "公告时间", "公告链接"]]
    big_df['公告时间'] = pd.to_datetime(big_df['公告时间'], unit="ms", utc=True, errors="coerce")
    big_df['公告时间'] = big_df['公告时间'].dt.tz_convert('Asia/Shanghai').dt.date
    return big_df


if __name__ == "__main__":
    stock_zh_a_disclosure_report_cninfo_df = stock_zh_a_disclosure_report_cninfo(
        symbol="000001",
        market="沪深京",
        start_date="20230618",
        end_date="20231219")
    print(stock_zh_a_disclosure_report_cninfo_df)

    stock_zh_a_disclosure_relation_cninfo_df = stock_zh_a_disclosure_relation_cninfo(
        symbol="000001",
        market="沪深京",
        start_date="20230618",
        end_date="20231219")
    print(stock_zh_a_disclosure_relation_cninfo_df)
