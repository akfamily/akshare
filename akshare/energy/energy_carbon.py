# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/3/21 16:55
Desc: 碳排放交易
北京市碳排放权电子交易平台-北京市碳排放权公开交易行情
https://www.bjets.com.cn/article/jyxx/

深圳碳排放交易所-国内碳情
http://www.cerx.cn/dailynewsCN/index.htm

深圳碳排放交易所-国际碳情
http://www.cerx.cn/dailynewsOuter/index.htm

湖北碳排放权交易中心-现货交易数据-配额-每日概况
http://www.cerx.cn/dailynewsOuter/index.htm

广州碳排放权交易中心-行情信息
http://www.cnemission.com/article/hqxx/
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def energy_carbon_bj() -> pd.DataFrame:
    """
    北京市碳排放权电子交易平台-北京市碳排放权公开交易行情
    https://www.bjets.com.cn/article/jyxx/
    :return: 北京市碳排放权公开交易行情
    :rtype: pandas.DataFrame
    """
    url = 'https://www.bjets.com.cn/article/jyxx/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    total_page = soup.find('table').find('script').string.split('=')[-1].strip().strip(';').strip('"')
    temp_df = pd.DataFrame()
    for i in tqdm(range(1, int(total_page)+1), desc="Please wait for a moment"):
        if i == 1:
            i = ""
        url = f"https://www.bjets.com.cn/article/jyxx/?{i}"
        res = requests.get(url)
        res.encoding = "utf-8"
        df = pd.read_html(res.text)[0]
        temp_df = temp_df.append(df, ignore_index=True)
    temp_df.columns = ["日期", "成交量", "成交均价", "成交额"]
    return temp_df


def energy_carbon_sz():
    """
    深圳碳排放交易所-国内碳情
    http://www.cerx.cn/dailynewsCN/index.htm
    :return: 国内碳情每日行情数据
    :rtype: pandas.DataFrame
    """
    url = "http://www.cerx.cn/dailynewsCN/index.htm"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    page_num = int(soup.find(attrs={"class": "pagebar"}).find_all("option")[-1].text)
    big_df = pd.read_html(r.text, header=0)[0]
    for page in tqdm(range(2, page_num+1), desc="Please wait for a moment"):
        url = f"http://www.cerx.cn/dailynewsCN/index_{page}.htm"
        r = requests.get(url)
        temp_df = pd.read_html(r.text, header=0)[0]
        big_df = big_df.append(temp_df, ignore_index=True)
    return big_df


def energy_carbon_eu():
    """
    深圳碳排放交易所-国际碳情
    http://www.cerx.cn/dailynewsOuter/index.htm
    :return: 国际碳情每日行情数据
    :rtype: pandas.DataFrame
    """
    url = "http://www.cerx.cn/dailynewsOuter/index.htm"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    page_num = int(soup.find(attrs={"class": "pagebar"}).find_all("option")[-1].text)
    big_df = pd.read_html(r.text, header=0)[0]
    for page in tqdm(range(2, page_num+1), desc="Please wait for a moment"):
        url = f"http://www.cerx.cn/dailynewsOuter/index_{page}.htm"
        r = requests.get(url)
        temp_df = pd.read_html(r.text, header=0)[0]
        big_df = big_df.append(temp_df, ignore_index=True)
    return big_df


def energy_carbon_hb():
    """
    湖北碳排放权交易中心-现货交易数据-配额-每日概况
    http://www.cerx.cn/dailynewsOuter/index.htm
    :return: 现货交易数据-配额-每日概况行情数据
    :rtype: pandas.DataFrame
    """
    url = "http://www.hbets.cn/index.php/index-show-tid-13.html?&p=1"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    columns = [item.text for item in soup.find(attrs={"class": "title"})]
    page_num = int(soup.find(attrs={"class": "page"}).text.split("/")[1].strip("共").strip("页"))
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num+1), desc="Please wait for a moment"):
        url = f"http://www.hbets.cn/index.php/index-show-tid-13.html?&p={page}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        page_node = [item for item in soup.find(attrs={"class": "future_table"}).find_all(attrs={"class": "cont"})]
        temp_list = []
        for item in page_node:
            temp_inner_list = []
            for inner_item in item.find_all("li"):
                temp_inner_list.append(inner_item.text)
            temp_list.append(temp_inner_list)
        temp_df = pd.DataFrame(temp_list)
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = columns
    return big_df


def energy_carbon_gz():
    """
    广州碳排放权交易中心-行情信息
    http://www.cnemission.com/article/hqxx/
    :return: 行情信息数据
    :rtype: pandas.DataFrame
    """
    url = "http://ets.cnemission.com/carbon/portalIndex/markethistory"
    params = {
        "Top": "1",
        "beginTime": "2010-01-01",
        "endTime": "2021-09-12",
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_html(r.text, header=0)[1]
    return temp_df


if __name__ == '__main__':
    energy_carbon_bj_df = energy_carbon_bj()
    print(energy_carbon_bj_df)

    energy_carbon_sz_df = energy_carbon_sz()
    print(energy_carbon_sz_df)

    energy_carbon_eu_df = energy_carbon_eu()
    print(energy_carbon_eu_df)

    energy_carbon_hb_df = energy_carbon_hb()
    print(energy_carbon_hb_df)

    energy_carbon_gz_df = energy_carbon_gz()
    print(energy_carbon_gz_df)
