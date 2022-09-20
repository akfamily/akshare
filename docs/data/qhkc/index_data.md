# 指数

## 指数信息

### 接口名称

index_info

### 接口描述

指数信息接口

### 请求参数

| 参数名      | 说明   | 举例                                        |
|:---------|:-----|-------------------------------------------|
| index_id | 指数id | index0070c0eb-93ba-2da9-6633-fa70cb90e959 |

### 返回参数

| 参数名           | 类型       | 说明                                   |
|:--------------|:---------|--------------------------------------|
| name          | string   | 指数名称                                 |
| all_brokers   | int      | 是否包含所有席位，0:否，1:是                     |
| created_time  | datetime | 创建时间                                 |
| all_varieties | int      | 是否包含所有品种，0:否，1:所有商品，2:所有股指，3:所有商品和股指 |
| status        | int      | 是否开放，0:不开放，1:开放                      |
| nickname      | string   | 创建人昵称                                |
| varieties     | array    | 包含品种的编码， all_varieties为0时返回          |
| brokers       | array    | 包含席位， all_brokers为0时返回               |

### 示例代码

```python
from akshare import pro_api

pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
index_info_df = pro.index_info(index_id="index0070c0eb-93ba-2da9-6633-fa70cb90e959")
print(index_info_df)
```

### 返回示例

```
   name  all_brokers  ... nickname  varieties
0  奇货黑链            1  ...     奇货可查         RB
1  奇货黑链            1  ...     奇货可查          I
2  奇货黑链            1  ...     奇货可查         JM
3  奇货黑链            1  ...     奇货可查          J
4  奇货黑链            1  ...     奇货可查         HC
5  奇货黑链            1  ...     奇货可查         SF
6  奇货黑链            1  ...     奇货可查         SM
```

## 指数权重数据

### 接口名称

index_weights

### 接口描述

指数权重数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|index_id |指数id   |index0070c0eb-93ba-2da9-6633-fa70cb90e959|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|variety |string   |品种编码  |
|weight |float   |权重值，百分数  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
index_weights_df = pro.index_weights(index_id="index0070c0eb-93ba-2da9-6633-fa70cb90e959", date="2018-08-08")
print(index_weights_df)
```

### 返回示例

```
  variety     weight
0      RB  37.714204
1       I  18.168484
2      JM   5.879807
3       J  26.265556
4      HC   7.369110
5      SF   2.431867
6      SM   2.170973
```

## 指数行情数据

### 接口名称

index_quotes

### 接口描述

指数行情数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|index_id |指数id   |index0070c0eb-93ba-2da9-6633-fa70cb90e959|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|trans_date |date   |日期  |
|volume |int   |指数成交量  |
|openint |int   |指数持仓量  |
|price |float   |指数价格  |
|bbr |float   |指数多空比  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
index_quotes_df = pro.index_quotes(index_id="index0070c0eb-93ba-2da9-6633-fa70cb90e959", date="2018-08-08")
print(index_quotes_df)
```

### 返回示例

```
           index_quotes
trans_date   2018-08-08
volume          4119565
openint         3584323
price           1195.06
bbr               51.57
```

## 指数沉淀资金数据

### 接口名称

index_money

### 接口描述

指数沉淀资金数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|index_id |指数id   |index0070c0eb-93ba-2da9-6633-fa70cb90e959|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|trans_date |date   |查询日期  |
|total_value |float   |指数沉淀资金，单位元  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
index_money_df = pro.index_money(index_id="index0070c0eb-93ba-2da9-6633-fa70cb90e959", date="2018-08-08")
print(index_money_df)
```

### 返回示例

```
             index_money
trans_date    2018-08-08
total_value  1.69873e+10
```

## 公共指数列表

### 接口名称

index_official

### 接口描述

公共指数列表接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|- |-   |-|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|id |string   |指数id  |
|name |string   |指数名  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
index_official_df = pro.index_official()
print(index_official_df)
```

### 返回示例

```
                                           id   name
0   index0070c0eb-93ba-2da9-6633-fa70cb90e959   奇货黑链
1   index0d5e051e-b262-bd7a-0fdc-89e2aab21ebb   奇货商品
2   index1ad9d461-7c43-9dea-9e8f-de20878b3ce1   奇货谷物
3   index35cc6f8a-dbca-0614-d48a-1d6258fad6b9  奇货贵金属
4   index6c063119-f98c-586e-64f2-7a42b5cd7d51   奇货饲料
5   index997af7f7-bd77-19cf-6f99-181a6d592f17  奇货软商品
6   indexa5dc7cfd-560e-86bb-50d7-5b4fb4f29ab5   奇货化工
7   indexa9a72e02-d36a-b4c4-58df-0bc75ad4e16b   奇货有色
8   indexd5e4f6e7-373e-334d-07b4-772ba758a9bd   奇货股指
9   indexe369e025-f33d-e787-c13d-0087e90c7d45  奇货铁合金
10  indexfa921e91-b136-605a-29fe-998d25355eaa   奇货油脂
```

## 个人指数列表

### 接口名称

index_mine

### 接口描述

个人指数列表接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|- |-   |-|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|id |string   |指数id  |
|name |string   |指数名  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
index_mine_df = pro.index_mine()
print(index_mine_df)
```

### 返回示例

```
                                           id    name
0   index027927d6-bba5-c432-9bf6-dfcaa75df2a8    油脂头部
1   index03cb6802-24a2-3f9b-813e-936f694fb2b2   新纪元反指
2   index04d11eef-ee50-9fef-e839-a64ad95c44eb     镍尾部
3   index153ca7e5-326d-2505-012f-c2eed754ef29     硬化工
4   index195e23d6-02ae-09e3-169c-f2331bc1d2a8    永兴黑色
5   index2a51db56-0424-75b6-35df-3c62fbcf92c9    螺纹亏损
6   index31e43117-e5e3-bb6f-24d6-8eff003d43dc    螺纹盈利
7   index33b671b8-3ac6-d41b-cb4c-554c44cf990f     软化工
8   index3491c65f-40bf-a739-84e3-5b935634ddcc    永安化工
9   index3cfbcf57-d3b5-cf0c-b4ba-c5db990f86ea    化工头部
10  index43cf357a-db28-c55b-03ac-21e2e4cc5aff    黑色头部
11  index4d44eb91-a7e6-eaf1-ba6e-f7f4e5255adb    油脂尾部
12  index54b33270-465a-c803-923a-f6a9ac7fa15e    东海道通
13  index5d9eb2bf-0aee-551b-58f8-5fac7cdda989     能化工
14  index5f6135ac-2283-4cab-05f0-f33d16444ee0    兴证化工
15  index6a66773f-d6b8-7138-4638-ff1d577252cf    永兴化工
16  index72db2cb8-32ba-50e6-c8b5-5d9e7700fb89  香蕉test
17  index763e0c86-ad90-d9b0-2997-fb298c79bff6   永兴海焦炭
18  index7f763d50-48d2-3a5c-9e30-0152ec31a84a   永兴瑞螺纹
19  index842902a2-4da0-0e8a-e060-3467c041dc20    黑色尾部
20  index91e9a576-ea5e-ffda-d295-35539c74ee60     镍头部
21  index92a6e980-de2b-e4b3-2c0d-0d217b4f870f   贵金属尾部
22  indexa36f1dd5-bc02-56dc-7a28-25ad7a3e4e10  永兴海PTA
23  indexabdbd00f-532a-46af-205f-fa96fa1eb048  兴证海通焦炭
24  indexac99bb42-2850-55ee-b0cd-91214a671288   动力煤盈利
25  indexc421b8f9-731a-a23e-9f3d-2832c3d43fc1    永安黑色
26  indexd10d46e8-ff5d-6199-129f-5e0408626aa5    化工头部
27  indexd4480270-06d1-f50b-5ec1-797afb236890    化工尾部
28  indexe0ef3f87-1e2f-fb76-96ec-3da230dc5d18  ma_top
29  indexef445153-4ed8-485d-a593-5a72fb9fa3e7    混沌黑色
30  indexf42a9e96-6747-5d56-b757-7b0c37a1b350   贵金属头部
```

## 指数资金动向

### 接口名称

index_trend

### 接口描述

指数资金动向接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|index_id |指数id   |index0070c0eb-93ba-2da9-6633-fa70cb90e959|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|broker |string   |席位  |
|variety |string   |品种编码  |
|money |float   |净持仓资金变化，正数为流多，负数为流空，单位元  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
index_trend_df = pro.index_trend(index_id="index0070c0eb-93ba-2da9-6633-fa70cb90e959", date="2018-08-08")
print(index_trend_df)
```

### 返回示例

```
    broker       money variety
0     一德期货  15417629.1      RB
1     一德期货 -17101588.0       I
2     一德期货     -1132.8      JM
3     一德期货   1743156.0       J
4     一德期货   1982721.6      HC
5     一德期货    119371.0      SF
6     一德期货     84793.1      SM
7     上海中期      4052.0       I
8     上海中期   -881926.5      SF
9     上海中期    -63940.8      SM
10    上海大陆    281848.0       I
11    上海大陆  -1539199.9      SF
12    上海大陆   -690040.4      SM
13    东亚期货    683400.0       I
14    东兴期货    -44717.4      SF
15    东兴期货   -944654.9      SM
16    东吴期货  -1711940.0       I
17    东吴期货    181650.0      SF
18    东吴期货   2104718.0      SM
19    东方汇金    293062.0      SF
20    东方汇金   -356715.8      SM
21    东海期货  34120575.0      RB
22    东海期货   -128124.0       I
23    东海期货  -5202372.0      JM
24    东海期货         0.0       J
25    东海期货   1732760.0      HC
26    东海期货    406896.0      SF
27    东航期货   2218860.0      RB
28    东航期货  12615508.0       I
29    东航期货  -1016428.8      JM
..     ...         ...     ...
306   道通期货    -77712.0       J
307   道通期货    396009.6      HC
308   道通期货      2923.9      SM
309   金元期货    105278.4      JM
310   金瑞期货    846864.9      RB
311   金瑞期货   5057712.0       I
312   金瑞期货    179521.6      HC
313   金瑞期货   -897637.3      SM
314   金鹏期货   2785860.0       I
315   银河期货 -18998891.1      RB
316   银河期货  21759360.0       I
317   银河期货   6617714.4      JM
318   银河期货  14434476.0       J
319   银河期货  13661480.0      HC
320   银河期货         0.0      SF
321   银河期货   -927011.4      SM
322   锦泰期货   -329640.0       I
323   长安期货   -357780.0       I
324   长安期货   -109494.0      SM
325   集成期货   4157011.2      JM
326   首创期货   1409441.6      HC
327   首创期货    -54747.0      SM
328   鲁证期货   2812517.1      RB
329   鲁证期货   1219528.0       I
330   鲁证期货   -826581.6      JM
331   鲁证期货   4429584.0       J
332   鲁证期货  -5784385.6      HC
333   鲁证期货     24332.0      SM
334   先锋期货    -16208.0       I
335   先锋期货    -84770.0      SF
```

## 指数的席位盈亏数据

### 接口名称

index_profit

### 接口描述

指数的席位盈亏数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----                           |
|index_id |指数id   |index0070c0eb-93ba-2da9-6633-fa70cb90e959|
|start_date |查询开始日期   |2018-07-08|
|end_date |查询结束日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|broker |string   |席位  |
|profit |float   |盈亏金额，正数为盈利，负数为亏损，单位元  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
index_profit_df = pro.index_profit(index_id="index0070c0eb-93ba-2da9-6633-fa70cb90e959", start_date="2018-07-08", end_date="2018-08-08")
print(index_profit_df)
```

### 返回示例

```
    broker     profit
0     中辉期货 -236037050
1     国富期货 -211233900
2     招商期货 -189026430
3     徽商期货 -177303650
4     中信建投 -162059340
5     光大期货 -161708310
6     宏源期货 -152712930
7     南华期货 -123349780
8     中大期货  -98211620
9     西南期货  -81650470
10    国贸期货  -77964940
11    东证期货  -55215900
12    华泰期货  -49744790
13    国信期货  -40138400
14    道通期货  -39560450
15    中信期货  -36253880
16    倍特期货  -25529630
17    上海大陆  -22757910
18    中国国际  -22142170
19    中财期货  -19836110
20    广金期货  -18279570
21    中钢期货  -17560300
22    创元期货  -17375800
23     美尔雅  -15690960
24    东吴期货  -13673950
25    集成期货  -13355650
26    混沌天成  -13257740
27    国联期货  -12468570
28    天风期货  -12027000
29    英大期货  -10035590
..     ...        ...
85    中金期货   12016800
86    格林大华   13952290
87    宝城期货   16466360
88    华鑫期货   20748590
89    恒泰期货   21447160
90    国海良时   22840150
91    先融期货   25679260
92    东航期货   46866870
93    东海期货   50519930
94    海证期货   51312130
95    建信期货   67504250
96    国投安信   68827180
97    弘业期货   75762520
98    五矿经易   92943700
99    一德期货  106023830
100   中粮期货  107062020
101   兴证期货  107773260
102   浙商期货  112590640
103   新湖期货  113574970
104   金瑞期货  120685700
105   银河期货  122931360
106   瑞达期货  144049340
107   方正中期  161708710
108   国泰君安  164995380
109   大地期货  174718740
110   信达期货  215495550
111   鲁证期货  227794850
112   申银万国  251123390
113   海通期货  277422320
114   永安期货  826966870
```