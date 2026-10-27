# [AKShare](https://github.com/akfamily/akshare) 贡献源码

## 贡献指南

### 克隆及提交代码

1. Fork [AKShare](https://github.com/akfamily/akshare) 仓库后克隆到本地，并切换到 [dev 分支](https://github.com/akfamily/akshare/tree/dev)，dev 分支中包含 AKShare 最新的开发代码
2. 安装 [uv](https://docs.astral.sh/uv/) 后，在仓库根目录运行 `uv sync` 安装开发环境，依赖版本由仓库中的 `uv.lock` 锁定
3. 运行 `uv run pre-commit install` 安装提交前检查和提交信息检查两个 git 钩子
4. 提交信息需要遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/) 规范，类型后面可以接中文描述，例如 `fix(index): 修复 index_all_cni 接口`
5. 修改完成后向 dev 分支发起 Pull Request

### 代码及接口设计规范

1. 代码需要符合 **PEP 8** 要求，由 [Ruff](https://github.com/astral-sh/ruff) 进行格式化和检查；提交时 pre-commit 会自动运行，也可以手动运行 `uv run ruff format .` 和 `uv run ruff check .`
2. 函数接口的设计参考 **stock_zh_a_hist_tx** 的结构，其中 **stock** 为金融产品，**zh** 为国家或地区，**a** 为市场或品种，**hist** 为 history 的缩写表示历史数据，**tx** 表示数据源为腾讯；常见的数据源后缀还有 **em**（东方财富）、**sina**（新浪财经）、**ths**（同花顺）等
3. 接口函数需要增加注释，注释规则请参考 **stock_zh_a_hist_tx** 接口的源码
4. 新增的接口需要在 `akshare/__init__.py` 中导入，用户才能通过 `ak.接口名` 调用
5. 需要在接口函数的注释中增加目标网站的地址（不是具体的数据接口地址，而是网页的地址）
6. 返回数据格式要求：
   1. 为了兼容 HTTP API 接口，所有返回的数据格式统一为 Pandas 中的 pandas.DataFrame 格式

### 标点符号规范

1. 中文正文统一使用全角标点 `，。；：？！（）“”、`，全角标点后面不再加空格；纯英文语境保持半角，例如写 `format: YYYYMMDD` 而不是 `format：`；
2. 该规范由 `scripts/check_punctuation.py` 检查，并已接入 pre-commit 的 `check-punctuation` 钩子自动修复。本地可以直接运行：

   ```shell
   python scripts/check_punctuation.py            # 只检查并列出待修改处
   python scripts/check_punctuation.py --fix      # 就地修复
   python scripts/check_punctuation.py --selftest # 运行内置守卫用例
   ```

3. 工具只会修改 **docstring、`#` 注释与 Markdown 正文**。以下三类内容是数据而不是正文，既不在工具范围内，也请不要手工去「纠正」：
   1. 中文列名与用户可传的参数值，例如 `"持股数（万股）"`、`"其中：境内法人持股"`、`ak.fund_fee_em(indicator="申购费率（前端）")`。它们既是对外的接口契约，也是与上游字段做匹配的键；
   2. 用于解析上游文本的字面量，例如 `.split("：")`、`.strip("（手续费更新时间：")`、`== "暂时没有数据！"`。其中的全角字符就是上游网页本身的内容。个别模块（如 `news_cctv.py`）会同时兼容半角和全角两种写法，这是有意的容错，不是冗余；
   3. Markdown 的围栏代码块，也就是 **接口示例** 与 **数据示例**，里面是真实的代码与输出。

4. 修改 `docs/data` 下的文档或 `akshare/__init__.py` 的导入后，需要重新生成接口元数据 `akshare/data/interfaces.json`，否则 CI 的 `registry-check` 会失败。pre-commit 会在提交时自动运行 `python scripts/build_registry.py` 完成这一步，未安装钩子时请手动运行。

### 文档撰写规范

1. 在新增或者修改接口后，需要修改相对应的接口文档，保持接口与文档的同步更新；
2. 具体的接口文档路径（以股票接口的文档为例）为：akshare->docs->data->stock->stock.md，其中 stock 表示股票文件夹，stock.md 为具体的 Markdown 文件，需要在 stock.md 中对相应的接口文档进行修改或新增；
3. 每个接口使用三级标题（`###`），放在对应的二级标题（`##`）分类下面，标题层级不能跳级；
4. 以股票分时数据接口文档为例：
   1. 主要包含以下部分内容：
      1. 接口：填写具体的接口名称
      2. 目标地址：填写具体数据获取网页的地址（不是数据接口地址）
      3. 描述：简单描述数据接口获取的数据
      4. 限量：返回数据的情况
      5. 输入参数：数据接口函数中需要输入的参数
      6. 输出参数：返回数据的字段，这里需要填写返回数据的字段和类型
      7. 接口示例：Python 调用该数据接口的代码
      8. 数据示例：利用 **接口示例** 代码获取的数据的接口，这里只需要复制前 **5** 行和后 **5** 行数据即可。

   2. 示例如下：

````markdown
### 分时数据-新浪

接口：stock_zh_a_minute

目标地址：http://finance.sina.com.cn/realstock/company/sh600519/nc.shtml

描述：新浪财经-沪深京 A 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率，可以指定是否复权

限量：单次返回指定股票或指数的指定频率的最近交易日的历史分时行情数据；注意调用频率

输入参数

| 名称     | 类型  | 描述                                                         |
|--------|-----|------------------------------------------------------------|
| symbol | str | symbol='sh000300'；同日频率数据接口                                |
| period | str | period='1'；获取 1, 5, 15, 30, 60 分钟的数据频率                    |
| adjust | str | adjust=""；默认为空：返回不复权的数据；qfq: 返回前复权后的数据；hfq: 返回后复权后的数据；|

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| day    | str     | -   |
| open   | float64 | -   |
| high   | float64 | -   |
| low    | float64 | -   |
| close  | float64 | -   |
| volume | float64 | -   |
| amount | float64 | -   |

接口示例

```python
import akshare as ak

stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol='sh600751', period='1', adjust="qfq")
print(stock_zh_a_minute_df)
```

数据示例

```
                      day  open  high   low  close  volume        amount
0     2026-02-05 13:53:00  3.91  3.91  3.90   3.90   20900    81593.0000
1     2026-02-05 13:54:00  3.91  3.91  3.90   3.91   18700    73076.0000
2     2026-02-05 13:55:00  3.91  3.91  3.90   3.91   12500    48832.0000
3     2026-02-05 13:56:00  3.90  3.91  3.90   3.90   13600    53093.0000
4     2026-02-05 13:57:00  3.90  3.91  3.90   3.90   36200   141190.0000
...                   ...   ...   ...   ...    ...     ...           ...
1965  2026-02-25 14:54:00  4.20  4.20  4.19   4.20  113600   476800.9888
1966  2026-02-25 14:55:00  4.19  4.20  4.19   4.19  255900  1073360.9803
1967  2026-02-25 14:56:00  4.20  4.21  4.19   4.21  745311  3132349.1281
1968  2026-02-25 14:57:00  4.21  4.22  4.20   4.21  367300  1545926.9902
1969  2026-02-25 15:00:00  4.20  4.20  4.20   4.20  845635  3551666.8430
[1970 rows x 7 columns]
```
````

## 声明

1. 所提交的代码如不符合上述规范，则可能会被拒绝合并；
2. 由于某些原因，您所提交的代码、数据接口和文档会被修改、删除或被第三方使用；
3. **输出参数**里面的字段类型按 pandas 3 的实际类型填写，可以在接口示例代码后运行 `print(df.dtypes)` 查看，常见的有以下几种：
   1. 整数为 int64，浮点数为 float64，布尔值为 bool；
   2. 字符串为 str。pandas 3 起默认把文本列推断为字符串类型，`df.dtypes` 显示为 `str`，不再是 `object`；
   3. 通过 `.dt.date` 转换得到的日期为 object，其中每个元素是 `datetime.date` 对象；未转换的日期时间列为 datetime64，并按实际显示填写精度，如 `datetime64[us]`；
   4. 整列都是空值、或者混合了多种类型的列为 object。
