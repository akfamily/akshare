#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
date: 2021/9/28 16:02
desc: 东方财富网-数据中心-特色数据-机构调研
http://data.eastmoney.com/jgdy/
东方财富网-数据中心-特色数据-机构调研-机构调研统计: http://data.eastmoney.com/jgdy/tj.html
东方财富网-数据中心-特色数据-机构调研-机构调研详细: http://data.eastmoney.com/jgdy/xx.html
"""
import pandas as pd
import requests
from tqdm import tqdm


def stock_em_jgdy_tj(start_date: str = "20180928") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-机构调研-机构调研统计
    http://data.eastmoney.com/jgdy/tj.html
    :param start_date: 开始时间
    :type start_date: str
    :return: 机构调研统计
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        'sortColumns': 'NOTICE_DATE,SUM,RECEIVE_START_DATE,SECURITY_CODE',
        'sortTypes': '-1,-1,-1,1',
        'pageSize': '500',
        'pageNumber': '1',
        'reportName': 'RPT_ORG_SURVEYNEW',
        'columns': 'ALL',
        'quoteColumns': 'f2~01~SECURITY_CODE~CLOSE_PRICE,f3~01~SECURITY_CODE~CHANGE_RATE',
        'source': 'WEB',
        'client': 'WEB',
        'filter': f"""(NUMBERNEW="1")(IS_SOURCE="1")(RECEIVE_START_DATE>'{'-'.join([start_date[:4], start_date[4:6], start_date[6:]])}')"""
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
        big_df = big_df.append(temp_df)
    big_df.reset_index(inplace=True)
    big_df["index"] = list(range(1, len(big_df) + 1))
    big_df.columns = [
        "序号",
        "_",
        "代码",
        "名称",
        "_",
        "公告日期",
        "接待日期",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "接待地点",
        "_",
        "接待方式",
        "_",
        "接待人员",
        "_",
        "_",
        "_",
        "_",
        "_",
        "接待机构数量",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "涨跌幅",
        "最新价",
    ]
    big_df = big_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "接待机构数量",
            "接待方式",
            "接待人员",
            "接待地点",
            "接待日期",
            "公告日期",
        ]
    ]
    big_df['最新价'] = pd.to_numeric(big_df['最新价'], errors="coerce")
    big_df['涨跌幅'] = pd.to_numeric(big_df['涨跌幅'], errors="coerce")
    big_df['接待机构数量'] = pd.to_numeric(big_df['接待机构数量'], errors="coerce")
    big_df['接待日期'] = pd.to_datetime(big_df['接待日期']).dt.date
    big_df['公告日期'] = pd.to_datetime(big_df['公告日期']).dt.date
    return big_df


def stock_em_jgdy_detail(start_date: str = "20180928") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-机构调研-机构调研详细
    http://data.eastmoney.com/jgdy/xx.html
    :param start_date: 开始时间
    :type start_date: str
    :return: 机构调研详细
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        'sortColumns': 'NOTICE_DATE,RECEIVE_START_DATE,SECURITY_CODE,NUMBERNEW',
        'sortTypes': '-1,-1,1,-1',
        'pageSize': '50000',
        'pageNumber': '1',
        'reportName': 'RPT_ORG_SURVEY',
        'columns': 'ALL',
        'quoteColumns': 'f2~01~SECURITY_CODE~CLOSE_PRICE,f3~01~SECURITY_CODE~CHANGE_RATE',
        'source': 'WEB',
        'client': 'WEB',
        'filter': f"""(IS_SOURCE="1")(RECEIVE_START_DATE>'{'-'.join([start_date[:4], start_date[4:6], start_date[6:]])}')"""
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
        big_df = big_df.append(temp_df)
    big_df.reset_index(inplace=True)
    big_df["index"] = list(range(1, len(big_df) + 1))
    big_df.columns = [
        "序号",
        "_",
        "代码",
        "名称",
        "_",
        "公告日期",
        "调研日期",
        "_",
        "_",
        "_",
        "调研机构",
        "_",
        "_",
        "_",
        "接待地点",
        "_",
        "接待方式",
        "调研人员",
        "接待人员",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "机构类型",
        "_",
        "_",
        "_",
        "_",
        "_",
        "最新价",
        "涨跌幅",
    ]
    big_df = big_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "调研机构",
            "机构类型",
            "调研人员",
            "接待方式",
            "接待人员",
            "接待地点",
            "调研日期",
            "公告日期",
        ]
    ]
    big_df['最新价'] = pd.to_numeric(big_df['最新价'], errors="coerce")
    big_df['涨跌幅'] = pd.to_numeric(big_df['涨跌幅'], errors="coerce")
    big_df['调研日期'] = pd.to_datetime(big_df['调研日期']).dt.date
    big_df['公告日期'] = pd.to_datetime(big_df['公告日期']).dt.date
    return big_df


if __name__ == "__main__":
    stock_em_jgdy_tj_df = stock_em_jgdy_tj(start_date="20180928")
    print(stock_em_jgdy_tj_df)

    stock_em_jgdy_detail_df = stock_em_jgdy_detail(start_date="20210915")
    print(stock_em_jgdy_detail_df)
