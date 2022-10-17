# [AKShare](https://github.com/akfamily/akshare) 版本更新

## 接口更名一览表

| AKShare 版本 | 旧接口名称                                       | 新接口名称                                       | 修改日期     |
|------------|---------------------------------------------|---------------------------------------------|----------|
| 1.7.27     | stock_em_qsjy                               | stock_qsjy_em                               | 20220921 |
| 1.7.23     | futures_pig_info                            | futures_hog_info                            | 20220916 |
| 1.7.23     | futures_pig_rank                            | futures_hog_rank                            | 20220916 |
| 1.6.86     | stock_em_gpzy_distribute_statistics_company | stock_gpzy_distribute_statistics_company_em | 20220811 |
| 1.6.86     | stock_em_gpzy_distribute_statistics_bank    | stock_gpzy_distribute_statistics_bank_em    | 20220811 |
| 1.5.94     | bond_conv_adj_logs_jsl                      | bond_cb_adj_logs_jsl                        | 20220524 |
| 1.5.94     | bond_cov_jsl                                | bond_cb_jsl                                 | 20220524 |
| 1.5.53     | stock_em_xjll                               | stock_xjll_em                               | 20220501 |
| 1.5.53     | stock_em_lrb                                | stock_lrb_em                                | 20220501 |
| 1.5.53     | stock_em_zcfz                               | stock_zcfz_em                               | 20220501 |
| 1.5.52     | stock_em_ggcg                               | stock_ggcg_em                               | 20220501 |
| 1.5.48     | futures_nh_price_index                      | futures_price_index_nh                      | 20220428 |
| 1.5.48     | futures_nh_index_symbol_table               | futures_index_symbol_table_nh               | 20220428 |
| 1.5.48     | futures_nh_return_index                     | futures_return_index_nh                     | 20220428 |
| 1.5.46     | stock_em_yzxdr                              | stock_yzxdr_em                              | 20220427 |
| 1.5.34     | stock_em_gpzy_industry_data                 | stock_gpzy_industry_data_em                 | 20220420 |
| 1.5.26     | stock_em_comment                            | stock_comment_em                            | 20220415 |
| 1.5.25     | stock_em_analyst_detail                     | stock_analyst_detail_em                     | 20220415 |
| 1.5.25     | stock_em_analyst_rank                       | stock_analyst_rank_em                       | 20220415 |
| 1.5.18     | fund_em_open_fund_rank                      | fund_open_fund_rank_em                      | 20220414 |
| 1.5.12     | stock_em_gpzy_pledge_ratio_detail           | stock_gpzy_pledge_ratio_detail_em           | 20220410 |
| 1.5.10     | stock_em_gpzy_pledge_ratio                  | stock_gpzy_pledge_ratio_em                  | 20220410 |
| 1.5.10     | stock_em_gpzy_profile                       | stock_gpzy_profile_em                       | 20220410 |
| 1.4.88     | fund_em_new_found                           | fund_new_found_em                           | 20220323 |
| 1.4.86     | fund_em_aum_hist                            | fund_aum_hist_em                            | 20220322 |
| 1.4.86     | fund_em_aum_trend                           | fund_aum_trend_em                           | 20220322 |
| 1.4.86     | fund_em_aum                                 | fund_aum_em                                 | 20220322 |

## 更新说明

1.7.55 add: add fx_quote_baidu interface

    1. 新增 fx_quote_baidu 接口

1.7.54 fix: fix stock_a_lg_indicator interface

    1. 修复 stock_a_lg_indicator 接口

1.7.53 add: add stock_buffett_index_lg interface

    1. 新增 stock_buffett_index_lg 接口

1.7.52 fix: fix stock_sse_summary interface

    1. 修复 stock_sse_summary 接口的字段对齐问题

1.7.51 fix: fix stock_a_lg_indicator interface

    1. 修复 stock_a_lg_indicator 接口

1.7.50 add: add stock_hot_search_baidu interface

    1. 新增 stock_hot_search_baidu 接口，获取百度热搜股票的数据

1.7.49 add: add futures_news_baidu interface

    1. 新增 futures_news_baidu 接口，获取百度股市通中期货相关新闻数据

1.7.48 add: add stock_zh_vote_baidu interface

    1. 新增 stock_zh_vote_baidu 接口

1.7.47 add: add stock_zh_valuation_baidu interface

    1. 新增 stock_zh_valuation_baidu 接口

1.7.46 fix: fix stock_hk_valuation_baidu interface

    1. 修复 stock_hk_valuation_baidu 接口

1.7.45 add: add stock_hk_valuation_baidu interface

    1. 新增 stock_hk_valuation_baidu 接口

1.7.44 add: add stock_allotment_cninfo interface

    1. 新增 stock_allotment_cninfo 接口

1.7.43 fix: fix stock_a_all_pb interface

    1. 修复 stock_a_all_pb 接口

1.7.42 add: add stock_sgt_reference_exchange_rate_szse interface

    1. 新增 stock_sgt_reference_exchange_rate_szse 接口

1.7.41 add: add stock_sgt_reference_exchange_rate_sse interface

    1. 新增 stock_sgt_reference_exchange_rate_sse 接口

1.7.40 add: add stock_sgt_settlement_exchange_rate_sse interface

    1. 新增 stock_sgt_settlement_exchange_rate_sse 接口

1.7.39 add: add stock_sgt_settlement_exchange_rate_szse interface

    1. 新增 stock_sgt_settlement_exchange_rate_szse 接口

1.7.38 add: add sw_index_second_info interface

    1. 新增 sw_index_second_info 接口

1.7.37 add: add sw_index_first_info interface

    1. 新增 sw_index_first_info 接口

1.7.36 fix: fix rename branch master to main

    1. 将项目的 master 分支重命名为 main

1.7.35 fix: fix stock_market_fund_flow interface

    1. 修复 stock_market_fund_flow 接口，规范数据输出格式

1.7.34 fix: fix bond_cb_jsl interface

    1. 修复 bond_cb_jsl 接口，统一字段

1.7.33 fix: fix stock_zh_ah_daily interface

    1. 修复 stock_zh_ah_daily 接口，调整输出的格式

1.7.32 fix: fix stock_a_ttm_lyr interface

    1. 修复 stock_a_ttm_lyr 接口

1.7.31 fix: fix stock_a_lg_indicator interface

    1. 修复 stock_a_lg_indicator 接口，调整输出的格式

1.7.30 fix: fix bond_cb_index_jsl interface

    1. 修复 bond_cb_index_jsl 接口

1.7.29 fix: fix stock_us_daily interface

    1. 修复 stock_us_daily 接口，去除索引

1.7.28 fix: fix stock_info_sh_name_code interface

    1. 修复 stock_info_sh_name_code 接口

1.7.27 fix: fix stock_qsjy_em interface

    1. 修复 stock_qsjy_em 接口

1.7.26 add: add bond_new_composite_index_cbond interface

    1. 新增 bond_new_composite_index_cbond 接口

1.7.25 add: add news_trade_notify_dividend_baidu interface

    1. 新增 news_trade_notify_dividend_baidu 接口

1.7.24 fix: fix amac_manager_classify_info interface

    1. 修复 amac_manager_classify_info 接口，增加输出字段及规范输出字段格式

1.7.23 fix: fix rename futures_pig_info and futures_pig_rank interface

    1. 修复 futures_pig_info 重命名为 futures_hog_info
    2. 修复 futures_pig_rank 重命名为 futures_hog_info

1.7.22 add: add index_investing_global_area_index_name_url interface

    1. 新增 index_investing_global_area_index_name_url 接口

1.7.21 fix: fix futures_hog_info interface

    1. 修复 futures_hog_info 接口，同意目标网站地址

1.7.20 fix: fix crypto_js_spot interface

    1. 修复 crypto_js_spot 接口

1.7.19 fix: fix index_value_name_funddb interface

    1. 修复 index_value_name_funddb 接口，新增字段及文档说明

1.7.18 fix: fix stock_lhb_jgmmtj_em interface

    1. 修复 stock_lhb_jgmmtj_em 接口

1.7.17 fix: fix bond_cb_jsl interface

    1. 修复 bond_cb_jsl 接口

1.7.16 fix: fix crypto_js_spot interface

    1. 修复 crypto_js_spot 接口

1.7.15 fix: fix news_economic_baidu interface

    1. 修复 news_economic_baidu 接口

1.7.14 fix: fix covid_19_risk_area interface

    1. 修复 covid_19_risk_area 接口

1.7.13 fix: fix stock_balance_sheet_by_yearly_em interface

    1. 修复 stock_balance_sheet_by_yearly_em 接口

1.7.12 fix: fix stock_repurchase_em interface

    1. 修复 stock_repurchase_em 接口

1.7.11 fix: fix bond_cash_summary_sse interface

    1. 修复 bond_cash_summary_sse 接口

1.7.10 fix: fix option_czce_daily interface

    1. 修复 option_czce_daily 接口，增加花生期权和菜籽油期权的支持

1.7.9 add: add index_market_representation_hist_sw interface

    1. 新增 index_market_representation_hist_sw 接口

1.7.8 add: add index_style_index_hist_sw interface

    1. 新增 index_style_index_hist_sw 接口

1.7.7 add: add index_level_one_hist_sw interface

    1. 新增 index_level_one_hist_sw 接口

1.7.6 fix: fix covid_19_risk_area interface

    1. 修复 covid_19_risk_area 接口

1.7.5 fix: fix fund_fh_em interface

    1. 修复 fund_fh_em 接口

1.7.4 fix: fix stock_analyst_rank_em interface

    1. 修复 stock_analyst_rank_em 接口，规范输出格式

1.7.3 fix: fix stock_profit_sheet_by_report_em interface

    1. 修复 stock_profit_sheet_by_report_em 接口

1.7.2 fix: fix futures_egg_price_yearly interface

    1. 修复 futures_egg_price_yearly 接口
    2. 修复 futures_egg_price 接口
    3. 修复 futures_egg_price_area 接口

1.7.1 fix: fix fund_etf_fund_info_em interface

    1. 修复 fund_etf_fund_info_em 接口，提高访问速度并规范输出格式

1.6.99 fix: fix macro_china_fx_gold interface

    1. 修复 macro_china_fx_gold 接口

1.6.98 fix: fix macro_china_real_estate interface

    1. 修复 macro_china_real_estate 接口

1.6.97 fix: fix macro_china_real_estate interface

    1. 修复 macro_china_real_estate 接口

1.6.96 fix: fix macro_china_bond_public interface

    1. 修复 macro_china_bond_public 接口

1.6.95 fix: fix energy_oil_detail interface

    1. 修复 energy_oil_detail 接口

1.6.94 fix: fix macro_china_hk_market_info interface

    1. 修复 macro_china_hk_market_info 接口，规范数据输出格式

1.6.93 fix: fix index_vix interface

    1. 修复 index_vix 接口

1.6.92 fix: fix hurun_rank interface

    1. 修复 hurun_rank 接口
    2. 修复 death_company 接口
    3. 修复 nicorn_company 接口
    4. 修复 maxima_company 接口

1.6.91 fix: fix forbes_rank interface

    1. 修复 forbes_rank 接口，取消证书验证

1.6.90 fix: fix macro_china_cpi_yearly interface

    1. 修复 macro_china_cpi_yearly 接口，规范输出格式

1.6.89 fix: fix stock_board_concept_name_ths interface

    1. 修复 stock_board_concept_name_ths 接口，增加字段说明

1.6.88 fix: fix option_cffex_zz1000_spot_sina interface

    1. 修复 option_cffex_zz1000_spot_sina 接口，规范输出数据格式

1.6.87 fix: fix stock_ggcg_em interface

    1. 修复 stock_ggcg_em 接口，增加 symbol 字段

1.6.86 fix: fix stock_gpzy_distribute_statistics_bank_em interface

    1. 修复 stock_gpzy_distribute_statistics_bank_em 接口，更新接口及文档
    2. 修复 stock_gpzy_distribute_statistics_company_em 接口，更新接口及文档

1.6.85 fix: fix option_finance_board interface

    1. 修复 option_finance_board 接口，新增对中证1000股指期权的支持

1.6.84 fix: fix stock_zt_pool_em interface

    1. 修复 stock_zt_pool_em 接口

1.6.83 fix: fix option_dce_daily interface

    1. 修复 option_dce_daily 接口，新增黄大豆1号，黄大豆2号，豆油等期权等支持

1.6.82 fix: fix option_cffex_hs300_spot_sina interface

    1. 修复 option_cffex_hs300_spot_sina 接口，对字段做异常处理

1.6.81 fix: fix currency_hist interface

    1. 修复 currency_hist 接口，同时修改该函数的参数及输出字段

1.6.80 fix: fix index_investing_global interface

    1. 修复 index_investing_global 接口，同时修改该函数的参数及输出字段

1.6.79 fix: fix fund_rating_all interface

    1. 修复 fund_rating_all 接口，字段与目标网站对齐

1.6.78 fix: fix stock_telegraph_cls interface

    1. 移除 pycryptodomex 依赖
    2. 移除冗余代码

1.6.77 fix: fix stock_telegraph_cls interface

    1. 修复 stock_telegraph_cls 接口

1.6.76 add: add pycryptodomex library

    1. 新增 pycryptodomex 依赖库支持

1.6.75 add: add option_cffex_zz1000_spot_sina interface

    1. 新增 option_cffex_zz1000_spot_sina 接口
    2. 将 stock_technology_ths.py 中所有接口 append 方法移除

1.6.74 add: add option_cffex_zz1000_list_sina interface

    1. 新增 option_cffex_zz1000_list_sina 接口
    2. 新增 option_cffex_zz1000_spot_sina 接口
    3. 新增 option_cffex_zz1000_daily_sina 接口

1.6.73 fix: fix macro_china_rmb interface

    1. 修复 macro_china_rmb 接口，规范输出的格式

1.6.72 add: add futures_news_shmet interface

    1. 新增 futures_news_shmet 接口，获取期货资讯数据

1.6.71 fix: fix bond_zh_hs_cov_pre_min interface

    1. 修复 bond_zh_hs_cov_pre_min 接口

1.6.70 add: add bond_zh_hs_cov_pre_min interface

    1. 新增 bond_zh_hs_cov_pre_min 接口，获取可转债的盘前分时数据

1.6.69 add: add fund_info_index_em interface

    1. 新增 fund_info_index_em 接口，获取指数型基金的基本信息

1.6.68 fix: fix stock_zh_a_minute interface

    1. 修复 stock_zh_a_minute 接口

1.6.67 fix: fix stock_zh_a_alerts_cls interface

    1. 修复 stock_zh_a_alerts_cls 接口，增加移除警告信息

1.6.66 fix: fix stock_balance_sheet_by_report_em interface

    1. 修复 stock_balance_sheet_by_report_em 接口，新增公司类型判断

1.6.65 fix: fix bond_cb_redeem_jsl interface

    1. 修复 bond_cb_redeem_jsl 接口，新增字段

1.6.64 fix: fix index_investing_global interface

    1. 修复 index_investing_global 接口的参数及文档说明

1.6.63 fix: fix fund_portfolio_em and futures_roll_yield interface

    1. 修复 fund_portfolio_em 和 futures_roll_yield 文件中的 pandas.DataFrame.append 问题

1.6.62 fix: fix futures_zh_spot interface

    1. 修复 futures_zh_spot 接口

1.6.61 fix: fix futures_shfe_warehouse_receipt interface

    1. 修复 futures_shfe_warehouse_receipt 接口，在 20140519 分开处理

1.6.60 add: add stock_telegraph_cls interface

    1. 新增 stock_telegraph_cls 接口

1.6.59 add: add stock_industry_change_cninfo interface

    1. 新增 stock_industry_change_cninfo 接口

1.6.58 fix: fix stock_gdfx_holding_analyse_em interface

    1. 修复 stock_gdfx_holding_analyse_em 接口

1.6.57 fix: fix stock_info_sh_name_code interface

    1. 修复 stock_info_sh_name_code 接口

1.6.56 fix: fix index_zh_a_hist interface

    1. 修复 index_zh_a_hist 接口

1.6.55 fix: fix stock_gdfx_free_holding_analyse_em interface

    1. 修复 stock_gdfx_free_holding_analyse_em 接口

1.6.54 fix: fix stock_hsgt_hold_stock_em interface

    1. 修复 stock_hsgt_hold_stock_em 接口

1.6.53 fix: fix fx_spot_quote interface

    1. 修复 fx_spot_quote 接口

1.6.52 fix: fix index_zh_a_hist interface

    1. 修复 index_zh_a_hist 接口，增加更多指数支持

1.6.51 fix: fix stock_analyst_detail_em interface

    1. 修复 stock_analyst_detail_em 接口，处理空数据情况

1.6.50 add: add stock_industry_category_cninfo interface

    1. 新增 stock_industry_category_cninfo 接口
    2. 新增 stock_industry_change_cninfo 接口
    3. 新增 stock_share_change_cninfo 接口
    4. 新增 stock_classify_sina 接口

1.6.49 fix: fix stock_zh_a_alerts_cls interface

    1. 修复 stock_zh_a_alerts_cls 接口

1.6.48 fix: fix stock_report_disclosure interface

    1. 修复 stock_report_disclosure 接口，添加北交所的数据

1.6.47 fix: fix stock_zh_a_minute interface

    1. 修复 stock_zh_a_minute 接口

1.6.46 fix: fix fund_open_fund_info_em interface

    1. 修复 fund_open_fund_info_em 接口

1.6.45 fix: fix stock_zh_index_hist_csindex interface

    1. 修复 stock_zh_index_hist_csindex 接口

1.6.44 fix: fix futures_inventory_em interface

    1. 修复 futures_inventory_em 接口

1.6.43 fix: fix futures_inventory_99 interface

    1. 修复 futures_inventory_99 接口

1.6.42 fix: fix stock_balance_sheet_by_yearly_em interface

    1. 修复 stock_balance_sheet_by_report_em 接口
    2. 修复 stock_balance_sheet_by_yearly_em 接口
    3. 修复 stock_profit_sheet_by_report_em 接口
    4. 修复 stock_profit_sheet_by_yearly_em 接口
    5. 修复 stock_profit_sheet_by_quarterly_em 接口
    6. 修复 stock_cash_flow_sheet_by_report_em 接口
    7. 修复 stock_cash_flow_sheet_by_yearly_em 接口
    8. 修复 stock_cash_flow_sheet_by_quarterly_em 接口

1.6.41 add: add futures_inventory_99 interface

    1. 新增 futures_inventory_99 接口，获取大宗商品库存数据

1.6.40 add: add stock_mda_ym interface

    1. 新增 stock_mda_ym 接口，获取管理层讨论与分析数据

1.6.39 fix: fix futures_symbol_mark interface

    1. 修复 futures_symbol_mark 接口编码问题

1.6.38 add: add stock_zygc_ym interface

    1. 新增 stock_zygc_ym 接口，获取股票的主营构成数据

1.6.37 fix: remove futures_inventory_99 interface

    1. 移除 futures_inventory_99 接口

1.6.36 fix: fix option_finance_board interface

    1. 修复 option_finance_board 接口

1.6.35 fix: fix stock_zh_index_hist_csindex interface

    1. 修复 stock_zh_index_hist_csindex 接口

1.6.34 fix: fix fx_spot_quote interface

    1. 修复 fx_spot_quote 接口，输出字段
    2. 修复 fx_swap_quote 接口，输出字段
    3. 修复 fx_pair_quote 接口，输出字段

1.6.33 fix: fix stock_report_fund_hold_detail interface

    1. 修复 stock_report_fund_hold_detail 接口

1.6.32 fix: fix get_czce_daily interface

    1. 修复 get_czce_daily 接口，获取 2010 年数据

1.6.31 fix: fix stock_gdfx_free_holding_detail_em interface

    1. 修复 stock_gdfx_free_holding_detail_em 接口，规范输出字段

1.6.30 fix: fix stock_info_a_code_name interface

    1. 修复 stock_info_a_code_name 接口，增加缓存

1.6.29 fix: fix stock_board_industry_name_em interface

    1. 修复 stock_board_industry_name_em 接口，输出字段容错处理

1.6.28 add: add currency_boc_safe interface

    1. 新增 currency_boc_safe 接口，获取人民币汇率中间价数据

1.6.27 fix: fix currency_boc_sina interface

    1. 修复 currency_boc_sina 接口，输出结果按时间排序

1.6.26 fix: fix bond_cb_index_jsl interface

    1. 修复 bond_cb_index_jsl 接口，对于 script 使用 string 适配 Linux 及 MacOS

1.6.25 fix: fix bond_cb_index_jsl interface

    1. 修复 bond_cb_index_jsl 接口，去除 lxml 解析器

1.6.24 fix: fix bond_cb_index_jsl interface

    1. 修复 bond_cb_index_jsl 接口，使用 ast.eval 替换

1.6.23 fix: fix bond_cb_index_jsl interface

    1. 修复 bond_cb_index_jsl 接口，适配 Linux 及 MacOS

1.6.22 add: add stock_kc_a_spot_em interface

    1. 新增 stock_kc_a_spot_em 接口，获取科创板行情

1.6.21 fix: fix baidu_search_index interface

    1. 修复 baidu_search_index 接口
    2. 修复 baidu_info_index 接口
    3. 修复 baidu_media_index 接口

1.6.20 fix: fix stock_board_industry_name_em and code_id_map_em interface

    1. 修复 stock_board_industry_name_em 接口，字段容错处理
    2. 修复 code_id_map_em 接口，股票超过 5000 只处理

1.6.19 fix: fix stock_comment_detail_zlkp_jgcyd_em interface

    1. 修复 stock_comment_detail_zlkp_jgcyd_em 接口

1.6.18 fix: fix stock_zh_a_spot_em interface

    1. 修复 stock_zh_a_spot_em 接口，增加股票获取的数量，目前已经超过 5000 只

1.6.17 fix: fix stock_new_a_spot_em interface

    1. 修复 stock_new_a_spot_em 接口上市日期字段

1.6.16 fix: fix baidu_search_index interface

    1. 修复 baidu_search_index 接口，对该接口增加 text 字段

1.6.15 fix: fix bond_zh_cov_info interface

    1. 修复 bond_zh_cov_info 接口，修改接口参数及返回数据

1.6.14 fix: fix stock_hsgt_board_rank_em interface

    1. 修复 stock_hsgt_board_rank_em 接口，字段调整

1.6.13 add: add stock_new_a_spot_em interface

    1. 新增 stock_new_a_spot_em 接口，获取新股行情数据

1.6.12 add: add stock_bj_a_spot_em interface

    1. 新增 stock_bj_a_spot_em 接口，获取北交所 A 股行情数据

1.6.11 add: add stock_sz_a_spot_em interface

    1. 新增 stock_sz_a_spot_em 接口，获取深证 A 股行情数据

1.6.10 add: add stock_sh_a_spot_em interface

    1. 新增 stock_sh_a_spot_em 接口，获取上证 A 股行情数据

1.6.9 fix: fix stock_zh_a_spot_em interface

    1. 修复 stock_zh_a_spot_em 接口，新增多个字段

1.6.8 fix: fix futures_zh_spot interface

    1. 修复 futures_zh_spot 接口

1.6.7 add: add futures_zh_realtime interface

    1. 新增 futures_zh_realtime 接口，获取期货的实时行情数据
    2. 新增 futures_symbol_mark 接口，获取新浪期货的所有品种标识

1.6.6 fix: fix fund_etf_hist_sina interface

    1. 修复 fund_etf_hist_sina 接口，规范输出数据类型

1.6.5 fix: fix stock_board_cons_ths interface

    1. 修复 stock_board_cons_ths 接口，修复获取链接的逻辑
    2. 给接口 stock_board_concept_name_ths 增加缓存功能

1.6.4 fix: fix stock_info_a_code_name interface

    1. 修复 stock_info_a_code_name 接口，调整文档输出

1.6.3 fix: fix stock_info_a_code_name and stock_info_sh_delist interface

    1. 修复 stock_info_a_code_name 接口，调整字段
    2. 修复 stock_info_sh_delist 接口，调整字段

1.6.2 fix: fix macro_china_cpi interface

    1. 修复 macro_china_cpi 接口，输出按日期排序

1.6.1 fix: fix stock_info_sh_name_code interface

    1. 修复 stock_info_sh_name_code 接口，字段对齐

1.5.99 fix: fix stock_zh_a_hist_163 interface

    1. 修复 stock_zh_a_hist_163 接口，修改编码格式为 GBK 编码

1.5.98 fix: fix news_cctv interface

    1. 修复 news_cctv 接口，适配 20220523 之后的新页面

1.5.97 fix: fix stock_zh_a_hist interface

    1. 修复 stock_zh_a_hist 接口，除以日期设置的边界问题

1.5.96 fix: fix macro_bank_usa_interest_rate interface

    1. 修复 macro_bank_usa_interest_rate 接口，规范输出数据格式且按时间排序

1.5.95 fix: fix stock_zh_a_hist_163 interface

    1. 修复 stock_zh_a_hist_163 接口，增加编码支持

1.5.94 add: add bond_cb_redeem_jsl interface

    1. 新增 bond_cb_redeem_jsl 接口，获取可转债强赎数据

1.5.93 fix: fix stock_zh_a_hist interface

    1. 修复 stock_zh_a_hist 接口，对非交易日及停牌日期返回 pandas.DataFrame

1.5.92 fix: fix rate_interbank interface

    1. 修复 rate_interbank 接口，修改函数签名及输出格式

1.5.91 add: add bond_cb_index_jsl interface

    1. 新增 bond_cb_index_jsl 接口，获取集思录可转债等权指数数据

1.5.90 fix: fix macro_china_bond_public interface

    1. 修复 macro_china_bond_public 接口

1.5.89 fix: fix stock_info_sh_name_code interface

    1. 修复 stock_info_sh_name_code 接口

1.5.88 fix: fix stock_board_concept_name_ths interface

    1. 修复 stock_board_concept_name_ths 接口，补充遗漏的概念板块

1.5.87 fix: fix stock_tfp_em interface

    1. 修复 stock_tfp_em 接口

1.5.86 fix: fix stock_us_fundamental interface

    1. 修复 stock_us_fundamental 接口的说明

1.5.85 fix: fix stock_zh_a_hist interface

    1. 修复 stock_zh_a_hist 接口，直接返回指定时间段之间的数据

1.5.84 fix: fix stock_three_report_em interface

    1. 修复 stock_balance_sheet_by_report_em 接口
    2. 修复 stock_balance_sheet_by_yearly_em 接口
    3. 修复 stock_profit_sheet_by_report_em 接口
    4. 修复 stock_profit_sheet_by_yearly_em 接口
    5. 修复 stock_profit_sheet_by_quarterly_em 接口
    6. 修复 stock_cash_flow_sheet_by_report_em 接口
    7. 修复 stock_cash_flow_sheet_by_yearly_em 接口

1.5.83 fix: fix energy_oil_hist, energy_oil_detail interface

    1. 修复 energy_oil_hist 接口，按时间排序输出且规范数据输出格式
    2. 修复 energy_oil_detail 接口，规范数据输出格式

1.5.82 add: add option_risk_indicator_sse interface

    1. 新增 option_risk_indicator_sse 接口，获取上海证券交易所-产品-股票期权-期权风险指标数据

1.5.81 fix: fix macro_china_gdp_yearly interface

    1. 修复 macro_china_gdp_yearly 接口，数据输出格式为 pandas.DataFrame

1.5.80 add: add stock_szse_sector_summary interface

    1. 新增 stock_szse_sector_summary 接口，获取深证证券交易所-总貌-股票行业成交数据

1.5.79 add: add stock_szse_area_summary interface

    1. 新增 stock_szse_area_summary 接口，获取深证证券交易所-总貌-地区交易排序数据

1.5.78 fix: fix stock_szse_summary interface

    1. 修复 stock_szse_summary 接口

1.5.77 fix: fix remove numpy dependency

    1. 移除 numpy 依赖

1.5.76 add: add news_report_time_baidu interface

    1. 新增 news_report_time_baidu 接口，获取财报发行时间

1.5.75 fix: fix stock_financial_analysis_indicator interface

    1. 修复 stock_financial_analysis_indicator 接口的日期字段

1.5.74 add: add news_trade_notify_suspend_baidu interface

    1. 新增 news_trade_notify_suspend_baidu 接口，获取 A 股及港股停复牌数据

1.5.73 fix: fix stock_notice_report interface

    1. 修复 stock_notice_report 接口，添加日期参数

1.5.72 add: add news_economic_baidu interface

    1. 新增 news_economic_baidu 接口，获取全球宏观事件数据

1.5.71 fix: fix import path problem

    1. 修复 covid 接口中的路径问题

1.5.70 fix: fix stock_zh_a_spot interface

    1. 修复 stock_zh_a_spot 中 pandas.DataFrame.append 警告

1.5.69 fix: fix setup.py

    1. 修复 setup.py 文件

1.5.68 fix: fix test function

    1. 修复 test_zipfile_func 函数

1.5.67 add: add test function

    1. 新增测试函数，用于测试数据文件的路径

1.5.66 fix: fix crypto_hist interface

    1. 修复 crypto_hist 接口，将部分数据存放到 data 文件夹读取，以提高访问稳定性及速度

1.5.65 fix: fix stock_repurchase_em interface

    1. 修复 stock_repurchase_em 接口，获取股票回购-股票回购数据

1.5.64 fix: fix stock_cash_flow_sheet_by_yearly_em interface

    1. 修复 stock_cash_flow_sheet_by_yearly_em 接口，获取现金流量表-按年度接口

1.5.63 fix: fix import path problem

    1. 修复 JS 文件及数据文件导入问题，方便在本地调试代码

1.5.62 add: add stock_cash_flow_sheet_by_quarterly_em interface

    1. 新增 stock_cash_flow_sheet_by_quarterly_em 接口，获取现金流量表-按单季度数据

1.5.61 add: add stock_cash_flow_sheet_by_report_em interface

    1. 新增 stock_cash_flow_sheet_by_report_em 接口，获取现金流量表-按报告期数据

1.5.60 fix: fix sw_index_second_spot interface

    1. 修复 sw_index_second_spot 接口，更新接口提交采纳数

1.5.59 add: add stock_profit_sheet_by_yearly_em interface

    1. 新增 stock_profit_sheet_by_yearly_em 接口，获取利润表-按年度数据

1.5.58 add: add stock_profit_sheet_by_quarterly_em interface

    1. 新增 stock_profit_sheet_by_quarterly_em 接口，获取利润表-按单季度数据

1.5.57 add: add stock_profit_sheet_by_report_em interface

    1. 新增 stock_profit_sheet_by_report_em 接口，获取利润表-报告期数据

1.5.56 add: add stock_balance_sheet_by_yearly_em interface

    1. 新增 stock_balance_sheet_by_yearly_em 接口，获取利润表-按年度数据

1.5.55 add: add stock_balance_sheet_by_report_em interface

    1. 新增 stock_balance_sheet_by_report_em 接口，获取资产负债表-按报告期数据

1.5.54 fix: fix stock_lrb_em interface

    1. 修复 stock_lrb_em 接口

1.5.53 fix: fix stock_zcfz_em interface

    1. 修复 stock_zcfz_em 接口，重命名该接口并规范数据输出格式
    2. 修复 stock_lrb_em 接口，重命名该接口并规范数据输出格式
    3. 修复 stock_xjll_em 接口，重命名该接口并规范数据输出格式

1.5.52 fix: fix stock_ggcg_em interface

    1. 修复 stock_ggcg_em 接口，重命名该接口、修改为东财的最新接口并规范数据输出

1.5.51 fix: fix stock_zh_a_tick_163 interface

    1. 修复 stock_zh_a_tick_163 接口，读取 Excel 文件

1.5.50 fix: fix covid_19_baidu interface

    1. 修复 covid_19_baidu 接口中的国内分省份详情和城市详情

1.5.49 add: add stock_inner_trade_xq interface

    1. 新增 stock_inner_trade_xq 接口，获取股票的内部交易数据

1.5.48 fix: fix futures_return_index_nh interface

    1. 修复 futures_return_index_nh 接口，重命名接口及规范数据输出格式
    2. 修复 futures_index_symbol_table_nh 接口，重名接口
    3. 修复 futures_price_index_nh 接口，重名接口

1.5.47 fix: fix macro_china_lpr interface

    1. 修复 macro_china_lpr 接口，规范数据的输出格式

1.5.46 fix: fix stock_yzxdr_em interface

    1. 修复 stock_yzxdr_em 接口，对接口进行重命名

1.5.45 add: add stock_hot_deal_xq interface

    1. 新增 stock_hot_deal_xq 接口，获取雪球-沪深股市-热度排行榜-分享交易排行榜数据

1.5.44 fix: fix futures_to_spot_czce interface

    1. 修复 futures_to_spot_czce 接口，直接读取 Excel 文件并规范输出的字段类型
    2. 修复 futures_delivery_czce 接口，直接读取 Excel 文件并规范输出的字段类型
    3. 修复 futures_delivery_match_czce 接口，直接读取 Excel 文件并规范输出的字段类型

1.5.43 fix: fix stock_zt_pool_em interface

    1. 修复 stock_zt_pool_em 接口，获取所有股票的数据

1.5.42 fix: fix stock_zt_pool_dtgc_em interface

    1. 修复 stock_zt_pool_dtgc_em 接口，获取所有股票的数据

1.5.41 fix: fix stock_margin_underlying_info_szse interface

    1. 修复 stock_margin_underlying_info_szse 接口，利用 pandas.concate 替换 pandas.DataFrame.append 方法

1.5.40 fix: fix js_news interface

    1. 修复 js_news 接口，规范输出数据的格式

1.5.39 add: add stock_comment_detail_scrd_desire_daily_em interface

    1. 新增 stock_comment_detail_scrd_desire_daily_em 接口，获取日度市场参与意愿数据数据

1.5.38 add: add stock_comment_detail_scrd_cost_em interface

    1. 新增 stock_comment_detail_scrd_cost_em 接口，获取市场成本数据

1.5.37 add: add stock_comment_detail_scrd_desire_em interface

    1. 新增 stock_comment_detail_scrd_desire_em 接口，获取市场参与意愿数据

1.5.36 add: add stock_comment_detail_scrd_focus_em interface

    1. 新增 stock_comment_detail_scrd_focus_em 接口，获取用户关注指数数据

1.5.35 add: add stock_comment_detail_zhpj_lspf_em interface

    1. 新增 stock_comment_detail_zhpj_lspf_em 接口，获取综合评价-历史评分数据

1.5.34 fix: fix stock_gpzy_industry_data_em interface

    1. 修复 stock_gpzy_industry_data_em 接口，并重命名为 stock_gpzy_industry_data_em

1.5.33 fix: fix fund_fh_em interface

    1. 修复 fund_fh_em, fund_cf_em 和 fund_fh_rank_em 接口

1.5.32 add: add stock_comment_detail_zlkp_jgcyd_em interface

    1. 新增 stock_comment_detail_zlkp_jgcyd_em 接口

1.5.31 fix: fix stock_individual_info_em interface

    1. 修复 stock_individual_info_em 接口

1.5.30 fix: fix hurun_rank interface

    1. 修复 hurun_rank 接口，新增多个排行榜及统一数据输出格式

1.5.29 fix: fix index_zh_a_hist_min_em interface

    1. 修复 index_zh_a_hist_min_em 接口，个别指数数据获取

1.5.28 fix: fix bond_zh_cov interface

    1. 修复 bond_zh_cov 接口

1.5.27 fix: fix stock_comment_em interface

    1. 修复 stock_comment_em 接口，补充字段跟网页数据源统一并新增`交易日`字段

1.5.26 fix: fix stock_comment_em interface

    1. 修复 stock_comment_em 接口，将接口重命名为 stock_comment_em，修改字段名称和字段类型

1.5.25 fix: fix stock_analyst_rank_em and stock_analyst_detail_em interface

    1. 修复 stock_analyst_rank_em 接口，将接口重命名为 stock_analyst_rank_em
    2. 修复 stock_analyst_detail_em 接口，将接口重命名为 stock_analyst_detail_em

1.5.24 fix: fix stock_profit_forecast interface

    1. 修复 stock_profit_forecast 接口，统一字段名称及类型

1.5.23 fix: fix stock_board_concept_name_em interface

    1. 修复 stock_board_concept_name_em 接口，增加字段的容错

1.5.22 fix: fix futures_correlation_nh interface

    1. 修复 futures_correlation_nh 接口，修改接口描述

1.5.21 add: add futures_variety_index_nh interface

    1. 新增 futures_variety_index_nh 接口，获取品种指数涨跌数据

1.5.20 add: add futures_board_index_nh interface

    1. 新增 futures_board_index_nh 接口，获取板块指数涨跌数据

1.5.19 add: add futures_correlation_nh interface

    1. 新增 futures_correlation_nh 接口，获取相关系数矩阵数据

1.5.18 fix: fix fund_open_fund_rank_em interface

    1. 修复 fund_open_fund_rank_em 接口，重命名 fund_em_open_fund_rank 为 fund_open_fund_rank_em

1.5.17 add: add macro_china_bsi_index interface

    1. 修复 macro_china_bsi_index 接口，获取超灵便型船运价指数数据

1.5.16 fix: fix stock_info_sh_delist interface

    1. 修复 stock_info_sh_delist 接口

1.5.15 fix: fix bond_cb_jsl interface

    1. 修复 bond_cb_jsl 接口

1.5.14 add: add macro_china_bdti_index interface

    1. 新增 macro_china_bdti_index 接口，获取原油运输指数数据

1.5.13 add: add macro_china_lpi_index interface

    1. 新增 macro_china_lpi_index 接口，获取物流景气指数数据

1.5.12 fix: fix stock_gpzy_pledge_ratio_detail_em interface

    1. 修复 stock_gpzy_pledge_ratio_detail_em 接口并重命名

1.5.11 add: add index_bloomberg_billionaires_hist interface

    1. 新增 index_bloomberg_billionaires_hist 接口，获取彭博亿万富豪历史数据

1.5.10 fix: fix stock_gpzy_pledge_ratio_em and stock_gpzy_profile_em interface

    1. 修复 stock_gpzy_profile_em 接口，对该接口重命名，并对返回的数据按时间升序排列
    2. 修复 stock_gpzy_pledge_ratio_em 接口，对该接口重名，并对返回的字段规范化

1.5.9 fix: fix air_quality_hist interface

    1. 修复 air_quality_hist 接口，主要修改接口的加密及解密逻辑

1.5.8 add: add macro_china_construction_price_index interface

    1. 新增 macro_china_construction_price_index 接口，获取建材价格指数数据

1.5.7 add: add macro_china_construction_index interface

    1. 新增 macro_china_construction_index 接口，获取建材指数数据

1.5.6 add: add macro_china_yw_electronic_index interface

    1. 新增 macro_china_yw_electronic_index 接口，获取义乌小商品指数-电子元器件数据

1.5.5 add: add macro_global_sox_index interface

    1. 新增 macro_global_sox_index 接口，获取费城半导体指数数据

1.5.4 add: add macro_china_commodity_price_index interface

    1. 新增 macro_china_commodity_price_index 接口，获取大宗商品价格数据

1.5.3 add: add macro_china_energy_index interface

    1. 新增 macro_china_energy_index 接口，获取能源指数数据

1.5.2 add: add macro_china_agricultural_index interface

    1. 新增 macro_china_agricultural_index 接口，获取农副指数数据

1.5.1 add: add macro_china_agricultural_product interface

    1. 新增 macro_china_agricultural_product 接口，获取农产品批发价格总指数数据

1.4.99 add: add macro_china_vegetable_basket interface

    1. 新增 macro_china_vegetable_basket 接口，获取菜篮子产品批发价格指数数据

1.4.98 fix: fix stock_board_industry_hist_em interface

    1. 修复 stock_board_industry_hist_em 接口，新增 start_date 和 end_date 参数

1.4.97 fix: fix bond_spot_deal interface

    1. 修复 bond_spot_deal 接口，对异常数据做处理

1.4.96 fix: fix stock_sse_deal_daily interface

    1. 修复 stock_sse_deal_daily 接口，最近接口调用新的地址

1.4.95 add: add bond_zh_cov_value_analysis interface

    1. 新增 bond_zh_cov_value_analysis 接口，获取可转债溢价率分析和可转债价值分析数据

1.4.94 add: add macro_china_mobile_number interface

    1. 新增 macro_china_mobile_number 接口，获取手机出货量数据

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

1.4.66 fix: fix stock_gpzy_profile_em interface

    1. 修复 stock_gpzy_profile_em 接口并设定返回数据的数据类型

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

1.7.55 add: add fx_quote_baidu interface

1.7.54 fix: fix stock_a_lg_indicator interface

1.7.53 add: add stock_buffett_index_lg interface

1.7.52 fix: fix stock_sse_summary interface

1.7.51 fix: fix stock_a_lg_indicator interface

1.7.50 add: add stock_hot_search_baidu interface

1.7.49 add: add futures_news_baidu interface

1.7.48 add: add stock_zh_vote_baidu interface

1.7.47 add: add stock_zh_valuation_baidu interface

1.7.46 fix: fix stock_hk_valuation_baidu interface

1.7.45 add: add stock_hk_valuation_baidu interface

1.7.44 add: add stock_allotment_cninfo interface

1.7.43 fix: fix stock_a_all_pb interface

1.7.42 add: add stock_sgt_reference_exchange_rate_szse interface

1.7.41 add: add stock_sgt_reference_exchange_rate_sse interface

1.7.40 add: add stock_sgt_settlement_exchange_rate_sse interface

1.7.39 add: add stock_sgt_settlement_exchange_rate_szse interface

1.7.38 add: add sw_index_second_info interface

1.7.37 add: add sw_index_first_info interface

1.7.36 fix: fix rename branch master to main

1.7.35 fix: fix stock_market_fund_flow interface

1.7.34 fix: fix bond_cb_jsl interface

1.7.33 fix: fix stock_zh_ah_daily interface

1.7.32 fix: fix stock_a_ttm_lyr interface

1.7.31 fix: fix stock_a_lg_indicator interface

1.7.30 fix: fix bond_cb_index_jsl interface

1.7.29 fix: fix stock_us_daily interface

1.7.28 fix: fix stock_info_sh_name_code interface

1.7.27 fix: fix stock_qsjy_em interface

1.7.26 add: add bond_new_composite_index_cbond interface

1.7.25 add: add news_trade_notify_dividend_baidu interface

1.7.24 fix: fix amac_manager_classify_info interface

1.7.23 fix: fix rename futures_pig_info and futures_pig_rank interface

1.7.22 add: add index_investing_global_area_index_name_url interface

1.7.21 fix: fix futures_hog_info interface

1.7.20 fix: fix crypto_js_spot interface

1.7.19 fix: fix index_value_name_funddb interface

1.7.18 fix: fix stock_lhb_jgmmtj_em interface

1.7.17 fix: fix bond_cb_jsl interface

1.7.16 fix: fix crypto_js_spot interface

1.7.15 fix: fix news_economic_baidu interface

1.7.14 fix: fix covid_19_risk_area interface

1.7.13 fix: fix stock_balance_sheet_by_yearly_em interface

1.7.12 fix: fix stock_repurchase_em interface

1.7.11 fix: fix bond_cash_summary_sse interface

1.7.10 fix: fix option_czce_daily interface

1.7.9 add: add index_market_representation_hist_sw interface

1.7.8 add: add index_style_index_hist_sw interface

1.7.7 add: add index_level_one_hist_sw interface

1.7.6 fix: fix covid_19_risk_area interface

1.7.5 fix: fix fund_fh_em interface

1.7.4 fix: fix stock_analyst_rank_em interface

1.7.3 fix: fix stock_profit_sheet_by_report_em interface

1.7.2 fix: fix futures_egg_price_yearly interface

1.7.1 fix: fix fund_etf_fund_info_em interface

1.6.99 fix: fix macro_china_fx_gold interface

1.6.98 fix: fix macro_china_real_estate interface

1.6.97 fix: fix macro_china_real_estate interface

1.6.96 fix: fix macro_china_bond_public interface

1.6.95 fix: fix energy_oil_detail interface

1.6.94 fix: fix macro_china_hk_market_info interface

1.6.93 fix: fix index_vix interface

1.6.92 fix: fix hurun_rank interface

1.6.91 fix: fix forbes_rank interface

1.6.90 fix: fix macro_china_cpi_yearly interface

1.6.89 fix: fix stock_board_concept_name_ths interface

1.6.88 fix: fix option_cffex_zz1000_spot_sina interface

1.6.87 fix: fix stock_ggcg_em interface

1.6.86 fix: fix stock_gpzy_distribute_statistics_bank_em interface

1.6.85 fix: fix option_finance_board interface

1.6.84 fix: fix stock_zt_pool_em interface

1.6.83 fix: fix option_dce_daily interface

1.6.82 fix: fix option_cffex_hs300_spot_sina interface

1.6.81 fix: fix currency_hist interface

1.6.80 fix: fix index_investing_global interface

1.6.79 fix: fix fund_rating_all interface

1.6.78 fix: fix stock_telegraph_cls interface

1.6.77 fix: fix stock_telegraph_cls interface

1.6.76 add: add pycryptodomex library

1.6.75 add: add option_cffex_zz1000_spot_sina interface

1.6.74 add: add option_cffex_zz1000_list_sina interface

1.6.73 fix: fix macro_china_rmb interface

1.6.72 add: add futures_news_shmet interface

1.6.71 fix: fix bond_zh_hs_cov_pre_min interface

1.6.70 add: add bond_zh_hs_cov_pre_min interface

1.6.69 add: add fund_info_index_em interface

1.6.68 fix: fix stock_zh_a_minute interface

1.6.67 fix: fix stock_zh_a_alerts_cls interface

1.6.66 fix: fix stock_balance_sheet_by_report_em interface

1.6.65 fix: fix bond_cb_redeem_jsl interface

1.6.64 fix: fix index_investing_global interface

1.6.63 fix: fix fund_portfolio_em and futures_roll_yield interface

1.6.62 fix: fix futures_zh_spot interface

1.6.61 fix: fix futures_shfe_warehouse_receipt interface

1.6.60 add: add stock_telegraph_cls interface

1.6.59 add: add stock_industry_change_cninfo interface

1.6.58 fix: fix stock_gdfx_holding_analyse_em interface

1.6.57 fix: fix stock_info_sh_name_code interface

1.6.56 fix: fix index_zh_a_hist interface

1.6.55 fix: fix stock_gdfx_free_holding_analyse_em interface

1.6.54 fix: fix stock_hsgt_hold_stock_em interface

1.6.53 fix: fix fx_spot_quote interface

1.6.52 fix: fix index_zh_a_hist interface

1.6.51 fix: fix stock_analyst_detail_em interface

1.6.50 add: add stock_industry_category_cninfo interface

1.6.49 fix: fix stock_zh_a_alerts_cls interface

1.6.48 fix: fix stock_report_disclosure interface

1.6.47 fix: fix stock_zh_a_minute interface

1.6.46 fix: fix fund_open_fund_info_em interface

1.6.45 fix: fix stock_zh_index_hist_csindex interface

1.6.44 fix: fix futures_inventory_em interface

1.6.43 fix: fix futures_inventory_99 interface

1.6.42 fix: fix stock_balance_sheet_by_yearly_em interface

1.6.41 add: add futures_inventory_99 interface

1.6.40 add: add stock_mda_ym interface

1.6.39 fix: fix futures_symbol_mark interface

1.6.38 add: add stock_zygc_ym interface

1.6.37 fix: remove futures_inventory_99 interface

1.6.36 fix: fix option_finance_board interface

1.6.35 fix: fix stock_zh_index_hist_csindex interface

1.6.34 fix: fix fx_spot_quote interface

1.6.33 fix: fix stock_report_fund_hold_detail interface

1.6.32 fix: fix get_czce_daily interface

1.6.31 fix: fix stock_gdfx_free_holding_detail_em interface

1.6.30 fix: fix stock_info_a_code_name interface

1.6.29 fix: fix stock_board_industry_name_em interface

1.6.28 add: add currency_boc_safe interface

1.6.27 fix: fix currency_boc_sina interface

1.6.26 fix: fix bond_cb_index_jsl interface

1.6.25 fix: fix bond_cb_index_jsl interface

1.6.24 fix: fix bond_cb_index_jsl interface

1.6.23 fix: fix bond_cb_index_jsl interface

1.6.22 add: add stock_kc_a_spot_em interface

1.6.21 fix: fix baidu_search_index interface

1.6.20 fix: fix stock_board_industry_name_em and code_id_map_em interface

1.6.19 fix: fix stock_comment_detail_zlkp_jgcyd_em interface

1.6.18 fix: fix stock_zh_a_spot_em interface

1.6.17 fix: fix stock_new_a_spot_em interface

1.6.16 fix: fix baidu_search_index interface

1.6.15 fix: fix bond_zh_cov_info interface

1.6.14 fix: fix stock_hsgt_board_rank_em interface

1.6.13 add: add stock_new_a_spot_em interface

1.6.12 add: add stock_bj_a_spot_em interface

1.6.11 add: add stock_sz_a_spot_em interface

1.6.10 add: add stock_sh_a_spot_em interface

1.6.9 fix: fix stock_zh_a_spot_em interface

1.6.8 fix: fix futures_zh_spot interface

1.6.7 add: add futures_zh_realtime interface

1.6.6 fix: fix fund_etf_hist_sina interface

1.6.5 fix: fix stock_board_cons_ths interface

1.6.4 fix: fix stock_info_a_code_name interface

1.6.3 fix: fix stock_info_a_code_name and stock_info_sh_delist interface

1.6.2 fix: fix macro_china_cpi interface

1.6.1 fix: fix stock_info_sh_name_code interface

1.5.99 fix: fix stock_zh_a_hist_163 interface

1.5.98 fix: fix news_cctv interface

1.5.97 fix: fix stock_zh_a_hist interface

1.5.96 fix: fix macro_bank_usa_interest_rate interface

1.5.95 fix: fix stock_zh_a_hist_163 interface

1.5.94 add: add bond_cb_redeem_jsl interface

1.5.93 fix: fix stock_zh_a_hist interface

1.5.92 fix: fix rate_interbank interface

1.5.91 add: add bond_cb_index_jsl interface

1.5.90 fix: fix macro_china_bond_public interface

1.5.89 fix: fix stock_info_sh_name_code interface

1.5.88 fix: fix stock_board_concept_name_ths interface

1.5.87 fix: fix stock_tfp_em interface

1.5.86 fix: fix stock_us_fundamental interface

1.5.85 fix: fix stock_zh_a_hist interface

1.5.84 fix: fix stock_three_report_em interface

1.5.83 fix: fix energy_oil_hist, energy_oil_detail interface

1.5.82 add: add option_risk_indicator_sse interface

1.5.81 fix: fix macro_china_gdp_yearly interface

1.5.80 add: add stock_szse_sector_summary interface

1.5.79 add: add stock_szse_area_summary interface

1.5.78 fix: fix stock_szse_summary interface

1.5.77 fix: fix remove numpy dependency

1.5.76 add: add news_report_time_baidu interface

1.5.75 fix: fix stock_financial_analysis_indicator interface

1.5.74 add: add news_trade_notify_suspend_baidu interface

1.5.73 fix: fix stock_notice_report interface

1.5.72 add: add news_economic_baidu interface

1.5.71 fix: fix import path problem

1.5.70 fix: fix stock_zh_a_spot interface

1.5.69 fix: fix setup.py

1.5.68 fix: fix test function

1.5.67 add: add test function

1.5.66 fix: fix crypto_hist interface

1.5.65 fix: fix stock_repurchase_em interface

1.5.64 fix: fix stock_cash_flow_sheet_by_yearly_em interface

1.5.63 fix: fix import path problem

1.5.62 add: add stock_cash_flow_sheet_by_quarterly_em interface

1.5.61 add: add stock_cash_flow_sheet_by_report_em interface

1.5.60 fix: fix sw_index_second_spot interface

1.5.59 add: add stock_profit_sheet_by_yearly_em interface

1.5.58 add: add stock_profit_sheet_by_quarterly_em interface

1.5.57 add: add stock_profit_sheet_by_report_em interface

1.5.56 add: add stock_balance_sheet_by_yearly_em interface

1.5.55 add: add stock_balance_sheet_by_report_em interface

1.5.54 fix: fix stock_lrb_em interface

1.5.53 fix: fix stock_zcfz_em interface

1.5.52 fix: fix stock_ggcg_em interface

1.5.51 fix: fix stock_zh_a_tick_163 interface

1.5.50 fix: fix covid_19_baidu interface

1.5.49 add: add stock_inner_trade_xq interface

1.5.48 fix: fix futures_return_index_nh interface

1.5.47 fix: fix macro_china_lpr interface

1.5.46 fix: fix stock_yzxdr_em interface

1.5.45 add: add stock_hot_deal_xq interface

1.5.44 fix: fix futures_to_spot_czce interface

1.5.43 fix: fix stock_zt_pool_em interface

1.5.42 fix: fix stock_zt_pool_dtgc_em interface

1.5.41 fix: fix stock_margin_underlying_info_szse interface

1.5.40 fix: fix js_news interface

1.5.39 add: add stock_comment_detail_scrd_desire_daily_em interface

1.5.38 add: add stock_comment_detail_scrd_cost_em interface

1.5.37 add: add stock_comment_detail_scrd_desire_em interface

1.5.36 add: add stock_comment_detail_scrd_focus_em interface

1.5.35 add: add stock_comment_detail_zhpj_lspf_em interface

1.5.34 fix: fix stock_gpzy_industry_data_em interface

1.5.33 fix: fix fund_fh_em interface

1.5.32 add: add stock_comment_detail_zlkp_jgcyd_em interface

1.5.31 fix: fix stock_individual_info_em interface

1.5.30 fix: fix hurun_rank interface

1.5.29 fix: fix index_zh_a_hist_min_em interface

1.5.28 fix: fix bond_zh_cov interface

1.5.27 fix: fix stock_comment_em interface

1.5.26 fix: fix stock_comment_em interface

1.5.25 fix: fix stock_analyst_rank_em and stock_analyst_detail_em interface

1.5.24 fix: fix stock_profit_forecast interface

1.5.23 fix: fix stock_board_concept_name_em interface

1.5.22 fix: fix futures_correlation_nh interface

1.5.21 add: add futures_variety_index_nh interface

1.5.20 add: add futures_board_index_nh interface

1.5.19 add: add futures_correlation_nh interface

1.5.18 fix: fix fund_open_fund_rank_em interface

1.5.17 add: add macro_china_bsi_index interface

1.5.16 fix: fix stock_info_sh_delist interface

1.5.15 fix: fix bond_cb_jsl interface

1.5.14 add: add macro_china_bdti_index interface

1.5.13 add: add macro_china_lpi_index interface

1.5.12 fix: fix stock_gpzy_pledge_ratio_detail_em interface

1.5.11 add: add index_bloomberg_billionaires_hist interface

1.5.10 fix: fix stock_gpzy_pledge_ratio_em and stock_gpzy_profile_em interface

1.5.9 fix: fix air_quality_hist interface

1.5.8 add: add macro_china_construction_price_index interface

1.5.7 add: add macro_china_construction_index interface

1.5.6 add: add macro_china_yw_electronic_index interface

1.5.5 add: add macro_global_sox_index interface

1.5.4 add: add macro_china_commodity_price_index interface

1.5.3 add: add macro_china_energy_index interface

1.5.2 add: add macro_china_agricultural_index interface

1.5.1 add: add macro_china_agricultural_product interface

1.4.99 add: add macro_china_vegetable_basket interface

1.4.98 fix: fix stock_board_industry_hist_em interface

1.4.97 fix: fix bond_spot_deal interface

1.4.96 fix: fix stock_sse_deal_daily interface

1.4.95 add: add bond_zh_cov_value_analysis interface

1.4.94 add: add macro_china_mobile_number interface

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

1.4.66 fix: fix stock_gpzy_profile_em interface

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
