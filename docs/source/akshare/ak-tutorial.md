# 快速入门

## 1. 先按照 [Anaconda安装说明及环境配置](#Anaconda安装说明及环境配置)

## 2. 查看 [AkShare](https://github.com/jindaxiang/akshare) 提供的数据接口

**Example 2.1** 查看 [AkShare](https://github.com/jindaxiang/akshare) 提供的数据接口

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
 # 宏观-中国
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
 # 宏观-美国
 'get_usa_interest_rate'  # 联储利率决议报告
 'get_usa_non_farm'  # 美国非农就业人数报告
 'get_usa_unemployment_rate'  # 美国失业率报告
 'get_usa_eia_crude_rate'  # 美国EIA原油库存报告
 'get_usa_core_pce_price'  # 美国核心PCE物价指数年率报告
 'get_usa_cpi_monthly'  # 美国CPI月率报告
 'get_usa_crude_alaska'  # 美国原油产量报告-美国阿拉斯加州原油产量
 'get_usa_crude_inner'  # 美国原油产量报告-美国国内原油总量
 'get_usa_crude_state'  # 美国原油产量报告-美国本土48州原油产量
 'get_usa_gdp_monthly'  # 美国国内生产总值(GDP)报告
 'get_usa_initial_jobless'  # 美国初请失业金人数报告
 'get_usa_lmci'  # 美联储劳动力市场状况指数报告
 'get_usa_adp_employment'  # 美国ADP就业人数报告
 # 宏观-欧洲
 'get_euro_interest_rate'  # 欧洲央行决议报告
 # 宏观-主要机构
 'get_cons_gold_amount'  # 全球最大黄金ETF—SPDR Gold Trust持仓报告-总价值
 'get_cons_gold_change'  # 全球最大黄金ETF—SPDR Gold Trust持仓报告-增持/减持
 'get_cons_gold_volume'  # 全球最大黄金ETF—SPDR Gold Trust持仓报告-总库存
 'get_cons_opec_month'  # 欧佩克报告-差异
 'get_cons_opec_near_change'  # 欧佩克报告-月份
 'get_cons_silver_amount'  # 全球最大白银ETF--iShares Silver Trust持仓报告-总价值
 'get_cons_silver_change'  # 全球最大白银ETF--iShares Silver Trust持仓报告-增持/减持
 'get_cons_silver_volume'  # 全球最大白银ETF--iShares Silver Trust持仓报告-总库存
 # 期货-仓单有效期
 'get_receipt_date'  # 期货仓单有效期数据
 # 中国期货跨期价差(自由价差)数据接口
 'get_futures_csa_params'  # 获取跨期价差参数
 'get_futures_csa_history'  # 获取跨期价差历史数据
 'get_futures_csa_seasonally'  # 获取跨期价差季节性数据
 # 新浪财经-期货
 'futures_zh_spot'  # 获取新浪-国内期货实时行情数据
 'futures_hq_spot'  # 获取新浪-外盘期货实时行情数据
 # 交易所金融期权数据
 'get_finance_option'  # 提供上海证券交易所期权数据
 # 数字货币行情
 'get_js_dc_current'  # 提供主流数字货币行情数据接口
 # 股票-企业社会责任
 'stock_zh_a_scr_report'  # 企业社会责任数据
 # 美股-中国概念股行情和历史数据
 'stock_us_zh_spot'  # 中国概念股行情
 'stock_us_zh_daily'  # 中国概念股历史数据
 # 新浪财经-港股
 'stock_hk_spot'  # 获取港股的历史行情数据(包括前后复权因子)
 'stock_hk_daily'  # 获取港股的实时行情数据(也可以用于获得所有港股代码)
 # 新浪财经-美股
 'stock_us_name'  # 获得美股的所有股票代码
 'stock_us_spot'  # 获取美股行情报价
 'stock_us_daily'  # 获取美股的历史数据(包括前复权因子)
 # A+H股实时行情数据和历史行情数据
 'stock_zh_ah_spot'  # 获取 A+H 股实时行情数据(延迟15分钟)
 'stock_zh_ah_daily'  # 获取 A+H 股历史行情数据(日频)
 'stock_zh_ah_name'  # 获取 A+H 股所有股票代码
 # A股实时行情数据和历史行情数据
 'stock_zh_a_spot'  # 获取 A 股实时行情数据
 'stock_zh_a_daily'  # 获取 A 股历史行情数据(日频)
 # 科创板实时行情数据和历史行情数据
 'stock_zh_kcb_spot'  # 获取科创板实时行情数据
 'stock_zh_kcb_daily'  # 获取科创板历史行情数据(日频)
 # 银保监分局本级行政处罚数据
 'bank_fjcf'  # 获取银保监分局本级行政处罚
 # 已实现波动率数据
 'article_oman_rv'  # O-MAN已实现波动率
 'article_rlab_rv'  # Risk-Lab已实现波动率
 # FF多因子模型数据
 'ff_crr'  # FF当前因子
 # 指数实时行情和历史行情
 'stock_zh_index_daily'  # 股票指数历史行情数据
 'stock_zh_index_spot'  # 股票指数实时行情数据
 # 股票分笔数据
 'stock_zh_a_tick'  # A股票分笔行情数据(近2年)
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
