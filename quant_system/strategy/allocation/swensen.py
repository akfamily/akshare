"""
斯文森资产配置策略（耶鲁捐赠基金模型）
大卫·斯文森管理耶鲁捐赠基金的长期资产配置策略
"""

import numpy as np
from typing import Dict, List


class SwensenStrategy:
    """
    斯文森（David Swensen）资产配置策略

    核心理念：
    1. 广泛分散：跨资产类别、跨地域分散
    2. 重视权益：长期看权益类资产收益更高
    3. 另类投资：配置PE、对冲基金、房地产等
    4. 再平衡纪律：严格执行再平衡，低买高卖
    5. 低成本：选择低费率产品

    耶鲁捐赠基金实际配置（2022年）：
    - 国内权益 3.75%
    - 海外权益 14.1%
    - 私募股权 39.3%
    - 对冲基金 23.7%
    - 房地产 10.4%
    - 债券及现金 5.2%
    - 自然资源 3.6%

    简化版（适合个人投资者）：
    - 国内权益 30%
    - 海外权益 15%
    - 新兴市场 5%
    - 房地产REITs 20%
    - 大宗商品 10%
    - 国债 15%
    - 通胀保护债券 5%
    """

    def __init__(self):
        # 标准配置（适合中国个人投资者的简化版）
        self.standard_allocation = {
            '国内权益': 0.30,       # A股宽基指数
            '海外权益': 0.15,       # 港股、美股指数
            '新兴市场': 0.05,       # 新兴市场ETF
            '房地产REITs': 0.20,   # REITs基金
            '大宗商品': 0.10,       # 商品期货、黄金
            '国债': 0.15,           # 长期国债
            '通胀保护债券': 0.05    # 国债ETF或货币基金
        }

        # 再平衡阈值（偏离超过此值时触发再平衡）
        self.rebalance_threshold = 0.05  # 5%

        # 各资产类别的预期收益和风险（年化）
        self.asset_stats = {
            '国内权益': {'return': 0.08, 'risk': 0.25},
            '海外权益': {'return': 0.09, 'risk': 0.22},
            '新兴市场': {'return': 0.10, 'risk': 0.30},
            '房地产REITs': {'return': 0.07, 'risk': 0.18},
            '大宗商品': {'return': 0.05, 'risk': 0.20},
            '国债': {'return': 0.03, 'risk': 0.05},
            '通胀保护债券': {'return': 0.025, 'risk': 0.03}
        }

    def get_allocation(self, risk_level: str = 'moderate') -> Dict:
        """
        获取资产配置建议

        Args:
            risk_level: 风险偏好 ('conservative', 'moderate', 'aggressive')

        Returns:
            资产配置字典
        """
        if risk_level == 'conservative':
            # 保守型：降低权益类，提高债券类
            allocation = {
                '国内权益': 0.20,
                '海外权益': 0.10,
                '新兴市场': 0.03,
                '房地产REITs': 0.15,
                '大宗商品': 0.07,
                '国债': 0.30,
                '通胀保护债券': 0.15
            }
        elif risk_level == 'aggressive':
            # 激进型：提高权益类，降低债券类
            allocation = {
                '国内权益': 0.35,
                '海外权益': 0.20,
                '新兴市场': 0.10,
                '房地产REITs': 0.20,
                '大宗商品': 0.10,
                '国债': 0.05,
                '通胀保护债券': 0.00
            }
        else:  # moderate
            allocation = self.standard_allocation.copy()

        return {
            'allocation': allocation,
            'risk_level': risk_level,
            'expected_return': self._calc_expected_return(allocation),
            'expected_risk': self._calc_expected_risk(allocation),
            'sharpe_ratio': self._calc_sharpe_ratio(allocation)
        }

    def check_rebalance_needed(self, current_allocation: Dict,
                                target_allocation: Dict = None) -> Dict:
        """
        检查是否需要再平衡

        Args:
            current_allocation: 当前配置
            target_allocation: 目标配置（如果None，使用标准配置）

        Returns:
            再平衡建议
        """
        if target_allocation is None:
            target_allocation = self.standard_allocation

        suggestions = []
        needs_rebalance = False

        for asset in target_allocation.keys():
            current = current_allocation.get(asset, 0)
            target = target_allocation[asset]
            diff = current - target

            if abs(diff) > self.rebalance_threshold:
                needs_rebalance = True
                action = '减持' if diff > 0 else '增持'
                amount = abs(diff)

                # 优先级判断
                if abs(diff) > 0.10:
                    priority = 'HIGH'
                elif abs(diff) > 0.07:
                    priority = 'MEDIUM'
                else:
                    priority = 'LOW'

                suggestions.append({
                    'asset': asset,
                    'current': current,
                    'target': target,
                    'diff': diff,
                    'action': action,
                    'amount': amount,
                    'priority': priority
                })

        return {
            'needs_rebalance': needs_rebalance,
            'suggestions': sorted(suggestions, key=lambda x: abs(x['diff']), reverse=True),
            'total_deviation': sum(abs(s['diff']) for s in suggestions)
        }

    def get_implementation_guide(self) -> Dict:
        """
        获取实施指南（适合中国投资者）

        Returns:
            实施指南字典
        """
        return {
            '国内权益': {
                'products': [
                    '沪深300ETF (510300)',
                    '中证500ETF (510500)',
                    '创业板ETF (159915)'
                ],
                'notes': '建议分散到大盘、中盘、创业板'
            },
            '海外权益': {
                'products': [
                    '恒生ETF (159920)',
                    '标普500 QDII (513500)',
                    '纳斯达克100 QDII (513100)'
                ],
                'notes': '港股+美股分散'
            },
            '新兴市场': {
                'products': [
                    '印度基金',
                    '越南基金',
                    '新兴市场QDII'
                ],
                'notes': '关注印度、越南等高增长市场'
            },
            '房地产REITs': {
                'products': [
                    '博时招商产业园REIT',
                    '华夏中国交建REIT',
                    '富国首创水务REIT'
                ],
                'notes': '中国公募REITs，重点配置产业园、物流、基建'
            },
            '大宗商品': {
                'products': [
                    '黄金ETF (518880)',
                    '白银LOF (161226)',
                    '商品期货基金'
                ],
                'notes': '黄金为主，可少量配置原油、农产品'
            },
            '国债': {
                'products': [
                    '10年期国债ETF (511260)',
                    '30年期国债ETF (511090)'
                ],
                'notes': '长久期国债，获取利率下行收益'
            },
            '通胀保护债券': {
                'products': [
                    '短债基金',
                    '货币基金',
                    '可转债基金'
                ],
                'notes': '灵活配置，可用可转债替代'
            }
        }

    def get_rebalance_strategy(self) -> Dict:
        """
        获取再平衡策略说明

        Returns:
            再平衡策略字典
        """
        return {
            '时间再平衡': {
                'description': '按固定时间间隔再平衡',
                'frequency': '每季度或每半年',
                'advantage': '纪律性强，操作简单',
                'disadvantage': '可能错过极端市场机会'
            },
            '阈值再平衡': {
                'description': '偏离超过阈值时再平衡',
                'threshold': '±5%',
                'advantage': '更灵活，抓住极端机会',
                'disadvantage': '需要频繁监控'
            },
            '混合策略': {
                'description': '时间+阈值组合',
                'rule': '每季度检查，偏离>5%时再平衡',
                'advantage': '兼顾纪律和灵活性',
                'disadvantage': '无'
            },
            '税收优化': {
                'description': '考虑税收成本的再平衡',
                'tips': [
                    '利用定投增持不足部分',
                    '优先卖出亏损资产',
                    '利用免税账户再平衡'
                ]
            }
        }

    def _calc_expected_return(self, allocation: Dict) -> float:
        """计算预期收益"""
        expected_return = 0
        for asset, weight in allocation.items():
            expected_return += weight * self.asset_stats[asset]['return']
        return expected_return

    def _calc_expected_risk(self, allocation: Dict) -> float:
        """计算预期风险（简化版，假设资产不完全相关）"""
        # 简化计算：加权平均风险 * 分散系数
        weighted_risk = sum(
            weight * self.asset_stats[asset]['risk']
            for asset, weight in allocation.items()
        )

        # 分散效应：7种资产，相关系数假设0.3
        # 分散系数约为 sqrt(1/7 + (1-1/7)*0.3) ≈ 0.55
        diversification_factor = 0.55

        return weighted_risk * diversification_factor

    def _calc_sharpe_ratio(self, allocation: Dict, risk_free_rate: float = 0.025) -> float:
        """计算夏普比率"""
        expected_return = self._calc_expected_return(allocation)
        expected_risk = self._calc_expected_risk(allocation)

        if expected_risk > 0:
            return (expected_return - risk_free_rate) / expected_risk
        else:
            return 0.0

    def get_philosophy(self) -> Dict:
        """
        获取斯文森投资哲学

        Returns:
            投资哲学字典
        """
        return {
            '核心原则': [
                '1. 股票为主：长期看权益类资产收益最高',
                '2. 广泛分散：不把鸡蛋放在一个篮子里',
                '3. 重视另类：配置非传统资产降低相关性',
                '4. 严格再平衡：纪律性低买高卖',
                '5. 长期持有：不因短期波动改变配置',
                '6. 低成本：费率差异长期影响巨大'
            ],
            '与传统60/40策略对比': {
                '传统60/40': '60%股票 + 40%债券',
                '斯文森策略': '50%权益 + 30%另类 + 20%债券',
                '优势': '更高分散度，更低相关性，长期收益更优'
            },
            '历史业绩': {
                '耶鲁捐赠基金20年年化收益': '11.8%',
                '同期美国大学捐赠基金平均': '7.7%',
                '同期标普500指数': '9.5%'
            },
            '适合人群': [
                '长期投资者（10年以上）',
                '能承受波动的投资者',
                '理解并认同分散化价值',
                '有纪律执行再平衡'
            ]
        }
