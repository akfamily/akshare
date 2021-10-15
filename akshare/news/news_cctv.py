# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/7/20 21:44
Desc: 新闻联播文字稿
https://tv.cctv.com/lm/xwlb/?spm=C52056131267.P4y8I53JvSWE.0.0
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def news_cctv(date: str = "20130308") -> pd.DataFrame:
    """
    新闻联播文字稿
    https://tv.cctv.com/lm/xwlb/?spm=C52056131267.P4y8I53JvSWE.0.0
    :param date: 需要获取数据的日期; 目前 20160203 年后
    :type date: str
    :return: 新闻联播文字稿
    :rtype: pandas.DataFrame
    """
    if int(date) <= int("20130708"):
        url = f'http://cctv.cntv.cn/lm/xinwenlianbo/{date}.shtml'
        r = requests.get(url)
        r.encoding = "gbk"
        import re
        raw_list = re.findall(r"title_array_01\((.*)", r.text)
        page_url = [re.findall("(http.*)", item)[0].split("'")[0] for item in raw_list[1:]]
        title_list = []
        content_list = []
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Cookie': 'cna=DLYSGBDthG4CAbRVCNxSxGT6',
            'Host': 'tv.cctv.com',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        for page in tqdm(page_url, leave=False):
            try:
                r = requests.get(page, headers=headers)
                r.encoding = 'utf-8'
                soup = BeautifulSoup(r.text, "lxml")
                title = soup.find('h3').text
                content = soup.find('div', attrs={"class": 'cnt_bd'}).text
                title_list.append(title.strip("[视频]").strip().replace("\n", " "))
                content_list.append(content.strip().strip("央视网消息(新闻联播)：").strip("央视网消息（新闻联播）：").strip("(新闻联播)：").strip().replace("\n", " "))
            except:
                continue
        temp_df = pd.DataFrame([[date]*len(title_list), title_list, content_list], index=["date", "title", "content"]).T
        return temp_df

    elif int(date) < int("20160203"):
        url = f'http://cctv.cntv.cn/lm/xinwenlianbo/{date}.shtml'
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "lxml")
        page_url = [item.find("a")['href'] for item in soup.find("div", attrs={"id": "contentELMT1368521805488378"}).find_all('li')[1:]]
        title_list = []
        content_list = []
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Cookie': 'cna=DLYSGBDthG4CAbRVCNxSxGT6',
            'Host': 'tv.cctv.com',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        for page in tqdm(page_url, leave=False):
            try:
                r = requests.get(page, headers=headers)
                r.encoding = 'utf-8'
                soup = BeautifulSoup(r.text, "lxml")
                title = soup.find('h3').text
                content = soup.find('div', attrs={"class": 'cnt_bd'}).text
                title_list.append(title.strip("[视频]").strip().replace("\n", " "))
                content_list.append(content.strip().strip("央视网消息(新闻联播)：").strip("央视网消息（新闻联播）：").strip("(新闻联播)：").strip().replace("\n", " "))
            except:
                continue
        temp_df = pd.DataFrame([[date]*len(title_list), title_list, content_list], index=["date", "title", "content"]).T
        return temp_df
    elif int(date) > int("20160203"):
        url = f'https://tv.cctv.com/lm/xwlb/day/{date}.shtml'
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "lxml")
        page_url = [item.find("a")['href'] for item in soup.find_all("li")[1:]]
        title_list = []
        content_list = []
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Cookie': 'cna=DLYSGBDthG4CAbRVCNxSxGT6',
            'Host': 'tv.cctv.com',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        for page in tqdm(page_url, leave=False):
            try:
                r = requests.get(page, headers=headers)
                r.encoding = 'utf-8'
                soup = BeautifulSoup(r.text, "lxml")
                title = soup.find('h3').text
                content = soup.find('div', attrs={"class": 'cnt_bd'}).text
                title_list.append(title.strip("[视频]").strip().replace("\n", " "))
                content_list.append(content.strip().strip("央视网消息(新闻联播)：").strip("央视网消息（新闻联播）：").strip("(新闻联播)：").strip().replace("\n", " "))
            except:
                continue
        temp_df = pd.DataFrame([[date]*len(title_list), title_list, content_list], index=["date", "title", "content"]).T
        return temp_df


if __name__ == "__main__":
    news_cctv_df = news_cctv(date="20150208")
    print(news_cctv_df)
