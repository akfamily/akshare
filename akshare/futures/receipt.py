# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/9/30 13:58
Desc: 从大连商品交易所, 上海期货交易所, 郑州商品交易所采集每日注册仓单数据, 建议下午 16:30 以后采集当天数据,
避免交易所数据更新不稳定导致的程序出错
"""
import datetime
import re
import warnings
from typing import List

import pandas as pd
import requests

from akshare.futures import cons
from akshare.futures.requests_fun import requests_link, pandas_read_html_link
from akshare.futures.symbol_var import chinese_to_english

calendar = cons.get_calendar()
shfe_20100126 = pd.DataFrame({'var': ['CU', 'AL', 'ZN', 'RU', 'FU', 'AU', 'RB', 'WR'],
                              'receipt': [29783, 285396, 187713, 116435, 376200, 12, 145648, 0]})
shfe_20101029 = pd.DataFrame({'var': ['CU', 'AL', 'ZN', 'RU', 'FU', 'AU', 'RB', 'WR'],
                              'receipt': [39214, 359729, 182562, 25990, 313600, 27, 36789, 0]})


def get_dce_receipt(date: str = None, symbol_list: List = cons.contract_symbols):
    """
    完成
    采集大连商品交易所注册仓单数据
    :param date: format 开始日期: YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象, 为空时为当天
    :param symbol_list: 合约品种如 RB, AL等列表, 为空时为所有商品数据从 20060106开始，每周五更新仓单数据。直到20090407起，每交易日都更新仓单数据
    :return: pd.DataFrame
    展期收益率数据(DataFrame):
    var             商品品种                     string
    receipt         仓单数                       int
    date            日期                         string YYYYMMDD
    """
    if not isinstance(symbol_list, list):
        return warnings.warn(f"symbol_list: 必须是列表")
    date = cons.convert_date(date) if date is not None else datetime.date.today()
    if date.strftime('%Y%m%d') not in calendar:
        warnings.warn(f"{date.strftime('%Y%m%d')}非交易日")
        return None
    payload = {
        "weekQuotes.variety": "all",
        "year": date.year,
        "month": date.month - 1,  # 网站月份描述少 1 个月, 属于网站问题
        "day": date.day
    }
    data = pandas_read_html_link(cons.DCE_RECEIPT_URL, method="post", data=payload, headers=cons.dce_headers)[0]
    records = pd.DataFrame()
    for x in data.to_dict(orient='records'):
        if isinstance(x['品种'], str):
            if x['品种'][-2:] == '小计':
                var = x['品种'][:-2]
                temp_data = {'var': chinese_to_english(var), 'receipt': int(x['今日仓单量']), 'receipt_chg': int(x['增减']),
                             'date': date.strftime('%Y%m%d')}
                records = records.append(pd.DataFrame(temp_data, index=[0]))
    if len(records.index) != 0:
        records.index = records['var']
        vars_in_market = [i for i in symbol_list if i in records.index]
        records = records.loc[vars_in_market, :]
    return records.reset_index(drop=True)


def get_shfe_receipt_1(date: str = None, vars_list: List = cons.contract_symbols):
    """
    抓取上海期货交易所注册仓单数据, 适用20081006至20140518(包括) 20100126、20101029日期交易所格式混乱，直接回复脚本中DataFrame, 20100416、20130821日期交易所数据丢失
    :param date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :param vars_list: 合约品种如RB、AL等列表 为空时为所有商品
    :return: pd.DataFrame
    展期收益率数据(DataFrame):
                    var             商品品种                     string
                    receipt         仓单数                       int
                    date            日期                         string YYYYMMDD           
    """
    date = cons.convert_date(date).strftime('%Y%m%d') if date is not None else datetime.date.today()
    if date not in calendar:
        warnings.warn(f"{date.strftime('%Y%m%d')}非交易日")
        return None
    if date == '20100126':
        shfe_20100126['date'] = date
        return shfe_20100126
    elif date == '20101029':
        shfe_20101029['date'] = date
        return shfe_20101029
    elif date in ['20100416', '20130821']:
        return warnings.warn('20100416、20130821日期交易所数据丢失')
    else:
        var_list = ['天然橡胶', '沥青仓库', '沥青厂库', '热轧卷板', '燃料油', '白银', '线材', '螺纹钢', '铅', '铜', '铝', '锌', '黄金', '锡', '镍']
        url = cons.SHFE_RECEIPT_URL_1 % date
        data = pandas_read_html_link(url)[0]
        indexes = [x for x in data.index if (data[0].tolist()[x] in var_list)]
        last_index = [x for x in data.index if '注' in str(data[0].tolist()[x])][0] - 1
        records = pd.DataFrame()
        for i in list(range(len(indexes))):
            if i != len(indexes) - 1:
                data_cut = data.loc[indexes[i]:indexes[i + 1] - 1, :]
            else:
                data_cut = data.loc[indexes[i]:last_index, :]
                data_cut = data_cut.fillna(method='pad')
            data_dict = dict()
            data_dict['var'] = chinese_to_english(data_cut[0].tolist()[0])
            data_dict['receipt'] = int(data_cut[2].tolist()[-1])
            data_dict['receipt_chg'] = int(data_cut[3].tolist()[-1])
            data_dict['date'] = date
            records = records.append(pd.DataFrame(data_dict, index=[0]))
    if len(records.index) != 0:
        records.index = records['var']
        vars_in_market = [i for i in vars_list if i in records.index]
        records = records.loc[vars_in_market, :]
    return records.reset_index(drop=True)


def get_shfe_receipt_2(date: str = None, vars_list: List = cons.contract_symbols):
    """
        抓取上海商品交易所注册仓单数据
        适用20140519(包括)至今
        Parameters
        ------
            date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars_list: 合约品种如RB、AL等列表 为空时为所有商品
        Return
        -------
            DataFrame:
                展期收益率数据(DataFrame):
                    var             商品品种                     string
                    receipt         仓单数                       int
                    date            日期                         string YYYYMMDD
    """
    date = cons.convert_date(date).strftime('%Y%m%d') if date is not None else datetime.date.today()
    if date not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    url = cons.SHFE_RECEIPT_URL_2 % date
    r = requests_link(url, encoding='utf-8')
    try:
        context = r.json()
    except:
        return pd.DataFrame()
    data = pd.DataFrame(context['o_cursor'])
    if len(data.columns) < 1:
        return pd.DataFrame()
    records = pd.DataFrame()
    for var in set(data['VARNAME'].tolist()):
        data_cut = data[data['VARNAME'] == var]
        data_dict = {'var': chinese_to_english(re.sub(r"\W|[a-zA-Z]", "", var)),
                     'receipt': int(data_cut['WRTWGHTS'].tolist()[-1]),
                     'receipt_chg': int(data_cut['WRTCHANGE'].tolist()[-1]),
                     'date': date}
        records = records.append(pd.DataFrame(data_dict, index=[0]))
    if len(records.index) != 0:
        records.index = records['var']
        vars_in_market = [i for i in vars_list if i in records.index]
        records = records.loc[vars_in_market, :]
    return records.reset_index(drop=True)


def get_czce_receipt_1(date: str = None, vars_list: List = cons.contract_symbols):
    """
    抓取郑州商品交易所注册仓单数据
    适用20080222至20100824(包括)
    :param date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :type date: str
    :param vars_list: list
    :type vars_list: 合约品种如CF、TA等列表 为空时为所有商品
    :return: 展期收益率数据
    :rtype: pandas.DataFrame
    var             商品品种                     string
    receipt         仓单数                       int
    date            日期                         string YYYYMMDD
    """
    date = cons.convert_date(date).strftime('%Y%m%d') if date is not None else datetime.date.today()
    if date not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    if date == '20090820':
        return pd.DataFrame()
    url = cons.CZCE_RECEIPT_URL_1 % date
    r = requests_link(url, encoding='utf-8')
    context = r.text
    data = pd.read_html(context)[1]
    records = pd.DataFrame()
    indexes = [x for x in data.index if '品种：' in str(data[0].tolist()[x])]
    ends = [x for x in data.index if '总计' in str(data[0].tolist()[x])]
    for i in list(range(len(indexes))):
        if i != len(indexes) - 1:
            data_cut = data.loc[indexes[i]:ends[i], :]
            data_cut = data_cut.fillna(method='pad')
        else:
            data_cut = data.loc[indexes[i]:, :]
            data_cut = data_cut.fillna(method='pad')
        if 'PTA' in data_cut[0].tolist()[0]:
            var = 'TA'
        else:
            var = chinese_to_english(re.sub(r'[A-Z]+', '', data_cut[0].tolist()[0][3:]))
        if var == 'CF':
            receipt = data_cut[6].tolist()[-1]
            receipt_chg = data_cut[7].tolist()[-1]
        else:
            receipt = data_cut[5].tolist()[-1]
            receipt_chg = data_cut[6].tolist()[-1]
        data_dict = {'var': var, 'receipt': int(receipt), 'receipt_chg': int(receipt_chg), 'date': date}
        records = records.append(pd.DataFrame(data_dict, index=[0]))
    if len(records.index) != 0:
        records.index = records['var']
        vars_in_market = [i for i in vars_list if i in records.index]
        records = records.loc[vars_in_market, :]
    return records.reset_index(drop=True)


def get_czce_receipt_2(date: str = None, vars_list: List = cons.contract_symbols):
    """
        抓取郑州商品交易所注册仓单数据
        适用20100825(包括)至20151111(包括)
        Parameters
        ------
            date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
            vars_list: 合约品种如CF、TA等列表 为空时为所有商品
        Return
        -------
            DataFrame:
                展期收益率数据(DataFrame):
                    var             商品品种                     string
                    receipt         仓单数                       int
                    date            日期                         string YYYYMMDD
    """
    date = cons.convert_date(date).strftime('%Y%m%d') if date is not None else datetime.date.today()
    if date not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    url = cons.CZCE_RECEIPT_URL_2 % (date[:4], date)
    r = requests.get(url)
    r.encoding = 'utf-8'
    data = pd.read_html(r.text)[3:]
    records = pd.DataFrame()
    for data_cut in data:
        if len(data_cut.columns) > 3:
            last_indexes = [x for x in data_cut.index if '注：' in str(data_cut[0].tolist()[x])]
            if len(last_indexes) > 0:
                last_index = last_indexes[0] - 1
                data_cut = data_cut.loc[:last_index, :]
            if 'PTA' in data_cut[0].tolist()[0]:
                var = 'TA'
            else:
                strings = data_cut[0].tolist()[0]
                string = strings.split(' ')[0][3:]
                var = chinese_to_english(re.sub(r'[A-Z]+', '', string))
            data_cut.columns = data_cut.T[1].tolist()
            receipt = data_cut['仓单数量'].tolist()[-1]
            receipt_chg = data_cut['当日增减'].tolist()[-1]
            data_dict = {'var': var, 'receipt': int(receipt), 'receipt_chg': int(receipt_chg), 'date': date}
            records = records.append(pd.DataFrame(data_dict, index=[0]))
    if len(records.index) != 0:
        records.index = records['var']
        vars_in_market = [i for i in vars_list if i in records.index]
        records = records.loc[vars_in_market, :]
    return records.reset_index(drop=True)


def get_czce_receipt_3(date: str = None, vars_list: List = cons.contract_symbols):
    """
    抓取郑州商品交易所注册仓单数据
    适用20151112(包括)至今
    Parameters
    ------
        date: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
        vars_list: 合约品种如CF、TA等列表 为空时为所有商品
    Return
    -------
        DataFrame:
            展期收益率数据(DataFrame):`1
                var             商品品种                     string
                receipt         仓单数                       int
                date            日期                         string YYYYMMDD
    """

    date = cons.convert_date(date).strftime('%Y%m%d') if date is not None else datetime.date.today()
    if date not in calendar:
        warnings.warn('%s非交易日' % date.strftime('%Y%m%d'))
        return None
    url = cons.CZCE_RECEIPT_URL_3 % (date[:4], date)
    r = requests_link(url, encoding='utf-8')
    r.encoding = 'utf-8'
    data = pd.read_html(r.text, encoding='gb2312')
    records = pd.DataFrame()
    if len(data) < 4:
        return records
    if int(date) <= 20171227:
        data = data[1:]
    for data_cut in data:
        if len(data_cut.columns) > 3 and len(data_cut.index) > 7:
            last_indexes = [x for x in data_cut.index if '注：' in str(data_cut[0].tolist()[x])]
            if len(last_indexes) > 0:
                last_index = last_indexes[0] - 1
                data_cut = data_cut.loc[:last_index, :]
            if 'PTA' in data_cut[0].tolist()[0]:
                var = 'TA'
            else:
                strings = data_cut[0].tolist()[0]
                string = strings.split(' ')[0][3:]
                if len(string) > 7:
                    continue
                print(string)
                var = chinese_to_english(re.sub('[A-Z]+', '', string))
            data_cut.columns = data_cut.loc[1, :]
            data_cut = data_cut.fillna(method='pad')
            try:
                receipt = data_cut.loc[:, '仓单数量'].tolist()[-1]
            except:
                receipt = data_cut.loc[:, '仓单数量(保税)'].tolist()[-1]
            receipt_chg = data_cut.loc[:, '当日增减'].tolist()[-1]
            data_dict = {'var': var, 'receipt': int(receipt), 'receipt_chg': int(receipt_chg), 'date': date}
            records = records.append(pd.DataFrame(data_dict, index=[0]))
    if len(records.index) != 0:
        records.index = records['var']
        vars_in_market = [i for i in vars_list if i in records.index]
        records = records.loc[vars_in_market, :]
    return records.reset_index(drop=True)


def get_receipt(start_day: str = None, end_day: str = None, vars_list: List = cons.contract_symbols):
    """
    大宗商品注册仓单数量
    :param start_day: 开始日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :type start_day: str
    :param end_day: 结束数据 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天
    :type end_day: str
    :param vars_list: 合约品种如RB、AL等列表 为空时为所有商品
    :type vars_list: str
    :return: 展期收益率数据
    :rtype: pandas.DataFrame
    """
    start_day = cons.convert_date(start_day) if start_day is not None else datetime.date.today()
    end_day = cons.convert_date(end_day) if end_day is not None else cons.convert_date(
        cons.get_latest_data_date(datetime.datetime.now()))
    records = pd.DataFrame()
    while start_day <= end_day:
        if start_day.strftime('%Y%m%d') not in calendar:
            warnings.warn(f"{start_day.strftime('%Y%m%d')}非交易日")
        else:
            print(start_day)
            for market, market_vars in cons.market_exchange_symbols.items():

                if market == 'dce':
                    if start_day >= datetime.date(2009, 4, 7):
                        f = get_dce_receipt
                    else:
                        print('20090407起，dce每交易日更新仓单数据')
                        f = None
                elif market == 'shfe':
                    if datetime.date(2008, 10, 6) <= start_day <= datetime.date(2014, 5, 16):
                        f = get_shfe_receipt_1
                    elif start_day > datetime.date(2014, 5, 16):
                        f = get_shfe_receipt_2
                    else:
                        f = None
                        print('20081006起，shfe每交易日更新仓单数据')
                elif market == 'czce':
                    if datetime.date(2008, 3, 3) <= start_day <= datetime.date(2010, 8, 24):
                        f = get_czce_receipt_1
                    elif datetime.date(2010, 8, 24) < start_day <= datetime.date(2015, 11, 11):
                        f = get_czce_receipt_2
                    elif start_day > datetime.date(2015, 11, 11):
                        f = get_czce_receipt_3
                    else:
                        f = None
                        print('20080303起，czce每交易日更新仓单数据')
                get_vars = [var for var in vars_list if var in market_vars]
                if market != 'cffex' and get_vars != []:
                    if f is not None:
                        records = records.append(f(start_day, get_vars))

        start_day += datetime.timedelta(days=1)
    records.reset_index(drop=True, inplace=True)
    if records.empty:
        return records
    if "MA" in records["var"].to_list():
        replace_index = records[records["var"] == "MA"]["receipt"].astype(str).str.split("0", expand=True)[0].index
        records.loc[replace_index, "receipt"] = records[records["var"] == "MA"]["receipt"].astype(str).str.split("0", expand=True)[0]
    return records


if __name__ == '__main__':
    get_receipt_df = get_receipt(start_day='20201022', end_day='20201022', vars_list=["RB"])
    print(get_receipt_df)
