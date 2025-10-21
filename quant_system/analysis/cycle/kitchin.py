"""
基钦周期识别引擎 (库存周期, 3-4年)
这是最高频、最实用的周期，直接指导短期配置
"""

import sys
import os
# 添加项目根目录到路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from utils.logger import logger
from utils.helpers import DataHelper


class KitchinCycle:
    """
    基钦周期识别 - 3-4年的库存周期

    四象限判断法：
              需求上升 | 需求下降
    库存上升  被动补库  | 主动去库
    库存下降  主动补库  | 被动去库
    """

    def __init__(self, data_fetcher=None):
        """
        Args:
            data_fetcher: 数据获取器实例
        """
        self.data_fetcher = data_fetcher
        self.data_window = 36  # 3年数据窗口（月）
        self.logger = logger

        # 导入数据加载器
        from data.data_loader import get_data_loader
        self.data_loader = get_data_loader()

        # 历史数据缓存
        self.historical_data = {
            'inventory': [],           # 产成品库存
            'demand_proxy': [],        # 需求代理指标
            'dates': []
        }

    def fetch_data(self) -> Dict:
        """
        获取库存周期判断所需数据

        Returns:
            包含各项指标的字典
        """
        try:
            # 简化版本：使用模拟数据
            # 在实际应用中，应该使用真实的经济数据

            data = {
                # 工业企业产成品库存同比（核心指标）
                'inventory_growth': self._get_inventory_growth(),

                # 需求指标：工业增加值同比
                'demand_growth': self._get_demand_growth(),

                # PMI产成品库存指数
                'pmi_inventory': self._get_pmi_inventory(),

                # PMI新订单
                'pmi_new_orders': self._get_pmi_new_orders(),

                # PPI环比
                'ppi_mom': self._get_ppi_mom()
            }

            self.logger.info("基钦周期数据获取成功")
            return data

        except Exception as e:
            self.logger.error(f"基钦周期数据获取失败: {str(e)}", exc_info=True)
            return {}

    def identify_phase(self, inventory_growth: float = None,
                       demand_growth: float = None) -> Dict:
        """
        判断当前处于库存周期的哪个阶段

        四象限识别：
        1. 被动补库：需求↑ 库存↑ (经济复苏初期)
        2. 主动补库：需求↑ 库存↓ (经济繁荣期)
        3. 被动去库：需求↓ 库存↓ (经济衰退期)
        4. 主动去库：需求↓ 库存↑ (经济萧条期)

        Args:
            inventory_growth: 库存增速（如果不提供则自动获取）
            demand_growth: 需求增速（如果不提供则自动获取）

        Returns:
            包含周期信息的字典
        """
        # 如果未提供数据，则获取最新数据
        if inventory_growth is None or demand_growth is None:
            data = self.fetch_data()
            inventory_growth = data.get('inventory_growth', 0)
            demand_growth = data.get('demand_growth', 0)

        # 需求方向：正为上升，负为下降
        demand_direction = 1 if demand_growth > 0 else -1

        # 库存方向：正为上升，负为下降
        inventory_direction = 1 if inventory_growth > 0 else -1

        # 四象限映射
        phase_mapping = {
            (1, 1): ('被动补库', 1),    # 需求↑ 库存↑
            (1, -1): ('主动补库', 2),   # 需求↑ 库存↓
            (-1, -1): ('被动去库', 3),  # 需求↓ 库存↓
            (-1, 1): ('主动去库', 4)    # 需求↓ 库存↑
        }

        phase_name, phase_code = phase_mapping[(demand_direction, inventory_direction)]

        # 计算周期进度（0-1，表示该阶段进行到什么程度）
        phase_progress = self._calc_phase_progress(phase_code)

        result = {
            'phase': phase_code,
            'phase_name': phase_name,
            'progress': phase_progress,
            'demand_growth': demand_growth,
            'inventory_growth': inventory_growth,
            'estimated_duration': self._estimate_remaining_months(phase_code, phase_progress),
            'confidence': self._calc_confidence(demand_growth, inventory_growth)
        }

        self.logger.info(f"基钦周期识别完成: {phase_name} (进度: {phase_progress:.1%})")

        return result

    def get_sector_rotation(self, phase: int) -> Dict:
        """
        根据库存周期阶段返回行业配置建议

        Args:
            phase: 周期阶段 (1-4)

        Returns:
            行业配置建议字典
        """
        rotation_map = {
            1: {  # 被动补库
                'phase_desc': '经济复苏初期，需求改善快于供给调整',
                'best': ['煤炭', '钢铁', '有色金属', '石油石化', '化工'],
                'good': ['建筑材料', '建筑装饰', '交运'],
                'avoid': ['消费', '医药', '科技'],
                'logic': '上游资源品受益于需求回暖和库存去化',
                'recommended_position': 0.75  # 建议仓位
            },
            2: {  # 主动补库
                'phase_desc': '经济繁荣期，企业乐观加库存',
                'best': ['机械设备', '电气设备', '汽车', '家电', '电子'],
                'good': ['计算机', '传媒', '轻工制造'],
                'avoid': ['上游周期', '防御性板块'],
                'logic': '中下游制造业和可选消费最受益',
                'recommended_position': 0.85
            },
            3: {  # 被动去库
                'phase_desc': '经济衰退初期，需求走弱但库存仍高',
                'best': ['医药生物', '食品饮料', '农林牧渔', '公用事业'],
                'good': ['银行', '非银金融'],
                'avoid': ['周期股全部', '可选消费'],
                'logic': '必需消费和防御性板块相对占优',
                'recommended_position': 0.50
            },
            4: {  # 主动去库
                'phase_desc': '经济衰退深化，企业主动去库存',
                'best': ['银行', '公用事业', '黄金（商品）'],
                'good': ['医药', '必需消费'],
                'avoid': ['制造业', '周期股'],
                'logic': '现金为王，配置债券或等待底部',
                'recommended_position': 0.30
            }
        }

        return rotation_map.get(phase, rotation_map[1])

    def get_timing_signal(self, phase: int, progress: float) -> Dict:
        """
        基于库存周期的择时信号

        Args:
            phase: 周期阶段
            progress: 阶段进度

        Returns:
            择时信号字典
        """
        # 重点关注周期切换时点
        if phase == 4 and progress > 0.7:
            # 主动去库末期 → 即将转向被动补库
            return {
                'signal': 'STRONG_BUY',
                'reason': '库存周期即将见底，布局周期股',
                'target_position': 0.85,
                'focus_sectors': ['上游资源', '建材', '化工'],
                'urgency': 'HIGH'
            }
        elif phase == 2 and progress > 0.7:
            # 主动补库末期 → 即将转向被动去库
            return {
                'signal': 'REDUCE',
                'reason': '库存周期接近顶部，降低周期股仓位',
                'target_position': 0.60,
                'focus_sectors': ['医药', '消费', '公用事业'],
                'urgency': 'HIGH'
            }
        elif phase == 1:
            # 被动补库阶段
            return {
                'signal': 'BUY',
                'reason': '需求回升，配置上游周期',
                'target_position': 0.75,
                'focus_sectors': ['煤炭', '有色', '钢铁'],
                'urgency': 'MEDIUM'
            }
        elif phase == 3:
            # 被动去库阶段
            return {
                'signal': 'DEFENSIVE',
                'reason': '需求下行，转向防御',
                'target_position': 0.50,
                'focus_sectors': ['食品饮料', '医药', '公用事业'],
                'urgency': 'MEDIUM'
            }
        else:
            return {
                'signal': 'HOLD',
                'reason': '周期中段，维持现有配置',
                'target_position': 0.70,
                'focus_sectors': [],
                'urgency': 'LOW'
            }

    # ==================== 私有方法 ====================

    def _get_inventory_growth(self) -> float:
        """获取库存增速（真实数据）"""
        try:
            # 从PMI数据中提取产成品库存指数
            pmi_data = self.data_loader.get_macro_data('pmi', use_mock=False)

            if not pmi_data.empty and len(pmi_data) >= 2:
                # 计算库存增速：当月库存指数 - 上月库存指数
                # PMI产成品库存通常在第3或第4列
                current = float(pmi_data.iloc[-1, 3]) if len(pmi_data.columns) > 3 else 50.0
                previous = float(pmi_data.iloc[-2, 3]) if len(pmi_data.columns) > 3 else 50.0

                # 转换为增速：(当前-50) - (上期-50)
                # PMI指数>50表示扩张，<50表示收缩
                inventory_growth = (current - 50) - (previous - 50)

                self.logger.info(f"库存增速（真实数据）: {inventory_growth:.2f}% (当前PMI库存: {current:.1f}, 上期: {previous:.1f})")
                return inventory_growth
            else:
                self.logger.warning("PMI数据不足，使用模拟数据")
                return np.random.uniform(-5, 5)

        except Exception as e:
            self.logger.error(f"获取库存增速失败: {e}, 使用模拟数据")
            return np.random.uniform(-5, 5)

    def _get_demand_growth(self) -> float:
        """获取需求增速（真实数据）"""
        try:
            # 使用PMI新订单指数作为需求代理指标
            pmi_data = self.data_loader.get_macro_data('pmi', use_mock=False)

            if not pmi_data.empty and len(pmi_data) >= 2:
                # PMI新订单通常在第2或第3列
                current = float(pmi_data.iloc[-1, 2]) if len(pmi_data.columns) > 2 else 50.0
                previous = float(pmi_data.iloc[-2, 2]) if len(pmi_data.columns) > 2 else 50.0

                # 计算需求增速
                demand_growth = (current - 50) * 2  # 放大系数，将PMI转换为类似增速的概念

                self.logger.info(f"需求增速（真实数据）: {demand_growth:.2f}% (当前PMI新订单: {current:.1f}, 上期: {previous:.1f})")
                return demand_growth
            else:
                self.logger.warning("PMI数据不足，使用模拟数据")
                return np.random.uniform(-3, 8)

        except Exception as e:
            self.logger.error(f"获取需求增速失败: {e}, 使用模拟数据")
            return np.random.uniform(-3, 8)

    def _get_pmi_inventory(self) -> float:
        """获取PMI产成品库存指数（真实数据）"""
        try:
            pmi_data = self.data_loader.get_macro_data('pmi', use_mock=False)

            if not pmi_data.empty:
                # 获取最新的PMI产成品库存指数
                pmi_inventory = float(pmi_data.iloc[-1, 3]) if len(pmi_data.columns) > 3 else 50.0

                self.logger.info(f"PMI产成品库存指数（真实数据）: {pmi_inventory:.2f}")
                return pmi_inventory
            else:
                return 50.0

        except Exception as e:
            self.logger.error(f"获取PMI库存指数失败: {e}")
            return 50.0

    def _get_pmi_new_orders(self) -> float:
        """获取PMI新订单指数（真实数据）"""
        try:
            pmi_data = self.data_loader.get_macro_data('pmi', use_mock=False)

            if not pmi_data.empty:
                # 获取最新的PMI新订单指数
                pmi_new_orders = float(pmi_data.iloc[-1, 2]) if len(pmi_data.columns) > 2 else 50.0

                self.logger.info(f"PMI新订单指数（真实数据）: {pmi_new_orders:.2f}")
                return pmi_new_orders
            else:
                return 50.0

        except Exception as e:
            self.logger.error(f"获取PMI新订单指数失败: {e}")
            return 50.0

    def _get_ppi_mom(self) -> float:
        """获取PPI环比（真实数据）"""
        try:
            ppi_data = self.data_loader.get_macro_data('ppi', use_mock=False)

            if not ppi_data.empty and len(ppi_data) >= 2:
                # 计算PPI环比增速
                current = float(ppi_data.iloc[-1, 1])
                previous = float(ppi_data.iloc[-2, 1])

                ppi_mom = ((current - previous) / previous) * 100

                self.logger.info(f"PPI环比（真实数据）: {ppi_mom:.2f}%")
                return ppi_mom
            else:
                return 0.0

        except Exception as e:
            self.logger.error(f"获取PPI环比失败: {e}")
            return 0.0

    def _calc_phase_progress(self, phase: int) -> float:
        """
        计算当前阶段的进度

        通过分析历史数据，估计当前阶段已经进行到什么程度
        """
        # 简化版本：返回随机进度
        # 实际应用中应该基于历史数据分析
        return np.random.uniform(0.2, 0.8)

    def _estimate_remaining_months(self, phase: int, progress: float) -> int:
        """
        估计当前阶段还剩余的月数

        Args:
            phase: 当前阶段
            progress: 当前进度

        Returns:
            剩余月数
        """
        # 每个阶段平均持续时间（月）
        avg_duration = {
            1: 9,   # 被动补库
            2: 12,  # 主动补库
            3: 9,   # 被动去库
            4: 9    # 主动去库
        }

        total_months = avg_duration.get(phase, 9)
        elapsed_months = total_months * progress
        remaining = total_months - elapsed_months

        return int(max(0, remaining))

    def _calc_confidence(self, demand_growth: float, inventory_growth: float) -> float:
        """
        计算判断的置信度

        Args:
            demand_growth: 需求增速
            inventory_growth: 库存增速

        Returns:
            置信度 (0-1)
        """
        # 信号越强，置信度越高
        demand_strength = min(abs(demand_growth) / 5.0, 1.0)
        inventory_strength = min(abs(inventory_growth) / 5.0, 1.0)

        confidence = (demand_strength + inventory_strength) / 2

        return confidence

    def get_historical_performance(self, phase: int) -> Dict:
        """
        获取该阶段的历史表现统计

        Args:
            phase: 周期阶段

        Returns:
            历史表现统计
        """
        # 模拟历史表现数据
        performance_map = {
            1: {
                'avg_return': 0.15,
                'win_rate': 0.72,
                'max_return': 0.45,
                'max_drawdown': -0.12,
                'best_sectors': ['有色金属', '煤炭', '化工']
            },
            2: {
                'avg_return': 0.22,
                'win_rate': 0.78,
                'max_return': 0.60,
                'max_drawdown': -0.15,
                'best_sectors': ['电子', '计算机', '机械设备']
            },
            3: {
                'avg_return': -0.08,
                'win_rate': 0.35,
                'max_return': 0.10,
                'max_drawdown': -0.25,
                'best_sectors': ['医药生物', '食品饮料', '公用事业']
            },
            4: {
                'avg_return': -0.15,
                'win_rate': 0.25,
                'max_return': 0.05,
                'max_drawdown': -0.30,
                'best_sectors': ['银行', '公用事业', '国债']
            }
        }

        return performance_map.get(phase, performance_map[1])
