# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
contact: jindaxiang@163.com
desc: 常用变量
"""
import re
import datetime
import json
import os

QHKC_URL = "https://www.qhkch.com/ajax/index_show.php"

# 键值对: 键为交易所代码, 值为具体合约代码, TODO 需要及时补充新增的品种
market_exchange_symbols = {
    'cffex': [
        'IF',
        'IC',
        'IH',
        'T',
        'TF',
        'TS'],
    'dce': [
        'C',
        'CS',
        'A',
        'B',
        'M',
        'Y',
        'P',
        'FB',
        'BB',
        'JD',
        'L',
        'V',
        'PP',
        'J',
        'JM',
        'I',
        'EG'],
    'czce': [
        'WH',
        'PM',
        'CF',
        'SR',
        'TA',
        'OI',
        'RI',
        'MA',
        'ME',
        'FG',
        'RS',
        'RM',
        'ZC',
        'JR',
        'LR',
        'SF',
        'SM',
        'WT',
        'TC',
        'GN',
        'RO',
        'ER',
        'SRX',
        'SRY',
        'WSX',
        'WSY',
        'CY',
        'AP',
        "UR"],
    'shfe': [
        'CU',
        'AL',
        'ZN',
        'PB',
        'NI',
        'SN',
        'AU',
        'AG',
        'RB',
        'WR',
        'HC',
        'FU',
        'BU',
        'RU',
        'SC',
        'SP']}

contract_symbols = []
[contract_symbols.extend(i) for i in market_exchange_symbols.values()]

headers = {
    'Host': 'www.czce.com.cn',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'DNT': '1',
    'Referer': 'http://www.super-ping.com/?ping=www.google.com&locale=sc',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6'}

shfe_headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

dce_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Content-Length": "71",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "www.dce.com.cn",
    "Origin": "http://www.dce.com.cn",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://www.dce.com.cn/publicweb/quotesdata/weekQuotesCh.html",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}

SYS_SPOT_PRICE_URL = 'http://www.100ppi.com/sf/day-{}.html'
SYS_SPOT_PRICE_LATEST_URL = 'http://www.100ppi.com/sf/'

SHFE_VOL_RANK_URL = 'http://www.shfe.com.cn/data/dailydata/kx/pm%s.dat'
CFFEX_VOL_RANK_URL = 'http://www.cffex.com.cn/fzjy/ccpm/%s/%s/%s_1.csv'
DCE_VOL_RANK_URL = 'http://www.dce.com.cn/publicweb/quotesdata/exportMemberDealPosiQuotesData.html?memberDealPosiQuotes.variety=%s&memberDealPosiQuotes.trade_type=0&contract.contract_id=all&contract.variety_id=%s&year=%s&month=%s&day=%s&exportFlag=txt'
CZCE_VOL_RANK_URL_1 = 'http://www.czce.com.cn/cn/exchange/jyxx/pm/pm%s.html'
CZCE_VOL_RANK_URL_2 = 'http://www.czce.com.cn/cn/exchange/%s/datatradeholding/%s.htm'
CZCE_VOL_RANK_URL_3 = 'http://www.czce.com.cn/cn/DFSStaticFiles/Future/%s/%s/FutureDataHolding.htm'

DCE_RECEIPT_URL = "http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html"
SHFE_RECEIPT_URL_1 = 'http://www.shfe.com.cn/data/dailydata/%sdailystock.html'
SHFE_RECEIPT_URL_2 = 'http://www.shfe.com.cn/data/dailydata/%sdailystock.dat'
CZCE_RECEIPT_URL_1 = 'http://www.czce.com.cn/cn/exchange/jyxx/sheet/sheet%s.html'
CZCE_RECEIPT_URL_2 = 'http://www.czce.com.cn/cn/exchange/%s/datawhsheet/%s.htm'
CZCE_RECEIPT_URL_3 = 'http://www.czce.com.cn/cn/DFSStaticFiles/Future/%s/%s/FutureDataWhsheet.htm'

CFFEX_DAILY_URL = 'http://www.cffex.com.cn/fzjy/mrhq/{}/{}/{}_1.csv'
SHFE_DAILY_URL = 'http://www.shfe.com.cn/data/dailydata/kx/kx%s.dat'
SHFE_V_WAP_URL = 'http://www.shfe.com.cn/data/dailydata/ck/%sdailyTimePrice.dat'
DCE_DAILY_URL = 'http://www.dce.com.cn//publicweb/quotesdata/dayQuotesCh.html'
CZCE_DAILY_URL_1 = 'http://www.czce.com.cn/cn/exchange/jyxx/hq/hq%s.html'
CZCE_DAILY_URL_2 = 'http://www.czce.com.cn/cn/exchange/%s/datadaily/%s.txt'
CZCE_DAILY_URL_3 = 'http://www.czce.com.cn/cn/DFSStaticFiles/Future/%s/%s/FutureDataDaily.txt'

DATE_PATTERN = re.compile(r'^([0-9]{4})[-/]?([0-9]{2})[-/]?([0-9]{2})')
FUTURES_SYMBOL_PATTERN = re.compile(r'(^[A-Za-z]{1,2})[0-9]+')

CFFEX_COLUMNS = [
    'open',
    'high',
    'low',
    'volume',
    'turnover',
    'open_interest',
    'close',
    'settle',
    'change1',
    'change2']

CZCE_COLUMNS = [
    'pre_settle',
    'open',
    'high',
    'low',
    'close',
    'settle',
    'change1',
    'change2',
    'volume',
    'open_interest',
    'oi_chg',
    'turnover',
    'final_settle']

CZCE_COLUMNS_2 = [
    'pre_settle',
    'open',
    'high',
    'low',
    'close',
    'settle',
    'change1',
    'volume',
    'open_interest',
    'oi_chg',
    'turnover',
    'final_settle']

SHFE_COLUMNS = {
    'CLOSEPRICE': 'close',
    'HIGHESTPRICE': 'high',
    'LOWESTPRICE': 'low',
    'OPENINTEREST': 'open_interest',
    'OPENPRICE': 'open',
    'PRESETTLEMENTPRICE': 'pre_settle',
    'SETTLEMENTPRICE': 'settle',
    'VOLUME': 'volume'}

SHFE_V_WAP_COLUMNS = {
    ':B1': 'date',
    'INSTRUMENT_ID': 'symbol',
    'TIME': 'time_range',
    'REF_SETTLEMENT_PRICE': 'v_wap'}

DCE_COLUMNS = [
    'open',
    'high',
    'low',
    'close',
    'pre_settle',
    'settle',
    'change1',
    'change2',
    'volume',
    'open_interest',
    'oi_chg',
    'turnover']

DCE_OPTION_COLUMNS = [
    'open',
    'high',
    'low',
    'close',
    'pre_settle',
    'settle',
    'change1',
    'change2',
    'delta',
    'volume',
    'open_interest',
    'oi_chg',
    'turnover',
    'exercise_volume']

OUTPUT_COLUMNS = [
    'symbol',
    'date',
    'open',
    'high',
    'low',
    'close',
    'volume',
    'open_interest',
    'turnover',
    'settle',
    'pre_settle',
    'variety']

OPTION_OUTPUT_COLUMNS = [
    'symbol',
    'date',
    'open',
    'high',
    'low',
    'close',
    'pre_settle',
    'settle',
    'delta',
    'volume',
    'open_interest',
    'oi_chg',
    'turnover',
    'implied_volatility',
    'exercise_volume',
    'variety']

DCE_MAP = {
    '豆一': 'A',
    '豆二': 'B',
    '豆粕': 'M',
    '豆油': 'Y',
    '棕榈油': 'P',
    '玉米': 'C',
    '玉米淀粉': 'CS',
    '鸡蛋': 'JD',
    '纤维板': 'FB',
    '胶合板': 'BB',
    '聚乙烯': 'L',
    '聚氯乙烯': 'V',
    '聚丙烯': 'PP',
    '焦炭': 'J',
    '焦煤': 'JM',
    '铁矿石': 'I',
    '乙二醇': 'EG'
}


def convert_date(date):
    """
    transform a date string to datetime.date object
    :param date, string, e.g. 2016-01-01, 20160101 or 2016/01/01
    :return: object of datetime.date(such as 2016-01-01) or None
    """
    if isinstance(date, datetime.date):
        return date
    elif isinstance(date, str):
        match = DATE_PATTERN.match(date)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                return datetime.date(
                    year=int(
                        groups[0]), month=int(
                        groups[1]), day=int(
                        groups[2]))
    return None


def get_json_path(name, module_file):
    """
    获取 JSON 配置文件的路径(从模块所在目录查找)
    :param name: 文件名
    :param module_file:
    :return: str json_file_path
    """
    module_folder = os.path.abspath(os.path.dirname(module_file))
    module_json_path = os.path.join(module_folder, '.', name)
    return module_json_path


def get_calendar():
    """
    获取交易日历至 2019 年结束, 这里的交易日历需要按年更新
    :return: json
    """
    setting_file_name = 'calendar.json'
    setting_file_path = get_json_path(setting_file_name, __file__)
    return json.load(open(setting_file_path, "r"))


def last_trading_day(day):
    """
    获取前一个交易日
    :param day: '%Y%m%d' or  datetime.date()
    :return last_day: '%Y%m%d' or  datetime.date()
    """
    calendar = get_calendar()

    if isinstance(day, str):
        if day not in calendar:
            print('Today is not trading day：' + day)
            return False
        pos = calendar.index(day)
        last_day = calendar[pos - 1]
        return last_day

    elif isinstance(day, datetime.date):
        d_str = day.strftime('%Y%m%d')
        if d_str not in calendar:
            print('Today is not working day：' + d_str)
            return False
        pos = calendar.index(d_str)
        last_day = calendar[pos - 1]
        last_day = datetime.datetime.strptime(last_day, '%Y%m%d').date()
        return last_day


def get_latest_data_date(day):
    """
    获取最新的有数据的交易日
    :param day: datetime.datetime()
    :return string YYYYMMDD
    """
    calendar = get_calendar()
    if day.strftime('%Y%m%d') in calendar:
        if day.time() > datetime.time(17, 0, 0):
            return day.strftime('%Y%m%d')
        else:
            return last_trading_day(day.strftime('%Y%m%d'))
    else:
        while day.strftime('%Y%m%d') not in calendar:
            day = day - datetime.timedelta(days=1)
        return day.strftime('%Y%m%d')


if __name__ == '__main__':
    d = datetime.datetime(2018, 10, 5, 17, 1, 0)
    print(get_latest_data_date(d))
