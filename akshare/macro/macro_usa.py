#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/4/4 18:00
Desc: 金十数据中心-经济指标-美国
https://datacenter.jin10.com/economic
"""

import time

import pandas as pd

from akshare.utils import http


# 东方财富-美国-未决房屋销售月率
def macro_usa_pending_home_sales_em() -> pd.DataFrame:
    """
    东方财富-经济数据一览-美国-未决房屋销售月率
    https://data.eastmoney.com/cjsj/foreign_0_5.html
    :return: 未决房屋销售月率
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_ECONOMICVALUE_USA",
        "columns": "ALL",
        "filter": '(INDICATOR_ID="EMG00342249")',
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "p": "1",
        "pageNo": "1",
        "pageNum": "1",
    }
    r = http.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df = temp_df.rename(
        columns={
            "REPORT_DATE_CH": "时间",
            "PUBLISH_DATE": "发布日期",
            "VALUE": "现值",
            "PRE_VALUE": "前值",
        }
    )
    temp_df = temp_df[
        [
            "时间",
            "前值",
            "现值",
            "发布日期",
        ]
    ]
    temp_df["前值"] = pd.to_numeric(temp_df["前值"], errors="coerce")
    temp_df["现值"] = pd.to_numeric(temp_df["现值"], errors="coerce")
    temp_df["发布日期"] = pd.to_datetime(temp_df["发布日期"], errors="coerce").dt.date
    return temp_df


# 东方财富-经济指标-美国-物价水平-美国核心CPI月率报告
def macro_usa_cpi_yoy() -> pd.DataFrame:
    """
    东方财富-经济数据一览-美国-CPI年率，数据区间从 2008-至今
    https://data.eastmoney.com/cjsj/foreign_0_12.html
    :return: 美国 CPI 年率报告
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_ECONOMICVALUE_USA",
        "columns": "ALL",
        "filter": '(INDICATOR_ID="EMG00000733")',
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
    }
    r = http.get(url, params=params)
    data_json = r.json()
    data_list = data_json["result"]["data"]
    temp_df = pd.DataFrame(
        data_list, columns=["REPORT_DATE", "PUBLISH_DATE", "VALUE", "PRE_VALUE"]
    )
    temp_df = temp_df.rename(
        columns={
            "REPORT_DATE": "时间",
            "PUBLISH_DATE": "发布日期",
            "VALUE": "现值",
            "PRE_VALUE": "前值",
        }
    )
    temp_df["时间"] = pd.to_datetime(temp_df["时间"], errors="coerce").dt.date
    temp_df["发布日期"] = pd.to_datetime(temp_df["发布日期"], errors="coerce").dt.date
    temp_df["前值"] = pd.to_numeric(temp_df["前值"], errors="coerce")
    temp_df["现值"] = pd.to_numeric(temp_df["现值"], errors="coerce")
    temp_df = temp_df.sort_values(by=["时间"], ignore_index=True)
    return temp_df


# 金十数据中心-经济指标-美国-其他-美国原油产量报告
def macro_usa_crude_production() -> pd.DataFrame:
    """
    美国原油产量报告，数据区间从 19830107-至今
    https://datacenter.jin10.com/reportType/dc_eia_crude_oil_produce
    :return: 美国原油产量报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {"_": t}
    res = http.get(
        url="https://cdn.jin10.com/data_center/reports/usa_oil.json", params=params
    )
    temp_df = pd.DataFrame(res.json().get("values")).T
    big_df = pd.DataFrame()
    big_df["美国国内原油总量-产量"] = temp_df["美国国内原油总量"].apply(lambda x: x[0])
    big_df["美国国内原油总量-变化"] = temp_df["美国国内原油总量"].apply(lambda x: x[1])
    big_df["美国本土48州原油产量-产量"] = temp_df["美国本土48州原油产量"].apply(
        lambda x: x[0]
    )
    big_df["美国本土48州原油产量-变化"] = temp_df["美国本土48州原油产量"].apply(
        lambda x: x[1]
    )
    big_df["美国阿拉斯加州原油产量-产量"] = temp_df["美国阿拉斯加州原油产量"].apply(
        lambda x: x[0]
    )
    big_df["美国阿拉斯加州原油产量-变化"] = temp_df["美国阿拉斯加州原油产量"].apply(
        lambda x: x[1]
    )
    big_df = big_df.astype("float")
    big_df = big_df.reset_index()
    big_df = big_df.rename(columns={"index": "日期"})
    big_df = big_df.sort_values(by=["日期"], ignore_index=True)
    return big_df


if __name__ == "__main__":
    # 东方财富-经济指标-美国-未决房屋销售月率
    macro_usa_pending_home_sales_em_df = macro_usa_pending_home_sales_em()
    print(macro_usa_pending_home_sales_em_df)

    # 金十数据中心-经济指标-美国-经济状况-美国GDP

    # 金十数据中心-经济指标-美国-物价水平-美国CPI月率报告

    # 金十数据中心-经济指标-美国-物价水平-美国核心CPI月率报告

    # 金十数据中心-经济指标-美国-物价水平-美国个人支出月率报告

    # 金十数据中心-经济指标-美国-物价水平-美国零售销售月率报告

    # 金十数据中心-经济指标-美国-物价水平-美国进口物价指数报告

    # 金十数据中心-经济指标-美国-物价水平-美国出口价格指数报告

    # 金十数据中心-经济指标-美国-劳动力市场-LMCI

    # 金十数据中心-经济指标-美国-劳动力市场-失业率-美国失业率报告

    # 金十数据中心-经济指标-美国-劳动力市场-失业率-美国挑战者企业裁员人数报告

    # 金十数据中心-经济指标-美国-劳动力市场-就业人口-美国非农就业人数报告

    # 金十数据中心-经济指标-美国-劳动力市场-就业人口-美国ADP就业人数报告

    # 金十数据中心-经济指标-美国-劳动力市场-消费者收入与支出-美国核心PCE物价指数年率报告

    # 金十数据中心-经济指标-美国-劳动力市场-消费者收入与支出-美国实际个人消费支出季率初值报告

    # 金十数据中心-经济指标-美国-贸易状况-美国贸易帐报告

    # 金十数据中心-经济指标-美国-贸易状况-美国经常帐报告

    # 金十数据中心-经济指标-美国-产业指标-制造业-贝克休斯钻井报告

    # 金十数据中心-经济指标-美国-产业指标-制造业-美国生产者物价指数(PPI)报告

    # 金十数据中心-经济指标-美国-产业指标-制造业-美国核心生产者物价指数(PPI)报告

    # 金十数据中心-经济指标-美国-产业指标-制造业-美国API原油库存报告

    # 金十数据中心-经济指标-美国-产业指标-制造业-美国Markit制造业PMI初值报告

    # 金十数据中心-经济指标-美国-产业指标-制造业-美国ISM制造业PMI报告

    # 金十数据中心-经济指标-美国-产业指标-房地产-美国NAHB房产市场指数报告

    # 金十数据中心-经济指标-美国-产业指标-房地产-美国新屋开工总数年化报告

    # 金十数据中心-经济指标-美国-产业指标-房地产-美国新屋销售总数年化报告

    # 金十数据中心-经济指标-美国-产业指标-房地产-美国营建许可总数报告

    # 金十数据中心-经济指标-美国-产业指标-房地产-美国成屋销售总数年化报告

    # 金十数据中心-经济指标-美国-产业指标-房地产-美国FHFA房价指数月率报告

    # 金十数据中心-经济指标-美国-产业指标-房地产-美国S&P/CS20座大城市房价指数年率报告

    # 金十数据中心-经济指标-美国-产业指标-房地产-美国成屋签约销售指数月率报告

    # 金十数据中心-经济指标-美国-领先指标-美国谘商会消费者信心指数报告

    # 金十数据中心-经济指标-美国-领先指标-美国NFIB小型企业信心指数报告

    # 金十数据中心-经济指标-美国-领先指标-美国密歇根大学消费者信心指数初值报告

    # 金十数据中心-经济指标-美国-其他-美国EIA原油库存报告

    # 金十数据中心-经济指标-美国-其他-美国初请失业金人数报告

    # 金十数据中心-经济指标-美国-其他-美国原油产量报告
    macro_usa_crude_production_df = macro_usa_crude_production()
    print(macro_usa_crude_production_df)

    # 金十数据中心-美国商品期货交易委员会CFTC外汇类非商业持仓报告

    # 金十数据中心-美国商品期货交易委员会CFTC商品类非商业持仓报告

    # 金十数据中心-美国商品期货交易委员会CFTC外汇类商业持仓报告

    # 金十数据中心-美国商品期货交易委员会CFTC商品类商业持仓报告

    # 金十数据中心-CME-贵金属
