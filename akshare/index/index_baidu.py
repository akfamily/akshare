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

# TODO 用户输入自己的 Cookie
COOKIES = "PSTM=1577979108; BAIDUID=1DCEF481438F38BC5D925AE2D4904885:FG=1; BIDUPSID=4EE8E9BA66768CFD68C8120B5EB3E658; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; H_PS_PSSID=1469_21117_30211_18560_26350_30482; PSINO=1; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1576162669,1576749442,1578574558; BDUSS=5KWG9DZFJyWn5aRW1yd2NBRmhqVldZS2I1MUU0cWZUWTFIM0Frd1RpN2tyejVlRVFBQUFBJCQAAAAAAAAAAAEAAAA9yPAAamluMDU3NQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOQiF17kIhdeSk; CHKFORREG=71d7aa6dd5330535976884a57e20f967; bdindexid=7u97io4v0mhqgnrb7e7ld1hmj5; bdshare_firstime=1578574588741; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1578574658"

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
        if len(result) == len(pd.date_range(start=start_date, end=end_date, freq="7D")):
            temp_df_7 = pd.DataFrame(
                [pd.date_range(start=start_date, end=end_date, freq="7D"), result],
                index=["date", word],
            ).T
            temp_df_7.index = pd.to_datetime(temp_df_7["date"])
            del temp_df_7["date"]
            return temp_df_7
        else:
            temp_df_1 = pd.DataFrame(
                [pd.date_range(start=start_date, end=end_date, freq="1D"), result],
                index=["date", word],
            ).T
            temp_df_1.index = pd.to_datetime(temp_df_1["date"])
            del temp_df_1["date"]
            return temp_df_1


def baidu_info_index(word: str, start_date: str, end_date: str) -> str:
    with session.get(
            url=f"http://index.baidu.com/api/FeedSearchApi/getFeedIndex?word={word}&area=0&startDate={start_date}&endDate={end_date}"
    ) as response:
        data = response.json()["data"]
        all_data = data["index"][0]["data"]
        uniqid = data["uniqid"]
        ptbk = get_ptbk(uniqid)
        result = decrypt(ptbk, all_data).split(",")
        result = [int(item) if item != "" else 0 for item in result]
        if len(result) == len(pd.date_range(start=start_date, end=end_date, freq="7D")):
            temp_df_7 = pd.DataFrame(
                [pd.date_range(start=start_date, end=end_date, freq="7D"), result],
                index=["date", word],
            ).T
            temp_df_7.index = pd.to_datetime(temp_df_7["date"])
            del temp_df_7["date"]
            return temp_df_7
        else:
            temp_df_1 = pd.DataFrame(
                [pd.date_range(start=start_date, end=end_date, freq="1D"), result],
                index=["date", word],
            ).T
            temp_df_1.index = pd.to_datetime(temp_df_1["date"])
            del temp_df_1["date"]
            return temp_df_1


def baidu_media_index(word: str, start_date: str, end_date: str) -> str:
    with session.get(
            url=f"http://index.baidu.com/api/NewsApi/getNewsIndex?word={word}&area=0&startDate={start_date}&endDate={end_date}"
    ) as response:
        data = response.json()["data"]
        all_data = data["index"][0]["data"]
        uniqid = data["uniqid"]
        ptbk = get_ptbk(uniqid)
        result = decrypt(ptbk, all_data).split(",")
        result = ["0" if item == "" else item for item in result]
        result = [int(item) for item in result]
        if len(result) == len(pd.date_range(start=start_date, end=end_date, freq="7D")):
            temp_df_7 = pd.DataFrame(
                [pd.date_range(start=start_date, end=end_date, freq="7D"), result],
                index=["date", word],
            ).T
            temp_df_7.index = pd.to_datetime(temp_df_7["date"])
            del temp_df_7["date"]
            return temp_df_7
        else:
            temp_df_1 = pd.DataFrame(
                [pd.date_range(start=start_date, end=end_date, freq="1D"), result],
                index=["date", word],
            ).T
            temp_df_1.index = pd.to_datetime(temp_df_1["date"])
            del temp_df_1["date"]
            return temp_df_1


if __name__ == "__main__":
    data = baidu_search_index(
        word="九寨沟",
        start_date='2017-12-27',
        end_date='2019-12-01'
    )
    print(data)
    data.dropna(inplace=True)
    data.plot()
    plt.show()
    data = baidu_info_index(word="九寨沟",
                            start_date='2017-07-03',
                            end_date='2019-12-01')
    print(data)
    data.dropna(inplace=True)
    data.plot()
    plt.show()
    data = baidu_media_index(
        word="九寨沟", start_date="2017-10-27", end_date="2019-12-01"
    )
    print(data)
    data.dropna(inplace=True)
    data.plot()
    plt.show()
