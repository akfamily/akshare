# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/1/15 16:59
Desc: 个股新闻数据
http://so.eastmoney.com/news/s?keyword=%E4%B8%AD%E5%9B%BD%E4%BA%BA%E5%AF%BF&pageindex=1&searchrange=8192&sortfiled=4
"""
import pandas as pd
import requests


def stock_news_em(stock: str = "601628") -> pd.DataFrame:
    """
    东方财富-个股新闻-最近 20 条新闻
    http://so.eastmoney.com/news/s?keyword=%E4%B8%AD%E5%9B%BD%E4%BA%BA%E5%AF%BF&pageindex=1&searchrange=8192&sortfiled=4
    :param stock: 股票代码
    :type stock: str
    :return: 个股新闻
    :rtype: pandas.DataFrame
    """
    url = "http://searchapi.eastmoney.com//bussiness/Web/GetCMSSearchList"
    params = {
        "type": "8196",
        "pageindex": "1",
        "pagesize": "20",
        "keyword": f"({stock})()",
        "name": "zixun",
        "_": "1608800267874",
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "searchapi.eastmoney.com",
        "Pragma": "no-cache",
        "Referer": "http://so.eastmoney.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }

    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["Data"])
    temp_df.columns = [
        "url",
        "title",
        "_",
        "public_time",
        "content",
    ]
    temp_df['code'] = stock
    temp_df = temp_df[
        [
            "code",
            "title",
            "content",
            "public_time",
            "url",
        ]
    ]
    temp_df["title"] = (
        temp_df["title"].str.replace(r"\(<em>", "", regex=True).str.replace(r"</em>\)", "", regex=True)
    )
    temp_df["content"] = (
        temp_df["content"].str.replace(r"\(<em>", "", regex=True).str.replace(r"</em>\)", "", regex=True)
    )
    temp_df["content"] = (
        temp_df["content"].str.replace(r"<em>", "", regex=True).str.replace(r"</em>", "", regex=True)
    )
    temp_df["content"] = temp_df["content"].str.replace(r"\u3000", "", regex=True)
    temp_df["content"] = temp_df["content"].str.replace(r"\r\n", " ", regex=True)
    return temp_df


if __name__ == "__main__":
    stock_news_em_df = stock_news_em(stock="601318")
    print(stock_news_em_df.info())
