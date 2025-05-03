#!python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/5/3 
Desc: 义乌小商品指数

目前可以通过这些接口直接请求到json数据

周价格指数：https://apiserver.chinagoods.com/yiwuindex/v1/active/industry/class/history/piweek?gcCode=

月价格指数：https://apiserver.chinagoods.com/yiwuindex/v1/active/industry/class/history/month?gcCode=

月景气指数：https://apiserver.chinagoods.com/yiwuindex/v1/active/industry/class/history/bi?gcCode=

上涨：https://apiserver.chinagoods.com/yiwuindex/v1/active/industry/class/get/rise

下跌：https://apiserver.chinagoods.com/yiwuindex/v1/active/industry/class/get/drop
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def index_yw(symbol: str = "月景气指数") -> pd.DataFrame:
    """
    义乌小商品指数
    https://www.ywindex.com/Home/Product/index/
    :param symbol: choice of {"周价格指数", "月价格指数", "月景气指数"}
    :type symbol: str
    :return: 指数结果
    :rtype: pandas.DataFrame
    """
    import urllib3

    # 禁用InsecureRequestWarning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    if symbol == "月景气指数":
        url = "https://apiserver.chinagoods.com/yiwuindex/v1/active/industry/class/history/bi?gcCode="
        res = requests.get(url, verify=False)
        json_data = res.json()["data"]
        table_df = pd.DataFrame(json_data)
        table_df = table_df[["indextimeno", "totalindex", "scopeindex", "benifitindex", "confidentindex"]]
        
        table_df.columns = ["期数", "景气指数", "规模指数", "效益指数", "市场信心指数"]
        table_df["期数"] = pd.to_datetime(table_df["期数"], errors="coerce").dt.date
        table_df["景气指数"] = pd.to_numeric(table_df["景气指数"], errors="coerce")
        table_df["规模指数"] = pd.to_numeric(table_df["规模指数"], errors="coerce")
        table_df["效益指数"] = pd.to_numeric(table_df["效益指数"], errors="coerce")
        table_df["市场信心指数"] = pd.to_numeric(
            table_df["市场信心指数"], errors="coerce"
        )
        table_df.sort_values(["期数"], inplace=True, ignore_index=True)
        return table_df
    else:
        symbol_map = {
            "周价格指数":"piweek",
            "月价格指数":"month"
        }
        url = f"https://apiserver.chinagoods.com/yiwuindex/v1/active/industry/class/history/{symbol_map[symbol]}?gcCode="
        res = requests.get(url, verify=False)
        json_data = res.json()["data"]
        columns_name = {
            "indextimeno":"期数",
            "totalpriceindex":"价格指数",
            "stockdealpriceindex":"场内价格指数",
            "netdealpriceindex":"网上价格指数",
            "orderdealpriceindex":"订单价格指数",
            "outdealpriceindex":"出口价格指数",
        }
        table_df = pd.DataFrame(json_data,columns=columns_name)
        table_df.columns = [columns_name[name] for name in table_df.columns]

        table_df["期数"] = pd.to_datetime(table_df["期数"], errors="coerce").dt.date
        table_df["价格指数"] = pd.to_numeric(table_df["价格指数"], errors="coerce")
        table_df["场内价格指数"] = pd.to_numeric(
            table_df["场内价格指数"], errors="coerce"
        )
        table_df["网上价格指数"] = pd.to_numeric(
            table_df["网上价格指数"], errors="coerce"
        )
        table_df["订单价格指数"] = pd.to_numeric(
            table_df["订单价格指数"], errors="coerce"
        )
        table_df["出口价格指数"] = pd.to_numeric(
            table_df["出口价格指数"], errors="coerce"
        )
        table_df.sort_values(["期数"], inplace=True, ignore_index=True)
        return table_df
    


if __name__ == "__main__":
    # index_yw_df = index_yw(symbol="周价格指数")
    # print(index_yw_df)

    index_yw_df = index_yw(symbol="月价格指数")
    print(index_yw_df)

    index_yw_df = index_yw(symbol="月景气指数")
    print(index_yw_df)
    
