# 快速入门

本页用几分钟带你完成第一次数据获取：安装 AKShare、调用一个接口、找到自己需要的接口，以及接口报错时怎么处理。

## 安装

AKShare 支持 Python 3.11 及以上版本，推荐 Python 3.13。在命令行中运行：

```
pip install akshare --upgrade
```

推荐使用 uv 创建独立的虚拟环境后再安装，详见 [AKShare uv 环境配置](uv.md)；其他安装方式见 [AKShare 安装指导](installation.md)。

```{tip}
数据源网站经常改版，AKShare 会随之修复接口。遇到接口报错时，请先升级到最新版本再重试。
```

## 第一次调用

所有接口都通过 `ak.接口名()` 调用，返回 pandas DataFrame。下面获取平安银行（sz000001）的前复权日线行情：

```python
import akshare as ak

stock_df = ak.stock_zh_a_hist_tx(
    symbol="sz000001", start_date="20261020", end_date="20261027", adjust="qfq"
)
print(stock_df)
```

```
         date   open  close   high    low     volume  turnover        amount
0  2026-10-20  11.62  11.44  11.68  11.38  1245097.0    0.0064  1.429560e+09
1  2026-10-21  11.44  11.41  11.51  11.39   813541.0    0.0042  9.305468e+08
2  2026-10-22  11.41  11.30  11.42  11.26  1297649.0    0.0067  1.468425e+09
3  2026-10-23  11.27  11.20  11.35  11.17  1448806.0    0.0075  1.628277e+09
4  2026-10-26  11.15  11.30  11.34  11.13  1323113.0    0.0068  1.486000e+09
5  2026-10-27  11.27  11.47  11.55  11.24  1529292.0    0.0079  1.750404e+09
```

大多数接口返回中文列名。例如获取中国居民消费价格指数（CPI）：

```python
import akshare as ak

cpi_df = ak.macro_china_cpi()
print(cpi_df.head())
```

```
          月份  全国-当月  全国-同比增长  全国-环比增长  ...  农村-当月  农村-同比增长  农村-环比增长  农村-累计
0  2026年09月份  100.9      0.9      0.2  ...  100.8      0.8      0.4  100.7
1  2026年08月份  100.8      0.8      0.4  ...  100.7      0.7      0.4  100.7
2  2026年07月份  100.5      0.5     -0.1  ...  100.4      0.4     -0.2  100.7
3  2026年06月份  101.0      1.0     -0.3  ...  100.8      0.8     -0.3  100.8
4  2026年05月份  101.2      1.2     -0.1  ...  101.1      1.1     -0.1  100.8

[5 rows x 13 columns]
```

返回结果是普通的 DataFrame，可以直接用 pandas 处理，例如 `stock_df.to_csv("stock.csv", index=False)` 保存为 CSV 文件。各接口的参数、输出列及单位见 [AKShare 数据字典](data/index.rst)。

## 查找接口

AKShare 提供 1000 余个数据接口。如果还不确定该调用哪个接口，可以先用内置的接口检索按关键词查找：

```python
import akshare as ak

# 按关键词检索接口
print(ak.search("可转债 实时行情", limit=5))

# 查看单个接口的输入参数、输出字段与调用示例
print(ak.interface_info("bond_zh_hs_cov_min"))

# 列出全部类目，可用于缩小检索范围
print(ak.list_categories())
```

检索完全在本地进行，不发起网络请求。传入完整接口名时，该接口一定排在第一位，因此也适合用来确认一个记不全的接口名。需要注意这是关键词匹配而非语义检索，详见 [AKShare 接口检索](search.md)。

也可以直接浏览 [AKShare 数据字典](data/index.rst)，它按股票、期货、基金、宏观等类目列出了全部接口。

## 接口报错怎么办

AKShare 从各网站实时采集数据，接口报错大多与数据源有关，可以按下面的顺序排查：

1. 升级到最新版本：`pip install akshare --upgrade`
2. 出现超时或连接被断开时，稍后重试并降低访问频率；数据源对频繁访问会限流或断开连接
3. 在 [AKShare 常见问题](faq.md) 中查找相同的报错
4. 仍无法解决时，在 [GitHub Issues](https://github.com/akfamily/akshare/issues) 中反馈，并附上 AKShare 版本号（`ak.__version__`）、完整的报错信息和调用代码

## 下一步

- [AKShare 数据字典](data/index.rst)：全部接口的详细说明
- [AKShare 策略回测](backtest.md)：结合 AKQuant、Backtrader 等框架的回测案例
- [AKShare HTTP API（AKTools）](aktools.md)：在 Python 以外的语言中使用 AKShare
