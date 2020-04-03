# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
update: 2020/3/17 13:06
contact: jindaxiang@163.com
desc: 从大连商品交易所、上海期货交易所、郑州商品交易所、中国金融期货交易所采集前 20 会员持仓数据;
建议下午 16:30 以后采集当天数据, 避免交易所数据更新不稳定;
郑州商品交易所格式分为三类
"""
import datetime
import json
import re
import warnings
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.futures import cons
from akshare.futures.requests_fun import (
    requests_link
)
from akshare.futures.symbol_var import chinese_to_english, find_chinese
from akshare.futures.symbol_var import (
    symbol_varieties
)

calendar = cons.get_calendar()
rank_columns = ['vol_party_name', 'vol', 'vol_chg', 'long_party_name', 'long_open_interest',
                'long_open_interest_chg', 'short_party_name', 'short_open_interest', 'short_open_interest_chg']
intColumns = ['vol', 'vol_chg', 'long_open_interest', 'long_open_interest_chg', 'short_open_interest',
              'short_open_interest_chg']


def get_rank_sum_daily(start_day=None, end_day=None, vars_list=cons.contract_symbols):
    """
    采集四个期货交易所前5、前10、前15、前20会员持仓排名数据
    注1：由于上期所和中金所只公布每个品种内部的标的排名，没有公布品种的总排名;
        所以函数输出的品种排名是由品种中的每个标的加总获得，并不是真实的品种排名列表
    注2：大商所只公布了品种排名，未公布标的排名
    :param start_day: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :param end_day: 结束数据 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :param vars_list: 合约品种如RB、AL等列表 为空时为所有商品
    :return: pd.DataFrame
    展期收益率数据(DataFrame):
    symbol                           标的合约                     string
    var                              商品品种                     string
    vol_top5                         成交量前5会员成交量总和         int
    vol_chg_top5                     成交量前5会员成交量变化总和      int
    long_open_interest_top5          持多单前5会员持多单总和         int
    long_open_interest_chg_top5      持多单前5会员持多单变化总和      int
    short_open_interest_top5         持空单前5会员持空单总和         int
    short_open_interest_chg_top5     持空单前5会员持空单变化总和      int
    vol_top10                        成交量前10会员成交量总和        int
    ...
    date                             日期                         string YYYYMMDD
    """
    start_day = cons.convert_date(start_day) if start_day is not None else datetime.date.today()
    end_day = cons.convert_date(end_day) if end_day is not None else cons.convert_date(
        cons.get_latest_data_date(datetime.datetime.now()))
    records = pd.DataFrame()
    while start_day <= end_day:
        print(start_day)
        if start_day.strftime('%Y%m%d') in calendar:
            data = get_rank_sum(start_day, vars_list)
            if data is False:
                print(f"{start_day.strftime('%Y-%m-%d')}日交易所数据连接失败，已超过20次，您的地址被网站墙了，请保存好返回数据，稍后从该日期起重试")
                return records.reset_index(drop=True)
            records = records.append(data)
        else:
            warnings.warn(f"{start_day.strftime('%Y%m%d')}非交易日")
        start_day += datetime.timedelta(days=1)

    return records.reset_index(drop=True)


def get_rank_sum(date=None, vars_list=cons.contract_symbols):
    """
    抓取四个期货交易所前5、前10、前15、前20会员持仓排名数据
    注1：由于上期所和中金所只公布每个品种内部的标的排名, 没有公布品种的总排名;
        所以函数输出的品种排名是由品种中的每个标的加总获得, 并不是真实的品种排名列表
    注2：大商所只公布了品种排名, 未公布标的排名
    :param date: 日期 format: YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :param vars_list: 合约品种如 RB, AL等列表 为空时为所有商品
    :return: pd.DataFrame:
    展期收益率数据
    symbol                           标的合约                     string
    var                              商品品种                     string
    vol_top5                         成交量前5会员成交量总和         int
    vol_chg_top5                     成交量前5会员成交量变化总和      int
    long_open_interest_top5          持多单前5会员持多单总和         int
    long_open_interest_chg_top5      持多单前5会员持多单变化总和      int
    short_open_interest_top5         持空单前5会员持空单总和         int
    short_open_interest_chg_top5     持空单前5会员持空单变化总和      int
    vol_top10                        成交量前10会员成交量总和        int
    ...
    date                             日期                         string YYYYMMDD
    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    dce_var = [i for i in vars_list if i in cons.market_exchange_symbols['dce']]
    shfe_var = [i for i in vars_list if i in cons.market_exchange_symbols['shfe']]
    czce_var = [i for i in vars_list if i in cons.market_exchange_symbols['czce']]
    cffex_var = [i for i in vars_list if i in cons.market_exchange_symbols['cffex']]
    big_dict = {}
    if len(dce_var) > 0:
        data = get_dce_rank_table(date, dce_var)
        if data is False:
            return False
        big_dict.update(data)
    if len(shfe_var) > 0:
        data = get_shfe_rank_table(date, shfe_var)
        if data is False:
            return False
        big_dict.update(data)
    if len(czce_var) > 0:
        data = get_czce_rank_table(date, czce_var)
        if data is False:
            return False
        big_dict.update(data)
    if len(cffex_var) > 0:
        data = get_cffex_rank_table(date, cffex_var)
        if data is False:
            return False
        big_dict.update(data)
    records = pd.DataFrame()

    for symbol, table in big_dict.items():
        table = table.applymap(lambda x: 0 if x == '' else x)
        for symbol_inner in set(table['symbol']):

            var = symbol_varieties(symbol_inner)
            if var in vars_list:
                table_cut = table[table['symbol'] == symbol_inner]
                table_cut['rank'] = table_cut['rank'].astype('float')
                table_cut_top5 = table_cut[table_cut['rank'] <= 5]
                table_cut_top10 = table_cut[table_cut['rank'] <= 10]
                table_cut_top15 = table_cut[table_cut['rank'] <= 15]
                table_cut_top20 = table_cut[table_cut['rank'] <= 20]

                big_dict = {'symbol': symbol_inner, 'variety': var,

                            'vol_top5': table_cut_top5['vol'].sum(), 'vol_chg_top5': table_cut_top5['vol_chg'].sum(),
                            'long_open_interest_top5': table_cut_top5['long_open_interest'].sum(),
                            'long_open_interest_chg_top5': table_cut_top5['long_open_interest_chg'].sum(),
                            'short_open_interest_top5': table_cut_top5['short_open_interest'].sum(),
                            'short_open_interest_chg_top5': table_cut_top5['short_open_interest_chg'].sum(),

                            'vol_top10': table_cut_top10['vol'].sum(),
                            'vol_chg_top10': table_cut_top10['vol_chg'].sum(),
                            'long_open_interest_top10': table_cut_top10['long_open_interest'].sum(),
                            'long_open_interest_chg_top10': table_cut_top10['long_open_interest_chg'].sum(),
                            'short_open_interest_top10': table_cut_top10['short_open_interest'].sum(),
                            'short_open_interest_chg_top10': table_cut_top10['short_open_interest_chg'].sum(),

                            'vol_top15': table_cut_top15['vol'].sum(),
                            'vol_chg_top15': table_cut_top15['vol_chg'].sum(),
                            'long_open_interest_top15': table_cut_top15['long_open_interest'].sum(),
                            'long_open_interest_chg_top15': table_cut_top15['long_open_interest_chg'].sum(),
                            'short_open_interest_top15': table_cut_top15['short_open_interest'].sum(),
                            'short_open_interest_chg_top15': table_cut_top15['short_open_interest_chg'].sum(),

                            'vol_top20': table_cut_top20['vol'].sum(),
                            'vol_chg_top20': table_cut_top20['vol_chg'].sum(),
                            'long_open_interest_top20': table_cut_top20['long_open_interest'].sum(),
                            'long_open_interest_chg_top20': table_cut_top20['long_open_interest_chg'].sum(),
                            'short_open_interest_top20': table_cut_top20['short_open_interest'].sum(),
                            'short_open_interest_chg_top20': table_cut_top20['short_open_interest_chg'].sum(),

                            'date': date.strftime('%Y%m%d')
                            }
                records = records.append(pd.DataFrame(big_dict, index=[0]))

    if len(big_dict.items()) > 0:
        add_vars = [i for i in cons.market_exchange_symbols['shfe'] + cons.market_exchange_symbols['cffex'] if
                    i in records['variety'].tolist()]
        for var in add_vars:
            records_cut = records[records['variety'] == var]
            var_record = pd.DataFrame(records_cut.sum()).T
            var_record['date'] = date.strftime('%Y%m%d')
            var_record.loc[:, ['variety', 'symbol']] = var
            records = records.append(var_record)

    return records.reset_index(drop=True)


def get_shfe_rank_table(date=None, vars_list=cons.contract_symbols):
    """
    上海期货交易所前 20 会员持仓排名数据明细
    注：该交易所只公布每个品种内部的标的排名，没有公布品种的总排名
    数据从20020107开始，每交易日16:30左右更新数据
    :param date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :param vars_list: 合约品种如RB、AL等列表 为空时为所有商品
    :return: pd.DataFrame
        rank                        排名                        int
        vol_party_name              成交量排序的当前名次会员        string(中文)
        vol                         该会员成交量                  int
        vol_chg                     该会员成交量变化量             int
        long_party_name             持多单排序的当前名次会员        string(中文)
        long_open_interest          该会员持多单                  int
        long_open_interest_chg      该会员持多单变化量             int
        short_party_name            持空单排序的当前名次会员        string(中文)
        short_open_interest         该会员持空单                  int
        short_open_interest_chg     该会员持空单变化量             int
        symbol                      标的合约                     string
        var                         品种                        string
        date                        日期                        string YYYYMMDD

    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date < datetime.date(2002, 1, 7):
        print("shfe数据源开始日期为20020107，跳过")
        return {}
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return {}
    url = cons.SHFE_VOL_RANK_URL % (date.strftime('%Y%m%d'))
    r = requests_link(url, 'utf-8')
    try:
        context = json.loads(r.text)
    except:
        return {}
    df = pd.DataFrame(context['o_cursor'])

    df = df.rename(
        columns={'CJ1': 'vol', 'CJ1_CHG': 'vol_chg', 'CJ2': 'long_open_interest', 'CJ2_CHG': 'long_open_interest_chg',
                 'CJ3': 'short_open_interest',
                 'CJ3_CHG': 'short_open_interest_chg', 'PARTICIPANTABBR1': 'vol_party_name',
                 'PARTICIPANTABBR2': 'long_party_name',
                 'PARTICIPANTABBR3': 'short_party_name', 'PRODUCTNAME': 'product1', 'RANK': 'rank',
                 'INSTRUMENTID': 'symbol', 'PRODUCTSORTNO': 'product2'})

    if len(df.columns) < 3:
        return {}
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.applymap(lambda x: None if x == '' else x)
    df['variety'] = df['symbol'].apply(lambda x: symbol_varieties(x))

    df = df[df['rank'] > 0]
    for col in ['PARTICIPANTID1', 'PARTICIPANTID2', 'PARTICIPANTID3', 'product1', 'product2']:
        try:
            del df[col]
        except:
            pass
    get_vars = [var for var in vars_list if var in df['variety'].tolist()]
    big_dict = {}
    for var in get_vars:
        df_var = df[df['variety'] == var]
        for symbol in set(df_var['symbol']):
            df_symbol = df_var[df_var['symbol'] == symbol]
            big_dict[symbol] = df_symbol.reset_index(drop=True)
    return big_dict


def _czce_df_read(url, skip_rows, encoding='utf-8', header=0):
    """
    郑州商品交易所的网页数据
    :param header:
    :type header:
    :param url: 网站 string
    :param skip_rows: 去掉前几行 int
    :param encoding: utf-8 or gbk or gb2312
    :return: pd.DataFrame
    """
    r = requests_link(url, encoding)
    data = pd.read_html(r.text, match='.+', flavor=None, header=header, index_col=0, skiprows=skip_rows, attrs=None,
                        parse_dates=False, thousands=', ', encoding="gbk", decimal='.',
                        converters=None, na_values=None, keep_default_na=True)
    return data


def get_czce_rank_table(date="20081015", vars_list=cons.contract_symbols):
    """
    郑州商品交易所前 20 会员持仓排名数据明细
    注：该交易所既公布了品种排名, 也公布了标的排名
    :param date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :param vars_list: 合约品种如RB、AL等列表 为空时为所有商品, 数据从20050509开始，每交易日16:30左右更新数据
    :return: pd.DataFrame
    rank                        排名                        int
    vol_party_name              成交量排序的当前名次会员        string(中文)
    vol                         该会员成交量                  int
    vol_chg                     该会员成交量变化量             int
    long_party_name             持多单排序的当前名次会员        string(中文)
    long_open_interest               该会员持多单                  int
    long_open_interest_chg           该会员持多单变化量             int
    short_party_name            持空单排序的当前名次会员        string(中文)
    short_open_interest              该会员持空单                  int
    short_open_interest_chg          该会员持空单变化量             int
    symbol                      标的合约                     string
    var                         品种                        string
    date                        日期                        string YYYYMMDD
    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date < datetime.date(2005, 5, 9):
        print("czce数据源开始日期为20050509，跳过")
        return {}
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return {}
    if date <= datetime.date(2010, 8, 25):
        url = cons.CZCE_VOL_RANK_URL_1 % (date.strftime('%Y%m%d'))
        r = requests.get(url)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "lxml")
        data = _czce_df_read(url, skip_rows=0)
        r = requests_link(url, 'utf-8')
        r.encoding = 'utf-8'
        symbols = []
        for link in soup.find_all('b'):
            strings = (str(link).split(' '))

            if len(strings) > 5:
                try:
                    symbol = chinese_to_english(strings[4])
                except:
                    symbol = strings[4]
                if symbol == "SR905日期:":
                    symbol = "SR905"
                symbols.append(symbol)
        big_dict = {}
        for i in range(len(symbols)):
            symbol = symbols[i]
            table_cut = data[i + 1]
            table_cut.columns = rank_columns
            table_cut = table_cut.iloc[:-1, :]
            table_cut.loc[:, 'rank'] = table_cut.index
            table_cut.loc['合计', 'rank'] = 999
            table_cut.loc['合计', ['vol_party_name', 'long_party_name', 'short_party_name']] = None
            table_cut.loc[:, 'symbol'] = symbol
            table_cut.loc[:, 'variety'] = symbol_varieties(symbol)
            table_cut[intColumns] = table_cut[intColumns].fillna(0)
            table_cut[intColumns] = table_cut[intColumns].astype(str)
            table_cut[intColumns] = table_cut[intColumns].applymap(lambda x: x.replace(',', ''))
            table_cut = table_cut.applymap(lambda x: 0 if x == '-' else x)

            table_cut[intColumns] = table_cut[intColumns].astype(float)
            table_cut[intColumns] = table_cut[intColumns].astype(int)
            big_dict[symbol] = table_cut.reset_index(drop=True)
        return big_dict

    elif date <= datetime.date(2015, 11, 11):  # 20200311 格式修正
        url = cons.CZCE_VOL_RANK_URL_2 % (date.year, date.strftime('%Y%m%d'))
        data = _czce_df_read(url, skip_rows=0, header=None)[3:]
        big_df = pd.DataFrame()
        for item in data:
            big_df = pd.concat([big_df, item], axis=0, ignore_index=False)
        big_df.columns = big_df.iloc[0, :].tolist()
        data = big_df.iloc[1:, :]
    elif date < datetime.date(2017, 12, 28):  # 20200311 格式修正
        url = cons.CZCE_VOL_RANK_URL_3 % (date.year, date.strftime('%Y%m%d'))
        data = _czce_df_read(url, skip_rows=0, header=0)[1]
    else:
        url = cons.CZCE_VOL_RANK_URL_3 % (date.year, date.strftime('%Y%m%d'))
        data = _czce_df_read(url, skip_rows=0)[0]

    if len(data.columns) < 6:
        return {}

    table = pd.DataFrame(data.iloc[:, :9])
    table.index.name = table.columns[0]
    table.columns = rank_columns
    table.loc[:, 'rank'] = table.index
    table[intColumns] = table[intColumns].astype(str)
    table[intColumns] = table[intColumns].applymap(lambda x: x.replace(',', ''))
    table = table.applymap(lambda x: 0 if x == '-' else x)
    indexes = [i for i in table.index if '合约' in i or '品种' in i]
    indexes.insert(0, 0)
    big_dict = {}

    for i in range(len(indexes)):

        if indexes[i] == 0:
            table_cut = table.loc[:indexes[i + 1], :]
            string = table_cut.index.name

        elif i < len(indexes) - 1:
            table_cut = table.loc[indexes[i]:indexes[i + 1], :]
            string = table_cut.index[0]

        else:
            table_cut = table.loc[indexes[i]:, :]
            string = table_cut.index[0]

        if 'PTA' in string:
            symbol = 'TA'
        else:
            try:
                symbol = chinese_to_english(find_chinese(re.compile(r'：(.*) ').findall(string)[0]))
            except:
                symbol = re.compile(r'：(.*) ').findall(string)[0]

        var = symbol_varieties(symbol)

        if var in vars_list:
            table_cut = table_cut.dropna(how='any').iloc[1:, :]
            table_cut = table_cut.loc[[x for x in table_cut.index if x in [str(i) for i in range(21)]], :]

            table_cut = _table_cut_cal(table_cut, symbol)
            big_dict[symbol.strip()] = table_cut.reset_index(drop=True)

    return big_dict


def get_dce_rank_table(date="20180404", vars_list=cons.contract_symbols):
    """
    大连商品交易所前 20 会员持仓排名数据明细
    注: 该交易所既公布品种排名, 也公布标的合约排名
    :param date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date 对象, 为空时为当天
    :param vars_list: 合约品种如 RB、AL等列表为空时为所有商品, 数据从 20060104 开始，每交易日 16:30 左右更新数据
    :return: pandas.DataFrame
    rank                        排名                        int
    vol_party_name              成交量排序的当前名次会员      string(中文)
    vol                         该会员成交量                 int
    vol_chg                     该会员成交量变化量            int
    long_party_name             持多单排序的当前名次会员      string(中文)
    long_open_interest          该会员持多单                 int
    long_open_interest_chg      该会员持多单变化量            int
    short_party_name            持空单排序的当前名次会员       string(中文)
    short_open_interest         该会员持空单                  int
    short_open_interest_chg     该会员持空单变化量             int
    symbol                      标的合约                     string
    var                         品种                        string
    date                        日期                        string YYYYMMDD
    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date < datetime.date(2006, 1, 4):
        print(Exception("大连商品交易所数据源开始日期为20060104，跳过"))
        return {}
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return {}
    vars_list = [i for i in vars_list if i in cons.market_exchange_symbols['dce']]
    big_dict = {}
    for var in vars_list:
        url = cons.DCE_VOL_RANK_URL % (var.lower(), var.lower(), date.year, date.month - 1, date.day)
        list_60_name = []
        list_60 = []
        list_60_chg = []
        rank = []
        texts = requests_link(url).content.splitlines()
        if not texts:
            return False
        if len(texts) > 30:
            for text in texts:
                line = text.decode("utf-8")
                string_list = line.split()
                try:
                    if int(string_list[0]) <= 20:
                        list_60_name.append(string_list[1])
                        list_60.append(string_list[2])
                        list_60_chg.append(string_list[3])
                        rank.append(string_list[0])
                except:
                    pass
            table_cut = pd.DataFrame({'rank': rank[0:20],
                                      'vol_party_name': list_60_name[0:20],
                                      'vol': list_60[0:20],
                                      'vol_chg': list_60_chg[0:20],
                                      'long_party_name': list_60_name[20:40],
                                      'long_open_interest': list_60[20:40],
                                      'long_open_interest_chg': list_60_chg[20:40],
                                      'short_party_name': list_60_name[40:60],
                                      'short_open_interest': list_60[40:60],
                                      'short_open_interest_chg': list_60_chg[40:60]
                                      })
            table_cut = table_cut.applymap(lambda x: x.replace(',', ''))
            table_cut = _table_cut_cal(table_cut, var)
            big_dict[var] = table_cut.reset_index(drop=True)
    return big_dict


def get_cffex_rank_table(date="20200311", vars_list=cons.contract_symbols):
    """
    中国金融期货交易所前20会员持仓排名数据明细
    注：该交易所既公布品种排名，也公布标的排名
    :param date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :param vars_list: 合约品种如RB、AL等列表 为空时为所有商品, 数据从20100416开始，每交易日16:30左右更新数据
    :return: pd.DataFrame
    rank                        排名                        int
    vol_party_name              成交量排序的当前名次会员        string(中文)
    vol                         该会员成交量                  int
    vol_chg                     该会员成交量变化量             int
    long_party_name             持多单排序的当前名次会员        string(中文)
    long_open_interest          该会员持多单                  int
    long_open_interest_chg      该会员持多单变化量             int
    short_party_name            持空单排序的当前名次会员        string(中文)
    short_open_interest         该会员持空单                  int
    short_open_interest_chg     该会员持空单变化量             int
    symbol                      标的合约                     string
    var                         品种                        string
    date                        日期                        string YYYYMMDD
    """
    vars_list = [i for i in vars_list if i in cons.market_exchange_symbols['cffex']]
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date < datetime.date(2010, 4, 16):
        print(Exception("cffex数据源开始日期为20100416，跳过"))
        return {}
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return {}
    big_dict = {}
    for var in vars_list:
        # print(var)
        url = cons.CFFEX_VOL_RANK_URL % (date.strftime('%Y%m'), date.strftime('%d'), var)
        r = requests_link(url, encoding='gbk')
        if not r:
            return False
        if '网页错误' not in r.text:
            try:
                temp_chche = StringIO(r.text.split('\n交易日,')[1])
            except:
                temp_chche = StringIO(r.text.split('\n交易日,')[0][4:])  # 20200316开始数据结构变化，统一格式
            table = pd.read_csv(temp_chche)
            table = table.dropna(how='any')
            table = table.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            for symbol in set(table['合约']):
                table_cut = table[table['合约'] == symbol]
                table_cut.columns = ['symbol', 'rank'] + rank_columns
                table_cut = _table_cut_cal(pd.DataFrame(table_cut), symbol)
                big_dict[symbol] = table_cut.reset_index(drop=True)
    return big_dict


def _table_cut_cal(table_cut, symbol):
    """
    表格切分
    :param table_cut: 需要切分的表格
    :type table_cut: pandas.DataFrame
    :param symbol: 具体合约的代码
    :type symbol: str
    :return:
    :rtype: pandas.DataFrame
    """
    var = symbol_varieties(symbol)
    table_cut[intColumns + ['rank']] = table_cut[intColumns + ['rank']].astype(int)
    table_cut_sum = table_cut.sum()
    table_cut_sum['rank'] = 999
    for col in ['vol_party_name', 'long_party_name', 'short_party_name']:
        table_cut_sum[col] = None
    table_cut = table_cut.append(pd.DataFrame(table_cut_sum).T, sort=True)
    table_cut['symbol'] = symbol
    table_cut['variety'] = var
    table_cut[intColumns + ['rank']] = table_cut[intColumns + ['rank']].astype(int)
    return table_cut


if __name__ == '__main__':
    get_czce_rank_table_first_df = get_czce_rank_table(date='20081015', vars_list=["SR"])
    print(get_czce_rank_table_first_df)
    get_czce_rank_table_second_df = get_czce_rank_table(date='20151112')
    print(get_czce_rank_table_second_df)
    get_czce_rank_table_third_df = get_czce_rank_table(date='20191227')
    print(get_czce_rank_table_third_df)
    get_cffex_rank_table_df = get_cffex_rank_table(date='20200316')
    print(get_cffex_rank_table_df)
    get_shfe_rank_table_df = get_shfe_rank_table(date='20190711')
    print(get_shfe_rank_table_df)
    get_shfe_rank_table_first_df = get_dce_rank_table(date='20131227')
    print(get_shfe_rank_table_first_df)
    get_shfe_rank_table_second_df = get_dce_rank_table(date='20171227')
    print(get_shfe_rank_table_second_df)
    get_shfe_rank_table_third_df = get_dce_rank_table(date='20180718')
    print(get_shfe_rank_table_third_df)
    get_rank_sum_daily_df = get_rank_sum_daily(start_day="20200313", end_day="20200317")
    print(get_rank_sum_daily_df)


