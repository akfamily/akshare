# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/10/30 11:28
Desc: 新浪财经-A股-实时行情数据和历史行情数据(包含前复权和后复权因子)
"""
import re
import json

import demjson
import execjs
import pandas as pd
import requests
from tqdm import tqdm

from akshare.stock.cons import (zh_sina_a_stock_payload,
                                zh_sina_a_stock_url,
                                zh_sina_a_stock_count_url,
                                zh_sina_a_stock_hist_url,
                                hk_js_decode,
                                zh_sina_a_stock_hfq_url,
                                zh_sina_a_stock_qfq_url,
                                zh_sina_a_stock_amount_url)


def _get_zh_a_page_count() -> int:
    """
    所有股票的总页数
    http://vip.stock.finance.sina.com.cn/mkt/#hs_a
    :return: 需要抓取的股票总页数
    :rtype: int
    """
    res = requests.get(zh_sina_a_stock_count_url)
    page_count = int(re.findall(re.compile(r"\d+"), res.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1


def stock_zh_a_spot() -> pd.DataFrame:
    """
    从新浪财经-A股获取所有A股的实时行情数据, 重复运行本函数会被新浪暂时封 IP
    http://vip.stock.finance.sina.com.cn/mkt/#qbgg_hk
    :return: pandas.DataFrame
                symbol    code  name   trade pricechange changepercent     buy  \
    0     sh600000  600000  浦发银行  12.920      -0.030        -0.232  12.920
    1     sh600004  600004  白云机场  18.110      -0.370        -2.002  18.110
    2     sh600006  600006  东风汽车   4.410      -0.030        -0.676   4.410
    3     sh600007  600007  中国国贸  17.240      -0.360        -2.045  17.240
    4     sh600008  600008  首创股份   3.320      -0.030        -0.896   3.310
            ...     ...   ...     ...         ...           ...     ...
    3755  sh600096  600096   云天化   5.270      -0.220        -4.007   5.270
    3756  sh600097  600097  开创国际  10.180      -0.120        -1.165  10.180
    3757  sh600098  600098  广州发展   6.550      -0.040        -0.607   6.540
    3758  sh600099  600099  林海股份   6.540      -0.150        -2.242   6.540
    3759  sh600100  600100  同方股份   8.200      -0.100        -1.205   8.200
            sell settlement    open    high     low    volume     amount  \
    0     12.930     12.950  12.950  13.100  12.860  46023920  597016896
    1     18.120     18.480  18.510  18.510  17.880  24175071  437419344
    2      4.420      4.440   4.490   4.490   4.410   4304900   19130233
    3     17.280     17.600  17.670  17.670  17.220    684801   11879731
    4      3.320      3.350   3.360   3.360   3.300   8284294   27579688
          ...        ...     ...     ...     ...       ...        ...
    3755   5.280      5.490   5.490   5.500   5.220  16964636   90595172
    3756  10.190     10.300  10.220  10.340  10.090   1001676   10231669
    3757   6.550      6.590   6.560   6.620   6.500   1996449   13098901
    3758   6.580      6.690   6.650   6.680   6.530   1866180   12314997
    3759   8.210      8.300   8.300   8.310   8.120  12087236   99281447
          ticktime      per     pb        mktcap           nmc  turnoverratio
    0     15:00:00    6.984  0.790  3.792289e+07  3.631006e+07        0.16376
    1     15:00:07   32.927  2.365  3.747539e+06  3.747539e+06        1.16826
    2     15:00:02   15.926  1.207  8.820000e+05  8.820000e+05        0.21525
    3     15:00:02   22.390  2.367  1.736555e+06  1.736555e+06        0.06798
    4     15:00:07   22.912  1.730  1.887569e+06  1.600444e+06        0.17185
            ...      ...    ...           ...           ...            ...
    3755  15:00:00   56.728  1.566  7.523847e+05  6.963668e+05        1.28386
    3756  15:00:00   17.552  1.434  2.452734e+05  2.303459e+05        0.44268
    3757  15:00:00   25.476  1.059  1.785659e+06  1.785659e+06        0.07323
    3758  15:00:00  540.496  3.023  1.433045e+05  1.433045e+05        0.85167
    3759  15:00:07   -6.264  1.465  2.430397e+06  2.430397e+06        0.40782
    """
    big_df = pd.DataFrame()
    page_count = _get_zh_a_page_count()
    zh_sina_stock_payload_copy = zh_sina_a_stock_payload.copy()
    for page in tqdm(range(1, page_count+1), desc="Please wait for a moment"):
        zh_sina_stock_payload_copy.update({"page": page})
        r = requests.get(
            zh_sina_a_stock_url,
            params=zh_sina_stock_payload_copy)
        data_json = demjson.decode(r.text)
        big_df = big_df.append(pd.DataFrame(data_json), ignore_index=True)
    big_df = big_df.astype({"trade": "float",
                            "pricechange": "float",
                            "changepercent": "float",
                            "buy": "float",
                            "sell": "float",
                            "settlement": "float",
                            "open": "float",
                            "high": "float",
                            "low": "float",
                            "volume": "float",
                            "amount": "float",
                            "per": "float",
                            "pb": "float",
                            "mktcap": "float",
                            "nmc": "float",
                            "turnoverratio": "float",
                            })
    return big_df


def stock_zh_a_daily(symbol: str = "sz000613", adjust: str = "") -> pd.DataFrame:
    """
    新浪财经-A股-个股的历史行情数据, 大量抓取容易封IP
    :param symbol: sh600000
    :type symbol: str
    :param adjust: 默认为空: 返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据; hfq-factor: 返回后复权因子; hfq-factor: 返回前复权因子
    :type adjust: str
    :return: specific data
    :rtype: pandas.DataFrame
    """
    res = requests.get(zh_sina_a_stock_hist_url.format(symbol))
    js_code = execjs.compile(hk_js_decode)
    dict_list = js_code.call(
        'd', res.text.split("=")[1].split(";")[0].replace(
            '"', ""))  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df["date"] = data_df["date"].str.split("T", expand=True).iloc[:, 0]
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["date"]
    data_df = data_df.astype("float")

    r = requests.get(zh_sina_a_stock_amount_url.format(symbol, symbol))
    amount_data_json = demjson.decode(r.text[r.text.find("["): r.text.rfind("]") + 1])
    amount_data_df = pd.DataFrame(amount_data_json)
    amount_data_df.index = pd.to_datetime(amount_data_df.date)
    del amount_data_df["date"]
    temp_df = pd.merge(data_df, amount_data_df, left_index=True, right_index=True, how="outer")
    temp_df.fillna(method="ffill", inplace=True)
    temp_df = temp_df.astype(float)
    temp_df["amount"] = temp_df["amount"] * 10000
    temp_df["turnover"] = temp_df["volume"] / temp_df["amount"]
    temp_df.columns = ['open', 'high', 'low', 'close', 'volume', 'outstanding_share', 'turnover']

    if adjust == "":
        return temp_df

    if adjust == "hfq":
        res = requests.get(zh_sina_a_stock_hfq_url.format(symbol))
        hfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])['data'])
        hfq_factor_df.columns = ["date", "hfq_factor"]
        hfq_factor_df.index = pd.to_datetime(hfq_factor_df.date)
        del hfq_factor_df["date"]

        temp_df = pd.merge(
            temp_df, hfq_factor_df, left_index=True, right_index=True, how="left"
        )
        temp_df.fillna(method="ffill", inplace=True)
        temp_df = temp_df.astype(float)
        temp_df["open"] = temp_df["open"] * temp_df["hfq_factor"]
        temp_df["high"] = temp_df["high"] * temp_df["hfq_factor"]
        temp_df["close"] = temp_df["close"] * temp_df["hfq_factor"]
        temp_df["low"] = temp_df["low"] * temp_df["hfq_factor"]
        return temp_df.iloc[:, :-1]

    if adjust == "qfq":
        res = requests.get(zh_sina_a_stock_qfq_url.format(symbol))
        qfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])['data'])
        qfq_factor_df.columns = ["date", "qfq_factor"]
        qfq_factor_df.index = pd.to_datetime(qfq_factor_df.date)
        del qfq_factor_df["date"]

        temp_df = pd.merge(
            temp_df, qfq_factor_df, left_index=True, right_index=True, how="left"
        )
        temp_df.fillna(method="ffill", inplace=True)
        temp_df = temp_df.astype(float)
        temp_df["open"] = temp_df["open"] / temp_df["qfq_factor"]
        temp_df["high"] = temp_df["high"] / temp_df["qfq_factor"]
        temp_df["close"] = temp_df["close"] / temp_df["qfq_factor"]
        temp_df["low"] = temp_df["low"] / temp_df["qfq_factor"]
        return temp_df.iloc[:, :-1]

    if adjust == "hfq-factor":
        res = requests.get(zh_sina_a_stock_hfq_url.format(symbol))
        hfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])['data'])
        hfq_factor_df.columns = ["date", "hfq_factor"]
        hfq_factor_df.index = pd.to_datetime(hfq_factor_df.date)
        del hfq_factor_df["date"]
        return hfq_factor_df

    if adjust == "qfq-factor":
        res = requests.get(zh_sina_a_stock_qfq_url.format(symbol))
        qfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])['data'])
        qfq_factor_df.columns = ["date", "qfq_factor"]
        qfq_factor_df.index = pd.to_datetime(qfq_factor_df.date)
        del qfq_factor_df["date"]
        return qfq_factor_df


def stock_zh_a_minute(symbol: str = 'sh000300', period: str = '1') -> pd.DataFrame:
    """
    股票及股票指数历史行情数据-分钟数据
    http://finance.sina.com.cn/realstock/company/sh600519/nc.shtml
    :param symbol: sh000300
    :type symbol: str
    :param period: 1, 5, 15, 30, 60 分钟的数据
    :type period: str
    :return: specific data
    :rtype: pandas.DataFrame
    """
    url = "https://quotes.sina.cn/cn/api/jsonp_v2.php/=/CN_MarketDataService.getKLineData"
    params = {
        "symbol": symbol,
        "scale": period,
        "datalen": "1023",
    }
    r = requests.get(url, params=params)
    temp_df = pd.DataFrame(json.loads(r.text.split('=(')[1].split(");")[0]))
    return temp_df


if __name__ == "__main__":
    stock_zh_a_daily_hfq_df = stock_zh_a_daily(symbol="sh600582", adjust="qfq-factor")
    print(stock_zh_a_daily_hfq_df)
    stock_zh_a_daily_df = stock_zh_a_daily(symbol="sh600582")
    print(stock_zh_a_daily_df)
    stock_zh_a_spot_df = stock_zh_a_spot()
    print(stock_zh_a_spot_df)
    stock_zh_a_minute_df = stock_zh_a_minute(symbol='sh600582', period='1')
    print(stock_zh_a_minute_df)
