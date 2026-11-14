#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2026/5/18 18:12
Desc: 百度股市通-外汇-行情榜单
https://finance.baidu.com/top/foreign-rmb
"""

import warnings

import pandas as pd

from akshare.exceptions import APIError
from akshare.utils import http


def fx_quote_baidu(symbol: str = "人民币", token: str = "") -> pd.DataFrame:
    """
    百度股市通-外汇-行情榜单
    https://finance.baidu.com/top/foreign-rmb
    :param symbol: choice of {"人民币", "美元"}
    :type symbol: str
    :param token: 目标网站复制 acs-token 后传入
    :type token: str
    :return: 外汇行情数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "人民币": "rmb",
        "美元": "dollar",
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Origin": "https://finance.baidu.com",
        "Referer": "https://finance.baidu.com/",
        "acs-token": token,
    }
    url = "https://finance.pae.baidu.com/api/getforeignrank"
    out_df = pd.DataFrame()
    num = 0
    while True:
        params = {
            "type": symbol_map[symbol],
            "pn": num,
            "rn": "20",
            "finClientType": "pc",
        }
        r = http.get(url, params=params, headers=headers)
        data_json = r.json()
        result = data_json.get("Result")
        if isinstance(result, dict) and result.get("code") == 403:
            # 被风控拦截时没有数据；放在返回码检查之前，否则只会得到一个空表
            raise APIError(
                "百度股市通拒绝了请求（风控校验，上游提示："
                f"{result.get('msg')}）。该接口需要传入 token：在浏览器打开 "
                "https://finance.baidu.com/top/foreign-rmb ，从请求头中复制 acs-token；"
                "token 很快过期，失效后需要重新复制"
            )
        # 显式检查返回码，便于调试
        if data_json.get("ResultCode") != "0":
            warnings.warn(f"[pn={num}] 接口返回异常: {data_json}")
            break
        result = data_json.get("Result")
        if not result:  # 空列表 → 已到末页
            break
        temp_df = pd.DataFrame(result)
        if temp_df.empty or "list" not in temp_df.columns:
            break
        temp_list = []
        item = None
        for item in temp_df["list"]:
            temp_list.append(list(pd.DataFrame(item).T.iloc[1, :].values))
        if item is None:
            break
        value_df = pd.DataFrame(
            temp_list, columns=pd.DataFrame(item).T.iloc[0, :].values
        )
        big_df = pd.concat(objs=[temp_df, value_df], axis=1)
        for col in ["market", "list", "status", "icon1", "icon2", "financeType"]:
            if col in big_df.columns:
                del big_df[col]
        big_df.columns = ["代码", "名称", "最新价", "涨跌额", "涨跌幅"]
        big_df["最新价"] = pd.to_numeric(big_df["最新价"], errors="coerce")
        big_df["涨跌额"] = pd.to_numeric(big_df["涨跌额"], errors="coerce")
        big_df["涨跌幅"] = (
            pd.to_numeric(big_df["涨跌幅"].str.strip("%"), errors="coerce") / 100
        )
        out_df = pd.concat(objs=[out_df, big_df], ignore_index=True)
        # 如果本页返回不足 20 条，说明是最后一页
        if len(big_df) < 20:
            break
        num += 20
    return out_df


if __name__ == "__main__":
    fx_quote_baidu_df = fx_quote_baidu(symbol="人民币")
    print(fx_quote_baidu_df)
