# [AKShare](https://github.com/akfamily/akshare) 版本更新

## 接口更名一览表

| AKShare 版本 | 旧接口名称                                       | 新接口名称                                       | 修改日期     |
|------------|---------------------------------------------|---------------------------------------------|----------|
| 1.13.19    | car_gasgoo_sale_rank                        | car_sale_rank_gasgoo                        | 20240403 |
| 1.13.19    | car_energy_sale_cpca                        | car_market_fuel_cpca                        | 20240403 |
| 1.13.15    | car_market_cpca                             | car_market_total_cpca                       | 20240331 |
| 1.12.95    | futures_hog_rank                            | futures_hog_cost                            | 20240318 |
| 1.12.95    | futures_hog_info                            | futures_hog_core                            | 20240318 |
| 1.12.93    | get_bond_bank                               | bond_debt_nafmii                            | 20240316 |
| 1.12.91    | stock_telegraph_cls                         | stock_info_global_cls                       | 20240313 |
| 1.12.11    | stock_zh_index_spot                         | stock_zh_index_spot_sina                    | 20240104 |
| 1.11.64    | futures_sgx_daily                           | futures_settlement_price_sgx                | 20231108 |
| 1.11.61    | fund_manager                                | fund_manager_em                             | 20231105 |
| 1.11.41    | weibo_index                                 | index_weibo_sina                            | 20231020 |
| 1.11.39    | option_300etf_min_qvix                      | index_option_300etf_min_qvix                | 20231019 |
| 1.11.39    | option_300etf_qvix                          | index_option_300etf_qvix                    | 20231019 |
| 1.11.39    | option_50etf_min_qvix                       | index_option_50etf_min_qvix                 | 20231019 |
| 1.11.39    | option_50etf_qvix                           | index_option_50etf_qvix                     | 20231019 |
| 1.10.50    | car_cpca_energy_sale                        | car_energy_sale_cpca                        | 20230710 |
| 1.10.36    | stock_em_sy_hy_list                         | stock_sy_hy_em                              | 20230624 |
| 1.10.36    | stock_em_sy_list                            | stock_sy_em                                 | 20230624 |
| 1.10.36    | stock_em_sy_jz_list                         | stock_sy_jz_em                              | 20230624 |
| 1.10.36    | stock_em_sy_yq_list                         | stock_sy_yq_em                              | 20230624 |
| 1.10.36    | stock_em_sy_profile                         | stock_sy_profile_em                         | 20230624 |
| 1.10.8     | futures_nh_volatility_index                 | futures_volatility_index_nh                 | 20230606 |
| 1.9.41     | stock_a_lg_indicator                        | stock_a_indicator_lg                        | 20230406 |
| 1.9.37     | stock_hk_eniu_indicator                     | stock_hk_indicator_eniu                     | 20230404 |
| 1.9.27     | fund_em_hk_rank                             | fund_hk_rank_em                             | 20230330 |
| 1.9.27     | fund_em_lcx_rank                            | fund_lcx_rank_em                            | 20230330 |
| 1.9.27     | fund_em_money_rank                          | fund_money_rank_em                          | 20230330 |
| 1.9.27     | fund_em_exchange_rank                       | fund_exchange_rank_em                       | 20230330 |
| 1.9.7      | stock_profit_forecast                       | stock_profit_forecast_em                    | 20230330 |
| 1.8.38     | macro_cons_silver_amount                    | macro_cons_silver                           | 20221227 |
| 1.8.38     | macro_cons_silver_change                    | macro_cons_silver                           | 20221227 |
| 1.8.38     | macro_cons_silver_volume                    | macro_cons_silver                           | 20221227 |
| 1.8.38     | macro_cons_gold_amount                      | macro_cons_gold                             | 20221227 |
| 1.8.38     | macro_cons_gold_change                      | macro_cons_gold                             | 20221227 |
| 1.8.38     | macro_cons_gold_volume                      | macro_cons_gold                             | 20221227 |
| 1.8.23     | stock_restricted_shares                     | stock_restricted_release_queue_sina         | 20221122 |
| 1.8.3      | stock_em_qbzf                               | stock_qbzf_em                               | 20221122 |
| 1.8.3      | stock_em_pg                                 | stock_pg_em                                 | 20221122 |
| 1.7.99     | stock_sina_lhb_jgmx                         | stock_lhb_jgmx_sina                         | 20221119 |
| 1.7.99     | stock_sina_lhb_jgzz                         | stock_lhb_jgzz_sina                         | 20221119 |
| 1.7.99     | stock_sina_lhb_yytj                         | stock_lhb_yytj_sina                         | 20221119 |
| 1.7.99     | stock_sina_lhb_ggtj                         | stock_lhb_ggtj_sina                         | 20221119 |
| 1.7.99     | stock_sina_lhb_detail_daily                 | stock_lhb_detail_daily_sina                 | 20221119 |
| 1.7.82     | index_analysis_sw                           | index_analysis_daily_sw                     | 20220921 |
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

## 更新说明详情

1.13.39 add: add index_news_sentiment_scope interface

    1. 新增 index_news_sentiment_scope 接口
    2. 修复 index_yw 接口

1.13.38 fix: fix stock_market_activity_legu interface

    1. 修复 stock_market_activity_legu 接口
    2. 修复 get_shfe_daily 接口
    3. 修复 get_czce_daily 接口

1.13.37 fix: fix stock_hk_index_daily_sina interface

    1. 修复 stock_hk_index_daily_sina 接口
    2. 新增 stock_info_broker_sina 接口

1.13.36 fix: fix stock_hsgt_hist_em interface

    1. 修复 stock_hsgt_hist_em 接口

1.13.35 fix: fix stock_margin_szse interface

    1. 修复 stock_margin_szse 接口

1.13.34 fix: fix bank_fjcf_table_detail interface

    1. 修复 bank_fjcf_table_detail 接口

1.13.33 fix: fix index_realtime_fund_sw interface

    1. 修复 index_realtime_fund_sw 接口
    2. 修复 stock_zt_pool_em 接口

1.13.32 fix: fix futures_contract_info_czce interface

    1. 修复 futures_contract_info_czce 接口
    2. 修复 stock_board_concept_cons_em 接口
    3. 修复 futures_comm_info 接口
    4. 修复 stock_us_pink_spot_em 接口

1.13.31 fix: fix stock_individual_spot_xq interface

    1. 修复 stock_individual_spot_xq 接口

1.13.30 fix: fix futures_contract_info_shfe interface

    1. 修复 futures_contract_info_shfe 接口

1.13.29 fix: fix stock_esg_msci_sina interface

    1. 修复 stock_esg_msci_sina 接口

1.13.28 fix: fix stock_restricted_release_queue_em interface

    1. 修复 stock_restricted_release_queue_em 接口
    2. 修复 stock_esg_msci_sina 接口

1.13.27 add: add stock_esg_msci_sina interface

    1. 新增 stock_esg_msci_sina 接口
    2. 新增 stock_esg_rft_sina 接口
    3. 新增 stock_esg_zd_sina 接口

1.13.26 fix: fix option_sse_minute_sina interface

    1. 修复 option_sse_minute_sina 接口

1.13.25 fix: fix futures_zh_daily_sina interface

    1. 修复 futures_zh_daily_sina 接口

1.13.24 fix: fix futures_spot_sys interface

    1. 修复 futures_spot_sys 接口

1.13.23 add: add macro_usa_cme_merchant_goods_holding interface

    1. 新增 macro_usa_cme_merchant_goods_holding 接口

1.13.22 fix: fix amac_manager_cancelled_info interface

    1. 修复 amac_manager_cancelled_info 接口
    2. 修复 macro_china_pmi_yearly 接口
    3. 修复 macro_euro_lme_stock 接口
    4. 修复 macro_usa_phs 接口
    5. 修复 macro_china_construction_index 接口

1.13.21 fix: fix stock_yjkb_em interface

    1. 修复 stock_yjkb_em 接口
    2. 修复 stock_pg_em 接口
    3. 修复 stock_comment_em 接口
    4. 修复 macro_usa_api_crude_stock 接口

1.13.20 fix: fix stock_zh_a_disclosure_report_cninfo interface

    1. 修复 stock_zh_a_disclosure_report_cninfo 接口

1.13.19 add: add car_market_country_cpca interface

    1. 新增 car_market_country_cpca 接口
    2. 新增 car_market_segment_cpca 接口

1.13.18 fix: fix macro_china_pmi_yearly interface

    1. 修复 crypto_js_spot 接口
    2. 修复 macro_cons_gold 接口
    3. 修复 macro_china_hk_cpi 接口
    4. 修复 macro_china_pmi_yearly 接口
    5. 新增 index_realtime_fund_sw 接口
    6. 新增 index_hist_fund_sw 接口
    7. 修复 macro_euro_lme_stock 接口
    8. 修复 macro_usa_cftc_merchant_goods_holding 接口
    9. 修复 macro_usa_ism_pmi 接口

1.13.17 fix: fix stock_zcfz_em interface

    1. 修复 stock_zcfz_em 接口
    2. 新增 fund_individual_detail_hold_xq 接口
    3. 修复 futures_dce_warehouse_receipt 接口

1.13.16 add: add car_market_cate_cpca interface

    1. 新增 car_market_cate_cpca 接口
    2. 修复 car_market_man_rank_cpca 接口

1.13.15 add: add car_market_man_rank_cpca interface

    1. 新增 car_market_man_rank_cpca 接口
    2. 修复 car_market_total_cpca 接口

1.13.14 fix: fix futures_fees_info interface

    1. 修复 futures_fees_info 接口

1.13.13 fix: fix car_market_cpca interface

    1. 修复 car_market_cpca 接口

1.13.12 fix: fix stock_zyjs_ths interface

    1. 修复 stock_zyjs_ths 接口

1.13.11 fix: fix option_minute_em interface

    1. 修复 option_minute_em 接口
    2. 修复 stock_hk_index_daily_em 接口

1.13.10 fix: fix news_trade_notify_dividend_baidu interface

    1. 修复 news_trade_notify_dividend_baidu 接口
    2. 修复 fund_etf_hist_em 接口

1.13.9 chore: remove pyarrow deps

    1. 移除 pyarrow 依赖

1.13.8 fix: fix fund_etf_hist_em interface

    1. 修复 fund_etf_hist_em 接口

1.13.7 add: add futures_fees_info interface

    1. 新增 futures_fees_info 接口

1.13.6 fix: fix stock_board_concept_name_ths interface

    1. 修复 stock_board_concept_name_ths 接口
    2. 修复 tool_trade_date_hist_sina 接口

1.13.5 fix: fix stock_main_fund_flow interface

    1. 修复 stock_main_fund_flow 接口

1.13.4 fix: fix stock_individual_spot_xq interface

    1. 修复 stock_individual_spot_xq 接口

1.13.3 fix: fix stock_main_fund_flow interface

    1. 修复 stock_main_fund_flow 接口

1.13.2 add: add stock_main_fund_flow interface

    1. 新增 stock_main_fund_flow 接口
    2. 修复 stock_intraday_sina 接口

1.13.1 fix: fix futures_spot_stock interface

    1. 修复 futures_spot_stock 接口

1.12.99 fix: fix index_hog_spot_price interface

    1. 修复 index_hog_spot_price 接口

1.12.98 fix: fix bond_zh_cov interface

    1. 修复 bond_zh_cov 接口

1.12.97 fix: fix stock_zh_a_hist_min_em interface

    1. 修复 stock_zh_a_hist_min_em 接口
    2. 修复 fund_etf_hist_min_em 接口
    3. 修复 fund_lof_hist_min_em 接口

1.12.96 fix: fix stock_bid_ask_em interface

    1. 修复 stock_bid_ask_em 接口
    2. 修复 stock_us_spot_em 接口

1.12.95 add: add futures_hog_core interface

    1. 新增 futures_hog_core 接口
    2. 新增 futures_hog_cost 接口
    3. 新增 futures_hog_supply 接口
    4. 移除 futures_hog_info 接口
    5. 新增 futures_hog_rank 接口

1.12.94 fix: fix stock_hk_index_daily_em interface

    1. 修复 stock_hk_index_daily_em 接口
    2. 修复 index_us_stock_sina 接口

1.12.93 fix: fix bond_debt_nafmii interface

    1. 修复 bond_debt_nafmii 接口

1.12.92 fix: fix fund_etf_hist_min_em interface

    1. 修复 fund_etf_hist_min_em 接口

1.12.91 add: add stock_info_global_em interface

    1. 新增 stock_info_global_em 接口
    1. 新增 stock_info_cjzc_em 接口
    1. 新增 stock_info_global_sina 接口
    1. 新增 stock_info_global_futu 接口
    1. 新增 stock_info_global_ths 接口
    1. 新增 stock_info_global_cls 接口
    1. 修复 fund_etf_spot_em 接口

1.12.90 fix: fix fund_etf_spot_em interface

    1. 修复 fund_etf_spot_em 接口

1.12.89 fix: fix bond_china_yield interface

    1. 修复 bond_china_yield 接口

1.12.88 fix: fix fund_etf_spot_em interface

    1. 修复 fund_etf_spot_em 接口

1.12.87 fix: fix fortune_rank interface

    1. 修复 fortune_rank 接口

1.12.86 fix: fix fund_etf_spot_em interface

    1. 修复 fund_etf_spot_em 接口

1.12.85 fix: fix stock_sector_fund_flow_summary interface

    1. 修复 stock_sector_fund_flow_summary 接口
    2. 修复 futures_foreign_commodity_realtime 接口

1.12.84 fix: fix stock_market_fund_flow interface

    1. 修复 stock_market_fund_flow 接口

1.12.83 fix: fix stock_sector_fund_flow_rank interface

    1. 修复 stock_sector_fund_flow_rank 接口
    2. 修复 stock_individual_spot_xq 接口

1.12.82 fix: fix stock_tfp_em interface

    1. 修复 stock_tfp_em 接口
    2. 修复 news_trade_notify_suspend_baidu 接口

1.12.81 fix: fix macro_china_bond_public interface

    1. 修复 macro_china_bond_public 接口

1.12.80 fix: fix get_czce_daily interface

    1. 修复 get_czce_daily 接口
    2. 修复 get_czce_rank_table 接口

1.12.79 fix: fix futures_main_sina interface

    1. 修复 futures_main_sina 接口

1.12.78 fix: fix stock_info_sh_delist interface

    1. 修复 stock_info_sh_delist 接口
    2. 修复 stock_info_sz_name_code 接口
    3. 修复 stock_info_sz_change_name 接口
    4. 修复 stock_info_sz_delist 接口

1.12.77 fix: fix futures_contract_info_shfe interface

    1. 修复 futures_contract_info_shfe 接口
    2. 修复 fund_open_fund_rank_em 接口

1.12.76 fix: fix bond_zh_hs_spot interface

    1. 修复 bond_zh_hs_spot 接口

1.12.75 add: add futures_contract_info_ine interface

    1. 新增 futures_contract_info_ine 接口

1.12.74 add: add futures_contract_info_czce interface

    1. 新增 futures_contract_info_shfe 接口
    2. 新增 futures_contract_info_dce 接口
    3. 新增 futures_contract_info_czce 接口
    4. 新增 futures_contract_info_gfex 接口
    5. 新增 futures_contract_info_cffex 接口

1.12.73 fix: fix stock_individual_spot_xq interface

    1. 修复 stock_individual_spot_xq 接口
    2. 新增 futures_contract_info_dce 接口

1.12.72 fix: fix stock_hot_rank_wc interface

    1. 修复 stock_hot_rank_wc 接口
    2. 新增 futures_contract_info_shfe 接口

1.12.71 fix: fix stock_zh_ah_spot interface

    1. 修复 stock_zh_ah_spot 接口

1.12.70 fix: fix stock_lhb_detail_daily_sina interface

    1. 修复 stock_lhb_detail_daily_sina 接口
    2. 修复 stock_lhb_ggtj_sina 接口
    3. 修复 stock_lhb_yytj_sina 接口

1.12.69 fix: fix futures_hold_pos_sina interface

    1. 修复 futures_hold_pos_sina 接口
    2. 修复 index_hist_sw 接口

1.12.68 fix: fix option_finance_board interface

    1. 修复 option_finance_board 接口
    2. 修复 futures_spot_sys 接口
    3. 新增 futures_stock_shfe_js 接口
    4. 修复 futures_hold_pos_sina 接口

1.12.67 fix: fix index_hist_sw interface

    1. 修复 index_hist_sw 接口

1.12.66 fix: fix stock_board_industry_hist_em interface

    1. 修复 stock_board_industry_hist_em 接口

1.12.65 fix: fix futures_foreign_commodity_realtime interface

    1. 修复 futures_foreign_commodity_realtime 接口

1.12.64 fix: fix stock_board_industry_index_ths interface

    1. 修复 stock_board_industry_index_ths 接口
    2. 修复 akqmt 导入

1.12.63 add: add akqmt interface

    1. 新增 akqmt 接口

1.12.62 fix: fix stock_fund_flow_individual interface

    1. 修复 stock_fund_flow_individual 接口
    2. 修复 stock_institute_hold 接口

1.12.61 fix: fix stock_bid_ask_em interface

    1. 修复 stock_bid_ask_em 接口

1.12.60 fix: fix movie_boxoffice_daily interface

    1. 修复 movie_boxoffice_daily 接口
    2. 修复 movie_boxoffice_weekly 接口
    3. 修复 movie_boxoffice_monthly 接口
    4. 修复 movie_boxoffice_yearly 接口
    5. 修复 movie_boxoffice_yearly_first_week 接口
    6. 修复 movie_boxoffice_cinema_daily 接口
    7. 修复 movie_boxoffice_cinema_weekly 接口

1.12.59 fix: fix movie_boxoffice_realtime interface

    1. 修复 movie_boxoffice_realtime 接口
    2. 修复 bank_fjcf_table_detail 接口

1.12.58 fix: fix stock_ipo_summary_cninfo interface

    1. 修复 stock_ipo_summary_cninfo 接口

1.12.57 fix: fix bank_fjcf_table_detail interface

    1. 修复 bank_fjcf_table_detail 接口

1.12.56 fix: fix stock_a_indicator_lg interface

    1. 修复 stock_a_indicator_lg 接口

1.12.55 fix: fix stock_us_hist interface

    1. 修复 stock_us_hist 接口
    2. 修复 stock_mda_ym 接口

1.12.54 fix: fix stock_gpzy_pledge_ratio_detail_em interface

    1. 修复 stock_gpzy_pledge_ratio_detail_em 接口
    2. 修复 stock_individual_spot_xq 接口

1.12.53 fix: fix stock_rank_xzjp_ths interface

    1. 修复 stock_rank_xzjp_ths 接口

1.12.52 fix: fix stock_rank_cxg_ths interface

    1. 修复 stock_rank_cxg_ths 接口

1.12.51 add: add stock_hsgt_fund_min_em interface

    1. 新增 stock_hsgt_fund_min_em 接口

1.12.50 fix: fix bond_china_close_return interface

    1. 修复 bond_china_close_return 接口
    2. 修复 stock_dxsyl_em 接口

1.12.49 fix: fix stock_dxsyl_em interface

    1. 修复 stock_dxsyl_em 接口
    2. 修复 option_minute_em 接口

1.12.48 fix: fix option_minute_em interface

    1. 修复 option_minute_em 接口
    2. 修复 option_current_em 接口

1.12.47 fix: fix stock_zh_ah_daily interface

    1. 修复 stock_zh_ah_daily 接口
    2. 修复 get_receipt 接口

1.12.46 fix: fix futures_contract_detail interface

    1. 修复 futures_contract_detail 接口

1.12.45 fix: fix stock_individual_spot_xq interface

    1. 修复 stock_individual_spot_xq 接口
    2. 新增 data_tips 文档页面

1.12.44 fix: fix stock_zh_ah_daily interface

    1. 修复 stock_zh_ah_daily 接口

1.12.43 fix: fix macro_china_market_margin_sh interface

    1. 修复 macro_china_market_margin_sh 接口

1.12.42 fix: fix stock_news_em interface

    1. 修复 stock_news_em 接口
    2. 修复 fund_portfolio_hold_em 接口

1.12.41 fix: fix sw_index_third_cons interface

    1. 修复 sw_index_third_cons 接口
    2. 修复 sunrise_daily 接口

1.12.40 fix: fix futures_to_spot_dce interface

    1. 修复 futures_to_spot_dce 接口

1.12.39 fix: fix futures_gfex_warehouse_receipt interface

    1. 修复 futures_gfex_warehouse_receipt 接口
    2. 修复 futures_zh_spot 接口

1.12.38 fix: fix futures_to_spot_dce interface

    1. 修复 futures_to_spot_dce 接口
    2. 修复 futures_to_spot_shfe 接口

1.12.37 fix: fix futures_delivery_shfe interface

    1. 修复 futures_delivery_shfe 接口
    2. 修复 futures_delivery_match_czce 接口
    3. 修复 futures_delivery_dce 接口

1.12.36 fix: fix bond_china_close_return interface

    1. 修复 bond_china_close_return 接口
    2. 新增 futures_gfex_warehouse_receipt 接口

1.12.35 fix: fix article_epu_index interface

    1. 修复 article_epu_index 接口

1.12.34 fix: fix repo_rate_hist interface

    1. 修复 repo_rate_hist 接口
    2. 修复 repo_rate_query 接口
    3. 修复 article_ff_crr 接口

1.12.33 fix: fix futures_global_em interface

    1. 修复 futures_global_em 接口

1.12.32 fix: fix energy_oil_hist interface

    1. 修复 energy_oil_hist 接口
    2. 修复 futures_foreign_hist 接口
    3. 修复 stock_hot_follow_xq 接口

1.12.31 add: add futures_global_em interface

    1. 新增 futures_global_em 接口
    2. 修复 futures_settlement_price_sgx 接口

1.12.30 fix: fix futures_settlement_price_sgx interface

    1. 修复 futures_settlement_price_sgx 接口

1.12.29 add: add stock_individual_spot_xq interface

    1. 新增 stock_individual_spot_xq 接口

1.12.28 fix: fix futures_foreign_commodity_realtime interface

    1. 修复 futures_foreign_commodity_realtime 接口

1.12.27 fix: fix stock_hk_fhpx_detail_ths interface

    1. 修复 stock_hk_fhpx_detail_ths 接口
    2. 修复 air_quality_hist 接口

1.12.26 fix: fix index_stock_info interface

    1. 修复 index_stock_info 接口

1.12.25 fix: fix fund_individual_basic_info_xq interface

    1. 修复 fund_individual_basic_info_xq 接口

1.12.24 fix: fix stock_hk_index_spot_em interface

    1. 修复 stock_hk_index_spot_em 接口
    2. 修复 stock_hk_index_daily_em 接口
    3. 修复 index_hist_cni 接口

1.12.23 fix: fix fund_etf_hist_min_em interface

    1. 修复 fund_etf_hist_min_em 接口

1.12.22 fix: fix stock_hsgt_board_rank_em interface

    1. 修复 stock_hsgt_board_rank_em 接口

1.12.21 fix: fix stock_hsgt_hold_stock_em interface

    1. 修复 stock_hsgt_hold_stock_em 接口
    2. 修复 stock_cyq_em 接口
    3. 修复 stock_industry_pe_ratio_cninfo 接口
    4. 移除 stock_average_position_legu 接口
    5. 修复 stock_hsgt_institution_statistics_em 接口
    6. 移除 index_weibo_sina 接口
    7. 移除 index_baidu 接口
    8. 移除 index_google 接口
    9. 修复 macro_china_bond_public 接口
    10. 移除 index_investing_global_from_url 接口

1.12.20 fix: fix futures_inventory_99 interface

    1. 修复 futures_inventory_99 接口

1.12.19 fix: fix stock_hk_profit_forecast_et interface

    1. 修复 stock_hk_profit_forecast_et 接口

1.12.18 fix: fix stock_board_industry_index_ths interface

    1. 修复 stock_board_industry_index_ths 接口

1.12.17 fix: fix option_current_em interface

    1. 修复 option_current_em 接口

1.12.16 fix: fix stock_hot_follow_xq interface

    1. 修复 stock_hot_follow_xq 接口
    2. 修复 stock_hot_tweet_xq 接口
    3. 修复 stock_hot_deal_xq 接口

1.12.15 fix: fix stock_hk_profit_forecast_et interface

    1. 修复 stock_hk_profit_forecast_et 接口

1.12.14 add: add stock_hk_profit_forecast_et interface

    1. 新增 stock_hk_profit_forecast_et 接口

1.12.13 fix: fix index_stock_cons_csindex interface

    1. 修复 index_stock_cons_csindex 接口

1.12.12 fix: fix stock_zh_index_daily interface

    1. 修复 stock_zh_index_daily 接口

1.12.11 add: add stock_zh_index_spot_em interface

    1. 新增 stock_zh_index_spot_em 接口
    2. 重命名 stock_zh_index_spot 为 stock_zh_index_spot_sina

1.12.10 fix: fix stock_add_stock interface

    1. 修复 stock_add_stock 接口

1.12.9 add: add fund_individual_basic_info_xq interface

    1. 新增 fund_individual_basic_info_xq 接口
    2. 新增 fund_individual_achievement_xq 接口
    3. 新增 fund_individual_analysis_xq 接口
    4. 新增 fund_individual_profit_probability_xq 接口
    5. 新增 fund_individual_detail_info_xq 接口
    6. 新增 get_receipt 接口
    7. 新增 reits_realtime_em 接口

1.12.8 fix: fix fund_open_fund_info_em interface

    1. 修复 fund_open_fund_info_em 接口

1.12.7 fix: fix option_gfex_daily interface

    1. 修复 option_gfex_daily 接口
    2. 更新 calendar.json 文件

1.12.6 fix: fix fund_open_fund_info_em interface

    1. 修复 fund_open_fund_info_em 接口

1.12.5 fix: fix stock_zh_a_gdhs interface

    1. 修复 stock_zh_a_gdhs 接口

1.12.4 fix: fix tool_trade_date_hist_sina interface

    1. 修复 tool_trade_date_hist_sina 接口

1.12.3 fix: fix stock_gdfx_free_holding_teamwork_em interface

    1. 修复 stock_gdfx_free_holding_teamwork_em 接口

1.12.2 fix: fix hurun_rank interface

    1. 修复 hurun_rank 接口

1.12.1 fix: fix futures_comm_info interface

    1. 修复 futures_comm_info 接口

1.11.99 fix: fix stock_zh_index_spot interface

    1. 修复 stock_zh_index_spot 接口

1.11.98 fix: fix stock_zh_a_disclosure_report_cninfo interface

    1. 修复 stock_zh_a_disclosure_report_cninfo 接口

1.11.97 add: add stock_zh_a_disclosure_report_cninfo interface

    1. 新增 stock_zh_a_disclosure_report_cninfo 接口
    2. 修复 stock_gdfx_free_holding_analyse_em 接口
    3. 修复 stock_gdfx_holding_analyse_em 接口

1.11.96 fix: fix fund_rating_all interface

    1. 修复 fund_rating_all 接口

1.11.95 fix: fix fund_etf_hist_min_em interface

    1. 修复 fund_etf_hist_min_em 接口

1.11.94 fix: fix index_zh_a_hist_min_em interface

    1. 修复 index_zh_a_hist_min_em 接口
    2. 修复 index_zh_a_hist 接口

1.11.93 fix: fix stock_zh_a_hist_pre_min_em interface

    1. 修复 stock_zh_a_hist_pre_min_em 接口
    2. 修复 stock_intraday_sina 接口

1.11.92 fix: fix get_gfex_receipt interface

    1. 修复 get_gfex_receipt 接口

1.11.91 fix: remove stock_us_fundamental interface

    1. 移除 stock_us_fundamental 接口

1.11.90 fix: fix futures_rule interface

    1. 修复 futures_rule 接口
    2. 修复 stock_zh_a_spot 接口

1.11.89 fix: fix bond_zh_us_rate interface

    1. 修复 bond_zh_us_rate 接口

1.11.88 fix: fix macro_china_swap_rate interface

    1. 修复 macro_china_swap_rate 接口

1.11.87 fix: fix futures_board_index_nh interface

    1. 修复 futures_board_index_nh 接口

1.11.86 fix: fix stock_telegraph_cls interface

    1. 修复 stock_telegraph_cls 接口
    2. 修复 stock_xgsglb_em 接口
    3. 修复 stock_market_activity_legu 接口

1.11.85 fix: fix stock_market_activity_legu interface

    1. 修复 stock_market_activity_legu 接口

1.11.84 fix: fix fund_name_em interface

    1. 修复 fund_name_em 接口

1.11.83 fix: fix stock_zt_pool_strong_em interface

    1. 修复 stock_zt_pool_em 接口
    2. 修复 stock_zt_pool_previous_em 接口
    3. 修复 stock_zt_pool_strong_em 接口
    4. 修复 stock_zt_pool_sub_new_em 接口
    5. 修复 stock_zt_pool_zbgc_em 接口
    6. 修复 stock_zt_pool_dtgc_em 接口

1.11.82 fix: fix bond_zh_us_rate interface

    1. 修复 bond_zh_us_rate 接口

1.11.81 fix: fix stock_gdfx_free_holding_detail_em interface

    1. 修复 stock_gdfx_free_holding_detail_em 接口

1.11.80 fix: fix stock_cash_flow_sheet_by_report_em interface

    1. 修复 stock_cash_flow_sheet_by_report_em 接口
    2. 修复 get_receipt 接口
    3. 修复 stock_zygc_ym 接口
    4. 修复 bond_china_close_return 接口

1.11.79 fix: fix get_receipt interface

    1. 修复 get_receipt 接口

1.11.78 add: add stock_financial_benefit_ths interface

    1. 新增 stock_financial_benefit_ths 接口
    2. 新增 stock_financial_cash_ths 接口
    3. 新增 stock_financial_debt_ths 接口

1.11.77 fix: fix futures_zh_spot interface

    1. 修复 futures_zh_spot 接口

1.11.76 fix: fix option_czce_daily interface

    1. 修复 option_czce_daily 接口
    2. 移除 stock_hot_tgb 接口
    3. 修复 futures_board_index_nh 接口
    4. 修复 stock_hk_hist 接口

1.11.75 fix: fix futures_comex_inventory interface

    1. 修复 futures_comex_inventory 接口

1.11.74 fix: fix stock_comment_em interface

    1. 修复 stock_comment_em 接口

1.11.73 fix: fix futures_comex_inventory interface

    1. 修复 futures_comex_inventory 接口

1.11.72 fix: fix get_rank_sum_daily interface

    1. 修复 get_rank_sum_daily 接口

1.11.71 fix: fix stock_balance_sheet_by_report_em interface

    1. 修复 stock_balance_sheet_by_report_em 接口

1.11.70 fix: fix futures_gfex_position_rank interface

    1. 修复 futures_gfex_position_rank 接口

1.11.69 add: add futures_gfex_position_rank interface

    1. 新增 futures_gfex_position_rank 接口

1.11.68 fix: fix fund_aum_em interface

    1. 修复 fund_aum_em 接口

1.11.67 fix: fix currency_boc_sina interface

    1. 修复 currency_boc_sina 接口

1.11.66 fix: fix fund_scale_structured_sina interface

    1. 修复 fund_scale_structured_sina 接口

1.11.65 fix: fix futures_index_ccidx interface

    1. 修复 futures_index_ccidx 接口

1.11.64 fix: fix futures_settlement_price_sgx interface

    1. 修复 futures_settlement_price_sgx 接口

1.11.63 fix: fix fund_scale_open_sina interface

    1. 修复 fund_scale_open_sina 接口

1.11.62 fix: fix stock_zt_pool_dtgc_em interface

    1. 修复 stock_zt_pool_dtgc_em 接口

1.11.61 fix: fix fund_manager_em interface

    1. 修复 fund_manager_em 接口

1.11.60 fix: fix bond_china_close_return interface

    1. 修复 bond_china_close_return 接口

1.11.59 fix: fix fund_portfolio_change_em interface

    1. 修复 fund_portfolio_change_em 接口

1.11.58 fix: fix bond_china_close_return interface

    1. 修复 bond_china_close_return 接口
    2. 修复 stock_zh_a_daily 接口

1.11.57 fix: fix stock_zt_pool_em interface

    1. 修复 stock_zt_pool_em 接口

1.11.56 fix: fix stock_balance_sheet_by_report_delisted_em interface

    1. 修复 stock_balance_sheet_by_report_delisted_em 接口

1.11.55 fix: fix fund_portfolio_bond_hold_em interface

    1. 修复 fund_portfolio_bond_hold_em 接口

1.11.54 fix: fix fund_portfolio_hold_em interface

    1. 修复 fund_portfolio_hold_em 接口

1.11.53 add: add stock_zh_a_hist_tx interface

    1. 新增 stock_zh_a_hist_tx 接口

1.11.52 fix: fix fund_scale_change_em interface

    1. 修复 fund_scale_change_em 接口

1.11.51 fix: fix stock_zh_a_daily interface

    1. 修复 stock_zh_a_daily 接口

1.11.50 fix: fix amac_fund_abs support

    1. 修复 amac_fund_abs 接口

1.11.49 add: add aarch64 support

    1. 新增 aarch64 支持

1.11.48 fix: fix installation.md

    1. 修复 installation.md

1.11.47 add: add akracer 0.0.8 support

    1. 修复 akracer 0.0.8 support

1.11.46 add: add akracer support

    1. 新增 akracer 支持 MacOS M 系列处理器使用

1.11.45 add: add stock_balance_sheet_by_report_delisted_em interface

    1. 新增 stock_balance_sheet_by_report_delisted_em 接口
    2. 新增 stock_profit_sheet_by_report_delisted_em 接口
    3. 新增 stock_cash_flow_sheet_by_report_delisted_em 接口

1.11.44 add: add stock_cyq_em interface

    1. 新增 stock_cyq_em 接口

1.11.43 fix: fix get_futures_daily interface

    1. 修复 get_futures_daily 接口

1.11.42 fix: fix stock_gpzy_pledge_ratio_em interface

    1. 修复 stock_gpzy_pledge_ratio_em 接口

1.11.41 fix: fix index_weibo_sina interface

    1. 重命名 weibo_index 为 index_weibo_sina 接口

1.11.40 fix: fix index_option_300etf_qvix interface

    1. 新增 index_option_300etf_qvix 接口

1.11.39 fix: fix index_option_50etf_qvix interface

    1. 重命名 option_50etf_qvix 为 index_option_50etf_qvix 接口
    2. 重命名 option_50etf_min_qvix 为 index_option_50etf_min_qvix 接口
    3. 重命名 option_300etf_qvix 为 index_option_300etf_qvix 接口
    4. 重命名 option_300etf_min_qvix 为 index_option_300etf_min_qvix 接口

1.11.38 fix: fix setup.py interface

    1. 新增 python 3.12 支持

1.11.37 fix: fix index_fear_greed_funddb interface

    1. 重命名 stock_fear_greed_funddb 为 index_fear_greed_funddb 接口

1.11.36 add: add stock_fear_greed_funddb interface

    1. 新增 stock_fear_greed_funddb 接口

1.11.35 fix: fix stock_board_concept_hist_ths interface

    1. 修复 stock_board_concept_hist_ths 接口

1.11.34 add: add stock_board_concept_graph_ths interface

    1. 新增 stock_board_concept_graph_ths 接口

1.11.33 add: add stock_intraday_em interface

    1. 新增 stock_intraday_em 接口

1.11.32 add: add stock_margin_ratio_pa interface

    1. 新增 stock_margin_ratio_pa 接口

1.11.31 fix: fix futures_dce_warehouse_receipt interface

    1. 修复 futures_dce_warehouse_receipt 接口

1.11.30 fix: fix stock_zh_a_st_em interface

    1. 修复 stock_zh_a_st_em 接口

1.11.29 fix: fix bond_new_composite_index_cbond interface

    1. 修复 bond_new_composite_index_cbond 接口

1.11.28 fix: fix stock_margin_detail_szse interface

    1. 修复 stock_margin_detail_szse 接口

1.11.27 fix: fix stock_margin_detail_szse interface

    1. 修复 stock_margin_detail_szse 接口

1.11.26 fix: fix macro_china_supply_of_money interface

    1. 修复 macro_china_supply_of_money 接口

1.11.25 fix: fix macro_china_central_bank_balance interface

    1. 修复 macro_china_central_bank_balance 接口

1.11.24 fix: fix macro_china_postal_telecommunicational interface

    1. 修复 macro_china_postal_telecommunicational 接口

1.11.23 fix: fix macro_china_society_traffic_volume interface

    1. 修复 macro_china_society_traffic_volume 接口

1.11.22 fix: fix option_dce_daily interface

    1. 修复 option_dce_daily 接口

1.11.21 fix: fix get_dce_daily interface

    1. 修复 get_dce_daily 接口

1.11.20 fix: fix option_dce_daily interface

    1. 修复 option_dce_daily 接口

1.11.19 fix: fix drewry_wci_index interface

    1. 修复 drewry_wci_index 接口

1.11.18 fix: fix get_rank_sum_daily interface

    1. 修复 get_rank_sum_daily 接口

1.11.17 fix: fix futures_spot_price_daily interface

    1. 修复 futures_spot_price_daily 接口

1.11.16 fix: fix stock_dividend_cninfo interface

    1. 修复 stock_dividend_cninfo 接口

1.11.15 fix: fix stock_dividend_cninfo interface

    1. 修复 stock_dividend_cninfo 接口
    2. 修复 stock_zh_a_daily 接口

1.11.14 fix: fix migration_area_baidu interface

    1. 修复 migration_area_baidu 接口

1.11.13 fix: fix futures_comm_info interface

    1. 修复 futures_comm_info 接口

1.11.12 fix: fix stock_board_concept_hist_ths interface

    1. 修复 stock_board_concept_hist_ths 接口

1.11.11 fix: fix spot_hist_sge interface

    1. 修复 spot_hist_sge 接口

1.11.10 fix: fix bond_new_composite_index_cbond interface

    1. 修复 bond_new_composite_index_cbond 接口
    2. 修复 stock_board_industry_summary_ths 接口

1.11.9 fix: fix currency_boc_safe interface

    1. 修复 currency_boc_safe 接口

1.11.8 fix: fix news_economic_baidu interface

    1. 修复 news_economic_baidu 接口

1.11.7 fix: fix get_futures_daily interface

    1. 修复 get_futures_daily 接口

1.11.6 fix: fix futures_main_sina interface

    1. 修复 futures_main_sina 接口
    2. 修复 get_receipt 接口

1.11.5 fix: fix macro_china_hk_cpi interface

    1. 修复 macro_china_hk_cpi 接口

1.11.4 fix: fix bond_cb_profile_sina interface

    1. 修复 bond_cb_profile_sina 接口

1.11.3 fix: fix stock_a_high_low_statistics interface

    1. 修复 stock_a_high_low_statistics 接口

1.11.2 fix: fix stock_a_below_net_asset_statistics interface

    1. 修复 stock_a_below_net_asset_statistics 接口

1.11.1 add: add index_us_stock_sina interface

    1. 新增 index_us_stock_sina 接口

1.10.99 fix: fix crypto_bitcoin_cme interface

    1. 修复 crypto_bitcoin_cme 接口

1.10.98 fix: fix get_cffex_rank_table interface

    1. 修复 get_cffex_rank_table 接口

1.10.97 fix: fix stock_financial_analysis_indicator interface

    1. 修复 stock_financial_analysis_indicator 接口

1.10.96 fix: fix stock_hk_daily interface

    1. 修复 stock_hk_daily 接口

1.10.95 fix: fix crypto_bitcoin_cme interface

    1. 修复 crypto_bitcoin_cme 接口
    2. 修复 stock_zh_a_minute 接口
    3. 修复 crypto_js_spot 接口

1.10.94 add: add macro_china_nbs_nation interface

    1. 修复 macro_china_nbs_nation 接口

1.10.93 add: add stock_ipo_summary_cninfo interface

    1. 新增 stock_ipo_summary_cninfo 接口

1.10.92 fix: fix stock_individual_fund_flow interface

    1. 修复 stock_individual_fund_flow 接口

1.10.91 fix: fix stock_share_hold_change_szse interface

    1. 修复 stock_share_hold_change_szse 接口
    2. 修复 futures_dce_position_rank 接口

1.10.90 fix: fix futures_comex_inventory interface

    1. 修复 futures_comex_inventory 接口

1.10.89 add: add stock_share_hold_change_bse interface

    1. 新增 stock_share_hold_change_bse 接口
    2. 新增 stock_share_hold_change_sse 接口
    3. 新增 stock_share_hold_change_szse 接口

1.10.88 add: add stock_research_report_em interface

    1. 新增 stock_research_report_em 接口

1.10.87 add: add stock_zdhtmx_em interface

    1. 新增 stock_zdhtmx_em 接口

1.10.86 add: add stock_gddh_em interface

    1. 新增 stock_gddh_em 接口

1.10.85 fix: fix stock_hot_rank_wc interface

    1. 修复 stock_hot_rank_wc 接口

1.10.84 fix: fix stock_us_fundamental interface

    1. 修复 stock_us_fundamental 接口

1.10.83 add: add stock_industry_clf_hist_sw interface

    1. 新增 stock_industry_clf_hist_sw 接口

1.10.82 fix: fix currency_boc_sina interface

    1. 修复 currency_boc_sina 接口
    2. 修复 futures_dce_position_rank 接口
    3. 修复 get_rank_sum_daily 接口

1.10.81 fix: fix stock_bid_ask_em interface

    1. 修复 stock_bid_ask_em 接口
    2. 移除 stock_us_zh_spot 接口

1.10.80 fix: fix macro_china_gyzjz interface

    1. 修复 macro_china_gyzjz 接口

1.10.79 add: add stock_hold_management_detail_em interface

    1. 新增 stock_hold_management_detail_em 接口
    2. 新增 stock_hold_management_person_em 接口
    3. 新增 stock_gsrl_gsdt_em 接口

1.10.78 fix: fix get_cffex_rank_table interface

    1. 修复 get_cffex_rank_table 接口
    2. 修复 futures_spot_price 接口

1.10.77 add: add bond_cb_profile_sina interface

    1. 新增 bond_cb_profile_sina 接口
    2. 新增 bond_cb_summary_sina 接口

1.10.76 fix: fix stock_notice_report interface

    1. 修复 stock_notice_report 接口
    2. 修复 stock_irm_cninfo 接口

1.10.75 add: add macro_china_urban_unemployment interface

    1. 新增 macro_china_urban_unemployment 接口

1.10.74 add: add stock_sns_sseinfo interface

    1. 新增 stock_sns_sseinfo 接口

1.10.73 add: add stock_irm_cninfo interface

    1. 新增 stock_irm_cninfo 接口
    2. 新增 stock_irm_ans_cninfo 接口

1.10.72 fix: fix stock_financial_hk_report_em interface

    1. 修复 stock_financial_hk_report_em 接口

1.10.71 fix: fix stock_us_hist interface

    1. 修复 stock_us_hist 接口
    2. 移除 sw 相关接口

1.10.70 fix: fix stock_zh_a_hist interface

    1. 修复 stock_zh_a_hist 接口

1.10.69 fix: fix currency_latest interface

    1. 修复 currency_latest 接口
    2. 修复 currency_history 接口
    3. 修复 currency_time_series 接口
    4. 修复 currency_currencies 接口
    5. 修复 currency_convert 接口

1.10.68 fix: fix option_gfex_daily interface

    1. 修复 option_gfex_daily 接口

1.10.67 rem: rem futures_egg_price_yearly interface

    1. 移除 futures_egg_price_yearly 等接口

1.10.66 fix: fix stock_financial_report_sina interface

    1. 修复 stock_financial_report_sina 接口

1.10.65 fix: fix macro_china_lpr interface

    1. 修复 macro_china_lpr 接口

1.10.64 fix: fix stock_zh_b_spot interface

    1. 修复 stock_zh_b_spot 接口

1.10.63 fix: fix stock_esg_hz_sina interface

    1. 修复 stock_esg_hz_sina 接口

1.10.62 fix: fix index_hist_sw interface

    1. 修复 index_hist_sw 接口

1.10.61 fix: fix macro_cnbs interface

    1. 修复 macro_cnbs 接口

1.10.60 add: add macro_usa_cpi_yoy interface

    1. 新增 macro_usa_cpi_yoy 接口

1.10.59 add: add fund_announcement_personnel_em interface

    1. 新增 fund_announcement_personnel_em 接口

1.10.58 fix: fix fund_etf_hist_em interface

    1. 修复 fund_etf_hist_em 接口

1.10.57 fix: fix stock_zh_valuation_baidu interface

    1. 修复 stock_zh_valuation_baidu 接口

1.10.56 fix: fix stock_zh_b_daily interface

    1. 修复 stock_zh_b_daily 接口

1.10.55 fix: fix macro_usa_personal_spending interface

    1. 修复 macro_usa_personal_spending 接口
    2. 修复 append to concat 方法

1.10.54 fix: fix macro_usa_core_cpi_monthly interface

    1. 修复 macro_usa_core_cpi_monthly 接口

1.10.53 fix: fix index_stock_cons_csindex interface

    1. 修复 index_stock_cons_csindex 接口

1.10.52 fix: fix stock_financial_hk_report_em interface

    1. 修复 stock_financial_hk_report_em 接口
    2. 修复 stock_financial_hk_analysis_indicator_em 接口
    3. 修复 index_value_name_funddb 接口

1.10.51 fix: fix fund_money_rank_em interface

    1. 修复 fund_money_rank_em 接口

1.10.50 fix: fix car_energy_sale_cpca interface

    1. 修复 car_energy_sale_cpca 接口

1.10.49 fix: fix stock_hot_rank_em interface

    1. 修复 stock_hot_rank_em 接口
    2. 移除 club_rank_game 接口
    3. 移除 player_rank_game 接口

1.10.48 add: add stock_esg_hz_sina interface

    1. 新增 stock_esg_hz_sina 接口

1.10.47 add: add stock_esg_rate_sina interface

    1. 新增 stock_esg_rate_sina 接口

1.10.46 fix: fix index_value_hist_funddb interface

    1. 修复 index_value_hist_funddb 接口

1.10.45 fix: fix stock_zh_a_minute interface

    1. 修复 stock_zh_a_minute 接口

1.10.44 fix: fix get_shfe_rank_table interface

    1. 修复 get_shfe_rank_table 接口

1.10.43 rem: rem index_vix interface

    1. 移除 index_vix 接口

1.10.42 fix: fix fund_rating_all interface

    1. 修复 fund_rating_all 接口
    2. 修复 fund_rating_sh 接口
    3. 修复 fund_rating_zs 接口
    4. 修复 fund_rating_ja 接口

1.10.41 add: add fund_lof_hist_em interface

    1. 新增 fund_lof_hist_em 接口
    2. 新增 fund_lof_spot_em 接口
    3. 新增 fund_lof_hist_min_em 接口

1.10.40 fix: fix futures_news_baidu interface

    1. 修复 futures_news_baidu 接口

1.10.39 fix: fix stock_board_concept_hist_min_em interface

    1. 修复 stock_board_concept_hist_min_em 接口

1.10.38 fix: fix stock_board_industry_hist_min_em interface

    1. 修复 stock_board_industry_hist_min_em 接口

1.10.37 rem: rem index_stock_hist interface

    1. 移除 index_stock_hist 接口

1.10.36 fix: fix stock_sy_profile_em interface

    1. 修复 stock_sy_profile_em 接口
    2. 修复 stock_sy_yq_em 接口
    3. 修复 stock_sy_jz_em 接口
    4. 修复 stock_sy_em 接口
    5. 修复 stock_sy_hy_em 接口

1.10.35 add: add get_gfex_receipt interface

    1. 新增 get_gfex_receipt 接口

1.10.34 fix: fix futures_display_main_sina interface

    1. 修复 futures_display_main_sina 接口

1.10.33 fix: fix index_sugar_msweet interface

    1. 修复 index_sugar_msweet 接口
    2. 修复 index_eri 接口
    3. 修复 drewry_wci_index 接口

1.10.32 fix: fix get_cffex_daily interface

    1. 修复 get_cffex_daily 接口

1.10.31 fix: fix zh_subscribe_exchange_symbol interface

    1. 修复 zh_subscribe_exchange_symbol 接口

1.10.30 fix: fix stock_info_sz_name_code interface

    1. 修复 stock_info_sz_name_code 接口

1.10.29 fix: fix stock_zh_index_daily_em interface

    1. 修复 stock_zh_index_daily_em 接口

1.10.28 fix: fix stock_hot_up_em interface

    1. 修复 stock_hot_up_em 接口

1.10.27 fix: fix stock_hot_up_em interface

    1. 修复 stock_hot_up_em 接口

1.10.26 add: add stock_hot_up_em interface

    1. 新增 stock_hot_up_em 接口

1.10.25 fix: fix index_sugar_msweet interface

    1. 修复 index_sugar_msweet 接口
    2. 修复 index_inner_quote_sugar_msweet 接口
    3. 修复 index_outer_quote_sugar_msweet 接口

1.10.24 fix: fix stock_zh_a_daily interface

    1. 修复 stock_zh_a_daily 接口

1.10.23 fix: fix index_kq_fz interface

    1. 修复 index_kq_fz 接口
    2. 修复 index_kq_fashion 接口

1.10.22 fix: fix macro_china_cpi_monthly interface

    1. 修复 macro_china_cpi_monthly 接口

1.10.21 fix: fix fund_report_stock_cninfo interface

    1. 修复 fund_report_stock_cninfo 接口
    2. 修复 fund_report_industry_allocation_cninfo 接口
    3. 修复 fund_report_asset_allocation_cninfo 接口

1.10.20 fix: fix stock_new_gh_cninfo interface

    1. 修复 stock_new_gh_cninfo 接口
    2. 修复 stock_new_ipo_cninfo 接口

1.10.19 fix: fix bond_treasure_issue_cninfo interface

    1. 修复 bond_treasure_issue_cninfo 接口
    2. 修复 bond_local_government_issue_cninfo 接口
    3. 修复 bond_corporate_issue_cninfo 接口
    4. 修复 bond_cov_issue_cninfo 接口
    5. 修复 bond_cov_stock_issue_cninfo 接口

1.10.18 fix: fix index_yw interface

    1. 修复 index_yw 接口
    2. 修复 spot_goods 接口

1.10.17 fix: fix stock_allotment_cninfo interface

    1. 修复 stock_allotment_cninfo 接口

1.10.16 fix: fix bond_zh_hs_cov_min interface

    1. 修复 bond_zh_hs_cov_min 接口

1.10.15 fix: fix bond_zh_hs_cov_pre_min interface

    1. 修复 bond_zh_hs_cov_pre_min 接口

1.10.14 fix: fix bond_zh_hs_cov_min interface

    1. 修复 bond_zh_hs_cov_min 接口的时间显示问题

1.10.13 fix: fix stock_share_change_cninfo interface

    1. 修复 stock_share_change_cninfo 接口

1.10.12 fix: fix bond_cb_adj_logs_jsl interface

    1. 修复 bond_cb_adj_logs_jsl 接口

1.10.11 fix: fix stock_zh_a_hist_pre_min_em interface

    1. 修复 stock_zh_a_hist_pre_min_em 接口

1.10.10 fix: fix stock_zh_a_hist interface

    1. 修复 stock_zh_a_hist 接口

1.10.9 fix: fix bond_zh_hs_cov_min interface

    1. 修复 bond_zh_hs_cov_min 接口

1.10.8 fix: fix futures_volatility_index_nh interface

    1. 修复 futures_volatility_index_nh 接口

1.10.7 fix: fix option_finance_board interface

    1. 修复 option_finance_board 接口

1.10.6 fix: fix futures_nh_volatility_index interface

    1. 修复 futures_nh_volatility_index 接口

1.10.5 fix: fix index_level_one_hist_sw interface

    1. 修复 index_level_one_hist_sw 接口

1.10.4 fix: fix futures_return_index_nh interface

    1. 修复 futures_return_index_nh 接口
    2. 修复 futures_price_index_nh 接口

1.10.3 fix: fix stock_gdfx_holding_analyse_em interface

    1. 修复 stock_gdfx_holding_analyse_em 接口

1.10.2 fix: fix stock_gdfx_holding_detail_em interface

    1. 修复 stock_gdfx_holding_detail_em 接口
    2. 修复 stock_gdfx_holding_analyse_em 接口

1.10.1 fix: fix stock_hold_control_cninfo interface

    1. 修复 stock_hold_control_cninfo 接口

1.9.99 fix: fix stock_hold_num_cninfo interface

    1. 修复 stock_hold_num_cninfo 接口

1.9.98 fix: fix stock_hold_control_cninfo interface

    1. 修复 stock_hold_control_cninfo 接口

1.9.97 fix: fix stock_industry_category_cninfo interface

    1. 修复 stock_industry_category_cninfo 接口

1.9.96 fix: fix stock_hold_control_cninfo interface

    1. 修复 stock_hold_control_cninfo 接口

1.9.95 fix: fix stock_zh_index_hist_csindex interface

    1. 修复 stock_zh_index_hist_csindex 接口

1.9.94 fix: fix stock_a_indicator_lg interface

    1. 修复 stock_a_indicator_lg 接口

1.9.93 fix: fix index_level_one_hist_sw interface

    1. 修复 index_level_one_hist_sw 接口

1.9.92 fix: fix article_ff_crr interface

    1. 修复 article_ff_crr 接口

1.9.91 add: add stock_financial_abstract_ths interface

    1. 新增 stock_financial_abstract_ths 接口

1.9.90 fix: fix stock_sse_deal_daily interface

    1. 修复 stock_sse_deal_daily 接口

1.9.89 fix: fix index_kq_fz interface

    1. 修复 index_kq_fz 接口

1.9.88 fix: fix setup.py

    1. 移除 setup.py 中的相关依赖

1.9.87 add: add option_minute_em interface

    1. 新增 option_minute_em 接口

1.9.86 fix: fix index_kq_fz interface

    1. 修复 index_kq_fz 接口

1.9.85 fix: fix option_dce_daily interface

    1. 修复 option_dce_daily 接口

1.9.84 fix: fix stock_hk_fhpx_detail_ths interface

    1. 修复 stock_hk_fhpx_detail_ths 接口

1.9.83 add: add stock_concept_fund_flow_hist interface

    1. 新增 stock_concept_fund_flow_hist 接口

1.9.82 fix: fix currency_boc_safe interface

    1. 修复 currency_boc_safe 接口

1.9.81 add: add stock_hk_index_spot_sina interface

    1. 新增 stock_hk_index_spot_sina 接口
    2. 新增 stock_hk_index_daily_em 接口
    3. 新增 stock_hk_index_spot_em 接口
    4. 新增 stock_hk_index_daily_sina 接口

1.9.80 fix: fix futures_spot_price interface

    1. 修复 futures_spot_price 接口

1.9.79 fix: fix stock_sse_deal_daily interface

    1. 修复 stock_sse_deal_daily 接口

1.9.78 fix: fix macro_usa_gdp_monthly interface

    1. 修复 macro_usa_gdp_monthly 接口

1.9.77 fix: fix stock_hot_rank_wc interface

    1. 修复 stock_hot_rank_wc 接口

1.9.76 fix: fix stock_sector_detail interface

    1. 修复 stock_sector_detail 接口

1.9.75 fix: fix stock_board_industry_index_ths interface

    1. 修复 stock_board_industry_index_ths 接口

1.9.74 fix: fix get_shfe_rank_table interface

    1. 修复 get_shfe_rank_table 接口

1.9.73 add: add bond_zh_cov_info_ths interface

    1. 新增 bond_zh_cov_info_ths 接口

1.9.72 fix: fix fund_manager interface

    1. 修复 fund_manager 接口

1.9.71 fix: fix stock_lh_yyb_most interface

    1. 修复 stock_lh_yyb_most 接口

1.9.70 fix: fix stock_szse_sector_summary interface

    1. 修复 stock_szse_sector_summary 接口

1.9.69 fix: fix stock_lh_yyb_capital interface

    1. 修复 stock_lh_yyb_capital 接口

1.9.68 fix: fix stock_lh_yyb_capital interface

    1. 修复 stock_lh_yyb_capital 接口

1.9.67 fix: fix futures_zh_daily_sina interface

    1. 修复 futures_zh_daily_sina 接口

1.9.66 fix: fix match_main_contract interface

    1. 修复 match_main_contract 接口

1.9.65 fix: fix stock_hot_search_baidu interface

    1. 修复 stock_hot_search_baidu 接口

1.9.64 fix: fix stock_a_indicator_lg interface

    1. 修复 stock_a_indicator_lg 接口

1.9.63 fix: fix get_czce_rank_table interface

    1. 修复 get_czce_rank_table 接口

1.9.62 fix: fix bond_zh_us_rate interface

    1. 修复 bond_zh_us_rate 接口

1.9.61 fix: fix stock_lhb_detail_daily_sina interface

    1. 修复 stock_lhb_detail_daily_sina 接口

1.9.60 add: add stock_hk_fhpx_detail_ths interface

    1. 新增 stock_hk_fhpx_detail_ths 接口

1.9.59 fix: fix stock_hot_search_baidu interface

    1. 修复 stock_hot_search_baidu 接口

1.9.58 add: add option_gfex_daily interface

    1. 新增 option_gfex_daily 接口
    2. 新增 option_gfex_vol_daily 接口

1.9.57 fix: fix stock_lhb_detail_em interface

    1. 修复 stock_lhb_detail_em 接口

1.9.56 fix: fix get_receipt interface

    1. 修复 get_receipt 接口

1.9.55 fix: fix stock_zh_valuation_baidu interface

    1. 修复 stock_zh_valuation_baidu 接口

1.9.54 fix: fix stock_board_concept_cons_ths interface

    1. 修复 stock_board_concept_cons_ths 接口

1.9.53 fix: fix get_ine_daily interface

    1. 修复 get_ine_daily 接口

1.9.52 fix: fix get_shfe_rank_table interface

    1. 修复 get_shfe_rank_table 接口

1.9.51 fix: fix get_shfe_daily interface

    1. 修复 get_shfe_daily 接口

1.9.50 fix: fix stock_a_all_pb interface

    1. 修复 stock_a_all_pb 接口
    2. 修复 stock_a_ttm_lyr 接口

1.9.49 add: add stock_lhb_yybph_em interface

    1. 新增 stock_lhb_yybph_em 接口
    2. 新增 stock_lhb_jgstatistic_em 接口
    3. 新增 stock_lhb_traderstatistic_em 接口

1.9.48 fix: fix index_stock_cons interface

    1. 修复 index_stock_cons 接口

1.9.47 fix: fix option_dce_daily interface

    1. 修复 option_dce_daily 接口

1.9.46 fix: fix stock_a_gxl_lg interface

    1. 修复 stock_a_gxl_lg 接口

1.9.45 add: add stock_fhps_detail_ths interface

    1. 新增 stock_fhps_detail_ths 接口

1.9.44 fix: fix stock_a_high_low_statistics interface

    1. 修复 stock_a_high_low_statistics 接口

1.9.43 fix: fix stock_a_congestion_lg interface

    1. 修复 stock_a_congestion_lg 接口

1.9.42 add: add stock_bid_ask_em interface

    1. 新增 stock_bid_ask_em 接口

1.9.41 fix: fix stock_a_indicator_lg interface

    1. 修复 stock_a_indicator_lg 接口

1.9.40 fix: fix stock_profit_forecast_em interface

    1. 修复 stock_profit_forecast_em 接口
    2. 修复 stock_index_pb_lg 接口
    3. 修复 stock_index_pe_lg 接口

1.9.39 fix: fix fund_stock_position_lg interface

    1. 修复 fund_stock_position_lg 接口
    2. 修复 fund_balance_position_lg 接口
    3. 修复 fund_linghuo_position_lg 接口
    4. 修复 stock_ebs_lg 接口
    5. 修复 stock_buffett_index_lg 接口

1.9.38 fix: fix stock_a_lg_indicator interface

    1. 修复 stock_a_lg_indicator 接口

1.9.37 fix: fix stock_hk_indicator_eniu interface

    1. 修复 stock_hk_indicator_eniu 接口

1.9.36 fix: fix stock_market_pe_lg interface

    1. 修复 stock_market_pe_lg 接口
    2. 修复 stock_market_pb_lg 接口
    3. 修复 stock_index_pb_lg 接口
    4. 修复 stock_index_pe_lg 接口

1.9.35 fix: fix stock_a_lg_indicator interface

    1. 修复 stock_a_lg_indicator 接口

1.9.34 fix: fix stock_zh_a_tick_tx_js interface

    1. 修复 stock_zh_a_tick_tx_js 接口

1.9.33 add: add stock_hk_main_board_spot_em interface

    1. 新增 stock_hk_main_board_spot_em 接口

1.9.32 fix: fix bank_fjcf_table_detail interface

    1. 修复 bank_fjcf_table_detail 接口

1.9.31 fix: fix amac_fund_info interface

    1. 修复 amac_fund_info 接口

1.9.30 fix: fix stock_a_lg_indicator interface

    1. 修复 stock_a_lg_indicator 接口

1.9.29 fix: fix stock_a_lg_indicator interface

    1. 修复 stock_a_lg_indicator 接口

1.9.28 fix: fix stock_financial_report_sina interface

    1. 修复 stock_financial_report_sina 接口

1.9.27 fix: fix fund_exchange_rank_em interface

    1. 修复 fund_exchange_rank_em 接口
    2. 修复 fund_money_rank_em 接口
    3. 修复 fund_hk_rank_em 接口
    4. 修复 fund_lcx_rank_em 接口

1.9.26 fix: fix bond_cb_jsl interface

    1. 修复 bond_cb_jsl 接口

1.9.25 add: add stock_hk_hot_rank_em interface

    1. 新增 stock_hk_hot_rank_em 接口
    2. 新增 stock_hk_hot_rank_detail_em 接口
    3. 新增 stock_hk_hot_rank_latest_em 接口
    4. 新增 stock_hk_hot_rank_detail_realtime_em 接口

1.9.24 fix: fix bond_cb_adj_logs_jsl interface

    1. 修复 bond_cb_adj_logs_jsl 接口

1.9.23 fix: fix bond_cb_redeem_jsl interface

    1. 修复 bond_cb_redeem_jsl 接口

1.9.22 fix: fix fund_hk_fund_hist_em interface

    1. 修复 fund_hk_fund_hist_em 接口

1.9.21 fix: fix fund_financial_fund_info_em interface

    1. 修复 fund_financial_fund_info_em 接口

1.9.20 fix: fix fund_financial_fund_info_em interface

    1. 修复 fund_financial_fund_info_em 接口

1.9.19 fix: fix macro_cnbs interface

    1. 修复 macro_cnbs 接口

1.9.18 fix: fix macro_china_market_margin_sh interface

    1. 修复 macro_china_market_margin_sh 接口

1.9.17 add: add stock_board_industry_spot_em interface

    1. 新增 stock_board_industry_spot_em 接口

1.9.16 fix: fix stock_financial_abstract interface

    1. 修复 stock_financial_abstract 接口

1.9.15 fix: fix stock_hk_daily interface

    1. 修复 stock_hk_daily 接口

1.9.14 fix: fix option_risk_analysis_em interface

    1. 修复 option_risk_analysis_em 接口

1.9.13 fix: fix stock_zh_valuation_baidu interface

    1. 修复 stock_zh_valuation_baidu 接口

1.9.12 fix: fix stock_hot_rank_wc interface

    1. 修复 stock_hot_rank_wc 接口

1.9.11 add: add stock_sector_fund_flow_hist interface

    1. 新增 stock_sector_fund_flow_hist 接口
    2. 新增 stock_sector_fund_flow_summary 接口

1.9.10 add: add macro_shipping_bcti interface

    1. 新增 macro_shipping_bcti 接口

1.9.9 add: add macro_shipping_bci interface

    1. 新增 macro_shipping_bci 接口
    2. 新增 macro_shipping_bdi 接口
    3. 新增 macro_shipping_bpi 接口
    4. 新增 macro_shipping_bcti 接口

1.9.8 fix: fix stock_hk_valuation_baidu interface

    1. 修复 stock_hk_valuation_baidu 接口

1.9.7 add: add stock_profit_forecast_ths interface

    1. 新增 stock_profit_forecast_ths 接口
    2. 重命名 stock_profit_forecast 为 stock_profit_forecast_em

1.9.6 fix: fix futures_hog_info interface

    1. 修复 futures_hog_info 接口

1.9.5 fix: fix stock_info_a_code_name interface

    1. 修复 stock_info_a_code_name 接口

1.9.4 fix: fix drewry_wci_index interface

    1. 修复 drewry_wci_index 接口

1.9.3 fix: fix fx_quote_baidu interface

    1. 修复 fx_quote_baidu 接口

1.9.2 fix: fix stock_xgsglb_em interface

    1. 修复 stock_xgsglb_em 接口

1.9.1 fix: fix index_value_name_funddb interface

    1. 修复 index_value_name_funddb 接口

1.8.99 add: add futures_news_shmet interface

    1. 新增 futures_news_shmet 接口

1.8.98 fix: fix stock_info_sz_delist interface

    1. 修复 stock_info_sz_delist 接口

1.8.97 fix: fix futures_egg_price_yearly interface

    1. 修复 futures_egg_price_yearly 接口
    2. 修复 futures_egg_price_area 接口
    3. 修复 futures_egg_price 接口

1.8.96 fix: fix option_finance_board interface

    1. 修复 option_finance_board 接口

1.8.95 fix: fix index_zh_a_hist interface

    1. 修复 index_zh_a_hist 接口

1.8.94 fix: fix Dockerfile

    1. 修复 Dockerfile

1.8.93 fix: fix stock_gdfx_holding_detail_em interface

    1. 修复 stock_gdfx_holding_detail_em 接口

1.8.92 fix: fix stock_institute_hold interface

    1. 修复 stock_institute_hold 接口

1.8.91 fix: fix sunrise_monthly interface

    1. 修复 sunrise_monthly 接口

1.8.90 fix: fix bond_info_detail_cm interface

    1. 修复 bond_info_detail_cm 接口

1.8.89 fix: fix sunrise_city_list interface

    1. 修复 sunrise_city_list 接口

1.8.88 fix: fix stock_info_sz_delist interface

    1. 修复 stock_info_sz_delist 接口

1.8.87 fix: fix stock_info_sz_change_name interface

    1. 修复 stock_info_sz_change_name 接口

1.8.86 fix: fix stock_info_sh_delist interface

    1. 修复 stock_info_sh_delist 接口

1.8.85 fix: fix stock_info_sh_name_code interface

    1. 修复 stock_info_sh_name_code 接口

1.8.84 remove: remove stock_zh_a_scr_report interface

    1. 移除 stock_zh_a_scr_report 接口

1.8.83 fix: fix stock_info_sh_name_code interface

    1. 修复 stock_info_sh_name_code 接口

1.8.82 fix: fix stock_fund_stock_holder interface

    1. 修复 stock_fund_stock_holder 接口

1.8.81 fix: fix futures_hog_info interface

    1. 修复 futures_hog_info 接口

1.8.80 fix: fix stock_profit_forecast interface

    1. 修复 stock_profit_forecast 接口

1.8.79 fix: fix stock_hk_valuation_baidu interface

    1. 修复 stock_hk_valuation_baidu 接口

1.8.78 fix: fix stock_profit_forecast interface

    1. 修复 stock_profit_forecast 接口

1.8.77 fix: fix stock_analyst_rank_em interface

    1. 修复 stock_analyst_rank_em 接口

1.8.76 remove: remove js_news and ws interface

    1. 移除 js_news 及 ws 相关接口

1.8.75 add: add stock_cy_a_spot_em interface

    1. 新增 stock_cy_a_spot_em 接口

1.8.74 fix: fix drewry_wci_index interface

    1. 修复 drewry_wci_index 接口

1.8.73 add: add stock_zyjs_ths interface

    1. 新增 stock_zyjs_ths 接口

1.8.72 fix: fix drewry_wci_index interface

    1. 修复 drewry_wci_index 接口

1.8.71 add: add stock_zygc_em interface

    1. 新增 stock_zygc_em 接口

1.8.70 add: add stock_market_pe_lg interface

    1. 新增 stock_market_pe_lg 接口
    2. 新增 stock_index_pe_lg 接口
    3. 新增 stock_market_pb_lg 接口
    4. 新增 stock_index_pb_lg 接口

1.8.69 fix: fix stock_individual_fund_flow_rank interface

    1. 修复 stock_individual_fund_flow_rank 接口

1.8.68 fix: fix stock_individual_fund_flow interface

    1. 修复 stock_individual_fund_flow 接口

1.8.67 fix: fix python warning 3.7.x support

    1. 修复 python warning 3.7.x support

1.8.66 fix: fix python 3.7.x support

    1. 修复 python 3.7.x support

1.8.65 fix: fix get_roll_yield_bar interface

    1. 修复 get_roll_yield_bar 接口

1.8.64 fix: fix stock_ggcg_em interface

    1. 修复 stock_ggcg_em 接口

1.8.63 fix: fix stock_cash_flow_sheet_by_report_em interface

    1. 修复 stock_cash_flow_sheet_by_report_em 接口

1.8.62 fix: fix stock_board_industry_index_ths interface

    1. 修复 stock_board_industry_index_ths 接口

1.8.61 fix: fix futures_comm_info interface

    1. 修复 futures_comm_info 接口

1.8.60 fix: fix hurun_rank interface

    1. 修复 hurun_rank 接口

1.8.59 fix: fix stock_zh_valuation_baidu interface

    1. 修复 stock_zh_valuation_baidu 接口

1.8.58 fix: fix get_calendar interface

    1. 修复 get_calendar 接口

1.8.57 fix: fix stock_szse_summary interface

    1. 修复 stock_szse_summary 接口

1.8.56 fix: fix stock_hk_valuation_baidu interface

    1. 修复 stock_hk_valuation_baidu 接口

1.8.55 fix: fix macro_usa_pmi interface

    1. 修复 macro_usa_pmi 接口

1.8.54 fix: fix get_roll_yield_bar interface

    1. 修复 get_roll_yield_bar 接口

1.8.53 fix: fix stock_hot_rank_wc interface

    1. 修复 stock_hot_rank_wc 接口

1.8.52 fix: fix index_value_hist_funddb interface

    1. 修复 index_value_hist_funddb 接口

1.8.51 fix: fix fortune_rank interface

    1. 修复 fortune_rank 接口

1.8.50 fix: fix stock_us_daily interface

    1. 修复 stock_us_daily 接口

1.8.49 fix: fix futures_comm_info interface

    1. 修复 futures_comm_info 接口

1.8.48 add: add fund_etf_hist_em interface

    1. 新增 fund_etf_hist_em 接口
    2. 新增 fund_etf_hist_min_em 接口
    3. 新增 fund_etf_spot_em 接口

1.8.47 add: add option_cffex_sz50_list_sina interface

    1. 新增 option_cffex_sz50_list_sina 接口
    2. 新增 option_cffex_sz50_spot_sina 接口
    3. 新增 option_cffex_sz50_daily_sina 接口

1.8.46 fix: fix get_roll_yield_bar interface

    1. 修复 get_roll_yield_bar 接口

1.8.45 fix: fix calendar.json

    1. 新增 calendar.json 2023 日历数据

1.8.44 fix: fix stock_info_bj_name_code interface

    1. 修复 stock_info_bj_name_code 接口

1.8.43 add: add stock_ebs_lg interface

    1. 新增 stock_ebs_lg 接口

1.8.42 add: add get_gfex_daily interface

    1. 新增 get_gfex_daily 接口, 获取广期所的量价数据

1.8.41 add: add futures_index_ccidx interface

    1. 新增 futures_index_ccidx 接口

1.8.40 add: add fund_balance_position_lg interface

    1. 新增 fund_balance_position_lg 接口

1.8.39 add: add stock_board_change_em interface

    1. 新增 stock_board_change_em 接口

1.8.38 fix: fix macro_cons_gold interface

    1. 修复 macro_cons_gold 接口

1.8.37 add: add fund_stock_position_lg interface

    1. 新增 fund_stock_position_lg 接口

1.8.36 add: add stock_a_congestion_lg interface

    1. 新增 stock_a_congestion_lg 接口

1.8.35 add: add stock_hk_gxl_lg interface

    1. 新增 stock_hk_gxl_lg 接口

1.8.34 add: add stock_a_gxl_lg interface

    1. 新增 stock_a_gxl_lg 接口

1.8.33 fix: fix stock_hot_rank_em interface

    1. 修复 stock_hot_rank_em 接口

1.8.32 fix: fix js_news interface

    1. 修复 js_news 接口

1.8.31 fix: fix get_dce_daily interface

    1. 修复 get_dce_daily 接口

1.8.30 fix: fix index_value_name_funddb interface

    1. 修复 index_value_name_funddb 接口

1.8.29 fix: fix baidu_search_index interface

    1. 修复 baidu_search_index 接口
    2. 修复 baidu_info_index 接口
    3. 修复 baidu_media_index 接口

1.8.28 fix: fix fund_fh_rank_em interface

    1. 修复 fund_fh_rank_em 接口

1.8.27 fix: fix fund_cf_em interface

    1. 修复 fund_cf_em 接口

1.8.26 fix: fix bond_china_close_return_map interface

    1. 修复 bond_china_close_return_map 接口

1.8.25 fix: fix stock_circulate_stock_holder interface

    1. 修复 stock_circulate_stock_holder 接口

1.8.24 fix: fix stock_ipo_benefit_ths interface

    1. 修复 stock_ipo_benefit_ths 接口

1.8.23 add: add stock_restricted_release_summary_em interface

    1. 新增 stock_restricted_release_summary_em 接口
    2. 新增 stock_restricted_release_detail_em 接口
    3. 新增 stock_restricted_release_queue_em 接口
    4. 新增 stock_restricted_release_stockholder_em 接口
    5. 修复 stock_restricted_release_queue_sina 接口

1.8.22 fix: fix stock_margin_detail_szse interface

    1. 修复 stock_margin_detail_szse 接口

1.8.21 fix: fix stock_board_concept_hist_em interface

    1. 修复 stock_board_concept_hist_em 接口

1.8.20 fix: fix stock_board_concept_hist_em interface

    1. 修复 stock_board_concept_hist_em 接口

1.8.19 fix: fix stock_balance_sheet_by_yearly_em interface

    1. 修复 stock_balance_sheet_by_yearly_em 接口

1.8.18 add: add stock_hsgt_fund_flow_summary_em interface

    1. 新增 stock_hsgt_fund_flow_summary_em 接口

1.8.17 fix: fix macro_china_fdi interface

    1. 修复 macro_china_fdi 接口

1.8.16 fix: fix macro_china_swap_rate interface

    1. 修复 macro_china_swap_rate 接口

1.8.15 fix: fix stock_price_js interface

    1. 修复 stock_price_js 接口

1.8.14 add: add stock_board_industry_summary_ths interface

    1. 新增 stock_board_industry_summary_ths 接口

1.8.13 fix: fix macro_china_new_house_price interface

    1. 修复 macro_china_new_house_price 接口
    2. 修复 macro_china_enterprise_boom_index 接口
    3. 修复 macro_china_national_tax_receipts 接口

1.8.12 fix: fix stock_yjyg_em interface

    1. 修复 stock_yjyg_em 接口

1.8.11 fix: fix macro_china_ppi interface

    1. 修复 macro_china_ppi 接口
    2. 修复 macro_china_pmi 接口

1.8.10 fix: fix stock_a_all_pb interface

    1. 修复 stock_a_all_pb 接口
    2. 修复 macro_china_cpi 接口

1.8.9 fix: fix stock_a_ttm_lyr interface

    1. 修复 stock_a_ttm_lyr 接口

1.8.8 fix: fix macro_china_gdp interface

    1. 修复 macro_china_gdp 接口

1.8.7 fix: fix stock_a_below_net_asset_statistics interface

    1. 修复 stock_a_below_net_asset_statistics 接口

1.8.6 fix: fix stock_market_activity_legu interface

    1. 修复 stock_market_activity_legu 接口

1.8.5 fix: fix stock_a_lg_indicator interface

    1. 修复 stock_a_lg_indicator 接口

1.8.4 fix: fix macro_china_hgjck interface

    1. 修复 macro_china_hgjck 接口

1.8.3 fix: fix stock_pg_em interface

    1. 修复 stock_pg_em 接口
    2. 修复 stock_qbzf_em 接口

1.8.2 fix: fix fund_portfolio_hold_em interface

    1. 修复 fund_portfolio_hold_em 接口

1.8.1 fix: fix stock_dxsyl_em interface

    1. 修复 stock_dxsyl_em 接口
    2. 修复 macro_china_qyspjg 接口

1.7.99 fix: fix stock_lhb_detail_daily_sina interface

    1. 修复 stock_lhb_detail_daily_sina 接口
    2. 修复 stock_lhb_ggtj_sina 接口
    3. 修复 stock_lhb_yytj_sina 接口
    4. 修复 stock_lhb_jgzz_sina 接口
    5. 修复 stock_lhb_jgmx_sina 接口

1.7.98 add: add stock_zh_a_gdhs interface

    1. 修复 stock_zh_a_gdhs 接口

1.7.97 add: add index_hog_spot_price interface

    1. 新增 index_hog_spot_price 接口

1.7.96 fix: fix futures_hog_info interface

    1. 修复 futures_hog_info 接口

1.7.95 fix: fix spot_golden_benchmark_sge interface

    1. 修复 spot_golden_benchmark_sge 接口

1.7.94 fix: fix fund_portfolio_hold_em interface

    1. 修复 fund_portfolio_hold_em 接口

1.7.93 fix: fix sw_index_third_cons interface

    1. 修复 sw_index_third_cons 接口

1.7.92 fix: fix fund_portfolio_hold_em interface

    1. 修复 fund_portfolio_hold_em 接口

1.7.91 fix: fix futures_price_index_nh interface

    1. 修复 futures_price_index_nh 接口时区对齐问题

1.7.90 fix: fix stock_yjbb_em interface

    1. 修复 stock_yjbb_em 接口

1.7.89 fix: fix stock_zh_index_daily_tx interface

    1. 修复 stock_zh_index_daily_tx 接口的索引问题

1.7.88 fix: fix stock_news_em interface

    1. 修复 stock_news_em 接口

1.7.87 fix: fix macro_uk interface

    1. 修复 macro_uk 所有接口

1.7.86 fix: fix bond_info_cm interface

    1. 修复 bond_info_cm 接口

1.7.85 fix: fix stock_board_industry_hist_em interface

    1. 修复 stock_board_industry_hist_em 接口

1.7.84 add: add bond_info_cm interface

    1. 新增 bond_info_cm 接口
    2. 新增 bond_info_detail_cm_df 接口

1.7.83 fix: fix macro_japan interface

    1. 修复 macro_japan 相关接口

1.7.82 fix: fix index_analysis_daily_sw interface

    1. 重命名 index_analysis_sw 为 index_analysis_daily_sw 接口
    2. 新增 index_analysis_weekly_sw 接口
    3. 新增 index_analysis_monthly_sw 接口
    4. 新增 index_analysis_week_month_sw 接口

1.7.81 fix: fix macro_swiss_svme interface

    1. 修复 macro_swiss_svme 接口

1.7.80 fix: fix stock_a_below_net_asset_statistics interface

    1. 修复 stock_a_below_net_asset_statistics 接口

1.7.79 fix: fix macro_germany interface

    1. 修复 macro_germany 所有接口

1.7.78 add: add index_analysis_sw interface

    1. 新增 index_analysis_sw 接口

1.7.77 fix: fix index_value_hist_funddb interface

    1. 修复 index_value_hist_funddb 接口

1.7.76 fix: fix macro_euro_gdp_yoy interface

    1. 修复 macro_euro_gdp_yoy 接口

1.7.75 add: add index_component_sw interface

    1. 新增 index_component_sw 接口

1.7.74 fix: fix futures_news_baidu interface

    1. 修复 futures_news_baidu 接口

1.7.73 fix: fix stock_zh_index_daily_tx interface

    1. 修复 stock_zh_index_daily_tx 接口

1.7.72 add: add index_min_sw interface

    1. 新增 index_min_sw 接口

1.7.71 add: add support for Python 3.11

    1. 增加对 Python 3.11 的支持

1.7.70 fix: fix index_hist_sw interface

    1. 修复 index_hist_sw 接口

1.7.69 add: add index_hist_sw interface

    1. 新增 index_hist_sw 接口

1.7.68 fix: fix hurun_rank interface

    1. 修复 hurun_rank 接口

1.7.67 fix: fix xincaifu_rank interface

    1. 修复 xincaifu_rank 接口

1.7.66 add: add index_realtime_sw interface

    1. 新增 index_realtime_sw 接口

1.7.65 fix: fix futures_rule interface

    1. 修复 futures_rule 接口

1.7.64 add: add option_50etf_min_qvix interface

    1. 新增 option_50etf_min_qvix 接口

1.7.63 add: add option_300etf_min_qvix interface

    1. 新增 option_300etf_min_qvix 接口

1.7.62 add: add option_300etf_qvix interface

    1. 新增 option_300etf_qvix 接口

1.7.61 add: add option_50etf_qvix interface

    1. 新增 option_50etf_qvix 接口

1.7.60 fix: fix stock_zh_a_spot_em interface

    1. 修复 stock_zh_a_spot_em 接口

1.7.59 fix: fix stock_a_high_low_statistics interface

    1. 修复 stock_a_high_low_statistics 接口

1.7.58 fix: fix bond_cb_redeem_jsl interface

    1. 修复 bond_cb_redeem_jsl 接口

1.7.57 fix: fix stock_a_high_low_statistics interface

    1. 修复 stock_a_high_low_statistics 接口

1.7.56 fix: fix stock_buffett_index_lg interface

    1. 修复 stock_buffett_index_lg 接口

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

1.13.39 add: add index_news_sentiment_scope interface

1.13.38 fix: fix stock_market_activity_legu interface

1.13.37 fix: fix stock_hk_index_daily_sina interface

1.13.36 fix: fix stock_hsgt_hist_em interface

1.13.35 fix: fix stock_margin_szse interface

1.13.34 fix: fix bank_fjcf_table_detail interface

1.13.33 fix: fix index_realtime_fund_sw interface

1.13.32 fix: fix futures_contract_info_czce interface

1.13.31 fix: fix stock_individual_spot_xq interface

1.13.30 fix: fix futures_contract_info_shfe interface

1.13.29 fix: fix stock_esg_msci_sina interface

1.13.28 fix: fix stock_restricted_release_queue_em interface

1.13.27 add: add stock_esg_msci_sina interface

1.13.26 fix: fix option_sse_minute_sina interface

1.13.25 fix: fix futures_zh_daily_sina interface

1.13.24 fix: fix futures_spot_sys interface

1.13.23 add: add macro_usa_cme_merchant_goods_holding interface

1.13.22 fix: fix amac_manager_cancelled_info interface

1.13.21 fix: fix stock_yjkb_em interface

1.13.20 fix: fix stock_zh_a_disclosure_report_cninfo interface

1.13.19 add: add car_market_country_cpca interface

1.13.18 fix: fix macro_china_pmi_yearly interface

1.13.17 fix: fix stock_zcfz_em interface

1.13.16 add: add car_market_cate_cpca interface

1.13.15 add: add car_market_man_rank_cpca interface

1.13.14 fix: fix futures_fees_info interface

1.13.13 fix: fix car_market_cpca interface

1.13.12 fix: fix stock_zyjs_ths interface

1.13.11 fix: fix option_minute_em interface

1.13.10 fix: fix news_trade_notify_dividend_baidu interface

1.13.9 chore: remove pyarrow deps

1.13.8 fix: fix fund_etf_hist_em interface

1.13.7 add: add futures_fees_info interface

1.13.6 fix: fix stock_board_concept_name_ths interface

1.13.5 fix: fix stock_main_fund_flow interface

1.13.4 fix: fix stock_individual_spot_xq interface

1.13.3 fix: fix stock_main_fund_flow interface

1.13.2 add: add stock_main_fund_flow interface

1.13.1 fix: fix futures_spot_stock interface

1.12.99 fix: fix index_hog_spot_price interface

1.12.98 fix: fix bond_zh_cov interface

1.12.97 fix: fix stock_zh_a_hist_min_em interface

1.12.96 fix: fix stock_bid_ask_em interface

1.12.95 add: add futures_hog_core interface

1.12.94 fix: fix stock_hk_index_daily_em interface

1.12.93 fix: fix bond_debt_nafmii interface

1.12.92 fix: fix fund_etf_hist_min_em interface

1.12.91 add: add stock_info_global_em interface

1.12.90 fix: fix fund_etf_spot_em interface

1.12.89 fix: fix bond_china_yield interface

1.12.88 fix: fix fund_etf_spot_em interface

1.12.87 fix: fix fortune_rank interface

1.12.86 fix: fix fund_etf_spot_em interface

1.12.85 fix: fix stock_sector_fund_flow_summary interface

1.12.84 fix: fix stock_market_fund_flow interface

1.12.83 fix: fix stock_sector_fund_flow_rank interface

1.12.82 fix: fix stock_tfp_em interface

1.12.81 fix: fix macro_china_bond_public interface

1.12.80 fix: fix get_czce_daily interface

1.12.79 fix: fix futures_main_sina interface

1.12.78 fix: fix stock_info_sh_delist interface

1.12.77 fix: fix futures_contract_info_shfe interface

1.12.76 fix: fix bond_zh_hs_spot interface

1.12.75 add: add futures_contract_info_ine interface

1.12.74 add: add futures_contract_info_czce interface

1.12.73 fix: fix stock_individual_spot_xq interface

1.12.72 fix: fix stock_hot_rank_wc interface

1.12.71 fix: fix stock_zh_ah_spot interface

1.12.70 fix: fix stock_lhb_detail_daily_sina interface

1.12.69 fix: fix futures_hold_pos_sina interface

1.12.68 fix: fix option_finance_board interface

1.12.67 fix: fix index_hist_sw interface

1.12.66 fix: fix stock_board_industry_hist_em interface

1.12.65 fix: fix futures_foreign_commodity_realtime interface

1.12.64 fix: fix stock_board_industry_index_ths interface

1.12.63 add: add akqmt interface

1.12.62 fix: fix stock_fund_flow_individual interface

1.12.61 fix: fix stock_bid_ask_em interface

1.12.60 fix: fix movie_boxoffice_daily interface

1.12.59 fix: fix movie_boxoffice_realtime interface

1.12.58 fix: fix stock_ipo_summary_cninfo interface

1.12.57 fix: fix bank_fjcf_table_detail interface

1.12.56 fix: fix stock_a_indicator_lg interface

1.12.55 fix: fix stock_us_hist interface

1.12.54 fix: fix stock_gpzy_pledge_ratio_detail_em interface

1.12.53 fix: fix stock_rank_xzjp_ths interface

1.12.52 fix: fix stock_rank_cxg_ths interface

1.12.51 add: add stock_hsgt_fund_min_em interface

1.12.50 fix: fix bond_china_close_return interface

1.12.49 fix: fix stock_dxsyl_em interface

1.12.48 fix: fix option_minute_em interface

1.12.47 fix: fix stock_zh_ah_daily interface

1.12.46 fix: fix futures_contract_detail interface

1.12.45 fix: fix stock_individual_spot_xq interface

1.12.44 fix: fix stock_zh_ah_daily interface

1.12.43 fix: fix macro_china_market_margin_sh interface

1.12.42 fix: fix stock_news_em interface

1.12.41 fix: fix sw_index_third_cons interface

1.12.40 fix: fix futures_to_spot_dce interface

1.12.39 fix: fix futures_gfex_warehouse_receipt interface

1.12.38 fix: fix futures_to_spot_dce interface

1.12.37 fix: fix futures_delivery_shfe interface

1.12.36 fix: fix bond_china_close_return interface

1.12.35 fix: fix article_epu_index interface

1.12.34 fix: fix repo_rate_hist interface

1.12.33 fix: fix futures_global_em interface

1.12.32 fix: fix energy_oil_hist interface

1.12.31 add: add futures_global_em interface

1.12.30 fix: fix futures_settlement_price_sgx interface

1.12.29 add: add stock_individual_spot_xq interface

1.12.28 fix: fix futures_foreign_commodity_realtime interface

1.12.27 fix: fix stock_hk_fhpx_detail_ths interface

1.12.26 fix: fix index_stock_info interface

1.12.25 fix: fix fund_individual_basic_info_xq interface

1.12.24 fix: fix stock_hk_index_spot_em interface

1.12.23 fix: fix fund_etf_hist_min_em interface

1.12.22 fix: fix stock_hsgt_board_rank_em interface

1.12.21 fix: fix stock_hsgt_hold_stock_em interface

1.12.20 fix: fix futures_inventory_99 interface

1.12.19 fix: fix stock_hk_profit_forecast_et interface

1.12.18 fix: fix stock_board_industry_index_ths interface

1.12.17 fix: fix option_current_em interface

1.12.16 fix: fix stock_hot_follow_xq interface

1.12.15 fix: fix stock_hk_profit_forecast_et interface

1.12.14 add: add stock_hk_profit_forecast_et interface

1.12.13 fix: fix index_stock_cons_csindex interface

1.12.12 fix: fix stock_zh_index_daily interface

1.12.11 add: add stock_zh_index_spot_em interface

1.12.10 fix: fix stock_add_stock interface

1.12.9 add: add fund_individual_basic_info_xq interface

1.12.8 fix: fix fund_open_fund_info_em interface

1.12.7 fix: fix option_gfex_daily interface

1.12.6 fix: fix fund_open_fund_info_em interface

1.12.5 fix: fix stock_zh_a_gdhs interface

1.12.4 fix: fix tool_trade_date_hist_sina interface

1.12.3 fix: fix stock_gdfx_free_holding_teamwork_em interface

1.12.2 fix: fix hurun_rank interface

1.12.1 fix: fix futures_comm_info interface

1.11.99 fix: fix stock_zh_index_spot interface

1.11.98 fix: fix stock_zh_a_disclosure_report_cninfo interface

1.11.97 add: add stock_zh_a_disclosure_report_cninfo interface

1.11.96 fix: fix fund_rating_all interface

1.11.95 fix: fix fund_etf_hist_min_em interface

1.11.94 fix: fix index_zh_a_hist_min_em interface

1.11.93 fix: fix stock_zh_a_hist_pre_min_em interface

1.11.92 fix: fix get_gfex_receipt interface

1.11.91 fix: remove stock_us_fundamental interface

1.11.90 fix: fix futures_rule interface

1.11.89 fix: fix bond_zh_us_rate interface

1.11.88 fix: fix futures_board_index_nh interface

1.11.87 fix: fix futures_board_index_nh interface

1.11.86 fix: fix stock_telegraph_cls interface

1.11.85 fix: fix stock_market_activity_legu interface

1.11.84 fix: fix fund_name_em interface

1.11.83 fix: fix stock_zt_pool_strong_em interface

1.11.82 fix: fix bond_zh_us_rate interface

1.11.81 fix: fix stock_gdfx_free_holding_detail_em interface

1.11.80 fix: fix stock_cash_flow_sheet_by_report_em interface

1.11.79 fix: fix get_receipt interface

1.11.78 add: add stock_financial_benefit_ths interface

1.11.77 fix: fix futures_zh_spot interface

1.11.76 fix: fix option_czce_daily interface

1.11.75 fix: fix futures_comex_inventory interface

1.11.74 fix: fix stock_comment_em interface

1.11.73 fix: fix futures_comex_inventory interface

1.11.72 fix: fix get_rank_sum_daily interface

1.11.71 fix: fix stock_balance_sheet_by_report_em interface

1.11.70 fix: fix futures_gfex_position_rank interface

1.11.69 add: add futures_gfex_position_rank interface

1.11.68 fix: fix fund_aum_em interface

1.11.67 fix: fix currency_boc_sina interface

1.11.66 fix: fix fund_scale_structured_sina interface

1.11.65 fix: fix futures_index_ccidx interface

1.11.64 fix: fix futures_settlement_price_sgx interface

1.11.63 fix: fix fund_scale_open_sina interface

1.11.62 fix: fix stock_zt_pool_dtgc_em interface

1.11.61 fix: fix fund_manager_em interface

1.11.60 fix: fix bond_china_close_return interface

1.11.59 fix: fix fund_portfolio_change_em interface

1.11.58 fix: fix bond_china_close_return interface

1.11.57 fix: fix stock_zt_pool_em interface

1.11.56 fix: fix stock_balance_sheet_by_report_delisted_em interface

1.11.55 fix: fix fund_portfolio_bond_hold_em interface

1.11.54 fix: fix fund_portfolio_hold_em interface

1.11.53 add: add stock_zh_a_hist_tx interface

1.11.52 fix: fix fund_scale_change_em interface

1.11.51 fix: fix stock_zh_a_daily interface

1.11.50 fix: fix amac_fund_abs support

1.11.49 add: add aarch64 support

1.11.48 fix: fix installation.md

1.11.47 add: add akracer 0.0.8 support

1.11.46 add: add akracer support

1.11.45 add: add stock_balance_sheet_by_report_delisted_em interface

1.11.44 add: add stock_cyq_em interface

1.11.43 fix: fix get_futures_daily interface

1.11.42 fix: fix stock_gpzy_pledge_ratio_em interface

1.11.41 fix: fix index_weibo_sina interface

1.11.40 fix: fix index_option_300etf_qvix interface

1.11.39 fix: fix index_option_50etf_qvix interface

1.11.38 fix: fix setup.py interface

1.11.37 fix: fix index_fear_greed_funddb interface

1.11.36 add: add stock_fear_greed_funddb interface

1.11.35 fix: fix stock_board_concept_hist_ths interface

1.11.34 add: add stock_board_concept_graph_ths interface

1.11.33 add: add stock_intraday_em interface

1.11.32 add: add stock_margin_ratio_pa interface

1.11.31 fix: fix futures_dce_warehouse_receipt interface

1.11.30 fix: fix stock_zh_a_st_em interface

1.11.29 fix: fix bond_new_composite_index_cbond interface

1.11.28 fix: fix stock_margin_detail_szse interface

1.11.27 fix: fix stock_margin_detail_szse interface

1.11.26 fix: fix macro_china_supply_of_money interface

1.11.25 fix: fix macro_china_central_bank_balance interface

1.11.24 fix: fix macro_china_postal_telecommunicational interface

1.11.23 fix: fix macro_china_society_traffic_volume interface

1.11.22 fix: fix option_dce_daily interface

1.11.21 fix: fix get_dce_daily interface

1.11.20 fix: fix option_dce_daily interface

1.11.19 fix: fix drewry_wci_index interface

1.11.18 fix: fix get_rank_sum_daily interface

1.11.17 fix: fix futures_spot_price_daily interface

1.11.16 fix: fix stock_dividend_cninfo interface

1.11.15 fix: fix stock_dividend_cninfo interface

1.11.14 fix: fix migration_area_baidu interface

1.11.13 fix: fix futures_comm_info interface

1.11.12 fix: fix stock_board_concept_hist_ths interface

1.11.11 fix: fix spot_hist_sge interface

1.11.10 fix: fix bond_new_composite_index_cbond interface

1.11.9 fix: fix currency_boc_safe interface

1.11.8 fix: fix news_economic_baidu interface

1.11.7 fix: fix get_futures_daily interface

1.11.6 fix: fix futures_main_sina interface

1.11.5 fix: fix macro_china_hk_cpi interface

1.11.4 fix: fix bond_cb_profile_sina interface

1.11.3 fix: fix stock_a_high_low_statistics interface

1.11.2 fix: fix stock_a_below_net_asset_statistics interface

1.11.1 add: add index_us_stock_sina interface

1.10.99 fix: fix crypto_bitcoin_cme interface

1.10.98 fix: fix get_cffex_rank_table interface

1.10.97 fix: fix stock_financial_analysis_indicator interface

1.10.96 fix: fix stock_hk_daily interface

1.10.95 fix: fix crypto_bitcoin_cme interface

1.10.94 add: add macro_china_nbs_nation interface

1.10.93 add: add stock_ipo_summary_cninfo interface

1.10.92 fix: fix stock_individual_fund_flow interface

1.10.91 fix: fix stock_share_hold_change_szse interface

1.10.90 fix: fix futures_comex_inventory interface

1.10.89 add: add stock_share_hold_change_bse interface

1.10.88 add: add stock_research_report_em interface

1.10.87 add: add stock_zdhtmx_em interface

1.10.86 add: add stock_gddh_em interface

1.10.85 fix: fix stock_hot_rank_wc interface

1.10.84 fix: fix stock_us_fundamental interface

1.10.83 add: add stock_industry_clf_hist_sw interface

1.10.82 fix: fix currency_boc_sina interface

1.10.81 fix: fix stock_bid_ask_em interface

1.10.80 fix: fix macro_china_gyzjz interface

1.10.79 add: add stock_hold_management_detail_em interface

1.10.78 fix: fix get_cffex_rank_table interface

1.10.77 add: add bond_cb_profile_sina interface

1.10.76 fix: fix stock_notice_report interface

1.10.75 add: add macro_china_urban_unemployment interface

1.10.74 add: add stock_sns_sseinfo interface

1.10.73 add: add stock_irm_cninfo interface

1.10.72 fix: fix stock_financial_hk_report_em interface

1.10.71 fix: fix stock_us_hist interface

1.10.70 fix: fix stock_zh_a_hist interface

1.10.69 fix: fix currency_latest interface

1.10.68 fix: fix option_gfex_daily interface

1.10.67 rem: rem futures_egg_price_yearly interface

1.10.66 fix: fix stock_financial_report_sina interface

1.10.65 fix: fix macro_china_lpr interface

1.10.64 fix: fix stock_zh_b_spot interface

1.10.63 fix: fix stock_esg_hz_sina interface

1.10.62 fix: fix index_hist_sw interface

1.10.61 fix: fix macro_cnbs interface

1.10.60 add: add macro_usa_cpi_yoy interface

1.10.59 add: add fund_announcement_personnel_em interface

1.10.58 fix: fix fund_etf_hist_em interface

1.10.57 fix: fix stock_zh_valuation_baidu interface

1.10.56 fix: fix stock_zh_b_daily interface

1.10.55 fix: fix macro_usa_personal_spending interface

1.10.54 fix: fix macro_usa_core_cpi_monthly interface

1.10.53 fix: fix index_stock_cons_csindex interface

1.10.52 fix: fix stock_financial_hk_report_em interface

1.10.51 fix: fix fund_money_rank_em interface

1.10.50 fix: fix car_energy_sale_cpca interface

1.10.49 fix: fix stock_hot_rank_em interface

1.10.48 add: add stock_esg_hz_sina interface

1.10.47 add: add stock_esg_rate_sina interface

1.10.46 fix: fix index_value_hist_funddb interface

1.10.45 fix: fix stock_zh_a_minute interface

1.10.44 fix: fix get_shfe_rank_table interface

1.10.43 rem: rem index_vix interface

1.10.42 fix: fix fund_rating_all interface

1.10.41 add: add fund_lof_hist_em interface

1.10.40 fix: fix futures_news_baidu interface

1.10.39 fix: fix stock_board_concept_hist_min_em interface

1.10.38 fix: fix stock_board_industry_hist_min_em interface

1.10.37 rem: rem index_stock_hist interface

1.10.36 fix: fix stock_sy_profile_em interface

1.10.35 add: add get_gfex_receipt interface

1.10.34 fix: fix futures_display_main_sina interface

1.10.33 fix: fix index_sugar_msweet interface

1.10.32 fix: fix get_cffex_daily interface

1.10.31 fix: fix zh_subscribe_exchange_symbol interface

1.10.30 fix: fix stock_info_sz_name_code interface

1.10.29 fix: fix stock_zh_index_daily_em interface

1.10.28 fix: fix stock_hot_up_em interface

1.10.27 fix: fix stock_hot_up_em interface

1.10.26 add: add stock_hot_up_em interface

1.10.25 fix: fix index_sugar_msweet interface

1.10.24 fix: fix stock_zh_a_daily interface

1.10.23 fix: fix index_kq_fz interface

1.10.22 fix: fix macro_china_cpi_monthly interface

1.10.21 fix: fix fund_report_stock_cninfo interface

1.10.20 fix: fix stock_new_gh_cninfo interface

1.10.19 fix: fix bond_treasure_issue_cninfo interface

1.10.18 fix: fix index_yw interface

1.10.17 fix: fix stock_allotment_cninfo interface

1.10.16 fix: fix bond_zh_hs_cov_min interface

1.10.15 fix: fix bond_zh_hs_cov_pre_min interface

1.10.14 fix: fix bond_zh_hs_cov_min interface

1.10.13 fix: fix stock_share_change_cninfo interface

1.10.12 fix: fix bond_cb_adj_logs_jsl interface

1.10.11 fix: fix stock_zh_a_hist_pre_min_em interface

1.10.10 fix: fix stock_zh_a_hist interface

1.10.9 fix: fix bond_zh_hs_cov_min interface

1.10.8 fix: fix futures_volatility_index_nh interface

1.10.7 fix: fix option_finance_board interface

1.10.6 fix: fix futures_nh_volatility_index interface

1.10.5 fix: fix index_level_one_hist_sw interface

1.10.4 fix: fix futures_return_index_nh interface

1.10.3 fix: fix stock_gdfx_holding_analyse_em interface

1.10.2 fix: fix stock_gdfx_holding_detail_em interface

1.10.1 fix: fix stock_hold_control_cninfo interface

1.9.99 fix: fix stock_hold_num_cninfo interface

1.9.98 fix: fix stock_hold_control_cninfo interface

1.9.97 fix: fix stock_industry_category_cninfo interface

1.9.96 fix: fix stock_hold_control_cninfo interface

1.9.95 fix: fix stock_zh_index_hist_csindex interface

1.9.94 fix: fix stock_a_indicator_lg interface

1.9.93 fix: fix index_level_one_hist_sw interface

1.9.92 fix: fix article_ff_crr interface

1.9.91 add: add stock_financial_abstract_ths interface

1.9.90 fix: fix stock_sse_deal_daily interface

1.9.89 fix: fix index_kq_fz interface

1.9.88 fix: fix setup.py

1.9.87 add: add option_minute_em interface

1.9.86 fix: fix index_kq_fz interface

1.9.85 fix: fix option_dce_daily interface

1.9.84 fix: fix stock_hk_fhpx_detail_ths interface

1.9.83 add: add stock_concept_fund_flow_hist interface

1.9.82 fix: fix currency_boc_safe interface

1.9.81 add: add stock_hk_index_spot_sina interface

1.9.80 fix: fix futures_spot_price interface

1.9.79 fix: fix stock_sse_deal_daily interface

1.9.78 fix: fix macro_usa_gdp_monthly interface

1.9.77 fix: fix stock_hot_rank_wc interface

1.9.76 fix: fix stock_sector_detail interface

1.9.75 fix: fix stock_board_industry_index_ths interface

1.9.74 fix: fix get_shfe_rank_table interface

1.9.73 add: add bond_zh_cov_info_ths interface

1.9.72 fix: fix fund_manager interface

1.9.71 fix: fix stock_lh_yyb_most interface

1.9.70 fix: fix stock_szse_sector_summary interface

1.9.69 fix: fix stock_lh_yyb_capital interface

1.9.68 fix: fix stock_lh_yyb_capital interface

1.9.67 fix: fix futures_zh_daily_sina interface

1.9.66 fix: fix match_main_contract interface

1.9.65 fix: fix stock_hot_search_baidu interface

1.9.64 fix: fix stock_a_indicator_lg interface

1.9.63 fix: fix get_czce_rank_table interface

1.9.62 fix: fix bond_zh_us_rate interface

1.9.61 fix: fix stock_lhb_detail_daily_sina interface

1.9.60 add: add stock_hk_fhpx_detail_ths interface

1.9.59 fix: fix stock_hot_search_baidu interface

1.9.58 add: add option_gfex_daily interface

1.9.57 fix: fix stock_lhb_detail_em interface

1.9.56 fix: fix get_receipt interface

1.9.55 fix: fix stock_zh_valuation_baidu interface

1.9.54 fix: fix stock_board_concept_cons_ths interface

1.9.53 fix: fix get_ine_daily interface

1.9.52 fix: fix get_shfe_rank_table interface

1.9.51 fix: fix get_shfe_daily interface

1.9.50 fix: fix stock_a_all_pb interface

1.9.49 add: add stock_lhb_yybph_em interface

1.9.48 fix: fix index_stock_cons interface

1.9.47 fix: fix option_dce_daily interface

1.9.46 fix: fix stock_a_gxl_lg interface

1.9.45 add: add stock_fhps_detail_ths interface

1.9.44 fix: fix stock_a_high_low_statistics interface

1.9.43 fix: fix stock_a_congestion_lg interface

1.9.42 add: add stock_bid_ask_em interface

1.9.41 fix: fix stock_a_indicator_lg interface

1.9.40 fix: fix stock_profit_forecast_em interface

1.9.39 fix: fix fund_stock_position_lg interface

1.9.38 fix: fix stock_a_lg_indicator interface

1.9.37 fix: fix stock_hk_indicator_eniu interface

1.9.36 fix: fix stock_market_pe_lg interface

1.9.35 fix: fix stock_a_lg_indicator interface

1.9.34 fix: fix stock_zh_a_tick_tx_js interface

1.9.33 add: add stock_hk_main_board_spot_em interface

1.9.32 fix: fix bank_fjcf_table_detail interface

1.9.31 fix: fix amac_fund_info interface

1.9.30 fix: fix stock_a_lg_indicator interface

1.9.29 fix: fix stock_a_lg_indicator interface

1.9.28 fix: fix stock_financial_report_sina interface

1.9.27 fix: fix fund_exchange_rank_em interface

1.9.26 fix: fix bond_cb_jsl interface

1.9.25 add: add stock_hk_hot_rank_em interface

1.9.24 fix: fix bond_cb_adj_logs_jsl interface

1.9.23 fix: fix bond_cb_redeem_jsl interface

1.9.22 fix: fix fund_hk_fund_hist_em interface

1.9.21 fix: fix fund_financial_fund_info_em interface

1.9.20 fix: fix fund_financial_fund_info_em interface

1.9.19 fix: fix macro_cnbs interface

1.9.18 fix: fix macro_china_market_margin_sh interface

1.9.17 add: add stock_board_industry_spot_em interface

1.9.16 fix: fix stock_financial_abstract interface

1.9.15 fix: fix stock_hk_daily interface

1.9.14 fix: fix option_risk_analysis_em interface

1.9.13 fix: fix stock_zh_valuation_baidu interface

1.9.12 fix: fix stock_hot_rank_wc interface

1.9.11 add: add stock_sector_fund_flow_hist interface

1.9.10 add: add macro_shipping_bcti interface

1.9.9 add: add macro_shipping_bci interface

1.9.8 fix: fix stock_hk_valuation_baidu interface

1.9.7 add: add stock_profit_forecast_ths interface

1.9.6 fix: fix futures_hog_info interface

1.9.5 fix: fix stock_info_a_code_name interface

1.9.4 fix: fix drewry_wci_index interface

1.9.3 fix: fix fx_quote_baidu interface

1.9.2 fix: fix stock_xgsglb_em interface

1.9.1 fix: fix index_value_name_funddb interface

1.8.99 add: add futures_news_shmet interface

1.8.98 fix: fix stock_info_sz_delist interface

1.8.97 fix: fix futures_egg_price_yearly interface

1.8.96 fix: fix option_finance_board interface

1.8.95 fix: fix index_zh_a_hist interface

1.8.94 fix: fix Dockerfile

1.8.93 fix: fix stock_gdfx_holding_detail_em interface

1.8.92 fix: fix stock_institute_hold interface

1.8.91 fix: fix sunrise_monthly interface

1.8.90 fix: fix bond_info_detail_cm interface

1.8.89 fix: fix sunrise_city_list interface

1.8.88 fix: fix stock_info_sz_delist interface

1.8.87 fix: fix stock_info_sz_change_name interface

1.8.86 fix: fix stock_info_sh_delist interface

1.8.85 fix: fix stock_info_sh_name_code interface

1.8.84 remove: remove stock_zh_a_scr_report interface

1.8.83 fix: fix stock_info_sh_name_code interface

1.8.82 fix: fix stock_fund_stock_holder interface

1.8.81 fix: fix futures_hog_info interface

1.8.80 fix: fix stock_profit_forecast interface

1.8.79 fix: fix stock_hk_valuation_baidu interface

1.8.78 fix: fix stock_profit_forecast interface

1.8.77 fix: fix stock_analyst_rank_em interface

1.8.76 remove: remove js_news and ws interface

1.8.75 add: add stock_cy_a_spot_em interface

1.8.74 fix: fix drewry_wci_index interface

1.8.73 add: add stock_zyjs_ths interface

1.8.72 fix: fix drewry_wci_index interface

1.8.71 add: add stock_zygc_em interface

1.8.70 add: add stock_market_pe_lg interface

1.8.69 fix: fix stock_individual_fund_flow_rank interface

1.8.68 fix: fix stock_individual_fund_flow interface

1.8.67 fix: fix python warning 3.7.x support

1.8.66 fix: fix python 3.7.x support

1.8.65 fix: fix get_roll_yield_bar interface

1.8.64 fix: fix stock_ggcg_em interface

1.8.63 fix: fix stock_cash_flow_sheet_by_report_em interface

1.8.62 fix: fix stock_board_industry_index_ths interface

1.8.61 fix: fix futures_comm_info interface

1.8.60 fix: fix hurun_rank interface

1.8.59 fix: fix stock_zh_valuation_baidu interface

1.8.58 fix: fix get_calendar interface

1.8.57 fix: fix stock_szse_summary interface

1.8.56 fix: fix stock_hk_valuation_baidu interface

1.8.55 fix: fix macro_usa_pmi interface

1.8.54 fix: fix get_roll_yield_bar interface

1.8.53 fix: fix stock_hot_rank_wc interface

1.8.52 fix: fix index_value_hist_funddb interface

1.8.51 fix: fix fortune_rank interface

1.8.50 fix: fix stock_us_daily interface

1.8.49 fix: fix futures_comm_info interface

1.8.48 add: add fund_etf_hist_em interface

1.8.47 add: add option_cffex_sz50_list_sina interface

1.8.46 fix: fix get_roll_yield_bar interface

1.8.45 fix: fix calendar.json

1.8.44 fix: fix stock_info_bj_name_code interface

1.8.43 add: add stock_ebs_lg interface

1.8.42 add: add get_gfex_daily interface

1.8.41 add: add futures_index_ccidx interface

1.8.40 add: add fund_balance_position_lg interface

1.8.39 add: add stock_board_change_em interface

1.8.38 fix: fix macro_cons_gold interface

1.8.37 add: add fund_stock_position_lg interface

1.8.36 add: add stock_a_congestion_lg interface

1.8.35 add: add stock_hk_gxl_lg interface

1.8.34 add: add stock_a_gxl_lg interface

1.8.33 fix: fix stock_hot_rank_em interface

1.8.32 fix: fix js_news interface

1.8.31 fix: fix get_dce_daily interface

1.8.30 fix: fix index_value_name_funddb interface

1.8.29 fix: fix baidu_search_index interface

1.8.28 fix: fix fund_fh_rank_em interface

1.8.27 fix: fix fund_cf_em interface

1.8.26 fix: fix bond_china_close_return_map interface

1.8.25 fix: fix stock_circulate_stock_holder interface

1.8.24 fix: fix stock_ipo_benefit_ths interface

1.8.23 add: add stock_restricted_release_summary_em interface

1.8.22 fix: fix stock_margin_detail_szse interface

1.8.21 fix: fix stock_board_concept_hist_em interface

1.8.20 fix: fix stock_board_concept_hist_em interface

1.8.19 fix: fix stock_balance_sheet_by_yearly_em interface

1.8.18 add: add stock_hsgt_fund_flow_summary_em interface

1.8.17 fix: fix macro_china_fdi interface

1.8.16 fix: fix macro_china_swap_rate interface

1.8.15 fix: fix stock_price_js interface

1.8.14 add: add stock_board_industry_summary_ths interface

1.8.13 fix: fix macro_china_new_house_price interface

1.8.12 fix: fix stock_yjyg_em interface

1.8.11 fix: fix macro_china_ppi interface

1.8.10 fix: fix stock_a_all_pb interface

1.8.9 fix: fix stock_a_ttm_lyr interface

1.8.8 fix: fix macro_china_gdp interface

1.8.7 fix: fix stock_a_below_net_asset_statistics interface

1.8.6 fix: fix stock_market_activity_legu interface

1.8.5 fix: fix stock_a_lg_indicator interface

1.8.4 fix: fix macro_china_hgjck interface

1.8.3 fix: fix stock_pg_em interface

1.8.2 fix: fix fund_portfolio_hold_em interface

1.8.1 fix: fix stock_dxsyl_em interface

1.7.99 fix: fix stock_lhb_detail_daily_sina interface

1.7.98 add: add stock_zh_a_gdhs interface

1.7.97 add: add index_hog_spot_price interface

1.7.96 fix: fix futures_hog_info interface

1.7.95 fix: fix spot_golden_benchmark_sge interface

1.7.94 fix: fix fund_portfolio_hold_em interface

1.7.93 fix: fix sw_index_third_cons interface

1.7.92 fix: fix fund_portfolio_hold_em interface

1.7.91 fix: fix futures_price_index_nh interface

1.7.90 fix: fix stock_yjbb_em interface

1.7.89 fix: fix stock_zh_index_daily_tx interface

1.7.88 fix: fix stock_news_em interface

1.7.87 fix: fix macro_uk interface

1.7.86 fix: fix bond_info_cm interface

1.7.85 fix: fix stock_board_industry_hist_em interface

1.7.84 add: add bond_info_cm interface

1.7.83 fix: fix macro_japan interface

1.7.82 fix: fix index_analysis_daily_sw interface

1.7.81 fix: fix macro_swiss_svme interface

1.7.80 fix: fix stock_a_below_net_asset_statistics interface

1.7.79 fix: fix macro_germany interface

1.7.78 add: add index_analysis_sw interface

1.7.77 fix: fix index_value_hist_funddb interface

1.7.76 fix: fix macro_euro_gdp_yoy interface

1.7.75 add: add index_component_sw interface

1.7.74 fix: fix futures_news_baidu interface

1.7.73 fix: fix stock_zh_index_daily_tx interface

1.7.72 add: add index_min_sw interface

1.7.71 add: add support for Python 3.11

1.7.70 fix: fix index_hist_sw interface

1.7.69 add: add index_hist_sw interface

1.7.68 fix: fix hurun_rank interface

1.7.67 fix: fix xincaifu_rank interface

1.7.66 add: add index_realtime_sw interface

1.7.65 fix: fix futures_rule interface

1.7.64 add: add option_50etf_min_qvix interface

1.7.63 add: add option_300etf_min_qvix interface

1.7.62 add: add option_300etf_qvix interface

1.7.61 add: add option_50etf_qvix interface

1.7.60 fix: fix stock_zh_a_spot_em interface

1.7.59 fix: fix stock_a_high_low_statistics interface

1.7.58 fix: fix bond_cb_redeem_jsl interface

1.7.57 fix: fix stock_a_high_low_statistics interface

1.7.56 fix: fix stock_buffett_index_lg interface

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
