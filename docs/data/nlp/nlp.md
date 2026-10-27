# 自然语言处理

(nlp_answer)=
## 智能问答

接口：nlp_answer

目标地址：https://ownthink.com/robot.html

描述：思知-对话机器人的接口，以此来进行智能问答

限量：单次返回查询的数据结果

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
