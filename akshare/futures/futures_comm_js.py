#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/2/22 15:45
Desc: 金十数据-期货手续费
https://www.jin10.com/
"""
import json

import pandas as pd
import requests


def futures_comm_js(date: str = "20260213") -> pd.DataFrame:
    """
    金十财经-期货手续费
    https://www.jin10.com/
    :param date: 日期; 格式为 YYYYMMDD，例如 "20250213"
    :type date: str
    :return: 期货手续费数据
    :rtype: pandas.DataFrame
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36",
        "x-app-id": "fiXF2nOnDycGutVA",
        "x-version": "1.0",
        "referer": "https://www.jin10.com/",
        "origin": "https://www.jin10.com",
    }
    url = "https://mp-api.jin10.com/api/dynamic-data/child"
    formatted_date = "-".join([date[:4], date[4:6], date[6:]])
    params = {
        "tb_name": "_vir_26",
        "search": json.dumps({"range,date": f"{formatted_date},{formatted_date}", "status": 1}),
        "order": "date,desc",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df = temp_df.rename(
        columns={
            "date": "日期",
            "heyue_name": "合约品种",
            "heyue_code": "合约代码",
            "pub_date_commission": "手续费公布时间",
            "pub_date_price": "价格公布时间",
            "heyue_price": "现价",
            "up_limit_num": "涨停板",
            "down_limit_num": "跌停板",
            "buy_ratio": "保证金/买开",
            "sell_ratio": "保证金/卖开",
            "per_lot_price": "保证金/每手",
            "per_ratio": "每手跳数",
            "buy_commission": "开仓",
            "sell_yesterday_commission": "平昨",
            "sell_cur_commission": "平今",
            "per_commission_price": "每跳毛利",
            "per_net_profit": "每跳净利",
            "jys": "交易所",
        }
    )
    temp_df = temp_df.drop(
        columns=["id", "status", "created_at", "updated_at", "_date", "_pub_date_commission", "_pub_date_price"],
        errors="ignore")
    temp_df['日期'] = pd.to_datetime(temp_df['日期'], errors="coerce").dt.date
    temp_df['现价'] = pd.to_numeric(temp_df['现价'], errors="coerce")
    temp_df['涨停板'] = pd.to_numeric(temp_df['涨停板'], errors="coerce")
    temp_df['跌停板'] = pd.to_numeric(temp_df['跌停板'], errors="coerce")
    temp_df['每手跳数'] = pd.to_numeric(temp_df['每手跳数'], errors="coerce")
    temp_df['每跳毛利'] = pd.to_numeric(temp_df['每跳毛利'], errors="coerce")
    temp_df['每跳净利'] = pd.to_numeric(temp_df['每跳净利'], errors="coerce")
    return temp_df


if __name__ == "__main__":
    futures_comm_js_df = futures_comm_js(date="20260213")
    print(futures_comm_js_df)
