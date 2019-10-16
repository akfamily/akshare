# -*- coding:utf-8 -*-
"""
Created on 2019年01月15日
@author: Ablert King
@contact: jindaxiang@163.com

from the official website: http://www.yidaiyilu.gov.cn/ get the country list
There are 64 countries in OBOR(exclude China)
The data here may be old version, so we will reference the
Big data report on trade cooperation under the belt and road initiative,
which was published by the State Information Center
"""

import requests
from bs4 import BeautifulSoup
import time


def get_plates_countries(data_type='dic'):
    """
    fetch the countries along the OBOR grouped by plates data
    p.s.：This api will change according to the adjust of the website
     Parameters
    ------
        data_type: data_type we want, dict or list
    Return
    -------
        dict:
            key                        plates                        string(chinese)
            value                      countries                     string(chinese)
    """
    url = 'http://www.yidaiyilu.gov.cn/info/iList.jsp'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'Lmlist=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8; __jsluid_h=9df0407204b4a1af667d96985643e1bb; __jsluid_s=a353e0bf9e8f4be9c2ae89bcbf83a628; __jsl_clearance=1564149554.258|0|0ERdLIgl2j0F3FXqkVYSKu%2FVHR4%3D; security_session_verify=6b3290f71c4c837517c276ac2bb8390b; JSESSIONID=9955D37DA047A6C65AD9C482BA1E3DF5; insert_cookie=50745398; Hm_lvt_25e78b3fa4b036e241d0874f836fb377=1564149558; Hm_lpvt_25e78b3fa4b036e241d0874f836fb377={}'.format(int(time.time())),
        'Host': 'www.yidaiyilu.gov.cn',
        'Referer': 'https://www.yidaiyilu.gov.cn/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    params = {'tm_id': 513}
    res = requests.get(url, headers=headers, params=params)
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
    # print(df)
    # print(len([item for item in df.keys()]))
