## [AKShare](https://github.com/jindaxiang/akshare) 策略示例

### 股票策略

#### BackTrader-基本策略

##### 代码

下载和安装 [BackTrader](https://www.backtrader.com/)

```python
from datetime import datetime

import backtrader as bt
import matplotlib.pyplot as plt
import akshare as ak

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

stock_hfq_df = ak.stock_zh_a_daily(symbol="sh600000", adjust="hfq")  # 利用 AkShare 获取后复权数据


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

        :return:
        :rtype:
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
start_date = datetime(2000, 1, 1)  # 回测开始时间
end_date = datetime(2020, 4, 21)  # 回测结束时间
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

#### BackTrader-参数优化

##### 代码

下载和安装 [BackTrader](https://www.backtrader.com/)

```python
import backtrader as bt
import matplotlib.pyplot as plt
import akshare as ak

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


def main(code="sh601318", start_cash=1000000, stake=100, commission_fee=0.001):
    cerebro = bt.Cerebro()  # 创建主控制器
    cerebro.optstrategy(MyStrategy, maperiod=range(3, 31))  # 导入策略参数寻优
    stock_zh_a_daily_df = ak.stock_zh_a_daily(
        symbol=code, adjust="hfq"
    )  # 通过 AkShare 获取需要的数据
    data = bt.feeds.PandasData(dataname=stock_zh_a_daily_df)  # 规范化数据格式
    cerebro.adddata(data)  # 将数据加载至回测系统
    cerebro.broker.setcash(start_cash)  # broker设置资金
    cerebro.broker.setcommission(commission=commission_fee)  # broker手续费
    cerebro.addsizer(bt.sizers.FixedSize, stake=stake)  # 设置买入数量
    print("期初总资金: %.2f" % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)  # 用单核 CPU 做优化
    print("期末总资金: %.2f" % cerebro.broker.getvalue())
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
