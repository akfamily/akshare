## [AKShare](https://github.com/akfamily/akshare) 货币数据

### 货币报价最新数据

接口: currency_latest

注意：此接口使用外部 API, 免费账号每月限量访问 5000 次, 可以在 [currencyscoop](https://currencyscoop.com/) 注册

目标地址: https://currencyscoop.com/

描述: 货币报价最新数据

限量: 单次返回指定货币的最新报价数据

输入参数

| 名称      | 类型  | 描述                                                                                                          |
|---------|-----|-------------------------------------------------------------------------------------------------------------|
| base    | str | base="USD"                                                                                                  |
| symbols | str | symbols=""; 默认返回全部, 可以在此处设置 symbols="AUD", 则返回 AUD 的数据; 可以在此处设置 symbols: str = "AUD,CNY", 则返回 AUD 和 CNY 的数据 |
| api_key | str | api_key="此处输入 API";                                                                                         |

更多相关参数可以访问: https://currencybeacon.com/api-documentation 和 https://currencybeacon.com/supported-currencies

输出参数

| 名称       | 类型                  | 描述        |
|----------|---------------------|-----------|
| currency | object              | 货币代码      |
| date     | datetime64[ns, UTC] | 日期时间-注意时区 |
| base     | object              | 货币        |
| rates    | float64             | 比率        |

接口示例

```python
import akshare as ak

currency_latest_df = ak.currency_latest(base="USD", symbols="", api_key="此处输入 API")
print(currency_latest_df)
```

数据示例

```
    currency                      date base         rates
0        ADA 2023-07-24 10:56:21+00:00  USD      3.213363
1        AED 2023-07-24 10:56:21+00:00  USD      3.672500
2        AFN 2023-07-24 10:56:21+00:00  USD     85.665822
3        ALL 2023-07-24 10:56:21+00:00  USD     91.125190
4        AMD 2023-07-24 10:56:21+00:00  USD    387.300314
..       ...                       ...  ...           ...
215      ZAR 2023-07-24 10:56:21+00:00  USD     17.927659
216      ZMK 2023-07-24 10:56:21+00:00  USD  19493.346892
217      ZMW 2023-07-24 10:56:21+00:00  USD     19.493347
218      ZWD 2023-07-24 10:56:21+00:00  USD    361.900000
219      ZWL 2023-07-24 10:56:21+00:00  USD   4677.170339
[220 rows x 4 columns]
```

### 货币报价历史数据

接口: currency_history

注意：此接口使用外部 API, 免费账号每月限量访问 5000 次, 可以在 [currencyscoop](https://currencyscoop.com/) 注册

目标地址: https://currencyscoop.com/

描述: 货币报价历史数据

限量: 单次返回指定货币在指定交易日的报价历史数据-免费账号每月限量访问 5000 次

输入参数

| 名称      | 类型  | 描述                                                                                                          |
|---------|-----|-------------------------------------------------------------------------------------------------------------|
| base    | str | base="USD"                                                                                                  |
| date    | str | date="2023-02-03"                                                                                           |
| symbols | str | symbols=""; 默认返回全部, 可以在此处设置 symbols="AUD", 则返回 AUD 的数据; 可以在此处设置 symbols: str = "AUD,CNY", 则返回 AUD 和 CNY 的数据 |
| api_key | str | api_key="此处输入 API";                                                                                         |

输出参数

| 名称       | 类型      | 描述   |
|----------|---------|------|
| currency | object  | 货币代码 |
| date     | object  | 日期   |
| base     | float64 | 货币   |
| rates    | float64 | 比率   |

接口示例

```python
import akshare as ak

currency_history_df = ak.currency_history(base="USD", date="2023-02-03", symbols="", api_key="此处输入 API")
print(currency_history_df)
```

数据示例

```
    currency       date base         rates
0        ADA 2023-02-03  USD      2.501764
1        AED 2023-02-03  USD      3.672500
2        AFN 2023-02-03  USD     89.667343
3        ALL 2023-02-03  USD    107.092799
4        AMD 2023-02-03  USD    395.155660
..       ...        ...  ...           ...
215      ZAR 2023-02-03  USD     17.470971
216      ZMK 2023-02-03  USD  19217.069221
217      ZMW 2023-02-03  USD     19.217069
218      ZWD 2023-02-03  USD    361.900000
219      ZWL 2023-02-03  USD    804.930876
[220 rows x 4 columns]
```

### 货币报价时间序列数据

接口: currency_time_series

注意：此接口使用外部 API, 免费账号每月限量访问 5000 次, 可以在 [currencyscoop](https://currencyscoop.com/) 注册

目标地址: https://currencyscoop.com/

描述: 货币报价时间序列数据

限量: 单次返回指定货币在指定交易日到另一指定交易日的报价数据

输入参数

| 名称         | 类型  | 描述                                                                                                          |
|------------|-----|-------------------------------------------------------------------------------------------------------------|
| base       | str | base="USD"                                                                                                  |
| start_date | str | start_date="2023-02-03"                                                                                     |
| end_date   | str | end_date="2023-03-04"                                                                                       |
| symbols    | str | symbols=""; 默认返回全部, 可以在此处设置 symbols="AUD", 则返回 AUD 的数据; 可以在此处设置 symbols: str = "AUD,CNY", 则返回 AUD 和 CNY 的数据 |
| api_key    | str | api_key="此处输入 API";                                                                                         |

输出参数

| 名称   | 类型      | 描述     |
|------|---------|--------|
| date | object  | 日期     |
| ...  | float64 | 货币价格数据 |

接口示例

```python
import akshare as ak

currency_time_series_df = ak.currency_time_series(base="USD", start_date="2023-02-03", end_date="2023-03-04", symbols="", api_key="此处输入 API")
print(currency_time_series_df)
```

数据示例

```
          date       ADA     AED  ...        ZMW    ZWD         ZWL
0   2023-02-03  2.501764  3.6725  ...  19.217069  361.9  804.930876
1   2023-02-04  2.523126  3.6725  ...  19.190104  361.9  804.930876
2   2023-02-05  2.548544  3.6725  ...  19.359966  361.9  804.898394
3   2023-02-06  2.588994  3.6725  ...  19.211667  361.9  812.084265
4   2023-02-07  2.503360  3.6725  ...  19.163126  361.9  816.624716
5   2023-02-08  2.615068  3.6725  ...  19.276132  361.9  831.793316
6   2023-02-09  2.772723  3.6725  ...  19.298303  361.9  833.966241
7   2023-02-10  2.767700  3.6725  ...  19.377991  361.9  839.246195
8   2023-02-11  2.736774  3.6725  ...  19.360544  361.9  839.246195
9   2023-02-12  2.748749  3.6725  ...  19.316502  361.9  839.264194
10  2023-02-13  2.803486  3.6725  ...  19.196452  361.9  846.084936
11  2023-02-14  2.587805  3.6725  ...  19.375476  361.9  850.135849
12  2023-02-15  2.443325  3.6725  ...  19.341588  361.9  856.219979
13  2023-02-16  2.523309  3.6725  ...  19.494675  361.9  860.307069
14  2023-02-17  2.474066  3.6725  ...  19.654148  361.9  863.222832
15  2023-02-18  2.487758  3.6725  ...  19.470201  361.9  863.222832
16  2023-02-19  2.485208  3.6725  ...  19.340051  361.9  863.295153
17  2023-02-20  2.487952  3.6725  ...  19.516557  361.9  893.102417
18  2023-02-21  2.582063  3.6725  ...  19.524095  361.9  893.264541
19  2023-02-22  2.552943  3.6725  ...  19.613078  361.9  873.680243
20  2023-02-23  2.621636  3.6725  ...  19.684268  361.9  873.836274
21  2023-02-24  2.745342  3.6725  ...  19.739989  361.9  894.480661
22  2023-02-25  2.765595  3.6725  ...  19.820979  361.9  894.480661
23  2023-02-26  2.737813  3.6725  ...  19.767109  361.9  894.489801
24  2023-02-27  2.738002  3.6725  ...  19.749675  361.9  886.192242
25  2023-02-28  2.797012  3.6725  ...  19.865244  361.9  889.436788
26  2023-03-01  2.803997  3.6725  ...  19.959017  361.9  892.608637
27  2023-03-02  2.980559  3.6725  ...  20.006057  361.9  898.930254
28  2023-03-03  2.925695  3.6725  ...  20.023367  361.9  899.419086
29  2023-03-04  2.939316  3.6725  ...  20.100199  361.9  899.419086
[30 rows x 221 columns]
```

### 货币基础信息查询

接口: currency_currencies

注意：此接口使用外部 API, 免费账号每月限量访问 5000 次, 可以在 [currencyscoop](https://currencyscoop.com/) 注册

目标地址: https://currencyscoop.com/

描述: 所有货币的基础信息

限量: 单次返回指定所有货币基础信息

输入参数

| 名称      | 类型  | 描述                  |
|---------|-----|---------------------|
| c_type  | str | c_type="fiat"       |
| api_key | str | api_key="此处输入 API"; |

输出参数

| 名称                  | 类型     | 描述 |
|---------------------|--------|----|
| id                  | int64  | -  |
| name                | object | -  |
| short_code          | object | -  |
| code                | object | -  |
| precision           | int64  | -  |
| subunit             | int64  | -  |
| symbol              | object | -  |
| symbol_first        | bool   | -  |
| decimal_mark        | object | -  |
| thousands_separator | object | -  |

接口示例

```python
import akshare as ak

currency_currencies_df = ak.currency_currencies(c_type="fiat", api_key="此处输入 API")
print(currency_currencies_df)
```

数据示例

```
      id                           name  ... decimal_mark thousands_separator
0      1                     UAE Dirham  ...            .                   ,
1      2                        Afghani  ...            .                   ,
2      3                            Lek  ...            .                   ,
3      4                  Armenian Dram  ...            .                   ,
4      5  Netherlands Antillean Guilder  ...            ,                   .
..   ...                            ...  ...          ...                 ...
156  157                      CFP Franc  ...            .                   ,
157  158                    Yemeni Rial  ...            .                   ,
158  159                           Rand  ...            .                   ,
159  160                 Zambian Kwacha  ...            .                   ,
160  161                Zimbabwe Dollar  ...            .                   ,
[161 rows x 10 columns]
```

### 货币对价格转换

接口: currency_convert

注意：此接口使用外部 API, 免费账号每月限量访问 5000 次, 可以在 [currencyscoop](https://currencyscoop.com/) 注册

目标地址: https://currencyscoop.com/

描述: 指定货币对指定货币数量的转换后价格

限量: 单次返回指定货币对的转换后价格

输入参数

| 名称      | 类型  | 描述                  |
|---------|-----|---------------------|
| base    | str | base="USD"; 基础货币    |
| to      | str | to="CNY"; 需要转换到的货币  |
| amount  | str | amount="10000"; 转换量 |
| api_key | str | api_key="此处输入 API"; |

输出参数

| 名称    | 类型     | 描述 |
|-------|--------|----|
| item  | object | -  |
| value | object | -  |

接口示例

```python
import akshare as ak

currency_convert_df = ak.currency_convert(base="USD", to="CNY", amount="10000", api_key="此处输入 API")
print(currency_convert_df)
```

数据示例

```
        item                value
0  timestamp  2023-07-24 11:31:20
1       date           2023-07-24
2       from                  USD
3         to                  CNY
4     amount                10000
5      value            71898.995
```
