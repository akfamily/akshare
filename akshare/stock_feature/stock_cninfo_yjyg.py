# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
desc: 巨潮资讯-首页-数据-预约披露
http://www.cninfo.com.cn/new/commonUrl?url=data/yypl
提取 具体页面 html 页面的 json 接口
http://www.cninfo.com.cn/new/information/getPrbookInfo
"""
import requests
import numpy as np
import pandas as pd


params={
    #'sectionTime':'2019-12-31',
    'firstTime':'',
    'lastTime':'',
    'market':'szsh',
    'stockCode':'',
    'orderClos':'7',
    'isDesc':'true',
    #'pagesize':200,
    #'pagenum':1,
}


def pre_book_info_num(sectiontime='2019-12-31'):
    """
    获取  巨潮资讯-首页-数据-预约披露 总条数
    http://www.cninfo.com.cn/new/information/getPrbookInfo
    :return: 总页数
    :rtype: int
    """
    main_url = "http://www.cninfo.com.cn/new/information/getPrbookInfo"
    params['sectionTime'] = sectiontime
    params['pagesize'] = 20
    params['pagenum'] = 1
    res = requests.post(main_url, params=params)
    return int(res.json()["totalRows"])


def pre_book_info_page_num(sectiontime='2019-12-31'):
    """
    获取  巨潮资讯-首页-数据-预约披露 总页数
    http://www.cninfo.com.cn/new/information/getPrbookInfo
    :return: 总页数
    :rtype: int
    """
    main_url = "http://www.cninfo.com.cn/new/information/getPrbookInfo"
    params['sectionTime'] = sectiontime
    params['pagesize'] = 20
    params['pagenum'] = 1
    res = requests.post(main_url, params=params)
    return int(res.json()["totalPages"])


def pre_book_info(page=2,sectiontime='2019-12-31',begin=1):
    """
    获取 巨潮资讯-首页-数据-预约披露-每一页的 json 数据
    :param page: 需要获取前 page 页的内容, 总页数请通过 pre_book_info_num() 获取
    :type page: int
    :return: 需要的字段
    :rtype: pandas.DataFrame
    """
    if page=='all':
        page=pre_book_info_page_num()
    main_url = "http://www.cninfo.com.cn/new/information/getPrbookInfo"
    temp_df = pd.DataFrame()
    for i_page in range(begin, page+begin):
        print(i_page)
        params['sectionTime'] = sectiontime
        params['pagesize'] = 200
        params['pagenum'] = i_page
        params['orderClos'] = '3'
        params['isDesc'] = 'false'
        res = requests.post(main_url, params=params)
        temp_df = temp_df.append(pd.DataFrame(res.json()["prbookinfos"]))
    return temp_df[["seccode", "secname", "f002d_0102", "f006d_0102", "f003d_0102", "f004d_0102", "f005d_0102", "f001d_0102", "orgId"]]



def pre_book_info_done(sectiontime='2019-12-31',begin=1):
    """
    获取 巨潮资讯-首页-数据-预约披露-已公布年报 json 数据
    :param page: 需要获取前 page 页的内容, 总页数请通过 pre_book_info_num() 获取
    :type page: int
    :return: 需要的字段
    :rtype: pandas.DataFrame
    """
    page=pre_book_info_page_num()
    main_url = "http://www.cninfo.com.cn/new/information/getPrbookInfo"
    temp_df = pd.DataFrame()
    for i_page in range(begin, page+begin):
        print(i_page)
        params['sectionTime'] = sectiontime
        params['pagesize'] = 200
        params['pagenum'] = i_page
        res = requests.post(main_url, params=params)
        _df=pd.DataFrame(res.json()["prbookinfos"])
        temp_df = temp_df.append(_df)
        print(temp_df)
        if len(_df[_df['f006d_0102']==''])>0:
            
            temp_df=temp_df[temp_df['f006d_0102']!='']
            break
    return temp_df[["seccode", "secname", "f002d_0102", "f006d_0102", "f003d_0102", "f004d_0102", "f005d_0102", "f001d_0102", "orgId"]]

if __name__ == '__main__':
    pre_book_info_done_df = pre_book_info_done()
    print(pre_book_info_done_df)
