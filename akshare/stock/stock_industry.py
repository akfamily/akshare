# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2020/5/18 20:49
Desc: 新浪行业-板块行情
http://finance.sina.com.cn/stock/sl/
"""
import json
import math

from akshare.utils import demjson
import pandas as pd
import requests


def stock_sector_spot(indicator: str = "新浪行业") -> pd.DataFrame:
    """
    新浪行业-板块行情
    http://finance.sina.com.cn/stock/sl/
    :param indicator: choice of {"新浪行业", "启明星行业", "概念", "地域", "行业"}
    :type indicator: str
    :return: 指定 indicator 的数据
    :rtype: pandas.DataFrame
    """

    if indicator == "新浪行业":
        url = "http://vip.stock.finance.sina.com.cn/q/view/newSinaHy.php"
        r = requests.get(url)
    if indicator == "启明星行业":
        url = "http://biz.finance.sina.com.cn/hq/qmxIndustryHq.php"
        r = requests.get(url)
        r.encoding = "gb2312"
    if indicator == "概念":
        url = "http://money.finance.sina.com.cn/q/view/newFLJK.php"
        params = {
            "param": "class"
        }
        r = requests.get(url, params=params)
    if indicator == "地域":
        url = "http://money.finance.sina.com.cn/q/view/newFLJK.php"
        params = {
            "param": "area"
        }
        r = requests.get(url, params=params)
    if indicator == "行业":
        url = "http://money.finance.sina.com.cn/q/view/newFLJK.php"
        params = {
            "param": "industry"
        }
        r = requests.get(url, params=params)
    text_data = r.text
    json_data = json.loads(text_data[text_data.find("{"):])
    temp_df = pd.DataFrame([value.split(",") for key, value in json_data.items()])
    temp_df.columns = [
        "label",
        "板块",
        "公司家数",
        "平均价格",
        "涨跌额",
        "涨跌幅",
        "总成交量(手)",
        "总成交额(万元)",
        "股票代码",
        "涨跌幅",
        "当前价",
        "涨跌额",
        "股票名称",
    ]
    return temp_df


def stock_sector_detail(sector: str = "gn_gfgn") -> pd.DataFrame:
    """
    新浪行业-板块行情-成份详情
    http://finance.sina.com.cn/stock/sl/#area_1
    :param sector: stock_sector_spot 返回的 label 值, choice of {"新浪行业", "概念", "地域", "行业"}; "启明星行业" 无详情
    :type sector: str
    :return: 指定 sector 的板块详情
    :rtype: pandas.DataFrame
    """
    url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount"
    params = {
        "node": sector
    }
    r = requests.get(url, params=params)
    total_num = int(r.json())
    total_page_num = math.ceil(int(total_num) / 80)

    big_df = pd.DataFrame()
    url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
    for page in range(1, total_page_num+1):
        params = {
            "page": str(page),
            "num": "80",
            "sort": "symbol",
            "asc": "1",
            "node": sector,
            "symbol": "",
            "_s_r_a": "page",
        }
        r = requests.get(url, params=params)
        temp_df = pd.DataFrame(demjson.decode(r.text))
        big_df = big_df.append(temp_df, ignore_index=True)
    return big_df


if __name__ == '__main__':
    stock_industry_sina_df = stock_sector_spot(indicator="新浪行业")
    print(stock_industry_sina_df)
    stock_industry_con_df = stock_sector_spot(indicator="概念")
    print(stock_industry_con_df)
    stock_industry_area_df = stock_sector_spot(indicator="地域")
    print(stock_industry_area_df)
    stock_industry_ind_df = stock_sector_spot(indicator="行业")
    print(stock_industry_ind_df)
    stock_industry_star_df = stock_sector_spot(indicator="启明星行业")
    print(stock_industry_star_df)

    stock_sector_detail_df = stock_sector_detail(sector="hangye_ZC27")
    print(stock_sector_detail_df)
