# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/7/2 15:32
Desc: 破净股统计历史走势
https://www.legulegu.com/stockdata/below-net-asset-statistics
"""
import pandas as pd
import requests


def stock_a_below_net_asset_statistics(symbol: str = "全部A股") -> pd.DataFrame:
    """
    破净股统计历史走势
    https://www.legulegu.com/stockdata/below-net-asset-statistics
    :param symbol: choice of {"全部A股", "沪深300"}
    :type symbol: str
    :return: 创新高和新低的股票数量
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "全部A股": "1",
        "沪深300": "000300.XSHG",
    }
    url = "https://www.legulegu.com/stockdata/below-net-asset-statistics-data"
    params = {
        "marketId": symbol_map[symbol],
        "token": "325843825a2745a2a8f9b9e3355cb864",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    temp_df["date"] = pd.to_datetime(temp_df["date"], unit="ms").dt.date
    del temp_df["id"]
    del temp_df["marketId"]
    temp_df = temp_df.iloc[:, :3]
    temp_df.columns = ["below_net_asset", "total_company", "date"]
    temp_df["below_net_asset_ratio"] = round(
        temp_df["below_net_asset"] / temp_df["total_company"], 4
    )
    temp_df = temp_df[
        ["date", "below_net_asset", "total_company", "below_net_asset_ratio"]
    ]
    temp_df.date = temp_df.date.astype("str")
    temp_df.iloc[:, 1:] = temp_df.iloc[:, 1:].astype(float)
    temp_df.sort_values(["date"], inplace=True)
    return temp_df


if __name__ == "__main__":
    stock_a_below_net_asset_statistics_df = stock_a_below_net_asset_statistics(symbol="全部A股")
    print(stock_a_below_net_asset_statistics_df)

    stock_a_below_net_asset_statistics_df = stock_a_below_net_asset_statistics(symbol="沪深300")
    print(stock_a_below_net_asset_statistics_df)
