# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/1/10 13:58
Desc: 得到 99 期货网的原始数据
"""
import requests
import pickle
from bs4 import BeautifulSoup
import time


url = "http://service.99qh.com/Storage/Storage.aspx?page=99qh"

sample_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Host": "service.99qh.com",
    "Origin": "http://service.99qh.com",
    "Referer": "http://www.99qh.com/d/store.aspx",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}

res = requests.get(url, headers=sample_headers)

soup = BeautifulSoup(res.text, "lxml")
view_state = soup.find_all(attrs={"id": "__VIEWSTATE"})[0]["value"]
even_validation = soup.find_all(attrs={"id": "__EVENTVALIDATION"})[0]["value"]

qh_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "4458",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "service.99qh.com",
    "Origin": "http://service.99qh.com",
    "Referer": "http://service.99qh.com/Storage/Storage.aspx?page=99qh",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}

code_temp_list = [item["value"] for item in soup.find_all("select")[0].find_all("option")]
name_temp_list = [item.get_text() for item in soup.find_all("select")[0].find_all("option")]
code_exchange_name_dict = dict(zip(code_temp_list, name_temp_list))
exchange_value = soup.find_all("select")[0].find_all(attrs={"selected": "selected"})[0]["value"]
symbol_list = soup.find_all("select")[1].get_text().split("\n")[1:-1]
symbol_value_list = [item["value"] for item in soup.find_all("select")[1].find_all("option")]
code_symbol_code_dict = dict()
code_symbol_code_dict[exchange_value] = symbol_value_list

exchange_symbol_list = {}
exchange_symbol_value_list = {}
for i in code_temp_list:
    # i = 14
    print(i)
    j = 0
    while j < 5:
        try:
            payload = {
                "__EVENTTARGET": "ddlExchName",
                "__EVENTARGUMENT": "",
                "__LASTFOCUS": "",
                "__VIEWSTATE": view_state,
                "__VIEWSTATEGENERATOR": "6EAC22FA",
                "__EVENTVALIDATION": even_validation,
                "ddlExchName": i,
                # "ddlGoodsName": 6
            }

            res = requests.post(url, data=payload, headers=qh_headers)
            soup = BeautifulSoup(res.text, "lxml")
            exchange = soup.find_all("select")[0].find_all(attrs={"selected": "selected"})[0].get_text()
            print(exchange)
            exchange_value = soup.find_all("select")[0].find_all(attrs={"selected": "selected"})[0]["value"]
            print(exchange_value)
            symbol_list = soup.find_all("select")[1].get_text().split("\n")[1:-1]
            exchange_symbol_list.update({exchange_value: symbol_list})
            symbol_value_list = [item["value"] for item in soup.find_all("select")[1].find_all("option")]
            exchange_symbol_value_list.update({exchange_value: symbol_value_list})
            view_state = soup.find_all(attrs={"id": "__VIEWSTATE"})[0]["value"]
            even_validation = soup.find_all(attrs={"id": "__EVENTVALIDATION"})[0]["value"]
            time.sleep(5)
        except:
            j += 1
            continue


with open('./akshare/futures/exchange_symbol_list.pk', 'wb') as f:
    pickle.dump(exchange_symbol_list, f)

with open('./akshare/futures/exchange_symbol_value_list.pk', 'wb') as f:
    pickle.dump(exchange_symbol_value_list, f)

with open('./akshare/futures/code_exchange_name_dict.pk', 'wb') as f:
    pickle.dump(code_exchange_name_dict, f)



