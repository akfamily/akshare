# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2024/7/31 16:30
Desc: 搜猪-生猪大数据-各省均价实时排行榜
https://www.soozhu.com/price/data/center/
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def spot_hog_soozhu() -> pd.DataFrame:
    """
    搜猪-生猪大数据-各省均价实时排行榜
    https://www.soozhu.com/price/data/center/
    :return: 各省均价实时排行榜
    :rtype: pd.DataFrame
    """
    session = requests.session()
    url = "https://www.soozhu.com/price/data/center/"
    r = session.get(url)
    soup = BeautifulSoup(r.text, features="lxml")
    token = soup.find(name="input", attrs={"name": "csrfmiddlewaretoken"})["value"]
    url = "https://www.soozhu.com/price/data/center/"
    payload = {"act": "mapdata", "csrfmiddlewaretoken": token}
    r = session.post(url, data=payload)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["vlist"])
    price_list = [item[0] for item in temp_df["value"]]
    pct_list = [item[1] for item in temp_df["value"]]
    big_df = pd.DataFrame([temp_df["name"].values, price_list, pct_list]).T
    big_df.columns = ["省份", "价格", "涨跌幅"]
    big_df["价格"] = pd.to_numeric(big_df["价格"], errors="coerce")
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"], errors="coerce")
    big_df["涨跌幅"] = round(big_df["涨跌幅"], 2)
    return big_df


if __name__ == "__main__":
    spot_hog_soozhu_df = spot_hog_soozhu()
    print(spot_hog_soozhu_df)
