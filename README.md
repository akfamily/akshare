# [AkShare](https://github.com/jindaxiang/akshare)
(本文档更新于 **2019-10-22**; 如发现库和文档相关问题, 请联系 [AkShare](https://github.com/jindaxiang/akshare) 作者: jindaxiang@163.com)

您也可以加入QQ群答疑解难: 326900231

<a target="_blank" href="https://shang.qq.com/wpa/qunwpa?idkey=aacb87089dd5ecb8c6620ce391de15b92310cfb65e3b37f37eb465769e3fc1a3"><img border="0" src="https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/qq/akshare_md_fold_1569925684166.png" alt="AkShare官方" title="AkShare官方"></a>

## [AkShare](https://github.com/jindaxiang/akshare) 的介绍

首先要特别感谢 [FuShare](https://github.com/jindaxiang/fushare), [TuShare](https://github.com/waditu/tushare) 在代码和项目开发上对本项目提供的借鉴和学习的机会!

[AkShare](https://github.com/jindaxiang/akshare) 于 **2019-10-08** 正式发布, 请访问 [AkShare文档](https://akshare.readthedocs.io) 了解和查询数据接口！

[AkShare](https://github.com/jindaxiang/akshare) 是基于 Python 的开源数据接口库, 目的是实现对期货, 期权, 基金等衍生金融产品和另类数据从数据采集, 数据清洗加工, 到数据下载的工具, 满足金融数据科学家, 数据科学爱好者在数据获取方面的需求. 它的特点是利用 [AkShare](https://github.com/jindaxiang/akshare) 获取的是基于交易所公布的原始数据, 广大数据科学家可以利用原始数据进行再加工, 得出科学的结论.

**后续会基于最新的学术研究论文和券商的金融工程报告添加更多的期货基本面指标和计算方法, 敬请关注.**

## [AkShare](https://github.com/jindaxiang/akshare) 的作者

**[Albert King](https://www.jfds.xyz/)** 致力于金融衍生品定价和价格预测、机器学习在金融领域的应用等研究.

<img src="https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/icon/images.jpg" width = 20% height = 10% align = center/>

## [AkShare](https://github.com/jindaxiang/akshare) 的特色

[AkShare](https://github.com/jindaxiang/akshare) 主要改进如下:

1. Python 语法符合 [PEP8](https://www.python.org/dev/peps/pep-0008/) 规范, 统一接口函数的命名;
2. 支持 Python 3.7 以上版本;
3. 后续加入 [asyncio](https://www.python.org/dev/peps/pep-3156/) 和 [aiohttp](https://aiohttp.readthedocs.io/en/stable/) 做异步加速;
4. 持续维护由于目标网页变化而导致的部分函数运行异常问题;
5. 后续更新会主要集中在提供更多金融数据接口, 同时优化源代码;
6. 增加更多的网络数据采集接口:

    6.1 增加[奇货可查网站](https://qhkch.com/)数据接口, 提供奇货可查指数数据(开发完成);
    
    6.2 增加[智道智科网站](https://www.ziasset.com/)数据接口, 提供私募指数数据(开发完成);
    
    6.3 增加[99期货网](http://www.99qh.com/)数据接口, 提供大宗商品库存数据(开发完成);
    
    6.4 增加[商品期权](https://github.com/jindaxiang/akshare)数据接口, 提供商品期货数据(开发完成);
    
    6.5 增加[英为财情网站-全球指数](https://github.com/jindaxiang/akshare)数据接口, 提供全球股指与期货指数数据(开发完成);
    
    6.6 增加[英为财情网站-全球债券](https://github.com/jindaxiang/akshare)数据接口, 提供全球政府债券行情与收益率数据(开发完成);
    
    6.7 增加[中国外汇交易中心暨全国银行间同业拆借中心网站](http://www.chinamoney.com.cn/chinese/)数据接口, 提供中国银行间债券行情和外汇数据(开发完成);

    6.8 增加[英为财情网站-商品](https://cn.investing.com/commodities/)数据接口, 提供全球商品历史数据(开发完成);
    
    6.9 增加[金十数据网站](https://www.jin10.com/)数据接口, 提供全球宏观经济数据接口-中国宏观(开发完成);
    
7. 提供完善的接口文档, 提高 [AkShare](https://github.com/jindaxiang/akshare) 的易用性;
9. 希望您能参与 [AkShare GitHub](https://github.com/jindaxiang/akshare) 的维护与管理.


## [AkShare](https://github.com/jindaxiang/akshare) 的初衷

[AkShare](https://github.com/jindaxiang/akshare) 希望能为各位同仁提供一个多源金融数据的接口, 助力个人
投资者、机构投资者、各大研究机构方便的搜集和整理关于金融产品, 金融衍生品等相关的数据. 

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/index/stock_futures_index.png)

上图是利用 [AkShare](https://github.com/jindaxiang/akshare) 的 **get_zdzk_fund_index** 接口获取的[智道智科](https://www.ziasset.com/company/)发布的股票策略指数和管理期货策略指数.
可以看出股票策略的波动性大于管理期货策略, 而且从 2015 年至今, 管理期货策略能获得较稳定的收益.

传统的 CTA 策略以趋势为主, 但是自从 2017 年以来, 无论是长线还是短线的趋势策略都受制于商品波动率的降低, 面临了多多少少的回撤, 
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
 # 交易所期货数据
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
 'get_country_index'  # 提供英为财情-股票指数-全球股指与期货指数数据
 'get_country_bond'  # 提供英为财情-债券数据-全球政府债券行情与收益率数据
 # 交易所商品期权数据
 'get_dce_option_daily'  # 提供大连商品交易所商品期权数据
 'get_czce_option_daily'  # 提供郑州商品交易所商品期权数据
 'get_shfe_option_daily'  # 提供上海期货交易所商品期权数据
 # 中国银行间市场债券行情数据
 'get_bond_market_quote'  # 债券市场行情-现券市场成交行情数据
 'get_bond_market_trade'  # 债券市场行情-现券市场做市报价数据
 # 外汇
 'get_fx_spot_quote'  # 人民币外汇即期报价数据
 'get_fx_swap_quote'  # 人民币外汇远掉报价数据
 'get_fx_pair_quote'  # 外币对即期报价数据
 # 商品
 'get_sector_futures'  # 全球商品数据数据
 # 宏观
 'get_china_yearly_cpi'  # 中国年度CPI数据
 'get_china_monthly_cpi'  # 中国月度CPI数据
 'get_china_yearly_m2'  # 中国年度M2数据
 'get_china_yearly_ppi'  # 中国年度PPI数据
 'get_china_yearly_pmi'  # 中国年度PMI数据
 'get_china_yearly_gdp'  # 中国年度GDP数据
 'get_china_yearly_cx_pmi'  # 中国年度财新PMI数据
 'get_china_yearly_fx_reserves'  # 中国外汇储备数据
 'get_china_daily_energy'  # 中国电力能源数据
 'get_china_non_man_pmi'  # 中国年度非制造业PMI数据
 'get_china_rmb'  # 人民币中间报价汇率
```

## 3. 案例演示

### 3. 获取展期收益率

**Example 3.1** 获取展期收益率数据:

代码:

```python
import akshare as ak
ak.get_roll_yield_bar(type_method="date", var="RB", start_day="20180618", end_day="20180718", plot=True)
```

结果显示: 日期, 展期收益率, 最近合约, 下一期合约

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

结果显示: 日期, 指数数值

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
```

# [AkShare](https://github.com/jindaxiang/akshare) 数据字典

## [AkShare](https://github.com/jindaxiang/akshare) 期货数据

### 期货基础信息

主要提供金融期货和商品期货相关的基本面和行情数据

#### 期货交易所

| 交易所名称    | 交易所代码 | 合约后缀 | 首页地址|
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
主力连续合约: 合约首次上市时, 以当日收盘同品种持仓量最大者作为从第二个交易日开始的主力合约. 当同品种其他合约持仓量在收盘后超过当前主力合约1.1倍时, 从第二个交易日开始进行主力合约的切换. 
日内不会进行主力合约的切换. 主力连续合约是由该品种期货不同时期主力合约接续而成, 代码以88或888结尾结尾, 例如 IF88 或 IF888. 前者为合约量价数据的简单拼接, 未做平滑处理;  后者对价格进行了”平滑”处理, 处理规则如下: 以主力合约切换前一天(T-1日)新、旧两个主力合约收盘价做差,  之后将 T-1 日及以前的主力连续合约的所有价格水平整体加上或减去该价差, 以”整体抬升”或”整体下降”主力合约的价格水平, 成交量、持仓量均不作调整, 成交额统一设置为0.

#### 指数连续合约
指数连续合约: 由当前品种全部可交易合约以累计持仓量为权重加权平均得到, 代码以99结尾, 例如 IF99. 

#### 展期收益率
展期收益率是由不同交割月的价差除以相隔月份数计算得来, 它反映了市场对该品种在近期交割和远期交割的价差预期.

### 期货基础数据

#### 库存数据

库存数据是从[99期货网站](http://www.99qh.com/d/store.aspx)获取的日频率数据, 
由于网站限制, 目前可以利用本接口获取历史数据的图片格式和近期数据的 **pandas.DataFrame** 格式. 调用例子如下: 

接口: get_inventory_data

目标地址: http://www.99qh.com/d/store.aspx

描述: 获取大宗商品库存数据

限量: 单次一个市场的某个具体品种, 请用 **help(get_inventory_data)** 查看使用方法

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

### 期货行情数据

#### 全球商品期货
接口: get_sector_futures

目标地址: https://cn.investing.com/commodities/

描述: 主要提供全球能源、农业、金属、商品指数历史数据

限量: 单次最大5000行, 建议用 for 获取行数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| sector | str  | Y    |  能源、农业、金属、商品指数之一|
| symbol | str  | Y    |  对应板块中的产品名称, 可以通过查询网页获取|
| start_date | str  | Y    |  需要获取数据的开始时间, e.g., start_date='2005/01/01'|
| end_date | str  | Y    |  需要获取数据的开始时间, e.g., end_date='2015/01/01' |


输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期索引  |
| 收盘      | float   | Y        | 收盘   |
| 开盘      | float   | Y        | 开盘        |
| 高        | float   | Y        |高    |
| 低         | float | Y        | 低         |
| 涨跌幅      | str | Y        | 涨跌幅      |


接口示例
```python
import akshare as ak
ak.get_sector_futures(sector="能源", symbol="伦敦布伦特原油", start_date='2005/01/01', end_date='2019/10/17')
```

数据示例
```
0              收盘     开盘      高      低      涨跌幅
日期                                             
2019-10-17  59.91  58.99  60.04  58.69  269.84K
2019-10-16  59.42  58.90  59.75  58.36  257.88K
2019-10-15  58.74  59.30  59.68  58.00  305.68K
2019-10-14  59.35  60.69  60.73  58.50  283.07K
2019-10-11  60.51  59.53  60.69  59.21  367.63K
...           ...    ...    ...    ...      ...
2005-01-10  42.92  43.20  44.85  42.90   27.65K
2005-01-07  43.18  42.75  43.75  42.20   29.64K
2005-01-06  42.85  40.43  43.20  39.82   51.63K
2005-01-05  40.51  40.80  41.00  39.90   42.23K
2005-01-04  41.04  39.40  41.25  38.81   40.10K
```


## [AkShare](https://github.com/jindaxiang/akshare) 债券数据

### 债券基础信息

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/index/bond_stock_index.png)

上图是利用 [AkShare](https://github.com/jindaxiang/akshare) 的 **get_bond_bank** 函数获取的中国银行间
交易商协会发布的债券数据来绘制的, 可以在上面明确看出近几个月发债规模急速上升.

### 债券基础名词

#### 固定收益证券
是指持券人可以在特定的时间内取得固定的收益并预先知道取得收益的数量和时间, 如固定利率债券、优先股股票等.

#### 国债

国债又称国家公债, 是国家以其信用为基础, 按照债券的一般原则, 通过向社会发行债券筹集资金所形成的债权债务关系. 国债是中央政府为筹集财政资金而发行的一种政府债券, 由中央政府向投资者出具的、承诺在一定时期支付利息和到期偿还本金的债权债务凭证, 由于国债的发行主体是国家, 所以它具有最高的信用度, 被公认为是最安全的投资工具. 

### 债券基础数据

#### 银行间市场债券发行基础数据
银行间市场的债券发行数据是由交易商协会公布的的日级数据, 在很大程度上可以债券发行规模变化. 调用例子如下: 

接口: get_bond_bank

目标地址: http://zhuce.nafmii.org.cn/fans/publicQuery/manager

描述: 获取银行间债券市场数据

限量: 单次最大20行, 建议用 for 获取行数据

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
6                14     2   徐工集团工程机械有限公司关于发行2019年度第二期短期融资券的注册报告(备案)   
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

### 中国债券行情数据

#### 现券市场成交行情
接口: get_bond_market_quote

目标地址: http://www.chinamoney.com.cn/chinese/mkdatabond/

描述: 提供中国外汇交易中心暨全国银行间同业拆借中心-市场数据-市场行情-债券市场行情-现券市场成交行情


限量: 单次返回所有即期数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 空 | 空 | 空 | 空 |

输出参数


| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 报价机构      | str   | Y        |   |
| 债券简称      | str   | Y        |    |
| 买入/卖出净价(元)      | str   | Y        |         |
| 买入/卖出收益率(%)        | str   | Y        |    |
| ***        | *   | *        |   * |


接口示例
```python
import akshare as ak
bond_df = ak.get_bond_market_quote()
print(bond_df)
print(bond_df.name)
```

数据示例

债券市场行情

```
         abdAssetEncdFullDescByRmb        tradeAmnt abdAssetEncdShrtDescByRmb  \
    0                               100.50 / 101.32
    1                                99.54 / 100.33
    2                                99.85 / 100.28
    3                               100.18 / 100.42
    4                                 99.35 / 99.74
                            ...              ...                       ...
    4539                              96.80 / 97.29
    4540                              96.89 / 97.12
    4541                              96.87 / 97.24
    4542                            110.67 / 118.18
    4543                            105.60 / 111.66
         contraRateByRmb   bondcode abdAssetEncdShrtDesc        code  \
    0                        190006             19附息国债06  76008ir9yz
    1                        190210               19国开10  75808ppkkk
    2                        190208               19国开08  81257k1w48
    3                        190207               19国开07  752516byyl
    4                        190203               19国开03  6344929pu6
                  ...        ...                  ...         ...
    4539                  111907080          19招商银行CD080  7659607080
    4540                  111906014          19交通银行CD014  6259506014
    4541                  111908046          19中信银行CD046  6965108046
    4542                    1480134              14国网债02  1000045704
    4543                    1280107              12国网债02  1000034728
         emaEntyEncdFullDescByRmb qbdEntryTrnsctDateTmst emaEntyEncdShrtDesc  \
    0                                                                   民生银行
    1                                                                   民生银行
    2                                                                   民生银行
    3                                                                   民生银行
    4                                                                   民生银行
                           ...                    ...                 ...
    4539                                                                中国银行
    4540                                                                中国银行
    4541                                                                中国银行
    4542                                                              国泰君安证券
    4543                                                              国泰君安证券
         qbdQuoteDate inptTp abdAssetEncdShrtDescEN       contraRate  \
    0                      0                         3.2288 / 3.1288
    1                      0                         3.7063 / 3.6063
    2                      0                         3.4525 / 3.3525
    3                      0                         3.1025 / 3.0025
    4                      0                         3.4638 / 3.3638
               ...    ...                    ...              ...
    4539                   0                         3.3008 / 2.4278
    4540                   0                         3.3125 / 2.3913
    4541                   0                         3.3069 / 2.4249
    4542                   0                         4.5732 / 3.6732
    4543                   0                         4.3622 / 3.4622
         emaEntyEncdShrtDescByRmb emaEntyEncdShrtDescEN
    0                                              MSBK
    1                                              MSBK
    2                                              MSBK
    3                                              MSBK
    4                                              MSBK
                           ...                   ...
    4539                                            BOC
    4540                                            BOC
    4541                                            BOC
    4542                                           GTJA
    4543                                           GTJA
```

#### 现券市场做市报价
接口: get_bond_market_trade

目标地址: http://www.chinamoney.com.cn/chinese/mkdatabond/

描述: 提供中国外汇交易中心暨全国银行间同业拆借中心-市场数据-市场行情-债券市场行情-现券市场做市报价


限量: 单次返回所有即期数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 空 | 空 | 空 | 空 |

输出参数


| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 债券简称      | str   | Y        |   |
| 成交净价(元)      | float   | Y        |    |
| 最新收益率(%)      | float   | Y        |         |
| 涨跌(BP)        | float   | Y        |    |
| 加权收益率(%)      | float   | Y        |         |
| 交易量(亿)        | float   | Y        |    |
| ***        | *   | *        |   * |

					

接口示例
```python
import akshare as ak
bond_df = ak.get_bond_market_trade()
print(bond_df)
print(bond_df.name)
```

数据示例

现券市场做市报价

```
         abdAssetEncdFullDescByRmb dmiLatestRateLabel  bpNum  \
    0                       19国开10             100.07  -0.93
    1                       19国开15              99.05   0.50
    2                     19附息国债06             100.90   7.83
    3                     19附息国债03              99.84   0.72
    4                     19附息国债04             100.83   1.25
                            ...                ...    ...
    1164               17今世缘MTN002             102.60   1.06
    1165                 19天业CP001             100.27   1.93
    1166                 17诸暨国资债01             103.17   2.64
    1167                  17附息国债06             101.07  -6.60
    1168                  18附息国债01             103.08  -1.10
         abdAssetEncdShrtDescByRmb bpLabel blank dmiTtlTradedAmnt  \
    0                       19国开10          None         756.3200
    1                       19国开15          None         189.3000
    2                     19附息国债06          None         153.7400
    3                     19附息国债03          None         153.4230
    4                     19附息国债04          None         122.1650
                            ...     ...   ...              ...
    1164                 17今世缘MTN0          None           0.0200
    1165                 19天业CP001          None           0.0200
    1166                   17诸暨国资�          None           0.0200
    1167                  17附息国债06          None           0.0050
    1168                  18附息国债01          None           0.0020
         dmiTtlTradedAmntLabel dmiLatestContraRateLabel   bondcode  \
    0                 756.3200                   3.6395     190210
    1                 189.3000                   3.5650     190215
    2                 153.7400                   3.1800     190006
    3                 153.4230                   2.7550     190003
    4                 122.1650                   2.9850     190004
                        ...                      ...        ...
    1164                0.0200                   5.0006  101753013
    1165                0.0200                   3.6293  041900345
    1166                0.0200                   4.0464    1780124
    1167                0.0050                   2.9340     170006
    1168                0.0020                   2.7990     180001
         abdAssetEncdShrtDesc        code             showDate  \
    0                  19国开10  75808ppkkk  2019-10-18 16:41:11
    1                  19国开15  92893523p5  2019-10-18 16:40:00
    2                19附息国债06  76008ir9yz  2019-10-18 16:36:56
    3                19附息国债03  664521tbo4  2019-10-18 16:31:11
    4                19附息国债04  70854w2ml3  2019-10-18 16:26:32
                       ...         ...                  ...
    1164          17今世缘MTN002  9578653013  2019-10-18 15:57:37
    1165            19天业CP001  90962lmhtp  2019-10-18 15:57:37
    1166            17诸暨国资债01  1000103754  2019-10-18 14:53:47
    1167             17附息国债06  1000093201  2019-10-18 14:51:07
    1168             18附息国债01  1000125437  2019-10-18 14:50:51
         dmiPrvsClsngContraRate    bp dmiLatestContraRate dmiWghtdContraRate  \
    0                      None  0.93              3.6395             3.6444
    1                      None  0.50              3.5650             3.5629
    2                      None  7.83              3.1800             3.1646
    3                      None  0.72              2.7550             2.7512
    4                      None  1.25              2.9850             2.9826
                         ...   ...                 ...                ...
    1164                   None  1.06              5.0006             5.0006
    1165                   None  1.93              3.6293             3.6293
    1166                   None  2.64              4.0464             4.0464
    1167                   None  6.60              2.9340             2.9340
    1168                   None  1.10              2.7990             2.7990
         dmiWghtdContraRateLabel inptTp dmiLatestRate
    0                     3.6444      0        100.07
    1                     3.5629      0         99.05
    2                     3.1646      0        100.90
    3                     2.7512      0         99.84
    4                     2.9826      0        100.83
                          ...    ...           ...
    1164                  5.0006      0        102.60
    1165                  3.6293      0        100.27
    1166                  4.0464      0        103.17
    1167                  2.9340      0        101.07
    1168                  2.7990      0        103.08
```

### 全球债券行情数据
接口: get_country_bond

目标地址: https://cn.investing.com/rates-bonds/

描述: 获取全球政府债券行情与收益率, 由于涉及国家和债券多(**近1000**个债券)具体参见[国家-债券目录](https://cn.investing.com/rates-bonds/world-government-bonds?maturity_from=10&maturity_to=310)
具体的调用方式可以参照: 
1. 先查询指数所在的国家名称;
2. 复制网页上国家名称(推荐复制), 如 **中国**;
3. 复制所显示的具体债券名称(推荐复制, 如果英文中间有空格, 也需要保留空格), 如 **中国1年期国债**;
4. 在安装 [AkShare](https://github.com/jindaxiang/akshare) 后输入, 如 **ak.get_country_bond(country="中国", index_name="中国1年期国债", start_date='2000/01/01', end_date='2019/10/17')**;
5. 稍后就可以获得所需数据.

限量: 单次返回某一个国家的具体某一个指数, 建议用 for 循环获取多个国家的多个指数, 注意不要大量获取, 以免给对方服务器造成压力!

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| country | str  | Y    |   country="中国"|
| index_name | str  | Y    |  index_name="中国1年期国债"|
| start_date | str  | Y    |  start_date='2000/01/01'|
| end_date | str  | Y    |  end_date='2019/10/17'|

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期索引  |
| 收盘      | float   | Y        | 收盘   |
| 开盘      | float   | Y        | 开盘        |
| 高        | float   | Y        |高    |
| 低         | float | Y        | 低         |
| 交易量      | str | Y        | 涨跌幅      |



接口示例
```python
import akshare as ak
bond_df = ak.get_country_bond(country="中国", index_name="中国1年期国债", start_date='2000/01/01', end_date='2019/10/17')
print(bond_df)
print(bond_df.name)
```

数据示例

bond_df.name:

```中国一年期国债收益率历史数据```

bond_df:

```
0          收盘     开盘      高      低      涨跌幅
日期                                             
2019-10-17  2.647  2.656  2.656  2.647   -1.65%
2019-10-16  2.691  2.700  2.700  2.691    0.67%
2019-10-15  2.673  2.673  2.673  2.673    0.75%
2019-10-14  2.653  2.671  2.671  2.653    0.19%
2019-10-11  2.648  2.677  2.677  2.648   -0.56%
...           ...    ...    ...    ...      ...
2002-06-10  1.955  1.955  1.955  1.955    2.20%
2002-06-07  1.913  1.913  1.913  1.913   -0.42%
2002-06-06  1.921  1.921  1.921  1.921  -12.60%
2002-06-05  2.198  2.198  2.198  2.198    0.18%
2002-06-04  2.194  2.194  2.194  2.194    3.44%
```

## [AkShare](https://github.com/jindaxiang/akshare) 期权数据

### 上海期货交易所

接口: get_shfe_option_daily

目标地址: http://www.shfe.com.cn/statements/dataview.html?paramid=kxQ

描述: 获取上海期货交易所商品期权数据

限量: 单次返回具体某天某个品种期权行情数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| trade_date | str  | Y    |   trade_date="20191017"|
| symbol | str  | Y    |  symbol_type="铜期权"|

上海期货交易所提供的商品期权品种

|交易所|对应名称|
|-------|---------------------|
| 上海期货交易所  | 铜期权           |
| 上海期货交易所  | 天胶期权         |

输出参数

Part-1: 上海期货交易所期权合约行情

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 合约代码      | str   | Y        |   |
| 开盘价      | float   | Y        |    |
| 最高价      | float   | Y        |   |
| 最低价      | float   | Y        |   |
| 收盘价      | float   | Y        |   |
| 前结算价    | float   | Y        |    |
| 结算价      | float   | Y        |   |
| 涨跌1      | float   | Y        |    |
| 涨跌2      | float   | Y        |   |
| 成交量      | float   | Y        |    |
| 持仓量      | float   | Y        |    |
| 持仓量变化  | float   | Y        |    |
| 成交额      | float   | Y        |    |
| 德尔塔(Delta)      | float   | Y        |    |
| 行权量      | float   | Y        |    |


注: 
1. 期权报价单位: 铜、天然橡胶为元/吨. 
2. 期权交易单位: 铜为5吨/手；天然橡胶为10吨/手. 
3. 成交量、持仓量、持仓量变化单位为手, 双边计算；成交额双边计算. 
4. 涨跌1=收盘价-前结算价, 涨跌2=结算价-前结算价. 
5. 合约系列: 具有相同月份标的期货合约的所有期权合约的统称. 
6. 隐含波动率: 根据期权市场交易价格, 利用期权定价模型计算出来的标的期货合约的价格波动率数值. 

Part-2: 上海期货交易所衍生品产品行情

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 品种      | str   | Y        |   |
| 成交量(手)      | float   | Y        |    |
| 成交额(万元)      | float   | Y        |   |
| 年成交量(万手)      | float   | Y        |   |
| 年成交额(亿元)      | float   | Y        |   |


注: 
1. 成交量、成交额、年成交量、年成交额双边计算. 
2. 成交量、成交额包含期权自对冲量. 

Part-3: 上海期货交易所隐含波动参考值

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 合约系列      | str   | Y        |   |
| 隐含波动率%      | float   | Y        |    |
						
接口示例

```python
import akshare as ak
part_1, part_2, part_3 = ak.get_shfe_option_daily(trade_date="20191017", symbol="天胶期权")
print(part_1)
print(part_2)
print(part_3)
```

数据示例

part_1: 上海期货交易所期权合约行情

```
        PRODUCTID  PRODUCTSORTNO       PRODUCTNAME  \
    288  ru_o                100  天胶期权
    289  ru_o                100  天胶期权
    290  ru_o                100  天胶期权
    291  ru_o                100  天胶期权
    292  ru_o                100  天胶期权
    ..        ...            ...               ...
    789  ru_o                100  天胶期权
    790  ru_o                100  天胶期权
    791  ru_o                100  天胶期权
    792  ru_o                100  天胶期权
    793  ru_o                100  天胶期权
                           INSTRUMENTID  PRESETTLEMENTPRICE OPENPRICE  \
    288  ru1911C10000                                   729
    289  ru1911C10250                                   495
    290  ru1911C10500                                   293
    291  ru1911C10750                                   146
    292  ru1911C11000                                    58
    ..                              ...                 ...       ...
    789  ru2010P9500                                    155
    790  ru2010P9600                                    172
    791  ru2010P9700                                    189
    792  ru2010P9800                                    209
    793  ru2010P9900                                    229
        HIGHESTPRICE LOWESTPRICE  CLOSEPRICE  SETTLEMENTPRICE  ZD1_CHG  ZD2_CHG  \
    288                                  778              778       49       49
    289                                  542              542       47       47
    290                                  334              334       41       41
    291                                  176              176       30       30
    292                                   76               76       18       18
    ..           ...         ...         ...              ...      ...      ...
    789                                  151              151       -4       -4
    790                                  167              167       -5       -5
    791                                  184              184       -5       -5
    792                                  204              204       -5       -5
    793                                  224              224       -5       -5
         VOLUME  OPENINTEREST  OPENINTERESTCHG  ORDERNO EXECVOLUME  TURNOVER  \
    288       0             0                0        0          0       0.0
    289       0             0                0        0          0       0.0
    290       0             0                0        0          0       0.0
    291       0             0                0        0          0       0.0
    292       0             4                0        0          0       0.0
    ..      ...           ...              ...      ...        ...       ...
    789       0             0                0        0          0       0.0
    790       0             0                0        0          0       0.0
    791       0             0                0        0          0       0.0
    792       0             0                0        0          0       0.0
    793       0             0                0        0          0       0.0
            DELTA
    288  0.976387
    289  0.908465
    290  0.757436
    291  0.531736
    292  0.299911
    ..        ...
    789 -0.112120
    790 -0.122028
    791 -0.131944
    792 -0.142837
    793 -0.154073
```

part_2: 上海期货交易所衍生品产品行情

```
       PRODUCTID  PRODUCTSORTNO       PRODUCTNAME HIGHESTPRICE LOWESTPRICE  \
    1  ru_o                100  天胶期权                     2774           2
      AVGPRICE  VOLUME  TURNOVER  YEARVOLUME  YEARTURNOVER EXECVOLUME  \
    1  148.573    8290  0.125033    112.5122     34.062215          0
       YEAREXECVOLUME
    1          1.0624
```

part_3: 上海期货交易所隐含波动参考值

```
       PRODUCTID  PRODUCTSORTNO       PRODUCTNAME    INSTRUMENTID  \
    12  ru_o                100  天胶期权              ru1911
    13  ru_o                100  天胶期权              ru2001
    14  ru_o                100  天胶期权              ru2003
    15  ru_o                100  天胶期权              ru2004
    16  ru_o                100  天胶期权              ru2005
    17  ru_o                100  天胶期权              ru2006
    18  ru_o                100  天胶期权              ru2007
    19  ru_o                100  天胶期权              ru2008
    20  ru_o                100  天胶期权              ru2009
    21  ru_o                100  天胶期权              ru2010
           SIGMA
    12  0.242419
    13  0.234428
    14  0.218916
    15  0.208057
    16  0.205821
    17  0.205821
    18  0.240689
    19  0.240689
    20  0.216861
    21  0.216861
```

### 大连商品交易所

接口: get_dce_option_daily

目标地址: http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/rxq/index.html

描述: 获取大连商品交易所商品期权数据

限量: 单次返回具体某天某个品种期权行情数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| trade_date | str  | Y    |   trade_date="20191017"|
| symbol | str  | Y    |  symbol_type="玉米期权"|

大连商品交易所提供的商品期权品种

|交易所|对应名称|
|-------|---------------------|
| 大连商品交易所  | 玉米期权           |
| 大连商品交易所  | 豆粕期权         |

输出参数

Part-1: 大连商品交易所期权合约行情

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 商品名称      | str   | Y        |   |
| 合约名称      | str   | Y        |   |
| 开盘价      | float   | Y        |    |
| 最高价      | float   | Y        |   |
| 最低价      | float   | Y        |   |
| 收盘价      | float   | Y        |   |
| 前结算价    | float   | Y        |    |
| 结算价      | float   | Y        |   |
| 涨跌      | float   | Y        |    |
| 涨跌1     | float   | Y        |   |
| 成交量      | float   | Y        |    |
| 持仓量      | float   | Y        |    |
| 持仓量变化  | float   | Y        |    |
| 成交额      | float   | Y        |    |
| 行权量      | float   | Y        |    |


说明: 
1. 价格: 元/吨, 鸡蛋为元/500千克, 纤维板、胶合板为元/张
2. 成交量、持仓量: 手(按双边计算)
3. 成交额: 万元(按双边计算)
4. 涨跌＝收盘价－前结算价
5. 涨跌1=今结算价-前结算价
6. 合约系列: 具有相同月份标的期货合约的所有期权合约的统称
7. 隐含波动率: 根据期权市场价格, 利用期权定价模型计算的标的期货合约价格波动率

Part-2: 隐含波动率参考值

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 合约系列      | str   | Y        |   |
| 隐含波动率%      | float   | Y        |    |
						
接口示例

```python
import akshare as ak
part_1, part_2= ak.get_dce_option_daily(trade_date="20191017", symbol="玉米期权")
print(part_1)
print(part_2)
```

数据示例

part_1: 大连商品交易所期权合约行情

```
                商品名称          合约名称    开盘价    最高价    最低价    收盘价   前结算价    结算价   涨跌  涨跌1  \
    0     玉米  c2001-C-1680  168.5  168.5  168.5  168.5  168.0  167.5  0.5 -0.5
    1     玉米  c2001-C-1700      0    0.0    0.0  148.0  148.0  148.0  0.0  0.0
    2     玉米  c2001-C-1720      0    0.0    0.0  129.0  128.0  129.0  1.0  1.0
    3     玉米  c2001-C-1740    115  115.0  115.0  115.0  108.0  111.0  7.0  3.0
    4     玉米  c2001-C-1760     89   95.5   89.0   95.5   89.0   93.5  6.5  4.5
    ..   ...           ...    ...    ...    ...    ...    ...    ...  ...  ...
    239   玉米  c2009-P-2040      0    0.0    0.0   91.0   88.5   91.0  2.5  2.5
    240   玉米  c2009-P-2060      0    0.0    0.0  106.0  104.0  106.0  2.0  2.0
    241   玉米  c2009-P-2080      0    0.0    0.0  121.5  120.5  121.5  1.0  1.0
    242   玉米  c2009-P-2100      0    0.0    0.0  138.5  137.5  138.5  1.0  1.0
    243   玉米  c2009-P-2120      0    0.0    0.0  155.5  155.5  155.5  0.0  0.0
         Delta 成交量    持仓量 持仓量变化   成交额  行权量
    0     0.98   2    236     0  0.34  0.0
    1     0.96   0    236     0     0  0.0
    2     0.94   0    210     0     0  0.0
    3     0.90  20  1,040     0   2.3  0.0
    4     0.85  12    680     0  1.11  0.0
    ..     ...  ..    ...   ...   ...  ...
    239  -0.70   0     30     0     0  0.0
    240  -0.75   0     50     0     0  0.0
    241  -0.80   0     20     0     0  0.0
    242  -0.84   0     10     0     0  0.0
    243  -0.88   0      0     0     0  0.0
```

part_2: 隐含波动率参考值

```
       合约系列 隐含波动率(%)
    1  c2001    12.95
    2  c2003     8.74
    3  c2005     8.75
    4  c2007      7.7
    5  c2009     6.85
```

### 郑州商品交易所

接口: get_czce_option_daily

目标地址: http://www.czce.com.cn/cn/jysj/mrhq/H770301index_1.htm

描述: 获取郑州商品交易所商品期权数据

限量: 单次返回具体某天某个品种期权行情数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| trade_date | str  | Y    |   trade_date="20191017"|
| symbol | str  | Y    |  symbol_type="白糖期权"|

郑州商品交易所提供的商品期权品种

|交易所|对应名称|
|-------|---------------------|
| 郑州商品交易所  | 白糖期权           |
| 郑州商品交易所  | 棉花期权         |

输出参数

郑州商品交易所期权合约行情

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 品种代码      | str   | Y        |   |
| 昨结算      | float   | Y        |   |
| 今开盘      | float   | Y        |   |
| 最高价      | float   | Y        |   |
| 最低价      | float   | Y        |   |
| 今收盘      | float   | Y        |   |
| 今结算      | float   | Y        |   |
| 涨跌1     | float   | Y        |    |
| 涨跌2     | float   | Y        |   |
| 成交量(手)      | float   | Y        |    |
| 空盘量      | float   | Y        |    |
| 增减量  | float   | Y        |    |
| 成交额(万元)      | float   | Y        |    |
| DELTA      | float   | Y        |    |
| 隐含波动率      | float   | Y        |    |
| 行权量      | float   | Y        |    |


说明:
1. 价格: 元/吨
2. 成交量、空盘量: 手
3. 成交额: 万元
4. 涨跌一: 今收盘-昨结算
5. 涨跌二: 今结算-昨结算
6. 隐含波动率: 将当日期权合约的结算价代入期权定价模型, 反推出来的波动率数值

						
接口示例
```python
import akshare as ak
option_df = ak.get_czce_option_daily(trade_date="20191017", symbol="白糖期权")
print(option_df)
```

数据示例

郑州商品交易所期权合约行情

```
         品种代码        昨结算         今开盘         最高价         最低价         今收盘      \
    0    CF001C10800  1,579.00    0.00        0.00        0.00        0.00
    1    CF001C11000  1,392.00    0.00        0.00        0.00        0.00
    2    CF001C11200  1,211.00    0.00        0.00        0.00        0.00
    3    CF001C11400  1,038.00    1,396.00    1,396.00    1,396.00    1,396.00
    4    CF001C11600  874.00      0.00        0.00        0.00        0.00
    ..           ...         ...         ...         ...         ...         ...
    398   SR009P5900  576.00      0.00        0.00        0.00        0.00
    399   SR009P6000  653.00      0.00        0.00        0.00        0.00
    400    小计
    401    SR合计
    402    总计
            今结算        涨跌1         涨跌2           成交量(手)     空盘量         增减量      \
    0    1,866.00    287.00      287.00      0           0           0
    1    1,672.00    280.00      280.00      0           0           0
    2    1,481.00    270.00      270.00      0           4           0
    3    1,295.00    358.00      257.00      2           68          0
    4    1,114.00    240.00      240.00      0           224         0
    ..          ...         ...         ...         ...         ...         ...
    398  580.00      4.00        4.00        0           0           0
    399  658.00      5.00        5.00        0           0           0
    400                                      656         860         400
    401                                      32,098      276,900     2252
    402                                      110,664     474,154     14770
         成交额(万元)  DELTA            隐含波动率  行权量
    0       0.00  0.9765      22.29         0
    1       0.00  0.9621      21.84         0
    2       0.00  0.9423      21.38         0
    3       1.40  0.9155      20.91         0
    4       0.00  0.8800      20.45         0
    ..       ...         ...         ...  ...
    398     0.00  -0.6639     16.24         0
    399     0.00  -0.7007     16.58         0
    400    97.28                            0
    401  2138.41                            0
    402  8769.52                            2
```

## [AkShare](https://github.com/jindaxiang/akshare) 外汇数据

### 人民币外汇即期报价

接口: get_fx_spot_quote

目标地址: http://www.chinamoney.com.cn/chinese/mkdatapfx/

描述: 获取人民币外汇即期报价

限量: 单次返回当前时点最近更新的即时数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

获取人民币外汇即期报价

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 货币对      | str   | Y        |   |
| 买报价      | float   | Y        |   |
| 卖报价      | float   | Y        |   |
| 中间价      | float   | Y        |  为空 |
| 时间      | str   | Y        |  为空 |

注：本行情为询价报价行情(美元为ODM), 实时更新. 
						
接口示例
```python
import akshare as ak
fx_df = ak.get_fx_spot_quote()
print(fx_df)
```

数据示例

人民币外汇即期报价

```
               ccyPair   bidPrc   askPrc midprice time
    0      USD/CNY   7.0810   7.0824      ---
    1      EUR/CNY   7.8878   7.8903      ---
    2   100JPY/CNY   6.5252   6.5275      ---
    3      HKD/CNY  0.90293  0.90316      ---
    4      GBP/CNY   9.1140   9.1181      ---
    5      AUD/CNY   4.8472   4.8491      ---
    6      NZD/CNY   4.5151   4.5172      ---
    7      SGD/CNY   5.1878   5.1897      ---
    8      CHF/CNY   7.1810   7.1838      ---
    9      CAD/CNY   5.3911   5.3929      ---
    10     CNY/MYR  0.58726  0.59527      ---
    11     CNY/RUB   9.0363   9.0489      ---
    12     CNY/ZAR   2.0883   2.0923      ---
    13     CNY/KRW   166.55   166.89      ---
    14     CNY/AED  0.51850  0.51886      ---
    15     CNY/SAR  0.52949  0.52979      ---
    16     CNY/HUF  41.8886  41.9805      ---
    17     CNY/PLN  0.54270  0.54331      ---
    18     CNY/DKK   0.9468   0.9473      ---
    19     CNY/SEK   1.3660   1.3667      ---
    20     CNY/NOK   1.2964   1.2971      ---
    21     CNY/TRY  0.81723  0.81918      ---
    22     CNY/MXN   2.7016   2.7041      ---
    23     CNY/THB   4.2753   4.2791      ---
```

### 人民币外汇远掉报价

接口: get_fx_swap_quote

目标地址: http://www.chinamoney.com.cn/chinese/mkdatapfx/

描述: 获取人民币外汇远掉报价

限量: 单次返回当前时点最近更新的即时数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

获取人民币外汇远掉报价

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 货币对      | str   | Y        |  e.g., "USD/CNY" |
| 1周      | str   | Y        |  e.g., "11.50/12.00" |
| 1月      | str   | Y        |   |
| 3月      | str   | Y        |   |
| 6月      | str   | Y        |   |
| 9月      | str   | Y        |   |
| 1年      | str   | Y        |   |


注：本行情为询价报价行情(美元为ODM), 实时更新. 
						
接口示例
```python
import akshare as ak
fx_df = ak.get_fx_swap_quote()
print(fx_df)
```

数据示例

人民币外汇远掉报价

```
            ccpair         label_1W         label_1M           label_3M  \
    0      USD/CNY      11.50/12.00      46.00/46.00      125.00/125.00
    1      EUR/CNY      51.90/52.12    218.17/218.56      658.41/658.56
    2   100JPY/CNY      40.03/40.13    177.78/177.83      530.98/531.17
    3      HKD/CNY        2.15/2.17        8.24/8.52        20.48/20.53
    4      GBP/CNY      37.65/37.87    150.56/150.58      445.90/446.01
    5      AUD/CNY      16.57/16.65      70.49/70.58      203.26/203.75
    6      NZD/CNY      16.07/16.22      60.94/61.58      168.29/169.03
    7      SGD/CNY      12.05/12.45      50.49/50.84      144.87/146.50
    8      CHF/CNY      51.31/52.25    218.56/218.56      675.03/675.18
    9      CAD/CNY      12.28/12.28      47.65/47.69      138.33/138.46
    10     CNY/MYR       -0.30/0.17       -0.24/0.61        -2.38/-0.84
    11     CNY/RUB      67.89/73.27    296.66/320.03      882.24/899.51
    12     CNY/ZAR      15.55/16.41      72.06/72.70      213.92/215.87
    13     CNY/KRW      -6.77/-3.84    -29.85/-15.77      -90.62/-52.66
    14     CNY/AED      -0.90/-0.70      -3.38/-2.96        -8.08/-7.46
    15     CNY/SAR      -1.31/-1.14      -4.81/-4.27       -10.27/-9.88
    16     CNY/HUF  -247.54/-213.70  -938.77/-908.44  -2937.98/-2827.36
    17     CNY/PLN      -1.50/-1.37      -5.52/-5.32      -14.85/-14.02
    18     CNY/DKK      -6.88/-6.74    -28.61/-28.13      -87.29/-83.40
    19     CNY/SEK      -8.83/-8.25    -34.51/-33.83    -104.48/-100.71
    20     CNY/NOK      -3.94/-2.84    -13.58/-11.24      -34.81/-33.72
    21     CNY/TRY      13.47/22.01     56.52/103.43      229.52/242.35
    22     CNY/MXN      -4.58/-4.40    -17.57/-17.57      -47.68/-46.55
    23     CNY/THB      -7.25/-6.87    -27.77/-27.72      -75.46/-75.42
                 label_6M           label_9M           label_1Y
    0       205.00/210.00      275.00/278.00      342.50/345.00
    1     1199.68/1201.39    1723.92/1730.71    2246.18/2249.27
    2       963.67/967.95    1402.82/1403.96    1793.50/1801.90
    3         32.31/32.67        40.96/40.96        48.84/49.03
    4       763.21/769.97    1052.69/1054.22    1336.20/1338.15
    5       364.81/364.87      499.29/502.99      623.56/627.52
    6       297.93/301.14      404.95/407.30      517.50/519.69
    7       257.36/259.91      341.81/346.18      427.37/428.44
    8     1237.70/1241.00    1770.44/1774.84    2310.22/2311.93
    9       195.51/199.29      231.22/231.30      263.39/263.40
    10          2.66/5.88        10.64/19.33        20.53/33.38
    11    1780.84/1814.49    2697.91/2759.32    3604.59/3663.77
    12      440.35/442.99      676.02/682.94      919.59/923.42
    13    -167.44/-110.12    -233.82/-171.47    -304.06/-233.52
    14      -13.13/-11.45      -15.97/-14.44      -18.74/-17.22
    15      -15.74/-15.13      -19.89/-18.33      -22.75/-21.21
    16  -5168.11/-4910.26  -7171.99/-6800.90  -9438.87/-8728.19
    17      -23.17/-21.13      -27.96/-25.45      -32.19/-28.86
    18    -158.56/-152.01    -225.33/-216.64    -290.38/-278.70
    19    -180.36/-177.42    -250.27/-248.86    -318.80/-305.83
    20      -50.00/-47.44      -60.16/-56.10      -70.53/-60.84
    21      436.90/494.04      651.61/750.10      895.51/993.76
    22      -79.94/-78.15    -105.72/-104.72    -131.06/-130.29
    23    -126.90/-123.92    -168.07/-166.21    -208.66/-207.02
```

### 外币对即期报价

接口: get_fx_pair_quote

目标地址: http://www.chinamoney.com.cn/chinese/mkdatapfx/

描述: 获取外币对即期报价

限量: 单次返回当前时点最近更新的即时数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

获取外币对即期报价

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 货币对      | str   | Y        |  e.g., "AUD/USD" |
| 买报价      | float   | Y        |  e.g., "0.68460" |
| 卖报价      | float   | Y        |   e.g., "0.68461"|
| 中间价      | float   | Y        |  为空 |
| 时间      | str   | Y        |  为空 |

注：本行情为询价报价行情(美元为ODM), 实时更新. 
						
接口示例
```python
import akshare as ak
fx_df = ak.get_fx_pair_quote()
print(fx_df)
```

数据示例

外币对即期报价

```
            ccyPair   bidPrc   askPrc midprice time
    0   AUD/USD  0.68460  0.68461      ---
    1   EUR/JPY  120.897  120.898      ---
    2   EUR/USD  1.11402  1.11403      ---
    3   GBP/USD  1.28724  1.28727      ---
    4   USD/CAD  1.31339  1.31340      ---
    5   USD/CHF  0.98599  0.98601      ---
    6   USD/HKD  7.84215  7.84217      ---
    7   USD/JPY  108.516  108.517      ---
    8   USD/SGD  1.36483  1.36485      ---
    9   NZD/USD  0.63772  0.63773      ---
    10  EUR/GBP  0.86544  0.86546      ---
```

## [AkShare](https://github.com/jindaxiang/akshare) 私募指数数据
接口: get_zdzk_fund_index

目标地址: https://www.ziasset.com/

描述: 获取智道智科的私募基金指数数据, 可以为用户提供私募基金策略发展方向的参考

限量: 单次返回某一个指数, 建议用 for 循环获取多个指数, 注意不要大量获取, 以免给对方服务器造成压力!

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| country | str  | Y    |   index_type=32, 其中的 32 对应的具体指数, 请参考下表(对应指数代码和名词一览表)|
| index_name | str  | Y    |  plot=True|

对应指数代码和名词一览表

|指数代码|对应名称|
|-------|---------------------|
| 1  | 商品综合           |
| 2  | 中债新综合         |
| 15 | 沪深               |
| 28 | 智道私募综合指数   |
| 30 | 智道股票策略指数   |
| 32 | 智道管理期货指数   |
| 34 | 智道固定收益指数   |
| 36 | 智道相对价值指数   |
| 38 | 智道复合策略指数   |
| 40 | 智道北京区域指数   |
| 42 | 智道上海区域指数   |
| 44 | 智道广州区域指数   |
| 46 | 智道深圳区域指数   |
| 48 | 智道浙江区域指数  |

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 收盘      | float   | Y        | 指数数值, 从 1000 点开始   |



接口示例
```python
import akshare as ak
index_se = ak.get_zdzk_fund_index(index_type=32, plot=True)
print(index_se.name)
print(index_se)
```

数据示例

index_se.name:

```智道管理期货指数```

index_se:

```
2014-12-26    1000.000000
2015-01-02     985.749098
2015-01-09    1032.860242
2015-01-16    1039.978586
2015-01-23    1046.235945
                 ...     
2019-08-30    1397.684642
2019-09-06    1402.711847
2019-09-13    1401.723599
2019-09-20    1386.570103
2019-09-27    1380.657989
```

图片示例
![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/index/zdzd_index.png)

## [AkShare](https://github.com/jindaxiang/akshare) 全球指数数据
接口: get_country_index

目标地址: https://cn.investing.com/indices/

描述: 获取世界主要国家的各种指数, 由于涉及国家和指数(**1000**+个指数)具体参见[国家-指数目录](https://cn.investing.com/indices/world-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on)
具体的调用方式可以参照:

1. 先查询指数所在的国家名称;
2. 复制网页上国家名称(推荐复制), 如 **美国**;
3. 复制所显示的具体指数名称(推荐复制, 如果英文中间有空格, 也需要保留空格), 如 **美元指数**;
4. 在安装 [AkShare](https://github.com/jindaxiang/akshare) 后输入, 如 **ak.get_country_index(country="美国", index_name="美元指数", start_date='2000/01/01', end_date='2019/10/17')**;
5. 稍后就可以获得所需数据.

限量: 单次返回某一个国家的具体某一个指数, 建议用 for 循环获取多个国家的多个指数, 注意不要大量获取, 以免给对方服务器造成压力!

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| country | str  | Y    |   country="美国"|
| index_name | str  | Y    |  index_name="美元指数"|
| start_date | str  | Y    |  start_date='2000/01/01'|
| end_date | str  | Y    |  end_date='2019/10/17'|

输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 收盘      | float   | Y        | 收盘   |
| 开盘      | float   | Y        | 开盘        |
| 高        | float   | Y        |高    |
| 低         | float | Y        | 低         |
| 交易量      | float | Y        | 交易量      |
| 百分比变化  | str | Y        | 百分比变化  |



接口示例
```python
import akshare as ak
index_df = ak.get_country_index(country="美国", index_name="美元指数", start_date='2000/01/01', end_date='2019/10/17')
print(index_df)
print(index_df.name)
```

数据示例

index_df.name:

```美元指数历史数据```

index_df:

```
0               收盘      开盘       高       低 交易量   百分比变化
日期                                                    
2019-05-10   97.33   97.43   97.45   97.13   -  -0.04%
2019-05-09   97.37   97.58   97.70   97.24   -  -0.26%
2019-05-08   97.62   97.57   97.68   97.42   -  -0.01%
2019-05-07   97.63   97.52   97.74   97.38   -   0.11%
2019-05-06   97.52   97.56   97.70   97.46   -   0.00%
...            ...     ...     ...     ...  ..     ...
2000-01-07  100.80  100.49  100.93  100.44   -   0.15%
2000-01-06  100.65  100.31  100.81   99.81   -   0.27%
2000-01-05  100.38  100.42  100.47   99.71   -  -0.03%
2000-01-04  100.41  100.55  100.86  100.01   -   0.19%
2000-01-03  100.22  101.67  101.83  100.19   -  -1.62%
```

## [AkShare](https://github.com/jindaxiang/akshare) 宏观数据

### 中国宏观

#### 中国CPI年率报告
接口: get_china_yearly_cpi

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_cpi_yoy

描述: 获取中国年度CPI数据, 数据区间从19860201-至今

限量: 单次返回某一个所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 年率      | float   | Y        | 年率   |


接口示例
```python
import akshare as ak
index_df = ak.get_china_yearly_cpi()
print(index_df)
print(index_df.name)
```

数据示例

index_df.name:

```cpi```

index_df:

```
1986-02-01    7.1
1986-03-01    7.1
1986-04-01    7.1
1986-05-01    7.1
1986-06-01    7.1
             ... 
2019-07-10    2.7
2019-08-09    2.8
2019-09-10    2.8
2019-10-15      3
2019-11-09      0
```


#### 中国CPI月率报告
接口: get_china_monthly_cpi

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_cpi_mom

描述: 获取中国月度CPI数据, 数据区间从19960201-至今

限量: 单次返回某一个所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 月率      | float   | Y        | 年率   |


接口示例
```python
import akshare as ak
index_df = ak.get_china_monthly_cpi()
print(index_df)
print(index_df.name)
```

数据示例

index_df.name:

```cpi```

index_df:

```
1996-02-01     2.1
1996-03-01     2.3
1996-04-01     0.6
1996-05-01     0.7
1996-06-01    -0.5
              ... 
2019-07-10    -0.1
2019-08-09     0.4
2019-09-10     0.7
2019-10-15     0.9
2019-11-09       0
```

#### 中国M2年率报告
接口: get_china_yearly_m2

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_m2_money_supply_yoy

描述: 获取中国年度M2数据, 数据区间从19980201-至今

限量: 单次返回某一个所有历史数据

输入参数

| 名称   | 类型 | 必选 | 描述                                                                              |
| -------- | ---- | ---- | --- |
| 无 | 无 | 无 | 无 |


输出参数

| 名称          | 类型 | 默认显示 | 描述           |
| --------------- | ----- | -------- | ---------------- |
| 日期      | str   | Y        | 日期-索引  |
| 年率      | float   | Y        | 年率   |


接口示例
```python
import akshare as ak
index_df = ak.get_china_yearly_m2()
print(index_df)
print(index_df.name)
```

数据示例

index_df.name:

```m2```

index_df:

```
1998-02-01    17.4
1998-03-01    16.7
1998-04-01    15.4
1998-05-01    14.6
1998-06-01    15.5
              ... 
2019-09-11     8.2
2019-09-13       0
2019-10-14       0
2019-10-15     8.4
2019-10-17       0
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
root 设置为 [AkShare](https://github.com/jindaxiang/akshare) 爬数据时存储的默认目录(需要保证目录存在), qqEmail 和 secret 为爬取到数据时把数据发送给自己的 qq 邮箱账号和密码. 需要开通SMTP服务, 如果不需要自己邮件提醒, 就不用设置(也不要改默认的qqEmail和secret). 
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

感谢[中国银行间市场交易商协会网站](http://www.nafmii.org.cn/)提供的银行间市场债券基本面数据;

感谢[99期货网站](http://www.99qh.com/)提供的大宗商品库存数据;

感谢[英为财情网站](https://cn.investing.com/)提供的全球股指与期货指数数据, 全球政府债券行情与收益率数据;

感谢[中国外汇交易中心暨全国银行间同业拆借中心网站](http://www.chinamoney.com.cn/chinese/)提供的外汇和债券相关数据;

感谢[金十数据网站](https://www.jin10.com/)提供的全球宏观数据-中国宏观数据;

感谢[中国金融期货交易所网站](http://www.cffex.com.cn/)提供的相关数据;

感谢[上海期货交易所网站](http://www.shfe.com.cn/)提供的相关数据;

感谢[大连商品交易所网站](http://www.dce.com.cn/)提供的相关数据;

感谢[郑州商品交易所网站](http://www.czce.com.cn/)提供的相关数据;

感谢[上海国际能源交易中心网站](http://www.ine.com.cn/)提供的相关数据.


## 交流

欢迎加 QQ 群交流: 326900231

您可以扫码或者点击群二维码申请加入, 请放心点击:

<a target="_blank" href="https://shang.qq.com/wpa/qunwpa?idkey=aacb87089dd5ecb8c6620ce391de15b92310cfb65e3b37f37eb465769e3fc1a3"><img border="0" src="https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/qq/akshare_md_fold_1569925684166.png" alt="AkShare官方" title="AkShare官方"></a>


## 声明

1. [AkShare](https://github.com/jindaxiang/akshare) 提供的数据仅供参考, 不构成任何投资建议;
2. 任何基于 [AkShare](https://github.com/jindaxiang/akshare) 进行研究的投资者请注意数据风险;
3. [AkShare](https://github.com/jindaxiang/akshare) 坚持提供开源金融数据, 请放心使用;
4. [AkShare](https://github.com/jindaxiang/akshare) 的使用请遵循相关开源协议;


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

0.1.64
更新 get_country_index 返回格式为日期索引

0.1.65
更新 get_country_index 返回格式数据开盘, 收盘, 高, 低为浮点型

0.1.66
提供英为财情-债券数据-全球政府债券行情与收益率
https://cn.investing.com/rates-bonds/
新增 get_country_bond 返回格式数据开盘, 收盘, 高, 低为浮点型

0.1.67
更新说明文档-私募指数数据说明

0.1.68
更新说明文档-私募指数数据说明-增加图片

0.1.69
更新说明文档-债券说明格式调整

0.1.70
更新大商所, 郑商所商品期权数据接口

0.1.71
更新大商所, 郑商所, 上期所商品期权数据接口

0.1.72
修改大商所, 郑商所, 上期所商品期权数据接口
增加函数说明
更新说明文档-期权部分

0.1.73
更新说明文档-期权部分

0.1.74
更新说明文档格式调整

0.1.75
新增外汇接口, 银行间债券市场行情数据接口

0.1.76
更新说明文档

0.1.77
新增全球期货历史数据查询接口

0.1.78
新增全球宏观数据-中国年度、月度CPI数据, 年度M2数据

0.1.79
更新说明文档

0.1.80
更新说明文档-刷新

0.1.81
新增全球宏观数据-中国宏观数据
中国年度PPI数据
中国年度PMI数据 
中国年度GDP数据
中国年度财新PMI数据
中国外汇储备数据
中国电力能源数据
中国年度非制造业PMI数据
人民币中间报价汇率
```