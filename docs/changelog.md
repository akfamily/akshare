---
tocdepth: 2
---

# 更新日志

本页记录 1.20.x 的更新，按版本号倒序排列，每个版本有固定锚点，如 `changelog.html#v1-20-2`。更早的版本见{doc}`历史更新日志 <changelog_archive>`，锚点名不变，如 `changelog_archive.html#v1-18-95`。接口改名记录见文末的{ref}`接口更名一览表 <changelog-rename>`。

## 1.20.x

(v1-20-2)=
### 1.20.2 fix: fix stock_board_concept_name_em interface

1. stock_board_concept_name_em、stock_board_industry_name_em 新增“领涨股票-代码”字段，股票名称变更（如加去 ST）时可按代码关联
2. 两个接口改为按东方财富字段名映射列名，上游新增字段时不再报 Length mismatch

(v1-20-1)=
### 1.20.1 build: switch release to trusted publishing

1. 接口与代码无变化，可放心升级
2. PyPI 发布改用 Trusted Publishing，安装包附带 PEP 740 数字证明，可验证来自 akfamily/akshare 仓库
3. 发布 tag 由 release-vX.Y.Z 改为 vX.Y.Z，本版本对应 tag v1.20.1
4. 不再提供 Docker 镜像；需要 HTTP API 时请使用 `pip install aktools` 部署，详见 [HTTP API（AKTools）](https://akshare.akfamily.xyz/aktools.html)
5. 删除多余的 setup.py，打包配置统一由 pyproject.toml 提供

(v1-20-0)=
### 1.20.0 refactor!: reorganize subpackages by interface category

1. 重新整理 `akshare/` 目录，不兼容旧的模块路径：子包名与 `ak.search()` 的类目名一一对应，股票接口按数据字典的 9 个主题分到 `akshare/stock/` 下的子目录，文件名统一为“类目_主题_数据源.py”。`ak.接口名()` 与 `from akshare import 接口名` 的用法不受影响；按 `from akshare.子包.模块 import 接口名` 导入的代码需要按 [AKShare 1.20.0 模块路径迁移](https://akshare.akfamily.xyz/migration.html) 中的对照表修改
2. 拆分接口跨类目的 3 个模块：bond_china_money、macro_other、news_baidu
3. 删除从未对外导出的失效或未完成代码：futures_rule_em、stock_kcb_renewal、stock_kcb_detail_renewal，以及 3 个未被使用的常量文件
4. 新增 fortune_rank 接口：历年《财富》世界 500 强榜单（1996 年至今），各年份输出统一为固定的 9 列
5. `akshare/__init__.py` 不再保留版本历史（完整记录见本页），导入语句按类目分组，文件由 7077 行减为约 2500 行
6. 内置数据文件统一放到 `akshare/data/`，通过 `akshare/datasets.py` 加载

(changelog-rename)=
## 接口更名一览表

| AKShare 版本 | 旧接口名称                                  | 新接口名称                                  | 修改日期 |
| ------------ | ------------------------------------------- | ------------------------------------------- | -------- |
| 1.17.81      | get_czce_rank_table                         | get_rank_table_czce                         | 20251103 |
| 1.17.81      | futures_czce_warehouse_receipt              | futures_warehouse_receipt_czce              | 20251103 |
| 1.17.72      | futures_dce_warehouse_receipt               | futures_warehouse_receipt_dce               | 20251027 |
| 1.17.68      | option_gfex_vol_daily                       | option_vol_gfex                             | 20251017 |
| 1.17.68      | option_gfex_daily                           | option_hist_gfex                            | 20251017 |
| 1.17.68      | option_shfe_daily                           | option_hist_shfe                            | 20251017 |
| 1.17.68      | option_czce_daily                           | option_hist_czce                            | 20251017 |
| 1.17.68      | option_dce_daily                            | option_hist_dce                             | 20251017 |
| 1.17.68      | option_czce_hist                            | option_hist_yearly_czce                     | 20251017 |
| 1.16.29      | futures_global_em                           | futures_global_spot_em                      | 20250305 |
| 1.13.88      | index_cflp_volume                           | index_volume_cflp                           | 20240527 |
| 1.13.88      | index_cflp_price                            | index_price_cflp                            | 20240527 |
| 1.13.19      | car_gasgoo_sale_rank                        | car_sale_rank_gasgoo                        | 20240403 |
| 1.13.19      | car_energy_sale_cpca                        | car_market_fuel_cpca                        | 20240403 |
| 1.13.15      | car_market_cpca                             | car_market_total_cpca                       | 20240331 |
| 1.12.95      | futures_hog_rank                            | futures_hog_cost                            | 20240318 |
| 1.12.95      | futures_hog_info                            | futures_hog_core                            | 20240318 |
| 1.12.93      | get_bond_bank                               | bond_debt_nafmii                            | 20240316 |
| 1.12.91      | stock_telegraph_cls                         | stock_info_global_cls                       | 20240313 |
| 1.12.11      | stock_zh_index_spot                         | stock_zh_index_spot_sina                    | 20240104 |
| 1.11.64      | futures_sgx_daily                           | futures_settlement_price_sgx                | 20231108 |
| 1.11.61      | fund_manager                                | fund_manager_em                             | 20231105 |
| 1.11.41      | weibo_index                                 | index_weibo_sina                            | 20231020 |
| 1.11.39      | option_300etf_min_qvix                      | index_option_300etf_min_qvix                | 20231019 |
| 1.11.39      | option_300etf_qvix                          | index_option_300etf_qvix                    | 20231019 |
| 1.11.39      | option_50etf_min_qvix                       | index_option_50etf_min_qvix                 | 20231019 |
| 1.11.39      | option_50etf_qvix                           | index_option_50etf_qvix                     | 20231019 |
| 1.10.50      | car_cpca_energy_sale                        | car_energy_sale_cpca                        | 20230710 |
| 1.10.36      | stock_em_sy_hy_list                         | stock_sy_hy_em                              | 20230624 |
| 1.10.36      | stock_em_sy_list                            | stock_sy_em                                 | 20230624 |
| 1.10.36      | stock_em_sy_jz_list                         | stock_sy_jz_em                              | 20230624 |
| 1.10.36      | stock_em_sy_yq_list                         | stock_sy_yq_em                              | 20230624 |
| 1.10.36      | stock_em_sy_profile                         | stock_sy_profile_em                         | 20230624 |
| 1.10.8       | futures_nh_volatility_index                 | futures_volatility_index_nh                 | 20230606 |
| 1.9.37       | stock_hk_eniu_indicator                     | stock_hk_indicator_eniu                     | 20230404 |
| 1.9.27       | fund_em_hk_rank                             | fund_hk_rank_em                             | 20230330 |
| 1.9.27       | fund_em_lcx_rank                            | fund_lcx_rank_em                            | 20230330 |
| 1.9.27       | fund_em_money_rank                          | fund_money_rank_em                          | 20230330 |
| 1.9.27       | fund_em_exchange_rank                       | fund_exchange_rank_em                       | 20230330 |
| 1.9.7        | stock_profit_forecast                       | stock_profit_forecast_em                    | 20230330 |
| 1.8.38       | macro_cons_silver_amount                    | macro_cons_silver                           | 20221227 |
| 1.8.38       | macro_cons_silver_change                    | macro_cons_silver                           | 20221227 |
| 1.8.38       | macro_cons_silver_volume                    | macro_cons_silver                           | 20221227 |
| 1.8.38       | macro_cons_gold_amount                      | macro_cons_gold                             | 20221227 |
| 1.8.38       | macro_cons_gold_change                      | macro_cons_gold                             | 20221227 |
| 1.8.38       | macro_cons_gold_volume                      | macro_cons_gold                             | 20221227 |
| 1.8.23       | stock_restricted_shares                     | stock_restricted_release_queue_sina         | 20221122 |
| 1.8.3        | stock_em_qbzf                               | stock_qbzf_em                               | 20221122 |
| 1.8.3        | stock_em_pg                                 | stock_pg_em                                 | 20221122 |
| 1.7.99       | stock_sina_lhb_jgmx                         | stock_lhb_jgmx_sina                         | 20221119 |
| 1.7.99       | stock_sina_lhb_jgzz                         | stock_lhb_jgzz_sina                         | 20221119 |
| 1.7.99       | stock_sina_lhb_yytj                         | stock_lhb_yytj_sina                         | 20221119 |
| 1.7.99       | stock_sina_lhb_ggtj                         | stock_lhb_ggtj_sina                         | 20221119 |
| 1.7.99       | stock_sina_lhb_detail_daily                 | stock_lhb_detail_daily_sina                 | 20221119 |
| 1.7.82       | index_analysis_sw                           | index_analysis_daily_sw                     | 20220921 |
| 1.7.27       | stock_em_qsjy                               | stock_qsjy_em                               | 20220921 |
| 1.7.23       | futures_pig_info                            | futures_hog_info                            | 20220916 |
| 1.7.23       | futures_pig_rank                            | futures_hog_rank                            | 20220916 |
| 1.6.86       | stock_em_gpzy_distribute_statistics_company | stock_gpzy_distribute_statistics_company_em | 20220811 |
| 1.6.86       | stock_em_gpzy_distribute_statistics_bank    | stock_gpzy_distribute_statistics_bank_em    | 20220811 |
| 1.5.94       | bond_conv_adj_logs_jsl                      | bond_cb_adj_logs_jsl                        | 20220524 |
| 1.5.94       | bond_cov_jsl                                | bond_cb_jsl                                 | 20220524 |
| 1.5.53       | stock_em_xjll                               | stock_xjll_em                               | 20220501 |
| 1.5.53       | stock_em_lrb                                | stock_lrb_em                                | 20220501 |
| 1.5.53       | stock_em_zcfz                               | stock_zcfz_em                               | 20220501 |
| 1.5.52       | stock_em_ggcg                               | stock_ggcg_em                               | 20220501 |
| 1.5.48       | futures_nh_price_index                      | futures_price_index_nh                      | 20220428 |
| 1.5.48       | futures_nh_index_symbol_table               | futures_index_symbol_table_nh               | 20220428 |
| 1.5.48       | futures_nh_return_index                     | futures_return_index_nh                     | 20220428 |
| 1.5.46       | stock_em_yzxdr                              | stock_yzxdr_em                              | 20220427 |
| 1.5.34       | stock_em_gpzy_industry_data                 | stock_gpzy_industry_data_em                 | 20220420 |
| 1.5.26       | stock_em_comment                            | stock_comment_em                            | 20220415 |
| 1.5.25       | stock_em_analyst_detail                     | stock_analyst_detail_em                     | 20220415 |
| 1.5.25       | stock_em_analyst_rank                       | stock_analyst_rank_em                       | 20220415 |
| 1.5.18       | fund_em_open_fund_rank                      | fund_open_fund_rank_em                      | 20220414 |
| 1.5.12       | stock_em_gpzy_pledge_ratio_detail           | stock_gpzy_pledge_ratio_detail_em           | 20220410 |
| 1.5.10       | stock_em_gpzy_pledge_ratio                  | stock_gpzy_pledge_ratio_em                  | 20220410 |
| 1.5.10       | stock_em_gpzy_profile                       | stock_gpzy_profile_em                       | 20220410 |
| 1.4.88       | fund_em_new_found                           | fund_new_found_em                           | 20220323 |
| 1.4.86       | fund_em_aum_hist                            | fund_aum_hist_em                            | 20220322 |
| 1.4.86       | fund_em_aum_trend                           | fund_aum_trend_em                           | 20220322 |
| 1.4.86       | fund_em_aum                                 | fund_aum_em                                 | 20220322 |
