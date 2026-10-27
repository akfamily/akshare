# 常见问题

本页汇总使用 AKShare 时常见的问题及解决办法，涉及安装、接口报错、数据与显示等。没有找到答案时，请在 [GitHub Issues](https://github.com/akfamily/akshare/issues) 中反馈，并附上 AKShare 版本号（`ak.__version__`）、完整的报错信息和调用代码。

## 安装与环境

### 安装速度慢，下载时间久

使用国内镜像源安装：

```
pip install akshare --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple
uv pip install akshare --upgrade --default-index https://pypi.tuna.tsinghua.edu.cn/simple
```

也可以通过代理安装，代理的配置方法请自行搜索。

### MiniRacer 报错缺少 ext 属性

报错信息：`AttributeError: 'MiniRacer' object has no attribute 'ext'`

请安装 64 位版本的 Python。

## 接口调用报错

### 提示 akshare 没有某个接口

报错信息：`AttributeError: module 'akshare' has no attribute 'xxx'`

1. 检查 Python 版本，需要 Python 3.11 及以上，推荐 Python 3.13
2. 检查是否安装了最新版本的 AKShare，如果不是请先升级
3. 在文档中确认该 `xxx` 接口是否存在，接口有可能改名或被移除，见[更新日志](changelog.md)
4. 检查运行的 Python 文件名，不能命名为 `akshare.py`，否则会与安装的 AKShare 冲突

### 请求超时

报错信息：`ReadTimeout: HTTPConnectionPool(host="www.xxx.com")`

1. 重新运行接口函数
2. 更换 IP 地址，可以使用代理访问
3. 降低数据访问的频率

### 使用代理时报错

报错信息：`check_hostname requires server_hostname`

1. 检查代理地址的协议：大多数本地代理软件提供的是 HTTP 代理，`https` 一项也应写成 `http://` 开头，例如 `{"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}`
2. 不要通过降低 urllib3 版本来规避，旧版本存在已知安全漏洞

### 升级到 1.20.0 后找不到模块

报错信息：`ModuleNotFoundError: No module named 'akshare.xxx'`

1.20.0 重新整理了模块路径。请改用 `ak.接口名()` 调用，或按 [1.20.0 模块路径迁移](migration.md) 中的对照表修改导入语句。

(faq-dce)=
### 大连商品交易所相关接口报错或返回空数据

1. 原因：大连商品交易所网站目前启用了瑞数反爬虫验证，程序发出的请求会被拒绝并返回 HTTP 412，这不是 AKShare 或本地环境的问题，暂时没有可用的解决办法
2. 只有 futures_warehouse_receipt_dce 会明确抛出带 412 状态码的 `APIError`，其他接口的报错各不相同，常见的有 `JSONDecodeError: Expecting value`、`BadZipFile: File is not a zip file`、`ValueError: No tables found`、`IndexError: list index out of range`，也有接口不报错而是返回空数据
3. 受影响的接口：futures_contract_info_dce、futures_dce_position_rank、futures_dce_position_rank_other、futures_delivery_dce、futures_delivery_match_dce、futures_to_spot_dce、futures_warehouse_receipt_dce、get_dce_daily、get_dce_rank_table、option_hist_dce、get_receipt、get_roll_yield、get_roll_yield_bar；get_futures_daily、get_rank_sum、get_rank_sum_daily 中涉及大连商品交易所的部分同样无法获取
4. 其他交易所的接口不受影响

## 数据与显示

### 无法获取指定日期区间的数据

大部分数据源一次性返回全部数据，所以 AKShare 的部分接口没有 `start_date`、`end_date` 这类参数。需要指定日期区间时，请在调用接口后用 pandas 自行筛选。

### 返回数据错位，如日期和价格错位

1. 多运行几次，确认是否由网络不稳定造成
2. 切换 IP 后重试
3. 升级 pandas 到最新版本
4. 仍有问题请在 [GitHub Issues](https://github.com/akfamily/akshare/issues) 中反馈

### 在 IDE 中显示全部行和列，中文列名对齐

全局设置 pandas 的显示选项：

```python
import pandas as pd
import akshare as ak
# 列名与数据对齐显示
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sz399552")
print(stock_zh_index_daily_df)
```

(known-data-issues)=
## 已知数据问题

以下记录数据源本身存在的异常，使用相关数据时请注意。

### stock_zh_a_hist 后复权价格出现负值

问题描述：股票 `600734` 后复权数据的开高低收字段出现负值

代码复现：

```python
import akshare as ak

stock_zh_a_hist_df = ak.stock_zh_a_hist(
    symbol="600734",
    period="daily",
    start_date="20050501",
    end_date="20050520",
    adjust="hfq"
)
print(stock_zh_a_hist_df)
```

结果复现：

```
      日期    开盘    收盘    最高    最低  ...  成交额     振幅    涨跌幅   涨跌额   换手率
0  2005-05-09 -0.13 -0.53  0.00 -0.53  ...  1571616.0   407.69 -507.69 -0.66  0.60
1  2005-05-10 -0.53 -0.50 -0.36 -0.79  ...  1150869.0   -81.13    5.66  0.03  0.45
2  2005-05-11 -0.50 -0.30 -0.20 -0.69  ...  1651719.0   -98.00   40.00  0.20  0.63
3  2005-05-12 -0.33 -0.20  0.00 -0.43  ...  2175707.0  -143.33   33.33  0.10  0.81
4  2005-05-13 -0.33 -0.13  0.07 -0.40  ...  1569427.0  -235.00   35.00  0.07  0.58
5  2005-05-16 -0.30 -0.10  0.10 -0.40  ...  2324469.0  -384.62   23.08  0.03  0.85
6  2005-05-17 -0.10  0.04  0.13 -0.23  ...  2682900.0  -360.00  140.00  0.14  0.96
7  2005-05-18  0.00  0.20  0.27 -0.13  ...  2261494.0  1000.00  400.00  0.16  0.81
8  2005-05-19  0.10  0.07  0.17 -0.06  ...  1589463.0   115.00  -65.00 -0.13  0.57
9  2005-05-20  0.07  0.00  0.13 -0.03  ...  1355000.0   228.57 -100.00 -0.07  0.48
[10 rows x 11 columns]
```
