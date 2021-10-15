# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/9/8 21:00
Desc: 东方财富网-数据中心-现货与股票
http://data.eastmoney.com/ifdata/xhgp.html
"""
from akshare.utils import demjson
import pandas as pd
import requests


def futures_spot_stock(indicator: str = "能源") -> pd.DataFrame:
    """
    东方财富网-数据中心-现货与股票
    http://data.eastmoney.com/ifdata/xhgp.html
    :param indicator: choice of {'能源', '化工', '塑料', '纺织', '有色', '钢铁', '建材', '农副'}
    :type indicator: str
    :return: 现货与股票上下游对应数据
    :rtype: pandas.DataFrame
    """
    map_dict = {
        "能源": 0,
        "化工": 1,
        "塑料": 2,
        "纺织": 3,
        "有色": 4,
        "钢铁": 5,
        "建材": 6,
        "农副": 7,
    }
    url = "http://data.eastmoney.com/ifdata/xhgp.html"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "data.eastmoney.com",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    data_text = r.text
    temp_json = demjson.decode(
        data_text[
            data_text.find("pagedata"): data_text.find(
                "/newstatic/js/common/emdataview.js"
            )
        ]
        .strip("pagedata= ")
        .strip(';\n        </script>\n        <script src="')
    )
    date_list = list(temp_json["dates"].values())
    temp_json = temp_json["datas"]
    temp_df = temp_json[map_dict.get(indicator)]
    temp_df = pd.DataFrame(temp_df["list"])
    xyyh_list = [
        "-" if item == [] else ", ".join([inner_item["name"] for inner_item in item])
        for item in temp_df["xyyhs"].tolist()
    ]
    scs_list = [
        "-" if item == [] else ", ".join([inner_item["name"] for inner_item in item])
        for item in temp_df["scss"].tolist()
    ]
    temp_df["scss"] = scs_list
    temp_df["xyyhs"] = xyyh_list
    temp_df.columns = [
        "商品名称",
        date_list[0],
        date_list[1],
        date_list[2],
        date_list[3],
        date_list[4],
        "最新价格",
        "近半年涨跌幅",
        "生产商",
        "下游用户",
    ]
    temp_df[date_list[0]] = pd.to_numeric(temp_df[date_list[0]])
    temp_df[date_list[1]] = pd.to_numeric(temp_df[date_list[1]])
    temp_df[date_list[2]] = pd.to_numeric(temp_df[date_list[2]])
    temp_df[date_list[3]] = pd.to_numeric(temp_df[date_list[3]])
    temp_df['最新价格'] = pd.to_numeric(temp_df['最新价格'])
    temp_df['近半年涨跌幅'] = pd.to_numeric(temp_df['近半年涨跌幅'])
    return temp_df


if __name__ == "__main__":
    for sector in ["能源", "化工", "塑料", "纺织", "有色", "钢铁", "建材", "农副"]:
        futures_spot_stock_df = futures_spot_stock(indicator=sector)
        print(futures_spot_stock_df)
