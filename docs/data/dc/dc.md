## [AKShare](https://github.com/jindaxiang/akshare) 加密货币数据

### 实时数据

接口: crypto_js_spot

目标地址: https://datacenter.jin10.com/reportType/dc_bitcoin_current

描述: 获取加密货币实时行情, 实时更新

限量: 单次返回主流加密货币当前时点行情数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| reported_at      | str   | Y        | 日期时间-索引  |
| bourse      | float   | Y        | 市场   |
| currency_pair      | str   | Y        | 货币对代码  |
| price      | float   | Y        | 最新价(注意货币币种)   |
| up_down      | str   | Y        | 涨跌幅  |
| up_down_rate      | float   | Y        | -   |
| hightest_price      | str   | Y        | 24小时最高价(注意货币币种)  |
| lowest_price      | float   | Y        | 24小时最低价(注意货币币种)  |
| volume      | str   | Y        | 24小时成交量  |

接口示例

```python
import akshare as ak
crypto_js_spot_df = ak.crypto_js_spot()
print(crypto_js_spot_df)
```

数据示例

```
                             bourse currency_pair  ...  lowest_price        volume
reported_at                                        ...                            
2020-02-28 16:37:15    Bitfinex(香港)        LTCUSD  ...        59.666  83980.753551
2020-02-28 16:37:15    Bitflyer(日本)        BTCJPY  ...    940368.000   6566.954034
2020-02-28 16:37:15    Bitstamp(美国)        BTCUSD  ...      8585.470   6958.242385
2020-02-28 16:36:27      CEX.IO(伦敦)        BTCUSD  ...      8653.900    129.747383
2020-02-28 16:37:15  Kraken_EUR(美国)        BTCEUR  ...      7897.100   5300.456910
2020-02-28 16:36:27      Kraken(美国)        LTCUSD  ...        58.410  40829.390880
2020-02-28 16:36:27      OKCoin(中国)        BTCUSD  ...      8614.120    756.123400
2020-02-28 16:36:27    Bitfinex(香港)        BCHUSD  ...       312.050  10427.392214
2020-02-28 16:37:15    Bitfinex(香港)        BTCUSD  ...      8569.200   5229.230908
2020-02-28 16:37:15      Kraken(美国)        BTCUSD  ...      8553.200   3910.324878
```

### 历史数据

接口: crypto_hist

目标地址: https://cn.investing.com/crypto/ethereum/historical-data

描述: 获取加密货币的历史数据主要是日频, 周频和月频的数据; 该接口需要通过代理访问

限量: 单次返回指定加密货币, 频率和时间周期的数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| symbol | str | Y | symbol="以太坊"; 通过调用 **crypto_name_map** 获取所有货币对的名称|
| period | str | Y | period="每日"; choice of {"每日", "每周", "每月"} |
| start_date | str | Y | start_date="20191020" |
| end_date | str | Y | end_date="20201020" |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期时间-索引  |
| 收盘      | str   | Y        | 注意单位: 美元  |
| 开盘      | float   | Y        | 注意单位: 美元   |
| 高      | str   | Y        | 注意单位: 美元  |
| 低      | float   | Y        | 注意单位: 美元   |
| 交易量      | str   | Y        | 已简化  |
| 涨跌幅      | float   | Y        | 已简化   |

接口示例

```python
import akshare as ak
crypto_hist_df = ak.crypto_hist(symbol="瑞波币", period="每日", start_date="20151020", end_date="20201023")
print(crypto_hist_df)
```

数据示例

```
                 收盘       开盘        高        低           交易量     涨跌幅
日期                                                                  
2020-10-23  0.25645  0.25701  0.25917  0.25485  1.070000e+09 -0.0028
2020-10-22  0.25718  0.25105  0.26354  0.25083  1.100000e+09  0.0245
2020-10-21  0.25102  0.24324  0.25555  0.24261  1.120000e+09  0.0320
2020-10-20  0.24324  0.24564  0.25021  0.24155  1.040000e+09 -0.0095
2020-10-19  0.24558  0.24216  0.24942  0.24013  1.080000e+09  0.0134
             ...      ...      ...      ...           ...     ...
2015-10-24  0.00460  0.00460  0.00550  0.00460  0.000000e+00  0.0000
2015-10-23  0.00460  0.00450  0.00465  0.00450  0.000000e+00  0.0240
2015-10-22  0.00449  0.00460  0.00550  0.00449  8.300000e+02 -0.0235
2015-10-21  0.00460  0.00480  0.00480  0.00460  9.100000e+02 -0.0417
2015-10-20  0.00480  0.00508  0.00508  0.00453  9.000000e+01 -0.0553
```

### 持仓报告

#### 比特币持仓报告

接口: crypto_bitcoin_hold_report

目标地址: https://datacenter.jin10.com/dc_report?name=bitcoint

描述: 获取比特币持仓报告

限量: 单次返回当前时点的比特币持仓报告数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 代码      | str   | Y        | 日期时间-索引  |
| 公司名称-英文      | float   | Y        | -   |
| 公司名称-中文      | str   | Y        | -  |
| 国家/地区      | float   | Y        | -   |
| 市值      | str   | Y        | - |
| 比特币占市值比重      | float   | Y        | 注意单位: %    |
| 持仓成本      | str   | Y        |  - |
| 持仓占比      | float   | Y        | 注意单位: %  |
| 持仓量      | str   | Y        | -  |
| 当日持仓市值      | str   | Y        | -  |
| 查询日期      | str   | Y        | -  |
| 公告链接      | str   | Y        | -  |
| 分类      | str   | Y        | -  |
| 倍数      | str   | Y        | -  |

接口示例

```python
import akshare as ak
crypto_bitcoin_hold_report_df = ak.crypto_bitcoin_hold_report()
print(crypto_bitcoin_hold_report_df)
```

数据示例

```
               代码                           公司名称-英文  ...      分类   倍数
0       NADQ:MSTR                MicroStrategy inc.  ...    公开交易  2.2
1       NADQ:TSLA                       Tesla, Inc.  ...    公开交易  1.7
2         NADQ:SQ                       Square inc.  ...    公开交易  2.0
3       NADQ:MARA         Marathon Digital Holdings  ...    公开交易  1.7
4       NADQ:COIN             Coinbase Global, Inc.  ...    公开交易    1
5        TSE:GLXY           Galaxy Digital Holdings  ...    公开交易    1
6          ADE.DE                  Bitcoin Group SE  ...    公开交易    1
7       TSX:Hut-8                 Hut 8 Mining Corp  ...    公开交易  4.4
8        CSE:VYGR               Voyager Digital LTD  ...    公开交易  8.4
9       NADQ:RIOT             Riot Blockchain, Inc.  ...    公开交易  8.8
10        AKER:NO                         Seetee AS  ...    公开交易  1.1
11      SEHK:1357                             Meitu  ...    公开交易  1.0
12    OTCPK:ARBKF               Argo Blockchain PLC  ...    公开交易    1
13   OTCMKTS:CCTL                  Coin Citadel Inc  ...    公开交易  149
14      NADQ:BTBT                 Bit Digital, Inc.  ...    公开交易    1
15       CSE:BITF                  Bitfarms Limited  ...    公开交易  1.7
16       CSE:HODL          Cypherpunk Holdings Inc.  ...    公开交易    3
17       CVE:HIVE                   Hive Blockchain  ...    公开交易    1
18      CNSX:BIGG          BIGG Digital Assets Inc.  ...    公开交易  6.0
19         ABT:GR  Advanced Bitcoin Technologies AG  ...    公开交易  6.4
20     TSX-V:DMGI     DMG Blockchain Solutions Inc.  ...    公开交易    1
21        ASX:DCC                          DigitalX  ...    公开交易   13
22    TSXV:DGHI.V          Digihost Technology Inc.  ...    公开交易  1.4
23      TSXV:FORT               Fortress Blockchain  ...    公开交易    1
24  OTCMKTS:BNXAF                Banxa Holdings Inc  ...    公开交易    1
25       LON:MODE              Mode Global Holdings  ...    公开交易    5
26      TSXV:DASH         Neptune Dash Technologies  ...    公开交易    1
27     OTCQB:BTCS                         BTCS Inc.  ...    公开交易    1
28   OTCMKTS:FRMO                        FRMO Corp.  ...    公开交易    1
29      NADQ:MOGO                    MOGO Financing  ...    公开交易    1
30       NYSE:BLK                         BlackRock  ...    公开交易    1
31      IST:NETHL        Net Holding Anonim Sirketi  ...    公开交易  1.9
32           None                        MTGOX K.K.  ...      私募  111
33           None                         Block.one  ...      私募    1
34           None              The Tezos Foundation  ...      私募    1
35           None        Stone Ridge Holdings Group  ...      私募  4.8
36            gov                 Ukraine (various)  ...  政府人员持仓    1
37     OTCQX:GBTC           Grayscale Bitcoin Trust  ...   ETF相关  1.0
38     COINXBT:SS         CoinShares / XBT Provider  ...   ETF相关  4.9
39       LON:RICA     Ruffer Investment Company Ltd  ...   ETF相关  3.2
40     TSX:QBTC.U              3iQ The Bitcoin Fund  ...   ETF相关    1
41        BTCE:GR             ETC Group Bitcoin ETP  ...   ETF相关    1
42  TSX:BTCC(U/B)              Purpose Bitcoin  ETF  ...   ETF相关    1
43     OTCQX:BITW      Bitwise 10 Crypto Index Fund  ...   ETF相关    1
44       multiple                       21Shares AG  ...   ETF相关    1
45   OTCMKTS:GDLC  Grayscale Digital Large Cap Fund  ...   ETF相关    1
46        BTCW:SW                WisdomTree Bitcoin  ...   ETF相关    1
47     TSX:BITC.U           Ninepoint Bitcoin Trust  ...   ETF相关  1.7
48     TSX:BTCG.U            CI Galaxy Bitcoin Fund  ...   ETF相关    1
49     XETRA:VBTC        VanEck Vectors Bitcoin ETN  ...   ETF相关    1
50         UBTCTQ       Leonteq Bitcoin Tracker USD  ...   ETF相关    1
51           OBTC              Osprey Bitcoin Trust  ...   ETF相关    1
52      TSX: EBIT               Evolve Bitcoin  ETF  ...   ETF相关    1
53      NADQ:PHUN                    Phunware, Inc.  ...    公开交易    1
```

### CME-成交量报告

接口: crypto_bitcoin_cme

目标地址: https://datacenter.jin10.com/reportType/dc_cme_btc_report

描述: 获取芝加哥商业交易所-比特币成交量报告

限量: 单次返回指定交易日的比特币成交量报告数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| date | str | Y | date="20210621" |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 商品      | object   | Y        | -  |
| 类型      | object   | Y        | -   |
| 电子交易合约      | int64   | Y        | -  |
| 场内成交合约      | int64   | Y        | -   |
| 场外成交合约      | int64   | Y        | - |
| 成交量      | int64   | Y        | -    |
| 未平仓合约      | int64   | Y        |  - |
| 持仓变化      | int64   | Y        | -  |

接口示例

```python
import akshare as ak
crypto_bitcoin_cme_df = ak.crypto_bitcoin_cme(date="20210621")
print(crypto_bitcoin_cme_df)
```

数据示例

```
    商品  类型  电子交易合约  场内成交合约  场外成交合约    成交量  未平仓合约  持仓变化
0    比特币  期货   13015       0      15  13030   8126   -90
1    比特币  期权      72       0       0     72   1325    32
2    比特币  看涨      38       0       0     38    525    34
3    比特币  看跌      34       0       0     34    800    -2
4  微型比特币  期货   35368       0       0  35368  26779  5551
```

### 加密货币全球市场指数

接口: crypto_crix

目标地址: https://thecrix.de/

描述: 获取加密货币全球市场指数

限量: 单次返回指定 symbol 的历史数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| symbol | str | Y | symbol="CRIX"; choice of {"CRIX", "VCRIX"} |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| date      | object   | Y        | - |
| value      | float64   | Y        | 访问 [thecrix](https://thecrix.de/) 了解定义   |

接口示例

```python
import akshare as ak
crypto_crix_df = ak.crypto_crix(symbol="CRIX")
print(crypto_crix_df)
```

数据示例

```
           date      value
0     2014-07-31    1000.00
1     2014-08-01    1018.20
2     2014-08-02    1008.77
3     2014-08-03    1004.42
4     2014-08-04    1004.98
          ...        ...
2516  2021-06-20   99857.76
2517  2021-06-21  100771.09
2518  2021-06-22   89383.27
2519  2021-06-23   90074.02
2520  2021-06-24   94013.24
```
