#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/10/30
Desc: 中国外汇交易中心暨全国银行间同业拆借中心-基准-外汇市场-外汇掉期曲线-外汇掉期 C-Swap 定盘曲线
https://www.chinamoney.com.cn/chinese/bkcurvfsw
"""

import pandas as pd

from akshare.utils import http


def fx_c_swap_cm():
    """
    中国外汇交易中心暨全国银行间同业拆借中心-基准-外汇市场-外汇掉期曲线-外汇掉期 C-Swap 定盘曲线
    https://www.chinamoney.com.cn/chinese/bkcurvfsw
    :return: 外汇掉期 C-Swap 定盘曲线
    :rtype: pandas.DataFrame
    """
    # www.chinamoney.org.cn 已无法完成 TLS 握手，同一路径在 www.chinamoney.com.cn
    # 下可正常访问，且无需再放开旧式 TLS 重协商
    url = "https://www.chinamoney.com.cn/r/cms/www/chinamoney/data/fx/fx-c-sw-curv-USD.CNY.json"
    payload = {
        "t": "1757402201554",
    }
    r = http.post(url, data=payload)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df = temp_df.rename(
        columns={
            "curveTime": "日期时间",
            "tenor": "期限品种",
            "swapPnt": "掉期点(Pips)",
            "dataSource": "掉期点数据源",
            "swapAllPrc": "全价汇率",
        },
    )
    temp_df = temp_df[
        [
            "日期时间",
            "期限品种",
            "掉期点(Pips)",
            "掉期点数据源",
            "全价汇率",
        ]
    ]
    temp_df["掉期点(Pips)"] = pd.to_numeric(temp_df["掉期点(Pips)"], errors="coerce")
    temp_df["全价汇率"] = pd.to_numeric(temp_df["全价汇率"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    fx_c_swap_cm_df = fx_c_swap_cm()
    print(fx_c_swap_cm_df)
