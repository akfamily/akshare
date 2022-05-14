#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/5/9 18:16
Desc: To test intention, just write test code here!
"""
from akshare.cost.cost_living import cost_living
from akshare.datasets import get_ths_js, get_crypto_info_csv
import pathlib


def test_cost_living():
    """
    just for test aim
    :return: assert result
    :rtype: assert
    """
    cost_living_df = cost_living()
    assert cost_living_df.shape[0] > 0


def test_path_func():
    """
    test path func
    :return: path of file
    :rtype: pathlib.Path
    """
    temp_path = get_ths_js("ths.js")
    assert isinstance(temp_path, pathlib.Path)


def test_zipfile_func():
    """
    test path func
    :return: path of file
    :rtype: pathlib.Path
    """
    temp_path = get_crypto_info_csv("crypto_info.zip")
    assert isinstance(temp_path, pathlib.Path)


if __name__ == "__main__":
    test_cost_living()
    test_path_func()
    test_zipfile_func()
