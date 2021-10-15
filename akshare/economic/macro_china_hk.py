# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/7/14 21:21
Desc: 中国-香港-宏观指标
https://data.eastmoney.com/cjsj/foreign_8_0.html
"""
from akshare.utils import demjson
import pandas as pd
import requests


def marco_china_hk_cpi() -> pd.DataFrame:
    """
    东方财富-经济数据一览-中国香港-消费者物价指数
    https://data.eastmoney.com/cjsj/foreign_8_0.html
    :return: 消费者物价指数
    :rtype: pandas.DataFrame
    """
    url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "8",
        "stat": "0",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1621332091873",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df['前值'] = pd.to_numeric(temp_df['前值'])
    temp_df['现值'] = pd.to_numeric(temp_df['现值'])
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    return temp_df


def marco_china_hk_cpi_ratio() -> pd.DataFrame:
    """
    东方财富-经济数据一览-中国香港-消费者物价指数年率
    https://data.eastmoney.com/cjsj/foreign_8_1.html
    :return: 消费者物价指数年率
    :rtype: pandas.DataFrame
    """
    url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "8",
        "stat": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1621332091873",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df['前值'] = pd.to_numeric(temp_df['前值'])
    temp_df['现值'] = pd.to_numeric(temp_df['现值'])
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    return temp_df


def marco_china_hk_rate_of_unemployment() -> pd.DataFrame:
    """
    东方财富-经济数据一览-中国香港-失业率
    https://data.eastmoney.com/cjsj/foreign_8_2.html
    :return: 失业率
    :rtype: pandas.DataFrame
    """
    url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "8",
        "stat": "2",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1621332091873",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df['前值'] = pd.to_numeric(temp_df['前值'])
    temp_df['现值'] = pd.to_numeric(temp_df['现值'])
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    return temp_df


def marco_china_hk_gbp() -> pd.DataFrame:
    """
    东方财富-经济数据一览-中国香港-香港 GDP
    https://data.eastmoney.com/cjsj/foreign_8_3.html
    :return: 香港 GDP
    :rtype: pandas.DataFrame
    """
    url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "8",
        "stat": "3",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1621332091873",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df['前值'] = pd.to_numeric(temp_df['前值'])
    temp_df['现值'] = pd.to_numeric(temp_df['现值'])
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    return temp_df


def marco_china_hk_gbp_ratio() -> pd.DataFrame:
    """
    东方财富-经济数据一览-中国香港-香港 GDP 同比
    https://data.eastmoney.com/cjsj/foreign_8_4.html
    :return: 香港 GDP 同比
    :rtype: pandas.DataFrame
    """
    url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "8",
        "stat": "4",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1621332091873",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df['前值'] = pd.to_numeric(temp_df['前值'])
    temp_df['现值'] = pd.to_numeric(temp_df['现值'])
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    return temp_df


def marco_china_hk_building_volume() -> pd.DataFrame:
    """
    东方财富-经济数据一览-中国香港-香港楼宇买卖合约数量
    https://data.eastmoney.com/cjsj/foreign_8_5.html
    :return: 香港楼宇买卖合约数量
    :rtype: pandas.DataFrame
    """
    url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "8",
        "stat": "5",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1621332091873",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df['前值'] = pd.to_numeric(temp_df['前值'])
    temp_df['现值'] = pd.to_numeric(temp_df['现值'])
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    return temp_df


def marco_china_hk_building_amount() -> pd.DataFrame:
    """
    东方财富-经济数据一览-中国香港-香港楼宇买卖合约成交金额
    https://data.eastmoney.com/cjsj/foreign_8_6.html
    :return: 香港楼宇买卖合约成交金额
    :rtype: pandas.DataFrame
    """
    url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "8",
        "stat": "6",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1621332091873",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df['前值'] = pd.to_numeric(temp_df['前值'])
    temp_df['现值'] = pd.to_numeric(temp_df['现值'])
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    return temp_df


def marco_china_hk_trade_diff_ratio() -> pd.DataFrame:
    """
    东方财富-经济数据一览-中国香港-香港商品贸易差额年率
    https://data.eastmoney.com/cjsj/foreign_8_7.html
    :return: 香港商品贸易差额年率
    :rtype: pandas.DataFrame
    """
    url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "8",
        "stat": "7",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1621332091873",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df['前值'] = pd.to_numeric(temp_df['前值'])
    temp_df['现值'] = pd.to_numeric(temp_df['现值'])
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    return temp_df


def marco_china_hk_ppi() -> pd.DataFrame:
    """
    东方财富-经济数据一览-中国香港-香港制造业 PPI 年率
    https://data.eastmoney.com/cjsj/foreign_8_8.html
    :return: 香港制造业 PPI 年率
    :rtype: pandas.DataFrame
    """
    url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
    params = {
        "type": "GJZB",
        "sty": "HKZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "8",
        "stat": "8",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1621332091873",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[1:-1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]
    temp_df['前值'] = pd.to_numeric(temp_df['前值'])
    temp_df['现值'] = pd.to_numeric(temp_df['现值'])
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).dt.date
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    return temp_df


if __name__ == "__main__":
    marco_china_hk_cpi_df = marco_china_hk_cpi()
    print(marco_china_hk_cpi_df)

    marco_china_hk_cpi_ratio_df = marco_china_hk_cpi_ratio()
    print(marco_china_hk_cpi_ratio_df)

    marco_china_hk_rate_of_unemployment_df = marco_china_hk_rate_of_unemployment()
    print(marco_china_hk_rate_of_unemployment_df)

    marco_china_hk_gbp_df = marco_china_hk_gbp()
    print(marco_china_hk_gbp_df)

    marco_china_hk_gbp_ratio_df = marco_china_hk_gbp_ratio()
    print(marco_china_hk_gbp_ratio_df)

    marco_china_hk_building_volume_df = marco_china_hk_building_volume()
    print(marco_china_hk_building_volume_df)

    marco_china_hk_building_amount_df = marco_china_hk_building_amount()
    print(marco_china_hk_building_amount_df)

    marco_china_hk_trade_diff_ratio_df = marco_china_hk_trade_diff_ratio()
    print(marco_china_hk_trade_diff_ratio_df)

    marco_china_hk_ppi_df = marco_china_hk_ppi()
    print(marco_china_hk_ppi_df)
