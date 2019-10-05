# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
contact: jindaxiang@163.com
desc: 从生意社网站采集大宗商品现货价格及相应基差数据, 目前数据从 20110104-至今
"""
import re
import time
import datetime
import warnings

import pandas as pd

from akshare.symbol_var import chinese_to_english
from akshare import cons
from akshare.requests_fun import pandas_read_html_link

calendar = cons.get_calendar()


def get_spot_price_daily(start_day=None, end_day=None, vars_list=cons.contract_symbols):
    """
    获取大宗商品现货价格及相应基差
    :param start_day: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象; 默认为当天
    :param end_day: 结束数据 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象; 默认为当天
    :param vars_list: 合约品种如 RB, AL 等列表; 为空时为所有商品
    :return: pd.DataFrame
    展期收益率数据(DataFrame):
        var             商品品种                     string
        sp              现货价格                     float
        near_symbol      临近交割合约                  string
        near_price       临近交割合约结算价             float
        dom_symbol       主力合约                     string
        dom_price        主力合约结算价                float
        near_basis       临近交割合约相对现货的基差      float
        dom_basis        主力合约相对现货的基差         float
        near_basis_rate   临近交割合约相对现货的基差率    float
        dom_basis_rate    主力合约相对现货的基差率       float
        date              日期                       string YYYYMMDD
    """
    start_day = cons.convert_date(start_day) if start_day is not None else datetime.date.today()
    end_day = cons.convert_date(end_day) if end_day is not None else cons.convert_date(
        cons.get_latest_data_date(datetime.datetime.now()))
    df_list = []
    while start_day <= end_day:
        print(start_day)
        temp_df = get_spot_price(start_day, vars_list)
        if temp_df is False:
            return pd.concat(df_list).reset_index(drop=True)
        elif temp_df is not None:
            df_list.append(temp_df)
        start_day += datetime.timedelta(days=1)
    if len(df_list) > 0:
        return pd.concat(df_list).reset_index(drop=True)


def get_spot_price(date=None, vars_list=cons.contract_symbols):
    """
    获取某一天大宗商品现货价格及相应基差
    :param date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :param vars_list: 合约品种如RB、AL等列表 为空时为所有商品
    :return: pd.DataFrame
    展期收益率数据(pd.DataFrame):
        var             商品品种                     string
        sp              现货价格                     float
        near_symbol      临近交割合约                  string
        near_price       临近交割合约结算价             float
        dom_symbol       主力合约                     string
        dom_price        主力合约结算价                float
        near_basis       临近交割合约相对现货的基差      float
        dom_basis        主力合约相对现货的基差         float
        near_basis_rate   临近交割合约相对现货的基差率    float
        dom_basis_rate    主力合约相对现货的基差率       float
        date              日期                       string YYYYMMDD
    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date < datetime.date(2011, 1, 4):
        raise Exception("数据源开始日期为 20110104, 请将获取数据时间点设置在 20110104 后")
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn(f"{date.strftime('%Y%m%d')}非交易日")
        return None
    u1 = cons.SYS_SPOT_PRICE_LATEST_URL
    u2 = cons.SYS_SPOT_PRICE_URL.format(date.strftime('%Y-%m-%d'))
    i = 1
    while True:
        for url in [u2, u1]:
            try:
                r = pandas_read_html_link(url)
                string = r[0].loc[1, 1]
                news = ''.join(re.findall(r'[0-9]', string))
                if news[3:11] == date.strftime('%Y%m%d'):
                    records = _check_information(r[1], date)
                    records.index = records['var']
                    var_list_in_market = [i for i in vars_list if i in records.index]
                    temp_df = records.loc[var_list_in_market, :]
                    temp_df.reset_index(drop=True)
                    temp_df.columns = ["var", "sp", "near_symbol", "near_price", "dom_symbol", "dom_price", "near_basis", "dom_basis", "near_basis_rate", "dom_basis_rate", "date"]
                    return temp_df
                else:
                    time.sleep(3)
            except IndexError as e:
                print(f"{date.strftime('%Y-%m-%d')}日生意社数据连接失败，第{str(i)}次尝试，最多5次", e)
                i += 1
                if i > 5:
                    print(f"{date.strftime('%Y-%m-%d')}日生意社数据连接失败，已超过5次，您的地址被网站墙了，请保存好返回数据，稍后从该日期起重试")
                    return False


def _check_information(df_data, date):
    if int(pd.__version__[2:4]) <= 23:
        df_data = df_data.loc[:, [0, 1, 2, 3, 7, 8]]
    else:
        df_data = df_data.loc[:, [0, 1, 2, 3, 5, 6]]
    df_data.columns = ['var', 'SP', 'nearSymbol', 'nearPrice', 'domSymbol', 'domPrice']
    records = pd.DataFrame()
    for string in df_data['var'].tolist():
        if string == 'PTA':
            news = 'PTA'
        else:
            news = ''.join(re.findall(r'[\u4e00-\u9fa5]', string))
        if news != '' and news not in ['商品', '价格', '上海期货交易所', '郑州商品交易所', '大连商品交易所']:
            var = chinese_to_english(news)
            record = pd.DataFrame(df_data[df_data['var'] == string])
            record.loc[:, 'var'] = var
            record.loc[:, 'SP'] = record.loc[:, 'SP'].astype(float)
            if var == 'JD':
                record.loc[:, 'SP'] = float(record['SP']) * 500
            if var == 'FG':
                record.loc[:, 'SP'] = record['SP'] * 80
            records = records.append(record)

    records.loc[:, ['nearPrice', 'domPrice', 'SP']] = records.loc[:, ['nearPrice', 'domPrice', 'SP']].astype(
        'float')

    records.loc[:, 'nearSymbol'] = records['nearSymbol'].replace(r'[^0-9]*(\d*)$', r'\g<1>', regex=True)
    records.loc[:, 'domSymbol'] = records['domSymbol'].replace(r'[^0-9]*(\d*)$', r'\g<1>', regex=True)

    records.loc[:, 'nearSymbol'] = records['var'] + records.loc[:, 'nearSymbol'].astype('int').astype('str')
    records.loc[:, 'domSymbol'] = records['var'] + records.loc[:, 'domSymbol'].astype('int').astype('str')

    records['nearSymbol'] = records['nearSymbol'].apply(
        lambda x: x.lower() if x[:-4] in cons.market_exchange_symbols['shfe'] + cons.market_exchange_symbols['dce'] else x)
    records.loc[:, 'domSymbol'] = records.loc[:, 'domSymbol'].apply(
        lambda x: x.lower() if x[:-4] in cons.market_exchange_symbols['shfe'] + cons.market_exchange_symbols['dce'] else x)
    records.loc[:, 'nearSymbol'] = records.loc[:, 'nearSymbol'].apply(
        lambda x: x[:-4] + x[-3:] if x[:-4] in cons.market_exchange_symbols['czce'] else x)
    records.loc[:, 'domSymbol'] = records.loc[:, 'domSymbol'].apply(
        lambda x: x[:-4] + x[-3:] if x[:-4] in cons.market_exchange_symbols['czce'] else x)

    records['nearBasis'] = records['nearPrice'] - records['SP']
    records['domBasis'] = records['domPrice'] - records['SP']
    records['nearBasisRate'] = records['nearPrice'] / records['SP'] - 1
    records['domBasisRate'] = records['domPrice'] / records['SP'] - 1
    records.loc[:, 'date'] = date.strftime('%Y%m%d')
    return records


if __name__ == '__main__':
    df = get_spot_price_daily(start_day='20181108', end_day='20181110')
    print(df)
    df = get_spot_price('20180910')
    print(df)
