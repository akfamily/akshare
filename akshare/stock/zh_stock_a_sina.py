# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/30 11:28
contact: jindaxiang@163.com
desc: 新浪财经-A股-实时行情数据和历史行情数据(包含前复权和后复权因子)
优化: 在A股行情的获取上采用多线程模式(新浪会封IP, 不再优化)
"""
import re

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
                                zh_sina_a_stock_qfq_url)


def get_zh_a_page_count():
    """
    所有股票的总页数
    http://vip.stock.finance.sina.com.cn/mkt/#hs_a
    :return: int 需要抓取的股票总页数
    """
    res = requests.get(zh_sina_a_stock_count_url)
    page_count = int(re.findall(re.compile(r"\d+"), res.text)[0]) / 80
    if isinstance(page_count, int):
        return page_count
    else:
        return int(page_count) + 1


def stock_zh_a_spot():
    """
    从新浪财经-A股获取所有A股的实时行情数据, 大量抓取容易封IP
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
    page_count = get_zh_a_page_count()
    zh_sina_stock_payload_copy = zh_sina_a_stock_payload.copy()
    for page in tqdm(range(1, page_count+1), desc="Please wait for a moment"):
        zh_sina_stock_payload_copy.update({"page": page})
        res = requests.get(
            zh_sina_a_stock_url,
            params=zh_sina_stock_payload_copy)
        data_json = demjson.decode(res.text)
        big_df = big_df.append(pd.DataFrame(data_json), ignore_index=True)
    return big_df


def stock_zh_a_daily(symbol="sh600000", factor=""):
    """
    新浪财经-A股获取某个股票的历史行情数据, 大量抓取容易封IP
    :param symbol: str sh600000
    :param factor: str 默认为空, 不复权; qfq, 前复权因子; hfq, 后复权因子;
    :return: pandas.DataFrame
    不复权数据
                     open   high    low  close     volume
    date
    1999-11-10  29.50  29.80  27.00  27.75  174085100
    1999-11-11  27.58  28.38  27.53  27.71   29403500
    1999-11-12  27.86  28.30  27.77  28.05   15008000
    1999-11-15  28.20  28.25  27.70  27.75   11921100
    1999-11-16  27.88  27.97  26.48  26.55   23223100
               ...    ...    ...    ...        ...
    2019-10-30  12.75  12.79  12.52  12.59   53734730
    2019-10-31  12.68  12.70  12.50  12.51   33347533
    2019-11-01  12.50  12.83  12.44  12.75   62705733
    2019-11-04  12.75  12.89  12.69  12.74   49737996
    2019-11-05  12.74  13.19  12.69  12.95   74274389

    后复权因子
                  date           hfq_factor
    0   2019-06-11  12.7227249211316980
    1   2018-07-13  12.3391802422000990
    2   2017-05-25  12.2102441895126000
    3   2016-06-23   9.2710670167499010
    4   2015-06-23   8.1856186501361000
    5   2014-06-24   7.8226125975203010
    6   2013-06-03   7.2881483827828000
    7   2012-06-26   6.9052943607646000
    8   2011-06-03   6.6571999525935000
    9   2010-06-10   5.0588982345161000
    10  2009-06-09   3.8599078005559000
    11  2008-04-24   2.7363470981385000
    12  2007-07-18   2.0953391363342000
    13  2006-05-25   2.0866878599662000
    14  2006-05-12   2.0595609177866000
    15  2005-05-12   1.5842776290666000
    16  2004-05-20   1.5573493974111000
    17  2003-06-23   1.5391056877503000
    18  2002-08-22   1.5263436173709000
    19  2000-07-06   1.0065019505852000
    20  1999-11-10   1.0000000000000000
    21  1900-01-01   1.0000000000000000

    前复权因子
                  date           qfq_factor
    0   2019-06-11   1.0000000000000000
    1   2018-07-13   1.0310834813499000
    2   2017-05-25   1.0419713745004000
    3   2016-06-23   1.3723042771825000
    4   2015-06-23   1.5542777479525000
    5   2014-06-24   1.6264035528443000
    6   2013-06-03   1.7456731467196000
    7   2012-06-26   1.8424594602978000
    8   2011-06-03   1.9111225457747000
    9   2010-06-10   2.5149201133019000
    10  2009-06-09   3.2961214563983000
    11  2008-04-24   4.6495289028892000
    12  2007-07-18   6.0719168083645000
    13  2006-05-25   6.0970905928105000
    14  2006-05-12   6.1773967505679000
    15  2005-05-12   8.0306157757383010
    16  2004-05-20   8.1694736854052000
    17  2003-06-23   8.2663101191762000
    18  2002-08-22   8.3354264245204000
    19  2000-07-06  12.6405367756464000
    20  1999-11-10  12.7227249211316980
    21  1900-01-01  12.7227249211316980
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
    data_df.astype("float")
    if not factor:
        return data_df
    if factor == "hfq":
        res = requests.get(zh_sina_a_stock_hfq_url.format(symbol))
        hfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])['data'])
        hfq_factor_df.columns = ["date", "hfq_factor"]
        return hfq_factor_df
    if factor == "qfq":
        res = requests.get(zh_sina_a_stock_qfq_url.format(symbol))
        qfq_factor_df = pd.DataFrame(
            eval(res.text.split("=")[1].split("\n")[0])['data'])
        qfq_factor_df.columns = ["date", "qfq_factor"]
        return qfq_factor_df


if __name__ == "__main__":
    stock_zh_a_daily_qfq_df = stock_zh_a_daily(symbol="sh600582", factor="qfq")
    print(stock_zh_a_daily_qfq_df)
    stock_zh_a_daily_df = stock_zh_a_daily(symbol="sh600582")
    print(stock_zh_a_daily_df)
    stock_zh_a_spot_df = stock_zh_a_spot()
    print(stock_zh_a_spot_df)
