# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/5/4 9:07
Desc: test
"""
import akshare


def test():
    print('测试及功能展示: ')

    # ----------------------------------------------------------------------
    print('\n' + '-' * 80 + '\n一个品种在时间轴上的展期收益率')
    df = akshare.get_roll_yield_bar(type_method='date', var='RB', start_day='20181206', end_day='20181210', plot=False)
    print(df)

    # ----------------------------------------------------------------------
    print('\n' + '-' * 80 + '\n一个品种在不同交割标的上的价格比较')
    df = akshare.get_roll_yield_bar(type_method='symbol', var='RB', date='20181210', plot=False)
    print(df)

    # ----------------------------------------------------------------------
    print('\n' + '-' * 80 + '\n多个品种在某天的展期收益率横截面比较')
    df = akshare.get_roll_yield_bar(type_method='var', date='20181210', plot=False)
    print(df)

    # ----------------------------------------------------------------------
    print('\n' + '-' * 80 + '\n特定两个标的的展期收益率')
    df = akshare.get_roll_yield(date='20181210', var='IF', symbol1='IF1812', symbol2='IF1901')
    print(df)

    # ----------------------------------------------------------------------
    print('\n' + '-' * 80 + '\n特定品种、特定时段的交易所注册仓单')
    df = akshare.get_receipt(start_day='20181207', end_day='20181210', vars_list=['CU', 'NI'])
    print(df)

    # ----------------------------------------------------------------------
    print('\n' + '-' * 80 + '\n特定日期的现货价格及基差')
    df = akshare.futures_spot_price('20181210')
    print(df)

    # ----------------------------------------------------------------------
    print('\n' + '-' * 80 + '\n特定品种、特定时段的现货价格及基差')
    df = akshare.futures_spot_price_daily(start_day='20181210', end_day='20181210', vars_list=['CU', 'RB'])
    print(df)

    # ----------------------------------------------------------------------
    print('\n' + '-' * 80 + '\n特定品种、特定时段的会员持仓排名求和')
    df = akshare.get_rank_sum_daily(start_day='20181210', end_day='20181210', vars_list=['IF', 'C'])
    print(df)

    # ----------------------------------------------------------------------
    print('\n' + '-' * 80 + '\n大商所会员持仓排名细节；郑商所、上期所、中金所分别改成get_czce_rank_table、get_shfe_rank_table、get_cffex_rank_table')
    df = akshare.get_dce_rank_table('20181210')
    print(df)

    # ----------------------------------------------------------------------
    print('\n' + '-' * 80 + '\n日线行情获取')
    df = akshare.get_futures_daily(start_date='20181210', end_date='20181210', market='DCE', index_bar=True)
    print(df)


if __name__ == '__main__':
    test()
