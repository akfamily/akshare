# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/7/5 20:23
Desc: 中国柯桥纺织指数
http://www.kqindex.cn/flzs/jiage
"""
import pandas as pd
import requests
from tqdm import tqdm


def index_kq_fz(symbol: str = "价格指数") -> pd.DataFrame:
    """
    中国柯桥纺织指数
    http://www.kqindex.cn/flzs/jiage
    :param symbol: choice of {'价格指数', '景气指数', '外贸指数'}
    :type symbol: str
    :return: 中国柯桥纺织指数
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "价格指数": "1_1",
        "景气指数": "1_2",
        "外贸指数": "2",
    }
    url = "http://www.kqindex.cn/flzs/table_data"
    params = {
        "category": "0",
        "start": "",
        "end": "",
        "indexType": f"{symbol_map[symbol]}",
        "pageindex": "1",
        "_": "1619871781413",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    page_num = data_json["page"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1), leave=False):
        params = {
            "category": "0",
            "start": "",
            "end": "",
            "indexType": f"{symbol_map[symbol]}",
            "pageindex": page,
            "_": "1619871781413",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"])
        big_df = big_df.append(temp_df, ignore_index=True)
    if symbol == "价格指数":
        big_df.columns = [
            "期次",
            "指数",
            "涨跌幅",
        ]
    elif symbol == "景气指数":
        big_df.columns = [
            "期次",
            "总景气指数",
            "涨跌幅",
            "流通景气指数",
            "生产景气指数",
        ]
    elif symbol == "外贸指数":
        big_df.columns = [
            "期次",
            "价格指数",
            "涨跌幅",
            "景气指数",
            "涨跌幅",
        ]
    return big_df


if __name__ == "__main__":
    index_kq_df = index_kq_fz(symbol="价格指数")
    print(index_kq_df)

    index_kq_df = index_kq_fz(symbol="景气指数")
    print(index_kq_df)

    index_kq_df = index_kq_fz(symbol="外贸指数")
    print(index_kq_df)
