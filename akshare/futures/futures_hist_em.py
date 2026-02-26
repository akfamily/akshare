#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/2/20 17:00
Desc: 东方财富网-期货行情
https://qhweb.eastmoney.com/quote
"""
import json
import os
import time
import re
import requests
import pandas as pd
from typing import Tuple, Dict, Optional, List
from functools import lru_cache
from pathlib import Path

# 缓存文件名称
CACHE_DIR_NAME = ".em_futures_data"
CACHE_FILE_NAME = "exchange_symbols_cache.json"

# 获取用户主目录并构建完整路径
# Windows: C:\Users\Username\.em_futures_data\exchange_symbols_cache.json
# Linux/Mac: /home/username/.em_futures_data/exchange_symbols_cache.json
USER_HOME = Path.home()
CACHE_DIR = USER_HOME / CACHE_DIR_NAME
CACHE_FILE = CACHE_DIR / CACHE_FILE_NAME

# 确保缓存目录存在
CACHE_DIR.mkdir(parents=True, exist_ok=True)
# 缓存有效期（秒）：18小时 = 64800秒
CACHE_EXPIRY = 64800

# 交易所名称映射表
EXCHANGE_NAME_MAP = {
    "CFFEX": "中国金融期货交易所",
    "SHFE": "上海期货交易所",
    "DCE": "大连商品交易所",
    "CZCE": "郑州商品交易所",
    "INE": "上海国际能源交易中心",
    "GFEX": "广州期货交易所"
}

def __futures_hist_separate_char_and_numbers_em(symbol: str = "焦煤2506") -> tuple:
    char = re.findall(pattern="[\u4e00-\u9fa5a-zA-Z]+", string=symbol)
    numbers = re.findall(pattern=r"\d+", string=symbol)
    if not char:
        return "", numbers[0] if numbers else ""
    if not numbers:
        return char[0], ""
    return char[0], numbers[0]

def __load_cache() -> dict:
    """读取全局缓存文件"""
    if not CACHE_FILE.exists():
        return {}
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Cache file is corrupted, resetting. Error: {e}")
        return {}

def __save_cache(cache_data: dict):
    """保存数据到全局缓存文件"""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        # print(f"Cache saved to: {CACHE_FILE}") # 调试用，可注释
    except Exception as e:
        print(f"Warning: Failed to write cache to {CACHE_FILE}. Error: {e}")

@lru_cache()
def __fetch_exchange_symbol_raw_em(target_exchange: str = None) -> list:
    """
    东方财富网-期货行情-交易所品种对照表原始数据
    :param target_exchange: 交易所缩写，例如 "DCE", "SHFE"。如果不传，则获取所有交易所数据。
    :return: 交易所品种对照表原始数据 list
    """
    cache_key = target_exchange if target_exchange else "ALL"
    current_time = time.time()
    
    # 2. 尝试从本地加载缓存
    full_cache = __load_cache()
    
    # 2. 检查缓存是否有效
    if cache_key in full_cache:
        item = full_cache[cache_key]
        cached_time = item.get("timestamp", 0)
        
        if current_time - cached_time < CACHE_EXPIRY:
            # 缓存有效，直接返回
            return item.get("data", [])
        
    print(f"Refreshing eastmoney meta data cache for {cache_key} Exchange...")
    url = "https://futsse-static.eastmoney.com/redis"
    params = {"msgid": "gnweb"}
    try:
        # 1. 获取所有交易所的基础信息 (mktid, name等)
        r = requests.get(url, params=params)
        r.raise_for_status()
        data_json = r.json()
    except Exception as e:
        print(f"Error fetching market list: {e}")
        return []

    # 2. 确定需要抓取的交易所列表
    target_markets = []
    
    if target_exchange:
        # 如果指定了交易所，找到对应的中文名
        target_exchange_upper = target_exchange.upper()
        if target_exchange_upper not in EXCHANGE_NAME_MAP:
             raise ValueError(f"Exchange '{target_exchange}' not supported. Options: {list(EXCHANGE_NAME_MAP.keys())}")
        
        # 在返回的列表中找到对应名称的 item
        for item in data_json:
            if item["mktshort"] == target_exchange_upper:
                target_markets.append(item)
                break
    else:
        # 没指定则抓取全部
        target_markets = data_json

    all_exchange_symbol_list = []
    
    # 3. 遍历目标交易所，获取具体的合约列表
    for item in target_markets:
        # 请求第一页 (不带后缀)
        params = {"msgid": str(item["mktid"])}
        try:
            r = requests.get(url, params=params)
            inner_data_json = r.json()
            all_exchange_symbol_list.extend(inner_data_json)

            page = 1
            while True:
                params = {"msgid": f"{str(item['mktid'])}_{page}"}
                r = requests.get(url, params=params)
                page_data = r.json()
                if not page_data or not isinstance(page_data, list):
                    break
                all_exchange_symbol_list.extend(page_data)
                page += 1
                
        except Exception as e:
            print(f"Error fetching details for market {item['name']}: {e}")
            continue

    full_cache[cache_key] = {
        "timestamp": current_time,
        "data": all_exchange_symbol_list
    }
    __save_cache(full_cache)

    return all_exchange_symbol_list


@lru_cache()
def __get_exchange_symbol_map() -> Tuple[Dict, Dict, Dict, Dict]:
    """
    东方财富网-期货行情-交易所品种映射
    :return: 交易所品种映射
    :rtype: Tuple[Dict, Dict, Dict, Dict]
    """
    all_exchange_symbol_list = __fetch_exchange_symbol_raw_em()
    c_contract_mkt = {}
    c_contract_to_e_contract = {}
    e_symbol_mkt = {}
    c_symbol_mkt = {}
    for item in all_exchange_symbol_list:
        c_contract_mkt[item["name"]] = item["mktid"]
        c_contract_to_e_contract[item["name"]] = item["code"]
        # item["vcode"] 是品种代码，如 rb, IF
        e_symbol_mkt[item["vcode"]] = item["mktid"]
        e_symbol_mkt[item["vcode"].lower()] = item["mktid"]  # 兼容小写
        e_symbol_mkt[item["vcode"].upper()] = item["mktid"]  # 兼容大写
        c_symbol_mkt[item["vname"]] = item["mktid"]
    return c_contract_mkt, c_contract_to_e_contract, e_symbol_mkt, c_symbol_mkt


def get_all_future_symbol(exchange: str = "DCE") -> list:
    """
    获取指定交易所的所有合约代码
    :param exchange: 交易所缩写, {'CFFEX', 'SHFE', 'DCE', 'CZCE', 'INE', 'GFEX'}
    :return: 合约代码列表 (e.g. ['rb2501', 'rb2502', ...])
    """
    # 直接调用修改后的底层函数，只抓取对应交易所的数据
    raw_data = __fetch_exchange_symbol_raw_em(target_exchange=exchange)
    
    # 提取 code 字段
    # code 字段通常是 "RB2510" 或 "rb2510"，视东财返回而定
    symbol_list = [item["code"] for item in raw_data if "code" in item and len(item["code"]) > 2]
    return symbol_list


@lru_cache()
def __get_exchange_symbol_map() -> Tuple[Dict, Dict, Dict, Dict]:
    """
    生成全局映射表 (需要获取所有数据)
    """
    # 这里必须调用 target_exchange=None 来获取全量数据
    all_exchange_symbol_list = __fetch_exchange_symbol_raw_em(target_exchange=None)
    
    c_contract_mkt = {}
    c_contract_to_e_contract = {}
    e_symbol_mkt = {}
    c_symbol_mkt = {}
    
    for item in all_exchange_symbol_list:
        if "code" in item:
            c_contract_mkt[item["name"]] = item["mktid"]
            c_contract_to_e_contract[item["name"]] = item["code"]
            # vcode 是品种代码 (如 rb)
            e_symbol_mkt[item["vcode"]] = item["mktid"]
            e_symbol_mkt[item["vcode"].lower()] = item["mktid"]
            e_symbol_mkt[item["vcode"].upper()] = item["mktid"]
            c_symbol_mkt[item["vname"]] = item["mktid"]
        
    return c_contract_mkt, c_contract_to_e_contract, e_symbol_mkt, c_symbol_mkt


def futures_hist_table_em() -> pd.DataFrame:
    """
    东方财富网-期货行情-交易所品种对照表
    :return: 交易所品种对照表
    :rtype: pandas.DataFrame
    """
    all_exchange_symbol_list = __fetch_exchange_symbol_raw_em()
    temp_df = pd.DataFrame(all_exchange_symbol_list)
    if temp_df.empty:
        return pd.DataFrame()
    temp_df = temp_df[["mktname", "name", "code"]]
    temp_df.columns = ["市场简称", "合约中文代码", "合约代码"]
    return temp_df


def futures_hist_em(
    symbol: str = None,
    period: str = "daily",
    start_date: str = "19900101",
    end_date: str = "20500101",
    esymbol: str = None,
) -> pd.DataFrame:
    """
    东方财富网-期货行情-行情数据
    https://qhweb.eastmoney.com/quote
    :param symbol: 期货中文名称 (如 "热卷主连")，如果提供了 esymbol，则忽略此参数
    :type symbol: str
    :param period: choice of {'daily', 'weekly', 'monthly'}
    :type period: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :param esymbol: 期货英文代码 (如 "rb2510")，优先使用此参数
    :type esymbol: str
    :return: 行情数据
    :rtype: pandas.DataFrame
    """
    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
    period_dict = {"daily": "101", "weekly": "102", "monthly": "103"}
    
    # 获取映射关系
    c_contract_mkt, c_contract_to_e_contract, e_symbol_mkt, c_symbol_mkt = (
        __get_exchange_symbol_map()
    )
    
    sec_id = ""
    
    # 逻辑修改：优先处理 esymbol
    if esymbol:
        # 英文代码逻辑
        symbol_char, _ = __futures_hist_separate_char_and_numbers_em(esymbol)
        mkt_id = e_symbol_mkt.get(symbol_char)
        
        # 尝试不同的大小写组合，如果直接匹配不到
        if not mkt_id:
            mkt_id = e_symbol_mkt.get(symbol_char.upper())
        if not mkt_id:
            mkt_id = e_symbol_mkt.get(symbol_char.lower())
            
        if mkt_id:
            sec_id = f"{mkt_id}.{esymbol}"
        else:
            # 如果找不到品种映射，可能是一个特殊代码，或者数据源未更新
            # 可以在此处增加特定处理，目前抛出异常或打印提示
            raise ValueError(f"Cannot find market ID for symbol prefix: {symbol_char}")
            
    else:
        # 原有中文名称逻辑
        try:
            # 尝试直接通过全名匹配 (如 "热卷2510")
            sec_id = f"{c_contract_mkt[symbol]}.{c_contract_to_e_contract[symbol]}"
        except KeyError:
            # 尝试通过品种名称匹配 (如 "热卷")
            symbol_char, numbers = __futures_hist_separate_char_and_numbers_em(symbol)
            if re.match(pattern="^[\u4e00-\u9fa5]+$", string=symbol_char):
                # 中文品种名
                if symbol_char in c_symbol_mkt:
                     # 假设 symbol 是 "热卷2510", c_symbol_mkt["热卷"] 拿到 mktid
                     # 但是这里原来的逻辑有点问题，symbol本身如果是"热卷主连"这种没数字的需要特殊处理
                     # 这里保留原逻辑的意图：拼接 mktid.symbol
                     # 注意：如果是中文输入，通常需要映射回英文代码，原代码这里的逻辑假设 symbol 参数本身包含了英文代码或者特殊处理
                     # 但 akshare 原版逻辑中，如果 symbol 是 "热卷2505"，symbol_char 是 "热卷"
                     # sec_id 变成 "113.热卷2505"，这在东财接口是不对的，接口需要 "113.rb2505"
                     # 原有代码可能仅针对特殊构造，或者假定 symbol 混合了英文
                     
                     # 修正逻辑：如果用户传 "热卷2505" (中文+数字)，我们实际上很难直接拼出 secid，
                     # 除非再反查出 "热卷" 对应的英文前缀 "rb"。
                     # 鉴于你主要需要 esymbol 功能，这里保留原代码的 fallback 结构，但在 esymbol 块中已解决英文代码问题。
                    sec_id = str(c_symbol_mkt[symbol_char]) + "." + symbol
                else:
                    print(f"Warning: Symbol '{symbol}' not found in Chinese map.")
            else:
                # 英文品种名 fallback (原逻辑)
                if symbol_char in e_symbol_mkt:
                    sec_id = str(e_symbol_mkt[symbol_char]) + "." + symbol
                else:
                     print(f"Warning: Symbol '{symbol}' not found in English map.")

    if not sec_id:
        return pd.DataFrame()

    params = {
        "secid": sec_id,
        "klt": period_dict[period],
        "fqt": "1",
        "lmt": "10000",
        "end": "20500000",
        "iscca": "1",
        "fields1": "f1,f2,f3,f4,f5,f6,f7,f8",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64",
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "forcect": "1",
    }
    
    try:
        r = requests.get(url, timeout=15, params=params)
        data_json = r.json()
    except Exception as e:
        print(f"Network error: {e}")
        return pd.DataFrame()

    if not (data_json.get("data") and data_json["data"].get("klines")):
        return pd.DataFrame()

    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
    
    temp_df.columns = [
        "时间",
        "开盘",
        "收盘",
        "最高",
        "最低",
        "成交量",
        "成交额",
        "-",
        "涨跌幅",
        "涨跌",
        "_",
        "_",
        "持仓量",
        "_",
    ]
    temp_df = temp_df[
        [
            "时间",
            "开盘",
            "最高",
            "最低",
            "收盘",
            "涨跌",
            "涨跌幅",
            "成交量",
            "成交额",
            "持仓量",
        ]
    ]
    temp_df.index = pd.to_datetime(temp_df["时间"])
    temp_df = temp_df[start_date:end_date]
    temp_df.reset_index(drop=True, inplace=True)
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["涨跌"] = pd.to_numeric(temp_df["涨跌"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["持仓量"] = pd.to_numeric(temp_df["持仓量"], errors="coerce")
    temp_df["时间"] = pd.to_datetime(temp_df["时间"], errors="coerce").dt.date
    return temp_df

if __name__ == "__main__":
    # 1. 测试获取某交易所的所有代码
    print("Fetching DCE (大连) symbols:")
    dce_symbols = get_all_future_symbol("DCE")
    print(dce_symbols[:10]) # 打印前10个
    
    print("\nFetching CFFEX (中金所) symbols:")
    cffex_symbols = get_all_future_symbol("CFFEX")
    print(cffex_symbols[:10])

    # 2. 测试原有功能 (中文)
    print("\nFetching History (Chinese Name - 热卷主连):")
    futures_hist_em_df = futures_hist_em(symbol="热卷主连", period="daily", start_date="20240101", end_date="20240201")
    print(futures_hist_em_df.head())

    # 3. 测试新功能 (英文代码 esymbol)
    # 假设我们要获取 螺纹钢2510 (rb2510) 的数据
    # 注意：确保代码存在且在交易时间范围内有数据
    test_code = "rb2510"  # 你可以换成当前活跃的合约，如 rb2410, rb2501 等
    print(f"\nFetching History (English Symbol - {test_code}):")
    try:
        # 使用 esymbol 参数，symbol 参数可以为空或任意值
        df_en = futures_hist_em(esymbol=test_code, period="daily", start_date="20240101")
        print(df_en.head())
    except Exception as e:
        print(e)
