# 商品

## 合约持仓数据

### 接口名称

variety_positions

### 接口描述

合约持仓数据接口

### 请求参数

|参数名|说明|举例|
|-----  |-----|-----|
|fields |多头/空头   |longs: 返回多头数据; shorts: 返回空头数据  |
|code |合约代号   |rb1810  |
|date |查询日期   |2018-08-08  |

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|:-----|
|longs |array   |多头龙虎榜  |
|shorts |array   |空头龙虎榜  |
|broker |string   |席位  |
|long |int   |该席位多头持仓量  |
|long_chge |int   |该席位多头持仓变化量  |
|short |int   |该席位空头持仓量  |
|short_chge |int   |该席位空头持仓变化量  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_positions_df = pro.variety_positions(fields="longs", code="rb1810", date="2018-08-08")
print(variety_positions_df)
```

### 返回示例

```
   broker   long  long_chge
0    永安期货  80565       3075
1    申银万国  65572       2992
2    华泰期货  49279      -1552
3    中信期货  46272       4286
4    海通期货  42596       -286
5    方正中期  41839      -7504
6    鲁证期货  41520       -550
7    银河期货  38892      -2800
8    一德期货  34618      -1378
9    国泰君安  25854      -2188
10   广发期货  21496      -1695
11   国投安信  21494       2193
12   大地期货  20705         23
13   兴证期货  20166       4071
14   浙商期货  20001       -817
15   南华期货  19311      -2173
16   东海期货  18912      -1259
17   东证期货  15956       -192
18   瑞达期货  15648      -2091
19   光大期货  14758       -910
20   中国国际  12772      12772
21   国海良时      0     -15721
```

## 商品持仓数据

### 接口名称

variety_all_positions

#### 接口描述

商品持仓数据接口

#### 请求参数

|参数名|说明|举例|
|-----  |-----|-----|
|fields |多头/空头   |longs: 返回多头数据; shorts: 返回空头数据  |
|symbol |合约代号   |RB  |
|date |查询日期   |2018-08-08  |

#### 返回参数

|参数名|类型|说明|
|:-----  |:-----|:-----|
|longs |array   |多头龙虎榜  |
|shorts |array   |空头龙虎榜  |
|broker |string   |席位  |
|long |int   |该席位多头持仓量  |
|long_chge |int   |该席位多头持仓变化量  |
|short |int   |该席位空头持仓量  |
|short_chge |int   |该席位空头持仓变化量  |
|code |string   |具体合约  |

#### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_all_positions_df = pro.variety_all_positions(fields="shorts", symbol="RB", date="2018-08-08")
print(variety_all_positions_df)
```

#### 返回示例

```
   broker   long  long_chge    code
0    东证期货      0        -60  rb1808
1    永安期货  80565       3075  rb1810
2    申银万国  65572       2992  rb1810
3    华泰期货  49279      -1552  rb1810
4    中信期货  46272       4286  rb1810
5    海通期货  42596       -286  rb1810
6    方正中期  41839      -7504  rb1810
7    鲁证期货  41520       -550  rb1810
8    银河期货  38892      -2800  rb1810
9    一德期货  34618      -1378  rb1810
10   国泰君安  25854      -2188  rb1810
11   广发期货  21496      -1695  rb1810
12   国投安信  21494       2193  rb1810
13   大地期货  20705         23  rb1810
14   兴证期货  20166       4071  rb1810
15   浙商期货  20001       -817  rb1810
16   南华期货  19311      -2173  rb1810
17   东海期货  18912      -1259  rb1810
18   东证期货  15956       -192  rb1810
19   瑞达期货  15648      -2091  rb1810
20   光大期货  14758       -910  rb1810
21   中国国际  12772      12772  rb1810
22   国海良时      0     -15721  rb1810
23   永安期货  76193       6726  rb1901
24   国泰君安  57533      10549  rb1901
25   东海期货  44408       2666  rb1901
26   华泰期货  43165      11233  rb1901
27   鲁证期货  33941        711  rb1901
28   银河期货  32133       2862  rb1901
29   一德期货  26147       4950  rb1901
30   方正中期  24644      -2103  rb1901
31   海通期货  23176       2234  rb1901
32   新湖期货  22354       -193  rb1901
33   金瑞期货  21595        229  rb1901
34   中信期货  20821       -226  rb1901
35   瑞达期货  20450       -768  rb1901
36   中国国际  20158        402  rb1901
37   华鑫期货  15665       5134  rb1901
38   海证期货  15444       -202  rb1901
39   中粮期货  13506        913  rb1901
40   东航期货  13312        600  rb1901
41   弘业期货  13267       -246  rb1901
42   申银万国  13233        631  rb1901
43   光大期货  10128      10128  rb1901
44   国投安信   8762       8762  rb1901
```

## 商品净持仓数据

### 接口名称

variety_net_positions

### 接口描述

商品净持仓数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|symbol |查询品种编码   |RB|
|broker |席位   |永安期货|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|trans_date |date   |查询日期  |
|net_position |int   |净持仓数据  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_net_positions_df = pro.variety_net_positions(symbol="RB", broker="永安期货", date="2018-08-08")
print(variety_net_positions_df)
```

### 返回示例

```
             variety_net_positions
trans_date              2018-08-08
net_position                 58463
```

## 合约行情数据

### 接口名称

variety_quotes

### 接口描述

合约行情数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|code |具体合约代号   |rb1810|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|open |float   |开盘价  |
|close |float   |收盘价  |
|high |float   |最高价  |
|low |float   |最低价  |
|volume |int   |成交量  |
|openint |int   |持仓量  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_quotes_df = pro.variety_quotes(code="rb1810", date="2018-08-08")
print(variety_quotes_df)
```

### 返回示例

```
              variety_quotes
open                    4237
close                   4236
high                    4278
low                     4205
volume               2620386
openint              2160052
settle_price            4240
```

## 商品沉淀资金数据

### 接口名称

variety_money

### 接口描述

商品沉淀资金数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|symbol |品种编码   |RB|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|trans_date |date   |查询日期  |
|total_value |float   |沉淀资金量，单位元  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_money_df = pro.variety_money(symbol="RB", date="2018-08-08")
print(variety_money_df)
```

### 返回示例

```
            variety_money
trans_date     2018-08-08
total_value   7.46824e+09
```

## 合约多空比数据

### 接口名称

variety_bbr

### 接口描述

合约多空比数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|code |具体合约代号   |rb1810|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|trans_date |date   |查询日期  |
|bbr |float   |多空比  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_bbr_df = pro.variety_bbr(code="rb1810", date="2018-08-08")
print(variety_bbr_df)
```

### 返回示例

```
           variety_bbr
trans_date  2018-08-08
bbr            54.5111
```

## 合约净持仓保证金变化数据

### 接口名称

variety_net_money_chge

### 接口描述

合约净持仓保证金变化数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|code |具体合约代号   |rb1810|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|broker |string   |席位  |
|value |float   |沉淀资金变化量，正数为向多，负数为向空，单位元  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_net_money_chge_df = pro.variety_net_money_chge(code="rb1810", date="2018-08-08")
print(variety_net_money_chge_df)
```

### 返回示例

```
   broker     value
0    国海良时 -59991336
1    方正中期 -45593568
2    国泰君安 -10364256
3    瑞达期货  -7979256
4    南华期货  -7742664
5    东海期货  -6521544
6    中大期货  -5998752
7    一德期货  -5258448
8    光大期货  -3152016
9    浙商期货  -3117672
10   华安期货         0
11   鲁证期货    183168
12   东证期货   1885104
13   广发期货   1911816
14   中辉期货   2110248
15   徽商期货   2316312
16   中信建投   2385000
17   银河期货   5449248
18   国投安信   7036704
19   海通期货   9528552
20   申银万国   9982656
21   永安期货  15821136
22   华泰期货  16198920
23   中信期货  18721296
24   兴证期货  18748008
25   中国国际  48737952
26   大地期货  55812816
```

## 合约净持仓保证金数据

### 接口名称

variety_net_money

### 接口描述

合约净持仓保证金数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|code |具体合约代号   |rb1810|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|broker |string   |席位  |
|value |float   |净持仓保证金数据，正数为净多，负数为净空，单位元  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_net_money_df = pro.variety_net_money(code="rb1810", date="2018-08-08")
print(variety_net_money_df)
```

### 返回示例

```
   broker      value
0    中辉期货  -99601416
1    中大期货  -90671976
2    银河期货  -84314520
3    徽商期货  -72374256
4    中信建投  -70912728
5    光大期货  -52279200
6    国泰君安  -40617504
7    东海期货  -39449808
8    南华期货  -32596272
9    东证期货  -21823704
10   兴证期货   -7998336
11   华安期货          0
12   国海良时          0
13   国投安信   17881776
14   广发期货   26360928
15   中信期货   31108032
16   方正中期   37144944
17   中国国际   48737952
18   海通期货   49447728
19   瑞达期货   59712768
20   鲁证期货   72576504
21   浙商期货   76323816
22   大地期货   79010280
23   永安期货   87939720
24   华泰期货  122886648
25   一德期货  132102288
26   申银万国  193455936
```

## 合约总持仓保证金数据

### 接口名称

variety_total_money

### 接口描述

合约总持仓保证金数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|code |具体合约代号   |rb1810|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|broker |string   |席位  |
|value |float   |总持仓保证金数据，单位元  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_total_money_df = pro.variety_total_money(code="rb1810", date="2018-08-08")
print(variety_total_money_df)
```

### 返回示例

```
   broker      value
0    中辉期货   99601416
1    中大期货   90671976
2    银河期货  381138264
3    徽商期货   72374256
4    中信建投   70912728
5    光大期货  164912256
6    国泰君安  237935232
7    东海期货  183786192
8    南华期货  179977824
9    东证期货  143599896
10   兴证期货  161905248
11   华安期货          0
12   国海良时          0
13   国投安信  146160432
14   广发期货  137696544
15   中信期货  322039872
16   方正中期  282170304
17   中国国际   48737952
18   海通期货  275644944
19   瑞达期货   59712768
20   鲁证期货  244304136
21   浙商期货   76323816
22   大地期货   79010280
23   永安期货  526932360
24   华泰期货  253210680
25   一德期货  132102288
26   申银万国  306989568
```

## 商品的席位盈亏数据

### 接口名称

variety_profit

### 接口描述

商品的席位盈亏数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|symbol |品种编码   |RB|
|start_date |查询开始日期   |2018-02-08|
|end_date |查询结束日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|broker |string   |席位  |
|total_profit |float   |盈亏数据，单位元  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_profit_df = pro.variety_profit(symbol="RB", start_date="2018-02-08", end_date="2018-08-08")
print(variety_profit_df)
```

### 返回示例

```
   broker  total_profit
0    中辉期货    -367083530
1    东证期货    -274196150
2    招商期货    -252721200
3    海通期货    -231433760
4    中信建投    -224441170
5    广发期货    -224286720
6    徽商期货    -173556810
7    光大期货    -153981100
8    南华期货    -126979400
9    浙商期货    -124635130
10   国联期货    -121934700
11   中信期货    -106715730
12   道通期货     -95878520
13   申银万国     -82166760
14   国泰君安     -68046340
15    美尔雅     -67452870
16   国富期货     -53265140
17   建信期货     -28952470
18   华创期货     -28168230
19   东吴期货     -27047350
20   倍特期货     -26667130
21   东海期货     -23452290
22   长江期货     -18914000
23   前海期货     -18877690
24   中财期货     -18359420
25   广金期货     -18279570
26   首创期货     -16325810
27   先融期货     -14990740
28   西南期货     -14951300
29   弘业期货     -12616830
..    ...           ...
58   大有期货      10754880
59   迈科期货      13973520
60   东华期货      23343430
61   东航期货      23730720
62   上海大陆      23984570
63   宝城期货      30425320
64   中粮期货      30954960
65   华安期货      31170640
66   国海良时      31988920
67   金元期货      47093010
68   宏源期货      49972150
69   华鑫期货      56233900
70   大地期货      62694890
71   一德期货      66660920
72   国投安信      87703230
73   五矿经易      98321360
74   格林大华     110700170
75   中国国际     112853750
76   鲁证期货     132389940
77   中钢期货     174935310
78   国贸期货     180413050
79   新湖期货     202053740
80   华泰期货     238926470
81   金瑞期货     242494130
82   信达期货     304877710
83   方正中期     307737560
84   兴证期货     331936440
85   瑞达期货     373100440
86   永安期货     436014140
87   银河期货     652020020
```

## 自研指标数据

### 接口名称

variety_strategies

### 接口描述

自研指标数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|code |合约代号   |rb1810|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|trans_date |date   |查询日期  |
|longhu |float   |龙虎比  |
|niuxiong |float   |牛熊线  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_strategies_df = pro.variety_strategies(code="rb1810", date="2018-08-08")
print(variety_strategies_df)
```

### 返回示例

```
           variety_strategies
trans_date         2018-08-08
longhu                  7.954
niuxiong                   10
```

## 龙虎比排行数据

### 多头排行

#### 接口名称

variety_longhu_top

#### 接口描述

龙虎比排行数据接口

#### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|date |查询日期   |2018-08-08|

#### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|symbol |string   |品种编码  |
|code |string   |具体合约代号  |
|value |float   |龙虎比  |

#### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_longhu_long_top_df = pro.variety_longhu_top(fields="long", date="2018-08-08")
print(variety_longhu_long_top_df)
```

#### 返回示例

```
     code symbol      value
0  cu1905     CU  56.976958
1  au1812     AU  41.579291
2  sm1901     SM  10.242171
3   v1901      V   9.424667
4  sf1901     SF   9.115990
5   j1901      J   7.243534
6  rb1901     RB   6.526060
7  hc1901     HC   4.098336
8  cu1811     CU   3.650439
9  al1810     AL   3.589835
```

### 空头排行

#### 接口名称

variety_longhu_top

#### 接口描述

龙虎比排行数据接口

#### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|date |查询日期   |2018-08-08|

#### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|symbol |string   |品种编码  |
|code |string   |具体合约代号  |
|value |float   |龙虎比  |

#### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_longhu_short_top_df = pro.variety_longhu_top(fields="short", date="2018-08-08")
print(variety_longhu_short_top_df)
```

#### 返回示例

```
     code symbol      value
0  oi1905     OI -39.089038
1  ru1905     RU -27.660905
2   y1905      Y -25.509936
3  al1812     AL -24.926301
4   m1905      M -24.878081
5  cu1901     CU -23.127945
6   a1901      A -21.994445
7   y1901      Y -21.953714
8   c1901      C -21.143036
9  rm1905     RM -19.026835
```

## 牛熊线排行数据

### 多头排行

#### 接口名称

variety_niuxiong_top

#### 接口描述

牛熊线排行数据接口

#### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|date |查询日期   |2018-08-08|

#### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|symbol |string   |品种编码  |
|code |string   |合约代号  |
|value |float   |牛熊线  |

#### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_niuxiong_long_top_df = pro.variety_niuxiong_top(fields="long", date="2018-08-08")
print(variety_niuxiong_long_top_df)
```

#### 返回示例

```
     code symbol  value
0  au1812     AU     45
1  rm1901     RM     30
2  sm1901     SM     28
3   v1901      V     27
4   t1812      T     23
5   j1901      J     23
6  sm1809     SM     23
7  ta1903     TA     23
8  ta1905     TA     21
9  sf1901     SF     20
```

### 空头排行

#### 接口名称

variety_niuxiong_top

#### 接口描述

牛熊线排行数据接口

#### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|date |查询日期   |2018-08-08|

#### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|symbol |string   |品种编码  |
|code |string   |合约代号  |
|value |float   |牛熊线  |

#### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_niuxiong_short_top_df = pro.variety_niuxiong_top(fields="short", date="2018-08-08")
print(variety_niuxiong_short_top_df)
```

#### 返回示例

```
     code symbol  value
0   a1901      A    -40
1  cu1810     CU    -37
2  zn1810     ZN    -32
3  ru1901     RU    -26
4  ru1905     RU    -23
5   y1905      Y    -22
6  al1811     AL    -21
7   l1901      L    -20
8  hc1810     HC    -16
9   y1901      Y    -14
```

## 商品相关研报数据

### 接口名称

variety_reports

### 接口描述

商品相关研报数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|csymbolode |品种编码   |RB|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|title |string   |研报标题  |
|pub |string   |研报发布人  |
|time |datetime   |发布时间  |
|url |string   |研报地址  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_reports_df = pro.variety_reports(csymbolode="RB", date="2018-08-08")
print(variety_reports_df)
```

### 返回示例

```
    pub  ...                                                url
0  中信期货  ...  https://report.qhkch.com/47/黑色建材日报/reportd471f...
1  格林大华  ...  https://report.qhkch.com/274/工业品/reportd836d83...
2  格林大华  ...  https://report.qhkch.com/274/深度报告/reportd003e4...
3  华泰期货  ...  https://report.qhkch.com/127/金属/report11f7a4db...
4  华泰期货  ...  https://report.qhkch.com/127/黑色建材/reportdd6bdd...
5  银河期货  ...  https://report.qhkch.com/416/黑色链/reportb05ee81...
6  兴证期货  ...  https://report.qhkch.com/101/工业品日报/report26db3...
```

## 商品列表数据

### 接口名称

variety_all

### 接口描述

商品列表数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|csymbolode |品种编码   |RB|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|name |string   |品种名称  |
|symbol |string   |品种编码  |
|market |string   |所在市场  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_all_df = pro.variety_all()
print(variety_all_df)
```

### 返回示例

```
   market name symbol
0     上期所  螺纹钢     RB
1     大商所  铁矿石      I
2     大商所   焦煤     JM
3     大商所   焦炭      J
4     郑商所   棉纱     CY
5     上期所   热卷     HC
6     郑商所   苹果     AP
7     郑商所   棉花     CF
8     郑商所   玻璃     FG
9     郑商所   甲醇     MA
10    郑商所   菜油     OI
11    郑商所   菜粕     RM
12    郑商所   硅铁     SF
13    郑商所   锰硅     SM
14    郑商所   白糖     SR
15    郑商所  PTA     TA
16    郑商所  动力煤     ZC
17    上期所   沪铜     CU
18    上期所   沪铝     AL
19    上期所   沪锌     ZN
20    上期所   沪铅     PB
21    上期所   沪镍     NI
22    上期所   沪锡     SN
23    上期所   沪金     AU
24    上期所   沪银     AG
25    上期所  燃料油     FU
26    上期所   沥青     BU
27    上期所   橡胶     RU
28    大商所   豆一      A
29    大商所   豆二      B
..    ...  ...    ...
35    大商所  棕榈油      P
36    大商所   PP     PP
37    大商所  PVC      V
38    大商所   豆油      Y
39    郑商所   强麦     WH
40    大商所  胶合板     BB
41    大商所  纤维板     FB
42    郑商所   稻谷     RI
43    郑商所  油菜籽     RS
44    郑商所   粳稻     JR
45    郑商所  晚籼稻     LR
46    上期所   线材     WR
47    上期所   原油     SC
48    郑商所   普麦     PM
49    上期所   纸浆     SP
50    大商所  乙二醇     EG
51    中金所   IF     IF
52    中金所   IC     IC
53    中金所   IH     IH
54    郑商所   红枣     CJ
55    郑商所   尿素     UR
56    上期所   NR     NR
57    大商所   粳米     RR
58    上期所  不锈钢     SS
59    大商所  苯乙烯     EB
60    郑商所   纯碱     SA
61    中金所   二债     TS
62    中金所   五债     TF
63    中金所   十债      T
64    大商所  LPG     PG
```

## 合约索引

### 接口名称

variety_list

### 接口描述

合约索引数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|- |string   | 合约  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_list_df = pro.variety_list(date="2018-08-08")
print(variety_list_df)
```

### 返回示例

```
          0
0     a1809
1     a1811
2     a1901
3     a1903
4     a1905
..      ...
495  zn1903
496  zn1904
497  zn1905
498  zn1906
499  zn1907
```

## 非期货公司净持仓

### 接口名称

variety_no_futures

### 接口描述

非期货公司净持仓数据接口

### 请求参数

|参数名|说明|举例|
|:-----  |:-----|-----|
|symbol |品种编码	   |RB|
|date |查询日期   |2018-08-08|

### 返回参数

|参数名|类型|说明|
|:-----  |:-----|-----|
|trans_date |date   | 查询日期  |
|net_value |int   | 非期货公司净持仓数据  |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
variety_no_futures_df = pro.variety_no_futures(symbol="RB", date="2018-08-08")
print(variety_no_futures_df)
```

### 返回示例

```
           variety_no_futures
trans_date         2018-08-08
net_value               -1000
```
