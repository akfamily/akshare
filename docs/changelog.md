# [AKShare](https://github.com/akfamily/akshare) 版本更新

## 接口更名一览表

| AKShare 版本 | 旧接口名称             | 新接口名称             | 修改日期     |
|------------|-------------------|-------------------|----------|
| 1.4.88     | fund_em_new_found | fund_new_found_em | 20220323 |
| 1.4.86     | fund_em_aum_hist  | fund_aum_hist_em  | 20220322 |
| 1.4.86     | fund_em_aum_trend | fund_aum_trend_em | 20220322 |
| 1.4.86     | fund_em_aum       | fund_aum_em       | 20220322 |

## 更新说明

1.4.93 add: add macro_china_insurance_income interface

    1. 新增 macro_china_insurance_income 接口，获取原保险保费收入数据

1.4.92 add: add stock_lhb_hyyyb_em interface

    1. 新增 stock_lhb_hyyyb_em 接口，获取东方财富网-数据中心-龙虎榜单-每日活跃营业部数据 

1.4.91 fix: fix macro_china_new_financial_credit interface

    1. 修复 macro_china_new_financial_credit 接口，规范返回字段的类型和按时间排序

1.4.90 add: add macro_china_bank_financing interface

    1. 新增 macro_china_bank_financing 接口，获取银行理财产品发行数量数据

1.4.89 fix: fix stock_us_hist interface

    1. 修复 stock_us_hist 接口，结果数据根据日期排序

1.4.88 fix: fix fund_new_found_em interface
    
    1. 修复 fund_em_new_found 接口命名为 fund_new_found_em 接口

1.4.87 add: add fund_portfolio_industry_allocation_em interface

    1. 新增 fund_portfolio_industry_allocation_em 接口，获取天天基金网-基金档案-投资组合-行业配置数据

1.4.86 fix: fix rename all interface in fund_aum_em.py

    1. 修改 fund_em_aum_hist 接口，重名为 fund_aum_hist_em
    2. 修改 fund_em_aum_trend 接口，重名为 fund_aum_trend_em
    3. 修改 fund_em_aum 接口，重名为 fund_aum_em

1.4.85 add: add fund_portfolio_bond_hold_em interface

    1. 新增 fund_portfolio_bond_hold_em 接口，获取天天基金网-基金档案-投资组合-债券持仓数据

1.4.84 fix: fix fund_portfolio_change_em interface

    1. 修复 fund_portfolio_change_em 接口，新增 indicator 字段

1.4.83 add: add stock_us_code_table_fu interface

    1. 新增 stock_us_code_table_fu 接口，获取股票代码

1.4.82 fix: fix stock_a_code_to_symbol interface

    1. 修复 stock_a_code_to_symbol 接口，支持北交所股票

1.4.81 add: add fund_portfolio_change_em interface

    1. 新增 fund_portfolio_change_em 接口，获取天天基金网-基金档案-投资组合-重大变动数据

1.4.80 add: add stock_board_concept_hist_min_em interface

    1. 新增 stock_board_concept_hist_min_em 接口，获取东方财富-沪深板块-概念板块-分时历史行情数据

1.4.79 add: add stock_board_industry_hist_min_em interface

    1. 新增 stock_board_industry_hist_min_em 接口，获取东方财富-沪深板块-行业板块-分时历史行情数据

1.4.78 add: add remove matplotlib module and support cache

    1. 移除 matplotlib 模块，让 AKShare 更专注于数据采集
    2. 新增缓存，对于速度较慢的接口逐步增加缓存支持
    3. 移除所有接口中的绘图功能
    4. 修复 google_index 接口
    5. 移除 西本新干线 接口
    6. 在 utils 模块中新增 ak_session 以支持缓存
    7. 添加 requests-cache 作为依赖库

1.4.77 fix: fix stock_hk_ggt_components_em interface

    1. 修复 stock_hsgt_em 文件中的所有 pandas.DataFrame 的 append 方法为 concat

1.4.76 add: add stock_lhb_stock_statistic_em interface

    1. 新增 stock_lhb_stock_statistic_em 接口，获取个股上榜统计数据

1.4.75 fix: fix stock_lhb_stock_detail_em interface

    1. 修复 stock_lhb_stock_detail_em 接口，处理有多种排行标准的数据

1.4.74 fix: fix stock_lhb_stock_detail_em interface

    1. 修复 stock_lhb_stock_detail_em 接口返回数据与目标网站统一

1.4.73 add: add stock_lhb_jgmmtj_em interface

    1. 新增 stock_lhb_jgmmtj_em 接口，该接口获取机构买卖每日统计数据

1.4.72 add: add stock_lhb_stock_statistic_em interface

    1. 新增 stock_lhb_stock_statistic_em 接口，该接口获取股票龙虎榜统计详情

1.4.71 add: add stock_lhb_stock_detail_em interface

    1. 新增 stock_lhb_stock_detail_em 接口，该接口获取龙虎榜个股详情数据

1.4.70 add: add stock_lhb_detail_em interface

    1. 新增 stock_lhb_detail_em 接口获取东方财富-股票数据-龙虎榜详情

1.4.69 fix: fix crypto_js_spot interface

    1. 修复 crypto_js_spot 接口，规范字段名称及返回数据的格式

1.4.68 fix: fix crypto_hist interface

    1. 修复 crypto_hist 接口，修改其中返回数据类型

1.4.67 fix: fix crypto_name_url_table interface

    1. 修复 crypto_name_url_table 获取可以获得历史数据的货币名称

1.4.66 fix: fix stock_em_gpzy_profile interface

    1. 修复 stock_em_gpzy_profile 接口并设定返回数据的数据类型

1.4.65 fix: fix spot_hist_sge interface

    1. 修复 spot_hist_sge 接口的数据输出格式

1.4.64 fix: fix bond_china_close_return interface

    1. 修复 bond_china_close_return 接口，修改文档增加描述信息

1.4.63 fix: fix macro_china_swap_rate interface

    1. 修复 macro_china_swap_rate 接口，并规范返回数据的类型

1.4.62 fix: fix option_finance_board interface

    1. 修复 option_finance_board 参数为 华泰柏瑞沪深300ETF期权 时的文档说明

1.4.61 fix: fix get_dce_daily interface

    1. 修复 get_dce_daily 接口的索引问题

1.4.60 fix: fix stock_zh_a_hist_163 interface
    
    1. 修复 stock_zh_a_hist_163 接口的冗余变量问题

1.4.59 add: add stock_zh_a_hist_163 interface

    1. 新增 stock_zh_a_hist_163 接口，用于获取沪深 A 股票的日频率量价数据，主要可以获取总市值和流通市值数据

1.4.58 fix: fix stock_zh_kcb_daily interface

    1. 修复 stock_zh_kcb_daily 返回数据的类型

1.4.57 fix: fix bond_spot_quote interface

    1. 修复 bond_spot_quote 接口数据错位问题

1.4.56 fix: fix index_detail_hist_cni and index_detail_cni interface

    1. 修改 index_detail_hist_cni 接口，新增 date 参数，可以指定 date 来获取数据
    2. 修改 index_detail_cni 的 date 参数的格式为 "202201"

1.4.55 fix: fix energy_carbon interface

    1. 修复 energy_carbon_gz 接口的返回字段格式并且按日期排序
    2. 修复 energy_carbon_hb 接口的返回字段格式并且按日期排序
    3. 修复 energy_carbon_eu 接口的返回字段格式并且按日期排序
    4. 修复 energy_carbon_sz 接口的返回字段格式并且按日期排序
    5. 修复 energy_carbon_bj 接口的返回字段格式并且按日期排序
    6. 修复上述接口的文档描述信息

1.4.54 fix: fix stock_hot_rank_relate_em interface

    1. 修复 stock_hot_rank_relate_em 接口的字段描述信息

1.4.53 add: add stock_hot_rank_relate_em interface

    1. 新增 stock_hot_rank_relate_em 接口，该接口可以获取东方财富-个股人气榜-相关股票数据

1.4.52 add: add stock_hot_rank_latest_em interface

    1. 新增 stock_hot_rank_latest_em 接口，该接口可以获取东方财富-个股人气榜-人气排名数据

1.4.51 add: add stock_hot_keyword_em interface

    1. 新增 stock_hot_keyword_em 接口，该接口可以获取指定股票的相关实时热门概念数据

1.4.50 add: add stock_hot_rank_detail_realtime_em interface

    1. 新增 stock_hot_rank_detail_realtime_em 接口，该接口可以获取东方财富个股人气榜-实时变动数据

1.4.49 fix: fix stock_sse_deal_daily interface

    1. 修复 stock_sse_deal_daily 接口，因为请求返回值新增了字段
    2. 划分为 20211224、20220224 和 20220225 之后三个时间段进行请求

1.4.48 fix: fix stock_sse_deal_daily interface

    1. 修复 stock_sse_deal_daily 接口，因为请求返回值新增了字段

1.4.47 add: add interface change log

    1. 增加接口更新的详细说明文档

1.4.46 fix: fix energy_oil_detail interface

    1. 修改 energy_oil_detail 的返回日期格式，从 '2022/1/1' 为 '2022-01-01'
    2. 修改 energy_oil_detail 的请求日期格式，从 '2022-01-01' 为 '20220101'
    3. 修改 energy_oil_hist 和 energy_oil_detail 的返回值数据格式为 Pandas 的数据类型
    4. 修改 energy_oil_hist 和 energy_oil_detail 的函数签名

1.4.45 fix: fix air_quality_rank interface

    1. 修改 air_city_list 的接口命名，修改后为 air_city_talbe
    2. 修改 air_quality_watch_point 接口的请求日期格式，从 '2022-01-01' 为 '20220101'
    3. 修改 air_quality_hist 接口的请求日期格式，从 '2022-01-01' 为 '20220101'

## 版本更新说明

1.4.93 add: add macro_china_insurance_income interface

1.4.92 add: add stock_lhb_hyyyb_em interface

1.4.91 fix: fix macro_china_new_financial_credit interface

1.4.90 add: add macro_china_bank_financing interface

1.4.89 fix: fix stock_us_hist interface

1.4.88 fix: fix fund_new_found_em interface

1.4.87 add: add fund_portfolio_industry_allocation_em interface

1.4.86 fix: fix rename all interface in fund_aum_em.py

1.4.85 add: add fund_portfolio_bond_hold_em interface

1.4.84 fix: fix fund_portfolio_change_em interface

1.4.83 add: add stock_us_code_table_fu interface

1.4.82 fix: fix stock_a_code_to_symbol interface

1.4.81 add: add fund_portfolio_change_em interface

1.4.80 add: add stock_board_concept_hist_min_em interface

1.4.79 add: add stock_board_industry_hist_min_em interface

1.4.78 add: add remove matplotlib module and support cache

1.4.77 fix: fix stock_hk_ggt_components_em interface

1.4.76 add: add stock_lhb_stock_statistic_em interface

1.4.75 fix: fix stock_lhb_stock_detail_em interface

1.4.74 fix: fix stock_lhb_stock_detail_em interface

1.4.73 add: add stock_lhb_jgmmtj_em interface

1.4.72 add: add stock_lhb_stock_statistic_em interface

1.4.71 add: add stock_lhb_stock_detail_em interface

1.4.70 add: add stock_lhb_detail_em interface

1.4.69 fix: fix crypto_js_spot interface

1.4.68 fix: fix crypto_hist interface

1.4.67 fix: fix crypto_name_url_table interface

1.4.66 fix: fix stock_em_gpzy_profile interface

1.4.65 fix: fix spot_hist_sge interface

1.4.64 fix: fix bond_china_close_return interface

1.4.63 fix: fix macro_china_swap_rate interface

1.4.62 fix: fix option_finance_board interface

1.4.61 fix: fix get_dce_daily interface

1.4.60 fix: fix stock_zh_a_hist_163 interface

1.4.59 add: add stock_zh_a_hist_163 interface

1.4.58 fix: fix stock_zh_kcb_daily interface

1.4.57 fix: fix bond_spot_quote interface

1.4.56 fix: fix index_detail_hist_cni and index_detail_cni interface

1.4.55 fix: fix energy_carbon interface

1.4.54 fix: fix stock_hot_rank_relate_em interface

1.4.53 add: add stock_hot_rank_relate_em interface

1.4.52 add: add stock_hot_rank_latest_em interface

1.4.51 add: add stock_hot_keyword_em interface

1.4.50 add: add stock_hot_rank_detail_realtime_em interface

1.4.49 fix: fix stock_sse_deal_daily interface

1.4.48 fix: fix stock_sse_deal_daily interface

1.4.47 add: add interface change log

1.4.46 fix: fix energy_oil_detail interface

1.4.45 fix: fix air_quality_rank interface
