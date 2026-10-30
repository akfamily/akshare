#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/4/25 17:00
Desc: 新闻联播文字稿
https://tv.cctv.com/lm/xwlb
"""

import re

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

from akshare.utils import http


# 正文开头的固定前缀，按原文的全角与半角括号两种写法都匹配
_CONTENT_PREFIXES = (
    "央视网消息(新闻联播)：",
    "央视网消息（新闻联播）：",
    "(新闻联播)：",
    "（新闻联播）：",
)


def _clean_title(title: str) -> str:
    """
    去掉标题开头的 [视频] 标记
    原先用 strip("[视频]")，会按字符集合删除两端所有的 [、视、频、]，
    以“视频”结尾的标题会被截掉末尾两个字
    """
    return title.strip().removeprefix("[视频]").strip().replace("\n", " ")


def _clean_content(content: str) -> str:
    """
    去掉正文开头的“央视网消息（新闻联播）：”等前缀
    原先用 strip 按字符集合删除，正文若以“新”“央”“视”等字开头会被误删
    """
    content = content.strip()
    for prefix in _CONTENT_PREFIXES:
        if content.startswith(prefix):
            content = content[len(prefix) :]
            break
    return content.strip().replace("\n", " ")


def news_cctv(date: str = "20240424") -> pd.DataFrame:
    """
    新闻联播文字稿
    https://tv.cctv.com/lm/xwlb
    :param date: 需要获取数据的日期；目前 20160203 年后
    :type date: str
    :return: 新闻联播文字稿
    :rtype: pandas.DataFrame
    """
    if int(date) <= int("20130708"):
        url = f"https://cctv.cntv.cn/lm/xinwenlianbo/{date}.shtml"
        r = http.get(url)
        r.encoding = "gbk"
        raw_list = re.findall(r"title_array_01\((.*)", r.text)
        page_url = [
            re.findall("(http.*)", item)[0].split("'")[0] for item in raw_list[1:]
        ]
        title_list = []
        content_list = []
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
            "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Host": "tv.cctv.com",
            "Pragma": "no-cache",
            "Proxy-Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/92.0.4515.159 Safari/537.36",
        }
        for page in tqdm(page_url, leave=False):
            try:
                r = http.get(page, headers=headers)
                r.encoding = "utf-8"
                soup = BeautifulSoup(r.text, "lxml")
                title = soup.find("h3").text
                content = soup.find("div", attrs={"class": "cnt_bd"}).text
                title_list.append(_clean_title(title))
                content_list.append(_clean_content(content))
            except Exception:
                continue
        temp_df = pd.DataFrame(
            data=[[date] * len(title_list), title_list, content_list],
            index=["date", "title", "content"],
        ).T
        return temp_df

    elif int(date) < int("20160203"):
        url = f"https://cctv.cntv.cn/lm/xinwenlianbo/{date}.shtml"
        r = http.get(url)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "lxml")
        page_url = [
            item.find("a")["href"]
            for item in soup.find(
                name="div", attrs={"id": "contentELMT1368521805488378"}
            ).find_all("li")[1:]
        ]
        title_list = []
        content_list = []
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
            "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Host": "tv.cctv.com",
            "Pragma": "no-cache",
            "Proxy-Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/92.0.4515.159 Safari/537.36",
        }
        for page in tqdm(page_url, leave=False):
            try:
                r = http.get(page, headers=headers)
                r.encoding = "utf-8"
                soup = BeautifulSoup(r.text, features="lxml")
                title = soup.find("h3").text
                content = soup.find(name="div", attrs={"class": "cnt_bd"}).text
                title_list.append(_clean_title(title))
                content_list.append(_clean_content(content))
            except Exception:
                continue
        temp_df = pd.DataFrame(
            data=[[date] * len(title_list), title_list, content_list],
            index=["date", "title", "content"],
        ).T
        return temp_df
    elif int(date) > int("20160203"):
        url = f"https://tv.cctv.com/lm/xwlb/day/{date}.shtml"
        r = http.get(url)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "lxml")
        page_url = [item.find("a")["href"] for item in soup.find_all("li")[1:]]
        title_list = []
        content_list = []
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
            "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Host": "tv.cctv.com",
            "Pragma": "no-cache",
            "Proxy-Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/92.0.4515.159 Safari/537.36",
        }
        for page in tqdm(page_url, leave=False):
            try:
                r = http.get(page, headers=headers)
                r.encoding = "utf-8"
                soup = BeautifulSoup(r.text, features="lxml")
                if soup.find("h3"):
                    title = soup.find("h3").text
                else:
                    title = soup.find(name="div", attrs={"class": "tit"}).text
                if soup.find(name="div", attrs={"class": "cnt_bd"}):
                    content = soup.find(name="div", attrs={"class": "cnt_bd"}).text
                else:
                    content = soup.find(
                        name="div", attrs={"class": "content_area"}
                    ).text
                title_list.append(_clean_title(title))
                content_list.append(_clean_content(content))
            except Exception:
                continue
        temp_df = pd.DataFrame(
            data=[[date] * len(title_list), title_list, content_list],
            index=["date", "title", "content"],
        ).T
        return temp_df


if __name__ == "__main__":
    news_cctv_df = news_cctv(date="20240424")
    print(news_cctv_df)
