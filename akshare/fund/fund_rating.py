# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/3/29 17:48
Desc: 基金评级
http://fund.eastmoney.com/data/fundrating.html
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup


def fund_rating_all() -> pd.DataFrame:
    """
    天天基金网-基金评级-基金评级总汇
    http://fund.eastmoney.com/data/fundrating.html
    :return: 基金评级总汇
    :rtype: pandas.DataFrame
    """
    url = "http://fund.eastmoney.com/data/fundrating.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    data_text = soup.find("div", attrs={"id": "fundinfo"}).find("script").string
    data_content = [
        item.split("|")
        for item in data_text.split("var")[6]
        .split("=")[1]
        .strip()
        .strip(";")
        .strip('"')
        .strip("|")
        .split("|_")
    ]
    temp_df = pd.DataFrame(data_content)
    temp_df.columns = [
        "代码",
        "简称",
        "类型",
        "基金经理",
        "_",
        "基金公司",
        "_",
        "5星评级家数",
        "上海证券",
        "上海证券-较上期",
        "招商证券",
        "招商证券-较上期",
        "济安金信",
        "济安金信-较上期",
        "_",
        "_",
        "_",
        "_",
        "手续费",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "代码",
            "简称",
            "基金经理",
            "基金公司",
            "5星评级家数",
            "上海证券",
            "招商证券",
            "济安金信",
            "手续费",
            "类型",
        ]
    ]
    return temp_df


def fund_rating_sh(date: str = '20200930') -> pd.DataFrame:
    """
    天天基金网-基金评级-上海证券评级
    http://fund.eastmoney.com/data/fundrating_3.html
    :return: 上海证券评级
    :rtype: pandas.DataFrame
    """
    url = "http://fund.eastmoney.com/data/fundrating_3.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    date_list = [item['value'] for item in soup.find('select', attrs={'id': 'rqoptions'})]
    date_format = '-'.join([date[:4], date[4:6], date[6:]])
    if date_format not in date_list:
        return '请访问 http://fund.eastmoney.com/data/fundrating_3.html 获取查询日期'
    url = f"http://fund.eastmoney.com/data/fundrating_3_{'-'.join([date[:4], date[4:6], date[6:]])}.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    data_text = soup.find("div", attrs={"id": "fundinfo"}).find("script").string
    data_content = [
        item.split("|")
        for item in data_text.split("var")[1]
        .split("=")[1]
        .strip()
        .strip(";")
        .strip('"')
        .strip("|")
        .split("|_")
    ]
    temp_df = pd.DataFrame(data_content)
    temp_df.columns = [
        "代码",
        "简称",
        "类型",
        "基金经理",
        "_",
        "基金公司",
        "_",
        "3年期评级-3年评级",
        "3年期评级-较上期",
        "5年期评级-5年评级",
        "5年期评级-较上期",
        "单位净值",
        "日期",
        "日增长率",
        "近1年涨幅",
        "近3年涨幅",
        "近5年涨幅",
        "手续费",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "代码",
            "简称",
            "基金经理",
            "基金公司",
            "3年期评级-3年评级",
            "3年期评级-较上期",
            "5年期评级-5年评级",
            "5年期评级-较上期",
            "单位净值",
            "日期",
            "日增长率",
            "近1年涨幅",
            "近3年涨幅",
            "近5年涨幅",
            "手续费",
            "类型",
        ]
    ]
    return temp_df


def fund_rating_zs(date: str = '20201030') -> pd.DataFrame:
    """
    天天基金网-基金评级-招商证券评级
    http://fund.eastmoney.com/data/fundrating_2.html
    :return: 招商证券评级-混合型
    :rtype: pandas.DataFrame
    """
    url = "http://fund.eastmoney.com/data/fundrating_2.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    date_list = [item['value'] for item in soup.find('select', attrs={'id': 'rqoptions'})]
    date_format = '-'.join([date[:4], date[4:6], date[6:]])
    if date_format not in date_list:
        return '请访问 http://fund.eastmoney.com/data/fundrating_2.html 获取查询日期'
    url = f"http://fund.eastmoney.com/data/fundrating_2_{'-'.join([date[:4], date[4:6], date[6:]])}.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    data_text = soup.find("div", attrs={"id": "fundinfo"}).find("script").string
    data_content = [
        item.split("|")
        for item in data_text.split("var")[1]
        .split("=")[1]
        .strip()
        .strip(";")
        .strip('"')
        .strip("|")
        .split("|_")
    ]
    temp_df = pd.DataFrame(data_content)
    temp_df.columns = [
        "代码",
        "简称",
        "_",
        "基金经理",
        "_",
        "基金公司",
        "_",
        "3年期评级-3年评级",
        "3年期评级-较上期",
        "单位净值",
        "日期",
        "日增长率",
        "近1年涨幅",
        "近3年涨幅",
        "近5年涨幅",
        "手续费",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "代码",
            "简称",
            "基金经理",
            "基金公司",
            "3年期评级-3年评级",
            "3年期评级-较上期",
            "单位净值",
            "日期",
            "日增长率",
            "近1年涨幅",
            "近3年涨幅",
            "近5年涨幅",
            "手续费",
        ]
    ]
    return temp_df


def fund_rating_ja(date: str = '20200930') -> pd.DataFrame:
    """
    天天基金网-基金评级-济安金信评级
    http://fund.eastmoney.com/data/fundrating_4.html
    :return: 济安金信评级
    :rtype: pandas.DataFrame
    """
    url = "http://fund.eastmoney.com/data/fundrating_4.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    date_list = [item['value'] for item in soup.find('select', attrs={'id': 'rqoptions'})]
    date_format = '-'.join([date[:4], date[4:6], date[6:]])
    if date_format not in date_list:
        return '请访问 http://fund.eastmoney.com/data/fundrating_4.html 获取查询日期'
    url = f"http://fund.eastmoney.com/data/fundrating_4_{'-'.join([date[:4], date[4:6], date[6:]])}.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    data_text = soup.find("div", attrs={"id": "fundinfo"}).find("script").string
    data_content = [
        item.split("|")
        for item in data_text.split("var")[1]
        .split("=")[1]
        .strip()
        .strip(";")
        .strip('"')
        .strip("|")
        .split("|_")
    ]
    temp_df = pd.DataFrame(data_content)
    temp_df.columns = [
        "代码",
        "简称",
        "类型",
        "基金经理",
        "_",
        "基金公司",
        "_",
        "3年期评级-3年评级",
        "3年期评级-较上期",
        "单位净值",
        "日期",
        "日增长率",
        "近1年涨幅",
        "近3年涨幅",
        "近5年涨幅",
        "手续费",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "代码",
            "简称",
            "基金经理",
            "基金公司",
            "3年期评级-3年评级",
            "3年期评级-较上期",
            "单位净值",
            "日期",
            "日增长率",
            "近1年涨幅",
            "近3年涨幅",
            "近5年涨幅",
            "手续费",
            "类型",
        ]
    ]
    return temp_df


if __name__ == "__main__":
    fund_rating_all_df = fund_rating_all()
    print(fund_rating_all_df)

    fund_rating_sh_df = fund_rating_sh(date='20200930')
    print(fund_rating_sh_df)

    fund_rating_zs_df = fund_rating_zs(date='20201030')
    print(fund_rating_zs_df)

    fund_rating_ja_df = fund_rating_ja(date='20200930')
    print(fund_rating_ja_df)
