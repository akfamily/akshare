## [AkShare](https://github.com/jindaxiang/akshare) 指数数据

### 全球指数数据

接口: get_country_index

目标地址: https://cn.investing.com/indices/

描述: 获取世界主要国家的各种指数, 由于涉及国家和指数(**1000**+个指数)具体参见[国家-指数目录](https://cn.investing.com/indices/world-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on)
具体的调用方式可以参照:

1. 先查询指数所在的国家名称;
2. 复制网页上国家名称(推荐复制), 如 **美国**;
3. 复制所显示的具体指数名称(推荐复制, 如果英文中间有空格, 也需要保留空格), 如 **美元指数**;
4. 在安装 [AkShare](https://github.com/jindaxiang/akshare) 后输入, 如 **ak.get_country_index(country="美国", index_name="美元指数", start_date='2000/01/01', end_date='2019/10/17')**;
5. 稍后就可以获得所需数据.

限量: 单次返回某一个国家的具体某一个指数, 建议用 for 循环获取多个国家的多个指数, 注意不要大量获取, 以免给对方服务器造成压力!

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| country | str  | Y    |   country="美国"|
| index_name | str  | Y    |  index_name="美元指数"|
| start_date | str  | Y    |  start_date='2000/01/01'|
| end_date | str  | Y    |  end_date='2019/10/17'|

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 收盘      | float   | Y        | 收盘   |
| 开盘      | float   | Y        | 开盘        |
| 高        | float   | Y        |高    |
| 低         | float | Y        | 低         |
| 交易量      | float | Y        | 交易量      |
| 百分比变化  | str | Y        | 百分比变化  |



接口示例
```python
import akshare as ak
index_df = ak.get_country_index(country="美国", index_name="美元指数", start_date='2000/01/01', end_date='2019/10/17')
print(index_df)
print(index_df.name)
```

数据示例

index_df.name:

```美元指数历史数据```

index_df:

```
0               收盘      开盘       高       低 交易量   百分比变化
日期                                                    
2019-05-10   97.33   97.43   97.45   97.13   -  -0.04%
2019-05-09   97.37   97.58   97.70   97.24   -  -0.26%
2019-05-08   97.62   97.57   97.68   97.42   -  -0.01%
2019-05-07   97.63   97.52   97.74   97.38   -   0.11%
2019-05-06   97.52   97.56   97.70   97.46   -   0.00%
...            ...     ...     ...     ...  ..     ...
2000-01-07  100.80  100.49  100.93  100.44   -   0.15%
2000-01-06  100.65  100.31  100.81   99.81   -   0.27%
2000-01-05  100.38  100.42  100.47   99.71   -  -0.03%
2000-01-04  100.41  100.55  100.86  100.01   -   0.19%
2000-01-03  100.22  101.67  101.83  100.19   -  -1.62%
```

### 微博指数数据

接口: weibo_index

目标地址: https://data.weibo.com/index/newindex

描述: 获取指定 **词语** 的微博指数

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| word | str  | Y    |   word="股票"|
| time_type | str  | Y    |  time_type="1hour"; 1hour, 1day, 1month, 3month 选其一|

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| date      | datetime   | Y        | 日期-索引  |
| index      | float   | Y        | 指数   |

接口示例

```python
import akshare as ak
df_index = ak.weibo_index(word="期货", time_type="3month")
print(df_index)
```

数据示例

```
             期货
index          
20190901  13334
20190902  46214
20190903  49017
20190904  53229
20190905  68506
         ...
20191127  68081
20191128  42348
20191129  62141
20191130  23448
20191201  16169
```
