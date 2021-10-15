# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/5/4 15:12
Desc: 东方财富网-数据中心-研究报告-盈利预测
http://data.eastmoney.com/report/profitforecast.jshtml
"""
from datetime import datetime

import pandas as pd
import requests
from tqdm import tqdm


def stock_profit_forecast():
    """
    东方财富网-数据中心-研究报告-盈利预测
    http://data.eastmoney.com/report/profitforecast.jshtml
    :return: 盈利预测
    :rtype: pandas.DataFrame
    """
    url = "http://reportapi.eastmoney.com/report/predic"
    date_now = datetime.now().date().isoformat()
    date_previous = date_now.replace(date_now[:4], str(int(date_now[:4]) - 2))
    params = {
        "dyCode": "*",
        "pageNo": "1",
        "pageSize": "100",
        "fields": "",
        "beginTime": date_previous,
        "endTime": date_now,
        "hyCode": "*",
        "gnCode": "*",
        "marketCode": "*",
        "sort": "count,desc",
        "p": "1",
        "pageNum": "1",
        "_": "1615374649216",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    page_num = data_json["TotalPage"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1)):
        params = {
            "dyCode": "*",
            "pageNo": page,
            "pageSize": "100",
            "fields": "",
            "beginTime": date_previous,
            "endTime": date_now,
            "hyCode": "*",
            "gnCode": "*",
            "marketCode": "*",
            "sort": "count,desc",
            "p": page,
            "pageNum": page,
            "_": "1615374649216",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    big_df.columns = [
        "序号",
        "名称",
        "代码",
        "研报数",
        "机构投资评级(近六个月)-买入",
        "机构投资评级(近六个月)-增持",
        "机构投资评级(近六个月)-中性",
        "机构投资评级(近六个月)-减持",
        "机构投资评级(近六个月)-卖出",
        "_",
        "_",
        "_",
        "_",
        f"{int(date_previous[:4])+2}预测每股收益",
        "_",
        "_",
        f"{int(date_previous[:4])+3}预测每股收益",
        f"{int(date_previous[:4])+4}预测每股收益",
        "_",
        "_",
        "_",
        "_",
        "_",
        f"{int(date_previous[:4])+1}预测每股收益",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]

    big_df = big_df[
        [
            "序号",
            "代码",
            "名称",
            "研报数",
            "机构投资评级(近六个月)-买入",
            "机构投资评级(近六个月)-增持",
            "机构投资评级(近六个月)-中性",
            "机构投资评级(近六个月)-减持",
            "机构投资评级(近六个月)-卖出",
            f"{int(date_previous[:4])+1}预测每股收益",
            f"{int(date_previous[:4])+2}预测每股收益",
            f"{int(date_previous[:4])+3}预测每股收益",
            f"{int(date_previous[:4])+4}预测每股收益",
        ]
    ]
    return big_df


if __name__ == "__main__":
    stock_profit_forecast_df = stock_profit_forecast()
    print(stock_profit_forecast_df)
