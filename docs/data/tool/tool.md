## [AKShare](https://github.com/jindaxiang/akshare) 工具箱

### 交易日历

接口: tool_trade_date_hist_sina

目标地址: https://finance.sina.com.cn/realstock/company/klc_td_sh.txt

描述: 获取新浪财经的股票交易日历数据

限量: 单次返回从 1990-12-19 到 2020-12-31 之间的股票交易日历数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| - | - | - | - |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| trade_date      | str   | Y |  从 1990-12-19 至 2020-12-31 的股票交易日数据 |

接口示例

```python
import akshare as ak
tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
print(tool_trade_date_hist_sina_df)
```

数据示例

```
      trade_date
0     1990-12-19
1     1990-12-20
2     1990-12-21
3     1990-12-24
4     1990-12-25
          ...
7337  2020-12-25
7338  2020-12-28
7339  2020-12-29
7340  2020-12-30
7341  2020-12-31
```

### GitHub

#### Github Star list

接口: tool_github_star_list

目标地址: https://api.github.com/graphql

描述: 获取具体 GitHub 上某个 Repo 的 Star 用户列表

限量: 单次返回本 Repo 的所有 Star 用户，由于 API 限制，大型项目速度慢

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| word | str | Y | owner="PiotrDabkowski"; owner of the repo; https://github.com/**PiotrDabkowski**/Js2Py |
| indicator | str | Y | name="Js2Py"; repo name; https://github.com/PiotrDabkowski/**Js2Py** |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| -      | -   | -| a list of username   |

接口示例

```python
import akshare as ak
result_list = ak.tool_github_star_list(owner="PiotrDabkowski", name="Js2Py")
print(result_list)
```

数据示例

```
['ai-rex', 'paranoidi', 'kwcto', 'CoolOppo', ---]
```

#### Github User Email

接口: tool_github_email_address

目标地址: https://api.github.com/graphql

描述: 获取 GitHub 上用户的邮箱地址

限量: 单次返回具体用户的邮箱, 若该用户没用邮箱, 则返回空值, 注意 IP 提取限制

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| username | str | Y | username="PiotrDabkowski"; owner of the repo; https://github.com/**PiotrDabkowski**/Js2Py |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| -      | -   | -| the email address of the user   |

接口示例

```python
import akshare as ak
address = ak.tool_github_email_address(username="lateautumn4lin")
print(address)
```

数据示例

```
hanqiulun1123@gmail.com
```
