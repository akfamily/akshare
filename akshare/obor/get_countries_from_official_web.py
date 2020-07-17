# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/10/17 0:50
Desc:
from the official website: http://www.yidaiyilu.gov.cn/ get the country list
There are 64 countries in OBOR(exclude China)
The data here may be old version, so we will reference the
Big data report on trade cooperation under the belt and road initiative,
which was published by the State Information Center
"""
import time

import requests
from bs4 import BeautifulSoup


def get_plates_countries(data_type='dic'):
    """
    fetch the countries along the OBOR grouped by plates data
    p.s.：This api will change according to the adjust of the website
    :param data_type: data_type we want, dict or list
    :return: dict:
    key                        plates                        string(chinese)
    value                      countries                     string(chinese)
    """
    url = 'https://www.yidaiyilu.gov.cn/jcsjpc.htm'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '__jsluid_s=a353e0bf9e8f4be9c2ae89bcbf83a628; __jsluid_h=a826f9b68333a200c94bf04b553b37ab; Lmlist=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8; __jsl_clearance=1571742739.152|0|dnNpqlBU6qWjtcFMkmoEXMK9yyQ%3D; security_session_verify=ab8b6005488308810e8a05472ba57483; insert_cookie=42578947; Hm_lvt_25e78b3fa4b036e241d0874f836fb377=1571243569,1571742742; JSESSIONID=FF2E48305A7361CD97343A816DECDFCC; Hm_lpvt_25e78b3fa4b036e241d0874f836fb377={}'.format(int(time.time())),
        "Pragma": "no-cache",
        "Referer": "https://www.yidaiyilu.gov.cn/jcsjpc.htm",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'lxml')
    plates = [item.get_text() for item in soup.find(attrs={'class': 'ggsj_sx'}).find('ul').find_all('li')]
    plates_countries = {}
    for i in range(len(plates)):
        plates_countries[plates[i]] = [item.get_text() for item in
                                       soup.find(attrs={'class': 'ggsj_sx'}).find_all('ul')[1 + i].find_all('li')]
    if data_type == 'list':
        df_list = []
        for item in plates_countries.values():
            df_list.extend(item)
        return df_list
    else:
        return plates_countries


if __name__ == '__main__':
    df = get_plates_countries(data_type='list')
    print(df)
    print(len(df))
    df = get_plates_countries(data_type='dict')
    print(df)
    print(len([item for item in df.keys()]))
