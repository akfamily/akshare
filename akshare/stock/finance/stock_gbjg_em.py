#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/4/3 18:00
Desc: 东方财富-A股数据-股本结构
https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SH603392&color=b#/gbjg/gbjg
"""

import re

import pandas as pd
import requests


def _normalize_em_secu_code(symbol: str) -> str:
    """
    规范化东方财富使用的证券代码格式。

    :param symbol: 原始证券代码
    :type symbol: str
    :return: 东方财富接口使用的证券代码
    :rtype: str
    """
    symbol = symbol.strip().upper()
    if re.fullmatch(r"\d{6}\.(SH|SZ|BJ)", symbol):
        return symbol
    if re.fullmatch(r"(SH|SZ|BJ)\d{6}", symbol):
        return f"{symbol[2:]}.{symbol[:2]}"
    if re.fullmatch(r"\d{6}", symbol):
        if symbol.startswith(("4", "8")):
            market = "BJ"
        elif symbol.startswith(("5", "6", "9")):
            market = "SH"
        else:
            market = "SZ"
        return f"{symbol}.{market}"
    raise ValueError("Please check if the symbol parameter is correct.")


def _empty_stock_zh_a_gbjg_em_df() -> pd.DataFrame:
    """
    返回股本结构接口的标准空表。

    :return: 标准空表
    :rtype: pandas.DataFrame
    """
    return pd.DataFrame(
        columns=[
            "变更日期",
            "总股本",
            "流通受限股份",
            "其他内资持股(受限)",
            "境内法人持股(受限)",
            "境内自然人持股(受限)",
            "已流通股份",
            "已上市流通A股",
            "变动原因",
        ]
    )


def stock_zh_a_gbjg_em(symbol: str = "603392.SH") -> pd.DataFrame:
    """
    东方财富-A股数据-股本结构
    https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html#/gbjg
    :param symbol: 股票代码
    :type symbol: str
    :return: 股本结构
    :rtype: pandas.DataFrame
    """
    symbol = _normalize_em_secu_code(symbol)
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {
        "reportName": "RPT_F10_EH_EQUITY",
        "columns": "SECUCODE,SECURITY_CODE,END_DATE,TOTAL_SHARES,LIMITED_SHARES,LIMITED_OTHARS,"
        "LIMITED_DOMESTIC_NATURAL,LIMITED_STATE_LEGAL,LIMITED_OVERSEAS_NOSTATE,LIMITED_OVERSEAS_NATURAL,"
        "UNLIMITED_SHARES,LISTED_A_SHARES,B_FREE_SHARE,H_FREE_SHARE,FREE_SHARES,LIMITED_A_SHARES,"
        "NON_FREE_SHARES,LIMITED_B_SHARES,OTHER_FREE_SHARES,LIMITED_STATE_SHARES,"
        "LIMITED_DOMESTIC_NOSTATE,LOCK_SHARES,LIMITED_FOREIGN_SHARES,LIMITED_H_SHARES,"
        "SPONSOR_SHARES,STATE_SPONSOR_SHARES,SPONSOR_SOCIAL_SHARES,RAISE_SHARES,"
        "RAISE_STATE_SHARES,RAISE_DOMESTIC_SHARES,RAISE_OVERSEAS_SHARES,CHANGE_REASON",
        "quoteColumns": "",
        "filter": f'(SECUCODE="{symbol}")',
        "pageNumber": "1",
        "pageSize": "500",
        "sortTypes": "-1",
        "sortColumns": "END_DATE",
        "source": "HSF10",
        "client": "PC",
        "v": "047483522105257925",
    }
    r = requests.get(url, params=params, timeout=30)
    data_json = r.json()
    result = data_json.get("result") or {}
    data_list = result.get("data") or []
    if not data_list:
        return _empty_stock_zh_a_gbjg_em_df()

    total_pages = int(result.get("pages") or 1)
    big_df = pd.DataFrame(data_list)
    # 逐页拉取，避免老股票较长的股本结构历史被静默截断。
    for page in range(2, total_pages + 1):
        params.update({"pageNumber": str(page)})
        r = requests.get(url, params=params, timeout=30)
        page_json = r.json()
        page_result = page_json.get("result") or {}
        page_data = page_result.get("data") or []
        if not page_data:
            continue
        page_df = pd.DataFrame(page_data)
        big_df = pd.concat([big_df, page_df], ignore_index=True)

    temp_df = big_df
    temp_df.rename(
        columns={
            "END_DATE": "变更日期",
            "TOTAL_SHARES": "总股本",
            "LISTED_A_SHARES": "已上市流通A股",
            "FREE_SHARES": "已流通股份",
            "CHANGE_REASON": "变动原因",
            "LIMITED_A_SHARES": "流通受限股份",
            "LIMITED_OTHARS": "其他内资持股(受限)",
            "LIMITED_DOMESTIC_NOSTATE": "境内法人持股(受限)",
            "LIMITED_DOMESTIC_NATURAL": "境内自然人持股(受限)",
        },
        inplace=True,
    )
    temp_df = temp_df[
        [
            "变更日期",
            "总股本",
            "流通受限股份",
            "其他内资持股(受限)",
            "境内法人持股(受限)",
            "境内自然人持股(受限)",
            "已流通股份",
            "已上市流通A股",
            "变动原因",
        ]
    ]
    temp_df["变更日期"] = pd.to_datetime(temp_df["变更日期"], errors="coerce").dt.date
    temp_df["总股本"] = pd.to_numeric(temp_df["总股本"], errors="coerce")
    temp_df["流通受限股份"] = pd.to_numeric(temp_df["流通受限股份"], errors="coerce")
    temp_df["其他内资持股(受限)"] = pd.to_numeric(
        temp_df["其他内资持股(受限)"], errors="coerce"
    )
    temp_df["境内法人持股(受限)"] = pd.to_numeric(
        temp_df["境内法人持股(受限)"], errors="coerce"
    )
    temp_df["境内自然人持股(受限)"] = pd.to_numeric(
        temp_df["境内自然人持股(受限)"], errors="coerce"
    )
    temp_df["已流通股份"] = pd.to_numeric(temp_df["已流通股份"], errors="coerce")
    temp_df["已上市流通A股"] = pd.to_numeric(temp_df["已上市流通A股"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    stock_zh_a_gbjg_em_df = stock_zh_a_gbjg_em(symbol="603392.SH")
    print(stock_zh_a_gbjg_em_df)
