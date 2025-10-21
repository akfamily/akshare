"""
全天候策略（桥水基金）- 简化版
基于经济四象限的资产配置策略
"""

import numpy as np
from typing import Dict


class AllWeatherStrategy:
    """
    桥水全天候策略 - 中国市场版

    经济四象限：
    1. 增长↑通胀↓ - 复苏
    2. 增长↑通胀↑ - 过热
    3. 增长↓通胀↓ - 衰退
    4. 增长↓通胀↑ - 滞胀
    """

    def __init__(self):
        self.risk_free_rate = 0.03  # 无风险利率

    def identify_regime(self, growth_rate: float = None, inflation_rate: float = None) -> Dict:
        """
        识别当前经济象限

        Args:
            growth_rate: GDP增速或PMI（如果None，使用模拟值）
            inflation_rate: CPI同比（如果None，使用模拟值）

        Returns:
            象限信息
        """
        # 使用模拟值（演示用）
        if growth_rate is None:
            growth_rate = np.random.uniform(-2, 8)  # GDP增速
        if inflation_rate is None:
            inflation_rate = np.random.uniform(-1, 5)  # CPI同比

        # 判断象限
        growth_threshold = 5.0  # GDP增速5%为分界线
        inflation_threshold = 2.5  # CPI 2.5%为分界线

        if growth_rate > growth_threshold:
            if inflation_rate > inflation_threshold:
                regime = 2  # 过热
                regime_name = "经济过热（增长↑通胀↑）"
            else:
                regime = 1  # 复苏
                regime_name = "经济复苏（增长↑通胀↓）"
        else:
            if inflation_rate > inflation_threshold:
                regime = 4  # 滞胀
                regime_name = "经济滞胀（增长↓通胀↑）"
            else:
                regime = 3  # 衰退
                regime_name = "经济衰退（增长↓通胀↓）"

        return {
            'regime': regime,
            'regime_name': regime_name,
            'growth_rate': growth_rate,
            'inflation_rate': inflation_rate
        }

    def get_allocation(self, regime: int = None) -> Dict:
        """
        获取对应象限的资产配置

        Args:
            regime: 经济象限(1-4)，如果None则自动识别

        Returns:
            资产配置建议
        """
        if regime is None:
            regime_info = self.identify_regime()
            regime = regime_info['regime']

        # 中国市场可投资资产类别
        allocations = {
            1: {  # 复苏：增长↑通胀↓
                '大盘股票': 0.25,
                '中小盘股票': 0.20,
                '成长股': 0.15,
                '国债': 0.15,
                '可转债': 0.10,
                '黄金': 0.05,
                '商品': 0.05,
                '现金': 0.05,
                'description': '股票为主，适度配置债券'
            },
            2: {  # 过热：增长↑通胀↑
                '大盘股票': 0.20,
                '中小盘股票': 0.15,
                '成长股': 0.20,
                '国债': 0.10,
                '可转债': 0.10,
                '黄金': 0.10,
                '商品': 0.10,
                '现金': 0.05,
                'description': '股票+商品，降低债券'
            },
            3: {  # 衰退：增长↓通胀↓
                '大盘股票': 0.10,
                '中小盘股票': 0.05,
                '成长股': 0.05,
                '国债': 0.40,
                '可转债': 0.15,
                '黄金': 0.15,
                '商品': 0.05,
                '现金': 0.05,
                'description': '债券为主，黄金避险'
            },
            4: {  # 滞胀：增长↓通胀↑
                '大盘股票': 0.10,
                '中小盘股票': 0.05,
                '成长股': 0.05,
                '国债': 0.25,
                '可转债': 0.10,
                '黄金': 0.25,
                '商品': 0.15,
                '现金': 0.05,
                'description': '黄金+商品抗通胀'
            }
        }

        allocation = allocations.get(regime, allocations[1])

        return {
            'regime': regime,
            'allocation': allocation,
            'expected_return': self._calc_expected_return(allocation),
            'expected_risk': self._calc_expected_risk(allocation)
        }

    def _calc_expected_return(self, allocation: Dict) -> float:
        """计算预期收益（简化版）"""
        # 各资产类别的历史年化收益（模拟）
        returns = {
            '大盘股票': 0.08,
            '中小盘股票': 0.10,
            '成长股': 0.12,
            '国债': 0.03,
            '可转债': 0.06,
            '黄金': 0.04,
            '商品': 0.05,
            '现金': 0.02
        }

        expected_return = 0
        for asset, weight in allocation.items():
            if asset != 'description':
                expected_return += weight * returns.get(asset, 0.05)

        return expected_return

    def _calc_expected_risk(self, allocation: Dict) -> float:
        """计算预期风险（简化版）"""
        # 各资产类别的历史波动率（模拟）
        volatilities = {
            '大盘股票': 0.25,
            '中小盘股票': 0.30,
            '成长股': 0.35,
            '国债': 0.05,
            '可转债': 0.15,
            '黄金': 0.18,
            '商品': 0.22,
            '现金': 0.01
        }

        # 简化计算：加权平均波动率
        expected_risk = 0
        for asset, weight in allocation.items():
            if asset != 'description':
                expected_risk += weight * volatilities.get(asset, 0.15)

        return expected_risk

    def get_rebalance_suggestion(self, current_allocation: Dict, target_allocation: Dict) -> Dict:
        """
        生成再平衡建议

        Args:
            current_allocation: 当前配置
            target_allocation: 目标配置

        Returns:
            再平衡建议
        """
        suggestions = []

        for asset in target_allocation.keys():
            if asset == 'description':
                continue

            current = current_allocation.get(asset, 0)
            target = target_allocation.get(asset, 0)
            diff = target - current

            if abs(diff) > 0.05:  # 偏离超过5%
                action = "增持" if diff > 0 else "减持"
                suggestions.append({
                    'asset': asset,
                    'action': action,
                    'amount': abs(diff),
                    'priority': 'HIGH' if abs(diff) > 0.10 else 'MEDIUM'
                })

        return {
            'needs_rebalance': len(suggestions) > 0,
            'suggestions': suggestions
        }
