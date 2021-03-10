# [AKShare](https://github.com/jindaxiang/akshare) 答疑专栏

## 专栏介绍

本专栏的主要目的是为了解决在使用 [AkShare](https://github.com/jindaxiang/akshare) 中遇到的各种问题，主题包括但不限于：环境配置、AkShare 安装和升级、数据接口请求、代理配置等等。

## 常见问题

1. 安装 AkShare 的速度慢，下载时间久

   1. 请使用国内的源来安装 AkShare
      1. 基于 Python 的代码如下：
```pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade ```
      2. 基于 Anaconda 的代码如下：
```pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --user  --upgrade```
   2. 使用代理安装，由于相关限制，在这里对代理的安装和使用不做介绍，请自行搜索配置。

2. 运行任意接口发现报错，错误类似：`AttributeError: module 'akshare' has no attribute 'xxx'`

   1. 检查 Python 的版本需要在 Python 3.6 以上，推荐使用 Python 3.7.5 及以上版本
   2. 检查是否安装了最新版本的 AkShare，如果不是最新版本，请先升级至最新版
   3. 检查在文档中是否具有该 `xxx` 接口，特定情况下有可能会改变接口的命名或者移除某些接口
   4. 检查所运行的 Python 文件名命名问题，不能用如下命名：`akshare.py` 与本地安装包冲突

3. 不能获取指定的日期期间的数据，比如从 20200401 至 20200415 的数据

   1. 由于目标网页的大部分的接口一次性返回所有数据，所以在 AkShare 的部分接口函数中没有设置类似 `start_date` 和 `end_date` 的参数
   2. 如果要获取指定日期间的数据，请在调用接口后自行处理

4. 接口报错出现类似错误提示： `ReadTimeout: HTTPConnectionPool(host="www.xxx.com")` 

   1. 重新运行接口函数
   2. 更换 IP 地址，可以使用代理访问
   3. 降低数据访问的频率

5. 接口报错出现类似错误提示：`cannot import name 'StringIO' from 'pandas.compat'`

   1. 建议安装 pandas 版本大于 **0.25.2**，建议 pandas 版本大于 **1.0**
   2. 升级命令如下: `pip install akshare --upgrade`

6. 出现数据返回错位，如日期数据和价格数据返回错位的情况

   1. 多运行几次，是否是网络稳定问题
   2. 切换 IP 后重试
   3. 可以在 [GitHub Issues](https://github.com/jindaxiang/akshare/issues) 中反馈

7. 全球疫情历史数据接口获取不到数据
    
   1. 由于 GitHub 服务器在国外，访问此数据接口最好使用代理访问
   2. 如没有代理的情况下，多重复请求几次
   
8. 返回值字段错位
    
   1. 升级 pandas 到最新版本

9. Linux 系统显示 `execjs._exceptions.RuntimeUnavailableError: Could not find an available JavaScript runtime.`

    1. 需要安装 `nodejs`
    2. 参考[文章](https://blog.csdn.net/qq_36853469/article/details/106401389)

10. 将数据在 IDE 全显示，避免折叠显示不全的情况

    1. 全局设置 `pandas`，使用方法: 
    
```python
import pandas as pd
import akshare as ak
# 列名与数据对其显示
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sz399552")
print(stock_zh_index_daily_df)
```

11. 出现 `AttributeError: 'MiniRacer' object has no attribute 'ext'` 报错
    1. 安装 64 位的 Python
    
12. 无法下载疫情的海外数据
    1. 访问 [IPAddress](https://www.ipaddress.com/)
    2. 查询 ```raw.githubusercontent.com``` 的真实 IP 地址
    3. 找到系统 host
        1. Windows 10 在目录 ```C:\Windows\System32\drivers\etc```
        2. Ubuntu 18.04 在目录 ```/etc/hosts```
    4. 修改 host
        1. 添加如下内容: ```199.232.28.133 raw.githubusercontent.com```
        2. 此处 ```199.232.28.133``` 为查找到的真实 IP