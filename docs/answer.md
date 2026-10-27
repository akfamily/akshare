# [AKShare](https://github.com/akfamily/akshare) 答疑专栏

## 专栏介绍

本专栏的主要目的是为了解决在使用 [AKShare](https://github.com/akfamily/akshare) 中遇到的各种问题，主题包括但不限于：环境配置、AKShare 安装和升级、数据接口请求、代理配置等等。

## 常见问题

1. 安装 AKShare 的速度慢，下载时间久

    1. 请使用国内的源来安装 AKShare
        1. 基于 pip 的代码如下：`pip install akshare --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple`
        2. 基于 uv 的代码如下：`uv pip install akshare --upgrade --default-index https://pypi.tuna.tsinghua.edu.cn/simple`
    2. 使用代理安装，由于相关限制，在这里对代理的安装和使用不做介绍，请自行搜索配置。

2. 运行任意接口发现报错，错误类似：`AttributeError: module 'akshare' has no attribute 'xxx'`

    1. 检查 Python 的版本需要在 Python 3.11 及以上，推荐使用 Python 3.13.x 及以上版本
    2. 检查是否安装了最新版本的 AKShare，如果不是最新版本，请先升级至最新版
    3. 检查在文档中是否具有该 `xxx` 接口，特定情况下有可能会改变接口的命名或者移除某些接口
    4. 检查所运行的 Python 文件名命名问题，不能用如下命名：`akshare.py` 与本地安装包冲突

3. 不能获取指定的日期期间的数据，比如从 20200401 至 20200415 的数据

    1. 由于目标网页的大部分的接口一次性返回所有数据，所以在 AKShare 的部分接口函数中没有设置类似 `start_date` 和 `end_date` 的参数
    2. 如果要获取指定日期间的数据，请在调用接口后自行处理

4. 接口报错出现类似错误提示：`ReadTimeout: HTTPConnectionPool(host="www.xxx.com")`

    1. 重新运行接口函数
    2. 更换 IP 地址，可以使用代理访问
    3. 降低数据访问的频率

5. 出现数据返回错位，如日期数据和价格数据返回错位的情况

    1. 多运行几次，查看是否是网络不稳定造成的问题
    2. 切换 IP 后重试
    3. 可以在 [GitHub Issues](https://github.com/akfamily/akshare/issues) 中反馈

6. 返回值字段错位

    1. 升级 pandas 到最新版本

7. 将数据在 IDE 全显示，避免折叠显示不全的情况

    1. 全局设置 `pandas`，使用方法：

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

8. 出现 `AttributeError: 'MiniRacer' object has no attribute 'ext'` 报错

    1. 安装 64 位版本的 Python

9. 使用代理的时候报错 `check_hostname requires server_hostname`

    1. 检查代理地址的协议：大多数本地代理软件提供的是 HTTP 代理，`https` 一项也应写成 `http://` 开头，例如 `{"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}`
    2. 不要通过降低 urllib3 版本来规避，旧版本存在已知安全漏洞

10. 大连商品交易所相关接口报错或返回空数据

    1. 原因：大连商品交易所网站目前启用了瑞数反爬虫验证，程序发出的请求会被拒绝并返回 HTTP 412，这不是 AKShare 或本地环境的问题，暂时没有可用的解决办法
    2. 只有 futures_warehouse_receipt_dce 会明确抛出带 412 状态码的 `APIError`，其他接口的报错各不相同，常见的有 `JSONDecodeError: Expecting value`、`BadZipFile: File is not a zip file`、`ValueError: No tables found`、`IndexError: list index out of range`，也有接口不报错而是返回空数据
    3. 受影响的接口：futures_contract_info_dce、futures_dce_position_rank、futures_dce_position_rank_other、futures_delivery_dce、futures_delivery_match_dce、futures_to_spot_dce、futures_warehouse_receipt_dce、get_dce_daily、get_dce_rank_table、option_hist_dce、get_receipt、get_roll_yield、get_roll_yield_bar；get_futures_daily、get_rank_sum、get_rank_sum_daily 中涉及大连商品交易所的部分同样无法获取
    4. 其他交易所的接口不受影响
