#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/11/20 120:15
Desc: 个股新闻数据
https://so.eastmoney.com/news/s?keyword=603777
"""

import json

import pandas as pd
import requests


def stock_news_em(symbol: str = "603777") -> pd.DataFrame:
    """
    东方财富-个股新闻-最近 100 条新闻
    https://so.eastmoney.com/news/s?keyword=603777
    :param symbol: 股票代码
    :type symbol: str
    :return: 个股新闻
    :rtype: pandas.DataFrame
    """
    url = "https://search-api-web.eastmoney.com/search/jsonp"
    inner_param = {
        "uid": "",
        "keyword": "603777",
        "type": ["cmsArticleWebOld"],
        "client": "web",
        "clientType": "web",
        "clientVersion": "curr",
        "param": {
            "cmsArticleWebOld": {
                "searchScope": "default",
                "sort": "default",
                "pageIndex": 1,
                "pageSize": 10,
                "preTag": "<em>",
                "postTag": "</em>"
            }
        }
    }
    params = {
        "cb": "jQuery35101792940631092459_1764599530165",
        "param": json.dumps(inner_param, ensure_ascii=False),  # 保留中文,
        "_": "1764599530176"
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
        "cache-control": "no-cache",
        "connection": "keep-alive",
        "cookie": "qgqp_b_id=652bf4c98a74e210088f372a17d4e27b; st_nvi=ulN5JAj9FUocz3p4klMME9f20; emshistory=%5B%22603777%22%5D; nid18=010d039dd427dc4d187090491f47d7ad; nid18_create_time=1764582801999; gviem=gSdeY51VWSuTzM3kWaagtf560; gviem_create_time=1764582801999; st_si=55269775884615; st_pvi=66803244437563; st_sp=2025-11-19%2014%3A19%3A16; st_inirUrl=https%3A%2F%2Fso.eastmoney.com%2Fnews%2Fs; st_sn=2; st_psi=20251201223210488-118000300905-0940816858; st_asi=delete",
        "host": "search-api-web.eastmoney.com",
        "pragma": "no-cache",
        "referer": "https://so.eastmoney.com/news/s?keyword=603777",
        "sec-ch-ua": "\"Chromium\";v=\"142\", \"Google Chrome\";v=\"142\", \"Not_A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = json.loads(
        data_text.strip("jQuery35101792940631092459_1764599530165(")[:-1]
    )
    temp_df = pd.DataFrame(data_json["result"]["cmsArticleWebOld"])
    temp_df["url"] = "http://finance.eastmoney.com/a/" + temp_df["code"] + ".html"
    temp_df.rename(
        columns={
            "date": "发布时间",
            "mediaName": "文章来源",
            "code": "-",
            "title": "新闻标题",
            "content": "新闻内容",
            "url": "新闻链接",
            "image": "-",
        },
        inplace=True,
    )
    temp_df["关键词"] = symbol
    temp_df = temp_df[
        [
            "关键词",
            "新闻标题",
            "新闻内容",
            "发布时间",
            "文章来源",
            "新闻链接",
        ]
    ]
    temp_df["新闻标题"] = (
        temp_df["新闻标题"]
        .str.replace(r"\(<em>", "", regex=True)
        .str.replace(r"</em>\)", "", regex=True)
    )
    temp_df["新闻标题"] = (
        temp_df["新闻标题"]
        .str.replace(r"<em>", "", regex=True)
        .str.replace(r"</em>", "", regex=True)
    )
    temp_df["新闻内容"] = (
        temp_df["新闻内容"]
        .str.replace(r"\(<em>", "", regex=True)
        .str.replace(r"</em>\)", "", regex=True)
    )
    temp_df["新闻内容"] = (
        temp_df["新闻内容"]
        .str.replace(r"<em>", "", regex=True)
        .str.replace(r"</em>", "", regex=True)
    )
    temp_df["新闻内容"] = temp_df["新闻内容"].str.replace(r"\u3000", "", regex=True)
    temp_df["新闻内容"] = temp_df["新闻内容"].str.replace(r"\r\n", " ", regex=True)
    return temp_df


if __name__ == "__main__":
    stock_news_em_df = stock_news_em(symbol="603777")
    print(stock_news_em_df)
