# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/2/10 21:30
Desc: 东方财富个股人气榜-人气榜
http://guba.eastmoney.com/rank/
"""
import requests
import pandas as pd


def stock_hot_rank_em() -> pd.DataFrame:
    """
    东方财富个股人气榜-人气榜
    http://guba.eastmoney.com/rank/
    :return: 人气榜
    :rtype: pandas.DataFrame
    """
    url = "https://emappdata.eastmoney.com/stockrank/getAllCurrentList"
    payload = {
        "appId": "appId01",
        "globalId": "786e4c21-70dc-435a-93bb-38",
        "marketType": "",
        "pageNo": 1,
        "pageSize": 100,
    }
    r = requests.post(url, json=payload)
    data_json = r.json()
    temp_rank_df = pd.DataFrame(data_json["data"])

    temp_rank_df["mark"] = [
        "0" + "." + item[2:] if "SZ" in item else "1" + "." + item[2:]
        for item in temp_rank_df["sc"]
    ]
    ",".join(temp_rank_df["mark"]) + "?v=08926209912590994"
    params = {
        "ut": "f057cbcbce2a86e2866ab8877db1d059",
        "fltt": "2",
        "invt": "2",
        "fields": "f14,f3,f12,f2",
        "secids": ",".join(temp_rank_df["mark"]) + ",?v=08926209912590994",
    }
    url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["diff"])
    temp_df.columns = ["最新价", "涨跌幅", "代码", "股票名称"]
    temp_df["当前排名"] = temp_rank_df["rk"]
    temp_df["代码"] = temp_rank_df["sc"]
    temp_df = temp_df[
        [
            "当前排名",
            "代码",
            "股票名称",
            "最新价",
            "涨跌幅",
        ]
    ]
    return temp_df


def stock_hot_rank_detail_em(symbol: str = "SH603123") -> pd.DataFrame:
    """
    东方财富个股人气榜-历史趋势及粉丝特征
    http://guba.eastmoney.com/rank/stock?code=000665
    :param symbol: 带市场表示的证券代码
    :type symbol: str
    :return: 个股的历史趋势及粉丝特征
    :rtype: pandas.DataFrame
    """
    url_rank = "https://emappdata.eastmoney.com/stockrank/getHisList"
    payload = {
        "appId": "appId01",
        "globalId": "786e4c21-70dc-435a-93bb-38",
        "marketType": "",
        "srcSecurityCode": symbol,
    }

    url_price = "https://emappdata.eastmoney.com/hisClosePrice/getHisClosePriceList"
    r = requests.post(url_price, json=payload)
    data_json = r.json()

    temp_df = pd.DataFrame(data_json["data"])
    r = requests.post(url_rank, json=payload)
    data_json = r.json()
    temp_df["rank"] = pd.DataFrame(data_json["data"])["rank"]
    temp_df.columns = ["证券代码", "时间", "收盘价", "排名"]
    temp_df = temp_df[["时间", "收盘价", "排名", "证券代码"]]

    url_follow = "https://emappdata.eastmoney.com/stockrank/getHisProfileList"
    r = requests.post(url_follow, json=payload)
    data_json = r.json()
    temp_df["新晋粉丝"] = (
        pd.DataFrame(data_json["data"])["newUidRate"].str.strip("%").astype(float) / 100
    )
    temp_df["铁杆粉丝"] = (
        pd.DataFrame(data_json["data"])["oldUidRate"].str.strip("%").astype(float) / 100
    )
    return temp_df


if __name__ == "__main__":
    stock_hot_rank_em_df = stock_hot_rank_em()
    print(stock_hot_rank_em_df)

    stock_hot_rank_detail_em_df = stock_hot_rank_detail_em()
    print(stock_hot_rank_detail_em_df)

    for stock in stock_hot_rank_em_df["代码"]:
        stock_hot_rank_detail_em_df = stock_hot_rank_detail_em(stock)
        print(stock_hot_rank_detail_em_df)
