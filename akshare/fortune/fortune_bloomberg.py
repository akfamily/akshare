# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/7/11 21:44
Desc: 彭博亿万富豪指数
https://www.bloomberg.com/billionaires/
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup


def index_bloomberg_billionaires() -> pd.DataFrame:
    """
    Bloomberg Billionaires Index
    https://www.bloomberg.com/billionaires/
    :return: 彭博亿万富豪指数
    :rtype: pandas.DataFrame
    """
    url = "https://www.bloomberg.com/billionaires/"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Host": "www.bloomberg.com",
        "Referer": "https://www.bloomberg.com/billionaires/",
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    big_content_list = list()
    soup_node = soup.find(attrs={"class": "table-chart"}).find_all(attrs={"class": "table-row"})
    for row in soup_node:
        temp_content_list = row.text.strip().replace("\n", "").split("  ")
        content_list = [item for item in temp_content_list if item != ""]
        big_content_list.append(content_list)
    temp_df = pd.DataFrame(big_content_list).iloc[:, :-1]
    temp_df.columns = ["rank", "name", "total_net_worth", "last_change", "YTD_change", "country", "industry"]
    return temp_df


if __name__ == '__main__':
    index_bloomberg_billionaires_df = index_bloomberg_billionaires()
    print(index_bloomberg_billionaires_df)
