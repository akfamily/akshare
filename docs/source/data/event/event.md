## [AkShare](https://github.com/jindaxiang/akshare) 事件数据

### 新型冠状病毒-网易

接口: epidemic_163

目标地址: https://news.163.com/special/epidemic/

描述: 获取网易-新型冠状病毒-疫情数据

限量: 单次返回实时数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 地区      | str   | Y        |   |
| 数据      | str   | Y        |   |
						
接口示例
```python
import akshare as ak
epidemic_163_df = ak.epidemic_163()
print(epidemic_163_df)
```

数据示例

```
          地区 数据-截止2020/01/24 14:30
0         湖北        湖北确诊549例，死亡24例
1         广东               广东确诊53例
2         浙江               浙江确诊43例
3         北京               北京确诊26例
4         上海               上海确诊20例
5         湖南               湖南确诊24例
6         安徽               安徽确诊15例
7         重庆               重庆确诊27例
8         四川               四川确诊15例
9         江西                江西确诊7例
10        山东               山东确诊15例
11        河南                河南确诊9例
12        海南                海南确诊8例
13        广西               广西确诊13例
14        福建               福建确诊10例
15        江苏                江苏确诊9例
16        天津                天津确诊7例
17        陕西                陕西确诊3例
18        辽宁                辽宁确诊4例
19        贵州                贵州确诊3例
20       黑龙江          黑龙江确诊4例，死亡1例
21        新疆                新疆确诊2例
22        甘肃                甘肃确诊2例
23        河北           河北确诊2例，死亡1例
24        云南                云南确诊2例
25       内蒙古               内蒙古确诊1例
26        山西                山西确诊1例
27        宁夏                宁夏确诊2例
28        吉林                吉林确诊3例
29        香港                香港确诊2例
30        澳门                澳门确诊2例
31        台湾                台湾确诊1例
32        泰国                泰国确诊4例
33        越南                越南确诊2例
34        日本                日本确诊1例
35        韩国                韩国确诊2例
36        美国                美国确诊1例
37       新加坡               新加坡确诊1例
38  中国（含港澳台）       确诊 877 例，死亡 26例
39        海外               确诊 14 例
```

### 新型冠状病毒-丁香园

接口: epidemic_dxy

目标地址: http://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579615030&enterid=1579615030&from=groupmessage&isappinstalled=0

描述: 获取丁香园-新型冠状病毒-疫情数据

限量: 单次返回实时数据

输入参数-info

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| indicator | str | Y | indicator="info", 返回全国统计数据|

输出参数-info

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 字符串      | str   | Y        |统计时间和情况概述   |

接口示例-info

```python
import akshare as ak
epidemic_dxy_df = ak.epidemic_dxy(indicator="info")
print(epidemic_dxy_df)
```

数据示例-info

```
截至 2020-01-24 14:33 数据统计全国 确诊 883 例 疑似 1073 例 治愈 35 例 死亡 26 例
```

输入参数-data

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| indicator | str | Y | indicator="data", 返回全国-地区统计数据|

输出参数-data

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 地区      | str   | Y        | 区域   |
| 确诊      | str   | Y        | 数据  |
| 治愈      | str   | Y        | 数据  |
					
接口示例-data

```python
import akshare as ak
epidemic_dxy_df = ak.epidemic_dxy(indicator="data")
print(epidemic_dxy_df)
```

数据示例-data

```
      地区   确诊  治愈
0     湖北  549  31
1     武汉  495  28
2     孝感   22    
3     黄冈   12    
4     荆州    8    
..   ...  ...  ..
167   宁夏    2    
168   银川    1    
169   中卫    1    
170  内蒙古    1    
171  满洲里    1 
```

输入参数-news

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| indicator | str | Y | indicator="news", 返回全国突发新闻数据|

输出参数-news

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| title      | str   | Y        |新闻标题   |
| summary      | str   | Y        | 数据概述  |
| infoSource      | str   | Y        | 新闻来源  |
| provinceName      | str   | Y        | 省份  |
| sourceUrl      | str   | Y        | 新闻地址  |

接口示例-news

```python
import akshare as ak
epidemic_dxy_df = ak.epidemic_dxy(indicator="news")
print(epidemic_dxy_df)
```

数据示例-news

```
                                          title  ...                                          sourceUrl
0                                    福建新增 1 例病例  ...      http://m.weibo.cn/2656274875/4464277568378388
1                                      上海启动一级响应  ...      http://m.weibo.cn/2803301701/4464275537960579
2                                      北京启动一级响应  ...      http://m.weibo.cn/2803301701/4464275537960579
3                               北京 1 新冠肺炎确诊患者出院  ...      http://m.weibo.cn/2803301701/4464259805726673
4                           国务院征集新冠肺炎疫情防控工作问题线索  ...  https://mp.weixin.qq.com/s/vQ-m0wW2cVZGYfJtAAMeiQ
5                                     天津确诊第 7 例  ...      http://m.weibo.cn/2656274875/4464245485576951
6                                      天津启动一级响应  ...      http://m.weibo.cn/2803301701/4464245166727843
7                                      安徽启动一级响应  ...      http://m.weibo.cn/2803301701/4464244898679663
8                            重磅！发热咳嗽非新冠肺炎唯一首发症状  ...    http://m.weibo.cn/2803301701/4464244348901450 ​
9                                  宁夏新增确诊1例疑似1例  ...      http://m.weibo.cn/2656274875/4464239232497670
10                     山东今日新增确诊 6 例，山东累计确诊 15 例  ...      http://m.weibo.cn/2803301701/4464230751473157
11                        福建新增确诊 4 例，福建累计确诊 9 例  ...      http://m.weibo.cn/2803301701/4464229795391738
12                                     武汉关闭过江隧道  ...      http://m.weibo.cn/2803301701/4464223541240916
13                                  内蒙古确诊首例新冠肺炎  ...    http://m.weibo.cn/2803301701/4464216926774457 ​
14                                     辽宁新增确诊1例  ...      http://m.weibo.cn/2803301701/4464215920401389
15                              转发提醒：这个春节尽量不聚会！  ...      http://m.weibo.cn/2803301701/4464209549089465
16                        海南新增确诊病例4例，海南累计确诊病例8例  ...     https://m.weibo.cn/2803301701/4464204335127376
17                      湖南新增确诊 15 例：湖南累计确诊 24 例  ...                             http://dxys.com/xyJAVU
18                    江苏新增新冠肺炎确诊病例4例，江苏累计新冠肺炎9例  ...        https://m.weibo.cn/status/4464192113565122?
19                      重庆新增确诊病例18例，重庆累计确诊病例27例  ...        https://m.weibo.cn/status/4464192578727481?
20        吉林新增2例新型肺炎确诊病例，吉林省累计报告新型冠状病毒感染的肺炎病例3例  ...        https://m.weibo.cn/status/4464191185997393?
21                   韩联社报道称，韩国出现第二例新型冠状病毒肺炎确诊病例  ...        https://m.weibo.cn/status/4464190838721454?
22                                 新疆新冠肺炎确诊病例2例  ...        https://m.weibo.cn/status/4464190448434604?
23                   四川新增新冠肺炎7例，四川累计新冠肺炎确诊病例15例  ...        https://m.weibo.cn/status/4464188997392969?
24                      浙江新增确诊病例16例，浙江累计确诊病例43例  ...  https://weibo.com/2803301701/IqVPiqaGC?ref=hom...
25           1月23日0时-24时，湖北省新增新型冠状病毒感染的肺炎病例105例  ...        https://m.weibo.cn/status/4464187650423052?
26                                 日本确诊2例新型肺炎病例  ...        https://m.weibo.cn/status/4464186283758930?
27  1月23日0-24时，黑龙江省报告新型冠状病毒感染的肺炎新增确诊病例2例，死亡病例1例  ...        https://m.weibo.cn/status/4464184127847534?
28        1月23日10时至24时，安徽省报告新型冠状病毒感染的肺炎新增确诊病例6例  ...        https://m.weibo.cn/status/4464183024267897?
29                               山东新增3例新型肺炎确诊病例  ...  https://weibo.com/2656274875/IqVDCt7bx?ref=hom...
30                              广东新冠肺炎新增确诊病例21例  ...  https://weibo.com/2803301701/IqVDxtTVg?ref=hom...
31                               河南新冠肺炎新增确诊病例4例  ...  https://weibo.com/2803301701/IqVxI77w5?ref=hom...
32                               全国确诊830例新型肺炎病例  ...  https://weibo.com/2656274875/IqVnfb1Hm?from=pa...
33                               上海新增4例新冠肺炎确诊病例  ...  https://weibo.com/2803301701/IqVhVnT9w?ref=hom...
34                                 武汉将以小汤山模式建医院  ...  https://weibo.com/2803301701/IqV7dq2sm?ref=hom...
35                         世卫组织：新型肺炎不构成国际突发卫生事件  ...  https://m.weibo.cn/status/4464150224652866?sud...
36                     北京新增4例新型肺炎确诊病例，累计确诊病例26例  ...        https://m.weibo.cn/status/4464099343625924?
37                               天津新增1例新型肺炎确诊病例  ...      http://m.weibo.cn/2656274875/4464091609170082
38                               广西新增新冠肺炎确诊病例8例  ...  https://www.weibo.com/2803301701/IqSJAANR5?fro...
39                           【湖北省新冠肺炎疫情防控指挥部通告】  ...  https://www.weibo.com/2803301701/IqSEcDHtL?fro...
40                           湖南启动重大突发公共卫生事件一级响应  ...  https://www.weibo.com/2803301701/IqSwMxPd0?fro...
41                         武汉开通24小时电话接收社会各界爱心捐赠  ...  https://mp.weixin.qq.com/s/cICSHZNVynQj7m63RSAv1Q
42                  文化和旅游部、国家文物局：出现疑似病人就地停止旅游活动  ...  https://mp.weixin.qq.com/s/cICSHZNVynQj7m63RSAv1Q
43                               河北 1 例新型肺炎病例死亡  ...  https://weibo.com/2656274875/IqSjFocrm?from=pa...
44                               江西新增 4 例新型肺炎病例  ...        https://m.weibo.cn/status/4464049040965675?
45                           湖北黄石 10 名疑似患者已隔离治疗  ...        https://m.weibo.cn/status/4464044838788193?
46                              昆明确诊第 2 例新型肺炎病例  ...        https://m.weibo.cn/status/4464047963266414?
47                              财政部拨10亿补助湖北防控疫情  ...      http://m.weibo.cn/2803301701/4464041822671982
```

输入参数-hospital

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| indicator | str | Y | indicator="hospital", 返回全国发热门诊数据|

输出参数-hospital

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 省级行政区      | str   | Y        |-   |
| 市级      | str   | Y        | -  |
| 机构-医院      | str   | Y        | -  |

接口示例-hospital

```python
import akshare as ak
epidemic_dxy_df = ak.epidemic_dxy(indicator="hospital")
print(epidemic_dxy_df)
```

数据示例-hospital

```
   省级行政区  市级      机构／医院
0    湖北省  全省  定点医院/发热门诊
1    湖北省  武汉  定点医院/发热门诊
2    湖北省  荆门  定点医院/发热门诊
3    湖北省  宜昌  定点医院/发热门诊
4    湖北省  恩施  定点医院/发热门诊
..   ...  ..        ...
69    宁夏   /  定点医院/发热门诊
70    西藏   /  定点医院/发热门诊
71    新疆   /  定点医院/发热门诊
72    青海   /       定点医院
73    甘肃   /       定点医院
```

输入参数-plot

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| indicator | str | Y | indicator="plot", 绘制-全国疫情趋势图|

输出参数-plot

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 图片      | str   | Y        |图片, 需要自己保存   |

接口示例-plot

```python
import akshare as ak
ak.epidemic_dxy(indicator="plot")
```

图片示例-plot

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/event/epidemic_trend.PNG)
