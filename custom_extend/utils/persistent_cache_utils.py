# -*- coding:utf-8 -*-
import json
# Author: PeterWeyland
# CreateTime: 2025-11-04
# Description: 持久化缓存，存到磁盘文件
import pickle
import os
from functools import lru_cache
from typing import Dict


def save_fund_etf_code_id_map_em_cache(data: Dict[str, int], filename: str = "persistent_cache/fund_etf_code_id_map_em_cache.json"):
    """
    保存ETF数据到JSON文件
    """
    try:
        # 确保目录存在
        dir_path = os.path.dirname(filename)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        # 保存为JSON格式
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 ETF数据已保存到: {filename}")
        return True
    except Exception as e:
        print(f"❌ 保存缓存失败: {e}")
        return False


def load_fund_etf_code_id_map_em_cache(filename: str = "persistent_cache/fund_etf_code_id_map_em_cache.json") -> Dict[str, int]:
    """
    从JSON文件加载ETF数据
    """
    try:
        if not os.path.exists(filename):
            return {}
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"📁 从缓存加载ETF数据: {filename}")
        return data
    except Exception as e:
        print(f"❌ 加载缓存失败: {e}")
        return {}