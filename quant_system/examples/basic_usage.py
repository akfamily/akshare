"""
基础使用示例
演示如何使用量化系统的各个模块
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import QuantSystem
from analysis.cycle.kitchin import KitchinCycle
from analysis.cycle.juglar import JuglarCycle
from analysis.cycle.marks_pendulum import MarksPendulum


def example_1_basic_report():
    """示例1：生成基础的每日报告"""
    print("\n" + "="*60)
    print("示例1：生成每日市场分析报告")
    print("="*60)

    # 初始化系统
    system = QuantSystem()

    # 生成报告
    report = system.generate_daily_report()

    # 打印报告
    print(report)


def example_2_cycle_analysis():
    """示例2：详细的周期分析"""
    print("\n" + "="*60)
    print("示例2：详细周期分析")
    print("="*60)

    system = QuantSystem()

    # 获取周期分析结果
    cycle_analysis = system.analyze_market_cycle()

    # 打印基钦周期
    print("\n【基钦周期（库存周期）】")
    kitchin = cycle_analysis['kitchin']
    print(f"当前阶段: {kitchin['phase_name']}")
    print(f"阶段进度: {kitchin['progress']:.1%}")
    print(f"需求增速: {kitchin['demand_growth']:.2f}%")
    print(f"库存增速: {kitchin['inventory_growth']:.2f}%")
    print(f"剩余时间: {kitchin['estimated_duration']}个月")
    print(f"置信度: {kitchin['confidence']:.1%}")

    # 打印朱格拉周期
    print("\n【朱格拉周期（产能周期）】")
    juglar = cycle_analysis['juglar']
    print(f"当前阶段: {juglar['phase_name']}")
    print(f"置信度: {juglar['confidence']:.1%}")
    print(f"拐点预测: {juglar['next_inflection']}")

    # 打印情绪分析
    print("\n【市场情绪（马克斯钟摆）】")
    pendulum = cycle_analysis['pendulum']
    print(f"总体得分: {pendulum['total_score']:.1f}/100")
    print(f"市场状态: {pendulum['level']}")
    print(f"估值得分: {pendulum['valuation']:.1f}")
    print(f"情绪得分: {pendulum['sentiment']:.1f}")
    print(f"流动性得分: {pendulum['liquidity']:.1f}")
    print(f"市场宽度得分: {pendulum['breadth']:.1f}")


def example_3_investment_advice():
    """示例3：获取投资建议"""
    print("\n" + "="*60)
    print("示例3：投资建议")
    print("="*60)

    system = QuantSystem()

    # 获取投资建议
    advice = system.get_investment_advice()

    print(f"\n【综合建议】")
    print(f"建议仓位: {advice['recommended_position']:.1%}")
    print(f"择时信号: {advice['timing_signal']}")
    print(f"情绪策略: {advice['sentiment_action']}")
    print(f"风险等级: {advice['risk_level']}")

    print(f"\n【行业配置】")
    print(f"超配行业: {', '.join(advice['sector_advice']['combined_recommendation']['overweight'][:5])}")
    print(f"低配行业: {', '.join(advice['sector_advice']['combined_recommendation']['underweight'][:3])}")

    print(f"\n【关键要点】")
    for i, point in enumerate(advice['key_points'], 1):
        print(f"{i}. {point}")


def example_4_sector_rotation():
    """示例4：行业轮动策略"""
    print("\n" + "="*60)
    print("示例4：行业轮动策略")
    print("="*60)

    kitchin = KitchinCycle()

    # 获取当前阶段
    result = kitchin.identify_phase()

    print(f"\n当前库存周期阶段: {result['phase_name']}")

    # 获取行业轮动建议
    rotation = kitchin.get_sector_rotation(result['phase'])

    print(f"\n阶段描述: {rotation['phase_desc']}")
    print(f"\n配置逻辑: {rotation['logic']}")
    print(f"\n最佳配置: {', '.join(rotation['best'])}")
    print(f"较好配置: {', '.join(rotation['good'])}")
    print(f"回避板块: {', '.join(rotation['avoid'])}")
    print(f"\n建议仓位: {rotation['recommended_position']:.1%}")


def example_5_timing_signals():
    """示例5：择时信号"""
    print("\n" + "="*60)
    print("示例5：择时信号")
    print("="*60)

    kitchin = KitchinCycle()

    # 获取当前阶段
    result = kitchin.identify_phase()

    # 获取择时信号
    signal = kitchin.get_timing_signal(result['phase'], result['progress'])

    print(f"\n当前阶段: {result['phase_name']}")
    print(f"阶段进度: {result['progress']:.1%}")

    print(f"\n【择时信号】")
    print(f"信号: {signal['signal']}")
    print(f"理由: {signal['reason']}")
    print(f"目标仓位: {signal['target_position']:.1%}")
    print(f"重点关注: {', '.join(signal['focus_sectors'])}")
    print(f"紧急程度: {signal['urgency']}")


def example_6_sentiment_analysis():
    """示例6：情绪分析详解"""
    print("\n" + "="*60)
    print("示例6：市场情绪分析")
    print("="*60)

    pendulum = MarksPendulum()

    # 计算钟摆位置
    result = pendulum.calculate_pendulum_position()

    print(f"\n【情绪温度计】")
    print(f"总体得分: {result['total_score']:.1f}/100")
    print(f"市场状态: {result['level']}")

    print(f"\n【各维度得分】")
    print(f"估值水平: {result['valuation']:.1f}/100")
    print(f"市场情绪: {result['sentiment']:.1f}/100")
    print(f"流动性: {result['liquidity']:.1f}/100")
    print(f"市场宽度: {result['breadth']:.1f}/100")

    print(f"\n【操作建议】")
    rec = result['recommendation']
    print(f"建议动作: {rec['action']}")
    print(f"建议仓位: {rec['position']:.1%}")
    print(f"投资风格: {rec['style']}")
    print(f"理由: {rec['reason']}")
    print(f"紧急程度: {rec['urgency']}")

    # 获取历史极值
    extremes = pendulum.get_historical_extremes()
    print(f"\n【历史参考】")
    print(f"历史最低点: {extremes['historical_low']['date']} "
          f"得分{extremes['historical_low']['score']} - "
          f"{extremes['historical_low']['description']}")
    print(f"历史最高点: {extremes['historical_high']['date']} "
          f"得分{extremes['historical_high']['score']} - "
          f"{extremes['historical_high']['description']}")


def main():
    """运行所有示例"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + " "*15 + "A股量化系统使用示例" + " "*15 + "█")
    print("█" + " "*58 + "█")
    print("█"*60)

    # 运行示例
    examples = [
        example_1_basic_report,
        example_2_cycle_analysis,
        example_3_investment_advice,
        example_4_sector_rotation,
        example_5_timing_signals,
        example_6_sentiment_analysis
    ]

    try:
        for i, example in enumerate(examples, 1):
            input(f"\n按回车键运行示例{i}...")
            example()

    except KeyboardInterrupt:
        print("\n\n用户中断，退出示例程序")

    print("\n" + "="*60)
    print("所有示例运行完成！")
    print("="*60)


if __name__ == '__main__':
    main()
