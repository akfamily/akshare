# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/10/17 18:11
Desc: 新浪财经-股票期权
https://stock.finance.sina.com.cn/option/quotes.html
期权-中金所-沪深300指数
https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php
期权-上交所-50ETF
期权-上交所-300ETF
https://stock.finance.sina.com.cn/option/quotes.html
"""
import json
import datetime
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup
import pandas as pd


# 期权-中金所-沪深300指数
def option_sina_cffex_hs300_list() -> Dict[str, List[str]]:
    """
    中金所-沪深300指数-所有合约, 返回的第一个合约为主力合约
    目前中金所只有 沪深300指数
    :return: 中金所-沪深300指数-所有合约
    :rtype: dict
    """
    url = "https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    symbol = soup.find(attrs={"id": "option_symbol"}).find("li").text
    contract = [
        item.text for item in soup.find(attrs={"id": "option_suffix"}).find_all("li")
    ]
    return {symbol: contract}


def option_sina_cffex_hs300_spot(contract: str = "io2004") -> pd.DataFrame:
    """
    中金所-沪深300指数-指定合约-实时行情
    :param contract: 合约代码, 用 option_sina_cffex_hs300_list 函数查看
    :type contract: str
    :return: 中金所-沪深300指数-指定合约-看涨看跌实时行情
    :rtype: pd.DataFrame
    """
    url = "https://stock.finance.sina.com.cn/futures/api/openapi.php/OptionService.getOptionData"
    payload = {
        "type": "futures",
        "product": "io",
        "exchange": "cffex",
        "pinzhong": contract,
    }
    r = requests.get(url, params=payload)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{") : data_text.rfind("}") + 1])
    option_call_df = pd.DataFrame(
        data_json["result"]["data"]["up"],
        columns=[
            "call_买量",
            "call_买价",
            "call_最新价",
            "call_卖价",
            "call_卖量",
            "call_持仓量",
            "call_涨跌",
            "call_行权价",
            "call_标识",
        ],
    )
    option_put_df = pd.DataFrame(
        data_json["result"]["data"]["down"],
        columns=[
            "put_买量",
            "put_买价",
            "put_最新价",
            "put_卖价",
            "put_卖量",
            "put_持仓量",
            "put_涨跌",
            "put_标识",
        ],
    )
    data_df = pd.concat([option_call_df, option_put_df], axis=1).iloc[:, :-1]
    return data_df


def option_sina_cffex_hs300_daily(contract: str = "io2004C4450") -> pd.DataFrame:
    """
    中金所-沪深300指数-指定合约-日频行情
    :param contract: 具体合约代码(包括看涨和看跌标识), 可以通过 option_sina_cffex_hs300_spot 中的 call_标识 获取
    :type contract: str
    :return: 日频率数据
    :rtype: pd.DataFrame
    """
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    url = f"https://stock.finance.sina.com.cn/futures/api/jsonp.php/var%20_{contract}{year}_{month}_{day}=/FutureOptionAllService.getOptionDayline"
    payload = {"symbol": contract}
    r = requests.get(url, params=payload)
    data_text = r.text
    data_df = pd.DataFrame(
        eval(data_text[data_text.find("["): data_text.rfind("]") + 1])
    )
    data_df.columns = ["open", "high", "low", "close", "volume", "date"]
    return data_df


# 期权-上交所-50ETF
def option_sina_sse_list(symbol: str = "50ETF", exchange: str = "null") -> List[str]:
    """
    期权-上交所-50ETF-合约到期月份列表
    :param symbol: 50ETF or 300ETF
    :type symbol: str
    :param exchange: null
    :type exchange: str
    :return: 合约到期时间
    :rtype: list
    """
    url = (
        f"http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName?"
        f"exchange={exchange}&cate={symbol}"
    )
    date_list = requests.get(url).json()["result"]["data"]["contractMonth"]
    return ["".join(i.split("-")) for i in date_list][1:]


def option_sina_sse_expire_day(
    trade_date: str = "202002", symbol="50ETF", exchange="null"
) -> Tuple[str, int]:
    """
    获取指定到期月份指定品种的剩余到期时间
    :param trade_date: 到期月份: 202002, 20203, 20206, 20209
    :type trade_date: str
    :param symbol: 50ETF or 300ETF
    :type symbol: str
    :param exchange: null
    :type exchange: str
    :return: (到期时间, 剩余时间)
    :rtype: tuple
    """
    url = (
        f"http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getRemainderDay?"
        f"exchange={exchange}&cate={symbol}&date={trade_date[:4]}-{trade_date[4:]}"
    )
    data = requests.get(url).json()["result"]["data"]
    if int(data["remainderDays"]) < 0:
        url = (
            f"http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getRemainderDay?"
            f"exchange={exchange}&cate={'XD' + symbol}&date={trade_date[:4]}-{trade_date[4:]}"
        )
        data = requests.get(url).json()["result"]["data"]
    return data["expireDay"], int(data["remainderDays"])


def option_sina_sse_codes(
    trade_date: str = "202002", underlying: str = "510300"
) -> Tuple[List[str], List[str]]:
    """
    获取上海证券交易所所有看涨和看跌合约的代码
    :param trade_date: 期权到期月份
    :type trade_date: "202002"
    :param underlying: 标的产品代码 华夏上证 50ETF: 510050 or 华泰柏瑞沪深 300ETF: 510300
    :type underlying: str
    :return: 看涨看跌合约的代码
    :rtype: Tuple[List, List]
    """
    url_up = "".join(
        ["http://hq.sinajs.cn/list=OP_UP_", underlying, str(trade_date)[-4:]]
    )
    url_down = "".join(
        ["http://hq.sinajs.cn/list=OP_DOWN_", underlying, str(trade_date)[-4:]]
    )
    data_up = requests.get(url_up).text.replace('"', ",").split(",")
    codes_up = [i[7:] for i in data_up if i.startswith("CON_OP_")]
    data_down = requests.get(url_down).text.replace('"', ",").split(",")
    codes_down = [i[7:] for i in data_down if i.startswith("CON_OP_")]
    return codes_up, codes_down


def option_sina_sse_spot_price(code: str = "10002273") -> pd.DataFrame:
    """
    期权实时数据
    :param code: 期权代码
    :type code: str
    :return: 期权量价数据
    :rtype: pandas.DataFrame
    """
    url = f"http://hq.sinajs.cn/list=CON_OP_{code}"
    data_text = requests.get(url).text
    data_list = data_text[data_text.find('"') + 1 : data_text.rfind('"')].split(",")
    field_list = [
        "买量",
        "买价",
        "最新价",
        "卖价",
        "卖量",
        "持仓量",
        "涨幅",
        "行权价",
        "昨收价",
        "开盘价",
        "涨停价",
        "跌停价",
        "申卖价五",
        "申卖量五",
        "申卖价四",
        "申卖量四",
        "申卖价三",
        "申卖量三",
        "申卖价二",
        "申卖量二",
        "申卖价一",
        "申卖量一",
        "申买价一",
        "申买量一 ",
        "申买价二",
        "申买量二",
        "申买价三",
        "申买量三",
        "申买价四",
        "申买量四",
        "申买价五",
        "申买量五",
        "行情时间",
        "主力合约标识",
        "状态码",
        "标的证券类型",
        "标的股票",
        "期权合约简称",
        "振幅",
        "最高价",
        "最低价",
        "成交量",
        "成交额",
    ]
    data_df = pd.DataFrame(list(zip(field_list, data_list)), columns=["字段", "值"])
    return data_df


def option_sina_sse_underlying_spot_price(code: str = "sh510300") -> pd.DataFrame:
    """
    期权标的物的实时数据
    :param code: sh510050 or sh510300
    :type code: str
    :return: 期权标的物的信息
    :rtype: pandas.DataFrame
    """
    url = f"http://hq.sinajs.cn/list={code}"
    data_text = requests.get(url).text
    data_list = data_text[data_text.find('"') + 1 : data_text.rfind('"')].split(",")
    field_list = [
        "证券简称",
        "今日开盘价",
        "昨日收盘价",
        "最近成交价",
        "最高成交价",
        "最低成交价",
        "买入价",
        "卖出价",
        "成交数量",
        "成交金额",
        "买数量一",
        "买价位一",
        "买数量二",
        "买价位二",
        "买数量三",
        "买价位三",
        "买数量四",
        "买价位四",
        "买数量五",
        "买价位五",
        "卖数量一",
        "卖价位一",
        "卖数量二",
        "卖价位二",
        "卖数量三",
        "卖价位三",
        "卖数量四",
        "卖价位四",
        "卖数量五",
        "卖价位五",
        "行情日期",
        "行情时间",
        "停牌状态",
    ]
    data_df = pd.DataFrame(list(zip(field_list, data_list)), columns=["字段", "值"])
    return data_df


def option_sina_sse_greeks(code: str = "10002273") -> pd.DataFrame:
    """
    期权基本信息表
    :param code: 合约代码
    :type code: str
    :return: 期权基本信息表
    :rtype: pandas.DataFrame
    """
    url = f"http://hq.sinajs.cn/list=CON_SO_{code}"
    data_text = requests.get(url).text
    data_list = data_text[data_text.find('"') + 1: data_text.rfind('"')].split(",")
    field_list = [
        "期权合约简称",
        "成交量",
        "Delta",
        "Gamma",
        "Theta",
        "Vega",
        "隐含波动率",
        "最高价",
        "最低价",
        "交易代码",
        "行权价",
        "最新价",
        "理论价值",
    ]
    data_df = pd.DataFrame(
        list(zip(field_list, [data_list[0]] + data_list[4:])), columns=["字段", "值"]
    )
    return data_df


def option_sina_sse_minute(code: str = "10002273") -> pd.DataFrame:
    """
    指定期权品种在当前交易日的分钟数据, 只能获取当前交易日的数据, 不能获取历史分钟数据
    https://stock.finance.sina.com.cn/option/quotes.html
    :param code: 期权代码
    :type code: str
    :return: 指定期权的当前交易日的分钟数据
    :rtype: pandas.DataFrame
    """
    url = (
        f"https://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionDaylineService.getOptionMinline?"
        f"symbol=CON_OP_{code}"
    )
    data_json = requests.get(url).json()["result"]["data"]
    data_df = pd.DataFrame(data_json)
    data_df.columns = ["时间", "价格", "成交", "持仓", "均价", "日期"]
    return data_df


def option_sina_sse_daily(code: str = "10002273") -> pd.DataFrame:
    """
    获取指定期权的日频率数据
    :param code: 期权代码
    :type code: str
    :return: 指定期权的所有日频率历史数据
    :rtype: pandas.DataFrame
    """
    url = (
        f"http://stock.finance.sina.com.cn/futures/api/jsonp_v2.php//StockOptionDaylineService.getSymbolInfo?"
        f"symbol=CON_OP_{code}"
    )
    data_text = requests.get(url).text
    data_json = json.loads(data_text[data_text.find("(") + 1 : data_text.rfind(")")])
    data_df = pd.DataFrame(data_json)
    data_df.columns = ["日期", "开盘", "最高", "最低", "收盘", "成交"]
    return data_df


def option_sina_finance_minute(code: str = "10002530") -> pd.DataFrame:
    """
    指定期权的分钟频率数据
    https://stock.finance.sina.com.cn/option/quotes.html
    :param code: 期权代码
    :type code: str
    :return: 指定期权的分钟频率数据
    :rtype: pandas.DataFrame
    """
    url = "https://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionDaylineService.getFiveDayLine"
    params = {
        "symbol": f"CON_OP_{code}",
    }
    r = requests.get(url, params=params)
    data_text = r.json()
    temp_df = pd.DataFrame()
    for item in data_text["result"]["data"]:
        temp_df = temp_df.append(pd.DataFrame(item), ignore_index=True)
    temp_df.fillna(method="ffill", inplace=True)
    temp_df.columns = ["time", "price", "volume", "_", "average_price", "date"]
    temp_df = temp_df[["date", "time", "price", "average_price", "volume"]]
    return temp_df


if __name__ == "__main__":
    # 期权-中金所-沪深300指数
    option_sina_cffex_hs300_list_df = option_sina_cffex_hs300_list()
    print(option_sina_cffex_hs300_list_df)

    option_sina_cffex_hs300_spot_df = option_sina_cffex_hs300_spot(contract="io2106")
    print(option_sina_cffex_hs300_spot_df)

    option_sina_cffex_hs300_daily_df = option_sina_cffex_hs300_daily(
        contract="io2106C3600"
    )
    print(option_sina_cffex_hs300_daily_df)

    # 期权-上交所-50ETF
    option_sina_sse_list_df = option_sina_sse_list(symbol="50ETF", exchange="null")
    print(option_sina_sse_list_df)

    option_sina_sse_expire_day_df = option_sina_sse_expire_day(
        trade_date="202101", symbol="50ETF", exchange="null"
    )
    print(option_sina_sse_expire_day_df)

    up, down = option_sina_sse_codes(
        trade_date="202012", underlying="510300"
    )
    print(up)
    print(down)

    option_sina_sse_spot_price_df = option_sina_sse_spot_price(code="10002497")
    print(option_sina_sse_spot_price_df)

    option_sina_sse_underlying_spot_price_df = option_sina_sse_underlying_spot_price(
        code="sh510300"
    )
    print(option_sina_sse_underlying_spot_price_df)

    option_sina_sse_greeks_df = option_sina_sse_greeks(code="10002498")
    print(option_sina_sse_greeks_df)

    option_sina_sse_minute_df = option_sina_sse_minute(code="10002498")
    print(option_sina_sse_minute_df)

    option_sina_sse_daily_df = option_sina_sse_daily(code="10002498")
    print(option_sina_sse_daily_df)

    option_sina_finance_minute_df = option_sina_finance_minute(code="10002498")
    print(option_sina_finance_minute_df)
