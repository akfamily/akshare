# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/12/4 20:31
Desc: 东方财富网-数据中心-大宗交易-市场统计
http://data.eastmoney.com/dzjy/dzjy_sctj.aspx
"""
import demjson
import pandas as pd
import requests


def stock_dzjy_sctj() -> pd.DataFrame:
    """
    东方财富网-数据中心-大宗交易-市场统计
    http://data.eastmoney.com/dzjy/dzjy_sctj.aspx
    :return: 市场统计表
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "DZJYSCTJ",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "TDATE",
        "sr": "-1",
        "p": "1",
        "ps": "50000",
        "js": "var xoqCPdgn={pages:(tp),data:(x)}",
        "rt": "53569504",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text.split("=")[1])
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.columns = [
        "交易日期",
        "上证指数",
        "上证指数涨跌幅",
        "大宗交易成交总额",
        "溢价成交总额",
        "溢价成交总额占比",
        "折价成交总额",
        "折价成交总额占比",
    ]
    temp_df["交易日期"] = pd.to_datetime(temp_df["交易日期"])
    temp_df["上证指数"] = round(temp_df["上证指数"], 2)
    temp_df["上证指数涨跌幅"] = round(temp_df["上证指数涨跌幅"], 4)
    temp_df["大宗交易成交总额"] = round(temp_df["大宗交易成交总额"].astype(float), 2)
    temp_df["溢价成交总额"] = round(temp_df["溢价成交总额"].astype(float), 2)
    temp_df["溢价成交总额占比"] = round(temp_df["溢价成交总额占比"].astype(float), 4)
    temp_df["折价成交总额"] = round(temp_df["折价成交总额"].astype(float), 2)
    temp_df["折价成交总额占比"] = round(temp_df["折价成交总额占比"].astype(float), 4)
    return temp_df


def stock_dzjy_mrmx(symbol: str = '债券', start_date: str = '2020-12-04', end_date: str = '2020-12-04') -> pd.DataFrame:
    """
    东方财富网-数据中心-大宗交易-每日明细
    http://data.eastmoney.com/dzjy/dzjy_mrmxa.aspx
    :param symbol: choice of {'A股', 'B股', '债券'}
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 每日明细
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        'A股': 'EQA',
        'B股': 'EQB',
        '债券': 'BD0',
    }
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "DZJYXQ",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "SECUCODE",
        "sr": "1",
        "p": "1",
        "ps": "5000",
        "js": "var kBPzKdtj={pages:(tp),data:(x)}",
        'filter': f"(Stype='{symbol_map[symbol]}')(TDATE>=^{start_date}^ and TDATE<=^{end_date}^)",
        "rt": "53569504",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text.split("=")[1])
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    if symbol in {'A股'}:
        temp_df.columns = [
            "序号",
            "交易日期",
            "证券代码",
            "证券简称",
            "成交价",
            "成交量",
            "成交额",
            "_",
            "买方营业部",
            "_",
            "卖方营业部",
            "_",
            "_",
            "涨跌幅",
            "收盘价",
            "_",
            "折溢率",
            "成交额/流通市值",
            "_",
            "_",
            "_",
            "_",
            "_",
        ]
        temp_df["交易日期"] = pd.to_datetime(temp_df["交易日期"])
        temp_df = temp_df[[
            "序号",
            "交易日期",
            "证券代码",
            "证券简称",
            "涨跌幅",
            "收盘价",
            "成交价",
            "折溢率",
            "成交量",
            "成交额",
            "成交额/流通市值",
            "买方营业部",
            "卖方营业部",
        ]]
        return temp_df
    if symbol in {'B股'}:
        temp_df.columns = [
            "序号",
            "交易日期",
            "证券代码",
            "证券简称",
            "成交价",
            "成交量",
            "成交额",
            "_",
            "买方营业部",
            "_",
            "卖方营业部",
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
        temp_df["交易日期"] = pd.to_datetime(temp_df["交易日期"])
        temp_df = temp_df[[
            "序号",
            "交易日期",
            "证券代码",
            "证券简称",
            "成交价",
            "成交量",
            "成交额",
            "买方营业部",
            "卖方营业部",
        ]]
        return temp_df
    if symbol in {'债券'}:
        temp_df.columns = [
            "序号",
            "交易日期",
            "证券代码",
            "证券简称",
            "成交价",
            "成交量",
            "成交额",
            "_",
            "买方营业部",
            "_",
            "卖方营业部",
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
    temp_df["交易日期"] = pd.to_datetime(temp_df["交易日期"])
    temp_df = temp_df[[
        "序号",
        "交易日期",
        "证券代码",
        "证券简称",
        "成交价",
        "成交量",
        "成交额",
        "买方营业部",
        "卖方营业部",
    ]]
    return temp_df


def stock_dzjy_mrtj(start_date: str = '2020-12-04', end_date: str = '2020-12-04') -> pd.DataFrame:
    """
    东方财富网-数据中心-大宗交易-每日统计
    http://data.eastmoney.com/dzjy/dzjy_mrtj.aspx
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 每日统计
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "DZJYGGTJ",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "Cjeltszb",
        "sr": "-1",
        "p": "1",
        "ps": "50000",
        "js": "var xoqCPdgn={pages:(tp),data:(x)}",
        'filter': f'(TDATE>=^{start_date}^ and TDATE<=^{end_date}^)',
        "rt": "53569504",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text.split("=")[1])
    temp_df = pd.DataFrame(data_json["data"])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.columns = [
        "序号",
        "交易日期",
        "证券代码",
        "证券简称",
        "涨跌幅",
        "收盘价",
        "成交均价",
        "折溢率",
        "成交笔数",
        "成交总额",
        "成交总量",
        "_",
        "成交总额/流通市值",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df["交易日期"] = pd.to_datetime(temp_df["交易日期"])
    temp_df = temp_df[[
        "序号",
        "交易日期",
        "证券代码",
        "证券简称",
        "涨跌幅",
        "收盘价",
        "成交均价",
        "折溢率",
        "成交笔数",
        "成交总量",
        "成交总额",
        "成交总额/流通市值",
    ]]
    return temp_df


if __name__ == "__main__":
    stock_dzjy_sctj_df = stock_dzjy_sctj()
    print(stock_dzjy_sctj_df)
    stock_dzjy_mrmx_df = stock_dzjy_mrmx(symbol='债券', start_date='2020-12-04', end_date='2020-12-04')
    print(stock_dzjy_mrmx_df)
    stock_dzjy_mrtj_df = stock_dzjy_mrtj(start_date='2020-12-04', end_date='2020-12-04')
    print(stock_dzjy_mrtj_df)
