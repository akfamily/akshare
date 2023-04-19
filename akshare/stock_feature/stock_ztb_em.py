#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/4/19 17:20
Desc: 首页-行情中心-涨停板行情-涨停股池
https://quote.eastmoney.com/ztb/detail#type=ztgc

涨停板行情专题为您展示了6个股票池，分别为
涨停股池：包含当日当前涨停的所有A股股票(不含未中断连续一字涨停板的新股)；
昨日涨停股池：包含上一交易日收盘时涨停的所有A股股票(不含未中断连续一字涨停板的新股)；
强势股池：包含创下60日新高或近期多次涨停的A股股票；
次新股池：包含上市一年以内且中断了连续一字涨停板的A股股票；
炸板股池：包含当日触及过涨停板且当前未封板的A股股票；
跌停股池：包含当日当前跌停的所有A股股票。
注：涨停板行情专题统计不包含ST股票及科创板股票。
"""
import pandas as pd
import requests


def stock_zt_pool_em(date: str = "20220426") -> pd.DataFrame:
    """
    东方财富网-行情中心-涨停板行情-涨停股池
    https://quote.eastmoney.com/ztb/detail#type=ztgc
    :return: 涨停股池
    :rtype: pandas.DataFrame
    """
    url = "http://push2ex.eastmoney.com/getTopicZTPool"
    params = {
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "dpt": "wz.ztzt",
        "Pageindex": "0",
        "pagesize": "10000",
        "sort": "fbt:asc",
        "date": date,
        "_": "1621590489736",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if data_json["data"] is None:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_json["data"]["pool"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.columns = [
        "序号",
        "代码",
        "_",
        "名称",
        "最新价",
        "涨跌幅",
        "成交额",
        "流通市值",
        "总市值",
        "换手率",
        "连板数",
        "首次封板时间",
        "最后封板时间",
        "封板资金",
        "炸板次数",
        "所属行业",
        "涨停统计",
    ]
    temp_df["涨停统计"] = (
        temp_df["涨停统计"].apply(lambda x: dict(x)["days"]).astype(str)
        + "/"
        + temp_df["涨停统计"].apply(lambda x: dict(x)["ct"]).astype(str)
    )
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "涨跌幅",
            "最新价",
            "成交额",
            "流通市值",
            "总市值",
            "换手率",
            "封板资金",
            "首次封板时间",
            "最后封板时间",
            "炸板次数",
            "涨停统计",
            "连板数",
            "所属行业",
        ]
    ]
    temp_df["首次封板时间"] = temp_df["首次封板时间"].astype(str).str.zfill(6)
    temp_df["最后封板时间"] = temp_df["最后封板时间"].astype(str).str.zfill(6)
    temp_df["最新价"] = temp_df["最新价"] / 1000
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"])
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
    temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"])
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"])
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"])
    temp_df["封板资金"] = pd.to_numeric(temp_df["封板资金"])
    temp_df["炸板次数"] = pd.to_numeric(temp_df["炸板次数"])
    temp_df["连板数"] = pd.to_numeric(temp_df["连板数"])

    return temp_df


def stock_zt_pool_previous_em(date: str = "20210521") -> pd.DataFrame:
    """
    东方财富网-行情中心-涨停板行情-昨日涨停股池
    https://quote.eastmoney.com/ztb/detail#type=zrzt
    :return: 昨日涨停股池
    :rtype: pandas.DataFrame
    """
    url = "http://push2ex.eastmoney.com/getYesterdayZTPool"
    params = {
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "dpt": "wz.ztzt",
        "Pageindex": "0",
        "pagesize": "170",
        "sort": "zs:desc",
        "date": date,
        "_": "1621590489736",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if data_json["data"] is None:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_json["data"]["pool"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.columns = [
        "序号",
        "代码",
        "_",
        "名称",
        "最新价",
        "涨停价",
        "涨跌幅",
        "成交额",
        "流通市值",
        "总市值",
        "换手率",
        "振幅",
        "涨速",
        "昨日封板时间",
        "昨日连板数",
        "所属行业",
        "涨停统计",
    ]
    temp_df["涨停统计"] = (
        temp_df["涨停统计"].apply(lambda x: dict(x)["days"]).astype(str)
        + "/"
        + temp_df["涨停统计"].apply(lambda x: dict(x)["ct"]).astype(str)
    )
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "涨跌幅",
            "最新价",
            "涨停价",
            "成交额",
            "流通市值",
            "总市值",
            "换手率",
            "涨速",
            "振幅",
            "昨日封板时间",
            "昨日连板数",
            "涨停统计",
            "所属行业",
        ]
    ]
    temp_df["最新价"] = temp_df["最新价"] / 1000
    temp_df["涨停价"] = temp_df["涨停价"] / 1000
    temp_df["昨日封板时间"] = temp_df["昨日封板时间"].astype(str).str.zfill(6)
    return temp_df


def stock_zt_pool_strong_em(date: str = "20210521") -> pd.DataFrame:
    """
    东方财富网-行情中心-涨停板行情-强势股池
    https://quote.eastmoney.com/ztb/detail#type=qsgc
    :return: 强势股池
    :rtype: pandas.DataFrame
    """
    url = "http://push2ex.eastmoney.com/getTopicQSPool"
    params = {
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "dpt": "wz.ztzt",
        "Pageindex": "0",
        "pagesize": "170",
        "sort": "zdp:desc",
        "date": date,
        "_": "1621590489736",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if data_json["data"] is None:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_json["data"]["pool"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.columns = [
        "序号",
        "代码",
        "_",
        "名称",
        "最新价",
        "涨停价",
        "_",
        "涨跌幅",
        "成交额",
        "流通市值",
        "总市值",
        "换手率",
        "是否新高",
        "入选理由",
        "量比",
        "涨速",
        "涨停统计",
        "所属行业",
    ]
    temp_df["涨停统计"] = (
        temp_df["涨停统计"].apply(lambda x: dict(x)["days"]).astype(str)
        + "/"
        + temp_df["涨停统计"].apply(lambda x: dict(x)["ct"]).astype(str)
    )
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "涨跌幅",
            "最新价",
            "涨停价",
            "成交额",
            "流通市值",
            "总市值",
            "换手率",
            "涨速",
            "是否新高",
            "量比",
            "涨停统计",
            "入选理由",
            "所属行业",
        ]
    ]
    temp_df["最新价"] = temp_df["最新价"] / 1000
    temp_df["涨停价"] = temp_df["涨停价"] / 1000
    return temp_df


def stock_zt_pool_sub_new_em(date: str = "20210525") -> pd.DataFrame:
    """
    东方财富网-行情中心-涨停板行情-次新股池
    https://quote.eastmoney.com/ztb/detail#type=cxgc
    :return: 次新股池
    :rtype: pandas.DataFrame
    """
    url = "http://push2ex.eastmoney.com/getTopicCXPooll"
    params = {
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "dpt": "wz.ztzt",
        "Pageindex": "0",
        "pagesize": "170",
        "sort": "ods:asc",
        "date": date,
        "_": "1621590489736",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if data_json["data"] is None:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_json["data"]["pool"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.columns = [
        "序号",
        "代码",
        "_",
        "名称",
        "最新价",
        "涨停价",
        "_",
        "涨跌幅",
        "成交额",
        "流通市值",
        "总市值",
        "转手率",
        "开板几日",
        "开板日期",
        "上市日期",
        "_",
        "是否新高",
        "涨停统计",
        "所属行业",
    ]
    temp_df["涨停统计"] = (
        temp_df["涨停统计"].apply(lambda x: dict(x)["days"]).astype(str)
        + "/"
        + temp_df["涨停统计"].apply(lambda x: dict(x)["ct"]).astype(str)
    )
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "涨跌幅",
            "最新价",
            "涨停价",
            "成交额",
            "流通市值",
            "总市值",
            "转手率",
            "开板几日",
            "开板日期",
            "上市日期",
            "是否新高",
            "涨停统计",
            "所属行业",
        ]
    ]
    temp_df["最新价"] = temp_df["最新价"] / 1000
    temp_df["涨停价"] = temp_df["涨停价"] / 1000
    temp_df.loc[temp_df["涨停价"] > 100000, "涨停价"] = "-"
    temp_df.loc[temp_df["上市日期"] == 0, "上市日期"] = "-"
    return temp_df


def stock_zt_pool_zbgc_em(date: str = "20210525") -> pd.DataFrame:
    """
    东方财富网-行情中心-涨停板行情-炸板股池
    https://quote.eastmoney.com/ztb/detail#type=zbgc
    :return: 炸板股池
    :rtype: pandas.DataFrame
    """
    url = "http://push2ex.eastmoney.com/getTopicZBPool"
    params = {
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "dpt": "wz.ztzt",
        "Pageindex": "0",
        "pagesize": "170",
        "sort": "fbt:asc",
        "date": date,
        "_": "1621590489736",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if data_json["data"] is None:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_json["data"]["pool"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.columns = [
        "序号",
        "代码",
        "_",
        "名称",
        "最新价",
        "涨停价",
        "涨跌幅",
        "成交额",
        "流通市值",
        "总市值",
        "换手率",
        "首次封板时间",
        "炸板次数",
        "振幅",
        "涨速",
        "涨停统计",
        "所属行业",
    ]
    temp_df["涨停统计"] = (
        temp_df["涨停统计"].apply(lambda x: dict(x)["days"]).astype(str)
        + "/"
        + temp_df["涨停统计"].apply(lambda x: dict(x)["ct"]).astype(str)
    )
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "涨跌幅",
            "最新价",
            "涨停价",
            "成交额",
            "流通市值",
            "总市值",
            "换手率",
            "涨速",
            "首次封板时间",
            "炸板次数",
            "涨停统计",
            "振幅",
            "所属行业",
        ]
    ]
    temp_df["最新价"] = temp_df["最新价"] / 1000
    temp_df["涨停价"] = temp_df["涨停价"] / 1000
    temp_df["首次封板时间"] = temp_df["首次封板时间"].astype(str).str.zfill(6)
    return temp_df


def stock_zt_pool_dtgc_em(date: str = "20220425") -> pd.DataFrame:
    """
    东方财富网-行情中心-涨停板行情-跌停股池
    https://quote.eastmoney.com/ztb/detail#type=dtgc
    :param date: 交易日
    :type date: str
    :return: 跌停股池
    :rtype: pandas.DataFrame
    """
    url = "http://push2ex.eastmoney.com/getTopicDTPool"
    params = {
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "dpt": "wz.ztzt",
        "Pageindex": "0",
        "pagesize": "10000",
        "sort": "fund:asc",
        "date": date,
        "_": "1621590489736",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if data_json["data"] is None:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_json["data"]["pool"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.columns = [
        "序号",
        "代码",
        "_",
        "名称",
        "最新价",
        "涨跌幅",
        "成交额",
        "流通市值",
        "总市值",
        "动态市盈率",
        "换手率",
        "封单资金",
        "最后封板时间",
        "板上成交额",
        "连续跌停",
        "开板次数",
        "所属行业",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "涨跌幅",
            "最新价",
            "成交额",
            "流通市值",
            "总市值",
            "动态市盈率",
            "换手率",
            "封单资金",
            "最后封板时间",
            "板上成交额",
            "连续跌停",
            "开板次数",
            "所属行业",
        ]
    ]
    temp_df["最新价"] = temp_df["最新价"] / 1000
    temp_df["最后封板时间"] = temp_df["最后封板时间"].astype(str).str.zfill(6)

    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"])
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
    temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"])
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"])
    temp_df["动态市盈率"] = pd.to_numeric(temp_df["动态市盈率"])
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"])
    temp_df["封单资金"] = pd.to_numeric(temp_df["封单资金"])
    temp_df["板上成交额"] = pd.to_numeric(temp_df["板上成交额"])
    temp_df["连续跌停"] = pd.to_numeric(temp_df["连续跌停"])
    temp_df["开板次数"] = pd.to_numeric(temp_df["开板次数"])
    temp_df["开板次数"] = pd.to_numeric(temp_df["开板次数"])

    return temp_df


if __name__ == "__main__":
    stock_zt_pool_em_df = stock_zt_pool_em(date="20220701")
    print(stock_zt_pool_em_df)

    stock_zt_pool_previous_em_df = stock_zt_pool_previous_em(date="20211224")
    print(stock_zt_pool_previous_em_df)

    stock_zt_pool_strong_em_df = stock_zt_pool_strong_em(date="20211224")
    print(stock_zt_pool_strong_em_df)

    stock_zt_pool_sub_new_em_df = stock_zt_pool_sub_new_em(date="20211224")
    print(stock_zt_pool_sub_new_em_df)

    stock_zt_pool_zbgc_em_df = stock_zt_pool_zbgc_em(date="20211224")
    print(stock_zt_pool_zbgc_em_df)

    stock_zt_pool_dtgc_em_df = stock_zt_pool_dtgc_em(date="20230419")
    print(stock_zt_pool_dtgc_em_df)
