# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/5/9 18:08
Desc: 导入文件工具，可以正确处理路径问题
"""
from importlib import resources
import pathlib


def get_ths_js(file: str = "ths.js") -> pathlib.Path:
    """Get path to data "ths.js" text file.

    Returns
    -------
    pathlib.PosixPath
        Path to file.

    References
    ----------
    .. [1] E.A.Abbott, ”Flatland”, Seeley & Co., 1884.
    """
    with resources.path("akshare.data", file) as f:
        data_file_path = f
        return data_file_path


def get_crypto_info_csv(file: str = "crypto_info.zip") -> pathlib.Path:
    """Get path to data "ths.js" text file.

    Returns
    -------
    pathlib.PosixPath
        Path to file.

    References
    ----------
    .. [1] E.A.Abbott, ”Flatland”, Seeley & Co., 1884.
    """
    with resources.path("akshare.data", file) as f:
        data_file_path = f
        return data_file_path


def get_covid_js(file: str = "covid.js") -> pathlib.Path:
    """Get path to data "ths.js" text file.

    Returns
    -------
    pathlib.PosixPath
        Path to file.

    References
    ----------
    .. [1] E.A.Abbott, ”Flatland”, Seeley & Co., 1884.
    """

    with resources.path("akshare.data", file) as f:
        data_file_path = f
        return data_file_path


if __name__ == "__main__":
    get_ths_js_path = get_ths_js(file="ths.js")
    print(get_ths_js_path)

    get_crypto_info_csv_path = get_crypto_info_csv(file="crypto_info.zip")
    print(get_crypto_info_csv_path)

    get_covid_js_path = get_covid_js(file="covid.js")
    print(get_covid_js_path)
