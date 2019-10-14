# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
contact: jindaxiang@163.com
desc: 
"""
import os
import pickle

import pandas as pd
import requests
from bs4 import BeautifulSoup
from akshare.futures.cons import (qh_headers,
                                  sample_headers)


def get_inventory_data(exchange=1, symbol=6, plot=True):
    """
    # 交易所代码
    '1': '上海期货交易所', '2': '郑州商品交易所', '3': '大连商品交易所', '7': 'LME', '8': 'NYMEX', '9': 'CBOT', '11': 'NYBOT', '12': 'TOCOM', '14': '上海国际能源交易中心'
    # 交易所对应合约代码
    '上海期货交易所': {'6': '铜', '7': '铝', '8': '橡胶', '21': '燃料油', '54': '锌', '58': '黄金', '59': '螺纹钢', '62': '线材', '64': '铅', '69': '白银', '78': '石油沥青', '85': '热轧卷板', '93': '锡', '94': '镍', '103': '纸浆'},
    '郑州商品交易所': {'9': '强麦', '10': '硬麦', '23': '一号棉', '51': '白糖', '53': 'PTA', '55': '菜籽油', '60': '早籼稻', '66': '甲醇', '67': '普麦', '72': '玻璃', '73': '油菜籽', '74': '菜籽粕', '81': '粳稻', '88': '晚籼稻', '90': '硅铁', '91': '锰硅', '99': '棉纱', '100': '苹果'},
    '大连商品交易所': {'11': '豆一', '12': '豆二', '16': '豆粕', '24': '玉米', '52': '豆油', '56': '聚乙烯', '57': '棕榈油', '61': '聚氯乙烯', '65': '焦炭', '75': '焦煤', '79': '铁矿石', '80': '鸡蛋', '82': '中密度纤维板', '83': '细木工板', '84': '聚丙烯', '92': '玉米淀粉', '104': '乙二醇'},
    '上海国际能源交易中心': {'102': '原油'}}
    'LME': {'18': 'LME铜', '19': 'LME铝', '25': 'LME镍', '26': 'LME铅', '27': 'LME锌', '45': 'LME锡', '50': 'LME铝合金'},
    'NYMEX': {'20': 'COMEX铜', '31': 'COMEX金', '32': 'COMEX银'},
    'CBOT': {'22': 'CBOT大豆', '46': 'CBOT小麦', '47': 'CBOT玉米', '48': 'CBOT燕麦', '49': 'CBOT糙米'},
    'NYBOT': {'30': 'NYBOT2号棉'}, 'TOCOM': {'44': 'TOCOM橡胶'},

    :param exchange:
    :param symbol:
    :param plot:
    :return:
    """
    with open(r'C:\Users\king\PycharmProjects\akshare\akshare\futures\exchange_symbol_value_list.pk', 'rb') as f:
        data_code = pickle.load(f)
    with open(r'C:\Users\king\PycharmProjects\akshare\akshare\futures\exchange_symbol_list.pk', 'rb') as f:
        data_name = pickle.load(f)
    with open(r'C:\Users\king\PycharmProjects\akshare\akshare\futures\code_exchange_name_dict.pk', 'rb') as f:
        out_exchange_name = pickle.load(f)
    name_temp_dict = {}
    code_temp_dict = {}
    for num in data_code.keys():
        name_temp_dict[out_exchange_name[num]] = dict(zip(data_code[num], data_name[num]))
        code_temp_dict[num] = dict(zip(data_code[num], data_name[num]))
    # print(name_temp_dict)
    # print(out_exchange_name)
    url = "http://service.99qh.com/Storage/Storage.aspx?page=99qh"
    # print(exchange)
    res = requests.get(url, headers=sample_headers)
    soup = BeautifulSoup(res.text, "lxml")
    view_state = soup.find_all(attrs={"id": "__VIEWSTATE"})[0]["value"]
    even_validation = soup.find_all(attrs={"id": "__EVENTVALIDATION"})[0]["value"]
    # print(symbol)
    if exchange != 1:
        payload = {
            "__EVENTTARGET": "ddlExchName",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": view_state,
            "__VIEWSTATEGENERATOR": "6EAC22FA",
            "__EVENTVALIDATION": even_validation,
            "ddlExchName": int(exchange),
            "ddlGoodsName": 6
        }
        res = requests.post(url, data=payload, headers=qh_headers)
        soup = BeautifulSoup(res.text, "lxml")
        exchange_name = soup.find_all("select")[0].find_all(attrs={"selected": "selected"})[0].get_text()
        print("切换后", exchange_name)
        view_state = soup.find_all(attrs={"id": "__VIEWSTATE"})[0]["value"]
        even_validation = soup.find_all(attrs={"id": "__EVENTVALIDATION"})[0]["value"]
        payload = {
            "__EVENTTARGET": "ddlGoodsName",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": view_state,
            "__VIEWSTATEGENERATOR": "6EAC22FA",
            "__EVENTVALIDATION": even_validation,
            "ddlExchName": int(exchange),
            "ddlGoodsName": int(symbol)
        }
        res = requests.post(url, data=payload, headers=qh_headers)
        soup = BeautifulSoup(res.text, "lxml")
        small_code = soup.find_all(attrs={"id": "chartData"})[0]["src"].split("&")[-2].split("=")[1]
        print(small_code)
        payload = {
            "__EVENTTARGET": "btnZoomAll",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": view_state,
            "__VIEWSTATEGENERATOR": "6EAC22FA",
            "__EVENTVALIDATION": even_validation,
            "ddlExchName": int(exchange),
            "ddlGoodsName": int(symbol)
        }
        res = requests.post(url, data=payload, headers=qh_headers)
        soup = BeautifulSoup(res.text, "lxml")
        inventory_table = pd.read_html(res.text)[-1]

        print("big code", soup.find_all(attrs={"id": "chartData"})[0]["src"].split("&")[-2].split("=")[1])
        params = {
            "ChartDirectorChartImage": "chart_chartData",
            "cacheId": soup.find_all(attrs={"id": "chartData"})[0]["src"].split("&")[-2].split("=")[1],
            "page": "99qh"
        }
        temp_headers = {
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "UM_distinctid=16c378978de5cc-02cfeac5f7869b-c343162-1fa400-16c378978df8d7; __utmz=181566328.1570520149.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ASP.NET_SessionId=wj5gxuzl3fvvr25503tquq55; __utmc=181566328; _fxaid=1D9A634AB9F5D0265856F7E85E7BC196%1D%2BOOl1inxPE7181fmKs5HCs%2BdLO%2Fq%2FbSvf46UVjo%2BE7w%3D%1DPYphpUa9OlzWUzatrOQTXLPOVillbwMhTIJas%2ByfkyVL2Hd5XA1GOSslksqDkMTccXvQ2duLNsc0CHT4789JrYNbakJrpzrxLnwtBC5GCTssKHGEpor6EwAZfWJgBUlCs4JYFcGUnh3jIO69A4LsOlRMOGf4c9cd%2FbohSjTx3VA%3D; __utma=181566328.1348268634.1564299852.1571066568.1571068391.7; tgw_l7_route=eb1311426274fc07631b2135a6431f7d; __utmt=1; __utmb=181566328.7.10.1571068391",
            "Host": "service.99qh.com",
            "Referer": "http://service.99qh.com/Storage/Storage.aspx?page=99qh",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }
        res = requests.get("http://service.99qh.com/Storage/Storage.aspx", params=params, headers=temp_headers)
        if plot:
            with open("{}_{}.jpg".format(exchange_name, code_temp_dict[str(exchange)][str(symbol)]), "wb") as fs:
                print("保存图片到本地{}".format(os.getcwd()))
                fs.write(res.content)
        return inventory_table

    else:
        payload = {
            "__EVENTTARGET": "btnZoomAll",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": view_state,
            "__VIEWSTATEGENERATOR": "6EAC22FA",
            "__EVENTVALIDATION": even_validation,
            "ddlExchName": int(exchange),
            "ddlGoodsName": int(symbol)
        }
        res = requests.post(url, data=payload, headers=qh_headers)
        inventory_table = pd.read_html(res.text)[-1]

        soup = BeautifulSoup(res.text, "lxml")
        exchange_name = soup.find_all("select")[0].find_all(attrs={"selected": "selected"})[0].get_text()
        params = {
            "ChartDirectorChartImage": "chart_chartData",
            "cacheId": soup.find_all(attrs={"id": "chartData"})[0]["src"].split("&")[-2].split("=")[1],
            "page": "99qh"
        }
        temp_headers = {
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "UM_distinctid=16c378978de5cc-02cfeac5f7869b-c343162-1fa400-16c378978df8d7; __utmz=181566328.1570520149.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ASP.NET_SessionId=wj5gxuzl3fvvr25503tquq55; __utmc=181566328; _fxaid=1D9A634AB9F5D0265856F7E85E7BC196%1D%2BOOl1inxPE7181fmKs5HCs%2BdLO%2Fq%2FbSvf46UVjo%2BE7w%3D%1DPYphpUa9OlzWUzatrOQTXLPOVillbwMhTIJas%2ByfkyVL2Hd5XA1GOSslksqDkMTccXvQ2duLNsc0CHT4789JrYNbakJrpzrxLnwtBC5GCTssKHGEpor6EwAZfWJgBUlCs4JYFcGUnh3jIO69A4LsOlRMOGf4c9cd%2FbohSjTx3VA%3D; __utma=181566328.1348268634.1564299852.1571066568.1571068391.7; tgw_l7_route=eb1311426274fc07631b2135a6431f7d; __utmt=1; __utmb=181566328.7.10.1571068391",
            "Host": "service.99qh.com",
            "Referer": "http://service.99qh.com/Storage/Storage.aspx?page=99qh",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }
        res = requests.get("http://service.99qh.com/Storage/Storage.aspx", params=params, headers=temp_headers)
        if plot:
            with open("{}_{}.jpg".format(exchange_name, code_temp_dict[str(exchange)][str(symbol)]), "wb") as fs:
                print("保存图片到本地{}".format(os.getcwd()))
                fs.write(res.content)
        return inventory_table


if __name__ == "__main__":
    for i in range(10):
        try:
            # help(get_inventory_data)
            data = get_inventory_data(exchange=1, symbol=6, plot=True)
            print(data)
            break
        except:
            continue
