#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/4/17 15:00
Desc: 为akshare的请求添加环境变量用于伪装防止目标网站反爬
"""
import os
from threading import Timer
import dotenv
# from fake_useragent import UserAgent

global_config_active = False
timer = None
global_request_count = 0
global_max_requests = None
global_proxy_active = False
global_use_fake_user_agent = False
global_set_timeout = None
global_force = False

def start_config(
        # config_max_time: float = None,
        # config_max_request: int = None,
        use_proxy: bool,
        config_max_time: float = None,
        config_max_request: int = None,
        #   = False,
        # use_fake_user_agent: bool = False,
        # set_timeout: float = None,
        # force: bool = False
        ):
    # if not use_proxy:
    # and not use_fake_user_agent and set_timeout is None:
        # raise ValueError("At least one parameter must be set.")
    if config_max_time is not None:
        if config_max_time <= 0:
            raise ValueError("max_time must be greater than 0.")
    if config_max_request is not None:
        if config_max_request <= 0:
            raise ValueError("max_request must be greater than 0.")
    # if set_timeout is not None:
    #     if set_timeout < 0:
    #         raise ValueError("timeout must be greater than or equal to 0.")
    global global_config_active
    global global_max_requests
    global global_use_fake_user_agent
    global global_set_timeout
    global global_force
    if global_config_active:
        stop_config()
    if config_max_time:
        timer_start(max_time = config_max_time)
    if config_max_request:
        global_max_requests = config_max_request
        add_request_monitoring()
    if use_proxy:
        proxy_on()
    # if use_fake_user_agent:
    #     global_use_fake_user_agent = use_fake_user_agent
    # if set_timeout:
    #     global_set_timeout = set_timeout
    # if force:
    #     global_force = force
    global_config_active = True
    print(f"""
            config is now active.
            max_time: {config_max_time}
            max_request: {config_max_request}
            use_proxy: {use_proxy}
            """)
            # use_user_agent: {use_fake_user_agent}
            # set_timeout: {set_timeout}
            # force: {force}
            # """)

def stop_config():
    remove_request_monitoring()
    timer_stop()
    proxy_off()
    global global_config_active
    global global_use_fake_user_agent
    global global_set_timeout
    global global_force
    global_config_active = False
    global_use_fake_user_agent = False
    global_set_timeout = None
    global_force = False
    print("Request config has been deactivated.")

def add_request_monitoring():
    import akshare as ak
    global global_request_count
    global_request_count = 0
    for func_name in dir(ak):
        func = getattr(ak, func_name)
        if callable(func):
            setattr(ak, func_name, monitored_call(func))

def remove_request_monitoring():
    import akshare as ak
    global global_request_count
    global global_max_requests
    global_request_count = 0
    if global_max_requests:
        global_max_requests = None
        for func_name in dir(ak):
            func = getattr(ak, func_name)
            if callable(func) and isinstance(func, monitored_call.__class__):
                original_func = func.__wrapped__
                setattr(ak, func_name, original_func)

def monitored_call(func):
    def wrapper(*args, **kwargs):
        global global_request_count
        global global_max_requests
        if func.__name__ in ['start_config', 'stop_config', 'change_proxy']:
            return func(*args, **kwargs)              
        result = func(*args, **kwargs)
        global_request_count += 1
        if global_max_requests:
            if global_request_count >= global_max_requests:
                print("Request limit reached. config will now stop.")
                stop_config()
        return result    
    wrapper.__wrapped__ = func
    return wrapper

def proxy_on():
    dotenv.load_dotenv()
    global global_proxy_active
    if global_proxy_active:
        proxy_off()
        global_proxy_active = False
    os.environ['HTTP_PROXY'] = os.getenv('PROXY', 'default_http_proxy')
    os.environ['HTTPS_PROXY'] = os.getenv('PROXY', 'default_http_proxy')
    global_proxy_active = True

def proxy_off():
    global global_proxy_active
    if global_proxy_active:
        if 'HTTP_PROXY' in os.environ:
            del os.environ['HTTP_PROXY']
        if 'HTTPS_PROXY' in os.environ:
            del os.environ['HTTPS_PROXY']
        global_proxy_active = False

def timer_start(max_time):
    global timer
    timer = Timer(max_time, stop_config_time)
    timer.start()

def stop_config_time():
    print("Time limit reached. Request config will now stop.")
    stop_config()

def timer_stop():
    global timer
    if timer:
        timer.cancel()
        timer = None

# def get_headers_and_timeout(headers, timeout):
#     global global_use_fake_user_agent
#     global global_set_timeout
#     global global_force
#     if global_use_fake_user_agent:
#         if 'User-Agent' in headers:
#             if global_force:
#                 ua = UserAgent().random
#                 headers.update({'User-Agent': ua})
#         else:
#             ua = UserAgent().random
#             headers.update({'User-Agent': ua})
#     if global_set_timeout is not None:
#         if timeout is not None:
#             if global_force:
#                 timeout = global_set_timeout
#         else:
#             timeout = global_set_timeout
#     return headers, timeout

def change_proxy(proxy: str):
    try:
        dotenv.set_key('.env', 'PROXY', proxy)
        print(f"Proxy has been changed to {proxy}.")
    except Exception as e:
        print(f"Change failed. Error: {e}")