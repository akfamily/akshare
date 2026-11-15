# 策略回测

本策略回测文档的主要目的是为了方便的展示 [AKShare](https://github.com/akfamily/akshare) 的数据接口
调用、基本的数据处理和回测框架使用，并不涉及任何投资建议，提供的示例代码也仅供参考。

本策略示例是基于 Python 编程语言的开源回测框架 [AKQuant](https://github.com/akfamily/akquant) 和
[PyBroker](https://www.pybroker.com) 来演示！
```{note}
本教程的开发是基于：Python (64 位) 3.12.4 来进行的
```

## AKQuant 介绍（强烈推荐）

AKQuant 是一款专为量化投研 (Quantitative Research) 打造的高性能混合架构引擎。它以
Rust 铸造极速撮合内核，以 Python 链接数据与 AI 生态，旨在为量化投资者提供可靠高效的解决方案。
它超越了传统工具的范畴，将**事件驱动**、**机器学习**与**生产级风控**深度融合，让量化交易不再受限于计算性能，专注于策略本身的逻辑与价值。

## AKQuant 安装

AKQuant 支持在 Windows、macOS 和 Linux 中的 Python 3.10（建议使用 Python 3.13）及以上版本使用。其安装非常简单，
只需要 ```pip install akquant``` 就可以实现一键安装。

## AKQuant 教程

AKShare 拥有最齐全的量化投研和使用文档，请访问：[AKQuant](https://akquant.akfamily.xyz)

## AKQuant 策略示例

```python
import akquant as aq
import akshare as ak
from akquant import Strategy

# 1. 准备数据
# 使用 akshare 获取 A 股历史数据 (需安装: pip install akshare)
df = ak.stock_zh_a_hist_sina(symbol="sh600000", start_date="20230101", end_date="20231231")


class MyStrategy(Strategy):
    def on_bar(self, bar):
        # 简单策略示例:
        # 当收盘价 > 开盘价 (阳线) -> 买入
        # 当收盘价 < 开盘价 (阴线) -> 卖出

        # 获取当前持仓
        current_pos = self.get_position(bar.symbol)

        if current_pos == 0 and bar.close > bar.open:
            self.buy(bar.symbol, 100)
            print(f"[{bar.timestamp_str}] Buy 100 at {bar.close:.2f}")

        elif current_pos > 0 and bar.close < bar.open:
            self.close_position(bar.symbol)
            print(f"[{bar.timestamp_str}] Sell 100 at {bar.close:.2f}")


# 运行回测
result = aq.run_backtest(
    data=df,
    strategy=MyStrategy,
    symbol="sh600000"
)

# 打印回测结果
print("\n=== Backtest Result ===")
print(result.metrics_df)

```

**运行结果示例：**

```text
=== Backtest Result ===
                                            value
name
start_time              2023-01-03 00:00:00+08:00
end_time                2023-12-29 00:00:00+08:00
duration                        360 days, 0:00:00
total_bars                                    242
trade_count                                  56.0
initial_market_value                    1000000.0
end_market_value                     999433.06461
total_pnl                                    17.0
unrealized_pnl                                2.0
total_return_pct                        -0.056694
annualized_return                       -0.000575
volatility                               0.000091
total_profit                                175.0
total_loss                                 -158.0
total_commission                        585.93539
max_drawdown                            566.93539
max_drawdown_pct                         0.056694
win_rate                                33.928571
loss_rate                               66.071429
winning_trades                               19.0
losing_trades                                37.0
avg_pnl                                  0.303571
avg_return_pct                           0.042808
avg_trade_bars                           1.946429
avg_profit                               9.210526
avg_profit_pct                           1.269445
avg_winning_trade_bars                   2.789474
avg_loss                                 -4.27027
avg_loss_pct                            -0.587086
avg_losing_trade_bars                    1.513514
largest_win                                  45.0
largest_win_pct                          6.016043
largest_win_bars                              4.0
largest_loss                                -33.0
largest_loss_pct                        -4.441454
largest_loss_bars                             1.0
max_wins                                      3.0
max_losses                                    7.0
sharpe_ratio                            -6.320253
sortino_ratio                           -6.831061
profit_factor                            1.107595
ulcer_index                              0.000307
upi                                     -1.874895
equity_r2                                0.981117
std_error                               22.958262
calmar_ratio                            -1.013885
exposure_time_pct                       45.867769
var_95                                  -0.000009
var_99                                  -0.000019
cvar_95                                 -0.000015
cvar_99                                 -0.000025
sqn                                       0.20869
kelly_criterion                          0.032959
```

## PyBroker 介绍

你是否希望借助 Python 和机器学习的力量来优化您的交易策略？那么你需要了解一下 PyBroker！这个 Python 框架专为开发算法交易策略而设计，
尤其关注使用机器学习的策略。借助 PyBroker，你可以轻松创建和微调交易规则，构建强大的模型，并深入了解你的策略表现。

## PyBroker 安装

PyBroker 支持在 Windows、macOS 和 Linux 中的 Python 3.9（建议使用 Python 3.11）及以上版本使用。其安装非常简单，
只需要 ```pip install lib-pybroker``` 就可以实现一键安装。

## PyBroker 文档

1. [PyBroker 官方文档](https://www.pybroker.com/)

## PyBroker 策略示例

```python
# 导入所需的库和模块
import pybroker as pb
from pybroker import Strategy, ExecContext
from pybroker.ext.data import AKShare

# 定义全局参数 "stock_code"（股票代码）、"percent"（持仓百分比）和 "stop_profit_pct"（止盈百分比）
pb.param(name='stock_code', value='600000')
pb.param(name='percent', value=1)
pb.param(name='stop_loss_pct', value=10)
pb.param(name='stop_profit_pct', value=10)

# 初始化 AKShare 数据源
akshare = AKShare()

# 使用 AKShare 数据源查询特定股票（由 "stock_code" 参数指定）在指定日期范围内的数据
df = akshare.query(symbols=[pb.param(name='stock_code')], start_date='20200131', end_date='20230228')


# 定义交易策略：如果当前没有持有该股票，则买入股票，并设置止盈点位
def buy_with_stop_loss(ctx: ExecContext):
    pos = ctx.long_pos()
    if not pos:
        # 计算目标股票数量，根据 "percent" 参数确定应购买的股票数量
        ctx.buy_shares = ctx.calc_target_shares(pb.param(name='percent'))
        ctx.hold_bars = 100
    else:
        ctx.sell_shares = pos.shares
        # 设置止盈点位，根据 "stop_profit_pct" 参数确定止盈点位
        ctx.stop_profit_pct = pb.param(name='stop_profit_pct')


# 创建策略配置，初始资金为 500000
my_config = pb.StrategyConfig(initial_cash=500000)
# 使用配置、数据源、起始日期、结束日期，以及刚才定义的交易策略创建策略对象
strategy = Strategy(akshare, start_date='20200131', end_date='20230228', config=my_config)
# 添加执行策略，设置股票代码和要执行的函数
strategy.add_execution(fn=buy_with_stop_loss, symbols=[pb.param(name='stock_code')])
# 执行回测，并打印出回测结果的度量值（四舍五入到小数点后四位）
result = strategy.backtest()
print(result.metrics_df.round(4))
```

```shell
Loading bar data...
Loaded bar data: 0:00:00
Backtesting: 2020-01-31 00:00:00 to 2023-02-28 00:00:00
Loading bar data...
Loaded bar data: 0:00:00
Test split: 2020-02-03 00:00:00 to 2023-02-28 00:00:00
100% (748 of 748) |######################| Elapsed Time: 0:00:00 Time:  0:00:00
Finished backtest: 0:00:03
                      name        value
0              trade_count     373.0000
1     initial_market_value  500000.0000
2         end_market_value  467328.0900
3                total_pnl  -33322.7800
4           unrealized_pnl     650.8700
5         total_return_pct      -6.6646
6             total_profit  530528.5100
7               total_loss -563851.2900
8               total_fees       0.0000
9             max_drawdown -113004.2700
10        max_drawdown_pct     -20.2704
11                win_rate      45.9215
12               loss_rate      54.0785
13          winning_trades     152.0000
14           losing_trades     179.0000
15                 avg_pnl     -89.3372
16          avg_return_pct      -0.0160
17          avg_trade_bars       1.0000
18              avg_profit    3490.3191
19          avg_profit_pct       0.6958
20  avg_winning_trade_bars       1.0000
21                avg_loss   -3150.0072
22            avg_loss_pct      -0.6241
23   avg_losing_trade_bars       1.0000
24             largest_win   31157.9400
25         largest_win_pct       5.9200
26        largest_win_bars       1.0000
27            largest_loss  -12682.6000
28        largest_loss_pct      -2.3100
29       largest_loss_bars       1.0000
30                max_wins       8.0000
31              max_losses       7.0000
32                  sharpe      -0.0132
33                 sortino      -0.0231
34           profit_factor       0.9638
35             ulcer_index       1.7639
36                     upi      -0.0039
37               equity_r2       0.5876
38               std_error   27448.1177
```
