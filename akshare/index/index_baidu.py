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
    return ''.join([a[j] for j in e])


COOKIES = 'BAIDUID=8759768F974CE3E6C2884260097331A4:FG=1; PSTM=1574683224; H_PS_PSSID=1445_21116_29567_29220; BIDUPSID=43233656E2011B10D268D7B02D7A956A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=2; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1574939615; BDUSS=hWWDJ0Z01VOWZINGdPaWRkTUotYmR4WlRhcEhJNTVDQzA3SUpDNzBSWHRPQWRlRVFBQUFBJCQAAAAAAAAAAAEAAAA3VXuxu6rPxNPQxMzGpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO2r313tq99daE; CHKFORREG=f47c79690c889b9fe3bb335ced026f76; bdindexid=j4g6p93elqe6o7phocmmfn53o2; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1574940479'

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Cookie': COOKIES,
    'DNT': '1',
    'Host': 'zhishu.baidu.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'zhishu.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
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
        result = decrypt(ptbk, all_data).split(',')
        result = [int(item) for item in result]
        temp_df = pd.DataFrame([pd.date_range(start=start_date, end=end_date, freq="7D"), result],
                               index=["date", word]).T
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
        result = decrypt(ptbk, all_data).split(',')
        result = [int(item) for item in result]
        temp_df = pd.DataFrame([pd.date_range(start=start_date, end=end_date, freq="7D"), result],
                               index=["date", word]).T
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
        result = decrypt(ptbk, all_data).split(',')
        result = ["0" if item == "" else item for item in result]
        result = [int(item) for item in result]
        temp_df = pd.DataFrame([pd.date_range(start=start_date, end=end_date, freq="7D"), result],
                               index=["date", word]).T
        temp_df.index = pd.to_datetime(temp_df["date"])
        del temp_df["date"]
        return temp_df


if __name__ == "__main__":
    # data = baidu_search_index(
    #     word="螺纹钢",
    #     start_date='2010-12-27',
    #     end_date='2019-12-01'
    # )
    # print(data)
    # data.dropna(inplace=True)
    # data.plot()
    # plt.show()
    # data = baidu_info_index(word="螺纹钢",
    #                          start_date='2017-07-03',
    #                          end_date='2019-12-01')
    # print(data)
    # data.dropna(inplace=True)
    # data.plot()
    # plt.show()
    data = baidu_media_index(word="人工智能",
                             start_date='2010-12-27',
                             end_date='2019-12-01')
    print(data)
    data.dropna(inplace=True)
    data.plot()
    plt.show()
