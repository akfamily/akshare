#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/1/12 15:06
Desc: 期货-中国-交易所-会员持仓数据接口
大连商品交易所、上海期货交易所、郑州商品交易所、中国金融期货交易所
采集前 20 会员持仓数据;
建议下午 16:30 以后采集当天数据, 避免交易所数据更新不稳定;
郑州商品交易所格式分为三类
大连商品交易所有具体合约的持仓排名, 通过 futures_dce_position_rank 获取
20171228
http://www.czce.com.cn/cn/DFSStaticFiles/Future/2020/20200727/FutureDataHolding.txt

20100825
http://www.czce.com.cn/cn/exchange/2014/datatradeholding/20140515.txt
"""
import datetime
import json
import re
import time
import warnings
import zipfile
from io import BytesIO
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.futures import cons
from akshare.futures.requests_fun import (
    requests_link
)
from akshare.futures.symbol_var import (
    symbol_varieties
)

calendar = cons.get_calendar()
rank_columns = ['vol_party_name', 'vol', 'vol_chg', 'long_party_name', 'long_open_interest',
                'long_open_interest_chg', 'short_party_name', 'short_open_interest', 'short_open_interest_chg']
intColumns = ['vol', 'vol_chg', 'long_open_interest', 'long_open_interest_chg', 'short_open_interest',
              'short_open_interest_chg']


def get_rank_sum_daily(start_day: str = "20210510", end_day: str = "20210510", vars_list: list = cons.contract_symbols):
    """
    采集四个期货交易所前 5、前 10、前 15、前 20 会员持仓排名数据
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


def get_rank_sum(date: str = "20210525", vars_list: list = cons.contract_symbols):
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
                if var in czce_var:
                    for col in [item for item in table.columns if item.find('open_interest') > -1] + ['vol', 'vol_chg']:
                        table[col] = [float(value.replace(',', '')) if value != '-' else 0.0 for value in table[col]]

                table_cut = table[table['symbol'] == symbol_inner]
                table_cut['rank'] = table_cut['rank'].astype('float')
                table_cut_top5 = table_cut[table_cut['rank'] <= 5]
                table_cut_top10 = table_cut[table_cut['rank'] <= 10]
                table_cut_top15 = table_cut[table_cut['rank'] <= 15]
                table_cut_top20 = table_cut[table_cut['rank'] <= 20]

                big_dict = {'symbol': symbol_inner,
                            'variety': var,
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
        add_vars = [i for i in cons.market_exchange_symbols['dce'] + cons.market_exchange_symbols['shfe'] +
                    cons.market_exchange_symbols['cffex'] if
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
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
        "Host": "www.czce.com.cn",
        "Cookie": "XquW6dFMPxV380S=CAaD3sMkdXv3fUoaJlICIEv0MVegGq5EoMyBcxkOjCgSjmpuovYFuTLtYFcxTZGw; XquW6dFMPxV380T=5QTTjUlA6f6WiDO7fMGmqNxHBWz.hKIc8lb_tc1o4nHrJM4nsXCAI9VHaKyV_jkHh4cIVvD25kGQAh.MvLL1SHRA20HCG9mVVHPhAzktNdPK3evjm0NYbTg2Gu_XGGtPhecxLvdFQ0.JlAxy_z0C15_KdO8kOI18i4K0rFERNPxjXq5qG1Gs.QiOm976wODY.pe8XCQtAsuLYJ.N4DpTgNfHJp04jhMl0SntHhr.jhh3dFjMXBx.JEHngXBzY6gQAhER7uSKAeSktruxFeuKlebse.vrPghHqWvJm4WPTEvDQ8q",
    }
    r = requests_link(url, encoding, headers=headers)
    data = pd.read_html(r.text, match='.+', flavor=None, header=header, index_col=0, skiprows=skip_rows, attrs=None,
                        parse_dates=False, thousands=', ', encoding="gbk", decimal='.',
                        converters=None, na_values=None, keep_default_na=True)
    return data


def get_czce_rank_table(date: str = "20210428", vars_list: list = cons.contract_symbols):
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
    if date < datetime.date(2015, 10, 8):
        print("CZCE可获取的数据源开始日期为 20151008, 请输入合适的日期参数")
        return {}
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return {}
    if date >= datetime.date(2015, 10, 8):
        url = f"http://www.czce.com.cn/cn/DFSStaticFiles/Future/{date.year}/{date.isoformat().replace('-', '')}/FutureDataHolding.xls"
        r = requests.get(url)
        temp_df = pd.read_excel(BytesIO(r.content))

    temp_pinzhong_index = [item + 1 for item in temp_df[temp_df.iloc[:, 0].str.contains("合计", na=False)].index.to_list()]
    temp_pinzhong_index.insert(0, 0)
    temp_pinzhong_index.pop()
    temp_symbol_index = temp_df.iloc[temp_pinzhong_index, 0].str.split(" ", expand=True).iloc[:, 0]
    symbol_list = [re.compile(r"[0-9a-zA-Z_]+").findall(item)[0] for item in temp_symbol_index.values]
    temp_symbol_index_list = temp_symbol_index.index.to_list()
    big_dict = {}
    for i in range(len(temp_symbol_index_list) - 1):
        inner_temp_df = temp_df[temp_symbol_index_list[i] + 2: temp_symbol_index_list[i + 1] - 1]
        inner_temp_df.columns = ["rank",
                                 "vol_party_name",
                                 "vol",
                                 "vol_chg",
                                 "long_party_name",
                                 "long_open_interest",
                                 "long_open_interest_chg",
                                 "short_party_name",
                                 "short_open_interest",
                                 "short_open_interest_chg",
                                 ]
        inner_temp_df.reset_index(inplace=True, drop=True)
        big_dict[symbol_list[i]] = inner_temp_df
        inner_temp_df = temp_df[temp_symbol_index_list[i + 1] + 2:-1]
        inner_temp_df.columns = ["rank",
                                 "vol_party_name",
                                 "vol",
                                 "vol_chg",
                                 "long_party_name",
                                 "long_open_interest",
                                 "long_open_interest_chg",
                                 "short_party_name",
                                 "short_open_interest",
                                 "short_open_interest_chg",
                                 ]
        inner_temp_df.reset_index(inplace=True, drop=True)
        big_dict[symbol_list[-1]] = inner_temp_df
    new_big_dict = {}
    for key, value in big_dict.items():
        value["symbol"] = key
        value["variety"] = re.compile(r"[a-zA-Z_]+").findall(key)[0]
        new_big_dict[key] = value

    return new_big_dict


def _get_dce_contract_list(date, var):
    """
    大连商品交易所取消了品种排名，只提供标的合约排名，需要获取标的合约列表
    :param date: 日期 datetime.date 对象, 为空时为当天
    :param var: 合约品种
    :return: list 公布了持仓排名的合约列表
    """
    url = 'http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "close",
        "Host": "www.dce.com.cn",
        "Origin": "http://www.dce.com.cn",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        'memberDealPosiQuotes.variety': var.lower(),
        'memberDealPosiQuotes.trade_type': '0',
        'year': date.year,
        'month': date.month - 1,
        'day': date.day,
        'contract.contract_id': 'all',
        'contract.variety_id': var.lower(),
        'contract': '',
    }

    while 1:
        try:
            r = requests.post(url, params=params, headers=headers)
            soup = BeautifulSoup(r.text, "lxml")
            contract_list = [re.findall(r"\d+", item["onclick"].strip("javascript:setContract_id('").strip("');"))[0]
                             for item in
                             soup.find_all(attrs={"name": "contract"})]
            contract_list = [var.lower() + item for item in contract_list]
            return contract_list
        except:
            time.sleep(5)
            continue


def get_dce_rank_table(date: str = "20210309", vars_list=cons.contract_symbols):
    """
    大连商品交易所前 20 会员持仓排名数据明细, 由于交易所网站问题, 需要 20200720 之后才有数据
    注: 该交易所只公布标的合约排名
    :param date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date 对象, 为空时为当天
    :param vars_list: 合约品种如 RB、AL 等列表为空时为所有商品, 数据从 20060104 开始，每交易日 16:30 左右更新数据
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
    date_string = date
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date < datetime.date(2006, 1, 4):
        print(Exception("大连商品交易所数据源开始日期为 20060104，跳过"))
        return {}
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return {}
    vars_list = [i for i in vars_list if i in cons.market_exchange_symbols['dce']]
    big_dict = {}
    for var in vars_list:
        # var = 'V'
        symbol_list = _get_dce_contract_list(date, var)
        for symbol in symbol_list:
            # print(symbol)
            url = cons.DCE_VOL_RANK_URL_1 % (var.lower(), symbol, var.lower(), date.year, date.month - 1, date.day)
            try:
                temp_df = pd.read_excel(url[:-3] + "excel", header=0, skiprows=3)
                temp_df.dropna(how='any', axis=0, inplace=True)
                temp_df = temp_df.applymap(lambda x: str(x).replace(',', ''))
                del temp_df["名次.1"]
                del temp_df["名次.2"]
                temp_df.rename(columns={"名次": "rank",
                                        "会员简称": "vol_party_name",
                                        "成交量": "vol",
                                        "增减": "vol_chg",
                                        "会员简称.1": "long_party_name",
                                        "持买单量": "long_open_interest",
                                        "增减.1": "long_open_interest_chg",
                                        "会员简称.2": "short_party_name",
                                        "持卖单量": "short_open_interest",
                                        "增减.2": "short_open_interest_chg",
                                        }, inplace=True)
                temp_df['symbol'] = symbol.upper()
                temp_df['var'] = var
                temp_df['date'] = date_string
                temp_df = temp_df.applymap(lambda x: str(x).replace("-", "0") if x == "-" else x)
                temp_df['rank'] = range(1, len(temp_df)+1)
                temp_df['vol'] = temp_df['vol'].astype(float)
                temp_df['vol_chg'] = temp_df['vol_chg'].astype(float)
                temp_df['long_open_interest'] = temp_df['long_open_interest'].astype(float)
                temp_df['long_open_interest_chg'] = temp_df['long_open_interest_chg'].astype(float)
                temp_df['short_open_interest'] = temp_df['short_open_interest'].astype(float)
                temp_df['short_open_interest_chg'] = temp_df['short_open_interest_chg'].astype(float)
                big_dict[symbol] = temp_df
            except:
                temp_url = "http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html"
                payload = {
                    "memberDealPosiQuotes.variety": var.lower(),
                    "memberDealPosiQuotes.trade_type": "0",
                    "year": date.year,
                    "month": date.month - 1,
                    "day": str(date.day).zfill(2),
                    "contract.contract_id": symbol,
                    "contract.variety_id": var.lower(),
                    "contract": ""
                }
                r = requests.post(temp_url, data=payload)
                if r.status_code != 200:
                    big_dict[symbol] = {}
                else:
                    temp_df = pd.read_html(r.text)[1].iloc[:-1, :]
                    del temp_df["名次.1"]
                    del temp_df["名次.2"]
                    temp_df.rename(columns={"名次": "rank",
                                            "会员简称": "vol_party_name",
                                            "成交量": "vol",
                                            "增减": "vol_chg",
                                            "会员简称.1": "long_party_name",
                                            "持买单量": "long_open_interest",
                                            "增减.1": "long_open_interest_chg",
                                            "会员简称.2": "short_party_name",
                                            "持卖单量": "short_open_interest",
                                            "增减.2": "short_open_interest_chg",
                                            }, inplace=True)
                    temp_df['symbol'] = symbol.upper()
                    temp_df['var'] = var
                    temp_df['date'] = date_string
                    temp_df = temp_df.applymap(lambda x: str(x).replace("-", "0") if x == "-" else x)
                    temp_df['rank'] = range(1, len(temp_df)+1)
                    temp_df['vol'] = temp_df['vol'].astype(float)
                    temp_df['vol_chg'] = temp_df['vol_chg'].astype(float)
                    temp_df['long_open_interest'] = temp_df['long_open_interest'].astype(float)
                    temp_df['long_open_interest_chg'] = temp_df['long_open_interest_chg'].astype(float)
                    temp_df['short_open_interest'] = temp_df['short_open_interest'].astype(float)
                    temp_df['short_open_interest_chg'] = temp_df['short_open_interest_chg'].astype(float)
                    big_dict[symbol] = temp_df
    return big_dict


def get_cffex_rank_table(date="20200427", vars_list=cons.contract_symbols):
    """
    中国金融期货交易所前 20 会员持仓排名数据明细
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
        # var = "IF"
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
    :return: 表格切分后的结果
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


def futures_dce_position_rank(date: str = "20160919") -> dict:
    """
    大连商品交易所-每日持仓排名-具体合约
    http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/rcjccpm/index.html
    :param date: 指定交易日; e.g., "20200511"
    :type date: str
    :return: 指定日期的持仓排名数据
    :rtype: pandas.DataFrame
    """
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return {}
    url = "http://www.dce.com.cn/publicweb/quotesdata/exportMemberDealPosiQuotesBatchData.html"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "160",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.dce.com.cn",
        "Origin": "http://www.dce.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    payload = {
        "memberDealPosiQuotes.variety": "a",
        "memberDealPosiQuotes.trade_type": "0",
        "contract.contract_id": "a2009",
        "contract.variety_id": "a",
        "year": date.year,
        "month": date.month - 1,
        "day": date.day,
        "batchExportFlag": "batch",
    }
    r = requests.post(url, payload, headers=headers)
    big_dict = dict()
    with zipfile.ZipFile(BytesIO(r.content), "r") as z:
        for i in z.namelist():
            file_name = i.encode('cp437').decode('GBK')
            if not file_name.startswith(date.strftime("%Y%m%d")):
                continue
            try:
                data = pd.read_table(z.open(i), header=None, sep="\t").iloc[:-6]
                if len(data) < 12:  # 处理没有活跃合约的情况
                    big_dict[file_name.split("_")[1]] = pd.DataFrame()
                    continue
                temp_filter = data[data.iloc[:, 0].str.find("名次") == 0].index.tolist()
                if temp_filter[1] - temp_filter[0] < 5:  # 过滤有无成交量但是有买卖持仓的数据, 如 20201105_c2011_成交量_买持仓_卖持仓排名.txt
                    big_dict[file_name.split("_")[1]] = pd.DataFrame()
                    continue
                start_list = data[data.iloc[:, 0].str.find("名次") == 0].index.tolist()
                data = data.iloc[start_list[0]:, data.columns[data.iloc[start_list[0], :].notnull()]]
                data.reset_index(inplace=True, drop=True)
                start_list = data[data.iloc[:, 0].str.find("名次") == 0].index.tolist()
                end_list = data[data.iloc[:, 0].str.find("总计") == 0].index.tolist()
                part_one = data[start_list[0]: end_list[0]].iloc[1:, :]
                part_two = data[start_list[1]: end_list[1]].iloc[1:, :]
                part_three = data[start_list[2]: end_list[2]].iloc[1:, :]
                temp_df = pd.concat([part_one.reset_index(drop=True), part_two.reset_index(drop=True),
                                     part_three.reset_index(drop=True)], axis=1, ignore_index=True)
                temp_df.columns = ["名次", "会员简称", "成交量", "增减", "名次", "会员简称", "持买单量", "增减", "名次", "会员简称", "持卖单量", "增减"]
                temp_df["rank"] = range(1, len(temp_df) + 1)
                del temp_df["名次"]
                temp_df.columns = ["vol_party_name", "vol", "vol_chg", "long_party_name", "long_open_interest",
                                   "long_open_interest_chg", "short_party_name", "short_open_interest",
                                   "short_open_interest_chg", "rank"]
                temp_df["symbol"] = file_name.split("_")[1]
                temp_df["variety"] = file_name.split("_")[1][:-4].upper()
                temp_df = temp_df[["long_open_interest", "long_open_interest_chg", "long_party_name", "rank",
                                   "short_open_interest", "short_open_interest_chg", "short_party_name",
                                   "vol", "vol_chg", "vol_party_name", "symbol", "variety"]]
                big_dict[file_name.split("_")[1]] = temp_df
            except UnicodeDecodeError as e:
                try:
                    data = pd.read_table(z.open(i), header=None, sep="\\s+", encoding="gb2312", skiprows=3)
                except:
                    data = pd.read_table(z.open(i), header=None, sep="\\s+", encoding="gb2312", skiprows=4)
                start_list = data[data.iloc[:, 0].str.find("名次") == 0].index.tolist()
                end_list = data[data.iloc[:, 0].str.find("总计") == 0].index.tolist()
                part_one = data[start_list[0]: end_list[0]].iloc[1:, :]
                part_two = data[start_list[1]: end_list[1]].iloc[1:, :]
                part_three = data[start_list[2]: end_list[2]].iloc[1:, :]
                temp_df = pd.concat([part_one.reset_index(drop=True), part_two.reset_index(drop=True),
                                     part_three.reset_index(drop=True)], axis=1, ignore_index=True)
                temp_df.columns = ["名次", "会员简称", "成交量", "增减", "名次", "会员简称", "持买单量", "增减", "名次", "会员简称", "持卖单量", "增减"]
                temp_df["rank"] = range(1, len(temp_df) + 1)
                del temp_df["名次"]
                temp_df.columns = ["vol_party_name", "vol", "vol_chg", "long_party_name", "long_open_interest",
                                   "long_open_interest_chg", "short_party_name", "short_open_interest",
                                   "short_open_interest_chg", "rank"]
                temp_df["symbol"] = file_name.split("_")[1]
                temp_df["variety"] = file_name.split("_")[1][:-4].upper()
                temp_df = temp_df[["long_open_interest", "long_open_interest_chg", "long_party_name", "rank",
                                   "short_open_interest", "short_open_interest_chg", "short_party_name",
                                   "vol", "vol_chg", "vol_party_name", "symbol", "variety"]]
                big_dict[file_name.split("_")[1]] = temp_df
    return big_dict


def futures_dce_position_rank_other(date: str = "20160104"):
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return {}
    url = "http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html"
    payload = {
        "memberDealPosiQuotes.variety": "c",
        "memberDealPosiQuotes.trade_type": "0",
        "year": date.year,
        "month": date.month - 1,
        "day": date.day,
        "contract.contract_id": "all",
        "contract.variety_id": "c",
        "contract": "",
    }
    r = requests.post(url, data=payload)
    soup = BeautifulSoup(r.text, "lxml")
    symbol_list = [item["onclick"].strip("javascript:setVariety(").strip("');") for item in
                   soup.find_all(attrs={"class": "selBox"})[-3].find_all("input")]
    big_df = dict()
    for symbol in symbol_list:
        payload = {
            "memberDealPosiQuotes.variety": symbol,
            "memberDealPosiQuotes.trade_type": "0",
            "year": date.year,
            "month": date.month - 1,
            "day": date.day,
            "contract.contract_id": "all",
            "contract.variety_id": symbol,
            "contract": "",
        }
        r = requests.post(url, data=payload)
        soup = BeautifulSoup(r.text, "lxml")
        contract_list = [item["onclick"].strip("javascript:setContract_id('").strip("');") for item in
                         soup.find_all(attrs={"name": "contract"})]
        if contract_list:
            if len(contract_list[0]) == 4:
                contract_list = [symbol + item for item in contract_list]
                for contract in contract_list:
                    payload = {
                        "memberDealPosiQuotes.variety": symbol,
                        "memberDealPosiQuotes.trade_type": "0",
                        "year": date.year,
                        "month": date.month - 1,
                        "day": date.day,
                        "contract.contract_id": contract,
                        "contract.variety_id": symbol,
                        "contract": "",
                    }
                    r = requests.post(url, data=payload)
                    temp_df = pd.read_html(r.text)[1].iloc[:-1, :]
                    temp_df.columns = ["rank", "vol_party_name", "vol", "vol_chg", "_", "long_party_name",
                                       "long_open_interest",
                                       "long_open_interest_chg", "_", "short_party_name", "short_open_interest",
                                       "short_open_interest_chg"]
                    temp_df["variety"] = symbol.upper()
                    temp_df["symbol"] = contract
                    temp_df = temp_df[["long_open_interest", "long_open_interest_chg", "long_party_name", "rank",
                                       "short_open_interest", "short_open_interest_chg", "short_party_name",
                                       "vol", "vol_chg", "vol_party_name", "symbol", "variety"]]
                    big_df[contract] = temp_df
    return big_df


if __name__ == '__main__':
    # 郑州商品交易所
    get_czce_rank_table_first_df = get_czce_rank_table(date='20210525')
    print(get_czce_rank_table_first_df)

    get_czce_rank_table_first_df = get_czce_rank_table(date='20201026')
    print(get_czce_rank_table_first_df)
    # 中国金融期货交易所
    get_cffex_rank_table_df = get_cffex_rank_table(date='20200325')
    print(get_cffex_rank_table_df)
    # 上海期货交易所
    get_shfe_rank_table_df = get_shfe_rank_table(date='20190711')
    print(get_shfe_rank_table_df)
    # 大连商品交易所
    get_dce_rank_table_first_df = get_dce_rank_table(date='20131227')
    print(get_dce_rank_table_first_df)
    get_dce_rank_table_second_df = get_dce_rank_table(date='20171227')
    print(get_dce_rank_table_second_df)
    get_dce_rank_table_third_df = get_dce_rank_table(date='20200929')
    print(get_dce_rank_table_third_df)
    get_dce_rank_table_third_df = get_dce_rank_table(date='20210517')
    print(get_dce_rank_table_third_df)
    get_dce_rank_table_fourth_df = get_dce_rank_table(date='20210517', vars_list=['V'])
    print(get_dce_rank_table_fourth_df)

    # 总接口
    get_rank_sum_daily_df = get_rank_sum_daily(start_day="20210515", end_day="20210518", vars_list=['PF'])
    print(get_rank_sum_daily_df)

    futures_dce_detail_dict = futures_dce_position_rank(date="20210407")
    print(futures_dce_detail_dict)

    futures_dce_position_rank_other_df = futures_dce_position_rank_other(date="20200727")
    print(futures_dce_position_rank_other_df)
