#!/usr/bin/env python
"""
Date: 2026/10/30
Desc: 全局网络配置：代理与超时
所有经 akshare.utils.http 发出的请求在调用时读取这里的值，运行中修改立即生效
"""

# 连接超时 10 秒、读取超时 60 秒。读取超时是两次收到数据之间的最长间隔，
# 不是整个请求的总时长，持续传输的大文件不会因此中断。
DEFAULT_TIMEOUT = (10, 60)


class AkshareConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.proxies = None
            cls._instance.timeout = DEFAULT_TIMEOUT
        return cls._instance

    @classmethod
    def set_proxies(cls, proxies):
        cls().proxies = proxies

    @classmethod
    def get_proxies(cls):
        return cls().proxies

    @classmethod
    def set_timeout(cls, timeout):
        cls().timeout = timeout

    @classmethod
    def get_timeout(cls):
        return cls().timeout


config = AkshareConfig()


def set_proxies(proxies):
    """
    设置全局代理，对经 akshare.utils.http 发出的请求生效，涵盖绝大多数数据接口
    :param proxies: requests 格式的代理字典，如 {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}；None 表示不指定，此时沿用 HTTP_PROXY、HTTPS_PROXY 环境变量
    :type proxies: dict
    """
    config.set_proxies(proxies)


def get_proxies():
    """
    获取当前的全局代理
    :return: 代理字典，未设置时为 None
    :rtype: dict
    """
    return config.get_proxies()


def set_timeout(timeout):
    """
    设置全局请求超时，对经 akshare.utils.http 发出的请求生效，涵盖绝大多数数据接口
    :param timeout: 秒数，或由连接超时与读取超时组成的二元组；None 表示不限时
    :type timeout: float or tuple
    """
    config.set_timeout(timeout)


def get_timeout():
    """
    获取当前的全局请求超时
    :return: 秒数，或由连接超时与读取超时组成的二元组，默认 (10, 60)
    :rtype: float or tuple
    """
    return config.get_timeout()


class ProxyContext:
    """
    在 with 代码块内临时使用指定代理，退出时恢复原设置
    """

    def __init__(self, proxies):
        self.proxies = proxies
        self.old_proxies = None

    def __enter__(self):
        self.old_proxies = config.get_proxies()
        config.set_proxies(self.proxies)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        config.set_proxies(self.old_proxies)
        return False  # 不处理异常
