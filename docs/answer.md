# [AkShare](https://github.com/jindaxiang/akshare) 答疑专栏

## 专栏介绍

本专栏的主要目的是为了解决在使用 [AkShare](https://github.com/jindaxiang/akshare) 中遇到的各种问题，主题包括但不限于：环境配置、AkShare 安装和升级、数据接口请求、代理配置等等。

## 常见问题

1. 安装 AkShare 的速度慢，下载时间久

   1. 请使用国内的源来安装 AkShare
      1. 基于纯 Python 的代码如下：`pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade `
      2. 基于 Anaconda 的代码如下：`pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --user  --upgrade`

   2. 使用代理安装，由于相关限制，在这里对代理的安装和使用不做介绍，请自行搜索配置。

2. 运行任意接口发现报错，错误类似：`AttributeError: module 'akshare' has no attribute 'xxx'`

   1. 检查 Python 的版本需要在 Python 3.6 以上，推荐使用 Python 3.7.5 及以上版本
   2. 检查是否安装了最新版本的 AkShare，如果不是最新版本，请先升级至最新版
   3. 检查在文档中是否具有该 `xxx` 接口，特定情况下有可能会改变接口的命名或者移除某些接口
   4. 检查所运行的 Python 文件名命名问题，不能用如下命名：`akshare.py` 与本地安装包冲突

3. 不能获取指定的日期期间的数据，比如从 20200401 至 20200415 的数据

   1. 由于目标网页的大部分的接口一次性返回所有数据，所以在 AkShare 的部分接口函数中没有设置类似 `start_date` 和 `end_date` 的参数
   2. 如果要获取指定日期间的数据，请在调用接口后自行处理

4. 接口出现类似： `ReadTimeout: HTTPConnectionPool(host="www.xxx.com")` 

   1. 重试运行接口
   2. 更换 IP 地址，可以试用代理访问
   3. 降低数据访问的频率