# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/10/17 0:50
Desc:
from the official website: https://cn.investing.com/indices/world-indices/ get the country index list
There are 45 countries in OBOR(exclude China), but we get the China data
We list the countries having financial index data fetched in investing.com
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from akshare.obor import cons


def get_countries_url():
    url = 'https://cn.investing.com/indices/world-indices'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    soup_data = soup.find_all(attrs={'class': 'wide selectBox inlineblock js-indice-country-filter'})
    soup_list = list()
    for country in soup_data:
        soup_list.append(country.get_text().strip())
    soup_en = soup.find_all('option')[1:96]
    english_url = []
    for item in soup_en:
        english_url.append(item['value'])
    chinese_name = []
    for item in soup_en:
        chinese_name.append(item.get_text())
    en_ch_data = pd.DataFrame([english_url, chinese_name]).T
    useful_data = cons.countries_dict.get('report_map_invest').values()
    web_site = pd.DataFrame()
    for item in useful_data:
        web_site = web_site.append(en_ch_data[en_ch_data.iloc[:, 1] == item])
    web_site = web_site.reset_index().iloc[:, 1:]
    return web_site


if __name__ == '__main__':
    df = get_countries_url()
    print(df)
