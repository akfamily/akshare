# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2021/10/31 16:08
Desc: 同花顺-数据中心-技术选股
http://data.10jqka.com.cn/rank/cxg/
"""
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup
from py_mini_racer import py_mini_racer
from tqdm import tqdm


def _get_js_path_ths(name: str = None, module_file: str = None) -> str:
    """
    获取 JS 文件的路径(从模块所在目录查找)
    :param name: 文件名
    :type name: str
    :param module_file: 模块路径
    :type module_file: str
    :return: 路径
    :rtype: str
    """
    module_folder = os.path.abspath(os.path.dirname(os.path.dirname(module_file)))
    module_json_path = os.path.join(module_folder, "stock_feature", name)
    return module_json_path


def _get_file_content_ths(file_name: str = "ase.min.js") -> str:
    """
    获取 JS 文件的内容
    :param file_name:  JS 文件名
    :type file_name: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_name = file_name
    setting_file_path = _get_js_path_ths(setting_file_name, __file__)
    with open(setting_file_path) as f:
        file_data = f.read()
    return file_data


def stock_rank_cxg_ths(symbol: str = "创月新高") -> pd.DataFrame:
    """
    同花顺-数据中心-技术选股-创新高
    http://data.10jqka.com.cn/rank/cxg/
    :param symbol: choice of {"创月新高", "半年新高", "一年新高", "历史新高"}
    :type symbol: str
    :return: 创新高数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "创月新高": "4",
        "半年新高": "3",
        "一年新高": "2",
        "历史新高": "1",
    }
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call('v')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Cookie': f'v={v_code}'
    }
    url = f'http://data.10jqka.com.cn/rank/cxg/board/{symbol_map[symbol]}/field/stockcode/order/asc/page/1/ajax/1/free/1/'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    try:
        total_page = soup.find("span", attrs={'class': 'page_info'}).text.split('/')[1]
    except AttributeError as e:
        total_page = 1
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(total_page)+1), leave=False):
        v_code = js_code.call('v')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Cookie': f'v={v_code}'
        }
        url = f'http://data.10jqka.com.cn/rank/cxg/board/{symbol_map[symbol]}/field/stockcode/order/asc/page/{page}/ajax/1/free/1/'
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = ['序号', '股票代码', '股票简称', '涨跌幅', '换手率', '最新价', '前期高点', '前期高点日期']
    big_df['股票代码'] = big_df['股票代码'].astype(str).str.zfill(6)
    big_df['涨跌幅'] = big_df['涨跌幅'].str.strip("%")
    big_df['换手率'] = big_df['换手率'].str.strip("%")
    big_df['前期高点日期'] = pd.to_datetime(big_df['前期高点日期']).dt.date
    big_df['涨跌幅'] = pd.to_numeric(big_df['涨跌幅'])
    big_df['换手率'] = pd.to_numeric(big_df['换手率'])
    big_df['最新价'] = pd.to_numeric(big_df['最新价'])
    big_df['前期高点'] = pd.to_numeric(big_df['前期高点'])
    return big_df


def stock_rank_cxd_ths(symbol: str = "创月新低") -> pd.DataFrame:
    """
    同花顺-数据中心-技术选股-创新低
    http://data.10jqka.com.cn/rank/cxd/
    :param symbol: choice of {"创月新低", "半年新低", "一年新低", "历史新低"}
    :type symbol: str
    :return: 创新低数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "创月新低": "4",
        "半年新低": "3",
        "一年新低": "2",
        "历史新低": "1",
    }
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call('v')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Cookie': f'v={v_code}'
    }
    url = f'http://data.10jqka.com.cn/rank/cxd/board/{symbol_map[symbol]}/field/stockcode/order/asc/page/1/ajax/1/free/1/'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    try:
        total_page = soup.find("span", attrs={'class': 'page_info'}).text.split('/')[1]
    except AttributeError as e:
        total_page = 1
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(total_page)+1), leave=False):
        v_code = js_code.call('v')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Cookie': f'v={v_code}'
        }
        url = f'http://data.10jqka.com.cn/rank/cxd/board/{symbol_map[symbol]}/field/stockcode/order/asc/page/{page}/ajax/1/free/1/'
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = ['序号', '股票代码', '股票简称', '涨跌幅', '换手率', '最新价', '前期低点', '前期低点日期']
    big_df['股票代码'] = big_df['股票代码'].astype(str).str.zfill(6)
    big_df['涨跌幅'] = big_df['涨跌幅'].str.strip("%")
    big_df['换手率'] = big_df['换手率'].str.strip("%")
    big_df['前期低点日期'] = pd.to_datetime(big_df['前期低点日期']).dt.date
    big_df['涨跌幅'] = pd.to_numeric(big_df['涨跌幅'])
    big_df['换手率'] = pd.to_numeric(big_df['换手率'])
    big_df['最新价'] = pd.to_numeric(big_df['最新价'])
    big_df['前期低点'] = pd.to_numeric(big_df['前期低点'])
    return big_df


if __name__ == '__main__':
    stock_rank_cxg_ths_df = stock_rank_cxg_ths(symbol="创月新高")
    print(stock_rank_cxg_ths_df)

    stock_rank_cxg_ths_df = stock_rank_cxg_ths(symbol="半年新高")
    print(stock_rank_cxg_ths_df)

    stock_rank_cxg_ths_df = stock_rank_cxg_ths(symbol="一年新高")
    print(stock_rank_cxg_ths_df)

    stock_rank_cxg_ths_df = stock_rank_cxg_ths(symbol="历史新高")
    print(stock_rank_cxg_ths_df)

    stock_rank_cxd_ths_df = stock_rank_cxd_ths(symbol="创月新低")
    print(stock_rank_cxd_ths_df)

    stock_rank_cxd_ths_df = stock_rank_cxd_ths(symbol="半年新低")
    print(stock_rank_cxd_ths_df)

    stock_rank_cxd_ths_df = stock_rank_cxd_ths(symbol="一年新低")
    print(stock_rank_cxd_ths_df)

    stock_rank_cxd_ths_df = stock_rank_cxd_ths(symbol="历史新低")
    print(stock_rank_cxd_ths_df)
