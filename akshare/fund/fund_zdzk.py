# coding=utf-8
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/15 18:27
desc: 获取智道智科的私募基金指数数据, 可以为用户提供私募基金策略发展方向的参考
"""
import matplotlib.pyplot as plt
import pandas as pd
import requests

from akshare.fund.cons import zdzk_headers, code_name_map_dict

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 步骤一(替换sans-serif字体)
plt.rcParams["axes.unicode_minus"] = False  # 步骤二(解决坐标轴负数的负号显示问题)


def zdzk_fund_index(index_type=28, plot=True):
    """
    两周更新
    index_type 设置如下值, 可以获取相应的指数数据
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
    :param index_type: int 请查看函数说明
    :param plot: Bool 是否画图
    :return: pandas.Series
    2010-01-01    1000.000000
    2010-01-08     998.797040
    2010-01-15    1026.032462
    2010-01-22    1010.435691
    2010-01-29     997.161471
                     ...
    2019-08-23    2002.386909
    2019-08-30    2002.164982
    2019-09-06    2039.292515
    2019-09-13    2050.871850
    2019-09-20    2046.159399
    Name: 智道私募综合指数, Length: 508, dtype: float64
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
    plt.ylabel("指数")
    plt.xlabel("时间")
    plt.legend(frameon=True)
    plt.show()


if __name__ == "__main__":
    zdzk_fund_index_se = zdzk_fund_index(index_type=30, plot=True)
    print(zdzk_fund_index_se)
