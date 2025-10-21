#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单测试脚本 - 验证系统是否正常工作
"""

print("="*60)
print("🔍 A股量化系统 - 环境测试")
print("="*60)
print()

# 测试1：基础库
print("【测试1】检查基础库...")
try:
    import pandas as pd
    import numpy as np
    print("  ✓ Pandas版本:", pd.__version__)
    print("  ✓ NumPy版本:", np.__version__)
except ImportError as e:
    print(f"  ✗ 失败: {e}")
    print()
    print("解决方法：")
    print("  pip install pandas numpy")
    exit(1)

print()

# 测试2：项目模块
print("【测试2】检查项目模块...")
try:
    from analysis.cycle.kitchin import KitchinCycle
    from analysis.cycle.juglar import JuglarCycle
    from analysis.cycle.marks_pendulum import MarksPendulum
    print("  ✓ 周期分析模块导入成功")
except ImportError as e:
    print(f"  ✗ 失败: {e}")
    print()
    print("解决方法：")
    print("  1. 确保在 quant_system 目录下运行")
    print("  2. 检查目录结构是否完整")
    exit(1)

print()

# 测试3：运行基钦周期
print("【测试3】运行基钦周期分析...")
try:
    kitchin = KitchinCycle()
    result = kitchin.identify_phase()

    print("  ✓ 基钦周期运行成功")
    print(f"    当前阶段: {result['phase_name']}")
    print(f"    阶段进度: {result['progress']:.1%}")
    print(f"    需求增速: {result['demand_growth']:.2f}%")
    print(f"    库存增速: {result['inventory_growth']:.2f}%")
    print(f"    置信度: {result['confidence']:.1%}")
except Exception as e:
    print(f"  ✗ 失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print()

# 测试4：运行朱格拉周期
print("【测试4】运行朱格拉周期分析...")
try:
    juglar = JuglarCycle()
    result = juglar.calculate_phase()

    print("  ✓ 朱格拉周期运行成功")
    print(f"    当前阶段: {result['phase_name']}")
    print(f"    置信度: {result['confidence']:.1%}")
except Exception as e:
    print(f"  ✗ 失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print()

# 测试5：运行市场情绪分析
print("【测试5】运行市场情绪分析...")
try:
    pendulum = MarksPendulum()
    result = pendulum.calculate_pendulum_position()

    print("  ✓ 市场情绪分析运行成功")
    print(f"    情绪温度: {result['total_score']:.1f}/100")
    print(f"    市场状态: {result['level']}")
    print(f"    估值得分: {result['valuation']:.1f}")
    print(f"    情绪得分: {result['sentiment']:.1f}")
    print(f"    流动性得分: {result['liquidity']:.1f}")
    print(f"    市场宽度得分: {result['breadth']:.1f}")
except Exception as e:
    print(f"  ✗ 失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print()

# 测试6：运行主程序
print("【测试6】测试主程序...")
try:
    from main import QuantSystem

    system = QuantSystem()
    advice = system.get_investment_advice()

    print("  ✓ 主程序运行成功")
    print(f"    建议仓位: {advice['recommended_position']:.1%}")
    print(f"    择时信号: {advice['timing_signal']}")
    print(f"    情绪策略: {advice['sentiment_action']}")
    print(f"    风险等级: {advice['risk_level']}")
except Exception as e:
    print(f"  ✗ 失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print()
print("="*60)
print("🎉 恭喜！所有测试通过！")
print("="*60)
print()
print("下一步：")
print("  1. 运行主程序：python main.py")
print("  2. 查看示例：python examples/basic_usage.py")
print("  3. 阅读文档：README.md")
print()
