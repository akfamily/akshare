# 另类数据

## 汽车销量排行

(car_market_total_cpca)=
### 乘联会-统计数据-总体市场

接口：car_market_total_cpca

目标地址：http://data.cpcadata.com/TotalMarket

描述：乘联会-统计数据-总体市场

限量：单次返回指定 symbol 和 indicator 的数据

输入参数

| 名称        | 类型  | 描述                                                 |
|-----------|-----|----------------------------------------------------|
| symbol    | str | symbol="狭义乘用车"; choice of {"狭义乘用车", "广义乘用车"}       |
| indicator | str | indicator="产量"; choice of {"产量", "批发", "零售", "出口"} |

输出参数

| 名称       | 类型      | 描述       |
|----------|---------|----------|
| 月份       | str     | -        |
| {前一个年份}年 | float64 | 注意单位：万辆 |
| {当前年份}年  | float64 | 注意单位：万辆 |

接口示例

```python
import akshare as ak

car_market_total_cpca_df = ak.car_market_total_cpca(symbol="狭义乘用车", indicator="产量")
print(car_market_total_cpca_df)
```

数据示例

```
     月份   2023年     2024年
0    1月  134.6266  202.0941
1    2月  166.4180  123.4852
2    3月  208.7694       NaN
3    4月  172.8825       NaN
4    5月  198.9448       NaN
5    6月  219.4569       NaN
6    7月  208.9492       NaN
7    8月  223.7048       NaN
8    9月  243.6938       NaN
9   10月  244.8691       NaN
10  11月  264.3703       NaN
11  12月  267.8423       NaN
```

(car_market_man_rank_cpca)=
### 乘联会-统计数据-厂商排名

接口：car_market_man_rank_cpca

目标地址：http://data.cpcadata.com/ManRank

描述：乘联会-统计数据-厂商排名

限量：单次返回指定 symbol 和 indicator 的数据

输入参数

| 名称        | 类型  | 描述                                                                            |
|-----------|-----|-------------------------------------------------------------------------------|
| symbol    | str | symbol="狭义乘用车-单月"; choice of {"狭义乘用车-单月", "狭义乘用车-累计", "广义乘用车-单月", "广义乘用车-累计"} |
| indicator | str | indicator="批发"; choice of {"批发", "零售"}                                        |

输出参数

| 名称       | 类型      | 描述       |
|----------|---------|----------|
| 月份       | str     | -        |
| {前一个年份}年 | float64 | 注意单位：万辆 |
| {当前年份}年  | float64 | 注意单位：万辆 |

接口示例

```python
import akshare as ak

car_market_man_rank_cpca_df = ak.car_market_man_rank_cpca(symbol="狭义乘用车-单月", indicator="批发")
print(car_market_man_rank_cpca_df)
```

数据示例

```
       厂商  2023年2月  2024年2月
0    奇瑞汽车   9.6553  13.7819
1   比亚迪汽车  19.1664  12.1748
2    吉利汽车  10.8701  11.1398
3    一汽大众  10.5007   8.4073
4    长安汽车  11.6407   8.3550
5    上汽大众   7.3303   6.3003
6    长城汽车   5.1053   6.0550
7   特斯拉中国   7.4402   6.0365
8  上汽通用五菱   3.7029   4.9366
9    华晨宝马   5.2871   4.1604
```

(car_market_cate_cpca)=
### 乘联会-统计数据-车型大类

接口：car_market_cate_cpca

目标地址：http://data.cpcadata.com/CategoryMarket

描述：乘联会-统计数据-车型大类

限量：单次返回指定 symbol 和 indicator 的数据

输入参数

| 名称        | 类型  | 描述                                                |
|-----------|-----|---------------------------------------------------|
| symbol    | str | symbol="轿车"; choice of {"轿车", "MPV", "SUV", "占比"} |
| indicator | str | indicator="批发"; choice of {"批发", "零售"}            |

输出参数

| 名称       | 类型      | 描述       |
|----------|---------|----------|
| 月份       | str     | -        |
| {前一个年份}年 | float64 | 注意单位：万辆 |
| {当前年份}年  | float64 | 注意单位：万辆 |

接口示例

```python
import akshare as ak

car_market_cate_cpca_df = ak.car_market_cate_cpca(symbol="轿车", indicator="批发")
print(car_market_cate_cpca_df)
```

数据示例

```
     月份   2023年    2024年
0    1月   63.2478  87.1795
1    2月   72.2022  54.5316
2    3月   90.4165      NaN
3    4月   79.3741      NaN
4    5月   89.9973      NaN
5    6月   98.1894      NaN
6    7月   91.2119      NaN
7    8月   97.8467      NaN
8    9月  106.0477      NaN
9   10月  105.2851      NaN
10  11月  110.8935      NaN
11  12月  122.1150      NaN
```

(car_market_country_cpca)=
### 乘联会-统计数据-国别细分市场

接口：car_market_country_cpca

目标地址：http://data.cpcadata.com/CountryMarket

描述：乘联会-统计数据-国别细分市场

限量：单次返回指定 symbol 和 indicator 的数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述       |
|------|---------|----------|
| 月份   | str     | -        |
| 自主   | float64 | 注意单位：万辆 |
| 德系   | float64 | 注意单位：万辆 |
| 日系   | float64 | 注意单位：万辆 |
| 法系   | float64 | 注意单位：万辆 |
| 美系   | float64 | 注意单位：万辆 |
| 韩系   | float64 | 注意单位：万辆 |
| 其他欧系 | float64 | 注意单位：万辆 |

接口示例

```python
import akshare as ak

car_market_country_cpca_df = ak.car_market_country_cpca()
print(car_market_country_cpca_df)
```

数据示例

```
     月份         自主      德系  ...        美系       韩系     其他欧系
0    2023-3月  52.937614  18.783411  ...  8.944649  1.841395  0.656085
1    2023-4月  56.117973  17.591091  ...  9.997354  1.454204  0.767231
2    2023-5月  54.849330  17.672825  ...  9.739207  1.441945  0.856578
3    2023-6月  53.630800  18.637491  ...  9.731017  1.782815  0.873428
4    2023-7月  58.120550  17.234150  ...  8.402960  1.375989  0.825758
5    2023-8月  57.429867  17.205738  ...  8.894298  1.640349  0.783967
6    2023-9月  56.517770  17.429178  ...  8.500368  1.590704  0.753809
7   2023-10月  59.985280  15.645699  ...  7.352488  1.470236  0.694709
8   2023-11月  59.638090  16.112440  ...  7.439157  1.567490  0.624859
9   2023-12月  57.890274  17.040712  ...  8.136273  1.738795  0.650838
10   2024-1月  60.437893  17.406410  ...  6.315318  1.404617  0.804964
11   2024-2月  60.124140  17.637665  ...  6.854863  1.837663  0.695454
[12 rows x 8 columns]
```

(car_market_segment_cpca)=
### 乘联会-统计数据-级别细分市场

接口：car_market_segment_cpca

目标地址：http://data.cpcadata.com/SegmentMarket

描述：乘联会-统计数据-级别细分市场

限量：单次返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                          |
|--------|-----|---------------------------------------------|
| symbol | str | symbol="轿车"; choice of {"轿车", "MPV", "SUV"} |

输出参数

| 名称  | 类型      | 描述       |
|-----|---------|----------|
| 月份  | str     | -        |
| A00 | float64 | 注意单位：万辆 |
| A0  | float64 | 注意单位：万辆 |
| A   | float64 | 注意单位：万辆 |
| B   | float64 | 注意单位：万辆 |
| C   | float64 | 注意单位：万辆 |

接口示例

```python
import akshare as ak

car_market_segment_cpca_df = ak.car_market_segment_cpca(symbol="轿车")
print(car_market_segment_cpca_df)
```

数据示例

```
          月份        A00         A0          A          B          C
0    2023-3月   5.456084   8.219518  42.917168  34.389297   9.017934
1    2023-4月   5.164784  10.342795  44.179653  30.211243  10.101533
2    2023-5月   4.764809   9.978744  46.005154  28.248846  11.002440
3    2023-6月   4.684416   9.713371  44.913500  30.345741  10.342969
4    2023-7月   4.699168  10.649708  45.020990  28.368778  11.261360
5    2023-8月   4.059616  11.460070  45.084000  29.152237  10.244087
6    2023-9月   7.940861   7.592339  43.092026  30.093441  11.281339
7   2023-10月   9.530694   8.313237  42.630062  28.593506  10.932507
8   2023-11月  11.200026   8.195070  40.859290  29.682444  10.063169
9   2023-12月  12.457766   8.930598  37.996150  30.184662  10.430823
10   2024-1月   9.581266   5.019070  41.158417  35.134407   9.106843
11   2024-2月   7.976292   7.585693  36.759968  36.646090  11.031953
```

(car_market_fuel_cpca)=
### 乘联会-统计数据-新能源细分市场

接口：car_market_fuel_cpca

目标地址：http://data.cpcadata.com/FuelMarket

描述：乘联会-统计数据-车型大类

限量：单次返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                                                 |
|--------|-----|--------------------------------------------------------------------|
| symbol | str | symbol="整体市场"; choice of {"整体市场", "销量占比-PHEV-BEV", "销量占比-ICE-NEV"} |

输出参数

| 名称       | 类型      | 描述       |
|----------|---------|----------|
| 月份       | str     | -        |
| {前一个年份}年 | float64 | 注意单位：万辆 |
| {当前年份}年  | float64 | 注意单位：万辆 |

接口示例

```python
import akshare as ak

car_market_fuel_cpca_df = ak.car_market_fuel_cpca()
print(car_market_fuel_cpca_df)
```

数据示例

```
     月份    2023年    2024年
0    1月  33.1542  66.7653
1    2月  43.9068  38.8294
2    3月  54.6472      NaN
3    4月  52.4730      NaN
4    5月  57.9938      NaN
5    6月  66.5066      NaN
6    7月  64.1005      NaN
7    8月  71.6335      NaN
8    9月  74.6305      NaN
9   10月  77.1797      NaN
10  11月  84.0500      NaN
11  12月  94.7347      NaN
```

(news_cctv)=
## 新闻联播文字稿

接口：news_cctv

目标地址：https://tv.cctv.com/lm/xwlb

描述：新闻联播文字稿，数据区间从 20160330-至今

限量：单次返回指定日期新闻联播文字稿数据

输入参数

| 名称   | 类型  | 描述                            |
|------|-----|-------------------------------|
| date | str | date="20240424";  20160330-至今 |

输出参数

| 名称      | 类型     | 描述   |
|---------|--------|------|
| date    | str    | 新闻日期 |
| title   | str    | 新闻标题 |
| content | str    | 新闻内容 |

接口示例

```python
import akshare as ak

news_cctv_df = ak.news_cctv(date="20240424")
print(news_cctv_df)
```

数据示例

```
      date  ...                                            content
0   20240424  ...  中共中央总书记、国家主席、中央军委主席习近平近日在重庆考察时强调，重庆要对标新时代新征程党的...
1   20240424  ...                   本台今天（4月24日）播发央视快评《奋力谱写西部大开发新篇章》。
2   20240424  ...  4月24日，国家主席习近平向首届“中国－拉美和加勒比国家航天合作论坛”致贺信。习近平指出，今...
3   20240424  ...  中共中央政治局常委、国务院总理李强4月24日在贵州调研。他强调，要深入贯彻习近平总书记关于巩...
4   20240424  ...  十四届全国人大常委会第二十四次委员长会议24日下午在北京人民大会堂举行。赵乐际委员长主持。会...
5   20240424  ...  应墨西哥参议长里维拉邀请，全国人大常委会委员长赵乐际于墨西哥当地时间23日在墨参议院成立20...
6   20240424  ...  全国政协主席王沪宁24日在京会见哈萨克斯坦议会下院议长科沙诺夫。王沪宁表示，在习近平主席和托...
7   20240424  ...  国家副主席韩正24日在京会见哈萨克斯坦议会下院议长科沙诺夫。韩正表示，去年，习近平主席同托卡...
8   20240424  ...  今天（4月24日），神舟十八号载人飞行任务新闻发布会在酒泉卫星发射中心举行，计划于4月25日...
9   20240424  ...  日前，中央纪委国家监委对八起违规吃喝典型问题进行公开通报。江西省人大常委会原党组副书记、副主...
10  20240424  ...  国务院新闻办公室今天（4月24日）举行发布会，国家知识产权局介绍，已经会同中国贸促会设立国家...
11  20240424  ...  全国多地举行中国航天日活动今天（4月24日）是第九个中国航天日，以“极目楚天，共襄星汉”为主...
[12 rows x 3 columns]
```

## 日出和日落

(sunrise_daily)=
### 日出和日落-天

接口：sunrise_daily

目标地址：https://www.timeanddate.com/sun/china/

描述：中国各大城市-日出和日落时间，数据区间从 19990101-至今，推荐使用代理访问

限量：单次返回指定日期和指定城市的数据

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20240428"            |
| city | str | city="beijing"；注意输入的城市的拼音 |

输出参数

| 名称         | 类型     | 描述                          |
|------------|--------|-----------------------------|
| date       | object | 日期                          |
| Sunrise    | str    | 日出                          |
| Sunset     | str    | 日落                          |
| Length     | str    | Daylength-Length            |
| Difference | str    | Daylength-Difference        |
| Start      | str    | Astronomical Twilight-Start |
| End        | str    | Astronomical Twilight-End   |
| Start.1    | str    | Nautical Twilight-Start     |
| End.1      | str    | Nautical Twilight-End       |
| Start.2    | str    | Civil Twilight-Start        |
| End.2      | str    | Civil Twilight-End          |
| Time       | str    | Solar Noon-Time             |
| Mil. km    | str    | Solar Noon-Mil. km          |

接口示例

```python
import akshare as ak

sunrise_daily_df = ak.sunrise_daily(date="20240428", city="beijing")
print(sunrise_daily_df)
```

数据示例

```
         date Apr          Sunrise  ...    End.2              Time Mil. mi
0  2024-04-28  28  5:18 am ↑ (71°)  ...  7:35 pm  12:11 pm (64.4°)  93.588
[1 rows x 14 columns]
```

(sunrise_monthly)=
### 日出和日落-月

接口：sunrise_monthly

目标地址：https://www.timeanddate.com/sun/china/

描述：中国各大城市-日出和日落时间，数据区间从 19990101-至今，推荐使用代理访问

限量：单次返回指定日期所在月份每天的数据，如果是未来日期则为预测值

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20240428"            |
| city | str | city="beijing"；注意输入的城市的拼音 |

输出参数

| 名称         | 类型     | 描述                          |
|------------|--------|-----------------------------|
| date       | str    | 日期-索引；XXXX-XX 格式           |
| feb        | str    | 月份简称-随月份变化                  |
| Sunrise    | str    | 日出                          |
| Sunset     | str    | 日落                          |
| Length     | str    | Daylength-Length            |
| Difference | str    | Daylength-Difference        |
| Start      | str    | Astronomical Twilight-Start |
| End        | str    | Astronomical Twilight-End   |
| Start.1    | str    | Nautical Twilight-Start     |
| End.1      | str    | Nautical Twilight-End       |
| Start.2    | str    | Civil Twilight-Start        |
| End.2      | str    | Civil Twilight-End          |
| Time       | str    | Solar Noon-Time             |
| Mil. km    | str    | Solar Noon-Mil. km          |

接口示例

```python
import akshare as ak

sunrise_monthly_df = ak.sunrise_monthly(date="20240428", city="beijing")
print(sunrise_monthly_df)
```

数据示例

```
    date Apr          Sunrise  ...    End.2              Time Mil. mi
0   202404   1  5:58 am ↑ (83°)  ...  7:06 pm  12:18 pm (54.8°)  92.891
1   202404   2  5:56 am ↑ (83°)  ...  7:07 pm  12:17 pm (55.2°)  92.918
2   202404   3  5:55 am ↑ (82°)  ...  7:08 pm  12:17 pm (55.6°)  92.945
3   202404   4  5:53 am ↑ (82°)  ...  7:09 pm  12:17 pm (56.0°)  92.972
4   202404   5  5:52 am ↑ (81°)  ...  7:10 pm  12:17 pm (56.3°)  93.000
5   202404   6  5:50 am ↑ (81°)  ...  7:11 pm  12:16 pm (56.7°)  93.027
6   202404   7  5:48 am ↑ (80°)  ...  7:12 pm  12:16 pm (57.1°)  93.054
7   202404   8  5:47 am ↑ (80°)  ...  7:13 pm  12:16 pm (57.5°)  93.080
8   202404   9  5:45 am ↑ (79°)  ...  7:14 pm  12:15 pm (57.8°)  93.107
9   202404  10  5:44 am ↑ (79°)  ...  7:15 pm  12:15 pm (58.2°)  93.133
10  202404  11  5:42 am ↑ (78°)  ...  7:16 pm  12:15 pm (58.6°)  93.159
11  202404  12  5:41 am ↑ (78°)  ...  7:17 pm  12:15 pm (58.9°)  93.185
12  202404  13  5:39 am ↑ (77°)  ...  7:18 pm  12:14 pm (59.3°)  93.211
13  202404  14  5:38 am ↑ (77°)  ...  7:19 pm  12:14 pm (59.7°)  93.237
14  202404  15  5:36 am ↑ (76°)  ...  7:20 pm  12:14 pm (60.0°)  93.262
15  202404  16  5:35 am ↑ (76°)  ...  7:22 pm  12:14 pm (60.4°)  93.288
16  202404  17  5:33 am ↑ (75°)  ...  7:23 pm  12:13 pm (60.7°)  93.313
17  202404  18  5:32 am ↑ (75°)  ...  7:24 pm  12:13 pm (61.1°)  93.338
18  202404  19  5:30 am ↑ (75°)  ...  7:25 pm  12:13 pm (61.4°)  93.364
19  202404  20  5:29 am ↑ (74°)  ...  7:26 pm  12:13 pm (61.8°)  93.389
20  202404  21  5:27 am ↑ (74°)  ...  7:27 pm  12:13 pm (62.1°)  93.414
21  202404  22  5:26 am ↑ (73°)  ...  7:28 pm  12:12 pm (62.4°)  93.439
22  202404  23  5:25 am ↑ (73°)  ...  7:29 pm  12:12 pm (62.8°)  93.464
23  202404  24  5:23 am ↑ (72°)  ...  7:30 pm  12:12 pm (63.1°)  93.489
24  202404  25  5:22 am ↑ (72°)  ...  7:31 pm  12:12 pm (63.4°)  93.514
25  202404  26  5:21 am ↑ (71°)  ...  7:32 pm  12:12 pm (63.8°)  93.539
26  202404  27  5:19 am ↑ (71°)  ...  7:33 pm  12:12 pm (64.1°)  93.563
27  202404  28  5:18 am ↑ (71°)  ...  7:35 pm  12:11 pm (64.4°)  93.588
28  202404  29  5:17 am ↑ (70°)  ...  7:36 pm  12:11 pm (64.7°)  93.613
29  202404  30  5:15 am ↑ (70°)  ...  7:37 pm  12:11 pm (65.0°)  93.637
[30 rows x 14 columns]
```

## 空气质量-河北

(air_quality_hebei)=
### 近期空气质量

接口：air_quality_hebei

目标地址：http://218.11.10.130:8080/#/application/home

描述：河北省实时空气质量数据

限量：单次返回所有城市数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称         | 类型      | 描述            |
|------------|---------|---------------|
| 城市         | str     | 城市名称          |
| 区域         | str     | 城市下属行政区域      |
| 监测点        | str     | 监测站点名称        |
| 时间         | str     | 监测时间          |
| AQI        | float64 | 空气质量指数        |
| 空气质量等级     | str     | 空气质量级别（优、良等）  |
| 首要污染物      | str     | 主要污染物         |
| 经度         | float64 | 监测站点经度        |
| 纬度         | float64 | 监测站点纬度        |
| PM10_IAQI  | float64 | PM10空气质量分指数   |
| PM10_浓度    | float64 | PM10浓度值       |
| PM2.5_IAQI | float64 | PM2.5空气质量分指数  |
| PM2.5_浓度   | float64 | PM2.5浓度值      |
| 一氧化碳_IAQI  | float64 | CO空气质量分指数     |
| 一氧化碳_浓度    | float64 | CO浓度值         |
| 二氧化氮_IAQI  | float64 | NO2空气质量分指数    |
| 二氧化氮_浓度    | float64 | NO2浓度值        |
| 二氧化硫_IAQI  | float64 | SO2空气质量分指数    |
| 二氧化硫_浓度    | float64 | SO2浓度值        |
| 臭氧1小时_IAQI | float64 | O3 1小时空气质量分指数 |
| 臭氧1小时_浓度   | float64 | O3 1小时浓度值     |
| 臭氧8小时_IAQI | float64 | O3 8小时空气质量分指数 |
| 臭氧8小时_浓度   | float64 | O3 8小时浓度值     |

接口示例

```python
import akshare as ak

air_quality_hebei_df = ak.air_quality_hebei()
print(air_quality_hebei_df)
```

数据示例

```
       城市   区域         监测点  ... 臭氧1小时_浓度  臭氧8小时_IAQI 臭氧8小时_浓度
0    石家庄市  长安区    市区22中南校区  ...     15.0         0.0     40.0
1    石家庄市  栾城区      栾城区星河路  ...      8.0         0.0     40.0
2    石家庄市  鹿泉区    鹿泉住建局(*)  ...     29.0         0.0     41.0
3    石家庄市  藁城区     藁城九中(*)  ...     16.0         0.0     43.0
4    石家庄市  桥西区      市区西南高教  ...      7.0         0.0     41.0
..    ...  ...         ...  ...      ...         ...      ...
359   衡水市  武强县   武强实验学校(*)  ...     11.0         0.0     38.0
360   衡水市   景县    景县交通局(*)  ...     28.0         0.0     48.0
361   衡水市  武邑县   武邑县委党校(*)  ...     16.0         0.0     36.0
362   衡水市   景县  景县市场监管局(*)  ...     33.0         0.0     58.0
363   衡水市  阜城县    阜城交通局(*)  ...     30.0         0.0     48.0
[364 rows x 23 columns]
```

## 空气质量-全国

(air_city_table)=
### 城市列表

接口：air_city_table

目标地址：https://www.aqistudy.cn/

描述：所有能获取空气质量数据的城市表

限量：单次返回所有可以获取的城市表数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述  |
|---------|---------|-----|
| 序号      | int64   | -   |
| 省份      | str     | -   |
| 城市      | str     | -   |
| AQI     | float64 | -   |
| 空气质量    | str     | -   |
| PM2.5浓度 | str     | -   |
| 首要污染物   | str     | -   |

接口示例

```python
import akshare as ak

air_city_table_df = ak.air_city_table()
print(air_city_table_df)
```

数据示例

```
      序号  省份  城市    AQI  空气质量    PM2.5浓度 首要污染物
0      1  北京  北京  204.0  重度污染  108 ug/m3    O3
1      2  河北  廊坊  199.0  中度污染   54 ug/m3    O3
2      3  河北  承德  198.0  中度污染   59 ug/m3    O3
3      4  河北  唐山  176.0  中度污染   74 ug/m3    O3
4      5  山西  晋城  164.0  中度污染   51 ug/m3    O3
..   ...  ..  ..    ...   ...        ...   ...
163  164  广东  中山   40.0     优   19 ug/m3   NaN
164  165  广东  东莞   39.0     优   20 ug/m3   NaN
165  166  广东  深圳   38.0     优   21 ug/m3   NaN
166  167  广东  珠海   34.0     优   17 ug/m3   NaN
167  168  海南  海口   32.0     优   14 ug/m3   NaN
```

(air_quality_hist)=
### 空气质量历史数据

接口：air_quality_hist

目标地址：https://www.zq12369.com/

描述：指定城市和数据频率下并且在指定时间段内的空气质量数据

限量：单次返回所有的数据；上游只提供最近约一年的数据，更早的日期返回空表；提取小时频率数据时时间跨度不宜过长

输入参数

| 名称         | 类型  | 描述                                                                             |
|------------|-----|--------------------------------------------------------------------------------|
| city       | str | city="北京"；调用 ak.air_city_table() 接口获取所有城市列表                                   |
| period     | str | period="day"; "hour": 每小时一个数据，由于数据量比较大，下载较慢；"day": 每天一个数据；"month": 每个月一个数据，上游目前返回其他城市的数据，会报错 |
| start_date | str | start_date="20260901"；注意 **start_date** 和 **end_date** 跨度不宜过长                 |
| end_date   | str | end_date="20261028"；注意 **start_date** 和 **end_date** 跨度不宜过长                   |

输出参数

| 名称                | 类型      | 描述     |
|-------------------|---------|--------|
| time              | str     | 日期时间索引 |
| aqi               | str     | AQI    |
| pm2_5             | float64 | PM2.5  |
| pm10              | str     | PM10   |
| co                | float64 | CO     |
| no2               | str     | NO2    |
| o3                | str     | O3     |
| so2               | str     | SO2    |
| complexindex      | str     | 综合指数   |
| rank              | str     | 排名     |
| primary_pollutant | str     | 主要污染物  |
| temp              | str     | 温度     |
| humi              | str     | 湿度     |
| windlevel         | str     | 风级     |
| winddirection     | str     | 风向     |
| weather           | str     | 天气     |

接口示例-小时频率

```python
import akshare as ak

air_quality_hist_df = ak.air_quality_hist(city="北京", period="hour", start_date="20261027", end_date="20261028")
print(air_quality_hist_df)
```

数据示例-小时频率

```
                      aqi  pm2_5  pm10  ...  windlevel winddirection weather
time                                    ...
2026-10-27 00:00:00  28.0    2.0   8.0  ...        5.0            西风       晴
2026-10-27 01:00:00  27.0    2.0   7.0  ...        3.0           西北风       晴
2026-10-27 02:00:00  27.0    1.0   6.0  ...        4.0            西风       晴
2026-10-27 03:00:00  28.0    1.0   6.0  ...        3.0           西北风       晴
2026-10-27 04:00:00  27.0    1.0   7.0  ...        3.0           西北风       晴
...
2026-10-28 19:00:00  74.0   45.0  83.0  ...        1.0           东南风       晴
2026-10-28 20:00:00  78.0   48.0  88.0  ...        1.0            南风       晴
2026-10-28 21:00:00  76.0   48.0  86.0  ...        1.0           西南风       晴
2026-10-28 22:00:00  73.0   45.0  81.0  ...        1.0            北风       霾
2026-10-28 23:00:00  66.0   40.0  72.0  ...        1.0           东北风       -

[48 rows x 15 columns]
```

接口示例-天频率

```python
import akshare as ak

air_quality_hist_df = ak.air_quality_hist(city="北京", period="day", start_date="20260901", end_date="20261028")
print(air_quality_hist_df)
```

数据示例-天频率

```
              aqi  pm2_5   pm10  ...  windlevel winddirection weather
time                             ...
2026-09-01   47.0    8.0   18.0  ...      1.611                     晴
2026-09-02   85.0   14.0   31.0  ...      1.409                     晴
2026-09-03   78.0   16.0   32.0  ...      1.333                     晴
2026-09-04   70.0   13.0   30.0  ...      1.292                     晴
2026-09-05  110.0   18.0   38.0  ...      1.458                     晴
...
2026-10-24  117.0   78.0  103.0  ...      1.083                     霾
2026-10-25   43.0   30.0   41.0  ...      1.417                     阴
2026-10-26   32.0    6.0   10.0  ...      1.958                     阴
2026-10-27   31.0    4.0   17.0  ...      2.417                     晴
2026-10-28   53.0   26.0   53.0  ...      1.500                     霾

[58 rows x 15 columns]
```

(air_quality_rank)=
### 空气质量排名

接口：air_quality_rank

目标地址：https://www.zq12369.com/environment.php

描述：获取指定 date 时间点上所有城市（168个）的空气质量数据

限量：单次返回所有的数据

输入参数

| 名称   | 类型  | 描述                                                                                       |
|------|-----|------------------------------------------------------------------------------------------|
| date | str | date=""; "": 当前时刻空气质量排名，默认；"20200312": 当日空气质量排名；"202003": 当月空气质量排名；"2019": 当年空气质量排名；|

输出参数

| 名称      | 类型    | 描述  |
|---------|-------|-----|
| 降序      | str   | 排名  |
| 省份      | str   | -   |
| 城市      | str   | -   |
| AQI     | float64 | -   |
| 空气质量    | str   | -   |
| PM2.5浓度 | str   | -   |
| 首要污染物   | str   | -   |

接口示例-实时

```python
import akshare as ak

air_quality_rank_df = ak.air_quality_rank(date="")
print(air_quality_rank_df)
```

数据示例-实时

```
        降序  省份  城市    AQI  空气质量   PM2.5浓度  首要污染物
1      1.0  山西  太原  123.0  轻度污染  93 ug/m3  PM2.5
2      2.0  山东  德州  116.0  轻度污染  33 ug/m3   PM10
3      3.0  河南  安阳  111.0  轻度污染  60 ug/m3   PM10
4      4.0  吉林  长春  108.0  轻度污染  81 ug/m3  PM2.5
5      5.0  广东  佛山  100.0     良  55 ug/m3     O3
..     ...  ..  ..    ...   ...       ...    ...
164  164.0  广东  珠海   34.0     优  16 ug/m3    NaN
165  165.0  江苏  南通   34.0     优  23 ug/m3    NaN
166  166.0  浙江  舟山   30.0     优  11 ug/m3    NaN
167  167.0  四川  雅安   30.0     优  13 ug/m3    NaN
168  168.0  西藏  拉萨   29.0     优   9 ug/m3    NaN
```

接口示例-具体某天

```python
import akshare as ak
air_quality_rank_df = ak.air_quality_rank(date="2020-03-20")
print(air_quality_rank_df)
```

数据示例-具体某天

```
        降序   省份    城市    AQI  空气质量   PM2.5浓度 首要污染物
1      1.0   山西    晋城  124.0  轻度污染  42 ug/m3  PM10
2      2.0   山东    德州  120.0  轻度污染  36 ug/m3  PM10
3      3.0   河南    焦作  118.0  轻度污染  42 ug/m3  PM10
4      4.0   山东    菏泽  118.0  轻度污染  33 ug/m3  PM10
5      5.0   河南    安阳  118.0  轻度污染  44 ug/m3  PM10
..     ...  ...   ...    ...   ...       ...   ...
164  164.0   广东    深圳   45.0     优  29 ug/m3   NaN
165  165.0  黑龙江   哈尔滨   43.0     优  30 ug/m3   NaN
166  166.0   广东    惠州   43.0     优  30 ug/m3   NaN
167  167.0   新疆  乌鲁木齐   32.0     优  17 ug/m3   NaN
168  168.0   海南    海口   29.0     优  13 ug/m3   NaN
```

接口示例-具体某月

```python
import akshare as ak
air_quality_rank_df = ak.air_quality_rank(date="2020-03")
print(air_quality_rank_df)
```

数据示例-具体某月

```
        降序  省份  城市  综合指数  最大指数  首要污染物
1      1.0  河南  安阳  5.29  1.60  PM2.5
2      2.0  山东  淄博  5.27  1.51  PM2.5
3      3.0  山东  枣庄  5.19  1.54  PM2.5
4      4.0  河南  焦作  5.16  1.54   PM10
5      5.0  陕西  西安  5.11  1.59   PM10
..     ...  ..  ..   ...   ...    ...
164  164.0  广东  惠州  2.52  0.69     O3
165  165.0  广东  中山  2.51  0.74     O3
166  166.0  浙江  舟山  2.27  0.70     O3
167  167.0  海南  海口  1.84  0.58     O3
168  168.0  西藏  拉萨  1.78  0.72     O3
```

接口示例-具体某年

```python
import akshare as ak
air_quality_rank_df = ak.air_quality_rank(date="2019")
print(air_quality_rank_df)
```

数据示例-具体某年

```
        降序  省份   城市  综合指数  最大指数  首要污染物
1      1.0  河南   安阳  6.91  2.03  PM2.5
2      2.0  河北   邢台  6.85  1.86  PM2.5
3      3.0  河北  石家庄  6.80  1.80  PM2.5
4      4.0  河北   邯郸  6.77  1.89  PM2.5
5      5.0  山西   临汾  6.74  1.77  PM2.5
..     ...  ..  ...   ...   ...    ...
164  164.0  福建   厦门  2.98  0.84     O3
165  165.0  安徽   黄山  2.95  0.84     O3
166  166.0  浙江   舟山  2.68  0.82     O3
167  167.0  海南   海口  2.47  0.90     O3
168  168.0  西藏   拉萨  2.39  0.81     O3
```

(air_quality_watch_point)=
### 监测点空气质量

接口：air_quality_watch_point

目标地址：https://www.zq12369.com/environment.php

描述：获取每个城市的所有空气质量监测点的数据

限量：单次返回指定城市指定日期区间的所有监测点的空气质量数据；上游只提供近期的数据，2022 年及更早的日期返回空表

输入参数

| 名称         | 类型     | 描述                                           |
|------------|--------|----------------------------------------------|
| city       | object | city="杭州"；调用 ak.air_city_table() 接口获取所有城市列表 | |
| start_date | object | start_date="20261027"                        |
| end_date   | object | end_date="20261028"                          |

输出参数

| 名称        | 类型      | 描述    |
|-----------|---------|-------|
| pointname | str     | 监测点名称 |
| aqi       | float64 | AQI   |
| pm2_5     | float64 | PM2.5 |
| pm10      | float64 | PM10  |
| no2       | float64 | NO2   |
| so2       | float64 | SO2   |
| o3        | float64 | O3    |
| co        | float64 | CO    |

接口示例

```python
import akshare as ak

air_quality_watch_point_df = ak.air_quality_watch_point(city="杭州", start_date="20261027", end_date="20261028")
print(air_quality_watch_point_df)
```

数据示例

```
   pointname      aqi  ...                  o3                  co
0         滨江  62.0000  ...               119.9                0.59
1       和睦小学  59.5000  ...  123.39999999999999               0.595
2        临平镇  59.0000  ...  116.30000000000001  0.6849999999999999
3         下沙  58.0000  ...               119.2                0.69
4       消防大队  56.0000  ...               116.9                0.69
5        城厢镇  55.5000  ...  110.10000000000001                0.69
6       市府大楼  55.5000  ...               113.5                0.49
7        镇二中  54.0000  ...               110.2                0.69
8       浙江农大  52.5000  ...               110.9                0.69
9         西溪  52.5000  ...               107.2                0.49
10        云栖  49.0000  ...  101.10000000000001                0.69
11       卧龙桥  48.5000  ...               104.1                0.49
12      桐庐江北  43.0000  ...                   0                0.79
13      桐庐江南  42.5000  ...                   0               0.795
14      第二中学  40.5000  ...                   0               0.795
15    建德监测大楼  38.0000  ...                   0                 0.7
16    淳安环保大楼  31.0000  ...                   0                 0.6
17    老年活动中心  28.5000  ...                   0               0.595

[18 rows x 8 columns]
```

(forbes_rank)=
## 福布斯中国榜单

接口：forbes_rank

目标地址：https://www.forbeschina.com/lists

描述：福布斯中国-榜单数据，一共 87 个指标的数据可以获取

限量：单次返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                                                                                                  |
|--------|-----|-----------------------------------------------------------------------------------------------------|
| symbol | str | symbol="2020年福布斯中国400富豪榜"；参考 **福布斯中国指标一览表**，也可以访问 https://www.forbeschina.com/lists 获取所需要的 symbol |

福布斯中国指标一览表

|     | name                     | url                                    |
|----:|:-------------------------|:---------------------------------------|
|   0 | 2020福布斯中国400富豪榜          | https://www.forbeschina.com/lists/1750 |
|   1 | 2020福布斯菲律宾富豪榜            | https://www.forbeschina.com/lists/1746 |
|   2 | 2020福布斯美国富豪榜             | https://www.forbeschina.com/lists/1745 |
|   3 | 2020福布斯中国名人榜             | https://www.forbeschina.com/lists/1744 |
|   4 | 2020福布斯新加坡富豪榜            | https://www.forbeschina.com/lists/1743 |
|   5 | 2020福布斯中国最佳CEO榜          | https://www.forbeschina.com/lists/1741 |
|   6 | 2020福布斯中国医疗健康富豪榜         | https://www.forbeschina.com/lists/1740 |
|   7 | 2020福布斯中国慈善榜             | https://www.forbeschina.com/lists/1739 |
|   8 | 2020福布斯韩国富豪榜             | https://www.forbeschina.com/lists/1738 |
|   9 | 2020福布斯中国科技女性榜           | https://www.forbeschina.com/lists/1737 |
|  10 | 2020福布斯全球亿万富豪榜中国子榜       | https://www.forbeschina.com/lists/1734 |
|  11 | 2020福布斯全球亿万富豪榜           | https://www.forbeschina.com/lists/1733 |
|  12 | 2019福布斯中国400富豪榜          | https://www.forbeschina.com/lists/1728 |
|  13 | 2019福布斯中国最佳创投人TOP100     | https://www.forbeschina.com/lists/1747 |
|  14 | 2019福布斯全球最有影响力体育经纪人      | https://www.forbeschina.com/lists/1727 |
|  15 | 2019福布斯中国30位30岁以下精英榜     | https://www.forbeschina.com/lists/1725 |
|  16 | 2019福布斯美国400富豪榜          | https://www.forbeschina.com/lists/1722 |
|  17 | 2019福布斯菲律宾富豪榜            | https://www.forbeschina.com/lists/1721 |
|  18 | 2019福布斯中国慈善榜             | https://www.forbeschina.com/lists/1718 |
|  19 | 2019福布斯100名人榜            | https://www.forbeschina.com/lists/1717 |
|  20 | 2019福布斯韩国富豪榜             | https://www.forbeschina.com/lists/1716 |
|  21 | 2019福布斯马来西亚50富豪榜         | https://www.forbeschina.com/lists/19   |
|  22 | 2019福布斯中国最杰出商界女性排行榜      | https://www.forbeschina.com/lists/1165 |
|  23 | 2019福布斯全球亿万富豪榜           | https://www.forbeschina.com/lists/21   |
|  24 | 2018福布斯中国商界25位潜力女性       | https://www.forbeschina.com/lists/13   |
|  25 | 2018福布斯中国慈善榜             | https://www.forbeschina.com/lists/1156 |
|  26 | 2018福布斯中国最佳创投人TOP100     | https://www.forbeschina.com/lists/1258 |
|  27 | 2018福布斯中国最富有女性Top25      | https://www.forbeschina.com/lists/11   |
|  28 | 2018福布斯中国最佳女性创投人TOP25    | https://www.forbeschina.com/lists/12   |
|  29 | 2018中国最杰出商界女性排行榜         | https://www.forbeschina.com/lists/1145 |
|  30 | 2018中国分析师最佳价值发现榜         | https://www.forbeschina.com/lists/1147 |
|  31 | 2018中国最佳分析师50强榜          | https://www.forbeschina.com/lists/1148 |
|  32 | 2018福布斯中国分析师最佳预测盈利能力榜    | https://www.forbeschina.com/lists/1149 |
|  33 | 2018全球亿万富豪榜              | https://www.forbeschina.com/lists/1151 |
|  34 | 2018福布斯中国30位30岁以下精英榜     | https://www.forbeschina.com/lists/1157 |
|  35 | 2018福布斯中国上市公司最佳CEO       | https://www.forbeschina.com/lists/1159 |
|  36 | 2018福布斯中国400富豪榜          | https://www.forbeschina.com/lists/1162 |
|  37 | 2017福布斯全球科技界100富豪榜       | https://www.forbeschina.com/lists/1618 |
|  38 | 2017福布斯中国30位30岁以下精英榜     | https://www.forbeschina.com/lists/1617 |
|  39 | 2017华人富豪榜                | https://www.forbeschina.com/lists/1131 |
|  40 | 2017全球亿万富豪榜              | https://www.forbeschina.com/lists/1132 |
|  41 | 2017福布斯全球运动员收入榜          | https://www.forbeschina.com/lists/1644 |
|  42 | 2017福布斯台湾50富豪榜           | https://www.forbeschina.com/lists/1133 |
|  43 | 2017福布斯中国上市公司最佳CEO       | https://www.forbeschina.com/lists/1134 |
|  44 | 2017福布斯中国名人榜             | https://www.forbeschina.com/lists/1135 |
|  45 | 2017中国慈善榜                | https://www.forbeschina.com/lists/1681 |
|  46 | 2017分析师最佳预测盈利能力榜         | https://www.forbeschina.com/lists/1253 |
|  47 | 2017福布斯中国最佳创投人TOP100     | https://www.forbeschina.com/lists/1254 |
|  48 | 2017中国最佳分析师50强榜          | https://www.forbeschina.com/lists/1252 |
|  49 | 2020年福布斯世界最佳雇主TOP100     | https://www.forbeschina.com/lists/1749 |
|  50 | 2020福布斯中国上市公司潜力企业榜       | https://www.forbeschina.com/lists/1748 |
|  51 | 2020福布斯亚州中小上市企业榜         | https://www.forbeschina.com/lists/1742 |
|  52 | 2020福布斯中国最具创新力企业榜        | https://www.forbeschina.com/lists/1736 |
|  53 | 2020福布斯全球企业2000强榜        | https://www.forbeschina.com/lists/1735 |
|  54 | 2019福布斯全球最具价值的体育经纪机构     | https://www.forbeschina.com/lists/1726 |
|  55 | 2019福布斯全球数字经济100强榜       | https://www.forbeschina.com/lists/1724 |
|  56 | 2019福布斯中国最具创新力企业榜        | https://www.forbeschina.com/lists/1715 |
|  57 | 2018福布斯中国新三板企业融资能力榜TOP50 | https://www.forbeschina.com/lists/14   |
|  58 | 2018福布斯中国最具创新力企业榜        | https://www.forbeschina.com/lists/17   |
|  59 | 2018非上市公司潜力企业榜           | https://www.forbeschina.com/lists/18   |
|  60 | 2018福布斯中国最佳创投机构          | https://www.forbeschina.com/lists/20   |
|  61 | 2018上市公司潜力企业榜            | https://www.forbeschina.com/lists/1152 |
|  62 | 2018福布斯中国新三板TOP100       | https://www.forbeschina.com/lists/1155 |
|  63 | 2018福布斯中国最佳PE机构          | https://www.forbeschina.com/lists/1257 |
|  64 | 2017福布斯中国家族企业            | https://www.forbeschina.com/lists/1136 |
|  65 | 2017福布斯全球企业2000强         | https://www.forbeschina.com/lists/1139 |
|  66 | 2017值得关注的新三板企业           | https://www.forbeschina.com/lists/1459 |
|  67 | 2017中国非上市公司潜力企业榜         | https://www.forbeschina.com/lists/1460 |
|  68 | 2017福布斯中国最佳PE机构          | https://www.forbeschina.com/lists/1255 |
|  69 | 2017福布斯中国最佳创投机构          | https://www.forbeschina.com/lists/1256 |
|  70 | 2019福布斯美国大学排行榜           | https://www.forbeschina.com/lists/1720 |
|  71 | 2018福布斯创新力最强的30个城市       | https://www.forbeschina.com/lists/15   |
|  72 | 2018福布斯最适合新生活的宜居城市       | https://www.forbeschina.com/lists/16   |
|  73 | 2018福布斯中国大陆最佳商业城市        | https://www.forbeschina.com/lists/1163 |
|  74 | 2017福布斯中国大陆最佳商业城市        | https://www.forbeschina.com/lists/1138 |
|  75 | 2017福布斯中国大陆最佳地级城市30强     | https://www.forbeschina.com/lists/1140 |
|  76 | 2017福布斯中国大陆最佳县级城市30强     | https://www.forbeschina.com/lists/1141 |
|  77 | 2017福布斯创新力最强的30个城市       | https://www.forbeschina.com/lists/1142 |
|  78 | 2017福布斯经营成本最高的30个城市      | https://www.forbeschina.com/lists/1143 |
|  79 | 2015福布斯全球最适宜经商的国家和地区     | https://www.forbeschina.com/lists/1120 |
|  80 | 2015美国最适宜经商和就业的城市        | https://www.forbeschina.com/lists/1453 |
|  81 | 2015美国就业增长最快城市100强       | https://www.forbeschina.com/lists/1525 |
|  82 | 2015美国最适合经商和就业的州         | https://www.forbeschina.com/lists/1526 |
|  83 | 2014美国最适宜经商和就业的地区        | https://www.forbeschina.com/lists/1515 |
|  84 | 2014福布斯美国最适合经商和就业的州      | https://www.forbeschina.com/lists/1516 |
|  85 | 2014年世界最负盛名城市榜           | https://www.forbeschina.com/lists/1517 |
|  86 | 2014福布斯全球最适宜经商的国家和地区     | https://www.forbeschina.com/lists/1524 |

输出参数

| 名称  | 类型  | 描述              |
|-----|-----|-----------------|
| 排名  | str | -               |
| -   | -   | 根据不同的 symbol 而异 |

接口示例

```python
import akshare as ak

forbes_rank_df = ak.forbes_rank(symbol="2020福布斯中国400富豪榜")
print(forbes_rank_df)
```

数据示例

```
      排名     姓名  财富（亿元）       财富来源  年龄 居住城市
0      1     马云  4377.2       阿里巴巴  56   杭州
1      2    马化腾  3683.2         腾讯  49   深圳
2      3    钟睒睒  3596.5  农夫山泉/万泰生物  65   杭州
3      4  孙飘扬家族  2335.4  恒瑞医药/翰森制药  62  连云港
4      5  何享健家族  2148.5       美的集团  78   佛山
..   ...    ...     ...        ...  ..  ...
395  394  李文美家族   105.4       万孚生物  58   广州
396  397    郭梓文   104.8       中国奥园  56   香港
397  398  袁建栋家族   104.1       博瑞医药  50   苏州
398  399     王帅   103.4       蚂蚁集团   /   杭州
399  399    卢竑岩   103.4        吉比特  43   厦门
```

(xincaifu_rank)=
## 新财富富豪榜

接口：xincaifu_rank

目标地址：http://www.xcf.cn/zhuanti/ztzz/hdzt1/500frb/index.html

描述：新财富 500 富豪榜，从 2003 年至今

限量：单次返回指定年份的富豪榜数据

输入参数

| 名称   | 类型  | 描述                      |
|------|-----|-------------------------|
| year | str | year="2020"；从 2003 年至今 |

输出参数

| 名称   | 类型      | 描述       |
|------|---------|----------|
| 排名   | int64   | -        |
| 财富   | float64 | 注意单位：亿元 |
| 姓名   | str     | -        |
| 主要公司 | str     | -        |
| 相关行业 | str     | -        |
| 公司总部 | str     | -        |
| 性别   | str     | -        |
| 年龄   | str     | -        |
| 年份   | int64   | -        |

接口示例

```python
import akshare as ak

xincaifu_rank_df = ak.xincaifu_rank(year="2022")
print(xincaifu_rank_df)
```

数据示例

```
      排名      财富       姓名       主要公司        相关行业     公司总部   性别     年龄    年份
0      1  4983.5      钟睒睒  农夫山泉/万泰生物  矿泉水饮料、医药生物  浙江杭州/北京    男     68  2022
1      2  3348.2      曾毓群       宁德时代        动力电池     福建宁德    男     54  2022
2      3  3010.8      马化腾       腾讯控股     互联网综合服务     广东深圳    男     51  2022
3      4  2916.0      张一鸣       今日头条  推荐引擎产品、短视频       北京    男     39  2022
4      5  1972.0       黄峥        拼多多          电商       上海    男     42  2022
..   ...     ...      ...        ...         ...      ...  ...    ...   ...
495  496    94.7      崔志祥     方圆有色金属     铜、金、银生产     山东东营    男     59  2022
496  497    94.6    胡成中家族        德力西  低压电器、仪器仪表等     浙江温州    男     61  2022
497  498    94.2  张宏亮/张秀根       曙光股份        汽车整车     辽宁丹东  男/男  38,61  2022
498  499    94.0       金磊       长春高新        生长激素     吉林长春    男     57  2022
499  500    93.7    赵轶/徐昕       长川科技    集成电路测试装备     浙江杭州  男/女  56,56  2022
```

(hurun_rank)=
## 胡润排行榜

接口：hurun_rank

目标地址：https://www.hurun.net/zh-CN/Rank/HsRankDetails?num=QWDD234E

描述：胡润百富榜单；富豪榜系列，创业系列，500强系列，特色系列

限量：单次返回指定 indicator 和 year 的榜单数据

输入参数

| 名称        | 类型  | 描述                                                                                                                                                                                                          |
|-----------|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| indicator | str | indicator="胡润百富榜"; choice of {"胡润百富榜", "胡润全球富豪榜", "胡润印度榜", "胡润全球独角兽榜", "全球瞪羚企业榜", "胡润Under30s创业领袖榜", "胡润世界500强", "胡润艺术榜"}                                                                                   |
| year      | str | year="2020"; choice of {"胡润百富榜": "2014-至今", "胡润全球富豪榜": "2019-至今", "胡润印度榜": "2018-至今", "胡润全球独角兽榜": "2019-至今", "全球瞪羚企业榜": "2021-至今", "胡润Under30s创业领袖榜": "2019-至今", "胡润世界500强": "2020-至今", "胡润艺术榜": "2019-至今"} |

输出参数-胡润百富榜

| 名称  | 类型      | 描述       |
|-----|---------|----------|
| 排名  | int64   | -        |
| 财富  | float64 | 注意单位：亿元 |
| 姓名  | str     | -        |
| 企业  | str     | -        |
| 行业  | str     | -        |

接口示例-胡润百富榜

```python
import akshare as ak

hurun_rank_df = ak.hurun_rank(indicator="胡润百富榜", year="2023")
print(hurun_rank_df)
```

数据示例-胡润百富榜

```
        排名      财富       姓名    企业       行业
0        1  4500.0      钟睒睒   养生堂  饮料、医疗保健
1        2  2800.0      马化腾    腾讯    互联网服务
2        3  2700.0       黄峥   拼多多     购物网站
3        4  2500.0      曾毓群  宁德时代      锂电池
4        5  2450.0      张一鸣  字节跳动     社交媒体
    ...     ...      ...   ...      ...
1236  1179    50.0  周富裕、唐建芳   周黑鸭       食品
1237  1179    50.0  周华松、吴文利  松霖科技     淋浴设备
1238  1179    50.0      周明华  华海药业       医药
1239  1179    50.0      周文起    华北   铜业、房地产
1240  1179    50.0      庄辰超  斑马投资       投资
[1241 rows x 5 columns]
```

输出参数-胡润全球富豪榜

| 名称  | 类型      | 描述        |
|-----|---------|-----------|
| 排名  | int64   | -         |
| 财富  | float64 | 注意单位：亿美元 |
| 姓名  | str     | -         |
| 企业  | str     | -         |
| 行业  | str     | -         |

接口示例-胡润全球富豪榜

```python
import akshare as ak

hurun_rank_df = ak.hurun_rank(indicator="胡润全球富豪榜", year="2023")
print(hurun_rank_df)
```

数据示例-胡润全球富豪榜

```
        排名       财富       姓名            企业       行业
0        1  13500.0  伯纳德·阿诺特  酩悦·轩尼诗-路易·威登      奢侈品
1        2  10500.0   埃隆·马斯克           特斯拉    新能源汽车
2        3   9000.0  贝特朗·皮埃奇           爱马仕      奢侈品
3        4   7900.0   杰夫·贝佐斯           亚马逊     电子商务
4        5   7800.0   沃伦·巴菲特      伯克希尔·哈撒韦       投资
    ...      ...      ...           ...      ...
3107  2923     67.0      钟宝申            隆基     绿色能源
3108  2923     67.0      钟培峰          晶晨股份      半导体
3109  2923     67.0       周剑           优必选      机器人
3110  2923     67.0      周明华          华海药业       医药
3111  2923     67.0   邹伟民、陈敏          传艺科技  消费电子零部件
[3112 rows x 5 columns]
```

输出参数-胡润全球独角兽榜

| 名称  | 类型      | 描述       |
|-----|---------|----------|
| 排名  | int64   | -        |
| 财富  | float64 | 注意单位：亿元 |
| 姓名  | str     | -        |
| 企业  | str     | -        |
| 行业  | str     | -        |

接口示例-胡润全球独角兽榜

```python
import akshare as ak

hurun_rank_df = ak.hurun_rank(indicator="胡润全球独角兽榜", year="2023")
print(hurun_rank_df)
```

数据示例-胡润全球独角兽榜

```
        排名       财富  ...      企业    行业
0        1  13800.0  ...    字节跳动  社交媒体
1        2   9450.0  ...  SpaceX    航天
2        3   8300.0  ...    蚂蚁集团  金融科技
3        4   4500.0  ...   Shein  电子商务
4        5   3800.0  ...  Stripe  金融科技
    ...      ...  ...     ...   ...
1355  1039     69.0  ...     云学堂  企业服务
1356  1039     69.0  ...   Zebec  金融科技
1357  1039     69.0  ...    Zeta  金融科技
1358  1039     69.0  ...    Zopa  金融科技
1359  1039     69.0  ...   Zwift  健康科技
[1360 rows x 5 columns]
```

输出参数-胡润世界500强

| 名称   | 类型      | 描述       |
|------|---------|----------|
| 排名   | int64   | -        |
| 排名变化 | int64   | -        |
| 企业估值 | float64 | 注意单位：亿元 |
| 企业信息 | str     | -        |
| CEO  | str     | -        |
| 行业   | str     | -        |

接口示例-胡润世界500强

```python
import akshare as ak

hurun_rank_df = ak.hurun_rank(indicator="胡润世界500强", year="2022")
print(hurun_rank_df)
```

数据示例-胡润世界500强

```
      排名  排名变化      企业估值      企业信息                   CEO        行业
0      1     0  171540.0        苹果                 蒂姆·库克       消费品
1      2     0  130860.0        微软               萨提亚·纳德拉     软件与服务
2      3     1   95770.0  Alphabet               桑达尔·皮查伊     传媒和娱乐
3      4    -1   88090.0       亚马逊                 安迪·贾西        零售
4      5     3   48720.0       特斯拉                埃隆·马斯克  汽车及汽车零部件
..   ...   ...       ...       ...                   ...       ...
495  495  -258    2100.0   Coupang           Bom Suk Kim        零售
496  495  -166    2100.0      东方财富                    其实      金融服务
497  495  -190    2100.0       爱德士  Jonathan J. Mazelsky      医疗健康
498  495  -176    2100.0      联发科技                   陈冠州       半导体
499  500  -247    2030.0        百度                   李彦宏     传媒和娱乐
[500 rows x 6 columns]
```

输出参数-胡润艺术榜

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 排名   | int64   | -       |
| 排名   | int64   | -       |
| 成交额  | float64 | 注意单位：万 |
| 姓名   | str     | -       |
| 年龄   | str     | -       |
| 艺术类别 | str     | -       |

接口示例-胡润艺术榜

```python
import akshare as ak

hurun_rank_df = ak.hurun_rank(indicator="胡润艺术榜", year="2023")
print(hurun_rank_df)
```

数据示例-胡润艺术榜

```
     排名 排名变化      成交额   姓名  年龄     艺术类别
0     1    1  14371.0  曾梵志  59       油画
1     2   -1  11106.0  崔如琢  79     中国书画
2     3    4  10148.0  黄建南  71  油画/中国书画
3     4    6   9405.0   范曾  85     中国书画
4     5    4   9058.0  黄宇兴  48       油画
..  ...  ...      ...  ...  ..      ...
95   96  New    388.0   邵帆  59     中国书画
96   97  -36    385.0   喻红  57       油画
97   98  -24    369.0   薛松  58     中国书画
98   99  New    362.0  陈文骥  69       油画
99  100  -27    358.0   林墉  82     中国书画
[100 rows x 6 columns]
```

(fortune_rank)=
## 财富世界 500 强

接口：fortune_rank

目标地址：https://www.fortunechina.com/fortune500/index.htm

描述：财富中文网-历年《财富》世界 500 强榜单，从 1996 年至今；各年份网页公布的字段不同，返回结果统一为固定的 9 列，当年未公布的字段为空值

限量：单次返回指定年份的 500 家公司

输入参数

| 名称   | 类型  | 描述                       |
|------|-----|--------------------------|
| year | str | year="2025"；从 1996 年至今 |

输出参数

| 名称   | 类型      | 描述                          |
|------|---------|-----------------------------|
| 排名   | Int64   | -                           |
| 上年排名 | Int64   | 2006 年、2008～2019 年公布       |
| 公司名称 | str     | -                           |
| 国家   | str     | 2010 年未公布                  |
| 营业收入 | float64 | 注意单位：百万美元                 |
| 利润   | float64 | 注意单位：百万美元                 |
| 资产   | float64 | 注意单位：百万美元；2008 年及以前公布，2007 年除外 |
| 股东权益 | float64 | 注意单位：百万美元；1997、1998、2000～2005、2008 年公布 |
| 雇员人数 | float64 | 2008 年及以前公布                |

接口示例

```python
import akshare as ak

fortune_rank_df = ak.fortune_rank(year="2025")
print(fortune_rank_df)
```

数据示例

```
      排名  上年排名  ...  股东权益  雇员人数
0      1  <NA>  ...   NaN   NaN
1      2  <NA>  ...   NaN   NaN
2      3  <NA>  ...   NaN   NaN
3      4  <NA>  ...   NaN   NaN
4      5  <NA>  ...   NaN   NaN
..   ...   ...  ...   ...   ...
495  496  <NA>  ...   NaN   NaN
496  497  <NA>  ...   NaN   NaN
497  498  <NA>  ...   NaN   NaN
498  499  <NA>  ...   NaN   NaN
499  500  <NA>  ...   NaN   NaN

[500 rows x 9 columns]
```

## 电影票房

(movie_boxoffice_realtime)=
### 实时票房

接口：movie_boxoffice_realtime

目标地址：https://ys.endata.cn/BoxOffice/Movie

描述：当前时刻的实时电影票房数据，每 5 分钟更新一次数据，实时票房包含今天未开映场次已售出的票房

限量：当前时刻的实时票房数据

说明：接口已切换至艺恩当前 `ys.endata.cn/enlib-api` 影片榜单接口，输出金额统一按 `万` 进行换算

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 排序   | int64   | 票房排名    |
| 影片名称 | str     | -       |
| 实时票房 | float64 | 注意单位：万 |
| 票房占比 | float64 | 注意单位：% |
| 上映天数 | int64   | -       |
| 累计票房 | float64 | 注意单位：万 |

接口示例

```python
import akshare as ak

movie_boxoffice_realtime_df = ak.movie_boxoffice_realtime()
print(movie_boxoffice_realtime_df)
```

数据示例

```
    排序            影片名称 实时票房   票房占比  上映天数  累计票房
0    1             第二十条  2773.21  27.29    11  160845.76
1    2            飞驰人生2  2499.77  24.60    11  267199.76
2    3         熊出没·逆转时空  2429.72  23.91    11  159079.03
3    4             热辣滚烫  2413.96  23.76    11  300038.28
4    5               孤军    11.60   0.11    55    2528.30
5    6           年会不能停！     7.36   0.07    54  128760.85
6    7  泰勒·斯威夫特：时代巡回演唱会     4.73   0.05    52    9594.50
7    8         还是觉得你最好2     4.45   0.04    -3      82.60
8    9          八戒之天蓬下界     2.98   0.03    11     345.28
9   10        舒克贝塔·五角飞碟     2.87   0.03    53    6548.90
10  11               其它    10.25   1.00     0       0.00
```

(movie_boxoffice_daily)=
### 单日票房

接口：movie_boxoffice_daily

目标地址：https://www.endata.com.cn/BoxOffice/BO/Day/index.html

描述：指定日期的电影票房数据，每日 10:30, 12:30更新日票房，16:30 同时补充前 7 日票房

限量：只能指定最近的日期

说明：接口已迁移至艺恩当前 `ys.endata.cn/enlib-api` 数据源；由于新站公开列表未返回口碑字段，`口碑指数` 当前统一返回空值

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20240219"；只能选择最近的日期 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 排序   | int64   | 票房排名    |
| 影片名称 | str     | -       |
| 单日票房 | int64   | 注意单位：万 |
| 环比变化 | float64 | 注意单位：% |
| 累计票房 | int64   | 注意单位：万 |
| 平均票价 | int64   | 注意单位：元 |
| 场均人次 | int64   | -       |
| 口碑指数 | float64 | -       |
| 上映天数 | int64   | -       |

接口示例

```python
import akshare as ak

movie_boxoffice_daily_df = ak.movie_boxoffice_daily(date="20240219")
print(movie_boxoffice_daily_df)
```

数据示例

```
   排序             影片名称   单日票房  环比变化    累计票房  平均票价  场均人次  口碑指数  上映天数
0   1             第二十条  12808 -23.0  158075    45    10  8.99    21
1   2            飞驰人生2  12693 -26.0  264702    46    10  9.04    17
2   3             热辣滚烫  13094 -29.0  297624    45    10  8.98    17
3   4         熊出没·逆转时空   9263 -27.0  156650    44    10  8.78    22
4   5               秋田     15  47.0      68    42    26  0.00    27
5   6           年会不能停！     17  18.0  128754    41    53  9.05     3
6   7        海王2：失落的王国     10  10.0   46449    39    62   NaN     6
7   8               孤军      7  14.0    2516    41    54  0.00   102
8   9  泰勒·斯威夫特：时代巡回演唱会      6   0.0    9590    48    51  0.00    11
9  10          八戒之天蓬下界     14 -64.0     342    42    10  0.00     2
```

(movie_boxoffice_weekly)=
### 单周票房

接口：movie_boxoffice_weekly

目标地址：https://www.endata.com.cn/BoxOffice/BO/Week/oneWeek.html

描述：指定日期所在完整周的票房数据，影片周票房数据初始更新周期为每周二，下周二补充数据

限量：指定日期所在完整周的票房数据

说明：艺恩新站公开周榜接口当前返回权限限制，调用时会抛出明确的上游权限异常，不再返回旧版 `JSONDecodeError`

输入参数

| 名称   | 类型  | 描述                             |
|------|-----|--------------------------------|
| date | str | date="20240218"；指定日期所在周必须已经完整 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 排序   | int64   | 票房排名    |
| 影片名称 | str     | -       |
| 排名变化 | int64   | -       |
| 单周票房 | int64   | 注意单位：万 |
| 环比变化 | int64   | 注意单位：% |
| 累计票房 | int64   | 注意单位：万 |
| 平均票价 | int64   | -       |
| 场均人次 | int64   | -       |
| 口碑指数 | float64 | -       |
| 上映天数 | int64   | -       |

接口示例

```python
import akshare as ak

movie_boxoffice_weekly_df = ak.movie_boxoffice_weekly(date="20240218")
print(movie_boxoffice_weekly_df)
```

数据示例

```
   排序     影片名称  排名变化  单周票房 环比变化 累计票房  平均票价 场均人次 口碑指数 上映天数
0   1       热辣滚烫  9999  208829  163  288355    49    40  9.02     9
1   2      飞驰人生2  9999  180105  139  255362    49    39  9.08     9
2   3       第二十条     1  114864  244  148245    48    39  9.03     9
3   4   熊出没·逆转时空    -1  106105  142  149889    47    41  8.98     9
4   5    我们一起摇太阳     2    4926    7    9512    49    16  9.20     9
5   6       红毯先生  9999    2977  -46    8488    54     8  8.52     9
6   7     年会不能停！    -2     264  -96  128733    45     9  9.06    52
7   8    八戒之天蓬下界    15     225  102     337    43     3   NaN     9
8   9  海王2：失落的王国     1     119  -88   46438    41    12  8.10    61
9  10   还是觉得你最好2     0      75    0      75    61    95   NaN    -5
```

(movie_boxoffice_monthly)=
### 单月票房

接口：movie_boxoffice_monthly

目标地址：https://www.endata.com.cn/BoxOffice/BO/Month/oneMonth.html

描述：获取指定日期所在月份的票房数据，每月5号更新上月票房，并补充之前两个月票房

限量：指定日期所在月份的票房数据，只能获取最近月份的数据

说明：接口已迁移至艺恩当前 `ys.endata.cn/enlib-api` 数据源；由于新站公开列表未返回口碑字段，`口碑指数` 当前统一返回空值

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20201019"；输入具体的日期即可 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 排序   | int64   | 票房排名    |
| 影片名称 | str     | -       |
| 单月票房 | int64   | 注意单位：万 |
| 月度占比 | float64 | 注意单位：% |
| 平均票价 | int64   | -       |
| 场均人次 | int64   | -       |
| 上映日期 | object  | -       |
| 口碑指数 | float64 | -       |
| 月内天数 | float64 | -       |

接口示例

```python
import akshare as ak

movie_boxoffice_monthly_df = ak.movie_boxoffice_monthly(date="20240218")
print(movie_boxoffice_monthly_df)
```

数据示例

```
     排序      影片名称 单月票房  月度占比 平均票价  场均人次  上映日期  口碑指数  月内天数
0     1       热辣滚烫  297624  31.8    49    42  2024-02-10  9.05  20.0
1     2      飞驰人生2  264702  28.3    49    40  2024-02-10  9.12  20.0
2     3       第二十条  158075  16.9    48    36  2024-02-10  9.06  20.0
3     4   熊出没·逆转时空  156645  16.8    47    43  2024-02-10  9.03  20.0
4     5     年会不能停！   14940   1.6    38     5  2023-12-29  9.07  29.0
5     6    我们一起摇太阳    9513   1.0    50    14  2024-02-10  9.24  20.0
6     7       红毯先生    8492   0.9    52    11  2024-02-10  8.54  20.0
7     8        金手指    5326   0.6    39     4  2023-12-30  8.10  29.0
8     9       临时劫案    5295   0.6    38     2  2024-01-19  7.95  29.0
9    10  海王2：失落的王国    2021   0.2    38     4  2023-12-20  8.12  29.0
10  999         其他   12222   1.3    38     2        None   NaN   NaN
```

(movie_boxoffice_yearly)=
### 年度票房

接口：movie_boxoffice_yearly

目标地址：https://www.endata.com.cn/BoxOffice/BO/Year/index.html

描述：指定日期所在年度的票房数据

限量：指定日期所在年度的票房数据，只能获取最近年度的数据

说明：接口已迁移至艺恩当前 `ys.endata.cn/enlib-api` 数据源

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20240218"；输入具体的日期即可 |

输出参数

| 名称    | 类型      | 描述      |
|-------|---------|---------|
| 排序    | int64   | 票房排名    |
| 影片名称  | str     | -       |
| 类型    | str     | -       |
| 总票房   | int64   | 注意单位：万 |
| 平均票价  | int64   | -       |
| 场均人次  | float64 | -       |
| 国家及地区 | string  | -       |
| 上映日期  | object  | -       |

接口示例

```python
import akshare as ak

movie_boxoffice_yearly_df = ak.movie_boxoffice_yearly(date="20240218")
print(movie_boxoffice_yearly_df)
```

数据示例

```
    排序           影片名称   类型  总票房  平均票价  场均人次  国家及地区   上映日期
0    1             热辣滚烫   剧情  299473    49  39.0       中国  2024-02-10
1    2            飞驰人生2   剧情  266592    49  37.0       中国  2024-02-10
2    3             第二十条   剧情  160201    48  33.0       中国  2024-02-10
3    4         熊出没·逆转时空   动画  158538    47  40.0       中国  2024-02-10
4    5           年会不能停！   剧情  105635    39   7.0       中国  2023-12-29
5    6              金手指   剧情   41595    40   6.0  中国/中国香港  2023-12-30
6    7             临时劫案   剧情   23658    38   4.0       中国  2024-01-19
7    8               潜行   剧情   20261    39   5.0       中国  2023-12-29
8    9          一闪一闪亮星星   爱情   14900    39   4.0       中国  2023-12-30
9   10              三大队   剧情   14518    42   5.0       中国  2023-12-15
10  11        海王2：失落的王国   动作   12891    39   6.0       美国  2023-12-20
11  12              养蜂人   动作   11342    41   4.0    美国/英国  2024-01-12
12  13         动物园里有什么？   喜剧   10802    37   3.0       中国  2024-01-12
13  14          我们一起摇太阳   剧情    9513    50  14.0       中国  2024-02-10
14  15             红毯先生   剧情    8492    52  11.0       中国  2024-02-10
15  16            非诚勿扰3   喜剧    5877    41   4.0       中国  2023-12-30
16  17  泰勒·斯威夫特：时代巡回演唱会  纪录片    5582    48   8.0       美国  2023-12-31
17  18        舒克贝塔·五角飞碟   动画    4270    37   4.0       中国  2023-12-30
18  19             天降大任   动画    3181    43   4.0       中国  2024-01-06
19  20      名侦探柯南：黑铁的鱼影   动画    3063    33   5.0       日本  2023-12-16
20  21        开心超人之时空营救   动画    2576    33   2.0       中国  2024-01-20
21  22               孤军   剧情    2334    46  65.0       中国  2023-12-28
22  23             照明商店   剧情    1809    40   3.0       中国  2023-12-08
23  24               大雨   动画    1718    41   2.0       中国  2024-01-12
24  25         志愿军：雄兵出击   战争    1047    96  55.0       中国  2023-09-28
```

(movie_boxoffice_yearly_first_week)=
### 年度首周票房

接口：movie_boxoffice_yearly_first_week

目标地址：https://www.endata.com.cn/BoxOffice/BO/Year/firstWeek.html

描述：指定日期所在年度的年度首周票房数据

限量：指定日期所在年度的年度首周票房数据，只能获取最近年度的数据

说明：接口已迁移至艺恩当前 `ys.endata.cn/enlib-api` 年榜数据源，其中 `首周天数` 依据上映日期按首周自然周区间估算

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20201018"；输入具体的日期即可 |

输出参数

| 名称     | 类型     | 描述      |
|--------|--------|---------|
| 排序     | int64  | 票房排名    |
| 影片名称   | str    | -       |
| 类型     | str    | -       |
| 首周票房   | int64  | 注意单位：万 |
| 占总票房比重 | int64  | 注意单位：% |
| 场均人次   | int64  | -       |
| 国家及地区  | string | -       |
| 上映日期   | object | -       |
| 首周天数   | int64  | -       |

接口示例

```python
import akshare as ak

movie_boxoffice_yearly_first_week_df = ak.movie_boxoffice_yearly_first_week(date="20201018")
print(movie_boxoffice_yearly_first_week_df)
```

数据示例

```
   排序                 影片名称  类型  首周票房  占总票房比重  场均人次  国家及地区        上映日期  首周天数
0   1                 鲨海逃生  灾难  2473      52     5  美国/英国  2020-01-10     3
1   2  紫罗兰永恒花园外传：永远与自动手记人偶  剧情  2342      48     6     日本  2020-01-10     3
2   3                动物特工局  动画  1489      33     6  中国/法国  2020-01-11     2
3   4                 为家而战  动作  1364      79     3  美国/英国  2020-01-10     3
4   5                   灭绝  科幻   997      62    10     美国  2020-01-18     2
5   6                 别告诉她  剧情   205      50     5  美国/中国  2020-01-10     3
6   7                 致敬英雄  剧情   199      54     6     中国  2020-01-10     3
7   8                格萨尔藏戏  剧情     0       0     1     中国  2020-08-21  -186
```

(movie_boxoffice_cinema_daily)=
### 影院票房-日票房排行

接口：movie_boxoffice_cinema_daily

目标地址：https://www.endata.com.cn/BoxOffice/BO/Cinema/day.html

描述：指定日期的每日各影院的票房数据

限量：指定日期各影院的票房数据，注意当前日期的数据需要第二日才可以获取

说明：接口已迁移至艺恩当前 `ys.endata.cn/enlib-api` 数据源

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20240219"；输入具体的日期即可 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 排序   | int64   | 票房排名    |
| 影院名称 | str     | -       |
| 单日票房 | float64 | 注意单位：元 |
| 单日场次 | int64   | -       |
| 场均人次 | float64 | -       |
| 场均票价 | float64 | -       |
| 上座率  | float64 | 注意单位：% |

接口示例

```python
import akshare as ak

movie_boxoffice_cinema_daily_df = ak.movie_boxoffice_cinema_daily(date="20240219")
print(movie_boxoffice_cinema_daily_df)
```

数据示例

```
     排序            影院名称       单日票房  单日场次   场均人次    场均票价    上座率
0     1       廊坊市橙天国际影城  381255.31    46  56.61  146.41  42.69
1     2       阜阳颍州万达广场店  254175.95    72  68.56   51.49  34.26
2     3       庆阳市M3电影城堡  234791.42    49  85.02   56.36  61.32
3     4  北京耀莱成龙影城（五棵松店）  231814.17   107  41.48   52.23  22.59
4     5     厦门万达影城SM广场店  218179.01    84  51.15   50.77  28.54
..  ...             ...        ...   ...    ...     ...    ...
95   96      长垣县艾影汇国际影城  127034.18    54  43.65   53.90  34.51
96   97       呼和浩特万达广场店  126514.62    58  41.71   52.30  24.82
97   98       西安高新万达广场店  126260.37   109  21.03   55.09  17.56
98   99  阜阳市星轶影城（吾悦广场店）  126209.61    34  61.76   60.10  38.07
99  100     中影国际影城燕郊永旺店  126176.63    52  46.17   52.55  23.97
[100 rows x 7 columns]
```

(movie_boxoffice_cinema_weekly)=
### 影院票房-周票房排行

接口：movie_boxoffice_cinema_weekly

目标地址：https://www.endata.com.cn/BoxOffice/BO/Cinema/week.html

描述：指定日期的完整周各影院的票房数据

限量：指定日期的完整周各影院的票房数据，注意当前日期的数据只能返回上周的数据

说明：艺恩新站公开影院周榜接口当前返回系统错误，调用时会抛出明确的上游权限异常，不再返回旧版 `JSONDecodeError`

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20240219"；输入具体的日期即可 |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 排序     | int64   | 票房排名    |
| 影院名称   | str     | -       |
| 当周票房   | float64 | 注意单位：万 |
| 单银幕票房  | float64 | 注意单位：元 |
| 场均人次   | float64 | -       |
| 单日单厅票房 | float64 | -       |
| 单日单厅场次 | float64 | -       |

接口示例

```python
import akshare as ak

movie_boxoffice_cinema_weekly_df = ak.movie_boxoffice_cinema_weekly(date="20240219")
print(movie_boxoffice_cinema_weekly_df)
```

数据示例

```
     排序     影院名称   当周票房   单银幕票房   场均人次  单日单厅票房  单日单厅场次
0     1      鄢陵奥斯卡国际影城  672.0  112.00   4.00   22.40    0.20
1     2      睢县奥斯卡天空影城  528.0  528.00  22.00   88.00    0.17
2     3         台山天悦影城  489.3   69.90   1.00   13.98    0.20
3     4  东莞中影南方国际影城地王店  462.0   33.00   1.00    9.43    0.29
4     5      三明永安华夏大剧院  454.0   75.67   1.67   15.13    0.20
..  ...            ...    ...     ...    ...     ...     ...
95   96  乳源瑶族自治县华景汇聚影城    0.0    0.00   0.00    0.00    0.20
96   97      来宾金秀县秀河影院    0.0    0.00   0.00    0.00    1.00
97   98        灵川县大唐影院    0.0    0.00   0.00    0.00    0.33
98   99      闽清县六都国际影城    0.0    0.00   0.00    0.00    0.33
99  100         建瓯市电影院    0.0    0.00   0.00    0.00    0.25
[100 rows x 7 columns]
```

## 视频播映

(video_tv)=
### 电视剧集

接口：video_tv

目标地址：https://www.endata.com.cn/Video/index.html

描述：艺恩-视频放映-电视剧集

限量：返回前一日的电视剧播映数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 排序   | int64   | -   |
| 名称   | object  | -   |
| 类型   | str     | -   |
| 播映指数 | float64 | -   |
| 媒体热度 | float64 | -   |
| 用户热度 | float64 | -   |
| 好评度  | float64 | -   |
| 观看度  | float64 | -   |
| 统计日期 | float64 | -   |

接口示例

```python
import akshare as ak

video_tv_df = ak.video_tv()
print(video_tv_df)
```

数据示例

```
   排序    名称     类型   播映指数   媒体热度  用户热度 好评度  观看度     统计日期
0   1    在暴雪时分  爱情/都市  79.44  74.46  75.72  68.00  80.43  2024-02-18
1   2     南来北往     爱情  78.67  76.24  75.63  53.39  83.90  2024-02-18
2   3     烟火人家  剧情/爱情  72.98  72.04  71.43  52.47  74.73  2024-02-18
3   4      莲花楼     古装  72.84  68.92  76.22  85.00  56.97  2024-02-18
4   5       繁花  剧情/爱情  72.40  75.92  65.39  86.00  63.16  2024-02-18
5   6     一念关山     古装  69.52  60.02  79.51  64.00  57.42  2024-02-18
6   7     要久久爱     剧情  69.45  63.88  71.14  72.00  60.50  2024-02-18
7   8   长相思第一季  爱情/奇幻  68.41  62.20  67.88  78.00  59.09  2024-02-18
8   9   乡村爱情16  喜剧/乡村  67.16  65.22  62.70  52.07  70.66  2024-02-18
9  10  繁花[沪语版]     剧情  66.96  75.93  65.39  51.32  63.16  2024-02-18
```

(video_variety_show)=
### 综艺节目

接口：video_variety_show

目标地址：https://www.endata.com.cn/Video/index.html

描述：艺恩-视频放映-综艺节目

限量：返回前一日的综艺播映数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 排序   | int64   | -   |
| 名称   | object  | -   |
| 类型   | str     | -   |
| 播映指数 | float64 | -   |
| 媒体热度 | float64 | -   |
| 用户热度 | float64 | -   |
| 好评度  | float64 | -   |
| 观看度  | float64 | -   |
| 统计日期 | float64 | -   |

接口示例

```python
import akshare as ak

video_variety_show_df = ak.video_variety_show()
print(video_variety_show_df)
```

数据示例

```
   排序         名称      类型   播映指数   媒体热度   用户热度    好评度  观看度    统计日期
0   1         声生不息家年华     真人秀  81.62  73.82  94.64  68.00  67.75  2024-02-18
1   2       你好星期六2024     真人秀  71.46  66.35  78.16  51.66  66.63  2024-02-18
2   3  声生不息·家年华 舞台纯享版  真人秀/衍生  71.35  73.82  94.64  49.75  47.48  2024-02-18
3   4          奔跑吧第七季     真人秀  70.35  73.40  73.98  72.00  56.05  2024-02-18
4   5        名侦探学院第七季     真人秀  64.80  73.86  68.72  50.51  55.14  2024-02-18
5   6     花儿与少年丝路季第五季     真人秀  63.89  64.07  65.74  91.00  42.49  2024-02-18
6   7         极限挑战第九季     真人秀  63.42  70.93  71.96  54.00  47.89  2024-02-18
7   8             毛雪汪     真人秀  62.93  41.64  65.67  74.00  56.81  2024-02-18
8   9        王牌对王牌第八季     真人秀  62.48  63.42  64.12  53.00  56.81  2024-02-18
9  10      极限挑战宝藏行第四季     真人秀  62.34  56.96  67.96  50.64  56.37  2024-02-18
```

## 艺人

(business_value_artist)=
### 艺人商业价值

接口：business_value_artist

目标地址：https://www.endata.com.cn/Marketing/Artist/business.html

描述：艺恩-艺人-艺人商业价值

限量：返回当前的艺人商业价值数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述                                                                                                         |
|------|---------|------------------------------------------------------------------------------------------------------------|
| 排名   | int64   | -                                                                                                          |
| 艺人   | str     | -                                                                                                          |
| 商业价值 | float64 | 商业价值由专业度，关注度，预测热度加权汇总计算后得出，分值范围0~100，综合反映明星作品、代言表现、近期热度及舆情口碑。                                              |
| 专业热度 | float64 | 艺人专业热度主要表现艺人历史作品及品牌代言的效果情况，参与计算的指标维度包括历史主演电影票房表现，历史主演视频节目播映热度，电影作品豆瓣评分，作品相关微博内容评论正负向，历史代言品牌数量，品牌热度，艺人获奖数量。 |
| 关注热度 | float64 | 艺人关注热度主要表现艺人网络中的舆情声量，参与计算的指标维度包括百度搜索指数，百度新闻数量，今日头条新闻数，微博转发量，微博评论量，微博点赞量，微博粉丝数量，贴吧关注数量，微博话题数量。              |
| 预测热度 | float64 | 预测热度的数值反映明星的未来发展潜力，包括粉丝增长规模，作品口碑以及未来作品预测。                                                                  |
| 美誉度  | float64 | 根据艺人近三年参演电影、视频作品在豆瓣等平台的评分、微博正向评价，以及微博好评率等指标综合加权得出。                                                         |
| 统计日期 | object  | -                                                                                                          |

接口示例

```python
import akshare as ak

business_value_artist_df = ak.business_value_artist()
print(business_value_artist_df)
```

数据示例

```
     排名  艺人 商业价值 专业热度 关注热 预测热度  美誉度     统计日期
0     1    杨幂  88.90  88.80  78.47  78.36  63.00  2021-11-16
1     2   朱一龙  85.09  92.40  71.17  13.76  72.00  2021-11-16
2     3  易烊千玺  84.65  85.73  75.19  57.26  65.67  2021-11-16
3     4   黄晓明  82.81  88.81  66.14  48.59  59.00  2021-11-16
4     5    刘涛  82.62  83.44  71.61  71.27  49.33  2021-11-16
..  ...   ...    ...    ...    ...    ...    ...         ...
95   96   张涵予  72.06  74.19  63.89  34.97  58.67  2021-11-16
96   97   胡一天  72.02  73.85  59.71  67.64  53.33  2021-11-16
97   98    徐峥  71.95  72.16  61.45  74.32  79.67  2021-11-16
98   99    魏晨  71.91  75.15  63.19  25.54  73.00  2021-11-16
99  100   钟楚曦  71.87  72.61  63.14  55.64  44.00  2021-11-16
```

(online_value_artist)=
### 艺人流量价值

接口：online_value_artist

目标地址：https://www.endata.com.cn/Marketing/Artist/business.html

描述：艺恩-艺人-艺人流量价值

限量：返回当前的艺人流量价值数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述                                                                                                         |
|------|---------|------------------------------------------------------------------------------------------------------------|
| 排名   | int64   | -                                                                                                          |
| 艺人   | str     | -                                                                                                          |
| 流量价值 | float64 | 流量价值由专业度，关注度，预测热度，带货力加权汇总计算后得出，分值范围0~100，在商业价值的基础上增加了明星近期热度及带货力的权重。                                        |
| 专业热度 | float64 | 艺人专业热度主要表现艺人历史作品及品牌代言的效果情况，参与计算的指标维度包括历史主演电影票房表现，历史主演视频节目播映热度，电影作品豆瓣评分，作品相关微博内容评论正负向，历史代言品牌数量，品牌热度，艺人获奖数量。 |
| 关注热度 | float64 | 艺人关注热度主要表现艺人网络中的舆情声量，参与计算的指标维度包括百度搜索指数，百度新闻数量，今日头条新闻数，微博转发量，微博评论量，微博点赞量，微博粉丝数量，贴吧关注数量，微博话题数量。              |
| 预测热度 | float64 | 预测热度的数值反映明星的未来发展潜力，包括粉丝增长规模，作品口碑以及未来作品预测。                                                                  |
| 带货力  | float64 | 带货力的数值代表艺人的带货号召力，包括艺人的铁杆粉丝规模，超话粉丝规模。                                                                       |
| 统计日期 | object  | -                                                                                                          |

接口示例

```python
import akshare as ak

online_value_artist_df = ak.online_value_artist()
print(online_value_artist_df)
```

数据示例

```
     排名  艺人 流量价值 专业热度 关注热度 预测热度 带货力    统计日期
0     1   杨紫  85.47  74.30  76.06  97.80  83.95  2021-11-16
1     2   杨幂  85.15  88.80  78.47  78.36  89.24  2021-11-16
2     3  王一博  82.18  81.34  71.35  87.57  94.60  2021-11-16
3     4   龚俊  80.94  70.46  72.67  87.62  88.60  2021-11-16
4     5  陈伟霆  79.42  80.35  74.84  73.49  77.83  2021-11-16
..  ...  ...    ...    ...    ...    ...    ...         ...
95   96  佟丽娅  67.11  81.30  60.15  57.87  73.44  2021-11-16
96   97  郭麒麟  67.09  81.95  62.45  44.96  76.56  2021-11-16
97   98   杨迪  67.06  65.26  63.42  55.52  73.07  2021-11-16
98   99  钟楚曦  67.03  72.61  63.14  55.64  68.99  2021-11-16
99  100  张子枫  67.02  74.36  65.76  41.24  71.71  2021-11-16
```

(stock_js_weibo_report)=
## 微博舆情报告

接口：stock_js_weibo_report

目标地址：https://datacenter.jin10.com/market

描述：微博舆情报告中近期受关注的股票

限量：单次返回指定时间内微博舆情报告中近期受关注的股票

输入参数

| 名称          | 类型  | 描述                                                                                     |
|-------------|-----|----------------------------------------------------------------------------------------|
| time_period | str | time_period="CNHOUR12"；详见下表**time_period参数一览表**，可通过调用 **stock_js_weibo_nlp_time** 获取 |

time_period 参数一览表

| 参数       | 说明   |
|----------|------|
| CNHOUR2  | 2小时  |
| CNHOUR6  | 6小时  |
| CNHOUR12 | 12小时 |
| CNHOUR24 | 1天   |
| CNDAY7   | 1周   |
| CNDAY30  | 1月   |

输出参数

| 名称   | 类型  | 描述     |
|------|-----|--------|
| name | str | 股票名称   |
| rate | str | 人气排行指数 |

接口示例

```python
import akshare as ak

stock_js_weibo_report_df = ak.stock_js_weibo_report(time_period="CNHOUR12")
print(stock_js_weibo_report_df)
```

数据示例

```
    name   rate
0   黄河旋风   9.86
1   东方财富   6.91
2   海王生物  10.09
3   秀强股份   4.56
4   江淮汽车  10.08
5    欧菲光  10.00
6   中兴通讯   9.98
7   鲁抗医药   9.97
8   海陆重工  10.07
9   中通客车   9.75
10  华天科技  10.02
11  亚星客车   7.70
12  中国平安  -0.66
13  新日恒力   9.98
14   同花顺  -0.90
15  赣锋锂业  10.00
16  北玻股份  10.09
17   比亚迪   7.02
18  沪电股份  10.00
19   太平洋   9.92
20  深康佳A  -8.02
21  天齐锂业   9.34
22  泰达股份   9.99
23  中信证券   0.68
24  欣龙控股  10.00
25  均胜电子  10.00
26   安居宝   9.98
27  联环药业  10.00
28  乾照光电   2.93
29  山东黄金  -3.38
30  国海证券   7.20
31  永鼎股份  10.00
32   漫步者  -4.51
33  江苏吴中  10.03
34  国农科技  10.00
35  中环股份   9.98
36  阳普医疗  10.01
37   新宙邦   8.91
38  兴森科技   9.98
39  南大光电   7.46
40  四环生物   9.98
41  海特高新  10.01
42  光环新网   7.97
43  晶方科技  -2.73
44  铜峰电子  10.04
45  华力创通  10.00
46  复星医药   9.41
47  力帆股份  10.14
48  永太科技   9.65
49  四维图新   8.76
```

## 彭博亿万富豪指数

(index_bloomberg_billionaires)=
### 彭博实时亿万富豪指数

接口：index_bloomberg_billionaires

目标地址：https://www.bloomberg.com/billionaires/

描述：彭博亿万富豪指数，全球前 500 名；该接口需要使用代理访问

限量：单次返回所有数据彭博亿万富豪排名数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称              | 类型  | 描述              |
|-----------------|-----|-----------------|
| rank            | str | Rank            |
| name            | str | Name            |
| total_net_worth | str | Total net worth |
| last_change     | str | $ Last change   |
| YTD_change      | str | $ YTD change    |
| country         | str | Country         |
| industry        | str | Industry        |

接口示例

```python
import akshare as ak

index_bloomberg_billionaires_df = ak.index_bloomberg_billionaires()
print(index_bloomberg_billionaires_df)
```

数据示例

```
    rank                        name  ...             country     industry
0      1                  Jeff Bezos  ...       United States   Technology
1      2                  Bill Gates  ...       United States   Technology
2      3             Mark Zuckerberg  ...       United States   Technology
3      4             Bernard Arnault  ...              France     Consumer
4      5               Steve Ballmer  ...       United States   Technology
..   ...                         ...  ...                 ...          ...
494  496                 Ira Rennert  ...       United States  Commodities
495  497  Traudl Engelhorn-Vechiatto  ...         Switzerland  Diversified
496  498            Sergey Galitskiy  ...  Russian Federation       Retail
497  499                  Xu Jingren  ...               China  Health Care
498  500                Shi Yonghong  ...           Singapore     Consumer
```

(index_bloomberg_billionaires_hist)=
### 历史彭博亿万富豪指数

接口：index_bloomberg_billionaires_hist

目标地址：https://stats.areppim.com/stats/links_billionairexlists.htm

描述：按照年份查询彭博亿万富豪指数；该接口需要使用代理访问

限量：单次返回当年所有数据彭博亿万富豪排名数据

输入参数

| 名称   | 类型  | 描述                                                   |
|------|-----|------------------------------------------------------|
| year | str | year="2021"; choice of {"2021", "2019", "2018", ...} |

输出参数

| 名称              | 类型  | 描述              |
|-----------------|-----|-----------------|
| rank            | str | Rank            |
| name            | str | Name            |
| total_net_worth | str | Total net worth |
| last_change     | str | $ Last change   |
| YTD_change      | str | $ YTD change    |
| country         | str | Country         |
| industry        | str | Industry        |
| age             | str | Age             |

接口示例

```python
import akshare as ak

index_bloomberg_billionaires_hist_df=ak.index_bloomberg_billionaires_hist(year='2019')
print(index_bloomberg_billionaires_hist_df)
```

数据示例

```
    rank                        name  ...             country     industry
0      1                  Jeff Bezos  ...       United States   Technology
1      2                  Bill Gates  ...       United States   Technology
2      3             Mark Zuckerberg  ...       United States   Technology
3      4             Bernard Arnault  ...              France     Consumer
4      5               Steve Ballmer  ...       United States   Technology
..   ...                         ...  ...                 ...          ...
494  496                 Ira Rennert  ...       United States  Commodities
495  497  Traudl Engelhorn-Vechiatto  ...         Switzerland  Diversified
496  498            Sergey Galitskiy  ...  Russian Federation       Retail
497  499                  Xu Jingren  ...               China  Health Care
498  500                Shi Yonghong  ...           Singapore     Consumer
```

(game_hot_rank_taptap)=
### TapTap 游戏榜单

接口：game_hot_rank_taptap

目标地址：https://www.taptap.cn/top/played

描述：按照榜单类型查询 TapTap 平台游戏排行榜数据

限量：单次返回指定榜单的全部游戏排名数据

输入参数

| 名称     | 类型  | 描述                                                          |
|--------|-----|-------------------------------------------------------------|
| symbol | str | symbol="热玩榜"; choice of {"热玩榜", "热门榜", "新品榜", "预约榜", "热卖榜"} |

输出参数

| 名称   | 类型             | 描述                        |
|------|----------------|---------------------------|
| 排名   | int64          | 榜单排名                      |
| 游戏名称 | str            | 游戏名称                      |
| 评分   | float64        | TapTap 玩家评分 (0-10 分制)     |
| 总点击量 | int64          | 游戏页面累计点击量                 |
| 游玩次数 | int64          | 累计游玩次数                    |
| 评论数  | int64          | 评论总数                      |
| 粉丝数  | int64          | 关注/粉丝数                    |
| 标签   | str            | 游戏标签 (逗号分隔，如 "模拟经营, 治愈") |
| 推荐语  | str            | 编辑/官方推荐语                  |
| 发布时间 | datetime64[ns] | 游戏发布时间                    |
| 游戏ID | str            | TapTap 平台游戏唯一 ID          |
| 图标链接 | str            | 游戏图标 URL                  |
| 简介   | str            | 游戏简介文本 (已清洗 HTML 标签)      |

接口示例

```python
import akshare as ak

game_hot_rank_taptap_df = ak.game_hot_rank_taptap(symbol="热玩榜")
print(game_hot_rank_taptap_df)
```

数据示例

```
      排名  ...                                                 简介
0      1  ...  直播时间：18:00-23:00\n《心动小镇》是一款慢节奏生活模拟游戏。无论拥有什么样的爱...
1      2  ...  这片银河中有名为「星神」的存在，祂们造就现实，抹消星辰，在无数「世界」中留下祂们的痕迹。你—...
2      3  ...  鹅鸭杀S2赛季［瀚漠迷踪］上线！黄沙漫天，神谕低语，全新地图「古代沙漠」、角色「决斗呆呆鸟」...
3      4  ...  神明娘爆涂乱射副副副游《乱涂！彩世界》4月28日正式上线！洛天依限时联动开启签到就送，首周爆...
4      5  ...  14W人打出96%好评如潮的《潜水员戴夫》国服手机版&TapPC版三端现已正式发售！白天潜水...
..   ...  ...                                                ...
145  146  ...  欢迎来到危机四伏的核污染海域，这里的一切生物都在悄然发生异变。你将化身为一条普通的小鱼，在这...
146  147  ...  【简介】\n玩家扮演一位家族老祖，开创一个家族，然后在大陆或者海域中，占领一个修仙灵山或小岛...
147  148  ...  【游戏介绍】\n《太空杀》是一款多人社交推理手游，在这里，你可能会收获一群黑心伙伴，一些爆笑...
148  149  ...  你睁开眼睛，\n发现自己身处于一个完全陌生的世界上——\n这是一场无限轮回的游戏，\n只有获...
149  150  ...  你说得对，但是《星落》是一款探险队沿途对抗大魔王的异世界冒险扫荡RPG。（绝赞发行中^^）\...
[150 rows x 13 columns]
```
