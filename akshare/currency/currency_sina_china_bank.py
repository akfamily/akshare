# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/6/14 12:49
Desc: 新浪财经-中行人民币牌价历史数据查询
http://biz.finance.sina.com.cn/forex/forex.php?startdate=2012-01-01&enddate=2021-06-14&money_code=EUR&type=0
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def _currency_boc_sina_map(date: str = "20210614") -> dict:
    """
    外汇 symbol 和代码映射
    :param date: 交易日
    :type date: str
    :return: 外汇 symbol 和代码映射
    :rtype: dict
    """
    url = "http://biz.finance.sina.com.cn/forex/forex.php"
    params = {
        "startdate": "2012-01-01",
        "enddate": "-".join([date[:4], date[4:6], date[6:]]),
        "money_code": "EUR",
        "type": "0",
    }
    r = requests.get(url, params=params)
    r.encoding = "gbk"
    soup = BeautifulSoup(r.text, "lxml")
    data_dict = dict(
        zip(
            [
                item.text
                for item in soup.find(attrs={"id": "money_code"}).find_all("option")
            ],
            [
                item["value"]
                for item in soup.find(attrs={"id": "money_code"}).find_all("option")
            ],
        )
    )
    return data_dict


def currency_boc_sina(symbol: str = "美元", date: str = "20210614") -> pd.DataFrame:
    """
    新浪财经-中行人民币牌价历史数据查询
    http://biz.finance.sina.com.cn/forex/forex.php?startdate=2012-01-01&enddate=2021-06-14&money_code=EUR&type=0
    :param symbol: choice of {'美元', '英镑', '欧元', '澳门元', '泰国铢', '菲律宾比索', '港币', '瑞士法郎', '新加坡元', '瑞典克朗', '丹麦克朗', '挪威克朗', '日元', '加拿大元', '澳大利亚元', '新西兰元', '韩国元'}
    :type symbol: str
    :param date: 交易日
    :type date: str
    :return: 中行人民币牌价历史数据查询
    :rtype: pandas.DataFrame
    """
    data_dict = _currency_boc_sina_map(date="20210614")
    url = "http://biz.finance.sina.com.cn/forex/forex.php"
    params = {
        "money_code": data_dict[symbol],
        "type": "0",
        "startdate": "2012-01-01",
        "enddate": "-".join([date[:4], date[4:6], date[6:]]),
        "page": "1",
        "call_type": "ajax",
    }
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "lxml")
    soup.find(attrs={"id": "money_code"})
    page_num = int(soup.find_all("a", attrs={"class": "page"})[-2].text)
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1)):
        params.update({"page": page})
        r = requests.get(url, params=params)
        temp_df = pd.read_html(r.text, header=0)[0]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [
        "日期",
        "中行汇买价",
        "中行钞买价",
        "中行钞卖价/汇卖价",
        "央行中间价",
    ]
    return big_df


if __name__ == "__main__":
    currency_boc_sina_df = currency_boc_sina(symbol="美元", date="20210614")
    print(currency_boc_sina_df)
