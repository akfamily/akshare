# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2025/9/13 16:00
Desc: 深圳证券交易所-期权子网-行情数据-当日合约
"""
from io import BytesIO

import pandas as pd
import requests


def option_current_day_szse() -> pd.DataFrame:
    """
    深圳证券交易所-期权子网-行情数据-当日合约
    https://www.sse.org.cn/option/quotation/contract/daycontract/index.html
    :return: 深圳期权当日合约
    :rtype: pandas.DataFrame
    """
    import warnings
    warnings.filterwarnings(action='ignore', message="Workbook contains no default style")
    url = "https://www.sse.org.cn/api/report/ShowReport"
    params = {
        "SHOWTYPE": "xlsx",
        "CATALOGID": "option_drhy",
        "TABKEY": "tab1",
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_excel(BytesIO(r.content))
    temp_df['序号'] = pd.to_numeric(temp_df['序号'], errors='coerce')
    temp_df['行权价'] = pd.to_numeric(temp_df['行权价'], errors='coerce')
    temp_df['合约单位'] = pd.to_numeric(temp_df['合约单位'], errors='coerce')
    temp_df['涨停价格'] = pd.to_numeric(temp_df['涨停价格'], errors='coerce')
    temp_df['跌停价格'] = pd.to_numeric(temp_df['跌停价格'], errors='coerce')
    temp_df['前结算价'] = pd.to_numeric(temp_df['前结算价'], errors='coerce')
    temp_df['合约总持仓'] = pd.to_numeric(temp_df['合约总持仓'], errors='coerce')
    temp_df['原行权价格'] = pd.to_numeric(temp_df['原行权价格'], errors='coerce')
    temp_df['原合约单位'] = pd.to_numeric(temp_df['原合约单位'], errors='coerce')
    temp_df['合约到期剩余交易天数'] = pd.to_numeric(temp_df['合约到期剩余交易天数'], errors='coerce')
    temp_df['合约到期剩余自然天数'] = pd.to_numeric(temp_df['合约到期剩余自然天数'], errors='coerce')
    temp_df['下次合约调整剩余交易天数'] = pd.to_numeric(temp_df['下次合约调整剩余交易天数'], errors='coerce')
    temp_df['下次合约调整剩余自然天数'] = pd.to_numeric(temp_df['下次合约调整剩余自然天数'], errors='coerce')
    temp_df['交易日期'] = pd.to_datetime(temp_df['交易日期'], errors='coerce').dt.date
    temp_df['最后交易日'] = pd.to_datetime(temp_df['最后交易日'], errors='coerce').dt.date
    temp_df['行权日'] = pd.to_datetime(temp_df['行权日'], errors='coerce').dt.date
    temp_df['到期日'] = pd.to_datetime(temp_df['到期日'], errors='coerce').dt.date
    temp_df['交收日'] = pd.to_datetime(temp_df['交收日'], errors='coerce').dt.date
    temp_df = temp_df[[
        '序号',
        '合约编码',
        '合约代码',
        '合约简称',
        '标的证券简称(代码)',
        '合约类型',
        '行权价',
        '合约单位',
        '最后交易日',
        '行权日',
        '到期日',
        '交收日',
        '新挂',
        '涨停价格',
        '跌停价格',
        '前结算价',
        '合约调整',
        '停牌',
        '合约总持仓',
        '挂牌原因',
        '原合约代码',
        '原合约简称',
        '原行权价格',
        '原合约单位',
        '合约到期剩余交易天数',
        '合约到期剩余自然天数',
        '下次合约调整剩余交易天数',
        '下次合约调整剩余自然天数',
        '交易日期',
    ]]
    return temp_df


if __name__ == "__main__":
    option_current_day_szse_df = option_current_day_szse()
    print(option_current_day_szse_df)
