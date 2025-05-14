# coding:utf-8

import datetime as dt
import json
import os
import sys
import time
import traceback

from . import xtbson as bson
from . import xtutil

__all__ = [
    'subscribe_quote',
    'subscribe_whole_quote',
    'unsubscribe_quote',
    'run',
    'get_market_data',
    'get_local_data',
    'get_full_tick',
    'get_divid_factors',
    'get_l2_quote',
    'get_l2_order',
    'get_l2_transaction',
    'download_history_data',
    'get_financial_data',
    'download_financial_data',
    'get_instrument_detail',
    'get_instrument_type',
    'get_trading_dates',
    'get_sector_list',
    'get_stock_list_in_sector',
    'download_sector_data',
    'add_sector',
    'remove_sector',
    'get_index_weight',
    'download_index_weight',
    'get_holidays',
    'get_trading_calendar',
    'get_trading_time',
    'get_etf_info',
    'download_etf_info',
    'get_main_contract',
    'download_history_contracts',
    'download_cb_data',
    'get_cb_info',
    'create_sector_folder',
    'create_sector',
    'remove_stock_from_sector',
    'reset_sector',
    'get_period_list',
    'download_his_st_data',
]


def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            exc_type, exc_instance, exc_traceback = sys.exc_info()
            formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
            message = '\n{0} raise {1}:{2}'.format(
                formatted_traceback,
                exc_type.__name__,
                exc_instance
            )
            # raise exc_type(message)
            # print(message)
            return None

    return wrapper


### config

debug_mode = 0

default_data_dir = '../userdata_mini/datadir'
data_dir = default_data_dir

enable_hello = True

### connection

__client = None
__client_last_spec = ('', None)

__hk_broke_info = {}
__download_version = None


def connect(ip='', port=None, remember_if_success=True):
    global __client
    global data_dir
    global __download_version

    if __client:
        if __client.is_connected():
            return __client

        __client.shutdown()
        __client = None
        data_dir = default_data_dir

    from . import xtconn

    if not ip:
        ip = 'localhost'

    if port:
        server_list = [f'{ip}:{port}']
        __client = xtconn.connect_any(server_list)
    else:
        server_list = xtconn.scan_available_server()

        default_addr = 'localhost:58610'
        if not default_addr in server_list:
            server_list.append(default_addr)

        __client = xtconn.connect_any(server_list)

    if not __client or not __client.is_connected():
        raise Exception("无法连接xtquant服务，请检查QMT-投研版或QMT-极简版是否开启")

    if remember_if_success:
        global __client_last_spec
        __client_last_spec = (ip, port)

    data_dir = __client.get_data_dir()
    if data_dir == "":
        data_dir = os.path.join(__client.get_app_dir(), default_data_dir)

    data_dir = os.path.abspath(data_dir)

    try:
        __download_version = __bsoncall_common(
            __client.commonControl, 'getapiversion', {}
        ).get('downloadversion', None)
    except:
        pass

    hello()
    return __client


def reconnect(ip='', port=None, remember_if_success=True):
    global __client
    global data_dir

    if __client:
        __client.shutdown()
        __client = None
        data_dir = default_data_dir

    return connect(ip, port, remember_if_success)


def get_client():
    global __client

    if not __client or not __client.is_connected():
        global __client_last_spec

        ip, port = __client_last_spec
        __client = connect(ip, port, False)

    return __client


def hello():
    global __client
    global enable_hello

    if not enable_hello:
        return

    server_info = None
    peer_addr = None
    data_dir = None

    try:
        server_info = bson.BSON.decode(__client.get_server_tag())
        peer_addr = __client.get_peer_addr()
        data_dir = __client.get_data_dir()
    except Exception as e:
        pass

    print(
        f'''***** xtdata连接成功 *****
服务信息: {server_info}
服务地址: {peer_addr}
数据路径: {data_dir}
设置xtdata.enable_hello = False可隐藏此消息
'''
    )
    return


__meta_field_list = {}


def get_field_list(metaid):
    global __meta_field_list

    if not __meta_field_list:
        x = open(os.path.join(os.path.dirname(__file__), 'config', 'metaInfo.json'), 'r', encoding="utf-8").read()
        metainfo = eval(x)

        for meta in metainfo:
            filed_dict = {}
            metadetail = metainfo.get(str(meta), {})
            filed = metadetail.get('fields', {})
            for key in filed:
                filed_dict[key] = filed[key].get('desc', key)

            filed_dict['G'] = 'time'
            filed_dict['S'] = 'stock'
            __meta_field_list[meta] = filed_dict

    return __meta_field_list.get(str(metaid), {})


### utils

def create_array(shape, dtype_tuple, capsule, size):
    import numpy as np
    import ctypes

    ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.POINTER(ctypes.c_char)
    ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object, ctypes.c_char_p]
    buff = ctypes.pythonapi.PyCapsule_GetPointer(capsule, None)
    base_type = size * buff._type_

    for dim in shape[::-1]:
        base_type = dim * base_type
    p_arr_type = ctypes.POINTER(base_type)
    obj = ctypes.cast(buff, p_arr_type).contents
    obj._base = capsule
    return np.ndarray(shape=shape, dtype=np.dtype(dtype_tuple), buffer=obj)


from .xtdatacenter import register_create_nparray

register_create_nparray(create_array)


def __bsoncall_common(interface, func, param):
    return bson.BSON.decode(interface(func, bson.BSON.encode(param)))


### function

def get_stock_list_in_sector(sector_name):
    '''
    获取板块成份股，支持客户端左侧板块列表中任意的板块，包括自定义板块
    :param sector_name: (str)板块名称
    :return: list
    '''
    client = get_client()
    return client.get_stock_list_in_sector(sector_name, 0)


def get_index_weight(index_code):
    '''
    获取某只股票在某指数中的绝对权重
    :param index_code: (str)指数名称
    :return: dict
    '''
    client = get_client()
    return client.get_weight_in_index(index_code)


def get_financial_data(stock_list, table_list=[], start_time='', end_time='', report_type='report_time'):
    '''
     获取财务数据
    :param stock_list: (list)合约代码列表
    :param table_list: (list)报表名称列表
    :param start_time: (str)起始时间
    :param end_time: (str)结束时间
    :param report_type: (str) 时段筛选方式 'announce_time' / 'report_time'
    :return:
        field: list[str]
        date: list[int]
        stock: list[str]
        value: list[list[float]]
    '''
    client = get_client()
    all_table = {
        'Balance': 'ASHAREBALANCESHEET'
        , 'Income': 'ASHAREINCOME'
        , 'CashFlow': 'ASHARECASHFLOW'
        , 'Capital': 'CAPITALSTRUCTURE'
        , 'HolderNum': 'SHAREHOLDER'
        , 'Top10Holder': 'TOP10HOLDER'
        , 'Top10FlowHolder': 'TOP10FLOWHOLDER'
        , 'PershareIndex': 'PERSHAREINDEX'
    }

    if not table_list:
        table_list = list(all_table.keys())

    all_table_upper = {table.upper(): all_table[table] for table in all_table}
    req_list = []
    names = {}
    for table in table_list:
        req_table = all_table_upper.get(table.upper(), table)
        req_list.append(req_table)
        names[req_table] = table

    data = {}
    sl_len = 20
    stock_list2 = [stock_list[i: i + sl_len] for i in range(0, len(stock_list), sl_len)]
    for sl in stock_list2:
        data2 = client.get_financial_data(sl, req_list, start_time, end_time, report_type)
        for s in data2:
            data[s] = data2[s]

    import time
    import math
    def conv_date(data, key, key2):
        if key in data:
            tmp_data = data[key]
            if math.isnan(tmp_data):
                if key2 not in data or math.isnan(data[key2]):
                    data[key] = ''
                else:
                    tmp_data = data[key2]
            data[key] = time.strftime('%Y%m%d', time.localtime(tmp_data / 1000))
        return

    result = {}
    import pandas as pd
    for stock in data:
        stock_data = data[stock]
        result[stock] = {}
        for table in stock_data:
            table_data = stock_data[table]
            for row_data in table_data:
                conv_date(row_data, 'm_anntime', 'm_timetag')
                conv_date(row_data, 'm_timetag', '')
                conv_date(row_data, 'declareDate', '')
                conv_date(row_data, 'endDate', '')
            result[stock][names[table]] = pd.DataFrame(table_data)
    return result


def get_market_data_ori(
        field_list=[], stock_list=[], period='1d'
        , start_time='', end_time='', count=-1
        , dividend_type='none', fill_data=True, enable_read_from_server=True
        , data_dir=''
):
    client = get_client()
    enable_read_from_local = period in {'1m', '5m', '15m', '30m', '1h', '1d', 'tick', '1w', '1mon', '1q', '1hy', '1y'}
    global debug_mode
    return client.get_market_data3(field_list, stock_list, period, start_time, end_time, count, dividend_type,
                                   fill_data, 'v2', enable_read_from_local, enable_read_from_server, debug_mode,
                                   data_dir)


def get_market_data(
        field_list=[], stock_list=[], period='1d'
        , start_time='', end_time='', count=-1
        , dividend_type='none', fill_data=True
):
    '''
    获取历史行情数据
    :param field_list: 行情数据字段列表，[]为全部字段
        K线可选字段：
            "time"                #时间戳
            "open"                #开盘价
            "high"                #最高价
            "low"                 #最低价
            "close"               #收盘价
            "volume"              #成交量
            "amount"              #成交额
            "settle"              #今结算
            "openInterest"        #持仓量
        分笔可选字段：
            "time"                #时间戳
            "lastPrice"           #最新价
            "open"                #开盘价
            "high"                #最高价
            "low"                 #最低价
            "lastClose"           #前收盘价
            "amount"              #成交总额
            "volume"              #成交总量
            "pvolume"             #原始成交总量
            "stockStatus"         #证券状态
            "openInt"             #持仓量
            "lastSettlementPrice" #前结算
            "askPrice1", "askPrice2", "askPrice3", "askPrice4", "askPrice5" #卖一价~卖五价
            "bidPrice1", "bidPrice2", "bidPrice3", "bidPrice4", "bidPrice5" #买一价~买五价
            "askVol1", "askVol2", "askVol3", "askVol4", "askVol5"           #卖一量~卖五量
            "bidVol1", "bidVol2", "bidVol3", "bidVol4", "bidVol5"           #买一量~买五量
    :param stock_list: 股票代码 "000001.SZ"
    :param period: 周期 分笔"tick" 分钟线"1m"/"5m"/"15m" 日线"1d"
        Level2行情快照"l2quote" Level2行情快照补充"l2quoteaux" Level2逐笔委托"l2order" Level2逐笔成交"l2transaction" Level2大单统计"l2transactioncount" Level2委买委卖队列"l2orderqueue"
        Level1逐笔成交统计一分钟“transactioncount1m” Level1逐笔成交统计日线“transactioncount1d”
        期货仓单“warehousereceipt” 期货席位“futureholderrank” 互动问答“interactiveqa”
    :param start_time: 起始时间 "20200101" "20200101093000"
    :param end_time: 结束时间 "20201231" "20201231150000"
    :param count: 数量 -1全部/n: 从结束时间向前数n个
    :param dividend_type: 除权类型"none" "front" "back" "front_ratio" "back_ratio"
    :param fill_data: 对齐时间戳时是否填充数据，仅对K线有效，分笔周期不对齐时间戳
        为True时，以缺失数据的前一条数据填充
            open、high、low、close 为前一条数据的close
            amount、volume为0
            settle、openInterest 和前一条数据相同
        为False时，缺失数据所有字段填NaN
    :return: 数据集，分笔数据和K线数据格式不同
        period为'tick'时：{stock1 : value1, stock2 : value2, ...}
            stock1, stock2, ... : 合约代码
            value1, value2, ... : np.ndarray 数据列表，按time增序排列
        period为其他K线周期时：{field1 : value1, field2 : value2, ...}
            field1, field2, ... : 数据字段
            value1, value2, ... : pd.DataFrame 字段对应的数据，各字段维度相同，index为stock_list，columns为time_list
    '''
    if period in {'1m', '5m', '15m', '30m', '1h', '1d', '1w', '1mon', '1q', '1hy', '1y'}:
        import pandas as pd
        index, data = get_market_data_ori(field_list, stock_list, period, start_time, end_time, count, dividend_type,
                                          fill_data)

        result = {}
        for field in data:
            result[field] = pd.DataFrame(data[field], index=index[0], columns=index[1])
        return result

    return get_market_data_ori(field_list, stock_list, period, start_time, end_time, count, dividend_type, fill_data)


def get_market_data_ex_ori(
        field_list=[], stock_list=[], period='1d'
        , start_time='', end_time='', count=-1
        , dividend_type='none', fill_data=True, enable_read_from_server=True
        , data_dir=''
):
    client = get_client()
    enable_read_from_local = period in {'1m', '5m', '15m', '30m', '1h', '1d', 'tick', '1w', '1mon', '1q', '1hy', '1y'}
    global debug_mode
    return client.get_market_data3(field_list, stock_list, period, start_time, end_time, count, dividend_type,
                                   fill_data, 'v3', enable_read_from_local, enable_read_from_server, debug_mode,
                                   data_dir)


def get_market_data_ex(
        field_list=[], stock_list=[], period='1d'
        , start_time='', end_time='', count=-1
        , dividend_type='none', fill_data=True
):
    if period == 'hkbrokerqueue' or period == 'hkbrokerqueue2' or period == (1820, 0):
        showbrokename = period == 'hkbrokerqueue2'
        return get_broker_queue_data(stock_list, start_time, end_time, count, showbrokename)

    period = _get_tuple_period(period) or period
    if isinstance(period, tuple):
        return _get_market_data_ex_tuple_period(field_list, stock_list, period, start_time, end_time, count,
                                                dividend_type, fill_data)

    if period in {'1m', '5m', '15m', '30m', '1h', '1d', '1w', '1mon', '1q', '1hy', '1y'}:
        return _get_market_data_ex_ori_221207(field_list, stock_list, period, start_time, end_time, count,
                                              dividend_type, fill_data)

    import pandas as pd
    result = {}

    ifield = 'time'
    query_field_list = field_list if (not field_list) or (ifield in field_list) else [ifield] + field_list
    ori_data = get_market_data_ex_ori(query_field_list, stock_list, period, start_time, end_time, count, dividend_type,
                                      fill_data)

    if not ori_data:
        return result

    fl = field_list
    stime_fmt = '%Y%m%d' if period == '1d' else '%Y%m%d%H%M%S'
    if fl:
        fl2 = fl if ifield in fl else [ifield] + fl
        for s in ori_data:
            sdata = pd.DataFrame(ori_data[s], columns=fl2)
            sdata2 = sdata[fl]
            sdata2.index = [timetag_to_datetime(t, stime_fmt) for t in sdata[ifield]]
            result[s] = sdata2
    else:
        needconvert, metaid = _needconvert_period(period)
        if needconvert:
            convert_field_list = get_field_list(metaid)

            for s in ori_data:
                odata = ori_data[s]
                if convert_field_list:
                    convert_data_list = []
                    for data in odata:
                        convert_data = _convert_component_info(data, convert_field_list)
                        convert_data_list.append(convert_data)
                    odata = convert_data_list

                sdata = pd.DataFrame(odata)
                sdata.index = [timetag_to_datetime(t, stime_fmt) for t in sdata[ifield]]
                result[s] = sdata
        else:
            for s in ori_data:
                sdata = pd.DataFrame(ori_data[s])
                sdata.index = [timetag_to_datetime(t, stime_fmt) for t in sdata[ifield]]
                result[s] = sdata

    return result


def _get_market_data_ex_ori_221207(
        field_list=[], stock_list=[], period='1d'
        , start_time='', end_time='', count=-1
        , dividend_type='none', fill_data=True, enable_read_from_server=True
        , data_dir=''
):
    import numpy as np
    import pandas as pd
    client = get_client()
    enable_read_from_local = period in {'1m', '5m', '15m', '30m', '1h', '1d', 'tick', '1w', '1mon', '1q', '1hy', '1y'}
    global debug_mode
    ret = client.get_market_data3(field_list, stock_list, period, start_time, end_time, count, dividend_type, fill_data,
                                  'v4', enable_read_from_local,
                                  enable_read_from_server, debug_mode, data_dir)
    result = {}
    for stock, index, npdatas in ret:
        data = {field: np.frombuffer(b, fi) for field, fi, b in npdatas}
        result[stock] = pd.DataFrame(data=data, index=index)
    return result


def _get_market_data_ex_221207(
        field_list=[], stock_list=[], period='1d'
        , start_time='', end_time='', count=-1
        , dividend_type='none', fill_data=True, enable_read_from_server=True
):
    ifield = 'time'
    query_field_list = field_list if (not field_list) or (ifield in field_list) else [ifield] + field_list

    if period in {'1m', '5m', '15m', '30m', '1h', '1d', '1w', '1mon', '1q', '1hy', '1y'}:
        ori_data = _get_market_data_ex_ori_221207(query_field_list, stock_list, period, start_time, end_time, count,
                                                  dividend_type, fill_data, enable_read_from_server)
    else:
        ori_data = get_market_data_ex_ori(query_field_list, stock_list, period, start_time, end_time, count,
                                          dividend_type, fill_data, enable_read_from_server)

    import pandas as pd
    result = {}

    fl = field_list

    if fl:
        fl2 = fl if ifield in fl else [ifield] + fl
        for s in ori_data:
            sdata = pd.DataFrame(ori_data[s], columns=fl2)
            sdata2 = sdata[fl]
            sdata2.index = pd.to_datetime((sdata[ifield] + 28800000) * 1000000)
            result[s] = sdata2
    else:
        for s in ori_data:
            sdata = pd.DataFrame(ori_data[s])
            sdata.index = pd.to_datetime((sdata[ifield] + 28800000) * 1000000)
            result[s] = sdata

    return result


get_market_data3 = _get_market_data_ex_221207


def _get_data_file_path(stocklist, period, date='20380119'):
    if isinstance(period, tuple):
        metaid, periodNum = period
        periodstr = ''
    else:
        periodstr = period
        metaid = -1
        periodNum = -1

    data = {
        'stocklist': stocklist
        , 'period': periodstr
        , 'metaid': metaid
        , 'periodNum': periodNum
        , 'date': date
    }

    client = get_client()

    path_result = __bsoncall_common(
        client.commonControl, 'getdatafilepath'
        , data
    )
    return path_result.get('result', {})


__TUPLE_PERIODS = {
    'warehousereceipt': (4015, 86400000)
    , 'futureholderrank': (5008, 86400000)
    , 'interactiveqa': (7011, 86400000)
    , 'northfinancechange1m': (3006, 60000)
    , 'northfinancechange1d': (3006, 86400000)
    , 'dividendplaninfo': (2025, 86401000)
    , 'etfredemptionlist': (2004, 86401000)
    , 'stoppricedata': (9506, 86400000)
    , 'historymaincontract': (5004, 86400000)
    , 'brokerqueue': (1820, 0)
    , 'brokerqueue2': (1820, 0)
    , 'brokerinfo': (2038, 86401000)
    , 'delistchangebond': (4020, 86401000)
    , 'replacechangebond': (4021, 86401000)
}

__STR_PERIODS = {
    (3001, 60000): '1m'
    , (3001, 300000): '5m'
    , (3001, 900000): '15m'
    , (3001, 1800000): '30m'
    , (3001, 3600000): '1h'
    , (3001, 86400000): '1d'
}


def _needconvert_period(period):
    datas = {
        'snapshotindex': 3004
    }
    return period in datas, datas.get(period, -1)


def _get_tuple_period(period):
    if isinstance(period, tuple):
        return __STR_PERIODS.get(period, None)
    else:
        return __TUPLE_PERIODS.get(period, None)


def _get_market_data_ex_tuple_period_ori(
        stock_list=[], period=()
        , start_time='', end_time=''
        , count=-1
):
    client = get_client()

    data_path_dict = _get_data_file_path(stock_list, period)

    ori_data = {}
    for stockcode in data_path_dict:
        file_name = data_path_dict[stockcode]
        data_list = bson.BSON.decode(client.read_local_data(file_name, start_time, end_time, count)).get('result')
        ori_data[stockcode] = data_list

    return ori_data


def _convert_component_info(data, convert_field_list):
    if not isinstance(data, dict):
        return data

    new_data = {}
    for key, value in data.items():
        name = convert_field_list.get(key, key)
        if isinstance(value, dict):
            new_data[name] = _convert_component_info(value, convert_field_list)
        elif isinstance(value, list):
            new_data[name] = [_convert_component_info(item, convert_field_list) for item in value]
        else:
            new_data[name] = value

    return new_data


def _get_market_data_ex_tuple_period(
        field_list=[], stock_list=[], period='1d'
        , start_time='', end_time='', count=-1
        , dividend_type='none', fill_data=True, enable_read_from_server=True
):
    if not isinstance(period, tuple):
        return {}

    all_data = _get_market_data_ex_tuple_period_ori(stock_list, period, start_time, end_time, count)

    metaid, periodNum = period
    convert_field_list = get_field_list(metaid)

    import pandas as pd

    ori_data = {}
    for stockcode, data_list in all_data.items():
        if convert_field_list:
            convert_data_list = []
            for data in data_list:
                convert_data = _convert_component_info(data, convert_field_list)
                convert_data_list.append(convert_data)
            data_list = convert_data_list
        ori_data[stockcode] = pd.DataFrame(data_list)

    return ori_data


def get_data_dir():
    cl = get_client()
    return os.path.abspath(cl.get_data_dir())


def get_local_data(field_list=[], stock_list=[], period='1d', start_time='', end_time='', count=-1,
                   dividend_type='none', fill_data=True, data_dir=None):
    if data_dir == None:
        data_dir = ''

    if period in {'1m', '5m', '15m', '30m', '1h', '1d', '1w', '1mon', '1q', '1hy', '1y'}:
        return _get_market_data_ex_ori_221207(field_list, stock_list, period, start_time, end_time, count,
                                              dividend_type, fill_data, False, data_dir)

    import pandas as pd
    result = {}

    ifield = 'time'
    query_field_list = field_list if (not field_list) or (ifield in field_list) else [ifield] + field_list
    ori_data = get_market_data_ex_ori(query_field_list, stock_list, period, start_time, end_time, count, dividend_type,
                                      fill_data, False, data_dir)

    if not ori_data:
        return result

    fl = field_list
    stime_fmt = '%Y%m%d' if period == '1d' else '%Y%m%d%H%M%S'
    if fl:
        fl2 = fl if ifield in fl else [ifield] + fl
        for s in ori_data:
            sdata = pd.DataFrame(ori_data[s], columns=fl2)
            sdata2 = sdata[fl]
            sdata2.index = [timetag_to_datetime(t, stime_fmt) for t in sdata[ifield]]
            result[s] = sdata2
    else:
        for s in ori_data:
            sdata = pd.DataFrame(ori_data[s])
            sdata.index = [timetag_to_datetime(t, stime_fmt) for t in sdata[ifield]]
            result[s] = sdata

    return result


def get_l2_quote(field_list=[], stock_code='', start_time='', end_time='', count=-1):
    '''
    level2实时行情
    '''
    global debug_mode
    client = get_client()
    datas = client.get_market_data3(field_list, [stock_code], 'l2quote', start_time, end_time, count, 'none', False, '',
                                    False, True, debug_mode, '')
    if datas:
        return datas[stock_code]
    return None


def get_l2_order(field_list=[], stock_code='', start_time='', end_time='', count=-1):
    '''
    level2逐笔委托
    '''
    global debug_mode
    client = get_client()
    datas = client.get_market_data3(field_list, [stock_code], 'l2order', start_time, end_time, count, 'none', False, '',
                                    False, True, debug_mode, '')
    if datas:
        return datas[stock_code]
    return None


def get_l2_transaction(field_list=[], stock_code='', start_time='', end_time='', count=-1):
    '''
    level2逐笔成交
    '''
    global debug_mode
    client = get_client()
    datas = client.get_market_data3(field_list, [stock_code], 'l2transaction', start_time, end_time, count, 'none',
                                    False, '', False, True, debug_mode, '')
    if datas:
        return datas[stock_code]
    return None


def get_divid_factors(stock_code, start_time='', end_time=''):
    '''
    获取除权除息日及对应的权息
    :param stock_code: (str)股票代码
    :param date: (str)日期
    :return: pd.DataFrame 数据集
    '''
    client = get_client()
    datas = client.get_divid_factors(stock_code, start_time, end_time)
    import pandas as pd
    datas = pd.DataFrame(datas).T
    return datas


@try_except
def getDividFactors(stock_code, date):
    client = get_client()
    resData = client.get_divid_factors(stock_code, date)
    res = {resData[i]: [resData[i + 1][j] for j in
                        range(0, len(resData[i + 1]), 1)] for i in range(0, len(resData), 2)}
    if isinstance(res, dict):
        for k, v in res.items():
            if isinstance(v, list) and len(v) > 5:
                v[5] = int(v[5])
    return res


def get_main_contract(code_market):
    '''
    获取当前期货主力合约
    :param code_market: (str)股票代码
    :return: str
    '''
    client = get_client()
    return client.get_main_contract(code_market)


def datetime_to_timetag(datetime, format="%Y%m%d%H%M%S"):
    if len(datetime) == 8:
        format = "%Y%m%d"
    timetag = time.mktime(time.strptime(datetime, format))
    return timetag * 1000


def timetag_to_datetime(timetag, format):
    '''
    将毫秒时间转换成日期时间
    :param timetag: (int)时间戳毫秒数
    :param format: (str)时间格式
    :return: str
    '''
    return timetagToDateTime(timetag, format)


@try_except
def timetagToDateTime(timetag, format):
    import time
    timetag = timetag / 1000
    time_local = time.localtime(timetag)
    return time.strftime(format, time_local)


def get_trading_dates(market, start_time='', end_time='', count=-1):
    '''
    根据市场获取交易日列表
    : param market: 市场代码 e.g. 'SH','SZ','IF','DF','SF','ZF'等
    : param start_time: 起始时间 '20200101'
    : param end_time: 结束时间 '20201231'
    : param count: 数据个数，-1为全部数据
    :return list(long) 毫秒数的时间戳列表
    '''
    client = get_client()
    datas = client.get_trading_dates_by_market(market, start_time, end_time, count)
    return datas


def get_full_tick(code_list):
    '''
    获取盘口tick数据
    :param code_list: (list)stock.market组成的股票代码列表
    :return: dict
    {'stock.market': {dict}}
    '''
    client = get_client()
    resp_json = client.get_full_tick(code_list)
    return json.loads(resp_json)


def subscribe_callback_wrapper(callback):
    import traceback
    def subscribe_callback(datas):
        try:
            if type(datas) == bytes:
                datas = bson.BSON.decode(datas)
            if callback:
                callback(datas)
        except:
            print('subscribe callback error:', callback)
            traceback.print_exc()

    return subscribe_callback


def subscribe_callback_wrapper_1820(callback):
    import traceback
    def subscribe_callback(datas):
        try:
            if type(datas) == bytes:
                datas = bson.BSON.decode(datas)
            datas = _covert_hk_broke_data(datas)
            if callback:
                callback(datas)
        except:
            print('subscribe callback error:', callback)
            traceback.print_exc()

    return subscribe_callback


def subscribe_callback_wrapper_convert(callback, metaid):
    import traceback
    convert_field_list = get_field_list(metaid)

    def subscribe_callback(datas):
        try:
            if type(datas) == bytes:
                datas = bson.BSON.decode(datas)
            if convert_field_list:
                for s in datas:
                    sdata = datas[s]
                    convert_data_list = []
                    for data in sdata:
                        convert_data = _convert_component_info(data, convert_field_list)
                        convert_data_list.append(convert_data)
                    datas[s] = convert_data_list
            if callback:
                callback(datas)
        except:
            print('subscribe callback error:', callback)
            traceback.print_exc()

    return subscribe_callback


def subscribe_quote(stock_code, period='1d', start_time='', end_time='', count=0, callback=None):
    '''
    订阅股票行情数据
    :param stock_code: 股票代码 e.g. "000001.SZ"
    :param start_time: 开始时间，格式YYYYMMDD/YYYYMMDDhhmmss/YYYYMMDDhhmmss.milli，e.g."20200427" "20200427093000" "20200427093000.000"
        若取某日全量历史数据，时间需要具体到秒，e.g."20200427093000"
    :param end_time: 结束时间 同“开始时间”
    :param count: 数量 -1全部/n: 从结束时间向前数n个
    :param period: 周期 分笔"tick" 分钟线"1m"/"5m" 日线"1d"
    :param callback:
        订阅回调函数onSubscribe(datas)
        :param datas: {stock : [data1, data2, ...]} 数据字典
    :return: int 订阅序号
    '''
    if callback:
        needconvert, metaid = _needconvert_period(period)
        if needconvert:
            callback = subscribe_callback_wrapper_convert(callback, metaid)
        elif period == 'brokerqueue2':
            callback = subscribe_callback_wrapper_1820(callback)
        else:
            callback = subscribe_callback_wrapper(callback)

    period = _get_tuple_period(period) or period
    if isinstance(period, tuple):
        metaid, periodNum = period
        meta = {'stockCode': stock_code, 'period': period, 'metaid': metaid, 'periodnum': periodNum}
    else:
        meta = {'stockCode': stock_code, 'period': period, 'metaid': -1, 'periodnum': -1}
    region = {'startTime': start_time, 'endTime': end_time, 'count': count}

    client = get_client()
    return client.subscribe_quote(bson.BSON.encode(meta), bson.BSON.encode(region), callback)


def subscribe_l2thousand(stock_code, gear_num=0, callback=None):
    '''
    订阅千档盘口
    '''
    if callback:
        callback = subscribe_callback_wrapper(callback)

    meta = {'stockCode': stock_code, 'period': 'l2thousand', 'metaid': -1, 'periodnum': -1}
    region = {'thousandGearNum': gear_num, 'thousandDetailGear': 0, 'thousandDetailNum': 0}

    client = get_client()
    return client.subscribe_quote(bson.BSON.encode(meta), bson.BSON.encode(region), callback)


def subscribe_l2thousand_queue(
        stock_code, callback=None
        , gear=None
        , price=None
):
    '''
        根据档位或价格订阅千档
        stock_code: 股票代码 e.g. "000001.SZ"
        callback:
            订阅回调函数onSubscribe(datas)
        gear: 按档位订阅 eg.
        price: 单个价格：float, 价格范围：eg.[8.66, 8.88], 一组价格list
        return: int 订阅序号
        例：
        def on_data(datas):
            for stock_code in datas:
                print(stock_code, datas[stock_code])
        subscribe_l2thousand_queue(‘000001.SZ’, callback = on_data, gear = 3)#订阅买卖3档数据
        subscribe_l2thousand_queue(‘000001.SZ’, callback = on_data, price = (8.68, 8.88))#订阅[8.68, 8.88]价格区间的数据
    '''

    if callback:
        callback = subscribe_callback_wrapper(callback)

    if gear is not None and price is not None:
        raise Exception('不能同时订阅档位和价格!')

    if gear is None:
        gear = 0
    if price is not None:
        if isinstance(price, float):
            price = [int(price * 10000)]
        elif isinstance(price, tuple):
            sprice, eprice = price
            price = [i for i in range(int(sprice * 10000), int((eprice + 0.01) * 10000), int(0.01 * 10000))]
        else:
            price = [i * 10000 for i in price]
        price.sort()

    meta = {'stockCode': stock_code, 'isSubscribeByType': True, 'gear': gear, 'price': price, 'period': 'l2thousand',
            'metaid': -1, 'periodnum': -1}
    region = {'thousandDetailGear': 1000, 'thousandDetailNum': 1000}

    client = get_client()
    return client.subscribe_quote(bson.BSON.encode(meta), bson.BSON.encode(region), callback)


def get_l2thousand_queue(stock_code, gear=None, price=None):
    '''
        根据档位或价格获取前档
        stock_code 股票代码 e.g. "000001.SZ"
        gear: Optional[int],
        price: Optional[list(float), tuple(2)]
    '''
    if gear is None:
        gear = 0
    if price is not None:
        if isinstance(price, float):
            price = [int(price * 10000)]
        elif isinstance(price, tuple):
            sprice, eprice = price
            price = [i for i in range(int(sprice * 10000), int((eprice + 0.01) * 10000), int(0.01 * 10000))]
        else:
            price = [i * 10000 for i in price]
        price.sort()

    client = get_client()

    data = {}
    data['stockcode'] = stock_code
    data['period'] = 'l2thousand'
    data['gear'] = gear
    data['price'] = price

    result_bson = client.commonControl('getl2thousandqueue', bson.BSON.encode(data))
    result = bson.BSON.decode(result_bson)
    return result.get('result')


def subscribe_whole_quote(code_list, callback=None):
    '''
    订阅全推数据
    :param code_list: 市场代码列表 ["SH", "SZ"]
    :param callback:
        订阅回调函数onSubscribe(datas)
        :param datas: {stock1 : data1, stock2 : data2, ...} 数据字典
    :return: int 订阅序号
    '''
    if callback:
        callback = subscribe_callback_wrapper(callback)

    client = get_client()
    return client.subscribe_whole_quote(code_list, callback)


def unsubscribe_quote(seq):
    """
    :param seq: 订阅接口subscribe_quote返回的订阅号
    :return:
    """
    client = get_client()
    return client.unsubscribe_quote(seq)


def run():
    """阻塞线程接收行情回调"""
    import time
    client = get_client()
    while True:
        time.sleep(3)
        if not client.is_connected():
            raise Exception('行情服务连接断开')
            break
    return


def create_sector_folder(parent_node, folder_name, overwrite=True):
    '''
    创建板块目录节点
    :parent_node str: 父节点,''为'我的' （默认目录）
    :sector_name str: 要创建的板块目录名称
    :overwrite bool:是否覆盖 True为跳过，False为在folder_name后增加数字编号，编号为从1开始自增的第一个不重复的值
    '''
    client = get_client()
    data = {}
    data['parent'] = parent_node
    data['foldername'] = folder_name
    data['overwrite'] = overwrite
    result_bson = client.commonControl('createsectorfolder', bson.BSON.encode(data))
    result = bson.BSON.decode(result_bson)
    return result.get('result')


def create_sector(parent_node, sector_name, overwrite=True):
    '''
    创建板块
    :parent_node str: 父节点,''为'我的' （默认目录）
    :sector_name str: 要创建的板块名
    :overwrite bool:是否覆盖 True为跳过，False为在sector_name后增加数字编号，编号为从1开始自增的第一个不重复的值
    '''
    client = get_client()
    data = {}
    data['parent'] = parent_node
    data['sectorname'] = sector_name
    data['overwrite'] = overwrite
    result_bson = client.commonControl('createsector', bson.BSON.encode(data))
    result = bson.BSON.decode(result_bson)
    return result.get('result')


def get_sector_list():
    '''
    获取板块列表
    :return: (list[str])
    '''
    client = get_client()
    return client.get_sector_list()


def add_sector(sector_name, stock_list):
    '''
    增加自定义板块
    :param sector_name: 板块名称 e.g. "我的自选"
    :param stock_list: (list)stock.market组成的股票代码列表
    '''
    client = get_client()
    data = {}
    data['sectorname'] = sector_name
    data['stocklist'] = stock_list
    result_bson = client.commonControl('addsector', bson.BSON.encode(data))
    result = bson.BSON.decode(result_bson)
    return result.get('result')


def remove_stock_from_sector(sector_name, stock_list):
    '''
    移除板块成分股
    :param sector_name: 板块名称 e.g. "我的自选"
    :stock_list: (list)stock.market组成的股票代码列表
    '''
    client = get_client()
    data = {}
    data['sectorname'] = sector_name
    data['stocklist'] = stock_list
    result_bson = client.commonControl('removestockfromsector', bson.BSON.encode(data))
    result = bson.BSON.decode(result_bson)
    return result.get('result')


def remove_sector(sector_name):
    '''
    删除自定义板块
    :param sector_name: 板块名称 e.g. "我的自选"
    '''
    client = get_client()
    data = {}
    data['sectorname'] = sector_name
    result_bson = client.commonControl('removesector', bson.BSON.encode(data))
    result = bson.BSON.decode(result_bson)
    return result.get('result')


def reset_sector(sector_name, stock_list):
    '''
    重置板块
    :param sector_name: 板块名称 e.g. "我的自选"
    :stock_list: (list)stock.market组成的股票代码列表
    '''
    client = get_client()
    data = {}
    data['sectorname'] = sector_name
    data['stocklist'] = stock_list
    result_bson = client.commonControl('resetsector', bson.BSON.encode(data))
    result = bson.BSON.decode(result_bson)
    return result.get('result')


def _get_instrument_detail(stock_code):
    client = get_client()
    inst = client.get_instrument_detail(stock_code)
    if not inst:
        return None

    inst = xtutil.read_from_bson_buffer(inst)

    if len(inst) != 1:
        return None
    return inst[0]


def get_instrument_detail(stock_code, iscomplete=False):
    '''
    获取合约信息
    :param stock_code: 股票代码 e.g. "600000.SH"
    :return: dict
        ExchangeID(str):合约市场代码
        , InstrumentID(str):合约代码
        , InstrumentName(str):合约名称
        , ProductID(str):合约的品种ID(期货)
        , ProductName(str):合约的品种名称(期货)
        , ExchangeCode(str):交易所代码
        , UniCode(str):统一规则代码
        , CreateDate(int):上市日期(期货)
        , OpenDate(int):IPO日期(股票)
        , ExpireDate(int):退市日或者到期日
        , PreClose(double):前收盘价格
        , SettlementPrice(double):前结算价格
        , UpStopPrice(double):当日涨停价
        , DownStopPrice(double):当日跌停价
        , FloatVolume(double):流通股本
        , TotalVolume(double):总股本
        , LongMarginRatio(double):多头保证金率
        , ShortMarginRatio(double):空头保证金率
        , PriceTick(double):最小变价单位
        , VolumeMultiple(int):合约乘数(对期货以外的品种，默认是1)
        , MainContract(int):主力合约标记
        , LastVolume(int):昨日持仓量
        , InstrumentStatus(int):合约停牌状态
        , IsTrading(bool):合约是否可交易
        , IsRecent(bool):是否是近月合约,
    '''

    inst = _get_instrument_detail(stock_code)
    if not inst:
        return None

    if iscomplete:
        if 'ExtendInfo' in inst:
            for field in inst['ExtendInfo']:
                inst[field] = inst['ExtendInfo'][field]
            del inst['ExtendInfo']

        def convNum2Str(field):
            if field in inst and isinstance(inst[field], int):
                inst[field] = str(inst[field])

        convNum2Str('CreateDate')
        convNum2Str('OpenDate')
        convNum2Str('ExpireDate')
        convNum2Str('EndDelivDate')

        if inst.get('FloatVolume', None) is None:
            inst['FloatVolume'] = inst.get('FloatVolumn')

        if inst.get('TotalVolume', None) is None:
            inst['TotalVolume'] = inst.get('TotalVolumn')

        return inst

    field_list = [
        'ExchangeID'
        , 'InstrumentID'
        , 'InstrumentName'
        , 'ProductID'
        , 'ProductName'
        , 'ExchangeCode'
        , 'UniCode'
        , 'CreateDate'
        , 'OpenDate'
        , 'ExpireDate'
        , 'PreClose'
        , 'SettlementPrice'
        , 'UpStopPrice'
        , 'DownStopPrice'
        , 'FloatVolume'
        , 'TotalVolume'
        , 'LongMarginRatio'
        , 'ShortMarginRatio'
        , 'PriceTick'
        , 'VolumeMultiple'
        , 'MainContract'
        , 'LastVolume'
        , 'InstrumentStatus'
        , 'IsTrading'
        , 'IsRecent'
    ]
    ret = {}
    for field in field_list:
        ret[field] = inst.get(field)

    exfield_list = [
        'ProductTradeQuota'
        , 'ContractTradeQuota'
        , 'ProductOpenInterestQuota'
        , 'ContractOpenInterestQuota'
    ]
    inst_ex = inst.get('ExtendInfo', {})
    for field in exfield_list:
        ret[field] = inst_ex.get(field)

    def convNum2Str(field):
        if field in ret and isinstance(ret[field], int):
            ret[field] = str(ret[field])

    convNum2Str('CreateDate')
    convNum2Str('OpenDate')

    if ret.get('FloatVolume', None) is None:
        ret['FloatVolume'] = inst.get('FloatVolumn')

    if ret.get('TotalVolume', None) is None:
        ret['TotalVolume'] = inst.get('TotalVolumn')

    return ret


def download_index_weight():
    '''
    下载指数权重数据
    '''
    client = get_client()
    client.down_index_weight()


def download_history_contracts():
    '''
    下载过期合约数据
    '''
    client = get_client()
    client.down_history_contracts()


def _download_meta_data(stock_code, metaid, period, start_time='', end_time='', incrementally=True):
    cl = get_client()

    result = __bsoncall_common(
        cl.commonControl, 'downloadmetadata'
        , {
            'stockcode': stock_code
            , 'metaid': metaid
            , 'period': period
            , 'starttime': start_time
            , 'endtime': end_time
            , 'incrementally': incrementally
        }
    )
    return


def _download_history_data(stock_code, period, start_time='', end_time=''):
    cl = get_client()
    cl.supply_history_data(stock_code, period, start_time, end_time)
    return


def download_history_data(stock_code, period, start_time='', end_time='', incrementally=None):
    '''
    :param stock_code: str 品种代码，例如：'000001.SZ'
    :param period: str 数据周期
    :param start_time: str 开始时间
        格式为 YYYYMMDD 或 YYYYMMDDhhmmss 或 ''
        例如：'20230101' '20231231235959'
        空字符串代表全部，自动扩展到完整范围
    :param end_time: str 结束时间 格式同开始时间
    :param incrementally: 是否增量下载
        bool: 是否增量下载
        None: 使用start_time控制，start_time为空则增量下载
    '''

    client = get_client()

    if __download_version == '1':
        return download_history_data2([stock_code], period, start_time, end_time, incrementally)
    else:
        if incrementally is None:
            incrementally = False if start_time else True

        period = _get_tuple_period(period) or period

        if isinstance(period, tuple):
            metaid, periodNum = period
            return _download_meta_data(stock_code, metaid, periodNum, start_time, end_time, incrementally)

        return _download_history_data(stock_code, period, start_time, end_time)


supply_history_data = download_history_data


def download_history_data2(stock_list, period, start_time='', end_time='', callback=None, incrementally=None):
    '''
    :param stock_code: 股票代码 e.g. "000001.SZ"
    :param period: 周期 分笔"tick" 分钟线"1m"/"5m" 日线"1d"
    :param start_time: 开始时间，格式YYYYMMDD/YYYYMMDDhhmmss/YYYYMMDDhhmmss.milli，e.g."20200427" "20200427093000" "20200427093000.000"
        若取某日全量历史数据，时间需要具体到秒，e.g."20200427093000"
    :param end_time: 结束时间 同上，若是未来某时刻会被视作当前时间
    :return: bool 是否成功
    '''
    client = get_client()

    if incrementally is None:
        incrementally = False if start_time else True

    param = {'incrementally': incrementally}

    period = _get_tuple_period(period) or period
    if isinstance(period, tuple):
        metaid, periodNum = period
        period = ''
        param['metaid'] = metaid
        param['period'] = periodNum

    status = [False, 0, 1, '']

    def on_progress(data):
        try:
            finished = data['finished']
            total = data['total']
            done = (finished >= total)
            status[0] = done
            status[1] = finished
            status[2] = total

            try:
                if callback:
                    callback(data)
            except:
                pass

            return done
        except:
            status[0] = True
            status[3] = 'exception'
            return True

    result = client.supply_history_data2(stock_list, period, start_time, end_time, bson.BSON.encode(param), on_progress)
    if not result:
        import time
        try:
            while not status[0] and client.is_connected():
                time.sleep(0.1)
        except:
            if status[1] < status[2]:
                client.stop_supply_history_data2()
            traceback.print_exc()
        if not client.is_connected():
            raise Exception('行情服务连接断开')
        if status[3]:
            raise Exception('下载数据失败：' + status[3])
    return


def download_financial_data(stock_list, table_list=[], start_time='', end_time=''):
    '''
    :param stock_list: 股票代码列表
    :param table_list: 财务数据表名列表，[]为全部表
        可选范围：['Balance','Income','CashFlow','Capital','Top10FlowHolder','Top10Holder','HolderNum','PershareIndex']
    :param start_time: 开始时间，格式YYYYMMDD，e.g."20200427"
    :param end_time: 结束时间 同上，若是未来某时刻会被视作当前时间
    '''
    client = get_client()
    if not table_list:
        table_list = ['Balance', 'Income', 'CashFlow', 'Capital', 'Top10FlowHolder', 'Top10Holder', 'HolderNum',
                      'PershareIndex']

    for stock_code in stock_list:
        for table in table_list:
            client.supply_history_data(stock_code, table, start_time, end_time)


def download_financial_data2(stock_list, table_list=[], start_time='', end_time='', callback=None):
    '''
    :param stock_list: 股票代码列表
    :param table_list: 财务数据表名列表，[]为全部表
        可选范围：['Balance','Income','CashFlow','Capital','Top10FlowHolder','Top10Holder','HolderNum','PershareIndex']
    :param start_time: 开始时间，格式YYYYMMDD，e.g."20200427"
    :param end_time: 结束时间 同上，若是未来某时刻会被视作当前时间
    '''
    client = get_client()
    if not table_list:
        table_list = ['Balance', 'Income', 'CashFlow', 'Capital', 'Top10FlowHolder', 'Top10Holder', 'HolderNum',
                      'PershareIndex']

    data = {}
    data['total'] = len(table_list) * len(stock_list)
    finish = 0
    for stock_code in stock_list:
        for table in table_list:
            client.supply_history_data(stock_code, table, start_time, end_time)

            finish = finish + 1
            try:
                data['finished'] = finish
                callback(data)
            except:
                pass

            if not client.is_connected():
                raise Exception('行情服务连接断开')
                break


def get_instrument_type(stock_code, variety_list=None):
    '''
    判断证券类型
    :param stock_code: 股票代码 e.g. "600000.SH"
    :return: dict{str : bool} {类型名：是否属于该类型}
    '''
    client = get_client()
    v_dct = client.get_stock_type(stock_code)  # 默认处理得到全部品种的信息
    if not v_dct:
        return {}
    v_dct1 = {}
    if variety_list == None or len(variety_list) == 0:  # 返回该stock_code所有的品种的T/None(False)
        v_dct1 = {k: v for k, v in v_dct.items() if v}
        return v_dct1

    for v in variety_list:
        if v in v_dct:
            v_dct1[v] = v_dct[v]
    return v_dct1


get_stock_type = get_instrument_type


def download_sector_data():
    '''
    下载行业板块数据
    '''
    client = get_client()
    client.down_all_sector_data()


def download_holiday_data():
    cl = get_client()

    inst = __bsoncall_common(
        cl.commonControl, 'downloadholidaydata', {}
    )
    return inst


def get_holidays():
    '''
    获取节假日列表
    :return: 8位int型日期
    '''
    client = get_client()
    return [str(d) for d in client.get_holidays()]


def get_market_last_trade_date(market):
    client = get_client()
    return client.get_market_last_trade_date(market)


def get_trading_calendar(market, start_time='', end_time=''):
    '''
    获取指定市场交易日历
    :param market: str 市场
    :param start_time: str 起始时间 '20200101'
    :param end_time: str 结束时间 '20201231'
    :return:
    '''
    if market != "SH" and market != "SZ":
        raise Exception("暂不支持除SH,SZ以外市场的交易日历")

    client = get_client()

    tdl = client.get_trading_dates_by_market(market, start_time, end_time, -1)
    tdl = [dt.datetime.fromtimestamp(tt / 1000) for tt in tdl]

    hl = client.get_holidays()
    hl = [dt.datetime(hh // 10000, ((hh // 100) % 100), hh % 100, 0, 0) for hh in hl]

    if start_time:
        ts = dt.datetime.strptime(start_time, '%Y%m%d') - dt.timedelta(days=1)
        if tdl:
            ts = max(ts, tdl[-1])
    else:
        if tdl:
            ts = tdl[-1]
        else:
            raise Exception('交易日列表为空')

    if end_time:
        te = dt.datetime.strptime(end_time, '%Y%m%d')
        if hl and hl[-1].year < te.year:
            raise Exception(f'end_time({end_time}) 超出现有节假日数据({hl[-1].year}1231)')
    else:
        if hl:
            te = dt.datetime(hl[-1].year, 12, 31, 0, 0)
        else:
            te = tdl[-1]

    hdset = set(hl)

    tt = ts + dt.timedelta(days=1)
    while tt <= te:
        if tt not in hdset and tt.weekday() < 5:
            tdl.append(tt)

        tt += dt.timedelta(days=1)

    return [tt.strftime('%Y%m%d') for tt in tdl]


def get_trading_time(stockcode):
    '''
    返回指定股票的交易时段
    :param stockcode:  代码.市场  例如 '600000.SH'
    :return: 返回交易时段列表，第一位是开始时间，第二位结束时间，第三位交易类型   （2 - 开盘竞价， 3 - 连续交易， 8 - 收盘竞价， 9 - 盘后定价）
    :note: 需要转换为datetime时，可以用以下方法转换
            import datetime as dt
            dt.datetime.combine(dt.date.today(), dt.time()) + dt.timedelta(seconds = 34200)
    '''
    cl = get_client()

    split_codes = stockcode.rsplit('.', 1)
    if len(split_codes) == 2:
        code = split_codes[0]
        market = split_codes[1]
    else:
        return []

    inst = __bsoncall_common(
        cl.commonControl, 'tradetime', {
            'market': market
            , 'code': code
        }
    )
    return inst.get('result', [])


def is_stock_type(stock, tag):
    client = get_client()
    return client.is_stock_type(stock, tag)


def download_cb_data():
    client = get_client()
    return client.down_cb_data()


def get_cb_info(stockcode):
    client = get_client()
    inst = client.get_cb_info(stockcode)
    return bson.BSON.decode(inst)


def get_option_detail_data(optioncode):
    inst = _get_instrument_detail(optioncode)
    if not inst:
        return None

    ret = {}
    market = inst.get('ExchangeID')
    if market == 'SHO' or market == "SZO" \
            or ((market == "CFFEX" or market == "IF") and inst.get('InstrumentID').find('-') >= 0) \
            or (market in ['SF', 'SHFE', 'DF', 'DCE', 'INE', 'GF', 'GFEX', 'ZF', 'CZCE'] and inst.get('ExtendInfo').get(
        'OptionType') in [0, 1]):
        field_list = [
            'ExchangeID'
            , 'InstrumentID'
            , 'ProductID'
            , 'OpenDate'
            , 'CreateDate'
            , 'ExpireDate'
            , 'PreClose'
            , 'SettlementPrice'
            , 'UpStopPrice'
            , 'DownStopPrice'
            , 'LongMarginRatio'
            , 'ShortMarginRatio'
            , 'PriceTick'
            , 'VolumeMultiple'
            , 'MaxMarketOrderVolume'
            , 'MinMarketOrderVolume'
            , 'MaxLimitOrderVolume'
            , 'MinLimitOrderVolume'
        ]
        ret = {}
        for field in field_list:
            ret[field] = inst.get(field)

        exfield_list = [
            'OptUnit'
            , 'MarginUnit'
            , 'OptUndlCode'
            , 'OptUndlMarket'
            , 'OptExercisePrice'
            , 'NeeqExeType'
            , 'OptUndlRiskFreeRate'
            , 'OptUndlHistoryRate'
            , 'EndDelivDate'
        ]
        inst_ex = inst.get('ExtendInfo', {})
        for field in exfield_list:
            ret[field] = inst_ex.get(field)

        def convNum2Str(field):
            if field in ret and isinstance(ret[field], int):
                ret[field] = str(ret[field])

        convNum2Str('ExpireDate')
        convNum2Str('CreateDate')
        convNum2Str('OpenDate')
        convNum2Str('EndDelivDate')

        ret["optType"] = ""

        instrumentName = inst.get("InstrumentName")
        if instrumentName.find('C') > 0 or instrumentName.find('购') > 0:
            ret["optType"] = "CALL"
        elif instrumentName.find('P') > 0 or instrumentName.find('沽') > 0:
            ret["optType"] = "PUT"
    return ret


def get_option_undl_data(undl_code_ref):
    def get_option_undl(opt_code):
        inst = get_option_detail_data(opt_code)
        if inst and 'OptUndlCode' in inst and 'OptUndlMarket' in inst:
            return inst['OptUndlCode'] + '.' + inst['OptUndlMarket']
        return ''

    if undl_code_ref:
        opt_list = []
        if undl_code_ref.endswith('.SH'):
            if undl_code_ref == "000016.SH" or undl_code_ref == "000300.SH" or undl_code_ref == "000852.SH" or undl_code_ref == "000905.SH":
                opt_list = get_stock_list_in_sector('中金所')
            else:
                opt_list = get_stock_list_in_sector('上证期权')
        if undl_code_ref.endswith('.SZ'):
            opt_list = get_stock_list_in_sector('深证期权')
        data = []
        for opt_code in opt_list:
            undl_code = get_option_undl(opt_code)
            if undl_code == undl_code_ref:
                data.append(opt_code)
        return data
    else:
        opt_list = []
        opt_list += get_stock_list_in_sector('上证期权')
        opt_list += get_stock_list_in_sector('深证期权')
        opt_list += get_stock_list_in_sector('中金所')
        result = {}
        for opt_code in opt_list:
            undl_code = get_option_undl(opt_code)
            if undl_code:
                if undl_code in result:
                    result[undl_code].append(opt_code)
                else:
                    result[undl_code] = [opt_code]
        return result


def get_option_list(undl_code, dedate, opttype="", isavailavle=False):
    result = []

    marketcodeList = undl_code.split('.')
    if (len(marketcodeList) != 2):
        return []
    undlCode = marketcodeList[0]
    undlMarket = marketcodeList[1]
    market = ""
    if (undlMarket == "SH"):
        if undlCode == "000016" or undlCode == "000300" or undlCode == "000852" or undlCode == "000905":
            market = 'IF'
        else:
            market = "SHO"
    elif (undlMarket == "SZ"):
        market = "SZO"
    if (opttype.upper() == "C"):
        opttype = "CALL"
    elif (opttype.upper() == "P"):
        opttype = "PUT"
    optList = []
    if market == 'SHO':
        optList += get_stock_list_in_sector('上证期权')
        optList += get_stock_list_in_sector('过期上证期权')
    elif market == 'SZO':
        optList += get_stock_list_in_sector('深证期权')
        optList += get_stock_list_in_sector('过期深证期权')
    elif market == 'IF':
        optList += get_stock_list_in_sector('中金所')
        optList += get_stock_list_in_sector('过期中金所')
    for opt in optList:
        if (opt.find(market) < 0):
            continue
        inst = get_option_detail_data(opt)
        if not inst:
            continue
        if (opttype.upper() != "" and opttype.upper() != inst["optType"]):
            continue
        if ((len(dedate) == 6 and inst['ExpireDate'].find(dedate) < 0)):
            continue
        if (len(dedate) == 8):  # option is trade,guosen demand
            createDate = inst['CreateDate']
            openDate = inst['OpenDate']
            if (createDate > '0'):
                openDate = min(openDate, createDate)
            if (openDate < '20150101' or openDate > dedate):
                continue
            endDate = inst['ExpireDate']
            if (isavailavle and endDate < dedate):
                continue
        if inst['OptUndlCode'].find(undlCode) >= 0:
            result.append(opt)
    return result


def get_ipo_info(start_time='', end_time=''):
    client = get_client()
    data = client.get_ipo_info(start_time, end_time)
    pylist = [
        'securityCode'  # 证券代码
        , 'codeName'  # 代码简称
        , 'market'  # 所属市场
        , 'actIssueQty'  # 发行总量  单位：股
        , 'onlineIssueQty'  # 网上发行量  单位：股
        , 'onlineSubCode'  # 申购代码
        , 'onlineSubMaxQty'  # 申购上限  单位：股
        , 'publishPrice'  # 发行价格
        , 'startDate'  # 申购开始日期
        , 'onlineSubMinQty'  # 最小申购数，单位：股
        , 'isProfit'  # 是否已盈利 0：上市时尚未盈利 1：上市时已盈利
        , 'industryPe'  # 行业市盈率
        , 'beforePE'  # 发行前市盈率
        , 'afterPE'  # 发行后市盈率
        , 'listedDate'  # 上市日期
        , 'declareDate'  # 中签号公布日期
        , 'paymentDate'  # 中签缴款日
        , 'lwr'  # 中签率
    ]
    result = []
    for datadict in data:
        resdict = {}
        for field in pylist:
            resdict[field] = datadict.get(field)
        result.append(resdict)
    return result


def get_markets():
    '''
    获取所有可选的市场
    返回 dict
        { <市场代码>: <市场名称>, ... }
    '''
    return {
        'SH': '上交所'
        , 'SZ': '深交所'
        , 'BJ': '北交所'
        , 'HK': '港交所'
        , 'HGT': '沪港通'
        , 'SGT': '深港通'
        , 'IF': '中金所'
        , 'SF': '上期所'
        , 'DF': '大商所'
        , 'ZF': '郑商所'
        , 'GF': '广期所'
        , 'INE': '能源交易所'
        , 'SHO': '上证期权'
        , 'SZO': '深证期权'
        , 'BKZS': '板块指数'
        , 'WP': '外盘'
    }


def get_his_st_data(stock_code):
    fileName = os.path.join(get_data_dir(), '..', 'data', 'SH_XXXXXX_2011_86400000.csv')

    try:
        with open(fileName, "r") as f:
            datas = f.readlines()
    except:
        return {}

    status = []
    for data in datas:
        cols = data.split(',')
        if len(cols) >= 4 and cols[0] == stock_code:
            status.append((cols[2], cols[3]))

    if not status:
        return {}

    result = {}
    i = 0
    while i < len(status):
        start = status[i][0]
        flag = status[i][1]

        i += 1

        end = '20380119'
        if i < len(status):
            end = status[i][0]

        realStatus = ''
        if (flag == '1'):
            realStatus = 'ST'
        elif (flag == '2'):
            realStatus = '*ST'
        elif (flag == '3'):
            realStatus = 'PT'
        else:
            continue

        if realStatus not in result:
            result[realStatus] = []
        result[realStatus].append([start, end])

    return result


def create_formula(formula_name, stock_code, period, start_time='', end_time='', count=-1, dividend_type='none',
                   extend_param={}, callback=None):
    cl = get_client()

    result = bson.BSON.decode(cl.commonControl('createrequestid', bson.BSON.encode({})))
    request_id = result['result']

    data = {
        'formulaname': formula_name, 'stockcode': stock_code, 'period': period
        , 'starttime': start_time, 'endtime': end_time, 'count': count
        , 'dividendtype': dividend_type, 'extendparam': extend_param
        , 'create': True
    }

    if callback:
        callback = subscribe_callback_wrapper(callback)

    cl.subscribeFormula(request_id, bson.BSON.encode(data), callback)
    return request_id


def subscribe_formula(request_id, callback=None):
    cl = get_client()

    if callback:
        callback = subscribe_callback_wrapper(callback)

    cl.subscribeFormula(request_id, bson.BSON.encode({}), callback)
    return


def unsubscribe_formula(request_id):
    cl = get_client()
    cl.subscribeFormula(request_id)
    return


def call_formula(
        formula_name, stock_code, period
        , start_time='', end_time='', count=-1
        , dividend_type='none', extend_param={}
):
    cl = get_client()

    result = bson.BSON.decode(cl.commonControl('createrequestid', bson.BSON.encode({})))
    request_id = result['result']

    data = {
        'formulaname': formula_name, 'stockcode': stock_code, 'period': period
        , 'starttime': start_time, 'endtime': end_time, 'count': count
        , 'dividendtype': dividend_type, 'extendparam': extend_param
        , 'create': True
    }

    data = cl.subscribeFormulaSync(request_id, bson.BSON.encode(data))
    return bson.BSON.decode(data)


gmd = get_market_data
gmd2 = get_market_data_ex
gmd3 = get_market_data3
gld = get_local_data
t2d = timetag_to_datetime
gsl = get_stock_list_in_sector


def reset_market_trading_day_list(market, datas):
    cl = get_client()

    result = __bsoncall_common(
        cl.custom_data_control, 'createmarketchange'
        , {
            'market': market
        }
    )
    cid = result['cid']

    result = __bsoncall_common(
        cl.custom_data_control, 'addtradingdaytochange'
        , {
            'cid': cid
            , 'datas': datas
            , 'coverall': True
        }
    )

    result = __bsoncall_common(
        cl.custom_data_control, 'finishmarketchange'
        , {
            'cid': cid
            # , 'abort': False
            , 'notifyupdate': True
        }
    )
    return


def reset_market_stock_list(market, datas):
    cl = get_client()

    result = __bsoncall_common(
        cl.custom_data_control, 'createmarketchange'
        , {
            'market': market
        }
    )
    cid = result['cid']

    result = __bsoncall_common(
        cl.custom_data_control, 'addstocktochange'
        , {
            'cid': cid
            , 'datas': datas
            , 'coverall': True
        }
    )

    result = __bsoncall_common(
        cl.custom_data_control, 'finishmarketchange'
        , {
            'cid': cid
            # , 'abort': False
            , 'notifyupdate': True
        }
    )
    return


def push_custom_data(meta, datas, coverall=False):
    cl = get_client()
    result = __bsoncall_common(
        cl.custom_data_control, 'pushcustomdata'
        , {
            "meta": meta
            , 'datas': datas
            , 'coverall': coverall
        }
    )
    return


def get_period_list():
    client = get_client()
    result = bson.BSON.decode(client.commonControl('getperiodlist', bson.BSON.encode({})))
    request_id = result['result']
    return request_id


def gen_factor_index(
        data_name, formula_name, vars, sector_list
        , start_time='', end_time='', period='1d'
        , dividend_type='none'
):
    '''
    生成因子指数扩展数据
    '''
    running_info = {
        'result': {}
        , 'finished': 0
        , 'total': 0
    }

    def onPushProgress(data):
        running_info['finished'] = data.get('finished', -1)
        if running_info['finished'] == -1:
            running_info['result'] = data
        else:
            running_info['total'] = data.get('total', -1)

    callback = subscribe_callback_wrapper(onPushProgress)

    get_client().subscribeCommonControl(
        'genfactorindex'
        , bson.BSON.encode(
            {
                'data_name': data_name
                , 'formula_name': formula_name
                , 'vars': vars
                , 'sector_list': sector_list
                , 'start_time': start_time
                , 'end_time': end_time
                , 'period': period
                , 'dividend_type': dividend_type
            }
        )
        , callback
    )

    last_finished = running_info['finished']
    time_count = 0
    while not running_info['result']:
        time.sleep(1)
        if last_finished != running_info['finished']:
            last_finished = running_info['finished']
            time_count = 0
        else:
            time_count += 1
            if time_count > 20:
                time_count = 0
                if get_client():
                    print(f'因子指数扩展数据生成进度长时间未更新，'
                          f'当前进度{running_info["finished"]}/{running_info["total"]}')

    return running_info['result']


def import_formula(formula_name, file_path):
    '''
    导入策略
    '''
    return __bsoncall_common(get_client().commonControl
                             , 'importformula'
                             , {'formula_name': formula_name, 'file_path': file_path}
                             )


def del_formula(formula_name):
    '''
    删除策略
    '''
    return __bsoncall_common(get_client().commonControl
                             , 'delformula'
                             , {'formula_name': formula_name}
                             )


def get_formulas():
    '''
    查询所有的策略
    '''
    return __bsoncall_common(get_client().commonControl, 'getformulas', {})


def read_feather(file_path):
    '''
    读取feather格式的arrow文件
    :param file_path: (str)
    :return: param_bin: (dict), df: (pandas.DataFrame)
    '''
    if sys.version_info.major > 2:
        from pyarrow import feather
        if sys.version_info.minor > 6:
            table = feather.read_table(source=file_path, columns=None, memory_map=True, use_threads=True)
        else:
            table = feather.read_table(source=file_path, columns=None, memory_map=True)

        metadata = table.schema.metadata
        param_bin_bytes = metadata.get(b'param_bin')
        # param_str_bytes = metadata.get(b'param_str')

        param_bin = bson.BSON.decode(param_bin_bytes)
        # param_str = param_str_bytes.decode('utf-8')
        df = table.to_pandas(use_threads=True)
        return param_bin, df

    return None, None


def write_feather(dest_path, param, df):
    '''
    将panads.DataFrame转换为arrow.Table以feather格式写入文件
    :param dest_path: (str)路径
    :param param: (dict) schema的metadata
    :param df: (pandas.DataFrame) 数据
    :return: (bool) 成功/失败
    '''
    if sys.version_info.major > 2:
        from pyarrow import feather, Schema, Table
        schema = Schema.from_pandas(df).with_metadata({
            'param_bin': bson.BSON.encode(param),
            'param_str': json.dumps(param)
        })
        table = Table.from_pandas(df, schema=schema)
        feather.write_feather(table, dest_path)
        return True

    return False


class QuoteServer:
    def __init__(self, info={}):
        '''
        info: {
            'ip': '218.16.123.121'
            , 'port': 55300
            , 'username': 'test'
            , 'pwd': 'testpwd'
        }
        '''
        self.info = info

        ip = info.get('ip', None)
        port = info.get('port', None)

        if not ip or not port:
            raise f'invalid address, ip:{ip}, port:{port}'
        return

    def __bsoncall_common(self, interface, func, param):
        return bson.BSON.decode(interface(func, bson.BSON.encode(param)))

    def __str__(self):
        return str(self.info)

    def connect(self):
        '''
        连接到这个地址
        '''
        cl = get_client()

        return self.__bsoncall_common(
            cl.commonControl, 'quoteserverconnect'
            , {
                'ip': self.info['ip']
                , 'port': self.info['port']
                , 'info': self.info
                , 'operation': 'login'
            }
        )

    def disconnect(self):
        '''
        断开连接
        '''
        cl = get_client()

        result = self.__bsoncall_common(
            cl.commonControl, 'quoteserverconnect'
            , {
                'ip': self.info['ip']
                , 'port': self.info['port']
                , 'info': self.info
                , 'operation': 'logout'
            }
        )
        return

    def set_key(self, key_list=[]):
        '''
        设置数据key到这个地址，后续会使用这个地址获取key对应的市场数据

        key_list: [key, ...]
        key:
            f'{market}_{level}'
        market:
            SH, SZ, ...
        level:
            'L1' # level 1
            'L2' # level 2
        '''
        cl = get_client()

        result = self.__bsoncall_common(
            cl.commonControl, 'quoteserversetkey'
            , {
                'ip': self.info['ip']
                , 'port': self.info['port']
                , 'info': self.info
                , 'keys': key_list
            }
        )
        return

    def test_load(self):
        '''
        获取这个地址的负载情况
        '''
        cl = get_client()

        result = self.__bsoncall_common(
            cl.commonControl, 'testload'
            , {
                'ip': self.info['ip']
                , 'port': self.info['port']
                , 'info': self.info
            }
        )
        return result

    def get_available_quote_key(self):
        '''
        获取这个地址可支持的数据key
        '''
        cl = get_client()

        inst = self.__bsoncall_common(
            cl.commonControl, 'getavailablekey'
            , {
                'ip': self.info['ip']
                , 'port': self.info['port']
                , 'info': self.info
            }
        )
        result = inst.get('result', [])

        return result

    def get_server_list(self):
        '''
        获取这个地址的服务器组列表
        '''
        cl = get_client()

        inst = self.__bsoncall_common(
            cl.commonControl, 'getserverlist'
            , {
                'ip': self.info['ip']
                , 'port': self.info['port']
                , 'info': self.info
            }
        )

        inst = inst.get('result', [])

        result = [QuoteServer(info) for info in inst]
        return result


def get_quote_server_config():
    '''
    获取连接配置

    result: [info, ...]
    '''
    cl = get_client()

    inst = __bsoncall_common(
        cl.commonControl, 'getquoteserverconfig', {}
    )
    inst = inst.get('result', [])

    result = [QuoteServer(info) for info in inst]
    return result


def get_quote_server_status():
    '''
    获取当前全局连接状态

    result: {
        quote_key: info
        , ...
    }
    '''
    cl = get_client()

    inst = __bsoncall_common(
        cl.commonControl, 'getquoteserverstatus', {}
    )
    inst = inst.get('result', [])

    result = {}
    for pair in inst:
        key = pair.get('key', '')
        info = pair.get('info', {})
        result[key] = QuoteServer(info)
    return result


def watch_quote_server_status(callback):
    '''
    监控全局连接状态变化

    def callback(info, status):
        #info: info
        #status: 'connected', 'disconnected'
        return
    '''
    cl = get_client()

    if callback:
        callback = subscribe_callback_wrapper(callback)

    cl.subscribeCommonControl("watchquoteserverstatus", bson.BSON.encode({}), callback)
    return


def fetch_quote(root_path, key_list):
    root_path = os.path.abspath(root_path)
    cl = get_client()
    inst = __bsoncall_common(
        cl.commonControl, 'fetchquote', {
            'dir': root_path
        }
    )

    config_dir = os.path.join(root_path, 'userdata_mini', 'users', 'xtquoterconfig.xml')
    if not os.path.isfile(config_dir):
        return

    import xml.etree.ElementTree as ET

    tree = ET.parse(config_dir)
    quoter_server_list = tree.find('QuoterServers')
    quoter_server_list = quoter_server_list.findall('QuoterServer')

    qs_infos = {}
    for server in quoter_server_list:
        quoter_type = server.attrib['quotertype']
        if quoter_type != '0':
            continue

        info = {'ip': server.attrib['address'], 'port': int(server.attrib['port']),
                'username': server.attrib['username'], 'pwd': server.attrib['password']}
        qs = QuoteServer(info)
        relate_servers = qs.get_server_list()
        for rs in relate_servers:
            keys = rs.info.get('keys', [])
            keys = ['0_' + key for key in keys if '0_' + key in key_list]

            if keys:
                addr = (rs.info['ip'], rs.info['port'])
                rs.info['keys'] = keys
                qs_infos[addr] = rs

    servers = {}
    for qs in qs_infos.values():
        qs.info.update(qs.test_load())
        for key in qs.info['keys']:
            if key not in servers:
                servers[key] = []
            servers[key].append(qs)

    for p in servers.items():
        p[1].sort(key=lambda x: x.info.get('delay', 1000000.0))

    for key_servers in servers.items():
        for qs in key_servers[1]:
            if qs.info['load'] != 1000000.0 and qs.info['delay'] != 1000000.0 and qs.info['accessible']:
                qs.set_key([key_servers[0]])
                break

    return


def get_etf_info():
    period = _get_tuple_period('etfredemptionlist')
    if not isinstance(period, tuple):
        return {}

    all_data = _get_market_data_ex_tuple_period_ori(['XXXXXX.SH', 'XXXXXX.SZ'], period)

    metaid, periodNum = period
    convert_field_list = get_field_list(metaid)

    result = {}
    for stockcode, data_list in all_data.items():
        market = stockcode.split('.')[1]

        for data in data_list:
            convert_data = {'market': market}

            if convert_field_list:
                data = _convert_component_info(data, convert_field_list)
            convert_data.update(data)

            stock_market = ''
            if '基金代码' in data:
                stock_market = data['基金代码'] + '.' + market

            convert_market = {'1': 'SH', '2': 'SZ', '3': 'HK', '4': 'BJ'}
            if '成份股信息' in convert_data:
                for sub_data in convert_data['成份股信息']:
                    if '成份股所属市场' in sub_data and '成份股代码' in sub_data and str(
                            sub_data['成份股所属市场']) in convert_market:
                        sub_data['成份股代码'] = sub_data['成份股代码'] + '.' + convert_market[
                            str(sub_data['成份股所属市场'])]
                        sub_data['成份股所属市场'] = convert_market[str(sub_data['成份股所属市场'])]

            if stock_market:
                result[stock_market] = convert_data

    return result


def download_etf_info():
    for stock_code in ['XXXXXX.SH', 'XXXXXX.SZ']:
        download_history_data(stock_code, 'etfredemptionlist', '', '')

    return


def download_his_st_data():
    '''
    下载历史st数据
    '''
    cl = get_client()

    result = __bsoncall_common(
        cl.commonControl, 'downloadhisstdata', {}
    )
    return result


def get_hk_broker_dict():
    global __hk_broke_info

    if not __hk_broke_info:
        data = _get_market_data_ex_tuple_period_ori(['XXXXXX.HK'], (2038, 86401000), '', '')

        for a in data['XXXXXX.HK']:
            list = a['1']
            name = a['0']
            for id in list:
                __hk_broke_info[id] = name

    return __hk_broke_info


def _covert_hk_broke_data(ori_data={}):
    broke_dict = get_hk_broker_dict()
    for s in ori_data:
        sdata = ori_data[s]
        for data in sdata:
            for Broker in data['bidbrokerqueues']:
                bidBrokerQueues = Broker['brokers']
                listbid = []
                for brokerid in bidBrokerQueues:
                    brokername = broke_dict.get(brokerid, '')
                    listbid.append((brokerid, brokername))
                Broker['brokers'] = listbid

            for Broker in data['askbrokerqueues']:
                askBrokerQueues = Broker['brokers']
                listask = []
                for brokerid in askBrokerQueues:
                    brokername = broke_dict.get(brokerid, '')
                    listask.append((brokerid, brokername))
                Broker['brokers'] = listask

    return ori_data


def get_broker_queue_data(stock_list=[], start_time='', end_time='', count=-1, show_broker_name=False):
    ori_data = get_market_data_ex_ori([], stock_list, 'hkbrokerqueue', start_time, end_time, count)

    if show_broker_name:
        return _covert_hk_broke_data(ori_data)
    return ori_data


def watch_xtquant_status(callback):
    '''
    监控xtquant连接状态变化

    def callback(info):
        #info: {peerAddress : 'ip:port', status: ''}
        #status: 'connected', 'disconnected'
        return
    '''
    cl = get_client()

    if callback:
        callback = subscribe_callback_wrapper(callback)

    cl.subscribeCommonControl("watchxtquantstatus", bson.BSON.encode({}), callback)
    return
