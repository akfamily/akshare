## [AkShare](https://github.com/jindaxiang/akshare) 宏观数据

### 中国宏观

#### 中国CPI年率报告
接口: get_china_yearly_cpi

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_cpi_yoy

描述: 获取中国年度CPI数据, 数据区间从19860201-至今

限量: 单次返回某一个所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 年率      | float   | Y        | 年率   |


接口示例
```python
import akshare as ak
index_df = ak.get_china_yearly_cpi()
print(index_df)
print(index_df.name)
```

数据示例

index_df.name:

```cpi```

index_df:

```
1986-02-01    7.1
1986-03-01    7.1
1986-04-01    7.1
1986-05-01    7.1
1986-06-01    7.1
             ... 
2019-07-10    2.7
2019-08-09    2.8
2019-09-10    2.8
2019-10-15      3
2019-11-09      0
```


#### 中国CPI月率报告
接口: get_china_monthly_cpi

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_cpi_mom

描述: 获取中国月度CPI数据, 数据区间从19960201-至今

限量: 单次返回某一个所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 月率      | float   | Y        | 年率   |


接口示例
```python
import akshare as ak
index_df = ak.get_china_monthly_cpi()
print(index_df)
print(index_df.name)
```

数据示例

index_df.name:

```cpi```

index_df:

```
1996-02-01     2.1
1996-03-01     2.3
1996-04-01     0.6
1996-05-01     0.7
1996-06-01    -0.5
              ... 
2019-07-10    -0.1
2019-08-09     0.4
2019-09-10     0.7
2019-10-15     0.9
2019-11-09       0
```

#### 中国M2年率报告
接口: get_china_yearly_m2

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_m2_money_supply_yoy

描述: 获取中国年度M2数据, 数据区间从19980201-至今

限量: 单次返回某一个所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 年率      | float   | Y        | 年率   |


接口示例
```python
import akshare as ak
index_df = ak.get_china_yearly_m2()
print(index_df)
print(index_df.name)
```

数据示例

index_df.name:

```m2```

index_df:

```
1998-02-01    17.4
1998-03-01    16.7
1998-04-01    15.4
1998-05-01    14.6
1998-06-01    15.5
              ... 
2019-09-11     8.2
2019-09-13       0
2019-10-14       0
2019-10-15     8.4
2019-10-17       0
```


### 美国宏观

#### 美联储利率决议报告

接口: get_usa_interest_rate

目标地址: https://datacenter.jin10.com/reportType/dc_usa_interest_rate_decision

描述: 获取美联储利率决议报告, 数据区间从19820927-至今

限量: 单次返回某一个所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 今值(%)     | float   | Y        | 今值(%)   |


接口示例
```python
import akshare as ak
index_se = ak.get_usa_interest_rate()
print(index_se)
print(index_se.name)
```

数据示例

index_se.name

```interest_rate```

index_se: pandas.Series

```
1982-09-27    10.25
1982-10-01       10
1982-10-07      9.5
1982-11-19        9
1982-12-14      8.5
              ...
2019-06-20      2.5
2019-08-01     2.25
2019-09-19        2
2019-10-31        0
2019-12-12        0
```

#### 美国非农就业人数报告

接口: get_usa_non_farm

目标地址: https://datacenter.jin10.com/reportType/dc_nonfarm_payrolls

描述: 获取美国非农就业人数报告, 数据区间从19700102-至今

限量: 单次返回某一个所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 今值(万人)      | float   | Y        | 今值(万人)   |


接口示例

```python
import akshare as ak
index_se = ak.get_usa_non_farm()
print(index_se.name)
print(index_se)
```

数据示例

index_se.name

```non_farm```

index_se: pandas.Series

```
1970-01-02    15.3
1970-02-06    -6.4
1970-03-06    12.8
1970-04-03    14.8
1970-05-01   -10.4
              ...
2019-07-05    19.3
2019-08-02    15.9
2019-09-06    16.8
2019-10-04    13.6
2019-11-01       0
```


#### 美国失业率报告

接口: get_usa_unemployment_rate

目标地址: https://datacenter.jin10.com/reportType/dc_usa_unemployment_rate

描述: 获取美国失业率报告, 数据区间从19700101-至今

限量: 单次返回某一个所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 今值(%)      | float   | Y        | 今值(%)   |


接口示例

```python
import akshare as ak
index_se = ak.get_usa_unemployment_rate()
print(index_se.name)
print(index_se)
```

数据示例

index_se.name

```unemployment_rate```

index_se: pandas.Series

```
1970-01-01    3.5
1970-02-01    3.9
1970-03-01    4.2
1970-04-01    4.4
1970-05-01    4.6
             ...
2019-07-05    3.7
2019-08-02    3.7
2019-09-06    3.7
2019-10-04    3.5
2019-11-01      0
```


#### 美国失业率报告

接口: get_usa_eia_crude_rate

目标地址: https://datacenter.jin10.com/reportType/dc_eia_crude_oil

描述: 获取美国EIA原油库存报告, 数据区间从19950801-至今

限量: 单次返回某一个所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 今值(万桶)      | float   | Y        | 今值(万桶)   |


接口示例

```python
import akshare as ak
index_se = ak.get_usa_eia_crude_rate()
print(index_se.name)
print(index_se)
```

数据示例

index_se.name

```eia_crude_rate```

index_se: pandas.Series

```
1982-09-01   -262.6
1982-10-01       -8
1982-11-01    -41.3
1982-12-01    -87.6
1983-01-01     51.3
              ...
2019-10-02      310
2019-10-09    292.7
2019-10-16        0
2019-10-17    928.1
2019-10-23        0
```
