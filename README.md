# [AkShare](https://github.com/jindaxiang/akshare)
(更新于 2019-10-17; 如发现库和文档问题, 请联系 [AkShare](https://github.com/jindaxiang/akshare) 作者: jindaxiang@163.com)
## [AkShare](https://github.com/jindaxiang/akshare) 的介绍

首先要特别感谢 [FuShare](https://github.com/jindaxiang/fushare), [TuShare](https://github.com/waditu/tushare) 在代码和项目开发上对本项目提供的借鉴和学习的机会!

[AkShare](https://github.com/jindaxiang/akshare) 已经于 **2019-10-08** 正式发布, 请访问 [AkShare文档](https://akshare.readthedocs.io) 了解和查询数据接口！

[AkShare](https://github.com/jindaxiang/akshare) 是基于 Python 的开源数据接口库, 目的是实现对期货, 期权, 基金等衍生金融产品和另类数据从数据采集, 数据清洗加工, 到数据下载的工具, 满足金融数据科学家, 数据科学爱好者在数据获取方面的需求. 它的特点是利用 [AkShare](https://github.com/jindaxiang/akshare) 获取的是基于交易所公布的原始数据, 广大数据科学家可以利用原始数据进行再加工, 得出科学的结论.

**后续会基于最新的学术研究论文和券商的金融工程报告添加更多的期货基本面指标和计算方法, 敬请关注**
## [AkShare](https://github.com/jindaxiang/akshare) 的作者

**[Albert King](https://www.jfds.xyz/)** 致力于金融衍生品定价和价格预测, 机器学习在金融领域的应用等研究.

<img src="https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/icon/images.jpg" width = 20% height = 10% align = center/>

## [AkShare](https://github.com/jindaxiang/akshare) 的特色
[AkShare](https://github.com/jindaxiang/akshare) 主要改进如下:
1. Python 语法符合 [PEP8](https://www.python.org/dev/peps/pep-0008/) 规范, 统一接口函数的命名;
2. 增加代码类型注释;
3. 支持 Python 3.7 以上版本的 Python;
4. 后续加入 [asyncio](https://www.python.org/dev/peps/pep-3156/) 和 [aiohttp](https://aiohttp.readthedocs.io/en/stable/) 做异步爬虫加速;
5. 持续维护由于原网站格式变化导致的部分函数运行异常的问题;
6. 增加更多的网络数据采集接口:

    6.1 增加[奇货可查网站](https://qhkch.com/)数据接口, 目前已经提供奇货可查指数数据部分(已完成);
    
    6.2 增加[智道智科网站](https://www.ziasset.com/)数据接口, 目前已经提供私募指数数据部分(已完成);
    
    6.3 增加[99期货网](http://www.99qh.com/)数据接口, 目前已经提供大宗商品库存数据部分(已完成);
    
    6.4 增加[商品期权](https://github.com/jindaxiang/akshare)数据接口, 目前已经提供大宗商品库存数据部分(开发中);
    
    6.5 增加主要国家股票市场指数数据接口(开发中);
    
7. 后续更新主要集中在增加更多数据接口, 同时修复源代码中 bug;
8. 更加完善的接口文档, 提高 [AkShare](https://github.com/jindaxiang/akshare) 的易用性;
9. 希望您能参与 [AkShare](https://github.com/jindaxiang/akshare) 的维护与管理.


## [AkShare](https://github.com/jindaxiang/akshare) 的初衷
![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/index/stock_futures_index.png)

上图是利用 [AkShare](https://github.com/jindaxiang/akshare) 的 **get_zdzk_fund_index** 接口获取的[智道智科](https://www.ziasset.com/company/)发布的股票策略指数和管理期货策略指数.

可以清晰的看到股票策略的波动性远远大于管理期货策略, 从 2015 年至今, 管理期货策略能获得较稳定的收益.

再结合传统的 CTA 策略以趋势为主, 但是自从 2017 年以来, 无论是长线还是短线的趋势策略都受制于商品波动率的降低, 面临了多多少少的回撤, 
同时市场也逐渐趋于机构化理性化, 因此在传统 CTA 策略的基础上加入基本面的因素显得迫在眉睫. 近几年各券商的研报陆续提出了许多依赖于趋势行情以外的有效信号, 它们的表现都与趋势策略有着很低的甚至负的相关性, 这样通过多种不同类型的信号对冲得到的策略, 就有机会在市场上取得非常棒的夏普率和稳定的收益. 

**上图调用 [AkShare](https://github.com/jindaxiang/akshare) 的绘制的代码如下**
```python
import akshare as ak
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

stock_df = ak.get_zdzk_fund_index(30, plot=False)  # 股票策略数据
futures_df = ak.get_zdzk_fund_index(32, plot=False)  # 管理期货策略数据

fig = plt.figure(111, figsize=(20, 10), dpi=300)
adjust_stock_df = stock_df["20150102":] / stock_df["20150102"] * 1000
adjust_stock_df.plot(linewidth=4)
adjust_futures_df = futures_df["20150102":] / futures_df["20150102"] * 1000
adjust_futures_df.plot(linewidth=4)
plt.title("智道智科股票策略和管理期货策略指数")
plt.legend()
plt.show()
```
[AkShare](https://github.com/jindaxiang/akshare) 希望能向各位同仁提供一个网络数据采集接口, 助力个人
投资者、机构投资者、各大研究机构方便的搜集和整理关于金融衍生品, 尤其是期货基本面相关的数据. 


# 安装方法
```
pip install akshare
```

# 升级方法
**p.s. 由于目前版本更新迭代比较频繁, 请在使用前先升级库**
```
pip install akshare --upgrade
```


# 快速入门

## 1. 先按照 [Anaconda安装说明及环境配置](#Anaconda安装说明及环境配置)
## 2. 查看 [AkShare](https://github.com/jindaxiang/akshare) 提供的数据获取接口

**Example 2.1** 查看 [AkShare](https://github.com/jindaxiang/akshare) 提供的数据获取接口

代码:

```python
import akshare as ak
[item for item in dir(ak) if item.startswith("get")]
```

结果显示: 数据获取函数说明

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
 # 智道智科-私募指数数据
 'get_zdzk_fund_index'  # 获取智道智科-私募指数数据
 # 提供英为财情数据接口
 'get_investing_index'  # 提供英为财情-股票指数-全球股指与期货指数数据接口
```

## 3. 案例演示

### 3. 获取展期收益率

**Example 3.1** 获取展期收益率数据:

代码:

```python
import akshare as ak
ak.get_roll_yield_bar(type_method="date", var="RB", start_day="20180618", end_day="20180718", plot=True)
```

结果显示：日期, 展期收益率, 最近合约, 下一期合约

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

### 4. 获取私募指数数据

**Example 4.1** 获取私募指数数据:

代码:

```python
import akshare as ak
ak.get_zdzk_fund_index(index_type=32, plot=True)
```

结果显示：日期, 指数数值

```
2014-12-26    1000.000000
2015-01-02     985.749098
2015-01-09    1032.860242
2015-01-16    1039.978586
2015-01-23    1046.235945
                 ...     
2019-08-23    1390.816835
2019-08-30    1397.684642
2019-09-06    1402.711847
2019-09-13    1401.723599
2019-09-20    1386.570103
Name: 智道管理期货指数, Length: 248, dtype: float64
```

# [AkShare](https://github.com/jindaxiang/akshare) 数据字典

## [AkShare](https://github.com/jindaxiang/akshare) 期货数据

### 期货基础信息

#### 期货交易所

| **交易所名称**    | **交易所代码** | **合约后缀** | **首页地址**|
| ------------------ | ---------- | -------- | --------|
| [中国金融期货交易所](http://www.cffex.com.cn/) | CFFEX      | .CFX     | http://www.cffex.com.cn/|
| [上海期货交易所](http://www.shfe.com.cn/) | SHFE       | .SHF     | http://www.shfe.com.cn/|
| [上海国际能源交易中心](http://www.ine.cn/) | INE        | .INE     | http://www.ine.cn/|
| [郑州商品交易所](http://www.czce.com.cn/) | CZCE       | .ZCE     | http://www.czce.com.cn/|
| [大连商品交易所](http://www.dce.com.cn/) | DCE        | .DCE     | http://www.dce.com.cn/|

#### 金融期货

##### 中国金融期货交易所

| 代码        | 名称            | 代码        | 名称               |
|-------------|-----------------|-------------|--------------------|
| IC9999.CCFX | 中证500主力合约 | T9999.CCFX  | 10年期国债主力合约 |
| IF9999.CCFX | 沪深300主力合约 | TF9999.CCFX | 5年期国债主力合约  |
| IH9999.CCFX | 上证50主力合约  | TS9999.CCFX | 2年期国债主力合约  |

#### 商品期货

##### 上海国际能源交易中心

| 名称     | 主力合约代码 | 指数合约代码 |
|----------|--------------|--------------|
| 原油合约 | SC9999.XINE  | SC8888.XINE  |
| 20号胶合约 | NR9999.XINE | NR8888.XINE |

##### 上海期货交易所

| 名称         | 主力合约代码 | 指数合约代码 |
|--------------|--------------|--------------|
| 白银合约     | AG9999.XSGE  | AG8888.XSGE  |
| 铝合约       | AL9999.XSGE  | AL8888.XSGE  |
| 黄金合约     | AU9999.XSGE  | AU8888.XSGE  |
| 沥青合约     | BU9999.XSGE  | BU8888.XSGE  |
| 铜合约       | CU9999.XSGE  | CU8888.XSGE  |
| 燃料油合约   | FU9999.XSGE  | FU8888.XSGE  |
| 热轧卷板合约 | HC9999.XSGE  | HC8888.XSGE  |
| 镍合约       | NI9999.XSGE  | NI8888.XSGE  |
| 铅合约       | PB9999.XSGE  | PB8888.XSGE  |
| 螺纹钢合约   | RB9999.XSGE  | RB8888.XSGE  |
| 天然橡胶合约 | RU9999.XSGE  | RU8888.XSGE  |
| 锡合约       | SN9999.XSGE  | SN8888.XSGE  |
| 线材合约     | WR9999.XSGE  | WR8888.XSGE  |
| 锌合约       | ZN9999.XSGE  | ZN8888.XSGE  |
| 纸浆合约     | SP9999.XSGE  | SP8888.XSGE  |
| 不锈钢合约 | SS9999.XSGE | SS8888.XSGE |

##### 郑州商品交易所

| 名称         | 主力合约代码 | 指数合约代码 | 备注                                   |
|--------------|--------------|--------------|----------------------------------------|
| 苹果合约     | AP9999.XZCE  | AP8888.XZCE  |                                        |
| 棉花合约     | CF9999.XZCE  | CF8888.XZCE  |                                        |
| 棉纱合约     | CY9999.XZCE  | CY8888.XZCE  |                                        |
| 早籼稻合约   | ER9999.XZCE  | ER8888.XZCE  |                                        |
| 玻璃合约     | FG9999.XZCE  | FG8888.XZCE  |                                        |
| 绿豆合约     | GN9999.XZCE  | GN8888.XZCE  | 已于2009年5月5日退市                   |
| 粳稻谷合约   | JR9999.XZCE  | JR8888.XZCE  |                                        |
| 晚籼稻合约   | LR9999.XZCE  | LR8888.XZCE  |                                        |
| 甲醇合约     | MA9999.XZCE  | MA8888.XZCE  | MA为新的甲醇合约代码, 自MA1506开始执行 |
| 甲醇合约     | ME9999.XZCE  | ME8888.XZCE  | ME为旧的甲醇合约代码, 自ME1505停止执行 |
| 菜籽油合约   | OI9999.XZCE  | OI8888.XZCE  |                                        |
| 普麦合约     | PM9999.XZCE  | PM8888.XZCE  |                                        |
| 早籼稻合约   | RI9999.XZCE  | RI8888.XZCE  |                                        |
| 菜籽粕合约   | RM9999.XZCE  | RM8888.XZCE  |                                        |
| 菜籽油合约   | RO9999.XZCE  | RO8888.XZCE  |                                        |
| 油菜籽合约   | RS9999.XZCE  | RS8888.XZCE  |                                        |
| 硅铁合约     | SF9999.XZCE  | SF8888.XZCE  |                                        |
| 锰硅合约     | SM9999.XZCE  | SM8888.XZCE  |                                        |
| 白糖合约     | SR9999.XZCE  | SR8888.XZCE  |                                        |
| PTA合约      | TA9999.XZCE  | TA8888.XZCE  |                                        |
| 动力煤合约   | TC9999.XZCE  | TC8888.XZCE  |                                        |
| 强麦合约     | WH9999.XZCE  | WH8888.XZCE  | WH为新的强麦合约代码, 自WH1307开始执行 |
| 强麦合约     | WS9999.XZCE  | WS8888.XZCE  | WS为旧的强麦合约代码, 自WS1305停止执行 |
| 硬白小麦合约 | WT9999.XZCE  | WT8888.XZCE  |                                        |
| 动力煤合约   | ZC9999.XZCE  | ZC8888.XZCE  |                                        |
| 红枣合约     | CJ9999.XZCE  | CJ8888.XZCE  |                                        |
| 尿素合约 | UR9999.XZCE | UR888.XZCE | |

##### 大连商品交易所

| 名称         | 主力合约代码 | 指数合约代码 |
|--------------|--------------|--------------|
| 豆一合约     | A9999.XDCE   | A8888.XDCE   |
| 豆二合约     | B9999.XDCE   | B8888.XDCE   |
| 胶合板合约   | BB9999.XDCE  | BB8888.XDCE  |
| 玉米合约     | C9999.XDCE   | C8888.XDCE   |
| 玉米淀粉合约 | CS9999.XDCE  | CS8888.XDCE  |
| 纤维板合约   | FB9999.XDCE  | FB8888.XDCE  |
| 铁矿石合约   | I9999.XDCE   | I8888.XDCE   |
| 焦炭合约     | J9999.XDCE   | J8888.XDCE   |
| 鸡蛋合约     | JD9999.XDCE  | JD8888.XDCE  |
| 焦煤合约     | JM9999.XDCE  | JM8888.XDCE  |
| 聚乙烯合约   | L9999.XDCE   | L8888.XDCE   |
| 豆粕合约     | M9999.XDCE   | M8888.XDCE   |
| 棕榈油合约   | P9999.XDCE   | P8888.XDCE   |
| 聚丙烯合约   | PP9999.XDCE  | PP8888.XDCE  |
| 聚氯乙烯合约 | V9999.XDCE   | V8888.XDCE   |
| 豆油合约     | Y9999.XDCE   | Y8888.XDCE   |
| 乙二醇合约   | EG9999.XDCE  | EG8888.XDCE  |
| 粳米合约     | RR9999.XDCE  | RR8888.XDCE |
| 苯乙烯合约   | EB9999.XDCE  | EB8888.XDCE |

### 期货基础名词

#### 连续合约

需要注意, 由于期货合约存续的特殊性, 针对每一品种的期货合约, 系统中都增加了主力连续合约以及指数连续合约两个人工合成的合约来满足使用需求. 

#### 主力连续合约
主力连续合约：合约首次上市时, 以当日收盘同品种持仓量最大者作为从第二个交易日开始的主力合约. 当同品种其他合约持仓量在收盘后超过当前主力合约1.1倍时, 从第二个交易日开始进行主力合约的切换. 
日内不会进行主力合约的切换. 主力连续合约是由该品种期货不同时期主力合约接续而成, 代码以88或888结尾结尾, 例如 IF88 或 IF888. 前者为合约量价数据的简单拼接, 未做平滑处理;  后者对价格进行了”平滑”处理, 处理规则如下：以主力合约切换前一天（T-1日）新、旧两个主力合约收盘价做差,  之后将 T-1 日及以前的主力连续合约的所有价格水平整体加上或减去该价差, 以”整体抬升”或”整体下降”主力合约的价格水平, 成交量、持仓量均不作调整, 成交额统一设置为0.

#### 指数连续合约
指数连续合约：由当前品种全部可交易合约以累计持仓量为权重加权平均得到, 代码以99结尾, 例如 IF99. 

#### 展期收益率
展期收益率是由不同交割月的价差除以相隔月份数计算得来, 它反映了市场对该品种在近期交割和远期交割的价差预期.

### 期货基础数据

#### 库存数据

库存数据是从[99期货网站](http://www.99qh.com/d/store.aspx)获取的日频率数据, 
由于网站限制, 目前可以利用本接口获取历史数据的图片格式和近期数据的 **pandas.DataFrame** 格式. 调用例子如下: 

接口：get_inventory_data

目标地址: http://www.99qh.com/d/store.aspx

描述：获取大宗商品库存数据

限量：单次一个市场的某个具体品种, 请用 **help(get_inventory_data)** 查看使用方法

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| exchange | int  | Y    |  默认参数 exchange=1 对应上海期货交易所, 请用 **help(get_inventory_data)** 查看参数|
| symbol | int  | Y    |  默认参数 symbol=6, 对应上海期货交易所-铜, 请用 **help(get_inventory_data)** 查看参数|
| plot | Bool  | Y    |  默认参数 plot=True, 是否输出历史数据图片|


输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| ------------ | ----- | -------- | ---------------- |
| 日期          | str   | Y        | 日期     |
| 库存          | str   | Y        | 库存数据(对应图片左边的Y轴)     |
| 增减          | str   | Y        | 相对前一个交易日的增减     |



接口示例

p.s. 由于[99期货网站](http://www.99qh.com/d/store.aspx)服务器不稳定, 请加
try ... except 语句, 如下格式; 另外请关注图片下载的路径, 会自动 **print** 出来
```python
import akshare as ak
for i in range(10):
    try:
        data = ak.get_inventory_data(exchange=1, symbol=6, plot=True)
        print(data)
        break
    except:
        continue
```

数据示例
```
   0           1           2           3           4           5           6   \
0  日期  2019-10-11  2019-09-30  2019-09-27  2019-09-20  2019-09-12  2019-09-06   
1  库存      134509      118108      117455      141379      152188      162059   
2  增减       16401         653      -23924       10809       -9871       18183   
           7           8           9           10  
0  2019-08-30  2019-08-23  2019-08-16  2019-08-09  
1      143876      156573      162830      156367  
2      -12697       -6257        6463         396 
```

图片示例

p.s.**库存(左轴)-绿色**, **增减(右轴)-蓝色**
![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/inventory/shfe_cu.jpg)


#### 展期收益率
展期收益率是由不同交割月的价差除以相隔月份数计算得来, 它反映了市场对该品种在近期交割和远期交割的价差预期. 

在 [AkShare](https://github.com/jindaxiang/akshare) 中可以通过 **get_roll_yield_bar** 接口下载展期收益率数据.

这里展期收益率列表的序列类型分为三种, 分别可以通过:

    1. type_method = "date"  # 某商品品种在不同日期的主力合约和次主力合约的价差组成
    2. type_method = "symbol"  # 某商品品种在某天的所有交割月合约价格组成, 可以很方便的观察该品种从近期到远期的展期结构
    3. type_method = "var"  # 某交易日, 所有品种的主力次主力合约展期收益率的组合, 可以方便的找到展期收益率高的品种和低的品种

来获取.

其中 "date" 类型, 调用方法例子为:
```
ak.get_roll_yield_bar(type_method="date", var="RB", date="20191008", plot=True)
```

其中 "symbol" 类型, 调用方法例子为: 
```
ak.get_roll_yield_bar(type_method="symbol", var="RB", date="20191008", plot=True)
```

其中 "var" 类型, 调用方法例子为: 
```
ak.get_roll_yield_bar(type_method="var", date="20191008", plot=True)
```

利用 **get_roll_yield** 接口, 可以找到特定合约特定日期的主力合约次主力合约展期收益率, 或通过 symbol1 和 symbol2 变量自定义某两个合约的展期收益率. 

```
ak.get_roll_yield(date="20180718", var="IF", symbol1="IF1812", symbol2="IF1811"), 如下图所示: 
```

注意: 
    
    1. 主力合约和次主力合约的定义, 是由该日的各交割月合约持仓量由大到小排序得到.


#### 注册仓单
注册仓单是由各交易所的公布的日级数据, 在一定程度上可以反映市场的库存变化. 调用例子如下: 
```python
import akshare as ak
ak.get_receipt(start_day="20180712", end_day="20180719", vars_list=["CU", "NI"])
```

注意:

    1. vars_list 变量接上需要爬取的品种列表, 即使是一个品种, 也需要以列表形式输入;
    
    2. 在研究仓单的方向变化时, 需要考虑一些品种的年度周期性, 如农产品的收割季、工业品的开工季等;
    
    3. 需考虑到交割日的仓单变化.


#### 现货价格和基差
基差是商品期货非常重要的基本面因素. 这里提供两种获取基差的方法: 
获取当天的基差数据
```python
import akshare as ak
ak.get_spot_price("20180712")
```
返回值分别为品种、现货价格、最近交割合约、最近交割合约价格、主力合约、主力合约价格、最近合约基差值、主力合约基差值、最近合约基差率、主力合约基差率. 




获取历史某段时间的基差值
```python
import akshare as ak
ak.get_spot_price_daily(start_day="20180710", end_day="20180719", vars_list=["CU", "RB"])
```


注意: 

    1. 现货价格是从生意社网站爬取获得, 仅支持从 2011 年至今每个交易日数据. 


#### 会员持仓排名
自从**蜘蛛网策略**问世以来, 会员持仓数据日益受到关注. 数据的获取方式如下所示: 
获取某段时间的会员持仓排名前 5、前 10、前 15、前 20 等总和.
```python
import akshare as ak
ak.get_rank_sum_daily(start_day="20180718", end_day="20180719", vars_list=["IF", "C"])
```


获取某交易日某品种的持仓排名榜
```
ak.get_dce_rank_table()
ak.get_cffex_rank_table()
ak.get_czce_rank_table()
ak.get_shfe_rank_table()
```

注意: 

    1. 因为每个交易所公布的持仓排名不同: 大连所只公布品种的总持仓排名;
    
    2. 没有按不同交割月划分;上海、中金交易所公布了每个交割月的持仓排名, 没有公布品种所有合约总排名;
    
    3. 因此这里的品种排名和是各合约加总计算得来;郑州交易所公布了各合约排名和品种排名, 因此这里都是交易所原始数据. 

#### 日线行情K线
通过采集交易所官网信息, 可以获得各合约日线行情, 以及根据持仓量加权的指数行情, 用法如下: 
```python
import akshare as ak
ak.get_futures_daily(start_day="20190107", end_day="20190108", market="SHFE", index_bar=True)
```

market 可以添为四个交易所的简称, 即 "dce" 代表大商所; "shfe" 代表上期所; "czce" 代表郑商所; "cffex" 代表中金所. 
index_bar 为 True 时, 在生成的 pd.DataFrame 中通过持仓量加权合成指数合约, 如 RB99.

## [AkShare](https://github.com/jindaxiang/akshare) 债券数据

### 债券基础信息

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/index/bond_stock_index.png)

上图是利用 [AkShare](https://github.com/jindaxiang/akshare) 的 **get_bond_bank** 函数获取的中国银行间
交易商协会发布的债券数据来绘制的, 可以在上面明确看出近几个月发债规模急速上升.

### 债券基础名词

#### 固定收益证券: 

#### 国债:

### 债券基础数据

#### 银行间市场债券发行基础数据
银行间市场的债券发行数据是由交易商协会公布的的日级数据, 在很大程度上可以债券发行规模变化. 调用例子如下: 

接口：get_bond_bank

目标地址: http://zhuce.nafmii.org.cn/fans/publicQuery/manager

描述：获取银行间债券市场数据

限量：单次最大20行, 建议用 for 获取行数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| page_num | int  | Y    |  默认参数 page_num=1, 输入想要提取的页码, 多页提取请用 for 循环|

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| firstIssueAmount   | str   | Y        | 金额(亿元)     |
| isReg        | str   | Y        | 是否注册, 显示为: 备案或者注册     |
| regFileName            | str   | Y        | 债券名称     |
| regPrdtType        | str   | Y        | 品种 |
| releaseTime      | float | Y        | 更新时间     |
| projPhase      | float | Y        | 项目阶段     |


接口示例
```python
import akshare as ak
ak.get_bond_bank(page_num=1)
```

数据示例
```
   firstIssueAmount isReg                               regFileName  \
0                 9     1    淮南市产业发展(集团)有限公司关于发行2019年度第一期短期融资券的注册报告   
1                10     1          光大嘉宝股份有限公司关于发行2019年度第一期中期票据的注册报告   
2                15     1           西安高新控股有限公司关于发行2019年第二期中期票据的注册报告   
3                10     1          启迪控股股份有限公司关于发行2019年度第一期中期票据的注册报告   
4                 5     2  云南华电金沙江中游水电开发有限公司关于发行2019年度第二期短期融资券的注册报告   
5                 5     1       南京栖霞山旅游发展有限公司关于发行2019年度第一期中期票据的注册报告   
6                14     2   徐工集团工程机械有限公司关于发行2019年度第二期短期融资券的注册报告（备案）   
7                10     1      天津临港投资控股有限公司关于发行2019年度第一期超短期融资券的注册报告   
8                 2     1          中德联合集团有限公司关于发行2019年度第一期中期票据的注册报告   
9                10     1             浙江恒逸集团有限公司2019年度第七期超短期融资券注册报告   
10                5     1        西王集团有限公司关于发行2019-2021年度超短期融资券的注册报告   
11                5     1   荆州市城市建设投资开发有限公司关于注册发行2019年度第二期中期票据的注册报告   
12               10     1       招商局通商融资租赁有限公司关于发行2019年度第一期中期票据的注册报告   
13               15     1          中国旅游集团有限公司关于发行2019年度第四期中期票据的注册报告   
14               22     1     天津市保障住房建设投资有限公司关于发行2019年度第二期中期票据的注册报告   
15                5     1     余姚市城市建设投资发展有限公司关于发行2019年度第四期中期票据的注册报告   
16                5     2       四川蓝光发展股份有限公司关于发行2019年度第二期短期融资券的注册报告   
17                5     1      连云港市工业投资集团有限公司关于发行2019年度第二期中期票据的注册报告   
18               10     1        德州德达城市建设投资运营有限公司2019年度第一期中期票据的注册报告   
19                5     2   厦门经济特区房地产开发集团有限公司关于发行2019年度第一期中期票据的注册报告   

   regPrdtType          releaseTime projPhase  
0           CP  2019-10-12 00:00:00        20  
1          MTN  2019-10-12 00:00:00        20  
2          MTN  2019-10-12 00:00:00        20  
3          MTN  2019-10-12 00:00:00        20  
4           CP  2019-10-12 00:00:00        60  
5          MTN  2019-10-12 00:00:00        20  
6           CP  2019-10-12 00:00:00        60  
7          SCP  2019-10-12 00:00:00        20  
8          MTN  2019-10-12 00:00:00        20  
9          SCP  2019-10-12 00:00:00        30  
10         SCP  2019-10-12 00:00:00        20  
11         MTN  2019-10-12 00:00:00        20  
12         MTN  2019-10-12 00:00:00        20  
13          PN  2019-10-12 00:00:00        20  
14         MTN  2019-10-12 00:00:00        20  
15         MTN  2019-10-12 00:00:00        20  
16          CP  2019-10-12 00:00:00        20  
17         MTN  2019-10-12 00:00:00        20  
18         MTN  2019-10-12 00:00:00        20  
19          PN  2019-10-12 00:00:00        60
```

## [AkShare](https://github.com/jindaxiang/akshare) 期权数据

## [AkShare](https://github.com/jindaxiang/akshare) 私募指数数据

## [AkShare](https://github.com/jindaxiang/akshare) 全球指数数据
接口：get_country_index

目标地址: https://cn.investing.com/indices/

描述：获取世界主要国家的各种指数, 具体参见目标地址网页

限量：单次返回某一个国家的具体某一个指数, 建议用 for 获取多个国家的多个指数

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| country | str  | Y    |   country="中国"|
| index_name | str  | Y    |  index_name="深证新兴"|
| start_date | str  | Y    |  start_date='2000/01/01'|
| end_date | str  | Y    |  end_date='2019/10/17'|

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期  |
| 收盘      | str   | Y        | 收盘   |
| 开盘      | str   | Y        | 开盘        |
| 高        | str   | Y        |高    |
| 低         | str | Y        | 低         |
| 交易量      | str | Y        | 交易量      |
| 百分比变化  | str | Y        | 百分比变化  |



接口示例
```python
import akshare as ak
index_df = ak.get_country_index(country="中国", index_name="深证新兴", start_date='2000/01/01', end_date='2019/10/17')
print(index_df)
print(index_df.name)
```

数据示例

index_df.name:

```深证战略性新兴产业指数历史数据```

index_df:

```
0              日期        收盘        开盘         高         低     交易量   百分比变化
1     2019年10月16日  1,692.60  1,695.38  1,708.59  1,691.39   4.65B  -0.01%
2     2019年10月15日  1,692.79  1,712.84  1,712.84  1,691.32   5.41B  -1.45%
3     2019年10月14日  1,717.74  1,713.70  1,726.25  1,710.30   5.99B   1.30%
4     2019年10月11日  1,695.62  1,695.28  1,703.79  1,680.60   5.15B   0.24%
5     2019年10月10日  1,691.63  1,664.54  1,693.21  1,660.60   5.36B   1.68%
...           ...       ...       ...       ...       ...     ...     ...
1647    2013年1月7日    914.17    901.32    914.17    899.97  18.97K   1.45%
1648    2013年1月4日    901.11    917.44    918.90    893.13  17.70K  -1.02%
1649  2012年12月31日    910.43    902.72    910.43    900.62  15.90K   1.11%
1650  2012年12月28日    900.42    892.72    900.42    888.62  13.82K   0.88%
1651  2012年12月27日    892.59    901.97    905.57    891.83  17.55K  -0.76%
```




# Anaconda安装说明及环境配置
## Anaconda 安装说明


Anaconda 是集成了上千个常用库的 Python 发行版本, 通过安装 Anaconda 能简化环境管理工作, 非常推荐使用. 
作者基于目前 Python2 即将停止更新, 且目前大部分使用者电脑系统基本都是 64 位, 所以建议选择 Python3.7.3 64 位版本
同时, 根据您电脑的操作系统选择相对应的版本: Windows 版, MacOS 或 Linux 版的 64 位安装包.

## 安装演示(以 64 位 windows 版本为例)
下图中红框为 64 位 Windows 选择的版本:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_download.png)

在这里, 作者建议下载 Anaconda3-2019.07, 点击下载 [最新版 Anaconda 官方下载链接](https://repo.anaconda.com/archive/Anaconda3-2019.07-Windows-x86_64.exe)

双击如下图标进行安装:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_icon.png)

点击 Next:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_1.png)

点击 I Agree:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_2.png)

点击 Just me --> Next:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_3.png)

修改 Destination Folder 为如图所示:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_4.png)

勾选下图红框选项(以便于把安装的环境加入系统路径) --> Install:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/anaconda_install_5.png)

安装好后, 找到 Anaconda Prompt 窗口:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt.png)

输入 python, 如果如下图所示, 即已经在系统目录中安装好 anaconda3 的环境. 

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt_1.png)

创建虚拟环境命令:

```
conda create -n ak_test python=3.7.3
```

输入上述命令后出现确认, 输入 y

```
Proceed 输入 y
```

显示出最后一个红框内容则创建虚拟环境成功.

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt_2.png)

在虚拟环境中安装 [AkShare](https://github.com/jindaxiang/akshare). 输入如下内容, 会在全新的环境中自动安装所需要的依赖包

激活已经创建好的 ak_test 虚拟环境

```
conda activate ak_test
```

在 ak_test 虚拟环境中安装并更新 [AkShare](https://github.com/jindaxiang/akshare)

```
pip install akshare --upgrade
```

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt_3.png)

在安装完毕后, 输入 **python** 进入虚拟环境中的 Python

```
python
```

在 ak_test 虚拟环境的 Python 环境里面输入:

```python
import akshare as ak
ak.__doc__
```

显示出如下图则虚拟环境和 [AkShare](https://github.com/jindaxiang/akshare) 安装成功:

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/anaconda/virtual_env/anaconda_prompt_4.png)


还可以在 ak_test 虚拟环境的 Python 环境中输入如下代码可以显示 [AkShare](https://github.com/jindaxiang/akshare) 的版本

```python
import akshare as ak
ak.__version__
```

# 每日监控下载配置
本地配置好 Anaconda, 以及通过 pip 安装好 akshare>=0.1.59 后, 在 github 上下载示例文件, 即按照下图选择. 

[https://github.com/jindaxiang/akshare](https://github.com/jindaxiang/akshare)

![image](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/oT9PEhN0Knbv7Q.hPIO9TyuDkHl*il8K92GILqm4QHQ!/b/dL4AAAAAAAAA&bo=EgTRAwAAAAADB.Y!&rf=viewer_4)

解压下载的文件, 然后来到 example 目录下, 设置 setting 配置文件
root 设置为 [AkShare](https://github.com/jindaxiang/akshare) 爬数据时存储的默认目录(需要保证目录存在), qqEmail 和 secret 为爬取到数据时把数据发送给自己的 qq 邮箱账号和密码. 需要开通SMTP服务, 如果不需要自己邮件提醒, 就不用设置（也不要改默认的qqEmail和secret）. 
![](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/Ja.CVdg.fgrxFKW2jBGJqT53b7qCNSY*DwmbGDBS928!/b/dL8AAAAAAAAA&bo=aQRbAwAAAAADBxc!&rf=viewer_4)

最后双击 monitor.cmd 即完成, 每日 17 点自动下载数据. 

# QQ邮箱SMTP服务设置
在利用 Python 程序发送 QQ 邮件时, 需要开启 QQ 邮件的 SMTP 服务, 操作方法如下, 第一步打开 QQ 邮箱, 点"设置". 

![](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/bvaIA.HUOZL.pKsEPMB4gj8dvT*9TLy*6x7zIKwzPQE!/b/dLwAAAAAAAAA&bo=HgR5AgAAAAADB0M!&rf=viewer_4)

找到"账户", 并下拉
![](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/umgOdgp4tRuhiDOmtbLXiVVIPZ*87HeSQBaVHd1jPcY!/b/dL8AAAAAAAAA&bo=HATrAAAAAAADF8E!&rf=viewer_4)

开启以下的两项服务, 并生成授权码, 授权码为 Python 程序通过 SMTP 发送邮件的密码, 即上一节文档的 secret(不同于QQ邮箱登录密码)
![](http://m.qpic.cn/psb?/V12c0Jww0zKwzz/XavUKCeQ3fSqFXFTPBU0kJN9eIoFMtOApCEp7ZNDRqs!/b/dL8AAAAAAAAA&bo=iAOWAgAAAAADFy0!&rf=viewer_4)

在启动服务的过程中, 如果该 QQ 账户没有绑定过手机号, 可能会需要验证, 这里不再赘述. 

# 特别说明

## 致谢

特别感谢 [FuShare](https://github.com/jindaxiang/fushare), [TuShare](https://github.com/waditu/tushare) 项目提供借鉴学习的机会;

感谢[生意社网站](http://www.100ppi.com/)提供的商品基差及相关数据;

感谢[奇货可查网站](https://qhkch.com/)提供的奇货指数及相关数据;

感谢[智道智科网站](https://www.ziasset.com/)提供的私募指数数据;

感谢[中国银行间市场交易商协会网站](http://www.nafmii.org.cn/)提供的银行间市场债券数据;

感谢[99期货网站](http://www.99qh.com/)提供的大宗商品库存数据;

感谢[英为财情网站](https://cn.investing.com/)提供的全球股指与期货指数数据;

感谢[中国金融期货交易所网站](http://www.cffex.com.cn/)提供的相关数据;

感谢[上海期货交易所网站](http://www.shfe.com.cn/)提供的相关数据;

感谢[大连商品交易所网站](http://www.dce.com.cn/)提供的相关数据;

感谢[郑州商品交易所网站](http://www.czce.com.cn/)提供的相关数据;

感谢[上海国际能源交易中心网站](http://www.ine.com.cn/)提供的相关数据.



## 交流

欢迎加 QQ 群交流: 326900231

您可以扫码或者点击群二维码

在开启 QQ 情况下, 点击下面的图片自动打开 QQ 并加入本群, 本功能由 QQ 提供, 请放心点击:

<a target="_blank" href="https://shang.qq.com/wpa/qunwpa?idkey=aacb87089dd5ecb8c6620ce391de15b92310cfb65e3b37f37eb465769e3fc1a3"><img border="0" src="https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/qq/akshare_md_fold_1569925684166.png" alt="AkShare官方" title="AkShare官方"></a>



## 声明

1. [AkShare](https://github.com/jindaxiang/akshare) 提供的数据仅供参考, 不构成任何投资建议;
2. 任何基于 [AkShare](https://github.com/jindaxiang/akshare) 进行研究的投资者请注意数据风险;
3. [AkShare](https://github.com/jindaxiang/akshare) 的使用请遵循相关开源协议.


# 量化策略介绍
[掘金量化策略文档](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/strategy/classic_strategy_myquant.pdf)

目录
- 双均线策略(期货)
- alpha对冲(股票+期货)
- 集合竞价选股(股票)
- 多因子选股(股票)
- 网格交易(期货)
- 指数增强(股票)
- 跨品种套利(期货)
- 跨期套利(期货)
- 日内回转交易(股票)
- 做市商交易(期货)
- 海龟交易法(期货)
- 行业轮动(股票)
- 机器学习(股票)

# 量化平台介绍

目录
- 聚宽量化
- 掘金量化
- BigQuant
- 万矿平台(万得资讯旗下)


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

0.1.46
修复 README.md 图片显示

0.1.47
修复 README.md 增加说明部分

0.1.48
更新大连商品交易所-粳米-RR品种

0.1.49
增加智道智科-私募指数数据接口
使用方法请 help(get_zdzk_fund_index) 查看

0.1.50
更新 README.md 文件

0.1.51
更新官方文档: https://akshare.readthedocs.io

0.1.52
增加量化策略和量化平台板块

0.1.53
增加期货品种列表和名词解释

0.1.54
修改 AkShare的初衷, 增加管理期货策略指数

0.1.55
新增 99期货(http://www.99qh.com/d/store.aspx) 库存数据接口

0.1.56
修复 99期货(http://www.99qh.com/d/store.aspx) 库存数据接口

0.1.57
更新 md 文件数据接口

0.1.58
更新 md 文件数据接口

0.1.59
更新 md 文件数据接口

0.1.60
更新 致谢部分, 申明借鉴和引用的 package

0.1.61
更新说明文档

0.1.62
提供英为财情-股票指数-全球股指与期货指数数据接口
https://cn.investing.com/indices/

0.1.63
更新说明文档-致谢英为财情
```