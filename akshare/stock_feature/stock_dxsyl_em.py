#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/11/21 23:40
Desc: 东方财富网-数据中心-新股数据-打新收益率
东方财富网-数据中心-新股申购-打新收益率
https://data.eastmoney.com/xg/xg/dxsyl.html
东方财富网-数据中心-新股数据-新股申购与中签查询
http://data.eastmoney.com/xg/xg/default_2.html
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_dxsyl_em() -> pd.DataFrame:
    """
    东方财富网-数据中心-新股申购-打新收益率
    https://data.eastmoney.com/xg/xg/dxsyl.html
    :return: 打新收益率数据
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "LISTING_DATE,SECURITY_CODE",
        "sortTypes": "-1,-1",
        "pageSize": "5000",
        "pageNumber": "1",
        "reportName": "RPTA_APP_IPOAPPLY",
        "quoteColumns": "f2~01~SECURITY_CODE,f14~01~SECURITY_CODE",
        "quoteType": "0",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": """((APPLY_DATE>'2010-01-01')(|@APPLY_DATE="NULL"))((LISTING_DATE>'2010-01-01')(|@LISTING_DATE="NULL"))(TRADE_MARKET_CODE!="069001017")""",
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
    big_df.rename(
        columns={
            "index": "序号",
            "SECURITY_CODE": "股票代码",
            "f14": "股票简称",
            "ISSUE_PRICE": "发行价",
            "LATELY_PRICE": "最新价",
            "ONLINE_ISSUE_LWR": "网上-发行中签率",
            "ONLINE_VA_SHARES": "网上-有效申购股数",
            "ONLINE_VA_NUM": "网上-有效申购户数",
            "ONLINE_ES_MULTIPLE": "网上-超额认购倍数",
            "OFFLINE_VAP_RATIO": "网下-配售中签率",
            "OFFLINE_VATS": "网下-有效申购股数",
            "OFFLINE_VAP_OBJECT": "网下-有效申购户数",
            "OFFLINE_VAS_MULTIPLE": "网下-配售认购倍数",
            "ISSUE_NUM": "总发行数量",
            "LD_OPEN_PREMIUM": "开盘溢价",
            "LD_CLOSE_CHANGE": "首日涨幅",
            "LISTING_DATE": "上市日期",
        },
        inplace=True,
    )
    big_df = big_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "发行价",
            "最新价",
            "网上-发行中签率",
            "网上-有效申购股数",
            "网上-有效申购户数",
            "网上-超额认购倍数",
            "网下-配售中签率",
            "网下-有效申购股数",
            "网下-有效申购户数",
            "网下-配售认购倍数",
            "总发行数量",
            "开盘溢价",
            "首日涨幅",
            "上市日期",
        ]
    ]
    big_df["发行价"] = pd.to_numeric(big_df["发行价"], errors="coerce")
    big_df["最新价"] = pd.to_numeric(big_df["最新价"], errors="coerce")
    big_df["网上-发行中签率"] = pd.to_numeric(big_df["网上-发行中签率"], errors="coerce")
    big_df["网上-有效申购股数"] = pd.to_numeric(big_df["网上-有效申购股数"], errors="coerce")
    big_df["网上-有效申购户数"] = pd.to_numeric(big_df["网上-有效申购户数"], errors="coerce")
    big_df["网上-超额认购倍数"] = pd.to_numeric(big_df["网上-超额认购倍数"], errors="coerce")
    big_df["网下-配售中签率"] = pd.to_numeric(big_df["网下-配售中签率"], errors="coerce")
    big_df["网下-有效申购股数"] = pd.to_numeric(big_df["网下-有效申购股数"], errors="coerce")
    big_df["网下-有效申购户数"] = pd.to_numeric(big_df["网下-有效申购户数"], errors="coerce")
    big_df["网下-配售认购倍数"] = pd.to_numeric(big_df["网下-配售认购倍数"], errors="coerce")
    big_df["总发行数量"] = pd.to_numeric(big_df["总发行数量"], errors="coerce")
    big_df["开盘溢价"] = pd.to_numeric(big_df["开盘溢价"], errors="coerce")
    big_df["首日涨幅"] = pd.to_numeric(big_df["首日涨幅"], errors="coerce")
    big_df["上市日期"] = pd.to_datetime(big_df["上市日期"]).dt.date
    return big_df


def stock_xgsglb_em(symbol: str = "京市A股") -> pd.DataFrame:
    """
    新股申购与中签查询
    http://data.eastmoney.com/xg/xg/default_2.html
    :param symbol: choice of {"全部股票", "沪市A股", "科创板", "深市A股", "创业板", "京市A股"}
    :type symbol: str
    :return: 新股申购与中签数据
    :rtype: pandas.DataFrame
    """
    market_map = {
        "全部股票": """(APPLY_DATE>'2010-01-01')""",
        "沪市A股": """(APPLY_DATE>'2010-01-01')(SECURITY_TYPE_CODE in ("058001001","058001008"))(TRADE_MARKET_CODE in ("069001001001","069001001003","069001001006"))""",
        "科创板": """(APPLY_DATE>'2010-01-01')(SECURITY_TYPE_CODE in ("058001001","058001008"))(TRADE_MARKET_CODE="069001001006")""",
        "深市A股": """(APPLY_DATE>'2010-01-01')(SECURITY_TYPE_CODE="058001001")(TRADE_MARKET_CODE in ("069001002001","069001002002","069001002003","069001002005"))""",
        "创业板": """(APPLY_DATE>'2010-01-01')(SECURITY_TYPE_CODE="058001001")(TRADE_MARKET_CODE="069001002002")""",
    }
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    if symbol == "京市A股":
        params = {
            "sortColumns": "APPLY_DATE",
            "sortTypes": "-1",
            "pageSize": "500",
            "pageNumber": "1",
            "columns": "ALL",
            "reportName": "RPT_NEEQ_ISSUEINFO_LIST",
            "quoteColumns": "f14~01~SECURITY_CODE~SECURITY_NAME_ABBR",
            "source": "NEEQSELECT",
            "client": "WEB",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        total_page = data_json["result"]["pages"]
        big_df = pd.DataFrame()
        for page in tqdm(range(1, 1 + int(total_page)), leave=False):
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
            "代码",
            "-",
            "简称",
            "申购代码",
            "发行总数",
            "-",
            "发行价格",
            "发行市盈率",
            "申购日",
            "发行结果公告日",
            "上市日",
            "网上发行数量",
            "顶格申购所需资金",
            "申购上限",
            "网上申购缴款日",
            "网上申购退款日",
            "-",
            "网上获配比例",
            "最新价",
            "首日收盘价",
            "网下有效申购倍数",
            "每百股获利",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
        ]
        big_df = big_df[
            [
                "序号",
                "代码",
                "简称",
                "申购代码",
                "发行总数",
                "网上发行数量",
                "顶格申购所需资金",
                "申购上限",
                "发行价格",
                "最新价",
                "首日收盘价",
                "申购日",
                "网上申购缴款日",
                "网上申购退款日",
                "上市日",
                "发行结果公告日",
                "发行市盈率",
                "网上获配比例",
                "网下有效申购倍数",
                "每百股获利",
            ]
        ]
        big_df["发行总数"] = pd.to_numeric(big_df["发行总数"])
        big_df["网上发行数量"] = pd.to_numeric(big_df["网上发行数量"])
        big_df["顶格申购所需资金"] = pd.to_numeric(big_df["顶格申购所需资金"])
        big_df["申购上限"] = pd.to_numeric(big_df["申购上限"])
        big_df["发行价格"] = pd.to_numeric(big_df["发行价格"])
        big_df["最新价"] = pd.to_numeric(big_df["最新价"])
        big_df["首日收盘价"] = pd.to_numeric(big_df["首日收盘价"])
        big_df["发行市盈率"] = pd.to_numeric(big_df["发行市盈率"])
        big_df["网上获配比例"] = pd.to_numeric(big_df["网上获配比例"])
        big_df["网下有效申购倍数"] = pd.to_numeric(big_df["网下有效申购倍数"])
        big_df["每百股获利"] = pd.to_numeric(big_df["每百股获利"])

        big_df["申购日"] = pd.to_datetime(big_df["申购日"]).dt.date
        big_df["网上申购缴款日"] = pd.to_datetime(big_df["网上申购缴款日"]).dt.date
        big_df["网上申购退款日"] = pd.to_datetime(big_df["网上申购退款日"]).dt.date
        big_df["上市日"] = pd.to_datetime(big_df["上市日"]).dt.date
        big_df["发行结果公告日"] = pd.to_datetime(big_df["发行结果公告日"]).dt.date
        return big_df
    else:
        params = {
            "sortColumns": "APPLY_DATE,SECURITY_CODE",
            "sortTypes": "-1,-1",
            "pageSize": "5000",
            "pageNumber": "1",
            "reportName": "RPTA_APP_IPOAPPLY",
            "columns": "SECURITY_CODE,SECURITY_NAME,TRADE_MARKET_CODE,APPLY_CODE,TRADE_MARKET,MARKET_TYPE,ORG_TYPE,ISSUE_NUM,ONLINE_ISSUE_NUM,OFFLINE_PLACING_NUM,TOP_APPLY_MARKETCAP,PREDICT_ONFUND_UPPER,ONLINE_APPLY_UPPER,PREDICT_ONAPPLY_UPPER,ISSUE_PRICE,LATELY_PRICE,CLOSE_PRICE,APPLY_DATE,BALLOT_NUM_DATE,BALLOT_PAY_DATE,LISTING_DATE,AFTER_ISSUE_PE,ONLINE_ISSUE_LWR,INITIAL_MULTIPLE,INDUSTRY_PE_NEW,OFFLINE_EP_OBJECT,CONTINUOUS_1WORD_NUM,TOTAL_CHANGE,PROFIT,LIMIT_UP_PRICE,INFO_CODE,OPEN_PRICE,LD_OPEN_PREMIUM,LD_CLOSE_CHANGE,TURNOVERRATE,LD_HIGH_CHANG,LD_AVERAGE_PRICE,OPEN_DATE,OPEN_AVERAGE_PRICE,PREDICT_PE,PREDICT_ISSUE_PRICE2,PREDICT_ISSUE_PRICE,PREDICT_ISSUE_PRICE1,PREDICT_ISSUE_PE,PREDICT_PE_THREE,ONLINE_APPLY_PRICE,MAIN_BUSINESS",
            "filter": market_map[symbol],
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
        big_df.columns = [
            "股票代码",
            "股票简称",
            "_",
            "申购代码",
            "_",
            "_",
            "_",
            "发行总数",
            "网上发行",
            "_",
            "顶格申购需配市值",
            "_",
            "申购上限",
            "_",
            "发行价格",
            "最新价",
            "首日收盘价",
            "申购日期",
            "中签号公布日",
            "中签缴款日期",
            "上市日期",
            "发行市盈率",
            "中签率",
            "询价累计报价倍数",
            "_",
            "配售对象报价家数",
            "连续一字板数量",
            "涨幅",
            "每中一签获利",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "行业市盈率",
            "_",
            "_",
            "_",
        ]
        big_df = big_df[
            [
                "股票代码",
                "股票简称",
                "申购代码",
                "发行总数",
                "网上发行",
                "顶格申购需配市值",
                "申购上限",
                "发行价格",
                "最新价",
                "首日收盘价",
                "申购日期",
                "中签号公布日",
                "中签缴款日期",
                "上市日期",
                "发行市盈率",
                "行业市盈率",
                "中签率",
                "询价累计报价倍数",
                "配售对象报价家数",
                "连续一字板数量",
                "涨幅",
                "每中一签获利",
            ]
        ]
        big_df["申购日期"] = pd.to_datetime(big_df["申购日期"]).dt.date
        big_df["中签号公布日"] = pd.to_datetime(big_df["中签号公布日"]).dt.date
        big_df["中签缴款日期"] = pd.to_datetime(big_df["中签缴款日期"]).dt.date
        big_df["发行总数"] = pd.to_numeric(big_df["发行总数"])
        big_df["网上发行"] = pd.to_numeric(big_df["网上发行"])
        big_df["顶格申购需配市值"] = pd.to_numeric(big_df["顶格申购需配市值"])
        big_df["申购上限"] = pd.to_numeric(big_df["申购上限"])
        big_df["发行价格"] = pd.to_numeric(big_df["发行价格"])
        big_df["最新价"] = pd.to_numeric(big_df["最新价"])
        big_df["首日收盘价"] = pd.to_numeric(big_df["首日收盘价"])
        big_df["发行市盈率"] = pd.to_numeric(big_df["发行市盈率"])
        big_df["行业市盈率"] = pd.to_numeric(big_df["行业市盈率"])
        big_df["中签率"] = pd.to_numeric(big_df["中签率"])
        big_df["询价累计报价倍数"] = pd.to_numeric(big_df["询价累计报价倍数"])
        big_df["配售对象报价家数"] = pd.to_numeric(big_df["配售对象报价家数"])
        big_df["涨幅"] = pd.to_numeric(big_df["涨幅"])
        big_df["每中一签获利"] = pd.to_numeric(big_df["每中一签获利"])
    return big_df


if __name__ == "__main__":
    stock_dxsyl_em_df = stock_dxsyl_em()
    print(stock_dxsyl_em_df)

    stock_xgsglb_em_df = stock_xgsglb_em(symbol="全部股票")
    print(stock_xgsglb_em_df)

    stock_xgsglb_em_df = stock_xgsglb_em(symbol="沪市A股")
    print(stock_xgsglb_em_df)

    stock_xgsglb_em_df = stock_xgsglb_em(symbol="科创板")
    print(stock_xgsglb_em_df)

    stock_xgsglb_em_df = stock_xgsglb_em(symbol="深市A股")
    print(stock_xgsglb_em_df)

    stock_xgsglb_em_df = stock_xgsglb_em(symbol="创业板")
    print(stock_xgsglb_em_df)

    stock_xgsglb_em_df = stock_xgsglb_em(symbol="京市A股")
    print(stock_xgsglb_em_df)
