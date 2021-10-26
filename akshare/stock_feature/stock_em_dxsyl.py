#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/7/16 12:02
Desc: 东方财富网-数据中心-新股数据-打新收益率
东方财富网-数据中心-新股数据-打新收益率
http://data.eastmoney.com/xg/xg/dxsyl.html
东方财富网-数据中心-新股数据-新股申购与中签查询
http://data.eastmoney.com/xg/xg/default_2.html
"""
from akshare.utils import demjson
import pandas as pd
import requests
from tqdm import tqdm


def _get_page_num_dxsyl(market: str = "上海主板") -> int:
    """
    东方财富网-数据中心-新股数据-打新收益率-总页数
    http://data.eastmoney.com/xg/xg/dxsyl.html
    :param market: choice of {"上海主板", "创业板", "深圳主板"}
    :type market: str
    :return: 总页数
    :rtype: int
    """
    market_map = {"上海主板": "2", "创业板": "3", "深圳主板": "4"}
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "NS",
        "sty": "NSDXSYL",
        "st": "16",
        "sr": "-1",
        "p": "1",
        "ps": "50",
        "js": "var oyfyNYmO={pages:(pc),data:[(x)]}",
        "stat": market_map[market],
        "rt": "52898446",
    }
    res = requests.get(url, params=params)
    data_json = demjson.decode(res.text[res.text.find("={") + 1 :])
    return data_json["pages"]


def stock_em_dxsyl(market: str = "上海主板") -> pd.DataFrame:
    """
    东方财富网-数据中心-新股数据-打新收益率
    http://data.eastmoney.com/xg/xg/dxsyl.html
    :param market: choice of {"上海主板", "创业板", "深圳主板"}
    :type market: str
    :return: 指定市场的打新收益率数据
    :rtype: pandas.DataFrame
    """
    market_map = {"上海主板": "2", "创业板": "3", "深圳主板": "4"}
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    page_num = _get_page_num_dxsyl(market=market)
    temp_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1), leave=False):
        params = {
            "type": "NS",
            "sty": "NSDXSYL",
            "st": "16",
            "sr": "-1",
            "p": str(page),
            "ps": "50",
            "js": "({data:[(x)],pages:(pc)})",
            "stat": market_map[market],
            "rt": "52898446",
        }
        res = requests.get(url, params=params)
        data_text = res.text
        data_json = demjson.decode(data_text[data_text.find("(") + 1 :-1])
        temp_df = temp_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    temp_df = temp_df.iloc[:, 0].str.split(",", expand=True)
    temp_df.columns = [
        "股票代码",
        "股票简称",
        "发行价",
        "最新价",
        "网上发行中签率",
        "网上有效申购股数",
        "网上有效申购户数",
        "网上超额认购倍数",
        "网下配售中签率",
        "网下有效申购股数",
        "网下有效申购户数",
        "网下配售认购倍数",
        "总发行数量",
        "开盘溢价",
        "首日涨幅",
        "打新收益",
        "上市日期",
        "市场",
    ]
    temp_df["发行价"] = pd.to_numeric(temp_df["发行价"])
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"])
    temp_df["网上发行中签率"] = pd.to_numeric(temp_df["网上发行中签率"])
    temp_df["网上有效申购股数"] = pd.to_numeric(temp_df["网上有效申购股数"])
    temp_df["网上有效申购户数"] = pd.to_numeric(temp_df["网上有效申购户数"])
    temp_df["网上超额认购倍数"] = pd.to_numeric(temp_df["网上超额认购倍数"])
    temp_df["网下配售中签率"] = pd.to_numeric(temp_df["网下配售中签率"])
    temp_df["网下有效申购股数"] = pd.to_numeric(temp_df["网下有效申购股数"])
    temp_df["网下有效申购户数"] = pd.to_numeric(temp_df["网下有效申购户数"])
    temp_df["网下配售认购倍数"] = pd.to_numeric(temp_df["网下配售认购倍数"])
    temp_df["总发行数量"] = pd.to_numeric(temp_df["总发行数量"])
    temp_df["开盘溢价"] = pd.to_numeric(temp_df["开盘溢价"])
    temp_df["首日涨幅"] = pd.to_numeric(temp_df["首日涨幅"])
    temp_df["打新收益"] = pd.to_numeric(temp_df["打新收益"])
    return temp_df


def stock_em_xgsglb(market: str = "沪市A股") -> pd.DataFrame:
    """
    新股申购与中签查询
    http://data.eastmoney.com/xg/xg/default_2.html
    :param market: choice of {"全部股票", "沪市A股", "科创板", "深市A股", "创业板"}
    :type market: str
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
    params = {
        'sortColumns': 'APPLY_DATE,SECURITY_CODE',
        'sortTypes': '-1,-1',
        'pageSize': '5000',
        'pageNumber': '1',
        'reportName': 'RPTA_APP_IPOAPPLY',
        'columns': 'SECURITY_CODE,SECURITY_NAME,TRADE_MARKET_CODE,APPLY_CODE,TRADE_MARKET,MARKET_TYPE,ORG_TYPE,ISSUE_NUM,ONLINE_ISSUE_NUM,OFFLINE_PLACING_NUM,TOP_APPLY_MARKETCAP,PREDICT_ONFUND_UPPER,ONLINE_APPLY_UPPER,PREDICT_ONAPPLY_UPPER,ISSUE_PRICE,LATELY_PRICE,CLOSE_PRICE,APPLY_DATE,BALLOT_NUM_DATE,BALLOT_PAY_DATE,LISTING_DATE,AFTER_ISSUE_PE,ONLINE_ISSUE_LWR,INITIAL_MULTIPLE,INDUSTRY_PE_NEW,OFFLINE_EP_OBJECT,CONTINUOUS_1WORD_NUM,TOTAL_CHANGE,PROFIT,LIMIT_UP_PRICE,INFO_CODE,OPEN_PRICE,LD_OPEN_PREMIUM,LD_CLOSE_CHANGE,TURNOVERRATE,LD_HIGH_CHANG,LD_AVERAGE_PRICE,OPEN_DATE,OPEN_AVERAGE_PRICE,PREDICT_PE,PREDICT_ISSUE_PRICE2,PREDICT_ISSUE_PRICE,PREDICT_ISSUE_PRICE1,PREDICT_ISSUE_PE,PREDICT_PE_THREE,ONLINE_APPLY_PRICE,MAIN_BUSINESS',
        'filter': market_map[market],
        'source': 'WEB',
        'client': 'WEB',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json['result']['pages']
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page+1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json['result']['data'])
        big_df = big_df.append(temp_df, ignore_index=True)
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
    big_df['申购日期'] = pd.to_datetime(big_df['申购日期']).dt.date
    big_df['中签号公布日'] = pd.to_datetime(big_df['中签号公布日']).dt.date
    big_df['中签缴款日期'] = pd.to_datetime(big_df['中签缴款日期']).dt.date
    big_df['发行总数'] = pd.to_numeric(big_df['发行总数'])
    big_df['网上发行'] = pd.to_numeric(big_df['网上发行'])
    big_df['顶格申购需配市值'] = pd.to_numeric(big_df['顶格申购需配市值'])
    big_df['申购上限'] = pd.to_numeric(big_df['申购上限'])
    big_df['发行价格'] = pd.to_numeric(big_df['发行价格'])
    big_df['最新价'] = pd.to_numeric(big_df['最新价'])
    big_df['首日收盘价'] = pd.to_numeric(big_df['首日收盘价'])
    big_df['发行市盈率'] = pd.to_numeric(big_df['发行市盈率'])
    big_df['行业市盈率'] = pd.to_numeric(big_df['行业市盈率'])
    big_df['中签率'] = pd.to_numeric(big_df['中签率'])
    big_df['询价累计报价倍数'] = pd.to_numeric(big_df['询价累计报价倍数'])
    big_df['配售对象报价家数'] = pd.to_numeric(big_df['配售对象报价家数'])
    big_df['涨幅'] = pd.to_numeric(big_df['涨幅'])
    big_df['每中一签获利'] = pd.to_numeric(big_df['每中一签获利'])
    return big_df


if __name__ == "__main__":
    stock_em_dxsyl_df = stock_em_dxsyl(market="上海主板")
    print(stock_em_dxsyl_df)

    stock_em_dxsyl_df = stock_em_dxsyl(market="创业板")
    print(stock_em_dxsyl_df)

    # stock_em_dxsyl_df = stock_em_dxsyl(market="深圳主板")
    # print(stock_em_dxsyl_df)

    stock_em_xgsglb_df = stock_em_xgsglb(market="全部股票")
    print(stock_em_xgsglb_df)

    stock_em_xgsglb_df = stock_em_xgsglb(market="沪市A股")
    print(stock_em_xgsglb_df)

    stock_em_xgsglb_df = stock_em_xgsglb(market="科创板")
    print(stock_em_xgsglb_df)

    stock_em_xgsglb_df = stock_em_xgsglb(market="深市A股")
    print(stock_em_xgsglb_df)

    stock_em_xgsglb_df = stock_em_xgsglb(market="创业板")
    print(stock_em_xgsglb_df)
