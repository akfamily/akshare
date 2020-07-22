# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/8 14:39
Desc: 宽客在线-阿尔戈斯全网监控预警系统
https://www.quantinfo.com/Argus/
"""
import requests
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def watch_argus():
    """
    https://www.quantinfo.com/Argus/
    :return:
    :rtype:
    """
    url = "https://www.quantinfo.com/API/Argus/predict"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }
    r = requests.get(url, headers=headers, verify=False)
    temp_df = pd.DataFrame(r.json())
    temp_df["time"] = pd.to_datetime(temp_df["time"], unit="s", utc=True).dt.tz_convert(
        "Asia/Shanghai"
    )
    return temp_df


if __name__ == "__main__":
    watch_argus_df = watch_argus()
    print(watch_argus_df)
