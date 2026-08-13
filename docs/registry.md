# [AKShare](https://github.com/akfamily/akshare) 接口检索

AKShare 目前提供 1000 余个数据接口，靠翻阅文档逐个查找并不高效，尤其是在
由大模型 (LLM) 驱动的程序中，需要先从一句自然语言描述定位到可调用的接口名，
再去查它的参数与返回字段。

为此 AKShare 内置了一层接口检索能力，提供 `ak.search`, `ak.interface_info`
和 `ak.list_categories` 三个函数。

这一层**完全离线**: 接口元数据在构建时从本项目的文档与导出表生成，随安装包一起
分发 (`akshare/data/interfaces.json`)，调用时不会发起任何网络请求，也不需要
任何 token. 数据在首次检索时才加载，因此不会影响 `import akshare` 的速度。

## 检索接口

接口：search

描述：按关键词检索 AKShare 接口，返回按匹配度降序排列的结果

限量：单次返回不超过 limit 条记录，默认 20 条

输入参数

| 名称              | 类型   | 描述                                                       |
|-----------------|------|----------------------------------------------------------|
| query           | str  | query="可转债 实时行情"；关键词以空格或逗号分隔；传入完整接口名时该接口置顶              |
| limit           | int  | limit=20；返回条数上限；不可为负数                                  |
| category        | str  | category=None；默认返回全部类目，可用 ak.list_categories() 查询可选值   |
| documented_only | bool | documented_only=False；默认返回全部接口，设为 True 时仅返回本文档中已收录的接口 |

输出参数

| 名称   | 类型      | 描述                                    |
|------|---------|---------------------------------------|
| 接口名  | object  | 可直接用于 getattr(ak，接口名) 调用            |
| 类目   | object  | -                                     |
| 描述   | object  | 取自本文档的接口描述，未收录的接口该字段为 None           |
| 有无文档 | bool    | 该接口是否已被本文档收录                          |
| 匹配分  | float64 | 仅供同一次查询内比较相对排序，不可跨查询比较，详见下方"能力边界"  |

接口示例

```python
import akshare as ak

search_df = ak.search("可转债 实时行情", limit=5)
print(search_df)
```

数据示例

```
                      接口名    类目                                                       描述  有无文档   匹配分
0             bond_cb_jsl  bond  集思录可转债实时数据，包含行情数据（涨跌幅，成交量和换手率等）及可转债基本信息（转股价，溢价率和到期收益率等）  True  27.0
1      bond_zh_hs_cov_min  bond                                           东方财富网-可转债-分时行情  True  20.0
2  bond_zh_hs_cov_pre_min  bond                                      东方财富网-可转债-分时行情-盘前分时  True  20.0
3     bond_cov_comparison  bond                                   东方财富网-行情中心-债券市场-可转债比价表  True  17.0
4        fund_etf_spot_em  fund                                            东方财富-ETF 实时行情  True  17.0
```

接口示例-限定类目

```python
import akshare as ak

search_df = ak.search("净值", category="fund", limit=5)
print(search_df)
```

数据示例-限定类目

```
                           接口名    类目                                描述  有无文档   匹配分
0        fund_etf_category_ths  fund              同花顺理财-基金数据-每日净值-实时行情  True  10.5
1        fund_etf_fund_info_em  fund   东方财富网站-天天基金网-基金数据-场内交易基金-历史净值数据  True  10.5
2            fund_etf_spot_ths  fund          同花顺理财-基金数据-每日净值-ETF-实时行情  True  10.5
3  fund_financial_fund_info_em  fund  东方财富网站-天天基金网-基金数据-理财型基金收益-历史净值明细  True  10.5
4      fund_money_fund_info_em  fund       东方财富网-天天基金网-基金数据-货币型基金-历史净值  True  10.5
```

## 接口元数据

接口：interface_info

描述：返回单个接口的完整元数据，含输入参数，输出字段与调用示例

限量：单次返回一个接口的元数据

输入参数

| 名称   | 类型  | 描述                                                        |
|------|-----|-----------------------------------------------------------|
| name | str | name="energy_carbon_bj"；接口名；传入未知接口名时抛出异常并在消息中给出最接近的候选 |

输出参数

返回一个 dict，含以下键：

| 名称         | 类型   | 描述                                        |
|------------|------|-------------------------------------------|
| name       | str  | 接口名                                       |
| module     | str  | 该接口所在的模块路径                                |
| category   | str  | 所属类目                                      |
| documented | bool | 是否已被本文档收录                                 |
| desc       | str  | 接口描述，未收录时为 None                          |
| url        | str  | 数据源地址，未收录时为 None                         |
| limit_desc | str  | 单次返回的数据量说明，无此说明时为 None                   |
| params      | list | 输入参数列表，每项含 name/type/desc 三个键            |
| outputs    | list | 输出字段列表，每项含 name/type/desc 三个键            |
| example    | str  | 调用示例代码，未收录时为 None                        |

接口示例

```python
import akshare as ak

interface_info_dict = ak.interface_info("energy_carbon_bj")
print(interface_info_dict)
```

数据示例

```
{
  "category": "energy",
  "desc": "北京市碳排放权电子交易平台-北京市碳排放权公开交易行情",
  "documented": true,
  "example": "import akshare as ak\n\nenergy_carbon_bj_df = ak.energy_carbon_bj()\nprint(energy_carbon_bj_df)",
  "limit_desc": "全部历史数据",
  "module": "akshare.energy.energy_carbon",
  "name": "energy_carbon_bj",
  "outputs": [
    {"desc": "", "name": "日期", "type": "object"},
    {"desc": "注意单位: 吨", "name": "成交量", "type": "int64"},
    {"desc": "注意单位: 元/吨", "name": "成交均价", "type": "float64"},
    {"desc": "注意单位: 元", "name": "成交额", "type": "float64"},
    {"desc": "-", "name": "成交单位", "type": "object"}
  ],
  "params": [
    {"desc": "-", "name": "-", "type": "-"}
  ],
  "url": "https://www.bjets.com.cn/article/jyxx/"
}
```

传入的接口名不存在时会抛出 `InvalidParameterError`，并在异常消息中给出最接近的
几个候选，便于纠正拼写：

```python
import akshare as ak

try:
    ak.interface_info("stock_zh_a_hisr")
except Exception as e:
    print(e)
```

```
未知接口 stock_zh_a_hisr，最接近的候选: stock_zh_a_daily、stock_zh_a_hist、stock_zh_a_hist_min_em
```

## 类目列表

接口：list_categories

描述：列出全部类目及其接口数量，可用于确定 ak.search 的 category 取值

限量：单次返回全部类目

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型     | 描述  |
|-----|--------|-----|
| 类目  | object | -   |
| 接口数 | int64  | -   |

接口示例

```python
import akshare as ak

list_categories_df = ak.list_categories()
print(list_categories_df)
```

数据示例

```
                    类目  接口数
0              article    7
1                 bank    1
2                 bond   44
3                  cal    3
4             currency    5
5                   dc    3
6               energy    8
7                event    2
8                 fund   90
9              futures   83
10  futures_derivative    1
11                  fx   11
12                  hf    1
13               index   94
14       interest_rate   14
15               macro  215
16                 nlp    2
17              option   46
18              others   34
19                qdii    3
20            qhkc_web    8
21               reits    1
22                spot   15
23               stock  388
24       stock_feature    6
25   stock_fundamental    4
26                tool    1
```

## 能力边界

为免误用，这里说明这一层能做什么，不能做什么。

**这是关键词匹配，不是语义检索.** 匹配基于接口名，描述，类目与输出字段名上的
子串比对，并对未打空格的查询做二元组降级召回。它不理解同义词，也不做语义推理：
查询"历史行情"能匹配到描述中写有"历史行情"的接口，但匹配不到描述写作"历史数据"
的接口，即使两者说的是同一件事。因此建议一次查询多试几个说法，或用
`ak.list_categories()` 配合 `category` 参数缩小范围。

**传入完整接口名时该接口一定排在第一位.** 这是本层最可靠的用法——半记得一个
接口名时，用它确认全名并取回参数说明。尾随的逗号，顿号等标点不影响这一保证。

**匹配分只能在同一次查询内比较.** 该分值随查询词长度与接口名长度累加，不同查询
之间，甚至同一次查询中两个精确匹配之间，数值都不具可比性。请把它当作同次结果的
相对排序参考，不要用作跨查询的置信度阈值。

**部分接口没有描述.** 元数据以代码中的实际导出为准，因此结果中的每个接口名都
保证可以通过 `getattr(ak, 接口名)` 取到；但本文档尚未收录的接口，其 `描述`,
`输入参数` 等字段为空，`有无文档` 为 `False`. 若只想检索有完整文档的接口，传入
`documented_only=True`.

**元数据是构建时的快照.** 它随安装包分发，反映的是该版本发布时的接口与文档状态，
升级 AKShare 即可获得更新后的元数据。
