# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/7/8 21:44
Desc: 新闻联播文字稿
https://tv.cctv.com/lm/xwlb/?spm=C52056131267.P4y8I53JvSWE.0.0
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def news_cctv(date: str = "20210708") -> pd.DataFrame:
    """
    新闻联播文字稿
    https://tv.cctv.com/lm/xwlb/?spm=C52056131267.P4y8I53JvSWE.0.0
    :param date: 需要获取数据的日期; 目前 20160330 年后
    :type date: str
    :return: 新闻联播文字稿
    :rtype: pandas.DataFrame
    """
    url = f'https://tv.cctv.com/lm/xwlb/day/{date}.shtml'
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "lxml")
    page_url = [item.find("a")['href'] for item in soup.find_all("li")[1:]]
    title_list = []
    content_list = []
    for page in tqdm(page_url, leave=False):
        r = requests.get(page)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "lxml")
        title = soup.find('h3').text
        content = soup.find('div', attrs={"class": 'cnt_bd'}).text
        title_list.append(title.strip("[视频]").strip().replace("\n", " "))
        content_list.append(content.strip("央视网消息（新闻联播）：").strip("(新闻联播)：").strip().replace("\n", " "))
    temp_df = pd.DataFrame([[date]*len(title_list), title_list, content_list], index=["date", "title", "content"]).T
    return temp_df


if __name__ == "__main__":
    news_cctv_df = news_cctv(date="20210708")
    print(news_cctv_df)
