import json
from datetime import datetime

import pandas as pd
import requests

"""
Date: 2021/5/29
Desc: 财联社今日快讯
https://www.cls.cn/searchPage?keyword=%E5%BF%AB%E8%AE%AF&type=all
"""

cls_url = "https://www.cls.cn/api/sw?app=CailianpressWeb&os=web&sv=7.5.5"

cls_headers = {
    "Host": "www.cls.cn",
    "Connection": "keep-alive",
    "Content-Length": "112",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://www.cls.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}


def stock_zh_a_alerts_cls() -> pd.DataFrame:
    """
    财联社今日快讯
    https://www.cls.cn/searchPage?keyword=%E5%BF%AB%E8%AE%AF&type=all
    :return: 今日快讯,id,时间
    :rtype: pandas.DataFrame
    """

    payload = json.dumps(
        {
            "type": "telegram",
            "keyword": "快讯",
            "page": 0,
            "rn": 30,
            "os": "web",
            "sv": "7.2.2",
            "app": "CailianpressWeb",
        }
    )
    today = datetime.today()
    today_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    response = requests.request("POST", cls_url, headers=cls_headers, data=payload)
    res = response.json()
    data = res["data"]["telegram"]["data"]
    df = pd.DataFrame(data)
    df = df[["descr", "id", "time"]]
    df["descr"] = df["descr"].astype(str).str.replace("</em>", "")
    df["descr"] = df["descr"].str.replace("<em>", "")
    df["time"] = df["time"].apply(datetime.fromtimestamp)
    df = df[df["time"] > today_start]
    df.columns = ["快讯信息", "id", "时间"]
    return df


if __name__ == "__main__":
    print(stock_zh_a_alerts_cls())
