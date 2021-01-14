# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/1/14 15:32
Desc: 破净股统计历史走势
https://www.legulegu.com/stockdata/below-net-asset-statistics
"""
import pandas as pd
import requests


def stock_a_below_net_asset_statistics() -> pd.DataFrame:
    """
    破净股统计历史走势
    https://www.legulegu.com/stockdata/below-net-asset-statistics
    :return: 创新高和新低的股票数量
    :rtype: pandas.DataFrame
    """
    url = "https://www.legulegu.com/stockdata/below-net-asset-statistics-data"
    r = requests.get(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    temp_df["date"] = pd.to_datetime(temp_df["date"], unit="ms").dt.date
    del temp_df["id"]
    temp_df.columns = ["below_net_asset", "total_company", "date"]
    temp_df["below_net_asset_ratio"] = temp_df["below_net_asset"] / temp_df["total_company"]
    temp_df = temp_df[["date", "below_net_asset", "total_company", "below_net_asset_ratio"]]
    temp_df.date = temp_df.date.astype("str")
    temp_df.iloc[:, 1:] = temp_df.iloc[:, 1:].astype(float)
    temp_df.sort_values(['date'], inplace=True)
    return temp_df


if __name__ == '__main__':
    stock_a_below_net_asset_statistics_df = stock_a_below_net_asset_statistics()
    print(stock_a_below_net_asset_statistics_df)
