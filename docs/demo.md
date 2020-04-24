## [AkShare](https://github.com/jindaxiang/akshare) 策略示例

### 股票策略

#### BackTrader

##### 代码

下载和安装 [BackTrader](https://www.backtrader.com/)

```python
from datetime import datetime

import backtrader as bt
import matplotlib.pyplot as plt
import akshare as ak

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

stock_hfq_df = ak.stock_zh_a_daily(symbol="sh600000", adjust="hfq")  # 利用 AkShare 一行获取复权数据


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
