# coding:utf-8
import json
import os

from .xtdatacenter import try_create_client

# config
localhost = '127.0.0.1'


# function

def try_create_connection(addr):
    '''
    addr: 'localhost:58610'
    '''
    ip, port = addr.split(':')
    if not ip:
        ip = localhost
    if not port:
        raise Exception('invalid port')

    cl = try_create_client()
    cl.set_config_addr(addr)

    ec, msg = cl.connect()
    if ec < 0:
        raise Exception((ec, msg))
    return cl


def create_connection(addr):
    try:
        return try_create_connection(addr)
    except Exception as e:
        return None


def scan_available_server():
    result = []

    try:
        from .xtdatacenter import get_local_server_port
        local_server_port = get_local_server_port()
        if local_server_port:
            result.append(f'127.0.0.1:{local_server_port}')
    except:
        pass

    try:
        config_dir = os.path.abspath(os.path.join(os.environ['USERPROFILE'], '.xtquant'))

        for f in os.scandir(config_dir):
            full_path = f.path

            is_running = False
            try:
                os.remove(os.path.join(full_path, 'running_status'))
            except PermissionError:
                is_running = True
            except Exception as e:
                pass

            if not is_running:
                continue

            try:
                config = json.load(open(os.path.join(full_path, 'xtdata.cfg'), 'r', encoding='utf-8'))

                ip = config.get('ip', localhost)
                port = config.get('port', None)
                if not port:
                    raise Exception(f'invalid port: {port}')

                addr = f'{ip}:{port}'
                result.append(addr)
            except Exception as e:
                continue

    except Exception as e:
        pass

    result.sort()
    return result


def connect_any(addr_list):
    '''
    addr_list: [ addr, ... ]
        addr: 'localhost:58610'
    '''
    for addr in addr_list:
        try:
            cl = create_connection(addr)
            if cl:
                return cl
        except Exception as e:
            continue

    return None
