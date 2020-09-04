# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/10/30 11:28
Desc: 新浪财经-所有指数-实时行情数据和历史行情数据
优化: 在指数行情的获取上采用多线程模式(新浪会封IP, 不再优化)
"""
import re
import datetime

import requests
import demjson
import pandas as pd
import execjs

from akshare.index.cons import (
    zh_sina_index_stock_payload,
    zh_sina_index_stock_url,
    zh_sina_index_stock_count_url,
    zh_sina_index_stock_hist_url,
)
from akshare.stock.cons import hk_js_decode


def get_zh_index_page_count() -> int:
    """
    所有指数的总页数
    http://vip.stock.finance.sina.com.cn/mkt/#hs_s
    :return: int 需要抓取的指数的总页数
    """
    res = requests.get(zh_sina_index_stock_count_url)
    page_count = int(re.findall(re.compile(r"\d+"), res.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1


def stock_zh_index_spot() -> pd.DataFrame:
    """
    从新浪财经-指数获取所有指数的实时行情数据, 大量抓取容易封IP
    http://vip.stock.finance.sina.com.cn/mkt/#hs_s
    :return: pandas.DataFrame
           symbol   name      trade pricechange changepercent buy sell settlement  \
    0    sh000001   上证指数  2891.3431     -18.527        -0.637   0    0  2909.8697
    1    sh000002   Ａ股指数  3029.2626     -19.372        -0.635   0    0  3048.6349
    2    sh000003   Ｂ股指数   255.2202      -2.955        -1.145   0    0   258.1752
    3    sh000004   工业指数  2265.4238     -19.259        -0.843   0    0  2284.6832
    4    sh000005   商业指数  2625.3647     -31.024        -1.168   0    0  2656.3890
    ..        ...    ...        ...         ...           ...  ..  ...        ...
    635  sh000079   公用等权  1855.8680     -26.981        -1.433   0    0  1882.8489
    636  sh000090   上证流通  1085.5027      -7.803        -0.714   0    0  1093.3057
    637  sh000091   沪财中小  7327.8375     -95.106        -1.281   0    0  7422.9430
    638  sh000092   资源50  2068.8152     -21.561        -1.031   0    0  2090.3766
    639  sh000093  180分层  9200.0115     -89.053        -0.959   0    0  9289.0642
              open       high        low     volume        amount    code  \
    0    2911.3500  2917.8293  2891.2043  135519463  152576392736  000001
    1    3050.1878  3057.0351  3029.1168  135417123  152529532272  000002
    2     258.2375   258.2375   255.2202     102341      46860464  000003
    3    2284.4955  2288.8948  2265.4238   81989859  100573430149  000004
    4    2654.1212  2661.1885  2624.7153    9706663   10959125999  000005
    ..         ...        ...        ...        ...           ...     ...
    635  1880.9163  1881.3908  1855.6935    3771090    2602021459  000079
    636  1093.7894  1095.7378  1085.5027  132459529  141897444366  000090
    637  7416.8197  7417.4444  7326.1919   14811864   17551488362  000091
    638  2089.1099  2089.8730  2068.8152    9466656    8101366245  000092
    639  9287.6393  9302.3461  9200.0115   49017964   59840452615  000093
         ticktime
    0    15:02:03
    1    15:02:03
    2    15:02:03
    3    15:02:03
    4    15:02:03
    ..        ...
    635  15:02:03
    636  15:02:03
    637  15:02:03
    638  15:02:03
    639  15:02:03
    """
    big_df = pd.DataFrame()
    page_count = get_zh_index_page_count()
    zh_sina_stock_payload_copy = zh_sina_index_stock_payload.copy()
    for page in range(1, page_count + 1):
        # print(page)
        zh_sina_stock_payload_copy.update({"page": page})
        res = requests.get(zh_sina_index_stock_url, params=zh_sina_stock_payload_copy)
        data_json = demjson.decode(res.text)
        big_df = big_df.append(pd.DataFrame(data_json), ignore_index=True)
    return big_df


def stock_zh_index_daily(symbol: str = "sh000922") -> pd.DataFrame:
    """
    新浪财经-指数获取某个指数的历史行情数据, 大量抓取容易封IP
    :param symbol: str e.g., sz399998
    :return: pandas.DataFrame
                    open      high       low     close      volume
    date
    2015-06-16  2526.056  2577.092  2469.216  2487.513  2224345088
    2015-06-17  2476.863  2567.842  2422.229  2560.914  2181699840
    2015-06-18  2553.739  2587.655  2480.321  2480.674  2032781312
    2015-06-19  2431.218  2453.794  2286.967  2287.758  1687013248
    2015-06-23  2280.189  2341.795  2156.396  2341.359  1627453440
                  ...       ...       ...       ...         ...
    2019-11-11  1210.968  1210.968  1182.442  1182.718   415074658
    2019-11-12  1184.118  1196.425  1184.005  1195.790   397246387
    2019-11-13  1195.925  1195.925  1180.293  1185.293   334027614
    2019-11-14  1185.788  1187.431  1178.414  1180.791   271514767
    2019-11-15  1181.090  1181.739  1165.898  1166.536   338309880
    """
    params = {"d": "2020_2_4"}
    res = requests.get(zh_sina_index_stock_hist_url.format(symbol), params=params)
    js_code = execjs.compile(hk_js_decode)
    dict_list = js_code.call(
        "d", res.text.split("=")[1].split(";")[0].replace('"', "")
    )  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df["date"] = data_df["date"].str.split("T", expand=True).iloc[:, 0]
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["date"]
    data_df = data_df.astype("float")
    return data_df


def _get_tx_start_year(symbol: str = "sh000922") -> pd.DataFrame:
    """
    腾讯证券-获取有股票数据的第一天, 注意这个数据是腾讯证券的历史数据第一天
    http://gu.qq.com/sh000919/zs
    :param symbol: 带市场标识的股票代码
    :type symbol: str
    :return: 开始日期
    :rtype: pandas.DataFrame
    """
    url = "http://web.ifzq.gtimg.cn/other/klineweb/klineWeb/weekTrends"
    params = {
        "code": symbol,
        "type": "qfq",
        "_var": "trend_qfq",
        "r": "0.3506048543943414",
    }
    res = requests.get(url, params=params)
    text = res.text
    start_date = demjson.decode(text[text.find("={") + 1 :])["data"][0][0]
    return start_date


def stock_zh_index_daily_tx(symbol: str = "sz000858") -> pd.DataFrame:
    """
    腾讯证券-日频-股票或者指数历史数据
    作为 stock_zh_index_daily 的补充, 因为在新浪中有部分指数数据缺失
    注意都是: 前复权, 不同网站复权方式不同, 不可混用数据
    http://gu.qq.com/sh000919/zs
    :param symbol: 带市场标识的股票或者指数代码
    :type symbol: str
    :return: 后复权的股票和指数数据
    :rtype: pandas.DataFrame
    """
    start_date = _get_tx_start_year(symbol=symbol)
    url = "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
    range_start = int(start_date.split("-")[0])
    range_end = datetime.date.today().year + 1
    temp_df = pd.DataFrame()
    for year in range(range_start, range_end):
        params = {
            "_var": f"kline_dayqfq{year}",
            "param": f"{symbol},day,{year}-01-01,{year + 1}-12-31,640,qfq",
            "r": "0.8205512681390605",
        }
        res = requests.get(url, params=params)
        text = res.text
        try:
            inner_temp_df = pd.DataFrame(
                demjson.decode(text[text.find("={") + 1:])["data"][symbol]["day"]
            )
        except:
            inner_temp_df = pd.DataFrame(
                demjson.decode(text[text.find("={") + 1:])["data"][symbol]["qfqday"]
            )
        temp_df = temp_df.append(inner_temp_df, ignore_index=True)
    if temp_df.shape[1] == 6:
        temp_df.columns = ["date", "open", "close", "high", "low", "amount"]
    else:
        temp_df = temp_df.iloc[:, :6]
        temp_df.columns = ["date", "open", "close", "high", "low", "amount"]
    temp_df.index = pd.to_datetime(temp_df["date"])
    del temp_df["date"]
    temp_df = temp_df.astype("float")
    temp_df.drop_duplicates(inplace=True)
    return temp_df


def stock_zh_index_daily_em(symbol: str = "sh000913") -> pd.DataFrame:
    """
    东方财富股票指数数据
    http://quote.eastmoney.com/center/hszs.html
    :param symbol: 带市场标识的指数代码
    :type symbol: str
    :return: 指数数据
    :rtype: pandas.DataFrame
    """
    market_map = {"sz": "0", "sh": "1"}
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "cb": "jQuery1124033485574041163946_1596700547000",
        "secid": f"{market_map[symbol[:2]]}.{symbol[2:]}",
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
        "klt": "101",  # 日频率
        "fqt": "0",
        "beg": "19900101",
        "end": "20220101",
        "_": "1596700547039",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):-2])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
    temp_df.columns = ["date", "open", "close", "high", "low", "volume", "amount", "_"]
    temp_df = temp_df[["date", "open", "close", "high", "low", "volume", "amount"]]
    temp_df = temp_df.astype({
        "open": float,
        "close": float,
        "high": float,
        "low": float,
        "volume": float,
        "amount": float,
    })
    return temp_df


if __name__ == "__main__":
    stock_zh_index_daily_df = stock_zh_index_daily(symbol="sz399812")
    print(stock_zh_index_daily_df)

    stock_zh_index_spot_df = stock_zh_index_spot()
    print(stock_zh_index_spot_df)

    stock_zh_index_daily_tx_df = stock_zh_index_daily_tx(symbol="sz000858")
    print(stock_zh_index_daily_tx_df)

    stock_zh_index_daily_em_df = stock_zh_index_daily_em(symbol="sz399812")
    print(stock_zh_index_daily_em_df)
