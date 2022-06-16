#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/6/14 17:21
Desc: 百度指数
https://index.baidu.com/v2/main/index.html#/trend/python?words=python
"""
import pandas as pd
import requests


def decrypt(t: str, e: str) -> str:
    """
    解密函数
    :param t:
    :type t:
    :param e:
    :type e:
    :return:
    :rtype:
    """
    n, i, a, result = list(t), list(e), {}, []
    ln = int(len(n) / 2)
    start, end = n[ln:], n[:ln]
    a = dict(zip(end, start))
    return "".join([a[j] for j in e])


def get_ptbk(uniqid: str, cookie: str) -> str:
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Cookie": cookie,
        "DNT": "1",
        "Host": "zhishu.baidu.com",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "zhishu.baidu.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    session = requests.Session()
    session.headers.update(headers)
    with session.get(
        url=f"http://index.baidu.com/Interface/ptbk?uniqid={uniqid}"
    ) as response:
        ptbk = response.json()["data"]
        return ptbk


def baidu_search_index(
    word: str = "python",
    start_date: str = "2020-01-01",
    end_date: str = "2020-05-01",
    cookie: str = None,
    text: str = None,
) -> str:
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Cipher-Text": text,
        "Cookie": cookie,
        "DNT": "1",
        "Host": "index.baidu.com",
        "Pragma": "no-cache",
        "Referer": "https://index.baidu.com/v2/main/index.html",
        "Proxy-Connection": "keep-alive",
        "Referer": "zhishu.baidu.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    session = requests.Session()
    session.headers.update(headers)
    params = {
        "area": "0",
        "word": '[[{"name":' + f'"{word}"' + ',"wordType"' + ":1}]]",
        "startDate": start_date,
        "endDate": end_date,
    }
    with session.get(
        url="http://index.baidu.com/api/SearchApi/index", params=params
    ) as response:
        data = response.json()["data"]
        all_data = data["userIndexes"][0]["all"]["data"]
        uniqid = data["uniqid"]
        ptbk = get_ptbk(uniqid, cookie)
        result = decrypt(ptbk, all_data).split(",")
        result = [int(item) if item != "" else 0 for item in result]
        if len(result) == len(
            pd.date_range(start=start_date, end=end_date, freq="7D")
        ):
            temp_df_7 = pd.DataFrame(
                [
                    pd.date_range(start=start_date, end=end_date, freq="7D"),
                    result,
                ],
                index=["date", word],
            ).T
            temp_df_7.index = pd.to_datetime(temp_df_7["date"])
            del temp_df_7["date"]
            return temp_df_7
        else:
            temp_df_1 = pd.DataFrame(
                [
                    pd.date_range(start=start_date, end=end_date, freq="1D"),
                    result,
                ],
                index=["date", word],
            ).T
            temp_df_1.index = pd.to_datetime(temp_df_1["date"])
            del temp_df_1["date"]
            return temp_df_1


def baidu_info_index(
    word: str, start_date: str, end_date: str, cookie: str, text: str
) -> str:
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Cipher-Text": text,
        "Cookie": cookie,
        "DNT": "1",
        "Host": "zhishu.baidu.com",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "zhishu.baidu.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    session = requests.Session()
    session.headers.update(headers)
    params = {
        "area": "0",
        "word": '[[{"name":' + f'"{word}"' + ',"wordType"' + ":1}]]",
        "startDate": start_date,
        "endDate": end_date,
    }
    with session.get(
        url=f"http://index.baidu.com/api/FeedSearchApi/getFeedIndex",
        params=params,
    ) as response:
        data = response.json()["data"]
        all_data = data["index"][0]["data"]
        uniqid = data["uniqid"]
        ptbk = get_ptbk(uniqid, cookie)
        result = decrypt(ptbk, all_data).split(",")
        result = [int(item) if item != "" else 0 for item in result]
        if len(result) == len(
            pd.date_range(start=start_date, end=end_date, freq="7D")
        ):
            temp_df_7 = pd.DataFrame(
                [
                    pd.date_range(start=start_date, end=end_date, freq="7D"),
                    result,
                ],
                index=["date", word],
            ).T
            temp_df_7.index = pd.to_datetime(temp_df_7["date"])
            del temp_df_7["date"]
            return temp_df_7
        else:
            temp_df_1 = pd.DataFrame(
                [
                    pd.date_range(start=start_date, end=end_date, freq="1D"),
                    result,
                ],
                index=["date", word],
            ).T
            temp_df_1.index = pd.to_datetime(temp_df_1["date"])
            del temp_df_1["date"]
            return temp_df_1


def baidu_media_index(
    word: str = "口罩",
    start_date: str = "2018-01-01",
    end_date: str = "2020-04-20",
    cookie: str = None,
    text: str = None,
) -> str:
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Cipher-Text": text,
        "Cookie": cookie,
        "DNT": "1",
        "Host": "zhishu.baidu.com",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "zhishu.baidu.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    session = requests.Session()
    session.headers.update(headers)
    params = {
        "area": "0",
        "word": '[[{"name":' + f'"{word}"' + ',"wordType"' + ":1}]]",
        "startDate": start_date,
        "endDate": end_date,
    }
    with session.get(
        url=f"http://index.baidu.com/api/NewsApi/getNewsIndex", params=params
    ) as response:
        data = response.json()["data"]
        all_data = data["index"][0]["data"]
        uniqid = data["uniqid"]
        ptbk = get_ptbk(uniqid, cookie)
        result = decrypt(ptbk, all_data).split(",")
        result = ["0" if item == "" else item for item in result]
        result = [int(item) for item in result]
        if len(result) == len(
            pd.date_range(start=start_date, end=end_date, freq="7D")
        ):
            temp_df_7 = pd.DataFrame(
                [
                    pd.date_range(start=start_date, end=end_date, freq="7D"),
                    result,
                ],
                index=["date", word],
            ).T
            temp_df_7.index = pd.to_datetime(temp_df_7["date"])
            del temp_df_7["date"]
            return temp_df_7
        else:
            temp_df_1 = pd.DataFrame(
                [
                    pd.date_range(start=start_date, end=end_date, freq="1D"),
                    result,
                ],
                index=["date", word],
            ).T
            temp_df_1.index = pd.to_datetime(temp_df_1["date"])
            del temp_df_1["date"]
            return temp_df_1


if __name__ == "__main__":
    cookie = ""
    text = ""

    baidu_search_index_df = baidu_search_index(
        word="疫苗",
        start_date="2021-01-01",
        end_date="2022-01-01",
        cookie=cookie,
        text=text,
    )
    print(baidu_search_index_df)

    baidu_info_index_df = baidu_info_index(
        word="口罩",
        start_date="2019-07-03",
        end_date="2022-09-21",
        cookie=cookie,
        text=text,
    )
    print(baidu_info_index_df)

    baidu_media_index_df = baidu_media_index(
        word="金融科技",
        start_date="2020-01-01",
        end_date="2022-09-20",
        cookie=cookie,
        text=text,
    )
    print(baidu_media_index_df)
