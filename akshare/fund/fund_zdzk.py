# coding=utf-8
# /usr/bin/env python
"""
Date: 2019/9/15 18:27
Desc: 获取智道智科的私募基金指数数据, 可以为用户提供私募基金策略发展方向的参考
"""
import matplotlib.pyplot as plt
import pandas as pd
import requests

from akshare.fund.cons import zdzk_headers, code_name_map_dict

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def zdzk_fund_index(index_type: int = 28, plot: bool = True) -> pd.DataFrame:
    """
    This interface should update every two weeks
    :param index_type: see docs or docstring
    :type index_type: int
    :param plot: True: plot; False: not plot
    :type plot: Bool
    :return: time series data of specific fund
    :rtype: pandas.Series
    "1": "商品综合",
    "2": "中债新综合",
    "15": "沪深300",
    "28": "智道私募综合指数",
    "30": "智道股票策略指数",
    "32": "智道管理期货指数",
    "34": "智道固定收益指数",
    "36": "智道相对价值指数",
    "38": "智道复合策略指数",
    "40": "智道北京区域指数",
    "42": "智道上海区域指数",
    "44": "智道广州区域指数",
    "46": "智道深圳区域指数",
    "48": "智道浙江区域指数",
    """
    if index_type in (28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48):
        params = {"frequency": 0, "types": index_type}
        url = "https://www.ziasset.com/web/api/complexIndex"
        res = requests.get(url, params=params, headers=zdzk_headers, verify=True)
        json_data = res.json()
        zd_dict = {}
        for item in json_data["data"][str(index_type)]:
            zd_dict.update({item["date"]: item["close"]})
        zd_df = pd.Series(zd_dict)
        zd_df.index = pd.to_datetime(zd_df.index)
        zd_df.name = code_name_map_dict[str(index_type)]
        if plot:
            _plot(data_df=zd_df, title=zd_df.name)
        return zd_df
    else:
        params = {"frequency": 0, "types": 28, "investStrategyTypes": index_type}
        url = "https://www.ziasset.com/web/api/complexIndex"
        res = requests.get(url, params=params, headers=zdzk_headers, verify=True)
        json_data = res.json()
        zd_dict = {}
        for item in json_data["data"][str(index_type)]:
            zd_dict.update({item["date"]: item["close"]})
        zd_df = pd.Series(zd_dict)
        zd_df.index = pd.to_datetime(zd_df.index)
        zd_df.name = code_name_map_dict[str(index_type)]
        if plot:
            _plot(data_df=zd_df, title=zd_df.name)
        return zd_df


def _plot(data_df, title):
    plt.figure(figsize=(20, 10), dpi=300)
    (data_df[0:] / (data_df[0] / 1000)).plot(linewidth=3)
    plt.title(f"私募证券投资基金指数-{title}")
    plt.ylabel("index")
    plt.xlabel("date")
    plt.legend(frameon=True)
    plt.show()


if __name__ == "__main__":
    zdzk_fund_index_se = zdzk_fund_index(index_type=30, plot=True)
    print(zdzk_fund_index_se)
