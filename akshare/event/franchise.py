# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2020/9/28 14:51
Desc: 中国-商业特许经营信息管理
http://txjy.syggs.mofcom.gov.cn/
需要输入验证码访问
"""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def _get_franchise_china_page_num() -> int:
    """
    特许经营总页数
    http://txjy.syggs.mofcom.gov.cn/index.do?method=entpsearch
    :return: 特许经营总页数
    :rtype: int
    """
    url = "http://txjy.syggs.mofcom.gov.cn/index.do"
    payload = {
        "method": "entps",
        "province": "",
        "city": "",
        "cpf.cpage": "1",
        "cpf.pagesize": "100",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    }
    r = requests.get(url, params=payload, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    page_num = re.findall(
        re.compile(r"\d+"),
        soup.find(attrs={"class": "inner"}).find_all("a")[-1]["href"],
    )[0]
    return int(page_num)


def franchise_china() -> pd.DataFrame:
    """
    中国-商业特许经营信息管理
    http://txjy.syggs.mofcom.gov.cn/
    :return: 中国-商业特许经营的所有企业
    :rtype: pandas.DataFrame
    """
    url = "http://txjy.syggs.mofcom.gov.cn/index.do"
    # file_url 历史数据文件, 主要是为了防止重复访问的速度和资源浪费问题
    file_url = "https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/franchise/franchise_china.csv"
    outer_df = pd.read_csv(file_url, encoding="gbk", index_col=0)
    try:
        for page in tqdm(range(1, int(5)), leave=False):  # 这里的 5 是硬编码, 长期后需要更新 file_url 文件
            payload = {
                "method": "entps",
                "province": "",
                "city": "",
                "cpf.cpage": str(page),
                "cpf.pagesize": "100",
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
            }
            r = requests.get(url, params=payload, headers=headers)
            temp_df = pd.read_html(r.text)[1]
            inner_df = temp_df.iloc[:, 0].str.split("  ", expand=True)
            inner_df.columns = ["特许人名称", "备案时间", "地址"]
            outer_df = outer_df.append(inner_df, ignore_index=True)
    except:
        pass
    outer_df.drop_duplicates(inplace=True)
    return outer_df


if __name__ == "__main__":
    franchise_china_df = franchise_china()
    print(franchise_china_df)
