# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/10/18 12:54
Desc: 新闻联播文字稿
http://www.xwlbo.com/date-2020-7-11.html
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def news_cctv(date: str = "20200902") -> pd.DataFrame:
    """
    新闻联播文字稿
    http://www.xwlbo.com/date-2020-7-11.html
    :param date: 需要获取数据的日期, 2018年后
    :type date: str
    :return: 新闻联播文字稿
    :rtype: pandas.DataFrame
    """
    url = f"http://www.xwlbo.com/date-{date[:4]}-{int(date[4:6])}-{date[6:]}.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    pattern = re.compile(f"{date[:4]}年{int(date[4:6])}月{int(date[6:])}日新闻联播")
    url = soup.find("a", text=pattern)["href"]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    news_list = soup.find("div", attrs={"class": "text_content"}).find_all("a")
    title_list = [item.get_text() for item in news_list]
    href_list = [item["href"] for item in news_list]
    news_content_list = []
    for href in tqdm(href_list):
        if "http://www.xwlbo.com" in href:
            url = href
        else:
            url = f"http://www.xwlbo.com/{href}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        content_list = (
            soup.find(attrs={"id": "tab_con2"})
            .find("div", attrs={"class": "text_content"})
            .find_all("p")
        )
        content = " ".join([item.get_text() for item in content_list])
        pure_content = content.strip("央视网消息（新闻联播文字版）：").strip()
        news_content_list.append(pure_content)
    temp_df = pd.DataFrame(
        [[date] * len(title_list), title_list, news_content_list],
        index=["date", "title", "content"],
    ).T
    return temp_df


if __name__ == "__main__":
    news_cctv_df = news_cctv(date="20201104")
    print(news_cctv_df)
