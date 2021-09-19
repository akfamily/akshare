# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/7/28 21:19
Desc: 股票指数成份股数据, 新浪有两个接口, 这里使用老接口:
新接口：http://vip.stock.finance.sina.com.cn/mkt/#zhishu_000001
老接口：http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page=1&indexid=399639
"""
import math
import time
from io import BytesIO

from akshare.utils import demjson
import pandas as pd
import requests
from bs4 import BeautifulSoup


def index_stock_cons_sina(index: str = "000300") -> pd.DataFrame:
    """
    新浪新版股票指数成份页面, 目前该接口可获取指数数量较少
    http://vip.stock.finance.sina.com.cn/mkt/#zhishu_000040
    :param index: 指数代码
    :type index: str
    :return: 指数的成份股
    :rtype: pandas.DataFrame
    """
    if index == "000300":
        index = 'hs300'
        url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCountSimple"
        params = {
            "node": f"{index}"
        }
        r = requests.get(url, params=params)
        page_num = math.ceil(int(r.json()) / 80) + 1
        temp_df = pd.DataFrame()
        for page in range(1, page_num):
            url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
            params = {
                "page": str(page),
                "num": "80",
                "sort": "symbol",
                "asc": "1",
                "node": "hs300",
                "symbol": "",
                "_s_r_a": "init",
            }
            r = requests.get(url, params=params)
            temp_df = temp_df.append(pd.DataFrame(demjson.decode(r.text)), ignore_index=True)
        return temp_df

    url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple"
    params = {
        "page": 1,
        "num": "3000",
        "sort": "symbol",
        "asc": "1",
        "node": f"zhishu_{index}",
        "_s_r_a": "setlen",
    }
    r = requests.get(url, params=params)
    return pd.DataFrame(demjson.decode(r.text))


def index_stock_info() -> pd.DataFrame:
    """
    聚宽-指数数据-指数列表
    https://www.joinquant.com/data/dict/indexData
    :return: 指数信息的数据框
    :rtype: pandas.DataFrame
    """
    index_df = pd.read_html("https://www.joinquant.com/data/dict/indexData")[0]
    index_df["指数代码"] = index_df["指数代码"].str.split(".", expand=True)[0]
    index_df.columns = ["index_code", "display_name", "publish_date", "-", "-"]
    return index_df[["index_code", "display_name", "publish_date"]]


def index_stock_cons(index: str = "399639") -> pd.DataFrame:
    """
    最新股票指数的成份股目录
    http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page=1&indexid=399639
    :param index: 指数代码, 可以通过 index_stock_info 函数获取
    :type index: str
    :return: 最新股票指数的成份股目录
    :rtype: pandas.DataFrame
    """
    url = f"http://vip.stock.finance.sina.com.cn/corp/go.php/vII_NewestComponent/indexid/{index}.phtml"
    r = requests.get(url)
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, "lxml")
    page_num = (
        soup.find(attrs={"class": "table2"})
        .find("td")
        .find_all("a")[-1]["href"]
        .split("page=")[-1]
        .split("&")[0]
    )
    if page_num == "#":
        temp_df = pd.read_html(r.text, header=1)[3].iloc[:, :3]
        temp_df["品种代码"] = temp_df["品种代码"].astype(str).str.zfill(6)
        return temp_df

    temp_df = pd.DataFrame()
    for page in range(1, int(page_num) + 1):
        url = f"http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page={page}&indexid={index}"
        r = requests.get(url)
        r.encoding = "gb2312"
        temp_df = temp_df.append(pd.read_html(r.text, header=1)[3], ignore_index=True)
    temp_df = temp_df.iloc[:, :3]
    temp_df["品种代码"] = temp_df["品种代码"].astype(str).str.zfill(6)
    return temp_df


def index_stock_cons_csindex(index: str = "000300") -> pd.DataFrame:
    """
    最新股票指数的成份股目录-中证指数网站
    http://www.csindex.com.cn/zh-CN/indices/index-detail/000300
    :param index: 指数代码, 可以通过 index_stock_info 函数获取
    :type index: str
    :return: 最新股票指数的成份股目录
    :rtype: pandas.DataFrame
    """
    timestamp = int(time.time())
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'www.csindex.com.cn',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }
    url = f"http://www.csindex.com.cn/uploads/file/autofile/cons/{index}cons.xls?t={timestamp}"
    r = requests.get(url, headers=headers)
    temp_df = pd.read_excel(BytesIO(r.content), usecols="E:F")
    temp_df.columns = ["stock_code", "stock_name"]
    temp_df['stock_code'] = temp_df['stock_code'].astype(str)
    return temp_df


def index_stock_hist(index: str = "sz399975") -> pd.DataFrame:
    """
    指数历史成份, 从 2005 年开始
    http://stock.jrj.com.cn/share,sh000300,2015nlscf_2.shtml
    :param index: 指数代码, 需要带市场前缀
    :type index: str
    :return: 历史成份的进入和退出数据
    :rtype: pandas.DataFrame
    """
    url = f"http://stock.jrj.com.cn/share,{index},2015nlscf.shtml"
    r = requests.get(url)
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, "lxml")
    last_page_num = soup.find_all("a", attrs={"target": "_self"})[-2].text
    temp_df = pd.read_html(r.text)[-1]
    if type(last_page_num) == str:
        temp_df["股票代码"] = temp_df["股票代码"].astype(str).str.zfill(6)
        del temp_df["股票名称"]
        temp_df.columns = ["stock_code", "in_date", "out_date"]
        return temp_df
    for page in range(2, int(last_page_num)+1):
        url = f"http://stock.jrj.com.cn/share,{index},2015nlscf_{page}.shtml"
        r = requests.get(url)
        r.encoding = "gb2312"
        inner_temp_df = pd.read_html(r.text)[-1]
        temp_df = temp_df.append(inner_temp_df)
    temp_df["股票代码"] = temp_df["股票代码"].astype(str).str.zfill(6)
    del temp_df["股票名称"]
    temp_df.columns = ["stock_code", "in_date", "out_date"]
    return temp_df


def stock_a_code_to_symbol(code: str = '000300'):
    """
    输入股票代码判断股票市场
    :return: 带股票市场符号的代码
    :rtype: str
    """
    if code.startswith('60') or code.startswith('900'):
        return f"sh{code}"
    else:
        return f"sz{code}"


if __name__ == "__main__":
    index_stock_cons_csindex_df = index_stock_cons_csindex(index="000300")
    print(index_stock_cons_csindex_df)

    index_stock_cons_csindex_df['symbol'] = index_stock_cons_csindex_df['stock_code'].apply(stock_a_code_to_symbol)
    index_stock_cons_sina_df = index_stock_cons_sina(index="000300")
    print(index_stock_cons_sina_df)

    index_stock_cons_df = index_stock_cons(index="399639")
    print(index_stock_cons_df)

    index_stock_cons_df['symbol'] = index_stock_cons_df['品种代码'].apply(stock_a_code_to_symbol)
    stock_index_hist_df = index_stock_hist(index="sz399975")
    print(stock_index_hist_df)

    index_list = index_stock_info()["index_code"].tolist()
    for item in index_list:
        index_stock_cons_df = index_stock_cons(index=item)
        print(index_stock_cons_df)

