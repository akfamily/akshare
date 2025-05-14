# coding:utf-8
import os
import time

from . import datacenter as __dc

__all__ = [
    'set_token',
    'set_data_home_dir',
    'init',
    'shutdown',
    'listen',
    'get_local_server_port',
    'register_create_nparray',
    'try_create_client',
    'RPCClient',
]

# config

__curdir = os.path.dirname(os.path.abspath(__file__))

__rpc_config_dir = os.path.join(__curdir, 'config')
__rpc_config_file = os.path.join(__curdir, 'xtdata.ini')
__rpc_init_status = __dc.rpc_init(__rpc_config_dir)
if __rpc_init_status < 0:
    raise Exception(f'rpc init failed, error_code:{__rpc_init_status}, configdir:{__rpc_config_dir}')

__dc.set_config_dir(os.path.join(__curdir, 'config'))

__data_home_dir = 'data'

__quote_token = ''

# function
get_local_server_port = __dc.get_local_server_port
register_create_nparray = __dc.register_create_nparray
RPCClient = __dc.IPythonApiClient


def try_create_client():
    '''
    尝试创建RPCClient，如果失败，会抛出异常
    '''
    cl = RPCClient()
    cl.init()

    ec = cl.load_config(__rpc_config_file, 'client_xtdata')
    if ec < 0:
        raise f'load config failed, file:{__rpc_config_file}'
    return cl


def set_token(token=''):
    '''
    设置用于登录行情服务的token，此接口应该先于init_quote调用
    token获取地址：https://xuntou.net/#/userInfo?product=xtquant
    迅投投研服务平台 - 用户中心 - 个人设置 - 接口TOKEN
    '''
    global __quote_token
    __quote_token = token
    return


def set_data_home_dir(data_home_dir):
    '''
    设置数据存储目录，此接口应该先于init_quote调用
    datacenter启动后，会在data_home_dir目录下建立若干目录存储数据
    如果不设置存储目录，会使用默认路径
    在datacenter作为独立行情服务的场景下，data_home_dir可以任意设置
    如果想使用现有数据，data_home_dir对应QMT的f'{安装目录}'，或对应极简模式的f'{安装目录}/userdata_mini'
    '''
    global __data_home_dir
    __data_home_dir = data_home_dir
    return


def set_kline_mirror_enabled(enable):
    '''
    设置K线全推功能是否开启，此接口应该先于init_quote调用
    此功能默认关闭，启用后，实时K线数据将优先从K线全推获取
    此功能仅vip用户可用
    '''
    __dc.set_kline_mirror_enabled(enable)
    return


def set_allow_optmize_address(list=[]):
    '''
    设置连接池，行情仅从连接池内的地址中选择连接，此接口应该先于init_quote调用
    地址格式为'127.0.0.1:55300'
    设置为空时，行情从全部的可用地址中选择连接
    '''
    __dc.set_allow_optmize_address(list)


def init(start_local_service=True):
    '''
    初始化行情模块
    start_local_service: bool
        如果start_local_service为True，会额外启动一个默认本地监听，以支持datacenter作为独立行情服务时的xtdata内置连接
    '''
    __dc.set_data_home_dir(__data_home_dir)
    __dc.set_token(__quote_token)
    __dc.start_init_quote()

    status = __dc.get_status()
    while not status.get('init_done', False):
        status = __dc.get_status()
        time.sleep(0.5)

    market_keys = [
        'SH', 'SZ', 'IF', 'SF', 'DF', 'ZF', 'GF', 'INE'
    ]
    result = __dc.fetch_init_result([f'0_{mkt}_L1' for mkt in market_keys])

    from . import xtbson as bson

    for mkt, boinfo in result.items():
        info = bson.decode(boinfo)

        if info['done'] == 1:
            if info['errorcode'] != 0:
                srv_addr = info['loginparam']['ip'] + ':' + str(info['loginparam']['port'])
                error = info['boerror']

                raise Exception(f'行情连接初始化异常 {mkt} {srv_addr} {error}')

            if info['resultcode'] != 0:
                srv_addr = info['loginparam']['ip'] + ':' + str(info['loginparam']['port'])
                error = info['resultdesc']
                reason = info['reason']

                raise Exception(f'行情连接初始化异常 {mkt} {srv_addr} {error} {reason}')
        else:
            status = bson.decode(__dc.fetch_server_list_status())

            status_show = {}

            for info in status.values():
                srv_addr = info['loginparam']['ip'] + ':' + str(info['loginparam']['port'])

                if info['errorcode'] != 0:
                    status_show[srv_addr] = info['boerror']
                else:
                    status_show[srv_addr] = info['resultdesc']

            raise Exception(f'行情连接初始化异常 {mkt}, 当前状态:{status_show}')

    if start_local_service:
        listen('127.0.0.1', 58609)
    return


def shutdown():
    '''
    关闭行情模块，停止所有服务和监听端口
    '''
    __dc.shutdown()
    return


def listen(ip='0.0.0.0', port=58610):
    '''
    独立行情服务模式，启动监听端口，支持xtdata.connect接入
    ip:
        str, '0.0.0.0'
    port:
        int, 指定监听端口
        tuple, 指定监听端口范围，从port[0]至port[1]逐个尝试监听
    返回:
        (ip, port), 表示监听的结果
    示例:
        from xtquant import xtdatacenter as xtdc
        ip, port = xtdc.listen('0.0.0.0', 58610)
        ip, port = xtdc.listen('0.0.0.0', (58610, 58620))
    '''

    if isinstance(port, tuple):
        port_start, port_end = port
        result = __dc.listen(ip, port_start, port_end)
    else:
        result = __dc.listen(ip, port, port)

    if result[1] == 0:
        raise Exception(f'端口监听失败: {port}')

    return result
