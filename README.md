# AkShare

AkShare 已经发布, 请访问[主页链接](https://github.com/jindaxiang/akshare)了解和查询数据接口！

AkShare 是实现对期货等衍生金融产品从数据采集, 数据清洗加工, 到数据下载的工具, 满足金融数据科学家, 数据科学爱好者在数据获取方面的需求. 它的特点是利用 AkShare 获取的是基于交易所公布的原始数据, 广大数据科学家可以利用原始数据进行再加工, 得出科学的结论.

**作者: Albert King**


<img src="https://jfds.nos-eastchina1.126.net/akshare/md_fold/images.jpg" width = 20% height = 10% align = center/>


# 安装方法
```
pip install akshare
```

# 升级方法
p.s. 由于目前版本更新迭代比较频繁, 请在使用前先升级库
```
pip install akshare --upgrade
```

# 版本更新说明
```
0.1.25
增加奇货可查指数接口 e.g. ak.get_qhkc_data("商品指数")

0.1.26
修复代码格式问题

0.1.27
修复说明格式问题

0.1.28
更新说明文档

0.1.29
规范说明文档格式

0.1.30
规范说明文档格式

0.1.31
规范 cot.py 函数说明

0.1.32
update basis.py

0.1.33
增加奇货可查数据三个接口:
get_qhkc_index, get_qhkc_index_trend, get_qhkc_index_profit_loss
使用方法请 help(get_qhkc_index) 查看

0.1.34
增加奇货可查-资金数据三个接口:
get_qhkc_fund_position_change, get_qhkc_fund_bs, get_qhkc_fund_position
使用方法请 help(get_qhkc_fund_position_change) 查看

0.1.35
增加奇货可查-工具-外盘比价接口:
get_qhkc_tool_foreign
使用方法请 help(get_qhkc_tool_foreign) 查看

0.1.36
增加奇货可查-工具-各地区经济数据接口:
get_qhkc_tool_gdp
使用方法请 help(get_qhkc_tool_gdp) 查看

0.1.37
增加中国银行间市场交易商协会-债券接口
get_bond_bank
使用方法请 help(get_bond_bank) 查看

0.1.38
修正小异常

0.1.39
模块化处理

0.1.40
统一接口函数参数 start --> start_day; end --> end_day

0.1.41
更新大连商品交易所-苯乙烯-EB品种

0.1.42
更新上海期货交易所-上海国际能源交易中心-20号胶-NR品种
更新上海期货交易所-不锈钢-SS品种

0.1.43
修改 example --> test.py 函数调用

0.1.44
修复 example --> daily_run.py 函数调用

0.1.45
修复 README.md 函数接口调用说明和感谢单位
```


# 目录
- [AkShare 库的特色](#AkShare库的特色)
- [AkShare 库的初衷](#AkShare库的初衷)
- [Quick-Start](#Quick-Start)
- [展期收益率](#展期收益率)
- [注册仓单](#注册仓单)
- [现货价格和基差](#现货价格和基差)
- [会员持仓排名](#会员持仓排名)
- [日线行情 K 线](#日线行情K线)
- [Anaconda安装说明及环境配置](#Anaconda安装说明及环境配置)
- [每日监控下载配置](#每日监控下载配置)
- [QQ 邮箱 SMTP 服务设置](#QQ邮箱SMTP服务设置)
- [特别说明](#特别说明)


## AkShare库的特色
AkShare 主要改进如下:
1. Python 语法更符合 PEP8 规范, 尤其在接口函数的命名上; 
2. 增加代码类型注释;
3. 支持 Python 3.7 以上版本的 Python;
4. 后续加入 asyncio 和 aiohttp 做异步爬虫加速(由于目前 aiohttp 尚未支持 Python 3.7);
5. 持续维护由于原网站格式变化导致的部分函数运行异常的问题;
6. 增加更多的网络数据采集接口:

    5.1 增加[奇货可查网站](https://qhkch.com/)数据接口, 目前已经提供奇货可查指数数据部分(已完成);
    
    5.2 增加主要国家股票市场指数数据接口(开发中);
    
7. 后续更新主要集中在增加更多数据接口部分, 同时修复源代码中 bug;
8. 更加完善的接口文档, 提高 [AkShare](https://github.com/jindaxiang/akshare) 的易用性;
9. 希望您能参与 AkShare 的维护与管理.


## AkShare库的初衷
由于 [FuShare](https://github.com/LowinLi/fushare) 库目前处于无人维护状态, 因此建立 [AkShare](https://github.com/jindaxiang/akshare) 库为用户提供持续数据支持.

传统的 CTA 策略以趋势为主, 但是自从 2017 年以来, 无论是长线还是短线的趋势策略都受制于商品波动率的降低, 面临了多多少少的回撤, 同时市场也逐渐趋于机构化理性化, 因此在传统CTA策略的基础上加入基本面的因素显得迫在眉睫. 近几年各券商的研报陆续提出了许多依赖于趋势行情以外的有效信号, 它们的表现都与趋势策略有着很低的甚至负的相关性, 这样通过多种不同类型的信号对冲得到的策略, 就有机会在市场上取得非常棒的夏普率和稳定的收益. 

[AkShare](https://github.com/jindaxiang/akshare) 库的公开就是为了向各位同仁提供一个网络数据采集接口, 避免各个研究组, 研究机构, 个人投资者重复造轮子采集相关数据造成的资源浪费. 


## Quick-Start

### 1. 先按照 [Anaconda安装说明及环境配置](#Anaconda安装说明及环境配置)
### 2. 查看 AkShare 提供的数据获取接口

**Example 2.1** 查看 AkShare 提供的数据获取接口

代码:

```python
import akshare as ak
[item for item in dir(ak) if item.startswith("get")]
```

结果显示:

> 数据获取函数说明

```
 # 交易所数据
 'get_cffex_daily',  # 获取中国金融期货交易所每日交易数据
 'get_cffex_rank_table',  # 获取中国金融期货交易所前20会员持仓数据明细
 'get_czce_daily',  # 获取郑州商品交易所每日交易数据
 'get_czce_rank_table',  # 获取郑州商品交易所前20会员持仓数据明细
 'get_dce_daily',  # 获取大连商品交易所每日交易数据
 'get_dce_rank_table',  #获取大连商品交易所前20会员持仓数据明细
 'get_futures_daily',  # 获取中国金融期货交易所每日基差数据
 'get_rank_sum',  # 获取四个期货交易所前5, 10, 15, 20会员持仓排名数据
 'get_rank_sum_daily',  # 获取每日四个期货交易所前5, 10, 15, 20会员持仓排名数据
 'get_receipt',  # 获取大宗商品注册仓单数据
 'get_roll_yield',  # 获取某一天某品种(主力和次主力)或固定两个合约的展期收益率
 'get_roll_yield_bar',  # 获取展期收益率
 'get_shfe_daily',  # 获取上海期货交易所每日交易数据
 'get_shfe_rank_table',  # 获取上海期货交易所前20会员持仓数据明细
 'get_shfe_v_wap',  # 获取上海期货交易所日成交均价数据
 'get_spot_price',  # 获取某一交易日大宗商品现货价格及相应基差数据
 'get_spot_price_daily'  # 获取一段交易日大宗商品现货价格及相应基差数据
 # 奇货可查数据
 'get_qhkc_index'  # 获取奇货可查-指数-数值数据
 'get_qhkc_index_profit_loss'  # 获取奇货可查-指数-累计盈亏数据
 'get_qhkc_index_trend'  # 获取奇货可查-指数-大资金动向数据
 'get_qhkc_fund_bs'  # 获取奇货可查-资金-净持仓分布数据
 'get_qhkc_fund_position'  # 获取奇货可查-资金-总持仓分布数据
 'get_qhkc_fund_position_change'  # 获取奇货可查-资金-净持仓变化分布数据
 'get_qhkc_tool_foreign'  # 获取奇货可查-工具-外盘比价数据
 'get_qhkc_tool_gdp'  # 获取奇货可查-工具-各地区经济数据
 # 中国银行间市场交易所数据
 'get_bond_bank'  # 获取中国银行间市场交易商协会-债券数据
```

### 3. 获取展期收益率

**Example 3.1** 获取展期收益率数据:

代码:

```python
import akshare as ak
ak.get_roll_yield_bar(type_method="date", var="RB", start_day="20180618", end_day="20180718", plot=True)
```

结果显示：

> 日期, 展期收益率, 最近合约, 下一期合约
```
            roll_yield near_by deferred
2018-06-19    0.191289  RB1810   RB1901
2018-06-20    0.192123  RB1810   RB1901
2018-06-21    0.183304  RB1810   RB1901
2018-06-22    0.190642  RB1810   RB1901
2018-06-25    0.194838  RB1810   RB1901
2018-06-26    0.204314  RB1810   RB1901
2018-06-27    0.213667  RB1810   RB1901
2018-06-28    0.211701  RB1810   RB1901
2018-06-29    0.205892  RB1810   RB1901
2018-07-02    0.224809  RB1810   RB1901
2018-07-03    0.229198  RB1810   RB1901
2018-07-04    0.222853  RB1810   RB1901
2018-07-05    0.247187  RB1810   RB1901
2018-07-06    0.261259  RB1810   RB1901
2018-07-09    0.253283  RB1810   RB1901
2018-07-10    0.225832  RB1810   RB1901
2018-07-11    0.210659  RB1810   RB1901
2018-07-12    0.212805  RB1810   RB1901
2018-07-13    0.170282  RB1810   RB1901
2018-07-16    0.218066  RB1810   RB1901
2018-07-17    0.229768  RB1810   RB1901
2018-07-18    0.225529  RB1810   RB1901
```


## 展期收益率
展期收益率是由不同交割月的价差除以相隔月份数计算得来, 它反映了市场对该品种在近期交割和远期交割的价差预期. 

通过 get_roll_yield_bar 接口下载展期收益率, 这里展期收益率列表的序列类型分为三种, 分别可以通过 type_method="date", "symbol", "var"获取. 
其中 "date" 类型是由某商品品种在不同日期的主力合约和次主力合约的价差组成, 调用方法例子为:


![展期收益率1](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/5*I5BdC65qlzua*UdvH8RLnUqlxUPZac.zFZudbuu70!/b/dEcBAAAAAAAA&bo=6gIZAQAAAAADB9I!&rf=viewer_4)


其中 "symbol" 类型是由某商品品种在某天的所有交割月合约价格组成, 可以很方便的观察该品种从近期到远期的展期结构, 调用方法例子为: 
```
ak.get_roll_yield_bar(type_method="symbol", var="RB", date="20180718", plot=True)
```
![展期收益率2](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/C4uCfCH4GmrJZIuM5bh4UxXIZVybLVQ1fg5PjxNRC4U!/b/dDEBAAAAAAAA&bo=3AIqAQAAAAADB9c!&rf=viewer_4)


其中 "var" 类型是由某交易日, 所有品种的主力次主力合约展期收益率的组合, 可以方便的找到展期收益率高的品种和低的品种, 调用方法例子为: 
```
ak.get_roll_yield_bar(type_method="var", date="20180718", plot=True)
```
![展期收益率3](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/A7sWrX8pHdkmNybpwx.qziH0pjFvl9ZDh7e1W8olQo8!/b/dDIBAAAAAAAA&bo=zAIxAQAAAAADB9w!&rf=viewer_4)


利用 get_roll_yield 接口, 可以找到特定合约特定日期的主力合约次主力合约展期收益率, 或通过 symbol1、symbol2 变量自定义某两个合约的展期收益率. 

```
ak.get_roll_yield(date="20180718", var="IF", symbol1="IF1812", symbol2="IF1811"), 如下图所示: 
```
![展期收益率4](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/sbBvkU.BCNWrQfDLkBL918x2*0j1QTbzXhjIP4rg5Ec!/b/dC0BAAAAAAAA&bo=VgRKAAAAAAADBzo!&rf=viewer_4)


注意:

主力合约和次主力合约的定义, 是由该日的各交割月合约持仓量由大到小排序得到.


## 注册仓单
注册仓单是由各交易所的公布的日级数据, 在一定程度上可以反映市场的库存变化. 调用例子如下: 
```python
import akshare as ak
ak.get_receipt(start_day="20180712", end_day="20180719", vars_list=["CU", "NI"])
```
下图有错误, [FuShare](https://github.com/jindaxiang/fushare) 的作者把 receipt 打错字为 recipet, 目前在 AkShare 已经修正为 receipt

![注册仓单](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/cOYxMVta6Ylp87IskIjwOG6nkkMJQ1HJ7HggCSgafog!/b/dDABAAAAAAAA&bo=WARNAgAAAAADBzE!&rf=viewer_4)

注意:

1. vars_list 变量接上需要爬取的品种列表, 即使是一个品种, 也需要以列表形式输入; 由于 vars 为 Python 内置, 后续将被移除

2. 在研究仓单的方向变化时, 需要考虑一些品种的年度周期性, 如农产品的收割季、工业品的开工季等;

3. 需考虑到交割日的仓单变化. 


## 现货价格和基差
基差是商品期货非常重要的基本面因素. 这里提供两种获取基差的方法: 
获取当天的基差数据
```python
import akshare as ak
ak.get_spot_price("20180712")
```
返回值分别为品种、现货价格、最近交割合约、最近交割合约价格、主力合约、主力合约价格、最近合约基差值、主力合约基差值、最近合约基差率、主力合约基差率. 


![现货价格和基差1](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/W.RAzR8m1YlGAQs0fgmlftn7AJO1KT*EmZVA4Aw.KKQ!/b/dFMBAAAAAAAA&bo=jQNOAQAAAAADB.M!&rf=viewer_4)


获取历史某段时间的基差值
```python
import akshare as ak
ak.get_spot_price_daily(start_day="20180710", end_day="20180719", vars_list=["CU", "RB"])
```
![现货价格和基差2](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/ctmFsF3vNZLCCnoH1j6EuZCKRztuIfNL*6yHBhUV*gk!/b/dFIBAAAAAAAA&bo=gwM4AgAAAAADF4g!&rf=viewer_4)


注意: 

现货价格是从生意社网站爬取获得, 仅支持从 2011 年至今每个交易日数据. 


## 会员持仓排名
自从 "蜘蛛网策略" 问世以来, 会员持仓数据受到日益关注. 数据的爬取方式如下所示: 
获取某段时间的会员持仓排名前 5、前 10、前 15、前 20 等总和.
```python
import akshare as ak
ak.get_rank_sum_daily(start_day="20180718", end_day="20180719", vars_list=["IF", "C"])
```
![会员持仓1](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/0BtIdxAyCswVlR4o1fjXfQxn49Odr3rKqt3u*KA0At0!/b/dDYBAAAAAAAA&bo=fgORAQAAAAADF98!&rf=viewer_4)


获取某交易日某品种的持仓排名榜
```
ak.get_dce_rank_table()
ak.get_cffex_rank_table()
ak.get_czce_rank_table()
ak.get_shfe_rank_table()
```
![会员持仓3](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/O905N6vk7SFlQlnPfaFJEZi2qTFUOl.7OKXIGmBeWm8!/b/dFoAAAAAAAAA&bo=pgM8AQAAAAADB7o!&rf=viewer_4)

注意: 

因为每个交易所公布的持仓排名不同: 大连所只公布品种的总持仓排名, 没有按不同交割月划分;上海、中金交易所公布了每个交割月的持仓排名, 没有公布品种所有合约总排名, 因此这里的品种排名和是各合约加总计算得来;郑州交易所公布了各合约排名和品种排名, 因此这里都是交易所原始数据. 

## 日线行情K线
通过爬取交易所官网信息, 可以获得各合约日线行情, 以及根据持仓量加权的指数行情, 用法如下: 
```python
import akshare as ak
ak.get_futures_daily(start_day="20190107", end_day="20190108", market="SHFE", index_bar=True)
```
![日线行情](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/0Kaa2Y9yMcyL7puvLxeaDs1oRW7Nlx6pkC5ENFtrQN0!/b/dLgAAAAAAAAA&bo=PATEAAAAAAADB94!&rf=viewer_4)

market 可以添为四个交易所的简称, 即 "dce" 代表大商所; "shfe" 代表上期所; "czce" 代表郑商所; "cffex" 代表中金所. 
index_bar 为 True 时, 在生成的 pd.DataFrame 中通过持仓量加权合成指数合约, 如 RB99.


## Anaconda安装说明及环境配置
### Anaconda 安装说明

> Anaconda 是集成了上千个常用库的 Python 发行版本, 通过安装 Anaconda 能简化环境管理工作, 非常推荐使用. 

> 作者基于目前 Python2 即将停止更新, 且目前大部分使用者电脑系统基本都是 64 位, 所以建议选择 Python3.7.3 64 位版本

> 同时, 根据您电脑的操作系统选择相对应的版本: Windows 版, MacOS 或 Linux 版的 64 位安装包.

#### 安装演示(以 64 位 windows 版本为例)
下图中红框为 64 位 Windows 选择的版本:
![anaconda安装图](https://jfds.nos-eastchina1.126.net/akshare/anaconda/anaconda_download.png)

在这里, 作者建议下载 Anaconda3-2019.07, 点击下载 [最新版 Anaconda 官方下载链接](https://repo.anaconda.com/archive/Anaconda3-2019.07-Windows-x86_64.exe)

> 双击如下图标进行安装:
>
![image](https://jfds.nos-eastchina1.126.net/akshare/anaconda/anaconda_icon.png)

> 点击 Next

![image](https://jfds.nos-eastchina1.126.net/akshare/anaconda/anaconda_install_1.png)

> 点击 I Agree

![image](https://jfds.nos-eastchina1.126.net/akshare/anaconda/anaconda_install_2.png)


> 点击 Just me --> Next

![image](https://jfds.nos-eastchina1.126.net/akshare/anaconda/anaconda_install_3.png)


> 修改 Destination Folder 为如图所示:

![image](https://jfds.nos-eastchina1.126.net/akshare/anaconda/anaconda_install_4.png)

> 勾选下图红框选项(以便于把安装的环境加入系统路径) --> Install

![image](https://jfds.nos-eastchina1.126.net/akshare/anaconda/anaconda_install_5.png)

> 安装好后, 找到 Anaconda Prompt 窗口:

![image](https://jfds.nos-eastchina1.126.net/akshare/prompt/anaconda_prompt.png)

> 输入 python, 如果如下图所示, 即已经在系统目录中安装好 anaconda3 的环境. 

![image](https://jfds.nos-eastchina1.126.net/akshare/prompt/anaconda_prompt_1.png)

> 创建虚拟环境
```
conda create -n ak_test python=3.7.3
```

```
Proceed 输入 y
```

> 显示出 最后一个红框内容则创建虚拟环境成功

![image](https://jfds.nos-eastchina1.126.net/akshare/prompt/anaconda_prompt_2.png)

> 在虚拟环境中安装 AkShare. 输入如下内容, 会在全新的环境中自动安装所需要的依赖包

```
pip install akshare --upgrade
```

![image](https://jfds.nos-eastchina1.126.net/akshare/prompt/anaconda_prompt_3.png)

> 在安装完毕后, 输入 python 进入虚拟环境中的 python

```
python
```

```python
import akshare as ak
ak.__doc__
```

> 如下界面则虚拟环境和 AkShare 安装成功

![image](https://jfds.nos-eastchina1.126.net/akshare/prompt/anaconda_prompt_4.png)


> 输入如下代码可以显示 AkShare 的版本
```python
import akshare as ak
ak.__version__
```


## 每日监控下载配置
本地配置好 Anaconda, 以及通过 pip 安装好 akshare>=0.1.25 后, 在 github 上下载示例文件, 即按照下图选择. 

[https://github.com/jindaxiang/akshare](https://github.com/jindaxiang/akshare)

![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/oT9PEhN0Knbv7Q.hPIO9TyuDkHl*il8K92GILqm4QHQ!/b/dL4AAAAAAAAA&bo=EgTRAwAAAAADB.Y!&rf=viewer_4)

解压下载的文件, 然后来到 example 目录下, 设置 setting 配置文件
root 设置为 AkShare 爬数据时存储的默认目录(需要保证目录存在), qqEmail 和 secret 为爬取到数据时把数据发送给自己的 qq 邮箱账号和密码. 需要开通SMTP服务, 如果不需要自己邮件提醒, 就不用设置（也不要改默认的qqEmail和secret）. 
![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/Ja.CVdg.fgrxFKW2jBGJqT53b7qCNSY*DwmbGDBS928!/b/dL8AAAAAAAAA&bo=aQRbAwAAAAADBxc!&rf=viewer_4)

最后双击 monitor.cmd 即完成, 每日 17 点自动下载数据. 

## QQ邮箱SMTP服务设置
在利用 Python 程序发送 QQ 邮件时, 需要开启 QQ 邮件的 SMTP 服务, 操作方法如下, 第一步打开 QQ 邮箱, 点"设置". 

![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/bvaIA.HUOZL.pKsEPMB4gj8dvT*9TLy*6x7zIKwzPQE!/b/dLwAAAAAAAAA&bo=HgR5AgAAAAADB0M!&rf=viewer_4)

找到"账户", 并下拉
![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/umgOdgp4tRuhiDOmtbLXiVVIPZ*87HeSQBaVHd1jPcY!/b/dL8AAAAAAAAA&bo=HATrAAAAAAADF8E!&rf=viewer_4)

开启以下的两项服务, 并生成授权码, 授权码为 Python 程序通过 SMTP 发送邮件的密码, 即上一节文档的 secret(不同于QQ邮箱登录密码)
![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/XavUKCeQ3fSqFXFTPBU0kJN9eIoFMtOApCEp7ZNDRqs!/b/dL8AAAAAAAAA&bo=iAOWAgAAAAADFy0!&rf=viewer_4)

在启动服务的过程中, 如果该 QQ 账户没有绑定过手机号, 可能会需要验证, 这里不再赘述. 

## 特别说明

### 致谢:

特别感谢 [FuShare](https://github.com/jindaxiang/fushare), [TuShare](https://github.com/waditu/tushare) 项目提供借鉴学习的机会;

感谢[生意社网站](http://www.100ppi.com/)提供的商品基差及相关数据;

感谢[奇货可查网站](https://qhkch.com/)提供的奇货指数及相关数据;

感谢[中国金融期货交易所网站](http://www.cffex.com.cn/)提供的相关数据;

感谢[上海期货交易所网站](http://www.shfe.com.cn/)提供的相关数据;

感谢[大连商品交易所网站](http://www.dce.com.cn/)提供的相关数据;

感谢[郑州商品交易所网站](http://www.czce.com.cn/)提供的相关数据;

感谢[上海国际能源交易中心网站](http://www.ine.com.cn/)提供的相关数据;



### 交流:

欢迎加 QQ 群交流: 326900231

您可以扫码或者点击群二维码

在开启 QQ 情况下, 点击下面的图片自动打开 QQ 并加入本群, 本功能由 QQ 提供, 请放心点击:

<a target="_blank" href="https://shang.qq.com/wpa/qunwpa?idkey=aacb87089dd5ecb8c6620ce391de15b92310cfb65e3b37f37eb465769e3fc1a3"><img border="0" src="https://jfds.nos-eastchina1.126.net/akshare/md_fold/1569925684166.png" alt="AkShare官方" title="AkShare官方"></a>



### 声明:

1. [AkShare](https://github.com/jindaxiang/akshare) 提供的数据仅供参考, 不构成任何投资建议;
2. 任何基于 [AkShare](https://github.com/jindaxiang/akshare) 进行研究的投资者请注意数据风险;
3. [AkShare](https://github.com/jindaxiang/akshare) 的使用请遵循相关开源协议;

