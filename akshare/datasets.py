# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/5/9 18:08
Desc: 导入文件工具，可以正确处理路径问题
"""
from importlib import resources


def get_ths_js(file: str = "ths.js"):
    """Get path to example "Flatland" [1]_ text file.

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


if __name__ == '__main__':
    temp_path = get_ths_js(file="ths.js")
    print(temp_path)
