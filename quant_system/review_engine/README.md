# A股日度复盘引擎

## 📋 项目状态

### ✅ 已完成（当前提交）

1. **项目架构设计**
   - 完整的目录结构
   - 配置系统（config.yaml + .env）
   - 数据层设计（SQLite + Parquet）

2. **数据提供者（providers/akshare_provider.py）**
   - ✅ AkShare接口封装
   - ✅ 指数数据获取（上证/深成/创业板/沪深300）
   - ✅ 成交额计算
   - ✅ 市场广度（涨跌家数、涨跌停、连板）
   - ✅ 北向资金
   - ✅ 数据校验机制
   - ✅ 错误处理与重试
   - ✅ SQLite持久化

3. **配置系统**
   - ✅ config.yaml（权重、规则、ETF分组）
   - ✅ .env.example（环境变量）

### 🚧 待实现（下一步）

按照PRD的要求，还需实现以下模块：

#### 1. 完善数据提供者
- [ ] ETF流向获取
- [ ] 融资融券数据
- [ ] 行业数据聚合
- [ ] 宏观数据（PMI、PPI、大宗商品）
- [ ] Parquet存储
- [ ] 连板持续率计算（需历史数据）

#### 2. 因子计算模块（core/factors.py）
- [ ] 多周期EMA计算（5/10/30）
- [ ] 线性斜率（回归β）
- [ ] rolling z-score
- [ ] 趋势标签生成

#### 3. 评分系统（core/scoring.py）
- [ ] Macro评分（25%）
- [ ] Liquidity评分（35%）
- [ ] Risk-on评分（20%）
- [ ] Momentum评分（20%）
- [ ] 总分合成

#### 4. 行业轮动（core/allocation.py）
- [ ] 强度计算（收益分位+净流分位）
- [ ] 拥挤度计算（换手分位+涨停分位）
- [ ] 四象限分类
- [ ] 超配/低配决策

#### 5. 配置映射（core/allocation.py）
- [ ] 总分→仓位/风格映射
- [ ] 行业权重分配

#### 6. 报告生成（reporting/renderer.py）
- [ ] Markdown文本报告
- [ ] 三段式收束（利好/利空/结论）
- [ ] JSON结构化输出
- [ ] 图表生成（可选）

#### 7. DeepSeek集成（integrations/deepseek.py）
- [ ] API接口
- [ ] 开关控制

#### 8. 主程序（run_daily.py）
- [ ] 完整流程编排
- [ ] 命令行参数
- [ ] 日志记录

#### 9. 测试（tests/）
- [ ] 自动验收脚本
- [ ] 单元测试
- [ ] 集成测试

---

## 🚀 快速开始（当前可用功能）

### 安装依赖

```bash
pip install akshare pandas numpy pyyaml python-dotenv sqlalchemy
```

### 测试数据获取

```python
import yaml
from providers.akshare_provider import AkShareProvider

# 加载配置
with open('config/config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 创建提供者
provider = AkShareProvider(config)

# 获取今日数据
from datetime import datetime
today = datetime.now().strftime('%Y-%m-%d')

# 获取并保存数据
provider.fetch_and_save_all(today)

# 数据已保存到 data/review.sqlite
```

---

## 📁 目录结构

```
review_engine/
├── config/
│   ├── config.yaml          # 主配置文件
│   └── .env.example         # 环境变量示例
├── providers/
│   └── akshare_provider.py  # ✅ AkShare数据提供者
├── core/
│   ├── factors.py           # 🚧 因子计算
│   ├── scoring.py           # 🚧 评分系统
│   └── allocation.py        # 🚧 配置决策
├── reporting/
│   └── renderer.py          # 🚧 报告生成
├── integrations/
│   └── deepseek.py          # 🚧 DeepSeek接口
├── data/
│   ├── review.sqlite        # SQLite数据库
│   └── parquet/             # Parquet文件
├── tests/
│   └── test_pipeline.py     # 🚧 验收测试
├── run_daily.py             # 🚧 主程序
└── README.md                # 本文件
```

---

## 🎯 核心设计原则

### 1. 严禁虚拟数据
- ✅ 所有数据必须来自AkShare
- ✅ 数据校验：空值、字段完整性
- ✅ 失败可追溯：清晰的错误信息

### 2. 数据持久化
- ✅ SQLite：结构化数据
- 🚧 Parquet：时间序列
- ✅ 幂等upsert：重复运行不出错

### 3. 多周期趋势
- 🚧 5/10/30日EMA、斜率、z-score
- 🚧 趋势标签（共振上行/分化震荡等）

### 4. 四维评分
- 🚧 Macro/Liquidity/Risk-on/Momentum
- 🚧 可配置权重
- 🚧 0-100标准化

### 5. 行业轮动
- 🚧 强度×拥挤度矩阵
- 🚧 四象限分类
- 🚧 超/标/低配决策

### 6. 报告输出
- 🚧 Markdown文本（三段式）
- 🚧 JSON结构化
- 🚧 图表（可选）

---

## 🐛 已知限制（当前版本）

1. **ETF流向**：暂未实现（需要份额变化或申赎数据）
2. **融资融券**：暂未实现
3. **行业聚合**：暂未实现
4. **宏观数据**：暂未实现
5. **连板持续率**：需要多日历史数据计算
6. **因子计算**：暂未实现
7. **评分系统**：暂未实现
8. **报告生成**：暂未实现

---

## 📝 下一步计划

### 阶段1：完善数据层（1-2天）
- [ ] 实现所有数据接口
- [ ] Parquet持久化
- [ ] 历史数据回填

### 阶段2：核心计算（2-3天）
- [ ] 因子计算模块
- [ ] 评分系统
- [ ] 行业轮动

### 阶段3：报告与集成（1-2天）
- [ ] 报告生成
- [ ] 主程序编排
- [ ] DeepSeek接口

### 阶段4：测试与优化（1天）
- [ ] 自动验收测试
- [ ] 性能优化
- [ ] 文档完善

---

## 🤝 开发说明

### 对于Claude Code

当前已完成**基础架构和数据层**，可以按以下顺序继续开发：

1. **优先级1**：完善`providers/akshare_provider.py`
   - 添加ETF、融资融券、行业、宏观数据接口
   - 实现Parquet持久化

2. **优先级2**：实现`core/factors.py`
   - 多周期EMA、斜率、z-score计算
   - 趋势标签生成

3. **优先级3**：实现`core/scoring.py`
   - 四维评分逻辑
   - 权重可配置

4. **优先级4**：实现`core/allocation.py`
   - 行业轮动矩阵
   - 仓位/风格决策

5. **优先级5**：实现`reporting/renderer.py`
   - Markdown报告
   - JSON输出
   - 三段式收束

6. **优先级6**：实现`run_daily.py`
   - 流程编排
   - 命令行参数

7. **优先级7**：实现测试
   - 自动验收清单

### 代码规范

- ✅ 严禁使用`random`、`np.random`等生成虚拟数据
- ✅ 所有异常必须有清晰的错误信息
- ✅ 日志级别：INFO（流程节点）、WARNING（降级）、ERROR（失败）
- ✅ 函数文档字符串说明参数、返回值、异常

---

## 📊 数据流程图

```
AkShare接口
    ↓
数据校验（字段、空值、单位）
    ↓
持久化（SQLite + Parquet）
    ↓
多周期因子计算（5/10/30）
    ↓
四维评分（Macro/Liquidity/Risk-on/Momentum）
    ↓
总分 → 仓位/风格/行业权重
    ↓
报告生成（Markdown + JSON）
    ↓
（可选）DeepSeek增强
```

---

## 🎉 总结

当前版本提供了**完整的架构设计**和**数据层基础**，确保：
- ✅ 真实数据源（AkShare）
- ✅ 数据校验与错误处理
- ✅ 持久化基础设施

接下来需要按照PRD逐步实现：
1. 完善数据接口
2. 因子计算
3. 评分系统
4. 行业轮动
5. 报告生成

这是一个**渐进式开发**的过程，每个模块都可以独立测试和验证。

---

**最后更新**: 2025-10-21
**作者**: Claude Code
**版本**: 0.1.0 (MVP架构阶段)
