## [AKShare](https://github.com/jindaxiang/akshare) 波动率数据

### 已实现波动率数据

#### Oxford-Man

接口: article_oman_rv

目标地址: https://realized.oxford-man.ox.ac.uk/data/visualization

描述: 获取 Oxford-Man 已实现波动率数据

限量: 单次返回某个指数具体指标的所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述   |
| -------- | ---- | ---- | --- |
| symbol | str  | Y    |  symbol="FTSE", 具体指数请查看如下 **已实现波动率指数一览表**|
| index | str  | Y     |  index="rk_th2", 具体指标请查看如下 **已实现波动率指标一览表**|
| plot | Bool  | Y    |  plot=True, 是否画图|

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

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| index      | datetime.datetime   | Y        | 日期  |  
| data      | float   | Y        | 数据  |  


接口示例

```python
import akshare as ak
df = ak.article_oman_rv(symbol="FTSE", index="rk_th2", plot=True)
print(df)
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

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| symbol | str  | Y    |  symbol="39693", 某个具体指数 help(article_rlab_rv)|
| plot | Bool  | Y    |  plot=True, 是否画图|


输出参数

Risk-Lab-已实现波动率数据

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| index      | datetime.datetime   | Y        | 日期  |  
| data      | float   | Y        | 数据  |  


接口示例

```python
import akshare as ak
df = ak.article_rlab_rv(symbol="39693")
print(df)
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

## [AkShare](https://github.com/jindaxiang/akshare) 多因子数据

### Current Research Returns

接口: article_ff_crr

目标地址: http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

描述: 获取 Current Research Returns 多因子数据

限量: 单次返回所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| - | -  | -    |  -|

输出参数

FF-Current Research Returns

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| September 2019      | float   | Y        | -  |  
| Last 3 Months      | float   | Y        | -  |  
| Last 12 Months      | float   | Y        | -  |  

接口示例

```python
import akshare as ak
df = ak.article_ff_crr()
print(df)
```

数据示例

```
                                            September  2019 Last 3  Months  \
Fama/French 3 Research Factors                            -              -   
Rm-Rf                                                  1.44           0.00   
SMB                                                   -0.89          -5.36   
HML                                                    6.73           1.39   
Fama/French 5 Research Factors (2x3)                      -              -   
Rm-Rf                                                  1.44           0.00   
SMB                                                    0.33          -4.94   
HML                                                    6.73           1.39   
RMW                                                    1.98           2.16   
CMA                                                    3.58           2.82   
Fama/French Research Portfolios                           -              -   
Size and Book-to-Market Portfolios                        -              -   
Small Value                                            5.77          -4.01   
Small Neutral                                          3.84          -1.84   
Big Neutral                                           -2.46          -7.08   
Small Growth                                           5.54           0.74   
Big Value                                              3.97           1.38   
Big Growth                                             0.30           1.04   
Size and Operating Profitability Portfolios               -              -   
Small Robust                                           3.73          -6.10   
Small Neutral                                          4.50          -1.20   
Small Weak                                            -0.22          -6.10   
Big Robust                                             1.12           2.24   
Big Neutral                                            2.60           0.67   
Big Weak                                               1.11          -2.08   
Size and Investment Portfolios                            -              -   
Small Conservative                                     3.57          -3.90   
Small Neutral                                          3.57          -1.41   
Small Aggressive                                       0.15          -6.10   
Big Conservative                                       3.08           2.35   
Big Neutral                                            2.42           1.45   
Big Aggressive                                        -0.66          -1.09   
                                            Last 12  Months  
Fama/French 3 Research Factors                            -  
Rm-Rf                                                 -0.45  
SMB                                                  -14.60  
HML                                                   -4.92  
Fama/French 5 Research Factors (2x3)                      -  
Rm-Rf                                                 -0.45  
SMB                                                  -14.74  
HML                                                   -4.92  
RMW                                                    4.97  
CMA                                                    2.98  
Fama/French Research Portfolios                           -  
Size and Book-to-Market Portfolios                        -  
Small Value                                          -16.59  
Small Neutral                                         -9.19  
Big Neutral                                          -12.36  
Small Growth                                          -1.87  
Big Value                                              3.79  
Big Growth                                             3.73  
Size and Operating Profitability Portfolios               -  
Small Robust                                         -15.42  
Small Neutral                                         -7.23  
Small Weak                                           -15.73  
Big Robust                                             4.76  
Big Neutral                                            3.40  
Big Weak                                              -4.88  
Size and Investment Portfolios                            -  
Small Conservative                                   -14.66  
Small Neutral                                         -8.16  
Small Aggressive                                     -15.00  
Big Conservative                                       5.23  
Big Neutral                                            4.49  
Big Aggressive                                        -0.38
```

## [AkShare](https://github.com/jindaxiang/akshare) 政策不确定性数据

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

## [AkShare](https://github.com/jindaxiang/akshare) 学术专栏

### Amit Goyal

#### 标普500和常用经济指标

接口: agoyal_stock_return

目标地址: http://www.hec.unil.ch/agoyal/

描述: 获取 Amit Goyal 在其论文:  A comprehensive look at the empirical performance of
equity premium prediction 中的标普 500 和常用经济指标

限量: 单次返回指定 **indicator** 的数据，本数据大约每年中旬更新(现在更新到 **2018** 年)

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| indicator | str  | Y    |  indicator="monthly"; 可以选择 {"Monthly", "Quarterly", "Annual"} 之一|

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| ---------- | ----- | -------- | ---------------- |
| yyyymm      | str   | Y        | -  |  
| Index      | str   | Y        | -  |  
| D12      | str   | Y        | -  |  
| E12      | str   | Y        | -  |  
| b/m      | str   | Y        | -  |  
| tbl      | str   | Y        | -  |  
| AAA      | str   | Y        | -  |  
| BAA      | str   | Y        | -  |  
| lty      | str   | Y        | -  |  
| ntis      | str   | Y        | -  |  
| Rfree      | str   | Y        | -  |  
| infl      | str   | Y        | -  |  
| ltr      | str   | Y        | -  |  
| corpr      | str   | Y        | -  |  
| svar      | str   | Y        | -  |  
| csp      | str   | Y        | -  |  
| CRSP_SPvw      | str   | Y        | -  |  
| CRSP_SPvwx      | str   | Y        | -  |  

接口示例

```python
import akshare as ak
agoyal_stock_return_df = ak.agoyal_stock_return(indicator="monthly")
print(agoyal_stock_return_df)
```

数据示例

```
      yyyymm    Index        D12     E12  ...      svar  csp  CRSP_SPvw  CRSP_SPvwx
0     187101     4.44   0.260000    0.40  ...       NaN  NaN        NaN         NaN
1     187102     4.50   0.260000    0.40  ...       NaN  NaN        NaN         NaN
2     187103     4.61   0.260000    0.40  ...       NaN  NaN        NaN         NaN
3     187104     4.74   0.260000    0.40  ...       NaN  NaN        NaN         NaN
4     187105     4.86   0.260000    0.40  ...       NaN  NaN        NaN         NaN
      ...      ...        ...     ...  ...       ...  ...        ...         ...
1771  201808  2901.52  52.338996  130.39  ...  0.000471  NaN   0.032938    0.030647
1772  201809  2913.98  52.338996  130.39  ...  0.000230  NaN   0.005138    0.003758
1773  201810  2711.74  53.748178  132.39  ...  0.004578  NaN  -0.068409   -0.069492
1774  201811  2760.17  53.748178  132.39  ...  0.002838  NaN   0.019980    0.017477
1775  201812  2506.85  53.748178  132.39  ...  0.006793  NaN  -0.090928   -0.092457
```
