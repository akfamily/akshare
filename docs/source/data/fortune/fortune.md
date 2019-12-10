## [AkShare](https://github.com/jindaxiang/akshare) 财富500强

接口: fortune_rank

目标地址: http://www.fortunechina.com/fortune500/node_65.htm

描述: 获取指定年份财富世界500强公司排行榜

限量: 单次返回某一个年份的所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述 |
| -------- | ---- | ---- | --- |
| year | int  | Y    |   year="2019"|

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 公司名称      | str   | Y        | -  |
| 营业收入      | float   | Y        | 注意单位   |
| 利润      | float   | Y        | 注意单位   |
| 国家      | float   | Y        | -   |

接口示例

```python
import akshare as ak
fortune_df = ak.fortune_rank(year="2019")
print(fortune_df)
```

数据示例

```
公司名称(中英文)  营业收入(百万美元)  利润(百万美元)   国家
0                             沃尔玛（WALMART)    514405.0    6670.0   美国
1                中国石油化工集团公司（SINOPEC GROUP)    414649.9    5845.0   中国
2            荷兰皇家壳牌石油公司（ROYAL DUTCH SHELL)    396556.0   23352.0   荷兰
3    中国石油天然气集团公司（CHINA NATIONAL PETROLEUM)    392976.6    2270.5   中国
4                       国家电网公司（STATE GRID)    387056.0    8174.8   中国
..                                     ...         ...       ...  ...
495                              纽柯（NUCOR)     25067.3    2360.8   美国
496               蒙特利尔银行（BANK OF MONTREAL)     25002.7    4235.1  加拿大
497        泰康保险集团（TAIKANG INSURANCE GROUP)     24931.7    1794.6   中国
498        Ultrapar控股公司（ULTRAPAR HOLDINGS)     24816.0     314.8   巴西
499                  法国液化空气集团（AIR LIQUIDE)     24796.6    2494.2   法国
```
