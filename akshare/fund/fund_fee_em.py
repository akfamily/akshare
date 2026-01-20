#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/12/22 17:00
Desc: 天天基金-基金档案
https://fundf10.eastmoney.com/jjfl_015641.html
"""

import re
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup


def fund_fee_em(symbol: str = "015641", indicator: str = "认购费率") -> pd.DataFrame:
    """
    天天基金-基金档案-购买信息
    https://fundf10.eastmoney.com/jjfl_015641.html
    :param symbol: 基金代码
    :type symbol: str
    :param indicator: choice of {"交易状态", "申购与赎回金额", "交易确认日", "运作费用", "认购费率（前端）", "认购费率（后端）","申购费率（前端）", "赎回费率"}
    :type indicator: str
    :return: 交易规则
    :rtype: pandas.DataFrame
    """
    url = f"https://fundf10.eastmoney.com/jjfl_{symbol}.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    tables_dict = {}
    title_elements = soup.find_all(name="h4", class_="t")
    for title_elem in title_elements:
        title_text = title_elem.get_text(strip=True)
        title_text = re.sub(r"\s+", " ", title_text).strip()
        if title_text == "申购与赎回金额":
            next_table = title_elem.find_all_next("table")[0]
            next_next_table = title_elem.find_all_next("table")[1]
            table_html = str(next_table)
            next_table_html = str(next_next_table)
            df_1 = pd.read_html(StringIO(table_html))[0]
            df_2 = pd.read_html(StringIO(next_table_html))[0]
            df = pd.concat(objs=[df_1, df_2], ignore_index=True)
            tables_dict[title_text] = df
            continue
        else:
            next_table = title_elem.find_next("table")

        if next_table:
            try:
                # 将表格转换为HTML字符串，然后使用pd.read_html读取
                table_html = str(next_table)
                df = pd.read_html(StringIO(table_html))[0]
                tables_dict[title_text] = df
            except Exception as e:
                print("Error:", e)
                continue

    if indicator == "交易状态":
        temp_df = tables_dict[indicator]
    elif indicator == "申购与赎回金额":
        temp_df = tables_dict[indicator]
    elif indicator == "交易确认日":
        temp_df = tables_dict[indicator]
    elif indicator == "运作费用":
        temp_df = tables_dict[indicator]
    elif indicator == "认购费率（后端）":
        temp_df = tables_dict[indicator]
    elif indicator == "认购费率（前端）":
        temp_df = tables_dict[indicator]
        temp_df["原费率"] = temp_df["原费率|天天基金优惠费率"].str.split(
            "|", expand=True
        )[0]
        temp_df["天天基金优惠费率"] = temp_df["原费率|天天基金优惠费率"].str.split(
            "|", expand=True
        )[1]
        del temp_df["原费率|天天基金优惠费率"]
        temp_df.loc[3, "天天基金优惠费率"] = temp_df.loc[3, "原费率"]
        temp_df["原费率"] = temp_df["原费率"].str.strip()
        temp_df["天天基金优惠费率"] = temp_df["天天基金优惠费率"].str.strip()
    elif indicator == "申购费率（前端）":
        temp_df = tables_dict[indicator]
        if temp_df["原费率|天天基金优惠费率 银行卡购买|活期宝购买"].str.split(
            "|", expand=True
        ).shape == (1, 1):
            temp_df["原费率"] = temp_df[
                "原费率|天天基金优惠费率 银行卡购买|活期宝购买"
            ].str.split("|", expand=True)[0]
            temp_df["天天基金优惠费率-银行卡购买"] = temp_df[
                "原费率|天天基金优惠费率 银行卡购买|活期宝购买"
            ].str.split("|", expand=True)[0]
            temp_df["天天基金优惠费率-活期宝购买"] = temp_df[
                "原费率|天天基金优惠费率 银行卡购买|活期宝购买"
            ].str.split("|", expand=True)[0]
            del temp_df["原费率|天天基金优惠费率 银行卡购买|活期宝购买"]
        elif temp_df["原费率|天天基金优惠费率 银行卡购买|活期宝购买"].str.split(
            "|", expand=True
        ).shape == (3, 3):
            temp_df["原费率"] = temp_df[
                "原费率|天天基金优惠费率 银行卡购买|活期宝购买"
            ].str.split("|", expand=True)[0]
            temp_df["天天基金优惠费率-银行卡购买"] = temp_df[
                "原费率|天天基金优惠费率 银行卡购买|活期宝购买"
            ].str.split("|", expand=True)[1]
            temp_df["天天基金优惠费率-活期宝购买"] = temp_df[
                "原费率|天天基金优惠费率 银行卡购买|活期宝购买"
            ].str.split("|", expand=True)[2]
            temp_df.loc[2, "天天基金优惠费率-银行卡购买"] = temp_df.loc[2, "原费率"]
            temp_df.loc[2, "天天基金优惠费率-活期宝购买"] = temp_df.loc[2, "原费率"]
            del temp_df["原费率|天天基金优惠费率 银行卡购买|活期宝购买"]
        else:
            temp_df["原费率"] = temp_df[
                "原费率|天天基金优惠费率 银行卡购买|活期宝购买"
            ].str.split("|", expand=True)[0]
            temp_df["天天基金优惠费率-银行卡购买"] = temp_df[
                "原费率|天天基金优惠费率 银行卡购买|活期宝购买"
            ].str.split("|", expand=True)[1]
            temp_df["天天基金优惠费率-活期宝购买"] = temp_df[
                "原费率|天天基金优惠费率 银行卡购买|活期宝购买"
            ].str.split("|", expand=True)[2]
            del temp_df["原费率|天天基金优惠费率 银行卡购买|活期宝购买"]
            temp_df.loc[3, "天天基金优惠费率-银行卡购买"] = temp_df.loc[3, "原费率"]
            temp_df.loc[3, "天天基金优惠费率-活期宝购买"] = temp_df.loc[3, "原费率"]
        temp_df["原费率"] = temp_df["原费率"].str.strip()
        temp_df["天天基金优惠费率-银行卡购买"] = temp_df[
            "天天基金优惠费率-银行卡购买"
        ].str.strip()
        temp_df["天天基金优惠费率-活期宝购买"] = temp_df[
            "天天基金优惠费率-活期宝购买"
        ].str.strip()
    elif indicator == "赎回费率":
        temp_df = tables_dict[indicator]
    else:
        temp_df = pd.DataFrame([])
    return temp_df


if __name__ == "__main__":
    fund_fee_em_df = fund_fee_em(symbol="019005", indicator="交易状态")
    print(fund_fee_em_df)

    fund_fee_em_df = fund_fee_em(symbol="019005", indicator="申购与赎回金额")
    print(fund_fee_em_df)

    fund_fee_em_df = fund_fee_em(symbol="019005", indicator="交易确认日")
    print(fund_fee_em_df)

    fund_fee_em_df = fund_fee_em(symbol="019005", indicator="运作费用")
    print(fund_fee_em_df)

    fund_fee_em_df = fund_fee_em(symbol="019005", indicator="认购费率（前端）")
    print(fund_fee_em_df)

    fund_fee_em_df = fund_fee_em(symbol="019005", indicator="申购费率（前端）")
    print(fund_fee_em_df)

    fund_fee_em_df = fund_fee_em(symbol="000011", indicator="赎回费率")
    print(fund_fee_em_df)

    fund_fee_em_df = fund_fee_em(symbol="022364", indicator="申购费率（前端）")
    print(fund_fee_em_df)

    fund_fee_em_df = fund_fee_em(symbol="022365", indicator="申购费率（前端）")
    print(fund_fee_em_df)

    fund_fee_em_df = fund_fee_em(symbol="006030", indicator="申购费率（前端）")
    print(fund_fee_em_df)

    fund_fee_em_df = fund_fee_em(symbol="000011", indicator="认购费率（后端）")
    print(fund_fee_em_df)
