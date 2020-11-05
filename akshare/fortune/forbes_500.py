# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/11/5 15:10
Desc: 福布斯中国-榜单
https://www.forbeschina.com/lists
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup


def forbes_rank(indicator: str = "2020福布斯美国富豪榜") -> pd.DataFrame:
    """
    福布斯中国-榜单
    https://www.forbeschina.com/lists
    https://www.forbeschina.com/lists/1750
    :param indicator: choice of {"2020福布斯美国富豪榜", "2020福布斯新加坡富豪榜", "2020福布斯中国名人榜", *}
    :type indicator: str
    :return: 具体指标的榜单
    :rtype: pandas.DataFrame
    """
    url = "https://www.forbeschina.com/lists"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    need_list = [
        item.find_all("a")
        for item in soup.find_all("div", attrs={"class": "col-sm-6 col-lg-4"})
    ]
    all_list = []
    for item in need_list:
        all_list.extend(item)
    name_url_dict = dict(
        zip(
            [item.text.strip() for item in all_list],
            ["https://www.forbeschina.com" + item["href"] for item in all_list],
        )
    )
    r = requests.get(name_url_dict[indicator])
    temp_df = pd.read_html(r.text)[0]
    return temp_df


if __name__ == "__main__":
    forbes_rank_df = forbes_rank(indicator="2020福布斯美国富豪榜")
    print(forbes_rank_df)
