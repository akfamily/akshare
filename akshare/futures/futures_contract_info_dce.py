#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/8/18 11:00
Desc: 大连商品交易所-业务/服务-业务参数-交易参数-合约信息查询
http://www.dce.com.cn/dalianshangpin/ywfw/ywcs/jycs/hyxxcx/index.html
"""

import pandas as pd
import requests


def futures_contract_info_dce() -> pd.DataFrame:
    """
    大连商品交易所-数据中心-业务数据-交易参数-合约信息
    http://www.dce.com.cn/dce/channel/list/180.html
    :return: 交易参数汇总查询
    :rtype: pandas.DataFrame
    """
    url = "http://www.dce.com.cn/dcereport/publicweb/tradepara/contractInfo"
    payload = {
        "lang": "zh",
        "tradeType": "1",
        "varietyId": "all",
    }
    r = requests.post(url, json=payload)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.rename(
        columns={
            "contractId": "合约",
            "variety": "品种名称",
            "varietyOrder": "品种代码",
            "unit": "交易单位",
            "tick": "最小变动价位",
            "startTradeDate": "开始交易日",
            "endTradeDate": "最后交易日",
            "endDeliveryDate": "最后交割日",
            "tradeType": "",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "品种名称",
            "合约",
            "交易单位",
            "最小变动价位",
            "开始交易日",
            "最后交易日",
            "最后交割日",
        ]
    ]
    temp_df["交易单位"] = pd.to_numeric(temp_df["交易单位"], errors="coerce")
    temp_df["最小变动价位"] = pd.to_numeric(temp_df["最小变动价位"], errors="coerce")
    temp_df["开始交易日"] = pd.to_datetime(
        temp_df["开始交易日"], format="%Y%m%d", errors="coerce"
    ).dt.date
    temp_df["最后交易日"] = pd.to_datetime(
        temp_df["最后交易日"], format="%Y%m%d", errors="coerce"
    ).dt.date
    temp_df["最后交割日"] = pd.to_datetime(
        temp_df["最后交割日"], format="%Y%m%d", errors="coerce"
    ).dt.date
    return temp_df


if __name__ == "__main__":
    futures_contract_info_dce_df = futures_contract_info_dce()
    print(futures_contract_info_dce_df)
