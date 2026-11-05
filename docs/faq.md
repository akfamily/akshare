# 常见问题

本页汇总使用 AKShare 时常见的问题及解决办法，分为安装与环境、接口调用报错、网络与代理、数据与显示四类，最后记录数据源本身已知的异常。

没有找到答案时，请在 [GitHub Issues](https://github.com/akfamily/akshare/issues) 中反馈，并附上：

- AKShare 版本号（`ak.__version__`）、Python 版本和操作系统
- 完整的报错信息
- 能复现问题的调用代码

## 安装与环境

### 安装速度慢，下载时间久

使用国内镜像源安装：

```
pip install akshare --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple
uv pip install akshare --upgrade --default-index https://pypi.tuna.tsinghua.edu.cn/simple
```

镜像源与官方源之间有同步延迟，刚发布的版本可能要过一段时间才能从镜像装到。急需最新版本时，可以改用官方源，或通过代理安装：

```
pip install akshare --upgrade --proxy http://127.0.0.1:7890
```

### 安装 mini-racer 失败

安装 AKShare 时，依赖包 mini-racer 下载或构建失败，提示找不到合适的版本或无法从源码构建。

mini-racer 用于执行数据源的 JavaScript 解密代码，只为以下环境提供安装包：

- 64 位的 Windows、macOS
- 64 位的 Linux，且 glibc 不低于 2.27，如 Ubuntu 18.04、Debian 10、CentOS 8 及更新的版本

请按以下步骤检查：

1. 确认安装的是 64 位 Python。可运行 `python -c "import struct; print(struct.calcsize('P') * 8)"`，输出 `64` 即为 64 位
2. Linux 上运行 `ldd --version` 查看 glibc 版本。CentOS 7 等 glibc 低于 2.27 的系统无法安装，请升级系统，或继续使用 1.20.24

(faq-mini-racer)=
### MiniRacer 报错 function 'mr_init_v8' not found

报错信息：

- `AttributeError: function 'mr_init_v8' not found`
- `AttributeError: module 'py_mini_racer' has no attribute 'MiniRacer'`
- `AttributeError: 'NoneType' object has no attribute 'mr_free_context'`

巨潮、同花顺、新浪等依赖 JavaScript 解密的接口都会出现这类报错，原因不在接口本身，而是 `site-packages/py_mini_racer` 目录里混入了其他包的文件。

1.20.25 起，AKShare 在所有平台改用 mini-racer。它与旧包 py-mini-racer、akracer 使用同一个导入名 `py_mini_racer`，安装在同一个目录，混装时文件会互相覆盖或被误删；而升级 AKShare 时，pip 不会卸载不再依赖的旧包。例如 Windows 上 mini-racer 的代码加载了 py-mini-racer 0.6.0 留下的 `mini_racer.dll`，就会报 `mr_init_v8` 找不到。

解决办法：

1. 关闭所有正在运行的 Python 和 Jupyter，已经运行的进程会继续使用旧文件
2. 卸载三个包后重新安装 mini-racer：

   ```
   pip uninstall -y py-mini-racer akracer mini-racer
   pip install --no-cache-dir "mini-racer>=0.13.0"
   ```

   三个包要一起卸载：只卸载 py-mini-racer 会把共用的文件一并删掉，mini-racer 也会随之损坏。未安装的包会提示跳过，不影响执行。

3. 运行下面的代码验证，输出 `2` 即恢复正常：

   ```python
   import py_mini_racer

   print(py_mini_racer.MiniRacer().eval("1 + 1"))
   ```

如果仍然报错，请在 [GitHub Issues](https://github.com/akfamily/akshare/issues) 中附上 `pip show -f mini-racer` 的输出，以及 `pip list` 中与 racer 相关的几行（Windows 用 `pip list | findstr /i racer`，Linux、macOS 用 `pip list | grep -i racer`）。

## 接口调用报错

### 提示 akshare 没有某个接口

报错信息：`AttributeError: module 'akshare' has no attribute 'xxx'`

1. 检查 Python 版本，需要 Python 3.11 及以上，推荐 Python 3.13
2. 检查是否安装了最新版本的 AKShare，如果不是请先升级
3. 在文档中确认该接口是否存在。接口可能已改名或被移除，见[更新日志](changelog.md)及文末的接口更名一览表
4. 检查运行的 Python 文件名，不能命名为 `akshare.py`，否则会与安装的 AKShare 冲突

### 升级到 1.20.0 后找不到模块

报错信息：`ModuleNotFoundError: No module named 'akshare.xxx'`

1.20.0 重新整理了模块路径。请改用 `ak.接口名()` 调用，或按 [1.20.0 模块路径迁移](migration.md) 中的对照表修改导入语句。

(faq-dce)=
### 大连商品交易所相关接口报错或返回空数据

大连商品交易所网站目前启用了瑞数反爬虫验证，程序发出的请求会被拒绝并返回 HTTP 412。这不是 AKShare 或本地环境的问题，暂时没有可用的解决办法；其他交易所的接口不受影响。

自 1.20.31 起，这些接口在被拒绝时统一抛出 `DceBlockedError`（`APIError` 的子类，`status_code` 为 412），报错信息会说明原因。更早的版本报错各不相同，常见的有 `JSONDecodeError: Expecting value`、`BadZipFile: File is not a zip file`、`ValueError: No tables found`、`IndexError: list index out of range`，也有接口不报错而返回空数据，升级到最新版即可看到明确的报错。大商所解除限制后，这些接口无需修改即可恢复。

大商所合约的成交持仓排名可以改用新浪财经的数据，按单个合约查询，合约需未到期，如：

```python
import akshare as ak

ak.futures_hold_pos_sina(symbol="多单持仓", contract="M2701", date="20261104")
```

受影响的接口：

- 期货：futures_contract_info_dce、futures_dce_position_rank、futures_dce_position_rank_other、futures_delivery_dce、futures_delivery_match_dce、futures_to_spot_dce、futures_warehouse_receipt_dce、get_dce_daily、get_dce_rank_table、get_receipt、get_roll_yield、get_roll_yield_bar
- 期权：option_hist_dce
- 部分受影响：get_futures_daily、get_rank_sum、get_rank_sum_daily 中涉及大连商品交易所的部分

## 网络与代理

### 请求超时

报错信息：`ConnectTimeout` 或 `ReadTimeout: HTTPConnectionPool(host="www.xxx.com")`

所有接口默认连接超时 10 秒、读取超时 60 秒，上游长时间无响应时会抛出上述异常，不会无限等待。读取超时指两次收到数据之间的最长间隔，持续传输的大文件不受影响。

1. 重新运行接口函数
2. 降低数据访问的频率
3. 更换 IP 地址，或使用代理访问
4. 网络较慢时调大超时，见下文“设置代理与超时”

(faq-proxy)=
### 设置代理与超时

代理与超时是全局设置，对全部接口生效，运行中修改立即生效：

```python
import akshare as ak

ak.set_proxies({"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
ak.set_timeout(30)  # 单位为秒；也可传 (连接超时, 读取超时)，如 (10, 120)
ak.set_timeout(None)  # 不限时

with ak.ProxyContext({"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}):
    stock_zh_a_daily_df = ak.stock_zh_a_daily(symbol="sh600000")  # 仅此代码块内使用该代理
```

- 未调用 `ak.set_proxies` 时，沿用 `HTTP_PROXY`、`HTTPS_PROXY` 环境变量和系统代理设置
- `ak.get_proxies()`、`ak.get_timeout()` 返回当前设置
- `stock_news_em`、百度股市通系列、国家统计局系列等少数需要模拟浏览器指纹的接口经 curl_cffi 发送请求，它把 `(连接超时, 读取超时)` 两项之和当作整个请求的总时长上限，默认为 70 秒

### 使用代理时报错

报错信息：`check_hostname requires server_hostname`

1. 检查代理地址的协议。大多数本地代理软件提供的是 HTTP 代理，`https` 一项也应写成 `http://` 开头，如 `{"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}`
2. 不要通过降低 urllib3 版本来规避，旧版本存在已知安全漏洞

(faq-eastmoney-ratelimit)=
### 东方财富行情接口报 RemoteDisconnected 或限流

报错信息：`Push2RateLimitError: 东方财富 push2 行情服务器断开了连接……`；旧版本报 `ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))`

东方财富 push2 行情服务器在短时间内收到较多请求时，会临时拒绝来自该 IP 的连接。实时行情、历史 K 线、板块、资金流等接口都使用这类服务器，需要翻页的接口最容易触发，如 stock_zh_a_spot_em 一次调用要请求约 60 页。

1. 首次限流一般约 5 分钟后恢复；恢复后如果马上又大量请求，会更快再次被限流，恢复时间也更长，实测超过 15 分钟仍未恢复
2. 等待期间不要重复调用东方财富的行情接口，否则会延长限流。东方财富数据中心、基金、F10 财务报表等接口使用其他服务器，实测不受影响
3. 识别到限流后，AKShare 会立即报错，不再自动重试。该异常同时是 `ak.RateLimitError` 与 `requests.ConnectionError` 的子类，可以用 `except ak.RateLimitError` 单独捕获

## 数据与显示

### 无法获取指定日期区间的数据

大部分数据源一次性返回全部数据，所以 AKShare 的部分接口没有 `start_date`、`end_date` 这类参数。需要指定日期区间时，请在调用接口后用 pandas 筛选：

```python
import akshare as ak
import pandas as pd

stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sh000300")
stock_zh_index_daily_df["date"] = pd.to_datetime(stock_zh_index_daily_df["date"])
result_df = stock_zh_index_daily_df[
    (stock_zh_index_daily_df["date"] >= "2024-01-01")
    & (stock_zh_index_daily_df["date"] <= "2024-03-31")
]
print(result_df)
```

### 在 IDE 中显示全部行和列，中文列名对齐

全局设置 pandas 的显示选项：

```python
import akshare as ak
import pandas as pd

# 列名与数据对齐显示
pd.set_option("display.unicode.ambiguous_as_wide", True)
pd.set_option("display.unicode.east_asian_width", True)
# 显示所有列
pd.set_option("display.max_columns", None)
# 显示所有行
pd.set_option("display.max_rows", None)

stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sz399552")
print(stock_zh_index_daily_df)
```

(known-data-issues)=
## 已知数据问题

以下记录数据源本身存在的异常，使用相关数据时请注意。

### stock_zh_a_hist 后复权价格出现负值

问题描述：股票 `600734` 后复权数据的开高低收字段出现负值。

代码复现：

```python
import akshare as ak

stock_zh_a_hist_df = ak.stock_zh_a_hist(
    symbol="600734",
    period="daily",
    start_date="20050501",
    end_date="20050520",
    adjust="hfq",
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
