## [AKShare](https://github.com/akfamily/akshare) 策略示例

本策略示例文档的主要目的是为了方便的展示 [AKShare](https://github.com/akfamily/akshare) 的数据接口
调用、基本的数据处理和回测框架使用，并不涉及任何投资建议，提供的示例代码也仅供参考。

本策略示例都是基于 Python 编程语言的开源回测和交易框架 [Backtrader](https://www.backtrader.com) 来演示的，有兴趣
想深入了解该框架的小伙伴，可以参考官网文档学习，同时也可以加入合作的知识星球 **数据科学家** 学习：
![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/qrcode/data_scientist.png)

注意：本教程的开发是基于：Python (64 位) 3.8.6 来进行的

### Backtrader 介绍

[Backtrader](https://www.backtrader.com) 是基于 Python 编程语言的主要用于量化投资开源回测和交易的框架，可以用于多种资产的回测。
目前，[Backtrader](https://www.backtrader.com) 可以用于实现股票、期货、期权、外汇、加密货币等资产的回测，同时该开源框架也有强大的第三方社区支持，目前已经实现了
基于 IB、Oanda、VC、CCXT、MT5 等接口量化交易，随着该框架的流行，后期会有更多的小伙伴提供更多的第三方模块，学习和使用该框架是一个不错的选择！

#### Backtrader 下载和安装

[Backtrader](https://www.backtrader.com) 的下载和安装都比较简单，尤其是在配置好 [AKShare](https://github.com/akfamily/akshare) 的
基础上，我们只需要 ```pip install backtrader``` 就可以实现一键安装。如果需要了解 [AKShare](https://github.com/akfamily/akshare) 的
环境配置，请参考 [AKShare 环境配置](https://www.akshare.xyz/zh_CN/latest/anaconda.html) 来设置本地环境。想要通过源码来安装的小伙伴，可以访问 [Backtrader 的 GitHub 地址](https://github.com/mementum/backtrader) 来下载安装，由于源码安装比较繁琐，建议直接通过 ```pip``` 或 ```conda``` 来安装和使用。需要注意的是如果要输出图形，请安装 ```pip install matplotlib==3.2.2```

### Backtrader 系列教程

1. [Backtrader-系列教程-01-介绍](https://zhuanlan.zhihu.com/p/418247765)
2. [Backtrader-系列教程-02-环境配置](https://zhuanlan.zhihu.com/p/418255493)

### 股票策略

#### 基本策略

##### 代码

```python
from datetime import datetime

import backtrader as bt  # 升级到最新版
import matplotlib.pyplot as plt  # 由于 Backtrader 的问题，此处要求 pip install matplotlib==3.2.2
import akshare as ak  # 升级到最新版
import pandas as pd

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
stock_hfq_df = ak.stock_zh_a_hist(symbol="000001", adjust="hfq").iloc[:, :6]
# 处理字段命名，以符合 Backtrader 的要求
stock_hfq_df.columns = [
    'date',
    'open',
    'close',
    'high',
    'low',
    'volume',
]
# 把 date 作为日期索引，以符合 Backtrader 的要求
stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])


class MyStrategy(bt.Strategy):
    """
    主策略程序
    """
    params = (("maperiod", 20),)  # 全局设定交易策略的参数

    def __init__(self):
        """
        初始化函数
        """
        self.data_close = self.datas[0].close  # 指定价格序列
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buy_price = None
        self.buy_comm = None
        # 添加移动均线指标
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
        )

    def next(self):
        """
        执行逻辑
        """
        if self.order:  # 检查是否有指令等待执行,
            return
        # 检查是否持仓
        if not self.position:  # 没有持仓
            if self.data_close[0] > self.sma[0]:  # 执行买入条件判断：收盘价格上涨突破20日均线
                self.order = self.buy(size=100)  # 执行买入
        else:
            if self.data_close[0] < self.sma[0]:  # 执行卖出条件判断：收盘价格跌破20日均线
                self.order = self.sell(size=100)  # 执行卖出


cerebro = bt.Cerebro()  # 初始化回测系统
start_date = datetime(1991, 4, 3)  # 回测开始时间
end_date = datetime(2020, 6, 16)  # 回测结束时间
data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)  # 加载数据
cerebro.adddata(data)  # 将数据传入回测系统
cerebro.addstrategy(MyStrategy)  # 将交易策略加载到回测系统中
start_cash = 1000000
cerebro.broker.setcash(start_cash)  # 设置初始资本为 100000
cerebro.broker.setcommission(commission=0.002)  # 设置交易手续费为 0.2%
cerebro.run()  # 运行回测系统

port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
pnl = port_value - start_cash  # 盈亏统计

print(f"初始资金: {start_cash}\n回测期间：{start_date.strftime('%Y%m%d')}:{end_date.strftime('%Y%m%d')}")
print(f"总资金: {round(port_value, 2)}")
print(f"净收益: {round(pnl, 2)}")

cerebro.plot(style='candlestick')  # 画图
```

##### 结果

```
初始资金: 1000000
回测期间：20000101:20200421
总资金: 1010238.65
净收益: 10238.65
```

##### 可视化

![](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/readme/strategy/Figure_0.png)

#### 参数优化

##### 代码

```python
from datetime import datetime

import akshare as ak
import backtrader as bt
import matplotlib.pyplot as plt  # 由于 Backtrader 的问题，此处要求 pip install matplotlib==3.2.2
import pandas as pd

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置画图时的中文显示
plt.rcParams["axes.unicode_minus"] = False  # 设置画图时的负号显示


class MyStrategy(bt.Strategy):
    """
    主策略程序
    """
    params = (("maperiod", 20),
              ('printlog', False),)  # 全局设定交易策略的参数, maperiod是 MA 均值的长度

    def __init__(self):
        """
        初始化函数
        """
        self.data_close = self.datas[0].close  # 指定价格序列
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buy_price = None
        self.buy_comm = None
        # 添加移动均线指标
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
        )

    def next(self):
        """
        主逻辑
        """

        # self.log(f'收盘价, {data_close[0]}')  # 记录收盘价
        if self.order:  # 检查是否有指令等待执行,
            return
        # 检查是否持仓
        if not self.position:  # 没有持仓
            # 执行买入条件判断：收盘价格上涨突破15日均线
            if self.data_close[0] > self.sma[0]:
                self.log("BUY CREATE, %.2f" % self.data_close[0])
                # 执行买入
                self.order = self.buy()
        else:
            # 执行卖出条件判断：收盘价格跌破15日均线
            if self.data_close[0] < self.sma[0]:
                self.log("SELL CREATE, %.2f" % self.data_close[0])
                # 执行卖出
                self.order = self.sell()

    def log(self, txt, dt=None, do_print=False):
        """
        Logging function fot this strategy
        """
        if self.params.printlog or do_print:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        """
        记录交易执行情况
        """
        # 如果 order 为 submitted/accepted,返回空
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 如果order为buy/sell executed,报告价格结果
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f"买入:\n价格:{order.executed.price},\
                成本:{order.executed.value},\
                手续费:{order.executed.comm}"
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    f"卖出:\n价格：{order.executed.price},\
                成本: {order.executed.value},\
                手续费{order.executed.comm}"
                )
            self.bar_executed = len(self)

            # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("交易失败")
        self.order = None

    def notify_trade(self, trade):
        """
        记录交易收益情况
        """
        if not trade.isclosed:
            return
        self.log(f"策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}")

    def stop(self):
        """
        回测结束后输出结果
        """
        self.log("(MA均线： %2d日) 期末总资金 %.2f" % (self.params.maperiod, self.broker.getvalue()), do_print=True)


def main(code="600070", start_cash=1000000, stake=100, commission_fee=0.001):
    cerebro = bt.Cerebro()  # 创建主控制器
    cerebro.optstrategy(MyStrategy, maperiod=range(3, 31))  # 导入策略参数寻优
    # 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
    stock_hfq_df = ak.stock_zh_a_hist(symbol=code, adjust="hfq", start_date='20000101', end_date='20210617').iloc[:, :6]
    # 处理字段命名，以符合 Backtrader 的要求
    stock_hfq_df.columns = [
        'date',
        'open',
        'close',
        'high',
        'low',
        'volume',
    ]
    # 把 date 作为日期索引，以符合 Backtrader 的要求
    stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
    start_date = datetime(1991, 4, 3)  # 回测开始时间
    end_date = datetime(2021, 6, 16)  # 回测结束时间
    data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)  # 规范化数据格式
    cerebro.adddata(data)  # 将数据加载至回测系统
    cerebro.broker.setcash(start_cash)  # broker设置资金
    cerebro.broker.setcommission(commission=commission_fee)  # broker手续费
    cerebro.addsizer(bt.sizers.FixedSize, stake=stake)  # 设置买入数量
    print("期初总资金: %.2f" % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)  # 用单核 CPU 做优化
    print("期末总资金: %.2f" % cerebro.broker.getvalue())


if __name__ == '__main__':
    main(code="600070", start_cash=1000000, stake=100, commission_fee=0.001)
```

##### 结果

```
期初总资金: 1000000.00
2020-06-12, (MA均线：  3日) 期末总资金 1004105.69
2020-06-12, (MA均线：  4日) 期末总资金 1002384.49
2020-06-12, (MA均线：  5日) 期末总资金 1002063.96
2020-06-12, (MA均线：  6日) 期末总资金 1002113.63
2020-06-12, (MA均线：  7日) 期末总资金 1001715.32
2020-06-12, (MA均线：  8日) 期末总资金 999702.60
2020-06-12, (MA均线：  9日) 期末总资金 1001658.65
2020-06-12, (MA均线： 10日) 期末总资金 999698.63
2020-06-12, (MA均线： 11日) 期末总资金 1003370.08
2020-06-12, (MA均线： 12日) 期末总资金 1002183.37
2020-06-12, (MA均线： 13日) 期末总资金 1006154.29
2020-06-12, (MA均线： 14日) 期末总资金 1007900.55
2020-06-12, (MA均线： 15日) 期末总资金 1008421.63
2020-06-12, (MA均线： 16日) 期末总资金 1008708.77
2020-06-12, (MA均线： 17日) 期末总资金 1008734.88
2020-06-12, (MA均线： 18日) 期末总资金 1010371.15
2020-06-12, (MA均线： 19日) 期末总资金 1010186.34
2020-06-12, (MA均线： 20日) 期末总资金 1010201.81
2020-06-12, (MA均线： 21日) 期末总资金 1010782.44
2020-06-12, (MA均线： 22日) 期末总资金 1011271.23
2020-06-12, (MA均线： 23日) 期末总资金 1011711.92
2020-06-12, (MA均线： 24日) 期末总资金 1012475.96
2020-06-12, (MA均线： 25日) 期末总资金 1010726.64
2020-06-12, (MA均线： 26日) 期末总资金 1012502.74
2020-06-12, (MA均线： 27日) 期末总资金 1011219.53
2020-06-12, (MA均线： 28日) 期末总资金 1013569.11
2020-06-12, (MA均线： 29日) 期末总资金 1014176.30
2020-06-12, (MA均线： 30日) 期末总资金 1014076.32
期末总资金: 1014076.32
```
