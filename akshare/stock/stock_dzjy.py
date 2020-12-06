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


def stock_dzjy_hygtj(period: str = '近三月') -> pd.DataFrame:
    """
    东方财富网-数据中心-大宗交易-活跃 A 股统计
    http://data.eastmoney.com/dzjy/dzjy_hygtj.aspx
    :param period: choice of {'近一月', '近三月', '近六月', '近一年'}
    :type period: str
    :return: 活跃 A 股统计
    :rtype: pandas.DataFrame
    """
    period_map = {
        '近一月': '1',
        '近三月': '3',
        '近六月': '6',
        '近一年': '12',
    }
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "DZJY_HHGGTJ",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "SBSumCount",
        "sr": "-1",
        "p": "1",
        "ps": "50000",
        "js": "var xoqCPdgn={pages:(tp),data:(x)}",
        'filter': f'(TYPE={period_map[period]})',
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
        "_",
        "最近上榜日",
        "证券代码",
        "证券简称",
        "涨跌幅",
        "最新价",
        "上榜次数-总计",
        "上榜次数-溢价",
        "上榜次数-折价",
        "总成交额",
        "_",
        "折溢率",
        "成交总额/流通市值",
        "上榜日后平均涨跌幅-1日",
        "上榜日后平均涨跌幅-5日",
        "上榜日后平均涨跌幅-10日",
        "上榜日后平均涨跌幅-20日",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df["最近上榜日"] = pd.to_datetime(temp_df["最近上榜日"])
    temp_df = temp_df[[
        "序号",
        "证券代码",
        "证券简称",
        "最新价",
        "涨跌幅",
        "最近上榜日",
        "上榜次数-总计",
        "上榜次数-溢价",
        "上榜次数-折价",
        "总成交额",
        "折溢率",
        "成交总额/流通市值",
        "上榜日后平均涨跌幅-1日",
        "上榜日后平均涨跌幅-5日",
        "上榜日后平均涨跌幅-10日",
        "上榜日后平均涨跌幅-20日",
    ]]
    return temp_df


def stock_dzjy_hyyybtj(period: str = '近3日') -> pd.DataFrame:
    """
    东方财富网-数据中心-大宗交易-活跃营业部统计
    http://data.eastmoney.com/dzjy/dzjy_hyyybtj.aspx
    :param period: choice of {'当前交易日', '近3日', '近5日', '近10日', '近30日'}
    :type period: str
    :return: 活跃营业部统计
    :rtype: pandas.DataFrame
    """
    period_map = {
        '当前交易日': '1',
        '近3日': '3',
        '近5日': '5',
        '近10日': '10',
        '近30日': '30',
    }
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "DZJY_HHYYBTJ",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "BCount",
        "sr": "-1",
        "p": "1",
        "ps": "50000",
        "js": "var xoqCPdgn={pages:(tp),data:(x)}",
        'filter': f'(TYPE={period_map[period]})',
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
        "_",
        "最近上榜日",
        "_",
        "营业部名称",
        "次数总计-买入",
        "次数总计-卖出",
        "成交金额统计-买入",
        "成交金额统计-卖出",
        "成交金额统计-净买入额",
        "买入的股票",
    ]
    temp_df["最近上榜日"] = pd.to_datetime(temp_df["最近上榜日"])
    temp_df = temp_df[[
        "序号",
        "最近上榜日",
        "营业部名称",
        "次数总计-买入",
        "次数总计-卖出",
        "成交金额统计-买入",
        "成交金额统计-卖出",
        "成交金额统计-净买入额",
        "买入的股票",
    ]]
    return temp_df


def stock_dzjy_yybph(period: str = '近三月') -> pd.DataFrame:
    """
    东方财富网-数据中心-大宗交易-营业部排行
    http://data.eastmoney.com/dzjy/dzjy_yybph.aspx
    :param period: choice of {'近一月', '近三月', '近六月', '近一年'}
    :type period: str
    :return: 营业部排行
    :rtype: pandas.DataFrame
    """
    period_map = {
        '近一月': '1',
        '近三月': '3',
        '近六月': '6',
        '近一年': '12',
    }
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "DZJY_YYBHB",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "BCount",
        "sr": "-1",
        "p": "1",
        "ps": "50000",
        "js": "var xoqCPdgn={pages:(tp),data:(x)}",
        'filter': f'(TYPE={period_map[period]})',
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
        "_",
        "_",
        "营业部名称",
        "上榜后1天-买入次数",
        "上榜后1天-平均涨幅",
        "_",
        "_",
        "上榜后1天-上涨概率",
        "上榜后5天-平均涨幅",
        "_",
        "_",
        "上榜后5天-上涨概率",
        "上榜后10天-平均涨幅",
        "_",
        "_",
        "上榜后10天-上涨概率",
        "上榜后20天-平均涨幅",
        "_",
        "_",
        "上榜后20天-上涨概率"
    ]
    temp_df = temp_df[[
        "序号",
        "营业部名称",
        "上榜后1天-买入次数",
        "上榜后1天-平均涨幅",
        "上榜后1天-上涨概率",
        "上榜后5天-平均涨幅",
        "上榜后5天-上涨概率",
        "上榜后10天-平均涨幅",
        "上榜后10天-上涨概率",
        "上榜后20天-平均涨幅",
        "上榜后20天-上涨概率"
    ]]
    return temp_df


if __name__ == "__main__":
    stock_dzjy_sctj_df = stock_dzjy_sctj()
    print(stock_dzjy_sctj_df)
    stock_dzjy_mrmx_df = stock_dzjy_mrmx(symbol='债券', start_date='2020-12-04', end_date='2020-12-04')
    print(stock_dzjy_mrmx_df)
    stock_dzjy_mrtj_df = stock_dzjy_mrtj(start_date='2020-12-04', end_date='2020-12-04')
    print(stock_dzjy_mrtj_df)
    stock_dzjy_hygtj_df = stock_dzjy_hygtj(period='近三月')
    print(stock_dzjy_hygtj_df)
    stock_dzjy_hyyybtj_df = stock_dzjy_hyyybtj(period='近3日')
    print(stock_dzjy_hyyybtj_df)
    stock_dzjy_yybph_df = stock_dzjy_yybph(period='近三月')
    print(stock_dzjy_yybph_df)
