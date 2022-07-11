#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2020/9/10 18:02
Desc: 东方财富网-数据中心-特色数据-商誉
东方财富网-数据中心-特色数据-商誉-A股商誉市场概况: http://data.eastmoney.com/sy/scgk.html
东方财富网-数据中心-特色数据-商誉-商誉减值预期明细: http://data.eastmoney.com/sy/yqlist.html
东方财富网-数据中心-特色数据-商誉-个股商誉减值明细: http://data.eastmoney.com/sy/jzlist.html
东方财富网-数据中心-特色数据-商誉-个股商誉明细: http://data.eastmoney.com/sy/list.html
东方财富网-数据中心-特色数据-商誉-行业商誉: http://data.eastmoney.com/sy/hylist.html
"""
from akshare.utils import demjson
from py_mini_racer import py_mini_racer
import pandas as pd
import requests
from tqdm import tqdm

from akshare.stock_feature.cons import stock_em_sy_js

ctx = py_mini_racer.MiniRacer()
ctx.eval(stock_em_sy_js)

# pd.set_option('display.max_columns', 500)
# pd.set_option('display.max_rows', 500)


def stock_em_sy_profile() -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-商誉-A股商誉市场概况
    http://data.eastmoney.com/sy/scgk.html
    :return: pandas.DataFrame
    """
    url = "http://datacenter.eastmoney.com/api/data/get"
    params = {
        "type": "RPT_GOODWILL_MARKETSTATISTICS",
        "sty": "ALL",
        "p": "1",
        "ps": "50",
        "st": "REPORT_DATE",
        "sr": "-1",
        "var": "feJIrwLX",
        "filter": '(TRADE_BOARD="all")((GOODWILL_STATE="1")(|IMPAIRMENT_STATE="1"))',
        "rt": "53324344",
    }
    res = requests.get(url, params=params)
    res.encoding = "gb2312"
    data_text = res.text
    data_json = demjson.decode(
        data_text[data_text.find("{"):-1]
    )
    data_df = pd.DataFrame(data_json["result"]["data"])
    data_df.columns = [
        "_",
        "报告期",
        "商誉",
        "商誉减值",
        "净资产",
        "商誉占净资产比例",
        "商誉减值占净资产比例",
        "净利润规模",
        "商誉减值占净利润比例",
        "_",
        "_",
    ]
    data_df = data_df[
        [
            "报告期",
            "商誉",
            "商誉减值",
            "净资产",
            "商誉占净资产比例",
            "商誉减值占净资产比例",
            "净利润规模",
            "商誉减值占净利润比例",
        ]
    ]
    data_df["报告期"] = pd.to_datetime(data_df["报告期"])
    return data_df


def _get_page_num_sy_yq_list(symbol: str = "沪深两市", trade_date: str = "2019-12-31") -> int:
    """
    东方财富网-数据中心-特色数据-商誉-商誉减值预期明细
    http://data.eastmoney.com/sy/yqlist.html
    :return: int 获取 商誉减值预期明细 的总页数
    """
    symbol_dict = {
        "沪市主板": f"(MKT='shzb' and ENDDATE=^{trade_date}^)",
        "深市主板": f"(MKT='szzb' and ENDDATE=^{trade_date}^)",
        "中小板": f"(MKT='zxb' and ENDDATE=^{trade_date}^)",
        "创业板": f"(MKT='cyb' and ENDDATE=^{trade_date}^)",
        "沪深两市": f"(ENDDATE=^{trade_date}^)",
    }
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    params = {
        "type": "SY_YG",
        "token": "894050c76af8597a853f5b408b759f5d",
        "st": "NOTICEDATE",
        "sr": "-1",
        "p": "1",
        "ps": "50",
        "js": "var {name}=".format(name=ctx.call("getCode", 8))
        + "{pages:(tp),data:(x),font:(font)}",
        "filter": symbol_dict[symbol],
        "rt": "52589731",
    }
    res = requests.get(url, params=params)
    data_json = demjson.decode(res.text[res.text.find("={") + 1 :])
    return data_json["pages"]


def stock_em_sy_yq_list(symbol: str = "沪市主板", trade_date: str = "2019-12-31") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-商誉-商誉减值预期明细
    http://data.eastmoney.com/sy/yqlist.html
    :return: pandas.DataFrame
    """
    symbol_dict = {
        "沪市主板": f"(MKT='shzb' and ENDDATE=^{trade_date}^)",
        "深市主板": f"(MKT='szzb' and ENDDATE=^{trade_date}^)",
        "中小板": f"(MKT='zxb' and ENDDATE=^{trade_date}^)",
        "创业板": f"(MKT='cyb' and ENDDATE=^{trade_date}^)",
        "沪深两市": f"(ENDDATE=^{trade_date}^)",
    }
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    page_num = _get_page_num_sy_yq_list(symbol=symbol, trade_date=trade_date)
    temp_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1)):
        params = {
            "type": "SY_YG",
            "token": "894050c76af8597a853f5b408b759f5d",
            "st": "NOTICEDATE",
            "sr": "-1",
            "p": str(page),
            "ps": "50",
            "js": "var {name}=".format(name=ctx.call("getCode", 8))
            + "{pages:(tp),data:(x),font:(font)}",
            "filter": symbol_dict[symbol],
            "rt": "52589731",
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("={") + 1:])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df.columns = [
        "股票代码",
        "COMPANYCODE",
        "公司名称",
        "MKT",
        "最新一期商誉(元)",
        "公告日期",
        "REPORTDATE",
        "ENDDATE",
        "PARENTNETPROFIT",
        "预计净利润(元)-下限",
        "预计净利润(元)-上限",
        "业绩变动幅度-上限",
        "业绩变动幅度-下限",
        "预告内容",
        "业绩变动原因",
        "FORECASTTYPE",
        "上年度同期净利润(元)",
        "FORECASTINDEXCODE",
        "PERIOD",
        "HYName",
        "HYCode",
        "上年商誉",
        "商誉报告日期",
    ]
    temp_df = temp_df[
        [
            "股票代码",
            "公司名称",
            "最新一期商誉(元)",
            "公告日期",
            "预计净利润(元)-下限",
            "预计净利润(元)-上限",
            "业绩变动幅度-上限",
            "业绩变动幅度-下限",
            "预告内容",
            "业绩变动原因",
            "上年度同期净利润(元)",
            "上年商誉",
            "商誉报告日期",
        ]
    ]
    temp_df["公告日期"] = pd.to_datetime(temp_df["公告日期"])
    return temp_df


def _get_page_num_sy_jz_list(symbol: str = "沪市主板", trade_date: str = "2019-06-30") -> int:
    """
    东方财富网-数据中心-特色数据-商誉-个股商誉减值明细
    http://data.eastmoney.com/sy/jzlist.html
    :return: int 获取 个股商誉减值明细 的总页数
    """
    symbol_dict = {
        "沪市主板": f"(MKT='shzb' and REPORTDATE=^{trade_date}^)",
        "深市主板": f"(MKT='szzb' and REPORTDATE=^{trade_date}^)",
        "中小板": f"(MKT='zxb' and REPORTDATE=^{trade_date}^)",
        "创业板": f"(MKT='cyb' and REPORTDATE=^{trade_date}^)",
        "沪深两市": f"(REPORTDATE=^{trade_date}^)",
    }
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    params = {
        "type": "SY_MX",
        "token": "894050c76af8597a853f5b408b759f5d",
        "st": "GOODWILL_Change",
        "sr": "-1",
        "p": "2",
        "ps": "50",
        "js": "var {name}=".format(name=ctx.call("getCode", 8))
        + "{pages:(tp),data:(x),font:(font)}",
        "filter": symbol_dict[symbol],
        "rt": "52584576",
    }
    res = requests.get(url, params=params)
    data_json = demjson.decode(res.text[res.text.find("={") + 1 :])
    return data_json["pages"]


def stock_em_sy_jz_list(symbol: str = "沪市主板", trade_date: str = "2019-06-30") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-商誉-个股商誉减值明细
    http://data.eastmoney.com/sy/jzlist.html
    :return: pandas.DataFrame
    """
    symbol_dict = {
        "沪市主板": f"(MKT='shzb' and REPORTDATE=^{trade_date}^)",
        "深市主板": f"(MKT='szzb' and REPORTDATE=^{trade_date}^)",
        "中小板": f"(MKT='zxb' and REPORTDATE=^{trade_date}^)",
        "创业板": f"(MKT='cyb' and REPORTDATE=^{trade_date}^)",
        "沪深两市": f"(REPORTDATE=^{trade_date}^)",
    }
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    page_num = _get_page_num_sy_jz_list(symbol=symbol, trade_date=trade_date)
    temp_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1)):
        params = {
            "type": "SY_MX",
            "token": "894050c76af8597a853f5b408b759f5d",
            "st": "GOODWILL_Change",
            "sr": "-1",
            "p": str(page),
            "ps": "50",
            "js": "var {name}=".format(name=ctx.call("getCode", 8))
            + "{pages:(tp),data:(x),font:(font)}",
            "filter": symbol_dict[symbol],
            "rt": "52584576",
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df.columns = [
        "股票代码",
        "COMPANYCODE",
        "股票简称",
        "MKT",
        "REPORTTIMETYPECODE",
        "COMBINETYPECODE",
        "DATAAJUSTTYPE",
        "商誉(元)",
        "商誉减值(元)",
        "SUMSHEQUITY",
        "SUMSHEQUITY_Rate",
        "商誉减值占净资产比例(%)",
        "NOTICEDATE",
        "REPORTDATE",
        "净利润(元)",
        "商誉减值占净利润比例(%)",
        "HYName",
        "HYCode",
        "SJLTZ",
        "GOODWILL_BeforeYear",
        "公告日期",
        "ListingState",
        "MX_Type",
    ]
    temp_df = temp_df[
        [
            "股票代码",
            "股票简称",
            "商誉(元)",
            "商誉减值(元)",
            "商誉减值占净资产比例(%)",
            "净利润(元)",
            "商誉减值占净利润比例(%)",
            "公告日期",
        ]
    ]
    temp_df["公告日期"] = pd.to_datetime(temp_df["公告日期"])
    return temp_df


def _get_page_num_sy_list(symbol: str = "沪市主板", trade_date: str = "2019-12-31") -> int:
    """
    东方财富网-数据中心-特色数据-商誉-个股商誉明细
    http://data.eastmoney.com/sy/list.html
    :param symbol: choice of {"沪市主板", "深市主板", "中小板", "创业板", "沪深两市"}
    :type symbol: str
    :param trade_date: 参考网站指定的数据日期
    :type trade_date: str
    :return: 个股商誉明细 的总页数
    :rtype: int
    """
    symbol_dict = {
        "沪市主板": f"""(TRADE_BOARD="shzb")(REPORT_DATE='{trade_date}')""",
        "深市主板": f"""(TRADE_BOARD="szzb")(REPORT_DATE='{trade_date}')""",
        "中小板": f"""(TRADE_BOARD="zxb")(REPORT_DATE='{trade_date}')""",
        "创业板": f"""(TRADE_BOARD="cyb")(REPORT_DATE='{trade_date}')""",
        "沪深两市": f"(REPORT_DATE='{trade_date}')",
    }
    url = "http://datacenter.eastmoney.com/api/data/get"
    params = {
        "type": "RPT_GOODWILL_STOCKDETAILS",
        "sty": "ALL",
        "p": "1",
        "ps": "50",
        "sr": "-1,-1",
        "st": "NOTICE_DATE,SECURITY_CODE",
        "var": "QvxsKBaH",
        "filter": symbol_dict[symbol],
        "rt": "53324381",
    }
    res = requests.get(url, params=params)
    data_json = demjson.decode(res.text[res.text.find("{"):-1])
    return data_json["result"]["pages"]


def stock_em_sy_list(symbol: str = "深市主板", trade_date: str = "2019-12-31") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-商誉-个股商誉明细
    http://data.eastmoney.com/sy/list.html
    :param symbol: choice of {"沪市主板", "深市主板", "中小板", "创业板", "沪深两市"}
    :type symbol: str
    :param trade_date: 参考网站指定的数据日期
    :type trade_date: str
    :return: 个股商誉明细数据
    :rtype: pandas.DataFrame
    """
    symbol_dict = {
        "沪市主板": f"""(TRADE_BOARD="shzb")(REPORT_DATE='{trade_date}')""",
        "深市主板": f"""(TRADE_BOARD="szzb")(REPORT_DATE='{trade_date}')""",
        "中小板": f"""(TRADE_BOARD="zxb")(REPORT_DATE='{trade_date}')""",
        "创业板": f"""(TRADE_BOARD="cyb")(REPORT_DATE='{trade_date}')""",
        "沪深两市": f"(REPORT_DATE='{trade_date}')",
    }
    url = "http://datacenter.eastmoney.com/api/data/get"
    page_num = _get_page_num_sy_list(symbol=symbol, trade_date=trade_date)
    temp_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1)):
        params = {
            "type": "RPT_GOODWILL_STOCKDETAILS",
            "sty": "ALL",
            "p": str(page),
            "ps": "50",
            "sr": "-1,-1",
            "st": "NOTICE_DATE,SECURITY_CODE",
            "var": "QvxsKBaH",
            "filter": symbol_dict[symbol],
            "rt": "53324381",
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("{"): -1])
        temp_df = temp_df.append(pd.DataFrame(data_json["result"]["data"]), ignore_index=True)
    temp_df.columns = [
        "_",
        "股票代码",
        "股票简称",
        "_",
        "_",
        "_",
        "_",
        "商誉",
        "_",
        "_",
        "_",
        "公告日期",
        "报告期",
        "上年商誉",
        "_",
        "_",
        "商誉占净资产比例",
        "_",
        "净利率",
        "_",
        "净利润同比",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "股票代码",
            "股票简称",
            "商誉",
            "商誉占净资产比例",
            "净利率",
            "净利润同比",
            "上年商誉",
            "公告日期",
        ]
    ]
    temp_df["公告日期"] = pd.to_datetime(temp_df["公告日期"])
    temp_df["股票代码"] = temp_df["股票代码"].str.zfill(6)
    return temp_df


def _get_page_num_sy_hy_list(trade_date: str = "2019-09-30") -> int:
    """
    东方财富网-数据中心-特色数据-商誉-行业商誉
    http://data.eastmoney.com/sy/hylist.html
    :return: int 获取 行业商誉 的总页数
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    params = {
        "type": "HY_SY_SUM",
        "token": "894050c76af8597a853f5b408b759f5d",
        "st": "SUMSHEQUITY_Rate",
        "sr": "-1",
        "p": "1",
        "ps": "50",
        "js": "var {name}=".format(name=ctx.call("getCode", 8))
        + "{pages:(tp),data:(x),font:(font)}",
        "filter": f"(MKT='all' and REPORTDATE=^{trade_date}^)",
        "rt": "52584617",
    }
    res = requests.get(url, params=params)
    data_json = demjson.decode(res.text[res.text.find("={") + 1 :])
    return data_json["pages"]


def stock_em_sy_hy_list(trade_date: str = "2019-09-30") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-商誉-行业商誉
    http://data.eastmoney.com/sy/hylist.html
    :return: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get"
    page_num = _get_page_num_sy_hy_list(trade_date=trade_date)
    temp_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1)):
        params = {
            "type": "HY_SY_SUM",
            "token": "894050c76af8597a853f5b408b759f5d",
            "st": "SUMSHEQUITY_Rate",
            "sr": "-1",
            "p": str(page),
            "ps": "50",
            "js": "var {name}=".format(name=ctx.call("getCode", 8))
            + "{pages:(tp),data:(x),font:(font)}",
            "filter": f"(MKT='all' and REPORTDATE=^{trade_date}^)",
            "rt": "52584617",
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("={") + 1 :])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df.columns = [
        "行业名称",
        "HYCode",
        "MKT",
        "公司家数",
        "商誉规模(元)",
        "GOODWILL_Change",
        "净资产(元)",
        "商誉规模占净资产规模比例(%)",
        "SUMSHEQUITY_Change_Rate",
        "REPORTDATE",
        "净利润规模(元)",
        "PARENTNETPROFIT_Change_Rate",
        "SygmType",
        "SyztType",
    ]
    temp_df = temp_df[
        ["行业名称", "公司家数", "商誉规模(元)", "净资产(元)", "商誉规模占净资产规模比例(%)", "净利润规模(元)"]
    ]
    return temp_df


if __name__ == "__main__":
    stock_em_sy_profile_df = stock_em_sy_profile()
    print(stock_em_sy_profile_df)
    stock_em_sy_yq_list_df = stock_em_sy_yq_list(symbol="沪市主板", trade_date="2019-12-31")
    print(stock_em_sy_yq_list_df)
    stock_em_sy_jz_list_df = stock_em_sy_jz_list(symbol="沪市主板", trade_date="2019-12-31")
    print(stock_em_sy_jz_list_df)
    stock_em_sy_list_df = stock_em_sy_list(symbol="沪深两市", trade_date="2019-12-31")
    print(stock_em_sy_list_df)
    stock_em_sy_hy_list_df = stock_em_sy_hy_list(trade_date="2019-12-31")
    print(stock_em_sy_hy_list_df)
