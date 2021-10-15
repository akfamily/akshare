# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/7/28 16:13
Desc: 深圳证券交易所-融资融券数据
http://www.szse.cn/disclosure/margin/object/index.html
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_margin_underlying_info_szse(date: str = "20010106") -> pd.DataFrame:
    """
    深圳证券交易所-融资融券数据-标的证券信息
    http://www.szse.cn/disclosure/margin/object/index.html
    :param date: 交易日
    :type date: str
    :return: 标的证券信息
    :rtype: pandas.DataFrame
    """
    url = "http://www.szse.cn/api/report/ShowReport/data"
    params = {
        "SHOWTYPE": "JSON",
        "CATALOGID": "1834_xxpl",
        "txtDate": "-".join([date[:4], date[4:6], date[6:]]),
        "tab1PAGENO": "1",
        "random": "0.7425245522795993",
    }
    headers = {
        "Referer": "http://www.szse.cn/disclosure/margin/object/index.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    total_page = data_json[0]["metadata"]["pagecount"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"tab1PAGENO": page})
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json[0]["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [
        "证券代码",
        "证券简称",
        "融资标的",
        "融券标的",
        "当日可融资",
        "当日可融券",
        "融券卖出价格限制",
        "涨跌幅限制",
    ]
    big_df["证券简称"] = big_df["证券简称"].str.replace("&nbsp;", "")
    return big_df


def stock_margin_szse(date: str = "20210727") -> pd.DataFrame:
    """
    深圳证券交易所-融资融券数据-融资融券汇总
    http://www.szse.cn/disclosure/margin/margin/index.html
    :param date: 交易日
    :type date: str
    :return: 融资融券汇总
    :rtype: pandas.DataFrame
    """
    url = "http://www.szse.cn/api/report/ShowReport/data"
    params = {
        "SHOWTYPE": "JSON",
        "CATALOGID": "1837_xxpl",
        "txtDate": "-".join([date[:4], date[4:6], date[6:]]),
        "tab1PAGENO": "1",
        "random": "0.7425245522795993",
    }
    headers = {
        "Referer": "http://www.szse.cn/disclosure/margin/object/index.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json[0]["data"])
    temp_df.columns = [
        "融资买入额",
        "融资余额",
        "融券卖出量",
        "融券余量",
        "融券余额",
        "融资融券余额",
    ]
    temp_df["融资买入额"] = temp_df["融资买入额"].str.replace(",", "")
    temp_df["融资买入额"] = pd.to_numeric(temp_df["融资买入额"])
    temp_df["融资余额"] = temp_df["融资余额"].str.replace(",", "")
    temp_df["融资余额"] = pd.to_numeric(temp_df["融资余额"])
    temp_df["融券卖出量"] = temp_df["融券卖出量"].str.replace(",", "")
    temp_df["融券卖出量"] = pd.to_numeric(temp_df["融券卖出量"])
    temp_df["融券余量"] = temp_df["融券余量"].str.replace(",", "")
    temp_df["融券余量"] = pd.to_numeric(temp_df["融券余量"])
    temp_df["融券余额"] = temp_df["融券余额"].str.replace(",", "")
    temp_df["融券余额"] = pd.to_numeric(temp_df["融券余额"])
    temp_df["融资融券余额"] = temp_df["融资融券余额"].str.replace(",", "")
    temp_df["融资融券余额"] = pd.to_numeric(temp_df["融资融券余额"])
    return temp_df


def stock_margin_detail_szse(date: str = "20210728") -> pd.DataFrame:
    """
    深证证券交易所-融资融券数据-融资融券明细
    http://www.szse.cn/disclosure/margin/margin/index.html
    :param date: 交易日期
    :type date: str
    :return: 融资融券明细
    :rtype: pandas.DataFrame
    """
    url = "http://www.szse.cn/api/report/ShowReport/data"
    params = {
        "SHOWTYPE": "JSON",
        "CATALOGID": "1837_xxpl",
        "txtDate": "-".join([date[:4], date[4:6], date[6:]]),
        "tab2PAGENO": "1",
        "random": "0.7425245522795993",
    }
    headers = {
        "Referer": "http://www.szse.cn/disclosure/margin/margin/index.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    total_page = data_json[1]["metadata"]["pagecount"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"tab2PAGENO": page})
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json[1]["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [
        "证券代码",
        "证券简称",
        "融资买入额",
        "融资余额",
        "融券卖出量",
        "融券余量",
        "融券余额",
        "融资融券余额",
    ]
    big_df["证券简称"] = big_df["证券简称"].str.replace("&nbsp;", "")
    big_df["融资买入额"] = big_df["融资买入额"].str.replace(",", "")
    big_df["融资买入额"] = pd.to_numeric(big_df["融资买入额"])
    big_df["融资余额"] = big_df["融资余额"].str.replace(",", "")
    big_df["融资余额"] = pd.to_numeric(big_df["融资余额"])
    big_df["融券卖出量"] = big_df["融券卖出量"].str.replace(",", "")
    big_df["融券卖出量"] = pd.to_numeric(big_df["融券卖出量"])
    big_df["融券余量"] = big_df["融券余量"].str.replace(",", "")
    big_df["融券余量"] = pd.to_numeric(big_df["融券余量"])
    big_df["融券余额"] = big_df["融券余额"].str.replace(",", "")
    big_df["融券余额"] = pd.to_numeric(big_df["融券余额"])
    big_df["融资融券余额"] = big_df["融资融券余额"].str.replace(",", "")
    big_df["融资融券余额"] = pd.to_numeric(big_df["融资融券余额"])
    return big_df


if __name__ == "__main__":
    stock_margin_underlying_info_szse_df = stock_margin_underlying_info_szse(
        date="20210727"
    )
    print(stock_margin_underlying_info_szse_df)

    stock_margin_szse_df = stock_margin_szse(date="20210401")
    print(stock_margin_szse_df)

    stock_margin_detail_szse_df = stock_margin_detail_szse(date="20210728")
    print(stock_margin_detail_szse_df)
