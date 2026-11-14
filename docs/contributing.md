# 贡献指南

## 贡献指南

### 克隆及提交代码

1. Fork [AKShare](https://github.com/akfamily/akshare) 仓库后克隆到本地，在 main 分支的基础上新建一个分支进行修改，main 分支中包含 AKShare 最新的开发代码
2. 安装 [uv](https://docs.astral.sh/uv/) 后，在仓库根目录运行 `uv sync` 安装开发环境，依赖版本由仓库中的 `uv.lock` 锁定
3. 运行 `uv run pre-commit install` 安装提交前检查和提交信息检查两个 git 钩子
4. 提交信息需要遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/) 规范，类型后面可以接中文描述，例如 `fix(index): 修复 index_all_cni 接口`
5. 修改完成后向 main 分支发起 Pull Request

### 代码及接口设计规范

1. 代码需要符合 **PEP 8** 要求，由 [Ruff](https://github.com/astral-sh/ruff) 进行格式化和检查；提交时 pre-commit 会自动运行，也可以手动运行 `uv run ruff format .` 和 `uv run ruff check .`
2. 接口名称遵循下文的“接口命名规范”，结构参考 **stock_zh_a_hist_tx**
3. 接口函数需要增加注释，注释规则请参考 **stock_zh_a_hist_tx** 接口的源码
4. 新增的接口需要在 `akshare/__init__.py` 中对应类目的分组里导入，用户才能通过 `ak.接口名` 调用
5. 模块放在与接口类目同名的子包中，文件名为“类目_主题_数据源.py”，例如期货接口放在 `akshare/futures/`，宏观接口放在 `akshare/macro/`；股票接口按数据字典的主题放在 `akshare/stock/quote/`、`finance/`、`holder/`、`issue/`、`valuation/`、`flow/`、`board/`、`research/`、`other/` 之一；一个模块只放同一类目的接口
6. 内置的 JS、JSON 等数据文件放在 `akshare/data/`，通过 `akshare/datasets.py` 中的函数获取路径，不要按模块文件的相对位置拼接路径
7. 需要在接口函数的注释中增加目标网站的地址（不是具体的数据接口地址，而是网页的地址）
8. 返回数据格式要求：
   1. 为了兼容 HTTP API 接口，所有返回的数据格式统一为 Pandas 中的 pandas.DataFrame 格式

### 接口命名规范

接口名是对外契约，改名即不兼容改动，新增接口时请一次定准。存量接口已在 1.20.41～1.20.46 中分批改名完毕；新接口必须符合本规范，否则 `tests/test_naming.py` 会失败。

1. 结构为“类目_市场或品种_主题_频率_数据源”，全部小写、以下划线分隔，没有的部分省略。以 **stock_zh_a_hist_tx** 为例：**stock** 为类目，**zh** 为国家或地区，**a** 为市场或品种，**hist** 表示历史行情，**tx** 表示数据源为腾讯
2. 第一段必须是接口所属的类目，即 `docs/data/` 下的目录名，如指数行情以 `index_` 开头，而不是 `stock_zh_index_`
3. 数据源或交易所标记放在末尾：**em**（东方财富）、**sina**（新浪财经）、**ths**（同花顺）、**tx**（腾讯）、**cninfo**（巨潮资讯）、**xq**（雪球）、**jsl**（集思录）、**lg**（乐咕乐股）、**js**（金十数据）、**sse**、**szse**、**bse**、**shfe**、**dce**、**czce**、**cffex**、**gfex**、**ine** 等，如 `futures_daily_dce`。同一种数据有多个数据源时必须带数据源后缀，不能靠调换词序区分
4. 用词要与金融含义一致，一个概念只用一种写法，一个词只表示一个概念：

| 含义 | 用词 | 不要使用 |
|------|------|----------|
| 实时行情（股票、基金、指数） | spot | - |
| 实时行情（期货、期权、债券、外汇、现货、加密货币） | realtime | spot，在这些类目中只表示现货、即期、现券 |
| 历史行情，可选日、周、月等周期 | hist | history |
| 只有日线的历史行情 | daily | 不用于表示“当日快照” |
| 分钟行情 | min | minute |
| 同比（年率）、环比（月率）、季率 | yoy、mom、qoq | yearly、monthly、quarterly，它们只表示数据频率 |
| 可转债 | cb | cov |
| 质押式回购 | repo | buy_back，它指股票回购 |
| 收益率 | yield | return、rate |
| 评级 | rating | rank（排名）、rate（利率、比率） |
| 净值 | nav | info |
| 库存 | inventory | stock |
| 手续费 | fee | comm |
| 商品 | commodity | comm |
| 外汇 | fx | forex、currency |
| 资产负债表、利润表、现金流量表 | balance_sheet、profit_sheet、cash_flow_sheet | debt、benefit、cash |
| 新闻、快讯 | news | info |
| 日历类数据（财报披露、分红、停复牌、经济日历） | calendar | news |
| 成份股 | cons | component、components |

5. 国家和地区使用固定写法：zh（中国内地的证券市场）、china（中国宏观数据）、hk、us（美国证券市场）、usa（美国宏观数据）、uk、euro、japan、germany、swiss、canada、australia
6. 有通行英文名称的概念使用英文，如财政收入、固定资产投资等宏观指标，不使用拼音首字母缩写。数据源网站的栏目名没有通行译名时（如龙虎榜 lhb、大宗交易 dzjy）沿用已有的拼音缩写，不再新造
7. 不使用 new、v2 等过渡性的词；接口被替换时直接移除旧接口
8. 接口更名需要在 `docs/changelog.md` 文末的“接口更名一览表”中登记

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
2. 接口文档位于 `docs/data/类目/` 目录下，一般每个类目一个 Markdown 文件，例如期货接口在 `docs/data/futures/futures.md`；股票和宏观数据按主题拆分为多个文件，例如股票行情接口在 `docs/data/stock/stock_quote.md`，请放到主题对应的文件中；目录名就是 `ak.search()` 中的类目名，不能修改；
3. 每个接口使用三级标题（`###`），放在对应的二级标题（`##`）分类下面，标题层级不能跳级；标题前一行写 `(接口名)=` 作为固定锚点，例如 `(stock_zh_a_hist_min_sina)=`，缺少时 CI 会报错；
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
(stock_zh_a_hist_min_sina)=
### 分时数据-新浪

接口：stock_zh_a_hist_min_sina

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

stock_zh_a_hist_min_sina_df = ak.stock_zh_a_hist_min_sina(symbol='sh600751', period='1', adjust="qfq")
print(stock_zh_a_hist_min_sina_df)
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

### 依赖选择说明

依赖及版本要求以 `pyproject.toml` 为准，这里说明两个关键依赖的选型原因：

1. mini-racer：用于执行数据源网页中的 JavaScript 解密代码。所有平台统一安装 [mini-racer](https://pypi.org/project/mini-racer/)（>=0.13.0），它是已停止更新的 py-mini-racer 的接续维护版本，导入名同为 `py_mini_racer`，提供 Windows、macOS 以及 x86_64、ARM64 Linux 的预编译包，Linux 需要 glibc 2.27 及以上。没有选用 PyExecJS，因为它自 2018 年起停止维护；也没有选用 Js2Py，因为它运行部分 JavaScript 代码时不稳定
2. pandas：用于采集后的数据清洗，要求 >=2.0.0，推荐使用最新版，AKShare 会优先支持最新版本

## 声明

1. 所提交的代码如不符合上述规范，则可能会被拒绝合并；
2. 由于某些原因，您所提交的代码、数据接口和文档会被修改、删除或被第三方使用；
3. **输出参数**里面的字段类型按 pandas 3 的实际类型填写，可以在接口示例代码后运行 `print(df.dtypes)` 查看，常见的有以下几种：
   1. 整数为 int64，浮点数为 float64，布尔值为 bool；
   2. 字符串为 str。pandas 3 起默认把文本列推断为字符串类型，`df.dtypes` 显示为 `str`，不再是 `object`；
   3. 通过 `.dt.date` 转换得到的日期为 object，其中每个元素是 `datetime.date` 对象；未转换的日期时间列为 datetime64，并按实际显示填写精度，如 `datetime64[us]`；
   4. 整列都是空值、或者混合了多种类型的列为 object。
