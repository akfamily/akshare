#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/12/18 17:30
Desc: 东方财富网-数据中心-特色数据-股权质押
东方财富网-数据中心-特色数据-股权质押-股权质押市场概况：https://data.eastmoney.com/gpzy/marketProfile.aspx
东方财富网-数据中心-特色数据-股权质押-上市公司质押比例：https://data.eastmoney.com/gpzy/pledgeRatio.aspx
东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细：https://data.eastmoney.com/gpzy/pledgeDetail.aspx
东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司：https://data.eastmoney.com/gpzy/distributeStatistics.aspx
东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行：https://data.eastmoney.com/gpzy/distributeStatistics.aspx
东方财富网-数据中心-特色数据-股权质押-行业数据：https://data.eastmoney.com/gpzy/industryData.aspx
"""

import math

import pandas as pd
from akshare.utils import http
from akshare.utils.tqdm import get_tqdm


def stock_gpzy_profile_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-股权质押市场概况
    https://data.eastmoney.com/gpzy/marketProfile.aspx
    :return: 股权质押市场概况
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "TRADE_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_CSDC_STATISTICS",
        "columns": "ALL",
        "quoteColumns": "",
        "source": "WEB",
        "client": "WEB",
    }
    r = http.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in range(1, total_page + 1):
        params.update({"pageNumber": page})
        r = http.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)

    big_df = big_df.rename(
        columns={
            "TRADE_DATE": "交易日期",
            "TOTAL_PLEDGED_SHARES": "质押总股数",
            "PLEDGE_MARKET_VALUE": "质押总市值",
            "CSI_300_INDEX": "沪深300指数",
            "CSI_300_CHG": "涨跌幅",
            "PM_RATIO": "A股质押总比例",
            "PLEDGE_CO_NUM": "质押公司数量",
            "DAILY_STATISTICS": "质押笔数",
        }
    )
    big_df = big_df[
        [
            "交易日期",
            "A股质押总比例",
            "质押公司数量",
            "质押笔数",
            "质押总股数",
            "质押总市值",
            "沪深300指数",
            "涨跌幅",
        ]
    ]
    big_df["交易日期"] = pd.to_datetime(big_df["交易日期"], errors="coerce").dt.date
    big_df["A股质押总比例"] = pd.to_numeric(big_df["A股质押总比例"], errors="coerce")
    big_df["质押公司数量"] = pd.to_numeric(big_df["质押公司数量"], errors="coerce")
    big_df["质押笔数"] = pd.to_numeric(big_df["质押笔数"], errors="coerce")
    big_df["质押总股数"] = pd.to_numeric(big_df["质押总股数"], errors="coerce")
    big_df["质押总市值"] = pd.to_numeric(big_df["质押总市值"], errors="coerce")
    big_df["沪深300指数"] = pd.to_numeric(big_df["沪深300指数"], errors="coerce")
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"], errors="coerce")
    big_df["A股质押总比例"] = big_df["A股质押总比例"] / 100
    big_df["A股质押总比例"] = pd.to_numeric(big_df["A股质押总比例"], errors="coerce")
    big_df = big_df.sort_values(["交易日期"])
    big_df = big_df.reset_index(drop=True)
    return big_df


def stock_gpzy_pledge_ratio_em(date: str = "20240906") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-上市公司质押比例
    https://data.eastmoney.com/gpzy/pledgeRatio.aspx
    :param date: 指定交易日，访问 https://data.eastmoney.com/gpzy/pledgeRatio.aspx 查询
    :type date: str
    :return: 上市公司质押比例
    :rtype: pandas.DataFrame
    """
    trade_date = "-".join([date[:4], date[4:6], date[6:]])
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "PLEDGE_RATIO",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_CSDC_LIST",
        "columns": "ALL",
        "quoteColumns": "",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(TRADE_DATE='{trade_date}')",
    }
    r = http.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    tqdm = get_tqdm()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = http.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)

    big_df = big_df.reset_index()
    big_df["index"] = big_df.index + 1
    big_df = big_df.rename(
        columns={
            "index": "序号",
            "SECURITY_CODE": "股票代码",
            "SECURITY_NAME_ABBR": "股票简称",
            "TRADE_DATE": "交易日期",
            "PLEDGE_RATIO": "质押比例",
            "REPURCHASE_BALANCE": "质押股数",
            "PLEDGE_DEAL_NUM": "质押笔数",
            "REPURCHASE_UNLIMITED_BALANCE": "无限售股质押数",
            "REPURCHASE_LIMITED_BALANCE": "限售股质押数",
            "PLEDGE_MARKET_CAP": "质押市值",
            "INDUSTRY": "所属行业",
            "Y1_CLOSE_ADJCHRATE": "近一年涨跌幅",
            "INDUSTRY_CODE": "所属行业代码",
        }
    )
    big_df = big_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "交易日期",
            "所属行业",
            "质押比例",
            "质押股数",
            "质押市值",
            "质押笔数",
            "无限售股质押数",
            "限售股质押数",
            "近一年涨跌幅",
            "所属行业代码",
        ]
    ]
    big_df["质押比例"] = pd.to_numeric(big_df["质押比例"], errors="coerce")
    big_df["质押股数"] = pd.to_numeric(big_df["质押股数"], errors="coerce")
    big_df["质押市值"] = pd.to_numeric(big_df["质押市值"], errors="coerce")
    big_df["质押笔数"] = pd.to_numeric(big_df["质押笔数"], errors="coerce")
    big_df["无限售股质押数"] = pd.to_numeric(big_df["无限售股质押数"], errors="coerce")
    big_df["限售股质押数"] = pd.to_numeric(big_df["限售股质押数"], errors="coerce")
    big_df["近一年涨跌幅"] = pd.to_numeric(big_df["近一年涨跌幅"], errors="coerce")
    big_df["交易日期"] = pd.to_datetime(big_df["交易日期"], errors="coerce").dt.date
    return big_df


def _get_page_num_gpzy_market_pledge_ratio_detail(filter: str = None) -> int:
    """
    东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细
    https://data.eastmoney.com/gpzy/pledgeDetail.aspx
    :return: int 获取 重要股东股权质押明细 的总页数
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "NOTICE_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPTA_APP_ACCUMDETAILS",
        "columns": "ALL",
        "quoteColumns": "",
        "source": "WEB",
        "client": "WEB",
        "filter": filter,
    }
    r = http.get(url, params=params)
    data_json = r.json()
    total_page = math.ceil(int(data_json["result"]["count"]) / 500)
    return total_page


def _stock_gpzy_pledge_ratio_detail_em(filter: str = None) -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细
    https://data.eastmoney.com/gpzy/pledgeDetail.aspx
    :return: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    total_page = _get_page_num_gpzy_market_pledge_ratio_detail(filter)
    big_df = pd.DataFrame()
    tqdm = get_tqdm()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params = {
            "sortColumns": "NOTICE_DATE",
            "sortTypes": "-1",
            "pageSize": "500",
            "pageNumber": page,
            "reportName": "RPTA_APP_ACCUMDETAILS",
            "columns": "ALL",
            "quoteColumns": "",
            "source": "WEB",
            "client": "WEB",
            "filter": filter,
        }
        r = http.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
    big_df = big_df.reset_index()
    big_df["index"] = big_df.index + 1
    big_df = big_df.rename(
        columns={
            "index": "序号",
            "SECURITY_NAME_ABBR": "股票简称",
            "SECURITY_CODE": "股票代码",
            "HOLDER_NAME": "股东名称",
            "NOTICE_DATE": "公告日期",
            "PF_ORG": "质押机构",
            "PF_NUM": "质押股份数量",
            "PF_HOLD_RATIO": "占所持股份比例",
            "PF_TSR": "占总股本比例",
            "CLOSE_FORWARD_ADJPRICE": "质押日收盘价",
            "PF_START_DATE": "质押开始日期",
            "ACTUAL_UNFREEZE_DATE": "质押结束日期",
            "UNFREEZE_STATE": "状态",
            "OPENLINE": "预估平仓线",
            "CLOSE_PRICE": "最新价",
        }
    )
    big_df = big_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "股东名称",
            "质押股份数量",
            "占所持股份比例",
            "占总股本比例",
            "质押机构",
            "最新价",
            "质押日收盘价",
            "预估平仓线",
            "质押开始日期",
            "质押结束日期",
            "状态",
            "公告日期",
        ]
    ]

    big_df["质押股份数量"] = pd.to_numeric(big_df["质押股份数量"], errors="coerce")
    big_df["占所持股份比例"] = pd.to_numeric(big_df["占所持股份比例"], errors="coerce")
    big_df["占总股本比例"] = pd.to_numeric(big_df["占总股本比例"], errors="coerce")
    big_df["最新价"] = pd.to_numeric(big_df["最新价"], errors="coerce")
    big_df["质押日收盘价"] = pd.to_numeric(big_df["质押日收盘价"], errors="coerce")
    big_df["预估平仓线"] = pd.to_numeric(big_df["预估平仓线"], errors="coerce")
    big_df["公告日期"] = pd.to_datetime(big_df["公告日期"], errors="coerce").dt.date
    big_df["质押开始日期"] = pd.to_datetime(
        big_df["质押开始日期"], errors="coerce"
    ).dt.date
    big_df["质押结束日期"] = pd.to_datetime(
        big_df["质押结束日期"], errors="coerce"
    ).dt.date
    return big_df


def stock_gpzy_pledge_ratio_detail_em() -> pd.DataFrame:
    return _stock_gpzy_pledge_ratio_detail_em()


def stock_gpzy_individual_pledge_ratio_detail_em(symbol: str) -> pd.DataFrame:
    return _stock_gpzy_pledge_ratio_detail_em(filter=f'(SECURITY_CODE="{symbol}")')


def stock_gpzy_distribute_statistics_company_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-证券公司
    https://data.eastmoney.com/gpzy/distributeStatistics.aspx
    :return: 质押机构分布统计-证券公司
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "ORG_NUM",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_GDZY_ZYJG_SUM",
        "columns": "ALL",
        "quoteColumns": "",
        "source": "WEB",
        "client": "WEB",
        # 2026-11 东方财富把机构类型由“证券”改为“证券Ⅱ”（末尾为罗马数字 Ⅱ），按旧值筛选返回空
        "filter": '(PFORG_TYPE="证券Ⅱ")',
    }
    r = http.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df = temp_df.reset_index()
    temp_df["index"] = temp_df.index + 1
    temp_df = temp_df.rename(
        columns={
            "index": "序号",
            "SECURITY_NAME_ABBR": "质押机构",
            "ORG_NUM": "质押公司数量",
            "PLEDGE_DEAL_NUM": "质押笔数",
            "PLEDGE_NUM": "质押数量",
            "WARNING_STATE_1_RATE": "未达预警线比例",
            "WARNING_STATE_2_RATE": "达到预警线未达平仓线比例",
            "WARNING_STATE_3_RATE": "达到平仓线比例",
        }
    )
    temp_df = temp_df[
        [
            "序号",
            "质押机构",
            "质押公司数量",
            "质押笔数",
            "质押数量",
            "未达预警线比例",
            "达到预警线未达平仓线比例",
            "达到平仓线比例",
        ]
    ]
    temp_df["质押公司数量"] = pd.to_numeric(temp_df["质押公司数量"], errors="coerce")
    temp_df["质押笔数"] = pd.to_numeric(temp_df["质押笔数"], errors="coerce")
    temp_df["质押数量"] = pd.to_numeric(temp_df["质押数量"], errors="coerce")
    temp_df["未达预警线比例"] = pd.to_numeric(
        temp_df["未达预警线比例"], errors="coerce"
    )
    temp_df["达到预警线未达平仓线比例"] = pd.to_numeric(
        temp_df["达到预警线未达平仓线比例"], errors="coerce"
    )
    temp_df["达到平仓线比例"] = pd.to_numeric(
        temp_df["达到平仓线比例"], errors="coerce"
    )
    return temp_df


def stock_gpzy_distribute_statistics_bank_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行
    https://data.eastmoney.com/gpzy/distributeStatistics.aspx
    :return: 质押机构分布统计-银行
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "ORG_NUM",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_GDZY_ZYJG_SUM",
        "columns": "ALL",
        "quoteColumns": "",
        "source": "WEB",
        "client": "WEB",
        # 2026-11 东方财富把机构类型由“银行”改为“银行Ⅱ”（末尾为罗马数字 Ⅱ），按旧值筛选返回空
        "filter": '(PFORG_TYPE="银行Ⅱ")',
    }
    r = http.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df = temp_df.reset_index()
    temp_df["index"] = temp_df.index + 1
    temp_df = temp_df.rename(
        columns={
            "index": "序号",
            "SECURITY_NAME_ABBR": "质押机构",
            "ORG_NUM": "质押公司数量",
            "PLEDGE_DEAL_NUM": "质押笔数",
            "PLEDGE_NUM": "质押数量",
            "WARNING_STATE_1_RATE": "未达预警线比例",
            "WARNING_STATE_2_RATE": "达到预警线未达平仓线比例",
            "WARNING_STATE_3_RATE": "达到平仓线比例",
        }
    )
    temp_df = temp_df[
        [
            "序号",
            "质押机构",
            "质押公司数量",
            "质押笔数",
            "质押数量",
            "未达预警线比例",
            "达到预警线未达平仓线比例",
            "达到平仓线比例",
        ]
    ]
    temp_df["质押公司数量"] = pd.to_numeric(temp_df["质押公司数量"], errors="coerce")
    temp_df["质押笔数"] = pd.to_numeric(temp_df["质押笔数"], errors="coerce")
    temp_df["质押数量"] = pd.to_numeric(temp_df["质押数量"], errors="coerce")
    temp_df["未达预警线比例"] = pd.to_numeric(
        temp_df["未达预警线比例"], errors="coerce"
    )
    temp_df["达到预警线未达平仓线比例"] = pd.to_numeric(
        temp_df["达到预警线未达平仓线比例"], errors="coerce"
    )
    temp_df["达到平仓线比例"] = pd.to_numeric(
        temp_df["达到平仓线比例"], errors="coerce"
    )
    return temp_df


def stock_gpzy_industry_data_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-股权质押-上市公司质押比例-行业数据
    https://data.eastmoney.com/gpzy/industryData.aspx
    :return: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "AVERAGE_PLEDGE_RATIO",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_CSDC_INDUSTRY_STATISTICS",
        "columns": "INDUSTRY_CODE,INDUSTRY,TRADE_DATE,AVERAGE_PLEDGE_RATIO,ORG_NUM,PLEDGE_TOTAL_NUM,"
        "TOTAL_PLEDGE_SHARES,PLEDGE_TOTAL_MARKETCAP",
        "quoteColumns": "",
        "source": "WEB",
        "client": "WEB",
    }
    r = http.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df = temp_df.reset_index()
    temp_df["index"] = temp_df.index + 1
    temp_df = temp_df.rename(
        columns={
            "index": "序号",
            "INDUSTRY": "行业",
            "TRADE_DATE": "统计时间",
            "AVERAGE_PLEDGE_RATIO": "平均质押比例",
            "ORG_NUM": "公司家数",
            "PLEDGE_TOTAL_NUM": "质押总笔数",
            "TOTAL_PLEDGE_SHARES": "质押总股本",
            "PLEDGE_TOTAL_MARKETCAP": "最新质押市值",
        }
    )
    temp_df = temp_df[
        [
            "序号",
            "行业",
            "平均质押比例",
            "公司家数",
            "质押总笔数",
            "质押总股本",
            "最新质押市值",
            "统计时间",
        ]
    ]
    temp_df["统计时间"] = pd.to_datetime(temp_df["统计时间"], errors="coerce").dt.date
    temp_df["平均质押比例"] = pd.to_numeric(temp_df["平均质押比例"], errors="coerce")
    temp_df["公司家数"] = pd.to_numeric(temp_df["公司家数"], errors="coerce")
    temp_df["质押总笔数"] = pd.to_numeric(temp_df["质押总笔数"], errors="coerce")
    temp_df["质押总股本"] = pd.to_numeric(temp_df["质押总股本"], errors="coerce")
    temp_df["最新质押市值"] = pd.to_numeric(temp_df["最新质押市值"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    stock_gpzy_profile_em_df = stock_gpzy_profile_em()
    print(stock_gpzy_profile_em_df)

    stock_em_gpzy_pledge_ratio_df = stock_gpzy_pledge_ratio_em(date="20241220")
    print(stock_em_gpzy_pledge_ratio_df)

    stock_gpzy_pledge_ratio_detail_em_df = stock_gpzy_pledge_ratio_detail_em()
    print(stock_gpzy_pledge_ratio_detail_em_df)

    stock_gpzy_individual_pledge_ratio_detail_em_df = (
        stock_gpzy_individual_pledge_ratio_detail_em(symbol="603132")
    )
    print(stock_gpzy_individual_pledge_ratio_detail_em_df)

    stock_em_gpzy_distribute_statistics_company_df = (
        stock_gpzy_distribute_statistics_company_em()
    )
    print(stock_em_gpzy_distribute_statistics_company_df)

    stock_em_gpzy_distribute_statistics_bank_df = (
        stock_gpzy_distribute_statistics_bank_em()
    )
    print(stock_em_gpzy_distribute_statistics_bank_df)

    stock_gpzy_industry_data_em_df = stock_gpzy_industry_data_em()
    print(stock_gpzy_industry_data_em_df)
