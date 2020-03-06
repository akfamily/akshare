## [AkShare](https://github.com/jindaxiang/akshare) 货币数据

### 货币最新报价

接口: currency_latest

目标地址: https://currencyscoop.com/

描述: 获取货币最新数据

限量: 单次返回主流数字货币当前时点行情数据

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
get_js_dc_current_df = ak.get_js_dc_current()
print(get_js_dc_current_df)
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
