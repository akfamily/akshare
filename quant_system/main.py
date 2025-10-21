"""
量化系统主程序
整合所有模块，提供统一的接口
"""

import sys
import os
from datetime import datetime
from typing import Dict, Optional

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config, DEFAULT_CONFIG
from utils.logger import logger, get_logger
from data.fetcher.akshare_api import AKShareAPI
from analysis.cycle.kitchin import KitchinCycle
from analysis.cycle.juglar import JuglarCycle
from analysis.cycle.marks_pendulum import MarksPendulum


class QuantSystem:
    """量化系统主类"""

    def __init__(self, config: Dict = None):
        """
        初始化量化系统

        Args:
            config: 自定义配置字典
        """
        # 配置
        self.config = Config(config)

        # 日志
        self.logger = get_logger()
        self.logger.info("="*50)
        self.logger.info("量化系统初始化开始")
        self.logger.info("="*50)

        # 数据获取器
        self.data_api = AKShareAPI()

        # 周期分析器
        self.kitchin_cycle = KitchinCycle(self.data_api)
        self.juglar_cycle = JuglarCycle(self.data_api)
        self.marks_pendulum = MarksPendulum(self.data_api)

        self.logger.info("量化系统初始化完成")

    def analyze_market_cycle(self) -> Dict:
        """
        分析市场周期状态

        Returns:
            包含所有周期分析结果的字典
        """
        self.logger.info("\n开始市场周期分析...")

        # 1. 基钦周期（库存周期）
        self.logger.info("\n1. 分析基钦周期（库存周期）...")
        kitchin_result = self.kitchin_cycle.identify_phase()

        # 2. 朱格拉周期（产能周期）
        self.logger.info("\n2. 分析朱格拉周期（产能周期）...")
        juglar_result = self.juglar_cycle.calculate_phase()

        # 3. 马克斯钟摆（情绪周期）
        self.logger.info("\n3. 分析市场情绪（马克斯钟摆）...")
        pendulum_result = self.marks_pendulum.calculate_pendulum_position()

        # 整合结果
        cycle_analysis = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'kitchin': kitchin_result,
            'juglar': juglar_result,
            'pendulum': pendulum_result
        }

        self.logger.info("\n市场周期分析完成")

        return cycle_analysis

    def get_investment_advice(self) -> Dict:
        """
        获取投资建议

        Returns:
            综合投资建议
        """
        self.logger.info("\n生成投资建议...")

        # 分析市场周期
        cycle_analysis = self.analyze_market_cycle()

        kitchin_phase = cycle_analysis['kitchin']['phase']
        juglar_phase = cycle_analysis['juglar']['phase']
        pendulum_score = cycle_analysis['pendulum']['total_score']

        # 1. 行业配置建议
        kitchin_sectors = self.kitchin_cycle.get_sector_rotation(kitchin_phase)
        juglar_sectors = self.juglar_cycle.get_industry_preference(juglar_phase)

        # 2. 仓位建议
        kitchin_timing = self.kitchin_cycle.get_timing_signal(
            kitchin_phase,
            cycle_analysis['kitchin']['progress']
        )
        pendulum_rec = cycle_analysis['pendulum']['recommendation']

        # 3. 综合建议
        recommended_position = (
            kitchin_timing['target_position'] * 0.4 +
            pendulum_rec['position'] * 0.6
        )

        advice = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'recommended_position': recommended_position,
            'market_phase': {
                'kitchin': cycle_analysis['kitchin']['phase_name'],
                'juglar': cycle_analysis['juglar']['phase_name'],
                'sentiment': cycle_analysis['pendulum']['level']
            },
            'sector_advice': {
                'kitchin_best': kitchin_sectors['best'],
                'juglar_overweight': juglar_sectors['overweight'],
                'combined_recommendation': self._combine_sector_advice(
                    kitchin_sectors,
                    juglar_sectors
                )
            },
            'timing_signal': kitchin_timing['signal'],
            'sentiment_action': pendulum_rec['action'],
            'risk_level': self._assess_risk_level(pendulum_score),
            'key_points': self._generate_key_points(cycle_analysis)
        }

        self.logger.info("投资建议生成完成")

        return advice

    def generate_daily_report(self) -> str:
        """
        生成每日市场分析报告

        Returns:
            报告文本
        """
        advice = self.get_investment_advice()

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║              A股量化系统 - 每日市场分析报告                    ║
╠══════════════════════════════════════════════════════════════╣
║ 报告日期: {advice['date']}
╠══════════════════════════════════════════════════════════════╣

【市场周期定位】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 基钦周期（库存周期）: {advice['market_phase']['kitchin']}
• 朱格拉周期（产能周期）: {advice['market_phase']['juglar']}
• 市场情绪温度: {advice['market_phase']['sentiment']}

【投资建议】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 建议仓位: {advice['recommended_position']:.1%}
• 择时信号: {advice['timing_signal']}
• 情绪策略: {advice['sentiment_action']}
• 风险等级: {advice['risk_level']}

【行业配置】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
推荐超配行业:
{self._format_list(advice['sector_advice']['combined_recommendation']['overweight'])}

标配行业:
{self._format_list(advice['sector_advice']['combined_recommendation']['neutral'])}

低配行业:
{self._format_list(advice['sector_advice']['combined_recommendation']['underweight'])}

【关键要点】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self._format_list(advice['key_points'], numbered=True)}

╚══════════════════════════════════════════════════════════════╝
        """

        return report

    # ==================== 私有方法 ====================

    def _combine_sector_advice(self, kitchin_sectors: Dict, juglar_sectors: Dict) -> Dict:
        """综合两个周期的行业建议"""
        # 简化版本：基钦周期权重60%，朱格拉周期权重40%
        return {
            'overweight': kitchin_sectors['best'][:3] + juglar_sectors['overweight'][:2],
            'neutral': kitchin_sectors['good'],
            'underweight': kitchin_sectors['avoid']
        }

    def _assess_risk_level(self, pendulum_score: float) -> str:
        """评估风险等级"""
        if pendulum_score > 80:
            return "高风险（建议大幅降低仓位）"
        elif pendulum_score > 60:
            return "中高风险（注意控制仓位）"
        elif pendulum_score > 40:
            return "中等风险（均衡配置）"
        elif pendulum_score > 20:
            return "中低风险（可逐步加仓）"
        else:
            return "低风险（历史性机会）"

    def _generate_key_points(self, cycle_analysis: Dict) -> list:
        """生成关键要点"""
        points = []

        # 基于基钦周期
        kitchin = cycle_analysis['kitchin']
        points.append(
            f"库存周期处于{kitchin['phase_name']}阶段，"
            f"预计还将持续{kitchin['estimated_duration']}个月"
        )

        # 基于朱格拉周期
        juglar = cycle_analysis['juglar']
        points.append(
            f"产能周期处于{juglar['phase_name']}阶段，"
            f"{juglar['next_inflection']}"
        )

        # 基于情绪
        pendulum = cycle_analysis['pendulum']
        points.append(
            f"市场情绪温度为{pendulum['total_score']:.1f}，"
            f"{pendulum['recommendation']['reason']}"
        )

        return points

    def _format_list(self, items: list, numbered=False) -> str:
        """格式化列表"""
        if numbered:
            return '\n'.join([f"{i+1}. {item}" for i, item in enumerate(items)])
        else:
            return '  ' + ', '.join(items) if items else '  无'


def main():
    """主函数示例"""
    # 初始化系统
    system = QuantSystem()

    # 生成每日报告
    report = system.generate_daily_report()

    # 打印报告
    print(report)

    # 保存报告
    report_dir = 'reports'
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    report_file = os.path.join(
        report_dir,
        f"daily_report_{datetime.now().strftime('%Y%m%d')}.txt"
    )

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n报告已保存至: {report_file}")


if __name__ == '__main__':
    main()
