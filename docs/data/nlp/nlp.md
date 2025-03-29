## [AKShare](https://github.com/akfamily/akshare) 自然语言处理

### 知识图谱

接口: nlp_ownthink

目标地址: https://ownthink.com/

描述: 思知-知识图谱的接口, 以此来查询知识图谱数据

限量: 单次返回查询的数据结果

输入参数

| 名称        | 类型  | 描述                                                        |
|-----------|-----|-----------------------------------------------------------|
| word      | str | word="人工智能"                                               |
| indicator | str | indicator="entity"; Please refer **Indicator Info** table |

Indicator Info

| fields | type             | description                    |
|--------|------------------|--------------------------------|
| entity | str              | 	实体名                           |
| desc   | str              | 	实体简介                          |
| tag    | list             | 	实体标签                          |
| avg    | pandas.DataFrame | 	实体属性值，第一列为实体的属性，第二列为实体属性所对应的值 |

输出参数-entity

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | str | 结果  |

接口示例-entity

```python
import akshare as ak

nlp_ownthink_df = ak.nlp_ownthink(word="人工智能", indicator="entity")
print(nlp_ownthink_df)
```

数据示例-entity

```
人工智能[计算机科学的一个分支]
```

输出参数-desc

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | str | 结果  |

接口示例-desc

```python
import akshare as ak

nlp_ownthink_df = ak.nlp_ownthink(word="人工智能", indicator="desc")
print(nlp_ownthink_df)
```

数据示例-desc

```
人工智能（Artificial Intelligence），英文缩写为AI。
```

输出参数-avg

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | str | 结果  |

接口示例-avg

```python
import akshare as ak

nlp_ownthink_df = ak.nlp_ownthink(word="人工智能", indicator="avg")
print(nlp_ownthink_df)
```

数据示例-avg

```
     字段                       值
0   中文名                    人工智能
1   外文名  ARTIFICIALINTELLIGENCE
2    简称                      AI
3  提出时间                   1956年
4  提出地点             DARTMOUTH学会
5  名称来源             雨果·德·加里斯的著作
```

输出参数-tag

| 名称  | 类型   | 描述  |
|-----|------|-----|
| -   | list | 结果  |

接口示例-tag

```python
import akshare as ak

nlp_ownthink_df = ak.nlp_ownthink(word="人工智能", indicator="tag")
print(nlp_ownthink_df)
```

数据示例-tag

```
['中国通信学会', '学科']
```

### 智能问答

接口: nlp_answer

目标地址: https://ownthink.com/robot.html

描述: 思知-对话机器人的接口, 以此来进行智能问答

限量: 单次返回查询的数据结果

输入参数

| 名称       | 类型  | 描述               |
|----------|-----|------------------|
| question | str | question="姚明的身高" |

输出参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | str | 答案  |

接口示例

```python
import akshare as ak

nlp_answer_df = ak.nlp_answer(question="姚明的身高")
print(nlp_answer_df)
```

数据示例

```
姚明的身高是226厘米
```
