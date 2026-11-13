#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/4/3 17:08
Desc: 金十数据中心-经济指标-欧元区
金十数据中心-经济指标-欧元区-国民经济运行状况-经济状况
金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平
金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场
金十数据中心-经济指标-欧元区-贸易状况
金十数据中心-经济指标-欧元区-产业指标
金十数据中心-经济指标-欧元区-领先指标
"""

import ast
import time

import pandas as pd

from akshare.utils import http


# 金十数据中心-伦敦金属交易所(LME)-库存报告
def macro_lme_inventory() -> pd.DataFrame:
    """
    伦敦金属交易所(LME)-库存报告，数据区间从 20140702-至今
    https://datacenter.jin10.com/reportType/dc_lme_report
    https://cdn.jin10.com/data_center/reports/lme_stock.json?_=1591535304783
    :return: 伦敦金属交易所(LME)-库存报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {"_": str(int(round(t * 1000)))}
    r = http.get(
        url="https://cdn.jin10.com/data_center/reports/lme_stock.json", params=params
    )
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(
                lambda x: ast.literal_eval(str(x))[i]
            )
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat(objs=[big_df, inner_temp_df], axis=1)
    big_df = big_df.sort_index()
    big_df = big_df.reset_index()
    big_df = big_df.rename(columns={"index": "日期"})
    return big_df


if __name__ == "__main__":
    # 金十数据中心-经济指标-欧元区-国民经济运行状况
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-经济状况
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-经济状况-欧元区季度GDP年率报告

    # 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区CPI月率报告
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区CPI年率报告
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区PPI月率报告
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区零售销售月率报告

    # 金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场-欧元区季调后就业人数季率报告
    # 金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场-欧元区失业率报告
    # 金十数据中心-经济指标-欧元区-贸易状况
    # 金十数据中心-经济指标-欧元区-贸易状况-欧元区未季调贸易帐报告
    # 金十数据中心-经济指标-欧元区-贸易状况-欧元区经常帐报告
    # 金十数据中心-经济指标-欧元区-产业指标
    # 金十数据中心-经济指标-欧元区-产业指标-欧元区工业产出月率报告
    # 金十数据中心-经济指标-欧元区-产业指标-欧元区制造业PMI初值报告

    # 金十数据中心-经济指标-欧元区-产业指标-欧元区服务业PMI终值报告

    # 金十数据中心-经济指标-欧元区-领先指标
    # 金十数据中心-经济指标-欧元区-领先指标-欧元区ZEW经济景气指数报告

    # 金十数据中心-经济指标-欧元区-领先指标-欧元区Sentix投资者信心指数报告

    # 金十数据中心-伦敦金属交易所(LME)-持仓报告

    # 金十数据中心-伦敦金属交易所(LME)-库存报告
    macro_lme_inventory_df = macro_lme_inventory()
    print(macro_lme_inventory_df)
