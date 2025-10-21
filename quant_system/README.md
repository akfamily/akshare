# A股量化分析系统

基于周期理论的A股量化投资系统，融入周金涛的周期嵌套理论和霍华德·马克斯的市场钟摆理论。

## 📋 系统特色

### 核心理念

1. **三层周期嵌套**
   - 朱格拉周期（7-11年产能周期）
   - 基钦周期（3-4年库存周期）
   - 市场情绪周期（马克斯钟摆）

2. **动态因子权重**
   - 根据周期阶段自动调整因子权重
   - 复苏期：成长+动量
   - 繁荣期：动量+情绪
   - 衰退期：价值+质量
   - 萧条期：质量+防御

3. **多维度分析**
   - 宏观经济周期
   - 行业景气轮动
   - 市场情绪温度
   - 估值水平分位

## 🏗️ 系统架构

```
quant_system/
├── data/                          # 数据层
│   ├── fetcher/                   # 数据获取
│   │   └── akshare_api.py         # AKShare接口封装
│   ├── storage/                   # 数据存储
│   └── processor/                 # 数据处理
│
├── analysis/                      # 分析层
│   ├── cycle/                     # 周期分析
│   │   ├── kitchin.py             # 基钦周期（库存周期）
│   │   ├── juglar.py              # 朱格拉周期（产能周期）
│   │   └── marks_pendulum.py      # 马克斯钟摆（情绪周期）
│   ├── factor/                    # 因子分析
│   ├── valuation/                 # 估值分析
│   └── sentiment/                 # 情绪分析
│
├── strategy/                      # 策略层
│   ├── allocation/                # 资产配置
│   ├── selection/                 # 选股策略
│   └── timing/                    # 择时策略
│
├── risk/                          # 风控层
├── backtest/                      # 回测层
├── execution/                     # 执行层
├── visualization/                 # 可视化层
├── config/                        # 配置
│   └── settings.py                # 系统配置
├── utils/                         # 工具
│   ├── helpers.py                 # 辅助函数
│   └── logger.py                  # 日志管理
│
├── main.py                        # 主程序
└── README.md                      # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd quant_system
pip install -r requirements.txt
```

### 2. 运行示例

```python
# 生成每日市场分析报告
python main.py
```

### 3. 使用示例

```python
from main import QuantSystem

# 初始化系统
system = QuantSystem()

# 分析市场周期
cycle_analysis = system.analyze_market_cycle()

# 获取投资建议
advice = system.get_investment_advice()

# 生成报告
report = system.generate_daily_report()
print(report)
```

## 📊 核心模块说明

### 1. 基钦周期（库存周期）

**功能**：识别3-4年的库存周期，判断当前处于哪个阶段

**四象限**：
- 被动补库：需求↑ 库存↑（复苏初期）→ 配置上游资源
- 主动补库：需求↑ 库存↓（繁荣期）→ 配置中下游制造
- 被动去库：需求↓ 库存↓（衰退期）→ 转向防御
- 主动去库：需求↓ 库存↑（萧条期）→ 现金为王

**使用示例**：
```python
from analysis.cycle.kitchin import KitchinCycle

kitchin = KitchinCycle()

# 识别当前阶段
result = kitchin.identify_phase()
print(f"当前阶段: {result['phase_name']}")
print(f"阶段进度: {result['progress']:.1%}")

# 获取行业轮动建议
sectors = kitchin.get_sector_rotation(result['phase'])
print(f"最佳行业: {sectors['best']}")

# 获取择时信号
signal = kitchin.get_timing_signal(result['phase'], result['progress'])
print(f"择时信号: {signal['signal']}")
print(f"建议仓位: {signal['target_position']:.1%}")
```

### 2. 朱格拉周期（产能周期）

**功能**：识别7-11年的产能投资周期

**四阶段**：
1. 复苏期：产能利用率回升 → 配置周期股
2. 繁荣期：产能扩张，企业盈利改善 → 配置成长股
3. 衰退期：产能过剩 → 转向防御
4. 萧条期：产能出清 → 等待新周期

**使用示例**：
```python
from analysis.cycle.juglar import JuglarCycle

juglar = JuglarCycle()

# 计算当前阶段
result = juglar.calculate_phase()
print(f"当前阶段: {result['phase_name']}")

# 获取行业配置建议
industries = juglar.get_industry_preference(result['phase'])
print(f"超配行业: {industries['overweight']}")
print(f"低配行业: {industries['underweight']}")

# 获取资产配置调整
allocation = juglar.get_asset_allocation_adjustment(result['phase'])
print(f"建议仓位: {allocation['recommended_position']:.1%}")
```

### 3. 马克斯钟摆（情绪周期）

**功能**：量化市场情绪，识别市场极端状态

**四维度**：
- 估值水平（PE/PB分位数、风险溢价）
- 市场情绪（融资融券、开户数、搜索热度）
- 流动性（M2-M1剪刀差、利率、北向资金）
- 市场宽度（涨跌家数、创新高低、破净股数）

**钟摆位置**：0（极度悲观）到 100（极度乐观）

**使用示例**：
```python
from analysis.cycle.marks_pendulum import MarksPendulum

pendulum = MarksPendulum()

# 计算钟摆位置
result = pendulum.calculate_pendulum_position()
print(f"情绪温度: {result['total_score']:.1f}")
print(f"市场状态: {result['level']}")

# 获取操作建议
rec = result['recommendation']
print(f"建议动作: {rec['action']}")
print(f"建议仓位: {rec['position']:.1%}")
print(f"原因: {rec['reason']}")
```

## 📈 输出示例

### 每日市场分析报告

```
╔══════════════════════════════════════════════════════════════╗
║              A股量化系统 - 每日市场分析报告                    ║
╠══════════════════════════════════════════════════════════════╣
║ 报告日期: 2025-10-21
╠══════════════════════════════════════════════════════════════╣

【市场周期定位】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 基钦周期（库存周期）: 被动补库
• 朱格拉周期（产能周期）: 复苏
• 市场情绪温度: 悲观（可以布局）

【投资建议】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 建议仓位: 76.0%
• 择时信号: BUY
• 情绪策略: 逐步建仓
• 风险等级: 中低风险（可逐步加仓）

【行业配置】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
推荐超配行业:
  煤炭, 钢铁, 有色金属, 机械设备, 化工

标配行业:
  建筑材料, 建筑装饰, 交运

低配行业:
  消费, 医药, 科技

【关键要点】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 库存周期处于被动补库阶段，预计还将持续6个月
2. 产能周期处于复苏阶段，预计12个月后进入下一阶段
3. 市场情绪温度为35.2，市场悲观，但尚未见底

╚══════════════════════════════════════════════════════════════╝
```

## 🔧 配置说明

系统配置位于 `config/settings.py`，主要配置项：

```python
DEFAULT_CONFIG = {
    # 周期配置
    'cycle': {
        'juglar_window': 120,     # 朱格拉周期观察窗口（月）
        'kitchin_window': 48,     # 基钦周期观察窗口（月）
        'sentiment_window': 60,   # 情绪指标观察窗口（日）
    },

    # 因子配置
    'factor': {
        'base_weights': {
            'value': 0.20,
            'quality': 0.20,
            'growth': 0.25,
            'momentum': 0.20,
            'sentiment': 0.10,
            'technical': 0.05
        },
    },

    # 风险控制
    'risk': {
        'max_position_pct': 0.10,       # 单只股票最大仓位
        'max_sector_pct': 0.30,         # 单个行业最大仓位
        'max_drawdown_limit': 0.25,     # 最大回撤限制
    }
}
```

## 📚 理论基础

### 周金涛的周期嵌套理论

1. **康波周期**（50-60年）：技术革命周期
2. **库兹涅茨周期**（15-25年）：房地产周期
3. **朱格拉周期**（7-11年）：产能投资周期
4. **基钦周期**（3-4年）：库存周期

### 霍华德·马克斯的钟摆理论

市场在"极度悲观"和"极度乐观"之间摆动，很少停留在"理性"的中点。

**核心观点**：
- 第一层思维：判断经济和企业基本面
- 第二层思维：判断市场对基本面的预期程度
- 最佳投资机会出现在钟摆摆到极端位置时

## ⚠️ 免责声明

本系统仅供学习研究使用，不构成任何投资建议。

- 历史表现不代表未来收益
- 模型基于历史数据和统计规律，可能失效
- 投资有风险，决策需谨慎

## 🔮 未来规划

### 第一阶段（已完成）
- ✅ 基础框架搭建
- ✅ 周期识别引擎
- ✅ 数据获取接口
- ✅ 基本配置系统

### 第二阶段（规划中）
- ⏳ 多因子选股引擎
- ⏳ 资产配置策略（全天候、斯文森）
- ⏳ 回测框架
- ⏳ 风险控制模块

### 第三阶段（规划中）
- ⏳ 可视化Dashboard
- ⏳ 实时监控系统
- ⏳ 参数优化器
- ⏳ 完整的文档和示例

## 📞 联系方式

- GitHub Issues: [提交问题](https://github.com/akfamily/akshare/issues)
- AKShare文档: https://akshare.akfamily.xyz/

## 📄 许可证

MIT License

---

**注意**：本系统是在AKShare项目基础上开发的量化分析工具，感谢AKShare团队提供的优秀数据接口。
