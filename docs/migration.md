# 1.20.0 模块路径迁移

1.20.0 重新整理了 `akshare/` 下的目录：子包名与 `ak.search()` 的类目名一一对应，股票接口按数据字典的 9 个主题分到 `akshare/stock/` 下的子目录，文件名统一为“类目_主题_数据源.py”。接口函数名、参数和返回结果都没有变化。

```{warning}
本次改动不保留旧的模块路径。按 `from akshare.旧子包.旧模块 import 接口名` 导入的代码会报 `ModuleNotFoundError`，请按下表改为新路径。
```

## 是否受影响

- 通过 `import akshare as ak` 后调用 `ak.接口名()`：不受影响，无需修改。
- 通过 `from akshare import 接口名` 导入：不受影响。
- 通过 `from akshare.子包.模块 import 接口名` 导入：受影响，按下表修改；建议改为 `ak.接口名()`，以后再整理目录也不会受影响。

## 新的目录结构

| 子包 | 内容 |
|---|---|
| `akshare/stock/quote/`、`finance/`、`holder/`、`issue/`、`valuation/`、`flow/`、`board/`、`research/`、`other/` | 股票数据，与数据字典股票页面的 9 个主题一一对应 |
| `akshare/macro/` | 宏观数据，原 `akshare/economic/` |
| `akshare/alternative/` | 另类数据，原 `air/`、`movie/`、`fortune/`、`other/` 与 `news/news_cctv.py` |
| `akshare/research/`、`indicator/`、`migration/`、`high_freq/`、`calendar/` | 原 `article/`、`cal/`、`event/`、`hf/`、`tool/` |
| `akshare/futures/`、`fund/`、`fx/`、`interest_rate/` | 另外并入了原 `futures_derivative/`、`reits/`、`forex/`、`rate/` |

## 模块路径对照表

| 旧模块 | 新模块 |
|---|---|
| `akshare.air.air_hebei` | `akshare.alternative.alternative_air_hebei` |
| `akshare.air.air_zhenqi` | `akshare.alternative.alternative_air_zhenqi` |
| `akshare.air.sunrise_tad` | `akshare.alternative.alternative_sunrise_tad` |
| `akshare.article.cons` | `akshare.research.cons` |
| `akshare.article.epu_index` | `akshare.research.research_epu_index` |
| `akshare.article.ff_factor` | `akshare.research.research_ff_factor` |
| `akshare.article.fred_md` | `akshare.research.research_fred_md` |
| `akshare.article.risk_rv` | `akshare.research.research_risk_rv` |
| `akshare.cal.rv` | `akshare.indicator.indicator_rv` |
| `akshare.currency.currency_china_bank_sina` | `akshare.fx.fx_china_bank_sina` |
| `akshare.currency.currency_safe` | `akshare.fx.fx_safe` |
| `akshare.economic.cons` | `akshare.macro.cons` |
| `akshare.economic.macro_australia` | `akshare.macro.macro_australia` |
| `akshare.economic.macro_bank` | `akshare.interest_rate.interest_rate_central_bank` |
| `akshare.economic.macro_canada` | `akshare.macro.macro_canada` |
| `akshare.economic.macro_china` | `akshare.macro.macro_china` |
| `akshare.economic.macro_china_hk` | `akshare.macro.macro_china_hk` |
| `akshare.economic.macro_china_nbs` | `akshare.macro.macro_china_nbs` |
| `akshare.economic.macro_constitute` | `akshare.macro.macro_constitute` |
| `akshare.economic.macro_euro` | `akshare.macro.macro_euro` |
| `akshare.economic.macro_finance_ths` | `akshare.macro.macro_finance_ths` |
| `akshare.economic.macro_germany` | `akshare.macro.macro_germany` |
| `akshare.economic.macro_info_ws` | `akshare.macro.macro_info_ws` |
| `akshare.economic.macro_japan` | `akshare.macro.macro_japan` |
| `akshare.economic.macro_swiss` | `akshare.macro.macro_swiss` |
| `akshare.economic.macro_uk` | `akshare.macro.macro_uk` |
| `akshare.economic.macro_usa` | `akshare.macro.macro_usa` |
| `akshare.economic.marco_cnbs` | `akshare.macro.macro_cnbs` |
| `akshare.event.cons` | `akshare.migration.cons` |
| `akshare.event.migration` | `akshare.migration.migration_baidu` |
| `akshare.forex.cons` | `akshare.fx.cons_forex` |
| `akshare.forex.forex_em` | `akshare.fx.fx_forex_em` |
| `akshare.fortune.fortune_500` | `akshare.alternative.alternative_fortune_500` |
| `akshare.fortune.fortune_bloomberg` | `akshare.alternative.alternative_fortune_bloomberg` |
| `akshare.fortune.fortune_forbes_500` | `akshare.alternative.alternative_fortune_forbes_500` |
| `akshare.fortune.fortune_hurun` | `akshare.alternative.alternative_fortune_hurun` |
| `akshare.fortune.fortune_xincaifu_500` | `akshare.alternative.alternative_fortune_xincaifu_500` |
| `akshare.futures.cot` | `akshare.futures.futures_cot` |
| `akshare.futures.receipt` | `akshare.futures.futures_receipt` |
| `akshare.futures_derivative.futures_contract_info_cffex` | `akshare.futures.futures_contract_info_cffex` |
| `akshare.futures_derivative.futures_contract_info_czce` | `akshare.futures.futures_contract_info_czce` |
| `akshare.futures_derivative.futures_contract_info_dce` | `akshare.futures.futures_contract_info_dce` |
| `akshare.futures_derivative.futures_contract_info_gfex` | `akshare.futures.futures_contract_info_gfex` |
| `akshare.futures_derivative.futures_contract_info_ine` | `akshare.futures.futures_contract_info_ine` |
| `akshare.futures_derivative.futures_contract_info_shfe` | `akshare.futures.futures_contract_info_shfe` |
| `akshare.futures_derivative.futures_cot_sina` | `akshare.futures.futures_cot_sina` |
| `akshare.futures_derivative.futures_hog` | `akshare.futures.futures_hog` |
| `akshare.futures_derivative.futures_index_sina` | `akshare.futures.futures_index_sina` |
| `akshare.futures_derivative.futures_spot_sys` | `akshare.futures.futures_spot_sys` |
| `akshare.fx.currency_investing` | `akshare.fx.fx_currency_investing` |
| `akshare.hf.hf_sp500` | `akshare.high_freq.high_freq_sp500` |
| `akshare.index.index_hog` | `akshare.futures.futures_hog_index` |
| `akshare.interest_rate.interbank_rate_em` | `akshare.interest_rate.interest_rate_interbank_em` |
| `akshare.movie.artist_yien` | `akshare.alternative.alternative_artist_yien` |
| `akshare.movie.movie_yien` | `akshare.alternative.alternative_movie_yien` |
| `akshare.movie.video_yien` | `akshare.alternative.alternative_video_yien` |
| `akshare.news.news_cctv` | `akshare.alternative.alternative_news_cctv` |
| `akshare.news.news_stock` | `akshare.stock.research.stock_news_stock` |
| `akshare.other.other_car_cpca` | `akshare.alternative.alternative_car_cpca` |
| `akshare.other.other_car_gasgoo` | `akshare.alternative.alternative_car_gasgoo` |
| `akshare.other.other_taptap` | `akshare.alternative.alternative_taptap` |
| `akshare.rate.repo_rate` | `akshare.interest_rate.interest_rate_repo` |
| `akshare.reits.reits_basic` | `akshare.fund.fund_reits` |
| `akshare.stock.stock_allotment_cninfo` | `akshare.stock.finance.stock_allotment_cninfo` |
| `akshare.stock.stock_ask_bid_em` | `akshare.stock.quote.stock_ask_bid_em` |
| `akshare.stock.stock_board_concept_em` | `akshare.stock.board.stock_board_concept_em` |
| `akshare.stock.stock_board_industry_em` | `akshare.stock.board.stock_board_industry_em` |
| `akshare.stock.stock_cg_equity_mortgage` | `akshare.stock.research.stock_cg_equity_mortgage` |
| `akshare.stock.stock_cg_guarantee` | `akshare.stock.research.stock_cg_guarantee` |
| `akshare.stock.stock_cg_lawsuit` | `akshare.stock.research.stock_cg_lawsuit` |
| `akshare.stock.stock_dividend_cninfo` | `akshare.stock.issue.stock_dividend_cninfo` |
| `akshare.stock.stock_dzjy_em` | `akshare.stock.flow.stock_dzjy_em` |
| `akshare.stock.stock_fund_em` | `akshare.stock.flow.stock_fund_em` |
| `akshare.stock.stock_fund_hold` | `akshare.stock.holder.stock_fund_hold` |
| `akshare.stock.stock_gsrl_em` | `akshare.stock.issue.stock_gsrl_em` |
| `akshare.stock.stock_hk_comparison_em` | `akshare.stock.quote.stock_hk_comparison_em` |
| `akshare.stock.stock_hk_famous` | `akshare.stock.quote.stock_hk_famous` |
| `akshare.stock.stock_hk_fhpx_ths` | `akshare.stock.issue.stock_hk_fhpx_ths` |
| `akshare.stock.stock_hk_hot_rank_em` | `akshare.stock.board.stock_hk_hot_rank_em` |
| `akshare.stock.stock_hk_sina` | `akshare.stock.quote.stock_hk_sina` |
| `akshare.stock.stock_hold_control_cninfo` | `akshare.stock.research.stock_hold_control_cninfo` |
| `akshare.stock.stock_hold_control_em` | `akshare.stock.research.stock_hold_control_em` |
| `akshare.stock.stock_hold_num_cninfo` | `akshare.stock.research.stock_hold_num_cninfo` |
| `akshare.stock.stock_hot_rank_em` | `akshare.stock.board.stock_hot_rank_em` |
| `akshare.stock.stock_hot_search_baidu` | `akshare.stock.board.stock_hot_search_baidu` |
| `akshare.stock.stock_hot_up_em` | `akshare.stock.board.stock_hot_up_em` |
| `akshare.stock.stock_hsgt_em` | `akshare.stock.quote.stock_hsgt_spot_em` |
| `akshare.stock.stock_industry` | `akshare.stock.board.stock_industry` |
| `akshare.stock.stock_industry_cninfo` | `akshare.stock.finance.stock_industry_cninfo` |
| `akshare.stock.stock_industry_pe_cninfo` | `akshare.stock.research.stock_industry_pe_cninfo` |
| `akshare.stock.stock_industry_sw` | `akshare.stock.research.stock_industry_sw` |
| `akshare.stock.stock_info` | `akshare.stock.issue.stock_info` |
| `akshare.stock.stock_info_em` | `akshare.stock.quote.stock_info_em` |
| `akshare.stock.stock_intraday_em` | `akshare.stock.quote.stock_intraday_em` |
| `akshare.stock.stock_intraday_sina` | `akshare.stock.quote.stock_intraday_sina` |
| `akshare.stock.stock_ipo_summary_cninfo` | `akshare.stock.finance.stock_ipo_summary_cninfo` |
| `akshare.stock.stock_new_cninfo` | `akshare.stock.research.stock_new_cninfo` |
| `akshare.stock.stock_news_cx` | `akshare.stock.research.stock_news_cx` |
| `akshare.stock.stock_profile_cninfo` | `akshare.stock.finance.stock_profile_cninfo` |
| `akshare.stock.stock_profile_em` | `akshare.stock.quote.stock_profile_em` |
| `akshare.stock.stock_rank_forecast` | `akshare.stock.research.stock_rank_forecast` |
| `akshare.stock.stock_repurchase_em` | `akshare.stock.issue.stock_repurchase_em` |
| `akshare.stock.stock_share_changes_cninfo` | `akshare.stock.finance.stock_share_changes_cninfo` |
| `akshare.stock.stock_share_hold` | `akshare.stock.research.stock_share_hold` |
| `akshare.stock.stock_stop` | `akshare.stock.issue.stock_stop` |
| `akshare.stock.stock_summary` | `akshare.stock.quote.stock_summary` |
| `akshare.stock.stock_us_famous` | `akshare.stock.quote.stock_us_famous` |
| `akshare.stock.stock_us_js` | `akshare.stock.research.stock_us_js` |
| `akshare.stock.stock_us_pink` | `akshare.stock.quote.stock_us_pink` |
| `akshare.stock.stock_us_sina` | `akshare.stock.quote.stock_us_sina` |
| `akshare.stock.stock_weibo_nlp` | `akshare.alternative.alternative_weibo_nlp` |
| `akshare.stock.stock_xq` | `akshare.stock.quote.stock_xq` |
| `akshare.stock.stock_zh_a_sina` | `akshare.stock.quote.stock_zh_a_sina` |
| `akshare.stock.stock_zh_a_special` | `akshare.stock.quote.stock_zh_a_special` |
| `akshare.stock.stock_zh_a_tick_tx` | `akshare.stock.quote.stock_zh_a_tick_tx` |
| `akshare.stock.stock_zh_a_tx` | `akshare.stock.quote.stock_zh_a_tx` |
| `akshare.stock.stock_zh_ah_tx` | `akshare.stock.quote.stock_zh_ah_tx` |
| `akshare.stock.stock_zh_b_sina` | `akshare.stock.quote.stock_zh_b_sina` |
| `akshare.stock.stock_zh_comparison_em` | `akshare.stock.quote.stock_zh_comparison_em` |
| `akshare.stock.stock_zh_kcb_report` | `akshare.stock.quote.stock_zh_kcb_report` |
| `akshare.stock.stock_zh_kcb_sina` | `akshare.stock.quote.stock_zh_kcb_sina` |
| `akshare.stock_feature.stock_a_below_net_asset_statistics` | `akshare.stock.valuation.stock_a_below_net_asset_statistics` |
| `akshare.stock_feature.stock_a_high_low` | `akshare.stock.valuation.stock_a_high_low` |
| `akshare.stock_feature.stock_a_indicator` | `akshare.stock.valuation.stock_a_indicator` |
| `akshare.stock_feature.stock_a_pe_and_pb` | `akshare.stock.valuation.stock_a_pe_and_pb` |
| `akshare.stock_feature.stock_account_em` | `akshare.stock.flow.stock_account_em` |
| `akshare.stock_feature.stock_all_pb` | `akshare.stock.valuation.stock_all_pb` |
| `akshare.stock_feature.stock_analyst_em` | `akshare.stock.research.stock_analyst_em` |
| `akshare.stock_feature.stock_board_concept_ths` | `akshare.stock.board.stock_board_concept_ths` |
| `akshare.stock_feature.stock_board_industry_ths` | `akshare.stock.board.stock_board_industry_ths` |
| `akshare.stock_feature.stock_buffett_index_lg` | `akshare.stock.valuation.stock_buffett_index_lg` |
| `akshare.stock_feature.stock_classify_sina` | `akshare.stock.board.stock_classify_sina` |
| `akshare.stock_feature.stock_comment_em` | `akshare.stock.board.stock_comment_em` |
| `akshare.stock_feature.stock_concept_futu` | `akshare.stock.board.stock_concept_futu` |
| `akshare.stock_feature.stock_congestion_lg` | `akshare.stock.valuation.stock_congestion_lg` |
| `akshare.stock_feature.stock_cyq_em` | `akshare.stock.flow.stock_cyq_em` |
| `akshare.stock_feature.stock_disclosure_cninfo` | `akshare.stock.finance.stock_disclosure_cninfo` |
| `akshare.stock_feature.stock_dxsyl_em` | `akshare.stock.issue.stock_dxsyl_em` |
| `akshare.stock_feature.stock_ebs_lg` | `akshare.stock.valuation.stock_ebs_lg` |
| `akshare.stock_feature.stock_esg_sina` | `akshare.stock.other.stock_esg_sina` |
| `akshare.stock_feature.stock_fhps_em` | `akshare.stock.issue.stock_fhps_em` |
| `akshare.stock_feature.stock_fhps_ths` | `akshare.stock.issue.stock_fhps_ths` |
| `akshare.stock_feature.stock_fund_flow` | `akshare.stock.flow.stock_fund_flow` |
| `akshare.stock_feature.stock_gddh_em` | `akshare.stock.holder.stock_gddh_em` |
| `akshare.stock_feature.stock_gdfx_em` | `akshare.stock.holder.stock_gdfx_em` |
| `akshare.stock_feature.stock_gdhs` | `akshare.stock.holder.stock_gdhs` |
| `akshare.stock_feature.stock_gdzjc_em` | `akshare.stock.holder.stock_gdzjc_em` |
| `akshare.stock_feature.stock_gpzy_em` | `akshare.stock.holder.stock_gpzy_em` |
| `akshare.stock_feature.stock_gxl_lg` | `akshare.stock.valuation.stock_gxl_lg` |
| `akshare.stock_feature.stock_hist_em` | `akshare.stock.quote.stock_hist_em` |
| `akshare.stock_feature.stock_hist_tx` | `akshare.stock.quote.stock_hist_tx` |
| `akshare.stock_feature.stock_hk_valuation_baidu` | `akshare.stock.valuation.stock_hk_valuation_baidu` |
| `akshare.stock_feature.stock_hot_xq` | `akshare.stock.board.stock_hot_xq` |
| `akshare.stock_feature.stock_hsgt_em` | `akshare.stock.flow.stock_hsgt_em` |
| `akshare.stock_feature.stock_hsgt_exchange_rate` | `akshare.stock.flow.stock_hsgt_exchange_rate` |
| `akshare.stock_feature.stock_hsgt_min_em` | `akshare.stock.flow.stock_hsgt_min_em` |
| `akshare.stock_feature.stock_info` | `akshare.stock.research.stock_info` |
| `akshare.stock_feature.stock_inner_trade_xq` | `akshare.stock.board.stock_inner_trade_xq` |
| `akshare.stock_feature.stock_irm_cninfo` | `akshare.stock.board.stock_irm_cninfo` |
| `akshare.stock_feature.stock_jgdy_em` | `akshare.stock.holder.stock_jgdy_em` |
| `akshare.stock_feature.stock_lh_yybpm` | `akshare.stock.flow.stock_lh_yybpm` |
| `akshare.stock_feature.stock_lhb_em` | `akshare.stock.flow.stock_lhb_em` |
| `akshare.stock_feature.stock_lhb_sina` | `akshare.stock.flow.stock_lhb_sina` |
| `akshare.stock_feature.stock_margin_bse` | `akshare.stock.flow.stock_margin_bse` |
| `akshare.stock_feature.stock_margin_em` | `akshare.stock.flow.stock_margin_em` |
| `akshare.stock_feature.stock_margin_sse` | `akshare.stock.flow.stock_margin_sse` |
| `akshare.stock_feature.stock_margin_szse` | `akshare.stock.flow.stock_margin_szse` |
| `akshare.stock_feature.stock_market_legu` | `akshare.stock.valuation.stock_market_legu` |
| `akshare.stock_feature.stock_pankou_em` | `akshare.stock.board.stock_pankou_em` |
| `akshare.stock_feature.stock_qsjy_em` | `akshare.stock.research.stock_qsjy_em` |
| `akshare.stock_feature.stock_report_em` | `akshare.stock.finance.stock_report_em` |
| `akshare.stock_feature.stock_research_report_em` | `akshare.stock.research.stock_research_report_em` |
| `akshare.stock_feature.stock_sns_sseinfo` | `akshare.stock.board.stock_sns_sseinfo` |
| `akshare.stock_feature.stock_sy_em` | `akshare.stock.finance.stock_sy_em` |
| `akshare.stock_feature.stock_technology_ths` | `akshare.stock.other.stock_technology_ths` |
| `akshare.stock_feature.stock_tfp_em` | `akshare.stock.issue.stock_tfp_em` |
| `akshare.stock_feature.stock_three_report_em` | `akshare.stock.finance.stock_three_report_em` |
| `akshare.stock_feature.stock_ttm_lyr` | `akshare.stock.valuation.stock_ttm_lyr` |
| `akshare.stock_feature.stock_us_valuation_baidu` | `akshare.stock.valuation.stock_us_valuation_baidu` |
| `akshare.stock_feature.stock_value_em` | `akshare.stock.valuation.stock_value_em` |
| `akshare.stock_feature.stock_yjbb_em` | `akshare.stock.finance.stock_yjbb_em` |
| `akshare.stock_feature.stock_yjyg_cninfo` | `akshare.stock.finance.stock_yjyg_cninfo` |
| `akshare.stock_feature.stock_yjyg_em` | `akshare.stock.finance.stock_yjyg_em` |
| `akshare.stock_feature.stock_yzxdr_em` | `akshare.stock.holder.stock_yzxdr_em` |
| `akshare.stock_feature.stock_zdhtmx_em` | `akshare.stock.research.stock_zdhtmx_em` |
| `akshare.stock_feature.stock_zf_pg` | `akshare.stock.issue.stock_zf_pg` |
| `akshare.stock_feature.stock_zh_valuation_baidu` | `akshare.stock.valuation.stock_zh_valuation_baidu` |
| `akshare.stock_feature.stock_zh_vote_baidu` | `akshare.stock.valuation.stock_zh_vote_baidu` |
| `akshare.stock_feature.stock_ztb_em` | `akshare.stock.quote.stock_ztb_em` |
| `akshare.stock_fundamental.stock_basic_info_xq` | `akshare.stock.quote.stock_basic_info_xq` |
| `akshare.stock_fundamental.stock_finance_hk_em` | `akshare.stock.finance.stock_finance_hk_em` |
| `akshare.stock_fundamental.stock_finance_sina` | `akshare.stock.issue.stock_finance_sina` |
| `akshare.stock_fundamental.stock_finance_ths` | `akshare.stock.finance.stock_finance_ths` |
| `akshare.stock_fundamental.stock_finance_us_em` | `akshare.stock.finance.stock_finance_us_em` |
| `akshare.stock_fundamental.stock_gbjg_em` | `akshare.stock.finance.stock_gbjg_em` |
| `akshare.stock_fundamental.stock_hold` | `akshare.stock.holder.stock_hold` |
| `akshare.stock_fundamental.stock_ipo_declare` | `akshare.stock.issue.stock_ipo_declare` |
| `akshare.stock_fundamental.stock_ipo_review` | `akshare.stock.issue.stock_ipo_review` |
| `akshare.stock_fundamental.stock_ipo_ths` | `akshare.stock.issue.stock_ipo_ths` |
| `akshare.stock_fundamental.stock_ipo_tutor` | `akshare.stock.issue.stock_ipo_tutor` |
| `akshare.stock_fundamental.stock_notice` | `akshare.stock.research.stock_notice` |
| `akshare.stock_fundamental.stock_profit_forecast_em` | `akshare.stock.research.stock_profit_forecast_em` |
| `akshare.stock_fundamental.stock_profit_forecast_hk_etnet` | `akshare.stock.research.stock_profit_forecast_hk_etnet` |
| `akshare.stock_fundamental.stock_profit_forecast_ths` | `akshare.stock.research.stock_profit_forecast_ths` |
| `akshare.stock_fundamental.stock_recommend` | `akshare.stock.research.stock_recommend` |
| `akshare.stock_fundamental.stock_register_em` | `akshare.stock.issue.stock_register_em` |
| `akshare.stock_fundamental.stock_restricted_em` | `akshare.stock.issue.stock_restricted_em` |
| `akshare.stock_fundamental.stock_zygc` | `akshare.stock.finance.stock_zygc` |
| `akshare.stock_fundamental.stock_zyjs_ths` | `akshare.stock.finance.stock_zyjs_ths` |
| `akshare.tool.trade_date_hist` | `akshare.calendar.calendar_trade_date_hist` |

## 拆分的模块

以下模块中的接口属于不同类目，已按接口拆分：

| 旧模块 | 接口 | 新模块 |
|---|---|---|
| `akshare.bond.bond_china_money` | macro_china_swap_rate、macro_china_bond_public | `akshare.macro.macro_china_money` |
| `akshare.economic.macro_other` | crypto_js_spot | `akshare.crypto.crypto_js_spot` |
| `akshare.economic.macro_other` | macro_fx_sentiment | `akshare.fx.fx_sentiment_jin10` |
| `akshare.news.news_baidu` | news_economic_baidu | `akshare.macro.macro_news_baidu` |
| `akshare.news.news_baidu` | news_trade_notify_suspend_baidu、news_trade_notify_dividend_baidu、news_report_time_baidu | `akshare.stock.issue.stock_news_baidu` |

`akshare.bond.bond_china_money` 中的 bond_china_close_return、bond_china_close_return_map 保留在原模块。

## 删除的模块

- `akshare.futures.futures_rule_em`：东方财富已下线该数据接口，且从未对外导出。
- `akshare.stock_fundamental.stock_kcb_sse`、`akshare.stock_fundamental.stock_kcb_detail_sse`：未完成的代码，从未对外导出；同类数据请使用 `ak.stock_register_kcb()`。
- `akshare.air.cons`、`akshare.futures_derivative.cons`、`akshare.stock_feature.cons`：未被任何代码使用的常量文件。
- `akshare/file_fold/`：其中的 calendar.json 已移到 `akshare/data/`，与其他内置数据文件放在一起。
