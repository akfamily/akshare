"""
朱格拉周期识别引擎 (产能周期, 7-11年)
中期经济周期，主要由固定资产投资和产能利用率驱动
"""

import sys
import os
# 添加项目根目录到路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
import numpy as np
from typing import Dict, Optional
from datetime import datetime

from utils.logger import logger
from utils.helpers import DataHelper


class JuglarCycle:
    """
    朱格拉周期识别 - 7-11年的产能投资周期

    判断方法：
    - 产能利用率 + 固定资产投资方向
    - PPI + ROE双轮驱动
    - 信贷周期（领先指标）
    """

    def __init__(self, data_fetcher=None):
        """
        Args:
            data_fetcher: 数据获取器实例
        """
        self.data_fetcher = data_fetcher
        self.logger = logger

        self.indicators = {
            'capacity_utilization': [],  # 产能利用率
            'fixed_investment': [],      # 固定资产投资
            'ppi': [],                   # PPI
            'roe': [],                   # 工业企业ROE
            'credit_growth': []          # 信贷增速
        }

    def fetch_data(self) -> Dict:
        """获取周期判断所需数据"""
        try:
            data = {
                # 制造业固定资产投资完成额同比
                'fixed_investment_growth': self._get_fixed_investment(),

                # PPI同比
                'ppi_yoy': self._get_ppi_yoy(),

                # 工业企业ROE（利润总额/净资产）
                'industrial_roe': self._get_industrial_roe(),

                # 社融/M2增速
                'credit_growth': self._get_credit_growth(),

                # 产能利用率
                'capacity_utilization': self._get_capacity_utilization()
            }

            self.logger.info("朱格拉周期数据获取成功")
            return data

        except Exception as e:
            self.logger.error(f"朱格拉周期数据获取失败: {str(e)}", exc_info=True)
            return {}

    def calculate_phase(self) -> Dict:
        """
        判断当前处于朱格拉周期的哪个阶段

        四阶段：
        1. 复苏期：产能利用率回升，投资开始增加
        2. 繁荣期：产能扩张，企业盈利改善
        3. 衰退期：产能过剩显现，盈利下滑
        4. 萧条期：产能出清，等待新一轮周期

        Returns:
            包含周期信息的字典
        """
        data = self.fetch_data()

        # 方法1：产能利用率 + 固定资产投资方向
        capacity_trend = self._calc_trend(data.get('capacity_utilization', 75))
        investment_trend = self._calc_trend(data.get('fixed_investment_growth', 0))

        # 方法2：PPI + ROE双轮驱动
        ppi_level = self._get_percentile(data.get('ppi_yoy', 0))
        roe_trend = self._calc_trend(data.get('industrial_roe', 10))

        # 方法3：信贷周期（领先指标，领先9-12个月）
        credit_trend = self._calc_trend(data.get('credit_growth', 10))

        # 综合判断
        phase = self._综合判断phase(
            capacity_trend,
            investment_trend,
            ppi_level,
            roe_trend,
            credit_trend
        )

        result = {
            'phase': phase,
            'phase_name': ['复苏', '繁荣', '衰退', '萧条'][phase - 1],
            'confidence': self._calc_confidence(capacity_trend, investment_trend),
            'time_in_phase': self._estimate_phase_duration(phase),
            'next_inflection': self._predict_inflection_point(phase),
            'indicators': {
                'capacity_trend': capacity_trend,
                'investment_trend': investment_trend,
                'ppi_level': ppi_level,
                'roe_trend': roe_trend,
                'credit_trend': credit_trend
            }
        }

        self.logger.info(f"朱格拉周期识别完成: {result['phase_name']} (置信度: {result['confidence']:.1%})")

        return result

    def get_industry_preference(self, phase: int) -> Dict:
        """
        根据朱格拉周期阶段返回行业配置建议

        Args:
            phase: 周期阶段 (1-4)

        Returns:
            行业配置建议
        """
        industry_map = {
            1: {  # 复苏期
                'overweight': ['机械设备', '化工', '建筑材料', '有色金属', '钢铁'],
                'neutral': ['电力设备', '汽车', '电子'],
                'underweight': ['食品饮料', '医药生物', '银行'],
                'reason': '产能利用率回升，周期品需求改善'
            },
            2: {  # 繁荣期
                'overweight': ['电子', '计算机', '传媒', '新能源', '军工'],
                'neutral': ['机械设备', '化工', '汽车'],
                'underweight': ['公用事业', '银行', '房地产'],
                'reason': '经济扩张，成长股表现最佳'
            },
            3: {  # 衰退期
                'overweight': ['医药生物', '食品饮料', '农林牧渔', '公用事业'],
                'neutral': ['家用电器', '轻工制造'],
                'underweight': ['有色金属', '钢铁', '煤炭', '化工'],
                'reason': '经济下行，防御性板块相对占优'
            },
            4: {  # 萧条期
                'overweight': ['公用事业', '银行', '黄金（商品）'],
                'neutral': ['医药生物', '必需消费'],
                'underweight': ['周期性行业全部'],
                'reason': '产能出清阶段，现金为王'
            }
        }

        return industry_map.get(phase, industry_map[2])

    def get_asset_allocation_adjustment(self, phase: int) -> Dict:
        """
        朱格拉周期对大类资产配置的影响系数

        Args:
            phase: 周期阶段

        Returns:
            各类资产的配置调整系数
        """
        allocation_adj = {
            1: {  # 复苏期
                'stock': 1.1,
                'bond': 0.9,
                'commodity': 1.2,
                'cash': 0.8,
                'recommended_position': 0.75
            },
            2: {  # 繁荣期
                'stock': 1.2,
                'bond': 0.8,
                'commodity': 1.0,
                'cash': 0.7,
                'recommended_position': 0.85
            },
            3: {  # 衰退期
                'stock': 0.8,
                'bond': 1.2,
                'commodity': 0.8,
                'cash': 1.1,
                'recommended_position': 0.50
            },
            4: {  # 萧条期
                'stock': 0.6,
                'bond': 1.3,
                'commodity': 0.7,
                'cash': 1.3,
                'recommended_position': 0.30
            }
        }

        return allocation_adj.get(phase, allocation_adj[2])

    # ==================== 私有方法 ====================

    def _get_fixed_investment(self) -> float:
        """获取固定资产投资增速（模拟）"""
        return np.random.uniform(-2, 10)

    def _get_ppi_yoy(self) -> float:
        """获取PPI同比（模拟）"""
        return np.random.uniform(-3, 8)

    def _get_industrial_roe(self) -> float:
        """获取工业企业ROE（模拟）"""
        return np.random.uniform(5, 15)

    def _get_credit_growth(self) -> float:
        """获取信贷增速（模拟）"""
        return np.random.uniform(8, 15)

    def _get_capacity_utilization(self) -> float:
        """获取产能利用率（模拟）"""
        return np.random.uniform(70, 85)

    def _calc_trend(self, current_value: float) -> float:
        """
        计算趋势方向

        Args:
            current_value: 当前值

        Returns:
            趋势值 (-1到1)
        """
        # 简化版本：基于阈值判断
        # 实际应用中应该计算移动平均线斜率
        if current_value > 80 or current_value > 10:  # 高位
            return 0.5
        elif current_value < 70 or current_value < 5:  # 低位
            return -0.5
        else:
            return 0.0

    def _get_percentile(self, value: float) -> float:
        """获取历史分位数（模拟）"""
        return np.random.uniform(0, 100)

    def _综合判断phase(self, capacity_trend: float, investment_trend: float,
                      ppi_level: float, roe_trend: float, credit_trend: float) -> int:
        """
        综合判断当前周期阶段

        Returns:
            1-复苏, 2-繁荣, 3-衰退, 4-萧条
        """
        # 简化的判断逻辑
        score = 0

        # 产能利用率上升+投资增加 → 繁荣
        if capacity_trend > 0 and investment_trend > 0:
            score += 2
        # 产能利用率下降+投资减少 → 衰退/萧条
        elif capacity_trend < 0 and investment_trend < 0:
            score -= 2

        # PPI高位 → 繁荣
        if ppi_level > 60:
            score += 1
        elif ppi_level < 40:
            score -= 1

        # ROE改善 → 复苏/繁荣
        if roe_trend > 0:
            score += 1
        else:
            score -= 1

        # 信贷领先指标
        if credit_trend > 0:
            score += 1
        else:
            score -= 1

        # 根据得分判断阶段
        if score >= 3:
            return 2  # 繁荣期
        elif score >= 1:
            return 1  # 复苏期
        elif score >= -1:
            return 3  # 衰退期
        else:
            return 4  # 萧条期

    def _calc_confidence(self, capacity_trend: float, investment_trend: float) -> float:
        """计算判断置信度"""
        # 信号一致性越高，置信度越高
        if capacity_trend * investment_trend > 0:  # 同向
            return 0.8
        else:
            return 0.5

    def _estimate_phase_duration(self, phase: int) -> int:
        """估计当前阶段已持续时间（月）"""
        # 模拟数据
        return np.random.randint(6, 36)

    def _predict_inflection_point(self, phase: int) -> str:
        """预测下一个拐点时间"""
        # 简化版本
        months = np.random.randint(3, 18)
        return f"预计{months}个月后进入下一阶段"
