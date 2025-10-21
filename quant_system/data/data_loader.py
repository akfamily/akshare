"""
数据加载器 - 优先使用缓存，失败时使用模拟数据
"""

import os
import pickle
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from data.fetcher.akshare_api import AKShareAPI
from utils.logger import logger


class DataLoader:
    """统一的数据加载接口"""

    def __init__(self, cache_dir='data/cache', use_cache=True):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.use_cache = use_cache
        self.api = AKShareAPI()
        self.logger = logger

    def get_macro_data(self, indicator='cpi', use_mock=False):
        """
        获取宏观数据

        Args:
            indicator: 'gdp', 'cpi', 'ppi', 'pmi', 'm2', 'social_financing'
            use_mock: 是否强制使用模拟数据

        Returns:
            DataFrame
        """
        if use_mock:
            return self._get_mock_macro_data(indicator)

        # 尝试从缓存加载
        if self.use_cache:
            cached_data = self._load_from_cache('macro_data')
            if cached_data and indicator in cached_data:
                self.logger.info(f"从缓存加载{indicator}数据")
                return cached_data[indicator]

        # 从API获取
        try:
            self.logger.info(f"从AKShare获取{indicator}数据")
            if indicator == 'cpi':
                data = self.api.get_macro_china_cpi()
            elif indicator == 'ppi':
                data = self.api.get_macro_china_ppi()
            elif indicator == 'pmi':
                data = self.api.get_macro_china_pmi()
            elif indicator == 'gdp':
                data = self.api.get_macro_china_gdp()
            elif indicator == 'm2':
                data = self.api.get_macro_china_m2()
            else:
                data = pd.DataFrame()

            if not data.empty:
                return data

        except Exception as e:
            self.logger.error(f"获取{indicator}数据失败: {e}")

        # 降级到模拟数据
        self.logger.warning(f"使用{indicator}模拟数据")
        return self._get_mock_macro_data(indicator)

    def get_latest_value(self, indicator, field='value'):
        """
        获取某个指标的最新值

        Args:
            indicator: 指标名称
            field: 字段名

        Returns:
            最新值（float）
        """
        data = self.get_macro_data(indicator)

        if data.empty:
            # 返回模拟值
            mock_values = {
                'cpi': 101.5,   # CPI同比
                'ppi': 102.0,   # PPI同比
                'pmi': 50.2,    # PMI
                'gdp': 5.2,     # GDP增速
                'm2': 10.5      # M2增速
            }
            return mock_values.get(indicator, 0.0)

        # 获取最新一行的数据
        try:
            # 尝试获取最后一行的第二列（通常是数值列）
            latest_value = data.iloc[-1, 1]
            return float(latest_value)
        except Exception as e:
            self.logger.error(f"解析{indicator}最新值失败: {e}")
            return 0.0

    def _load_from_cache(self, cache_name):
        """从缓存加载数据"""
        cache_file = self.cache_dir / f'{cache_name}.pkl'
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                self.logger.error(f"加载缓存失败: {e}")
        return None

    def _get_mock_macro_data(self, indicator):
        """生成模拟宏观数据（用于演示）"""
        dates = pd.date_range(end=datetime.now(), periods=36, freq='M')

        if indicator == 'cpi':
            values = np.random.uniform(98, 103, 36)
            column_name = 'CPI'
        elif indicator == 'ppi':
            values = np.random.uniform(95, 107, 36)
            column_name = 'PPI'
        elif indicator == 'pmi':
            values = np.random.uniform(48, 52, 36)
            column_name = 'PMI'
        elif indicator == 'gdp':
            values = np.random.uniform(4, 7, 12)  # 季度数据
            dates = dates[::3][:12]
            column_name = 'GDP增速'
        elif indicator == 'm2':
            values = np.random.uniform(8, 12, 36)
            column_name = 'M2同比'
        else:
            values = np.zeros(36)
            column_name = '数值'

        return pd.DataFrame({
            '日期': dates,
            column_name: values
        })

    def check_cache_status(self):
        """检查缓存状态"""
        last_download = self._load_from_cache('last_download')

        if last_download:
            download_date = datetime.strptime(last_download['date'], '%Y-%m-%d %H:%M:%S')
            age_days = (datetime.now() - download_date).days

            return {
                'has_cache': True,
                'download_date': last_download['date'],
                'age_days': age_days,
                'is_fresh': age_days <= 7
            }
        else:
            return {
                'has_cache': False,
                'download_date': None,
                'age_days': None,
                'is_fresh': False
            }


# 全局数据加载器实例
_data_loader = None


def get_data_loader():
    """获取全局数据加载器实例"""
    global _data_loader
    if _data_loader is None:
        _data_loader = DataLoader()
    return _data_loader
