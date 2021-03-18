# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/3/18 16:48
Desc: 同花顺-板块-概念板块-成份股
http://q.10jqka.com.cn/gn/detail/code/301558/
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from py_mini_racer import py_mini_racer
from tqdm import tqdm


def stock_board_concept_name_ths() -> pd.DataFrame:
    """
    同花顺-板块-概念板块-概念
    http://q.10jqka.com.cn/gn/detail/code/301558/
    :return: 所有概念板块的名称和链接
    :rtype: pandas.DataFrame
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }
    url = 'http://q.10jqka.com.cn/gn/'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    html_list = soup.find('div', attrs={'class': 'boxShadow'}).find_all('a', attrs={'target': '_blank'})
    name_list = [item.text for item in html_list]
    url_list = [item['href'] for item in html_list]
    temp_df = pd.DataFrame([name_list, url_list], index=['name', 'url']).T
    return temp_df


def stock_board_concept_cons_ths(symbol_code: str = "阿里巴巴概念") -> pd.DataFrame:
    """
    同花顺-板块-概念板块-成份股
    http://q.10jqka.com.cn/gn/detail/code/301558/
    :param symbol_code: 板块名称
    :type symbol_code: str
    :return: 成份股
    :rtype: pandas.DataFrame
    """
    stock_board_ths_map_df = stock_board_concept_name_ths()
    symbol_code = stock_board_ths_map_df[stock_board_ths_map_df['name'] == symbol_code]['url'].values[0].split('/')[-2]
    with open('./aes.min.js', 'r') as f:
        js_content = f.read()
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(js_content)
    v_code = js_code.call('v')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Cookie': f'v={v_code}'
    }
    url = f'http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/1/ajax/1/code/{symbol_code}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    page_num = int(soup.find_all('a', attrs={'class': 'changePage'})[-1]['page'])
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num+1)):
        v_code = js_code.call('v')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Cookie': f'v={v_code}'
        }
        url = f'http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/{page}/ajax/1/code/{symbol_code}'
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.rename({"涨跌幅(%)": "涨跌幅",
                   "涨速(%)": "涨速",
                   "换手(%)": "换手",
                   "振幅(%)": "振幅",
                   }, inplace=True, axis=1)
    del big_df['加自选']
    return big_df


if __name__ == '__main__':
    stock_board_concept_name_ths_df = stock_board_concept_name_ths()
    print(stock_board_concept_name_ths_df)
    stock_board_ths_df = stock_board_concept_cons_ths(symbol_code="人脸识别")
    print(stock_board_ths_df)
