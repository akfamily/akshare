# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/7/15 22:00
Desc: 东方财富网-数据中心-股东分析
https://data.eastmoney.com/gdfx/
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_gdfx_free_holding_statistics_em(
    date: str = "20210630",
) -> pd.DataFrame:
    """
    东方财富网-数据中心-股东分析-股东持股统计-十大流通股东
    https://data.eastmoney.com/gdfx/HoldingAnalyse.html
    :param date: 报告期
    :type date: str
    :return: 十大流通股东
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "STATISTICS_TIMES,COOPERATION_HOLDER_MARK",
        "sortTypes": "-1,-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_COOPFREEHOLDERS_ANALYSIS",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"""(HOLDNUM_CHANGE_TYPE="001")(END_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')""",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "-",
        "股东名称",
        "股东类型",
        "-",
        "统计次数",
        "公告日后涨幅统计-10个交易日-平均涨幅",
        "公告日后涨幅统计-10个交易日-最大涨幅",
        "公告日后涨幅统计-10个交易日-最小涨幅",
        "公告日后涨幅统计-30个交易日-平均涨幅",
        "公告日后涨幅统计-30个交易日-最大涨幅",
        "公告日后涨幅统计-30个交易日-最小涨幅",
        "公告日后涨幅统计-60个交易日-平均涨幅",
        "公告日后涨幅统计-60个交易日-最大涨幅",
        "公告日后涨幅统计-60个交易日-最小涨幅",
        "持有个股",
    ]
    big_df = big_df[
        [
            "序号",
            "股东名称",
            "股东类型",
            "统计次数",
            "公告日后涨幅统计-10个交易日-平均涨幅",
            "公告日后涨幅统计-10个交易日-最大涨幅",
            "公告日后涨幅统计-10个交易日-最小涨幅",
            "公告日后涨幅统计-30个交易日-平均涨幅",
            "公告日后涨幅统计-30个交易日-最大涨幅",
            "公告日后涨幅统计-30个交易日-最小涨幅",
            "公告日后涨幅统计-60个交易日-平均涨幅",
            "公告日后涨幅统计-60个交易日-最大涨幅",
            "公告日后涨幅统计-60个交易日-最小涨幅",
            "持有个股",
        ]
    ]
    big_df["统计次数"] = pd.to_numeric(big_df["统计次数"])
    big_df["公告日后涨幅统计-10个交易日-平均涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-10个交易日-平均涨幅"]
    )
    big_df["公告日后涨幅统计-10个交易日-最大涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-10个交易日-最大涨幅"]
    )
    big_df["公告日后涨幅统计-10个交易日-最小涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-10个交易日-最小涨幅"]
    )
    big_df["公告日后涨幅统计-30个交易日-平均涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-30个交易日-平均涨幅"]
    )
    big_df["公告日后涨幅统计-30个交易日-最大涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-30个交易日-最大涨幅"]
    )
    big_df["公告日后涨幅统计-30个交易日-最小涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-30个交易日-最小涨幅"]
    )
    big_df["公告日后涨幅统计-60个交易日-平均涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-60个交易日-平均涨幅"]
    )
    big_df["公告日后涨幅统计-60个交易日-最大涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-60个交易日-最大涨幅"]
    )
    big_df["公告日后涨幅统计-60个交易日-最小涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-60个交易日-最小涨幅"]
    )
    return big_df


def stock_gdfx_holding_statistics_em(date: str = "20210930") -> pd.DataFrame:
    """
    东方财富网-数据中心-股东分析-股东持股统计-十大股东
    https://data.eastmoney.com/gdfx/HoldingAnalyse.html
    :param date: 报告期
    :type date: str
    :return: 十大股东
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "STATISTICS_TIMES,COOPERATION_HOLDER_MARK",
        "sortTypes": "-1,-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_COOPHOLDERS_ANALYSIS",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"""(HOLDNUM_CHANGE_TYPE="001")(END_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')""",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "-",
        "股东名称",
        "股东类型",
        "-",
        "统计次数",
        "公告日后涨幅统计-10个交易日-平均涨幅",
        "公告日后涨幅统计-10个交易日-最大涨幅",
        "公告日后涨幅统计-10个交易日-最小涨幅",
        "公告日后涨幅统计-30个交易日-平均涨幅",
        "公告日后涨幅统计-30个交易日-最大涨幅",
        "公告日后涨幅统计-30个交易日-最小涨幅",
        "公告日后涨幅统计-60个交易日-平均涨幅",
        "公告日后涨幅统计-60个交易日-最大涨幅",
        "公告日后涨幅统计-60个交易日-最小涨幅",
        "持有个股",
    ]
    big_df = big_df[
        [
            "序号",
            "股东名称",
            "股东类型",
            "统计次数",
            "公告日后涨幅统计-10个交易日-平均涨幅",
            "公告日后涨幅统计-10个交易日-最大涨幅",
            "公告日后涨幅统计-10个交易日-最小涨幅",
            "公告日后涨幅统计-30个交易日-平均涨幅",
            "公告日后涨幅统计-30个交易日-最大涨幅",
            "公告日后涨幅统计-30个交易日-最小涨幅",
            "公告日后涨幅统计-60个交易日-平均涨幅",
            "公告日后涨幅统计-60个交易日-最大涨幅",
            "公告日后涨幅统计-60个交易日-最小涨幅",
            "持有个股",
        ]
    ]
    big_df["统计次数"] = pd.to_numeric(big_df["统计次数"])
    big_df["公告日后涨幅统计-10个交易日-平均涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-10个交易日-平均涨幅"]
    )
    big_df["公告日后涨幅统计-10个交易日-最大涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-10个交易日-最大涨幅"]
    )
    big_df["公告日后涨幅统计-10个交易日-最小涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-10个交易日-最小涨幅"]
    )
    big_df["公告日后涨幅统计-30个交易日-平均涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-30个交易日-平均涨幅"]
    )
    big_df["公告日后涨幅统计-30个交易日-最大涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-30个交易日-最大涨幅"]
    )
    big_df["公告日后涨幅统计-30个交易日-最小涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-30个交易日-最小涨幅"]
    )
    big_df["公告日后涨幅统计-60个交易日-平均涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-60个交易日-平均涨幅"]
    )
    big_df["公告日后涨幅统计-60个交易日-最大涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-60个交易日-最大涨幅"]
    )
    big_df["公告日后涨幅统计-60个交易日-最小涨幅"] = pd.to_numeric(
        big_df["公告日后涨幅统计-60个交易日-最小涨幅"]
    )
    return big_df


def stock_gdfx_free_holding_change_em(date: str = "20210930") -> pd.DataFrame:
    """
    东方财富网-数据中心-股东分析-股东持股变动统计-十大流通股东
    https://data.eastmoney.com/gdfx/HoldingAnalyse.html
    :param date: 报告期
    :type date: str
    :return: 十大流通股东
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "HOLDER_NUM,HOLDER_NEW",
        "sortTypes": "-1,-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_FREEHOLDERS_BASIC_INFO",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(END_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "-",
        "股东名称",
        "-",
        "股东类型",
        "-",
        "-",
        "-",
        "期末持股只数统计-总持有",
        "期末持股只数统计-新进",
        "期末持股只数统计-增加",
        "期末持股只数统计-减少",
        "期末持股只数统计-不变",
        "-",
        "流通市值统计",
        "持有个股",
        "-",
    ]
    big_df = big_df[
        [
            "序号",
            "股东名称",
            "股东类型",
            "期末持股只数统计-总持有",
            "期末持股只数统计-新进",
            "期末持股只数统计-增加",
            "期末持股只数统计-不变",
            "期末持股只数统计-减少",
            "流通市值统计",
            "持有个股",
        ]
    ]
    big_df["期末持股只数统计-总持有"] = pd.to_numeric(big_df["期末持股只数统计-总持有"])
    big_df["期末持股只数统计-新进"] = pd.to_numeric(big_df["期末持股只数统计-新进"])
    big_df["期末持股只数统计-增加"] = pd.to_numeric(big_df["期末持股只数统计-增加"])
    big_df["期末持股只数统计-不变"] = pd.to_numeric(big_df["期末持股只数统计-不变"])
    big_df["期末持股只数统计-减少"] = pd.to_numeric(big_df["期末持股只数统计-减少"])
    big_df["流通市值统计"] = pd.to_numeric(big_df["流通市值统计"])
    return big_df


def stock_gdfx_holding_change_em(date: str = "20210930") -> pd.DataFrame:
    """
    东方财富网-数据中心-股东分析-股东持股变动统计-十大股东
    https://data.eastmoney.com/gdfx/HoldingAnalyse.html
    :param date: 报告期
    :type date: str
    :return: 十大流通股东
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "HOLDER_NUM,HOLDER_NEW",
        "sortTypes": "-1,-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_HOLDERS_BASIC_INFO",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(END_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "-",
        "股东名称",
        "-",
        "股东类型",
        "-",
        "-",
        "-",
        "期末持股只数统计-总持有",
        "期末持股只数统计-新进",
        "期末持股只数统计-增加",
        "期末持股只数统计-减少",
        "期末持股只数统计-不变",
        "-",
        "-",
        "持有个股",
        "流通市值统计",
    ]
    big_df = big_df[
        [
            "序号",
            "股东名称",
            "股东类型",
            "期末持股只数统计-总持有",
            "期末持股只数统计-新进",
            "期末持股只数统计-增加",
            "期末持股只数统计-不变",
            "期末持股只数统计-减少",
            "流通市值统计",
            "持有个股",
        ]
    ]
    big_df["期末持股只数统计-总持有"] = pd.to_numeric(big_df["期末持股只数统计-总持有"])
    big_df["期末持股只数统计-新进"] = pd.to_numeric(big_df["期末持股只数统计-新进"])
    big_df["期末持股只数统计-增加"] = pd.to_numeric(big_df["期末持股只数统计-增加"])
    big_df["期末持股只数统计-不变"] = pd.to_numeric(big_df["期末持股只数统计-不变"])
    big_df["期末持股只数统计-减少"] = pd.to_numeric(big_df["期末持股只数统计-减少"])
    big_df["流通市值统计"] = pd.to_numeric(big_df["流通市值统计"])
    return big_df


def stock_gdfx_free_top_10_em(
    symbol: str = "sh688686", date: str = "20210630"
) -> pd.DataFrame:
    """
    东方财富网-个股-十大流通股东
    https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/Index?type=web&code=SH688686#sdltgd-0
    :param symbol: 带市场标识的股票代码
    :type symbol: str
    :param date: 报告期
    :type date: str
    :return: 十大股东
    :rtype: pandas.DataFrame
    """
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/PageSDLTGD"
    params = {
        "code": f"{symbol.upper()}",
        "date": f"{'-'.join([date[:4], date[4:6], date[6:]])}",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["sdltgd"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "名次",
        "-",
        "-",
        "-",
        "-",
        "股东名称",
        "股东性质",
        "股份类型",
        "持股数",
        "占总流通股本持股比例",
        "增减",
        "变动比率",
    ]
    temp_df = temp_df[
        [
            "名次",
            "股东名称",
            "股东性质",
            "股份类型",
            "持股数",
            "占总流通股本持股比例",
            "增减",
            "变动比率",
        ]
    ]
    temp_df["持股数"] = pd.to_numeric(temp_df["持股数"])
    temp_df["占总流通股本持股比例"] = pd.to_numeric(temp_df["占总流通股本持股比例"])
    temp_df["变动比率"] = pd.to_numeric(temp_df["变动比率"])
    return temp_df


def stock_gdfx_top_10_em(
    symbol: str = "sh688686", date: str = "20210630"
) -> pd.DataFrame:
    """
    东方财富网-个股-十大股东
    https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/Index?type=web&code=SH688686#sdgd-0
    :param symbol: 带市场标识的股票代码
    :type symbol: str
    :param date: 报告期
    :type date: str
    :return: 十大股东
    :rtype: pandas.DataFrame
    """
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/PageSDGD"
    params = {
        "code": f"{symbol.upper()}",
        "date": f"{'-'.join([date[:4], date[4:6], date[6:]])}",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["sdgd"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "名次",
        "-",
        "-",
        "-",
        "-",
        "股东名称",
        "股份类型",
        "持股数",
        "占总股本持股比例",
        "增减",
        "变动比率",
    ]
    temp_df = temp_df[
        [
            "名次",
            "股东名称",
            "股份类型",
            "持股数",
            "占总股本持股比例",
            "增减",
            "变动比率",
        ]
    ]
    temp_df["持股数"] = pd.to_numeric(temp_df["持股数"])
    temp_df["占总股本持股比例"] = pd.to_numeric(temp_df["占总股本持股比例"])
    temp_df["变动比率"] = pd.to_numeric(temp_df["变动比率"])
    return temp_df


def stock_gdfx_free_holding_detail_em(date: str = "20210930") -> pd.DataFrame:
    """
    东方财富网-数据中心-股东分析-股东持股明细-十大流通股东
    https://data.eastmoney.com/gdfx/HoldingAnalyse.html
    :param date: 报告期
    :type date: str
    :return: 十大流通股东
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "UPDATE_DATE,SECURITY_CODE,HOLDER_RANK",
        "sortTypes": "-1,1,1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_F10_EH_FREEHOLDERS",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(END_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "股票代码",
        "-",
        "报告期",
        "股东名称",
        "期末持股-数量",
        "-",
        "期末持股-持股变动",
        "-",
        "-",
        "-",
        "股票简称",
        "-",
        "-",
        "-",
        "期末持股-流通市值",
        "-",
        "-",
        "期末持股-数量变化比例",
        "股东类型",
        "-",
        "公告日",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "期末持股-数量变化",
        "-",
    ]
    big_df = big_df[
        [
            "序号",
            "股东名称",
            "股东类型",
            "股票代码",
            "股票简称",
            "报告期",
            "期末持股-数量",
            "期末持股-数量变化",
            "期末持股-数量变化比例",
            "期末持股-持股变动",
            "期末持股-流通市值",
            "公告日",
        ]
    ]
    big_df["报告期"] = pd.to_datetime(big_df["报告期"]).dt.date
    big_df["公告日"] = pd.to_datetime(big_df["公告日"]).dt.date
    big_df["期末持股-数量"] = pd.to_numeric(big_df["期末持股-数量"])
    big_df["期末持股-数量变化"] = pd.to_numeric(big_df["期末持股-数量变化"])
    big_df["期末持股-数量变化比例"] = pd.to_numeric(big_df["期末持股-数量变化比例"])
    big_df["期末持股-流通市值"] = pd.to_numeric(big_df["期末持股-流通市值"])
    return big_df


def stock_gdfx_holding_detail_em(date: str = "20210930") -> pd.DataFrame:
    """
    东方财富网-数据中心-股东分析-股东持股明细-十大股东
    https://data.eastmoney.com/gdfx/HoldingAnalyse.html
    :param date: 报告期
    :type date: str
    :return: 十大股东
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "NOTICE_DATE,SECURITY_CODE,RANK",
        "sortTypes": "-1,1,1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_DMSK_HOLDERS",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(END_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "股票代码",
        "-",
        "-",
        "报告期",
        "股东排名",
        "-",
        "股东名称",
        "期末持股-数量",
        "期末持股-持股占流通股比",
        "期末持股-数量变化",
        "期末持股-数量变化比例",
        "-",
        "-",
        "-",
        "-",
        "-",
        "公告日",
        "期末持股-流通市值",
        "-",
        "-",
        "股票简称",
        "-",
        "-",
        "-",
        "期末持股-持股变动",
        "-",
        "股东类型",
        "-",
        "-",
    ]
    big_df = big_df[
        [
            "序号",
            "股东名称",
            "股东类型",
            "股东排名",
            "股票代码",
            "股票简称",
            "报告期",
            "期末持股-数量",
            "期末持股-持股占流通股比",
            "期末持股-数量变化",
            "期末持股-数量变化比例",
            "期末持股-持股变动",
            "期末持股-流通市值",
            "公告日",
        ]
    ]
    big_df["报告期"] = pd.to_datetime(big_df["报告期"]).dt.date
    big_df["公告日"] = pd.to_datetime(big_df["公告日"]).dt.date
    big_df["期末持股-数量"] = pd.to_numeric(big_df["期末持股-数量"])
    big_df["期末持股-持股占流通股比"] = pd.to_numeric(big_df["期末持股-持股占流通股比"])
    big_df["期末持股-数量变化"] = pd.to_numeric(big_df["期末持股-数量变化"])
    big_df["期末持股-数量变化比例"] = pd.to_numeric(big_df["期末持股-数量变化比例"])
    big_df["期末持股-流通市值"] = pd.to_numeric(big_df["期末持股-流通市值"])
    return big_df


def stock_gdfx_free_holding_analyse_em(date: str = "20210930") -> pd.DataFrame:
    """
    东方财富网-数据中心-股东分析-股东持股分析-十大流通股东
    https://data.eastmoney.com/gdfx/HoldingAnalyse.html
    :param date: 报告期
    :type date: str
    :return: 十大流通股东
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "UPDATE_DATE,SECURITY_CODE,HOLDER_RANK",
        "sortTypes": "-1,1,1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_CUSTOM_F10_EH_FREEHOLDERS_JOIN_FREEHOLDER_SHAREANALYSIS",
        "columns": "ALL;D10_ADJCHRATE,D30_ADJCHRATE,D60_ADJCHRATE",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(END_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "股票代码",
        "-",
        "-",
        "股东名称",
        "期末持股-数量",
        "-",
        "-",
        "-",
        "-",
        "-",
        "股票简称",
        "-",
        "-",
        "-",
        "期末持股-流通市值",
        "-",
        "-",
        "期末持股-数量变化比例",
        "股东类型",
        "-",
        "公告日",
        "报告期",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "期末持股-持股变动",
        "-",
        "-",
        "-",
        "-",
        "期末持股-数量变化",
        "-",
        "公告日后涨跌幅-10个交易日",
        "公告日后涨跌幅-30个交易日",
        "公告日后涨跌幅-60个交易日",
    ]
    big_df = big_df[
        [
            "序号",
            "股东名称",
            "股东类型",
            "股票代码",
            "股票简称",
            "报告期",
            "期末持股-数量",
            "期末持股-数量变化",
            "期末持股-数量变化比例",
            "期末持股-持股变动",
            "期末持股-流通市值",
            "公告日",
            "公告日后涨跌幅-10个交易日",
            "公告日后涨跌幅-30个交易日",
            "公告日后涨跌幅-60个交易日",
        ]
    ]
    big_df["公告日"] = pd.to_datetime(big_df["公告日"]).dt.date
    big_df["期末持股-数量"] = pd.to_numeric(big_df["期末持股-数量"])
    big_df["期末持股-数量变化"] = pd.to_numeric(big_df["期末持股-数量变化"])
    big_df["期末持股-数量变化比例"] = pd.to_numeric(big_df["期末持股-数量变化比例"])
    big_df["期末持股-流通市值"] = pd.to_numeric(big_df["期末持股-流通市值"])
    big_df["公告日后涨跌幅-10个交易日"] = pd.to_numeric(big_df["公告日后涨跌幅-10个交易日"])
    big_df["公告日后涨跌幅-30个交易日"] = pd.to_numeric(big_df["公告日后涨跌幅-30个交易日"])
    big_df["公告日后涨跌幅-60个交易日"] = pd.to_numeric(big_df["公告日后涨跌幅-60个交易日"])
    return big_df


def stock_gdfx_holding_analyse_em(date: str = "20220331") -> pd.DataFrame:
    """
    东方财富网-数据中心-股东分析-股东持股分析-十大股东
    https://data.eastmoney.com/gdfx/HoldingAnalyse.html
    :param date: 报告期
    :type date: str
    :return: 十大股东
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "NOTICE_DATE,SECURITY_CODE,RANK",
        "sortTypes": "-1,1,1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_CUSTOM_DMSK_HOLDERS_JOIN_HOLDER_SHAREANALYSIS",
        "columns": "ALL;D10_ADJCHRATE,D30_ADJCHRATE,D60_ADJCHRATE",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(END_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "股票代码",
        "-",
        "-",
        "报告期",
        "-",
        "-",
        "股东名称",
        "期末持股-数量",
        "-",
        "期末持股-数量变化",
        "期末持股-数量变化比例",
        "-",
        "-",
        "股东类型",
        "-",
        "-",
        "公告日",
        "-",
        "-",
        "-",
        "股票简称",
        "-",
        "-",
        "期末持股-持股变动",
        "期末持股-流通市值",
        "-",
        "-",
        "-",
        "-",
        "公告日后涨跌幅-10个交易日",
        "公告日后涨跌幅-30个交易日",
        "公告日后涨跌幅-60个交易日",
    ]
    big_df = big_df[
        [
            "序号",
            "股东名称",
            "股东类型",
            "股票代码",
            "股票简称",
            "报告期",
            "期末持股-数量",
            "期末持股-数量变化",
            "期末持股-数量变化比例",
            "期末持股-持股变动",
            "期末持股-流通市值",
            "公告日",
            "公告日后涨跌幅-10个交易日",
            "公告日后涨跌幅-30个交易日",
            "公告日后涨跌幅-60个交易日",
        ]
    ]
    big_df["公告日"] = pd.to_datetime(big_df["公告日"]).dt.date
    big_df["报告期"] = pd.to_datetime(big_df["报告期"]).dt.date
    big_df["期末持股-数量"] = pd.to_numeric(big_df["期末持股-数量"])
    big_df["期末持股-数量变化"] = pd.to_numeric(big_df["期末持股-数量变化"])
    big_df["期末持股-数量变化比例"] = pd.to_numeric(big_df["期末持股-数量变化比例"])
    big_df["期末持股-流通市值"] = pd.to_numeric(big_df["期末持股-流通市值"])
    big_df["公告日后涨跌幅-10个交易日"] = pd.to_numeric(big_df["公告日后涨跌幅-10个交易日"])
    big_df["公告日后涨跌幅-30个交易日"] = pd.to_numeric(big_df["公告日后涨跌幅-30个交易日"])
    big_df["公告日后涨跌幅-60个交易日"] = pd.to_numeric(big_df["公告日后涨跌幅-60个交易日"])
    return big_df


def stock_gdfx_free_holding_teamwork_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-股东分析-股东协同-十大流通股东
    https://data.eastmoney.com/gdfx/HoldingAnalyse.html
    :return: 十大流通股东
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "COOPERAT_NUM,HOLDER_NEW,COOPERAT_HOLDER_NEW",
        "sortTypes": "-1,-1,-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_COOPFREEHOLDER",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "股东名称",
        "股东类型",
        "-",
        "协同股东名称",
        "协同股东类型",
        "协同次数",
        "个股详情",
    ]
    big_df = big_df[
        [
            "序号",
            "股东名称",
            "股东类型",
            "协同股东名称",
            "协同股东类型",
            "协同次数",
            "个股详情",
        ]
    ]
    big_df["协同次数"] = pd.to_numeric(big_df["协同次数"])
    return big_df


def stock_gdfx_holding_teamwork_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-股东分析-股东协同-十大股东
    https://data.eastmoney.com/gdfx/HoldingAnalyse.html
    :return: 十大股东
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "COOPERAT_NUM,HOLDER_NEW,COOPERAT_HOLDER_NEW",
        "sortTypes": "-1,-1,-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_TENHOLDERS_COOPHOLDERS",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号",
        "-",
        "股东名称",
        "股东类型",
        "-",
        "协同股东名称",
        "协同股东类型",
        "协同次数",
        "个股详情",
    ]
    big_df = big_df[
        [
            "序号",
            "股东名称",
            "股东类型",
            "协同股东名称",
            "协同股东类型",
            "协同次数",
            "个股详情",
        ]
    ]
    big_df["协同次数"] = pd.to_numeric(big_df["协同次数"])
    return big_df


if __name__ == "__main__":
    stock_gdfx_free_holding_statistics_em_df = (
        stock_gdfx_free_holding_statistics_em(date="20210930")
    )
    print(stock_gdfx_free_holding_statistics_em_df)

    stock_gdfx_holding_statistics_em_df = stock_gdfx_holding_statistics_em(
        date="20210930"
    )
    print(stock_gdfx_holding_statistics_em_df)

    stock_gdfx_free_holding_change_em_df = stock_gdfx_free_holding_change_em(
        date="20210930"
    )
    print(stock_gdfx_free_holding_change_em_df)

    stock_gdfx_holding_change_em_df = stock_gdfx_holding_change_em(
        date="20210930"
    )
    print(stock_gdfx_holding_change_em_df)

    stock_gdfx_free_top_10_em_df = stock_gdfx_free_top_10_em(
        symbol="sz000420", date="20220331"
    )
    print(stock_gdfx_free_top_10_em_df)

    stock_gdfx_top_10_em_df = stock_gdfx_top_10_em(
        symbol="sh688686", date="20210630"
    )
    print(stock_gdfx_top_10_em_df)

    stock_gdfx_free_holding_detail_em_df = stock_gdfx_free_holding_detail_em(
        date="20210930"
    )
    print(stock_gdfx_free_holding_detail_em_df)

    stock_gdfx_holding_detail_em_df = stock_gdfx_holding_detail_em(
        date="20210930"
    )
    print(stock_gdfx_holding_detail_em_df)

    stock_gdfx_free_holding_analyse_em_df = stock_gdfx_free_holding_analyse_em(
        date="20220331"
    )
    print(stock_gdfx_free_holding_analyse_em_df)

    stock_gdfx_holding_analyse_em_df = stock_gdfx_holding_analyse_em(
        date="20220331"
    )
    print(stock_gdfx_holding_analyse_em_df)

    stock_gdfx_free_holding_teamwork_em_df = (
        stock_gdfx_free_holding_teamwork_em()
    )
    print(stock_gdfx_free_holding_teamwork_em_df)

    stock_gdfx_holding_teamwork_em_df = stock_gdfx_holding_teamwork_em()
    print(stock_gdfx_holding_teamwork_em_df)
