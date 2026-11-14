# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2024/11/5 16:00
Desc: 雪球-行情中心-沪深股市-内部交易
https://xueqiu.com/hq/insider
"""

from typing import Any

import pandas as pd
import requests

from akshare.exceptions import APIError, NetworkError
from akshare.stock.board.stock_hot_xq import xq_session


def _get_xq_inner_trade_data() -> dict[str, Any]:
    """
    获取雪球内部交易接口原始数据

    :return: 接口 data 字段
    :rtype: dict[str, Any]
    :raises NetworkError: 网络请求异常
    :raises APIError: 上游接口返回异常
    """
    url = "https://xueqiu.com/service/v5/stock/f10/cn/skholderchg"
    params = {
        "size": "100000",
        "page": "1",
        "extend": "true",
    }
    try:
        r = xq_session().get(url, params=params)
        data_json = r.json()
    except requests.RequestException as err:
        raise NetworkError(
            f"Failed to request Xueqiu inner trade endpoint: {err}"
        ) from err
    except ValueError as err:
        raise APIError("Xueqiu inner trade endpoint returned invalid JSON") from err

    if "data" not in data_json:
        error_code = data_json.get("error_code")
        error_description = data_json.get("error_description", "Unknown error")
        raise APIError(
            "Xueqiu inner trade endpoint returned an invalid response; "
            f"upstream returned {error_code}: {error_description}",
            status_code=r.status_code,
        )
    return data_json["data"]


def stock_inner_trade_xq() -> pd.DataFrame:
    """
    雪球-行情中心-沪深股市-内部交易
    https://xueqiu.com/hq/insider
    :return: 内部交易
    :rtype: pandas.DataFrame
    """
    data = _get_xq_inner_trade_data()
    temp_df = pd.DataFrame(data.get("items") or [])
    if temp_df.empty:
        return pd.DataFrame(
            columns=[
                "股票代码",
                "股票名称",
                "变动日期",
                "变动人",
                "变动股数",
                "成交均价",
                "变动后持股数",
                "与董监高关系",
                "董监高职务",
            ]
        )
    temp_df.columns = [
        "股票代码",
        "股票名称",
        "变动人",
        "-",
        "变动日期",
        "变动股数",
        "成交均价",
        "变动后持股数",
        "与董监高关系",
        "董监高职务",
    ]
    temp_df = temp_df[
        [
            "股票代码",
            "股票名称",
            "变动日期",
            "变动人",
            "变动股数",
            "成交均价",
            "变动后持股数",
            "与董监高关系",
            "董监高职务",
        ]
    ]
    temp_df["变动日期"] = (
        pd.to_datetime(temp_df["变动日期"], unit="ms", utc=True)
        .dt.tz_convert("Asia/Shanghai")
        .dt.date
    )
    temp_df["变动股数"] = pd.to_numeric(temp_df["变动股数"], errors="coerce")
    temp_df["成交均价"] = pd.to_numeric(temp_df["成交均价"], errors="coerce")
    temp_df["变动后持股数"] = pd.to_numeric(temp_df["变动后持股数"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    stock_inner_trade_xq_df = stock_inner_trade_xq()
    print(stock_inner_trade_xq_df)
