"""
马克斯钟摆模型 - 市场情绪周期分析
霍华德·马克斯的市场钟摆理论，衡量市场情绪和风险偏好
"""

import sys
import os
# 添加项目根目录到路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
import numpy as np
from typing import Dict

from utils.logger import logger
from utils.helpers import DataHelper


class MarksPendulum:
    """
    霍华德·马克斯的市场钟摆理论
    衡量市场情绪和风险偏好

    钟摆位置：0（极度悲观）到 100（极度乐观）
    """

    def __init__(self, data_fetcher=None):
        """
        Args:
            data_fetcher: 数据获取器实例
        """
        self.data_fetcher = data_fetcher
        self.logger = logger

        # 导入数据加载器
        from data.data_loader import get_data_loader
        self.data_loader = get_data_loader()

        # 各维度权重
        self.components = {
            'valuation': 0.3,      # 估值水平权重
            'sentiment': 0.3,      # 情绪指标权重
            'liquidity': 0.2,      # 流动性权重
            'breadth': 0.2         # 市场宽度权重
        }

    def calculate_pendulum_position(self) -> Dict:
        """
        计算钟摆位置：0（极度悲观）到 100（极度乐观）

        Returns:
            包含总分及各维度得分的字典
        """
        # 1. 估值维度 (0-100)
        valuation_score = self._calc_valuation_percentile()

        # 2. 情绪维度 (0-100)
        sentiment_score = self._calc_sentiment_score()

        # 3. 流动性维度 (0-100)
        liquidity_score = self._calc_liquidity_score()

        # 4. 市场宽度维度 (0-100)
        breadth_score = self._calc_market_breadth()

        # 综合得分
        total_score = (
            valuation_score * self.components['valuation'] +
            sentiment_score * self.components['sentiment'] +
            liquidity_score * self.components['liquidity'] +
            breadth_score * self.components['breadth']
        )

        result = {
            'total_score': total_score,
            'level': self._classify_level(total_score),
            'valuation': valuation_score,
            'sentiment': sentiment_score,
            'liquidity': liquidity_score,
            'breadth': breadth_score,
            'recommendation': self._get_recommendation(total_score)
        }

        self.logger.info(f"市场情绪温度: {total_score:.1f} ({result['level']})")

        return result

    def _calc_valuation_percentile(self) -> float:
        """
        计算估值维度得分

        指标：
        - 全A股PE/PB历史分位数（5年）
        - 风险溢价（1/PE - 10年国债收益率）
        - 股债性价比

        Returns:
            估值得分 (0-100)
        """
        # 简化版本：模拟数据
        # 实际应用中应该使用真实市场数据

        # 全A PE历史分位数
        pe_percentile = np.random.uniform(20, 80)

        # 全A PB历史分位数
        pb_percentile = np.random.uniform(20, 80)

        # 风险溢价得分（溢价越高，估值越低，得分越低）
        risk_premium = np.random.uniform(2, 6)  # 百分点
        risk_premium_score = max(0, 100 - risk_premium * 15)

        # 加权平均
        valuation_score = (
            pe_percentile * 0.4 +
            pb_percentile * 0.4 +
            risk_premium_score * 0.2
        )

        return valuation_score

    def _calc_sentiment_score(self) -> float:
        """
        计算情绪维度得分

        指标：
        - 融资买入额 / 总成交额
        - 两融余额增速
        - 新开户数（周度）
        - 交易软件下载量排名
        - 搜索指数："股票"、"炒股"

        Returns:
            情绪得分 (0-100)
        """
        # 融资买入占比（正常范围5-15%）
        margin_buy_ratio = np.random.uniform(5, 15)
        margin_score = min((margin_buy_ratio - 5) / 10 * 100, 100)

        # 两融余额增速（-20%到+40%）
        margin_balance_growth = np.random.uniform(-20, 40)
        balance_score = min((margin_balance_growth + 20) / 60 * 100, 100)

        # 新开户数增速
        new_account_growth = np.random.uniform(-30, 100)
        account_score = min((new_account_growth + 30) / 130 * 100, 100)

        # 搜索热度（相对值）
        search_heat = np.random.uniform(30, 100)

        # 加权平均
        sentiment_score = (
            margin_score * 0.3 +
            balance_score * 0.3 +
            account_score * 0.2 +
            search_heat * 0.2
        )

        return sentiment_score

    def _calc_liquidity_score(self) -> float:
        """
        计算流动性维度得分

        指标：
        - M2-M1剪刀差（反向，剪刀差大→流动性紧→得分低）
        - Shibor利率水平（反向）
        - 10年国债收益率（反向）
        - 信用利差（反向）
        - 北向资金流向强度

        Returns:
            流动性得分 (0-100)
        """
        try:
            # 尝试获取真实M2数据
            m2_data = self.data_loader.get_macro_data('m2', use_mock=False)

            if not m2_data.empty and len(m2_data) >= 2:
                # 获取最新M2增速
                m2_growth = float(m2_data.iloc[-1, 1])

                # M2增速越高，流动性越宽松，得分越高
                # 假设M2增速范围为5%-15%
                gap_score = min(max((m2_growth - 5) / 10 * 100, 0), 100)

                self.logger.info(f"M2增速（真实数据）: {m2_growth:.2f}%, 流动性得分: {gap_score:.1f}")
            else:
                # 降级到模拟数据
                m2_m1_gap = np.random.uniform(0, 10)
                gap_score = max(0, 100 - m2_m1_gap * 10)
                self.logger.warning("M2数据不足，使用模拟流动性数据")

        except Exception as e:
            self.logger.error(f"获取M2数据失败: {e}, 使用模拟数据")
            m2_m1_gap = np.random.uniform(0, 10)
            gap_score = max(0, 100 - m2_m1_gap * 10)

        # Shibor利率（1-5%）- 暂时使用模拟数据
        shibor = np.random.uniform(1, 5)
        shibor_score = max(0, 100 - (shibor - 1) * 25)

        # 10年国债收益率（2-4%）- 暂时使用模拟数据
        bond_yield = np.random.uniform(2, 4)
        yield_score = max(0, 100 - (bond_yield - 2) * 50)

        # 北向资金流入强度（-100亿到+200亿）- 暂时使用模拟数据
        northbound_flow = np.random.uniform(-100, 200)
        flow_score = min((northbound_flow + 100) / 300 * 100, 100)

        # 加权平均
        liquidity_score = (
            gap_score * 0.25 +
            shibor_score * 0.25 +
            yield_score * 0.25 +
            flow_score * 0.25
        )

        return liquidity_score

    def _calc_market_breadth(self) -> float:
        """
        计算市场宽度得分

        指标：
        - 上涨家数 / (上涨+下跌家数)
        - 创新高股票数 / 创新低股票数
        - 涨停跌停比
        - 破净股数量（反向）
        - 行业上涨数量占比

        Returns:
            市场宽度得分 (0-100)
        """
        # 上涨家数占比（0-100%）
        advance_ratio = np.random.uniform(0, 100)

        # 创新高/创新低比值（0-10）
        new_high_low_ratio = np.random.uniform(0, 10)
        high_low_score = min(new_high_low_ratio / 10 * 100, 100)

        # 涨停/跌停比值（0-20）
        limit_up_down_ratio = np.random.uniform(0, 20)
        limit_score = min(limit_up_down_ratio / 20 * 100, 100)

        # 破净股数量（反向，0-500只）
        pb_below_one = np.random.uniform(0, 500)
        pb_score = max(0, 100 - pb_below_one / 5)

        # 行业上涨占比
        industry_advance_ratio = np.random.uniform(0, 100)

        # 加权平均
        breadth_score = (
            advance_ratio * 0.3 +
            high_low_score * 0.2 +
            limit_score * 0.15 +
            pb_score * 0.15 +
            industry_advance_ratio * 0.2
        )

        return breadth_score

    def _classify_level(self, score: float) -> str:
        """
        分类钟摆位置

        Args:
            score: 综合得分

        Returns:
            市场情绪级别描述
        """
        if score < 20:
            return '极度悲观（历史机遇）'
        elif score < 40:
            return '悲观（可以布局）'
        elif score < 60:
            return '中性（等待方向）'
        elif score < 80:
            return '乐观（注意风险）'
        else:
            return '极度乐观（危险区域）'

    def _get_recommendation(self, score: float) -> Dict:
        """
        根据钟摆位置给出操作建议

        Args:
            score: 综合得分

        Returns:
            操作建议字典
        """
        recommendations = [
            {
                'range': (0, 20),
                'position': 0.90,
                'action': '激进买入',
                'style': '价值+成长均衡',
                'reason': '市场极度悲观，历史性机会',
                'urgency': 'HIGH'
            },
            {
                'range': (20, 40),
                'position': 0.80,
                'action': '逐步建仓',
                'style': '偏价值',
                'reason': '市场悲观，但尚未见底',
                'urgency': 'MEDIUM'
            },
            {
                'range': (40, 60),
                'position': 0.65,
                'action': '持有观望',
                'style': '均衡配置',
                'reason': '市场中性，等待方向明确',
                'urgency': 'LOW'
            },
            {
                'range': (60, 80),
                'position': 0.50,
                'action': '逐步减仓',
                'style': '偏防御',
                'reason': '市场乐观，注意回调风险',
                'urgency': 'MEDIUM'
            },
            {
                'range': (80, 100),
                'position': 0.30,
                'action': '大幅减仓',
                'style': '纯防御',
                'reason': '市场极度乐观，泡沫风险高',
                'urgency': 'HIGH'
            }
        ]

        for rec in recommendations:
            if rec['range'][0] <= score < rec['range'][1]:
                return rec

        # 默认中性建议
        return recommendations[2]

    def get_historical_extremes(self) -> Dict:
        """
        获取历史极值点

        Returns:
            历史极值统计
        """
        return {
            'historical_low': {
                'date': '2008-10-28',
                'score': 8,
                'description': '金融危机最恐慌时刻'
            },
            'historical_high': {
                'date': '2015-06-12',
                'score': 95,
                'description': '杠杆牛市顶峰'
            },
            'recent_low': {
                'date': '2022-04-27',
                'score': 15,
                'description': '疫情恐慌底'
            },
            'recent_high': {
                'date': '2021-02-18',
                'score': 85,
                'description': '抱团股泡沫顶峰'
            }
        }
