## [AKShare](https://github.com/akfamily/akshare) 波动率数据

### 已实现波动率数据

#### Oxford-Man

接口: article_oman_rv

目标地址: https://realized.oxford-man.ox.ac.uk/data/visualization

描述: 获取 Oxford-Man 已实现波动率数据

限量: 单次返回某个指数具体指标的所有历史数据

输入参数

| 名称     | 类型  | 必选  | 描述                                        |
|--------|-----|-----|-------------------------------------------|
| symbol | str | Y   | symbol="FTSE", 具体指数请查看如下 **已实现波动率指数一览表**  |
| index  | str | Y   | index="rk_th2", 具体指标请查看如下 **已实现波动率指标一览表** |

已实现波动率指数一览表

| Symbol    | Name                                      | Earliest Available | Latest Available  |
|-----------|-------------------------------------------|--------------------|-------------------|
| .AEX      | AEX index                                 | January 03, 2000   | November 28, 2019 |
| .AORD     | All Ordinaries                            | January 04, 2000   | November 28, 2019 |
| .BFX      | Bell 20 Index                             | January 03, 2000   | November 28, 2019 |
| .BSESN    | S&P BSE Sensex                            | January 03, 2000   | November 28, 2019 |
| .BVLG     | PSI All-Share Index                       | October 15, 2012   | November 28, 2019 |
| .BVSP     | BVSP BOVESPA Index                        | January 03, 2000   | November 28, 2019 |
| .DJI      | Dow Jones Industrial Average              | January 03, 2000   | November 27, 2019 |
| .FCHI     | CAC 40                                    | January 03, 2000   | November 28, 2019 |
| .FTMIB    | FTSE MIB                                  | June 01, 2009      | November 28, 2019 |
| .FTSE     | FTSE 100                                  | January 04, 2000   | November 28, 2019 |
| .GDAXI    | DAX                                       | January 03, 2000   | November 28, 2019 |
| .GSPTSE   | S&P/TSX Composite index                   | May 02, 2002       | November 28, 2019 |
| .HSI      | HANG SENG Index                           | January 03, 2000   | November 28, 2019 |
| .IBEX     | IBEX 35 Index                             | January 03, 2000   | November 28, 2019 |
| .IXIC     | Nasdaq 100                                | January 03, 2000   | November 27, 2019 |
| .KS11     | Korea Composite Stock Price Index (KOSPI) | January 04, 2000   | November 28, 2019 |
| .KSE      | Karachi SE 100 Index                      | January 03, 2000   | November 28, 2019 |
| .MXX      | IPC Mexico                                | January 03, 2000   | November 28, 2019 |
| .N225     | Nikkei 225                                | February 02, 2000  | November 28, 2019 |
| .NSEI     | NIFTY 50                                  | January 03, 2000   | November 28, 2019 |
| .OMXC20   | OMX Copenhagen 20 Index                   | October 03, 2005   | November 28, 2019 |
| .OMXHPI   | OMX Helsinki All Share Index              | October 03, 2005   | November 28, 2019 |
| .OMXSPI   | OMX Stockholm All Share Index             | October 03, 2005   | November 28, 2019 |
| .OSEAX    | Oslo Exchange All-share Index             | September 03, 2001 | November 28, 2019 |
| .RUT      | Russel 2000                               | January 03, 2000   | November 27, 2019 |
| .SMSI     | Madrid General Index                      | July 04, 2005      | November 28, 2019 |
| .SPX      | S&P 500 Index                             | January 03, 2000   | November 27, 2019 |
| .SSEC     | Shanghai Composite Index                  | January 04, 2000   | November 28, 2019 |
| .SSMI     | Swiss Stock Market Index                  | January 04, 2000   | November 28, 2019 |
| .STI      | Straits Times Index                       | January 03, 2000   | November 28, 2019 |
| .STOXX50E | EURO STOXX 50                             | January 03, 2000   | November 28, 2019 |

已实现波动率指标一览表

| Code          | Description                                   |
|---------------|-----------------------------------------------|
| bv            | Bipower Variation (5-min)                     |
| bv_ss         | Bipower Variation (5-min Sub-sampled)         |
| close_price   | Closing (Last) Price                          |
| close_time    | Closing Time                                  |
| medrv         | Median Realized Variance (5-min)              |
| nobs          | Number of Observations                        |
| open_price    | Opening (First) Price                         |
| open_time     | Opening Time                                  |
| open_to_close | Open to Close Return                          |
| rk_parzen     | Realized Kernel Variance (Non-Flat Parzen)    |
| rk_th2        | Realized Kernel Variance (Tukey-Hanning(2))   |
| rk_twoscale   | Realized Kernel Variance (Two-Scale/Bartlett) |
| rsv           | Realized Semi-variance (5-min)                |
| rsv_ss        | Realized Semi-variance (5-min Sub-sampled)    |
| rv10          | Realized Variance (10-min)                    |
| rv10_ss       | Realized Variance (10-min Sub-sampled)        |
| rv5           | Realized Variance (5-min)                     |
| rv5_ss        | Realized Variance (5-min Sub-sampled)         |

输出参数

Oxford-Man-已实现波动率数据

| 名称    | 类型                | 默认显示 | 描述  |
|-------|-------------------|------|-----|
| index | datetime.datetime | Y    | 日期  |  
| data  | float             | Y    | 数据  |  

接口示例

```python
import akshare as ak

article_oman_rv_df = ak.article_oman_rv(symbol="FTSE", index="rk_th2")
print(article_oman_rv_df)
```

数据示例
```
2000-01-04    22.95
2000-01-05    19.37
2000-01-06    18.22
2000-01-07    19.34
2000-01-10    15.67
              ...  
2019-11-04     6.71
2019-11-05     5.90
2019-11-06     6.43
2019-11-07     5.81
2019-11-08     6.75
```

#### Risk-Lab

接口: article_rlab_rv

目标地址: https://dachxiu.chicagobooth.edu/

描述: 获取 Risk-Lab 已实现波动率数据

限量: 单次返回某个指数所有历史数据

输入参数

| 名称     | 类型  | 描述                                           |
|--------|-----|----------------------------------------------|
| symbol | str | symbol="39693", 某个具体指数 help(article_rlab_rv) |

输出参数

Risk-Lab-已实现波动率数据

| 名称    | 类型                | 描述  |
|-------|-------------------|-----|
| index | datetime.datetime | 日期  |  
| data  | float             | 数据  |  

接口示例

```python
import akshare as ak

article_rlab_rv_df = ak.article_rlab_rv(symbol="39693")
print(article_rlab_rv_df)
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

## [AKShare](https://github.com/akfamily/akshare) 多因子数据

### Current Research Returns

接口: article_ff_crr

目标地址: http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

描述: 获取 Current Research Returns 多因子数据; 更多信息请访问目标地址

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

FF-Current Research Returns

| 名称             | 类型     | 描述   |
|----------------|--------|------|
| item           | object | -    |  
| September 2019 | object | 动态日期 |  
| Last 3 Months  | object | 动态日期 |  
| Last 12 Months | object | 动态日期 |  

接口示例

```python
import akshare as ak

article_ff_crr_df = ak.article_ff_crr()
print(article_ff_crr_df)
```

数据示例

```
                                           item  ... Last 12  Months
0                Fama/French 3 Research Factors  ...               -
1                                         Rm-Rf  ...          -11.50
2                                           SMB  ...           -1.53
3                                           HML  ...            1.52
4          Fama/French 5 Research Factors (2x3)  ...               -
5                                         Rm-Rf  ...          -11.50
6                                           SMB  ...           -0.26
7                                           HML  ...            1.52
8                                           RMW  ...            9.61
9                                           CMA  ...            4.53
10              Fama/French Research Portfolios  ...               -
11           Size and Book-to-Market Portfolios  ...               -
12                                  Small Value  ...          -10.89
13                                Small Neutral  ...           -5.21
14                                  Big Neutral  ...          -11.90
15                                 Small Growth  ...           -7.23
16                                    Big Value  ...           -6.92
17                                   Big Growth  ...           -9.27
18  Size and Operating Profitability Portfolios  ...               -
19                                 Small Robust  ...           -5.23
20                                Small Neutral  ...           -4.06
21                                   Small Weak  ...          -16.12
22                                   Big Robust  ...           -3.68
23                                  Big Neutral  ...          -14.64
24                                     Big Weak  ...          -12.01
25               Size and Investment Portfolios  ...               -
26                           Small Conservative  ...           -9.80
27                                Small Neutral  ...           -5.30
28                             Small Aggressive  ...          -11.87
29                             Big Conservative  ...           -6.99
30                                  Big Neutral  ...           -3.36
31                               Big Aggressive  ...          -13.98
```

## [AKShare](https://github.com/akfamily/akshare) 政策不确定性数据

### 国家和地区指数

接口: article_epu_index

目标地址: http://www.policyuncertainty.com/index.html

描述: 获取国家或地区的经济政策不确定性(EPU)数据

限量: 单次返回某个具体国家或地区的所有月度经济政策不确定性数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| index | str  | Y    |  index="China"; 按 **国家和地区一览表** 输入相应参数|

国家和地区一览表

| 英文名词          | 说明 |
| --------------- | ----- | 
| Global |  | 
| Australia |  | 
| Canada |  | 
| China |  | 
| Europe | 欧洲 | 
| Germany | 欧洲 | 
| Hong Kong |  | 
| Ireland |  | 
| Japan |  | 
| Mexico |  | 
| Russia |  | 
| Spain |  | 
| UK |  | 
| USA |  | 
| Brazil |  | 
| Chile |  | 
| Colombia | 有两种, 默认第一种(FKT) | 
| France | 欧洲 | 
| Greece |  | 
| India |  | 
| Italy | 欧洲 | 
| South Korea |  | 
| Netherlands |  | 
| Singapore |  | 
| Sweden |  |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| -      | -   | -        | 每个国家或地区不同  |  

接口示例

```python
import akshare as ak
epu_index_df = ak.article_epu_index(index="China")  # 注意单词第一个字母大写
print(epu_index_df)
```

数据示例

```
     year  month  China_Policy_Index
0    1995      1           192.91190
1    1995      2           193.98790
2    1995      3            88.22704
3    1995      4           131.03470
4    1995      5           177.09690
..    ...    ...                 ...
287  2018     12           935.31030
288  2019      1           654.96260
289  2019      2           720.15790
290  2019      3           753.10770
291  2019      4           502.55000
```
