# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2021/9/1 19:27
Desc: 新浪财经-债券-沪深可转债-实时行情数据和历史行情数据
http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
"""
import datetime
import json
import re

from akshare.utils import demjson
import pandas as pd
import requests
from bs4 import BeautifulSoup
from py_mini_racer import py_mini_racer
from tqdm import tqdm

from akshare.bond.cons import (
    zh_sina_bond_hs_cov_count_url,
    zh_sina_bond_hs_cov_payload,
    zh_sina_bond_hs_cov_url,
    zh_sina_bond_hs_cov_hist_url,
)
from akshare.stock.cons import hk_js_decode


def _get_zh_bond_hs_cov_page_count() -> int:
    """
    新浪财经-行情中心-债券-沪深可转债的总页数
    http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
    :return: 总页数
    :rtype: int
    """
    params = {
        "node": "hskzz_z",
    }
    r = requests.get(zh_sina_bond_hs_cov_count_url, params=params)
    page_count = int(re.findall(re.compile(r"\d+"), r.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1


def bond_zh_hs_cov_spot() -> pd.DataFrame:
    """
    新浪财经-债券-沪深可转债的实时行情数据; 大量抓取容易封IP
    http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
    :return: 所有沪深可转债在当前时刻的实时行情数据
    :rtype: pandas.DataFrame
    """
    big_df = pd.DataFrame()
    page_count = _get_zh_bond_hs_cov_page_count()
    zh_sina_bond_hs_payload_copy = zh_sina_bond_hs_cov_payload.copy()
    for page in tqdm(range(1, page_count + 1), leave=False):
        zh_sina_bond_hs_payload_copy.update({"page": page})
        res = requests.get(zh_sina_bond_hs_cov_url, params=zh_sina_bond_hs_payload_copy)
        data_json = demjson.decode(res.text)
        big_df = big_df.append(pd.DataFrame(data_json), ignore_index=True)
    return big_df


def bond_zh_hs_cov_daily(symbol: str = "sz123111") -> pd.DataFrame:
    """
    新浪财经-债券-沪深可转债的历史行情数据, 大量抓取容易封 IP
    http://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
    :param symbol: 沪深可转债代码; e.g., sh010107
    :type symbol: str
    :return: 指定沪深可转债代码的日 K 线数据
    :rtype: pandas.DataFrame
    """
    r = requests.get(
        zh_sina_bond_hs_cov_hist_url.format(
            symbol, datetime.datetime.now().strftime("%Y_%m_%d")
        )
    )
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(hk_js_decode)
    dict_list = js_code.call(
        "d", r.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df['date'] = pd.to_datetime(data_df["date"]).dt.date
    return data_df


def bond_zh_cov() -> pd.DataFrame:
    """
    东方财富网-数据中心-新股数据-可转债数据
    http://data.eastmoney.com/kzz/default.html
    :return: 可转债数据
    :rtype: pandas.DataFrame
    """
    url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get"
    params = {
        "type": "KZZ_LB2.0",
        "token": "70f12f2f4f091e459a279469fe49eca5",
        "cmd": "",
        "st": "STARTDATE",
        "sr": "-1",
        "p": "1",
        "ps": "5000",
        "js": "var {jsname}={pages:(tp),data:(x),font:(font)}",
        "rt": "53603537",
    }
    r = requests.get(url, params=params)
    text_data = r.text
    json_data = demjson.decode(text_data[text_data.find("=") + 1:])
    temp_df = pd.DataFrame(json_data["data"])
    map_dict = {
        item["code"]: item["value"] for item in json_data["font"]["FontMapping"]
    }
    for key, value in map_dict.items():
        for i in range(1, 9):
            temp_df.iloc[:, -i] = temp_df.iloc[:, -i].apply(
                lambda x: x.replace(key, str(value))
            )
    temp_df.columns = [
        "债券代码",
        "交易场所",
        "_",
        "债券简称",
        "申购日期",
        "申购代码",
        "_",
        "正股代码",
        "正股简称",
        "债券面值",
        "发行价格",
        "_",
        "中签号发布日",
        "中签率",
        "上市时间",
        "_",
        "备忘录",
        "正股价",
        "市场类型",
        "_",
        "_",
        "_",
        "原股东配售-股权登记日",
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
        "申购上限",
        "_",
        "转股价",
        "转股价值",
        "债现价",
        "转股溢价率",
        "原股东配售-每股配售额",
        "发行规模",
    ]
    temp_df = temp_df[
        [
            "债券代码",
            "债券简称",
            "申购日期",
            "申购代码",
            "申购上限",
            "正股代码",
            "正股简称",
            "正股价",
            "转股价",
            "转股价值",
            "债现价",
            "转股溢价率",
            "原股东配售-股权登记日",
            "原股东配售-每股配售额",
            "发行规模",
            "中签号发布日",
            "中签率",
            "上市时间",
        ]
    ]
    temp_df['申购日期'] = pd.to_datetime(temp_df['申购日期'], errors='coerce').dt.date
    temp_df['申购上限'] = pd.to_numeric(temp_df['申购上限'], errors='coerce')
    temp_df['正股价'] = pd.to_numeric(temp_df['正股价'], errors='coerce')
    temp_df['转股价'] = pd.to_numeric(temp_df['转股价'], errors='coerce')
    temp_df['转股价值'] = pd.to_numeric(temp_df['转股价值'], errors='coerce')
    temp_df['债现价'] = pd.to_numeric(temp_df['债现价'], errors='coerce')
    temp_df['转股溢价率'] = pd.to_numeric(temp_df['转股溢价率'], errors='coerce')
    temp_df['原股东配售-股权登记日'] = pd.to_datetime(temp_df['原股东配售-股权登记日'], errors='coerce').dt.date
    temp_df['原股东配售-每股配售额'] = pd.to_numeric(temp_df['原股东配售-每股配售额'], errors='coerce')
    temp_df['发行规模'] = pd.to_numeric(temp_df['发行规模'], errors='coerce')
    temp_df['中签号发布日'] = pd.to_datetime(temp_df['中签号发布日'], errors='coerce').dt.date
    temp_df['中签率'] = pd.to_numeric(temp_df['中签率'], errors='coerce')
    temp_df['上市时间'] = pd.to_datetime(temp_df['上市时间'], errors='coerce').dt.date
    return temp_df


def bond_cov_comparison() -> pd.DataFrame:
    """
    东方财富网-行情中心-债券市场-可转债比价表
    http://quote.eastmoney.com/center/fullscreenlist.html#convertible_comparison
    :return: 可转债比价表数据
    :rtype: pandas.DataFrame
    """
    url = "http://16.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f243",
        "fs": "b:MK0354",
        "fields": "f1,f152,f2,f3,f12,f13,f14,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f26,f243",
        "_": "1590386857527",
    }
    r = requests.get(url, params=params)
    text_data = r.text
    json_data = demjson.decode(text_data)
    temp_df = pd.DataFrame(json_data["data"]["diff"])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.columns = [
        "序号",
        "_",
        "转债最新价",
        "转债涨跌幅",
        "转债代码",
        "_",
        "转债名称",
        "上市日期",
        "_",
        "纯债价值",
        "_",
        "正股最新价",
        "正股涨跌幅",
        "_",
        "正股代码",
        "_",
        "正股名称",
        "转股价",
        "转股价值",
        "转股溢价率",
        "纯债溢价率",
        "回售触发价",
        "强赎触发价",
        "到期赎回价",
        "开始转股日",
        "申购日期",
    ]
    temp_df = temp_df[
        [
            "序号",
            "转债代码",
            "转债名称",
            "转债最新价",
            "转债涨跌幅",
            "正股代码",
            "正股名称",
            "正股最新价",
            "正股涨跌幅",
            "转股价",
            "转股价值",
            "转股溢价率",
            "纯债溢价率",
            "回售触发价",
            "强赎触发价",
            "到期赎回价",
            "纯债价值",
            "开始转股日",
            "上市日期",
            "申购日期",
        ]
    ]
    return temp_df


def bond_zh_cov_info(symbol: str = "123121") -> pd.DataFrame:
    """
    https://data.eastmoney.com/kzz/detail/123121.html
    东方财富网-数据中心-新股数据-可转债详情
    :return: 可转债详情
    :rtype: pandas.DataFrame
    """
    if symbol == 'all':
        bond_zh_cov_temp = bond_zh_cov()
        code_list = bond_zh_cov_temp['债券代码'].tolist()
        big_df = pd.DataFrame()
        for item in tqdm(code_list, leave=False):
            url = f"http://data.eastmoney.com/kzz/detail/{item}.html"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "lxml")
            data_text = soup.find("script").string.strip()
            data_json = json.loads(re.findall("var info= (.*)", data_text)[0][:-1])
            temp_df = pd.json_normalize(data_json)
            big_df = big_df.append(temp_df, ignore_index=True)
        return big_df
    else:
        url = f"http://data.eastmoney.com/kzz/detail/{symbol}.html"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        data_text = soup.find("script").string.strip()
        data_json = json.loads(re.findall("var info= (.*)", data_text)[0][:-1])
        temp_df = pd.json_normalize(data_json)
        return temp_df

    # big_df.rename({
    #     'SECURITY_CODE': '债券代码',
    #     'SECUCODE': '申购代码',
    #     'TRADE_MARKET': '交易市场',
    #     'SECURITY_NAME_ABBR': '债券简称',
    #     'DELIST_DATE': '_',
    #     'LISTING_DATE': '上市日',
    #     'CONVERT_STOCK_CODE': '交易市场',
    #     'BOND_EXPIRE': '交易市场',
    #     'RATING',
    #     'VALUE_DATE',
    #     'ISSUE_YEAR',
    #     'CEASE_DATE',
    #     'EXPIRE_DATE',
    #     'PAY_INTEREST_DAY',
    #     'INTEREST_RATE_EXPLAIN',
    #     'BOND_COMBINE_CODE',
    #     'ACTUAL_ISSUE_SCALE',
    #     'ISSUE_PRICE',
    #     'REMARK',
    #     'PAR_VALUE',
    #     'ISSUE_OBJECT',
    #     'REDEEM_TYPE',
    #     'EXECUTE_REASON_HS',
    #     'NOTICE_DATE_HS',
    #     'NOTICE_DATE_SH',
    #     'EXECUTE_PRICE_HS',
    #     'EXECUTE_PRICE_SH',
    #     'RECORD_DATE_SH',
    #     'EXECUTE_START_DATESH',
    #     'EXECUTE_START_DATEHS',
    #     'EXECUTE_END_DATE',
    #     'CORRECODE',
    #     'CORRECODE_NAME_ABBR',
    #     'PUBLIC_START_DATE',
    #     'CORRECODEO',
    #     'CORRECODE_NAME_ABBRO',
    #     'BOND_START_DATE',
    #     'SECURITY_START_DATE',
    #     'SECURITY_SHORT_NAME',
    #     'FIRST_PER_PREPLACING',
    #     'ONLINE_GENERAL_AAU',
    #     'ONLINE_GENERAL_LWR',
    #     'INITIAL_TRANSFER_PRICE',
    #     'TRANSFER_END_DATE',
    #     'TRANSFER_START_DATE',
    #     'RESALE_CLAUSE',
    #     'REDEEM_CLAUSE',
    #     'PARTY_NAME',
    #     'CONVERT_STOCK_PRICE',
    #     'TRANSFER_PRICE',
    #     'TRANSFER_VALUE',
    #     'CURRENT_BOND_PRICE',
    #     'TRANSFER_PREMIUM_RATIO',
    #     'CONVERT_STOCK_PRICEHQ',
    #     'MARKET',
    #     'RESALE_TRIG_PRICE',
    #     'REDEEM_TRIG_PRICE',
    #     'PBV_RATIO',
    #     'IB_START_DATE',
    #     'IB_END_DATE',
    #     'CASHFLOW_DATE',
    #     'COUPON_IR',
    #     'PARAM_NAME',
    #     'ISSUE_TYPE',
    #     'EXECUTE_REASON_SH',
    #     'PAYDAYNEW',
    #     'CURRENT_BOND_PRICENEW'
    # })


if __name__ == "__main__":
    bond_zh_hs_cov_daily_df = bond_zh_hs_cov_daily(symbol="sz123124")
    print(bond_zh_hs_cov_daily_df)

    bond_zh_hs_cov_spot_df = bond_zh_hs_cov_spot()
    print(bond_zh_hs_cov_spot_df)

    bond_zh_cov_df = bond_zh_cov()
    print(bond_zh_cov_df)

    bond_cov_comparison_df = bond_cov_comparison()
    print(bond_cov_comparison_df)

    bond_zh_cov_info_df = bond_zh_cov_info(symbol="all")
    print(bond_zh_cov_info_df)
