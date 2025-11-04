# !/usr/bin/env python
"""
Date: 2025/3/10 18:00
Desc: 通用帮助函数
"""

import math
import random
from typing import List, Dict

import pandas as pd
import requests

import undetected_chromedriver as uc
from akshare.utils.tqdm import get_tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urlencode
import time
import json

from t.trequest.requests0_manual_set_cookie import get_cookie

BROWSER_EXECUTABLE_PATH = r"D:\Program Files\chrome-win64\141.0.7390.78\chrome.exe"  # chrome.exe 路径
DRIVER_EXECUTABLE_PATH = r"D:\Program Files\chromedriver-win64\141.0.7390.78\chromedriver.exe"  # chromedriver.exe 路径


def fetch_paginated_data(url: str, base_params: Dict, timeout: int = 15):
    """
    东方财富-分页获取数据并合并结果
    https://quote.eastmoney.com/f1.html?newcode=0.000001
    :param url: 股票代码
    :type url: str
    :param base_params: 基础请求参数
    :type base_params: dict
    :param timeout: 请求超时时间
    :type timeout: str
    :return: 合并后的数据
    :rtype: pandas.DataFrame
    """
    # 复制参数以避免修改原始参数
    params = base_params.copy()
    # 获取第一页数据，用于确定分页信息
    # 返回信息:
    # {
    #   "rc": 0,           // 返回码，0表示成功
    #   "rt": 6,           // 响应时间
    #   "svr": 181669449,  // 服务器标识
    #   "lt": 1,           // 未知参数
    #   "full": 1,         // 是否完整
    #   "dlmkts": "",      // 市场延迟
    #   "data": {
    #     "total": 1277,   // 总数据条数
    #     "diff": [        // 实际数据数组
    #       {
    #         "f3": 1.79,   // 涨跌幅
    #         "f12": "516210", // ETF代码
    #         "f13": 1        // 市场标识（1-沪市，2-深市）
    #       }
    #     ]
    #   }
    # }
    # r = requests.get(url, params=params, timeout=timeout)
    # data_json = r.json()
    data_json = driver_get(url, params=params, timeout=timeout)
    # 计算分页信息
    per_page_num = len(data_json["data"]["diff"])
    total_page = math.ceil(data_json["data"]["total"] / per_page_num)
    print(f'total_page: {total_page}')
    # 存储所有页面数据
    temp_list = []
    # 添加第一页数据
    temp_list.append(pd.DataFrame(data_json["data"]["diff"]))
    # 获取进度条
    tqdm = get_tqdm()
    # 获取剩余页面数据
    for page in tqdm(range(2, total_page + 1), leave=False):
        params.update({"pn": page})
        # r = requests.get(url, params=params, timeout=timeout)
        # data_json = r.json()
        data_json = driver_get(url, params=params, timeout=timeout)
        inner_temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_list.append(inner_temp_df)
    # 合并所有数据
    temp_df = pd.concat(temp_list, ignore_index=True)
    temp_df["f3"] = pd.to_numeric(temp_df["f3"], errors="coerce")
    temp_df.sort_values(by=["f3"], ascending=False, inplace=True, ignore_index=True)
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df["index"].astype(int) + 1
    return temp_df

PRE_URL = "https://eastmoney.com"
DRIVER_GET_INDEX_SLEEP_TIME = 1.5  # driver_get主页等待时间
DRIVER_GET_SLEEP_TIME = 3  # driver_get其他网址等待时间


def driver_get(url, params, timeout):
    try:
        # 指定 Chrome 浏览器路径和驱动路径
        driver = uc.Chrome(
            browser_executable_path=BROWSER_EXECUTABLE_PATH,  # chrome.exe路径
            driver_executable_path=DRIVER_EXECUTABLE_PATH  # chromedriver.exe路径
        )

        print('访问主页...')
        driver.get(PRE_URL)
        time.sleep(get_sleep_time(DRIVER_GET_INDEX_SLEEP_TIME))

        full_url = f"{url}?{urlencode(params)}"
        print(f"访问URL: {full_url}")
        driver.get(full_url)
        time.sleep(get_sleep_time(DRIVER_GET_SLEEP_TIME))

        pre_element = driver.find_element(By.TAG_NAME, "pre")
        data = json.loads(pre_element.text)
        with open("data/t_data0.txt", "a", encoding="utf-8") as file:
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
            file.write(f'获取数据成功:\n{json_str}\n')
        return data
    except Exception as e:
        print(f"错误: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

def get_sleep_time(n):
    """
    根据给定睡眠时间随机生成睡眠时间
    """
    if n < 1.5:
        return random.uniform(n, n + 0.5)
    return random.uniform(n - 0.5, n + 0.5)

def fetch_paginated_data_3(url: str, base_params: Dict, timeout: int = 15):
    """
    直接访问拿不到数据的原因就是缺cookie，所以先访问东方财富主页拿到cookie，然后再访问指定网址
    东方财富-分页获取数据并合并结果
    https://quote.eastmoney.com/f1.html?newcode=0.000001
    :param url: 股票代码
    :type url: str
    :param base_params: 基础请求参数
    :type base_params: dict
    :param timeout: 请求超时时间
    :type timeout: str
    :return: 合并后的数据
    :rtype: pandas.DataFrame
    """
    # 复制参数以避免修改原始参数
    params = base_params.copy()
    # 获取第一页数据，用于确定分页信息
    # r = requests.get(url, params=params, timeout=timeout)
    # data_json = request_get_by_update_cookies(url, params=params, timeout=timeout)
    data_json = request_get_by_manual_set_cookies(url, params=params, timeout=timeout)
    # formatted = json.dumps(data_json, indent=2, ensure_ascii=False)
    # print(formatted)
    # 计算分页信息
    per_page_num = len(data_json["data"]["diff"])
    total_page = math.ceil(data_json["data"]["total"] / per_page_num)
    # 存储所有页面数据
    temp_list = []
    # 添加第一页数据
    temp_list.append(pd.DataFrame(data_json["data"]["diff"]))
    # 获取进度条
    tqdm = get_tqdm()
    # 获取剩余页面数据
    for page in tqdm(range(2, total_page + 1), leave=False):
        params.update({"pn": page})
        # r = requests.get(url, params=params, timeout=timeout)
        # data_json = r.json()
        data_json = request_get_by_manual_set_cookies(url, params=params, timeout=timeout)
        inner_temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_list.append(inner_temp_df)
    # 合并所有数据
    temp_df = pd.concat(temp_list, ignore_index=True)
    temp_df["f3"] = pd.to_numeric(temp_df["f3"], errors="coerce")
    temp_df.sort_values(by=["f3"], ascending=False, inplace=True, ignore_index=True)
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df["index"].astype(int) + 1
    return temp_df


def request_get_by_update_cookies(url, params, timeout):
    """
    先访问东方财富主页拿到cookie，然后再访问指定网址
    """
    session = requests.Session()

    # 设置基础headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://quote.eastmoney.com/',
    }

    # 1. 先访问东方财富主页获取Cookie
    print("获取Cookie...")
    try:
        main_response = session.get("https://www.eastmoney.com/", headers=headers, timeout=10)
        print(f"主页访问状态: {main_response.status_code}")
        time.sleep(2)  # 等待Cookie设置
    except Exception as e:
        print(f"获取Cookie失败: {e}")
        return None

    # 2. 访问API获取数据
    # print("获取股票数据...")
    try:
        response = session.get(url, params=params, headers=headers, timeout=timeout)
        # print(f"API响应状态: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                # print("数据获取成功！")
                return data
            else:
                print("数据格式异常")
        else:
            print(f"请求失败: {response.status_code}")

    except Exception as e:
        print(f"获取数据失败: {e}")

    return None


def request_get_by_manual_set_cookies(url, params, timeout):
    # print("获取股票数据...")
    try:
        cookie = get_cookie()
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'connection': 'keep-alive',
            'host': '88.push2.eastmoney.com',
            'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',
            # 从你的成功请求中复制完整的cookie
            'cookie': cookie
        }
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        # print(f"API响应状态: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                # print("数据获取成功！")
                return data
            else:
                print("数据格式异常")
        else:
            print(f"请求失败: {response.status_code}")

    except Exception as e:
        print(f"获取数据失败: {e}")

    return None


def set_df_columns(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """
    设置 pandas.DataFrame 为空的情况
    :param df: 需要设置命名的数据框
    :type df: pandas.DataFrame
    :param cols: 字段的列表
    :type cols: list
    :return: 重新设置后的数据
    :rtype: pandas.DataFrame
    """
    if df.shape == (0, 0):
        return pd.DataFrame(data=[], columns=cols)
    else:
        df.columns = cols
        return df


if __name__ == '__main__':
    with open("data/t_data0.txt", "a", encoding="utf-8") as file:
        t_json_str = '{}'
        file.write(f'获取数据成功:\n{t_json_str}\n')