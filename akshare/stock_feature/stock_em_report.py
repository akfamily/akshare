# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/4/5 16:53
Desc: 东方财富-数据中心-年报季报-业绩快报-三大报表
资产负债表
http://data.eastmoney.com/bbsj/202003/zcfz.html
利润表
http://data.eastmoney.com/bbsj/202003/lrb.html
现金流量表
http://data.eastmoney.com/bbsj/202003/xjll.html
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_em_zcfz(date: str = "20200331") -> pd.DataFrame:
    """
    东方财富-数据中心-年报季报-业绩快报-资产负债表
    http://data.eastmoney.com/bbsj/202003/zcfz.html
    :param date: "20200331", "20200630", "20200930", "20201231"; 从 20100331 开始
    :type date: str
    :return: 资产负债表
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter-web.eastmoney.com/api/data/get"
    params = {
        "st": "NOTICE_DATE,SECURITY_CODE",
        "sr": "-1,-1",
        "ps": "5000",
        "p": "1",
        "type": "RPT_DMSK_FN_BALANCE",
        "sty": "ALL",
        "token": "894050c76af8597a853f5b408b759f5d",
        "filter": f"(REPORT_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    page_num = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1)):
        params = {
            "st": "NOTICE_DATE,SECURITY_CODE",
            "sr": "-1,-1",
            "ps": "5000",
            "p": page,
            "type": "RPT_DMSK_FN_BALANCE",
            "sty": "ALL",
            "token": "894050c76af8597a853f5b408b759f5d",
            "filter": f"(REPORT_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = big_df.append(temp_df, ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    big_df.columns = [
        "序号",
        "_",
        "股票代码",
        "_",
        "_",
        "股票简称",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "公告日期",
        "_",
        "资产-总资产",
        "_",
        "资产-货币资金",
        "_",
        "资产-应收账款",
        "_",
        "资产-存货",
        "_",
        "负债-总负债",
        "负债-应付账款",
        "_",
        "负债-预收账款",
        "_",
        "股东权益合计",
        "_",
        "资产-总资产同比",
        "负债-总负债同比",
        "_",
        "资产负债率",
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
    ]
    big_df = big_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "资产-货币资金",
            "资产-应收账款",
            "资产-存货",
            "资产-总资产",
            "资产-总资产同比",
            "负债-应付账款",
            "负债-预收账款",
            "负债-总负债",
            "负债-总负债同比",
            "资产负债率",
            "股东权益合计",
            "公告日期",
        ]
    ]
    return big_df


def stock_em_lrb(date: str = "20200331") -> pd.DataFrame:
    """
    东方财富-数据中心-年报季报-业绩快报-利润表
    http://data.eastmoney.com/bbsj/202003/lrb.html
    :param date: "20200331", "20200630", "20200930", "20201231"; 从 20100331 开始
    :type date: str
    :return: 利润表
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter-web.eastmoney.com/api/data/get"
    params = {
        "st": "NOTICE_DATE,SECURITY_CODE",
        "sr": "-1,-1",
        "ps": "5000",
        "p": "1",
        "type": "RPT_DMSK_FN_INCOME",
        "sty": "ALL",
        "token": "894050c76af8597a853f5b408b759f5d",
        "filter": f"(REPORT_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    page_num = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1)):
        params = {
            "st": "NOTICE_DATE,SECURITY_CODE",
            "sr": "-1,-1",
            "ps": "5000",
            "p": page,
            "type": "RPT_DMSK_FN_INCOME",
            "sty": "ALL",
            "token": "894050c76af8597a853f5b408b759f5d",
            "filter": f"(REPORT_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = big_df.append(temp_df, ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    big_df.columns = [
        "序号",
        "_",
        "股票代码",
        "_",
        "_",
        "股票简称",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "公告日期",
        "_",
        "净利润",
        "营业总收入",
        "营业总支出-营业总支出",
        "_",
        "营业总支出-营业支出",
        "_",
        "_",
        "营业总支出-销售费用",
        "营业总支出-管理费用",
        "营业总支出-财务费用",
        "营业利润",
        "利润总额",
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
        "_",
        "营业总收入同比",
        "_",
        "净利润同比",
        "_",
        "_",
    ]
    big_df = big_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "净利润",
            "净利润同比",
            "营业总收入",
            "营业总收入同比",
            "营业总支出-营业支出",
            "营业总支出-销售费用",
            "营业总支出-管理费用",
            "营业总支出-财务费用",
            "营业总支出-营业总支出",
            "营业利润",
            "利润总额",
            "公告日期",
        ]
    ]
    return big_df


def stock_em_xjll(date: str = "20200331") -> pd.DataFrame:
    """
    东方财富-数据中心-年报季报-业绩快报-现金流量表
    http://data.eastmoney.com/bbsj/202003/xjll.html
    :param date: "20200331", "20200630", "20200930", "20201231"; 从 20100331 开始
    :type date: str
    :return: 现金流量表
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter-web.eastmoney.com/api/data/get"
    params = {
        "st": "NOTICE_DATE,SECURITY_CODE",
        "sr": "-1,-1",
        "ps": "5000",
        "p": "1",
        "type": "RPT_DMSK_FN_CASHFLOW",
        "sty": "ALL",
        "token": "894050c76af8597a853f5b408b759f5d",
        "filter": f"(REPORT_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    page_num = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1)):
        params = {
            "st": "NOTICE_DATE,SECURITY_CODE",
            "sr": "-1,-1",
            "ps": "5000",
            "p": page,
            "type": "RPT_DMSK_FN_CASHFLOW",
            "sty": "ALL",
            "token": "894050c76af8597a853f5b408b759f5d",
            "filter": f"(REPORT_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = big_df.append(temp_df, ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    big_df.columns = [
        "序号",
        "_",
        "股票代码",
        "_",
        "_",
        "股票简称",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "公告日期",
        "_",
        "经营性现金流-现金流量净额",
        "经营性现金流-净现金流占比",
        "_",
        "_",
        "_",
        "_",
        "投资性现金流-现金流量净额",
        "投资性现金流-净现金流占比",
        "_",
        "_",
        "_",
        "_",
        "融资性现金流-现金流量净额",
        "融资性现金流-净现金流占比",
        "净现金流-净现金流",
        "净现金流-同比增长",
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
        "_",
        "_",
        "_",
        "_",
    ]
    big_df = big_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "净现金流-净现金流",
            "净现金流-同比增长",
            "经营性现金流-现金流量净额",
            "经营性现金流-净现金流占比",
            "投资性现金流-现金流量净额",
            "投资性现金流-净现金流占比",
            "融资性现金流-现金流量净额",
            "融资性现金流-净现金流占比",
            "公告日期",
        ]
    ]
    return big_df


if __name__ == "__main__":
    stock_em_zcfz_df = stock_em_zcfz(date="20200331")
    print(stock_em_zcfz_df)

    stock_em_lrb_df = stock_em_lrb(date="20200331")
    print(stock_em_lrb_df)

    stock_em_xjll_df = stock_em_xjll(date="20200331")
    print(stock_em_xjll_df)
