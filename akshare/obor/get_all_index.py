# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/10/17 0:50
Desc: 获取具体指数数据, 科威特剔除
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from akshare.obor.get_countries_from_invest_web import get_countries_url

web_site = get_countries_url()

for item_1 in web_site.iloc[:, 0]:
    # item_1 = web_site.iloc[:, 0][0]
    url = 'https://cn.investing.com' + item_1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
    }
    res = requests.post(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    title = soup.select('title')[0].get_text().split('-')[0].strip().split('_')[0]
    if title == "科威特股市指数":
        continue
    useful_web = soup.find_all(attrs={'id': 'cr1'})[0].find_all(attrs={'class': 'bold left noWrap elp plusIconTd'})[0].select('a')[0]['href']
    useful_title = soup.find_all(attrs={'id': 'cr1'})[0].find_all(attrs={'class': 'bold left noWrap elp plusIconTd'})[0].select('a')[0]['title']

    url = 'https://cn.investing.com' + useful_web + '-historical-data'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
    }
    res = requests.post(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.find_all(text=re.compile('window.histDataExcessInfo'))[0].strip()
    para_data = re.findall(r'\d+', data)
    start_date = '2000/01/01'
    end_date = '2019/10/17'
    para_header = soup.find_all(attrs={'class': 'float_lang_base_1 inlineblock'})[0].get_text()
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '143',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'PHPSESSID=gqemr8f6b5k3ln2sm2mot584c1; geoC=CN; adBlockerNewUserDomains=1505836027; StickySession=id.24390176506.946.cn.investing.com; __gads=ID=64a5550702122294:T=1505836033:S=ALNI_MarJZek4h5Tsuhfp_UlmdEui3sqvw; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A1%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228849%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A22%3A%22%2Fcommodities%2Fcrude-oil%22%3B%7D%7D%7D%7D; travelDistance=4; billboardCounter_6=0; _ga=GA1.2.328544075.1505836032; _gid=GA1.2.1402998722.1505836033; Hm_lvt_a1e3d50107c2a0e021d734fe76f85914=1505836033; Hm_lpvt_a1e3d50107c2a0e021d734fe76f85914=1505837460; nyxDorf=NTI3ZmczZCY0Y2puYi8xMDZvN3IzNWFgMTA%3D',
        'Host': 'cn.investing.com',
        'Origin': 'https://cn.investing.com',
        'Referer': 'https://cn.investing.com/commodities/crude-oil-historical-data',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'curr_id': para_data[0],
        'smlID': para_data[1],
        'header': para_header,
        'st_date': start_date,
        'end_date': end_date,
        'interval_sec': 'Daily',
        'sort_col': 'date',
        'sort_ord': 'DESC',
        'action': 'historical_data'
    }
    url = 'https://cn.investing.com/instruments/HistoricalDataAjax'
    res = requests.post(url, data=data, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    vest_time = [item.get_text() for item in soup.find_all('td', attrs={'class': "first left bold noWrap"})]
    vest_list = [item.get_text().strip().split('\n') for item in soup.find_all('tr')]
    list_date = list()
    for item in vest_list[:-1]:
        list_date.append(item[0])
    list_new = list()
    for item in vest_list[:-1]:
        list_new.append(item[1])
    list_open = list()
    for item in vest_list[:-1]:
        list_open.append(item[2])
    list_high = list()
    for item in vest_list[:-1]:
        list_high.append(item[3])
    list_low = list()
    for item in vest_list[:-1]:
        list_low.append(item[4])
    list_vol_per = list()
    for item in vest_list[:-1]:
        list_vol_per.append(item[5])
    list_vol = list()
    list_per = list()
    for item in list_vol_per:
        list_vol.append(item.split(' ')[0])
        list_per.append(item.split(' ')[1])

    list_date.append(vest_list[-1][0])
    list_new.append(vest_list[-1][1])
    list_open.append(vest_list[-1][2])
    list_high.append(vest_list[-1][3])
    list_low.append(vest_list[-1][4])

    df_data = pd.DataFrame([list_date, list_new, list_open, list_high, list_low, list_vol, list_per]).T
    df_data.iloc[0, :][5] = '交易量'
    df_data.iloc[0, :][6] = '百分比变化'
    df_data.columns = df_data.iloc[0, :]
    df_data = df_data.iloc[1:, :]
    df_data = df_data[:-1]  # 去掉最后一行
    if useful_title.split(' ')[0] == 'FTSE/JSE':
        useful_title = 'FTSE'
    else:
        useful_title = useful_title
    print(para_header.split(' ')[0])
    df_data.index = pd.to_datetime(df_data["日期"], format="%Y年%m月%d日")
    df_data["收盘"] = df_data["收盘"].str.replace(",", "").astype(float)
    df_data["开盘"] = df_data["开盘"].str.replace(",", "").astype(float)
    df_data["高"] = df_data["高"].str.replace(",", "").astype(float)
    df_data["低"] = df_data["低"].str.replace(",", "").astype(float)
    if any(df_data["交易量"].astype(str).str.contains("-")):
        df_data["交易量"][df_data["交易量"].str.contains("-")] = df_data["交易量"][df_data["交易量"].str.contains("-")].replace("-", 0)
    if any(df_data["交易量"].astype(str).str.contains("B")):
        df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)] = df_data["交易量"][df_data["交易量"].str.contains("B").fillna(False)].str.replace("B", "").astype(float) * 1000000000
    if any(df_data["交易量"].astype(str).str.contains("M")):
        df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)] = df_data["交易量"][df_data["交易量"].str.contains("M").fillna(False)].str.replace("M", "").astype(float) * 1000000
    if any(df_data["交易量"].astype(str).str.contains("K")):
        df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)] = df_data["交易量"][df_data["交易量"].str.contains("K").fillna(False)].str.replace("K", "").astype(float) * 1000
    df_data["交易量"] = df_data["交易量"].astype(float)
    df_data = df_data[["收盘", "开盘", "高", "低", "交易量"]]
    df_data.to_csv('C:\\Users\\king\\Desktop\\obor_rank\\data\\' + useful_title + '--' + title + '.csv', encoding='gb2312')
