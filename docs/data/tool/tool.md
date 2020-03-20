## [AkShare](https://github.com/jindaxiang/akshare) 工具箱

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
| username str | Y | username="PiotrDabkowski"; owner of the repo; https://github.com/**PiotrDabkowski**/Js2Py |

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
