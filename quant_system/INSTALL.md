# 安装指南

## 环境要求

- Python 3.8+
- pip

## 安装步骤

### 1. 安装依赖包

```bash
# 进入项目目录
cd quant_system

# 安装依赖
pip install -r requirements.txt
```

如果上述命令失败，可以逐个安装：

```bash
pip install pandas numpy scipy scikit-learn sqlalchemy plotly matplotlib python-dateutil statsmodels
```

### 2. 验证安装

```bash
# 运行主程序
python main.py
```

如果成功，将看到每日市场分析报告。

### 3. 运行示例

```bash
# 运行基础示例
python examples/basic_usage.py
```

## 常见问题

### Q1: ModuleNotFoundError: No module named 'pandas'

**解决方案**：
```bash
pip install pandas
```

### Q2: 导入akshare失败

**解决方案**：
确保从项目根目录运行，系统会自动找到akshare模块。

### Q3: 数据获取失败

**说明**：
当前版本使用模拟数据进行演示。实际使用时需要：
1. 确保网络连接正常
2. akshare能够正常访问数据源

## 快速测试

创建一个简单的测试脚本 `test_basic.py`：

```python
import sys
sys.path.insert(0, '.')

from analysis.cycle.kitchin import KitchinCycle

# 测试基钦周期
kitchin = KitchinCycle()
result = kitchin.identify_phase()

print("="*50)
print("基钦周期测试")
print("="*50)
print(f"当前阶段: {result['phase_name']}")
print(f"阶段进度: {result['progress']:.1%}")
print(f"需求增速: {result['demand_growth']:.2f}%")
print(f"库存增速: {result['inventory_growth']:.2f}%")
print("="*50)
print("测试通过！")
```

运行测试：
```bash
python test_basic.py
```

## 下一步

安装完成后，建议：

1. 阅读 `README.md` 了解系统架构
2. 运行 `python main.py` 生成每日报告
3. 查看 `examples/basic_usage.py` 学习各模块用法
4. 根据需要调整 `config/settings.py` 中的配置

## 技术支持

如遇问题，请：
1. 查看日志文件 `logs/quant_system_YYYYMMDD.log`
2. 提交 GitHub Issue
3. 参考 AKShare 官方文档: https://akshare.akfamily.xyz/
