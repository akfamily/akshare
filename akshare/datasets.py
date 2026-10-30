# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2026/10/30
Desc: 导入文件工具，可以正确处理路径问题
"""

import pathlib
from importlib import resources


def _data_path(file: str) -> pathlib.Path:
    """
    返回 akshare/data 下文件的路径
    原先用 importlib.resources.path，它自 Python 3.11 起弃用，而且返回的路径只在 with 块内
    保证有效，块结束后就 return 出去。akshare 总是以普通目录安装，files() 返回的就是磁盘上的
    真实路径，可以直接使用
    """
    return pathlib.Path(str(resources.files("akshare.data").joinpath(file)))


def get_ths_js(file: str = "ths.js") -> pathlib.Path:
    """
    get path to data "ths.js" text file.
    :return: 文件路径
    :rtype: pathlib.Path
    """
    return _data_path(file)


def get_crypto_info_csv(file: str = "crypto_info.zip") -> pathlib.Path:
    """
    get path to data "ths.js" text file.
    :return: 文件路径
    :rtype: pathlib.Path
    """
    return _data_path(file)


def get_data_file(file: str) -> pathlib.Path:
    """
    获取 akshare/data 下内置数据文件的路径，如 calendar.json、jm.js
    :param file: 文件名
    :type file: str
    :return: 文件路径
    :rtype: pathlib.Path
    """
    return _data_path(file)


def get_registry_json(file: str = "interfaces.json") -> pathlib.Path:
    """
    get path to data "interfaces.json" file.
    :return: 文件路径
    :rtype: pathlib.Path
    """
    return _data_path(file)


if __name__ == "__main__":
    get_ths_js_path = get_ths_js(file="ths.js")
    print(get_ths_js_path)

    get_crypto_info_csv_path = get_crypto_info_csv(file="crypto_info.zip")
    print(get_crypto_info_csv_path)

    get_registry_json_path = get_registry_json(file="interfaces.json")
    print(get_registry_json_path)
