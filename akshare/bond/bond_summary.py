# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/1/6 12:55
Desc: 上登债券信息网-债券成交概览
http://bond.sse.com.cn/data/statistics/overview/turnover/
"""
from io import BytesIO

import pandas as pd
import requests


def bond_summary_sse(date: str = '20200104') -> pd.DataFrame:
    """
    上登债券信息网-债券成交概览
    http://bond.sse.com.cn/data/statistics/overview/turnover/
    :param date: 指定日期
    :type date: str
    :return: 债券成交概览
    :rtype: pandas.DataFrame
    """
    url = 'http://query.sse.com.cn/commonExcelDd.do'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://bond.sse.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    params = {
        'sqlId': 'COMMON_SSEBOND_SCSJ_SCTJ_SCGL_ZQCJGL_CX_L',
        'TRADE_DATE': f'{date[:4]}-{date[4:6]}-{date[6:]}',
    }
    r = requests.get(url, params=params, headers=headers)
    temp_df = pd.read_excel(BytesIO(r.content))
    temp_df.columns = [
        '债券类型',
        '当日成交笔数',
        '当日成交金额',
        '当年成交笔数',
        '当年成交金额',
        '数据日期',
    ]
    return temp_df


if __name__ == '__main__':
    bond_summary_sse_df = bond_summary_sse(date='20210104')
    print(bond_summary_sse_df)
