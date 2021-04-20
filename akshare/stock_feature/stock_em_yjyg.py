# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/18 21:27
Desc: 东方财富-数据中心-年报季报
东方财富-数据中心-年报季报-业绩预告
http://data.eastmoney.com/bbsj/202003/yjyg.html
东方财富-数据中心-年报季报-预约披露时间
http://data.eastmoney.com/bbsj/202003/yysj.html
"""
import demjson
import pandas as pd
import requests
from tqdm import tqdm


def stock_em_yjkb(date: str = "20201231") -> pd.DataFrame:
    """
    东方财富-数据中心-年报季报-业绩快报
    http://data.eastmoney.com/bbsj/202003/yjkb.html
    :param date: "20200331", "20200630", "20200930", "20201231"; 从 20100331 开始
    :type date: str
    :return: 业绩快报
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter.eastmoney.com/api/data/get"
    params = {
        "st": "UPDATE_DATE,SECURITY_CODE",
        "sr": "-1,-1",
        "ps": "5000",
        "p": "1",
        "type": "RPT_FCI_PERFORMANCEE",
        "sty": "ALL",
        "token": "894050c76af8597a853f5b408b759f5d",
        "filter": f"(REPORT_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    page_num = data_json["result"]["pages"]
    if page_num > 1:
        big_df = pd.DataFrame()
        for page in tqdm(range(1, page_num + 1)):
            params = {
                "st": "UPDATE_DATE,SECURITY_CODE",
                "sr": "-1,-1",
                "ps": "5000",
                "p": page,
                "type": "RPT_FCI_PERFORMANCEE",
                "sty": "ALL",
                "token": "894050c76af8597a853f5b408b759f5d",
                "filter": f"(REPORT_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
            }
            r = requests.get(url, params=params)
            data_json = r.json()
            temp_df = pd.DataFrame(data_json["result"]["data"])
            temp_df.reset_index(inplace=True)
            temp_df["index"] = range(1, len(temp_df) + 1)
            big_df = big_df.append(temp_df, ignore_index=True)
        big_df.columns = [
            "序号",
            "股票代码",
            "股票简称",
            "市场板块",
            "_",
            "证券类型",
            "_",
            "公告日期",
            "_",
            "每股收益",
            "营业收入-营业收入",
            "营业收入-去年同期",
            "净利润-净利润",
            "净利润-去年同期",
            "每股净资产",
            "净资产收益率",
            "营业收入-同比增长",
            "净利润-同比增长",
            "营业收入-季度环比增长",
            "净利润-季度环比增长",
            "所处行业",
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
                "每股收益",
                "营业收入-营业收入",
                "营业收入-去年同期",
                "营业收入-同比增长",
                "营业收入-季度环比增长",
                "净利润-净利润",
                "净利润-去年同期",
                "净利润-同比增长",
                "净利润-季度环比增长",
                "每股净资产",
                "净资产收益率",
                "所处行业",
                "公告日期",
                "市场板块",
                "证券类型",
            ]
        ]
        return big_df

    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.columns = [
        "序号",
        "股票代码",
        "股票简称",
        "市场板块",
        "_",
        "证券类型",
        "_",
        "公告日期",
        "_",
        "每股收益",
        "营业收入-营业收入",
        "营业收入-去年同期",
        "净利润-净利润",
        "净利润-去年同期",
        "每股净资产",
        "净资产收益率",
        "营业收入-同比增长",
        "净利润-同比增长",
        "营业收入-季度环比增长",
        "净利润-季度环比增长",
        "所处行业",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "每股收益",
            "营业收入-营业收入",
            "营业收入-去年同期",
            "营业收入-同比增长",
            "营业收入-季度环比增长",
            "净利润-净利润",
            "净利润-去年同期",
            "净利润-同比增长",
            "净利润-季度环比增长",
            "每股净资产",
            "净资产收益率",
            "所处行业",
            "公告日期",
            "市场板块",
            "证券类型",
        ]
    ]
    return temp_df


def stock_em_yjyg(date: str = "20200331") -> pd.DataFrame:
    """
    东方财富-数据中心-年报季报-业绩预告
    http://data.eastmoney.com/bbsj/202003/yjyg.html
    :param date: "2020-03-31", "2020-06-30", "2020-09-30", "2020-12-31"; 从 2008-12-31 开始
    :type date: str
    :return: 业绩预告
    :rtype: pandas.DataFrame
    """
    url = "http://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {
        "sortColumns": "NOTICE_DATE,SECURITY_CODE",
        "sortTypes": "-1,-1",
        "pageSize": "50",
        "pageNumber": "1",
        "reportName": "RPT_PUBLIC_OP_NEWPREDICT",
        "columns": "ALL",
        "token": "894050c76af8597a853f5b408b759f5d",
        "filter": f" (REPORT_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    big_df = pd.DataFrame()
    total_page = data_json["result"]["pages"]
    for page in tqdm(range(1, total_page + 1)):
        params = {
            "sortColumns": "NOTICE_DATE,SECURITY_CODE",
            "sortTypes": "-1,-1",
            "pageSize": "50",
            "pageNumber": page,
            "reportName": "RPT_PUBLIC_OP_NEWPREDICT",
            "columns": "ALL",
            "token": "894050c76af8597a853f5b408b759f5d",
            "filter": f" (REPORT_DATE='{'-'.join([date[:4], date[4:6], date[6:]])}')",
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
        "股票简称",
        "_",
        "公告日期",
        "报告日期",
        "_",
        "预测指标",
        "_",
        "_",
        "_",
        "_",
        "业绩变动",
        "业绩变动原因",
        "预告类型",
        "上年同期值",
        "_",
        "_",
        "_",
        "_",
        "业绩变动幅度",
        "预测数值",
        "_",
        "_",
    ]
    big_df = big_df[
        [
            "序号",
            "股票代码",
            "股票简称",
            "预测指标",
            "业绩变动",
            "预测数值",
            "业绩变动幅度",
            "业绩变动原因",
            "预告类型",
            "上年同期值",
            "公告日期",
        ]
    ]
    return big_df


def stock_em_yysj(date: str = "20200331") -> pd.DataFrame:
    """
    东方财富-数据中心-年报季报-预约披露时间
    http://data.eastmoney.com/bbsj/202003/yysj.html
    :param date: "20190331", "20190630", "20190930", "20191231"; 从 20081231 开始
    :type date: str
    :return: 指定时间的上市公司预约披露时间数据
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "YJBB21_YYPL",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "st": "frdate",
        "sr": "1",
        "p": "1",
        "ps": "5000",
        "js": "var HXutCoUP={pages:(tp),data: (x),font:(font)}",
        "filter": f"(securitytypecode='058001001')(reportdate=^{'-'.join([date[:4], date[4:6], date[6:]])}^)",
        "rt": "52907209",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") :])
    temp_df = pd.DataFrame(data_json["data"])
    return temp_df


if __name__ == "__main__":
    stock_em_yjkb_df = stock_em_yjkb(date="20200331")
    print(stock_em_yjkb_df)

    stock_em_yjyg_df = stock_em_yjyg(date="20191231")
    print(stock_em_yjyg_df)

    stock_em_yysj_df = stock_em_yysj(date="20191231")
    print(stock_em_yysj_df)
