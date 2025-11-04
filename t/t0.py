# -*- coding:utf-8 -*-

# Author: PeterWeyland
# CreateTime: 2025-10-17
# Description: simple introduction of the code
import akshare as ak
import pandas as pd

if __name__ == '__main__':
    pd.set_option('display.max_rows', None)  # 设置行数为无限制
    pd.set_option('display.max_columns', None)  # 设置列数为无限制
    pd.set_option('display.width', 1000)  # 设置列宽
    pd.set_option('display.colheader_justify', 'left')  # 设置列标题靠左

    fund_etf_hist_em_df = ak.fund_etf_hist_em(symbol="510180", period="daily", start_date="20071019",
                                              end_date="20071019", adjust="qfq")
    print(fund_etf_hist_em_df)
