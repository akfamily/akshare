# Pandas 概览

**Pandas** 是 [Python](https://www.python.org/) 的核心数据分析支持库，提供了快速、灵活、明确的数据结构，旨在简单、直观地处理关系型、标记型数据。Pandas 的目标是成为 Python 数据分析实践与实战的必备高级工具，其长远目标是成为**最强大、最灵活、可以支持任何语言的开源数据分析工具**。经过多年不懈的努力，Pandas 离这个目标已经越来越近了。

Pandas 适用于处理以下类型的数据：

* 与 SQL 或 Excel 表类似的，含异构列的表格数据;
* 有序和无序（非固定频率）的时间序列数据;
* 带行列标签的矩阵数据，包括同构或异构型数据;
* 任意其它形式的观测、统计数据集, 数据转入 Pandas 数据结构时不必事先标记。

Pandas 的主要数据结构是 [Series](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series)（一维数据）与 [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)（二维数据），这两种数据结构足以处理金融、统计、社会科学、工程等领域里的大多数典型用例。对于 R 用户，DataFrame 提供了比 R 语言 data.frame 更丰富的功能。Pandas 基于 [NumPy](https://www.numpy.org/) 开发，可以与其它第三方科学计算支持库完美集成。

Pandas 就像一把万能瑞士军刀，下面仅列出了它的部分优势 ：

* 处理浮点与非浮点数据里的**缺失数据**，表示为 `NaN`；
* 大小可变：**插入或删除** DataFrame 等多维对象的列；
* 自动、显式**数据对齐**：显式地将对象与一组标签对齐，也可以忽略标签，在 Series、DataFrame 计算时自动与数据对齐；
* 强大、灵活的**分组（group by）**功能：**拆分-应用-组合**数据集，聚合、转换数据；
* 把 Python 和 NumPy 数据结构里不规则、不同索引的数据**轻松**地转换为 DataFrame 对象；
* 基于智能标签，对大型数据集进行**切片**、**花式索引**、**子集分解**等操作；
* 直观地**合并（merge）**、**连接（join）**数据集；
* 灵活地**重塑（reshape）**、**透视（pivot）**数据集；
*  **轴**支持结构化标签：一个刻度支持多个标签；
* 成熟的 IO 工具：读取**文本文件**（CSV 等支持分隔符的文件）、Excel 文件、数据库等来源的数据，利用超快的 **HDF5** 格式保存 / 加载数据；
* **时间序列**：支持日期范围生成、频率转换、移动窗口统计、移动窗口线性回归、日期位移等时间序列功能。

这些功能主要是为了解决其它编程语言、科研环境的痛点。处理数据一般分为几个阶段：数据整理与清洗、数据分析与建模、数据可视化与制表，Pandas 是处理数据的理想工具。

其它说明：

* Pandas 速度**很快**。Pandas 的很多底层算法都用 [Cython](https://cython.org/) 优化过。然而，为了保持通用性，必然要牺牲一些性能，如果专注某一功能，完全可以开发出比 Pandas 更快的专用工具。
* Pandas 是 [statsmodels](https://www.statsmodels.org/stable/index.html) 的依赖项，因此，Pandas 也是 Python 中统计计算生态系统的重要组成部分。
* Pandas 已广泛应用于金融领域。

## 数据结构

| 维数 | 名称      | 描述                               |
| ---- | --------- | ---------------------------------- |
| 1    | Series    | 带标签的一维同构数组               |
| 2    | DataFrame | 带标签的，大小可变的，二维异构表格 |

### 为什么有多个数据结构？

Pandas 数据结构就像是低维数据的容器。比如，DataFrame 是 Series 的容器，Series 则是标量的容器。使用这种方式，可以在容器中以字典的形式插入或删除对象。

此外，通用 API 函数的默认操作要顾及时间序列与截面数据集的方向。多维数组存储二维或三维数据时，编写函数要注意数据集的方向，这对用户来说是一种负担；如果不考虑 C 或 Fortran 中连续性对性能的影响，一般情况下，不同的轴在程序里其实没有什么区别。Pandas 里，轴的概念主要是为了给数据赋予更直观的语义，即用“更恰当”的方式表示数据集的方向。这样做可以让用户编写数据转换函数时，少费点脑子。

处理 DataFrame 等表格数据时，**index**（行）或 **columns**（列）比 **axis 0** 和 **axis 1** 更直观。用这种方式迭代 DataFrame 的列，代码更易读易懂：

``` python
for col in df.columns:
    series = df[col]
    # do something with series
```

## 大小可变与数据复制

Pandas 所有数据结构的值都是可变的，但数据结构的大小并非都是可变的，比如，Series 的长度不可改变，但 DataFrame 里就可以插入列。

Pandas 里，绝大多数方法都不改变原始的输入数据，而是复制数据，生成新的对象。 一般来说，原始输入数据**不变**更稳妥。

## 获得支持

发现 Pandas 的问题或有任何建议，请反馈到 [Github 问题跟踪器](https://github.com/Pandas-dev/Pandas/issues)。日常应用问题请在 [Stack Overflow](https://stackoverflow.com/questions/tagged/Pandas) 上咨询 Pandas 社区专家。

## 社区

Pandas 如今由来自全球的同道中人组成的社区提供支持，社区里的每个人都贡献了宝贵的时间和精力，正因如此，才成就了开源 Pandas，在此，我们要感谢[所有贡献者](https://github.com/Pandas-dev/Pandas/graphs/contributors)。

若您有意为 Pandas 贡献自己的力量，请先阅读[贡献指南](https://Pandas.pydata.org/Pandas-docs/stable/development/contributing.html#contributing)。

Pandas 是 [NumFOCUS](https://www.numfocus.org/open-source-projects/) 赞助的项目。有了稳定的资金来源，就确保了 Pandas，这一世界级开源项目的成功，为本项目[捐款](https://Pandas.pydata.org/donate.html)也更有保障。

## 项目监管

自 2008 年以来，Pandas 沿用的监管流程已正式编纂为[项目监管文档](https://github.com/Pandas-dev/Pandas-governance)。这些文件阐明了如何决策，如何处理营利组织与非营利实体进行开源协作开发的关系等内容。

Wes McKinney 是仁慈的终身独裁者。

## 开发团队
核心团队成员列表及详细信息可在 Github 仓库的[人员页面](https://github.com/Pandas-dev/Pandas-governance/blob/master/people.md)上查询。

## 机构合作伙伴

现有机构合作伙伴信息可在 [Pandas 网站页面](https://pandas.pydata.org/)上查询。

## 许可协议

```
BSD 3-Clause License

Copyright (c) 2008-2012, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```