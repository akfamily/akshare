# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/4/7 13:04
Desc: 胡润排行榜
http://www.hurun.net/CN/HuList/Index
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup


def hurun_rank(indicator: str = "胡润百富榜", year: str = "2019") -> pd.DataFrame:
    """
    胡润排行榜
    http://www.hurun.net/CN/HuList/Index?num=3YwKs889SRIm
    :param indicator: choice of {"百富榜", "富豪榜", "至尚优品"}
    :type indicator: str
    :param year: 指定年份; {"百富榜": "2015至今", "富豪榜": "2015至今", "至尚优品": "2017至今"}
    :type year: str
    :return: 指定 indicator 和 year 的数据
    :rtype: pandas.DataFrame
    """
    url = "https://www.hurun.net/zh-CN/Rank/HsRankDetails?num=Q9TGQF1L"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    url_list = ['https://www.hurun.net' + item['href'] for item in soup.find('div', attrs={'aria-labelledby': 'navbarDropdown'}).find_all('a')]
    name_list = [item.text for item in soup.find('div', attrs={'aria-labelledby': 'navbarDropdown'}).find_all('a')]
    name_url_map = dict(zip(name_list, url_list))
    r = requests.get(name_url_map[indicator])
    soup = BeautifulSoup(r.text, 'lxml')
    code_list = [item['value'].split('=')[1] for item in soup.find(attrs={'id': 'exampleFormControlSelect1'}).find_all('option')]
    year_list = [item.text.split(' ')[0] for item in soup.find(attrs={'id': 'exampleFormControlSelect1'}).find_all('option')]
    year_code_map = dict(zip(year_list, code_list))
    params = {
        'num': year_code_map[year],
        'search': ''
    }
    url = 'https://www.hurun.net/zh-CN/Rank/HsRankDetailsList'
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    return temp_df


if __name__ == "__main__":
    hurun_rank_df = hurun_rank(indicator="胡润百富榜", year="2020")
    print(hurun_rank_df)
