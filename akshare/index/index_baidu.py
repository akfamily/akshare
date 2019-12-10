# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/2 23:53
contact: jindaxiang@163.com
desc: 百度指数
感谢 https://cloudcrawler.club/categories/2019%E5%B9%B4%E6%9C%AB%E9%80%86%E5%90%91%E5%A4%8D%E4%B9%A0/
"""
import requests
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 显示中文标签


def decrypt(t: str, e: str) -> str:
    n, i, a, result = list(t), list(e), {}, []
    ln = int(len(n) / 2)
    start, end = n[ln:], n[:ln]
    a = dict(zip(end, start))
    return "".join([a[j] for j in e])


COOKIES = "PSTM=1575382863; BAIDUID=C01F1BDBA4D8C7ECF8049F18CF9CECF2:FG=1; BIDUPSID=4EE8E9BA66768CFD68C8120B5EB3E658; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; bdindexid=jqsit8468qh1hforfns4v3eos3; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=7; H_PS_PSSID=1443_21116_30210_30125_26350; BDSFRCVID=goLsJeCCxG3JggRwNmmVoAsw6kFOeQZRddMu3J; H_BDCLCKID_SF=tJkjVIPytIt3fP36qRbsbtCs5Uo0q6FXKKOLV-JJ3q7keq8CDR52hULrDpJwLtrrHmOB3-Tt3DQIjR72y5jHhnKsylCDBqkHtK74XfJGabnpsIJMbJAWbT8U5f5lWlbpaKviaMnjBMb1fIJDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6j0jH_HJ58qf5QBBbFyfIP_Hn7zq4b_ePLuBPnZKxtqtHQU2noqWt3FEnnEqfn8-nF-hMnXBljnWncKW56gKh8WHRbGLPQ4X5533b3405OT2j-O0KJcbR_aVDohhPJvypksXnO7-5OlXbrtXp7_2J0WStbKy4oTjxL1Db3JKjvMtgDtVDDQ2RrfetPk-4QEbbQH-UnLqhvyfT7Z0lOnMp05OR3T0RJFhqIrDbOP3tIO3eO-bxc45nbYfDO_e6L3MtCObqAX5to05TIX3b7Efb3o8-O_bfbT2MbyyxJMQJbwaCjpWhjbbKQOsl7N0q6Cb-0I5HbZqtJHKbDD_K8yJU5; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1575379659,1575471527,1575887345,1575887773; BDUSS=HRZdVJndW43bG9wSXBqVEFnejg2Tm1BdC1LajRyQ2sxemg3NElZc241WHZzQlZlRUFBQUFBJCQAAAAAAAAAAAEAAAA9yPAAamluMDU3NQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO8j7l3vI-5dR; CHKFORREG=71d7aa6dd5330535976884a57e20f967; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1575887859"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Cookie": COOKIES,
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


def get_ptbk(uniqid: str) -> str:
    with session.get(
            url=f"http://index.baidu.com/Interface/ptbk?uniqid={uniqid}"
    ) as response:
        ptbk = response.json()["data"]
        return ptbk


def baidu_search_index(word: str, start_date: str, end_date: str) -> str:
    with session.get(
            url=f"http://index.baidu.com/api/SearchApi/index?word={word}&area=0&startDate={start_date}&endDate={end_date}"
    ) as response:
        data = response.json()["data"]
        all_data = data["userIndexes"][0]["all"]["data"]
        uniqid = data["uniqid"]
        ptbk = get_ptbk(uniqid)
        result = decrypt(ptbk, all_data).split(",")
        result = [int(item) for item in result]
        temp_df = pd.DataFrame(
            [pd.date_range(start=start_date, end=end_date, freq="7D"), result],
            index=["date", word],
        ).T
        temp_df.index = pd.to_datetime(temp_df["date"])
        del temp_df["date"]
        return temp_df


def baidu_info_index(word: str, start_date: str, end_date: str) -> str:
    with session.get(
            url=f"http://index.baidu.com/api/FeedSearchApi/getFeedIndex?word={word}&area=0"
    ) as response:
        data = response.json()["data"]
        all_data = data["index"][0]["data"]
        uniqid = data["uniqid"]
        ptbk = get_ptbk(uniqid)
        result = decrypt(ptbk, all_data).split(",")
        result = [int(item) for item in result]
        temp_df = pd.DataFrame(
            [pd.date_range(start=start_date, end=end_date, freq="7D"), result],
            index=["date", word],
        ).T
        temp_df.index = pd.to_datetime(temp_df["date"])
        del temp_df["date"]
        return temp_df


def baidu_media_index(word: str, start_date: str, end_date: str) -> str:
    with session.get(
            url=f"http://index.baidu.com/api/NewsApi/getNewsIndex?word={word}&area=0"
    ) as response:
        data = response.json()["data"]
        all_data = data["index"][0]["data"]
        uniqid = data["uniqid"]
        ptbk = get_ptbk(uniqid)
        result = decrypt(ptbk, all_data).split(",")
        result = ["0" if item == "" else item for item in result]
        result = [int(item) for item in result]
        temp_df = pd.DataFrame(
            [pd.date_range(start=start_date, end=end_date, freq="7D"), result],
            index=["date", word],
        ).T
        temp_df.index = pd.to_datetime(temp_df["date"])
        del temp_df["date"]
        return temp_df


if __name__ == "__main__":
    data = baidu_search_index(
        word="地震",
        start_date='2010-12-27',
        end_date='2019-12-01'
    )
    print(data)
    data.dropna(inplace=True)
    data.plot()
    plt.show()
    data = baidu_info_index(word="地震",
                            start_date='2017-07-03',
                            end_date='2019-12-01')
    print(data)
    data.dropna(inplace=True)
    data.plot()
    plt.show()
    data = baidu_media_index(
        word="地震", start_date="2010-12-27", end_date="2019-12-01"
    )
    print(data)
    data.dropna(inplace=True)
    data.plot()
    plt.show()
