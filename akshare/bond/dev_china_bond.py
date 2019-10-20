# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/18 10:24
contact: jindaxiang@163.com
desc: 获取中国外汇交易中心暨全国银行间同业拆借中心-市场数据-市场行情-债券市场行情
现券市场做市报价: get_bond_market_quote
现券市场成交行情: get_bond_market_trade
"""
import requests
import pandas as pd

from akshare.bond.cons import (SHORT_HEADERS,
                               MARKET_QUOTE_PAYLOAD,
                               MARKET_QUOTE_URL,
                               MARKET_TRADE_URL,
                               MARKET_TRADE_PAYLOAD)


def get_bond_market_quote():
    """
    中国外汇交易中心暨全国银行间同业拆借中心-市场数据-市场行情-债券市场行情-现券市场成交行情
    :return: pandas.DataFrame
             abdAssetEncdFullDescByRmb        tradeAmnt abdAssetEncdShrtDescByRmb  \
    0                               100.50 / 101.32
    1                                99.54 / 100.33
    2                                99.85 / 100.28
    3                               100.18 / 100.42
    4                                 99.35 / 99.74
                            ...              ...                       ...
    4539                              96.80 / 97.29
    4540                              96.89 / 97.12
    4541                              96.87 / 97.24
    4542                            110.67 / 118.18
    4543                            105.60 / 111.66
         contraRateByRmb   bondcode abdAssetEncdShrtDesc        code  \
    0                        190006             19附息国债06  76008ir9yz
    1                        190210               19国开10  75808ppkkk
    2                        190208               19国开08  81257k1w48
    3                        190207               19国开07  752516byyl
    4                        190203               19国开03  6344929pu6
                  ...        ...                  ...         ...
    4539                  111907080          19招商银行CD080  7659607080
    4540                  111906014          19交通银行CD014  6259506014
    4541                  111908046          19中信银行CD046  6965108046
    4542                    1480134              14国网债02  1000045704
    4543                    1280107              12国网债02  1000034728
         emaEntyEncdFullDescByRmb qbdEntryTrnsctDateTmst emaEntyEncdShrtDesc  \
    0                                                                   民生银行
    1                                                                   民生银行
    2                                                                   民生银行
    3                                                                   民生银行
    4                                                                   民生银行
                           ...                    ...                 ...
    4539                                                                中国银行
    4540                                                                中国银行
    4541                                                                中国银行
    4542                                                              国泰君安证券
    4543                                                              国泰君安证券
         qbdQuoteDate inptTp abdAssetEncdShrtDescEN       contraRate  \
    0                      0                         3.2288 / 3.1288
    1                      0                         3.7063 / 3.6063
    2                      0                         3.4525 / 3.3525
    3                      0                         3.1025 / 3.0025
    4                      0                         3.4638 / 3.3638
               ...    ...                    ...              ...
    4539                   0                         3.3008 / 2.4278
    4540                   0                         3.3125 / 2.3913
    4541                   0                         3.3069 / 2.4249
    4542                   0                         4.5732 / 3.6732
    4543                   0                         4.3622 / 3.4622
         emaEntyEncdShrtDescByRmb emaEntyEncdShrtDescEN
    0                                              MSBK
    1                                              MSBK
    2                                              MSBK
    3                                              MSBK
    4                                              MSBK
                           ...                   ...
    4539                                            BOC
    4540                                            BOC
    4541                                            BOC
    4542                                           GTJA
    4543                                           GTJA
    """
    res = requests.post(MARKET_QUOTE_URL, data=MARKET_QUOTE_PAYLOAD, headers=SHORT_HEADERS)
    return pd.DataFrame(res.json()["records"])


def get_bond_market_trade():
    """
    中国外汇交易中心暨全国银行间同业拆借中心-市场数据-市场行情-债券市场行情-现券市场做市报价
    :return: pandas.DataFrame
             abdAssetEncdFullDescByRmb dmiLatestRateLabel  bpNum  \
    0                       19国开10             100.07  -0.93
    1                       19国开15              99.05   0.50
    2                     19附息国债06             100.90   7.83
    3                     19附息国债03              99.84   0.72
    4                     19附息国债04             100.83   1.25
                            ...                ...    ...
    1164               17今世缘MTN002             102.60   1.06
    1165                 19天业CP001             100.27   1.93
    1166                 17诸暨国资债01             103.17   2.64
    1167                  17附息国债06             101.07  -6.60
    1168                  18附息国债01             103.08  -1.10
         abdAssetEncdShrtDescByRmb bpLabel blank dmiTtlTradedAmnt  \
    0                       19国开10          None         756.3200
    1                       19国开15          None         189.3000
    2                     19附息国债06          None         153.7400
    3                     19附息国债03          None         153.4230
    4                     19附息国债04          None         122.1650
                            ...     ...   ...              ...
    1164                 17今世缘MTN0          None           0.0200
    1165                 19天业CP001          None           0.0200
    1166                   17诸暨国资�          None           0.0200
    1167                  17附息国债06          None           0.0050
    1168                  18附息国债01          None           0.0020
         dmiTtlTradedAmntLabel dmiLatestContraRateLabel   bondcode  \
    0                 756.3200                   3.6395     190210
    1                 189.3000                   3.5650     190215
    2                 153.7400                   3.1800     190006
    3                 153.4230                   2.7550     190003
    4                 122.1650                   2.9850     190004
                        ...                      ...        ...
    1164                0.0200                   5.0006  101753013
    1165                0.0200                   3.6293  041900345
    1166                0.0200                   4.0464    1780124
    1167                0.0050                   2.9340     170006
    1168                0.0020                   2.7990     180001
         abdAssetEncdShrtDesc        code             showDate  \
    0                  19国开10  75808ppkkk  2019-10-18 16:41:11
    1                  19国开15  92893523p5  2019-10-18 16:40:00
    2                19附息国债06  76008ir9yz  2019-10-18 16:36:56
    3                19附息国债03  664521tbo4  2019-10-18 16:31:11
    4                19附息国债04  70854w2ml3  2019-10-18 16:26:32
                       ...         ...                  ...
    1164          17今世缘MTN002  9578653013  2019-10-18 15:57:37
    1165            19天业CP001  90962lmhtp  2019-10-18 15:57:37
    1166            17诸暨国资债01  1000103754  2019-10-18 14:53:47
    1167             17附息国债06  1000093201  2019-10-18 14:51:07
    1168             18附息国债01  1000125437  2019-10-18 14:50:51
         dmiPrvsClsngContraRate    bp dmiLatestContraRate dmiWghtdContraRate  \
    0                      None  0.93              3.6395             3.6444
    1                      None  0.50              3.5650             3.5629
    2                      None  7.83              3.1800             3.1646
    3                      None  0.72              2.7550             2.7512
    4                      None  1.25              2.9850             2.9826
                         ...   ...                 ...                ...
    1164                   None  1.06              5.0006             5.0006
    1165                   None  1.93              3.6293             3.6293
    1166                   None  2.64              4.0464             4.0464
    1167                   None  6.60              2.9340             2.9340
    1168                   None  1.10              2.7990             2.7990
         dmiWghtdContraRateLabel inptTp dmiLatestRate
    0                     3.6444      0        100.07
    1                     3.5629      0         99.05
    2                     3.1646      0        100.90
    3                     2.7512      0         99.84
    4                     2.9826      0        100.83
                          ...    ...           ...
    1164                  5.0006      0        102.60
    1165                  3.6293      0        100.27
    1166                  4.0464      0        103.17
    1167                  2.9340      0        101.07
    1168                  2.7990      0        103.08
    """
    res = requests.post(MARKET_TRADE_URL, data=MARKET_TRADE_PAYLOAD, headers=SHORT_HEADERS)
    return pd.DataFrame(res.json()["records"])


if __name__ == "__main__":
    df = get_bond_market_quote()
    print(df)
    df = get_bond_market_trade()
    print(df)
