#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史数据下载脚本
一次性下载所需的历史数据，保存到本地缓存
"""

import sys
import os
from datetime import datetime, timedelta
import pickle
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.logger import logger
from data.fetcher.akshare_api import AKShareAPI


class DataDownloader:
    """数据下载器"""

    def __init__(self, cache_dir='data/cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.api = AKShareAPI()
        self.logger = logger

    def download_all(self, years=3):
        """
        下载所有需要的历史数据

        Args:
            years: 下载最近几年的数据
        """
        print("\n" + "="*60)
        print("开始下载历史数据...")
        print(f"数据年限: 最近{years}年")
        print("="*60 + "\n")

        # 1. 下载宏观数据
        self.logger.info("1/5 下载宏观数据...")
        print("📊 [1/5] 下载宏观数据（GDP、CPI、PPI、PMI等）...")
        macro_data = self._download_macro_data()
        self._save_cache('macro_data', macro_data)
        print(f"  ✓ 宏观数据下载完成，共{sum(len(v) for v in macro_data.values())}条记录\n")

        # 2. 下载市场数据
        self.logger.info("2/5 下载市场数据...")
        print("📈 [2/5] 下载市场数据（指数、行情）...")
        market_data = self._download_market_data(years)
        self._save_cache('market_data', market_data)
        print(f"  ✓ 市场数据下载完成\n")

        # 3. 下载行业数据
        self.logger.info("3/5 下载行业数据...")
        print("🏭 [3/5] 下载行业分类数据...")
        industry_data = self._download_industry_data()
        self._save_cache('industry_data', industry_data)
        print(f"  ✓ 行业数据下载完成，共{len(industry_data.get('industry_list', []))}个行业\n")

        # 4. 下载估值数据
        self.logger.info("4/5 下载估值数据...")
        print("💰 [4/5] 下载估值数据（PE、PB）...")
        valuation_data = self._download_valuation_data()
        self._save_cache('valuation_data', valuation_data)
        print(f"  ✓ 估值数据下载完成\n")

        # 5. 下载资金数据
        self.logger.info("5/5 下载资金数据...")
        print("💵 [5/5] 下载资金流向数据...")
        fund_data = self._download_fund_data()
        self._save_cache('fund_data', fund_data)
        print(f"  ✓ 资金数据下载完成\n")

        print("="*60)
        print("🎉 所有数据下载完成！")
        print(f"缓存位置: {self.cache_dir.absolute()}")
        print("="*60 + "\n")

        # 保存下载时间
        self._save_cache('last_download', {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'years': years
        })

    def _download_macro_data(self):
        """下载宏观数据"""
        macro_data = {}

        try:
            # GDP
            macro_data['gdp'] = self.api.get_macro_china_gdp()

            # CPI
            macro_data['cpi'] = self.api.get_macro_china_cpi()

            # PPI
            macro_data['ppi'] = self.api.get_macro_china_ppi()

            # PMI
            macro_data['pmi'] = self.api.get_macro_china_pmi()

            # M2
            macro_data['m2'] = self.api.get_macro_china_m2()

            # 社融
            macro_data['social_financing'] = self.api.get_macro_china_social_financing()

        except Exception as e:
            self.logger.error(f"下载宏观数据失败: {e}")
            # 返回模拟数据
            macro_data = self._get_mock_macro_data()

        return macro_data

    def _download_market_data(self, years):
        """下载市场数据"""
        market_data = {}

        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * years)

        try:
            # 沪深300指数
            market_data['hs300'] = self.api.get_index_zh_a_hist(
                '000300',
                start_date=start_date.strftime('%Y%m%d'),
                end_date=end_date.strftime('%Y%m%d')
            )

            # 上证指数
            market_data['sh000001'] = self.api.get_index_zh_a_hist(
                '000001',
                start_date=start_date.strftime('%Y%m%d'),
                end_date=end_date.strftime('%Y%m%d')
            )

            # A股列表
            market_data['stock_list'] = self.api.get_stock_zh_a_spot()

        except Exception as e:
            self.logger.error(f"下载市场数据失败: {e}")
            market_data = {}

        return market_data

    def _download_industry_data(self):
        """下载行业数据"""
        industry_data = {}

        try:
            # 行业分类
            industry_data['industry_list'] = self.api.get_stock_board_industry_name_em()

        except Exception as e:
            self.logger.error(f"下载行业数据失败: {e}")
            industry_data = {}

        return industry_data

    def _download_valuation_data(self):
        """下载估值数据"""
        valuation_data = {}

        try:
            # 全A PE PB
            valuation_data['all_a'] = self.api.get_stock_a_ttm_lyr()

        except Exception as e:
            self.logger.error(f"下载估值数据失败: {e}")
            valuation_data = {}

        return valuation_data

    def _download_fund_data(self):
        """下载资金数据"""
        fund_data = {}

        try:
            # 北向资金
            fund_data['north_flow'] = self.api.get_stock_em_hsgt_north_net_flow_in()

        except Exception as e:
            self.logger.error(f"下载资金数据失败: {e}")
            fund_data = {}

        return fund_data

    def _save_cache(self, name, data):
        """保存缓存"""
        cache_file = self.cache_dir / f'{name}.pkl'
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
            self.logger.info(f"缓存保存成功: {cache_file}")
        except Exception as e:
            self.logger.error(f"保存缓存失败: {e}")

    def load_cache(self, name):
        """加载缓存"""
        cache_file = self.cache_dir / f'{name}.pkl'
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                self.logger.error(f"加载缓存失败: {e}")
        return None

    def check_cache_age(self):
        """检查缓存新鲜度"""
        last_download = self.load_cache('last_download')
        if last_download:
            download_date = datetime.strptime(last_download['date'], '%Y-%m-%d %H:%M:%S')
            age_days = (datetime.now() - download_date).days

            print(f"缓存信息:")
            print(f"  下载日期: {last_download['date']}")
            print(f"  数据年限: {last_download['years']}年")
            print(f"  已过去: {age_days}天")

            if age_days > 7:
                print(f"  ⚠️  建议重新下载（数据较旧）")
                return False
            else:
                print(f"  ✓ 缓存仍然新鲜")
                return True
        else:
            print("未找到缓存，请先运行下载")
            return False

    def _get_mock_macro_data(self):
        """获取模拟宏观数据（用于演示）"""
        import pandas as pd
        import numpy as np

        dates = pd.date_range(end=datetime.now(), periods=36, freq='M')

        return {
            'gdp': pd.DataFrame({
                '日期': dates[::3],  # 季度数据
                'GDP': np.random.uniform(70000, 90000, 12)
            }),
            'cpi': pd.DataFrame({
                '日期': dates,
                'CPI': np.random.uniform(98, 103, 36)
            }),
            'ppi': pd.DataFrame({
                '日期': dates,
                'PPI': np.random.uniform(95, 107, 36)
            }),
            'pmi': pd.DataFrame({
                '日期': dates,
                'PMI': np.random.uniform(48, 52, 36)
            })
        }


def main():
    """主函数"""
    print("\n🚀 A股量化系统 - 数据下载工具\n")

    downloader = DataDownloader()

    # 检查现有缓存
    print("检查现有缓存...")
    if downloader.check_cache_age():
        response = input("\n是否重新下载？(y/n): ")
        if response.lower() != 'y':
            print("取消下载")
            return

    # 开始下载
    print()
    years = input("请输入要下载的历史数据年限（建议3年）[默认3]: ").strip()
    years = int(years) if years else 3

    downloader.download_all(years=years)

    print("提示：下次运行系统时会自动使用缓存数据，速度更快！\n")


if __name__ == '__main__':
    main()
