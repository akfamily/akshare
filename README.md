**简体中文** | [English](https://github.com/akfamily/akshare/blob/main/README_EN.md)

**资源分享**：对于想了解更多财经数据与量化投研的小伙伴，推荐一个专注于财经数据和量化研究的知识社区。
该社区提供相关文档和视频学习资源，汇集了各类财经数据源和量化投研工具的使用经验。
有兴趣深入学习的朋友可点此[了解更多](https://t.zsxq.com/ZCxUG)，也推荐大家关注微信公众号【数据科学实战】。

**重磅推荐**：AKQuant 是一款专为 **量化投研 (Quantitative Research)** 打造的高性能量化回测框架。它以 Rust 铸造极速撮合内核，
以 Python 链接数据与 AI 生态，旨在为量化投资者提供可靠高效的量化投研解决方案。参见[AKQuant](https://github.com/akfamily/akquant)

**工具推荐**：期魔方是一款本地化期货量化分析工具，适合数据分析爱好者使用。无需复杂部署，支持数据分析和机器学习功能，研究功能免费开放。
如需了解更多信息可访问[期魔方](https://qmfquant.com)。

![AKShare Logo](https://raw.githubusercontent.com/akfamily/akshare/main/assets/images/akshare_logo.jpg)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/akshare.svg)](https://pypi.org/project/akshare/)
[![PyPI](https://img.shields.io/pypi/v/akshare.svg)](https://pypi.org/project/akshare/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/akshare?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/akshare)
[![Documentation Status](https://img.shields.io/readthedocs/akshare/latest)](https://akshare.akfamily.xyz/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![akshare](https://img.shields.io/badge/Data%20Science-AKShare-green)](https://github.com/akfamily/akshare)
[![Checks Status](https://github.com/akfamily/akshare/actions/workflows/main_dev_check.yml/badge.svg)](https://github.com/akfamily/akshare/actions/workflows/main_dev_check.yml)
[![Release Status](https://github.com/akfamily/akshare/actions/workflows/release_and_deploy.yml/badge.svg)](https://github.com/akfamily/akshare/actions/workflows/release_and_deploy.yml)
[![MIT Licence](https://img.shields.io/badge/license-MIT-blue)](https://github.com/akfamily/akshare/blob/main/LICENSE)
[![](https://img.shields.io/github/forks/akfamily/akshare)](https://github.com/akfamily/akshare)
[![](https://img.shields.io/github/stars/akfamily/akshare)](https://github.com/akfamily/akshare)
[![](https://img.shields.io/github/issues/akfamily/akshare)](https://github.com/akfamily/akshare)

## 概览

[AKShare](https://github.com/akfamily/akshare) 是基于 Python 的开源财经数据接口库，目标是让获取财经数据变得简单，需要 64 位的 Python 3.11.5 或更高版本。

**Write less, get more!**

- 文档：[中文文档](https://akshare.akfamily.xyz/)
- **供 AI 助手使用的 MCP 服务**：[AKTools](https://github.com/akfamily/aktools) 让 Claude、Cursor 等 MCP 客户端用自然语言获取 AKShare 的数据，见 [AI 助手（MCP）](#ai-助手mcp)
- HTTP API：[AKTools](https://aktools.akfamily.xyz/) 还能把 AKShare 部署为 HTTP 服务，供其他编程语言调用

## AI 助手（MCP）

AKShare 是一个 Python 库，本身不提供 MCP 服务。配套项目 [AKTools](https://github.com/akfamily/aktools) 提供了 MCP 服务，并以 `io.github.akfamily/aktools` 登记在 [MCP 官方注册表](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.akfamily/aktools)中。Claude Code、Claude Desktop、Cursor 等 AI 助手可以根据一句自然语言的提问查找并调用 AKShare 的全部接口，例如“贵州茅台 2024 年 10 月 8 日到 11 日的前复权日线行情”。

只需要安装 [uv](https://docs.astral.sh/uv/)，不必另外安装其他软件：

```shell
claude mcp add aktools -- uvx --from aktools aktools-mcp
```

Claude Desktop、Cursor 等客户端的配置：

```json
{
  "mcpServers": {
    "aktools": {
      "command": "uvx",
      "args": ["--from", "aktools", "aktools-mcp"]
    }
  }
}
```

[![Add AKTools MCP server to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=aktools&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJha3Rvb2xzIiwiYWt0b29scy1tY3AiXX0%3D)

AKTools 没有把约 950 个接口逐个登记为工具，而是提供 3 个通用只读工具，由 AI 助手依次调用：

| 工具 | 用途 |
| --- | --- |
| `search_interfaces` | 按关键词查找接口名 |
| `describe_interface` | 查看接口的参数、默认值与说明 |
| `get_data` | 调用接口，最多返回 `max_rows` 行（默认 100，最大 1000） |

stdio 方式下还有第 4 个工具 `save_data`（AKTools 0.1.12 起），可以把完整数据保存为本机 CSV 文件，不受 `get_data` 的 1000 行限制；它会写文件，没有标注为只读。

用 `python -m aktools` 启动的服务在 `http://127.0.0.1:8080/mcp` 以 Streamable HTTP 方式提供上述 3 个只读工具，不提供 `save_data`；完整数据可通过 `get_data` 返回的 CSV 下载地址获取。HTTP 方式、代理、访问令牌与局域网访问的设置见 [MCP 使用指南](https://akshare.akfamily.xyz/mcp.html)。

## 安装

### uv（推荐）

```shell
uv pip install akshare --upgrade
```

uv 的安装与虚拟环境的创建见 [uv 环境配置](https://akshare.akfamily.xyz/uv.html)。

### pip

```shell
pip install akshare --upgrade
```

### 国内镜像

```shell
uv pip install akshare --upgrade --default-index https://pypi.tuna.tsinghua.edu.cn/simple
# 或者
pip install akshare --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 使用

### 获取数据

代码：

```python
import akshare as ak

stock_zh_a_hist_sina_df = ak.stock_zh_a_hist_sina(symbol="sz000001", period="daily", start_date="20170301", end_date="20231022", adjust="")
print(stock_zh_a_hist_sina_df)
```

输出：

```
            date   open   high  ...        amount  outstanding_share  turnover
0     2017-03-01   9.49   9.55  ...  3.301580e+08       1.691799e+10  0.002051
1     2017-03-02   9.51   9.54  ...  3.823959e+08       1.691799e+10  0.002386
2     2017-03-03   9.41   9.43  ...  3.219525e+08       1.691799e+10  0.002025
3     2017-03-06   9.40   9.46  ...  3.812123e+08       1.691799e+10  0.002391
4     2017-03-07   9.44   9.46  ...  2.777474e+08       1.691799e+10  0.001742
...          ...    ...    ...  ...           ...                ...       ...
1610  2023-10-16  11.00  11.03  ...  5.509887e+08       1.940555e+10  0.002585
1611  2023-10-17  11.01  11.05  ...  5.431709e+08       1.940555e+10  0.002543
1612  2023-10-18  10.99  11.02  ...  7.139799e+08       1.940555e+10  0.003359
1613  2023-10-19  10.91  10.92  ...  1.271915e+09       1.940555e+10  0.006127
1614  2023-10-20  10.55  10.67  ...  5.576186e+08       1.940555e+10  0.002711

[1615 rows x 9 columns]
```

### 搜索接口

AKShare 自带一份离线的接口登记，不必离开 Python、也不需要联网，就能按关键词查到接口。由大模型驱动的程序需要把一句描述对应到可调用的接口名时，这一功能尤其有用。

代码：

```python
import akshare as ak

search_df = ak.search("可转债 实时行情", limit=5)
print(search_df)

# 单个接口的完整信息：参数、输出字段与调用示例
interface_info_dict = ak.interface_info("bond_cb_jsl")
print(interface_info_dict)
```

输出：

```
                     接口名    类目                                                       描述  有无文档   匹配分
0  bond_cb_realtime_sina  bond                                             新浪财经-沪深可转债数据  True  34.5
1            bond_cb_jsl  bond  集思录可转债实时数据，包含行情数据（涨跌幅，成交量和换手率等）及可转债基本信息（转股价，溢价率和到期收益率等）  True  28.5
2        bond_cb_info_em  bond                                    东方财富网-数据中心-新股数据-可转债详情  True  15.0
3        bond_cb_list_em  bond                                 东方财富网-数据中心-新股数据-可转债数据一览表  True  15.0
4       bond_cb_list_ths  bond                                             同花顺-数据中心-可转债  True  15.0
```

传入完整的接口名时，该接口总是排在第一位，可以用来确认一个记不太清的名称。搜索是关键词匹配而不是语义检索，能做什么、不能做什么见[接口检索文档](https://akshare.akfamily.xyz/search.html)。

### 接口命名

接口名的结构是 `<类目>_<市场或主体>_<主题>_<数据源>`。以 `stock_zh_a_hist_em` 为例：类目 `stock`，市场 `zh_a`，主题 `hist`（历史行情），数据源 `em`（东方财富）。

- 第一段是 `ak.list_categories()` 返回的 15 个类目之一：`stock`、`index`、`fund`、`futures`、`option`、`bond`、`fx`、`macro`、`interest_rate`、`spot`、`energy`、`crypto`、`calendar`、`research`、`alternative`
- 最后一段通常是数据源，如 `em`、`sina`、`ths`、`tx`、`cninfo`、`sse`、`szse`，同一数据来自不同数据源时，接口名只有后缀不同
- 行情接口中，名称里的 `daily` 表示只有日线；带 `period` 参数（`daily`、`weekly`、`monthly`）的接口叫 `hist`，如 `stock_zh_a_hist_em` 和 `stock_zh_a_hist_sina`

### 从 1.20.41 之前的版本升级

1.20.41 至 1.20.54 把所有接口统一到上面的命名规则：约 320 个接口改名（如 `stock_zh_a_hist` 改为 `stock_zh_a_hist_em`，`stock_zh_index_daily` 改为 `index_zh_daily_sina`），少数参数统一为 `symbol`、`date`、`start_date`、`end_date`，上游数据源已关闭的接口被移除。旧名称没有保留为别名，但调用时会提示去向：

```python
import akshare as ak

ak.stock_zh_a_hist(symbol="000001")
# AttributeError: stock_zh_a_hist 已在 1.20.46 更名为 stock_zh_a_hist_em，请改用 ak.stock_zh_a_hist_em；…

ak.renamed_info("stock_zh_a_hist")
# {'name': 'stock_zh_a_hist', 'status': 'renamed', 'new_name': 'stock_zh_a_hist_em', 'version': '1.20.46', 'url': '…'}
```

用旧名称调用 `ak.search` 时，现在的名称也排在第一位。完整的新旧名称对照见[更新日志](https://akshare.akfamily.xyz/changelog.html#changelog-rename)末尾的接口更名一览表。

## 特点

- **简单易用**：一行代码获取数据
- **便于扩展**：容易与其他程序结合，定制自己的代码
- **生态丰富**：依托 Python 的数据科学生态

## 教程

1. [项目概览](https://akshare.akfamily.xyz/introduction.html)
2. [安装指导](https://akshare.akfamily.xyz/installation.html)
3. [接口检索](https://akshare.akfamily.xyz/search.html)
4. [AI 助手（MCP）](https://akshare.akfamily.xyz/mcp.html)
5. [快速入门](https://akshare.akfamily.xyz/tutorial.html)
6. [数据字典](https://akshare.akfamily.xyz/data/index.html)
7. [量化指标](https://akshare.akfamily.xyz/indicator.html)
8. [常见问题](https://akshare.akfamily.xyz/faq.html)
9. [实盘交易](https://akshare.akfamily.xyz/trade.html)

## 参与贡献

[AKShare](https://github.com/akfamily/akshare) 仍在持续开发中，欢迎提交 issue 和 pull request：

- 报告或修复问题
- 提出需求或贡献新接口
- 撰写或修订文档
- 补充测试用例

提交 pull request 之前请先阅读[贡献指南](https://akshare.akfamily.xyz/contributing.html)。

> 说明：本项目使用 [Ruff](https://github.com/astral-sh/ruff) 格式化代码

## 声明

1. [AKShare](https://github.com/akfamily/akshare) 提供的数据仅供学术研究使用；
2. [AKShare](https://github.com/akfamily/akshare) 提供的数据仅供参考，不构成任何投资建议；
3. 基于 [AKShare](https://github.com/akfamily/akshare) 做研究的投资者应当注意数据风险；
4. [AKShare](https://github.com/akfamily/akshare) 将坚持提供开源的财经数据；
5. 受不可控因素影响，[AKShare](https://github.com/akfamily/akshare) 的部分数据接口可能被移除；
6. 请遵守 [AKShare](https://github.com/akfamily/akshare) 使用的开源协议；
7. 为其他编程语言和 AI 助手提供 HTTP API 与 MCP 服务：[AKTools](https://aktools.akfamily.xyz/)。

## 展示徽章

在项目的 README.md 中使用徽章：

```markdown
[![Data: akshare](https://img.shields.io/badge/Data%20Science-AKShare-green)](https://github.com/akfamily/akshare)
```

在 README.rst 中使用徽章：

```
.. image:: https://img.shields.io/badge/Data%20Science-AKShare-green
    :target: https://github.com/akfamily/akshare
```

显示效果：

[![Data: akshare](https://img.shields.io/badge/Data%20Science-AKShare-green)](https://github.com/akfamily/akshare)

## 引用

在论文或出版物中引用本项目时，请使用下面的 **bibtex**：

```markdown
@misc{akshare,
    author = {Albert King and Yaojie Zhang},
    title = {AKShare},
    year = {2022},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/akfamily/akshare}},
}
```

## 致谢

特别感谢 [FuShare](https://github.com/LowinLi/fushare) 项目提供的学习机会；

特别感谢 [TuShare](https://github.com/waditu/tushare) 项目提供的学习机会；

感谢 [东方财富网站](http://data.eastmoney.com) 提供的数据；

感谢 [新浪财经网站](https://finance.sina.com.cn) 提供的数据；

感谢 [金十数据网站](https://www.jin10.com/) 提供的数据；

感谢 [生意社网站](http://www.100ppi.com/) 提供的数据；

感谢 [中国银行间市场交易商协会网站](http://www.nafmii.org.cn/) 提供的数据；

感谢 [99期货网站](http://www.99qh.com/) 提供的数据；

感谢 [中国外汇交易中心暨全国银行间同业拆借中心网站](http://www.chinamoney.com.cn/chinese/) 提供的数据；

感谢 [和讯财经网站](http://www.hexun.com/) 提供的数据；

感谢 [DACHENG-XIU 网站](https://dachxiu.chicagobooth.edu/) 提供的数据；

感谢 [上海证券交易所网站](http://www.sse.com.cn/assortment/options/price/) 提供的数据；

感谢 [深圳证券交易所网站](http://www.szse.cn/) 提供的数据；

感谢 [北京证券交易所网站](http://www.bse.cn/) 提供的数据；

感谢 [中国金融期货交易所网站](http://www.cffex.com.cn/) 提供的数据；

感谢 [上海期货交易所网站](http://www.shfe.com.cn/) 提供的数据；

感谢 [大连商品交易所网站](http://www.dce.com.cn/) 提供的数据；

感谢 [郑州商品交易所网站](http://www.czce.com.cn/) 提供的数据；

感谢 [上海国际能源交易中心网站](http://www.ine.com.cn/) 提供的数据；

感谢 [Timeanddate 网站](https://www.timeanddate.com/) 提供的数据；

感谢 [河北省空气质量预报信息发布系统网站](http://218.11.10.130:8080/) 提供的数据；

感谢 [Economic Policy Uncertainty 网站](https://www.policyuncertainty.com/) 提供的数据；

感谢 申万指数网站 提供的数据；

感谢 [真气网网站](https://www.zq12369.com/) 提供的数据；

感谢 [财富网站](http://www.fortunechina.com/) 提供的数据；

感谢 [中国证券投资基金业协会网站](http://gs.amac.org.cn/) 提供的数据；

感谢 [Expatistan 网站](https://www.expatistan.com/cost-of-living) 提供的数据；

感谢 [北京市碳排放权电子交易平台网站](https://www.bjets.com.cn/article/jyxx/) 提供的数据；

感谢 [国家金融与发展实验室网站](http://www.nifd.cn/) 提供的数据；

感谢 [义乌小商品指数网站](https://www.ywindex.com/) 提供的数据；

感谢 [百度迁徙网站](https://qianxi.baidu.com/?from=shoubai#city=0) 提供的数据；

感谢 [思知网站](https://www.ownthink.com/) 提供的数据；

感谢 [新加坡交易所网站](https://www.sgx.com/zh-hans/research-education/derivatives) 提供的数据。
