# akshare(python3.7)
[主页链接](https://github.com/jindaxiang/akshare)

[策略示例链接--聚宽社区](https://www.joinquant.com/post/15594)


建议安装方法
--------------
    pip install akshare

升级方法
---------------
    pip install akshare --upgrade
    
最新版本
---------------
    1.2.1
    新增了每交易日 17 点自动爬数据并存本地 csv 文件功能, 进而将数据发送给自己 QQ 邮件(微信有提醒)
    
    1.2.3
    新增指数日线行情爬取(持仓量加权)
    
    1.2.5
    修复指数日线行情bug
    
    1.2.6
    同bug, 改成持仓量或成交量为 0 时都不进行加权
    
    1.2.7
    czce的rank_table中有的数值类型变成numpy.int, 在_tableCut_cal函数末尾加了一句保证数据类型转换为int
    
    1.2.8
    pandas 最新版 0.24.0 的 pd.read_html 函数在 basis 脚本中识别格式有区别, 脚本中针对不同pandas版本识别不同
    
    1.2.9
    大商所的仓单数据网站格式变化
    
    1.2.10
    上期所成交量 0 时候有的为 str 格式的空白, 解决该问题
    20190502, 20190503, 去掉该交易日
    
    1.2.11
    修复 receipt 接口不能访问的问题



**作者: Albert King**

**目录**
- [akshare库的特色](#akshare库的特色)
- [akshare库的初衷](#akshare库的初衷)
- [展期收益率](#展期收益率)
- [注册仓单](#注册仓单)
- [现货价格和基差](#现货价格和基差)
- [会员持仓排名](#会员持仓排名)
- [日线行情K线](#日线行情K线)
- [anaconda环境配置](#anaconda环境配置)
- [每日监控下载配置](#每日监控下载配置)
- [QQ邮箱SMTP服务设置](#QQ邮箱SMTP服务设置)

## akshare库的特色

akshare 后期主要改进如下:
1. 语法更符合 PEP8 规范, 尤其在函数命名上
2. 支持 Python3.7 以上版本
3. 后续加入 asyncio 和 aiohttp 做异步爬虫加速
4. 修正函数不能运行的问题
5. 增加更多的功能



## akshare库的初衷

传统的CTA策略以趋势为主, 但是自从2017年以来, 无论是长线还是短线的趋势策略都受制于商品波动率的降低, 面临了多多少少的回撤, 同时市场也逐渐趋于机构化理性化, 因此在传统CTA策略的基础上加入基本面的因素显得迫在眉睫。近几年各券商的研报陆续提出了许多依赖于趋势行情以外的有效信号, 它们的表现都与趋势策略有着很低的甚至负的相关性, 这样通过多种不同类型的信号对冲得到的策略, 就有机会在市场上取得非常棒的夏普率和稳定的收益。

akshare 库的公开就是为了向各位同仁提供一个爬虫接口, 避免各个研究组、机构重复造轮子爬取相关数据的资源浪费。


## 展期收益率
展期收益率是由不同交割月的价差除以相隔月份数计算得来, 它反映了市场对该品种在近期交割和远期交割的价差预判。

通过get_rollYield_bar接口下载展期收益率, 这里展期收益率列表的序列类型分为三种, 分别可以通过type='date'、'symbol'、'var'获取。
其中'date'类型是由某商品品种在不同日期的主力合约次主力合约的价差组成, 调用方法例子为：
```
import akshare as ak
ak.get_rollYield_bar(type = 'date', var = 'RB', start = '20180618', end = '20180718',plot = True)
```
![展期收益率1](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/5*I5BdC65qlzua*UdvH8RLnUqlxUPZac.zFZudbuu70!/b/dEcBAAAAAAAA&bo=6gIZAQAAAAADB9I!&rf=viewer_4)


其中'symbol'类型是由某商品品种在某天的所有交割月合约价格组成, 可以很方便的观察该品种从近期到远期的展期结构, 调用方法例子为：
```
ak.get_rollYield_bar(type = 'symbol', var = 'RB', date = '20180718',plot = True)
```
![展期收益率2](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/C4uCfCH4GmrJZIuM5bh4UxXIZVybLVQ1fg5PjxNRC4U!/b/dDEBAAAAAAAA&bo=3AIqAQAAAAADB9c!&rf=viewer_4)


其中'var'类型是由某交易日, 所有品种的主力次主力合约展期收益率的组合, 可以方便的找到展期收益率高的品种和低的品种, 调用方法例子为：
```
ak.get_rollYield_bar(type = 'var', date = '20180718',plot = True)
```
![展期收益率3](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/A7sWrX8pHdkmNybpwx.qziH0pjFvl9ZDh7e1W8olQo8!/b/dDIBAAAAAAAA&bo=zAIxAQAAAAADB9w!&rf=viewer_4)


利用get_rollYield接口, 可以找到特定合约特定日期的主力合约次主力合约展期收益率, 或通过symbol1、symbol2变量自定义某两个合约的展期收益率。

```
ak.get_rollYield(date = '20180718', var = 'IF', symbol1 = 'IF1812', symbol2 = 'IF1811'), 如下图所示：
```
![展期收益率4](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/sbBvkU.BCNWrQfDLkBL918x2*0j1QTbzXhjIP4rg5Ec!/b/dC0BAAAAAAAA&bo=VgRKAAAAAAADBzo!&rf=viewer_4)


注意：

主力合约和次主力合约的定义, 是由该日的各交割月合约持仓量由大到小排序得到。


## 注册仓单
注册仓单是由各交易所的公布的日级数据, 在一定程度上可以反映市场的库存变化。调用例子如下：
```
ak.get_reciept(start = '20180712', end = '20180719', vars = ['CU', 'NI'])
```
![注册仓单](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/cOYxMVta6Ylp87IskIjwOG6nkkMJQ1HJ7HggCSgafog!/b/dDABAAAAAAAA&bo=WARNAgAAAAADBzE!&rf=viewer_4)

注意：

1.vars变量接上需要爬取的品种列表, 即使是一个品种, 也需要以列表形式输入；

2.在研究仓单的方向变化时, 需要考虑一些品种的年度周期性, 如农产品的收割季、工业品的开工季等；

3.需考虑到交割日的仓单变化。


## 现货价格和基差
基差是商品期货非常重要的基本面因素。这里提供两种获取基差的方法：
获取当天的基差数据
```
ak.get_spotPrice('20180712')
```
返回值分别为品种、现货价格、最近交割合约、最近交割合约价格、主力合约、主力合约价格、最近合约基差值、主力合约基差值、最近合约基差率、主力合约基差率。


![现货价格和基差1](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/W.RAzR8m1YlGAQs0fgmlftn7AJO1KT*EmZVA4Aw.KKQ!/b/dFMBAAAAAAAA&bo=jQNOAQAAAAADB.M!&rf=viewer_4)


获取历史某段时间的基差值
```
ak.get_spotPrice_daily(start = '20180710', end = '20180719', vars = ['CU', 'RB'])
```
![现货价格和基差2](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/ctmFsF3vNZLCCnoH1j6EuZCKRztuIfNL*6yHBhUV*gk!/b/dFIBAAAAAAAA&bo=gwM4AgAAAAADF4g!&rf=viewer_4)


注意：

现货价格是从生意社网站爬取获得, 仅支持从2011年至今每个交易日数据。


## 会员持仓排名
自从“蜘蛛网策略”问世以来, 会员持仓数据受到日益关注。数据的爬取方式如下所示：
获取某段时间的会员持仓排名前5、前10、前15、前20等总和
```
ak.get_rank_sum_daily(start = '20180718', end = '20180719', vars = ['IF', 'C'])
```
![会员持仓1](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/0BtIdxAyCswVlR4o1fjXfQxn49Odr3rKqt3u*KA0At0!/b/dDYBAAAAAAAA&bo=fgORAQAAAAADF98!&rf=viewer_4)


获取某交易日某品种的持仓排名榜
```
ak.get_dce_rank_table()、ak.get_cffex_rank_table()、ak.get_czce_rank_table()、ak.get_shfe_rank_table()
```
![会员持仓3](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/O905N6vk7SFlQlnPfaFJEZi2qTFUOl.7OKXIGmBeWm8!/b/dFoAAAAAAAAA&bo=pgM8AQAAAAADB7o!&rf=viewer_4)

注意：

因为每个交易所公布的持仓排名不同：大连所只公布品种的总持仓排名, 没有按不同交割月划分；上海、中金交易所公布了每个交割月的持仓排名, 没有公布品种所有合约总排名, 因此这里的品种排名和是各合约加总计算得来；郑州交易所公布了各合约排名和品种排名, 因此这里都是交易所原始数据。

## 日线行情K线
通过爬取交易所官网信息, 可以获得各合约日线行情, 以及根据持仓量加权的指数行情, 用法如下：
```
ak.get_future_daily(start='20190107', end='20190108', market='SHFE', indexBar = True)
```
![日线行情](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/0Kaa2Y9yMcyL7puvLxeaDs1oRW7Nlx6pkC5ENFtrQN0!/b/dLgAAAAAAAAA&bo=PATEAAAAAAADB94!&rf=viewer_4)

market可以添为四个交易所的简称, 即'dce'代表大商所；'shfe'代表上期所；'czce'代表郑商所；'cffex'代表中金所。
indexBar为True时, 在生成的dataframe中通过持仓量加权合成指数合约, 如RB99


## anaconda环境配置
anaconda是集成了上千个常用包的python发行版本, 通过安装anaconda简化了环境管理工作, 非常推荐使用。

[anaconda下载链接](https://repo.anaconda.com/archive/)

建议选择成熟的python3.6版本, 即anaconda3-5.2.0。根据系统选择windows版、linux版或mac版, 及32位或64位。红框为64位windows选择的版本
![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/bGJd4p3Vc6xvQjC2GL8tkzuH*PPtvppmtQ1LCIO4lqM!/b/dMAAAAAAAAAA&bo=vQMBBQAAAAADB5g!&rf=viewer_4)

双击安装过程中有一个界面需要注意, 即下图把两个钩都选上, 以便于把安装的环境加入系统路径。

![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/trxwrKu7FsArWoYY.3n9erIExJdt3BlOhZJ1q1720XY!/b/dLYAAAAAAAAA&bo=8AGBAQAAAAADF0M!&rf=viewer_4)

安装好后, 打开cmd窗口, 输入python, 如果如下图所示, 即已经在系统目录中安装好anaconda5.2.0(python3.6)的环境。
![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/khK1RedWmG.k4hI6XwnI*CmYGXfvHuIlu2QlDHmEtYA!/b/dL8AAAAAAAAA&bo=9gIBAgAAAAADB9U!&rf=viewer_4)

用ctrl+Z可以退出刚才的python运行环境回到cmd命令下, 输入
```
pip install akshare
```
即在python环境中安装了akshare库(有网络情况下)

![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/cLA3Un4yK4rE3JHXHdHhO5mDxKokQ158J734BBmz69Q!/b/dL8AAAAAAAAA&bo=.AKpBAAAAAADF2U!&rf=viewer_4)

再次输入python, 进入python环境, 输入
```
import akshare
```
即导入了akshare库, 再输入
```
akshare.__version__
```
可以查看当前安装的akshare版本号
![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/7fePfBNlfdeBiuiSFd*Ba2X2jBrjXb4wjS9jPyH*7Nc!/b/dL8AAAAAAAAA&bo=.AKfAQAAAAADB0Y!&rf=viewer_4)


## 每日监控下载配置
本地配置好anaconda, 以及通过pip安装好akshare>=1.2.1后, 在github上下载示例文件, 即按照下图选择。

[https://github.com/jindaxiang/akshare](https://github.com/jindaxiang/akshare)

![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/oT9PEhN0Knbv7Q.hPIO9TyuDkHl*il8K92GILqm4QHQ!/b/dL4AAAAAAAAA&bo=EgTRAwAAAAADB.Y!&rf=viewer_4)

解压下载的文件, 然后来到example目录下, 设置setting配置文件
root设置为akshare爬数据时存储的默认目录（需要保证目录存在）, qqEmail和secret为爬取到数据时把数据发送给自己的qq邮箱账号和密码。需要开通SMTP服务, 如果不需要自己邮件提醒, 就不用设置（也不要改默认的qqEmail和secret）。
![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/Ja.CVdg.fgrxFKW2jBGJqT53b7qCNSY*DwmbGDBS928!/b/dL8AAAAAAAAA&bo=aQRbAwAAAAADBxc!&rf=viewer_4)

最后双击monitor.cmd即完成, 每日17点自动下载数据。

## QQ邮箱SMTP服务设置
在利用python程序发送QQ邮件时, 需要开启QQ邮件的SMTP服务, 操作方法如下, 第一步打开QQ邮箱, 点‘设置’。

![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/bvaIA.HUOZL.pKsEPMB4gj8dvT*9TLy*6x7zIKwzPQE!/b/dLwAAAAAAAAA&bo=HgR5AgAAAAADB0M!&rf=viewer_4)

找到‘账户’, 并下拉
![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/umgOdgp4tRuhiDOmtbLXiVVIPZ*87HeSQBaVHd1jPcY!/b/dL8AAAAAAAAA&bo=HATrAAAAAAADF8E!&rf=viewer_4)

开启以下的两项服务, 并生成授权码, 授权码为python程序通过SMTP发送邮件的密码, 即上一节文档的secret（不同于QQ邮箱登录密码）
![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/XavUKCeQ3fSqFXFTPBU0kJN9eIoFMtOApCEp7ZNDRqs!/b/dL8AAAAAAAAA&bo=iAOWAgAAAAADFy0!&rf=viewer_4)

在启动服务的过程中, 如果该QQ账户没有绑定过手机号, 可能会需要验证, 这里不再赘述。





致谢:
感谢akshare, tushare项目提供借鉴学习的机会；感谢生意社网站的商品基差数据的公开。

交流:
欢迎加QQ群交流809290570

数据仅供参考, 不构成投资建议, 投资者请自行研究, 风险自担。
