#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2025/12/18 16:00
Desc: 同花顺-财务指标-主要指标
https://basic.10jqka.com.cn/new/000063/finance.html
"""

import json

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.utils.cons import headers


def stock_financial_abstract_ths(
    symbol: str = "000063", indicator: str = "按报告期"
) -> pd.DataFrame:
    """
    同花顺-财务指标-主要指标
    https://basic.10jqka.com.cn/new/000063/finance.html
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: 指标; choice of {"按报告期", "按年度", "按单季度"}
    :type indicator: str
    :return: 同花顺-财务指标-主要指标
    :rtype: pandas.DataFrame
    """
    url = f"https://basic.10jqka.com.cn/new/{symbol}/finance.html"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")
    data_text = soup.find(name="p", attrs={"id": "main"}).string
    data_json = json.loads(data_text)
    df_index = [
        item[0] if isinstance(item, list) else item for item in data_json["title"]
    ]
    if indicator == "按报告期":
        temp_df = pd.DataFrame(
            data_json["report"][1:], columns=data_json["report"][0], index=df_index[1:]
        )
    elif indicator == "按单季度":
        temp_df = pd.DataFrame(
            data_json["simple"][1:], columns=data_json["simple"][0], index=df_index[1:]
        )
    else:
        temp_df = pd.DataFrame(
            data_json["year"][1:], columns=data_json["year"][0], index=df_index[1:]
        )
    temp_df = temp_df.T
    temp_df.reset_index(inplace=True)
    temp_df.rename(columns={"index": "报告期"}, inplace=True)
    temp_df.sort_values(by="报告期", ignore_index=True, inplace=True)
    return temp_df


def stock_financial_debt_ths(
    symbol: str = "000063", indicator: str = "按报告期"
) -> pd.DataFrame:
    """
    同花顺-财务指标-资产负债表
    https://basic.10jqka.com.cn/new/000063/finance.html
    https://basic.10jqka.com.cn/api/stock/finance/000063_debt.json
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: 指标; choice of {"按报告期", "按年度"}
    :type indicator: str
    :return: 同花顺-财务指标-资产负债表
    :rtype: pandas.DataFrame
    """
    url = f"https://basic.10jqka.com.cn/api/stock/finance/{symbol}_debt.json"
    r = requests.get(url, headers=headers)
    data_json = json.loads(json.loads(r.text)["flashData"])
    df_index = [
        item[0] if isinstance(item, list) else item for item in data_json["title"]
    ]
    if indicator == "按报告期":
        temp_df = pd.DataFrame(
            data_json["report"][1:], columns=data_json["report"][0], index=df_index[1:]
        )
    else:
        temp_df = pd.DataFrame(
            data_json["year"][1:], columns=data_json["year"][0], index=df_index[1:]
        )
    temp_df = temp_df.T
    temp_df.reset_index(inplace=True)
    temp_df.rename(columns={"index": "报告期"}, inplace=True)
    return temp_df


def stock_financial_benefit_ths(
    symbol: str = "000063", indicator: str = "按报告期"
) -> pd.DataFrame:
    """
    同花顺-财务指标-利润表
    https://basic.10jqka.com.cn/new/000063/finance.html
    https://basic.10jqka.com.cn/api/stock/finance/000063_benefit.json
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: 指标; choice of {"按报告期","按单季度", "按年度"}
    :type indicator: str
    :return: 同花顺-财务指标-利润表
    :rtype: pandas.DataFrame
    """
    url = f"https://basic.10jqka.com.cn/api/stock/finance/{symbol}_benefit.json"
    r = requests.get(url, headers=headers)
    data_json = json.loads(json.loads(r.text)["flashData"])
    df_index = [
        item[0] if isinstance(item, list) else item for item in data_json["title"]
    ]
    if indicator == "按报告期":
        temp_df = pd.DataFrame(
            data_json["report"][1:], columns=data_json["report"][0], index=df_index[1:]
        )
    elif indicator == "按单季度":
        temp_df = pd.DataFrame(
            data_json["simple"][1:], columns=data_json["simple"][0], index=df_index[1:]
        )
    else:
        temp_df = pd.DataFrame(
            data_json["year"][1:], columns=data_json["year"][0], index=df_index[1:]
        )
    temp_df = temp_df.T
    temp_df.reset_index(inplace=True)
    temp_df.rename(columns={"index": "报告期"}, inplace=True)
    return temp_df


def stock_financial_cash_ths(
    symbol: str = "000063", indicator: str = "按报告期"
) -> pd.DataFrame:
    """
    同花顺-财务指标-现金流量表
    https://basic.10jqka.com.cn/new/000063/finance.html
    https://basic.10jqka.com.cn/api/stock/finance/000063_cash.json
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: 指标; choice of {"按报告期","按单季度", "按年度"}
    :type indicator: str
    :return: 同花顺-财务指标-现金流量表
    :rtype: pandas.DataFrame
    """
    url = f"https://basic.10jqka.com.cn/api/stock/finance/{symbol}_cash.json"
    r = requests.get(url, headers=headers)
    data_json = json.loads(json.loads(r.text)["flashData"])
    df_index = [
        item[0] if isinstance(item, list) else item for item in data_json["title"]
    ]
    if indicator == "按报告期":
        temp_df = pd.DataFrame(
            data_json["report"][1:], columns=data_json["report"][0], index=df_index[1:]
        )
    elif indicator == "按单季度":
        temp_df = pd.DataFrame(
            data_json["simple"][1:], columns=data_json["simple"][0], index=df_index[1:]
        )
    else:
        temp_df = pd.DataFrame(
            data_json["year"][1:], columns=data_json["year"][0], index=df_index[1:]
        )
    temp_df = temp_df.T
    temp_df.reset_index(inplace=True)
    temp_df.rename(columns={"index": "报告期"}, inplace=True)
    return temp_df


def __get_market_code(stock_code: str = "000063") -> int:
    """
    同花顺-财务指标-主要指标-股票所属市场判断
    :param stock_code: 股票代码
    :type stock_code: str
    :return: 同花顺-财务指标-主要指标
    :rtype: pandas.DataFrame
    """
    # 确保股票代码是字符串并去掉空格
    stock_code = str(stock_code).strip()
    # 检查代码长度
    if len(stock_code) < 6:
        raise "请输入正确的股票代码"
    # 深交所股票: 000, 001, 002, 003, 300开头 (market代码33)
    if stock_code.startswith(("000", "001", "002", "003", "300")):
        return 33
    # 上交所股票: 600, 601, 603, 605, 688开头 (market代码17)
    if stock_code.startswith(("600", "601", "603", "605", "688")):
        return 17
    # 北交所股票: 920开头 (market代码151)
    if stock_code.startswith("920"):
        return 151
    # 其他情况无法识别
    return 0


def stock_financial_abstract_new_ths(
    symbol: str = "000063", indicator: str = "按报告期"
) -> pd.DataFrame:
    """
    同花顺-财务指标-重要指标
    https://basic.10jqka.com.cn/new/000063/finance.html
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: 指标; choice of {"按报告期", "一季度", "二季度", "三季度", "四季度", "按年度"}
    :type indicator: str
    :return: 同花顺-财务指标-主要指标
    :rtype: pandas.DataFrame
    """
    url = "https://basic.10jqka.com.cn/basicapi/finance/index/v1/app_data/"
    if indicator == "按报告期":
        period = "0"
    elif indicator == "一季度":
        period = "1"
    elif indicator == "二季度":
        period = "2"
    elif indicator == "三季度":
        period = "3"
    elif indicator == "四季度":
        period = "4"
    else:
        period = "4"
    params = {
        "code": symbol,
        "id": "client_stock_importance",
        "market": __get_market_code(symbol),
        "type": "stock",
        "page": "1",
        "size": "50",
        "period": period,
    }
    r = requests.get(url, headers=headers, params=params)
    data_json = r.json()
    # 提取财务数据
    financial_data = data_json["data"]["data"]
    # 创建空列表用于存储处理后的数据
    records = []
    # 收集所有可能的指标字段
    all_metric_fields = set()
    # 首先遍历一次，找出所有的字段名
    for report in financial_data:
        for metric_name, metric_values in report["index_list"].items():
            if isinstance(metric_values, dict):
                all_metric_fields.update(metric_values.keys())
    # 遍历每个报告期的数据
    for report in financial_data:
        report_date = report["date"]
        report_name = report["report_name"]
        report_period = report["report"]
        quarter_name = report["quarter_name"]
        # 遍历该报告期的所有财务指标
        for metric_name, metric_values in report["index_list"].items():
            # 基本信息
            record = {
                "report_date": report_date,
                "report_name": report_name,
                "report_period": report_period,
                "quarter_name": quarter_name,
                "metric_name": metric_name,
            }
            # 动态添加所有指标字段
            if isinstance(metric_values, dict):
                for field, value in metric_values.items():
                    record[field] = value
            else:
                # 如果不是字典，将其作为'value'字段
                record["value"] = metric_values
            records.append(record)
    # 创建DataFrame
    df = pd.DataFrame(records)
    # 自动识别并转换数值列
    numeric_columns = []
    for col in df.columns:
        if col not in [
            "report_date",
            "report_name",
            "report_period",
            "quarter_name",
            "metric_name",
        ]:
            # 尝试将列转换为数值类型
            if df[col].dtype == "object":
                # 替换空字符串为NaN
                df[col] = df[col].replace(to_replace="", value=pd.NA)
                # 尝试转换为数值
                numeric_series = pd.to_numeric(df[col], errors="coerce")
                # 如果大部分能转换为数值，则保留转换结果
                if numeric_series.notna().sum() > len(numeric_series) * 0.5:
                    df[col] = numeric_series
                    numeric_columns.append(col)
    return df


def stock_financial_debt_new_ths(
    symbol: str = "000063", indicator: str = "按报告期"
) -> pd.DataFrame:
    """
    同花顺-财务指标-资产负债表
    https://basic.10jqka.com.cn/astockpc/astockmain/index.html#/financen?code=000063
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: 指标; choice of {"按报告期", "按年度"}
    :type indicator: str
    :return: 同花顺-财务指标-资产负债表
    :rtype: pandas.DataFrame
    """
    url = "https://basic.10jqka.com.cn/basicapi/finance/index/v1/app_data/"
    if indicator == "按报告期":
        period = "0"
    else:
        period = "4"
    params = {
        "code": symbol,
        "id": "client_stock_debt",
        "market": __get_market_code(symbol),
        "type": "stock",
        "page": "1",
        "size": "50",
        "period": period,
    }
    r = requests.get(url, headers=headers, params=params)
    data_json = r.json()
    # 提取财务数据
    financial_data = data_json["data"]["data"]
    # 创建空列表用于存储处理后的数据
    records = []
    # 收集所有可能的指标字段
    all_metric_fields = set()
    # 首先遍历一次，找出所有的字段名
    for report in financial_data:
        for metric_name, metric_values in report["index_list"].items():
            if isinstance(metric_values, dict):
                all_metric_fields.update(metric_values.keys())
    # 遍历每个报告期的数据
    for report in financial_data:
        report_date = report["date"]
        report_name = report["report_name"]
        report_period = report["report"]
        quarter_name = report["quarter_name"]
        # 遍历该报告期的所有财务指标
        for metric_name, metric_values in report["index_list"].items():
            # 基本信息
            record = {
                "report_date": report_date,
                "report_name": report_name,
                "report_period": report_period,
                "quarter_name": quarter_name,
                "metric_name": metric_name,
            }
            # 动态添加所有指标字段
            if isinstance(metric_values, dict):
                for field, value in metric_values.items():
                    record[field] = value
            else:
                # 如果不是字典，将其作为'value'字段
                record["value"] = metric_values
            records.append(record)
    # 创建DataFrame
    df = pd.DataFrame(records)
    # 自动识别并转换数值列
    numeric_columns = []
    for col in df.columns:
        if col not in [
            "report_date",
            "report_name",
            "report_period",
            "quarter_name",
            "metric_name",
        ]:
            # 尝试将列转换为数值类型
            if df[col].dtype == "object":
                # 替换空字符串为NaN
                df[col] = df[col].replace(to_replace="", value=pd.NA)
                # 尝试转换为数值
                numeric_series = pd.to_numeric(df[col], errors="coerce")
                # 如果大部分能转换为数值，则保留转换结果
                if numeric_series.notna().sum() > len(numeric_series) * 0.5:
                    df[col] = numeric_series
                    numeric_columns.append(col)
    return df


def stock_financial_benefit_new_ths(
    symbol: str = "000063", indicator: str = "按报告期"
) -> pd.DataFrame:
    """
    同花顺-财务指标-利润表
    https://basic.10jqka.com.cn/astockpc/astockmain/index.html#/financen?code=000063
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: 指标; choice of {"按报告期", "一季度", "二季度", "三季度", "四季度", "按年度"}
    :type indicator: str
    :return: 同花顺-财务指标-利润表
    :rtype: pandas.DataFrame
    """
    url = "https://basic.10jqka.com.cn/basicapi/finance/index/v1/app_data/"
    if indicator == "按报告期":
        period = "0"
    elif indicator == "一季度":
        period = "1"
    elif indicator == "二季度":
        period = "2"
    elif indicator == "三季度":
        period = "3"
    elif indicator == "四季度":
        period = "4"
    else:
        period = "4"
    params = {
        "code": symbol,
        "id": "client_stock_benefit",
        "market": __get_market_code(symbol),
        "type": "stock",
        "page": "1",
        "size": "50",
        "period": period,
    }
    r = requests.get(url, headers=headers, params=params)
    data_json = r.json()
    # 提取财务数据
    financial_data = data_json["data"]["data"]
    # 创建空列表用于存储处理后的数据
    records = []
    # 收集所有可能的指标字段
    all_metric_fields = set()
    # 首先遍历一次，找出所有的字段名
    for report in financial_data:
        for metric_name, metric_values in report["index_list"].items():
            if isinstance(metric_values, dict):
                all_metric_fields.update(metric_values.keys())
    # 遍历每个报告期的数据
    for report in financial_data:
        report_date = report["date"]
        report_name = report["report_name"]
        report_period = report["report"]
        quarter_name = report["quarter_name"]
        # 遍历该报告期的所有财务指标
        for metric_name, metric_values in report["index_list"].items():
            # 基本信息
            record = {
                "report_date": report_date,
                "report_name": report_name,
                "report_period": report_period,
                "quarter_name": quarter_name,
                "metric_name": metric_name,
            }
            # 动态添加所有指标字段
            if isinstance(metric_values, dict):
                for field, value in metric_values.items():
                    record[field] = value
            else:
                # 如果不是字典，将其作为'value'字段
                record["value"] = metric_values
            records.append(record)
    # 创建DataFrame
    df = pd.DataFrame(records)
    # 自动识别并转换数值列
    numeric_columns = []
    for col in df.columns:
        if col not in [
            "report_date",
            "report_name",
            "report_period",
            "quarter_name",
            "metric_name",
        ]:
            # 尝试将列转换为数值类型
            if df[col].dtype == "object":
                # 替换空字符串为NaN
                df[col] = df[col].replace(to_replace="", value=pd.NA)
                # 尝试转换为数值
                numeric_series = pd.to_numeric(df[col], errors="coerce")
                # 如果大部分能转换为数值，则保留转换结果
                if numeric_series.notna().sum() > len(numeric_series) * 0.5:
                    df[col] = numeric_series
                    numeric_columns.append(col)
    return df


def stock_financial_cash_new_ths(
    symbol: str = "000063", indicator: str = "按报告期"
) -> pd.DataFrame:
    """
    同花顺-财务指标-现金流量表
    https://basic.10jqka.com.cn/astockpc/astockmain/index.html#/financen?code=000063
    :param symbol: 股票代码
    :type symbol: str
    :param indicator: 指标; choice of {"按报告期", "一季度", "二季度", "三季度", "四季度", "按年度"}
    :type indicator: str
    :return: 同花顺-财务指标-现金流量表
    :rtype: pandas.DataFrame
    """
    url = "https://basic.10jqka.com.cn/basicapi/finance/index/v1/app_data/"
    if indicator == "按报告期":
        period = "0"
    elif indicator == "一季度":
        period = "1"
    elif indicator == "二季度":
        period = "2"
    elif indicator == "三季度":
        period = "3"
    elif indicator == "四季度":
        period = "4"
    else:
        period = "4"
    params = {
        "code": symbol,
        "id": "client_stock_cash",
        "market": __get_market_code(symbol),
        "type": "stock",
        "page": "1",
        "size": "50",
        "period": period,
    }
    r = requests.get(url, headers=headers, params=params)
    data_json = r.json()
    # 提取财务数据
    financial_data = data_json["data"]["data"]
    # 创建空列表用于存储处理后的数据
    records = []
    # 收集所有可能的指标字段
    all_metric_fields = set()
    # 首先遍历一次，找出所有的字段名
    for report in financial_data:
        for metric_name, metric_values in report["index_list"].items():
            if isinstance(metric_values, dict):
                all_metric_fields.update(metric_values.keys())
    # 遍历每个报告期的数据
    for report in financial_data:
        report_date = report["date"]
        report_name = report["report_name"]
        report_period = report["report"]
        quarter_name = report["quarter_name"]
        # 遍历该报告期的所有财务指标
        for metric_name, metric_values in report["index_list"].items():
            # 基本信息
            record = {
                "report_date": report_date,
                "report_name": report_name,
                "report_period": report_period,
                "quarter_name": quarter_name,
                "metric_name": metric_name,
            }
            # 动态添加所有指标字段
            if isinstance(metric_values, dict):
                for field, value in metric_values.items():
                    record[field] = value
            else:
                # 如果不是字典，将其作为'value'字段
                record["value"] = metric_values
            records.append(record)
    # 创建DataFrame
    df = pd.DataFrame(records)
    # 自动识别并转换数值列
    numeric_columns = []
    for col in df.columns:
        if col not in [
            "report_date",
            "report_name",
            "report_period",
            "quarter_name",
            "metric_name",
        ]:
            # 尝试将列转换为数值类型
            if df[col].dtype == "object":
                # 替换空字符串为NaN
                df[col] = df[col].replace(to_replace="", value=pd.NA)
                # 尝试转换为数值
                numeric_series = pd.to_numeric(df[col], errors="coerce")
                # 如果大部分能转换为数值，则保留转换结果
                if numeric_series.notna().sum() > len(numeric_series) * 0.5:
                    df[col] = numeric_series
                    numeric_columns.append(col)
    return df


def stock_management_change_ths(symbol: str = "688981") -> pd.DataFrame:
    """
    同花顺-公司大事-高管持股变动
    https://basic.10jqka.com.cn/new/688981/event.html
    :param symbol: 股票代码
    :type symbol: str
    :return: 同花顺-公司大事-高管持股变动
    :rtype: pandas.DataFrame
    """
    url = f"https://basic.10jqka.com.cn/new/{symbol}/event.html"
    r = requests.get(url, headers=headers)
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, features="lxml")
    soup_find = soup.find(name="table", attrs={"class": "data_table_1 m_table m_hl"})
    if soup_find is not None:
        content_list = [item.text.strip() for item in soup_find]
        column_names = content_list[1].split("\n")
        row = (
            content_list[3]
            .replace(" ", "")
            .replace("\t", "")
            .replace("\n\n", "")
            .replace("   ", "\n")
            .replace("\n\n", "\n")
            .split("\n")
        )
        row = [item for item in row if item != ""]
        new_rows = []
        step = len(column_names)
        for i in range(0, len(row), step):
            new_rows.append(row[i : i + step])
        temp_df = pd.DataFrame(new_rows, columns=column_names)
        temp_df.sort_values(by="变动日期", ignore_index=True, inplace=True)
        temp_df["变动日期"] = pd.to_datetime(
            temp_df["变动日期"], errors="coerce"
        ).dt.date
        temp_df.rename(
            columns={
                "变动数量（股）": "变动数量",
                "交易均价（元）": "交易均价",
                "剩余股数（股）": "剩余股数",
            },
            inplace=True,
        )
        return temp_df
    return pd.DataFrame()


def stock_shareholder_change_ths(symbol: str = "688981") -> pd.DataFrame:
    """
    同花顺-公司大事-股东持股变动
    https://basic.10jqka.com.cn/new/688981/event.html
    :param symbol: 股票代码
    :type symbol: str
    :return: 同花顺-公司大事-股东持股变动
    :rtype: pandas.DataFrame
    """
    url = f"https://basic.10jqka.com.cn/new/{symbol}/event.html"
    r = requests.get(url, headers=headers)
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, features="lxml")
    soup_find = soup.find(name="table", attrs={"class": "m_table data_table_1 m_hl"})
    if soup_find is not None:
        content_list = [item.text.strip() for item in soup_find]
        column_names = content_list[1].split("\n")
        row = (
            content_list[3]
            .replace("\t", "")
            .replace("\n\n", "")
            .replace("   ", "\n")
            .replace(" ", "")
            .replace("\n\n", "\n")
            .split("\n")
        )
        row = [item for item in row if item != ""]
        new_rows = []
        step = len(column_names)
        for i in range(0, len(row), step):
            new_rows.append(row[i : i + step])
        temp_df = pd.DataFrame(new_rows, columns=column_names)
        temp_df.sort_values(by="公告日期", ignore_index=True, inplace=True)
        temp_df["公告日期"] = pd.to_datetime(
            temp_df["公告日期"], errors="coerce"
        ).dt.date
        temp_df.rename(
            columns={
                "变动数量(股)": "变动数量",
                "交易均价(元)": "交易均价",
                "剩余股份总数(股)": "剩余股份总数",
            },
            inplace=True,
        )
        return temp_df
    return pd.DataFrame()


if __name__ == "__main__":
    stock_financial_abstract_new_ths_df = stock_financial_abstract_new_ths(
        symbol="000063", indicator="按报告期"
    )
    print(stock_financial_abstract_new_ths_df)

    stock_financial_abstract_new_ths_df = stock_financial_abstract_new_ths(
        symbol="000063", indicator="按年度"
    )
    print(stock_financial_abstract_new_ths_df)

    stock_financial_abstract_new_ths_df = stock_financial_abstract_new_ths(
        symbol="000063", indicator="一季度"
    )
    print(stock_financial_abstract_new_ths_df)

    stock_financial_debt_new_ths_df = stock_financial_debt_new_ths(
        symbol="002004", indicator="按报告期"
    )
    print(stock_financial_debt_new_ths_df)

    stock_financial_debt_new_ths_df = stock_financial_debt_new_ths(
        symbol="000063", indicator="按年度"
    )
    print(stock_financial_debt_new_ths_df)

    stock_financial_benefit_new_ths_df = stock_financial_benefit_new_ths(
        symbol="000063", indicator="按报告期"
    )
    print(stock_financial_benefit_new_ths_df)

    stock_financial_benefit_new_ths_df = stock_financial_benefit_new_ths(
        symbol="000063", indicator="按年度"
    )
    print(stock_financial_benefit_new_ths_df)

    stock_financial_benefit_new_ths_df = stock_financial_benefit_new_ths(
        symbol="000063", indicator="一季度"
    )
    print(stock_financial_benefit_new_ths_df)

    stock_financial_cash_new_ths_df = stock_financial_cash_new_ths(
        symbol="000063", indicator="按报告期"
    )
    print(stock_financial_cash_new_ths_df)

    stock_financial_cash_new_ths_df = stock_financial_cash_new_ths(
        symbol="000063", indicator="按年度"
    )
    print(stock_financial_cash_new_ths_df)

    stock_financial_cash_new_ths_df = stock_financial_cash_new_ths(
        symbol="000063", indicator="一季度"
    )
    print(stock_financial_cash_new_ths_df)

    stock_management_change_ths_df = stock_management_change_ths(symbol="688981")
    print(stock_management_change_ths_df)

    stock_shareholder_change_ths_df = stock_shareholder_change_ths(symbol="688981")
    print(stock_shareholder_change_ths_df)
