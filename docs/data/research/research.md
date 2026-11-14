# 学术研究数据

## AKShare 波动率数据

### 已实现波动率数据

(research_rv_rlab)=
#### Risk-Lab

接口：research_rv_rlab

目标地址：https://dachxiu.chicagobooth.edu/

描述：获取 Risk-Lab 已实现波动率数据

限量：单次返回某个指数所有历史数据

输入参数

| 名称     | 类型  | 描述                                           |
|--------|-----|----------------------------------------------|
| symbol | str | symbol="39693"，某个具体指数 help(research_rv_rlab) |

输出参数

| 名称    | 类型                | 描述  |
|-------|-------------------|-----|
| index | datetime.datetime | 日期  |
| data  | float64           | 数据  |

接口示例

```python
import akshare as ak

research_rv_rlab_df = ak.research_rv_rlab(symbol="39693")
print(research_rv_rlab_df)
```

数据示例

```
1996-01-02    0.000000
1996-01-04    0.000000
1996-01-05    0.000000
1996-01-09    0.000000
1996-01-10    0.000000
                ...
2019-11-04    0.175107
2019-11-05    0.185112
2019-11-06    0.210373
2019-11-07    0.240808
2019-11-08    0.199549
```

(research_rv_input_futures_sina)=
#### 已实现波动率-期货分钟数据

接口：research_rv_input_futures_sina

目标地址：https://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_3

描述：从新浪财经获取期货合约的分钟行情，并整理成 research_yz_rv 计算已实现波动率所需的格式

限量：单次返回指定合约的近期分钟数据

输入参数

| 名称     | 类型  | 描述                                                 |
|--------|-----|----------------------------------------------------|
| symbol | str | symbol="IF2612"；期货合约代码，如"IF2008"代表沪深300期货2020年8月合约 |
| period | str | period="5"；时间周期，可选{'1','5','15','30','60'}分钟       |

输出参数

| 名称     | 类型      | 描述 |
|--------|---------|----|
| Open   | float64 | -  |
| High   | float64 | -  |
| Low    | float64 | -  |
| Close  | float64 | -  |
| volume | int64   | -  |
| hold   | int64   | -  |

接口示例

```python
import akshare as ak

research_rv_input_futures_sina_df = ak.research_rv_input_futures_sina(symbol="IF2612", period="5")
print(research_rv_input_futures_sina_df)
```

数据示例

```
                       Open    High     Low   Close  volume    hold
Date
2026-10-15 13:50:00  4093.0  4101.2  4078.0  4078.2    1167  176950
2026-10-15 13:55:00  4078.8  4078.8  4063.2  4065.4    1906  177762
2026-10-15 14:00:00  4066.2  4067.0  4052.0  4053.2    1148  178445
2026-10-15 14:05:00  4054.0  4064.0  4050.4  4059.8     110  179212
2026-10-15 14:10:00  4058.6  4067.2  4055.4  4064.4     415  179637
...                     ...     ...     ...     ...     ...     ...
2026-11-13 14:40:00  3966.0  3968.2  3962.0  3967.0     914  171914
2026-11-13 14:45:00  3967.0  3971.4  3965.8  3968.6    1331  172254
2026-11-13 14:50:00  3969.0  3970.4  3959.8  3959.8     967  172530
2026-11-13 14:55:00  3959.8  3959.8  3954.0  3956.2    2540  172697
2026-11-13 15:00:00  3955.6  3961.0  3954.0  3956.6    2063  173340
[1023 rows x 6 columns]
```

(research_rv_input_stock_em)=
#### 已实现波动率-股票分钟数据

接口：research_rv_input_stock_em

目标地址：https://quote.eastmoney.com/concept/sh603777.html?from=classic

描述：从东方财富获取股票的分钟行情，并整理成 research_yz_rv 计算已实现波动率所需的格式：以时间为索引，开盘、最高、最低、收盘改名为 Open、High、Low、Close，其余列与 stock_zh_a_hist_min_em 相同；该接口请求东方财富的行情服务器，短时间内多次调用会被临时限流

限量：单次返回指定股票指定时间段的分钟数据

输入参数

| 名称         | 类型  | 描述                                                              |
|------------|-----|-----------------------------------------------------------------|
| symbol     | str | symbol="000001"；股票代码，如"000001"                                  |
| start_date | str | start_date="2026-11-12 09:30:00"；开始日期时间，格式"YYYY-MM-DD HH:MM:SS" |
| end_date   | str | end_date="2026-11-13 15:00:00"；结束日期时间，格式"YYYY-MM-DD HH:MM:SS"   |
| period     | str | period="1"；时间周期，可选{'1','5','15','30','60'}分钟                    |
| adjust     | str | adjust="hfq"；复权方式，可选{'','qfq'(前复权),'hfq'(后复权)}                  |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| Open  | float64 | -  |
| High  | float64 | -  |
| Low   | float64 | -  |
| Close | float64 | -  |

接口示例

```python
import akshare as ak

research_rv_input_stock_em_df = ak.research_rv_input_stock_em(symbol="000001", start_date="2026-11-12 09:30:00", end_date="2026-11-13 15:00:00", period="1", adjust="hfq")
print(research_rv_input_stock_em_df)
```

数据示例

```
因请求限流或耗时过长，暂无数据示例
```

(research_yz_rv)=
#### Yang-Zhang 已实现波动率

接口：research_yz_rv

目标地址：https://github.com/hugogobato/Yang-Zhang-s-Realized-Volatility-Automated-Estimation-in-Python

描述：按 Yang-Zhang 方法由分钟行情计算每日的已实现波动率；输入为 research_rv_input_futures_sina 或 research_rv_input_stock_em 返回的表格，本接口不联网

限量：单次返回输入数据覆盖的每个交易日的已实现波动率

输入参数

| 名称   | 类型               | 描述                                  |
|------|------------------|-------------------------------------|
| data | pandas.DataFrame | 分钟行情，含 Open、High、Low、Close 四列，索引为时间 |

输出参数

| 名称   | 类型      | 描述 |
|------|---------|----|
| date | object  | -  |
| rv   | float64 | -  |

接口示例

```python
import akshare as ak

research_yz_rv_df = ak.research_yz_rv(ak.research_rv_input_futures_sina(symbol="IF2612", period="5"))
print(research_yz_rv_df)
```

数据示例

```
          date        rv
0   2026-10-15  0.003135
1   2026-10-16  0.002258
2   2026-10-19  0.002162
3   2026-10-20  0.001959
4   2026-10-21  0.001773
5   2026-10-22  0.002756
6   2026-10-23  0.003648
7   2026-10-26  0.002027
8   2026-10-27  0.001565
9   2026-10-28  0.001855
10  2026-10-29  0.002459
11  2026-10-30  0.002971
12  2026-11-02  0.002892
13  2026-11-03  0.002680
14  2026-11-04  0.002871
15  2026-11-05  0.001858
16  2026-11-06  0.002118
17  2026-11-09  0.001328
18  2026-11-10  0.001155
19  2026-11-11  0.001697
20  2026-11-12  0.001427
21  2026-11-13  0.001662
```

## AKShare 多因子数据

(research_ff_crr)=
### Current Research Returns

接口：research_ff_crr

目标地址：https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

描述：获取 Current Research Returns 多因子数据；更多信息请访问目标地址

限量：单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称             | 类型     | 描述   |
|----------------|--------|------|
| item           | str    | -    |
| September 2019 | str    | 动态日期 |
| Last 3 Months  | str    | 动态日期 |
| Last 12 Months | str    | 动态日期 |

接口示例

```python
import akshare as ak

research_ff_crr_df = ak.research_ff_crr()
print(research_ff_crr_df)
```

数据示例

```
                                           item  ... Last 12  Months
0                Fama/French 3 Research Factors  ...               -
1                                         Rm-Rf  ...            8.12
2                                           SMB  ...           -9.44
3                                           HML  ...          -14.98
4          Fama/French 5 Research Factors (2x3)  ...               -
5                                         Rm-Rf  ...            8.12
6                                           SMB  ...          -12.25
7                                           HML  ...          -14.98
8                                           RMW  ...            8.46
9                                           CMA  ...          -14.63
10              Fama/French Research Portfolios  ...               -
11           Size and Book-to-Market Portfolios  ...               -
12                                  Small Value  ...           -7.16
13                                Small Neutral  ...            1.97
14                                  Big Neutral  ...           -2.47
15                                 Small Growth  ...           -2.56
16                                    Big Value  ...            0.51
17                                   Big Growth  ...           22.70
18  Size and Operating Profitability Portfolios  ...               -
19                                 Small Robust  ...            4.19
20                                Small Neutral  ...            0.17
21                                   Small Weak  ...           -4.93
22                                   Big Robust  ...           19.99
23                                  Big Neutral  ...            5.67
24                                     Big Weak  ...           12.20
25               Size and Investment Portfolios  ...               -
26                           Small Conservative  ...           -6.81
27                                Small Neutral  ...           -1.21
28                             Small Aggressive  ...            1.64
29                             Big Conservative  ...            0.77
30                                  Big Neutral  ...           14.75
31                               Big Aggressive  ...           21.59
[32 rows x 4 columns]
```

## AKShare 政策不确定性数据

(research_epu_index)=
### 国家和地区指数

接口：research_epu_index

目标地址：https://www.policyuncertainty.com/index.html

描述：国家或地区的经济政策不确定性(EPU)数据

限量：单次返回某个具体国家或地区的所有月度经济政策不确定性数据

输入参数

| 名称     | 类型  | 描述                                    |
|--------|-----|---------------------------------------|
| symbol | str | symbol="China"；按 **国家和地区一览表** 输入相应参数 |

国家和地区一览表

| 英文名词        | 说明              |
|-------------|-----------------|
| Global      |                 |
| Australia   |                 |
| Canada      |                 |
| China       |                 |
| Europe      | 欧洲              |
| Germany     | 欧洲              |
| Hong Kong   |                 |
| Ireland     |                 |
| Japan       |                 |
| Mexico      |                 |
| Russia      |                 |
| Spain       |                 |
| UK          |                 |
| USA         |                 |
| Brazil      |                 |
| Chile       |                 |
| Colombia    | 有两种，默认第一种(FKT) |
| France      | 欧洲              |
| Greece      |                 |
| India       |                 |
| Italy       | 欧洲              |
| South Korea |                 |
| Netherlands |                 |
| Singapore   |                 |
| Sweden      |                 |

输出参数

| 名称 | 类型 | 描述        |
|----|----|-----------|
| -  | -  | 每个国家或地区不同 |

接口示例

```python
import akshare as ak

research_epu_index_df = ak.research_epu_index(symbol="China")  # 注意单词第一个字母大写
print(research_epu_index_df)
```

数据示例

```
     year  month  China_Policy_Index
0    1995      1          192.911910
1    1995      2          193.987850
2    1995      3           88.227035
3    1995      4          131.034710
4    1995      5          177.096860
..    ...    ...                 ...
342  2023      7          704.566080
343  2023      8          709.881990
344  2023      9          819.746150
345  2023     10          603.739890
346  2023     11          743.397580
[347 rows x 3 columns]
```

(research_fred_md)=
### FRED-MD 月度宏观数据集

接口：research_fred_md

目标地址：https://www.stlouisfed.org/research/economists/mccracken/fred-databases

描述：圣路易斯联储 FRED-MD 月度宏观经济数据集（Michael McCracken 维护），返回指定月份发布的版本；服务器在国外，需要使用代理访问

限量：单次返回指定版本的全部序列；首次获取当年以前的版本需下载约 36 MB 的历史压缩包

输入参数

| 名称   | 类型  | 描述                                                    |
|------|-----|-------------------------------------------------------|
| date | str | date="2026-10"；e.g., "2020-03"; from "2015-01" to now |

输出参数

| 名称 | 类型 | 描述 |
|----|----|----|
| sasdate | str | 观测日期，按月排列 |
| 其余各列 | float64 | 以 FRED 序列代码为列名，共约 126 个序列，含义见目标地址提供的数据说明 |

接口示例

```python
import akshare as ak

research_fred_md_df = ak.research_fred_md(date="2026-10")
print(research_fred_md_df)
```

数据示例

```
        sasdate        RPI  W875RX1  ...   DTCTHFNM     INVEST  VIXCLSx
0    Transform:      5.000      5.0  ...       6.00     6.0000   1.0000
1      1/1/1959   2583.560   2426.0  ...   12298.00    84.2043      NaN
2      2/1/1959   2593.596   2434.8  ...   12298.00    83.5280      NaN
3      3/1/1959   2610.396   2452.7  ...   12349.00    81.6405      NaN
4      4/1/1959   2627.446   2470.0  ...   12484.00    81.8099      NaN
..          ...        ...      ...  ...        ...        ...      ...
809    5/1/2026  20890.655  16980.9  ...  919845.34  5757.6467  17.2719
810    6/1/2026  20959.614  17024.8  ...  919293.57  5787.5575  18.0718
811    7/1/2026  21015.820  17068.3  ...  918085.96  5835.9800  17.1994
812    8/1/2026  21011.444  17068.4  ...  916070.46  5813.7860  15.1179
813    9/1/2026  20950.003  17015.2  ...        NaN  5783.1389  15.6369
[814 rows x 127 columns]
```

(research_fred_qd)=
### FRED-QD 季度宏观数据集

接口：research_fred_qd

目标地址：https://www.stlouisfed.org/research/economists/mccracken/fred-databases

描述：圣路易斯联储 FRED-QD 季度宏观经济数据集，是 FRED-MD 的季度版；服务器在国外，需要使用代理访问

限量：单次返回指定版本的全部序列；首次获取当年以前的版本需下载约 20 MB 的历史压缩包

输入参数

| 名称   | 类型  | 描述                                                    |
|------|-----|-------------------------------------------------------|
| date | str | date="2026-10"；e.g., "2020-03"; from "2018-05" to now |

输出参数

| 名称 | 类型 | 描述 |
|----|----|----|
| sasdate | str | 观测日期，按季排列 |
| 其余各列 | float64 | 以 FRED 序列代码为列名，共约 245 个序列，含义见目标地址提供的数据说明 |

接口示例

```python
import akshare as ak

research_fred_qd_df = ak.research_fred_qd(date="2026-10")
print(research_fred_qd_df)
```

数据示例

```
       sasdate      GDPC1  ...  S&P div yield  S&P PE ratio
0      factors      0.000  ...         0.0000        0.0000
1    transform      5.000  ...         2.0000        5.0000
2     3/1/1959   3352.129  ...         3.1765       18.6211
3     6/1/1959   3427.667  ...         3.1012       19.2899
4     9/1/1959   3430.057  ...         3.0720       18.9544
..         ...        ...  ...            ...           ...
268   9/1/2025  24112.966  ...         1.2150       29.7155
269  12/1/2025  24125.479  ...         1.1684       30.3245
270   3/1/2026  24274.383  ...         1.1737       29.3716
271   6/1/2026  24408.011  ...         1.1120       29.4022
272   9/1/2026  24611.077  ...            NaN       29.1186
[273 rows x 246 columns]
```
