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

人民币外汇即期报价

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 省份      | str   | Y        |   |
| 数据      | str   | Y        |   |
						
接口示例
```python
import akshare as ak
epidemic_163_df = ak.epidemic_163()
print(epidemic_163_df)
```

数据示例

```
     地区 数据-截止2020/01/23 10:20
0    湖北        湖北确诊444例，死亡17例
1    广东               广东确诊26例
2    北京               北京确诊14例
3    浙江               浙江确诊10例
4    上海               上海确诊16例
5    四川                四川确诊8例
6    重庆                重庆确诊6例
7    山东                山东确诊6例
8    河南                河南确诊5例
9    海南                海南确诊4例
10   天津                天津确诊4例
11   湖南                湖南确诊4例
12   辽宁                辽宁确诊2例
13   广西                广西确诊5例
14   江西                江西确诊2例
15   澳门                澳门确诊2例
16   山西                山西确诊1例
17   安徽                安徽确诊1例
18   宁夏                宁夏确诊1例
19   台湾                台湾确诊1例
20   云南                云南确诊1例
21   贵州                贵州确诊1例
22   福建                福建确诊1例
23   河北                河北确诊1例
24   江苏                江苏确诊1例
25  黑龙江               黑龙江确诊1例
26   泰国                泰国确诊4例
27   日本                日本确诊1例
28   韩国                韩国确诊1例
29   美国                美国确诊1例
```

### 新型冠状病毒-丁香园

接口: epidemic_dxy

目标地址: http://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579615030&enterid=1579615030&from=groupmessage&isappinstalled=0

描述: 获取丁香园-新型冠状病毒-疫情数据

限量: 单次返回实时数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| indicator | 无 | 无 | indicator="data", 返回统计数据, 其余返回新闻数据 |

输出参数-数据

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| provinceShortName      | str   | Y        |省份   |
| tags      | str   | Y        | 数据  |
					
接口示例-数据

```python
import akshare as ak
epidemic_dxy_df = ak.epidemic_dxy(indicator="data")
print(epidemic_dxy_df)
```

数据示例-数据

```
   provinceShortName                               tags
0                 湖北  确诊 444 例，疑似病例数待确认，治愈 28 例，死亡 17 例
1                 河北                             确诊 1 例
2                 云南                             确诊 1 例
3                 四川                      确诊 5 例，疑似 2 例
4                 山东                     确诊 2 例， 疑似 2 例
5                 广西                             确诊 5 例
6                 贵州                             确诊 1 例
7                 福建                             确诊 1 例
8                 安徽                      确诊 1 例，疑似 4 例
9                 海南                             确诊 4 例
10                宁夏                             确诊 1 例
11                吉林                             疑似 1 例
12                江西                             确诊 2 例
13                天津                             确诊 4 例
14                河南                             确诊 5 例
15                重庆                             确诊 6 例
16                澳门                             确诊 2 例
17                山西                             确诊 1 例
18                台湾                             确诊 1 例
19                香港                    确诊 1 例，疑似 117 例
20                陕西                             疑似 4 例
21                湖南                             确诊 4 例
22                辽宁                             确诊 2 例
23                北京                            确诊 14 例
24                广东                     确诊 26 例，疑似 1 例
25                上海                    确诊 16 例，疑似 22 例
26                浙江                            确诊 10 例
27               黑龙江                      确诊 1 例，疑似 1 例
28                江苏                             确诊 1 例
```

输出参数-新闻

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| title      | str   | Y        |省份   |
| summary      | str   | Y        | 数据  |
| infoSource      | str   | Y        | 数据  |
| provinceName      | str   | Y        | 数据  |
| sourceUrl      | str   | Y        | 数据  |

接口示例-新闻

```python
import akshare as ak
epidemic_dxy_df = ak.epidemic_dxy(indicator="")
print(epidemic_dxy_df)  # 新闻
```

数据示例-新闻

```
                        title  ...                                          sourceUrl
0       上海新增7例新型冠状病毒感染的肺炎确诊病例  ...                             http://dxys.com/g8Vhk6
1                陕西新增 4 例疑似病例  ...                             http://dxys.com/gTAnvn
2     截至1月22日24时，国内累计571例新型肺炎  ...     https://m.weibo.cn/2656274875/4463810716443567
3          武汉公交地铁轮渡长途客运23日起停运  ...  https://www.weibo.com/2803301701/IqJCvwRuB?fro...
4                广西新增3例新型肺炎病例  ...  https://www.weibo.com/2656274875/IqJdjB2oy?fro...
..                        ...  ...                                                ...
83    武汉 11 日无新增新型冠状病毒感染的肺炎病例  ...  http://wjw.wuhan.gov.cn/front/web/showDetail/2...
84  武汉初步诊断有新型冠状病毒感染的肺炎病例 41 例  ...  http://wjw.wuhan.gov.cn/front/web/showDetail/2...
85        武汉共发现病毒性肺炎诊断患者 59 例  ...  http://wjw.wuhan.gov.cn/front/web/showDetail/2...
86        武汉共发现病毒性肺炎诊断患者 44 例  ...  http://wjw.wuhan.gov.cn/front/web/showDetail/2...
87              武汉发现 27 例肺炎病例  ...  http://wjw.wuhan.gov.cn/front/web/showDetail/2...
```
