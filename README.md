AkShare

AkShare 已经发布, 请访问[主页链接](https://github.com/jindaxiang/akshare)了解和查询数据接口！

AkShare 是实现对期货等衍生金融产品从数据采集, 数据清洗加工, 到数据下载的工具, 满足金融数据科学家, 数据科学爱好者在数据获取方面的需求. 它的特点是利用 AkShare 获取的是基于交易所公布的原始数据, 广大数据科学家可以利用原始数据进行再加工, 得出科学的结论.

**作者: Albert King**

<img src="https://jfds.nos-eastchina1.126.net/AkShare/md_fold/images.jpg" width = 20% height = 10% align = center/>






建议安装方法
-
    pip install AkShare


升级方法
-
    pip install AkShare --upgrade
    
最新版本
-
    0.1.11
    更新完毕所有基于 fushare 接口, 后续开发特色期货数据接口


**目录**
- [AkShare 库的特色](#AkShare库的特色)
- [AkShare 库的初衷](#AkShare库的初衷)
- [展期收益率](#展期收益率)
- [注册仓单](#注册仓单)
- [现货价格和基差](#现货价格和基差)
- [会员持仓排名](#会员持仓排名)
- [日线行情 K 线](#日线行情K线)
- [Anaconda 环境配置](#anaconda环境配置)
- [每日监控下载配置](#每日监控下载配置)
- [QQ 邮箱 SMTP 服务设置](#QQ邮箱SMTP服务设置)
- [特别说明](#特别说明)



## AkShare库的特色
AkShare 后期主要改进如下:
1. 语法更符合 PEP8 规范, 尤其在函数命名上;
2. 仅支持 Python 3.7 以上版本的 Python
3. 后续加入 asyncio 和 aiohttp 做异步爬虫加速
4. 修正函数不能运行的问题
5. 增加更多的网络数据采集功能

    5.1 增加奇货可查(https://qhkch.com/)数据接口, 目前已经提供奇货可查指数部分
    
6. 后续更新主要集中在数据部分, 也希望您能参与 AkShare 的维护管理


## AkShare库的初衷
由于 fushare 库目前处于无人维护状态, 特建立 AkShare 库

传统的 CTA 策略以趋势为主, 但是自从 2017 年以来, 无论是长线还是短线的趋势策略都受制于商品波动率的降低, 面临了多多少少的回撤, 同时市场也逐渐趋于机构化理性化, 因此在传统CTA策略的基础上加入基本面的因素显得迫在眉睫. 近几年各券商的研报陆续提出了许多依赖于趋势行情以外的有效信号, 它们的表现都与趋势策略有着很低的甚至负的相关性, 这样通过多种不同类型的信号对冲得到的策略, 就有机会在市场上取得非常棒的夏普率和稳定的收益. 

AkShare 库的公开就是为了向各位同仁提供一个爬虫接口, 避免各个研究组、机构重复造轮子爬取相关数据的资源浪费. 



## 展期收益率
展期收益率是由不同交割月的价差除以相隔月份数计算得来, 它反映了市场对该品种在近期交割和远期交割的价差预判. 

通过 get_roll_yield_bar 接口下载展期收益率, 这里展期收益率列表的序列类型分为三种, 分别可以通过 type="date"、"symbol"、"var"获取. 
其中 "date" 类型是由某商品品种在不同日期的主力合约次主力合约的价差组成, 调用方法例子为: 
```
import akshare as ak
ak.get_roll_yield_bar(type="date", var="RB", start="20180618", end="20180718", plot=True)
```
![展期收益率1](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/5*I5BdC65qlzua*UdvH8RLnUqlxUPZac.zFZudbuu70!/b/dEcBAAAAAAAA&bo=6gIZAQAAAAADB9I!&rf=viewer_4)


其中 "symbol" 类型是由某商品品种在某天的所有交割月合约价格组成, 可以很方便的观察该品种从近期到远期的展期结构, 调用方法例子为: 
```
ak.get_roll_yield_bar(type="symbol", var="RB", date="20180718", plot=True)
```
![展期收益率2](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/C4uCfCH4GmrJZIuM5bh4UxXIZVybLVQ1fg5PjxNRC4U!/b/dDEBAAAAAAAA&bo=3AIqAQAAAAADB9c!&rf=viewer_4)


其中 "var" 类型是由某交易日, 所有品种的主力次主力合约展期收益率的组合, 可以方便的找到展期收益率高的品种和低的品种, 调用方法例子为: 
```
ak.get_roll_yield_bar(type="var", date="20180718", plot=True)
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
```
ak.get_receipt(start="20180712", end="20180719", vars=["CU", "NI"])
```
下图有错误, fushare 的原作者把 receipt 打错字为 recipet, 目前在 AkShare 已经修正为 receipt

![注册仓单](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/cOYxMVta6Ylp87IskIjwOG6nkkMJQ1HJ7HggCSgafog!/b/dDABAAAAAAAA&bo=WARNAgAAAAADBzE!&rf=viewer_4)

注意:

1. vars 变量接上需要爬取的品种列表, 即使是一个品种, 也需要以列表形式输入; 由于 vars 为 Python 内置, 后续将被移除

2. 在研究仓单的方向变化时, 需要考虑一些品种的年度周期性, 如农产品的收割季、工业品的开工季等;

3. 需考虑到交割日的仓单变化. 


## 现货价格和基差
基差是商品期货非常重要的基本面因素. 这里提供两种获取基差的方法: 
获取当天的基差数据
```
ak.get_spot_price("20180712")
```
返回值分别为品种、现货价格、最近交割合约、最近交割合约价格、主力合约、主力合约价格、最近合约基差值、主力合约基差值、最近合约基差率、主力合约基差率. 


![现货价格和基差1](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/W.RAzR8m1YlGAQs0fgmlftn7AJO1KT*EmZVA4Aw.KKQ!/b/dFMBAAAAAAAA&bo=jQNOAQAAAAADB.M!&rf=viewer_4)


获取历史某段时间的基差值
```
ak.get_spot_price_daily(start="20180710", end="20180719", vars=["CU", "RB"])
```
![现货价格和基差2](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/ctmFsF3vNZLCCnoH1j6EuZCKRztuIfNL*6yHBhUV*gk!/b/dFIBAAAAAAAA&bo=gwM4AgAAAAADF4g!&rf=viewer_4)


注意: 

现货价格是从生意社网站爬取获得, 仅支持从 2011 年至今每个交易日数据. 


## 会员持仓排名
自从 "蜘蛛网策略" 问世以来, 会员持仓数据受到日益关注. 数据的爬取方式如下所示: 
获取某段时间的会员持仓排名前 5、前 10、前 15、前 20 等总和.
```
ak.get_rank_sum_daily(start="20180718", end="20180719", vars=["IF", "C"])
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
```
ak.get_futures_daily(start="20190107", end="20190108", market="SHFE", index_bar=True)
```
![日线行情](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/0Kaa2Y9yMcyL7puvLxeaDs1oRW7Nlx6pkC5ENFtrQN0!/b/dLgAAAAAAAAA&bo=PATEAAAAAAADB94!&rf=viewer_4)

market 可以添为四个交易所的简称, 即 "dce" 代表大商所; "shfe" 代表上期所; "czce" 代表郑商所; "cffex" 代表中金所. 
index_bar为True时, 在生成的 pd.DataFrame 中通过持仓量加权合成指数合约, 如 RB99.


## Anaconda环境配置
Anaconda 是集成了上千个常用包的 Python 发行版本, 通过安装 Anaconda 简化了环境管理工作, 非常推荐使用. 

[最新版 Anaconda 官方下载链接](https://repo.anaconda.com/archive/Anaconda3-2019.07-Windows-x86_64.exe)

建议选择成熟的 python3.7.3 版本, 即 Anaconda3-2019.07; 根据系统选择 windows 版、linux版或 mac 版, 64位. 红框为 64 位 windows 选择的版本
![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/bGJd4p3Vc6xvQjC2GL8tkzuH*PPtvppmtQ1LCIO4lqM!/b/dMAAAAAAAAAA&bo=vQMBBQAAAAADB5g!&rf=viewer_4)

双击安装过程中有一个界面需要注意, 即下图把两个钩都选上, 以便于把安装的环境加入系统路径. 

![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/trxwrKu7FsArWoYY.3n9erIExJdt3BlOhZJ1q1720XY!/b/dLYAAAAAAAAA&bo=8AGBAQAAAAADF0M!&rf=viewer_4)

安装好后, 打开cmd窗口, 输入python, 如果如下图所示, 即已经在系统目录中安装好anaconda5.2.0(python3.6)的环境. 
![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/khK1RedWmG.k4hI6XwnI*CmYGXfvHuIlu2QlDHmEtYA!/b/dL8AAAAAAAAA&bo=9gIBAgAAAAADB9U!&rf=viewer_4)

用 ctrl+z 可以退出刚才的 Python 运行环境回到 cmd 命令下, 输入
```
pip install AkShare
```
即在 Python 环境中安装了AkShare 库(有网络情况下)

![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/cLA3Un4yK4rE3JHXHdHhO5mDxKokQ158J734BBmz69Q!/b/dL8AAAAAAAAA&bo=.AKpBAAAAAADF2U!&rf=viewer_4)

再次输入 python, 进入 python 环境, 输入
```
import akshare
```
即导入了 AkShare 库, 再输入
```
akshare.__version__
```
可以查看当前安装的 AkShare 版本号
![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/7fePfBNlfdeBiuiSFd*Ba2X2jBrjXb4wjS9jPyH*7Nc!/b/dL8AAAAAAAAA&bo=.AKfAQAAAAADB0Y!&rf=viewer_4)


## 每日监控下载配置
本地配置好 Anaconda, 以及通过 pip 安装好 akshare>=0.1.2 后, 在 github 上下载示例文件, 即按照下图选择. 

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

致谢:

感谢 fushare, tushare 项目提供借鉴学习的机会; 感谢生意社网站的商品基差数据的公开.

交流:

欢迎加 QQ 群交流: 326900231

![image](https://jfds.nos-eastchina1.126.net/AkShare/md_fold/1569925684166.png)

点击加入下面的图片自动 QQ 打开加入:

<a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=aacb87089dd5ecb8c6620ce391de15b92310cfb65e3b37f37eb465769e3fc1a3"><img border="0" src="https://jfds.nos-eastchina1.126.net/AkShare/md_fold/images.jpg" alt="AkShare官方" title="AkShare官方"></a>

声明:

数据仅供参考, 不构成任何投资建议, 投资者请自行研究, 当然风险自担. 
