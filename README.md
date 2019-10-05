AkShare

AkShare 已经发布, 请访问[主页链接](https://github.com/jindaxiang/akshare)了解和查询数据接口！

AkShare 是实现对期货等衍生金融产品从数据采集, 数据清洗加工, 到数据下载的工具, 满足金融数据科学家, 数据科学爱好者在数据获取方面的需求. 它的特点是利用 AkShare 获取的是基于交易所公布的原始数据, 广大数据科学家可以利用原始数据进行再加工, 得出科学的结论.

**作者: Albert King**


<img src="https://jfds.nos-eastchina1.126.net/akshare/md_fold/images.jpg" width = 20% height = 10% align = center/>






建议安装方法
-
    pip install akshare


升级方法
-
    pip install akshare --upgrade
    
最新版本
-
    0.1.13
    更新所有基于 fushare 的接口
    
    0.1.14
    更新 requirements.txt 文件
    
    0.1.15
    自动安装所需要的 packages
    
    0.1.16
    修正部分函数命名
    
    0.1.17
    更新版本号自动管理
    
    0.1.18
    更新说明文档
    
    0.1.25
    增加奇货可查指数接口 e.g. ak.get_qhkc_data("商品指数")


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
- [最新说明文档](#最新说明文档)



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

![image](https://jfds.nos-eastchina1.126.net/akshare/md_fold/1569925684166.png)

点击加入下面的图片自动 QQ 打开加入:

<a target="_blank" href="https://shang.qq.com/wpa/qunwpa?idkey=aacb87089dd5ecb8c6620ce391de15b92310cfb65e3b37f37eb465769e3fc1a3"><img border="0" src="https://jfds.nos-eastchina1.126.net/akshare/md_fold/images.jpg" alt="AkShare官方" title="AkShare官方"></a>

声明:

数据仅供参考, 不构成任何投资建议, 投资者请自行研究, 当然风险自担. 

## 最新说明文档

# AkShare 使用说明

## 导入 akshare, 标记为缩写 ak


```python
import akshare as ak
```


```python
ak.__doc__
```




    'AkShare 是实现对期货等衍生金融产品从数据采集, 数据清洗加工, 到数据下载的工具, 满足金融数据科学家, 数据科学爱好者在数据获取方面的需求. 它的特点是利用 AkShare 获取的是基于交易所公布的原始数据, 广大数据科学家可以利用原始数据进行再加工, 得出科学的结论.'



## 查看 AkShare 版本


```python
ak.__version__
```




    '0.1.23'



# 查看 AkShare 提供的接口


```python
[item for item in dir(ak) if item.startswith("get")]
```




    ['get_cffex_daily',
     'get_cffex_rank_table',
     'get_czce_daily',
     'get_czce_rank_table',
     'get_dce_daily',
     'get_dce_rank_table',
     'get_futures_daily',
     'get_qhkc_data',
     'get_rank_sum',
     'get_rank_sum_daily',
     'get_receipt',
     'get_roll_yield',
     'get_roll_yield_bar',
     'get_shfe_daily',
     'get_shfe_rank_table',
     'get_shfe_v_wap',
     'get_spot_price',
     'get_spot_price_daily']



## 测试及功能展示

### 一个品种在时间轴上的展期收益率



```python
ak.get_roll_yield_bar(type_method='date', var='RB', start='20181206', end='20181210', plot=False)
```

    C:\Anaconda3\lib\site-packages\akshare\roll_yield.py:133: UserWarning: 20181208非交易日
      warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
    C:\Anaconda3\lib\site-packages\akshare\roll_yield.py:133: UserWarning: 20181209非交易日
      warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>roll_yield</th>
      <th>near_by</th>
      <th>deferred</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2018-12-06</td>
      <td>0.298430</td>
      <td>RB1901</td>
      <td>RB1905</td>
    </tr>
    <tr>
      <td>2018-12-07</td>
      <td>0.282155</td>
      <td>RB1901</td>
      <td>RB1905</td>
    </tr>
    <tr>
      <td>2018-12-10</td>
      <td>0.294811</td>
      <td>RB1901</td>
      <td>RB1905</td>
    </tr>
  </tbody>
</table>
</div>




```python
ak.get_roll_yield_bar(type_method='date', var='RB', start='20181206', end='20181210', plot=True)
```


![png](output_11_0.png)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>roll_yield</th>
      <th>near_by</th>
      <th>deferred</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2018-12-06</td>
      <td>0.298430</td>
      <td>RB1901</td>
      <td>RB1905</td>
    </tr>
    <tr>
      <td>2018-12-07</td>
      <td>0.282155</td>
      <td>RB1901</td>
      <td>RB1905</td>
    </tr>
    <tr>
      <td>2018-12-10</td>
      <td>0.294811</td>
      <td>RB1901</td>
      <td>RB1905</td>
    </tr>
  </tbody>
</table>
</div>



### 一个品种在不同交割标的上的价格比较



```python
ak.get_roll_yield_bar(type_method='symbol', var='RB', date='20181210', plot=False)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>symbol</th>
      <th>date</th>
      <th>open</th>
      <th>high</th>
      <th>low</th>
      <th>close</th>
      <th>volume</th>
      <th>open_interest</th>
      <th>turnover</th>
      <th>settle</th>
      <th>pre_settle</th>
      <th>variety</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>92</td>
      <td>RB1812</td>
      <td>20181210</td>
      <td>3504</td>
      <td>3620</td>
      <td>3503</td>
      <td>3620.0</td>
      <td>180</td>
      <td>300</td>
      <td>6.375600e+05</td>
      <td>3542.0</td>
      <td>3592.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>93</td>
      <td>RB1901</td>
      <td>20181210</td>
      <td>3717</td>
      <td>3728</td>
      <td>3648</td>
      <td>3654.0</td>
      <td>527694</td>
      <td>606054</td>
      <td>1.940859e+09</td>
      <td>3678.0</td>
      <td>3717.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>94</td>
      <td>RB1902</td>
      <td>20181210</td>
      <td>3488</td>
      <td>3504</td>
      <td>3414</td>
      <td>3414.0</td>
      <td>388</td>
      <td>10092</td>
      <td>1.337824e+06</td>
      <td>3448.0</td>
      <td>3494.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>95</td>
      <td>RB1903</td>
      <td>20181210</td>
      <td>3468</td>
      <td>3468</td>
      <td>3379</td>
      <td>3380.0</td>
      <td>224</td>
      <td>9652</td>
      <td>7.674240e+05</td>
      <td>3426.0</td>
      <td>3453.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>96</td>
      <td>RB1904</td>
      <td>20181210</td>
      <td>3469</td>
      <td>3469</td>
      <td>3395</td>
      <td>3404.0</td>
      <td>84</td>
      <td>1256</td>
      <td>2.868600e+05</td>
      <td>3415.0</td>
      <td>3465.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>97</td>
      <td>RB1905</td>
      <td>20181210</td>
      <td>3388</td>
      <td>3398</td>
      <td>3303</td>
      <td>3312.0</td>
      <td>4741366</td>
      <td>2476276</td>
      <td>1.584565e+10</td>
      <td>3342.0</td>
      <td>3372.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>98</td>
      <td>RB1906</td>
      <td>20181210</td>
      <td>3351</td>
      <td>3351</td>
      <td>3288</td>
      <td>3288.0</td>
      <td>490</td>
      <td>1678</td>
      <td>1.621410e+06</td>
      <td>3309.0</td>
      <td>3357.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>99</td>
      <td>RB1907</td>
      <td>20181210</td>
      <td>3340</td>
      <td>3364</td>
      <td>3278</td>
      <td>3283.0</td>
      <td>36</td>
      <td>2784</td>
      <td>1.194840e+05</td>
      <td>3319.0</td>
      <td>3344.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>100</td>
      <td>RB1908</td>
      <td>20181210</td>
      <td>3312</td>
      <td>3339</td>
      <td>3281</td>
      <td>3296.0</td>
      <td>56</td>
      <td>2076</td>
      <td>1.849680e+05</td>
      <td>3303.0</td>
      <td>3343.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>101</td>
      <td>RB1909</td>
      <td>20181210</td>
      <td>3304</td>
      <td>3311</td>
      <td>3226</td>
      <td>3228.0</td>
      <td>638</td>
      <td>4904</td>
      <td>2.079880e+06</td>
      <td>3260.0</td>
      <td>3293.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>102</td>
      <td>RB1910</td>
      <td>20181210</td>
      <td>3255</td>
      <td>3255</td>
      <td>3167</td>
      <td>3173.0</td>
      <td>132724</td>
      <td>309510</td>
      <td>4.248495e+08</td>
      <td>3201.0</td>
      <td>3225.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>103</td>
      <td>RB1911</td>
      <td>20181210</td>
      <td>3213</td>
      <td>3213</td>
      <td>3146</td>
      <td>3158.0</td>
      <td>118</td>
      <td>466</td>
      <td>3.750040e+05</td>
      <td>3178.0</td>
      <td>3203.0</td>
      <td>RB</td>
    </tr>
  </tbody>
</table>
</div>




```python
ak.get_roll_yield_bar(type_method='symbol', var='RB', date='20181210', plot=True)
```


![png](output_14_0.png)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>symbol</th>
      <th>date</th>
      <th>open</th>
      <th>high</th>
      <th>low</th>
      <th>close</th>
      <th>volume</th>
      <th>open_interest</th>
      <th>turnover</th>
      <th>settle</th>
      <th>pre_settle</th>
      <th>variety</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>92</td>
      <td>RB1812</td>
      <td>20181210</td>
      <td>3504</td>
      <td>3620</td>
      <td>3503</td>
      <td>3620.0</td>
      <td>180</td>
      <td>300</td>
      <td>6.375600e+05</td>
      <td>3542.0</td>
      <td>3592.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>93</td>
      <td>RB1901</td>
      <td>20181210</td>
      <td>3717</td>
      <td>3728</td>
      <td>3648</td>
      <td>3654.0</td>
      <td>527694</td>
      <td>606054</td>
      <td>1.940859e+09</td>
      <td>3678.0</td>
      <td>3717.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>94</td>
      <td>RB1902</td>
      <td>20181210</td>
      <td>3488</td>
      <td>3504</td>
      <td>3414</td>
      <td>3414.0</td>
      <td>388</td>
      <td>10092</td>
      <td>1.337824e+06</td>
      <td>3448.0</td>
      <td>3494.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>95</td>
      <td>RB1903</td>
      <td>20181210</td>
      <td>3468</td>
      <td>3468</td>
      <td>3379</td>
      <td>3380.0</td>
      <td>224</td>
      <td>9652</td>
      <td>7.674240e+05</td>
      <td>3426.0</td>
      <td>3453.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>96</td>
      <td>RB1904</td>
      <td>20181210</td>
      <td>3469</td>
      <td>3469</td>
      <td>3395</td>
      <td>3404.0</td>
      <td>84</td>
      <td>1256</td>
      <td>2.868600e+05</td>
      <td>3415.0</td>
      <td>3465.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>97</td>
      <td>RB1905</td>
      <td>20181210</td>
      <td>3388</td>
      <td>3398</td>
      <td>3303</td>
      <td>3312.0</td>
      <td>4741366</td>
      <td>2476276</td>
      <td>1.584565e+10</td>
      <td>3342.0</td>
      <td>3372.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>98</td>
      <td>RB1906</td>
      <td>20181210</td>
      <td>3351</td>
      <td>3351</td>
      <td>3288</td>
      <td>3288.0</td>
      <td>490</td>
      <td>1678</td>
      <td>1.621410e+06</td>
      <td>3309.0</td>
      <td>3357.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>99</td>
      <td>RB1907</td>
      <td>20181210</td>
      <td>3340</td>
      <td>3364</td>
      <td>3278</td>
      <td>3283.0</td>
      <td>36</td>
      <td>2784</td>
      <td>1.194840e+05</td>
      <td>3319.0</td>
      <td>3344.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>100</td>
      <td>RB1908</td>
      <td>20181210</td>
      <td>3312</td>
      <td>3339</td>
      <td>3281</td>
      <td>3296.0</td>
      <td>56</td>
      <td>2076</td>
      <td>1.849680e+05</td>
      <td>3303.0</td>
      <td>3343.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>101</td>
      <td>RB1909</td>
      <td>20181210</td>
      <td>3304</td>
      <td>3311</td>
      <td>3226</td>
      <td>3228.0</td>
      <td>638</td>
      <td>4904</td>
      <td>2.079880e+06</td>
      <td>3260.0</td>
      <td>3293.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>102</td>
      <td>RB1910</td>
      <td>20181210</td>
      <td>3255</td>
      <td>3255</td>
      <td>3167</td>
      <td>3173.0</td>
      <td>132724</td>
      <td>309510</td>
      <td>4.248495e+08</td>
      <td>3201.0</td>
      <td>3225.0</td>
      <td>RB</td>
    </tr>
    <tr>
      <td>103</td>
      <td>RB1911</td>
      <td>20181210</td>
      <td>3213</td>
      <td>3213</td>
      <td>3146</td>
      <td>3158.0</td>
      <td>118</td>
      <td>466</td>
      <td>3.750040e+05</td>
      <td>3178.0</td>
      <td>3203.0</td>
      <td>RB</td>
    </tr>
  </tbody>
</table>
</div>



### 多个品种在某天的展期收益率横截面比较


```python
ak.get_roll_yield_bar(type_method='var', date='20181210', plot=False)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>roll_yield</th>
      <th>near_by</th>
      <th>deferred</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>P</td>
      <td>-0.263205</td>
      <td>P1901</td>
      <td>P1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>A</td>
      <td>-0.216919</td>
      <td>A1901</td>
      <td>A1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>Y</td>
      <td>-0.157068</td>
      <td>Y1901</td>
      <td>Y1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>SC</td>
      <td>-0.130079</td>
      <td>SC1901</td>
      <td>SC1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>CF</td>
      <td>-0.129128</td>
      <td>CF901</td>
      <td>CF905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>OI</td>
      <td>-0.084165</td>
      <td>OI901</td>
      <td>OI905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>B</td>
      <td>-0.075830</td>
      <td>B1905</td>
      <td>B1909</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>AP</td>
      <td>-0.073559</td>
      <td>AP901</td>
      <td>AP905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>RU</td>
      <td>-0.067631</td>
      <td>RU1901</td>
      <td>RU1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>C</td>
      <td>-0.052619</td>
      <td>C1905</td>
      <td>C1909</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>MA</td>
      <td>-0.051777</td>
      <td>MA901</td>
      <td>MA905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>IH</td>
      <td>-0.038215</td>
      <td>IH1812</td>
      <td>IH1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>AU</td>
      <td>-0.031875</td>
      <td>AU1904</td>
      <td>AU1906</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>SN</td>
      <td>-0.030524</td>
      <td>SN1901</td>
      <td>SN1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>CY</td>
      <td>-0.028840</td>
      <td>CY901</td>
      <td>CY905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>AG</td>
      <td>-0.028114</td>
      <td>AG1812</td>
      <td>AG1906</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>AL</td>
      <td>-0.026374</td>
      <td>AL1901</td>
      <td>AL1902</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>IF</td>
      <td>-0.022802</td>
      <td>IF1812</td>
      <td>IF1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>T</td>
      <td>-0.019991</td>
      <td>T1812</td>
      <td>T1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>BU</td>
      <td>-0.017119</td>
      <td>BU1906</td>
      <td>BU1912</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>BB</td>
      <td>-0.002783</td>
      <td>BB1812</td>
      <td>BB1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>SR</td>
      <td>0.003031</td>
      <td>SR901</td>
      <td>SR905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>TS</td>
      <td>0.008598</td>
      <td>TS1903</td>
      <td>TS1906</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>CU</td>
      <td>0.009806</td>
      <td>CU1901</td>
      <td>CU1902</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>CS</td>
      <td>0.015411</td>
      <td>CS1901</td>
      <td>CS1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>NI</td>
      <td>0.015412</td>
      <td>NI1901</td>
      <td>NI1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>FU</td>
      <td>0.017341</td>
      <td>FU1901</td>
      <td>FU1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>RM</td>
      <td>0.017595</td>
      <td>RM901</td>
      <td>RM905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>TF</td>
      <td>0.039739</td>
      <td>TF1812</td>
      <td>TF1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>IC</td>
      <td>0.052550</td>
      <td>IC1812</td>
      <td>IC1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>EG</td>
      <td>0.053940</td>
      <td>EG1906</td>
      <td>EG1909</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>SF</td>
      <td>0.100009</td>
      <td>SF901</td>
      <td>SF905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>SP</td>
      <td>0.116269</td>
      <td>SP1906</td>
      <td>SP1909</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>V</td>
      <td>0.126581</td>
      <td>V1901</td>
      <td>V1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>FG</td>
      <td>0.133971</td>
      <td>FG901</td>
      <td>FG905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>WH</td>
      <td>0.149438</td>
      <td>WH901</td>
      <td>WH905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>L</td>
      <td>0.170197</td>
      <td>L1901</td>
      <td>L1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>ZN</td>
      <td>0.170902</td>
      <td>ZN1901</td>
      <td>ZN1902</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>ZC</td>
      <td>0.194331</td>
      <td>ZC901</td>
      <td>ZC905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>PP</td>
      <td>0.194476</td>
      <td>PP1901</td>
      <td>PP1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>TA</td>
      <td>0.200516</td>
      <td>TA901</td>
      <td>TA905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>I</td>
      <td>0.205521</td>
      <td>I1903</td>
      <td>I1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>M</td>
      <td>0.246920</td>
      <td>M1901</td>
      <td>M1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>WR</td>
      <td>0.258545</td>
      <td>WR1905</td>
      <td>WR1907</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>RB</td>
      <td>0.294811</td>
      <td>RB1901</td>
      <td>RB1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>HC</td>
      <td>0.294977</td>
      <td>HC1901</td>
      <td>HC1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>PB</td>
      <td>0.301655</td>
      <td>PB1901</td>
      <td>PB1902</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>SM</td>
      <td>0.357260</td>
      <td>SM901</td>
      <td>SM905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>J</td>
      <td>0.534467</td>
      <td>J1901</td>
      <td>J1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>JD</td>
      <td>0.539171</td>
      <td>JD1901</td>
      <td>JD1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>JM</td>
      <td>0.569068</td>
      <td>JM1901</td>
      <td>JM1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>FB</td>
      <td>0.678381</td>
      <td>FB1901</td>
      <td>FB1902</td>
      <td>2018-12-10</td>
    </tr>
  </tbody>
</table>
</div>




```python
ak.get_roll_yield_bar(type_method='var', date='20181210', plot=True)
```


![png](output_17_0.png)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>roll_yield</th>
      <th>near_by</th>
      <th>deferred</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>P</td>
      <td>-0.263205</td>
      <td>P1901</td>
      <td>P1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>A</td>
      <td>-0.216919</td>
      <td>A1901</td>
      <td>A1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>Y</td>
      <td>-0.157068</td>
      <td>Y1901</td>
      <td>Y1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>SC</td>
      <td>-0.130079</td>
      <td>SC1901</td>
      <td>SC1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>CF</td>
      <td>-0.129128</td>
      <td>CF901</td>
      <td>CF905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>OI</td>
      <td>-0.084165</td>
      <td>OI901</td>
      <td>OI905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>B</td>
      <td>-0.075830</td>
      <td>B1905</td>
      <td>B1909</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>AP</td>
      <td>-0.073559</td>
      <td>AP901</td>
      <td>AP905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>RU</td>
      <td>-0.067631</td>
      <td>RU1901</td>
      <td>RU1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>C</td>
      <td>-0.052619</td>
      <td>C1905</td>
      <td>C1909</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>MA</td>
      <td>-0.051777</td>
      <td>MA901</td>
      <td>MA905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>IH</td>
      <td>-0.038215</td>
      <td>IH1812</td>
      <td>IH1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>AU</td>
      <td>-0.031875</td>
      <td>AU1904</td>
      <td>AU1906</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>SN</td>
      <td>-0.030524</td>
      <td>SN1901</td>
      <td>SN1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>CY</td>
      <td>-0.028840</td>
      <td>CY901</td>
      <td>CY905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>AG</td>
      <td>-0.028114</td>
      <td>AG1812</td>
      <td>AG1906</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>AL</td>
      <td>-0.026374</td>
      <td>AL1901</td>
      <td>AL1902</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>IF</td>
      <td>-0.022802</td>
      <td>IF1812</td>
      <td>IF1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>T</td>
      <td>-0.019991</td>
      <td>T1812</td>
      <td>T1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>BU</td>
      <td>-0.017119</td>
      <td>BU1906</td>
      <td>BU1912</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>BB</td>
      <td>-0.002783</td>
      <td>BB1812</td>
      <td>BB1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>SR</td>
      <td>0.003031</td>
      <td>SR901</td>
      <td>SR905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>TS</td>
      <td>0.008598</td>
      <td>TS1903</td>
      <td>TS1906</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>CU</td>
      <td>0.009806</td>
      <td>CU1901</td>
      <td>CU1902</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>CS</td>
      <td>0.015411</td>
      <td>CS1901</td>
      <td>CS1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>NI</td>
      <td>0.015412</td>
      <td>NI1901</td>
      <td>NI1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>FU</td>
      <td>0.017341</td>
      <td>FU1901</td>
      <td>FU1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>RM</td>
      <td>0.017595</td>
      <td>RM901</td>
      <td>RM905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>TF</td>
      <td>0.039739</td>
      <td>TF1812</td>
      <td>TF1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>IC</td>
      <td>0.052550</td>
      <td>IC1812</td>
      <td>IC1903</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>EG</td>
      <td>0.053940</td>
      <td>EG1906</td>
      <td>EG1909</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>SF</td>
      <td>0.100009</td>
      <td>SF901</td>
      <td>SF905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>SP</td>
      <td>0.116269</td>
      <td>SP1906</td>
      <td>SP1909</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>V</td>
      <td>0.126581</td>
      <td>V1901</td>
      <td>V1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>FG</td>
      <td>0.133971</td>
      <td>FG901</td>
      <td>FG905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>WH</td>
      <td>0.149438</td>
      <td>WH901</td>
      <td>WH905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>L</td>
      <td>0.170197</td>
      <td>L1901</td>
      <td>L1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>ZN</td>
      <td>0.170902</td>
      <td>ZN1901</td>
      <td>ZN1902</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>ZC</td>
      <td>0.194331</td>
      <td>ZC901</td>
      <td>ZC905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>PP</td>
      <td>0.194476</td>
      <td>PP1901</td>
      <td>PP1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>TA</td>
      <td>0.200516</td>
      <td>TA901</td>
      <td>TA905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>I</td>
      <td>0.205521</td>
      <td>I1903</td>
      <td>I1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>M</td>
      <td>0.246920</td>
      <td>M1901</td>
      <td>M1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>WR</td>
      <td>0.258545</td>
      <td>WR1905</td>
      <td>WR1907</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>RB</td>
      <td>0.294811</td>
      <td>RB1901</td>
      <td>RB1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>HC</td>
      <td>0.294977</td>
      <td>HC1901</td>
      <td>HC1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>PB</td>
      <td>0.301655</td>
      <td>PB1901</td>
      <td>PB1902</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>SM</td>
      <td>0.357260</td>
      <td>SM901</td>
      <td>SM905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>J</td>
      <td>0.534467</td>
      <td>J1901</td>
      <td>J1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>JD</td>
      <td>0.539171</td>
      <td>JD1901</td>
      <td>JD1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>JM</td>
      <td>0.569068</td>
      <td>JM1901</td>
      <td>JM1905</td>
      <td>2018-12-10</td>
    </tr>
    <tr>
      <td>FB</td>
      <td>0.678381</td>
      <td>FB1901</td>
      <td>FB1902</td>
      <td>2018-12-10</td>
    </tr>
  </tbody>
</table>
</div>



### 特定两个标的的展期收益率


```python
ak.get_roll_yield(date='20181210', var='IF', symbol1='IF1812', symbol2='IF1901')
```




    (-0.022802189947221208, 'IF1812', 'IF1903')



### 特定品种、特定时段的交易所注册仓单


```python
ak.get_receipt(start='20181207', end='20181210', vars=['CU', 'NI'])
```

    2018-12-07
    

    C:\Anaconda3\lib\site-packages\akshare\receipt.py:344: UserWarning: 20181208非交易日
      warnings.warn(f"{start.strftime('%Y%m%d')}非交易日")
    C:\Anaconda3\lib\site-packages\akshare\receipt.py:344: UserWarning: 20181209非交易日
      warnings.warn(f"{start.strftime('%Y%m%d')}非交易日")
    

    2018-12-10
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>var</th>
      <th>receipt</th>
      <th>receipt_chg</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>CU</td>
      <td>51319</td>
      <td>-1820</td>
      <td>20181207</td>
    </tr>
    <tr>
      <td>1</td>
      <td>NI</td>
      <td>14087</td>
      <td>0</td>
      <td>20181207</td>
    </tr>
    <tr>
      <td>2</td>
      <td>CU</td>
      <td>49842</td>
      <td>-1477</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>3</td>
      <td>NI</td>
      <td>13753</td>
      <td>-334</td>
      <td>20181210</td>
    </tr>
  </tbody>
</table>
</div>



### 特定日期的现货价格及基差


```python
ak.get_spot_price('20181210')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>var</th>
      <th>sp</th>
      <th>near_symbol</th>
      <th>near_price</th>
      <th>dom_symbol</th>
      <th>dom_price</th>
      <th>near_basis</th>
      <th>dom_basis</th>
      <th>near_basis_rate</th>
      <th>dom_basis_rate</th>
      <th>date</th>
    </tr>
    <tr>
      <th>var</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>C</td>
      <td>C</td>
      <td>1866.43</td>
      <td>c1901</td>
      <td>1862.00</td>
      <td>c1905</td>
      <td>1866.00</td>
      <td>-4.43</td>
      <td>-0.43</td>
      <td>-0.002374</td>
      <td>-0.000230</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>CS</td>
      <td>CS</td>
      <td>2513.00</td>
      <td>cs1901</td>
      <td>2338.00</td>
      <td>cs1905</td>
      <td>2336.00</td>
      <td>-175.00</td>
      <td>-177.00</td>
      <td>-0.069638</td>
      <td>-0.070434</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>A</td>
      <td>A</td>
      <td>3593.33</td>
      <td>a1901</td>
      <td>3216.00</td>
      <td>a1901</td>
      <td>3216.00</td>
      <td>-377.33</td>
      <td>-377.33</td>
      <td>-0.105008</td>
      <td>-0.105008</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>M</td>
      <td>M</td>
      <td>2980.00</td>
      <td>m1812</td>
      <td>2900.00</td>
      <td>m1905</td>
      <td>2687.00</td>
      <td>-80.00</td>
      <td>-293.00</td>
      <td>-0.026846</td>
      <td>-0.098322</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>Y</td>
      <td>Y</td>
      <td>5253.33</td>
      <td>y1812</td>
      <td>5284.00</td>
      <td>y1905</td>
      <td>5458.00</td>
      <td>30.67</td>
      <td>204.67</td>
      <td>0.005838</td>
      <td>0.038960</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>P</td>
      <td>P</td>
      <td>4180.00</td>
      <td>p1812</td>
      <td>4398.00</td>
      <td>p1905</td>
      <td>4512.00</td>
      <td>218.00</td>
      <td>332.00</td>
      <td>0.052153</td>
      <td>0.079426</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>JD</td>
      <td>JD</td>
      <td>4090.00</td>
      <td>jd1812</td>
      <td>4209.00</td>
      <td>jd1905</td>
      <td>3466.00</td>
      <td>119.00</td>
      <td>-624.00</td>
      <td>0.029095</td>
      <td>-0.152567</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>L</td>
      <td>L</td>
      <td>9350.00</td>
      <td>l1812</td>
      <td>9035.00</td>
      <td>l1905</td>
      <td>8505.00</td>
      <td>-315.00</td>
      <td>-845.00</td>
      <td>-0.033690</td>
      <td>-0.090374</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>V</td>
      <td>V</td>
      <td>6575.00</td>
      <td>v1812</td>
      <td>6505.00</td>
      <td>v1905</td>
      <td>6295.00</td>
      <td>-70.00</td>
      <td>-280.00</td>
      <td>-0.010646</td>
      <td>-0.042586</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>PP</td>
      <td>PP</td>
      <td>9650.00</td>
      <td>pp1812</td>
      <td>11168.00</td>
      <td>pp1905</td>
      <td>8533.00</td>
      <td>1518.00</td>
      <td>-1117.00</td>
      <td>0.157306</td>
      <td>-0.115751</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>J</td>
      <td>J</td>
      <td>2053.33</td>
      <td>j1812</td>
      <td>3410.00</td>
      <td>j1905</td>
      <td>2012.50</td>
      <td>1356.67</td>
      <td>-40.83</td>
      <td>0.660717</td>
      <td>-0.019885</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>JM</td>
      <td>JM</td>
      <td>1560.83</td>
      <td>jm1812</td>
      <td>1380.00</td>
      <td>jm1901</td>
      <td>1443.50</td>
      <td>-180.83</td>
      <td>-117.33</td>
      <td>-0.115855</td>
      <td>-0.075172</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>I</td>
      <td>I</td>
      <td>543.89</td>
      <td>i1812</td>
      <td>499.50</td>
      <td>i1905</td>
      <td>472.00</td>
      <td>-44.39</td>
      <td>-71.89</td>
      <td>-0.081616</td>
      <td>-0.132177</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>PM</td>
      <td>PM</td>
      <td>2520.00</td>
      <td>PM901</td>
      <td>2419.00</td>
      <td>PM901</td>
      <td>2419.00</td>
      <td>-101.00</td>
      <td>-101.00</td>
      <td>-0.040079</td>
      <td>-0.040079</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>CF</td>
      <td>CF</td>
      <td>15354.43</td>
      <td>CF901</td>
      <td>14635.00</td>
      <td>CF905</td>
      <td>15295.00</td>
      <td>-719.43</td>
      <td>-59.43</td>
      <td>-0.046855</td>
      <td>-0.003871</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>SR</td>
      <td>SR</td>
      <td>5362.00</td>
      <td>SR901</td>
      <td>4963.00</td>
      <td>SR905</td>
      <td>4946.00</td>
      <td>-399.00</td>
      <td>-416.00</td>
      <td>-0.074413</td>
      <td>-0.077583</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>TA</td>
      <td>TA</td>
      <td>6734.44</td>
      <td>TA812</td>
      <td>6698.00</td>
      <td>TA905</td>
      <td>6232.00</td>
      <td>-36.44</td>
      <td>-502.44</td>
      <td>-0.005411</td>
      <td>-0.074608</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>OI</td>
      <td>OI</td>
      <td>6496.67</td>
      <td>OI901</td>
      <td>6493.00</td>
      <td>OI905</td>
      <td>6673.00</td>
      <td>-3.67</td>
      <td>176.33</td>
      <td>-0.000565</td>
      <td>0.027142</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>MA</td>
      <td>MA</td>
      <td>2430.00</td>
      <td>MA812</td>
      <td>2645.00</td>
      <td>MA901</td>
      <td>2524.00</td>
      <td>215.00</td>
      <td>94.00</td>
      <td>0.088477</td>
      <td>0.038683</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>FG</td>
      <td>FG</td>
      <td>1376.00</td>
      <td>FG812</td>
      <td>1383.00</td>
      <td>FG901</td>
      <td>1333.00</td>
      <td>7.00</td>
      <td>-43.00</td>
      <td>0.005087</td>
      <td>-0.031250</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>RS</td>
      <td>RS</td>
      <td>5100.00</td>
      <td>RS907</td>
      <td>5271.00</td>
      <td>RS909</td>
      <td>5464.00</td>
      <td>171.00</td>
      <td>364.00</td>
      <td>0.033529</td>
      <td>0.071373</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>RM</td>
      <td>RM</td>
      <td>2351.67</td>
      <td>RM901</td>
      <td>2228.00</td>
      <td>RM905</td>
      <td>2216.00</td>
      <td>-123.67</td>
      <td>-135.67</td>
      <td>-0.052588</td>
      <td>-0.057691</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>ZC</td>
      <td>ZC</td>
      <td>621.00</td>
      <td>ZC901</td>
      <td>615.60</td>
      <td>ZC905</td>
      <td>573.80</td>
      <td>-5.40</td>
      <td>-47.20</td>
      <td>-0.008696</td>
      <td>-0.076006</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>SF</td>
      <td>SF</td>
      <td>6456.25</td>
      <td>SF812</td>
      <td>6056.00</td>
      <td>SF901</td>
      <td>6208.00</td>
      <td>-400.25</td>
      <td>-248.25</td>
      <td>-0.061994</td>
      <td>-0.038451</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>SM</td>
      <td>SM</td>
      <td>8507.14</td>
      <td>SM812</td>
      <td>8274.00</td>
      <td>SM901</td>
      <td>8444.00</td>
      <td>-233.14</td>
      <td>-63.14</td>
      <td>-0.027405</td>
      <td>-0.007422</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>CY</td>
      <td>CY</td>
      <td>24725.00</td>
      <td>CY812</td>
      <td>24175.00</td>
      <td>CY901</td>
      <td>23910.00</td>
      <td>-550.00</td>
      <td>-815.00</td>
      <td>-0.022245</td>
      <td>-0.032963</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>CU</td>
      <td>CU</td>
      <td>49410.00</td>
      <td>cu1812</td>
      <td>49030.00</td>
      <td>cu1902</td>
      <td>49060.00</td>
      <td>-380.00</td>
      <td>-350.00</td>
      <td>-0.007691</td>
      <td>-0.007084</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>AL</td>
      <td>AL</td>
      <td>13600.00</td>
      <td>al1812</td>
      <td>13570.00</td>
      <td>al1902</td>
      <td>13685.00</td>
      <td>-30.00</td>
      <td>85.00</td>
      <td>-0.002206</td>
      <td>0.006250</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>ZN</td>
      <td>ZN</td>
      <td>22120.00</td>
      <td>zn1812</td>
      <td>21550.00</td>
      <td>zn1902</td>
      <td>21110.00</td>
      <td>-570.00</td>
      <td>-1010.00</td>
      <td>-0.025769</td>
      <td>-0.045660</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>PB</td>
      <td>PB</td>
      <td>18850.00</td>
      <td>pb1812</td>
      <td>18985.00</td>
      <td>pb1901</td>
      <td>18530.00</td>
      <td>135.00</td>
      <td>-320.00</td>
      <td>0.007162</td>
      <td>-0.016976</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>NI</td>
      <td>NI</td>
      <td>92800.00</td>
      <td>ni1812</td>
      <td>88600.00</td>
      <td>ni1905</td>
      <td>89280.00</td>
      <td>-4200.00</td>
      <td>-3520.00</td>
      <td>-0.045259</td>
      <td>-0.037931</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>SN</td>
      <td>SN</td>
      <td>145000.00</td>
      <td>sn1812</td>
      <td>144850.00</td>
      <td>sn1905</td>
      <td>146020.00</td>
      <td>-150.00</td>
      <td>1020.00</td>
      <td>-0.001034</td>
      <td>0.007034</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>AU</td>
      <td>AU</td>
      <td>278.00</td>
      <td>au1812</td>
      <td>278.25</td>
      <td>au1906</td>
      <td>281.85</td>
      <td>0.25</td>
      <td>3.85</td>
      <td>0.000899</td>
      <td>0.013849</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>AG</td>
      <td>AG</td>
      <td>3527.00</td>
      <td>ag1812</td>
      <td>3524.00</td>
      <td>ag1906</td>
      <td>3567.00</td>
      <td>-3.00</td>
      <td>40.00</td>
      <td>-0.000851</td>
      <td>0.011341</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>RB</td>
      <td>RB</td>
      <td>3790.77</td>
      <td>rb1812</td>
      <td>3542.00</td>
      <td>rb1905</td>
      <td>3342.00</td>
      <td>-248.77</td>
      <td>-448.77</td>
      <td>-0.065625</td>
      <td>-0.118385</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>WR</td>
      <td>WR</td>
      <td>4090.00</td>
      <td>wr1903</td>
      <td>3683.00</td>
      <td>wr1905</td>
      <td>3447.00</td>
      <td>-407.00</td>
      <td>-643.00</td>
      <td>-0.099511</td>
      <td>-0.157213</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>HC</td>
      <td>HC</td>
      <td>3766.67</td>
      <td>hc1812</td>
      <td>3700.00</td>
      <td>hc1905</td>
      <td>3313.00</td>
      <td>-66.67</td>
      <td>-453.67</td>
      <td>-0.017700</td>
      <td>-0.120443</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>BU</td>
      <td>BU</td>
      <td>3700.33</td>
      <td>bu1812</td>
      <td>2732.00</td>
      <td>bu1906</td>
      <td>2818.00</td>
      <td>-968.33</td>
      <td>-882.33</td>
      <td>-0.261687</td>
      <td>-0.238446</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>RU</td>
      <td>RU</td>
      <td>10410.00</td>
      <td>ru1901</td>
      <td>11010.00</td>
      <td>ru1905</td>
      <td>11275.00</td>
      <td>600.00</td>
      <td>865.00</td>
      <td>0.057637</td>
      <td>0.083093</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>SP</td>
      <td>SP</td>
      <td>5875.00</td>
      <td>sp1906</td>
      <td>5182.00</td>
      <td>sp1906</td>
      <td>5182.00</td>
      <td>-693.00</td>
      <td>-693.00</td>
      <td>-0.117957</td>
      <td>-0.117957</td>
      <td>20181210</td>
    </tr>
  </tbody>
</table>
</div>



### 特定品种、特定时段的现货价格及基差


```python
ak.get_spot_price_daily(start_day='20181210', end_day='20181210', vars_list=['CU', 'RB'])
```

    2018-12-10
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>var</th>
      <th>sp</th>
      <th>near_symbol</th>
      <th>near_price</th>
      <th>dom_symbol</th>
      <th>dom_price</th>
      <th>near_basis</th>
      <th>dom_basis</th>
      <th>near_basis_rate</th>
      <th>dom_basis_rate</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>CU</td>
      <td>49410.00</td>
      <td>cu1812</td>
      <td>49030.0</td>
      <td>cu1902</td>
      <td>49060.0</td>
      <td>-380.00</td>
      <td>-350.00</td>
      <td>-0.007691</td>
      <td>-0.007084</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>1</td>
      <td>RB</td>
      <td>3790.77</td>
      <td>rb1812</td>
      <td>3542.0</td>
      <td>rb1905</td>
      <td>3342.0</td>
      <td>-248.77</td>
      <td>-448.77</td>
      <td>-0.065625</td>
      <td>-0.118385</td>
      <td>20181210</td>
    </tr>
  </tbody>
</table>
</div>



### 特定品种、特定时段的会员持仓排名求和


```python
ak.get_rank_sum_daily(start='20181210', end='20181210', vars_list=['IF', 'C'])
```

    2018-12-10
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>symbol</th>
      <th>variety</th>
      <th>vol_top5</th>
      <th>vol_chg_top5</th>
      <th>long_open_interest_top5</th>
      <th>long_open_interest_chg_top5</th>
      <th>short_open_interest_top5</th>
      <th>short_open_interest_chg_top5</th>
      <th>vol_top10</th>
      <th>vol_chg_top10</th>
      <th>...</th>
      <th>long_open_interest_chg_top15</th>
      <th>short_open_interest_top15</th>
      <th>short_open_interest_chg_top15</th>
      <th>vol_top20</th>
      <th>vol_chg_top20</th>
      <th>long_open_interest_top20</th>
      <th>long_open_interest_chg_top20</th>
      <th>short_open_interest_top20</th>
      <th>short_open_interest_chg_top20</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>C</td>
      <td>C</td>
      <td>178455</td>
      <td>-77360</td>
      <td>330993</td>
      <td>8066</td>
      <td>232921</td>
      <td>8135</td>
      <td>258486</td>
      <td>-117689</td>
      <td>...</td>
      <td>17975</td>
      <td>435181</td>
      <td>13902</td>
      <td>349525</td>
      <td>-180536</td>
      <td>581708</td>
      <td>16319</td>
      <td>509143</td>
      <td>15070</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>1</td>
      <td>IF1812</td>
      <td>IF</td>
      <td>24362</td>
      <td>2664</td>
      <td>16701</td>
      <td>78</td>
      <td>19242</td>
      <td>6</td>
      <td>35515</td>
      <td>3936</td>
      <td>...</td>
      <td>677</td>
      <td>34039</td>
      <td>95</td>
      <td>50100</td>
      <td>5676</td>
      <td>34376</td>
      <td>962</td>
      <td>37605</td>
      <td>736</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>2</td>
      <td>IF1903</td>
      <td>IF</td>
      <td>2299</td>
      <td>530</td>
      <td>5633</td>
      <td>149</td>
      <td>6266</td>
      <td>112</td>
      <td>3323</td>
      <td>747</td>
      <td>...</td>
      <td>403</td>
      <td>10298</td>
      <td>731</td>
      <td>4762</td>
      <td>1151</td>
      <td>9556</td>
      <td>590</td>
      <td>11047</td>
      <td>798</td>
      <td>20181210</td>
    </tr>
    <tr>
      <td>3</td>
      <td>IF</td>
      <td>IF</td>
      <td>26661</td>
      <td>3194</td>
      <td>22334</td>
      <td>227</td>
      <td>25508</td>
      <td>118</td>
      <td>38838</td>
      <td>4683</td>
      <td>...</td>
      <td>1080</td>
      <td>44337</td>
      <td>826</td>
      <td>54862</td>
      <td>6827</td>
      <td>43932</td>
      <td>1552</td>
      <td>48652</td>
      <td>1534</td>
      <td>20181210</td>
    </tr>
  </tbody>
</table>
<p>4 rows × 27 columns</p>
</div>



### 大商所会员持仓排名细节；郑商所、上期所、中金所分别改成get_czce_rank_table、get_shfe_rank_table、get_cffex_rank_table


```python
ak.get_dce_rank_table('20181210')
```




    {'C':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0               100430                    3888            国投安信     1   
     1                88044                   -3022            金瑞期货     2   
     2                74026                    4098            永安期货     3   
     3                39104                     297            中粮期货     4   
     4                29389                    2805            国泰君安     5   
     5                28108                    3185            光大期货     6   
     6                27975                     544            东海期货     7   
     7                25925                    -126            南华期货     8   
     8                22191                     -13            东证期货     9   
     9                19712                    6303            中信期货    10   
     10               17220                    -313            鲁证期货    11   
     11               17115                    1500            华安期货    12   
     12               14788                    -643            华泰期货    13   
     13               14567                       0            摩根大通    14   
     14               12848                    -528            广发期货    15   
     15               12418                    -958            徽商期货    16   
     16               11841                       6            银河期货    17   
     17                9775                    -574            兴证期货    18   
     18                8152                    -209            海通期货    19   
     19                8080                      79            渤海期货    20   
     20              581708                   16319            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 66317                     2066             永安期货   50304   
     1                 46299                    -1172             国投安信   39600   
     2                 45154                     3439             国泰君安   36877   
     3                 37881                      785             光大期货   27330   
     4                 37270                     3017             方正中期   24344   
     5                 27751                     -622             国富期货   18298   
     6                 24342                     1518             中国国际   18025   
     7                 22592                     2194             浙商期货   15791   
     8                 21514                     -936             中信期货   14979   
     9                 19316                     1095             中融汇信   12938   
     10                19075                     1542             新湖期货   12094   
     11                18993                     -868             鲁证期货   10702   
     12                17226                     -111             申银万国   10608   
     13                15777                        0             招商期货   10595   
     14                15674                     1955             格林大华    9153   
     15                15429                      322             银河期货    8516   
     16                15350                     -281             天风期货    7658   
     17                14590                     1196             海通期货    7480   
     18                14340                      361             国海良时    7229   
     19                14253                     -430             国金期货    7004   
     20               509143                    15070             None  349525   
     
         vol_chg vol_party_name symbol variety  
     0    -25581           光大期货      C       C  
     1     -9687           东证期货      C       C  
     2    -16437           中信期货      C       C  
     3    -18022           迈科期货      C       C  
     4     -7633           国投安信      C       C  
     5      -946           国泰君安      C       C  
     6      4788           金瑞期货      C       C  
     7     -3747           海通期货      C       C  
     8    -24192           徽商期货      C       C  
     9    -16232           永安期货      C       C  
     10     3215           申银万国      C       C  
     11   -11855           华泰期货      C       C  
     12    -8123           长江期货      C       C  
     13    -8697           兴证期货      C       C  
     14    -3699           广州金控      C       C  
     15   -19469           方正中期      C       C  
     16     4521           上海中期      C       C  
     17    -4589           华安期货      C       C  
     18    -2304           中粮期货      C       C  
     19   -11847           浙商期货      C       C  
     20  -180536           None      C       C  ,
     'CS':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                12459                    -143            国投安信     1   
     1                12004                   -1157            东证期货     2   
     2                 8940                     235            华安期货     3   
     3                 8746                     179            金瑞期货     4   
     4                 8574                    -652            中信期货     5   
     5                 8359                    -778            国泰君安     6   
     6                 8165                    -517            中粮期货     7   
     7                 6721                      76            华泰期货     8   
     8                 5880                       7            中金期货     9   
     9                 5750                   -1329            徽商期货    10   
     10                5091                    -112            永安期货    11   
     11                3525                    -167            中融汇信    12   
     12                3138                     105            南华期货    13   
     13                3138                      -9            中国国际    14   
     14                2725                     167            光大期货    15   
     15                2626                     253            银河期货    16   
     16                2176                    -111            兴证期货    17   
     17                2170                     834            广发期货    18   
     18                1204                      90            北京首创    19   
     19                1110                    -305            中信建投    20   
     20              112501                   -3334            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                  8546                      237             国投安信   27840   
     1                  6329                     -203             天风期货   12716   
     2                  5125                       43             中粮期货   10338   
     3                  5081                      820             中信期货    9912   
     4                  5003                      289             永安期货    9546   
     5                  5001                      929             兴证期货    8767   
     6                  4995                     -246             华泰期货    6723   
     7                  4515                     -253             中辉期货    6033   
     8                  4122                     -652             方正中期    5194   
     9                  3840                      -45             广州金控    4936   
     10                 3141                      993             国泰君安    4382   
     11                 3134                    -1271             渤海期货    4243   
     12                 2986                       73             光大期货    4108   
     13                 2900                       42             东兴期货    3682   
     14                 2795                       26             银河期货    3566   
     15                 2787                      509             海通期货    3374   
     16                 2702                     -310             鲁证期货    3138   
     17                 2400                      -63             南华期货    2892   
     18                 2003                     -305             东航期货    2755   
     19                 1929                        5             冠通期货    2711   
     20                79334                      618             None  136856   
     
         vol_chg vol_party_name symbol variety  
     0    -17224           东证期货     CS      CS  
     1     -2445           光大期货     CS      CS  
     2     -5414           中信期货     CS      CS  
     3     -2235           国投安信     CS      CS  
     4     -6739           海通期货     CS      CS  
     5        47           广州金控     CS      CS  
     6     -7287           国泰君安     CS      CS  
     7     -5287           徽商期货     CS      CS  
     8     -9904           方正中期     CS      CS  
     9     -5960           华泰期货     CS      CS  
     10     -940           广发期货     CS      CS  
     11    -2380           永安期货     CS      CS  
     12    -2592           兴证期货     CS      CS  
     13    -6368           金瑞期货     CS      CS  
     14    -2082           中辉期货     CS      CS  
     15     -522           上海大陆     CS      CS  
     16    -3920           华安期货     CS      CS  
     17    -1888           中信建投     CS      CS  
     18     -989           东航期货     CS      CS  
     19    -4227           长江期货     CS      CS  
     20   -88356           None     CS      CS  ,
     'A':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 7104                      74            国投安信     1   
     1                 6589                    -372            国泰君安     2   
     2                 6181                    -215            华安期货     3   
     3                 5889                     -37            中信期货     4   
     4                 4962                     -74            永安期货     5   
     5                 4609                     -14            华泰期货     6   
     6                 4562                    -197            银河期货     7   
     7                 4322                      67            五矿经易     8   
     8                 4298                    -596            广发期货     9   
     9                 3372                    1031            广州期货    10   
     10                3344                    -141            鲁证期货    11   
     11                3155                     -90            宏源期货    12   
     12                3024                    -180            海通期货    13   
     13                2924                    -102            徽商期货    14   
     14                2834                    -182            中大期货    15   
     15                2816                     -17            一德期货    16   
     16                2287                     -38            国信期货    17   
     17                2259                    1143            东证期货    18   
     18                2244                     239            浙商期货    19   
     19                2211                      34            广州金控    20   
     20               78986                     333            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                 12006                      286             国投安信  12795   
     1                 11507                     -347             中信期货   5930   
     2                 10065                       56             国泰君安   5282   
     3                  9165                     -255             华泰期货   4912   
     4                  7054                     -138             华安期货   3587   
     5                  6543                      258             永安期货   3578   
     6                  5946                     -330             兴证期货   3374   
     7                  5446                       45             中金期货   3156   
     8                  5345                        0             摩根大通   2846   
     9                  4940                     1356             东证期货   2639   
     10                 3404                     -164             南华期货   2569   
     11                 3378                      955             广州期货   2498   
     12                 3119                     -450             徽商期货   2447   
     13                 2944                      -32             海通期货   2330   
     14                 2746                       40             渤海期货   2185   
     15                 2740                      -10             天风期货   2065   
     16                 2412                      -30             银河期货   1849   
     17                 2232                       93             一德期货   1837   
     18                 1905                     -177             方正中期   1793   
     19                 1861                       11             西部期货   1739   
     20               104758                     1167             None  69411   
     
         vol_chg vol_party_name symbol variety  
     0     -1278           东证期货      A       A  
     1     -3070           海通期货      A       A  
     2     -7985           国泰君安      A       A  
     3     -2967           中信期货      A       A  
     4     -4477           华泰期货      A       A  
     5     -2904           徽商期货      A       A  
     6       917           广州期货      A       A  
     7     -5967           方正中期      A       A  
     8     -1207           永安期货      A       A  
     9      -198           东航期货      A       A  
     10    -2039           银河期货      A       A  
     11     -736           广发期货      A       A  
     12    -2786           兴证期货      A       A  
     13    -4092           国投安信      A       A  
     14     -892           长江期货      A       A  
     15    -6577           华安期货      A       A  
     16       94           中财期货      A       A  
     17    -2850           光大期货      A       A  
     18     -170           南华期货      A       A  
     19     -111           浙商期货      A       A  
     20   -49295           None      A       A  ,
     'B':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 4160                     183            徽商期货     1   
     1                 2512                      46            申银万国     2   
     2                 2278                       9            英大期货     3   
     3                 2259                     101            银河期货     4   
     4                 2057                      48            方正中期     5   
     5                 1817                      47            广州金控     6   
     6                 1630                      29            宏源期货     7   
     7                 1614                      13            瑞达期货     8   
     8                 1602                      24            永安期货     9   
     9                 1534                      31            国泰君安    10   
     10                1386                    -172            兴证期货    11   
     11                1370                      62            华安期货    12   
     12                1366                      39            国投安信    13   
     13                1347                    -126            国海良时    14   
     14                1346                      48            新湖期货    15   
     15                1317                      81            中信建投    16   
     16                1292                      18            浙商期货    17   
     17                1263                      16            中信期货    18   
     18                1255                    -174            南华期货    19   
     19                1240                     -28            华泰期货    20   
     20               34645                     295            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                  4655                        0             摩根大通   11046   
     1                  2378                      162             国投安信   11012   
     2                  2373                      -19             北京首创   10994   
     3                  2170                      118             宏源期货    7691   
     4                  2109                       20             银河期货    6340   
     5                  2067                      206             方正中期    6127   
     6                  1976                     -296             广州金控    6080   
     7                  1784                      223             徽商期货    6053   
     8                  1782                       28             永安期货    6019   
     9                  1594                      166             华泰期货    5998   
     10                 1532                        7             一德期货    5983   
     11                 1492                      155             倍特期货    5964   
     12                 1481                        0             五矿经易    5793   
     13                 1445                       -2             新湖期货    5570   
     14                 1377                       29             兴证期货    5529   
     15                 1341                       44             华安期货    5262   
     16                 1339                       -4             安粮期货    5219   
     17                 1326                       38             中银国际    5199   
     18                 1228                      112             国富期货    5154   
     19                 1221                        6             华西期货    5080   
     20                36670                      993             None  132113   
     
         vol_chg vol_party_name symbol variety  
     0     10865           中衍期货      B       B  
     1     10941           渤海期货      B       B  
     2     10966           兴业期货      B       B  
     3      -978           弘业期货      B       B  
     4     -4274           华安期货      B       B  
     5      -319           格林大华      B       B  
     6      1213           国信期货      B       B  
     7      2675           广州金控      B       B  
     8     -1497           中辉期货      B       B  
     9      1824           海证期货      B       B  
     10    -1303           申银万国      B       B  
     11     4485           长江期货      B       B  
     12      956           冠通期货      B       B  
     13     5146           北京首创      B       B  
     14     1380           鲁证期货      B       B  
     15     1176           长安期货      B       B  
     16      747           安粮期货      B       B  
     17    -4797           国联期货      B       B  
     18      750           英大期货      B       B  
     19      780           创元期货      B       B  
     20    40736           None      B       B  ,
     'M':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0               109144                    6695            永安期货     1   
     1                60179                   -2679            中粮期货     2   
     2                53823                   -4277            国投安信     3   
     3                50079                    3608            中信期货     4   
     4                49129                    1419            申银万国     5   
     5                35846                    1525            南华期货     6   
     6                35179                   -3542            东证期货     7   
     7                33971                     201            新湖期货     8   
     8                32279                     478            五矿经易     9   
     9                23965                     106            摩根大通    10   
     10               23932                     741            广发期货    11   
     11               21914                     736            格林大华    12   
     12               21128                    2048            国泰君安    13   
     13               20190                    2668            华泰期货    14   
     14               18716                   -1346            中国国际    15   
     15               17194                     612            光大期货    16   
     16               16808                    4155            浙商期货    17   
     17               16000                    2394            一德期货    18   
     18               14744                    1010            银河期货    19   
     19               14067                    1769            方正中期    20   
     20              668287                   18321            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                124646                     9837             永安期货  181781   
     1                 82863                     2355             国投安信   95047   
     2                 73811                    -5281             中粮期货   68570   
     3                 72701                     1938             摩根大通   61683   
     4                 68961                    -1144             银河期货   50373   
     5                 45193                      -49             新湖期货   48733   
     6                 43541                     5236             申银万国   44826   
     7                 38298                    -1357             国泰君安   39449   
     8                 35277                    -1187             广发期货   36787   
     9                 33468                      835             中国国际   33538   
     10                32995                     1223             中信期货   33231   
     11                25878                     -999             东证期货   29156   
     12                24665                       42             北京首创   28788   
     13                22544                    -3608             五矿经易   28781   
     14                21119                     1676             一德期货   28612   
     15                17339                       37             信达期货   28355   
     16                16636                     -439             华泰期货   27973   
     17                15548                      320             南华期货   27563   
     18                13749                       68             浙商期货   23549   
     19                13165                     1769             格林大华   23033   
     20               822397                    11272             None  939828   
     
         vol_chg vol_party_name symbol variety  
     0     13078           东证期货      M       M  
     1      5364           海通期货      M       M  
     2     13139           永安期货      M       M  
     3      -733           中信期货      M       M  
     4       -93           中信建投      M       M  
     5     -9582           国泰君安      M       M  
     6      2218           国投安信      M       M  
     7      -289           方正中期      M       M  
     8      -974           华泰期货      M       M  
     9     14058           宏源期货      M       M  
     10    14030           浙商期货      M       M  
     11     5238           徽商期货      M       M  
     12   -24446           银河期货      M       M  
     13     2862           申银万国      M       M  
     14     3672           中粮期货      M       M  
     15     2700           长江期货      M       M  
     16    -1993           兴证期货      M       M  
     17    -5130           光大期货      M       M  
     18     1283           南华期货      M       M  
     19    -3718           中国国际      M       M  
     20    30684           None      M       M  ,
     'Y':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                28978                    -261            永安期货     1   
     1                21556                     -72            五矿经易     2   
     2                20991                    -354            中信期货     3   
     3                20653                    1192            前海期货     4   
     4                20560                     741            中粮期货     5   
     5                19705                   -2818            银河期货     6   
     6                16916                      98            南华期货     7   
     7                16680                    -903            国投安信     8   
     8                15544                    2044            广发期货     9   
     9                14476                    -451            宝城期货    10   
     10               11372                    -128            浙商期货    11   
     11               10476                     512            申银万国    12   
     12               10203                     224            冠通期货    13   
     13                9203                     367            摩根大通    14   
     14                8890                   -1790            宏源期货    15   
     15                8888                     897            中国国际    16   
     16                8544                     261            光大期货    17   
     17                8114                     407            徽商期货    18   
     18                8041                     -81            东证期货    19   
     19                8033                     165            华泰期货    20   
     20              287823                      50            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 53211                     -904             中粮期货   56774   
     1                 42259                      487             国投安信   25574   
     2                 40471                    -1148             银河期货   18170   
     3                 28337                    -3536             建信期货   17760   
     4                 27021                     -290             摩根大通   15338   
     5                 26946                    -1493             永安期货   14836   
     6                 22157                     1724             广发期货   12978   
     7                 20676                     -866             中信期货   11764   
     8                 16841                      334             信达期货   10401   
     9                 13392                    -2878             宏源期货   10054   
     10                11760                      -38             上海中期    8716   
     11                10543                       44             北京首创    8595   
     12                10526                     -227             格林大华    8361   
     13                10244                     1295             渤海期货    8266   
     14                 9799                      -42             新湖期货    7396   
     15                 9762                      355             申银万国    6571   
     16                 8287                      734             华泰期货    6497   
     17                 8143                      -17             兴证期货    6021   
     18                 8013                     2826             国富期货    5351   
     19                 7813                       65             中金期货    5247   
     20               386201                    -3575             None  264670   
     
         vol_chg vol_party_name symbol variety  
     0    -24532           东证期货      Y       Y  
     1     -8263           海通期货      Y       Y  
     2    -14272           中信期货      Y       Y  
     3      6886           永安期货      Y       Y  
     4     -9853           银河期货      Y       Y  
     5     -8400           国投安信      Y       Y  
     6     -8968           国泰君安      Y       Y  
     7      -907           光大期货      Y       Y  
     8     -2776           方正中期      Y       Y  
     9     -9515           国元期货      Y       Y  
     10   -13336           广发期货      Y       Y  
     11    -5104           中粮期货      Y       Y  
     12    -4162           华泰期货      Y       Y  
     13    -2378           长江期货      Y       Y  
     14    -1351           宏源期货      Y       Y  
     15    -5739           徽商期货      Y       Y  
     16     2177           国富期货      Y       Y  
     17     -461           鲁证期货      Y       Y  
     18    -2733           建信期货      Y       Y  
     19     3175           信达期货      Y       Y  
     20  -110512           None      Y       Y  ,
     'P':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                15555                     657            永安期货     1   
     1                13503                      88            海通期货     2   
     2                12149                     193            宏源期货     3   
     3                11770                    -365            东证期货     4   
     4                11397                     246            国投安信     5   
     5                10832                    -139            中信建投     6   
     6                10574                    -481            中信期货     7   
     7                 9532                     101            中粮期货     8   
     8                 9252                     248            摩根大通     9   
     9                 8438                    2950            国富期货    10   
     10                7769                     151            银河期货    11   
     11                7527                     442            广发期货    12   
     12                7175                    -116            申银万国    13   
     13                6893                     177            方正中期    14   
     14                6858                    1026            徽商期货    15   
     15                6248                    -149            光大期货    16   
     16                5963                      79            华泰期货    17   
     17                5780                    -753            南华期货    18   
     18                5182                    -517            新湖期货    19   
     19                5084                      67            北京首创    20   
     20              177481                    3905            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 32382                      688             中粮期货   75557   
     1                 29287                     -139             银河期货   19965   
     2                 25278                     1662             国投安信   17808   
     3                 22231                     -430             国富期货   13397   
     4                 19764                      -98             中信期货   11136   
     5                 18746                     2057             广发期货   10296   
     6                 13140                     -484             华泰期货   10176   
     7                 12467                      980             永安期货   10149   
     8                  8684                     -444             申银万国    9779   
     9                  7663                      227             宏源期货    8982   
     10                 6841                       26             兴证期货    8884   
     11                 6470                     -150             海通期货    8848   
     12                 5334                       48             国泰君安    6705   
     13                 5148                      547             鲁证期货    6340   
     14                 5025                       11             中金期货    6284   
     15                 4432                      -59             国贸期货    5981   
     16                 4422                     -103             英大期货    5926   
     17                 4283                     -750             东证期货    5688   
     18                 4146                      288             一德期货    5513   
     19                 4038                       79             安粮期货    5416   
     20               239781                     3956             None  252830   
     
         vol_chg vol_party_name symbol variety  
     0      9059           东证期货      P       P  
     1       314           中信期货      P       P  
     2     -3360           海通期货      P       P  
     3       271           国泰君安      P       P  
     4     -3001           兴证期货      P       P  
     5      -192           国投安信      P       P  
     6     -1366           方正中期      P       P  
     7       383           永安期货      P       P  
     8      -639           广发期货      P       P  
     9      3930           宏源期货      P       P  
     10     -224           徽商期货      P       P  
     11    -1822           光大期货      P       P  
     12      944           华安期货      P       P  
     13     5408           深圳瑞龙      P       P  
     14     3284           国富期货      P       P  
     15    -1032           华泰期货      P       P  
     16    -5653           申银万国      P       P  
     17    -2978           银河期货      P       P  
     18    -1624           长江期货      P       P  
     19    -2722           国元期货      P       P  
     20    -1020           None      P       P  ,
     'JD':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 3708                    -286            方正中期     1   
     1                 3316                    -335            永安期货     2   
     2                 2750                     289            中信期货     3   
     3                 2666                     124            鲁证期货     4   
     4                 2621                      31            银河期货     5   
     5                 2572                    -216            招金期货     6   
     6                 1933                     -26            浙商期货     7   
     7                 1745                     -61            东证期货     8   
     8                 1688                     128            中信建投     9   
     9                 1634                      93            兴证期货    10   
     10                1592                     221            海通期货    11   
     11                1570                      29            弘业期货    12   
     12                1554                     158            东航期货    13   
     13                1552                    -174            中辉期货    14   
     14                1511                     196            广发期货    15   
     15                1493                    -107            广州期货    16   
     16                1472                     -42            华泰期货    17   
     17                1466                      78            徽商期货    18   
     18                1462                    -172            南华期货    19   
     19                1387                     133            格林大华    20   
     20               39692                      61            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  3676                     -726             中信建投   7805   
     1                  3604                     -180             永安期货   5910   
     2                  2884                      100             新湖期货   5370   
     3                  2839                      320             方正中期   4686   
     4                  2709                       56             国泰君安   3942   
     5                  2201                      454             宏源期货   3926   
     6                  2112                      132             中信期货   3859   
     7                  1994                      296             华泰期货   3825   
     8                  1946                     -156             九州期货   3689   
     9                  1926                     -272             徽商期货   2774   
     10                 1710                      -76             兴证期货   2496   
     11                 1690                      238             广发期货   2302   
     12                 1672                      253             光大期货   2115   
     13                 1584                      207             银河期货   2086   
     14                 1534                      -28             华安期货   2057   
     15                 1486                       36             和合期货   1974   
     16                 1483                      220             东航期货   1922   
     17                 1343                      100             海通期货   1901   
     18                 1336                      208             申银万国   1874   
     19                 1263                      465             国投安信   1873   
     20                40992                     1647             None  66386   
     
         vol_chg vol_party_name symbol variety  
     0       967           海通期货     JD      JD  
     1      2050           东证期货     JD      JD  
     2       802           方正中期     JD      JD  
     3       421           徽商期货     JD      JD  
     4       218           华泰期货     JD      JD  
     5      1737           中信建投     JD      JD  
     6       730           中信期货     JD      JD  
     7      -159           永安期货     JD      JD  
     8        72           国泰君安     JD      JD  
     9      -233           华安期货     JD      JD  
     10      169           银河期货     JD      JD  
     11      133           国投安信     JD      JD  
     12     -306           申银万国     JD      JD  
     13      686           国信期货     JD      JD  
     14     -337           光大期货     JD      JD  
     15     -317           广发期货     JD      JD  
     16      245           东航期货     JD      JD  
     17     -200           招金期货     JD      JD  
     18     -211           宏源期货     JD      JD  
     19      402           南华期货     JD      JD  
     20     6869           None     JD      JD  ,
     'L':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                40097                     228            永安期货     1   
     1                17503                    -123            华泰期货     2   
     2                12938                    2637            弘业期货     3   
     3                11123                     313            方正中期     4   
     4                11021                      95            浙商期货     5   
     5                 9563                     867            国投安信     6   
     6                 8455                    -613            建信期货     7   
     7                 7280                     -84            南华期货     8   
     8                 6690                     288            宏源期货     9   
     9                 6657                     264            大地期货    10   
     10                6613                    -125            一德期货    11   
     11                6390                    1535            大越期货    12   
     12                5949                    -103            中信期货    13   
     13                5660                    -611            申银万国    14   
     14                5524                      21            鲁证期货    15   
     15                5392                      -4            银河期货    16   
     16                5386                     469            东证期货    17   
     17                5326                    -156            广发期货    18   
     18                4962                    -149            宝城期货    19   
     19                4834                    -225            徽商期货    20   
     20              187363                    4524            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 72659                    -1704             永安期货   49426   
     1                 29035                      272             申银万国   27538   
     2                 13421                     -900             国投安信   17302   
     3                 11523                    -2112             海通期货   16159   
     4                 10774                    -1179             华泰期货   15225   
     5                 10470                      601             银河期货   14759   
     6                  8876                      504             国泰君安   13682   
     7                  8655                     -752             中信期货    8004   
     8                  7772                     1365             光大期货    6806   
     9                  6347                      894             浙商期货    6599   
     10                 6019                       -7             中金期货    5764   
     11                 5926                      117             中财期货    4863   
     12                 5528                     1425             金瑞期货    4481   
     13                 5267                       16             国海良时    4200   
     14                 5264                     2783             信达期货    3986   
     15                 5079                     -817             东证期货    3568   
     16                 4792                      -45             建信期货    3479   
     17                 4649                      111             新湖期货    3386   
     18                 4483                      -23             五矿经易    3351   
     19                 4391                    -2010             中粮期货    3299   
     20               230930                    -1461             None  215877   
     
         vol_chg vol_party_name symbol variety  
     0      7564           东证期货      L       L  
     1      3143           光大期货      L       L  
     2      -509           海通期货      L       L  
     3      4198           中信期货      L       L  
     4      1763           国泰君安      L       L  
     5      2769           方正中期      L       L  
     6      1369           永安期货      L       L  
     7      1284           弘业期货      L       L  
     8     -1324           华泰期货      L       L  
     9     -2220           国投安信      L       L  
     10     2950           东航期货      L       L  
     11     2132           宏源期货      L       L  
     12    -2288           南华期货      L       L  
     13     -397           徽商期货      L       L  
     14    -3152           兴证期货      L       L  
     15     1667           国信期货      L       L  
     16     2859           信达期货      L       L  
     17     1464           中粮期货      L       L  
     18      856           银河期货      L       L  
     19     1480           浙商期货      L       L  
     20    25608           None      L       L  ,
     'V':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                37000                    1024            永安期货     1   
     1                15079                   -1178            方正中期     2   
     2                 9390                    -744            中信期货     3   
     3                 9058                    4519            建信期货     4   
     4                 8748                    1560            南华期货     5   
     5                 7311                    2493            申银万国     6   
     6                 6665                    -952            国投安信     7   
     7                 5791                    1297            中财期货     8   
     8                 5580                   -1415            兴证期货     9   
     9                 5065                    -847            国泰君安    10   
     10                3944                    -169            东证期货    11   
     11                3779                     303            宏源期货    12   
     12                3624                    -193            海证期货    13   
     13                3414                     349            光大期货    14   
     14                3385                     174            国贸期货    15   
     15                3371                      53            浙商期货    16   
     16                3109                     184            国金期货    17   
     17                2906                     143            国联期货    18   
     18                2857                     271            西部期货    19   
     19                2821                    -136            广州期货    20   
     20              142897                    6736            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 28130                    -2987             永安期货   36425   
     1                 23840                      240             国泰君安   24408   
     2                 11434                      564             申银万国   15531   
     3                 11135                     3057             国投安信   15415   
     4                  8101                       86             招商期货   15007   
     5                  5475                    -1126             宝城期货   14721   
     6                  5053                     -103             华泰期货   12589   
     7                  4658                     3356             中粮期货   12441   
     8                  4439                      228             宏源期货   11161   
     9                  4236                     2342             东证期货    8021   
     10                 4108                      222             中信期货    7064   
     11                 4003                     -436             银河期货    6378   
     12                 3565                      323             中金期货    5354   
     13                 3535                      114             南华期货    5034   
     14                 3485                     -298             中财期货    4817   
     15                 3393                      303             信达期货    4482   
     16                 3129                      115             华安期货    4273   
     17                 2861                      489             徽商期货    4179   
     18                 2666                    -2170             兴证期货    4054   
     19                 2551                      -13             新湖期货    4047   
     20               139797                     4306             None  215401   
     
         vol_chg vol_party_name symbol variety  
     0     15193           东证期货      V       V  
     1      4300           中信期货      V       V  
     2      7990           光大期货      V       V  
     3      5310           永安期货      V       V  
     4      6769           兴证期货      V       V  
     5     -2098           海通期货      V       V  
     6      2415           国泰君安      V       V  
     7      6361           方正中期      V       V  
     8       111           申银万国      V       V  
     9      4601           国投安信      V       V  
     10     3797           银河期货      V       V  
     11     3883           东航期货      V       V  
     12     3010           徽商期货      V       V  
     13      408           建信期货      V       V  
     14     1840           中财期货      V       V  
     15      375           长江期货      V       V  
     16     2339           广发期货      V       V  
     17       28           华泰期货      V       V  
     18     3412           中粮期货      V       V  
     19     1769           大有期货      V       V  
     20    71813           None      V       V  ,
     'PP':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                44605                   -4128            永安期货     1   
     1                15329                   -5429            申银万国     2   
     2                11891                    1075            建信期货     3   
     3                11280                   -1771            国投安信     4   
     4                10173                     575            南华期货     5   
     5                 8613                     -58            国泰君安     6   
     6                 8065                    1323            前海期货     7   
     7                 7198                     900            弘业期货     8   
     8                 6893                    2605            一德期货     9   
     9                 6834                    -713            华泰期货    10   
     10                6688                    -163            中信期货    11   
     11                6597                     429            银河期货    12   
     12                6291                   -1197            浙商期货    13   
     13                5701                     289            信达期货    14   
     14                4783                      10            中粮期货    15   
     15                4430                     621            兴证期货    16   
     16                4262                      75            国海良时    17   
     17                4164                     343            东证期货    18   
     18                4011                     736            光大期货    19   
     19                3941                     990            五矿经易    20   
     20              181749                   -3488            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 36942                      273             永安期货   46271   
     1                 23333                     1742             国泰君安   33432   
     2                 11807                    -1754             银河期货   29042   
     3                  9376                     1096             浙商期货   26572   
     4                  9183                     -243             中财期货   25634   
     5                  8416                     -549             中粮期货   23599   
     6                  8183                    -2604             南华期货   19196   
     7                  8101                      706             前海期货   17944   
     8                  6751                     -534             华泰期货   17375   
     9                  6733                      351             中信期货   14861   
     10                 6460                     1675             方正中期   14339   
     11                 6373                       50             信达期货   13329   
     12                 5350                     -582             弘业期货   11585   
     13                 4612                       62             铜冠金源   10412   
     14                 4421                      121             新湖期货    9679   
     15                 4121                     -623             国投安信    9523   
     16                 3941                       73             徽商期货    9456   
     17                 3772                      438             海通期货    9122   
     18                 3509                     -574             兴证期货    8921   
     19                 3444                     -472             东证期货    8843   
     20               174828                    -1348             None  359135   
     
         vol_chg vol_party_name symbol variety  
     0     -6007           东证期货     PP      PP  
     1    -19193           海通期货     PP      PP  
     2    -19102           方正中期     PP      PP  
     3    -10265           国泰君安     PP      PP  
     4     -8282           中信期货     PP      PP  
     5     -1639           光大期货     PP      PP  
     6      5582           申银万国     PP      PP  
     7     -9586           徽商期货     PP      PP  
     8     -3645           华泰期货     PP      PP  
     9     -4805           永安期货     PP      PP  
     10     3035           东海期货     PP      PP  
     11    -4013           浙商期货     PP      PP  
     12    -4622           南华期货     PP      PP  
     13    -4884           弘业期货     PP      PP  
     14    -8284           兴证期货     PP      PP  
     15    -3065           东航期货     PP      PP  
     16    -9795           华安期货     PP      PP  
     17    -4605           国投安信     PP      PP  
     18     -410           国信期货     PP      PP  
     19    -5048           银河期货     PP      PP  
     20  -118633           None     PP      PP  ,
     'J':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                19206                   -1423            海通期货     1   
     1                15777                    1417            中信期货     2   
     2                14539                   -2768            永安期货     3   
     3                11549                    -883            光大期货     4   
     4                10487                   -3632            国泰君安     5   
     5                 9697                   -4195            国富期货     6   
     6                 9518                    -130            东证期货     7   
     7                 8641                     722            国投安信     8   
     8                 8442                    -255            方正中期     9   
     9                 6999                   -1783            广发期货    10   
     10                6941                   -2146            鲁证期货    11   
     11                6258                      25            大越期货    12   
     12                6198                     469            申银万国    13   
     13                5599                     301            大地期货    14   
     14                5436                    -357            华泰期货    15   
     15                5206                     157            一德期货    16   
     16                4246                     -64            浙商期货    17   
     17                4016                    -133            银河期货    18   
     18                3799                      57            信达期货    19   
     19                3791                    -706            兴证期货    20   
     20              166345                  -15327            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 18877                      552             海通期货   86561   
     1                 17805                    -3475             国泰君安   47845   
     2                 15390                      682             中信期货   44346   
     3                 12144                     1206             永安期货   43883   
     4                 10900                     -935             光大期货   40377   
     5                 10467                     -217             东证期货   39291   
     6                  9827                      542             浙商期货   32450   
     7                  9373                    -4694             国富期货   31759   
     8                  9137                      414             方正中期   26540   
     9                  7930                     -441             华泰期货   26003   
     10                 6252                     -505             银河期货   24765   
     11                 6025                     1370             申银万国   24080   
     12                 5573                    -2339             广发期货   20504   
     13                 4538                      587             中粮期货   18021   
     14                 4359                      125             国投安信   15958   
     15                 3850                     -161             一德期货   15301   
     16                 3620                     -982             国信期货   15170   
     17                 3479                      693             兴证期货   14409   
     18                 3351                      -94             南华期货   14006   
     19                 3222                     -365             东方财富   13563   
     20               166119                    -8037             None  594832   
     
         vol_chg vol_party_name symbol variety  
     0     -9407           海通期货      J       J  
     1      1413           国富期货      J       J  
     2      3438           光大期货      J       J  
     3     -2820           国泰君安      J       J  
     4     -6764           东证期货      J       J  
     5     -8210           中信期货      J       J  
     6    -12155           永安期货      J       J  
     7      2513           申银万国      J       J  
     8     -9223           广发期货      J       J  
     9     -6328           方正中期      J       J  
     10    -8806           徽商期货      J       J  
     11    -3851           华泰期货      J       J  
     12    -4781           华安期货      J       J  
     13    -4790           东方财富      J       J  
     14    -4291           中信建投      J       J  
     15    -2340           国投安信      J       J  
     16    -4264           银河期货      J       J  
     17    -6815           兴证期货      J       J  
     18    -2061           中辉期货      J       J  
     19    -4707           国信期货      J       J  
     20   -94249           None      J       J  ,
     'JM':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                12991                     629            永安期货     1   
     1                10184                   -1405            海通期货     2   
     2                 9569                   -1801            中信期货     3   
     3                 8853                   -4456            国泰君安     4   
     4                 8787                     223            银河期货     5   
     5                 7947                   -6516            东证期货     6   
     6                 5812                     298            格林大华     7   
     7                 5785                    -337            南华期货     8   
     8                 5765                    -239            国投安信     9   
     9                 5636                     137            华泰期货    10   
     10                5097                    -927            兴证期货    11   
     11                4728                      29            中金期货    12   
     12                4170                     -47            英大期货    13   
     13                4004                    -286            天风期货    14   
     14                3967                    -361            一德期货    15   
     15                3258                    -746            广发期货    16   
     16                3234                    -610            国贸期货    17   
     17                3084                     -71            五矿经易    18   
     18                2980                     707            浙商期货    19   
     19                2840                    -158            方正中期    20   
     20              118691                  -15937            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 13219                     -617             海通期货   37523   
     1                 10402                       -9             永安期货   29352   
     2                  9574                     -206             华泰期货   18979   
     3                  9153                    -6941             东证期货   14816   
     4                  8453                     -839             中信期货   11953   
     5                  8220                     -855             银河期货   11747   
     6                  7843                    -1019             方正中期   10008   
     7                  7307                    -4503             国泰君安    9883   
     8                  6061                     -215             国投安信    9027   
     9                  5442                      159             浙商期货    7940   
     10                 4686                     -939             中粮期货    7775   
     11                 4434                     -339             广发期货    6466   
     12                 3931                      113             国富期货    6246   
     13                 3828                     -256             徽商期货    5946   
     14                 2926                      259             格林大华    5845   
     15                 2893                      414             申银万国    5722   
     16                 2776                     -176             东航期货    5223   
     17                 2696                      -52             一德期货    5162   
     18                 2516                      476             鲁证期货    5085   
     19                 2420                     -307             光大期货    3909   
     20               118780                   -15852             None  218607   
     
         vol_chg vol_party_name symbol variety  
     0     -6830           东证期货     JM      JM  
     1     -5470           海通期货     JM      JM  
     2     -5879           国泰君安     JM      JM  
     3     -3171           中信期货     JM      JM  
     4      -769           国富期货     JM      JM  
     5     -3105           方正中期     JM      JM  
     6     -5001           兴证期货     JM      JM  
     7     -4078           广发期货     JM      JM  
     8     -4674           华泰期货     JM      JM  
     9     -4526           光大期货     JM      JM  
     10    -8928           徽商期货     JM      JM  
     11    -6554           永安期货     JM      JM  
     12    -1321           国投安信     JM      JM  
     13    -6253           银河期货     JM      JM  
     14      -60           鲁证期货     JM      JM  
     15    -4780           华安期货     JM      JM  
     16    -2705           申银万国     JM      JM  
     17    -1635           国信期货     JM      JM  
     18    -2169           中信建投     JM      JM  
     19    -2559           一德期货     JM      JM  
     20   -80467           None     JM      JM  ,
     'I':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                34546                   -2152            永安期货     1   
     1                28303                    1572            一德期货     2   
     2                19064                    3900            鲁证期货     3   
     3                17860                   -8172            银河期货     4   
     4                17125                    2768            国泰君安     5   
     5                13910                    2324            申银万国     6   
     6                13879                   -1905            中信期货     7   
     7                13159                    3700            冠通期货     8   
     8                12025                    -610            国投安信     9   
     9                10776                    1041            大地期货    10   
     10               10690                      -4            大越期货    11   
     11               10446                    5985            中投期货    12   
     12               10213                    -240            广发期货    13   
     13               10097                    -521            华泰期货    14   
     14                9052                    -674            海通期货    15   
     15                8059                   -1093            渤海期货    16   
     16                7533                   -1166            徽商期货    17   
     17                7414                     295            中粮期货    18   
     18                7404                     590            北京金鹏    19   
     19                6789                    -396            光大期货    20   
     20              268344                    5242            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 46963                    -3896             永安期货  130822   
     1                 30911                    -2479             方正中期  100956   
     2                 27388                     1301             银河期货   76607   
     3                 27024                    -1126             中信期货   63948   
     4                 16446                     -191             一德期货   58813   
     5                 12401                     1266             中粮期货   51630   
     6                 12178                    -3488             鲁证期货   48362   
     7                 11729                     1330             国投安信   41051   
     8                 11620                      292             徽商期货   34554   
     9                 11577                      971             国泰君安   32586   
     10                10458                      384             海通期货   29666   
     11                10038                      906             国贸期货   29196   
     12                 9827                     -106             东证期货   26127   
     13                 8865                      763             光大期货   25944   
     14                 7413                      215             建信期货   21745   
     15                 6441                     -389             招商期货   21190   
     16                 6432                      273             中国国际   21050   
     17                 6139                      782             江苏东华   20644   
     18                 5254                      -43             创元期货   20548   
     19                 5240                      -29             华泰期货   19759   
     20               284344                    -3264             None  875198   
     
         vol_chg vol_party_name symbol variety  
     0     -2928           东证期货      I       I  
     1    -11754           冠通期货      I       I  
     2     24650           中信期货      I       I  
     3     21824           永安期货      I       I  
     4     15435           银河期货      I       I  
     5      1591           海通期货      I       I  
     6     -3680           国投安信      I       I  
     7      6183           国泰君安      I       I  
     8     16147           国富期货      I       I  
     9      4920           徽商期货      I       I  
     10    -8076           方正中期      I       I  
     11    18987           西部期货      I       I  
     12    -2308           光大期货      I       I  
     13     8125           中信建投      I       I  
     14      637           安粮期货      I       I  
     15     8959           鲁证期货      I       I  
     16     6252           申银万国      I       I  
     17     3601           广发期货      I       I  
     18     3526           国海良时      I       I  
     19    11259           东吴期货      I       I  
     20   123350           None      I       I  ,
     'EG':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 4410                    4410            新湖期货     1   
     1                 3936                    3936            方正中期     2   
     2                 2346                    2346            中信期货     3   
     3                 2205                    2205            国泰君安     4   
     4                 1970                    1970            华泰期货     5   
     5                 1132                    1132            永安期货     6   
     6                 1032                    1032            中大期货     7   
     7                  903                     903            信达期货     8   
     8                  814                     814            东海期货     9   
     9                  737                     737            南华期货    10   
     10                 726                     726            徽商期货    11   
     11                 712                     712            国贸期货    12   
     12                 659                     659            中州期货    13   
     13                 594                     594            东吴期货    14   
     14                 481                     481            华安期货    15   
     15                 473                     473            宝城期货    16   
     16                 466                     466            渤海期货    17   
     17                 462                     462            弘业期货    18   
     18                 459                     459            安粮期货    19   
     19                 453                     453            银河期货    20   
     20               24970                   24970            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                  5946                     5946             银河期货   33635   
     1                  3364                     3364             浙商期货   29689   
     2                  2208                     2208             东吴期货   26131   
     3                  1602                     1602             永安期货   26050   
     4                  1589                     1589             五矿经易   25943   
     5                  1246                     1246             海通期货   18793   
     6                  1103                     1103             中信期货   18319   
     7                  1068                     1068             信达期货   18223   
     8                  1011                     1011             国泰君安   18121   
     9                  1001                     1001             国投安信   16453   
     10                  781                      781             长江期货   16348   
     11                  776                      776             国信期货   16161   
     12                  771                      771             国海良时   14627   
     13                  740                      740             建信期货   14330   
     14                  643                      643             华泰期货   13159   
     15                  634                      634             中信建投   12124   
     16                  624                      624             广州期货   11832   
     17                  530                      530             金瑞期货   11470   
     18                  472                      472             方正中期   10940   
     19                  365                      365             大地期货   10509   
     20                26474                    26474             None  362857   
     
         vol_chg vol_party_name symbol variety  
     0     33635           徽商期货     EG      EG  
     1     29689           银河期货     EG      EG  
     2     26131           华安期货     EG      EG  
     3     26050           中信建投     EG      EG  
     4     25943           华泰期货     EG      EG  
     5     18793           创元期货     EG      EG  
     6     18319           新湖期货     EG      EG  
     7     18223           东航期货     EG      EG  
     8     18121           海通期货     EG      EG  
     9     16453           广州金控     EG      EG  
     10    16348           国泰君安     EG      EG  
     11    16161           中信期货     EG      EG  
     12    14627           兴证期货     EG      EG  
     13    14330           方正中期     EG      EG  
     14    13159           国富期货     EG      EG  
     15    12124           华信期货     EG      EG  
     16    11832           东证期货     EG      EG  
     17    11470           宏源期货     EG      EG  
     18    10940           广发期货     EG      EG  
     19    10509           冠通期货     EG      EG  
     20   362857           None     EG      EG  }




```python
ak.get_czce_rank_table('20181210')
```




    {'AP':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 9313                      76            一德期货     1   
     1                 7156                     -47            中信期货     2   
     2                 5646                     -90            申银万国     3   
     3                 5080                    -156            浙商期货     4   
     4                 4993                     208            永安期货     5   
     5                 4959                      80            东证期货     6   
     6                 4815                     394            中辉期货     7   
     7                 4588                    -353            海通期货     8   
     8                 4463                     -51            国泰君安     9   
     9                 4292                    -249            华泰期货    10   
     10                3940                     -14            中信建投    11   
     11                3785                     135            光大期货    12   
     12                3734                     196            鲁证期货    13   
     13                3620                     -66            国信期货    14   
     14                3260                     154            方正中期    15   
     15                3175                    -108            华安期货    16   
     16                3097                     111            宏源期货    17   
     17                3003                     161            东航期货    18   
     18                2689                     -24            国海良时    19   
     19                2621                     -56            南华期货    20   
     20               88229                     301            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                  8036                      396             方正中期   18240   
     1                  5940                     -357             国泰君安   12985   
     2                  5693                     -252             永安期货    8039   
     3                  5460                      185             华泰期货    7454   
     4                  4657                     -171             海通期货    7136   
     5                  4644                       58             银河期货    6832   
     6                  4376                      396             徽商期货    6386   
     7                  4062                      -65             南华期货    5490   
     8                  3984                      -30             光大期货    5336   
     9                  3970                     -169             中信期货    5324   
     10                 3854                     -172             申银万国    5228   
     11                 3816                        0             国海良时    5196   
     12                 3567                     -229             广发期货    3559   
     13                 3326                      -24             宏源期货    3492   
     14                 3250                      -56             中信建投    3363   
     15                 3204                      104             浙商期货    3292   
     16                 2909                      -16           国投安信期货    3266   
     17                 2867                       72             华安期货    3164   
     18                 2544                     -163             东证期货    3056   
     19                 2312                       19             金元期货    2985   
     20                82471                     -474             None  119823   
     
         vol_chg vol_party_name symbol variety  
     0     -4568           海通期货     AP      AP  
     1     -1938           东证期货     AP      AP  
     2     -2998           光大期货     AP      AP  
     3     -1396           徽商期货     AP      AP  
     4     -2323           中信期货     AP      AP  
     5     -2900           华泰期货     AP      AP  
     6     -1711           建信期货     AP      AP  
     7     -3515           国泰君安     AP      AP  
     8     -1590           华安期货     AP      AP  
     9     -2548           方正中期     AP      AP  
     10     -401           申银万国     AP      AP  
     11    -2921           创元期货     AP      AP  
     12     -891           宏源期货     AP      AP  
     13      321           中财期货     AP      AP  
     14    -1638           东航期货     AP      AP  
     15     -903           浙商期货     AP      AP  
     16    -1020           银河期货     AP      AP  
     17    -1127           金瑞期货     AP      AP  
     18     -760           中辉期货     AP      AP  
     19     -463           安粮期货     AP      AP  
     20   -35290           None     AP      AP  ,
     'CF':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                21556                    1425            中信期货     1   
     1                16050                    2117          国投安信期货     2   
     2                14328                   -1381            永安期货     3   
     3                 9942                     122            中国国际     4   
     4                 9901                     866            东证期货     5   
     5                 7938                      52          格林大华期货     6   
     6                 7894                     -47            上海中期     7   
     7                 7123                     -10            中粮期货     8   
     8                 5714                     527            国泰君安     9   
     9                 5531                    -371            长江期货    10   
     10                5304                    -251            华泰期货    11   
     11                5117                     103            方正中期    12   
     12                5103                    -156            华信期货    13   
     13                4933                    -478            银河期货    14   
     14                4662                      68            一德期货    15   
     15                4484                     368            光大期货    16   
     16                4347                      27            广发期货    17   
     17                4227                     120            建信期货    18   
     18                3604                     465            首创期货    19   
     19                3468                     217            浙商期货    20   
     20              151226                    3783            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 16609                     1465             东证期货   24828   
     1                 14094                      242             永安期货    9825   
     2                 11866                      270           格林大华期货    8541   
     3                 11741                      288             中粮期货    8141   
     4                 11686                     -566             中信期货    8024   
     5                 10378                      521           国投安信期货    7613   
     6                 10305                      -29             金瑞期货    6707   
     7                 10288                      166             华信期货    6260   
     8                  9812                     -147             华泰期货    5984   
     9                  7949                     -367             兴证期货    5000   
     10                 7922                     -180             宏源期货    4844   
     11                 7761                     -103             长江期货    4823   
     12                 7612                        3             国贸期货    4561   
     13                 7410                      -63             中国国际    4363   
     14                 6763                      -48             中金期货    4056   
     15                 6613                      294             建信期货    3479   
     16                 5568                      425             国泰君安    3431   
     17                 4782                      230             光大期货    3220   
     18                 4695                     -343             大有期货    3191   
     19                 4680                      -76             兴业期货    3163   
     20               178534                     1982             None  130054   
     
         vol_chg vol_party_name symbol variety  
     0     11508           华泰期货     CF      CF  
     1      5253           东证期货     CF      CF  
     2      5155           华安期货     CF      CF  
     3      2734           中信期货     CF      CF  
     4      4534           中辉期货     CF      CF  
     5      3311           宏源期货     CF      CF  
     6      1304           永安期货     CF      CF  
     7      4880         国投安信期货     CF      CF  
     8      3327           海通期货     CF      CF  
     9      2744           南华期货     CF      CF  
     10     2708           国泰君安     CF      CF  
     11     1302           新湖期货     CF      CF  
     12     2328           方正中期     CF      CF  
     13     2449           徽商期货     CF      CF  
     14     1841           光大期货     CF      CF  
     15     2338           银河期货     CF      CF  
     16     1623           冠通期货     CF      CF  
     17     2396           国信期货     CF      CF  
     18     2142           申银万国     CF      CF  
     19     2677           金石期货     CF      CF  
     20    66554           None     CF      CF  ,
     'CY':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                   64                      -4            永安期货     1   
     1                   61                     -32            中信期货     2   
     2                   51                       3            银河期货     3   
     3                   44                       2            浙商期货     4   
     4                   25                       3            大有期货     5   
     5                   24                       0            金石期货     6   
     6                   24                       0            海通期货     7   
     7                   20                       1            华泰期货     8   
     8                   20                       1            道通期货     9   
     9                   18                       1            国泰君安    10   
     10                  17                       0            东航期货    11   
     11                  16                       0           浙江新世纪    12   
     12                  11                       0           新纪元期货    13   
     13                  11                       1            徽商期货    14   
     14                  10                      -1            国信期货    15   
     15                   9                     -36            方正中期    16   
     16                   9                       0            金鹏期货    17   
     17                   9                       4            华安期货    18   
     18                   8                       3            中原期货    19   
     19                   8                      -1            光大期货    20   
     20                 459                     -55            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                   135                        0             国泰君安   70   
     1                    68                       -4             银河期货   61   
     2                    66                       -6             华泰期货   58   
     3                    57                        1             永安期货   49   
     4                    27                        0             华安期货   48   
     5                    26                        0             东方财富   41   
     6                    19                        1             申银万国   38   
     7                    17                        6             中大期货   37   
     8                    15                        1             长江期货   33   
     9                    15                        0             中原期货   26   
     10                   12                       -7             弘业期货   24   
     11                   12                        0             大连良运   23   
     12                   11                        0            浙江新世纪   23   
     13                   11                        0             广州金控   22   
     14                    9                        6             创元期货   21   
     15                    8                        0             中国国际   20   
     16                    8                       -8             兴证期货   17   
     17                    6                        0             江西瑞奇   16   
     18                    6                        0             中信期货   16   
     19                    6                        0             中粮期货   15   
     20                  534                      -10             None  658   
     
         vol_chg vol_party_name symbol variety  
     0        28           东证期货     CY      CY  
     1        27           华泰期货     CY      CY  
     2        34           中信期货     CY      CY  
     3        -6           海通期货     CY      CY  
     4        11           方正中期     CY      CY  
     5        19           国信期货     CY      CY  
     6         1           光大期货     CY      CY  
     7       -21           兴证期货     CY      CY  
     8       -10           东航期货     CY      CY  
     9         5           徽商期货     CY      CY  
     10       14           神华期货     CY      CY  
     11        6         国投安信期货     CY      CY  
     12        8           银河期货     CY      CY  
     13      -10           中辉期货     CY      CY  
     14        1           弘业期货     CY      CY  
     15       12           安粮期货     CY      CY  
     16      -57           永安期货     CY      CY  
     17       14          新纪元期货     CY      CY  
     18       13           海证期货     CY      CY  
     19       14           国联期货     CY      CY  
     20      103           None     CY      CY  ,
     'FG':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                14446                   -4131            永安期货     1   
     1                 6151                     267            中信期货     2   
     2                 5354                    1642            国泰君安     3   
     3                 5265                    -633            华泰期货     4   
     4                 4949                   -1457            海通期货     5   
     5                 4912                     343            兴证期货     6   
     6                 4283                      32            银河期货     7   
     7                 3682                    -161            方正中期     8   
     8                 3574                    -609          国投安信期货     9   
     9                 3501                     -97            宏源期货    10   
     10                2514                   -1814            新湖期货    11   
     11                2294                      -5            国信期货    12   
     12                2178                   -1414            光大期货    13   
     13                2168                      66            徽商期货    14   
     14                2158                    -201            东证期货    15   
     15                2100                     251            东航期货    16   
     16                2029                    -204            西部期货    17   
     17                1605                    -147            广发期货    18   
     18                1412                     297            华安期货    19   
     19                1289                     253            南华期货    20   
     20               75864                   -7722            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  9926                     -143             永安期货  10994   
     1                  7041                      161             国泰君安   9172   
     2                  6178                       87             中信期货   7032   
     3                  5249                    -2550             海通期货   6669   
     4                  4805                     -845             方正中期   6591   
     5                  3907                      508             中粮期货   5904   
     6                  3266                    -1281             华泰期货   5804   
     7                  3027                    -1654             新湖期货   5327   
     8                  3006                      685             南华期货   4977   
     9                  2816                      460             广发期货   4601   
     10                 2814                     -348             徽商期货   4349   
     11                 2696                    -1713             光大期货   4112   
     12                 2532                      -60             摩根大通   3758   
     13                 2356                     -608             宏源期货   2899   
     14                 2237                     -382             东证期货   2772   
     15                 2214                     -127             弘业期货   2508   
     16                 2172                      403             银河期货   2506   
     17                 2118                     -552             兴证期货   1986   
     18                 2042                      -77             上海东方   1933   
     19                 1698                     -214             华安期货   1873   
     20                72100                    -8250             None  95767   
     
         vol_chg vol_party_name symbol variety  
     0     -4132           新湖期货     FG      FG  
     1     -3950           永安期货     FG      FG  
     2      -969           华泰期货     FG      FG  
     3      -761           海通期货     FG      FG  
     4     -1459           国泰君安     FG      FG  
     5       268           方正中期     FG      FG  
     6      -374           中信期货     FG      FG  
     7     -1564           华安期货     FG      FG  
     8     -1995           光大期货     FG      FG  
     9     -1577           东证期货     FG      FG  
     10    -1165           宏源期货     FG      FG  
     11    -2177           徽商期货     FG      FG  
     12      310           南华期货     FG      FG  
     13     -350           银河期货     FG      FG  
     14      313         国投安信期货     FG      FG  
     15     -358           申银万国     FG      FG  
     16      466           长江期货     FG      FG  
     17    -1086           东航期货     FG      FG  
     18      122           大地期货     FG      FG  
     19     -295           广发期货     FG      FG  
     20   -20733           None     FG      FG  ,
     'JR':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                   44                       0            深圳瑞龙     1   
     1                   37                       0            西南期货     2   
     2                   35                       0            永安期货     3   
     3                   22                       0            英大期货     4   
     4                   15                       0            东方财富     5   
     5                   13                       0            国金期货     6   
     6                   11                       0            华安期货     7   
     7                    8                       0            鲁证期货     8   
     8                    8                       0           浙江新世纪     9   
     9                    7                       0            银河期货    10   
     10                   6                       0            华泰期货    11   
     11                   6                       0            徽商期货    12   
     12                   5                       0            中大期货    13   
     13                   4                       0            弘业期货    14   
     14                   4                       0            长江期货    15   
     15                   4                       0            兴业期货    16   
     16                   4                       0            东吴期货    17   
     17                   3                       0            申银万国    18   
     18                   3                       0            方正中期    19   
     19                   3                       0            中信期货    20   
     20                 242                       0            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                   184                        0             一德期货    1   
     1                    80                        0             中信期货    1   
     2                    22                        0             英大期货    0   
     3                    12                       -1           国投安信期货    0   
     4                     1                        0             中粮期货    0   
     5                     1                        0             东证期货    0   
     6                     1                        0             光大期货    0   
     7                     0                        0            新纪元期货    0   
     8                     0                        0             华泰期货    0   
     9                     0                        0             招商期货    0   
     10                    0                        0             中财期货    0   
     11                    0                        0             国信期货    0   
     12                    0                        0             弘业期货    0   
     13                    0                        0             徽商期货    0   
     14                    0                        0             申银万国    0   
     15                    0                        0             方正中期    0   
     16                    0                        0             国元期货    0   
     17                    0                        0             银河期货    0   
     18                    0                        0             鲁证期货    0   
     19                    0                        0             西南期货    0   
     20                  301                       -1             None    2   
     
         vol_chg vol_party_name symbol variety  
     0         0         国投安信期货     JR      JR  
     1         1           中国国际     JR      JR  
     2         0          新纪元期货     JR      JR  
     3         0           华泰期货     JR      JR  
     4         0           招商期货     JR      JR  
     5        -2           中财期货     JR      JR  
     6         0           国信期货     JR      JR  
     7         0           弘业期货     JR      JR  
     8         0           徽商期货     JR      JR  
     9        -1           申银万国     JR      JR  
     10        0           方正中期     JR      JR  
     11        0           国元期货     JR      JR  
     12        0           银河期货     JR      JR  
     13        0           中信期货     JR      JR  
     14        0           鲁证期货     JR      JR  
     15        0           中粮期货     JR      JR  
     16        0           西南期货     JR      JR  
     17        0           长江期货     JR      JR  
     18        0           津投期货     JR      JR  
     19        0           南证期货     JR      JR  
     20       -2           None     JR      JR  ,
     'LR':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                  316                      -4            申银万国     1   
     1                  167                       2            华安期货     2   
     2                  152                       0            金石期货     3   
     3                  146                       0            方正中期     4   
     4                  145                       0            创元期货     5   
     5                  118                       0            东海期货     6   
     6                  108                       0            首创期货     7   
     7                  107                      -3            中国国际     8   
     8                   92                       0            浙商期货     9   
     9                   82                       1            永安期货    10   
     10                  77                      -1            徽商期货    11   
     11                  75                       0          国投安信期货    12   
     12                  62                       0            长江期货    13   
     13                  62                      -2            平安期货    14   
     14                  60                       0            东航期货    15   
     15                  50                       0            英大期货    16   
     16                  47                       0          格林大华期货    17   
     17                  47                       0            福能期货    18   
     18                  47                       0            新湖期货    19   
     19                  45                       0            中辉期货    20   
     20                2005                      -7            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                   766                        0             南华期货   69   
     1                   306                        0             长江期货   30   
     2                   182                        0             华信期货   22   
     3                   163                       53             华金期货   21   
     4                   152                        0             中粮期货   18   
     5                   131                      -12             银河期货   16   
     6                   127                        0             浙商期货   16   
     7                   105                        0             永安期货   15   
     8                   104                      -30             宝城期货   14   
     9                    96                        0             申银万国   13   
     10                   94                        0             东海期货   12   
     11                   84                        0             东吴期货   12   
     12                   81                        4           国投安信期货   12   
     13                   78                        3             中信期货   12   
     14                   57                       -1             海通期货   10   
     15                   53                        1             光大期货   10   
     16                   51                        0             广州期货    9   
     17                   46                        0             徽商期货    9   
     18                   46                        0             英大期货    7   
     19                   27                        1             中国国际    7   
     20                 2749                       19             None  334   
     
         vol_chg vol_party_name symbol variety  
     0        50           华金期货     LR      LR  
     1        27           宝城期货     LR      LR  
     2       -30           中信期货     LR      LR  
     3        14           东兴期货     LR      LR  
     4       -10           华泰期货     LR      LR  
     5       -49           申银万国     LR      LR  
     6        12           安粮期货     LR      LR  
     7        12           东吴期货     LR      LR  
     8         6           江西瑞奇     LR      LR  
     9        -5           银河期货     LR      LR  
     10      -19           方正中期     LR      LR  
     11      -12           海通期货     LR      LR  
     12        7           华鑫期货     LR      LR  
     13      -22           华安期货     LR      LR  
     14       -9         国投安信期货     LR      LR  
     15        5           国泰君安     LR      LR  
     16        9           盛达期货     LR      LR  
     17        2           鲁证期货     LR      LR  
     18       -3           国信期货     LR      LR  
     19       -9           徽商期货     LR      LR  
     20      -24           None     LR      LR  ,
     'MA':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                64977                  -10881            海通期货     1   
     1                46657                  -13704            华泰期货     2   
     2                37216                   -7452            永安期货     3   
     3                26996                   -5729            光大期货     4   
     4                21522                    3774            中信期货     5   
     5                17990                   -1705            申银万国     6   
     6                17917                    1041            国泰君安     7   
     7                16925                     934            徽商期货     8   
     8                13385                      90            新湖期货     9   
     9                12523                   -1228            东海期货    10   
     10               12506                   -5448            东证期货    11   
     11               10164                     334            方正中期    12   
     12               10057                   -1719            广发期货    13   
     13                9250                   -6713          国投安信期货    14   
     14                9118                    1016            安粮期货    15   
     15                9073                    -217            华安期货    16   
     16                8988                   -7860            西部期货    17   
     17                8668                    -449            银河期货    18   
     18                8604                     108            国信期货    19   
     19                8422                   -1413            中财期货    20   
     20              370958                  -57221            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name      vol  \
     0                 78759                    -7227             海通期货   335738   
     1                 58664                    -8796             华泰期货   310782   
     2                 34622                      723             永安期货   126725   
     3                 34147                     8599             国泰君安   125535   
     4                 30530                    -1154             银河期货   124294   
     5                 24713                    -8404             光大期货   105525   
     6                 23418                     2758             中信期货   104086   
     7                 16602                      897             方正中期    89728   
     8                 15007                      -43             东海期货    88334   
     9                 14836                     -467             新湖期货    87495   
     10                11589                     3119             兴证期货    83801   
     11                11049                     -349             信达期货    81392   
     12                10733                    -3636             东证期货    74073   
     13                 9887                    -1065             广发期货    64869   
     14                 9786                    -7304             西部期货    64528   
     15                 9463                    -5300             申银万国    60066   
     16                 8991                     2005             浙商期货    58740   
     17                 8323                     1032           国投安信期货    57329   
     18                 7587                       55             中金期货    53993   
     19                 7299                    -1060             国富期货    52752   
     20               426005                   -25617             None  2149785   
     
         vol_chg vol_party_name symbol variety  
     0     -8936           海通期货     MA      MA  
     1    -15653           华泰期货     MA      MA  
     2      6699           光大期货     MA      MA  
     3     -7615           创元期货     MA      MA  
     4    -40033           徽商期货     MA      MA  
     5    -13128           永安期货     MA      MA  
     6    -18959           华安期货     MA      MA  
     7       167           中信期货     MA      MA  
     8    -17022           东证期货     MA      MA  
     9    -19842           方正中期     MA      MA  
     10   -11009           申银万国     MA      MA  
     11     2251           国泰君安     MA      MA  
     12    -1896           新湖期货     MA      MA  
     13   -14002           浙商期货     MA      MA  
     14   -12316           广发期货     MA      MA  
     15    -6078           安粮期货     MA      MA  
     16   -17185           东航期货     MA      MA  
     17   -10335           中信建投     MA      MA  
     18   -10310           银河期货     MA      MA  
     19      851           中辉期货     MA      MA  
     20  -214351           None     MA      MA  ,
     'OI':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                21248                     398            国富期货     1   
     1                16730                    1503          国投安信期货     2   
     2                13498                    -259            国泰君安     3   
     3                12371                    1471            银河期货     4   
     4                 8930                    1344            广发期货     5   
     5                 7791                    -170            中信建投     6   
     6                 7774                    1010            宏源期货     7   
     7                 7040                     -91            永安期货     8   
     8                 6309                      72            建信期货     9   
     9                 6095                    -389            中信期货    10   
     10                5917                     173            新湖期货    11   
     11                5384                    -454            兴证期货    12   
     12                4282                     461            鲁证期货    13   
     13                3800                    -509            首创期货    14   
     14                3669                     440            广州期货    15   
     15                3625                    -280            华信期货    16   
     16                3407                    -665            兴业期货    17   
     17                3236                      98            华泰期货    18   
     18                3107                     119            中粮期货    19   
     19                2958                       5            金石期货    20   
     20              147171                    4277            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 25617                      560             中粮期货   22786   
     1                 24240                      163           国投安信期货   17797   
     2                 17354                      838             中信期货   15652   
     3                  9594                      727             广发期货   11875   
     4                  7336                      145             永安期货   10954   
     5                  6712                      121             中国国际   10363   
     6                  6691                      120             南华期货    8430   
     7                  6352                      138             华泰期货    8220   
     8                  6176                      -65             银河期货    7345   
     9                  5859                      -49             兴证期货    5820   
     10                 5783                      -27             中金期货    5594   
     11                 5381                        5             建信期货    5411   
     12                 5037                      500             摩根大通    4938   
     13                 4508                      613             鲁证期货    4748   
     14                 4469                     -187             新湖期货    4650   
     15                 4154                      282             深圳瑞龙    4596   
     16                 4019                       71             申银万国    3620   
     17                 3951                      276             海通期货    3309   
     18                 3848                     -304             宏源期货    3194   
     19                 3336                       22             上海中期    2921   
     20               160417                     3949             None  162223   
     
         vol_chg vol_party_name symbol variety  
     0    -10945           华泰期货     OI      OI  
     1     -3781           建信期货     OI      OI  
     2     -1965           海通期货     OI      OI  
     3     -1829           中信期货     OI      OI  
     4      -302           东证期货     OI      OI  
     5       141           华安期货     OI      OI  
     6       717         国投安信期货     OI      OI  
     7      -696           光大期货     OI      OI  
     8     -5303           广发期货     OI      OI  
     9       774           宏源期货     OI      OI  
     10     1778           银河期货     OI      OI  
     11     2001           申银万国     OI      OI  
     12    -2823           徽商期货     OI      OI  
     13    -4788           永安期货     OI      OI  
     14    -1092           国泰君安     OI      OI  
     15      168           中辉期货     OI      OI  
     16    -2119           创元期货     OI      OI  
     17     1520           兴业期货     OI      OI  
     18     1086            美尔雅     OI      OI  
     19     -199           国元期货     OI      OI  
     20   -27657           None     OI      OI  ,
     'PM':    long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                   7                       0            申银万国     1   
     1                   5                       0            上海中期     2   
     2                   4                       0            华信期货     3   
     3                   1                       0            深圳金汇     4   
     4                   1                       0            东航期货     5   
     5                   1                       0            国泰君安     6   
     6                   0                       0            长江期货     7   
     7                   0                       0            永安期货     8   
     8                  19                       0            None   999   
     
        short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                   11                        0             华信期货    0   
     1                    5                        0             永安期货    0   
     2                    3                        0             长江期货    0   
     3                    0                        0             申银万国    0   
     4                    0                        0             深圳金汇    0   
     5                    0                        0             东航期货    0   
     6                    0                        0             上海中期    0   
     7                    0                        0             国泰君安    0   
     8                   19                        0             None    0   
     
        vol_chg vol_party_name symbol variety  
     0        0           申银万国     PM      PM  
     1        0           华信期货     PM      PM  
     2        0           长江期货     PM      PM  
     3        0           深圳金汇     PM      PM  
     4        0           东航期货     PM      PM  
     5        0           上海中期     PM      PM  
     6        0           国泰君安     PM      PM  
     7        0           永安期货     PM      PM  
     8        0           None     PM      PM  ,
     'ER':    long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                   1                       0            华信期货     1   
     1                   0                       0            江西瑞奇     2   
     2                   1                       0            None   999   
     
        short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                    1                        0             江西瑞奇    0   
     1                    0                        0             华信期货    0   
     2                    1                        0             None    0   
     
        vol_chg vol_party_name symbol variety  
     0        0           江西瑞奇     ER      ER  
     1        0           华信期货     ER      ER  
     2        0           None     ER      ER  ,
     'RM':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                37517                     -50            冠通期货     1   
     1                28901                    3467            中信期货     2   
     2                25180                     310            兴证期货     3   
     3                23347                   -1049            申银万国     4   
     4                15642                    -987            永安期货     5   
     5                14052                    -238          国投安信期货     6   
     6                12003                    -242            上海中期     7   
     7                11915                   -9926            国贸期货     8   
     8                11124                       6          格林大华期货     9   
     9                10606                   -1442            弘业期货    10   
     10               10481                    1209            银河期货    11   
     11                8574                     -72            中辉期货    12   
     12                8562                     340            国元期货    13   
     13                7561                     228            广发期货    14   
     14                7533                    -120            徽商期货    15   
     15                7242                   -7881            光大期货    16   
     16                6453                      35            宏源期货    17   
     17                6167                    1250            国泰君安    18   
     18                4994                      82            东证期货    19   
     19                4930                     134            中粮期货    20   
     20              262784                  -14946            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 37375                       81             冠通期货   95277   
     1                 36254                     2656             中信期货   74001   
     2                 31450                     2066             兴证期货   66905   
     3                 24876                     1214           国投安信期货   52226   
     4                 18177                      821             中粮期货   34243   
     5                 14358                    -3857             申银万国   32145   
     6                 11139                   -10055             国贸期货   31372   
     7                 10620                      868             银河期货   28786   
     8                 10557                      -27             上海中期   27754   
     9                  9754                     -129           格林大华期货   24152   
     10                 9478                     -146             国泰君安   21351   
     11                 9239                     1468             南华期货   19408   
     12                 8715                      -44             中金期货   15590   
     13                 8654                    -1995             弘业期货   14956   
     14                 7783                      -98             国元期货   14242   
     15                 7711                     -630             中辉期货   13943   
     16                 6462                    -8672             光大期货   12879   
     17                 5879                     -326             宏源期货   12534   
     18                 5824                      -70             徽商期货   12282   
     19                 5783                      -26             兴业期货   11969   
     20               280088                   -16901             None  616015   
     
         vol_chg vol_party_name symbol variety  
     0     -9764           海通期货     RM      RM  
     1     -4032           光大期货     RM      RM  
     2      9394           华泰期货     RM      RM  
     3     -5510           建信期货     RM      RM  
     4      6927           中信期货     RM      RM  
     5     -4124           东证期货     RM      RM  
     6       381           徽商期货     RM      RM  
     7      8242           国泰君安     RM      RM  
     8      -686           金瑞期货     RM      RM  
     9    -11049           兴证期货     RM      RM  
     10    18559           国贸期货     RM      RM  
     11    -4738           华安期货     RM      RM  
     12    -3505           中辉期货     RM      RM  
     13    -8559           广发期货     RM      RM  
     14     1669           申银万国     RM      RM  
     15    -8268           方正中期     RM      RM  
     16      -80           长江期货     RM      RM  
     17       -9           东航期货     RM      RM  
     18    -4759           创元期货     RM      RM  
     19      371           冠通期货     RM      RM  
     20   -19540           None     RM      RM  ,
     'RS':    long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                   5                       0            方正中期     1   
     1                   2                       0            国泰君安     2   
     2                   0                       0            招商期货     3   
     3                   0                       0            海通期货     4   
     4                   0                       0            中原期货     5   
     5                   0                       0            华安期货     6   
     6                   0                       0            平安期货     7   
     7                   7                       0            None   999   
     
        short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                    4                        0             海通期货    2   
     1                    2                        0             华安期货    2   
     2                    1                        0             平安期货    0   
     3                    0                        0             招商期货    0   
     4                    0                        0             方正中期    0   
     5                    0                        0             中原期货    0   
     6                    0                        0             国泰君安    0   
     7                    7                        0             None    4   
     
        vol_chg vol_party_name symbol variety  
     0        2           招商期货     RS      RS  
     1        2           中原期货     RS      RS  
     2        0           方正中期     RS      RS  
     3        0           海通期货     RS      RS  
     4        0           国泰君安     RS      RS  
     5        0           华安期货     RS      RS  
     6        0           平安期货     RS      RS  
     7        4           None     RS      RS  ,
     'SF':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 4771                     489            中信期货     1   
     1                 2832                     336          五矿经易期货     2   
     2                 2531                     466            弘业期货     3   
     3                 2449                    1008            华泰期货     4   
     4                 1780                     476          国投安信期货     5   
     5                 1545                     336            国信期货     6   
     6                 1387                     586            新湖期货     7   
     7                 1279                    -184            华信期货     8   
     8                 1150                    -154            浙商期货     9   
     9                 1147                     435            华龙期货    10   
     10                1115                     -44            东证期货    11   
     11                1111                    -289            申银万国    12   
     12                 987                      23            西部期货    13   
     13                 947                     -76            永安期货    14   
     14                 747                     498            一德期货    15   
     15                 571                     -36            上海中期    16   
     16                 529                     237            兴证期货    17   
     17                 520                     -35            中财期货    18   
     18                 513                     464            江西瑞奇    19   
     19                 485                     -21            中信建投    20   
     20               28396                    4515            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  3186                      -10             中信期货   7698   
     1                  3100                     1096             华泰期货   5021   
     2                  1890                       11             中金期货   4013   
     3                  1886                      426             兴证期货   3915   
     4                  1870                       25             国泰君安   3079   
     5                  1576                      629             新湖期货   2751   
     6                  1458                      -62             宏源期货   2141   
     7                  1304                      192             东航期货   1990   
     8                  1165                       77             东证期货   1861   
     9                  1160                       64             申银万国   1557   
     10                 1032                      269             国信期货   1514   
     11                  900                      -13           五矿经易期货   1465   
     12                  769                       46             永安期货   1431   
     13                  683                       82             华安期货   1370   
     14                  676                      192             光大期货   1332   
     15                  671                      177             徽商期货   1325   
     16                  592                     -463             南华期货   1210   
     17                  585                       27             海通期货   1183   
     18                  579                      274             广发期货   1179   
     19                  568                     -310             方正中期   1158   
     20                25650                     2729             None  47193   
     
         vol_chg vol_party_name symbol variety  
     0      -458           华泰期货     SF      SF  
     1         6           东证期货     SF      SF  
     2      -254           新湖期货     SF      SF  
     3     -1934           中信期货     SF      SF  
     4       420           国信期货     SF      SF  
     5      -120           弘业期货     SF      SF  
     6       839           方正中期     SF      SF  
     7       342           华安期货     SF      SF  
     8      -492           徽商期货     SF      SF  
     9      -214         五矿经易期货     SF      SF  
     10     1063           南华期货     SF      SF  
     11      265         国投安信期货     SF      SF  
     12     -862           兴证期货     SF      SF  
     13      352           西部期货     SF      SF  
     14      114           银河期货     SF      SF  
     15      217           国泰君安     SF      SF  
     16      123           华信期货     SF      SF  
     17     -598           中原期货     SF      SF  
     18      346           一德期货     SF      SF  
     19      234           东航期货     SF      SF  
     20     -611           None     SF      SF  ,
     'SM':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                11002                     -72          国投安信期货     1   
     1                 9011                     381            上海大陆     2   
     2                 6570                     390            弘业期货     3   
     3                 6101                    -836            中信期货     4   
     4                 3201                    -860            华泰期货     5   
     5                 3182                     479            中信建投     6   
     6                 2895                     -35            浙商期货     7   
     7                 2206                     436            新湖期货     8   
     8                 2044                     133            兴业期货     9   
     9                 2042                     -15            福能期货    10   
     10                2009                     260            中金期货    11   
     11                1866                     163            英大期货    12   
     12                1834                    -193            南华期货    13   
     13                1831                    -101            国泰君安    14   
     14                1759                    -109            方正中期    15   
     15                1703                    -366            申银万国    16   
     16                1473                      22            华信期货    17   
     17                1322                      53            永安期货    18   
     18                1320                       7            国信期货    19   
     19                1175                    1074            天风期货    20   
     20               64546                     811            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  4030                     -160             永安期货  11161   
     1                  3583                     -596           国投安信期货   9689   
     2                  3571                     -711             华泰期货   6367   
     3                  3360                     -802             中信期货   6236   
     4                  3296                      302             申银万国   6043   
     5                  3094                     -974             中粮期货   5537   
     6                  3079                     -190             海通期货   4097   
     7                  2582                      592             上海中期   3980   
     8                  2463                    -1545             东证期货   3550   
     9                  2304                     -514             弘业期货   3029   
     10                 2076                      625             新湖期货   3006   
     11                 1992                      365             方正中期   2986   
     12                 1629                       23             国信期货   2762   
     13                 1574                      114             国泰君安   2414   
     14                 1459                      -96             上海大陆   2268   
     15                 1376                     -258             南证期货   2249   
     16                 1321                       19             国海良时   2133   
     17                 1307                      470             南华期货   2118   
     18                 1303                       11             国贸期货   2056   
     19                 1289                       94             宏源期货   1932   
     20                46688                    -3231             None  83613   
     
         vol_chg vol_party_name symbol variety  
     0     -4343           华泰期货     SM      SM  
     1     -2996           东证期货     SM      SM  
     2     -1181           新湖期货     SM      SM  
     3     -2878           中信期货     SM      SM  
     4     -4021           上海大陆     SM      SM  
     5     -1317           海通期货     SM      SM  
     6     -2386           国泰君安     SM      SM  
     7     -3457           弘业期货     SM      SM  
     8     -2387           徽商期货     SM      SM  
     9     -1780           华安期货     SM      SM  
     10      -75           国信期货     SM      SM  
     11       95           兴证期货     SM      SM  
     12      126           西部期货     SM      SM  
     13    -3193         国投安信期货     SM      SM  
     14     -685           申银万国     SM      SM  
     15      925           中信建投     SM      SM  
     16      169           南华期货     SM      SM  
     17    -1419           方正中期     SM      SM  
     18     1240           天风期货     SM      SM  
     19     1157           南证期货     SM      SM  
     20   -28406           None     SM      SM  ,
     'SR':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                13728                     701            中信期货     1   
     1                12161                    1670            东兴期货     2   
     2                11435                   -2888            中粮期货     3   
     3                11312                      -3            首创期货     4   
     4                10692                      87            广发期货     5   
     5                 9841                    -130            光大期货     6   
     6                 9490                    -240            鲁证期货     7   
     7                 8616                     479            华泰期货     8   
     8                 8089                      38            创元期货     9   
     9                 6791                     419            宏源期货    10   
     10                6661                     117            金瑞期货    11   
     11                6318                     -11          国投安信期货    12   
     12                5972                     391            永安期货    13   
     13                5562                     123            华信期货    14   
     14                5086                   -2967            兴证期货    15   
     15                4995                     683            国泰君安    16   
     16                4529                     203            银河期货    17   
     17                4353                    -293            东证期货    18   
     18                4240                     -62            中投天琪    19   
     19                3966                    -682            天风期货    20   
     20              153837                   -2365            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 23332                     1037             中粮期货   27889   
     1                 16945                      214             华泰期货   25045   
     2                 14772                     1538             英大期货   23779   
     3                 11908                    -2085             中信期货   22339   
     4                 11867                       98             永安期货   16506   
     5                 11402                       18             中金期货    8876   
     6                  9288                     -106           国投安信期货    8070   
     7                  8917                     -803             广发期货    7949   
     8                  8292                     -175             光大期货    7659   
     9                  7780                      210             浙商期货    7157   
     10                 7230                     -153             国泰君安    7014   
     11                 6920                      -36             宏源期货    6685   
     12                 6492                     -100             银河期货    5794   
     13                 6323                      -83             兴业期货    5648   
     14                 6242                     1667             东兴期货    5257   
     15                 6082                     -507             大地期货    5243   
     16                 5795                     -368             国联期货    4906   
     17                 4813                      -83             国信期货    4741   
     18                 4811                       54             深圳瑞龙    4672   
     19                 4760                      427             兴证期货    4430   
     20               183971                      764             None  209659   
     
         vol_chg vol_party_name symbol variety  
     0    -11226           建信期货     SR      SR  
     1     -7519           华泰期货     SR      SR  
     2     -2899           东证期货     SR      SR  
     3    -13558           海通期货     SR      SR  
     4      -183           中信期货     SR      SR  
     5       797           兴证期货     SR      SR  
     6     -2550           徽商期货     SR      SR  
     7     -3172           光大期货     SR      SR  
     8     -2611           华安期货     SR      SR  
     9     -3054           海证期货     SR      SR  
     10    -1550           国泰君安     SR      SR  
     11      766           中粮期货     SR      SR  
     12       81           创元期货     SR      SR  
     13    -3019           广发期货     SR      SR  
     14    -2097           国贸期货     SR      SR  
     15    -3006           宏源期货     SR      SR  
     16    -1188           东航期货     SR      SR  
     17    -2316           方正中期     SR      SR  
     18       85           安粮期货     SR      SR  
     19      -59           申银万国     SR      SR  
     20   -58278           None     SR      SR  ,
     'TA':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                73462                   -5654            华泰期货     1   
     1                55491                    -635            国贸期货     2   
     2                54030                    6632            南华期货     3   
     3                48471                   -5778            永安期货     4   
     4                45707                    1038            建信期货     5   
     5                40589                    2559            中信期货     6   
     6                37532                    8210            招商期货     7   
     7                36076                      51            中粮期货     8   
     8                34439                     367            国泰君安     9   
     9                25833                   -8131            天风期货    10   
     10               24884                    2621            光大期货    11   
     11               24749                     199            广发期货    12   
     12               20972                       7            银河期货    13   
     13               14702                   -3770            新湖期货    14   
     14               13408                    3572            申银万国    15   
     15               11082                   -1133            方正中期    16   
     16               10674                     859            东航期货    17   
     17               10639                    4576            东证期货    18   
     18                9688                     343            信达期货    19   
     19                9253                     132            通惠期货    20   
     20              601681                    6065            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name      vol  \
     0                 95314                    -7671             永安期货   175051   
     1                 65127                   -11953             银河期货   150788   
     2                 33257                     1895             中信期货   122589   
     3                 28431                     3701             华泰期货    98580   
     4                 28422                      626             国泰君安    86750   
     5                 22102                     -355             招商期货    84031   
     6                 21651                      -99             浙商期货    59226   
     7                 19605                     1142             方正中期    58075   
     8                 19546                     3187             光大期货    53937   
     9                 19190                    10905             中粮期货    52013   
     10                18850                     3016             宝城期货    50734   
     11                17110                     -321           五矿经易期货    48569   
     12                16217                     -579             信达期货    47262   
     13                14542                    -3802             东吴期货    46325   
     14                14521                    -1207           国投安信期货    44985   
     15                14212                     1796             海通期货    43849   
     16                13801                    -1007             大地期货    40706   
     17                13270                     7381             东证期货    38095   
     18                12742                    -3930             建信期货    35147   
     19                12464                       74             东航期货    34818   
     20               500374                     2799             None  1371530   
     
         vol_chg vol_party_name symbol variety  
     0    -95704           华泰期货     TA      TA  
     1    -36180           海通期货     TA      TA  
     2    -26018           永安期货     TA      TA  
     3     -2051           新湖期货     TA      TA  
     4     -4633           中信期货     TA      TA  
     5     -6252           东证期货     TA      TA  
     6     -9593           光大期货     TA      TA  
     7     10035           西部期货     TA      TA  
     8     -4299           南华期货     TA      TA  
     9     -9561           华安期货     TA      TA  
     10   -14282           申银万国     TA      TA  
     11   -40580           创元期货     TA      TA  
     12    -1291           广发期货     TA      TA  
     13   -11351           方正中期     TA      TA  
     14   -29951           徽商期货     TA      TA  
     15   -13859           东方财富     TA      TA  
     16   -16456           银河期货     TA      TA  
     17   -18985           国泰君安     TA      TA  
     18    -8334         国投安信期货     TA      TA  
     19      873           国元期货     TA      TA  
     20  -338472           None     TA      TA  ,
     'WH':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                  267                       0            首创期货     1   
     1                  129                     -12          国投安信期货     2   
     2                  109                       0            华鑫期货     3   
     3                   29                      -1            银河期货     4   
     4                   29                       0            国泰君安     5   
     5                   28                      -7            永安期货     6   
     6                   27                       0          格林大华期货     7   
     7                   27                       1            国信期货     8   
     8                   26                       1            中信期货     9   
     9                   22                      -2            东航期货    10   
     10                  22                       0            宏源期货    11   
     11                  18                       0            中原期货    12   
     12                  15                      -2            中辉期货    13   
     13                  14                       0            光大期货    14   
     14                  11                       4            广发期货    15   
     15                  11                      -2            财达期货    16   
     16                  10                      -1            中粮期货    17   
     17                  10                       0            海通期货    18   
     18                  10                       0            平安期货    19   
     19                   9                      -1            华泰期货    20   
     20                 823                     -22            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                   513                        4             永安期货   31   
     1                   271                      -28             迈科期货   29   
     2                    50                        2             申银万国   23   
     3                    32                        3             华闻期货   16   
     4                    13                        4             中国国际   13   
     5                    11                        5             光大期货   10   
     6                    10                        0             招金期货    9   
     7                     9                        0             东航期货    8   
     8                     8                       -2           五矿经易期货    6   
     9                     7                        0             海航期货    5   
     10                    7                        1             中信期货    4   
     11                    7                        0             东证期货    4   
     12                    7                        0             宏源期货    3   
     13                    6                        0             安粮期货    3   
     14                    5                        0             国信期货    3   
     15                    5                       -1             鲁证期货    3   
     16                    4                        0             国泰君安    2   
     17                    3                        0             中财期货    2   
     18                    3                        0             英大期货    2   
     19                    2                        1             徽商期货    2   
     20                  973                      -11             None  178   
     
         vol_chg vol_party_name symbol variety  
     0        25           永安期货     WH      WH  
     1        20           迈科期货     WH      WH  
     2        14           弘业期货     WH      WH  
     3        -4           创元期货     WH      WH  
     4         1         国投安信期货     WH      WH  
     5         4           广发期货     WH      WH  
     6         0           大有期货     WH      WH  
     7         0           中国国际     WH      WH  
     8         6           东海期货     WH      WH  
     9         2           光大期货     WH      WH  
     10       -4           东航期货     WH      WH  
     11        4           国联期货     WH      WH  
     12       -2           国信期货     WH      WH  
     13        3           中融汇信     WH      WH  
     14        3           华联期货     WH      WH  
     15        3           华闻期货     WH      WH  
     16        2           招商期货     WH      WH  
     17      -47           申银万国     WH      WH  
     18        0           中信期货     WH      WH  
     19        2           鲁证期货     WH      WH  
     20       32           None     WH      WH  ,
     'ZC':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                11297                     365            中信期货     1   
     1                 8540                      24            国信期货     2   
     2                 7853                    -361            中粮期货     3   
     3                 7846                    -291            建信期货     4   
     4                 7790                   -1211            银河期货     5   
     5                 7542                     -75            鲁证期货     6   
     6                 7370                    -173          国投安信期货     7   
     7                 7262                    1863             美尔雅     8   
     8                 6446                     565            广发期货     9   
     9                 6003                    -606           中电投先融    10   
     10                5546                      19            方正中期    11   
     11                5447                      58            摩根大通    12   
     12                5435                     214            一德期货    13   
     13                5073                     163            永安期货    14   
     14                4968                      82            中大期货    15   
     15                4785                     878            宏源期货    16   
     16                4398                    -203            弘业期货    17   
     17                4184                    -155            渤海期货    18   
     18                4172                    -605            南华期货    19   
     19                3972                    -138            新湖期货    20   
     20              125929                     413            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 25068                      744             永安期货   19528   
     1                 11070                     1376             一德期货   14477   
     2                  9930                     -246             方正中期   13028   
     3                  9778                     -450             中信期货   12468   
     4                  8148                      573             银河期货    9399   
     5                  7961                     -873             华泰期货    8549   
     6                  6991                     -239           国投安信期货    7902   
     7                  5822                     -515             国泰君安    7469   
     8                  5731                     -451             大地期货    7342   
     9                  5693                       13             新湖期货    7314   
     10                 5653                       58             浙商期货    7223   
     11                 5537                     -384             东证期货    5997   
     12                 4563                      155             广发期货    5756   
     13                 4530                      901             长江期货    5382   
     14                 4407                       47             南华期货    5311   
     15                 4301                      216             申银万国    4645   
     16                 4063                     -142             宏源期货    4508   
     17                 3871                      243             鲁证期货    4375   
     18                 3233                     2462             红塔期货    4314   
     19                 3121                       15             渤海期货    4184   
     20               139471                     3503             None  159171   
     
         vol_chg vol_party_name symbol variety  
     0     -3328           建信期货     ZC      ZC  
     1     -5719           华泰期货     ZC      ZC  
     2     -7065           东证期货     ZC      ZC  
     3      5272           宏源期货     ZC      ZC  
     4     -5584           中信期货     ZC      ZC  
     5      4255           新湖期货     ZC      ZC  
     6     -3811           银河期货     ZC      ZC  
     7     -2397           海通期货     ZC      ZC  
     8     -2664           光大期货     ZC      ZC  
     9     -2150           国泰君安     ZC      ZC  
     10    -8009           方正中期     ZC      ZC  
     11    -2260           永安期货     ZC      ZC  
     12    -2097           一德期货     ZC      ZC  
     13     -751           南华期货     ZC      ZC  
     14      184           中信建投     ZC      ZC  
     15      -46           兴证期货     ZC      ZC  
     16    -1823           广发期货     ZC      ZC  
     17    -3167           徽商期货     ZC      ZC  
     18     -925           浙商期货     ZC      ZC  
     19    -1627         国投安信期货     ZC      ZC  
     20   -43712           None     ZC      ZC  ,
     'AP812 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                  100                       0            中信期货     1   
     1                   34                       0            宏源期货     2   
     2                   20                       2            浙商期货     3   
     3                   20                       0            国泰君安     4   
     4                   13                       0            华泰期货     5   
     5                   10                       0            渤海期货     6   
     6                   10                       0            大地期货     7   
     7                   10                       0            德盛期货     8   
     8                    9                       0            申银万国     9   
     9                    9                       0            中粮期货    10   
     10                   6                      -1            前海期货    11   
     11                   6                       0            海证期货    12   
     12                   2                       0            海通期货    13   
     13                   2                       0            中信建投    14   
     14                   2                       0            南华期货    15   
     15                   2                       0            一德期货    16   
     16                 255                       1            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                    82                        0             浙商期货    2   
     1                    50                        0             中信期货    1   
     2                    50                        0             中大期货    1   
     3                    34                        0             一德期货    0   
     4                    22                        0           五矿经易期货    0   
     5                     6                        0             永安期货    0   
     6                     4                        0             中财期货    0   
     7                     3                        0             华泰期货    0   
     8                     2                        0             金瑞期货    0   
     9                     2                        0             南证期货    0   
     10                    0                        0                0    0   
     11                    0                        0                0    0   
     12                    0                        0                0    0   
     13                    0                        0                0    0   
     14                    0                        0                0    0   
     15                    0                        0                0    0   
     16                  255                        0             None    4   
     
         vol_chg vol_party_name  symbol variety  
     0        -1           浙商期货  AP812       AP  
     1         0           前海期货  AP812       AP  
     2         1           西部期货  AP812       AP  
     3         0              0  AP812       AP  
     4         0              0  AP812       AP  
     5         0              0  AP812       AP  
     6         0              0  AP812       AP  
     7         0              0  AP812       AP  
     8         0              0  AP812       AP  
     9         0              0  AP812       AP  
     10        0              0  AP812       AP  
     11        0              0  AP812       AP  
     12        0              0  AP812       AP  
     13        0              0  AP812       AP  
     14        0              0  AP812       AP  
     15        0              0  AP812       AP  
     16        0           None  AP812       AP  ,
     'AP901 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 1150                     -14            中信期货     1   
     1                 1111                      40            申银万国     2   
     2                  566                       5            招金期货     3   
     3                  552                     -23            永安期货     4   
     4                  546                       0            一德期货     5   
     5                  534                      -1            方正中期     6   
     6                  460                      13            银河期货     7   
     7                  431                     -44            兴证期货     8   
     8                  411                      -6            东航期货     9   
     9                  397                       2            中融汇信    10   
     10                 388                       6            国泰君安    11   
     11                 363                     -32            光大期货    12   
     12                 335                       4            中国国际    13   
     13                 328                     -93            渤海期货    14   
     14                 320                    -100            上海东亚    15   
     15                 276                      -2            中信建投    16   
     16                 270                     -15            浙商期货    17   
     17                 261                       5            东证期货    18   
     18                 258                       2            鲁证期货    19   
     19                 255                     -22            金瑞期货    20   
     20                9212                    -275            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name   vol  \
     0                   679                       -4             大地期货  1105   
     1                   644                      -62             永安期货   547   
     2                   511                       -9             中信期货   414   
     3                   490                      -20             上海东亚   345   
     4                   446                      -14             光大期货   282   
     5                   439                       -3             方正中期   277   
     6                   436                      -21             华泰期货   273   
     7                   393                      -14             南华期货   249   
     8                   381                       -8             中大期货   177   
     9                   374                       -4             广发期货   156   
     10                  338                        0           五矿经易期货   152   
     11                  334                      -19             一德期货   124   
     12                  306                       11             申银万国   120   
     13                  277                      -16             国海良时   116   
     14                  273                       -2             招商期货   115   
     15                  273                       -1             江西瑞奇   114   
     16                  272                       -5             西部期货   113   
     17                  261                        7             国泰君安    99   
     18                  254                       -1            新纪元期货    94   
     19                  247                       -2             东航期货    83   
     20                 7628                     -187             None  4955   
     
         vol_chg vol_party_name  symbol variety  
     0     -1200           东证期货  AP901       AP  
     1       -53           华泰期货  AP901       AP  
     2      -415           建信期货  AP901       AP  
     3      -415           中信期货  AP901       AP  
     4      -390           光大期货  AP901       AP  
     5      -244           海通期货  AP901       AP  
     6        47           国泰君安  AP901       AP  
     7         7           徽商期货  AP901       AP  
     8        37           宏源期货  AP901       AP  
     9      -158           华安期货  AP901       AP  
     10       53           鲁证期货  AP901       AP  
     11       67           东海期货  AP901       AP  
     12      109           上海东亚  AP901       AP  
     13       20           广州期货  AP901       AP  
     14     -159           永安期货  AP901       AP  
     15      -59           安粮期货  AP901       AP  
     16      -59           中辉期货  AP901       AP  
     17       87           渤海期货  AP901       AP  
     18     -122         国投安信期货  AP901       AP  
     19      -43           国金期货  AP901       AP  
     20    -2890           None  AP901       AP  ,
     'AP903 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                  850                     -15            一德期货     1   
     1                  572                       2            中辉期货     2   
     2                  567                      14            海通期货     3   
     3                  548                       0            国海良时     4   
     4                  521                       0            上海中期     5   
     5                  520                       0            西南期货     6   
     6                  511                       0            国信期货     7   
     7                  503                       0            华信期货     8   
     8                  500                      -1            瑞达期货     9   
     9                  472                      -1            浙商期货    10   
     10                 459                       3            新湖期货    11   
     11                 441                       0            光大期货    12   
     12                 384                       0            和合期货    13   
     13                 356                       0            中信期货    14   
     14                 341                       1            中信建投    15   
     15                 337                       1            国泰君安    16   
     16                 328                       2            华泰期货    17   
     17                 272                       0            方正中期    18   
     18                 207                       9            永安期货    19   
     19                 163                       0            广发期货    20   
     20                8852                      15            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name   vol  \
     0                   738                      -91             兴证期货   193   
     1                   707                       33             华泰期货   185   
     2                   707                        0             广发期货   125   
     3                   677                        6             银河期货    94   
     4                   625                       -3             南华期货    91   
     5                   524                        1             金元期货    82   
     6                   519                        1           格林大华期货    76   
     7                   440                      -35             华安期货    68   
     8                   419                      -85             渤海期货    66   
     9                   410                        1             建信期货    64   
     10                  358                        0             天风期货    46   
     11                  353                       13           国投安信期货    41   
     12                  280                       35             徽商期货    38   
     13                  260                        8             金瑞期货    36   
     14                  244                        6             国泰君安    36   
     15                  211                        0             中国国际    35   
     16                  202                       -5             永安期货    34   
     17                  166                      -19             光大期货    33   
     18                  159                        0             申银万国    33   
     19                  159                       40             宏源期货    31   
     20                 8158                      -94             None  1407   
     
         vol_chg vol_party_name  symbol variety  
     0       -59           海通期货  AP903       AP  
     1        -3           安粮期货  AP903       AP  
     2      -198           华泰期货  AP903       AP  
     3        16           兴证期货  AP903       AP  
     4        57           渤海期货  AP903       AP  
     5        16           宏源期货  AP903       AP  
     6        76           建信期货  AP903       AP  
     7        -7           徽商期货  AP903       AP  
     8      -193           华安期货  AP903       AP  
     9        40           东海期货  AP903       AP  
     10       -6           首创期货  AP903       AP  
     11        0           海证期货  AP903       AP  
     12     -298           鲁证期货  AP903       AP  
     13      -67           创元期货  AP903       AP  
     14      -36           永安期货  AP903       AP  
     15      -33           光大期货  AP903       AP  
     16        3           浙商期货  AP903       AP  
     17      -43         国投安信期货  AP903       AP  
     18      -22           银河期货  AP903       AP  
     19     -173           国泰君安  AP903       AP  
     20     -930           None  AP903       AP  ,
     'AP905 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 7486                      98            一德期货     1   
     1                 4691                       0            中信期货     2   
     2                 4304                      33            东证期货     3   
     3                 4177                    -133            申银万国     4   
     4                 3941                     222            永安期货     5   
     5                 3541                     366            中辉期货     6   
     6                 3428                    -124            浙商期货     7   
     7                 3263                    -302            海通期货     8   
     8                 2979                    -266            华泰期货     9   
     9                 2866                     -51            国泰君安    10   
     10                2692                     130            宏源期货    11   
     11                2667                     -32            华安期货    12   
     12                2604                     -72            国信期货    13   
     13                2558                     156            光大期货    14   
     14                2409                     -12            中信建投    15   
     15                2290                     192            鲁证期货    16   
     16                2290                     -40            南华期货    17   
     17                2274                     167            东航期货    18   
     18                2199                     155            方正中期    19   
     19                2146                     -91            徽商期货    20   
     20               64805                     396            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                  7234                      407             方正中期   17405   
     1                  4956                     -261             国泰君安   11565   
     2                  4058                     -181             永安期货    7558   
     3                  3829                     -149             海通期货    7062   
     4                  3478                      391             徽商期货    6580   
     5                  3315                       70             银河期货    5887   
     6                  2984                     -138             中信期货    5821   
     7                  2858                      -47             南华期货    5224   
     8                  2784                       -6             光大期货    5077   
     9                  2680                      -50             中信建投    5064   
     10                 2669                      109             浙商期货    5004   
     11                 2593                      173             华泰期货    5000   
     12                 2481                      -65             宏源期货    3479   
     13                 2460                     -214             申银万国    3316   
     14                 2244                     -226             广发期货    3225   
     15                 2097                       -4           国投安信期货    3143   
     16                 2062                      132             华安期货    3135   
     17                 2008                     -204             东证期货    3081   
     18                 1803                       12             中粮期货    2868   
     19                 1774                      325             东航期货    2741   
     20                60367                       74             None  112235   
     
         vol_chg vol_party_name  symbol variety  
     0     -4255           海通期货  AP905       AP  
     1      -813           东证期货  AP905       AP  
     2     -2590           光大期货  AP905       AP  
     3     -1293           徽商期货  AP905       AP  
     4     -1817           中信期货  AP905       AP  
     5     -1257           建信期货  AP905       AP  
     6     -2513           华泰期货  AP905       AP  
     7     -2175           方正中期  AP905       AP  
     8      -109           申银万国  AP905       AP  
     9     -2854           创元期货  AP905       AP  
     10    -3078           国泰君安  AP905       AP  
     11    -1255           华安期货  AP905       AP  
     12      426           中财期货  AP905       AP  
     13    -1384           东航期货  AP905       AP  
     14     -932           宏源期货  AP905       AP  
     15     -615           浙商期货  AP905       AP  
     16     -874           银河期货  AP905       AP  
     17     -889           金瑞期货  AP905       AP  
     18     -721           中辉期货  AP905       AP  
     19    -1377           永安期货  AP905       AP  
     20   -30375           None  AP905       AP  ,
     'AP907 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                  999                       1            鲁证期货     1   
     1                  779                       0            中信建投     2   
     2                  720                      -3            国泰君安     3   
     3                  704                       0            国海良时     4   
     4                  515                       0            浙商期货     5   
     5                  502                       1            上海中期     6   
     6                  500                       0            西南期货     7   
     7                  440                       1            新湖期货     8   
     8                  438                      -5            中信期货     9   
     9                  414                       2            海通期货    10   
     10                 381                       0            华鑫期货    11   
     11                 319                       0            金元期货    12   
     12                 306                       0            华信期货    13   
     13                 255                     -18            东吴期货    14   
     14                 192                       0            中国国际    15   
     15                 189                      -6            一德期货    16   
     16                 163                       5            光大期货    17   
     17                 150                     -60            安粮期货    18   
     18                 144                      -1            东航期货    19   
     19                 140                       0            永安期货    20   
     20                8250                     -83            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name   vol  \
     0                  1208                       18             华泰期货   211   
     1                   780                        0             天风期货   209   
     2                   773                       21             申银万国   159   
     3                   406                        5             光大期货   150   
     4                   345                     -100             国泰君安   127   
     5                   316                       -2           国投安信期货    95   
     6                   311                       -7             永安期货    78   
     7                   282                       -2             长江期货    74   
     8                   250                       -6             中信期货    70   
     9                   239                       -9             银河期货    65   
     10                  232                        1             广发期货    47   
     11                  205                        0           格林大华期货    47   
     12                  203                        0             首创期货    45   
     13                  198                       -2             中信建投    43   
     14                  194                       28             东证期货    43   
     15                  193                        4             宏源期货    41   
     16                  183                       -5             海通期货    40   
     17                  183                       -2             中国国际    39   
     18                  182                        0             方正中期    37   
     19                  144                       -5             徽商期货    34   
     20                 6827                      -63             None  1654   
     
         vol_chg vol_party_name  symbol variety  
     0       -31           海通期货  AP907       AP  
     1        16           东证期货  AP907       AP  
     2      -270           国泰君安  AP907       AP  
     3      -158           华泰期货  AP907       AP  
     4       -85           中信期货  AP907       AP  
     5        90           西部期货  AP907       AP  
     6        36           安粮期货  AP907       AP  
     7       -59           上海大陆  AP907       AP  
     8        24           光大期货  AP907       AP  
     9        44           金鹏期货  AP907       AP  
     10      -38           申银万国  AP907       AP  
     11      -69           永安期货  AP907       AP  
     12      -33           徽商期货  AP907       AP  
     13        1           银河期货  AP907       AP  
     14        3           华安期货  AP907       AP  
     15       32           东海期货  AP907       AP  
     16       -9           国富期货  AP907       AP  
     17       30           新湖期货  AP907       AP  
     18       24          浙江新世纪  AP907       AP  
     19       17           国贸期货  AP907       AP  
     20     -435           None  AP907       AP  ,
     'AP910 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                  509                       0            大地期货     1   
     1                  489                       1            华泰期货     2   
     2                  392                      63            中辉期货     3   
     3                  370                     -17            浙商期货     4   
     4                  264                      -2            银河期货     5   
     5                  263                       0            申银万国     6   
     6                  263                     -28            中信期货     7   
     7                  234                      -1            一德期货     8   
     8                  221                      -1            弘业期货     9   
     9                  208                       3            光大期货    10   
     10                 201                       2            国信期货    11   
     11                 198                      40            东证期货    12   
     12                 189                       0            方正中期    13   
     13                 183                       4            东海期货    14   
     14                 168                      -3            海证期货    15   
     15                 163                       8            中国国际    16   
     16                 154                       1            南华期货    17   
     17                 151                       0            金瑞期货    18   
     18                 151                       0            中州期货    19   
     19                 137                      -8            华安期货    20   
     20                4908                      62            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name   vol  \
     0                  1200                       -1             国海良时   154   
     1                   595                        0             西南期货   154   
     2                   514                        0             金元期货   101   
     3                   513                        7             华泰期货   100   
     4                   510                        1             国联期货    97   
     5                   472                        3             永安期货    80   
     6                   466                        5             海证期货    71   
     7                   302                        1             宏源期货    69   
     8                   289                       -4             海通期货    64   
     9                   226                      -13             新湖期货    53   
     10                  222                        0             中粮期货    46   
     11                  164                       -1             银河期货    46   
     12                  157                       50             渤海期货    42   
     13                  156                      -12             徽商期货    39   
     14                  136                       20             安粮期货    32   
     15                  133                        1             英大期货    31   
     16                  131                       -9             国泰君安    29   
     17                  127                      -11             中国国际    28   
     18                  124                      -10             江西瑞奇    27   
     19                  124                       -2             方正中期    26   
     20                 6561                       25             None  1289   
     
         vol_chg vol_party_name  symbol variety  
     0        -1           华泰期货  AP910       AP  
     1        22           海通期货  AP910       AP  
     2        74           东证期货  AP910       AP  
     3        96           东兴期货  AP910       AP  
     4        83           招金期货  AP910       AP  
     5       -22           光大期货  AP910       AP  
     6        14           华安期货  AP910       AP  
     7        10           中信期货  AP910       AP  
     8        43           中辉期货  AP910       AP  
     9        53           渤海期货  AP910       AP  
     10       -3           浙商期货  AP910       AP  
     11       44           东吴期货  AP910       AP  
     12       27           中投天琪  AP910       AP  
     13       37           国贸期货  AP910       AP  
     14        4           方正中期  AP910       AP  
     15       19           宏源期货  AP910       AP  
     16      -63           徽商期货  AP910       AP  
     17       15           新晟期货  AP910       AP  
     18        9         国投安信期货  AP910       AP  
     19        1           创元期货  AP910       AP  
     20      462           None  AP910       AP  ,
     'CF901 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 9564                     477          国投安信期货     1   
     1                 5139                     -77            上海中期     2   
     2                 3844                     -83            中信期货     3   
     3                 3524                     -26            中国国际     4   
     4                 3107                     -29            长江期货     5   
     5                 3089                    -154            永安期货     6   
     6                 3030                    -102            华信期货     7   
     7                 2605                     402            东证期货     8   
     8                 2462                    -457            华泰期货     9   
     9                 2278                     -19            广发期货    10   
     10                2221                     -29            中粮期货    11   
     11                1740                    -420            方正中期    12   
     12                1381                     -11            建信期货    13   
     13                1272                     274            光大期货    14   
     14                1186                     -20            弘业期货    15   
     15                1116                    -413            金石期货    16   
     16                1010                     -49            英大期货    17   
     17                 945                      97            海通期货    18   
     18                 877                    -345            鲁证期货    19   
     19                 816                     -38            平安期货    20   
     20               51206                   -1022            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  8071                       24             东证期货   6418   
     1                  5287                        4             永安期货   1948   
     2                  3983                       -4             华信期货   1532   
     3                  3442                     -184             宏源期货   1208   
     4                  3415                      -14             中国国际   1201   
     5                  3368                     -353             大有期货   1177   
     6                  2941                      -80             兴证期货   1062   
     7                  2864                     -221             中信期货    979   
     8                  2813                       -9             金瑞期货    947   
     9                  2571                      100             海通期货    889   
     10                 2506                      -19             国贸期货    792   
     11                 2279                      184             光大期货    652   
     12                 2097                      -23             建信期货    612   
     13                 1914                      -46             兴业期货    537   
     14                 1905                     -567             华泰期货    508   
     15                 1683                      -24           格林大华期货    507   
     16                 1418                       -6             广发期货    503   
     17                 1346                     -125           国投安信期货    482   
     18                 1234                      -41             中大期货    473   
     19                 1199                      -91             渤海期货    451   
     20                56336                    -1495             None  22878   
     
         vol_chg vol_party_name  symbol variety  
     0      2864           华泰期货  CF901       CF  
     1       571           东证期货  CF901       CF  
     2       491           西南期货  CF901       CF  
     3       524           光大期货  CF901       CF  
     4       885           华安期货  CF901       CF  
     5       708           中辉期货  CF901       CF  
     6       617         国投安信期货  CF901       CF  
     7       524           宏源期货  CF901       CF  
     8       903           中融汇信  CF901       CF  
     9       225           海通期货  CF901       CF  
     10       -6           永安期货  CF901       CF  
     11      552           大有期货  CF901       CF  
     12     -995           中信期货  CF901       CF  
     13      226           方正中期  CF901       CF  
     14      367           国泰君安  CF901       CF  
     15      227           南华期货  CF901       CF  
     16      358           银河期货  CF901       CF  
     17      351           徽商期货  CF901       CF  
     18      468           金石期货  CF901       CF  
     19      104           兴业期货  CF901       CF  
     20     9964           None  CF901       CF  ,
     'CF905 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                16579                    1497            中信期货     1   
     1                10825                   -1269            永安期货     2   
     2                 7683                      50          格林大华期货     3   
     3                 6662                     349            东证期货     4   
     4                 6055                     164            中国国际     5   
     5                 5580                    1629          国投安信期货     6   
     6                 4789                     491            国泰君安     7   
     7                 4321                      19            中粮期货     8   
     8                 4000                    -335            银河期货     9   
     9                 3632                      81            一德期货    10   
     10                3328                     465            首创期货    11   
     11                2775                     131            建信期货    12   
     12                2697                      30            上海中期    13   
     13                2667                     271            方正中期    14   
     14                2661                       4            光大期货    15   
     15                2590                     459            南华期货    16   
     16                2536                     120            华泰期货    17   
     17                2524                     -37            东兴期货    18   
     18                2468                     943            东海期货    19   
     19                2355                     -27            金瑞期货    20   
     20               96727                    5035            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                  9838                      488             中粮期货   18123   
     1                  8810                     -343             中信期货    7465   
     2                  8334                     1438             东证期货    7018   
     3                  7578                      -71             长江期货    6726   
     4                  7388                      -21             金瑞期货    6241   
     5                  7208                      457             华泰期货    5833   
     6                  7184                      345           国投安信期货    5656   
     7                  6732                      -48             中金期货    5067   
     8                  6512                      292           格林大华期货    4760   
     9                  6260                      157             华信期货    4639   
     10                 6210                      241             永安期货    4486   
     11                 5090                       21             国贸期货    4120   
     12                 4377                     -298             兴证期货    3820   
     13                 4373                       77             宏源期货    3640   
     14                 4317                      317             建信期货    3095   
     15                 3970                      -49             中国国际    2751   
     16                 3353                      141             华安期货    2739   
     17                 2766                      -30             兴业期货    2698   
     18                 2675                      479             国泰君安    2589   
     19                 2498                       70             银河期货    2576   
     20               115473                     3663             None  104042   
     
         vol_chg vol_party_name  symbol variety  
     0      8362           华泰期货  CF905       CF  
     1      4558           东证期货  CF905       CF  
     2      3539           中信期货  CF905       CF  
     3      3827           中辉期货  CF905       CF  
     4      2466           宏源期货  CF905       CF  
     5      3337           华安期货  CF905       CF  
     6      1202           永安期货  CF905       CF  
     7      3083           海通期货  CF905       CF  
     8      3837         国投安信期货  CF905       CF  
     9      1227           新湖期货  CF905       CF  
     10     2520           南华期货  CF905       CF  
     11     2224           国泰君安  CF905       CF  
     12     2059           徽商期货  CF905       CF  
     13     2057           方正中期  CF905       CF  
     14     2418           国信期货  CF905       CF  
     15     1286           创元期货  CF905       CF  
     16     1776           银河期货  CF905       CF  
     17     1413           光大期货  CF905       CF  
     18     1139           东航期货  CF905       CF  
     19     1818           兴证期货  CF905       CF  
     20    54148           None  CF905       CF  ,
     'CF909 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 1441                       0           浙江新世纪     1   
     1                 1403                      -4            中原期货     2   
     2                 1330                     -32            安粮期货     3   
     3                 1291                     239            迈科期货     4   
     4                 1262                      13          混沌天成期货     5   
     5                 1131                      11            中信期货     6   
     6                 1050                      -2            上海浙石     7   
     7                 1009                     224            浙商期货     8   
     8                  902                      11          国投安信期货     9   
     9                  889                      32            金鹏期货    10   
     10                 710                     252            方正中期    11   
     11                 625                     -27            华安期货    12   
     12                 581                       0            中粮期货    13   
     13                 480                     282            金石期货    14   
     14                 479                      19            广州金控    15   
     15                 407                      13            中融汇信    16   
     16                 405                     112            东证期货    17   
     17                 401                       0            一德期货    18   
     18                 394                      42            永安期货    19   
     19                 389                      96            光大期货    20   
     20               16579                    1281            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name   vol  \
     0                  3238                        0           格林大华期货  1507   
     1                  2643                     -126             国泰君安  1417   
     2                  2597                       -3             永安期货   673   
     3                  2196                       32             一德期货   606   
     4                  1950                        0             东兴期货   511   
     5                  1848                      301           国投安信期货   438   
     6                  1409                      148             银河期货   409   
     7                  1305                      600             天风期货   385   
     8                  1170                        0             中粮期货   384   
     9                   942                      360             首创期货   378   
     10                  681                      -37             华泰期货   365   
     11                  612                       11             兴证期货   361   
     12                  473                        0             光大期货   320   
     13                  409                       24             大地期货   287   
     14                  317                       -2             方正中期   259   
     15                  305                       70             冠通期货   237   
     16                  300                        0             渤海期货   237   
     17                  291                       81             弘业期货   222   
     18                  248                       25             浙商期货   216   
     19                  200                        0             大有期货   201   
     20                23134                     1484             None  9413   
     
         vol_chg vol_party_name  symbol variety  
     0       933           华安期货  CF909       CF  
     1       711           冠通期货  CF909       CF  
     2       656           浙商期货  CF909       CF  
     3        97           天风期货  CF909       CF  
     4       190           中信期货  CF909       CF  
     5       426         国投安信期货  CF909       CF  
     6       121           东证期货  CF909       CF  
     7       313           宏源期货  CF909       CF  
     8        45           方正中期  CF909       CF  
     9       372           首创期货  CF909       CF  
     10      364           迈科期货  CF909       CF  
     11      190           大地期货  CF909       CF  
     12      294           金石期货  CF909       CF  
     13      282           华泰期货  CF909       CF  
     14      108           永安期货  CF909       CF  
     15      146           申银万国  CF909       CF  
     16      204           银河期货  CF909       CF  
     17      102            美尔雅  CF909       CF  
     18      117           国泰君安  CF909       CF  
     19      199           平安期货  CF909       CF  
     20     5870           None  CF909       CF  ,
     'FG901 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 7779                   -4406            永安期货     1   
     1                 4246                     159            中信期货     2   
     2                 3999                    -482            华泰期货     3   
     3                 3957                     386            兴证期货     4   
     4                 3010                     907            国泰君安     5   
     5                 2100                      -2            银河期货     6   
     6                 1673                    -420            方正中期     7   
     7                 1560                   -1366            光大期货     8   
     8                 1537                   -1047            海通期货     9   
     9                 1274                    -106            东证期货    10   
     10                1251                    -215            西部期货    11   
     11                1243                    -349            宏源期货    12   
     12                1220                     151            东航期货    13   
     13                1172                      -2            国信期货    14   
     14                1136                    -165            徽商期货    15   
     15                1061                    -617          国投安信期货    16   
     16                 850                     108            国富期货    17   
     17                 848                     193            华安期货    18   
     18                 708                    -203            广发期货    19   
     19                 684                      17            华创期货    20   
     20               41308                   -7459            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  5909                     -384             永安期货   6586   
     1                  4247                    -2058             海通期货   6226   
     2                  3305                      501             中粮期货   5382   
     3                  3248                    -1139             方正中期   4973   
     4                  3197                      653             国泰君安   4195   
     5                  2848                      816             中信期货   4092   
     6                  2078                    -1094             华泰期货   3511   
     7                  2021                      -90             上海东方   3129   
     8                  1902                     -363             徽商期货   2923   
     9                  1879                    -1599             光大期货   2798   
     10                 1772                     -361             南华期货   2618   
     11                 1768                     -441             兴证期货   2578   
     12                 1696                      -81             弘业期货   2410   
     13                 1511                      701             长江期货   1532   
     14                 1305                      183             银河期货   1501   
     15                 1049                     -102             广发期货   1467   
     16                 1049                     1007             一德期货   1430   
     17                 1008                     -280             东证期货   1313   
     18                  894                       70             金元期货   1277   
     19                  750                     -517             申银万国   1177   
     20                43436                    -4578             None  61118   
     
         vol_chg vol_party_name  symbol variety  
     0     -3360           新湖期货  FG901       FG  
     1     -2366           永安期货  FG901       FG  
     2      -273           华泰期货  FG901       FG  
     3      -263           海通期货  FG901       FG  
     4     -1834           光大期货  FG901       FG  
     5     -1516           国泰君安  FG901       FG  
     6       425           中信期货  FG901       FG  
     7      -993           方正中期  FG901       FG  
     8     -1309           华安期货  FG901       FG  
     9     -1107           东证期货  FG901       FG  
     10    -1375           徽商期货  FG901       FG  
     11      244         国投安信期货  FG901       FG  
     12     -381           宏源期货  FG901       FG  
     13      307           长江期货  FG901       FG  
     14     -915           银河期货  FG901       FG  
     15     -862           申银万国  FG901       FG  
     16      146           建信期货  FG901       FG  
     17     -445           兴证期货  FG901       FG  
     18    -1609           南华期货  FG901       FG  
     19     1013           一德期货  FG901       FG  
     20   -16473           None  FG901       FG  ,
     'FG905 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 5678                     276            永安期货     1   
     1                 3357                    -410            海通期货     2   
     2                 2489                       9          国投安信期货     3   
     3                 2297                     740            国泰君安     4   
     4                 2143                      43            银河期货     5   
     5                 2024                     219            宏源期货     6   
     6                 1813                     726            新湖期货     7   
     7                 1750                      81            中信期货     8   
     8                 1525                     208            方正中期     9   
     9                 1127                    -199            华泰期货    10   
     10                1105                       9            国信期货    11   
     11                 945                     250            徽商期货    12   
     12                 935                     -54            兴证期货    13   
     13                 778                      11            西部期货    14   
     14                 761                      97            东航期货    15   
     15                 651                     -25            南华期货    16   
     16                 634                       0            中辉期货    17   
     17                 622                     -51            中国国际    18   
     18                 607                     -48            光大期货    19   
     19                 597                       4            招商期货    20   
     20               31838                    1886            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  3824                     -492             国泰君安   4369   
     1                  3285                     -729             中信期货   2752   
     2                  2532                      -60             摩根大通   2701   
     3                  2323                      847             新湖期货   2486   
     4                  1598                      154             永安期货   2480   
     5                  1576                      561             广发期货   2404   
     6                  1537                      293             方正中期   2258   
     7                  1230                     1045             南华期货   1796   
     8                  1196                     -102             东证期货   1729   
     9                  1183                     -188             华泰期货   1690   
     10                 1023                     -652             中金期货   1555   
     11                 1021                      140             华安期货   1417   
     12                  951                        0             道通期货   1384   
     13                  903                     -494             海通期货   1143   
     14                  851                      -65             宝城期货   1028   
     15                  826                      217             银河期货   1019   
     16                  812                     -115             光大期货    962   
     17                  809                       19             宏源期货    906   
     18                  805                      -36             国信期货    889   
     19                  745                       29             徽商期货    781   
     20                29030                      372             None  35749   
     
         vol_chg vol_party_name  symbol variety  
     0      -696           新湖期货  FG905       FG  
     1      -642           永安期货  FG905       FG  
     2      1200           方正中期  FG905       FG  
     3       116           国泰君安  FG905       FG  
     4      1920           南华期货  FG905       FG  
     5      -165           华安期货  FG905       FG  
     6      -677           中信期货  FG905       FG  
     7      -434           宏源期货  FG905       FG  
     8      -217           东证期货  FG905       FG  
     9      -491           海通期货  FG905       FG  
     10     -787           华泰期货  FG905       FG  
     11     -779           徽商期货  FG905       FG  
     12      577           银河期货  FG905       FG  
     13      139           东航期货  FG905       FG  
     14      496           申银万国  FG905       FG  
     15      516           广发期货  FG905       FG  
     16      151           长江期货  FG905       FG  
     17        7           大地期货  FG905       FG  
     18     -919           中粮期货  FG905       FG  
     19     -162           光大期货  FG905       FG  
     20     -847           None  FG905       FG  ,
     'MA901 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                52782                  -10712            海通期货     1   
     1                27789                   -2949            华泰期货     2   
     2                14342                    1270            中信期货     3   
     3                13967                   -2164            光大期货     4   
     4                12321                   -6316            永安期货     5   
     5                10980                   -1241            徽商期货     6   
     6                10052                    -706            国泰君安     7   
     7                 7219                      -5            国信期货     8   
     8                 6410                    -407            新湖期货     9   
     9                 6355                     152            山西三立    10   
     10                6290                   -4911            西部期货    11   
     11                6047                   -1056            申银万国    12   
     12                5640                    -356            华安期货    13   
     13                5407                   -3539            兴证期货    14   
     14                5226                    2502            国贸期货    15   
     15                4969                   -4313            东证期货    16   
     16                4937                   -1213            中财期货    17   
     17                4363                    -988            国海良时    18   
     18                4334                    -545            银河期货    19   
     19                4304                     496            浙商期货    20   
     20              213734                  -37001            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name      vol  \
     0                 63875                   -10011             海通期货   267381   
     1                 34452                     -224             华泰期货   181307   
     2                 23974                     5546             永安期货   102050   
     3                 14170                     -609             银河期货    77194   
     4                 13808                     1006             中信期货    70192   
     5                 13165                    -3464             光大期货    69526   
     6                 10495                    -1176             国泰君安    66367   
     7                 10477                     -423             信达期货    62116   
     8                  9974                     -462             东海期货    61052   
     9                  9282                     2715             兴证期货    58524   
     10                 8370                     -190             新湖期货    53836   
     11                 6912                    -4478             西部期货    47564   
     12                 5639                    -4199             东证期货    44189   
     13                 5460                    -1603             国富期货    41961   
     14                 4887                     -183             方正中期    37469   
     15                 4063                     1197             浙商期货    37459   
     16                 3787                    -5246             申银万国    37236   
     17                 3690                    -1035             上海中期    37088   
     18                 3623                    -1510             创元期货    36842   
     19                 3603                      -39             国信期货    36011   
     20               253706                   -24388             None  1425364   
     
         vol_chg vol_party_name  symbol variety  
     0     -8744           海通期货  MA901       MA  
     1    -11859           华泰期货  MA901       MA  
     2    -10463           创元期货  MA901       MA  
     3    -39332           徽商期货  MA901       MA  
     4      2933           光大期货  MA901       MA  
     5     -1291           永安期货  MA901       MA  
     6    -16956           华安期货  MA901       MA  
     7    -10150           东证期货  MA901       MA  
     8     -7626           中信期货  MA901       MA  
     9     -7619           申银万国  MA901       MA  
     10   -18826           方正中期  MA901       MA  
     11    -7143           国泰君安  MA901       MA  
     12    -5944           新湖期货  MA901       MA  
     13    -8627           中信建投  MA901       MA  
     14    -7719           浙商期货  MA901       MA  
     15     -734           中辉期货  MA901       MA  
     16   -22061           广发期货  MA901       MA  
     17   -14250           东航期货  MA901       MA  
     18    -5663           安粮期货  MA901       MA  
     19    -1831           东方财富  MA901       MA  
     20  -203905           None  MA901       MA  ,
     'MA905 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                24795                    -900            永安期货     1   
     1                18497                  -10746            华泰期货     2   
     2                12676                   -3567            光大期货     3   
     3                12107                    -154            海通期货     4   
     4                11893                    -660            申银万国     5   
     5                 7982                    -229            东海期货     6   
     6                 7565                    1728            国泰君安     7   
     7                 7055                    2495            中信期货     8   
     8                 6834                     406            新湖期货     9   
     9                 6562                   -1030          国投安信期货    10   
     10                6504                    3378            广发期货    11   
     11                5909                    1472            方正中期    12   
     12                5817                     213            安粮期货    13   
     13                5788                   -1608            东证期货    14   
     14                5042                    1191          五矿经易期货    15   
     15                4732                    2114            徽商期货    16   
     16                4290                    1847            创元期货    17   
     17                4183                      86            银河期货    18   
     18                3739                    2469            瑞达期货    19   
     19                3564                    -173            宏源期货    20   
     20              165534                   -1668            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 23916                    -8629             华泰期货  129357   
     1                 23639                     9810             国泰君安   68279   
     2                 16344                     -548             银河期货   56333   
     3                 14882                     2785             海通期货   46867   
     4                 11619                     1052             方正中期   37426   
     5                 11507                    -4974             光大期货   35589   
     6                 10330                    -4757             永安期货   33698   
     7                  9509                     1753             中信期货   33360   
     8                  7587                       55             中金期货   29707   
     9                  7417                     3542             广发期货   28624   
     10                 6402                     -293             新湖期货   27477   
     11                 5668                      -57             申银万国   27294   
     12                 5608                     2206           国投安信期货   27014   
     13                 5020                      560             东证期货   25628   
     14                 4854                      520             广州期货   25221   
     15                 4597                      338             东海期货   22585   
     16                 4187                      772             浙商期货   22486   
     17                 4074                      -58             华安期货   21342   
     18                 3928                      530             中辉期货   21123   
     19                 3483                     1984             国贸期货   19216   
     20               184571                     6591             None  738626   
     
         vol_chg vol_party_name  symbol variety  
     0     -3851           华泰期货  MA905       MA  
     1      -225           海通期货  MA905       MA  
     2      7614           光大期货  MA905       MA  
     3      -631           徽商期货  MA905       MA  
     4     -1771           华安期货  MA905       MA  
     5    -11835           永安期货  MA905       MA  
     6      9509           国泰君安  MA905       MA  
     7     -1143           方正中期  MA905       MA  
     8      3953           新湖期货  MA905       MA  
     9      7917           中信期货  MA905       MA  
     10    10783           弘业期货  MA905       MA  
     11    -6278           浙商期货  MA905       MA  
     12     9618           广发期货  MA905       MA  
     13    -7354           东证期货  MA905       MA  
     14    -3389           申银万国  MA905       MA  
     15     2721           创元期货  MA905       MA  
     16       72           安粮期货  MA905       MA  
     17    -7754           宏源期货  MA905       MA  
     18    -3235           东航期货  MA905       MA  
     19    -1773          新纪元期货  MA905       MA  
     20     2948           None  MA905       MA  ,
     'MA907 ':    long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                   2                       1            安粮期货     1   
     1                   2                       0            中信建投     2   
     2                   1                       0            徽商期货     3   
     3                   1                       0            福能期货     4   
     4                   1                       0            中国国际     5   
     5                   0                       0               0     6   
     6                   7                       1            None   999   
     
        short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                    6                        1             浙商期货    4   
     1                    1                        1             华安期货    3   
     2                    0                        0                0    2   
     3                    0                        0                0    1   
     4                    0                        0                0    1   
     5                    0                        0                0    1   
     6                    7                        2             None   12   
     
        vol_chg vol_party_name  symbol variety  
     0        4           信达期货  MA907       MA  
     1       -1           浙商期货  MA907       MA  
     2      -18           江苏东华  MA907       MA  
     3       -8           安粮期货  MA907       MA  
     4       -1           华安期货  MA907       MA  
     5        0           深圳瑞龙  MA907       MA  
     6      -24           None  MA907       MA  ,
     'MA909 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 1746                     473            东证期货     1   
     1                 1211                      61            徽商期货     2   
     2                  881                       1           浙江新世纪     3   
     3                  389                      15            中信建投     4   
     4                  371                      -9            华泰期货     5   
     5                  367                      23            方正中期     6   
     6                  353                       2            光大期货     7   
     7                  353                     125            东海期货     8   
     8                  299                      19            国泰君安     9   
     9                  278                       0            广发期货    10   
     10                 263                     -18            浙商期货    11   
     11                 247                      10            南华期货    12   
     12                 228                    -217            宏源期货    13   
     13                 224                       9            福能期货    14   
     14                 224                     158            中辉期货    15   
     15                 186                    -251            神华期货    16   
     16                 145                      10            银河期货    17   
     17                 144                    -141            创元期货    18   
     18                 141                      91            新湖期货    19   
     19                 139                      56            东航期货    20   
     20                8189                     417            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name   vol  \
     0                  4771                       65             安粮期货   900   
     1                  1052                       -1             招金期货   852   
     2                   731                       37             浙商期货   730   
     3                   513                      100             中财期货   590   
     4                   436                       81             东海期货   525   
     5                   318                      -66             永安期货   459   
     6                   315                        8           五矿经易期货   410   
     7                   293                       57             华泰期货   383   
     8                   263                      -88             宏源期货   298   
     9                   245                     -115             创元期货   289   
     10                  152                       14             和合期货   286   
     11                  140                        1             首创期货   274   
     12                  140                       30             一德期货   274   
     13                  101                       -1             中信期货   256   
     14                   98                       20             中粮期货   231   
     15                   95                       29             方正中期   205   
     16                   86                       -2             徽商期货   200   
     17                   75                      -56             广发期货   177   
     18                   68                        3             东证期货   165   
     19                   67                       20             锦泰期货   153   
     20                 9959                      136             None  7657   
     
         vol_chg vol_party_name  symbol variety  
     0       127           创元期货  MA909       MA  
     1       242           东海期货  MA909       MA  
     2      -471           安粮期货  MA909       MA  
     3       485           东证期货  MA909       MA  
     4       304           东航期货  MA909       MA  
     5       347         国投安信期货  MA909       MA  
     6         0           永安期货  MA909       MA  
     7      -252           宏源期货  MA909       MA  
     8       126           方正中期  MA909       MA  
     9      -227           华安期货  MA909       MA  
     10      263           金瑞期货  MA909       MA  
     11       17           国金期货  MA909       MA  
     12      123           广发期货  MA909       MA  
     13      254           神华期货  MA909       MA  
     14      -41           徽商期货  MA909       MA  
     15      117           中辉期货  MA909       MA  
     16      152           光大期货  MA909       MA  
     17       95           新湖期货  MA909       MA  
     18      -12           长安期货  MA909       MA  
     19      -66           中信建投  MA909       MA  
     20     1583           None  MA909       MA  ,
     'OI901 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 8249                      20            国富期货     1   
     1                 4909                     -61          国投安信期货     2   
     2                 4709                     -78            银河期货     3   
     3                 4011                     -60            建信期货     4   
     4                 3683                   -1049            永安期货     5   
     5                 3649                    -351            国泰君安     6   
     6                 3156                    -110            鲁证期货     7   
     7                 2566                      -4            兴证期货     8   
     8                 2379                     299            广发期货     9   
     9                 2164                    -467            中信期货    10   
     10                1853                     -92            华信期货    11   
     11                1725                    -471            兴业期货    12   
     12                1681                       6            广州期货    13   
     13                1582                      -5            中国国际    14   
     14                1512                     -27          五矿经易期货    15   
     15                1343                     178            中粮期货    16   
     16                1337                      30            安粮期货    17   
     17                1244                      -8            上海大陆    18   
     18                1190                      27            华金期货    19   
     19                1095                    -197            宏源期货    20   
     20               54037                   -2420            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  7138                      262             中粮期货   8996   
     1                  6528                     -683             中信期货   4406   
     2                  5524                      289           国投安信期货   3570   
     3                  4679                        5             银河期货   2914   
     4                  3431                        2             南华期货   2666   
     5                  3072                       -2             西部期货   2508   
     6                  3032                       -4             建信期货   1936   
     7                  3001                      -52             上海中期   1484   
     8                  2887                        7             永安期货   1395   
     9                  2800                        0             长安期货   1338   
     10                 2739                      -24             申银万国   1082   
     11                 2708                     -214             新湖期货   1060   
     12                 2448                     -407             宏源期货    948   
     13                 2043                     -490             国富期货    868   
     14                 1554                     -593             中国国际    788   
     15                 1452                     -226             海通期货    779   
     16                 1366                        0             深圳瑞龙    738   
     17                 1274                       -4             国贸期货    701   
     18                 1195                      -18             广发期货    701   
     19                 1079                      -62             东证期货    675   
     20                59950                    -2214             None  39553   
     
         vol_chg vol_party_name  symbol variety  
     0     -5841           华泰期货  OI901       OI  
     1      -857           中信期货  OI901       OI  
     2     -2130           海通期货  OI901       OI  
     3       387           华安期货  OI901       OI  
     4     -1125           建信期货  OI901       OI  
     5      -397           光大期货  OI901       OI  
     6      -448           东证期货  OI901       OI  
     7     -2174         国投安信期货  OI901       OI  
     8     -2810           广发期货  OI901       OI  
     9     -1599           永安期货  OI901       OI  
     10     -555           冠通期货  OI901       OI  
     11     -278           倍特期货  OI901       OI  
     12      112           宏源期货  OI901       OI  
     13     -622           创元期货  OI901       OI  
     14     -249           申银万国  OI901       OI  
     15      100           兴业期货  OI901       OI  
     16    -1743           中粮期货  OI901       OI  
     17      530            美尔雅  OI901       OI  
     18      537           上海中期  OI901       OI  
     19     -146           天风期货  OI901       OI  
     20   -19308           None  OI901       OI  ,
     'OI905 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                10981                     363            国富期货     1   
     1                10202                    1440          国投安信期货     2   
     2                 9765                      89            国泰君安     3   
     3                 7539                    -253            中信建投     4   
     4                 6632                    1562            银河期货     5   
     5                 5946                     687            宏源期货     6   
     6                 5064                     148            新湖期货     7   
     7                 4899                     485            广发期货     8   
     8                 3749                      86            中信期货     9   
     9                 3296                     958            永安期货    10   
     10                3033                    -509            首创期货    11   
     11                2879                       5            金石期货    12   
     12                2705                    -467            兴证期货    13   
     13                2688                     -22            平安期货    14   
     14                2532                    -127            倍特期货    15   
     15                2065                       0            国都期货    16   
     16                1938                     434            广州期货    17   
     17                1752                     -59            中粮期货    18   
     18                1747                    -191            华信期货    19   
     19                1682                    -106            兴业期货    20   
     20               91094                    4523            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 18477                      298             中粮期货   14986   
     1                 17801                      -57           国投安信期货   13669   
     2                 10346                     1319             中信期货   11980   
     3                  8270                      641             广发期货    8876   
     4                  5783                      -27             中金期货    6989   
     5                  5283                      103             华泰期货    6976   
     6                  4711                      535             中国国际    6397   
     7                  4128                      138             永安期货    5540   
     8                  3436                      258             鲁证期货    5016   
     9                  3264                     -208             徽商期货    4948   
     10                 3249                      118             南华期货    4475   
     11                 2604                      280             深圳瑞龙    4429   
     12                 2438                      502             海通期货    4321   
     13                 2347                        8             建信期货    4260   
     14                 2235                      500             摩根大通    4136   
     15                 2194                       -6             华信期货    3388   
     16                 2079                        7             国泰君安    2589   
     17                 1959                      114             安粮期货    2493   
     18                 1949                      116             兴证期货    2448   
     19                 1721                       30             新湖期货    2173   
     20               104274                     4669             None  120089   
     
         vol_chg vol_party_name  symbol variety  
     0     -1774           建信期货  OI905       OI  
     1     -5168           华泰期货  OI905       OI  
     2        72           海通期货  OI905       OI  
     3        27           东证期货  OI905       OI  
     4      -925           中信期货  OI905       OI  
     5      -118           华安期货  OI905       OI  
     6      2501         国投安信期货  OI905       OI  
     7      -440           光大期货  OI905       OI  
     8     -2846           广发期货  OI905       OI  
     9      2343           银河期货  OI905       OI  
     10      264           中辉期货  OI905       OI  
     11     2264           申银万国  OI905       OI  
     12     -720           徽商期货  OI905       OI  
     13      233           宏源期货  OI905       OI  
     14     -895           国泰君安  OI905       OI  
     15    -2604           永安期货  OI905       OI  
     16     -157           国元期货  OI905       OI  
     17      575            美尔雅  OI905       OI  
     18    -1058           创元期货  OI905       OI  
     19      179           方正中期  OI905       OI  
     20    -8247           None  OI905       OI  ,
     'OI909 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 2018                      15            国富期货     1   
     1                 1652                     560            广发期货     2   
     2                 1619                     124          国投安信期货     3   
     3                 1342                      36            建信期货     4   
     4                 1030                     -13            银河期货     5   
     5                  733                     520            宏源期货     6   
     6                  623                      12            国信期货     7   
     7                  620                       2            华泰期货     8   
     8                  407                       9            浙商期货     9   
     9                  407                       1            海证期货    10   
     10                 400                     -50            中原期货    11   
     11                 384                       0          格林大华期货    12   
     12                 378                      75            大有期货    13   
     13                 307                     300            深圳瑞龙    14   
     14                 301                       0            长安期货    15   
     15                 300                      -2            光大期货    16   
     16                 269                     237            鲁证期货    17   
     17                 203                     -93            徽商期货    18   
     18                 182                      -8            中信期货    19   
     19                 169                       2            华金期货    20   
     20               13344                    1727            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name   vol  \
     0                  3473                     -150             兴证期货   934   
     1                  2797                        0             摩根大通   623   
     2                  1509                       42             首创期货   612   
     3                  1000                      387             兴业期货   549   
     4                   915                      -69           国投安信期货   485   
     5                   892                        9             长江期货   480   
     6                   638                      170             申银万国   473   
     7                   500                        0             和合期货   330   
     8                   480                      202             中信期货   318   
     9                   447                      179             中国国际   304   
     10                  388                      362             鲁证期货   231   
     11                  321                        0             永安期货   229   
     12                  245                       11             华安期货   214   
     13                  184                        2             深圳瑞龙   204   
     14                  166                       36             国海良时   197   
     15                  144                      105             华泰期货   194   
     16                  129                        0             银河期货   176   
     17                  129                      104             广发期货   174   
     18                  124                       49             金瑞期货   172   
     19                  110                       20             国联期货   155   
     20                14591                     1459             None  7054   
     
         vol_chg vol_party_name  symbol variety  
     0       353           广发期货  OI909       OI  
     1       577           鲁证期货  OI909       OI  
     2       429           宏源期货  OI909       OI  
     3       390         国投安信期货  OI909       OI  
     4       396           兴业期货  OI909       OI  
     5       -47           中信期货  OI909       OI  
     6      -128           华安期货  OI909       OI  
     7       312           深圳瑞龙  OI909       OI  
     8       204           国元期货  OI909       OI  
     9      -439           创元期货  OI909       OI  
     10     -319           国金期货  OI909       OI  
     11       28           西南期货  OI909       OI  
     12      185           中国国际  OI909       OI  
     13     -559           浙商期货  OI909       OI  
     14      127           兴证期货  OI909       OI  
     15      -14           申银万国  OI909       OI  
     16       -9           华金期货  OI909       OI  
     17     -145           徽商期货  OI909       OI  
     18      141           光大期货  OI909       OI  
     19       39           新湖期货  OI909       OI  
     20     1521           None  OI909       OI  ,
     'PM901 ':    long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                   5                       0            上海中期     1   
     1                   4                       0            华信期货     2   
     2                   1                       0            东航期货     3   
     3                  10                       0            None   999   
     
        short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                    6                        0             华信期货    0   
     1                    4                        0             永安期货    0   
     2                    0                        0                0    0   
     3                   10                        0             None    0   
     
        vol_chg vol_party_name  symbol variety  
     0        0              0  PM901       PM  
     1        0              0  PM901       PM  
     2        0              0  PM901       PM  
     3        0           None  PM901       PM  ,
     'RM901 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 6568                    -300          国投安信期货     1   
     1                 5672                    -838            永安期货     2   
     2                 4968                     -82            申银万国     3   
     3                 4422                     219            中信期货     4   
     4                 3909                     -32            广州金控     5   
     5                 3327                    -611            徽商期货     6   
     6                 2537                   -1554            弘业期货     7   
     7                 2403                     -58            华金期货     8   
     8                 2249                     -77            国泰君安     9   
     9                 1971                    1128            银河期货    10   
     10                1681                      -4            广发期货    11   
     11                1367                      57            和合期货    12   
     12                1302                    -124            方正中期    13   
     13                1166                    -350            兴证期货    14   
     14                1094                    -133            中粮期货    15   
     15                1092                   -1201            海通期货    16   
     16                1073                    -296            华泰期货    17   
     17                1045                      97            长江期货    18   
     18                1033                      -2            天风期货    19   
     19                 880                     206            中州期货    20   
     20               49759                   -3955            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                  6736                    -2014             中信期货   59674   
     1                  6471                     1025             中粮期货   46843   
     2                  5530                     -208             兴业期货   36332   
     3                  4528                     -202             一德期货   22293   
     4                  3420                        3             广州金控   19737   
     5                  3268                     -951             国泰君安   19254   
     6                  3245                      634             兴证期货   17506   
     7                  2511                    -1655             弘业期货   16272   
     8                  2330                      -36             广发期货   15199   
     9                  2189                      105           国投安信期货   13835   
     10                 1976                     -544             光大期货    9876   
     11                 1868                      939             南华期货    8398   
     12                 1696                    -1105             摩根大通    7776   
     13                 1343                       58             中国国际    7687   
     14                 1299                      173             英大期货    7506   
     15                 1243                      251             海通期货    7365   
     16                 1205                       22             恒泰期货    6952   
     17                 1115                     -233             东兴期货    6341   
     18                 1101                      -89             长江期货    5872   
     19                 1086                      -24             金瑞期货    5725   
     20                54160                    -3851             None  340443   
     
         vol_chg vol_party_name  symbol variety  
     0     -7405           海通期货  RM901       RM  
     1      7544           华泰期货  RM901       RM  
     2      5523           光大期货  RM901       RM  
     3     -5507           东证期货  RM901       RM  
     4     -8621           建信期货  RM901       RM  
     5      1121           兴证期货  RM901       RM  
     6      5621           国泰君安  RM901       RM  
     7      -842           金瑞期货  RM901       RM  
     8     -1936           徽商期货  RM901       RM  
     9       255           中信期货  RM901       RM  
     10    -3456           方正中期  RM901       RM  
     11    -4136           创元期货  RM901       RM  
     12    -4158           广发期货  RM901       RM  
     13    -3447           华安期货  RM901       RM  
     14     3938           中信建投  RM901       RM  
     15     -241           中辉期货  RM901       RM  
     16     1355           长江期货  RM901       RM  
     17      250           弘业期货  RM901       RM  
     18     1384           西部期货  RM901       RM  
     19     2217           南华期货  RM901       RM  
     20   -10541           None  RM901       RM  ,
     'RM903 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                10605                       0            冠通期货     1   
     1                 7685                       0            国元期货     2   
     2                 6621                       0            兴证期货     3   
     3                 5000                   -5000            国贸期货     4   
     4                 2350                       0            中辉期货     5   
     5                  250                      24            东吴期货     6   
     6                   86                       0            中信期货     7   
     7                    7                       1            银河期货     8   
     8                    6                       0            一德期货     9   
     9                    4                       0            徽商期货    10   
     10                   4                       0            鲁证期货    11   
     11                   3                       0            大有期货    12   
     12                   2                       1            华泰期货    13   
     13                   2                       0            中原期货    14   
     14                   2                       0            东证期货    15   
     15                   1                       0            华创期货    16   
     16                   1                       0            广发期货    17   
     17                   1                       0            永安期货    18   
     18                   1                       0            新湖期货    19   
     19                   0                       0               0    20   
     20               32631                   -4974            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                 10605                        0             冠通期货  10004   
     1                  7685                        0             国元期货   8008   
     2                  6658                       38             兴证期货    178   
     3                  5000                    -5000             国贸期货     87   
     4                  2350                        0             中辉期货     77   
     5                   114                      -15             东吴期货     56   
     6                    90                        0             海航期货     38   
     7                    28                       13             国泰君安     36   
     8                    28                       25             国海良时     31   
     9                    26                       13             华泰期货     27   
     10                   11                      -53             徽商期货     24   
     11                   11                       -3             浙商期货     23   
     12                    6                        6             中信期货     14   
     13                    5                        1             平安期货      8   
     14                    4                       -4             中粮期货      8   
     15                    3                        2             方正中期      8   
     16                    3                        2             鲁证期货      6   
     17                    2                        0             长江期货      6   
     18                    2                        0             海通期货      6   
     19                    0                        0                0      4   
     20                32631                    -4975             None  18649   
     
         vol_chg vol_party_name  symbol variety  
     0     10004           国贸期货  RM903       RM  
     1         8           光大期货  RM903       RM  
     2       151           中粮期货  RM903       RM  
     3        62           徽商期货  RM903       RM  
     4        75           东吴期货  RM903       RM  
     5        56           华鑫期货  RM903       RM  
     6        38           兴证期货  RM903       RM  
     7        34           弘业期货  RM903       RM  
     8        27           国海良时  RM903       RM  
     9        27           国泰君安  RM903       RM  
     10       24           华泰期货  RM903       RM  
     11       19           银河期货  RM903       RM  
     12       14         格林大华期货  RM903       RM  
     13        8           华信期货  RM903       RM  
     14        6           东海期货  RM903       RM  
     15        8           上海东亚  RM903       RM  
     16        6           方正中期  RM903       RM  
     17        6           中信期货  RM903       RM  
     18        6           宏源期货  RM903       RM  
     19        4           浙商期货  RM903       RM  
     20    10583           None  RM903       RM  ,
     'RM905 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                22222                    1247            中信期货     1   
     1                15933                    -927            申银万国     2   
     2                 9639                    -144            永安期货     3   
     3                 7541                      75            弘业期货     4   
     4                 7062                      54          国投安信期货     5   
     5                 6256                      19          格林大华期货     6   
     6                 5715                   -4960            国贸期货     7   
     7                 5633                     660            兴证期货     8   
     8                 4447                      96            东证期货     9   
     9                 3812                     227            广发期货    10   
     10                3706                     256            中粮期货    11   
     11                3675                    1308            国泰君安    12   
     12                3549                     469            徽商期货    13   
     13                3419                     139            宏源期货    14   
     14                3099                      12            神华期货    15   
     15                2757                     167            中辉期货    16   
     16                2688                    -396            一德期货    17   
     17                2602                     623            华安期货    18   
     18                2595                     130            浙商期货    19   
     19                2511                     304            光大期货    20   
     20              118861                    -641            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 27412                     2659             中信期货   35470   
     1                 22450                     1005           国投安信期货   32400   
     2                 11699                     -199             中粮期货   21614   
     3                  9751                     1411             兴证期货   19964   
     4                  8715                      206             中金期货   16156   
     5                  7664                    -3806             申银万国   14496   
     6                  7349                      529             南华期货   11481   
     7                  6137                     -329             弘业期货   11034   
     8                  5889                      753             国泰君安   10969   
     9                  5225                      -80           格林大华期货   10765   
     10                 5066                    -5037             国贸期货    9761   
     11                 4049                     1510             海通期货    9397   
     12                 3997                     -131             华泰期货    8145   
     13                 3211                        0             摩根大通    7002   
     14                 3076                     1057             银河期货    6721   
     15                 2934                     -192             宏源期货    6353   
     16                 2724                      -39             神华期货    6109   
     17                 2663                      983             天风期货    5987   
     18                 2558                     -476             中辉期货    5797   
     19                 2429                      161             东航期货    5513   
     20               144998                      -15             None  255134   
     
         vol_chg vol_party_name  symbol variety  
     0     -2246           海通期货  RM905       RM  
     1      3039           建信期货  RM905       RM  
     2     -1592           光大期货  RM905       RM  
     3      1815           华泰期货  RM905       RM  
     4      2587           中信期货  RM905       RM  
     5      1732           徽商期货  RM905       RM  
     6       186           金瑞期货  RM905       RM  
     7     -1410           华安期货  RM905       RM  
     8      9847           国贸期货  RM905       RM  
     9      2426           国泰君安  RM905       RM  
     10     1421           东证期货  RM905       RM  
     11     1636           申银万国  RM905       RM  
     12    -3289           中辉期货  RM905       RM  
     13    -4310           广发期货  RM905       RM  
     14      271           东航期货  RM905       RM  
     15       44           冠通期货  RM905       RM  
     16     4904         五矿经易期货  RM905       RM  
     17     1948           宏源期货  RM905       RM  
     18     -959           长江期货  RM905       RM  
     19      297           国金期货  RM905       RM  
     20    18347           None  RM905       RM  ,
     'RM907 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                14100                       0            冠通期货     1   
     1                 7818                       0            兴证期货     2   
     2                 2450                       0            中辉期货     3   
     3                 1000                       0            宏源期货     4   
     4                  500                       0            国贸期货     5   
     5                   14                       0            国海良时     6   
     6                    6                       0            长江期货     7   
     7                    3                       0            中信期货     8   
     8                    3                       0            中国国际     9   
     9                    2                       1            江苏东华    10   
     10                   2                       0            徽商期货    11   
     11                   2                       2            国泰君安    12   
     12                   1                       0            招商期货    13   
     13                   1                       0          东方汇金期货    14   
     14                   1                       0            中原期货    15   
     15               25903                       3            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                 14100                        0             冠通期货    4   
     1                  7800                        0             兴证期货    4   
     2                  2450                        0             中辉期货    2   
     3                  1000                        0             宏源期货    1   
     4                   500                        0             国贸期货    1   
     5                    17                        0             国海良时    1   
     6                    10                        1             浙商期货    1   
     7                     9                        0             一德期货    1   
     8                     6                        0             华泰期货    1   
     9                     3                        0             长江期货    0   
     10                    2                        1             鲁证期货    0   
     11                    2                        0             迈科期货    0   
     12                    2                       -1             东吴期货    0   
     13                    1                        0             安粮期货    0   
     14                    1                        0             中国国际    0   
     15                25903                        1             None   16   
     
         vol_chg vol_party_name  symbol variety  
     0         2           中银国际  RM907       RM  
     1         4           东证期货  RM907       RM  
     2         2           国泰君安  RM907       RM  
     3         1           江苏东华  RM907       RM  
     4        -9           银河期货  RM907       RM  
     5         0           鲁证期货  RM907       RM  
     6        -1           浙商期货  RM907       RM  
     7        -1           东吴期货  RM907       RM  
     8        -2           广州期货  RM907       RM  
     9         0              0  RM907       RM  
     10        0              0  RM907       RM  
     11        0              0  RM907       RM  
     12        0              0  RM907       RM  
     13        0              0  RM907       RM  
     14        0              0  RM907       RM  
     15       -4           None  RM907       RM  ,
     'RM908 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 8000                       0            上海中期     1   
     1                 7050                       0            冠通期货     2   
     2                 4000                   -4000            光大期货     3   
     3                 3900                       0            兴证期货     4   
     4                 3000                       0            银河期货     5   
     5                 1000                       0            宏源期货     6   
     6                    4                       0            长江期货     7   
     7                    2                       0            方正中期     8   
     8                    2                       2            国海良时     9   
     9                    1                       0            鲁证期货    10   
     10                   1                       0            中粮期货    11   
     11               26960                   -3998            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name   vol  \
     0                  8000                        0             上海中期  8000   
     1                  7050                        0             冠通期货     2   
     2                  4000                    -4000             光大期货     1   
     3                  3900                        0             兴证期货     1   
     4                  3000                        0             银河期货     0   
     5                  1000                        0             宏源期货     0   
     6                     5                        0             广州期货     0   
     7                     2                        1             鲁证期货     0   
     8                     1                        1             申银万国     0   
     9                     1                        0             中信期货     0   
     10                    1                        0             国都期货     0   
     11                26960                    -3998             None  8004   
     
         vol_chg vol_party_name  symbol variety  
     0         0           光大期货  RM908       RM  
     1         2           国海良时  RM908       RM  
     2         1           申银万国  RM908       RM  
     3         0           鲁证期货  RM908       RM  
     4         0              0  RM908       RM  
     5         0              0  RM908       RM  
     6         0              0  RM908       RM  
     7         0              0  RM908       RM  
     8         0              0  RM908       RM  
     9         0              0  RM908       RM  
     10        0              0  RM908       RM  
     11        3           None  RM908       RM  ,
     'RM909 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 4643                       4          格林大华期货     1   
     1                 2442                     -41            申银万国     2   
     2                 2166                    2001            中信期货     3   
     3                 2095                       4            上海中期     4   
     4                 2033                       6            广发期货     5   
     5                  864                       0            华安期货     6   
     6                  658                      -1            浙商期货     7   
     7                  651                      23            徽商期货     8   
     8                  530                     -30            银河期货     9   
     9                  524                      35            弘业期货    10   
     10                 519                      16            华泰期货    11   
     11                 511                       0            国贸期货    12   
     12                 447                      22            恒泰期货    13   
     13                 419                       8          国投安信期货    14   
     14                 417                       3            方正中期    15   
     15                 399                     212            中国国际    16   
     16                 343                       4            东航期货    17   
     17                 329                      -6            永安期货    18   
     18                 328                      22            国联期货    19   
     19                 323                       7            中辉期货    20   
     20               20641                    2289            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  6061                        5             申银万国   4246   
     1                  4472                      -30           格林大华期货   1589   
     2                  3411                     -266             徽商期货    805   
     3                  2099                     2005             中信期货    683   
     4                  2026                       -4             上海中期    670   
     5                   893                        1             东证期货    578   
     6                   661                     -103             长江期货    486   
     7                   603                        1             信达期货    378   
     8                   516                       -6             永安期货    313   
     9                   501                        0             国贸期货    282   
     10                  479                       79             浙商期货    248   
     11                  340                        0             中融汇信    242   
     12                  302                        1             鲁证期货    230   
     13                  301                        0             天风期货    216   
     14                  293                       39             国泰君安    213   
     15                  259                        1             金元期货    207   
     16                  258                        0             中天期货    191   
     17                  257                       91             华安期货    177   
     18                  240                       99             方正中期    170   
     19                  237                      104           国投安信期货    153   
     20                24209                     2017             None  12077   
     
         vol_chg vol_party_name  symbol variety  
     0      4079           中信期货  RM909       RM  
     1       525           徽商期货  RM909       RM  
     2         3           创元期货  RM909       RM  
     3       135           华安期货  RM909       RM  
     4       441           浙商期货  RM909       RM  
     5       124           中信建投  RM909       RM  
     6       167           国泰君安  RM909       RM  
     7       -45           国金期货  RM909       RM  
     8       313           广州金控  RM909       RM  
     9       131           中国国际  RM909       RM  
     10      207           倍特期货  RM909       RM  
     11       44           东航期货  RM909       RM  
     12      -26           方正中期  RM909       RM  
     13      143           平安期货  RM909       RM  
     14     -136           宏源期货  RM909       RM  
     15      139           海证期货  RM909       RM  
     16     -108           长安期货  RM909       RM  
     17      -88           广发期货  RM909       RM  
     18       24         国投安信期货  RM909       RM  
     19       98           长城期货  RM909       RM  
     20     6170           None  RM909       RM  ,
     'SF812 ':    long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                   7                       0          五矿经易期货     1   
     1                   7                       0            None   999   
     
        short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                    7                        0             中原期货    0   
     1                    7                        0             None    0   
     
        vol_chg vol_party_name  symbol variety  
     0        0              0  SF812       SF  
     1        0           None  SF812       SF  ,
     'SF901 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 3559                     224            中信期货     1   
     1                 2414                     298          五矿经易期货     2   
     2                 2163                     798            华泰期货     3   
     3                 1474                     151            弘业期货     4   
     4                 1125                     381          国投安信期货     5   
     5                 1051                     315            新湖期货     6   
     6                 1000                     344            国信期货     7   
     7                  891                    -213            浙商期货     8   
     8                  850                    -284            申银万国     9   
     9                  828                     224            华龙期货    10   
     10                 818                     -72            东证期货    11   
     11                 743                     -18            西部期货    12   
     12                 663                     478            一德期货    13   
     13                 564                     -37            上海中期    14   
     14                 473                     238            兴证期货    15   
     15                 438                     433            江西瑞奇    16   
     16                 438                      24            鲁证期货    17   
     17                 413                     -34            中财期货    18   
     18                 404                     -38            中信建投    19   
     19                 386                     297            华鑫期货    20   
     20               20695                    3509            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  2594                       78             中信期货   6906   
     1                  2549                      842             华泰期货   4783   
     2                  1804                      399             兴证期货   3208   
     3                  1581                     -141             中金期货   3062   
     4                  1195                      -93             宏源期货   2710   
     5                  1068                      389             新湖期货   2002   
     6                  1034                       49             东证期货   1931   
     7                   873                      -33           五矿经易期货   1532   
     8                   859                      168             东航期货   1481   
     9                   816                     -123             国泰君安   1431   
     10                  640                      184             光大期货   1385   
     11                  562                       50             永安期货   1294   
     12                  554                      -65             申银万国   1243   
     13                  538                      282             国信期货   1230   
     14                  529                     -481             南华期货   1136   
     15                  503                       39             中财期货   1058   
     16                  491                     -313             方正中期   1028   
     17                  490                      -15             东吴期货   1021   
     18                  467                      247             广发期货   1016   
     19                  460                      -47             华安期货    993   
     20                19607                     1416             None  40450   
     
         vol_chg vol_party_name  symbol variety  
     0      -419           华泰期货  SF901       SF  
     1      -109           东证期货  SF901       SF  
     2      -466           新湖期货  SF901       SF  
     3     -1845           中信期货  SF901       SF  
     4       422           国信期货  SF901       SF  
     5      -485           弘业期货  SF901       SF  
     6       751           方正中期  SF901       SF  
     7       -13           华安期货  SF901       SF  
     8      -281         五矿经易期货  SF901       SF  
     9      1021           南华期货  SF901       SF  
     10     -839           兴证期货  SF901       SF  
     11     -833           徽商期货  SF901       SF  
     12       92           银河期货  SF901       SF  
     13      386         国投安信期货  SF901       SF  
     14      232           西部期货  SF901       SF  
     15      287           一德期货  SF901       SF  
     16     -737           中原期货  SF901       SF  
     17      167           华信期货  SF901       SF  
     18      217           东航期货  SF901       SF  
     19       69           国泰君安  SF901       SF  
     20    -2383           None  SF901       SF  ,
     'SM901 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                10084                    -134          国投安信期货     1   
     1                 8072                     140            上海大陆     2   
     2                 5203                     210            弘业期货     3   
     3                 4880                    -408            中信期货     4   
     4                 2833                     -35            浙商期货     5   
     5                 2662                    -596            华泰期货     6   
     6                 2010                     -15            福能期货     7   
     7                 1916                     109            兴业期货     8   
     8                 1852                     155            英大期货     9   
     9                 1808                    -198            南华期货    10   
     10                1740                    -109            国泰君安    11   
     11                1568                     362            新湖期货    12   
     12                1355                       5            中金期货    13   
     13                1007                    -604            海通期货    14   
     14                 987                     111            国贸期货    15   
     15                 982                     -17            华信期货    16   
     16                 962                     328            西部期货    17   
     17                 894                    -796            东证期货    18   
     18                 867                    -679            兴证期货    19   
     19                 805                     801            南证期货    20   
     20               52487                   -1370            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  3646                     -108             永安期货   9755   
     1                  3148                     -627           国投安信期货   8265   
     2                  2931                     -998             中粮期货   5302   
     3                  2871                     -541             华泰期货   4517   
     4                  2731                       95             海通期货   3832   
     5                  2429                       23             申银万国   3688   
     6                  2364                      670             上海中期   3300   
     7                  1892                     -646             中信期货   3105   
     8                  1865                    -1569             东证期货   2813   
     9                  1663                      558             新湖期货   2588   
     10                 1571                      230             方正中期   2478   
     11                 1355                        6             上海大陆   2137   
     12                 1193                      154             兴证期货   2049   
     13                 1191                      503             南华期货   2019   
     14                 1095                       36             华安期货   1745   
     15                 1065                     -298             南证期货   1708   
     16                 1059                     -605             弘业期货   1679   
     17                 1053                      -51             国海良时   1546   
     18                  939                      -20           五矿经易期货   1521   
     19                  892                      413             西部期货   1453   
     20                36953                    -2775             None  65500   
     
         vol_chg vol_party_name  symbol variety  
     0     -3468           华泰期货  SM901       SM  
     1     -2700           东证期货  SM901       SM  
     2     -1163           新湖期货  SM901       SM  
     3     -1033           海通期货  SM901       SM  
     4     -1832           国泰君安  SM901       SM  
     5     -3129           中信期货  SM901       SM  
     6     -5671           上海大陆  SM901       SM  
     7     -2488           弘业期货  SM901       SM  
     8        28           兴证期货  SM901       SM  
     9       145           国信期货  SM901       SM  
     10    -2002           徽商期货  SM901       SM  
     11    -2772         国投安信期货  SM901       SM  
     12    -1559           华安期货  SM901       SM  
     13      261           西部期货  SM901       SM  
     14       27           南华期货  SM901       SM  
     15     -692           申银万国  SM901       SM  
     16     -225           华信期货  SM901       SM  
     17     1166           天风期货  SM901       SM  
     18     1065           南证期货  SM901       SM  
     19    -1667           方正中期  SM901       SM  
     20   -27709           None  SM901       SM  ,
     'SM905 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 3101                     512            中信建投     1   
     1                 1368                       7            申银万国     2   
     2                 1366                     180            弘业期货     3   
     3                 1155                    -428            中信期货     4   
     4                 1154                     114            方正中期     5   
     5                  951                     -29            鲁证期货     6   
     6                  938                     261            上海大陆     7   
     7                  872                      44          国投安信期货     8   
     8                  819                     176            上海中期     9   
     9                  764                     120            西南期货    10   
     10                 704                      73            永安期货    11   
     11                 698                      36            国信期货    12   
     12                 654                     255            中金期货    13   
     13                 638                      74            新湖期货    14   
     14                 539                    -264            华泰期货    15   
     15                 538                      -2            江西瑞奇    16   
     16                 491                      39            华信期货    17   
     17                 412                     405            天风期货    18   
     18                 365                      20            瑞达期货    19   
     19                 349                       0            冠通期货    20   
     20               17876                    1593            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  1434                     -154             中信期货   2711   
     1                  1245                       91             弘业期货   2526   
     2                  1082                      101             长安期货   1419   
     3                   979                       51             一德期货   1406   
     4                   886                        0             国泰君安   1190   
     5                   872                      105             国贸期货   1068   
     6                   865                      280             申银万国   1065   
     7                   751                       12             国信期货   1016   
     8                   707                       62             宝城期货    969   
     9                   700                     -170             华泰期货    875   
     10                  598                       25             东证期货    743   
     11                  491                       15             东海期货    708   
     12                  435                       31           国投安信期货    665   
     13                  421                      135             方正中期    557   
     14                  420                      -27             天风期货    510   
     15                  413                       67             新湖期货    491   
     16                  411                      162             瑞达期货    489   
     17                  406                       98             宏源期货    432   
     18                  385                      191             国富期货    423   
     19                  382                      165             徽商期货    418   
     20                13883                     1240             None  19681   
     
         vol_chg vol_party_name  symbol variety  
     0      1705           上海大陆  SM905       SM  
     1       346           中信期货  SM905       SM  
     2      -298           东证期货  SM905       SM  
     3      -875           华泰期货  SM905       SM  
     4       686           中信建投  SM905       SM  
     5      -383           徽商期货  SM905       SM  
     6       -16           新湖期货  SM905       SM  
     7      -288           海通期货  SM905       SM  
     8      -232           华安期货  SM905       SM  
     9      -969           弘业期货  SM905       SM  
     10     -133           西部期货  SM905       SM  
     11     -110           铜冠金源  SM905       SM  
     12      248           方正中期  SM905       SM  
     13        5           申银万国  SM905       SM  
     14       74           天风期货  SM905       SM  
     15      -21           东方财富  SM905       SM  
     16       42           宏源期货  SM905       SM  
     17       59           中辉期货  SM905       SM  
     18      -52           金瑞期货  SM905       SM  
     19     -219           国信期货  SM905       SM  
     20     -431           None  SM905       SM  ,
     'SR901 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 4871                   -2486            中粮期货     1   
     1                 3492                    1700            东兴期货     2   
     2                 2681                     -39          国投安信期货     3   
     3                 2651                       3            中投天琪     4   
     4                 2525                    -187            中信期货     5   
     5                 2495                    -253            宏源期货     6   
     6                 2300                    -280            兴证期货     7   
     7                 1699                     -66            英大期货     8   
     8                 1606                      81            海证期货     9   
     9                 1181                     -98            徽商期货    10   
     10                1101                      -3            华联期货    11   
     11                1041                     -18            国海良时    12   
     12                 985                     -18            鲁证期货    13   
     13                 854                     -53            申银万国    14   
     14                 835                    -225            华泰期货    15   
     15                 798                     -59            方正中期    16   
     16                 798                    -129            国贸期货    17   
     17                 775                     -89            海通期货    18   
     18                 715                     697            渤海期货    19   
     19                 697                      57            大地期货    20   
     20               34100                   -1465            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  4905                      -44             中粮期货   3916   
     1                  4853                      -95           国投安信期货   3236   
     2                  3631                     -322             光大期货   2896   
     3                  3148                      -16             宏源期货   2242   
     4                  3021                      -57             中投天琪   2117   
     5                  2731                      -30             中信期货   2030   
     6                  2608                       -9             英大期货   1731   
     7                  2505                      593             华信期货   1330   
     8                  2274                     -128             华泰期货    743   
     9                  2118                     -130             国信期货    720   
     10                 1992                      -81             永安期货    679   
     11                 1729                        2             上海大陆    588   
     12                 1650                     -220             国联期货    526   
     13                 1610                     -261             方正中期    481   
     14                 1507                        0             摩根大通    445   
     15                 1209                     -336             中大期货    437   
     16                  971                      -93             银河期货    410   
     17                  845                       -9             东兴期货    389   
     18                  529                       15             一德期货    385   
     19                  520                       -7             海通期货    382   
     20                44356                    -1228             None  25683   
     
         vol_chg vol_party_name  symbol variety  
     0       165           海通期货  SR901       SR  
     1     -1554           建信期货  SR901       SR  
     2      1375           中粮期货  SR901       SR  
     3      -111           东证期货  SR901       SR  
     4       522           中信期货  SR901       SR  
     5      -870           光大期货  SR901       SR  
     6      1656           东兴期货  SR901       SR  
     7      -325           华信期货  SR901       SR  
     8     -1001           华泰期货  SR901       SR  
     9       651           渤海期货  SR901       SR  
     10      489           大地期货  SR901       SR  
     11       92           兴证期货  SR901       SR  
     12     -559           方正中期  SR901       SR  
     13     -138           国金期货  SR901       SR  
     14      328           中大期货  SR901       SR  
     15     -334           徽商期货  SR901       SR  
     16       20         国投安信期货  SR901       SR  
     17     -157           宏源期货  SR901       SR  
     18      109           一德期货  SR901       SR  
     19     -183           广州金控  SR901       SR  
     20      175           None  SR901       SR  ,
     'SR905 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                10090                     864            中信期货     1   
     1                 9810                      37            广发期货     2   
     2                 8231                     -41            东兴期货     3   
     3                 7882                      29            创元期货     4   
     4                 7460                    -354            鲁证期货     5   
     5                 7357                     195            光大期货     6   
     6                 6489                     688            华泰期货     7   
     7                 6460                      88            首创期货     8   
     8                 6275                    -396            中粮期货     9   
     9                 5947                     139            金瑞期货    10   
     10                4904                     114            华信期货    11   
     11                4440                     272            永安期货    12   
     12                4250                     718            国泰君安    13   
     13                3545                     639            宏源期货    14   
     14                3093                     100            银河期货    15   
     15                2977                     -51          国投安信期货    16   
     16                2945                    -420            中财期货    17   
     17                2901                     -19          五矿经易期货    18   
     18                2728                   -2683            兴证期货    19   
     19                2651                      29            长安期货    20   
     20              110435                     -52            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 13509                      358             华泰期货   24601   
     1                 11770                      746             中粮期货   23414   
     2                 11402                       18             中金期货   20785   
     3                  9770                      206             永安期货   18254   
     4                  8666                    -2054             中信期货   13796   
     5                  8424                     -752             广发期货    8268   
     6                  7344                      217             浙商期货    7419   
     7                  6958                        9             英大期货    6923   
     8                  5567                     -122             国泰君安    6386   
     9                  4921                      -36             大地期货    5746   
     10                 4741                       59             深圳瑞龙    5355   
     11                 4641                      -34             银河期货    5232   
     12                 4397                      447             兴证期货    5213   
     13                 3759                      -42           国投安信期货    4748   
     14                 3622                      -20             宏源期货    4743   
     15                 3602                      147             光大期货    4547   
     16                 3591                      -83             兴业期货    4460   
     17                 3402                       53             海通期货    4152   
     18                 3133                     -149             国联期货    3944   
     19                 3123                       -6             中国国际    3854   
     20               126342                    -1038             None  181840   
     
         vol_chg vol_party_name  symbol variety  
     0     -9674           建信期货  SR905       SR  
     1     -6219           华泰期货  SR905       SR  
     2     -2993           东证期货  SR905       SR  
     3    -13816           海通期货  SR905       SR  
     4      -626           中信期货  SR905       SR  
     5       751           兴证期货  SR905       SR  
     6     -2134           徽商期货  SR905       SR  
     7     -1544           海证期货  SR905       SR  
     8     -2356           华安期货  SR905       SR  
     9     -2372           光大期货  SR905       SR  
     10       81           创元期货  SR905       SR  
     11    -1034           国泰君安  SR905       SR  
     12    -3029           广发期货  SR905       SR  
     13    -1582           国贸期货  SR905       SR  
     14    -2808           宏源期货  SR905       SR  
     15      131           安粮期货  SR905       SR  
     16     -932           东航期货  SR905       SR  
     17       29           申银万国  SR905       SR  
     18    -1885           方正中期  SR905       SR  
     19      453           国海良时  SR905       SR  
     20   -51559           None  SR905       SR  ,
     'SR909 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 4734                     -44            首创期货     1   
     1                 2269                    -147            光大期货     2   
     2                 1892                       6            东证期货     3   
     3                 1466                     750          混沌天成期货     4   
     4                 1400                       0            天风期货     5   
     5                 1278                      16            华泰期货     6   
     6                 1211                      93            长江期货     7   
     7                 1101                      24            中信期货     8   
     8                 1037                     132            鲁证期货     9   
     9                  993                       3            国联期货    10   
     10                 895                      62            华安期货    11   
     11                 861                     224            永安期货    12   
     12                 860                     116            银河期货    13   
     13                 844                     -11            浙商期货    14   
     14                 751                      34            宏源期货    15   
     15                 660                      79          国投安信期货    16   
     16                 517                     -22            国贸期货    17   
     17                 511                      32            海通期货    18   
     18                 467                      -6            华联期货    19   
     19                 438                      11            东兴期货    20   
     20               24185                    1352            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  6613                      335             中粮期货   1581   
     1                  5206                     1538             英大期货   1422   
     2                  3110                        0             东兴期货   1282   
     3                  2280                        0             兴业期货    925   
     4                  1518                        2             国泰君安    884   
     5                  1141                        0             国贸期货    880   
     6                  1128                      -14             华泰期货    752   
     7                  1059                        0             光大期货    723   
     8                  1012                        1             国联期货    707   
     9                   862                       28             银河期货    595   
     10                  767                        0             国信期货    593   
     11                  712                        0             东方财富    440   
     12                  704                      -19             大地期货    387   
     13                  677                        3             华信期货    348   
     14                  676                       31           国投安信期货    341   
     15                  665                        1             渤海期货    295   
     16                  584                       11             申银万国    271   
     17                  562                      -50             南华期货    259   
     18                  531                     -127             一德期货    240   
     19                  511                       -1             中信期货    226   
     20                30318                     1739             None  13151   
     
         vol_chg vol_party_name  symbol variety  
     0       784           英大期货  SR909       SR  
     1      -354           国泰君安  SR909       SR  
     2       545           冠通期货  SR909       SR  
     3       128           华安期货  SR909       SR  
     4      -287           华泰期货  SR909       SR  
     5       615         混沌天成期货  SR909       SR  
     6       205           东证期货  SR909       SR  
     7       227           一德期货  SR909       SR  
     8       604           信达期货  SR909       SR  
     9       302           中粮期货  SR909       SR  
     10      -79           中信期货  SR909       SR  
     11      372           国联期货  SR909       SR  
     12       64           国金期货  SR909       SR  
     13      159         国投安信期货  SR909       SR  
     14     -249           东海期货  SR909       SR  
     15      223           永安期货  SR909       SR  
     16      128           方正中期  SR909       SR  
     17       80           创元期货  SR909       SR  
     18       28           国信期货  SR909       SR  
     19     -323           国贸期货  SR909       SR  
     20     3172           None  SR909       SR  ,
     'TA812 ':    long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 134                       1            东吴期货     1   
     1                   6                       0            东海期货     2   
     2                   2                      -1            光大期货     3   
     3                   0                       0               0     4   
     4                 142                       0            None   999   
     
        short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                  123                        0             东证期货    2   
     1                   12                        0             中信期货    1   
     2                    6                        0             华泰期货    1   
     3                    1                       -1             光大期货    0   
     4                  142                       -1             None    4   
     
        vol_chg vol_party_name  symbol variety  
     0        2           光大期货  TA812       TA  
     1        1           华泰期货  TA812       TA  
     2        1           东吴期货  TA812       TA  
     3        0              0  TA812       TA  
     4        4           None  TA812       TA  ,
     'TA901 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                23807                   -2314            华泰期货     1   
     1                22776                    5006            南华期货     2   
     2                13940                   -1268            银河期货     3   
     3                12108                    -676            国泰君安     4   
     4                11352                    9058            招商期货     5   
     5                10782                    2901            建信期货     6   
     6                 8927                    2055            光大期货     7   
     7                 8925                    -502            永安期货     8   
     8                 7714                   -7061            天风期货     9   
     9                 6566                   -7127            国贸期货    10   
     10                6433                      13            中粮期货    11   
     11                5874                    -113            中信期货    12   
     12                5763                      13            国富期货    13   
     13                4087                   -1396            深圳瑞龙    14   
     14                3114                    -990            大越期货    15   
     15                2564                    -111            前海期货    16   
     16                2022                    -150            鲁证期货    17   
     17                1917                    -195            广发期货    18   
     18                1842                    1598            申银万国    19   
     19                1497                    -302            中信建投    20   
     20              162010                   -1561            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name     vol  \
     0                 17841                    -1568             银河期货   20754   
     1                 11975                      992             永安期货   14958   
     2                  9190                      396             中信期货   13619   
     3                  7737                     1394             光大期货   11699   
     4                  7320                      470             招商期货   10068   
     5                  6719                     -332             宝城期货    9098   
     6                  6602                      -51             华安期货    8171   
     7                  6375                    -1692             华泰期货    6576   
     8                  6124                      422             国泰君安    6286   
     9                  6014                     -205             信达期货    6183   
     10                 5356                     -675             东海期货    5786   
     11                 5178                     1553             中粮期货    3853   
     12                 5049                      341             建信期货    3451   
     13                 4951                      -27             中辉期货    3382   
     14                 3894                      632             东航期货    3362   
     15                 3669                     -426             浙商期货    3343   
     16                 3355                     -192             广发期货    3236   
     17                 3285                     -167             国信期货    3066   
     18                 3086                    -1405             国联期货    3034   
     19                 2990                     -703             大地期货    3022   
     20               126710                    -1243             None  142947   
     
         vol_chg vol_party_name  symbol variety  
     0      5331           南华期货  TA901       TA  
     1    -22509           华泰期货  TA901       TA  
     2      3723           光大期货  TA901       TA  
     3     -1737           新湖期货  TA901       TA  
     4      6969           招商期货  TA901       TA  
     5      3242           国贸期货  TA901       TA  
     6      2018           天风期货  TA901       TA  
     7      4533           建信期货  TA901       TA  
     8     -6677           永安期货  TA901       TA  
     9     -9994           海通期货  TA901       TA  
     10    -8488           银河期货  TA901       TA  
     11      635           东航期货  TA901       TA  
     12    -1847           浙商期货  TA901       TA  
     13      911           大地期货  TA901       TA  
     14    -1843           东证期货  TA901       TA  
     15    -1199           中信期货  TA901       TA  
     16    -1573           徽商期货  TA901       TA  
     17     -225         五矿经易期货  TA901       TA  
     18    -5979           方正中期  TA901       TA  
     19    -1071           华安期货  TA901       TA  
     20   -35780           None  TA901       TA  ,
     'TA903 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                20401                    1388            永安期货     1   
     1                11680                       3            中粮期货     2   
     2                 5939                      19            光大期货     3   
     3                 5642                       7            中信期货     4   
     4                 4242                   -1222            中原期货     5   
     5                 3392                    -250            东吴期货     6   
     6                 3122                      10            上海中期     7   
     7                 3070                      41            广发期货     8   
     8                 2560                      48            国泰君安     9   
     9                 2261                     -17            国海良时    10   
     10                2170                     302          五矿经易期货    11   
     11                2043                       3            宏源期货    12   
     12                2004                      18            东航期货    13   
     13                1658                      -5            申银万国    14   
     14                1532                    -171            方正中期    15   
     15                1412                      -3            建信期货    16   
     16                1398                    -397            大地期货    17   
     17                1237                    -148            东海期货    18   
     18                1027                    -642            华泰期货    19   
     19                 955                      14            中银国际    20   
     20               77745                   -1002            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                 12579                     -403             招商期货  15681   
     1                  9385                        0             信达期货  10136   
     2                  6945                     -500             中大期货   6277   
     3                  5672                      -27             中信期货   5966   
     4                  5019                      740             通惠期货   5846   
     5                  4090                    -1250             中原期货   5841   
     6                  3626                     -185             东吴期货   5071   
     7                  3440                        0             中辉期货   4860   
     8                  3127                     -306             光大期货   4126   
     9                  2832                       15             上海中期   3899   
     10                 2251                        0             国海良时   3699   
     11                 2238                      443             华安期货   3284   
     12                 2004                     1999             国信期货   2774   
     13                 1950                      400             宝城期货   2624   
     14                 1868                     -269             方正中期   2587   
     15                 1828                    -2761             建信期货   2174   
     16                 1653                      -75             申银万国   2126   
     17                 1390                      -22             新湖期货   2044   
     18                 1368                     -450             大地期货   1945   
     19                 1337                     -455             华泰期货   1813   
     20                74602                    -3106             None  92773   
     
         vol_chg vol_party_name  symbol variety  
     0    -16130           华泰期货  TA903       TA  
     1      2552           广发期货  TA903       TA  
     2      -855           华金期货  TA903       TA  
     3      -656           新湖期货  TA903       TA  
     4      2044           中信期货  TA903       TA  
     5     -1470           西部期货  TA903       TA  
     6      3402           南华期货  TA903       TA  
     7      -320         五矿经易期货  TA903       TA  
     8      2148           中原期货  TA903       TA  
     9     -5271           东海期货  TA903       TA  
     10     -771           永安期货  TA903       TA  
     11    -2749           华安期货  TA903       TA  
     12     2349           建信期货  TA903       TA  
     13     -655           申银万国  TA903       TA  
     14     1551           国海良时  TA903       TA  
     15    -3521           海通期货  TA903       TA  
     16     1645           国信期货  TA903       TA  
     17    -1123           创元期货  TA903       TA  
     18     -872           光大期货  TA903       TA  
     19      368           渤海期货  TA903       TA  
     20   -18334           None  TA903       TA  ,
     'TA905 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                48787                    6494            国贸期货     1   
     1                48517                   -2720            华泰期货     2   
     2                33490                   -1869            建信期货     3   
     3                29431                    2147            南华期货     4   
     4                26083                    -858            招商期货     5   
     5                22858                    2694            中信期货     6   
     6                19116                     852            国泰君安     7   
     7                18628                   -6414            永安期货     8   
     8                18114                    -797            天风期货     9   
     9                17134                      32            中粮期货    10   
     10               13253                    -219            新湖期货    11   
     11               11855                     287            广发期货    12   
     12                9681                    4479            东证期货    13   
     13                9573                     527            光大期货    14   
     14                9366                     327            信达期货    15   
     15                8307                    1259            东航期货    16   
     16                7597                    1952            申银万国    17   
     17                6750                    1332            银河期货    18   
     18                6708                     100            方正中期    19   
     19                6468                     181            通惠期货    20   
     20              371716                    9786            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name      vol  \
     0                 79485                    -7705             永安期货   143031   
     1                 45218                   -10351             银河期货   140543   
     2                 20297                     5887             华泰期货   110401   
     3                 19697                     -276             国泰君安    79261   
     4                 17778                      402             浙商期货    78021   
     5                 17042                     1565             中信期货    70345   
     6                 13849                     -893           五矿经易期货    47071   
     7                 13154                     9345             中粮期货    42966   
     8                 12917                     1625             方正中期    42632   
     9                 12613                    -1051           国投安信期货    42385   
     10                11906                     7326             东证期货    41632   
     11                10171                     2948             宝城期货    40924   
     12                 9822                      848             鲁证期货    39687   
     13                 9344                     2957             海通期货    39649   
     14                 8525                     2134             光大期货    34373   
     15                 7700                     -654           格林大华期货    33949   
     16                 7194                      -93             大地期货    33476   
     17                 6971                    -2806             东吴期货    31126   
     18                 6785                     1981             东方财富    30974   
     19                 5999                     4965            浙江新世纪    27560   
     20               336467                    18154             None  1150006   
     
         vol_chg vol_party_name  symbol variety  
     0    -58113           华泰期货  TA905       TA  
     1    -18302           海通期货  TA905       TA  
     2    -18521           永安期货  TA905       TA  
     3      -927           新湖期货  TA905       TA  
     4     -1489           东证期货  TA905       TA  
     5     -7827           中信期货  TA905       TA  
     6     11740           西部期货  TA905       TA  
     7    -12345           申银万国  TA905       TA  
     8     -8607           华安期货  TA905       TA  
     9    -11810           光大期货  TA905       TA  
     10   -39461           创元期货  TA905       TA  
     11   -13247           东方财富  TA905       TA  
     12   -26770           徽商期货  TA905       TA  
     13    -6539           方正中期  TA905       TA  
     14    -7234           银河期货  TA905       TA  
     15    -3364           广发期货  TA905       TA  
     16    -6648         国投安信期货  TA905       TA  
     17   -13269           国泰君安  TA905       TA  
     18    -8402           金瑞期货  TA905       TA  
     19      924           兴证期货  TA905       TA  
     20  -250211           None  TA905       TA  ,
     'TA907 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 3350                    -147            东吴期货     1   
     1                 2205                       0            海通期货     2   
     2                 2112                      86            方正中期     3   
     3                 1587                      15            申银万国     4   
     4                 1202                    -267            大地期货     5   
     5                 1013                     538            中原期货     6   
     6                 1010                    -190            南华期货     7   
     7                  759                      -1            中信期货     8   
     8                  548                      -1          五矿经易期货     9   
     9                  515                      79            国泰君安    10   
     10                 500                     -50           浙江新世纪    11   
     11                 411                      -1            国海良时    12   
     12                 205                       1            永安期货    13   
     13                 198                       0            中粮期货    14   
     14                 136                      17            光大期货    15   
     15                 110                       0            广发期货    16   
     16                  94                       5            东海期货    17   
     17                  92                      92            瑞达期货    18   
     18                  88                      -5            上海中期    19   
     19                  80                      52            东证期货    20   
     20               16215                     223            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  3350                     -147             东吴期货  14122   
     1                  2224                      -65             方正中期   5123   
     2                  2201                       -8             海通期货   4978   
     3                  1528                      -25             申银万国   4128   
     4                  1202                     -258             大地期货   2638   
     5                  1043                      584             中原期货   2543   
     6                  1010                     -190             南华期货   2478   
     7                   754                      -13           五矿经易期货   2190   
     8                   670                      -16             中信期货   1831   
     9                   600                        0             永安期货   1826   
     10                  416                       -6             国海良时   1716   
     11                  348                      190             一德期货   1514   
     12                  200                        0             瑞达期货   1417   
     13                  150                      150             华金期货   1403   
     14                  147                      -35             光大期货   1356   
     15                  109                       10             广发期货   1146   
     16                   94                        5             东海期货   1047   
     17                   85                      -10             上海中期   1038   
     18                   81                        7             华安期货    958   
     19                   80                       65             安粮期货    661   
     20                16292                      238             None  54113   
     
         vol_chg vol_party_name  symbol variety  
     0      3460           国元期货  TA907       TA  
     1      2154           中信期货  TA907       TA  
     2      -167           西部期货  TA907       TA  
     3      3272           南华期货  TA907       TA  
     4       880         五矿经易期货  TA907       TA  
     5      1598           国海良时  TA907       TA  
     6      1076           中原期货  TA907       TA  
     7      -230           国泰君安  TA907       TA  
     8       666           国信期货  TA907       TA  
     9      -452           申银万国  TA907       TA  
     10    -3164           海通期货  TA907       TA  
     11      392           创元期货  TA907       TA  
     12      635           方正中期  TA907       TA  
     13     -215           东证期货  TA907       TA  
     14      334           东吴期货  TA907       TA  
     15       39           光大期货  TA907       TA  
     16      -77           上海中期  TA907       TA  
     17      698           一德期货  TA907       TA  
     18      326           东海期货  TA907       TA  
     19      345           永安期货  TA907       TA  
     20    11570           None  TA907       TA  ,
     'TA909 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 7797                      66            广发期货     1   
     1                 5429                     -29            中信期货     2   
     2                 2571                      10            通惠期货     3   
     3                  850                     -73            渤海期货     4   
     4                  723                      12            申银万国     5   
     5                  716                       1            金瑞期货     6   
     6                  631                       3            中粮期货     7   
     7                  600                      -2            中银国际     8   
     8                  416                       1            国联期货     9   
     9                  367                    -543            新湖期货    10   
     10                 317                     129            大地期货    11   
     11                 312                    -251            永安期货    12   
     12                 307                       4            光大期货    13   
     13                 260                    -252            方正中期    14   
     14                 233                      13            中信建投    15   
     15                 216                     119            银河期货    16   
     16                 214                     102            中国国际    17   
     17                 208                    -301            广州期货    18   
     18                 204                      30          五矿经易期货    19   
     19                 189                     -89            中大期货    20   
     20               22560                   -1050            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  3628                     -161             东航期货   2684   
     1                  2734                     -853             永安期货   2092   
     2                  1557                      517             国泰君安   1709   
     3                  1505                     -270             方正中期   1540   
     4                  1390                        0             银河期货   1477   
     5                  1047                      497             大地期货   1188   
     6                  1008                      600             建信期货   1156   
     7                   911                     -110             申银万国   1066   
     8                   818                       33             金瑞期货   1044   
     9                   807                        7             国贸期货    950   
     10                  804                       -1             中粮期货    898   
     11                  756                        2             中财期货    857   
     12                  753                    -1031             渤海期货    780   
     13                  707                      602             中大期货    774   
     14                  678                     -358             安粮期货    737   
     15                  671                      -23             中信期货    632   
     16                  600                       -2             中银国际    611   
     17                  594                      154             华安期货    605   
     18                  578                       31             迈科期货    603   
     19                  518                       12             一德期货    579   
     20                22064                     -354             None  21982   
     
         vol_chg vol_party_name  symbol variety  
     0      2571           华安期货  TA909       TA  
     1       195           中信期货  TA909       TA  
     2      -935           国泰君安  TA909       TA  
     3      -396           永安期货  TA909       TA  
     4       292           上海大陆  TA909       TA  
     5       -96           渤海期货  TA909       TA  
     6       996           新湖期货  TA909       TA  
     7       609           国金期货  TA909       TA  
     8       177           大地期货  TA909       TA  
     9       633           华泰期货  TA909       TA  
     10      584           安粮期货  TA909       TA  
     11      396         五矿经易期货  TA909       TA  
     12      522           东航期货  TA909       TA  
     13      346           方正中期  TA909       TA  
     14      687           中大期货  TA909       TA  
     15      181           国信期货  TA909       TA  
     16      600           建信期货  TA909       TA  
     17      354           创元期货  TA909       TA  
     18    -1529           东证期货  TA909       TA  
     19    -1556           国元期货  TA909       TA  
     20     4631           None  TA909       TA  ,
     'WH901 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                  267                       0            首创期货     1   
     1                  128                     -12          国投安信期货     2   
     2                   29                      -1            银河期货     3   
     3                   26                       0            国泰君安     4   
     4                   25                      -7            永安期货     5   
     5                   21                       0            华鑫期货     6   
     6                   18                       0            中原期货     7   
     7                   14                       0            中信期货     8   
     8                   11                       0            国信期货     9   
     9                   10                       0            海通期货    10   
     10                   9                      -1            华泰期货    11   
     11                   9                       1            中衍期货    12   
     12                   8                       0            光大期货    13   
     13                   8                       0            安粮期货    14   
     14                   8                      -2            中辉期货    15   
     15                   8                       0            平安期货    16   
     16                   7                       0            新湖期货    17   
     17                   6                       0            方正中期    18   
     18                   6                       0            宏源期货    19   
     19                   5                       0            中财期货    20   
     20                 623                     -22            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  vol  \
     0                   407                        4             永安期货   31   
     1                   133                      -27             迈科期货   28   
     2                    50                        2             申银万国   23   
     3                    22                        1             华闻期货   16   
     4                     9                        0             招金期货   13   
     5                     8                       -2           五矿经易期货    6   
     6                     7                        0             海航期货    5   
     7                     7                        1             中信期货    4   
     8                     7                        0             东证期货    4   
     9                     7                        0             宏源期货    4   
     10                    6                        0             安粮期货    3   
     11                    5                        0             国信期货    3   
     12                    5                        0             鲁证期货    2   
     13                    5                        5             光大期货    2   
     14                    4                        0             国泰君安    2   
     15                    3                        0             中财期货    2   
     16                    3                       -2             中国国际    2   
     17                    3                        0             英大期货    2   
     18                    2                        1             徽商期货    2   
     19                    2                        0             方正中期    2   
     20                  695                      -17             None  156   
     
         vol_chg vol_party_name  symbol variety  
     0        25           永安期货  WH901       WH  
     1        19           迈科期货  WH901       WH  
     2        14           弘业期货  WH901       WH  
     3        -4           创元期货  WH901       WH  
     4         1         国投安信期货  WH901       WH  
     5         6           东海期货  WH901       WH  
     6         2           光大期货  WH901       WH  
     7        -4           东航期货  WH901       WH  
     8         0           广发期货  WH901       WH  
     9         4           国联期货  WH901       WH  
     10        3           中融汇信  WH901       WH  
     11        3           华联期货  WH901       WH  
     12        2           招商期货  WH901       WH  
     13      -47           申银万国  WH901       WH  
     14        1            美尔雅  WH901       WH  
     15        2           瑞达期货  WH901       WH  
     16       -6           中国国际  WH901       WH  
     17       -3           大有期货  WH901       WH  
     18        2         五矿经易期货  WH901       WH  
     19        1           中辉期货  WH901       WH  
     20       21           None  WH901       WH  ,
     'ZC901 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 4924                    -672            中信期货     1   
     1                 4191                     -59            一德期货     2   
     2                 3914                    -261            中粮期货     3   
     3                 2712                     -13           中电投先融     4   
     4                 2662                    -218            建信期货     5   
     5                 2451                       2            永安期货     6   
     6                 1936                    -429            国泰君安     7   
     7                 1919                    -289            广发期货     8   
     8                 1859                     -58            华泰期货     9   
     9                 1727                     -31          格林大华期货    10   
     10                1593                   -1150            银河期货    11   
     11                1421                     201            海证期货    12   
     12                1320                    -105            申银万国    13   
     13                1236                     517            宏源期货    14   
     14                1194                    -184            方正中期    15   
     15                1159                    -232            金瑞期货    16   
     16                1137                      58            摩根大通    17   
     17                1099                      18            鲁证期货    18   
     18                1074                     -45            中大期货    19   
     19                1051                     356            华鑫期货    20   
     20               40579                   -2594            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                 12925                     -651             永安期货   9085   
     1                  3679                     -262             华泰期货   8736   
     2                  3459                      -62             一德期货   8712   
     3                  3074                     -328             中信期货   5104   
     4                  2742                      -66             申银万国   4345   
     5                  2140                     -108             银河期货   4166   
     6                  1867                     -253             中国国际   3198   
     7                  1789                      -73           国投安信期货   2979   
     8                  1784                     -265             广发期货   2872   
     9                  1596                      -81             东证期货   2774   
     10                 1388                     -317             建信期货   2630   
     11                 1336                      527             长江期货   2171   
     12                 1300                        0             中钢期货   2127   
     13                 1079                       16             东海期货   1718   
     14                  960                      100             福能期货   1603   
     15                  939                     -454             方正中期   1558   
     16                  911                       92             光大期货   1514   
     17                  908                     -485             国泰君安   1480   
     18                  776                      -32             南华期货   1443   
     19                  715                     -246             中粮期货   1417   
     20                45367                    -2948             None  69632   
     
         vol_chg vol_party_name  symbol variety  
     0     -3153           建信期货  ZC901       ZC  
     1     -6535           东证期货  ZC901       ZC  
     2     -4626           华泰期货  ZC901       ZC  
     3     -1063           海通期货  ZC901       ZC  
     4     -2496           光大期货  ZC901       ZC  
     5      -693           方正中期  ZC901       ZC  
     6      -975           国泰君安  ZC901       ZC  
     7     -2224           鲁证期货  ZC901       ZC  
     8     -4594           中信期货  ZC901       ZC  
     9     -2938           银河期货  ZC901       ZC  
     10    -1925           金瑞期货  ZC901       ZC  
     11     -358           兴证期货  ZC901       ZC  
     12    -2509           一德期货  ZC901       ZC  
     13     -584           中辉期货  ZC901       ZC  
     14     -775           创元期货  ZC901       ZC  
     15    -2217           徽商期货  ZC901       ZC  
     16    -2698           广发期货  ZC901       ZC  
     17     -124           中信建投  ZC901       ZC  
     18     -496           东吴期货  ZC901       ZC  
     19    -2739           永安期货  ZC901       ZC  
     20   -43722           None  ZC901       ZC  ,
     'ZC903 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 3707                     -23            国信期货     1   
     1                 1794                      34          国投安信期货     2   
     2                 1551                     -32            新湖期货     3   
     3                 1545                     108            宏源期货     4   
     4                 1542                       1            上海中期     5   
     5                 1325                      35            中大期货     6   
     6                 1257                     -14            方正中期     7   
     7                 1073                       0            中粮期货     8   
     8                 1059                     -51            南华期货     9   
     9                  941                      21            东海期货    10   
     10                 935                     106          格林大华期货    11   
     11                 922                      51            中原期货    12   
     12                 859                      15            海通期货    13   
     13                 859                    -296           中电投先融    14   
     14                 829                     131            东证期货    15   
     15                 739                     -39            渤海期货    16   
     16                 678                    -154            浙商期货    17   
     17                 610                       0            摩根大通    18   
     18                 574                     253            安粮期货    19   
     19                 500                      29            大地期货    20   
     20               23299                     175            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  3269                      173             一德期货   4828   
     1                  3026                       80             永安期货   3812   
     2                  1858                      -62           国投安信期货   2442   
     3                  1767                       -6             方正中期   2411   
     4                  1595                      131             华泰期货   2336   
     5                  1546                       -1             上海中期   2322   
     6                  1429                      290             银河期货   2216   
     7                  1292                      163             福能期货   1717   
     8                  1204                      -12             宏源期货   1706   
     9                  1121                      -56             南华期货   1684   
     10                 1117                       20             中信期货   1350   
     11                 1082                      -24             新湖期货   1302   
     12                  746                      -11             中原期货   1053   
     13                  627                       29             中粮期货    738   
     14                  607                        5           格林大华期货    682   
     15                  578                        4             中辉期货    659   
     16                  574                       12             浙商期货    639   
     17                  571                      -51             广发期货    597   
     18                  500                      500             新晟期货    570   
     19                  416                      -62             光大期货    522   
     20                24925                     1122             None  33586   
     
         vol_chg vol_party_name  symbol variety  
     0      2701           宏源期货  ZC903       ZC  
     1      2556           新湖期货  ZC903       ZC  
     2      -615           浙商期货  ZC903       ZC  
     3       406         格林大华期货  ZC903       ZC  
     4       379         国投安信期货  ZC903       ZC  
     5       375           锦泰期货  ZC903       ZC  
     6       229           上海中期  ZC903       ZC  
     7      -105           南华期货  ZC903       ZC  
     8      -715           银河期货  ZC903       ZC  
     9       -69         五矿经易期货  ZC903       ZC  
     10      243           建信期货  ZC903       ZC  
     11     -278           东证期货  ZC903       ZC  
     12     -571           国联期货  ZC903       ZC  
     13     -470           安粮期货  ZC903       ZC  
     14    -1733          中电投先融  ZC903       ZC  
     15     -968           大地期货  ZC903       ZC  
     16     -574           一德期货  ZC903       ZC  
     17     -200           华泰期货  ZC903       ZC  
     18      160           华安期货  ZC903       ZC  
     19      522           新晟期货  ZC903       ZC  
     20     1273           None  ZC903       ZC  ,
     'ZC905 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 7096                    1877             美尔雅     1   
     1                 6333                    -118            鲁证期货     2   
     2                 5961                    1020            中信期货     3   
     3                 4828                     -52            建信期货     4   
     4                 4735                       5          国投安信期货     5   
     5                 4332                     -59            银河期货     6   
     6                 4117                    -181            弘业期货     7   
     7                 3700                       0            摩根大通     8   
     8                 3556                      16            大越期货     9   
     9                 3448                     818            广发期货    10   
     10                3371                     -96            渤海期货    11   
     11                2871                      74            国信期货    12   
     12                2832                    -100            中粮期货    13   
     13                2473                      51            中大期货    14   
     14                2391                      51            广州期货    15   
     15                2189                     -11            海通期货    16   
     16                2128                     146            永安期货    17   
     17                2056                     227            方正中期    18   
     18                2022                       7            中银国际    19   
     19                1938                     990            兴证期货    20   
     20               72377                    4665            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  8738                     1356             永安期货   9003   
     1                  5832                      -51             方正中期   6289   
     2                  5335                     -143             中信期货   4971   
     3                  4331                     1265             一德期货   3966   
     4                  4327                     -110             国泰君安   3698   
     5                  4255                      391             银河期货   3622   
     6                  3966                     -467             大地期货   3366   
     7                  3876                      230             浙商期货   3160   
     8                  3678                     -372             东证期货   2980   
     9                  3604                      199             鲁证期货   2974   
     10                 3267                     -102           国投安信期货   2903   
     11                 3107                     2463             红塔期货   2702   
     12                 2661                       41             长江期货   2647   
     13                 2497                      127             国海良时   2563   
     14                 2382                     -594             华泰期货   2436   
     15                 2155                       54             新湖期货   2371   
     16                 2148                      469             广发期货   2284   
     17                 1993                      103             宏源期货   2237   
     18                 1682                     -345             中金期货   2046   
     19                 1653                      191             中辉期货   1813   
     20                71487                     4705             None  68031   
     
         vol_chg vol_party_name  symbol variety  
     0      -448           建信期货  ZC905       ZC  
     1      -959           中信期货  ZC905       ZC  
     2      -852           华泰期货  ZC905       ZC  
     3       999           永安期货  ZC905       ZC  
     4       246           中信建投  ZC905       ZC  
     5      -244           国泰君安  ZC905       ZC  
     6       -42           银河期货  ZC905       ZC  
     7      2625            美尔雅  ZC905       ZC  
     8       979           一德期货  ZC905       ZC  
     9      -222           东证期货  ZC905       ZC  
     10      -65           光大期货  ZC905       ZC  
     11    -2477           方正中期  ZC905       ZC  
     12      765           广发期货  ZC905       ZC  
     13     2492           红塔期货  ZC905       ZC  
     14      396           兴证期货  ZC905       ZC  
     15     -978           徽商期货  ZC905       ZC  
     16     1625           华西期货  ZC905       ZC  
     17     -141           华安期货  ZC905       ZC  
     18    -1058           海通期货  ZC905       ZC  
     19       42           大地期货  ZC905       ZC  
     20     2683           None  ZC905       ZC  ,
     'ZC907 ':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 1700                     -21            南华期货     1   
     1                 1134                      13           中电投先融     2   
     2                 1121                      25            大地期货     3   
     3                 1102                       0            国信期货     4   
     4                  923                       0            广发期货     5   
     5                  911                     -11            方正中期     6   
     6                  879                       0            浙商期货     7   
     7                  858                       0            银河期货     8   
     8                  605                       0            中原期货     9   
     9                  571                       0            海证期货    10   
     10                 505                       1            宝城期货    11   
     11                 496                      -2            锦泰期货    12   
     12                 478                     -21            新湖期货    13   
     13                 344                      -4            建信期货    14   
     14                 310                     -46            宏源期货    15   
     15                 265                       0            永安期货    16   
     16                 235                      -1            国盛期货    17   
     17                 216                      -5            申银万国    18   
     18                 200                       0            民生期货    19   
     19                 185                       0            华泰期货    20   
     20               13038                     -72            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name    vol  \
     0                  2471                      -40             渤海期货   4472   
     1                  1824                      -22             新湖期货   3595   
     2                  1733                      -15             南华期货   1598   
     3                  1227                       45             大地期货    580   
     4                  1226                      266             方正中期    301   
     5                   894                      -10             浙商期货    292   
     6                   875                        0             东兴期货    265   
     7                   603                        0             中原期货    207   
     8                   412                        4             东海期货    176   
     9                   320                        0             中大期货    163   
     10                  293                      -41           五矿经易期货    156   
     11                  252                      -62             宏源期货    140   
     12                  240                        0             中信期货    116   
     13                  173                      -12             锦泰期货     90   
     14                  167                      -45             永安期货     76   
     15                  162                        2             国联期货     61   
     16                  140                      -15             长江期货     55   
     17                  102                      -67             徽商期货     41   
     18                   89                        0             银河期货     40   
     19                   86                      -28             创元期货     40   
     20                13289                      -40             None  12464   
     
         vol_chg vol_party_name  symbol variety  
     0      2573           宏源期货  ZC907       ZC  
     1      2895           新湖期货  ZC907       ZC  
     2      -166           南华期货  ZC907       ZC  
     3      -430           大地期货  ZC907       ZC  
     4     -2178           方正中期  ZC907       ZC  
     5       286           东吴期货  ZC907       ZC  
     6     -1894          中电投先融  ZC907       ZC  
     7        88         五矿经易期货  ZC907       ZC  
     8       -17           锦泰期货  ZC907       ZC  
     9       -83           永安期货  ZC907       ZC  
     10     -156           国联期货  ZC907       ZC  
     11       76           徽商期货  ZC907       ZC  
     12       18           创元期货  ZC907       ZC  
     13       30           建信期货  ZC907       ZC  
     14      -20           浙商期货  ZC907       ZC  
     15       46           东海期货  ZC907       ZC  
     16       43           山西三立  ZC907       ZC  
     17      -32           弘业期货  ZC907       ZC  
     18       40           渤海期货  ZC907       ZC  
     19      -15           华安期货  ZC907       ZC  
     20     1104           None  ZC907       ZC  }




```python
ak.get_shfe_rank_table('20181210')
```




    {'cu1905':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   cu1905     1           东证期货   867.0    181.0            中信期货   
     1   cu1905     2           华泰期货   660.0    397.0            金瑞期货   
     2   cu1905     3           广发期货   498.0    460.0            东方财富   
     3   cu1905     4           国投安信   423.0     61.0            国贸期货   
     4   cu1905     5           中信期货   419.0    110.0            南华期货   
     5   cu1905     6           五矿经易   351.0    -78.0            广发期货   
     6   cu1905     7           迈科期货   318.0    307.0            长安期货   
     7   cu1905     8           中银国际   248.0     62.0            申万期货   
     8   cu1905     9           中辉期货   219.0    -13.0            创元期货   
     9   cu1905    10           方正中期   210.0     79.0            迈科期货   
     10  cu1905    11           西部期货   174.0     51.0            中粮期货   
     11  cu1905    12           新湖期货   141.0     32.0            徽商期货   
     12  cu1905    13           铜冠金源   136.0    124.0            银河期货   
     13  cu1905    14           中粮期货   130.0    -74.0            国投安信   
     14  cu1905    15           永安期货   124.0     28.0            建信期货   
     15  cu1905    16           一德期货   123.0    113.0            瑞达期货   
     16  cu1905    17           海通期货   117.0    -20.0            方正中期   
     17  cu1905    18           东方财富   113.0     -9.0            五矿经易   
     18  cu1905    19           鲁证期货   107.0     69.0            华泰期货   
     19  cu1905    20           申万期货    98.0    -13.0            宝城期货   
     20  cu1905   999           None  5476.0   1867.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               3399.0                   114.0             中粮期货   
     1               1956.0                    23.0             国贸期货   
     2                623.0                    61.0             国泰君安   
     3                603.0                     0.0             中钢期货   
     4                534.0                    -4.0             建信期货   
     5                401.0                    73.0             华金期货   
     6                386.0                     0.0             广发期货   
     7                378.0                     3.0             东方财富   
     8                334.0                    19.0             中信期货   
     9                325.0                   -92.0             中信建投   
     10               293.0                    -5.0             金瑞期货   
     11               268.0                    94.0             大越期货   
     12               259.0                     5.0             五矿经易   
     13               241.0                    -4.0             华泰期货   
     14               228.0                     0.0             云晨期货   
     15               226.0                    13.0             海通期货   
     16               211.0                    90.0             鲁证期货   
     17               206.0                   187.0             一德期货   
     18               185.0                    36.0             通惠期货   
     19               184.0                     0.0             宝城期货   
     20             11240.0                   613.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                1135.0                    115.0      CU  
     1                 930.0                      0.0      CU  
     2                 917.0                     -2.0      CU  
     3                 910.0                      0.0      CU  
     4                 850.0                      0.0      CU  
     5                 842.0                      0.0      CU  
     6                 742.0                    411.0      CU  
     7                 647.0                     -4.0      CU  
     8                 626.0                    101.0      CU  
     9                 624.0                    -31.0      CU  
     10                584.0                      0.0      CU  
     11                403.0                      1.0      CU  
     12                383.0                    -44.0      CU  
     13                371.0                    354.0      CU  
     14                325.0                      0.0      CU  
     15                255.0                     -1.0      CU  
     16                175.0                    -55.0      CU  
     17                168.0                   -121.0      CU  
     18                162.0                    -10.0      CU  
     19                155.0                      3.0      CU  
     20              11204.0                    717.0      CU  ,
     'cu1903':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   cu1903     1           东证期货   2810.0   -556.0            金瑞期货   
     1   cu1903     2           国投安信   2484.0    -37.0            建信期货   
     2   cu1903     3           中信期货   2036.0   -211.0            广发期货   
     3   cu1903     4           中银国际   2000.0   -148.0            云晨期货   
     4   cu1903     5           华泰期货   1039.0    -24.0            五矿经易   
     5   cu1903     6           国泰君安   1021.0     -4.0            中信期货   
     6   cu1903     7           五矿经易    901.0    569.0            迈科期货   
     7   cu1903     8           海通期货    891.0  -1014.0            瑞达期货   
     8   cu1903     9           金瑞期货    838.0    146.0            国泰君安   
     9   cu1903    10           方正中期    759.0    153.0            上海中期   
     10  cu1903    11           上海中期    746.0   -137.0            方正中期   
     11  cu1903    12           广发期货    693.0    159.0            首创期货   
     12  cu1903    13           铜冠金源    663.0   -148.0            银河期货   
     13  cu1903    14           云晨期货    662.0     54.0            铜冠金源   
     14  cu1903    15           永安期货    609.0    -17.0            华泰期货   
     15  cu1903    16           东方财富    602.0   -320.0            永安期货   
     16  cu1903    17           鲁证期货    533.0   -454.0            弘业期货   
     17  cu1903    18           中融汇信    500.0   -114.0            海通期货   
     18  cu1903    19           首创期货    478.0   -294.0            东方财富   
     19  cu1903    20           中辉期货    434.0    -29.0            兴业期货   
     20  cu1903   999           None  20699.0  -2426.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               3526.0                   112.0             永安期货   
     1               2662.0                   134.0             五矿经易   
     2               2090.0                   514.0             国泰君安   
     3               1801.0                   404.0             云晨期货   
     4               1593.0                   102.0             中信期货   
     5               1491.0                   156.0             广发期货   
     6               1426.0                    97.0             瑞达期货   
     7               1279.0                    16.0             方正中期   
     8               1264.0                    53.0             兴业期货   
     9               1235.0                    -4.0             国投安信   
     10              1179.0                   396.0             金瑞期货   
     11              1178.0                    89.0             宏源期货   
     12              1163.0                    22.0             新湖期货   
     13              1075.0                  -115.0             鲁证期货   
     14              1069.0                   260.0             东方财富   
     15               996.0                   -67.0             兴证期货   
     16               967.0                    -7.0             海通期货   
     17               966.0                    -4.0             光大期货   
     18               806.0                  -175.0             一德期货   
     19               631.0                     4.0             道通期货   
     20             28397.0                  1987.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                3823.0                     28.0      CU  
     1                2327.0                    481.0      CU  
     2                2238.0                    174.0      CU  
     3                2226.0                    218.0      CU  
     4                1890.0                    -94.0      CU  
     5                1818.0                    -55.0      CU  
     6                1413.0                      0.0      CU  
     7                1301.0                     85.0      CU  
     8                1197.0                     29.0      CU  
     9                1194.0                     40.0      CU  
     10               1151.0                    234.0      CU  
     11               1022.0                    223.0      CU  
     12                947.0                     31.0      CU  
     13                928.0                    190.0      CU  
     14                815.0                     11.0      CU  
     15                811.0                    -40.0      CU  
     16                692.0                     11.0      CU  
     17                657.0                     82.0      CU  
     18                629.0                    243.0      CU  
     19                590.0                      3.0      CU  
     20              27669.0                   1894.0      CU  ,
     'cu1901':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   cu1901     1           华泰期货   9795.0  -2312.0            金瑞期货   
     1   cu1901     2           东证期货   6356.0   -523.0            中信期货   
     2   cu1901     3           国投安信   4135.0  -1194.0            永安期货   
     3   cu1901     4           中信期货   3773.0    -65.0            五矿经易   
     4   cu1901     5           中银国际   2624.0   -877.0            建信期货   
     5   cu1901     6           国泰君安   2605.0    -62.0            海通期货   
     6   cu1901     7           海通期货   2107.0     56.0            中粮期货   
     7   cu1901     8           银河期货   2081.0    279.0            鲁证期货   
     8   cu1901     9           五矿经易   1910.0    587.0            一德期货   
     9   cu1901    10           鲁证期货   1895.0    -19.0            铜冠金源   
     10  cu1901    11           金瑞期货   1675.0  -1086.0            广发期货   
     11  cu1901    12           兴证期货   1562.0   -588.0            中辉期货   
     12  cu1901    13           铜冠金源   1503.0   -229.0            江海汇鑫   
     13  cu1901    14           西部期货   1188.0   -272.0            方正中期   
     14  cu1901    15           上海中期   1180.0   -274.0            上海大陆   
     15  cu1901    16           建信期货   1087.0    -20.0            渤海期货   
     16  cu1901    17           中融汇信    972.0   -177.0            银河期货   
     17  cu1901    18           宏源期货    952.0   -423.0            兴业期货   
     18  cu1901    19           永安期货    852.0    340.0            南华期货   
     19  cu1901    20           一德期货    837.0    255.0            中信建投   
     20  cu1901   999           None  49089.0  -6604.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               9727.0                   -80.0             五矿经易   
     1               5375.0                   -20.0             国泰君安   
     2               2540.0                    31.0             金瑞期货   
     3               2004.0                  -364.0             中信期货   
     4               1942.0                  -211.0             永安期货   
     5               1891.0                   -52.0             迈科期货   
     6               1595.0                    89.0             信达期货   
     7               1313.0                   118.0             建信期货   
     8               1251.0                  -367.0             云晨期货   
     9               1245.0                    37.0             鲁证期货   
     10              1233.0                   -25.0             华泰期货   
     11              1168.0                    96.0             兴业期货   
     12              1115.0                     0.0             铜冠金源   
     13              1074.0                    -7.0             新湖期货   
     14               961.0                    15.0             国贸期货   
     15               923.0                   380.0             银河期货   
     16               919.0                   153.0             广发期货   
     17               889.0                    63.0             华安期货   
     18               771.0                    -8.0             东海期货   
     19               758.0                   -26.0             大有期货   
     20             38694.0                  -178.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                5377.0                   -446.0      CU  
     1                5349.0                    -17.0      CU  
     2                5204.0                    271.0      CU  
     3                3565.0                   -137.0      CU  
     4                2372.0                   -197.0      CU  
     5                2271.0                   -258.0      CU  
     6                2264.0                     73.0      CU  
     7                1456.0                    132.0      CU  
     8                1287.0                     28.0      CU  
     9                1266.0                    125.0      CU  
     10               1140.0                     41.0      CU  
     11               1136.0                    293.0      CU  
     12               1071.0                    138.0      CU  
     13               1057.0                    -57.0      CU  
     14                994.0                    -37.0      CU  
     15                918.0                    -84.0      CU  
     16                872.0                    -10.0      CU  
     17                835.0                    137.0      CU  
     18                759.0                    321.0      CU  
     19                758.0                     71.0      CU  
     20              39951.0                    387.0      CU  ,
     'cu1812':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   cu1812     1           金瑞期货   1735.0   -845.0            金瑞期货   
     1   cu1812     2           五矿经易   1225.0    155.0            金信期货   
     2   cu1812     3           迈科期货   1055.0    745.0            中银国际   
     3   cu1812     4           国泰君安   1030.0    565.0            中粮期货   
     4   cu1812     5           中银国际    950.0     20.0            华安期货   
     5   cu1812     6           华金期货    840.0    235.0            五矿经易   
     6   cu1812     7           国投安信    790.0     10.0            国泰君安   
     7   cu1812     8           海通期货    670.0   -165.0            中信期货   
     8   cu1812     9           宏源期货    610.0   -230.0            国投安信   
     9   cu1812    10           云晨期货    610.0    165.0            迈科期货   
     10  cu1812    11           铜冠金源    595.0    465.0            银河期货   
     11  cu1812    12           方正中期    540.0    330.0            南华期货   
     12  cu1812    13           银河期货    515.0    225.0            兴业期货   
     13  cu1812    14           永安期货    490.0    265.0            建信期货   
     14  cu1812    15           中信期货    475.0   -540.0            永安期货   
     15  cu1812    16           光大期货    450.0   -135.0            中航期货   
     16  cu1812    17           中信建投    395.0    125.0            渤海期货   
     17  cu1812    18           华泰期货    370.0   -270.0            中信建投   
     18  cu1812    19           长江期货    305.0    195.0            方正中期   
     19  cu1812    20           东海期货    280.0    -90.0            广发期货   
     20  cu1812   999           None  13930.0   1225.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               2125.0                    50.0             金瑞期货   
     1               1175.0                   -40.0             中信期货   
     2               1045.0                   410.0             云晨期货   
     3                895.0                  -205.0             五矿经易   
     4                795.0                  -110.0             迈科期货   
     5                650.0                  -535.0             鲁证期货   
     6                640.0                  -585.0             中辉期货   
     7                575.0                   -25.0             国泰君安   
     8                555.0                   120.0             永安期货   
     9                495.0                  -340.0             建信期货   
     10               410.0                  -350.0             兴业期货   
     11               340.0                   -55.0             银河期货   
     12               340.0                    40.0             一德期货   
     13               320.0                   -45.0             海通期货   
     14               310.0                  -135.0             东海期货   
     15               300.0                     0.0             创元期货   
     16               300.0                     0.0             广州期货   
     17               285.0                   -60.0             铜冠金源   
     18               270.0                  -335.0             方正中期   
     19               270.0                    20.0             华泰期货   
     20             12095.0                 -2180.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                3990.0                   -885.0      CU  
     1                1645.0                    -30.0      CU  
     2                1550.0                   -110.0      CU  
     3                1470.0                   -250.0      CU  
     4                 890.0                   -405.0      CU  
     5                 520.0                      0.0      CU  
     6                 390.0                    -45.0      CU  
     7                 370.0                   -185.0      CU  
     8                 365.0                    355.0      CU  
     9                 360.0                   -105.0      CU  
     10                340.0                    -10.0      CU  
     11                270.0                      5.0      CU  
     12                230.0                    -55.0      CU  
     13                220.0                   -175.0      CU  
     14                170.0                   -160.0      CU  
     15                165.0                    -15.0      CU  
     16                160.0                      0.0      CU  
     17                150.0                     50.0      CU  
     18                150.0                   -115.0      CU  
     19                150.0                     85.0      CU  
     20              13555.0                  -2050.0      CU  ,
     'cu1902':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   cu1902     1           华泰期货   17753.0  -2344.0            金瑞期货   
     1   cu1902     2           东证期货   14108.0  -1945.0            中信期货   
     2   cu1902     3           国投安信   10670.0  -2595.0            云晨期货   
     3   cu1902     4           海通期货    8311.0  -2884.0            建信期货   
     4   cu1902     5           中信期货    7638.0  -3698.0            广发期货   
     5   cu1902     6           中银国际    6046.0   -292.0            迈科期货   
     6   cu1902     7           上海中期    4340.0    570.0            华安期货   
     7   cu1902     8           中融汇信    4106.0  -2158.0            五矿经易   
     8   cu1902     9           兴证期货    3292.0  -1009.0            海通期货   
     9   cu1902    10           方正中期    3165.0  -1642.0            中钢期货   
     10  cu1902    11           永安期货    3093.0  -2044.0            中粮期货   
     11  cu1902    12           银河期货    3076.0    250.0            中航期货   
     12  cu1902    13           鲁证期货    2559.0   -795.0            弘业期货   
     13  cu1902    14           金瑞期货    2205.0   -592.0            方正中期   
     14  cu1902    15           南华期货    2017.0    -81.0            一德期货   
     15  cu1902    16           集成期货    1823.0     -3.0            国泰君安   
     16  cu1902    17           长江期货    1784.0    357.0            南华期货   
     17  cu1902    18           东航期货    1769.0    898.0            东吴期货   
     18  cu1902    19           华安期货    1758.0   -216.0            银河期货   
     19  cu1902    20           申万期货    1748.0    237.0            宏源期货   
     20  cu1902   999           None  101261.0 -19986.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               5781.0                   254.0             永安期货   
     1               5104.0                  -178.0             云晨期货   
     2               4318.0                    20.0             申万期货   
     3               4301.0                   290.0             中信期货   
     4               4226.0                    88.0             国投安信   
     5               4117.0                   -43.0             五矿经易   
     6               3483.0                   150.0             华泰期货   
     7               3041.0                   306.0             格林大华   
     8               2685.0                     4.0             金瑞期货   
     9               2237.0                     0.0             浙商期货   
     10              2188.0                    -9.0             兴业期货   
     11              2084.0                     8.0             南华期货   
     12              1825.0                   -99.0             东海期货   
     13              1768.0                   171.0             东证期货   
     14              1617.0                     5.0             中粮期货   
     15              1576.0                     8.0             光大期货   
     16              1514.0                    82.0             方正中期   
     17              1300.0                   100.0             银河期货   
     18              1285.0                   189.0             国泰君安   
     19              1212.0                   303.0             道通期货   
     20             55662.0                  1649.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               12572.0                    639.0      CU  
     1                5376.0                      0.0      CU  
     2                4893.0                   -392.0      CU  
     3                4892.0                     24.0      CU  
     4                4844.0                    -35.0      CU  
     5                3120.0                     51.0      CU  
     6                2588.0                    524.0      CU  
     7                2305.0                     28.0      CU  
     8                2268.0                   -217.0      CU  
     9                2220.0                     22.0      CU  
     10               2166.0                    -32.0      CU  
     11               1913.0                   -179.0      CU  
     12               1879.0                    308.0      CU  
     13               1877.0                    504.0      CU  
     14               1858.0                     31.0      CU  
     15               1752.0                    104.0      CU  
     16               1668.0                    162.0      CU  
     17               1652.0                    -51.0      CU  
     18               1491.0                    -48.0      CU  
     19               1465.0                    -45.0      CU  
     20              62799.0                   1398.0      CU  ,
     'cu1904':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   cu1904     1           东证期货  1162.0    -93.0            中信期货   
     1   cu1904     2           国投安信   954.0    138.0            金瑞期货   
     2   cu1904     3           中信期货   738.0    -29.0            东方财富   
     3   cu1904     4           东方财富   412.0    -81.0            瑞达期货   
     4   cu1904     5           渤海期货   408.0    386.0            方正中期   
     5   cu1904     6           五矿经易   395.0    376.0            银河期货   
     6   cu1904     7           华泰期货   373.0   -154.0            兴证期货   
     7   cu1904     8           中银国际   344.0    -36.0            五矿经易   
     8   cu1904     9           方正中期   322.0   -539.0            迈科期货   
     9   cu1904    10           铜冠金源   292.0    100.0            南华期货   
     10  cu1904    11           金元期货   292.0    292.0            东兴期货   
     11  cu1904    12           银河期货   276.0     78.0            建信期货   
     12  cu1904    13           西部期货   232.0     19.0            云晨期货   
     13  cu1904    14           金瑞期货   225.0     58.0            宏源期货   
     14  cu1904    15           宏源期货   220.0    174.0            新湖期货   
     15  cu1904    16           一德期货   203.0    155.0            永安期货   
     16  cu1904    17           海通期货   197.0   -198.0            国投安信   
     17  cu1904    18           中辉期货   166.0   -139.0            弘业期货   
     18  cu1904    19           中信建投   107.0     97.0            中粮期货   
     19  cu1904    20           国富期货    96.0     10.0            华泰期货   
     20  cu1904   999           None  7414.0    614.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               2904.0                  -117.0             东方财富   
     1               2707.0                   225.0             广发期货   
     2               2595.0                    -3.0             中钢期货   
     3               1355.0                     6.0             国投安信   
     4               1149.0                    41.0             金信期货   
     5                621.0                   -64.0             中信期货   
     6                542.0                    -3.0             建信期货   
     7                497.0                    32.0             国泰君安   
     8                486.0                     0.0             国贸期货   
     9                385.0                   -40.0             上海中期   
     10               356.0                     0.0             中粮期货   
     11               350.0                     0.0             中信建投   
     12               310.0                     0.0             华泰期货   
     13               252.0                    10.0             银河期货   
     14               250.0                     0.0             渤海期货   
     15               220.0                     2.0             一德期货   
     16               219.0                    81.0             云晨期货   
     17               217.0                     4.0             华安期货   
     18               215.0                    -1.0             兴业期货   
     19               207.0                    -4.0             徽商期货   
     20             15837.0                   169.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                2985.0                   -135.0      CU  
     1                1498.0                     81.0      CU  
     2                1454.0                      0.0      CU  
     3                1367.0                     -7.0      CU  
     4                 983.0                      0.0      CU  
     5                 968.0                      7.0      CU  
     6                 906.0                      3.0      CU  
     7                 901.0                      0.0      CU  
     8                 800.0                      0.0      CU  
     9                 732.0                      4.0      CU  
     10                618.0                      0.0      CU  
     11                576.0                     70.0      CU  
     12                544.0                    -19.0      CU  
     13                505.0                    146.0      CU  
     14                410.0                    388.0      CU  
     15                401.0                   -203.0      CU  
     16                330.0                      0.0      CU  
     17                314.0                     -5.0      CU  
     18                284.0                     14.0      CU  
     19                253.0                     34.0      CU  
     20              16829.0                    378.0      CU  ,
     'al1905':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   al1905     1           申万期货   490.0  -1008.0            国信期货   
     1   al1905     2           渤海期货   200.0    114.0            中信建投   
     2   al1905     3           上海中期   177.0    167.0            上海中期   
     3   al1905     4           银河期货   111.0    -56.0            建信期货   
     4   al1905     5           中辉期货    94.0    -22.0            先融期货   
     5   al1905     6           海通期货    84.0    -53.0            中粮期货   
     6   al1905     7           金元期货    71.0    -43.0            金瑞期货   
     7   al1905     8           鲁证期货    68.0    -72.0            新湖期货   
     8   al1905     9           西部期货    58.0     58.0            中钢期货   
     9   al1905    10           华泰期货    53.0      9.0            银河期货   
     10  al1905    11           中融汇信    48.0    -17.0             新世纪   
     11  al1905    12           中银国际    44.0   -457.0            光大期货   
     12  al1905    13           平安期货    33.0    -48.0            鲁证期货   
     13  al1905    14           一德期货    29.0    -49.0            金石期货   
     14  al1905    15           宝城期货    28.0    -68.0            海通期货   
     15  al1905    16           光大期货    26.0     20.0            信达期货   
     16  al1905    17           通惠期货    24.0     21.0            一德期货   
     17  al1905    18           新晟期货    24.0    -15.0            中金期货   
     18  al1905    19           广发期货    22.0    -22.0            福能期货   
     19  al1905    20           先融期货    22.0   -140.0            海航期货   
     20  al1905   999           None  1706.0  -1681.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               3029.0                     5.0             永安期货   
     1               1893.0                    -8.0             首创期货   
     2               1884.0                     0.0             申万期货   
     3               1208.0                     0.0             东兴期货   
     4               1201.0                    -4.0             国信期货   
     5               1197.0                    -3.0             大地期货   
     6                948.0                     0.0             建信期货   
     7                465.0                     0.0             五矿经易   
     8                413.0                     0.0             国海良时   
     9                385.0                    14.0             一德期货   
     10               301.0                     0.0             上海中期   
     11               277.0                   -24.0             海通期货   
     12               259.0                    51.0             广发期货   
     13               247.0                     0.0             渤海期货   
     14               231.0                     1.0             中信期货   
     15               230.0                     0.0             格林大华   
     16               226.0                    -3.0             中银国际   
     17               225.0                     0.0             国联期货   
     18               222.0                     0.0             倍特期货   
     19               211.0                    -1.0             银河期货   
     20             15052.0                    28.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                3221.0                      3.0      AL  
     1                3115.0                      0.0      AL  
     2                1163.0                     78.0      AL  
     3                1042.0                     -6.0      AL  
     4                1037.0                      1.0      AL  
     5                 904.0                    -16.0      AL  
     6                 685.0                      0.0      AL  
     7                 625.0                      0.0      AL  
     8                 543.0                      1.0      AL  
     9                 504.0                     20.0      AL  
     10                452.0                    175.0      AL  
     11                405.0                     -1.0      AL  
     12                385.0                      0.0      AL  
     13                376.0                   -200.0      AL  
     14                363.0                     -5.0      AL  
     15                218.0                     -1.0      AL  
     16                169.0                      2.0      AL  
     17                167.0                     -3.0      AL  
     18                125.0                     20.0      AL  
     19                112.0                      5.0      AL  
     20              15611.0                     73.0      AL  ,
     'al1904':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   al1904     1           申万期货   697.0   -897.0            国信期货   
     1   al1904     2           中信期货   346.0   -185.0            中粮期货   
     2   al1904     3           华泰期货   319.0    -43.0            金瑞期货   
     3   al1904     4           建信期货   211.0   -186.0            中信期货   
     4   al1904     5           中辉期货   192.0    -88.0            格林大华   
     5   al1904     6           国投安信   177.0    -73.0            上海中期   
     6   al1904     7           海通期货   174.0   -118.0            建信期货   
     7   al1904     8           东方财富   162.0      4.0            宏源期货   
     8   al1904     9           东亚期货   160.0    160.0            瑞达期货   
     9   al1904    10           中银国际   160.0    -23.0            先融期货   
     10  al1904    11           广发期货   140.0    110.0            天风期货   
     11  al1904    12           银河期货   138.0    -44.0            海通期货   
     12  al1904    13           中融汇信   133.0   -183.0            华信期货   
     13  al1904    14           兴证期货   106.0     77.0            东兴期货   
     14  al1904    15           新晟期货    90.0     78.0            倍特期货   
     15  al1904    16           平安期货    69.0     -1.0            瑞龙期货   
     16  al1904    17           西部期货    66.0     64.0            新湖期货   
     17  al1904    18           新湖期货    64.0    -57.0            申万期货   
     18  al1904    19           海证期货    54.0      2.0            信达期货   
     19  al1904    20           鲁证期货    50.0    -65.0            方正中期   
     20  al1904   999           None  3508.0  -1468.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               2654.0                     8.0             建信期货   
     1               1812.0                     0.0             中粮期货   
     2               1596.0                    33.0             上海中期   
     3               1291.0                     5.0             永安期货   
     4                984.0                     3.0             五矿经易   
     5                918.0                     0.0             中信期货   
     6                838.0                     9.0             一德期货   
     7                815.0                     0.0             国信期货   
     8                801.0                     0.0             金瑞期货   
     9                800.0                     0.0             中信建投   
     10               750.0                     0.0             大地期货   
     11               701.0                    11.0             东兴期货   
     12               691.0                    -3.0             中钢期货   
     13               628.0                     5.0             徽商期货   
     14               501.0                     0.0             国金期货   
     15               483.0                   -30.0             海通期货   
     16               482.0                     0.0             冠通期货   
     17               438.0                    65.0             兴证期货   
     18               420.0                     0.0             国投安信   
     19               415.0                     0.0             方正中期   
     20             18018.0                   106.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                2440.0                    200.0      AL  
     1                2296.0                      0.0      AL  
     2                2204.0                     -3.0      AL  
     3                1872.0                      2.0      AL  
     4                1844.0                     -4.0      AL  
     5                1581.0                     99.0      AL  
     6                1470.0                      0.0      AL  
     7                1233.0                     -2.0      AL  
     8                1000.0                      0.0      AL  
     9                 636.0                      0.0      AL  
     10                627.0                    -40.0      AL  
     11                614.0                     -5.0      AL  
     12                555.0                      0.0      AL  
     13                514.0                     -8.0      AL  
     14                417.0                      0.0      AL  
     15                395.0                      1.0      AL  
     16                360.0                      0.0      AL  
     17                328.0                    100.0      AL  
     18                326.0                     -2.0      AL  
     19                306.0                      5.0      AL  
     20              21018.0                    343.0      AL  ,
     'al1902':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   al1902     1           中信期货   8506.0     80.0            中信期货   
     1   al1902     2           海通期货   7696.0   -535.0            国信期货   
     2   al1902     3           中辉期货   5239.0  -1460.0            建信期货   
     3   al1902     4           东证期货   5117.0  -1902.0            华泰期货   
     4   al1902     5           国投安信   5083.0    545.0            金瑞期货   
     5   al1902     6           兴证期货   3205.0   1587.0            迈科期货   
     6   al1902     7           华泰期货   2614.0  -1557.0            五矿经易   
     7   al1902     8           申万期货   2584.0  -1621.0            中粮期货   
     8   al1902     9           国泰君安   2311.0    379.0            上海中期   
     9   al1902    10           建信期货   1844.0    263.0            方正中期   
     10  al1902    11           广州期货   1650.0   1511.0            国投安信   
     11  al1902    12           长江期货   1627.0    -31.0            格林大华   
     12  al1902    13           方正中期   1524.0  -1091.0            信达期货   
     13  al1902    14           宏源期货   1490.0    102.0            先融期货   
     14  al1902    15           中银国际   1474.0   -262.0            创元期货   
     15  al1902    16           铜冠金源   1351.0    152.0            中信建投   
     16  al1902    17           中融汇信   1237.0   -382.0            海通期货   
     17  al1902    18           国信期货   1216.0   -558.0            招商期货   
     18  al1902    19           国富期货   1116.0    370.0            徽商期货   
     19  al1902    20           东亚期货   1041.0    565.0            兴证期货   
     20  al1902   999           None  57925.0  -3845.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0              13193.0                   428.0             中信期货   
     1              10483.0                  -294.0             永安期货   
     2               8508.0                   639.0             申万期货   
     3               5576.0                   -18.0             格林大华   
     4               5095.0                   134.0             上海中期   
     5               4698.0                    -9.0             建信期货   
     6               4645.0                  -371.0             国泰君安   
     7               4064.0                   -12.0             国投安信   
     8               2756.0                    51.0             海通期货   
     9               2666.0                    24.0             云晨期货   
     10              2506.0                   119.0             兴证期货   
     11              2334.0                   551.0             中金期货   
     12              1940.0                   -23.0             中国国际   
     13              1810.0                     0.0             方正中期   
     14              1722.0                     0.0             银河期货   
     15              1631.0                   -62.0             中粮期货   
     16              1478.0                     7.0             华泰期货   
     17              1465.0                     0.0             首创期货   
     18              1414.0                     4.0             一德期货   
     19              1302.0                   245.0             东兴期货   
     20             79286.0                  1413.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               15701.0                   1808.0      AL  
     1               11457.0                     49.0      AL  
     2                5147.0                    100.0      AL  
     3                4892.0                    -91.0      AL  
     4                4659.0                     41.0      AL  
     5                4459.0                   -117.0      AL  
     6                3846.0                    695.0      AL  
     7                3676.0                   -678.0      AL  
     8                3235.0                   -159.0      AL  
     9                2706.0                    -11.0      AL  
     10               2607.0                   1042.0      AL  
     11               2607.0                     11.0      AL  
     12               2547.0                     19.0      AL  
     13               2333.0                   -232.0      AL  
     14               2260.0                     42.0      AL  
     15               2128.0                   -170.0      AL  
     16               2017.0                    134.0      AL  
     17               1958.0                    -75.0      AL  
     18               1768.0                    -19.0      AL  
     19               1723.0                    142.0      AL  
     20              81726.0                   2531.0      AL  ,
     'al1903':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   al1903     1           海通期货   3403.0  -1195.0            上海中期   
     1   al1903     2           国投安信   1971.0    472.0            国信期货   
     2   al1903     3           中辉期货   1971.0   -161.0            建信期货   
     3   al1903     4           申万期货   1848.0   -454.0            中粮期货   
     4   al1903     5           中信期货   1739.0  -1019.0            五矿经易   
     5   al1903     6           东证期货   1079.0   -744.0            金瑞期货   
     6   al1903     7           江海汇鑫   1006.0   1000.0            方正中期   
     7   al1903     8           华泰期货    978.0   -454.0            先融期货   
     8   al1903     9           建信期货    873.0    619.0            迈科期货   
     9   al1903    10           创元期货    650.0    644.0            中信期货   
     10  al1903    11           中融汇信    596.0   -178.0            信达期货   
     11  al1903    12           上海中期    565.0   -337.0            永安期货   
     12  al1903    13           中银国际    563.0   -132.0            瑞达期货   
     13  al1903    14           迈科期货    523.0  -1785.0            东兴期货   
     14  al1903    15           方正中期    450.0   -520.0            国投安信   
     15  al1903    16           银河期货    449.0   -575.0            海通期货   
     16  al1903    17           国泰君安    440.0    -70.0            华泰期货   
     17  al1903    18           永安期货    401.0    156.0            南华期货   
     18  al1903    19           鲁证期货    384.0   -285.0            广州期货   
     19  al1903    20           东亚期货    340.0    340.0            创元期货   
     20  al1903   999           None  20229.0  -4678.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               8553.0                   160.0             中信期货   
     1               7480.0                   -26.0             建信期货   
     2               5319.0                   729.0             中粮期货   
     3               5278.0                    -1.0             一德期货   
     4               4697.0                    -5.0             永安期货   
     5               3807.0                     0.0             迈科期货   
     6               3249.0                   -15.0             鲁证期货   
     7               2815.0                     0.0             上海中期   
     8               2052.0                    70.0             中金期货   
     9               1370.0                    -7.0             银河期货   
     10              1173.0                     4.0             五矿经易   
     11              1166.0                   102.0             华信期货   
     12              1142.0                     0.0             格林大华   
     13               949.0                     2.0             大地期货   
     14               943.0                  -681.0             国信期货   
     15               929.0                    20.0             广发期货   
     16               867.0                    20.0             中银国际   
     17               865.0                     0.0             中钢期货   
     18               755.0                    86.0             倍特期货   
     19               730.0                   650.0             海通期货   
     20             54139.0                  1108.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                9219.0                    -12.0      AL  
     1                4549.0                    102.0      AL  
     2                4507.0                    171.0      AL  
     3                4421.0                     39.0      AL  
     4                4339.0                   -229.0      AL  
     5                2670.0                     -9.0      AL  
     6                2509.0                    -38.0      AL  
     7                2413.0                   -133.0      AL  
     8                2184.0                      6.0      AL  
     9                1949.0                     74.0      AL  
     10               1860.0                      0.0      AL  
     11               1650.0                    277.0      AL  
     12               1380.0                   -105.0      AL  
     13               1363.0                    -41.0      AL  
     14               1152.0                     42.0      AL  
     15               1067.0                     28.0      AL  
     16               1062.0                     -1.0      AL  
     17                942.0                      0.0      AL  
     18                717.0                     79.0      AL  
     19                686.0                     11.0      AL  
     20              50639.0                    261.0      AL  ,
     'al1812':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   al1812     1           中信期货  1720.0    200.0            中信期货   
     1   al1812     2           一德期货   780.0  -1000.0            中粮期货   
     2   al1812     3           光大期货   535.0    110.0            一德期货   
     3   al1812     4           首创期货   485.0  -1260.0            首创期货   
     4   al1812     5           德盛期货   480.0    -20.0            国信期货   
     5   al1812     6           金瑞期货   420.0   -335.0            大地期货   
     6   al1812     7           华泰期货   410.0     50.0            五矿经易   
     7   al1812     8           国信期货   410.0   -550.0            金瑞期货   
     8   al1812     9           方正中期   355.0    155.0            格林大华   
     9   al1812    10           申万期货   345.0    -90.0            国海良时   
     10  al1812    11           中财期货   330.0    285.0            建信期货   
     11  al1812    12           浙商期货   300.0     30.0            方正中期   
     12  al1812    13           东证期货   300.0   -625.0            光大期货   
     13  al1812    14           铜冠金源   275.0     95.0            大有期货   
     14  al1812    15           国金期货   260.0    105.0            国泰君安   
     15  al1812    16           中银国际   260.0    -60.0            浙商期货   
     16  al1812    17           迈科期货   245.0    235.0            华泰期货   
     17  al1812    18           海通期货   245.0   -505.0            国投安信   
     18  al1812    19           中粮期货   230.0   -885.0            申万期货   
     19  al1812    20           建信期货   205.0   -320.0            铜冠金源   
     20  al1812   999           None  8590.0  -4385.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               3745.0                   180.0             国贸期货   
     1               3240.0                   185.0             中信期货   
     2               2310.0                   210.0             建信期货   
     3               1770.0                    15.0             五矿经易   
     4               1705.0                  -400.0             国信期货   
     5               1295.0                    95.0             中粮期货   
     6               1200.0                    55.0             上海中期   
     7               1160.0                  -370.0             鲁证期货   
     8               1155.0                    15.0             首创期货   
     9                990.0                   120.0             兴证期货   
     10               980.0                    35.0             一德期货   
     11               790.0                  -150.0             德盛期货   
     12               655.0                   170.0             金瑞期货   
     13               590.0                     0.0             大地期货   
     14               575.0                   -60.0             新湖期货   
     15               540.0                  -300.0             格林大华   
     16               520.0                  -310.0             国投安信   
     17               515.0                     0.0             中国国际   
     18               465.0                   -45.0             东亚期货   
     19               415.0                  -195.0             中银国际   
     20             24615.0                  -750.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                3020.0                      0.0      AL  
     1                2740.0                    430.0      AL  
     2                2500.0                    -60.0      AL  
     3                2480.0                     20.0      AL  
     4                2275.0                    -10.0      AL  
     5                1565.0                    -45.0      AL  
     6                1480.0                      0.0      AL  
     7                1450.0                    -15.0      AL  
     8                1385.0                      0.0      AL  
     9                1195.0                     -5.0      AL  
     10                980.0                   -430.0      AL  
     11                700.0                      0.0      AL  
     12                650.0                     50.0      AL  
     13                645.0                      0.0      AL  
     14                600.0                      0.0      AL  
     15                585.0                     85.0      AL  
     16                565.0                      0.0      AL  
     17                515.0                    -50.0      AL  
     18                510.0                      0.0      AL  
     19                445.0                      5.0      AL  
     20              26285.0                    -25.0      AL  ,
     'al1901':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   al1901     1           海通期货  15833.0  -6709.0            中信期货   
     1   al1901     2           中信期货   7746.0   -913.0            中粮期货   
     2   al1901     3           东证期货   6958.0  -3421.0            华泰期货   
     3   al1901     4           中融汇信   6154.0  -2130.0            永安期货   
     4   al1901     5           华泰期货   4765.0  -1809.0            建信期货   
     5   al1901     6           国投安信   4625.0   -649.0            国信期货   
     6   al1901     7           兴证期货   3120.0  -1110.0            金瑞期货   
     7   al1901     8           申万期货   2370.0  -2425.0            鲁证期货   
     8   al1901     9           中辉期货   2163.0  -2426.0            上海中期   
     9   al1901    10           光大期货   2056.0   -893.0            一德期货   
     10  al1901    11           一德期货   1951.0    458.0            首创期货   
     11  al1901    12           方正中期   1903.0   -464.0            华安期货   
     12  al1901    13           鲁证期货   1789.0   -426.0            国泰君安   
     13  al1901    14           金瑞期货   1783.0   -549.0            五矿经易   
     14  al1901    15           中银国际   1666.0   -553.0            方正中期   
     15  al1901    16           国泰君安   1577.0    566.0            格林大华   
     16  al1901    17           大有期货   1498.0   -691.0            迈科期货   
     17  al1901    18           南华期货   1403.0   -341.0            兴证期货   
     18  al1901    19           创元期货   1305.0    344.0            海通期货   
     19  al1901    20           铜冠金源   1207.0   -192.0            银河期货   
     20  al1901   999           None  71872.0 -24333.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               8047.0                  -210.0             中信期货   
     1               7652.0                   -68.0             中粮期货   
     2               7596.0                   361.0             永安期货   
     3               5538.0                    45.0             建信期货   
     4               4339.0                    -4.0             一德期货   
     5               4239.0                  -147.0             云晨期货   
     6               4144.0                    66.0             海通期货   
     7               3094.0                   166.0             国投安信   
     8               2530.0                   -64.0             华泰期货   
     9               2132.0                  -189.0             首创期货   
     10              2127.0                   -91.0             方正中期   
     11              1972.0                   -88.0             国海良时   
     12              1818.0                    82.0             鲁证期货   
     13              1744.0                    17.0             申万期货   
     14              1342.0                   -29.0             中国国际   
     15              1252.0                  -277.0             兴证期货   
     16              1216.0                   -23.0             五矿经易   
     17              1192.0                  -243.0             浙商期货   
     18              1159.0                  -320.0             广发期货   
     19              1088.0                    34.0             中辉期货   
     20             64221.0                  -982.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               15963.0                  -1852.0      AL  
     1                5351.0                    142.0      AL  
     2                5125.0                   -411.0      AL  
     3                4666.0                    227.0      AL  
     4                4177.0                    492.0      AL  
     5                3172.0                    320.0      AL  
     6                2792.0                    -83.0      AL  
     7                2692.0                    468.0      AL  
     8                2405.0                   -102.0      AL  
     9                2125.0                    150.0      AL  
     10               1975.0                     -4.0      AL  
     11               1919.0                    304.0      AL  
     12               1858.0                   -425.0      AL  
     13               1773.0                   -112.0      AL  
     14               1665.0                     -6.0      AL  
     15               1649.0                   -901.0      AL  
     16               1648.0                    159.0      AL  
     17               1539.0                    166.0      AL  
     18               1473.0                    -46.0      AL  
     19               1354.0                    210.0      AL  
     20              65321.0                  -1304.0      AL  ,
     'zn1901':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   zn1901     1           华泰期货   25912.0 -16978.0            永安期货   
     1   zn1901     2           中信期货   17804.0  -7491.0            中信期货   
     2   zn1901     3           海通期货   16320.0 -22415.0            广发期货   
     3   zn1901     4           东证期货   11211.0  -6348.0            海通期货   
     4   zn1901     5           国投安信    9845.0  -2643.0            五矿经易   
     5   zn1901     6           中融汇信    7421.0 -14748.0            金瑞期货   
     6   zn1901     7           中银国际    6468.0  -4231.0            国投安信   
     7   zn1901     8           鲁证期货    5183.0  -2387.0            中粮期货   
     8   zn1901     9           方正中期    5016.0  -4038.0            东亚期货   
     9   zn1901    10           银河期货    3963.0  -1909.0            华泰期货   
     10  zn1901    11           大有期货    3830.0    553.0            上海中期   
     11  zn1901    12           永安期货    3560.0  -1790.0            一德期货   
     12  zn1901    13           国泰君安    3356.0   -399.0            鲁证期货   
     13  zn1901    14           上海中期    3071.0    256.0            银河期货   
     14  zn1901    15           兴证期货    2867.0    -42.0            中财期货   
     15  zn1901    16           西部期货    2694.0   1166.0            格林大华   
     16  zn1901    17           南华期货    2625.0    -40.0            建信期货   
     17  zn1901    18           广发期货    2575.0    -60.0            迈科期货   
     18  zn1901    19           五矿经易    2569.0   -383.0            南华期货   
     19  zn1901    20           徽商期货    2556.0  -1270.0            国贸期货   
     20  zn1901   999           None  138846.0 -85197.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               6177.0                 -1029.0             中信期货   
     1               4831.0                  -707.0             永安期货   
     2               3489.0                  -468.0             华泰期货   
     3               3397.0                   145.0             五矿经易   
     4               3160.0                  -483.0             格林大华   
     5               2816.0                    46.0             铜冠金源   
     6               2636.0                   -60.0             中粮期货   
     7               1723.0                    -4.0             金瑞期货   
     8               1720.0                     0.0             一德期货   
     9               1560.0                  -417.0             建信期货   
     10              1430.0                    74.0             国投安信   
     11              1325.0                    91.0             广发期货   
     12              1231.0                  -942.0             南华期货   
     13              1134.0                   137.0             方正中期   
     14              1120.0                  -331.0             海通期货   
     15              1038.0                    25.0             大有期货   
     16              1015.0                     2.0             鲁证期货   
     17               945.0                     0.0             兴证期货   
     18               845.0                  -441.0             银河期货   
     19               824.0                    -5.0             中钢期货   
     20             42416.0                 -4367.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                5530.0                    243.0      ZN  
     1                4511.0                   -669.0      ZN  
     2                4049.0                   -617.0      ZN  
     3                3106.0                     66.0      ZN  
     4                2956.0                   -237.0      ZN  
     5                2937.0                   -328.0      ZN  
     6                2659.0                   -136.0      ZN  
     7                2325.0                    154.0      ZN  
     8                2309.0                     56.0      ZN  
     9                1434.0                   -745.0      ZN  
     10               1297.0                   -137.0      ZN  
     11               1242.0                   -233.0      ZN  
     12               1082.0                     58.0      ZN  
     13               1045.0                   -273.0      ZN  
     14               1002.0                   -205.0      ZN  
     15                986.0                   -293.0      ZN  
     16                895.0                     51.0      ZN  
     17                806.0                    560.0      ZN  
     18                786.0                   -288.0      ZN  
     19                723.0                      0.0      ZN  
     20              41680.0                  -2973.0      ZN  ,
     'zn1812':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   zn1812     1           海通期货  2205.0    865.0            永安期货   
     1   zn1812     2           方正中期   725.0    655.0            五矿经易   
     2   zn1812     3           中信期货   640.0    -30.0            海通期货   
     3   zn1812     4           一德期货   635.0   -615.0            迈科期货   
     4   zn1812     5           银河期货   525.0    120.0            上海中期   
     5   zn1812     6           迈科期货   475.0    120.0            大有期货   
     6   zn1812     7           华泰期货   455.0    150.0            鲁证期货   
     7   zn1812     8           建信期货   435.0    310.0            上海大陆   
     8   zn1812     9           铜冠金源   355.0    215.0            中钢期货   
     9   zn1812    10           中银国际   335.0      0.0            中信期货   
     10  zn1812    11           光大期货   290.0  -1095.0            中粮期货   
     11  zn1812    12           申万期货   260.0   -270.0            金汇期货   
     12  zn1812    13           永安期货   255.0  -1265.0            一德期货   
     13  zn1812    14           徽商期货   200.0    140.0            建信期货   
     14  zn1812    15           广发期货   180.0     80.0            瑞达期货   
     15  zn1812    16           国富期货   175.0    -65.0            中融汇信   
     16  zn1812    17           中财期货   130.0    130.0            中财期货   
     17  zn1812    18           金瑞期货   110.0    -15.0            广发期货   
     18  zn1812    19           东证期货    90.0     75.0            西南期货   
     19  zn1812    20           东方财富    90.0    -50.0            光大期货   
     20  zn1812   999           None  8565.0   -545.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0                635.0                  -145.0             中信期货   
     1                470.0                     0.0             迈科期货   
     2                435.0                  -940.0             国贸期货   
     3                315.0                   -10.0             金瑞期货   
     4                305.0                   -10.0             华泰期货   
     5                285.0                     0.0             中大期货   
     6                280.0                     0.0             一德期货   
     7                255.0                   -10.0             东证期货   
     8                250.0                     0.0             银河期货   
     9                205.0                  -145.0             五矿经易   
     10               195.0                   -20.0             铜冠金源   
     11               190.0                     0.0             首创期货   
     12               190.0                    -5.0             中粮期货   
     13               175.0                  -435.0             宝城期货   
     14               175.0                     0.0             兴证期货   
     15               170.0                     0.0             创元期货   
     16               170.0                  -130.0             中钢期货   
     17               160.0                  -100.0             格林大华   
     18               155.0                     0.0             浙商期货   
     19               150.0                  -130.0             国富期货   
     20              5165.0                 -2080.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                1370.0                   -255.0      ZN  
     1                1195.0                   -305.0      ZN  
     2                 630.0                      0.0      ZN  
     3                 555.0                    -30.0      ZN  
     4                 360.0                    -95.0      ZN  
     5                 350.0                    -20.0      ZN  
     6                 260.0                   -350.0      ZN  
     7                 245.0                    -55.0      ZN  
     8                 140.0                   -135.0      ZN  
     9                 105.0                      0.0      ZN  
     10                100.0                   -355.0      ZN  
     11                 65.0                    -20.0      ZN  
     12                 65.0                    -25.0      ZN  
     13                 35.0                      0.0      ZN  
     14                 35.0                    -15.0      ZN  
     15                 25.0                      0.0      ZN  
     16                 20.0                      0.0      ZN  
     17                 20.0                    -30.0      ZN  
     18                 20.0                      5.0      ZN  
     19                 20.0                     10.0      ZN  
     20               5615.0                  -1675.0      ZN  ,
     'zn1902':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   zn1902     1           华泰期货   56407.0  -1481.0            五矿经易   
     1   zn1902     2           海通期货   43668.0  11661.0            中信期货   
     2   zn1902     3           中信期货   37326.0 -14743.0            银河期货   
     3   zn1902     4           国投安信   25304.0   6712.0            广发期货   
     4   zn1902     5           东证期货   22217.0   3113.0            永安期货   
     5   zn1902     6           方正中期   21792.0  11220.0            天鸿期货   
     6   zn1902     7           中融汇信   21698.0   9217.0            华泰期货   
     7   zn1902     8           徽商期货   16216.0   4615.0            迈科期货   
     8   zn1902     9           中银国际   14929.0   8093.0            上海大陆   
     9   zn1902    10           银河期货   12735.0   5104.0            海通期货   
     10  zn1902    11           申万期货    8499.0   3304.0            兴证期货   
     11  zn1902    12           华安期货    8363.0    417.0            英大期货   
     12  zn1902    13           国泰君安    7546.0  -2174.0            西南期货   
     13  zn1902    14           上海中期    7320.0   1537.0            方正中期   
     14  zn1902    15           永安期货    7318.0   -625.0            上海中期   
     15  zn1902    16           东航期货    7179.0  -2543.0            兴业期货   
     16  zn1902    17           信达期货    7018.0   5531.0            国投安信   
     17  zn1902    18           鲁证期货    6930.0  -3700.0            东亚期货   
     18  zn1902    19           兴证期货    6553.0    462.0            东方财富   
     19  zn1902    20           广发期货    6481.0   2888.0            中钢期货   
     20  zn1902   999           None  345499.0  48608.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               8003.0                    24.0             永安期货   
     1               7372.0                  1018.0             中信期货   
     2               6374.0                   -29.0             国泰君安   
     3               5022.0                   503.0             五矿经易   
     4               4102.0                   -16.0             南华期货   
     5               4035.0                   902.0             华泰期货   
     6               3745.0                    -2.0             东证期货   
     7               3226.0                     3.0             申万期货   
     8               3144.0                    26.0             国投安信   
     9               3081.0                  -598.0             海通期货   
     10              2735.0                  -656.0             招商期货   
     11              2656.0                     5.0             银河期货   
     12              2630.0                   986.0             格林大华   
     13              2605.0                   483.0             首创期货   
     14              2287.0                    80.0             迈科期货   
     15              2281.0                    36.0             上海中期   
     16              2243.0                   -77.0             中粮期货   
     17              2241.0                    70.0             中国国际   
     18              2152.0                   229.0             鲁证期货   
     19              2109.0                     3.0             铜冠金源   
     20             72043.0                  2990.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               13192.0                   1712.0      ZN  
     1                5704.0                    406.0      ZN  
     2                3964.0                    559.0      ZN  
     3                3888.0                   -111.0      ZN  
     4                3759.0                    707.0      ZN  
     5                3681.0                   -201.0      ZN  
     6                3244.0                    102.0      ZN  
     7                2674.0                   -729.0      ZN  
     8                2599.0                    437.0      ZN  
     9                2590.0                    106.0      ZN  
     10               2498.0                     31.0      ZN  
     11               2478.0                   -110.0      ZN  
     12               2048.0                     -6.0      ZN  
     13               2033.0                   -182.0      ZN  
     14               1872.0                    -22.0      ZN  
     15               1694.0                    -36.0      ZN  
     16               1673.0                   -404.0      ZN  
     17               1671.0                   -147.0      ZN  
     18               1633.0                  -1284.0      ZN  
     19               1629.0                   -207.0      ZN  
     20              64524.0                    621.0      ZN  ,
     'zn1904':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   zn1904     1           中信期货   1512.0    218.0            中信期货   
     1   zn1904     2           海通期货   1469.0   -304.0            瑞达期货   
     2   zn1904     3           国投安信   1268.0   -619.0            东方财富   
     3   zn1904     4           华泰期货   1203.0   -721.0            永安期货   
     4   zn1904     5           东证期货   1161.0    328.0            首创期货   
     5   zn1904     6           西部期货    680.0   -468.0            银河期货   
     6   zn1904     7           东方财富    582.0    -46.0            建信期货   
     7   zn1904     8           方正中期    570.0   -770.0            五矿经易   
     8   zn1904     9           国泰君安    559.0    236.0            格林大华   
     9   zn1904    10           银河期货    517.0   -670.0            金瑞期货   
     10  zn1904    11           中融汇信    441.0     70.0            国泰君安   
     11  zn1904    12           鲁证期货    379.0   -113.0            东兴期货   
     12  zn1904    13           国富期货    301.0    122.0            一德期货   
     13  zn1904    14           华西期货    272.0    141.0            兴证期货   
     14  zn1904    15           五矿经易    197.0   -389.0            华金期货   
     15  zn1904    16           上海中期    191.0    186.0            国富期货   
     16  zn1904    17           宏源期货    173.0    120.0            招金期货   
     17  zn1904    18           兴证期货    144.0    -84.0            中粮期货   
     18  zn1904    19           中银国际    134.0    -88.0            华泰期货   
     19  zn1904    20           一德期货    113.0    108.0            国投安信   
     20  zn1904   999           None  11866.0  -2743.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               2561.0                    84.0             瑞达期货   
     1               2140.0                     0.0             国贸期货   
     2               1724.0                  -108.0             五矿经易   
     3               1482.0                     4.0             方正中期   
     4               1139.0                    10.0             东方财富   
     5               1077.0                     0.0             中钢期货   
     6                931.0                     0.0             中粮期货   
     7                762.0                    26.0             银河期货   
     8                705.0                     0.0             中信建投   
     9                592.0                    -6.0             南华期货   
     10               452.0                     2.0             华泰期货   
     11               400.0                     0.0             兴业期货   
     12               282.0                     1.0             招金期货   
     13               232.0                    43.0             国海良时   
     14               142.0                     0.0             浙商期货   
     15               134.0                   -12.0             东证期货   
     16               121.0                    -3.0             江海汇鑫   
     17               108.0                     2.0             中信期货   
     18                99.0                   -19.0             海证期货   
     19                82.0                   -24.0             鲁证期货   
     20             15165.0                     0.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                2000.0                      0.0      ZN  
     1                1657.0                     37.0      ZN  
     2                1524.0                     95.0      ZN  
     3                1420.0                    -48.0      ZN  
     4                1369.0                     74.0      ZN  
     5                1354.0                      3.0      ZN  
     6                1000.0                      0.0      ZN  
     7                 968.0                     87.0      ZN  
     8                 379.0                    -50.0      ZN  
     9                 290.0                     -3.0      ZN  
     10                281.0                     64.0      ZN  
     11                258.0                      0.0      ZN  
     12                243.0                      0.0      ZN  
     13                224.0                      8.0      ZN  
     14                224.0                     -1.0      ZN  
     15                159.0                    -17.0      ZN  
     16                155.0                      0.0      ZN  
     17                149.0                      8.0      ZN  
     18                125.0                      4.0      ZN  
     19                125.0                    117.0      ZN  
     20              13904.0                    378.0      ZN  ,
     'zn1903':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   zn1903     1           中信期货   6286.0  -1947.0            五矿经易   
     1   zn1903     2           华泰期货   5897.0  -3741.0            中信期货   
     2   zn1903     3           东证期货   4334.0    486.0            瑞达期货   
     3   zn1903     4           方正中期   3827.0    638.0            方正中期   
     4   zn1903     5           国投安信   3437.0  -1374.0            海通期货   
     5   zn1903     6           海通期货   3413.0   -302.0            东方财富   
     6   zn1903     7           鲁证期货   2794.0  -1219.0            国贸期货   
     7   zn1903     8           银河期货   2686.0    -96.0            建信期货   
     8   zn1903     9           中融汇信   1813.0   -966.0            银河期货   
     9   zn1903    10           西部期货   1674.0  -1083.0            鲁证期货   
     10  zn1903    11           国泰君安   1415.0   -401.0            招商期货   
     11  zn1903    12           中辉期货   1115.0      6.0            光大期货   
     12  zn1903    13           天鸿期货   1059.0   -686.0            东亚期货   
     13  zn1903    14           中银国际    998.0   -348.0            广发期货   
     14  zn1903    15           国信期货    978.0    402.0            首创期货   
     15  zn1903    16           瑞达期货    908.0    730.0            迈科期货   
     16  zn1903    17           上海中期    851.0  -1448.0            华泰期货   
     17  zn1903    18           永安期货    838.0    227.0            中信建投   
     18  zn1903    19           东方财富    830.0   -571.0            永安期货   
     19  zn1903    20           安粮期货    632.0    261.0            云晨期货   
     20  zn1903   999           None  45785.0 -11432.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               5210.0                    76.0             永安期货   
     1               4867.0                   531.0             天鸿期货   
     2               4623.0                   866.0             东方财富   
     3               3297.0                  1524.0             海通期货   
     4               2640.0                   -30.0             中信期货   
     5               2582.0                   -39.0             上海中期   
     6               2373.0                    48.0             华泰期货   
     7               2066.0                    -1.0             方正中期   
     8               1740.0                   283.0             五矿经易   
     9               1713.0                  -459.0             中粮期货   
     10              1558.0                    -3.0             中金期货   
     11              1536.0                    -2.0             国泰君安   
     12              1455.0                   350.0             中国国际   
     13              1418.0                  -376.0             格林大华   
     14              1239.0                  -110.0             宏源期货   
     15               902.0                    -2.0             国贸期货   
     16               746.0                  -165.0             银河期货   
     17               602.0                    10.0             大地期货   
     18               590.0                    -8.0             国富期货   
     19               521.0                     5.0             国投安信   
     20             41678.0                  2498.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                4493.0                    176.0      ZN  
     1                4015.0                   1059.0      ZN  
     2                3813.0                    -43.0      ZN  
     3                3338.0                    -21.0      ZN  
     4                2041.0                     23.0      ZN  
     5                1643.0                     34.0      ZN  
     6                1576.0                   -272.0      ZN  
     7                1527.0                    -33.0      ZN  
     8                1507.0                    112.0      ZN  
     9                1354.0                    187.0      ZN  
     10               1240.0                    -46.0      ZN  
     11               1073.0                    152.0      ZN  
     12                930.0                     10.0      ZN  
     13                896.0                     -2.0      ZN  
     14                794.0                    227.0      ZN  
     15                775.0                     -4.0      ZN  
     16                757.0                    223.0      ZN  
     17                754.0                     65.0      ZN  
     18                706.0                    -79.0      ZN  
     19                557.0                    -53.0      ZN  
     20              33789.0                   1715.0      ZN  ,
     'pb1901':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   pb1901     1           海通期货   5223.0    260.0            永安期货   
     1   pb1901     2           兴证期货   2372.0   -305.0            中信期货   
     2   pb1901     3           国投安信   1888.0   -332.0            海通期货   
     3   pb1901     4           方正中期   1262.0   -309.0            金瑞期货   
     4   pb1901     5           大有期货   1254.0    163.0            国投安信   
     5   pb1901     6           东证期货   1218.0    -97.0            银河期货   
     6   pb1901     7           中信期货   1209.0  -1513.0            首创期货   
     7   pb1901     8           华泰期货   1037.0   -130.0            华泰期货   
     8   pb1901     9           铜冠金源    950.0      6.0            五矿经易   
     9   pb1901    10           南华期货    701.0    -70.0            兴证期货   
     10  pb1901    11           五矿经易    594.0    177.0            东航期货   
     11  pb1901    12           中银国际    579.0    -93.0            申万期货   
     12  pb1901    13           银河期货    565.0   -567.0            南华期货   
     13  pb1901    14           华安期货    539.0    232.0            广州期货   
     14  pb1901    15           国泰君安    515.0    -42.0            东证期货   
     15  pb1901    16           中信建投    451.0    -38.0            光大期货   
     16  pb1901    17           中财期货    450.0    357.0            方正中期   
     17  pb1901    18           永安期货    449.0   -173.0            中金期货   
     18  pb1901    19           广金期货    393.0     47.0            国海良时   
     19  pb1901    20           西部期货    374.0    -28.0            国泰君安   
     20  pb1901   999           None  22023.0  -2455.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               4199.0                    33.0             国泰君安   
     1               2589.0                   -99.0             铜冠金源   
     2               1217.0                    51.0             海通期货   
     3               1208.0                    -6.0             建信期货   
     4               1155.0                    -2.0             中辉期货   
     5                988.0                   -45.0             五矿经易   
     6                980.0                   -45.0             中信期货   
     7                905.0                    -1.0             银河期货   
     8                867.0                   -13.0             方正中期   
     9                865.0                   -98.0             格林大华   
     10               832.0                   -34.0             金瑞期货   
     11               685.0                   -22.0             国投安信   
     12               643.0                  -130.0             兴证期货   
     13               603.0                    -1.0             首创期货   
     14               495.0                   -89.0             东证期货   
     15               453.0                   -16.0             中银国际   
     16               429.0                    44.0             中粮期货   
     17               363.0                     8.0             弘业期货   
     18               354.0                    15.0             广发期货   
     19               325.0                   -27.0             广金期货   
     20             20155.0                  -477.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                3177.0                     -2.0      PB  
     1                1921.0                    283.0      PB  
     2                1705.0                   -150.0      PB  
     3                1613.0                      7.0      PB  
     4                1435.0                    -34.0      PB  
     5                1346.0                    151.0      PB  
     6                1333.0                    -62.0      PB  
     7                1319.0                   -138.0      PB  
     8                1297.0                   -110.0      PB  
     9                1187.0                    -23.0      PB  
     10                748.0                   -140.0      PB  
     11                736.0                     56.0      PB  
     12                725.0                     20.0      PB  
     13                504.0                     97.0      PB  
     14                471.0                     -3.0      PB  
     15                430.0                     27.0      PB  
     16                423.0                    -25.0      PB  
     17                411.0                    -22.0      PB  
     18                357.0                    -98.0      PB  
     19                341.0                    315.0      PB  
     20              21479.0                    149.0      PB  ,
     'pb1902':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   pb1902     1           海通期货  1627.0   -549.0            兴证期货   
     1   pb1902     2           中信期货  1588.0  -1237.0            永安期货   
     2   pb1902     3           国泰君安   703.0   -145.0            申万期货   
     3   pb1902     4           西南期货   661.0    -83.0            五矿经易   
     4   pb1902     5           国投安信   642.0   -166.0            中信期货   
     5   pb1902     6           申万期货   515.0    188.0            西南期货   
     6   pb1902     7           东证期货   455.0     -8.0            方正中期   
     7   pb1902     8           五矿经易   390.0    -47.0            国泰君安   
     8   pb1902     9           华泰期货   380.0   -220.0            一德期货   
     9   pb1902    10           国信期货   374.0   -294.0            中信建投   
     10  pb1902    11           中银国际   340.0   -195.0            金瑞期货   
     11  pb1902    12           银河期货   286.0     -1.0            东证期货   
     12  pb1902    13           西部期货   247.0    -95.0            国投安信   
     13  pb1902    14           方正中期   245.0   -443.0            银河期货   
     14  pb1902    15           上海中期   242.0   -139.0            华西期货   
     15  pb1902    16           永安期货   232.0   -290.0            国联期货   
     16  pb1902    17           弘业期货   230.0   -104.0            建信期货   
     17  pb1902    18           长江期货   226.0    -66.0            海通期货   
     18  pb1902    19           徽商期货   214.0    -68.0            国元期货   
     19  pb1902    20            美尔雅   192.0      0.0            盛达期货   
     20  pb1902   999           None  9789.0  -3962.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               2249.0                    18.0             中信期货   
     1               1440.0                    26.0             上海中期   
     2               1385.0                  -189.0             银河期货   
     3               1212.0                   138.0             迈科期货   
     4                768.0                   126.0             中银国际   
     5                615.0                   153.0             金瑞期货   
     6                528.0                    -1.0             方正中期   
     7                466.0                    37.0             中粮期货   
     8                418.0                    36.0             国泰君安   
     9                400.0                     1.0             首创期货   
     10               391.0                   -90.0             国投安信   
     11               285.0                    83.0             鲁证期货   
     12               277.0                    47.0             国贸期货   
     13               275.0                   115.0             申万期货   
     14               234.0                    27.0             永安期货   
     15               201.0                     6.0             中国国际   
     16               195.0                   -44.0             华泰期货   
     17               193.0                     7.0              美尔雅   
     18               181.0                     1.0             瑞达期货   
     19               160.0                     0.0             国富期货   
     20             11873.0                   497.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                3790.0                     90.0      PB  
     1                1599.0                    -21.0      PB  
     2                1550.0                    135.0      PB  
     3                1053.0                     -1.0      PB  
     4                 936.0                     20.0      PB  
     5                 796.0                      5.0      PB  
     6                 531.0                      0.0      PB  
     7                 452.0                     -2.0      PB  
     8                 387.0                    -14.0      PB  
     9                 336.0                      0.0      PB  
     10                309.0                     -7.0      PB  
     11                297.0                      3.0      PB  
     12                242.0                     17.0      PB  
     13                213.0                     42.0      PB  
     14                199.0                     80.0      PB  
     15                181.0                    -82.0      PB  
     16                159.0                    -29.0      PB  
     17                134.0                    -13.0      PB  
     18                125.0                    119.0      PB  
     19                121.0                    116.0      PB  
     20              13410.0                    458.0      PB  ,
     'pb1812':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   pb1812     1           方正中期   360.0    225.0            中信期货   
     1   pb1812     2           招商期货   250.0    250.0            上海中期   
     2   pb1812     3           五矿经易   245.0     60.0            海通期货   
     3   pb1812     4           海通期货   185.0     15.0            华泰期货   
     4   pb1812     5           上海中期   170.0    100.0            方正中期   
     5   pb1812     6           中信期货   155.0    -10.0            建信期货   
     6   pb1812     7           广发期货   135.0    135.0            瑞达期货   
     7   pb1812     8           金瑞期货   100.0     85.0            中辉期货   
     8   pb1812     9           国泰君安    90.0   -100.0            英大期货   
     9   pb1812    10           兴证期货    80.0     55.0            中粮期货   
     10  pb1812    11           国贸期货    60.0     20.0            山金期货   
     11  pb1812    12           中财期货    60.0     60.0            首创期货   
     12  pb1812    13           华泰期货    60.0   -410.0            南华期货   
     13  pb1812    14           国富期货    40.0    -35.0            None   
     14  pb1812    15           光大期货    35.0    -20.0            None   
     15  pb1812    16           一德期货    30.0    -55.0            None   
     16  pb1812    17            美尔雅    30.0     30.0            None   
     17  pb1812    18           中银国际    30.0     20.0            None   
     18  pb1812    19           中辉期货    25.0   -110.0            None   
     19  pb1812    20           申万期货    20.0    -65.0            None   
     20  pb1812   999           None  2160.0    250.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               1600.0                  -155.0             铜冠金源   
     1               1380.0                   -35.0             中辉期货   
     2               1065.0                  -185.0             五矿经易   
     3                410.0                   -60.0             上海中期   
     4                390.0                   330.0             格林大华   
     5                270.0                     0.0             中大期货   
     6                230.0                     0.0             方正中期   
     7                 45.0                     0.0             国投安信   
     8                 30.0                     0.0             中国国际   
     9                 20.0                     0.0             东证期货   
     10                15.0                     0.0             广发期货   
     11                10.0                     0.0             鲁证期货   
     12                 5.0                     0.0             一德期货   
     13                 NaN                     NaN             南华期货   
     14                 NaN                     NaN             创元期货   
     15                 NaN                     NaN             广金期货   
     16                 NaN                     NaN             宏源期货   
     17                 NaN                     NaN             兴证期货   
     18                 NaN                     NaN             东兴期货   
     19                 NaN                     NaN             华泰期货   
     20              5470.0                  -105.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                1200.0                      0.0      PB  
     1                 760.0                     25.0      PB  
     2                 515.0                   -245.0      PB  
     3                 300.0                    135.0      PB  
     4                 300.0                      0.0      PB  
     5                 300.0                      0.0      PB  
     6                 220.0                    -30.0      PB  
     7                 220.0                      0.0      PB  
     8                 160.0                      0.0      PB  
     9                 160.0                      0.0      PB  
     10                135.0                    135.0      PB  
     11                110.0                      0.0      PB  
     12                110.0                     10.0      PB  
     13                105.0                     10.0      PB  
     14                100.0                      0.0      PB  
     15                100.0                      0.0      PB  
     16                 95.0                      5.0      PB  
     17                 85.0                     80.0      PB  
     18                 75.0                     15.0      PB  
     19                 60.0                      0.0      PB  
     20               5110.0                    140.0      PB  ,
     'ni1905':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   ni1905     1           华泰期货   37506.0   -789.0            五矿经易   
     1   ni1905     2           东证期货   19824.0   3741.0            中信期货   
     2   ni1905     3           中信期货   16594.0   1934.0            瑞达期货   
     3   ni1905     4           海通期货   14404.0   2424.0            广发期货   
     4   ni1905     5           方正中期    7094.0   -593.0            国贸期货   
     5   ni1905     6           国泰君安    6967.0    547.0            方正中期   
     6   ni1905     7           华安期货    6777.0   1016.0            永安期货   
     7   ni1905     8           广发期货    6477.0   3494.0            国泰君安   
     8   ni1905     9           徽商期货    6351.0  -1273.0            申万期货   
     9   ni1905    10           银河期货    6207.0    416.0            银河期货   
     10  ni1905    11           国信期货    6200.0   2251.0            南华期货   
     11  ni1905    12           中银国际    5503.0   1658.0            海通期货   
     12  ni1905    13           国投安信    4961.0  -1882.0            铜冠金源   
     13  ni1905    14           上海中期    4960.0   1430.0            英大期货   
     14  ni1905    15           中融汇信    4722.0   -322.0            华泰期货   
     15  ni1905    16           混沌天成    4718.0  -1001.0            鲁证期货   
     16  ni1905    17           永安期货    4651.0  -2270.0            东兴期货   
     17  ni1905    18           金瑞期货    4559.0   2972.0            中国国际   
     18  ni1905    19           申万期货    4460.0   1685.0            国投安信   
     19  ni1905    20           鲁证期货    4402.0   -479.0            中银国际   
     20  ni1905   999           None  177337.0  14959.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               8152.0                    21.0             永安期货   
     1               7208.0                    41.0             中信期货   
     2               6225.0                   637.0             银河期货   
     3               5917.0                   121.0             中金期货   
     4               5649.0                    54.0             华泰期货   
     5               5607.0                   659.0             海通期货   
     6               4190.0                  -101.0             瑞达期货   
     7               3572.0                    54.0             国泰君安   
     8               3345.0                   122.0             中粮期货   
     9               3288.0                  -348.0             申万期货   
     10              2952.0                   330.0             广发期货   
     11              2773.0                   597.0             方正中期   
     12              2553.0                  1073.0             鲁证期货   
     13              2552.0                    13.0             金瑞期货   
     14              2431.0                  1327.0             五矿经易   
     15              2395.0                   -29.0             国贸期货   
     16              2301.0                    15.0             华信期货   
     17              2202.0                   -48.0             招商期货   
     18              1950.0                    49.0             兴证期货   
     19              1867.0                    48.0             东方财富   
     20             77129.0                  4635.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               12094.0                   1032.0      NI  
     1                9138.0                   1475.0      NI  
     2                5685.0                     33.0      NI  
     3                5303.0                     87.0      NI  
     4                5285.0                    641.0      NI  
     5                5255.0                    551.0      NI  
     6                5171.0                    151.0      NI  
     7                5079.0                   1091.0      NI  
     8                4876.0                     30.0      NI  
     9                4723.0                   -198.0      NI  
     10               4629.0                    786.0      NI  
     11               4212.0                   -177.0      NI  
     12               4055.0                    391.0      NI  
     13               3557.0                     44.0      NI  
     14               3431.0                   -143.0      NI  
     15               3390.0                    -52.0      NI  
     16               2250.0                    -66.0      NI  
     17               2219.0                    122.0      NI  
     18               2186.0                    708.0      NI  
     19               2069.0                    -51.0      NI  
     20              94607.0                   6455.0      NI  ,
     'ni1812':    symbol  rank vol_party_name   vol  vol_chg long_party_name  \
     0  ni1812     1           国泰君安   6.0      6.0            一德期货   
     1  ni1812     2           一德期货   6.0      6.0            国泰君安   
     2  ni1812     3           None   NaN      NaN            光大期货   
     3  ni1812     4           None   NaN      NaN            大有期货   
     4  ni1812   999           None  12.0     12.0            None   
     
        long_open_interest  long_open_interest_chg short_party_name  \
     0                42.0                    -6.0             中财期货   
     1                24.0                     6.0             一德期货   
     2                24.0                     0.0             首创期货   
     3                 6.0                     0.0             None   
     4                96.0                     0.0             None   
     
        short_open_interest  short_open_interest_chg variety  
     0                 60.0                      0.0      NI  
     1                 30.0                      0.0      NI  
     2                  6.0                      0.0      NI  
     3                  NaN                      NaN      NI  
     4                 96.0                      0.0      NI  ,
     'ni1901':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   ni1901     1           华泰期货   28535.0 -10459.0            广发期货   
     1   ni1901     2           中信期货   21389.0   -900.0            中信期货   
     2   ni1901     3           海通期货   18514.0  -8432.0            中国国际   
     3   ni1901     4           东证期货   11906.0  -4283.0            永安期货   
     4   ni1901     5           方正中期    9428.0  -3780.0            国泰君安   
     5   ni1901     6           国投安信    8003.0  -2710.0            银河期货   
     6   ni1901     7           国泰君安    6948.0  -1962.0            华泰期货   
     7   ni1901     8           兴证期货    6543.0  -3371.0            招商期货   
     8   ni1901     9           中融汇信    6438.0  -1948.0            中大期货   
     9   ni1901    10           华安期货    5075.0  -2125.0            大有期货   
     10  ni1901    11           申万期货    4902.0  -1128.0            南华期货   
     11  ni1901    12           永安期货    4759.0   -951.0            方正中期   
     12  ni1901    13           光大期货    4676.0  -1511.0            申万期货   
     13  ni1901    14           徽商期货    4466.0  -3054.0            国信期货   
     14  ni1901    15           银河期货    4455.0  -2738.0            浙商期货   
     15  ni1901    16           鲁证期货    4423.0    -63.0            海通期货   
     16  ni1901    17           广发期货    4154.0  -3199.0            国都期货   
     17  ni1901    18           东航期货    3777.0  -1036.0            一德期货   
     18  ni1901    19           中信建投    3750.0  -1475.0            兴业期货   
     19  ni1901    20           南华期货    3049.0   -733.0            铜冠金源   
     20  ni1901   999           None  165190.0 -55858.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               4951.0                  -336.0             永安期货   
     1               4730.0                  -339.0             中信期货   
     2               3958.0                  -130.0             中银国际   
     3               3275.0                   -42.0             海通期货   
     4               2668.0                  -391.0             广发期货   
     5               2244.0                  -126.0             国投安信   
     6               2000.0                  -885.0             华安期货   
     7               1905.0                   -56.0             国泰君安   
     8               1884.0                  -216.0             渤海期货   
     9               1803.0                   -18.0             兴证期货   
     10              1697.0                    89.0             金瑞期货   
     11              1629.0                  -645.0             华泰期货   
     12              1560.0                  -247.0             东证期货   
     13              1487.0                   -15.0             上海中期   
     14              1468.0                   -99.0             申万期货   
     15              1361.0                   -37.0             银河期货   
     16              1236.0                     5.0             中粮期货   
     17              1231.0                    -9.0             鲁证期货   
     18               930.0                   -40.0             方正中期   
     19               921.0                  -720.0             五矿经易   
     20             42938.0                 -4257.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                7142.0                  -1387.0      NI  
     1                7077.0                  -1352.0      NI  
     2                6191.0                     -4.0      NI  
     3                4103.0                  -1641.0      NI  
     4                3117.0                   -104.0      NI  
     5                3060.0                   -339.0      NI  
     6                2668.0                    -75.0      NI  
     7                2396.0                  -1011.0      NI  
     8                2334.0                     96.0      NI  
     9                1857.0                  -2028.0      NI  
     10               1835.0                    212.0      NI  
     11               1788.0                   -290.0      NI  
     12               1751.0                    349.0      NI  
     13               1527.0                   -160.0      NI  
     14               1419.0                    -15.0      NI  
     15               1265.0                    131.0      NI  
     16               1263.0                    308.0      NI  
     17               1187.0                   -128.0      NI  
     18               1094.0                     37.0      NI  
     19               1082.0                    -75.0      NI  
     20              54156.0                  -7476.0      NI  ,
     'ni1903':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   ni1903     1           中信期货   7850.0  -4092.0            中信期货   
     1   ni1903     2           东证期货   5360.0   -951.0            国泰君安   
     2   ni1903     3           海通期货   5208.0  -1803.0            广发期货   
     3   ni1903     4           华泰期货   3596.0  -1543.0            五矿经易   
     4   ni1903     5           方正中期   3431.0    114.0            鲁证期货   
     5   ni1903     6           国投安信   3290.0  -2191.0            瑞达期货   
     6   ni1903     7           五矿经易   2778.0  -1070.0            南华期货   
     7   ni1903     8           创元期货   2403.0    354.0            浙商期货   
     8   ni1903     9           中粮期货   2291.0    209.0            中粮期货   
     9   ni1903    10           鲁证期货   2259.0  -1013.0            东证期货   
     10  ni1903    11           中银国际   2028.0    532.0            海通期货   
     11  ni1903    12           国泰君安   1678.0  -2435.0            银河期货   
     12  ni1903    13           南华期货   1670.0   -561.0            国投安信   
     13  ni1903    14           中融汇信   1627.0   -254.0            招商期货   
     14  ni1903    15            美尔雅   1526.0    847.0            华泰期货   
     15  ni1903    16           银河期货   1341.0   -544.0            中国国际   
     16  ni1903    17           西部期货   1273.0   -273.0            兴证期货   
     17  ni1903    18           广发期货   1261.0   -701.0            中银国际   
     18  ni1903    19           华安期货   1150.0   -124.0            创元期货   
     19  ni1903    20           兴业期货    927.0    611.0            兴业期货   
     20  ni1903   999           None  52947.0 -14888.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               7896.0                    68.0             中信期货   
     1               4162.0                  -110.0             五矿经易   
     2               3661.0                   832.0             海通期货   
     3               3555.0                   -88.0             国泰君安   
     4               3218.0                   388.0             大地期货   
     5               1971.0                     3.0             华泰期货   
     6               1705.0                    20.0             永安期货   
     7               1697.0                   120.0             南华期货   
     8               1620.0                   287.0             瑞达期货   
     9               1457.0                   -93.0             方正中期   
     10              1240.0                   158.0             浙商期货   
     11              1224.0                    15.0             中粮期货   
     12              1000.0                    -1.0             国投安信   
     13               946.0                   102.0             东兴期货   
     14               896.0                   286.0             兴证期货   
     15               830.0                   174.0             东证期货   
     16               824.0                   -10.0             格林大华   
     17               692.0                   -26.0             招商期货   
     18               625.0                    22.0             银河期货   
     19               622.0                  -866.0             信达期货   
     20             39841.0                  1281.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                7657.0                    246.0      NI  
     1                4875.0                     -6.0      NI  
     2                4719.0                    -40.0      NI  
     3                4477.0                   -194.0      NI  
     4                3151.0                   -141.0      NI  
     5                2394.0                      4.0      NI  
     6                2106.0                      0.0      NI  
     7                1878.0                     44.0      NI  
     8                1692.0                      1.0      NI  
     9                1654.0                    -93.0      NI  
     10               1639.0                    123.0      NI  
     11               1477.0                      4.0      NI  
     12               1008.0                     25.0      NI  
     13               1000.0                      0.0      NI  
     14                998.0                     -9.0      NI  
     15                940.0                     67.0      NI  
     16                817.0                     -5.0      NI  
     17                806.0                    102.0      NI  
     18                797.0                     96.0      NI  
     19                757.0                    563.0      NI  
     20              44842.0                    787.0      NI  ,
     'sn1905':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   sn1905     1           中信期货   680.0   -252.0            中信期货   
     1   sn1905     2           国信期货   659.0    116.0            金瑞期货   
     2   sn1905     3           国泰君安   464.0   -170.0            上海中期   
     3   sn1905     4           华泰期货   430.0   -108.0            中国国际   
     4   sn1905     5           海通期货   406.0   -712.0            国泰君安   
     5   sn1905     6           东证期货   386.0     -1.0            英大期货   
     6   sn1905     7           金瑞期货   320.0    -57.0            东证期货   
     7   sn1905     8           中银国际   271.0    199.0            广州期货   
     8   sn1905     9           方正中期   237.0   -118.0            云晨期货   
     9   sn1905    10           西部期货   227.0    -47.0            国信期货   
     10  sn1905    11           国富期货   172.0    -49.0            弘业期货   
     11  sn1905    12           瑞达期货   143.0     14.0            大有期货   
     12  sn1905    13           中辉期货   141.0    -93.0            瑞达期货   
     13  sn1905    14           五矿经易   129.0    -11.0            南华期货   
     14  sn1905    15           广发期货   129.0     57.0            海航期货   
     15  sn1905    16           国投安信   120.0     59.0            广发期货   
     16  sn1905    17           徽商期货   116.0     -3.0            德盛期货   
     17  sn1905    18           永安期货   115.0   -129.0            浙商期货   
     18  sn1905    19           东吴期货   115.0    112.0            混沌天成   
     19  sn1905    20           申万期货   110.0    -39.0            东海期货   
     20  sn1905   999           None  5370.0  -1232.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               3959.0                    58.0             首创期货   
     1               2538.0                   212.0             中信期货   
     2               1462.0                    -2.0             格林大华   
     3                911.0                    -4.0             五矿经易   
     4                855.0                   147.0             东证期货   
     5                500.0                    -8.0             华泰期货   
     6                420.0                   150.0             一德期货   
     7                404.0                    60.0             申万期货   
     8                177.0                     0.0             永安期货   
     9                172.0                    38.0             海通期货   
     10               156.0                     3.0             中银国际   
     11               149.0                     0.0             中粮期货   
     12               130.0                    48.0              美尔雅   
     13                96.0                    34.0             中投期货   
     14                92.0                     0.0             国泰君安   
     15                81.0                    33.0             广发期货   
     16                61.0                     0.0             鲁证期货   
     17                56.0                     0.0             兴证期货   
     18                55.0                    -2.0             东航期货   
     19                48.0                     3.0             方正中期   
     20             12322.0                   770.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                2063.0                      3.0      SN  
     1                1631.0                     86.0      SN  
     2                 917.0                      3.0      SN  
     3                 894.0                     34.0      SN  
     4                 544.0                     16.0      SN  
     5                 472.0                     45.0      SN  
     6                 365.0                     -7.0      SN  
     7                 346.0                      9.0      SN  
     8                 333.0                     42.0      SN  
     9                 290.0                     26.0      SN  
     10                278.0                    153.0      SN  
     11                271.0                     -6.0      SN  
     12                258.0                    -13.0      SN  
     13                258.0                    -82.0      SN  
     14                249.0                     29.0      SN  
     15                214.0                     -6.0      SN  
     16                182.0                      3.0      SN  
     17                170.0                     71.0      SN  
     18                167.0                      8.0      SN  
     19                164.0                     18.0      SN  
     20              10066.0                    432.0      SN  ,
     'sn1901':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   sn1901     1           海通期货  1917.0   -215.0            首创期货   
     1   sn1901     2           方正中期   773.0    127.0            金瑞期货   
     2   sn1901     3           华泰期货   738.0   -136.0            一德期货   
     3   sn1901     4           中信期货   672.0   -118.0            东证期货   
     4   sn1901     5           东证期货   403.0    -13.0            南华期货   
     5   sn1901     6           金瑞期货   378.0    -24.0            五矿经易   
     6   sn1901     7           中辉期货   314.0    -33.0            中粮期货   
     7   sn1901     8           东吴期货   268.0    188.0            云晨期货   
     8   sn1901     9           国泰君安   257.0   -183.0            光大期货   
     9   sn1901    10           瑞达期货   231.0      8.0            大有期货   
     10  sn1901    11           宏源期货   200.0   -196.0            国泰君安   
     11  sn1901    12           南华期货   196.0     -9.0            国投安信   
     12  sn1901    13           国信期货   181.0   -104.0            海通期货   
     13  sn1901    14           银河期货   179.0    -28.0            招金期货   
     14  sn1901    15           兴证期货   154.0    -64.0            国贸期货   
     15  sn1901    16           申万期货   147.0     -2.0            中信期货   
     16  sn1901    17            美尔雅   141.0     56.0            永安期货   
     17  sn1901    18           华安期货   133.0      7.0            弘业期货   
     18  sn1901    19           光大期货   118.0   -124.0            银河期货   
     19  sn1901    20           西部期货   117.0    -49.0            瑞达期货   
     20  sn1901   999           None  7517.0   -912.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               1467.0                     0.0             格林大华   
     1               1258.0                   -84.0             中信期货   
     2                655.0                    16.0             海通期货   
     3                633.0                   -32.0             五矿经易   
     4                468.0                    -2.0             兴证期货   
     5                462.0                     0.0             银河期货   
     6                283.0                     3.0             上海中期   
     7                254.0                    -2.0             国贸期货   
     8                218.0                     0.0             光大期货   
     9                202.0                    -5.0             一德期货   
     10               201.0                  -121.0             华泰期货   
     11               191.0                     1.0             大地期货   
     12               160.0                    -9.0             方正中期   
     13               158.0                   -17.0             广发期货   
     14               150.0                     0.0             宏源期货   
     15               140.0                   -34.0             建信期货   
     16               138.0                    -6.0             中辉期货   
     17               133.0                    -5.0             国泰君安   
     18               116.0                   -24.0             兴业期货   
     19                94.0                    -5.0             浙商期货   
     20              7381.0                  -326.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                1917.0                     -1.0      SN  
     1                 966.0                    -38.0      SN  
     2                 889.0                   -144.0      SN  
     3                 647.0                     15.0      SN  
     4                 412.0                    -43.0      SN  
     5                 353.0                      5.0      SN  
     6                 302.0                      1.0      SN  
     7                 198.0                      6.0      SN  
     8                 197.0                     20.0      SN  
     9                 174.0                    -12.0      SN  
     10                152.0                    -21.0      SN  
     11                144.0                     -1.0      SN  
     12                135.0                     27.0      SN  
     13                127.0                     -5.0      SN  
     14                124.0                      1.0      SN  
     15                117.0                    -15.0      SN  
     16                113.0                      0.0      SN  
     17                111.0                    -32.0      SN  
     18                105.0                     -2.0      SN  
     19                 87.0                      8.0      SN  
     20               7270.0                   -231.0      SN  ,
     'sn1812':    symbol  rank vol_party_name  vol  vol_chg long_party_name  \
     0  sn1812     1           None  NaN      NaN            一德期货   
     1  sn1812   999           None  NaN      NaN            None   
     
        long_open_interest  long_open_interest_chg short_party_name  \
     0                24.0                     0.0             一德期货   
     1                24.0                     0.0             None   
     
        short_open_interest  short_open_interest_chg variety  
     0                 24.0                      0.0      SN  
     1                 24.0                      0.0      SN  ,
     'au1906':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   au1906     1           海通期货   40727.0   7214.0            国泰君安   
     1   au1906     2           国投安信   14663.0   3434.0            中金期货   
     2   au1906     3           中银国际    9683.0   2850.0            银河期货   
     3   au1906     4           国泰君安    9584.0   1984.0            海通期货   
     4   au1906     5           中信期货    9171.0   1864.0            永安期货   
     5   au1906     6           上海中期    9084.0   2685.0            中信期货   
     6   au1906     7           平安期货    8590.0   1176.0            五矿经易   
     7   au1906     8           东证期货    7618.0   2873.0            宏源期货   
     8   au1906     9           西部期货    6772.0   4190.0            中衍期货   
     9   au1906    10           华泰期货    5575.0   1698.0            中信建投   
     10  au1906    11           华安期货    5454.0   1269.0            华泰期货   
     11  au1906    12           东方财富    5048.0   4584.0            徽商期货   
     12  au1906    13           徽商期货    4736.0   2737.0            东证期货   
     13  au1906    14           建信期货    4651.0   3219.0            建信期货   
     14  au1906    15           光大期货    4180.0    920.0            上海大陆   
     15  au1906    16           国信期货    3751.0   -218.0            平安期货   
     16  au1906    17           兴证期货    3691.0  -1942.0            南华期货   
     17  au1906    18           方正中期    3609.0   1826.0            兴证期货   
     18  au1906    19           广发期货    3190.0   1085.0            鲁证期货   
     19  au1906    20           中信建投    3089.0   1613.0            方正中期   
     20  au1906   999           None  162866.0  45061.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0              13377.0                   948.0             平安期货   
     1               5227.0                   536.0             招金期货   
     2               4697.0                   214.0             中信期货   
     3               4554.0                 -1452.0             东证期货   
     4               4162.0                   214.0             广发期货   
     5               3452.0                   930.0             国泰君安   
     6               3397.0                   663.0             新湖期货   
     7               3251.0                   661.0             华泰期货   
     8               3149.0                    26.0             铜冠金源   
     9               3107.0                  1102.0             东兴期货   
     10              2817.0                   242.0             海通期货   
     11              2774.0                  2509.0             首创期货   
     12              2649.0                  1209.0             上海中期   
     13              2377.0                   -15.0             银河期货   
     14              2188.0                   604.0             金瑞期货   
     15              1909.0                  -275.0             徽商期货   
     16              1849.0                   254.0             南华期货   
     17              1739.0                    89.0             国贸期货   
     18              1694.0                     3.0             方正中期   
     19              1606.0                   631.0             五矿经易   
     20             69975.0                  9093.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                5881.0                   1417.0      AU  
     1                4793.0                    449.0      AU  
     2                4131.0                   1945.0      AU  
     3                3815.0                    155.0      AU  
     4                2631.0                    652.0      AU  
     5                2515.0                    308.0      AU  
     6                1847.0                     43.0      AU  
     7                1386.0                    241.0      AU  
     8                1376.0                    219.0      AU  
     9                1283.0                    308.0      AU  
     10               1276.0                    -85.0      AU  
     11               1268.0                    257.0      AU  
     12               1167.0                    465.0      AU  
     13               1081.0                     37.0      AU  
     14                747.0                    -18.0      AU  
     15                747.0                    343.0      AU  
     16                719.0                    -36.0      AU  
     17                688.0                    -69.0      AU  
     18                684.0                     82.0      AU  
     19                571.0                   -367.0      AU  
     20              38606.0                   6346.0      AU  ,
     'au1904':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   au1904     1           中信期货  1328.0   -373.0            东吴期货   
     1   au1904     2           国投安信   872.0   -287.0            东证期货   
     2   au1904     3           中辉期货   839.0    202.0            申万期货   
     3   au1904     4           国泰君安   798.0   -833.0            中信建投   
     4   au1904     5           海通期货   742.0   -375.0            银河期货   
     5   au1904     6           东吴期货   722.0     62.0            中金期货   
     6   au1904     7           东证期货   655.0    -95.0            方正中期   
     7   au1904     8           招金期货   532.0   -244.0            招金期货   
     8   au1904     9           方正中期   504.0   -205.0            中信期货   
     9   au1904    10           银河期货   473.0   -565.0            国泰君安   
     10  au1904    11           迈科期货   422.0   -630.0            西部期货   
     11  au1904    12           格林大华   410.0   -547.0            迈科期货   
     12  au1904    13           中信建投   287.0    -22.0            格林大华   
     13  au1904    14           申万期货   269.0   -268.0            中辉期货   
     14  au1904    15           上海中期   218.0     20.0            鲁证期货   
     15  au1904    16           鲁证期货   212.0     30.0            中银国际   
     16  au1904    17           中融汇信   176.0     22.0            国富期货   
     17  au1904    18           西部期货   150.0   -100.0            兴证期货   
     18  au1904    19           国信期货   136.0     22.0            宏源期货   
     19  au1904    20           东方财富   119.0     26.0            浙商期货   
     20  au1904   999           None  9864.0  -4160.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               2829.0                    12.0             东吴期货   
     1               1561.0                    57.0             东证期货   
     2                818.0                     7.0             国泰君安   
     3                702.0                     1.0             申万期货   
     4                695.0                     5.0             中信建投   
     5                650.0                     0.0             银河期货   
     6                622.0                   -10.0             方正中期   
     7                461.0                    39.0             中信期货   
     8                445.0                    -1.0             招金期货   
     9                416.0                     3.0             迈科期货   
     10               300.0                    29.0             格林大华   
     11               161.0                     0.0             国信期货   
     12               137.0                     0.0             西部期货   
     13                31.0                    25.0             上海中期   
     14                31.0                    -3.0             鲁证期货   
     15                29.0                     0.0             国投安信   
     16                29.0                     0.0             中财期货   
     17                22.0                    19.0             新湖期货   
     18                15.0                   -10.0             国海良时   
     19                13.0                     5.0              美尔雅   
     20              9967.0                   178.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                2824.0                     12.0      AU  
     1                1553.0                     40.0      AU  
     2                 875.0                      3.0      AU  
     3                 849.0                      2.0      AU  
     4                 702.0                      2.0      AU  
     5                 700.0                      8.0      AU  
     6                 623.0                     -2.0      AU  
     7                 427.0                    -13.0      AU  
     8                 376.0                      5.0      AU  
     9                 164.0                      0.0      AU  
     10                143.0                      4.0      AU  
     11                 67.0                     40.0      AU  
     12                 27.0                     -3.0      AU  
     13                 13.0                      1.0      AU  
     14                  9.0                     -3.0      AU  
     15                  8.0                      8.0      AU  
     16                  6.0                      0.0      AU  
     17                  6.0                      0.0      AU  
     18                  5.0                      0.0      AU  
     19                  5.0                      0.0      AU  
     20               9382.0                    104.0      AU  ,
     'au1812':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   au1812     1           光大期货   255.0     42.0            五矿经易   
     1   au1812     2           上海中期   162.0     60.0            东亚期货   
     2   au1812     3           铜冠金源   123.0     66.0            招商期货   
     3   au1812     4           海通期货   123.0    123.0            银河期货   
     4   au1812     5           东证期货   108.0     48.0            瑞达期货   
     5   au1812     6           招金期货   105.0      0.0            申万期货   
     6   au1812     7           国贸期货    90.0     90.0            永安期货   
     7   au1812     8           中信期货    84.0     60.0            浙商期货   
     8   au1812     9           鲁证期货    60.0     57.0            中信期货   
     9   au1812    10           广发期货    48.0     42.0            国信期货   
     10  au1812    11           东海期货    33.0      6.0            招金期货   
     11  au1812    12           华泰期货    33.0    -12.0            上海中期   
     12  au1812    13           申万期货    30.0    -51.0            方正中期   
     13  au1812    14           银河期货    30.0    -24.0            中大期货   
     14  au1812    15           招商期货    15.0     -9.0            华联期货   
     15  au1812    16           国投安信    12.0     12.0            None   
     16  au1812    17           宏源期货    12.0     -6.0            None   
     17  au1812    18           浙商期货     9.0      9.0            None   
     18  au1812    19           瑞龙期货     9.0    -30.0            None   
     19  au1812    20           方正中期     6.0     -6.0            None   
     20  au1812   999           None  1347.0    477.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0                 24.0                     0.0             招金期货   
     1                  9.0                     0.0             上海中期   
     2                  9.0                    -6.0             中信期货   
     3                  9.0                   -12.0             中航期货   
     4                  6.0                     0.0             中辉期货   
     5                  6.0                     6.0             中粮期货   
     6                  6.0                     0.0             国贸期货   
     7                  6.0                    -9.0             南华期货   
     8                  6.0                     0.0             光大期货   
     9                  6.0                     0.0             瑞达期货   
     10                 3.0                     0.0             国投安信   
     11                 3.0                   -15.0             中国国际   
     12                 3.0                    -3.0             东证期货   
     13                 3.0                     0.0             徽商期货   
     14                 3.0                     0.0             申万期货   
     15                 NaN                     NaN             海通期货   
     16                 NaN                     NaN             瑞龙期货   
     17                 NaN                     NaN             广发期货   
     18                 NaN                     NaN             银河期货   
     19                 NaN                     NaN             长江期货   
     20               102.0                   -39.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                1002.0                    -51.0      AU  
     1                 333.0                     99.0      AU  
     2                 186.0                    -30.0      AU  
     3                 168.0                      0.0      AU  
     4                 159.0                      0.0      AU  
     5                 132.0                      0.0      AU  
     6                  90.0                     90.0      AU  
     7                  66.0                      0.0      AU  
     8                  18.0                     -6.0      AU  
     9                  15.0                      0.0      AU  
     10                 12.0                    -12.0      AU  
     11                  9.0                      0.0      AU  
     12                  9.0                   -102.0      AU  
     13                  9.0                      6.0      AU  
     14                  6.0                    -12.0      AU  
     15                  6.0                     -6.0      AU  
     16                  6.0                      6.0      AU  
     17                  6.0                      0.0      AU  
     18                  6.0                      6.0      AU  
     19                  3.0                      3.0      AU  
     20               2241.0                     -9.0      AU  ,
     'ag1906':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   ag1906     1           海通期货   47728.0   1872.0            海通期货   
     1   ag1906     2           中银国际   29258.0   8488.0            鲁证期货   
     2   ag1906     3           国投安信   23266.0   9299.0            方正中期   
     3   ag1906     4           中信期货   19295.0   9920.0            华泰期货   
     4   ag1906     5           国信期货   14763.0   5842.0            首创期货   
     5   ag1906     6           方正中期   11229.0  -2411.0            中州期货   
     6   ag1906     7           国泰君安   10721.0   3331.0            永安期货   
     7   ag1906     8           华泰期货   10654.0   4771.0            国投安信   
     8   ag1906     9           上海中期   10216.0   5072.0            国泰君安   
     9   ag1906    10           东证期货   10193.0   2408.0            上海中期   
     10  ag1906    11           宏源期货    9436.0   3330.0            中信期货   
     11  ag1906    12           鲁证期货    8650.0   4720.0            五矿经易   
     12  ag1906    13           兴证期货    8329.0   2911.0            中衍期货   
     13  ag1906    14           中信建投    8152.0   3782.0            银河期货   
     14  ag1906    15           光大期货    8106.0    840.0            招商期货   
     15  ag1906    16           银河期货    7993.0   3437.0            云晨期货   
     16  ag1906    17           徽商期货    7248.0   2642.0            广发期货   
     17  ag1906    18           浙商期货    6054.0   2518.0            南华期货   
     18  ag1906    19           东航期货    5799.0   2288.0            中信建投   
     19  ag1906    20           华安期货    5664.0   1610.0            兴证期货   
     20  ag1906   999           None  262754.0  76670.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0              23359.0                   637.0             中信期货   
     1              13027.0                   312.0             申万期货   
     2              12160.0                   723.0             国泰君安   
     3               9919.0                  1061.0             五矿经易   
     4               9419.0                   267.0             银河期货   
     5               8747.0                  -109.0             格林大华   
     6               8746.0                   938.0             平安期货   
     7               8633.0                   780.0             东兴期货   
     8               8297.0                   488.0             海通期货   
     9               7472.0                  -157.0             金瑞期货   
     10              7050.0                   820.0             国贸期货   
     11              6795.0                 -1851.0             永安期货   
     12              6657.0                   -35.0             新湖期货   
     13              6479.0                  -266.0             方正中期   
     14              6394.0                   419.0             中金期货   
     15              5920.0                  -119.0             中银国际   
     16              5339.0                   406.0             华泰期货   
     17              5275.0                   439.0             迈科期货   
     18              5165.0                   528.0             铜冠金源   
     19              5135.0                  1177.0             建信期货   
     20            169988.0                  6458.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               39259.0                    487.0      AG  
     1               15179.0                   -129.0      AG  
     2               14799.0                     31.0      AG  
     3               13465.0                    492.0      AG  
     4               11443.0                   3295.0      AG  
     5                9589.0                    -11.0      AG  
     6                9236.0                   1643.0      AG  
     7                8831.0                   3273.0      AG  
     8                7337.0                   -469.0      AG  
     9                7298.0                    397.0      AG  
     10               7141.0                    109.0      AG  
     11               7053.0                     -9.0      AG  
     12               6727.0                    116.0      AG  
     13               5954.0                    374.0      AG  
     14               5316.0                    -88.0      AG  
     15               4212.0                   2753.0      AG  
     16               3927.0                   1227.0      AG  
     17               3827.0                     49.0      AG  
     18               3442.0                    800.0      AG  
     19               3193.0                    140.0      AG  
     20             187228.0                  14480.0      AG  ,
     'ag1812':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   ag1812     1           东证期货  1100.0    380.0            大地期货   
     1   ag1812     2           海通期货   558.0    520.0            方正中期   
     2   ag1812     3           五矿经易   492.0    462.0            上海中期   
     3   ag1812     4           瑞龙期货   438.0    322.0            鲁证期货   
     4   ag1812     5           上海中期   414.0    260.0            国泰君安   
     5   ag1812     6           永安期货   358.0    306.0            建信期货   
     6   ag1812     7           大地期货   336.0    328.0            东方财富   
     7   ag1812     8           招金期货   334.0    -24.0            五矿经易   
     8   ag1812     9           华安期货   332.0    -44.0            一德期货   
     9   ag1812    10           国投安信   258.0    196.0            海通期货   
     10  ag1812    11           国泰君安   248.0    188.0            中银国际   
     11  ag1812    12           中钢期货   222.0    192.0            中粮期货   
     12  ag1812    13           方正中期   208.0    204.0            瑞龙期货   
     13  ag1812    14           申万期货   180.0     16.0            中国国际   
     14  ag1812    15           光大期货   176.0    158.0            东证期货   
     15  ag1812    16           中粮期货   154.0  -1128.0            东亚期货   
     16  ag1812    17           中国国际   152.0     82.0             美尔雅   
     17  ag1812    18           一德期货   142.0    104.0            中信期货   
     18  ag1812    19           西南期货   138.0    138.0            南华期货   
     19  ag1812    20           铜冠金源   114.0   -386.0            中信建投   
     20  ag1812   999           None  6354.0   2274.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               2568.0                   212.0             国泰君安   
     1               1672.0                  -208.0             中钢期货   
     2                690.0                   -50.0             中粮期货   
     3                670.0                     0.0             铜冠金源   
     4                660.0                   -74.0             银河期货   
     5                640.0                   -16.0             国贸期货   
     6                542.0                    -2.0             中大期货   
     7                504.0                     4.0             德盛期货   
     8                482.0                    54.0             光大期货   
     9                458.0                   286.0             首创期货   
     10               412.0                    -2.0             华安期货   
     11               406.0                   106.0             华泰期货   
     12               398.0                   378.0             中信期货   
     13               390.0                  -152.0             南华期货   
     14               388.0                    48.0             方正中期   
     15               300.0                    -2.0             申万期货   
     16               204.0                   -34.0             国富期货   
     17               196.0                   -14.0             一德期货   
     18               178.0                   -20.0             国投安信   
     19               176.0                   -32.0             中辉期货   
     20             11934.0                   482.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                4236.0                     30.0      AG  
     1                1398.0                   -186.0      AG  
     2                1396.0                      0.0      AG  
     3                1134.0                      0.0      AG  
     4                1002.0                      0.0      AG  
     5                 914.0                      0.0      AG  
     6                 704.0                     20.0      AG  
     7                 532.0                     40.0      AG  
     8                 440.0                   -112.0      AG  
     9                 316.0                      0.0      AG  
     10                300.0                      0.0      AG  
     11                260.0                      0.0      AG  
     12                250.0                      0.0      AG  
     13                210.0                      0.0      AG  
     14                200.0                      0.0      AG  
     15                172.0                      0.0      AG  
     16                158.0                    -42.0      AG  
     17                150.0                    -20.0      AG  
     18                126.0                      0.0      AG  
     19                 94.0                      4.0      AG  
     20              13992.0                   -266.0      AG  ,
     'rb1812':    symbol  rank vol_party_name    vol  vol_chg long_party_name  \
     0  rb1812     1           瑞达期货   90.0      0.0            瑞达期货   
     1  rb1812     2           国联期货   60.0     60.0            永安期货   
     2  rb1812     3           申万期货   30.0      0.0            冠通期货   
     3  rb1812   999           None  180.0     60.0            None   
     
        long_open_interest  long_open_interest_chg short_party_name  \
     0                90.0                    30.0             宝城期货   
     1                30.0                     0.0             一德期货   
     2                30.0                     0.0             None   
     3               150.0                    30.0             None   
     
        short_open_interest  short_open_interest_chg variety  
     0                 90.0                      0.0      RB  
     1                 60.0                      0.0      RB  
     2                  NaN                      NaN      RB  
     3                150.0                      0.0      RB  ,
     'rb1905':     symbol  rank vol_party_name        vol   vol_chg long_party_name  \
     0   rb1905     1           海通期货   365921.0  -35608.0            永安期货   
     1   rb1905     2           中信期货   273597.0  -40328.0            中信期货   
     2   rb1905     3           永安期货   229201.0   33487.0            银河期货   
     3   rb1905     4           方正中期   170406.0  -42704.0            申万期货   
     4   rb1905     5           东证期货   153286.0    -535.0            方正中期   
     5   rb1905     6           国投安信   145563.0    7505.0            鲁证期货   
     6   rb1905     7           申万期货   110904.0    -779.0            一德期货   
     7   rb1905     8           国泰君安   109314.0   -9396.0            海通期货   
     8   rb1905     9           华泰期货   108859.0    -263.0            国泰君安   
     9   rb1905    10           上海大陆   103070.0   18353.0            东海期货   
     10  rb1905    11           徽商期货   101996.0   -6105.0            中大期货   
     11  rb1905    12           东方财富   100814.0  -43445.0            国投安信   
     12  rb1905    13           银河期货    98406.0  -19680.0            道通期货   
     13  rb1905    14           光大期货    98122.0   -6196.0            瑞达期货   
     14  rb1905    15           国贸期货    95129.0  -23391.0            华泰期货   
     15  rb1905    16           中辉期货    88751.0   27990.0            广发期货   
     16  rb1905    17           中信建投    78718.0    1337.0            南华期货   
     17  rb1905    18           华安期货    74403.0   -5884.0            渤海期货   
     18  rb1905    19           上海中期    72921.0  -47075.0            徽商期货   
     19  rb1905    20           鲁证期货    68582.0   12553.0            中钢期货   
     20  rb1905   999           None  2647963.0 -180164.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0              89775.0                -10953.0             永安期货   
     1              56640.0                 -2831.0             银河期货   
     2              45976.0                  8925.0             方正中期   
     3              43857.0                 -8748.0             国泰君安   
     4              38663.0                  5807.0             鲁证期货   
     5              33858.0                  4083.0             华泰期货   
     6              32669.0                  2596.0             一德期货   
     7              30381.0                  -313.0             海通期货   
     8              29078.0                 -3571.0             中信期货   
     9              25654.0                  1904.0             兴证期货   
     10             25542.0                  1314.0             申万期货   
     11             23408.0                  3213.0             广发期货   
     12             22641.0                   701.0             信达期货   
     13             22531.0                  3582.0             东证期货   
     14             22366.0                 -8963.0             国海良时   
     15             22229.0                  6922.0             东海期货   
     16             21046.0                  2430.0             中国国际   
     17             20766.0                 15675.0             新湖期货   
     18             17898.0                   941.0             中粮期货   
     19             17616.0                   677.0             东航期货   
     20            642594.0                 23391.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0              121702.0                  10508.0      RB  
     1              104971.0                   1943.0      RB  
     2               91792.0                   4051.0      RB  
     3               53953.0                   8707.0      RB  
     4               48423.0                  12129.0      RB  
     5               44354.0                  -3620.0      RB  
     6               35061.0                   -918.0      RB  
     7               31947.0                   3734.0      RB  
     8               30235.0                   4600.0      RB  
     9               28792.0                    750.0      RB  
     10              28487.0                   9266.0      RB  
     11              24436.0                  -2159.0      RB  
     12              24413.0                   1290.0      RB  
     13              21893.0                   4560.0      RB  
     14              19564.0                   1824.0      RB  
     15              19433.0                   3559.0      RB  
     16              17686.0                   2838.0      RB  
     17              17363.0                   7164.0      RB  
     18              16948.0                   -127.0      RB  
     19              16666.0                   4065.0      RB  
     20             798119.0                  74164.0      RB  ,
     'rb1901':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   rb1901     1           海通期货   62364.0 -21329.0            永安期货   
     1   rb1901     2           永安期货   29375.0   6752.0            华泰期货   
     2   rb1901     3           中信期货   28214.0  -9960.0            天富期货   
     3   rb1901     4           东证期货   27720.0  -7345.0            中信期货   
     4   rb1901     5           国泰君安   19943.0 -10490.0            国泰君安   
     5   rb1901     6           华泰期货   17268.0  -8799.0            国贸期货   
     6   rb1901     7           国投安信   15683.0  -5073.0            一德期货   
     7   rb1901     8           银河期货   15638.0   -347.0            广发期货   
     8   rb1901     9           西部期货   15524.0    -42.0            方正中期   
     9   rb1901    10           方正中期   14333.0  -6993.0            东兴期货   
     10  rb1901    11           徽商期货   13490.0    150.0            大地期货   
     11  rb1901    12           中银国际   10750.0  -3394.0            东方汇金   
     12  rb1901    13           中信建投    9952.0   3117.0            银河期货   
     13  rb1901    14           鲁证期货    9668.0  -7115.0            海通期货   
     14  rb1901    15           新湖期货    8767.0  -5767.0            国投安信   
     15  rb1901    16           光大期货    8481.0  -1887.0            中信建投   
     16  rb1901    17           中财期货    7174.0  -3339.0            鲁证期货   
     17  rb1901    18           申万期货    7132.0  -3703.0            东证期货   
     18  rb1901    19           南华期货    6435.0  -4197.0            大越期货   
     19  rb1901    20           一德期货    6218.0  -6420.0            锦泰期货   
     20  rb1901   999           None  334129.0 -96181.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0              23954.0                   933.0             永安期货   
     1              12114.0                  -745.0             国泰君安   
     2              10039.0                    -3.0             银河期货   
     3               9112.0                   -66.0             海通期货   
     4               8142.0                  -817.0             东证期货   
     5               8035.0                   153.0             中信期货   
     6               7283.0                  -182.0             华泰期货   
     7               7161.0                    87.0             光大期货   
     8               6933.0                 -1005.0             国贸期货   
     9               6499.0                  -155.0             鲁证期货   
     10              6213.0                   -32.0             东海期货   
     11              6037.0                   -14.0             上海大陆   
     12              5646.0                  -460.0             大地期货   
     13              5601.0                 -3681.0             天风期货   
     14              5308.0                    -5.0             国联期货   
     15              4941.0                  -217.0             方正中期   
     16              4812.0                 -1039.0             南华期货   
     17              4803.0                  -340.0             东航期货   
     18              4782.0                   115.0             信达期货   
     19              4326.0                    50.0             广发期货   
     20            151741.0                 -7423.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               32765.0                    438.0      RB  
     1               17650.0                   1366.0      RB  
     2               15117.0                   -898.0      RB  
     3               13862.0                   -427.0      RB  
     4               11780.0                    812.0      RB  
     5               11556.0                    334.0      RB  
     6                7470.0                  -1749.0      RB  
     7                6821.0                    661.0      RB  
     8                5969.0                  -3859.0      RB  
     9                5939.0                    445.0      RB  
     10               5600.0                   -712.0      RB  
     11               5375.0                     29.0      RB  
     12               5254.0                    -14.0      RB  
     13               5040.0                     30.0      RB  
     14               4900.0                   -316.0      RB  
     15               4782.0                  -1100.0      RB  
     16               4771.0                     99.0      RB  
     17               4721.0                     53.0      RB  
     18               4373.0                    -71.0      RB  
     19               3948.0                   -316.0      RB  
     20             177693.0                  -5195.0      RB  ,
     'rb1910':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   rb1910     1           中信期货  14328.0   1596.0            鲁证期货   
     1   rb1910     2           海通期货  10156.0    323.0            格林大华   
     2   rb1910     3           银河期货   5685.0   2202.0            国泰君安   
     3   rb1910     4           鲁证期货   5301.0    248.0            申万期货   
     4   rb1910     5           东证期货   4575.0  -1081.0            中大期货   
     5   rb1910     6           西部期货   3943.0    154.0            中信期货   
     6   rb1910     7           大连良运   3706.0   -603.0            宏源期货   
     7   rb1910     8           国泰君安   3425.0   1032.0            银河期货   
     8   rb1910     9           方正中期   3398.0    306.0            新湖期货   
     9   rb1910    10           华泰期货   3313.0    492.0            海通期货   
     10  rb1910    11           国投安信   3268.0    922.0            兴证期货   
     11  rb1910    12            新世纪   3250.0   1848.0            东海期货   
     12  rb1910    13           光大期货   3231.0   1445.0            浙商期货   
     13  rb1910    14           五矿经易   3191.0   -611.0            光大期货   
     14  rb1910    15           中辉期货   3031.0   2166.0            中辉期货   
     15  rb1910    16           广发期货   2734.0    451.0            永安期货   
     16  rb1910    17           永安期货   2448.0   -743.0            中钢期货   
     17  rb1910    18           中融汇信   2196.0   -195.0            方正中期   
     18  rb1910    19           国信期货   2036.0     78.0            信达期货   
     19  rb1910    20           华安期货   1891.0   -133.0            广发期货   
     20  rb1910   999           None  85106.0   9897.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0              10191.0                   229.0             银河期货   
     1               8113.0                   100.0             海通期货   
     2               7255.0                   337.0             永安期货   
     3               6376.0                   317.0             东海期货   
     4               6000.0                   194.0             中信期货   
     5               4999.0                  1778.0             国投安信   
     6               4901.0                   248.0             国贸期货   
     7               4852.0                   216.0              新世纪   
     8               4393.0                    82.0             五矿经易   
     9               4155.0                   112.0             光大期货   
     10              3833.0                    -8.0             东证期货   
     11              3666.0                    84.0             鲁证期货   
     12              3588.0                   398.0             东吴期货   
     13              3550.0                   199.0             一德期货   
     14              3280.0                  2544.0             华泰期货   
     15              3273.0                   653.0             中信建投   
     16              2401.0                    55.0             长江期货   
     17              2337.0                   342.0             锦泰期货   
     18              2331.0                  1144.0             渤海期货   
     19              2303.0                   651.0             海证期货   
     20             91797.0                  9675.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               18316.0                   2539.0      RB  
     1               11987.0                    218.0      RB  
     2               10124.0                    141.0      RB  
     3                9404.0                     15.0      RB  
     4                8096.0                   1180.0      RB  
     5                7588.0                    330.0      RB  
     6                7328.0                    164.0      RB  
     7                6239.0                   2975.0      RB  
     8                5710.0                   1143.0      RB  
     9                4822.0                   1554.0      RB  
     10               4600.0                    271.0      RB  
     11               3500.0                    946.0      RB  
     12               3316.0                   1094.0      RB  
     13               3073.0                    127.0      RB  
     14               2880.0                    183.0      RB  
     15               2265.0                    733.0      RB  
     16               2162.0                    241.0      RB  
     17               2003.0                     -3.0      RB  
     18               1969.0                    256.0      RB  
     19               1934.0                     93.0      RB  
     20             117316.0                  14200.0      RB  ,
     'hc1905':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   hc1905     1           海通期货   88732.0 -14120.0            银河期货   
     1   hc1905     2           方正中期   45527.0  12437.0            中信期货   
     2   hc1905     3           中信期货   37703.0  -3697.0            永安期货   
     3   hc1905     4           永安期货   31509.0  -7668.0            海通期货   
     4   hc1905     5           东证期货   27441.0   -528.0            光大期货   
     5   hc1905     6           国投安信   25879.0   4308.0            五矿经易   
     6   hc1905     7           华泰期货   23253.0    324.0            方正中期   
     7   hc1905     8           兴证期货   21164.0    419.0            国投安信   
     8   hc1905     9           国泰君安   13552.0   2394.0            兴证期货   
     9   hc1905    10           徽商期货   10082.0  -1671.0            申万期货   
     10  hc1905    11           上海大陆    9770.0    718.0            中大期货   
     11  hc1905    12           西南期货    9719.0  -4388.0            国泰君安   
     12  hc1905    13           华安期货    9333.0  -1385.0            广发期货   
     13  hc1905    14           银河期货    9312.0    338.0            南华期货   
     14  hc1905    15           东吴期货    9134.0   -757.0            西南期货   
     15  hc1905    16           安粮期货    9094.0   -765.0            东证期货   
     16  hc1905    17           一德期货    8428.0   -515.0            一德期货   
     17  hc1905    18           中融汇信    8200.0  -3054.0            华泰期货   
     18  hc1905    19           广发期货    7993.0   1230.0            浙商期货   
     19  hc1905    20           南华期货    7949.0   1042.0            建信期货   
     20  hc1905   999           None  413774.0 -15338.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0              24831.0                  -760.0             永安期货   
     1              21105.0                  -492.0             国泰君安   
     2              18209.0                   131.0             方正中期   
     3              14165.0                  3205.0             中信期货   
     4               9679.0                  2408.0             华泰期货   
     5               9192.0                   897.0             银河期货   
     6               8907.0                 -1452.0             中辉期货   
     7               6775.0                    91.0             一德期货   
     8               6556.0                  3516.0             瑞达期货   
     9               5898.0                  -600.0             东证期货   
     10              5444.0                   856.0             申万期货   
     11              5113.0                  -342.0             兴证期货   
     12              5039.0                   810.0             海通期货   
     13              4870.0                   -98.0             集成期货   
     14              4761.0                  2409.0             广发期货   
     15              4581.0                  -708.0             南华期货   
     16              4213.0                  1070.0             新晟期货   
     17              4114.0                 -4696.0             中粮期货   
     18              3939.0                   590.0             国投安信   
     19              3905.0                    72.0             中国国际   
     20            171296.0                  6907.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               41394.0                  -6480.0      HC  
     1               40254.0                   4158.0      HC  
     2               22033.0                   8475.0      HC  
     3               12395.0                   1535.0      HC  
     4               10740.0                   3259.0      HC  
     5                9466.0                   1660.0      HC  
     6                7354.0                  -1103.0      HC  
     7                6366.0                   1204.0      HC  
     8                4991.0                    -88.0      HC  
     9                4733.0                   -209.0      HC  
     10               4262.0                   -326.0      HC  
     11               3788.0                   -962.0      HC  
     12               3769.0                    747.0      HC  
     13               3645.0                   1077.0      HC  
     14               3598.0                   -161.0      HC  
     15               3588.0                   2157.0      HC  
     16               3084.0                    -19.0      HC  
     17               3010.0                    131.0      HC  
     18               2962.0                   -112.0      HC  
     19               2836.0                    222.0      HC  
     20             194268.0                  15165.0      HC  ,
     'hc1812':    symbol  rank vol_party_name   vol  vol_chg long_party_name  \
     0  hc1812     1           国泰君安  30.0     30.0            永安期货   
     1  hc1812     2           永安期货  30.0    -30.0            方正中期   
     2  hc1812     3           None   NaN      NaN            None   
     3  hc1812   999           None  60.0      0.0            None   
     
        long_open_interest  long_open_interest_chg short_party_name  \
     0               240.0                   -30.0             东证期货   
     1                30.0                     0.0             东海期货   
     2                 NaN                     NaN             海通期货   
     3               270.0                   -30.0             None   
     
        short_open_interest  short_open_interest_chg variety  
     0                150.0                      0.0      HC  
     1                 90.0                      0.0      HC  
     2                 30.0                      0.0      HC  
     3                270.0                      0.0      HC  ,
     'hc1901':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   hc1901     1           海通期货  18784.0  -7863.0            永安期货   
     1   hc1901     2           中信期货   5685.0  -2258.0            上海大陆   
     2   hc1901     3           国投安信   4648.0  -1065.0            银河期货   
     3   hc1901     4           东证期货   4504.0  -1633.0            广州期货   
     4   hc1901     5           永安期货   3756.0   -131.0            中信期货   
     5   hc1901     6           新湖期货   2833.0    324.0            建信期货   
     6   hc1901     7           华泰期货   2766.0  -3179.0            华泰期货   
     7   hc1901     8           鲁证期货   2256.0  -2061.0            国联期货   
     8   hc1901     9           国泰君安   2182.0  -2639.0            国贸期货   
     9   hc1901    10           方正中期   2122.0   -403.0            新湖期货   
     10  hc1901    11           五矿经易   2080.0  -2360.0            海通期货   
     11  hc1901    12           银河期货   1719.0  -2154.0            鲁证期货   
     12  hc1901    13           信达期货   1576.0   1105.0            东证期货   
     13  hc1901    14           西部期货   1481.0  -1479.0            南华期货   
     14  hc1901    15           东兴期货   1449.0   1342.0            大地期货   
     15  hc1901    16           中衍期货   1434.0   -588.0            方正中期   
     16  hc1901    17           兴证期货   1428.0  -1833.0            瑞达期货   
     17  hc1901    18           中融汇信   1282.0   -564.0            中大期货   
     18  hc1901    19           光大期货   1271.0     59.0            中国国际   
     19  hc1901    20           安粮期货   1222.0  -3832.0            国金期货   
     20  hc1901   999           None  64478.0 -31212.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0              10306.0                  -255.0             瑞达期货   
     1               5385.0                    -5.0             永安期货   
     2               5115.0                   571.0             海通期货   
     3               4937.0                   -25.0             国泰君安   
     4               3984.0                  -867.0             一德期货   
     5               3733.0                  -388.0             银河期货   
     6               3479.0                  -162.0             弘业期货   
     7               3200.0                   -32.0             鲁证期货   
     8               2921.0                  -321.0             五矿经易   
     9               2808.0                   -26.0             东兴期货   
     10              2643.0                  -157.0             东航期货   
     11              2313.0                   -20.0             南华期货   
     12              1587.0                   -66.0             申万期货   
     13              1487.0                    30.0             锦泰期货   
     14              1361.0                   -36.0             东证期货   
     15              1304.0                  -592.0             国贸期货   
     16              1161.0                    26.0             国投安信   
     17              1112.0                   -70.0              鑫鼎盛   
     18              1042.0                    -3.0             华泰期货   
     19               983.0                   -18.0             迈科期货   
     20             60861.0                 -2416.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                8174.0                   -754.0      HC  
     1                7896.0                  -1931.0      HC  
     2                7371.0                    687.0      HC  
     3                4948.0                      6.0      HC  
     4                4925.0                   -140.0      HC  
     5                4222.0                   -388.0      HC  
     6                3072.0                    -21.0      HC  
     7                2912.0                   -390.0      HC  
     8                2791.0                    552.0      HC  
     9                2140.0                   -202.0      HC  
     10               1958.0                    -23.0      HC  
     11               1692.0                    -94.0      HC  
     12               1623.0                    -38.0      HC  
     13               1417.0                      0.0      HC  
     14               1332.0                   -140.0      HC  
     15               1295.0                    -40.0      HC  
     16               1271.0                    -89.0      HC  
     17               1160.0                   -521.0      HC  
     18               1071.0                     48.0      HC  
     19                898.0                   -225.0      HC  
     20              62168.0                  -3703.0      HC  ,
     'fu1905':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   fu1905     1           华泰期货   37460.0   9608.0            永安期货   
     1   fu1905     2           中信期货   34103.0  11726.0            申万期货   
     2   fu1905     3           国泰君安   29588.0   3554.0            五矿经易   
     3   fu1905     4           海通期货   27567.0   7189.0            南华期货   
     4   fu1905     5           银河期货   26664.0   3082.0            银河期货   
     5   fu1905     6           东证期货   23334.0   3675.0            广金期货   
     6   fu1905     7           国投安信   21238.0   2867.0            国投安信   
     7   fu1905     8           中银国际   19521.0  10187.0            海通期货   
     8   fu1905     9           徽商期货   18301.0   4437.0            宏源期货   
     9   fu1905    10           宏源期货   13046.0   3099.0            广发期货   
     10  fu1905    11           华安期货   12971.0   2224.0            中信期货   
     11  fu1905    12           东方财富   12518.0   6022.0            国泰君安   
     12  fu1905    13           申万期货   11644.0   1237.0            华泰期货   
     13  fu1905    14           兴证期货   10424.0   4422.0            浙商期货   
     14  fu1905    15           永安期货    9942.0   3616.0            国海良时   
     15  fu1905    16           国信期货    9092.0   2597.0            华西期货   
     16  fu1905    17           新湖期货    8700.0   3523.0            徽商期货   
     17  fu1905    18           西部期货    8665.0  -3087.0            东证期货   
     18  fu1905    19           方正中期    8607.0  -1741.0            大地期货   
     19  fu1905    20           东亚期货    8078.0   1119.0            建信期货   
     20  fu1905   999           None  351463.0  79356.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0              13640.0                  -731.0             中银国际   
     1               4985.0                  -249.0             银河期货   
     2               4354.0                  -195.0             上海浙石   
     3               4045.0                  -296.0             海通期货   
     4               3553.0                  -229.0             渤海期货   
     5               3049.0                   -48.0             中信期货   
     6               2209.0                  -433.0             永安期货   
     7               2171.0                  -268.0             国投安信   
     8               2022.0                  -213.0             天风期货   
     9               1938.0                   -67.0             中财期货   
     10              1909.0                  -893.0             国信期货   
     11              1897.0                  -706.0             东兴期货   
     12              1843.0                   329.0             申万期货   
     13              1649.0                  -885.0             国泰君安   
     14              1550.0                   -27.0             东航期货   
     15              1535.0                  -110.0             兴证期货   
     16              1418.0                  -638.0             宏源期货   
     17              1254.0                   -58.0             华泰期货   
     18              1164.0                  -236.0             五矿经易   
     19              1149.0                  -192.0             广发期货   
     20             57334.0                 -6145.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               21250.0                   -207.0      FU  
     1               13343.0                  -4985.0      FU  
     2                7320.0                    -49.0      FU  
     3                7016.0                   -677.0      FU  
     4                6771.0                      1.0      FU  
     5                4672.0                  -1374.0      FU  
     6                4063.0                   -969.0      FU  
     7                3232.0                    135.0      FU  
     8                1620.0                    -32.0      FU  
     9                1367.0                     85.0      FU  
     10               1258.0                    -99.0      FU  
     11               1105.0                      5.0      FU  
     12                946.0                     95.0      FU  
     13                767.0                    -20.0      FU  
     14                741.0                    510.0      FU  
     15                715.0                  -1078.0      FU  
     16                701.0                   -105.0      FU  
     17                690.0                   -527.0      FU  
     18                640.0                   -202.0      FU  
     19                623.0                    399.0      FU  
     20              78840.0                  -9094.0      FU  ,
     'fu1901':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   fu1901     1           华泰期货   69110.0 -25264.0            徽商期货   
     1   fu1901     2           海通期货   55663.0   8438.0            银河期货   
     2   fu1901     3           国投安信   35761.0  -6814.0            东证期货   
     3   fu1901     4           中信期货   27939.0  -4670.0            西部期货   
     4   fu1901     5           东证期货   27156.0   2771.0            国信期货   
     5   fu1901     6           中银国际   22988.0   4303.0            中信建投   
     6   fu1901     7           中融汇信   20980.0  -8753.0            中信期货   
     7   fu1901     8           兴证期货   18270.0   5617.0            华安期货   
     8   fu1901     9           徽商期货   13987.0   -169.0            海通期货   
     9   fu1901    10           华安期货   12719.0    418.0            永安期货   
     10  fu1901    11           银河期货   11849.0  -1548.0            方正中期   
     11  fu1901    12           西部期货   10353.0  -1570.0            浙商期货   
     12  fu1901    13           国泰君安    9210.0  -2438.0            国投安信   
     13  fu1901    14           光大期货    8027.0    303.0            国富期货   
     14  fu1901    15           方正中期    7987.0   -869.0            广发期货   
     15  fu1901    16           上海中期    7820.0  -1408.0            锦泰期货   
     16  fu1901    17           金瑞期货    7333.0   -347.0            申万期货   
     17  fu1901    18           中信建投    6351.0  -1164.0            东吴期货   
     18  fu1901    19           申万期货    6272.0   -497.0            平安期货   
     19  fu1901    20           广发期货    5838.0    680.0            招商期货   
     20  fu1901   999           None  385613.0 -32981.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0                936.0                  -341.0             中银国际   
     1                809.0                    85.0             银河期货   
     2                801.0                   -23.0             中信期货   
     3                783.0                   129.0             永安期货   
     4                782.0                   -60.0             平安期货   
     5                753.0                  -100.0             渤海期货   
     6                718.0                  -236.0             海通期货   
     7                679.0                  -287.0             国泰君安   
     8                675.0                  -135.0             国投安信   
     9                672.0                  -154.0             上海浙石   
     10               652.0                  -325.0             英大期货   
     11               626.0                    -8.0             徽商期货   
     12               622.0                   -77.0             西部期货   
     13               525.0                    52.0             兴证期货   
     14               522.0                  -365.0             广金期货   
     15               473.0                    10.0             华泰期货   
     16               471.0                  -144.0             宏源期货   
     17               451.0                   -14.0             华安期货   
     18               447.0                   -46.0             申万期货   
     19               436.0                   -20.0             华联期货   
     20             12833.0                 -2059.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               10626.0                    -33.0      FU  
     1                1094.0                   -454.0      FU  
     2                 867.0                   -307.0      FU  
     3                 662.0                   -122.0      FU  
     4                 575.0                    355.0      FU  
     5                 526.0                     18.0      FU  
     6                 509.0                   -258.0      FU  
     7                 498.0                   -207.0      FU  
     8                 496.0                    -30.0      FU  
     9                 474.0                  -1803.0      FU  
     10                351.0                   -118.0      FU  
     11                347.0                    -40.0      FU  
     12                346.0                    128.0      FU  
     13                330.0                     10.0      FU  
     14                316.0                    -33.0      FU  
     15                315.0                     20.0      FU  
     16                313.0                    -99.0      FU  
     17                306.0                   -150.0      FU  
     18                301.0                     16.0      FU  
     19                301.0                    288.0      FU  
     20              19553.0                  -2819.0      FU  ,
     'bu1906':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   bu1906     1           海通期货  103934.0   8413.0            永安期货   
     1   bu1906     2           永安期货   41634.0  26384.0            海通期货   
     2   bu1906     3           国投安信   30520.0   3065.0            银河期货   
     3   bu1906     4           中信期货   27138.0  -2680.0            广发期货   
     4   bu1906     5           东证期货   21611.0  -2390.0            国投安信   
     5   bu1906     6           国泰君安   21535.0   1641.0            中信建投   
     6   bu1906     7           兴证期货   21012.0   5501.0            华泰期货   
     7   bu1906     8           方正中期   20022.0  -2994.0            中信期货   
     8   bu1906     9           广发期货   19090.0   4034.0            方正中期   
     9   bu1906    10           华泰期货   18664.0  -2105.0            国泰君安   
     10  bu1906    11           徽商期货   17917.0  -2709.0            浙商期货   
     11  bu1906    12           华鑫期货   17093.0  15851.0            东证期货   
     12  bu1906    13           华安期货   16694.0   -562.0            申万期货   
     13  bu1906    14           银河期货   16015.0  -5789.0            东海期货   
     14  bu1906    15           南华期货   15916.0   6780.0            兴证期货   
     15  bu1906    16           申万期货   15068.0   -471.0            鲁证期货   
     16  bu1906    17           创元期货   12143.0  -2315.0            广州期货   
     17  bu1906    18           宏源期货   11481.0   2615.0            徽商期货   
     18  bu1906    19           东航期货   11406.0   -417.0            华安期货   
     19  bu1906    20           东方财富   11371.0  -1964.0            中国国际   
     20  bu1906   999           None  470264.0  49888.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0              21201.0                   580.0             海通期货   
     1              17488.0                 -3078.0             永安期货   
     2               9946.0                 -1731.0             银河期货   
     3               7128.0                   733.0             中信期货   
     4               7073.0                  -604.0             方正中期   
     5               6595.0                   -56.0             南华期货   
     6               6105.0                    14.0             兴证期货   
     7               5890.0                   439.0             国泰君安   
     8               5424.0                     9.0             华泰期货   
     9               4977.0                 -2127.0             东证期货   
     10              4314.0                  -177.0             国投安信   
     11              4204.0                   167.0             申万期货   
     12              4052.0                  -148.0             长江期货   
     13              3875.0                  -261.0             中金期货   
     14              3572.0                  -906.0             浙商期货   
     15              2874.0                   892.0             东吴期货   
     16              2814.0                  -320.0             东方财富   
     17              2781.0                   111.0             东航期货   
     18              2636.0                   915.0             广发期货   
     19              2419.0                   320.0             盛达期货   
     20            125368.0                 -5228.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               19159.0                  -3106.0      BU  
     1               18261.0                   4244.0      BU  
     2               12981.0                  -2742.0      BU  
     3               10756.0                   -287.0      BU  
     4                8941.0                   -319.0      BU  
     5                7768.0                   1237.0      BU  
     6                6426.0                   -310.0      BU  
     7                6041.0                   -786.0      BU  
     8                5863.0                   1540.0      BU  
     9                5244.0                  -1786.0      BU  
     10               4782.0                  -2178.0      BU  
     11               4770.0                    788.0      BU  
     12               4670.0                   -104.0      BU  
     13               4411.0                    240.0      BU  
     14               3883.0                   -545.0      BU  
     15               3481.0                     52.0      BU  
     16               3129.0                   -168.0      BU  
     17               2981.0                    -42.0      BU  
     18               2960.0                   -155.0      BU  
     19               2722.0                     12.0      BU  
     20             139229.0                  -4415.0      BU  ,
     'bu1812':     symbol  rank vol_party_name     vol  vol_chg long_party_name  \
     0   bu1812     1           国泰君安   485.0    281.0            浙商期货   
     1   bu1812     2           光大期货   427.0     85.0            中信期货   
     2   bu1812     3           鲁证期货   269.0     19.0            格林大华   
     3   bu1812     4           中信建投   250.0     70.0            国泰君安   
     4   bu1812     5           徽商期货   243.0   -109.0            中粮期货   
     5   bu1812     6           海通期货   176.0     66.0            兴业期货   
     6   bu1812     7           宏源期货   175.0    109.0            徽商期货   
     7   bu1812     8           招金期货   165.0    159.0             新纪元   
     8   bu1812     9           华安期货   153.0   -173.0            方正中期   
     9   bu1812    10           银河期货   126.0     -7.0            海通期货   
     10  bu1812    11           中粮期货   125.0   -211.0            东航期货   
     11  bu1812    12           浙商期货   120.0    -79.0            弘业期货   
     12  bu1812    13           申万期货   104.0    -66.0            广发期货   
     13  bu1812    14           渤海期货   104.0     97.0            中银国际   
     14  bu1812    15           东证期货    99.0     39.0            中国国际   
     15  bu1812    16           广发期货    97.0      2.0            华安期货   
     16  bu1812    17           东方财富    96.0     -8.0            华泰期货   
     17  bu1812    18           方正中期    91.0    -58.0            上海大陆   
     18  bu1812    19           华信期货    91.0     -6.0            第一创业   
     19  bu1812    20           中信期货    86.0    -21.0            国元期货   
     20  bu1812   999           None  3482.0    189.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0                765.0                    80.0             银河期货   
     1                617.0                    -8.0             永安期货   
     2                503.0                   -21.0             国泰君安   
     3                367.0                    -3.0             大地期货   
     4                209.0                   -37.0              新世纪   
     5                151.0                     0.0             大有期货   
     6                137.0                   -44.0             方正中期   
     7                134.0                   -14.0             国信期货   
     8                130.0                    10.0             宝城期货   
     9                126.0                    40.0             渤海期货   
     10               117.0                    -6.0             瑞达期货   
     11               115.0                   -11.0             招金期货   
     12               100.0                   -24.0             平安期货   
     13                85.0                   -10.0             东海期货   
     14                68.0                    -6.0             国金期货   
     15                66.0                    -6.0             中信期货   
     16                64.0                    -2.0             上海大陆   
     17                57.0                    -7.0             招商期货   
     18                55.0                    -4.0             中信建投   
     19                54.0                     0.0             东兴期货   
     20              3920.0                   -73.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                3626.0                    -31.0      BU  
     1                1004.0                    -10.0      BU  
     2                 129.0                   -352.0      BU  
     3                 101.0                      0.0      BU  
     4                  73.0                     73.0      BU  
     5                  38.0                      0.0      BU  
     6                  33.0                     -1.0      BU  
     7                  23.0                     13.0      BU  
     8                  20.0                      0.0      BU  
     9                  20.0                     19.0      BU  
     10                 19.0                     -1.0      BU  
     11                 18.0                     18.0      BU  
     12                 18.0                    -10.0      BU  
     13                 17.0                      0.0      BU  
     14                 16.0                      0.0      BU  
     15                 15.0                     -2.0      BU  
     16                 14.0                     -1.0      BU  
     17                 14.0                      0.0      BU  
     18                 14.0                     10.0      BU  
     19                 14.0                      0.0      BU  
     20               5226.0                   -275.0      BU  ,
     'ru1909':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   ru1909     1           中信期货   2569.0    625.0            大地期货   
     1   ru1909     2           东证期货   1384.0    372.0            永安期货   
     2   ru1909     3           海通期货   1221.0    431.0            宝城期货   
     3   ru1909     4           中融汇信   1217.0    -27.0            瑞达期货   
     4   ru1909     5           国泰君安    721.0    320.0            国泰君安   
     5   ru1909     6           华泰期货    706.0   -113.0            华泰期货   
     6   ru1909     7           鲁证期货    579.0     91.0            新湖期货   
     7   ru1909     8           方正中期    523.0    105.0            国信期货   
     8   ru1909     9           中钢期货    463.0    140.0            浙商期货   
     9   ru1909    10           首创期货    460.0    310.0            广发期货   
     10  ru1909    11           大地期货    451.0    300.0            一德期货   
     11  ru1909    12           格林大华    442.0    -95.0            国贸期货   
     12  ru1909    13           上海中期    408.0    187.0            山金期货   
     13  ru1909    14           中辉期货    392.0     11.0            格林大华   
     14  ru1909    15           东方财富    355.0     40.0            方正中期   
     15  ru1909    16           永安期货    304.0     52.0            金瑞期货   
     16  ru1909    17           西部期货    286.0    -23.0            国投安信   
     17  ru1909    18           广发期货    278.0    143.0            大越期货   
     18  ru1909    19           瑞达期货    267.0    -47.0            福能期货   
     19  ru1909    20           一德期货    259.0    169.0            东兴期货   
     20  ru1909   999           None  13285.0   2991.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               1338.0                    47.0             中银国际   
     1               1284.0                    27.0             南华期货   
     2               1168.0                    22.0             中信期货   
     3               1153.0                    -4.0             国泰君安   
     4               1126.0                    44.0             格林大华   
     5                990.0                    58.0             永安期货   
     6                971.0                     8.0             申万期货   
     7                908.0                     4.0             中粮期货   
     8                868.0                    11.0             国投安信   
     9                756.0                     7.0             华泰期货   
     10               723.0                    14.0             五矿经易   
     11               718.0                     5.0             广发期货   
     12               714.0                     0.0             中钢期货   
     13               696.0                    -8.0             方正中期   
     14               663.0                   136.0             银河期货   
     15               652.0                     9.0             首创期货   
     16               641.0                     7.0             金瑞期货   
     17               627.0                    23.0             东方财富   
     18               622.0                     8.0             东证期货   
     19               528.0                    -2.0             西部期货   
     20             17146.0                   416.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                4271.0                      0.0      RU  
     1                2952.0                     -4.0      RU  
     2                2435.0                     19.0      RU  
     3                1832.0                     87.0      RU  
     4                1745.0                   -154.0      RU  
     5                1548.0                    -15.0      RU  
     6                1237.0                     24.0      RU  
     7                1224.0                      0.0      RU  
     8                1104.0                     -9.0      RU  
     9                 982.0                     16.0      RU  
     10                918.0                     18.0      RU  
     11                736.0                     75.0      RU  
     12                607.0                     91.0      RU  
     13                516.0                     13.0      RU  
     14                485.0                     17.0      RU  
     15                464.0                    102.0      RU  
     16                460.0                      0.0      RU  
     17                437.0                     98.0      RU  
     18                407.0                     14.0      RU  
     19                405.0                     -1.0      RU  
     20              24765.0                    391.0      RU  ,
     'ru1905':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   ru1905     1           海通期货   38781.0   5511.0            永安期货   
     1   ru1905     2           东证期货   23122.0   4306.0            方正中期   
     2   ru1905     3           中信期货   19462.0     69.0            华泰期货   
     3   ru1905     4           方正中期   17452.0   5705.0            国泰君安   
     4   ru1905     5           国投安信   16518.0   3321.0            银河期货   
     5   ru1905     6           中融汇信   12664.0   2777.0            中信期货   
     6   ru1905     7           光大期货   10722.0   2190.0            浙商期货   
     7   ru1905     8           华泰期货    9974.0   4222.0            南华期货   
     8   ru1905     9           永安期货    6802.0   -385.0            瑞达期货   
     9   ru1905    10           申万期货    6585.0   2787.0            弘业期货   
     10  ru1905    11           徽商期货    5731.0   1622.0            广发期货   
     11  ru1905    12           国泰君安    5486.0    361.0            中国国际   
     12  ru1905    13           中信建投    5266.0   1621.0            海通期货   
     13  ru1905    14           冠通期货    4319.0    737.0            国投安信   
     14  ru1905    15           银河期货    4302.0   1375.0            徽商期货   
     15  ru1905    16           国信期货    4002.0    800.0            宏源期货   
     16  ru1905    17           东航期货    3895.0    679.0            中辉期货   
     17  ru1905    18           中国国际    3857.0   1502.0            申万期货   
     18  ru1905    19           东方财富    3713.0    271.0            大地期货   
     19  ru1905    20           南华期货    3632.0    620.0            五矿经易   
     20  ru1905   999           None  206285.0  40091.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               8173.0                   349.0             中银国际   
     1               6117.0                   825.0             中信期货   
     2               4440.0                   110.0             永安期货   
     3               3895.0                   129.0             海通期货   
     4               3590.0                   658.0             国泰君安   
     5               3335.0                  -188.0             银河期货   
     6               3237.0                   197.0             国投安信   
     7               3149.0                   267.0             新湖期货   
     8               2986.0                    80.0             大地期货   
     9               2822.0                   104.0             格林大华   
     10              2510.0                    65.0             东证期货   
     11              2462.0                    83.0             华泰期货   
     12              2405.0                  -682.0             南华期货   
     13              2396.0                    60.0             方正中期   
     14              2211.0                   -72.0             广发期货   
     15              2096.0                    16.0             浙商期货   
     16              2085.0                    91.0             倍特期货   
     17              2076.0                   188.0             建信期货   
     18              2073.0                    75.0             宏源期货   
     19              2002.0                   161.0             中粮期货   
     20             64060.0                  2516.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               16071.0                     25.0      RU  
     1                8978.0                    196.0      RU  
     2                8658.0                    245.0      RU  
     3                8500.0                   1107.0      RU  
     4                7499.0                    175.0      RU  
     5                5439.0                     88.0      RU  
     6                5387.0                    -24.0      RU  
     7                4413.0                     21.0      RU  
     8                4205.0                     -8.0      RU  
     9                3655.0                    541.0      RU  
     10               3285.0                    550.0      RU  
     11               3167.0                    346.0      RU  
     12               2540.0                     35.0      RU  
     13               2401.0                    117.0      RU  
     14               2322.0                     60.0      RU  
     15               2074.0                   -126.0      RU  
     16               2000.0                    530.0      RU  
     17               1912.0                    158.0      RU  
     18               1841.0                    154.0      RU  
     19               1785.0                     92.0      RU  
     20              96132.0                   4282.0      RU  ,
     'ru1901':     symbol  rank vol_party_name      vol  vol_chg long_party_name  \
     0   ru1901     1           海通期货  11821.0    666.0            永安期货   
     1   ru1901     2           东证期货   5231.0   1112.0            海通期货   
     2   ru1901     3           中信期货   4362.0    757.0            中信期货   
     3   ru1901     4           国投安信   2332.0   -212.0            华泰期货   
     4   ru1901     5           中融汇信   2328.0     17.0            方正中期   
     5   ru1901     6           华泰期货   1889.0     42.0            南华期货   
     6   ru1901     7           国泰君安   1750.0     55.0            广发期货   
     7   ru1901     8           大有期货   1639.0    541.0            银河期货   
     8   ru1901     9           方正中期   1525.0    448.0            徽商期货   
     9   ru1901    10           鲁证期货   1423.0    -47.0            浙商期货   
     10  ru1901    11           中银国际   1318.0   -288.0            瑞达期货   
     11  ru1901    12           中辉期货   1247.0     13.0            中大期货   
     12  ru1901    13           格林大华   1154.0    877.0            鲁证期货   
     13  ru1901    14           信达期货   1085.0   -154.0            国海良时   
     14  ru1901    15           永安期货   1020.0    188.0            中国国际   
     15  ru1901    16           国信期货    987.0    164.0            中辉期货   
     16  ru1901    17           银河期货    909.0    159.0            弘业期货   
     17  ru1901    18           中信建投    834.0    375.0            国投安信   
     18  ru1901    19           南华期货    833.0     37.0            国泰君安   
     19  ru1901    20           倍特期货    721.0    587.0            申万期货   
     20  ru1901   999           None  44408.0   5337.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               2670.0                  -113.0             国信期货   
     1               2471.0                  -167.0             永安期货   
     2               2018.0                  -379.0             中粮期货   
     3               1769.0                  -135.0             海通期货   
     4               1684.0                  -212.0             华泰期货   
     5               1515.0                  -164.0             中信期货   
     6               1433.0                   -73.0             银河期货   
     7               1360.0                  -106.0             瑞达期货   
     8               1312.0                  -130.0             格林大华   
     9               1201.0                   -26.0             中信建投   
     10              1165.0                   -27.0             中大期货   
     11              1158.0                  -174.0             国泰君安   
     12              1154.0                   -35.0             新湖期货   
     13              1040.0                   -85.0             建信期货   
     14              1001.0                   -79.0             国富期货   
     15               994.0                   -52.0             国投安信   
     16               985.0                   -25.0             国贸期货   
     17               941.0                   -50.0             中银国际   
     18               922.0                  -153.0             申万期货   
     19               914.0                   -35.0             东证期货   
     20             27707.0                 -2220.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0                4729.0                   -170.0      RU  
     1                3968.0                   -471.0      RU  
     2                3318.0                    -10.0      RU  
     3                3273.0                   -150.0      RU  
     4                2808.0                   -100.0      RU  
     5                2493.0                    -71.0      RU  
     6                2152.0                     -3.0      RU  
     7                2128.0                     14.0      RU  
     8                2113.0                   -610.0      RU  
     9                2048.0                   -300.0      RU  
     10               1701.0                    -85.0      RU  
     11               1616.0                    -63.0      RU  
     12               1510.0                    -19.0      RU  
     13               1419.0                    -12.0      RU  
     14               1394.0                     -5.0      RU  
     15               1249.0                     -8.0      RU  
     16               1050.0                    -60.0      RU  
     17                895.0                    -16.0      RU  
     18                831.0                    -94.0      RU  
     19                716.0                     52.0      RU  
     20              41411.0                  -2181.0      RU  ,
     'sp1906':     symbol  rank vol_party_name       vol  vol_chg long_party_name  \
     0   sp1906     1           海通期货   71031.0   3807.0            永安期货   
     1   sp1906     2           东证期货   66204.0  -3306.0            海通期货   
     2   sp1906     3           申万期货   54580.0 -24061.0            浙商期货   
     3   sp1906     4           国泰君安   48505.0  12693.0            渤海期货   
     4   sp1906     5           中信期货   43689.0  -1257.0            中信建投   
     5   sp1906     6           中银国际   41792.0  19854.0            平安期货   
     6   sp1906     7           徽商期货   39764.0  -4713.0            中信期货   
     7   sp1906     8           广发期货   39469.0  -4417.0            徽商期货   
     8   sp1906     9           华安期货   38025.0  -2017.0            大地期货   
     9   sp1906    10           国投安信   30844.0 -16831.0            广发期货   
     10  sp1906    11           方正中期   29380.0  -4040.0            华安期货   
     11  sp1906    12           华泰期货   28262.0  -5154.0            方正中期   
     12  sp1906    13           铜冠金源   21810.0 -17043.0            银河期货   
     13  sp1906    14           东亚期货   19477.0  -3493.0            国泰君安   
     14  sp1906    15           中信建投   17820.0  -1217.0            东航期货   
     15  sp1906    16           上海中期   17764.0  -2338.0            鲁证期货   
     16  sp1906    17           东方财富   14618.0 -16063.0            国贸期货   
     17  sp1906    18           冠通期货   14241.0   2316.0            五矿经易   
     18  sp1906    19           平安期货   14162.0  -3314.0            光大期货   
     19  sp1906    20           东航期货   13964.0  -2736.0            国投安信   
     20  sp1906   999           None  665401.0 -73330.0            None   
     
         long_open_interest  long_open_interest_chg short_party_name  \
     0               6159.0                   327.0             方正中期   
     1               3875.0                   259.0             永安期货   
     2               3567.0                   -81.0             海通期货   
     3               3317.0                   -70.0             浙商期货   
     4               2514.0                   400.0             国金期货   
     5               2388.0                  -199.0             银河期货   
     6               2365.0                   292.0             五矿经易   
     7               2241.0                    -9.0             华泰期货   
     8               2118.0                  -464.0             国泰君安   
     9               2002.0                    47.0             中信期货   
     10              1934.0                   -92.0             申万期货   
     11              1922.0                    45.0             国富期货   
     12              1921.0                   374.0             南华期货   
     13              1722.0                  -269.0             国投安信   
     14              1645.0                    61.0             建信期货   
     15              1467.0                   338.0             国贸期货   
     16              1441.0                   177.0             中信建投   
     17              1343.0                   471.0             华安期货   
     18              1265.0                  -229.0             宝城期货   
     19              1263.0                   -40.0             徽商期货   
     20             46469.0                  1338.0             None   
     
         short_open_interest  short_open_interest_chg variety  
     0               12652.0                    391.0      SP  
     1                8391.0                  -1325.0      SP  
     2                5229.0                    942.0      SP  
     3                4949.0                   -122.0      SP  
     4                3640.0                    123.0      SP  
     5                3249.0                   -306.0      SP  
     6                3167.0                     29.0      SP  
     7                3106.0                    494.0      SP  
     8                2743.0                   -110.0      SP  
     9                2655.0                   -361.0      SP  
     10               2551.0                     84.0      SP  
     11               1877.0                   -719.0      SP  
     12               1636.0                    195.0      SP  
     13               1536.0                    162.0      SP  
     14               1257.0                     96.0      SP  
     15               1231.0                    945.0      SP  
     16               1162.0                    162.0      SP  
     17               1069.0                    449.0      SP  
     18               1003.0                    -82.0      SP  
     19               1000.0                      9.0      SP  
     20              64103.0                   1056.0      SP  }




```python
ak.get_cffex_rank_table('20181210')
```




    {'IF1812':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 5472                      43            中信期货     1   
     1                 3007                       7            广发期货     2   
     2                 2902                      51            海通期货     3   
     3                 2898                    -118            国泰君安     4   
     4                 2422                      95            华泰期货     5   
     5                 1829                      17            申银万国     6   
     6                 1807                     197            兴证期货     7   
     7                 1752                       9            银河期货     8   
     8                 1451                       4            上海东证     9   
     9                 1411                     -21            永安期货    10   
     10                1240                     145            招商期货    11   
     11                1219                      48            国投安信    12   
     12                1033                     103            光大期货    13   
     13                 959                      31            方正中期    14   
     14                 943                      66            国信期货    15   
     15                 943                      14            中信建投    16   
     16                 928                     171            五矿经易    17   
     17                 728                      15            宏源期货    18   
     18                 725                      61            浙商期货    19   
     19                 707                      24            中金期货    20   
     20               34376                     962            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  symbol  \
     0                  7053                      182             中信期货  IF1812   
     1                  3523                     -110             华泰期货  IF1812   
     2                  3033                     -120             上海东证  IF1812   
     3                  2852                       38             银河期货  IF1812   
     4                  2781                       16             国泰君安  IF1812   
     5                  2294                       19             海通期货  IF1812   
     6                  2150                      147             兴证期货  IF1812   
     7                  1813                      -98             申银万国  IF1812   
     8                  1390                      -91             广发期货  IF1812   
     9                  1299                      -26             国投安信  IF1812   
     10                 1286                      -60             永安期货  IF1812   
     11                 1285                      128             方正中期  IF1812   
     12                 1276                       -2             招商期货  IF1812   
     13                 1008                       42             光大期货  IF1812   
     14                  996                       30             国信期货  IF1812   
     15                  968                      146             五矿经易  IF1812   
     16                  785                      481             瑞银期货  IF1812   
     17                  621                       20             宏源期货  IF1812   
     18                  617                        9             华西期货  IF1812   
     19                  575                      -15             长江期货  IF1812   
     20                37605                      736             None  IF1812   
     
           vol  vol_chg vol_party_name variety  
     0    7705      688           中信期货      IF  
     1    4918      717           海通期货      IF  
     2    4100      457           国泰君安      IF  
     3    4042      391           兴证期货      IF  
     4    3597      411           华泰期货      IF  
     5    2567      556           申银万国      IF  
     6    2253      127           银河期货      IF  
     7    2169       73           五矿经易      IF  
     8    2144      550           国投安信      IF  
     9    2020      -34           广发期货      IF  
     10   1903      289           光大期货      IF  
     11   1781       33           招商期货      IF  
     12   1548      182           上海东证      IF  
     13   1532     -140           中融汇信      IF  
     14   1471      365           方正中期      IF  
     15   1363      291           永安期货      IF  
     16   1330       28           国信期货      IF  
     17   1311      240           浙商期货      IF  
     18   1178      183           中信建投      IF  
     19   1168      269           南华期货      IF  
     20  50100     5676           None      IF  ,
     'IF1903':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 2540                      24            国泰君安     1   
     1                 1061                     -11            国富期货     2   
     2                  885                     122            中信期货     3   
     3                  769                      -1            中银国际     4   
     4                  378                      15            申银万国     5   
     5                  375                      38            海通期货     6   
     6                  357                      22            永安期货     7   
     7                  343                     104            南华期货     8   
     8                  313                      56            方正中期     9   
     9                  298                      12            国投安信    10   
     10                 291                      46            上海东证    11   
     11                 275                     -17            招商期货    12   
     12                 249                      -4            华泰期货    13   
     13                 248                      20            银河期货    14   
     14                 247                     -23            东吴期货    15   
     15                 231                     106            华西期货    16   
     16                 176                      43            中信建投    17   
     17                 176                       2            华联期货    18   
     18                 173                      -8            广发期货    19   
     19                 171                      44            光大期货    20   
     20                9556                     590            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  symbol  \
     0                  2035                      -39             平安期货  IF1903   
     1                  1487                       43             上海东证  IF1903   
     2                  1008                       15             国泰君安  IF1903   
     3                   899                       14             华泰期货  IF1903   
     4                   837                       79             中信期货  IF1903   
     5                   684                        2             银河期货  IF1903   
     6                   579                       22             广发期货  IF1903   
     7                   503                      116             国投安信  IF1903   
     8                   478                       43             兴证期货  IF1903   
     9                   396                       29             海通期货  IF1903   
     10                  395                       82             华西期货  IF1903   
     11                  307                       20             国信期货  IF1903   
     12                  263                      248             瑞银期货  IF1903   
     13                  221                        1             建信期货  IF1903   
     14                  206                       56             永安期货  IF1903   
     15                  202                       99             申银万国  IF1903   
     16                  155                        0             国元期货  IF1903   
     17                  140                      -22             招商期货  IF1903   
     18                  132                      -21             浙商期货  IF1903   
     19                  120                       11             恒泰期货  IF1903   
     20                11047                      798             None  IF1903   
     
          vol  vol_chg vol_party_name variety  
     0    665      163           中信期货      IF  
     1    596      181           华西期货      IF  
     2    399       11           海通期货      IF  
     3    374      -75           中融汇信      IF  
     4    265      250           瑞银期货      IF  
     5    231      -50           国泰君安      IF  
     6    212       48           华泰期货      IF  
     7    206       41           兴证期货      IF  
     8    189       39           国信期货      IF  
     9    186      139           南华期货      IF  
     10   180      102           申银万国      IF  
     11   153       58           浙商期货      IF  
     12   152       66           光大期货      IF  
     13   148       -6           国投安信      IF  
     14   146       30           永安期货      IF  
     15   140      -24           银河期货      IF  
     16   135       68           上海东证      IF  
     17   130       47           恒泰期货      IF  
     18   128        0           广发期货      IF  
     19   127       63           招商期货      IF  
     20  4762     1151           None      IF  ,
     'IC1903':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 2647                      79            中信期货     1   
     1                 1851                      -1            中金期货     2   
     2                 1640                     -11            国富期货     3   
     3                 1382                      -2            华泰期货     4   
     4                  899                      21            广发期货     5   
     5                  869                       3            申银万国     6   
     6                  866                       6            国泰君安     7   
     7                  677                       0            瑞银期货     8   
     8                  445                       6            海通期货     9   
     9                  315                       2            国投安信    10   
     10                 231                     126            华西期货    11   
     11                 209                       5            上海东证    12   
     12                 203                     -20            兴证期货    13   
     13                 200                       3            银河期货    14   
     14                 193                       4            永安期货    15   
     15                 154                      23            五矿经易    16   
     16                 140                      21            光大期货    17   
     17                 133                       8            鲁证期货    18   
     18                 129                      23            浙商期货    19   
     19                 106                      -2            华联期货    20   
     20               13289                     294            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  symbol  \
     0                  1939                       37             中信期货  IC1903   
     1                  1356                       10             永安期货  IC1903   
     2                  1311                       14             东吴期货  IC1903   
     3                  1080                       23             国信期货  IC1903   
     4                   909                      -15             海通期货  IC1903   
     5                   901                       -6             国泰君安  IC1903   
     6                   766                       54             银河期货  IC1903   
     7                   586                       -2             华泰期货  IC1903   
     8                   585                       -6             兴证期货  IC1903   
     9                   530                       20             兴业期货  IC1903   
     10                  493                        4             申银万国  IC1903   
     11                  472                        0             国投安信  IC1903   
     12                  402                        6             上海东证  IC1903   
     13                  306                       11             广发期货  IC1903   
     14                  296                      133             华西期货  IC1903   
     15                  280                       39             南华期货  IC1903   
     16                  260                       12             中金期货  IC1903   
     17                  254                       16             中融汇信  IC1903   
     18                  235                       25             招商期货  IC1903   
     19                  188                       11             格林大华  IC1903   
     20                13149                      386             None  IC1903   
     
          vol  vol_chg vol_party_name variety  
     0    604       -5           中信期货      IC  
     1    583       53           华西期货      IC  
     2    249       73           国信期货      IC  
     3    219       -1           中融汇信      IC  
     4    215      -92           海通期货      IC  
     5    147       82           光大期货      IC  
     6    118      -21           兴证期货      IC  
     7    112       55           新湖期货      IC  
     8    108       18           华泰期货      IC  
     9    103        0           银河期货      IC  
     10   100       78           永安期货      IC  
     11    99       66           南华期货      IC  
     12    86       -7           中信建投      IC  
     13    84      -31           国泰君安      IC  
     14    79        4           东吴期货      IC  
     15    63        3           西部期货      IC  
     16    50       47           招商期货      IC  
     17    48       34           方正中期      IC  
     18    47       25           宏源期货      IC  
     19    44       12           广发期货      IC  
     20  3158      393           None      IC  ,
     'IC1812':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 5382                     -76            中信期货     1   
     1                 2945                     166            国泰君安     2   
     2                 2938                     -24            华泰期货     3   
     3                 1864                      23            海通期货     4   
     4                 1832                     194            国投安信     5   
     5                 1779                      -1            银河期货     6   
     6                 1686                      22            永安期货     7   
     7                 1459                    -378            中金期货     8   
     8                 1297                     -26            五矿经易     9   
     9                 1115                      31            广发期货    10   
     10                1040                      13            上海东证    11   
     11                 833                      53            申银万国    12   
     12                 820                      35            鲁证期货    13   
     13                 763                     112            兴证期货    14   
     14                 654                       1            宏源期货    15   
     15                 645                      -2            光大期货    16   
     16                 561                      -8            招商期货    17   
     17                 538                      17            国信期货    18   
     18                 505                      -6            平安期货    19   
     19                 435                      18            南华期货    20   
     20               29091                     164            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  symbol  \
     0                  5100                     -126             中信期货  IC1812   
     1                  3342                      -17             华泰期货  IC1812   
     2                  2173                      -63             海通期货  IC1812   
     3                  2107                      212             国泰君安  IC1812   
     4                  1939                      173             兴证期货  IC1812   
     5                  1802                       87             上海东证  IC1812   
     6                  1552                     -108             银河期货  IC1812   
     7                  1528                      -41             永安期货  IC1812   
     8                  1512                     -182             光大期货  IC1812   
     9                  1347                      153             国投安信  IC1812   
     10                 1021                      -77             南华期货  IC1812   
     11                  986                      -46             申银万国  IC1812   
     12                  733                      -13             国信期货  IC1812   
     13                  723                      -11             浙商期货  IC1812   
     14                  723                       13             招商期货  IC1812   
     15                  624                       22             广发期货  IC1812   
     16                  621                      -34             五矿经易  IC1812   
     17                  608                      -85             宏源期货  IC1812   
     18                  568                      -48             中信建投  IC1812   
     19                  515                        5             中金期货  IC1812   
     20                29524                     -186             None  IC1812   
     
           vol  vol_chg vol_party_name variety  
     0    5270      -87           中信期货      IC  
     1    3192      434           海通期货      IC  
     2    2402     -155           国泰君安      IC  
     3    2008       81           五矿经易      IC  
     4    1941      283           华泰期货      IC  
     5    1809      122           国投安信      IC  
     6    1779      252           兴证期货      IC  
     7    1632      351           光大期货      IC  
     8    1190      167           宏源期货      IC  
     9    1082     -189           中融汇信      IC  
     10   1077      152           南华期货      IC  
     11   1057       68           银河期货      IC  
     12   1031      188           申银万国      IC  
     13    960      -16           国信期货      IC  
     14    919       64           浙商期货      IC  
     15    854       77           上海东证      IC  
     16    813      149           广发期货      IC  
     17    771       66           中信建投      IC  
     18    745       26           招商期货      IC  
     19    633      108           永安期货      IC  
     20  31165     2141           None      IC  ,
     'IH1812':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 2184                     238            中信期货     1   
     1                 1355                     181            海通期货     2   
     2                 1117                      20            永安期货     3   
     3                 1075                       4            华泰期货     4   
     4                  869                      93            广发期货     5   
     5                  779                     103            国泰君安     6   
     6                  770                      59            上海东证     7   
     7                  640                      34            银河期货     8   
     8                  613                      79            兴证期货     9   
     9                  610                      64            申银万国    10   
     10                 558                      39            五矿经易    11   
     11                 546                      75            光大期货    12   
     12                 529                      27            国信期货    13   
     13                 515                      -4            招商期货    14   
     14                 507                     102            中信建投    15   
     15                 495                      66            国投安信    16   
     16                 470                      56            南华期货    17   
     17                 444                      13            浙商期货    18   
     18                 401                      12            鲁证期货    19   
     19                 359                      83            中融汇信    20   
     20               14836                    1344            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  symbol  \
     0                  2308                      206             中信期货  IH1812   
     1                  1644                      244             国泰君安  IH1812   
     2                  1433                      -70             海通期货  IH1812   
     3                  1377                       35             华泰期货  IH1812   
     4                  1132                      119             广发期货  IH1812   
     5                   988                      115             银河期货  IH1812   
     6                   925                        8             五矿经易  IH1812   
     7                   679                      140             光大期货  IH1812   
     8                   614                       85             国投安信  IH1812   
     9                   577                       -3             中金期货  IH1812   
     10                  570                        8             兴证期货  IH1812   
     11                  515                        3             永安期货  IH1812   
     12                  513                      -25             上海东证  IH1812   
     13                  491                       66             申银万国  IH1812   
     14                  414                      129             平安期货  IH1812   
     15                  393                      -32             招商期货  IH1812   
     16                  369                      100             南华期货  IH1812   
     17                  367                       47             国信期货  IH1812   
     18                  366                      135             国富期货  IH1812   
     19                  336                      -29             建信期货  IH1812   
     20                16011                     1281             None  IH1812   
     
           vol  vol_chg vol_party_name variety  
     0    3300     -329           中信期货      IH  
     1    2569      270           海通期货      IH  
     2    1719      194           国泰君安      IH  
     3    1559      515           五矿经易      IH  
     4    1187       46           华泰期货      IH  
     5    1149      124           兴证期货      IH  
     6    1047      128           光大期货      IH  
     7     945      213           国投安信      IH  
     8     930       51           广发期货      IH  
     9     908      158           招商期货      IH  
     10    856      167           南华期货      IH  
     11    829     -118           中融汇信      IH  
     12    824       92           鲁证期货      IH  
     13    694      201           申银万国      IH  
     14    680      152           国信期货      IH  
     15    633      104           银河期货      IH  
     16    628       -8           上海东证      IH  
     17    621       44           永安期货      IH  
     18    509        1           浙商期货      IH  
     19    509       12           中信建投      IH  
     20  22096     2017           None      IH  ,
     'T1903':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 6693                     -58            国泰君安     1   
     1                 4907                     -77            中信期货     2   
     2                 4732                      64            银河期货     3   
     3                 3627                      46            浙商期货     4   
     4                 3258                       3            中金期货     5   
     5                 3193                     -96            海通期货     6   
     6                 2574                      31            新湖期货     7   
     7                 2558                      35            广发期货     8   
     8                 2464                    -135            永安期货     9   
     9                 2337                      11            南华期货    10   
     10                1962                       7            国富期货    11   
     11                1688                     210            华泰期货    12   
     12                1582                     -48            天风期货    13   
     13                1523                     -25            鲁证期货    14   
     14                1511                      58            国投安信    15   
     15                1407                      69            上海东证    16   
     16                1293                      24            建信期货    17   
     17                1211                   -1190            五矿经易    18   
     18                1171                     -23            招商期货    19   
     19                1063                      86            中信建投    20   
     20               50754                   -1008            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name symbol  \
     0                  8595                      626             中信期货  T1903   
     1                  7660                        1             国泰君安  T1903   
     2                  6105                      -59             永安期货  T1903   
     3                  5848                       22             银河期货  T1903   
     4                  5749                      -92             海通期货  T1903   
     5                  3696                       37             广发期货  T1903   
     6                  2610                     -217             国金期货  T1903   
     7                  1935                      -37             宝城期货  T1903   
     8                  1686                       44             国海良时  T1903   
     9                  1663                        2             华西期货  T1903   
     10                 1487                     -160             天风期货  T1903   
     11                 1469                       81             华安期货  T1903   
     12                 1275                      -25             华泰期货  T1903   
     13                 1143                     -130             平安期货  T1903   
     14                 1052                      -10             大有期货  T1903   
     15                  953                      -40             鲁证期货  T1903   
     16                  934                      -32             东海期货  T1903   
     17                  881                     -417             浙商期货  T1903   
     18                  791                      -12             光大期货  T1903   
     19                  681                      -25             方正中期  T1903   
     20                56213                     -443             None  T1903   
     
           vol  vol_chg vol_party_name variety  
     0    8676     1316           海通期货       T  
     1    6895        2           中信期货       T  
     2    5801      629           国泰君安       T  
     3    4735     -262           国投安信       T  
     4    3608     -257           天风期货       T  
     5    3327     -396           上海东证       T  
     6    2634     -796           华鑫期货       T  
     7    2404     -649           国金期货       T  
     8    1641    -1471           鲁证期货       T  
     9    1539       99           华泰期货       T  
     10   1474      400           西部期货       T  
     11   1397       66           中信建投       T  
     12   1378      691           五矿经易       T  
     13   1198      671           东吴期货       T  
     14   1193      195           浙商期货       T  
     15   1089     -268           徽商期货       T  
     16   1088     -791           广发期货       T  
     17   1062     -498           永安期货       T  
     18   1038     -169           申银万国       T  
     19   1007     -130           国信期货       T  
     20  53184    -1618           None       T  ,
     'T1812':    long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 392                       0            平安期货     1   
     1                 175                       0            银河期货     2   
     2                   0                       0            永安期货     3   
     3                   0                       0            中信期货     4   
     4                   0                       0            国金期货     5   
     5                   0                       0            华西期货     6   
     6                 567                       0            None   999   
     
        short_open_interest  short_open_interest_chg short_party_name symbol  vol  \
     0                  360                        0             永安期货  T1812    0   
     1                  132                        0             国金期货  T1812    0   
     2                   50                        0             中信期货  T1812    0   
     3                   25                        0             华西期货  T1812    0   
     4                    0                        0             平安期货  T1812    0   
     5                    0                        0             银河期货  T1812    0   
     6                  567                        0             None  T1812    0   
     
        vol_chg vol_party_name variety  
     0        0           永安期货       T  
     1        0           中信期货       T  
     2        0           平安期货       T  
     3        0           银河期货       T  
     4        0           国金期货       T  
     5        0           华西期货       T  
     6        0           None       T  ,
     'TF1812':    long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                  80                    -400            国金期货     1   
     1                  55                    -381            平安期货     2   
     2                   5                    -674            永安期货     3   
     3                   0                       0            宏源期货     4   
     4                   0                       0            上海东证     5   
     5                   0                       0            中金期货     6   
     6                 140                   -1455            None   999   
     
        short_open_interest  short_open_interest_chg short_party_name  symbol  vol  \
     0                  120                        0             中金期货  TF1812    0   
     1                   20                        0             上海东证  TF1812    0   
     2                    0                        0             永安期货  TF1812    0   
     3                    0                        0             平安期货  TF1812    0   
     4                    0                        0             国金期货  TF1812    0   
     5                    0                    -1455             宏源期货  TF1812    0   
     6                  140                    -1455             None  TF1812    0   
     
        vol_chg vol_party_name variety  
     0        0           永安期货      TF  
     1        0           平安期货      TF  
     2        0           国金期货      TF  
     3        0           宏源期货      TF  
     4        0           上海东证      TF  
     5        0           中金期货      TF  
     6        0           None      TF  ,
     'TF1903':     long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                 2089                      28            新湖期货     1   
     1                 1646                      98            中信期货     2   
     2                 1528                       0            国富期货     3   
     3                 1407                      26            国泰君安     4   
     4                  999                      76            广发期货     5   
     5                  997                      78            中金期货     6   
     6                  695                      30            银河期货     7   
     7                  650                       0            和融期货     8   
     8                  499                      -6            国贸期货     9   
     9                  486                       7            天风期货    10   
     10                 449                     -29            平安期货    11   
     11                 352                       2            海通期货    12   
     12                 350                      -6            上海东证    13   
     13                 278                      -3            方正中期    14   
     14                 273                       0            中信建投    15   
     15                 244                      32            华泰期货    16   
     16                 226                      11            永安期货    17   
     17                 211                       0            广州期货    18   
     18                 188                      12            兴证期货    19   
     19                 162                       3            国信期货    20   
     20               13729                     359            None   999   
     
         short_open_interest  short_open_interest_chg short_party_name  symbol  \
     0                  2019                      -11             永安期货  TF1903   
     1                  1748                       -3             海通期货  TF1903   
     2                  1528                      -31             格林大华  TF1903   
     3                  1381                       13             中信期货  TF1903   
     4                  1220                        0             方正中期  TF1903   
     5                  1122                        5             广发期货  TF1903   
     6                   990                        0             国金期货  TF1903   
     7                   832                      214             天风期货  TF1903   
     8                   412                       24             银河期货  TF1903   
     9                   406                       52             上海东证  TF1903   
     10                  399                       64             第一创业  TF1903   
     11                  377                      -12             国海良时  TF1903   
     12                  367                      194             中信建投  TF1903   
     13                  326                        0             恒泰期货  TF1903   
     14                  324                        0             光大期货  TF1903   
     15                  293                      -18             国泰君安  TF1903   
     16                  236                       23             平安期货  TF1903   
     17                  228                       -3             华安期货  TF1903   
     18                  160                     -100             上海大陆  TF1903   
     19                  159                        0             一德期货  TF1903   
     20                14527                      411             None  TF1903   
     
          vol  vol_chg vol_party_name variety  
     0   1741      169           中信期货      TF  
     1    850       84           上海东证      TF  
     2    650       12           华鑫期货      TF  
     3    536      -79           中信建投      TF  
     4    386      -62           国泰君安      TF  
     5    374       92           光大期货      TF  
     6    367      129           西部期货      TF  
     7    281      -23           国海良时      TF  
     8    271     -316           海通期货      TF  
     9    243       49           天风期货      TF  
     10   241      -38           华泰期货      TF  
     11   229     -176           广发期货      TF  
     12   202      -64           金瑞期货      TF  
     13   170      -80           华西期货      TF  
     14   167       17           招商期货      TF  
     15   164      -86           第一创业      TF  
     16   147       41           新湖期货      TF  
     17   143      -12           国信期货      TF  
     18   127       99           中辉期货      TF  
     19   121     -120           南华期货      TF  
     20  7410     -364           None      TF  ,
     'TS1812':    long_open_interest  long_open_interest_chg long_party_name  rank  \
     0                   0                    -170            永安期货     1   
     1                   0                       0            宏源期货     2   
     2                   0                     -10            中金期货     3   
     3                   0                     -20            乾坤期货     4   
     4                   0                    -200            None   999   
     
        short_open_interest  short_open_interest_chg short_party_name  symbol  vol  \
     0                    0                        0             永安期货  TS1812    0   
     1                    0                     -200             宏源期货  TS1812    0   
     2                    0                        0             中金期货  TS1812    0   
     3                    0                        0             乾坤期货  TS1812    0   
     4                    0                     -200             None  TS1812    0   
     
        vol_chg vol_party_name variety  
     0        0           永安期货      TS  
     1        0           宏源期货      TS  
     2        0           中金期货      TS  
     3        0           乾坤期货      TS  
     4        0           None      TS  }



### 日线行情获取


```python
ak.get_futures_daily(start='20181210', end='20181210', market='DCE', index_bar=True)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>symbol</th>
      <th>date</th>
      <th>open</th>
      <th>high</th>
      <th>low</th>
      <th>close</th>
      <th>volume</th>
      <th>open_interest</th>
      <th>turnover</th>
      <th>settle</th>
      <th>pre_settle</th>
      <th>variety</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>A1901</td>
      <td>20181210</td>
      <td>3210</td>
      <td>3232</td>
      <td>3204</td>
      <td>3214</td>
      <td>83178</td>
      <td>197702</td>
      <td>267514</td>
      <td>3216</td>
      <td>3224</td>
      <td>A</td>
    </tr>
    <tr>
      <td>1</td>
      <td>A1903</td>
      <td>20181210</td>
      <td>3269</td>
      <td>3270</td>
      <td>3268</td>
      <td>3268</td>
      <td>12</td>
      <td>290</td>
      <td>39.23</td>
      <td>3269</td>
      <td>3275</td>
      <td>A</td>
    </tr>
    <tr>
      <td>2</td>
      <td>A1905</td>
      <td>20181210</td>
      <td>3470</td>
      <td>3470</td>
      <td>3438</td>
      <td>3455</td>
      <td>33900</td>
      <td>98294</td>
      <td>116981</td>
      <td>3450</td>
      <td>3467</td>
      <td>A</td>
    </tr>
    <tr>
      <td>3</td>
      <td>A1907</td>
      <td>20181210</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>3473</td>
      <td>0</td>
      <td>4</td>
      <td>0</td>
      <td>3473</td>
      <td>3473</td>
      <td>A</td>
    </tr>
    <tr>
      <td>4</td>
      <td>A1909</td>
      <td>20181210</td>
      <td>3529</td>
      <td>3529</td>
      <td>3507</td>
      <td>3525</td>
      <td>954</td>
      <td>8158</td>
      <td>3357.5</td>
      <td>3519</td>
      <td>3530</td>
      <td>A</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>185</td>
      <td>Y99</td>
      <td>20181210</td>
      <td>5373.8</td>
      <td>5408.28</td>
      <td>5354.01</td>
      <td>5365.09</td>
      <td>429904</td>
      <td>1.04699e+06</td>
      <td>2.30961e+06</td>
      <td>5381.89</td>
      <td>5424.48</td>
      <td>Y</td>
    </tr>
    <tr>
      <td>186</td>
      <td>P99</td>
      <td>20181210</td>
      <td>4389.51</td>
      <td>4422.7</td>
      <td>4367.57</td>
      <td>4403.84</td>
      <td>398116</td>
      <td>653060</td>
      <td>1.76773e+06</td>
      <td>4397.47</td>
      <td>4404.21</td>
      <td>P</td>
    </tr>
    <tr>
      <td>187</td>
      <td>I99</td>
      <td>20181210</td>
      <td>484.549</td>
      <td>487.042</td>
      <td>477.313</td>
      <td>483.022</td>
      <td>1.47904e+06</td>
      <td>951204</td>
      <td>7.11175e+06</td>
      <td>482.368</td>
      <td>478.908</td>
      <td>I</td>
    </tr>
    <tr>
      <td>188</td>
      <td>B99</td>
      <td>20181210</td>
      <td>3084.82</td>
      <td>3095.65</td>
      <td>3062.23</td>
      <td>3072.89</td>
      <td>318162</td>
      <td>204754</td>
      <td>987145</td>
      <td>3077.4</td>
      <td>3096.56</td>
      <td>B</td>
    </tr>
    <tr>
      <td>189</td>
      <td>V99</td>
      <td>20181210</td>
      <td>6408.89</td>
      <td>6416.76</td>
      <td>6273.07</td>
      <td>6313.3</td>
      <td>315750</td>
      <td>403606</td>
      <td>1.01024e+06</td>
      <td>6332.13</td>
      <td>6411.12</td>
      <td>V</td>
    </tr>
  </tbody>
</table>
<p>190 rows × 12 columns</p>
</div>



### 获取奇货可查指数


```python
ak.get_qhkc_data()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>2013-01-04</td>
      <td>1000</td>
    </tr>
    <tr>
      <td>1</td>
      <td>2013-01-07</td>
      <td>999.778</td>
    </tr>
    <tr>
      <td>2</td>
      <td>2013-01-08</td>
      <td>999.535</td>
    </tr>
    <tr>
      <td>3</td>
      <td>2013-01-09</td>
      <td>996.662</td>
    </tr>
    <tr>
      <td>4</td>
      <td>2013-01-10</td>
      <td>997.957</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>1636</td>
      <td>2019-09-24</td>
      <td>1126.26</td>
    </tr>
    <tr>
      <td>1637</td>
      <td>2019-09-25</td>
      <td>1126.36</td>
    </tr>
    <tr>
      <td>1638</td>
      <td>2019-09-26</td>
      <td>1121.67</td>
    </tr>
    <tr>
      <td>1639</td>
      <td>2019-09-27</td>
      <td>1115.25</td>
    </tr>
    <tr>
      <td>1640</td>
      <td>2019-09-30</td>
      <td>1117.81</td>
    </tr>
  </tbody>
</table>
<p>1641 rows × 2 columns</p>
</div>




```python

```

