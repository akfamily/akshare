# !/usr/bin/env python
"""
Date: 2025/3/10 18:00
Desc: 通用帮助函数
"""

import math
from typing import List, Dict

import pandas as pd
import requests

from akshare.utils.tqdm import get_tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urlencode
import time
import json


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
    r = requests.get(url, params=params, timeout=timeout)
    data_json = r.json()
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
        r = requests.get(url, params=params, timeout=timeout)
        data_json = r.json()
        inner_temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_list.append(inner_temp_df)
    # 合并所有数据
    temp_df = pd.concat(temp_list, ignore_index=True)
    temp_df["f3"] = pd.to_numeric(temp_df["f3"], errors="coerce")
    temp_df.sort_values(by=["f3"], ascending=False, inplace=True, ignore_index=True)
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df["index"].astype(int) + 1
    return temp_df


def fetch_paginated_data_2(url: str, base_params: Dict, timeout: int = 15):
    """
    不用requests.get，用chromedriver
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
    data_json = driver_get(url, params=params, timeout=timeout)
    formatted = json.dumps(data_json, indent=2, ensure_ascii=False)
    print(formatted)
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
        r = requests.get(url, params=params, timeout=timeout)
        data_json = r.json()
        inner_temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_list.append(inner_temp_df)
    # 合并所有数据
    temp_df = pd.concat(temp_list, ignore_index=True)
    temp_df["f3"] = pd.to_numeric(temp_df["f3"], errors="coerce")
    temp_df.sort_values(by=["f3"], ascending=False, inplace=True, ignore_index=True)
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df["index"].astype(int) + 1
    return temp_df


def driver_get(url, params, timeout):
    """
    通过webdriver访问网址
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

    # 指定浏览器和驱动路径
    chrome_binary_path = r"D:\Program Files\chrome-win64\141.0.7390.78\chrome.exe"  # 修改为你的 Chrome 路径
    chromedriver_path = r"D:\Program Files\chromedriver-win64\141.0.7390.78\chromedriver.exe"  # 修改为你的驱动路径

    chrome_options.binary_location = chrome_binary_path
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    full_url = f"{url}?{urlencode(params)}"

    try:
        driver.get(full_url)
        if timeout < 1:
            time.sleep(1)
        else:
            time.sleep(3)

        pre_element = driver.find_element(By.TAG_NAME, "pre")
        data = json.loads(pre_element.text)
        print("请求成功！")
        return data
    except Exception as e:
        print(f"Selenium 请求失败: {e}")
        return None
    finally:
        driver.quit()


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
    data_json = request_get_by_update_cookies(url, params=params, timeout=timeout)
    formatted = json.dumps(data_json, indent=2, ensure_ascii=False)
    print(formatted)
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
        r = requests.get(url, params=params, timeout=timeout)
        data_json = r.json()
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
    print("获取股票数据...")
    try:
        response = session.get(url, params=params, headers=headers, timeout=timeout)
        print(f"API响应状态: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                print("数据获取成功！")
                return data
            else:
                print("数据格式异常")
        else:
            print(f"请求失败: {response.status_code}")

    except Exception as e:
        print(f"获取数据失败: {e}")

    return None











    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

    # 指定浏览器和驱动路径
    chrome_binary_path = r"D:\Program Files\chrome-win64\141.0.7390.78\chrome.exe"  # 修改为你的 Chrome 路径
    chromedriver_path = r"D:\Program Files\chromedriver-win64\141.0.7390.78\chromedriver.exe"  # 修改为你的驱动路径

    chrome_options.binary_location = chrome_binary_path
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    full_url = f"{url}?{urlencode(params)}"

    try:
        driver.get(full_url)
        if timeout < 1:
            time.sleep(1)
        else:
            time.sleep(3)

        pre_element = driver.find_element(By.TAG_NAME, "pre")
        data = json.loads(pre_element.text)
        print("请求成功！")
        return data
    except Exception as e:
        print(f"Selenium 请求失败: {e}")
        return None
    finally:
        driver.quit()


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
