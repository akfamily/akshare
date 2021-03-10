## [AKShare](https://github.com/jindaxiang/akshare) 货币数据

### 货币报价最新数据

接口: currency_latest

目标地址: https://currencyscoop.com/

描述: 获取货币报价最新数据

限量: 单次返回指定货币的最新报价数据-免费账号每月限量访问 5000 次

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| base | str | Y | base="USD" |
| api_key | str | Y | api_key="Please put your api key here"; you can register [currencyscoop](https://currencyscoop.com/), [Gmail](http://mail.google.com/) well be better |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| date      | str   | Y        | 日期时间-注意时区  |
| base      | float   | Y        | 货币   |
| rates      | str   | Y        | 比率  |

接口示例

```python
import akshare as ak
currency_latest_df = ak.currency_latest(base="USD", api_key="Please put your api key here")
print(currency_latest_df)
```

数据示例

```
                         date base       rates
AED 2020-03-07 13:45:25+00:00  USD    3.672500
AFN 2020-03-07 13:45:25+00:00  USD   76.099722
ALL 2020-03-07 13:45:25+00:00  USD  108.450334
AMD 2020-03-07 13:45:25+00:00  USD  479.819972
ANG 2020-03-07 13:45:25+00:00  USD    1.786501
..                        ...  ...         ...
XPT 2020-03-07 13:45:25+00:00  USD    0.001113
YER 2020-03-07 13:45:25+00:00  USD  250.279406
ZAR 2020-03-07 13:45:25+00:00  USD   15.667657
ZMW 2020-03-07 13:45:25+00:00  USD   15.245795
ZWD 2020-03-07 13:45:25+00:00  USD  361.899994
```

### 货币报价历史数据

接口: currency_history

目标地址: https://currencyscoop.com/

描述: 获取货币报价历史数据

限量: 单次返回指定货币在指定交易日的报价历史数据-免费账号每月限量访问 5000 次

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| base | str | Y | base="USD" |
| date | str | Y | date="2020-02-03" |
| api_key | str | Y | api_key="Please put your api key here"; you can register [currencyscoop](https://currencyscoop.com/), [Gmail](http://mail.google.com/) well be better |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| date      | str   | Y        | 日期时间-注意时区  |
| base      | float   | Y        | 货币   |
| rates      | str   | Y        | 比率  |

接口示例

```python
import akshare as ak
currency_history_df = ak.currency_history(base="USD", date="2020-02-03", api_key="Please put your api key here")
print(currency_history_df)
```

数据示例

```
          date base       rates
AED 2020-02-03  USD    3.672500
AFN 2020-02-03  USD   76.350078
ALL 2020-02-03  USD  110.256982
AMD 2020-02-03  USD  478.447633
ANG 2020-02-03  USD    1.790009
..         ...  ...         ...
XPT 2020-02-03  USD    0.001032
YER 2020-02-03  USD  250.312033
ZAR 2020-02-03  USD   14.826424
ZMW 2020-02-03  USD   14.627862
ZWD 2020-02-03  USD  361.899994
```

### 货币报价时间序列数据

接口: currency_time_series

目标地址: https://currencyscoop.com/

描述: 获取货币报价时间序列数据

限量: 单次返回指定货币在指定交易日到另一指定交易日的报价数据-免费账号每月限量访问 5000 次

输入参数

| 名称   | 类型 | 必选 | 描述   |
| -------- | ---- | ---- | --- |
| base | str | Y | base="USD" |
| start_date | str | Y | start_date="2020-02-03" |
| end_date | str | Y | end_date="2020-03-04" |
| api_key | str | Y | api_key="Please put your api key here"; you can register [currencyscoop](https://currencyscoop.com/), [Gmail](http://mail.google.com/) well be better |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| date      | str   | Y        | 日期时间-注意时区  |
| base      | float   | Y        | 货币   |
| rates      | str   | Y        | 比率  |

接口示例

```python
import akshare as ak
currency_time_series_df = ak.currency_time_series(base="USD", start_date="2020-02-03", end_date="2020-03-04", api_key="Please put your api key here")
print(currency_time_series_df)
```

数据示例(由于没有权限，此示例仅作占位)

```
          date base       rates
AED 2020-02-03  USD    3.672500
AFN 2020-02-03  USD   76.350078
ALL 2020-02-03  USD  110.256982
AMD 2020-02-03  USD  478.447633
ANG 2020-02-03  USD    1.790009
..         ...  ...         ...
XPT 2020-02-03  USD    0.001032
YER 2020-02-03  USD  250.312033
ZAR 2020-02-03  USD   14.826424
ZMW 2020-02-03  USD   14.627862
ZWD 2020-02-03  USD  361.899994
```

### 货币基础信息查询

接口: currency_currencies

目标地址: https://currencyscoop.com/

描述: 获取所有货币的基础信息

限量: 单次返回指定所有货币基础信息-免费账号每月限量访问 5000 次

输入参数

| 名称   | 类型 | 必选 | 描述   |
| -------- | ---- | ---- | --- |
| c_type | str | Y | c_type="fiat" |
| api_key | str | Y | api_key="Please put your api key here"; you can register [currencyscoop](https://currencyscoop.com/), [Gmail](http://mail.google.com/) well be better |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| currency_name      | str   | Y        | 货币名称  |
| currency_code      | str   | Y        | 货币代码   |
| decimal_units      | int   | Y        | 小数点位  |
| countries      | str   | Y        | 使用此货币的国家  |

接口示例

```python
import akshare as ak
currency_currencies_df = ak.currency_currencies(c_type="fiat", api_key="Please put your api key here")
print(currency_currencies_df)
```

数据示例

```
                     currency_name  ...                          countries
AED    United Arab Emirates dirham  ...             [United Arab Emirates]
AFN                 Afghan afghani  ...                      [Afghanistan]
ALL                   Albanian lek  ...                          [Albania]
AMD                  Armenian dram  ...                          [Armenia]
ANG  Netherlands Antillean guilder  ...  [Curaçao (CW), Sint Maarten (SX)]
..                             ...  ...                                ...
XXX                    No currency  ...                                 []
YER                    Yemeni rial  ...                            [Yemen]
ZAR             South African rand  ...   [Lesotho, Namibia, South Africa]
ZMW                 Zambian kwacha  ...                           [Zambia]
ZWL              Zimbabwean dollar  ...                         [Zimbabwe]
```

### 货币对价格转换

接口: currency_convert

目标地址: https://currencyscoop.com/

描述: 获取指定货币对指定货币数量的转换后价格

限量: 单次返回指定货币对的转换后价格-免费账号每月限量访问 5000 次

输入参数

| 名称   | 类型 | 必选 | 描述   |
| -------- | ---- | ---- | --- |
| base | str | Y | base="USD" |
| to | str | Y | to="CNY" |
| amount | str | Y | amount="10000" |
| api_key | str | Y | api_key="Please put your api key here"; you can register [currencyscoop](https://currencyscoop.com/), [Gmail](http://mail.google.com/) well be better |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| currency_name      | str   | Y        | 货币名称  |
| currency_code      | str   | Y        | 货币代码   |
| decimal_units      | int   | Y        | 小数点位  |
| countries      | str   | Y        | 使用此货币的国家  |

接口示例

```python
import akshare as ak
currency_convert_se = ak.currency_convert(base="USD", to="CNY", amount="10000", api_key="Please put your api key here")
print(currency_convert_se)
```

数据示例

```
timestamp    2020-03-07 13:45:31
date                  2020-03-07
from                         USD
to                           CNY
amount                     10000
value                      69320
```
