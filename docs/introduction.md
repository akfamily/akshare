# [AKShare](https://github.com/akfamily/akshare) 项目概览

本次发布 [AKTools](https://github.com/akfamily/aktools) 作为 AKShare 的 HTTP API 版本，突破 Python 语言的限制，欢迎各位小伙伴试用并提出更好的意见或建议！
点击 [AKTools](https://github.com/akfamily/aktools) 查看使用指南。

**风险提示**：[AKShare](https://github.com/akfamily/akshare) 开源财经数据接口库所采集的数据皆来自公开的数据源，不涉及任何个人隐私数据和非公开数据。
同时本项目提供的数据接口及相关数据仅用于学术研究，任何个人、机构及团体使用本项目的数据接口及相关数据请注意商业风险。

1. 本文档更新时间：**2026-02-04**；
2. 如有 [AKShare](https://github.com/akfamily/akshare) 库、文档及数据的相关问题，请在 [AKShare Issues](https://github.com/akfamily/akshare/issues) 中提 Issues；

## 引用

如果您想在文章或者项目中引用 [AKShare](https://github.com/akfamily/akshare/)，请使用如下 **bibtex** 格式：

```
@misc{akshare2022,
    author = {Albert King},
    title = {AKShare},
    year = {2022},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/akfamily/akshare}},
}
```

## [AKShare](https://github.com/akfamily/akshare) 的介绍

首先要特别感谢 [FuShare](https://github.com/LowinLi/fushare) 和 [TuShare](https://github.com/waditu/tushare) 在代码和项目开发上对本项目提供的借鉴和学习的机会!

[AKShare](https://github.com/akfamily/akshare) 是基于 Python 的财经数据接口库，目的是实现对股票、期货、期权、基金、外汇、债券、指数、加密货币等金融产品的基本面数据、实时和历史行情数据、衍生数据从数据采集、数据清洗到数据落地的一套工具，主要用于学术研究目的。

[AKShare](https://github.com/akfamily/akshare) 的特点是获取的是相对权威的财经数据网站公布的原始数据，通过利用原始数据进行各数据源之间的交叉验证，进而再加工，从而得出科学的结论。

**[AKShare](https://github.com/akfamily/akshare) 后续会基于学术论文和研究报告来添加更多数据接口和衍生指标，并提供相应的计算代码，敬请关注。**

## [AKShare](https://github.com/akfamily/akshare) 的特色

[AKShare](https://github.com/akfamily/akshare) 主要改进如下：

1. 代码语法符合 [PEP8](https://peps.python.org/pep-0008/) 规范，数据接口的命名统一；
2. 最佳支持 Python 3.12 及其以上版本；
3. 提供最佳的文档支持，每个数据接口均提供详细的说明和示例，只需要复制粘贴就可以下载数据；
4. 持续维护由于目标网页变化而导致的部分数据接口运行异常问题；
5. 持续更新财经数据接口，同时优化源代码；
6. 提供完善的接口文档，提高 [AKShare](https://github.com/akfamily/akshare) 的易用性；
7. 对于非 Python 用户，提供 HTTP API 接口工具 [AKTools](https://aktools.akfamily.xyz/)。

## [AKShare](https://github.com/akfamily/akshare) 的初衷

[AKShare](https://github.com/akfamily/akshare) 主要是用于财经研究，解决在财经研究中数据获取的问题。目前的版本主要是基于 Python
语言，通过调用相关的数据接口来获取数据到本地。原理上，就是在用户本地运行 Python
代码，实时从网络采集数据到本地，便利与数据分析。由于网络数据采集需要维护的接口众多，且经常由于目标网站变换网页格式需要维护及更新相关接口，所以用户在使用本项目的过程中需要经常更新本项目到最新版本。同时也需要关注项目文档的更新，因为最新的使用方式和接口变更都会第一时间更新到文档中。
