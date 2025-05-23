# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Base class for modeling portfolio and measuring its performance.

Provides the class `vectorbt.portfolio.base.Portfolio` for modeling portfolio performance
and calculating various risk and performance metrics. It uses Numba-compiled
functions from `vectorbt.portfolio.nb` for most computations and record classes based on
`vectorbt.records.base.Records` for evaluating events such as orders, logs, trades, positions, and drawdowns.

The job of the `Portfolio` class is to create a series of positions allocated 
against a cash component, produce an equity curve, incorporate basic transaction costs
and produce a set of statistics about its performance. In particular, it outputs
position/profit metrics and drawdown information.

Run for the examples below:

```pycon
>>> import numpy as np
>>> import pandas as pd
>>> from datetime import datetime
>>> import talib
>>> from numba import njit

>>> import vectorbt as vbt
>>> from vectorbt.utils.colors import adjust_opacity
>>> from vectorbt.utils.enum_ import map_enum_fields
>>> from vectorbt.base.reshape_fns import broadcast, flex_select_auto_nb, to_2d_array
>>> from vectorbt.portfolio.enums import SizeType, Direction, NoOrder, OrderStatus, OrderSide
>>> from vectorbt.portfolio import nb
```

## Workflow

`Portfolio` class does quite a few things to simulate your strategy.

**Preparation** phase (in the particular class method):

* Receives a set of inputs, such as signal arrays and other parameters
* Resolves parameter defaults by searching for them in the global settings
* Brings input arrays to a single shape
* Does some basic validation of inputs and converts Pandas objects to NumPy arrays
* Passes everything to a Numba-compiled simulation function

**Simulation** phase (in the particular simulation function using Numba):

* The simulation function traverses the broadcasted shape element by element, row by row (time dimension),
    column by column (asset dimension)
* For each asset and timestamp (= element):
    * Gets all available information related to this element and executes the logic
    * Generates an order or skips the element altogether
    * If an order has been issued, processes the order and fills/ignores/rejects it
    * If the order has been filled, registers the result by appending it to the order records
    * Updates the current state such as the cash and asset balances

**Construction** phase (in the particular class method):

* Receives the returned order records and initializes a new `Portfolio` object

**Analysis** phase (in the `Portfolio` object)

* Offers a broad range of risk & performance metrics based on order records

## Simulation modes

There are three main simulation modes.

### From orders

`Portfolio.from_orders` is the most straightforward and the fastest out of all simulation modes.

An order is a simple instruction that contains size, price, fees, and other information
(see `vectorbt.portfolio.enums.Order` for details about what information a typical order requires).
Instead of creating a `vectorbt.portfolio.enums.Order` tuple for each asset and timestamp (which may
waste a lot of memory) and appending it to a (potentially huge) list for processing, `Portfolio.from_orders`
takes each of those information pieces as an array, broadcasts them against each other, and creates a
`vectorbt.portfolio.enums.Order` tuple out of each element for us.

Thanks to broadcasting, we can pass any of the information as a 2-dim array, as a 1-dim array
per column or row, and as a constant. And we don't even need to provide every piece of information -
vectorbt fills the missing data with default constants, without wasting memory.

Here's an example:

```pycon
>>> size = pd.Series([1, -1, 1, -1])  # per row
>>> price = pd.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 3, 2, 1]})  # per element
>>> direction = ['longonly', 'shortonly']  # per column
>>> fees = 0.01  # per frame

>>> pf = vbt.Portfolio.from_orders(price, size, direction=direction, fees=fees)
>>> pf.orders.records_readable
   Order Id Column  Timestamp  Size  Price  Fees  Side
0         0      a          0   1.0    1.0  0.01   Buy
1         1      a          1   1.0    2.0  0.02  Sell
2         2      a          2   1.0    3.0  0.03   Buy
3         3      a          3   1.0    4.0  0.04  Sell
4         4      b          0   1.0    4.0  0.04  Sell
5         5      b          1   1.0    3.0  0.03   Buy
6         6      b          2   1.0    2.0  0.02  Sell
7         7      b          3   1.0    1.0  0.01   Buy
```

This method is particularly useful in situations where you don't need any further logic
apart from filling orders at predefined timestamps. If you want to issue orders depending
upon the previous performance, the current state, or other custom conditions, head over to
`Portfolio.from_signals` or `Portfolio.from_order_func`.

### From signals

`Portfolio.from_signals` is centered around signals. It adds an abstraction layer on top of `Portfolio.from_orders`
to automate some signaling processes. For example, by default, it won't let us execute another entry signal
if we are already in the position. It also implements stop loss and take profit orders for exiting positions.
Nevertheless, this method behaves similarly to `Portfolio.from_orders` and accepts most of its arguments;
in fact, by setting `accumulate=True`, it behaves quite similarly to `Portfolio.from_orders`.

Let's replicate the example above using signals:

```pycon
>>> entries = pd.Series([True, False, True, False])
>>> exits = pd.Series([False, True, False, True])

>>> pf = vbt.Portfolio.from_signals(price, entries, exits, size=1, direction=direction, fees=fees)
>>> pf.orders.records_readable
   Order Id Column  Timestamp  Size  Price  Fees  Side
0         0      a          0   1.0    1.0  0.01   Buy
1         1      a          1   1.0    2.0  0.02  Sell
2         2      a          2   1.0    3.0  0.03   Buy
3         3      a          3   1.0    4.0  0.04  Sell
4         4      b          0   1.0    4.0  0.04  Sell
5         5      b          1   1.0    3.0  0.03   Buy
6         6      b          2   1.0    2.0  0.02  Sell
7         7      b          3   1.0    1.0  0.01   Buy
```

In a nutshell: this method automates some procedures that otherwise would be only possible by using
`Portfolio.from_order_func` while following the same broadcasting principles as `Portfolio.from_orders` -
the best of both worlds, given you can express your strategy as a sequence of signals. But as soon as
your strategy requires any signal to depend upon more complex conditions or to generate multiple orders at once,
it's best to run your custom signaling logic using `Portfolio.from_order_func`.

### From order function

`Portfolio.from_order_func` is the most powerful form of simulation. Instead of pulling information
from predefined arrays, it lets us define an arbitrary logic through callbacks. There are multiple
kinds of callbacks, each called at some point while the simulation function traverses the shape.
For example, apart from the main callback that returns an order (`order_func_nb`), there is a callback
that does preprocessing on the entire group of columns at once. For more details on the general procedure
and the callback zoo, see `vectorbt.portfolio.nb.simulate_nb`.

Let's replicate our example using an order function:

```pycon
>>> @njit
>>> def order_func_nb(c, size, direction, fees):
...     return nb.order_nb(
...         price=c.close[c.i, c.col],
...         size=size[c.i],
...         direction=direction[c.col],
...         fees=fees
... )

>>> direction_num = map_enum_fields(direction, Direction)
>>> pf = vbt.Portfolio.from_order_func(
...     price,
...     order_func_nb,
...     np.asarray(size), np.asarray(direction_num), fees
... )
>>> pf.orders.records_readable
   Order Id Column  Timestamp  Size  Price  Fees  Side
0         0      a          0   1.0    1.0  0.01   Buy
1         1      a          1   1.0    2.0  0.02  Sell
2         2      a          2   1.0    3.0  0.03   Buy
3         3      a          3   1.0    4.0  0.04  Sell
4         4      b          0   1.0    4.0  0.04  Sell
5         5      b          1   1.0    3.0  0.03   Buy
6         6      b          2   1.0    2.0  0.02  Sell
7         7      b          3   1.0    1.0  0.01   Buy
```

There is an even more flexible version available - `vectorbt.portfolio.nb.flex_simulate_nb` (activated by
passing `flexible=True` to `Portfolio.from_order_func`) - that allows creating multiple orders per symbol and bar.

This method has many advantages:

* Realistic simulation as it follows the event-driven approach - less risk of exposure to the look-ahead bias
* Provides a lot of useful information during the runtime, such as the current position's PnL
* Enables putting all logic including custom indicators into a single place, and running it as the data
 comes in, in a memory-friendly manner

But there are drawbacks too:

* Doesn't broadcast arrays - needs to be done by the user prior to the execution
* Requires at least a basic knowledge of NumPy and Numba
* Requires at least an intermediate knowledge of both to optimize for efficiency

## Example

To showcase the features of `Portfolio`, run the following example: it checks candlestick data of 6 major
cryptocurrencies in 2020 against every single pattern found in TA-Lib, and translates them into orders.

```pycon
>>> # Fetch price history
>>> symbols = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'BNB-USD', 'BCH-USD', 'LTC-USD']
>>> start = '2020-01-01 UTC'  # crypto is UTC
>>> end = '2020-09-01 UTC'
>>> # OHLCV by column
>>> ohlcv = vbt.YFData.download(symbols, start=start, end=end).concat()
>>> ohlcv['Open']

symbol                          BTC-USD     ETH-USD   XRP-USD    BNB-USD  \\
Date
2020-01-01 00:00:00+00:00   7194.892090  129.630661  0.192912  13.730962
2020-01-02 00:00:00+00:00   7202.551270  130.820038  0.192708  13.698126
2020-01-03 00:00:00+00:00   6984.428711  127.411263  0.187948  13.035329
...                                 ...         ...       ...        ...
2020-08-30 00:00:00+00:00  11508.713867  399.616699  0.274568  23.009060
2020-08-31 00:00:00+00:00  11713.306641  428.509003  0.283065  23.647858
2020-09-01 00:00:00+00:00  11679.316406  434.874451  0.281612  23.185047

symbol                        BCH-USD    LTC-USD
Date
2020-01-01 00:00:00+00:00  204.671295  41.326534
2020-01-02 00:00:00+00:00  204.354538  42.018085
2020-01-03 00:00:00+00:00  196.007690  39.863129
...                               ...        ...
2020-08-30 00:00:00+00:00  268.842865  57.207737
2020-08-31 00:00:00+00:00  279.280426  62.844059
2020-09-01 00:00:00+00:00  274.480865  61.105076

[244 rows x 6 columns]

>>> # Run every single pattern recognition indicator and combine the results
>>> result = pd.DataFrame.vbt.empty_like(ohlcv['Open'], fill_value=0.)
>>> for pattern in talib.get_function_groups()['Pattern Recognition']:
...     PRecognizer = vbt.IndicatorFactory.from_talib(pattern)
...     pr = PRecognizer.run(ohlcv['Open'], ohlcv['High'], ohlcv['Low'], ohlcv['Close'])
...     result = result + pr.integer

>>> # Don't look into the future
>>> result = result.vbt.fshift(1)

>>> # Treat each number as order value in USD
>>> size = result / ohlcv['Open']

>>> # Simulate portfolio
>>> pf = vbt.Portfolio.from_orders(
...     ohlcv['Close'], size, price=ohlcv['Open'],
...     init_cash='autoalign', fees=0.001, slippage=0.001)

>>> # Visualize portfolio value
>>> pf.value().vbt.plot()
```

![](/assets/images/portfolio_value.svg)

## Broadcasting

`Portfolio` is very flexible towards inputs:

* Accepts both Series and DataFrames as inputs
* Broadcasts inputs to the same shape using vectorbt's own broadcasting rules
* Many inputs (such as `fees`) can be passed as a single value, value per column/row, or as a matrix
* Implements flexible indexing wherever possible to save memory

### Flexible indexing

Instead of expensive broadcasting, most methods keep the original shape and do indexing in a smart way.
A nice feature of this is that it has almost no memory footprint and can broadcast in
any direction indefinitely.

For example, let's broadcast three inputs and select the last element using both approaches:

```pycon
>>> # Classic way
>>> a = np.array([1, 2, 3])
>>> b = np.array([[4], [5], [6]])
>>> c = np.array(10)
>>> a_, b_, c_ = broadcast(a, b, c)

>>> a_
array([[1, 2, 3],
       [1, 2, 3],
       [1, 2, 3]])
>>> a_[2, 2]
3

>>> b_
array([[4, 4, 4],
       [5, 5, 5],
       [6, 6, 6]])
>>> b_[2, 2]
6

>>> c_
array([[10, 10, 10],
       [10, 10, 10],
       [10, 10, 10]])
>>> c_[2, 2]
10

>>> # Flexible indexing being done during simulation
>>> flex_select_auto_nb(a, 2, 2)
3
>>> flex_select_auto_nb(b, 2, 2)
6
>>> flex_select_auto_nb(c, 2, 2)
10
```

## Defaults

If you look at the arguments of each class method, you will notice that most of them default to None.
None has a special meaning in vectorbt: it's a command to pull the default value from the global settings config
- `vectorbt._settings.settings`. The branch for the `Portfolio` can be found under the key 'portfolio'.
For example, the default size used in `Portfolio.from_signals` and `Portfolio.from_orders` is `np.inf`:

```pycon
>>> vbt.settings.portfolio['size']
inf
```

## Grouping

One of the key features of `Portfolio` is the ability to group columns. Groups can be specified by
`group_by`, which can be anything from positions or names of column levels, to a NumPy array with
actual groups. Groups can be formed to share capital between columns (make sure to pass `cash_sharing=True`)
or to compute metrics for a combined portfolio of multiple independent columns.

For example, let's divide our portfolio into two groups sharing the same cash balance:

```pycon
>>> # Simulate combined portfolio
>>> group_by = pd.Index([
...     'first', 'first', 'first',
...     'second', 'second', 'second'
... ], name='group')
>>> comb_pf = vbt.Portfolio.from_orders(
...     ohlcv['Close'], size, price=ohlcv['Open'],
...     init_cash='autoalign', fees=0.001, slippage=0.001,
...     group_by=group_by, cash_sharing=True)

>>> # Get total profit per group
>>> comb_pf.total_profit()
group
first     26221.571200
second    10141.952674
Name: total_profit, dtype: float64
```

Not only can we analyze each group, but also each column in the group:

```pycon
>>> # Get total profit per column
>>> comb_pf.total_profit(group_by=False)
symbol
BTC-USD     5792.120252
ETH-USD    16380.039692
XRP-USD     4049.411256
BNB-USD     6081.253551
BCH-USD      400.573418
LTC-USD     3660.125705
Name: total_profit, dtype: float64
```

In the same way, we can introduce new grouping to the method itself:

```pycon
>>> # Get total profit per group
>>> pf.total_profit(group_by=group_by)
group
first     26221.571200
second    10141.952674
Name: total_profit, dtype: float64
```

!!! note
    If cash sharing is enabled, grouping can be disabled but cannot be modified.

## Indexing

Like any other class subclassing `vectorbt.base.array_wrapper.Wrapping`, we can do pandas indexing
on a `Portfolio` instance, which forwards indexing operation to each object with columns:

```pycon
>>> pf['BTC-USD']
<vectorbt.portfolio.base.Portfolio at 0x7fac7517ac88>

>>> pf['BTC-USD'].total_profit()
5792.120252189081
```

Combined portfolio is indexed by group:

```pycon
>>> comb_pf['first']
<vectorbt.portfolio.base.Portfolio at 0x7fac5756b828>

>>> comb_pf['first'].total_profit()
26221.57120014546
```

!!! note
    Changing index (time axis) is not supported. The object should be treated as a Series
    rather than a DataFrame; for example, use `pf.iloc[0]` instead of `pf.iloc[:, 0]`.

    Indexing behavior depends solely upon `vectorbt.base.array_wrapper.ArrayWrapper`.
    For example, if `group_select` is enabled indexing will be performed on groups,
    otherwise on single columns. You can pass wrapper arguments with `wrapper_kwargs`.

## Logging

To collect more information on how a specific order was processed or to be able to track the whole
simulation from the beginning to the end, we can turn on logging:

```pycon
>>> # Simulate portfolio with logging
>>> pf = vbt.Portfolio.from_orders(
...     ohlcv['Close'], size, price=ohlcv['Open'],
...     init_cash='autoalign', fees=0.001, slippage=0.001, log=True)

>>> pf.logs.records
        id  group  col  idx  cash    position  debt  free_cash    val_price  \\
0        0      0    0    0   inf    0.000000   0.0        inf  7194.892090
1        1      0    0    1   inf    0.000000   0.0        inf  7202.551270
2        2      0    0    2   inf    0.000000   0.0        inf  6984.428711
...    ...    ...  ...  ...   ...         ...   ...        ...          ...
1461  1461      5    5  241   inf  272.389644   0.0        inf    57.207737
1462  1462      5    5  242   inf  274.137659   0.0        inf    62.844059
1463  1463      5    5  243   inf  282.093860   0.0        inf    61.105076

      value  ...  new_free_cash  new_val_price  new_value  res_size  \\
0       inf  ...            inf    7194.892090        inf       NaN
1       inf  ...            inf    7202.551270        inf       NaN
2       inf  ...            inf    6984.428711        inf       NaN
...     ...  ...            ...            ...        ...       ...
1461    inf  ...            inf      57.207737        inf  1.748015
1462    inf  ...            inf      62.844059        inf  7.956202
1463    inf  ...            inf      61.105076        inf  1.636525

        res_price  res_fees  res_side  res_status  res_status_info  order_id
0             NaN       NaN        -1           1                0        -1
1             NaN       NaN        -1           1                5        -1
2             NaN       NaN        -1           1                5        -1
...           ...       ...       ...         ...              ...       ...
1461    57.264945    0.1001         0           0               -1      1070
1462    62.906903    0.5005         0           0               -1      1071
1463    61.043971    0.0999         1           0               -1      1072

[1464 rows x 37 columns]
```

Just as orders, logs are also records and thus can be easily analyzed:

```pycon
>>> pf.logs.res_status.value_counts()
symbol   BTC-USD  ETH-USD  XRP-USD  BNB-USD  BCH-USD  LTC-USD
Filled       184      172      177      178      177      185
Ignored       60       72       67       66       67       59
```

Logging can also be turned on just for one order, row, or column, since as many other
variables it's specified per order and can broadcast automatically.

!!! note
    Logging can slow down simulation.

## Caching

`Portfolio` heavily relies upon caching. If a method or a property requires heavy computation,
it's wrapped with `vectorbt.utils.decorators.cached_method` and `vectorbt.utils.decorators.cached_property`
respectively. Caching can be disabled globally via `caching` in `vectorbt._settings.settings`.

!!! note
    Because of caching, class is meant to be immutable and all properties are read-only.
    To change any attribute, use the `copy` method and pass the attribute as keyword argument.

Alternatively, we can precisely point at attributes and methods that should or shouldn't
be cached. For example, we can blacklist the entire `Portfolio` class except a few most called
methods such as `Portfolio.cash_flow` and `Portfolio.asset_flow`:

```pycon
>>> vbt.settings.caching['blacklist'].append(
...     vbt.CacheCondition(base_cls='Portfolio')
... )
>>> vbt.settings.caching['whitelist'].extend([
...     vbt.CacheCondition(base_cls='Portfolio', func='cash_flow'),
...     vbt.CacheCondition(base_cls='Portfolio', func='asset_flow')
... ])
```

Define rules for one instance of `Portfolio`:

```pycon
>>> vbt.settings.caching['blacklist'].append(
...     vbt.CacheCondition(instance=pf)
... )
>>> vbt.settings.caching['whitelist'].extend([
...     vbt.CacheCondition(instance=pf, func='cash_flow'),
...     vbt.CacheCondition(instance=pf, func='asset_flow')
... ])
```

See `vectorbt.utils.decorators.should_cache` for caching rules.

To reset caching:

```pycon
>>> vbt.settings.caching.reset()
```

## Performance and memory

If you're running out of memory when working with large arrays, make sure to disable caching
and then store most important time series manually. For example, if you're interested in Sharpe
ratio or other metrics based on returns, run and save `Portfolio.returns` in a variable and then use the
`vectorbt.returns.accessors.ReturnsAccessor` to analyze them. Do not use methods akin to
`Portfolio.sharpe_ratio` because they will re-calculate returns each time.

Alternatively, you can track portfolio value and returns using `Portfolio.from_order_func` and its callbacks
(preferably in `post_segment_func_nb`):

```pycon
>>> pf_baseline = vbt.Portfolio.from_orders(
...     ohlcv['Close'], size, price=ohlcv['Open'],
...     init_cash='autoalign', fees=0.001, slippage=0.001, freq='d')
>>> pf_baseline.sharpe_ratio()
symbol
BTC-USD    1.743437
ETH-USD    2.800903
XRP-USD    1.607904
BNB-USD    1.805373
BCH-USD    0.269392
LTC-USD    1.040494
Name: sharpe_ratio, dtype: float64

>>> @njit
... def order_func_nb(c, size, price, fees, slippage):
...     return nb.order_nb(
...         size=nb.get_elem_nb(c, size),
...         price=nb.get_elem_nb(c, price),
...         fees=nb.get_elem_nb(c, fees),
...         slippage=nb.get_elem_nb(c, slippage),
...     )

>>> @njit
... def post_segment_func_nb(c, returns_out):
...     returns_out[c.i, c.group] = c.last_return[c.group]

>>> returns_out = np.empty_like(ohlcv['Close'], dtype=np.float64)
>>> pf = vbt.Portfolio.from_order_func(
...     ohlcv['Close'],
...     order_func_nb,
...     np.asarray(size),
...     np.asarray(ohlcv['Open']),
...     np.asarray(0.001),
...     np.asarray(0.001),
...     post_segment_func_nb=post_segment_func_nb,
...     post_segment_args=(returns_out,),
...     init_cash=pf_baseline.init_cash
... )

>>> returns = pf.wrapper.wrap(returns_out)
>>> del pf
>>> returns.vbt.returns(freq='d').sharpe_ratio()
symbol
BTC-USD   -2.261443
ETH-USD    0.059538
XRP-USD    2.159093
BNB-USD    1.555386
BCH-USD    0.784214
LTC-USD    1.460077
Name: sharpe_ratio, dtype: float64
```

The only drawback of this approach is that you cannot use `init_cash='auto'` or `init_cash='autoalign'`
because then, during the simulation, the portfolio value is `np.inf` and the returns are `np.nan`.

## Saving and loading

Like any other class subclassing `vectorbt.utils.config.Pickleable`, we can save a `Portfolio`
instance to the disk with `Portfolio.save` and load it with `Portfolio.load`:

```pycon
>>> pf = vbt.Portfolio.from_orders(
...     ohlcv['Close'], size, price=ohlcv['Open'],
...     init_cash='autoalign', fees=0.001, slippage=0.001, freq='d')
>>> pf.sharpe_ratio()
symbol
BTC-USD    1.743437
ETH-USD    2.800903
XRP-USD    1.607904
BNB-USD    1.805373
BCH-USD    0.269392
LTC-USD    1.040494
Name: sharpe_ratio, dtype: float64

>>> pf.save('my_pf')
>>> pf = vbt.Portfolio.load('my_pf')
>>> pf.sharpe_ratio()
symbol
BTC-USD    1.743437
ETH-USD    2.800903
XRP-USD    1.607904
BNB-USD    1.805373
BCH-USD    0.269392
LTC-USD    1.040494
Name: sharpe_ratio, dtype: float64
```

!!! note
    Save files won't include neither cached results nor global defaults. For example,
    passing `fillna_close` as None will also use None when the portfolio is loaded from disk.
    Make sure to either pass all arguments explicitly or to also save the `vectorbt._settings.settings` config.

## Stats

!!! hint
    See `vectorbt.generic.stats_builder.StatsBuilderMixin.stats` and `Portfolio.metrics`.

Let's simulate a portfolio with two columns:

```pycon
>>> close = vbt.YFData.download(
...     "BTC-USD",
...     start='2020-01-01 UTC',
...     end='2020-09-01 UTC'
... ).get('Close')

>>> pf = vbt.Portfolio.from_random_signals(close, n=[10, 20], seed=42)
>>> pf.wrapper.columns
Index([10, 20], dtype='int64', name='rand_n')
```

### Column, group, and tag selection

To return the statistics for a particular column/group, use the `column` argument:

```pycon
>>> pf.stats(column=10)
UserWarning: Metric 'sharpe_ratio' requires frequency to be set
UserWarning: Metric 'calmar_ratio' requires frequency to be set
UserWarning: Metric 'omega_ratio' requires frequency to be set
UserWarning: Metric 'sortino_ratio' requires frequency to be set

Start                         2020-01-01 00:00:00+00:00
End                           2020-09-01 00:00:00+00:00
Period                                              244
Start Value                                       100.0
End Value                                    106.721585
Total Return [%]                               6.721585
Benchmark Return [%]                          66.252621
Max Gross Exposure [%]                            100.0
Total Fees Paid                                     0.0
Max Drawdown [%]                              22.190944
Max Drawdown Duration                             101.0
Total Trades                                         10
Total Closed Trades                                  10
Total Open Trades                                     0
Open Trade PnL                                      0.0
Win Rate [%]                                       60.0
Best Trade [%]                                 15.31962
Worst Trade [%]                               -9.904223
Avg Winning Trade [%]                          4.671959
Avg Losing Trade [%]                          -4.851205
Avg Winning Trade Duration                    11.333333
Avg Losing Trade Duration                         14.25
Profit Factor                                  1.347457
Expectancy                                     0.672158
Name: 10, dtype: object
```

If vectorbt couldn't parse the frequency of `close`:

1) it won't return any duration in time units,
2) it won't return any metric that requires annualization, and
3) it will throw a bunch of warnings (you can silence those by passing `silence_warnings=True`)

We can provide the frequency as part of the settings dict:

```pycon
>>> pf.stats(column=10, settings=dict(freq='d'))
UserWarning: Changing the frequency will create a copy of this object.
Consider setting the frequency upon object creation to re-use existing cache.

Start                         2020-01-01 00:00:00+00:00
End                           2020-09-01 00:00:00+00:00
Period                                244 days 00:00:00
Start Value                                       100.0
End Value                                    106.721585
Total Return [%]                               6.721585
Benchmark Return [%]                          66.252621
Max Gross Exposure [%]                            100.0
Total Fees Paid                                     0.0
Max Drawdown [%]                              22.190944
Max Drawdown Duration                 101 days 00:00:00
Total Trades                                         10
Total Closed Trades                                  10
Total Open Trades                                     0
Open Trade PnL                                      0.0
Win Rate [%]                                       60.0
Best Trade [%]                                 15.31962
Worst Trade [%]                               -9.904223
Avg Winning Trade [%]                          4.671959
Avg Losing Trade [%]                          -4.851205
Avg Winning Trade Duration             11 days 08:00:00
Avg Losing Trade Duration              14 days 06:00:00
Profit Factor                                  1.347457
Expectancy                                     0.672158
Sharpe Ratio                                   0.445231
Calmar Ratio                                   0.460573
Omega Ratio                                    1.099192
Sortino Ratio                                  0.706986
Name: 10, dtype: object
```

But in this case, our portfolio will be copied to set the new frequency and we wouldn't be
able to re-use its cached attributes. Let's define the frequency upon the simulation instead:

```pycon
>>> pf = vbt.Portfolio.from_random_signals(close, n=[10, 20], seed=42, freq='d')
```

We can change the grouping of the portfolio on the fly. Let's form a single group:

```pycon
>>> pf.stats(group_by=True)
Start                         2020-01-01 00:00:00+00:00
End                           2020-09-01 00:00:00+00:00
Period                                244 days 00:00:00
Start Value                                       200.0
End Value                                     277.49299
Total Return [%]                              38.746495
Benchmark Return [%]                          66.252621
Max Gross Exposure [%]                            100.0
Total Fees Paid                                     0.0
Max Drawdown [%]                              14.219327
Max Drawdown Duration                  86 days 00:00:00
Total Trades                                         30
Total Closed Trades                                  30
Total Open Trades                                     0
Open Trade PnL                                      0.0
Win Rate [%]                                  66.666667
Best Trade [%]                                18.332559
Worst Trade [%]                               -9.904223
Avg Winning Trade [%]                          5.754788
Avg Losing Trade [%]                          -4.718907
Avg Winning Trade Duration              7 days 19:12:00
Avg Losing Trade Duration               8 days 07:12:00
Profit Factor                                  2.427948
Expectancy                                       2.5831
Sharpe Ratio                                    1.57907
Calmar Ratio                                   4.445448
Omega Ratio                                    1.334032
Sortino Ratio                                   2.59669
Name: group, dtype: object
```

We can see how the initial cash has changed from $100 to $200, indicating that both columns now
contribute to the performance.

### Aggregation

If the portfolio consists of multiple columns/groups and no column/group has been selected,
each metric is aggregated across all columns/groups based on `agg_func`, which is `np.mean` by default.

```pycon
>>> pf.stats()
UserWarning: Object has multiple columns. Aggregating using <function mean at 0x7fc77152bb70>.
Pass column to select a single column/group.

Start                         2020-01-01 00:00:00+00:00
End                           2020-09-01 00:00:00+00:00
Period                                244 days 00:00:00
Start Value                                       100.0
End Value                                    138.746495
Total Return [%]                              38.746495
Benchmark Return [%]                          66.252621
Max Gross Exposure [%]                            100.0
Total Fees Paid                                     0.0
Max Drawdown [%]                               20.35869
Max Drawdown Duration                  93 days 00:00:00
Total Trades                                       15.0
Total Closed Trades                                15.0
Total Open Trades                                   0.0
Open Trade PnL                                      0.0
Win Rate [%]                                       65.0
Best Trade [%]                                 16.82609
Worst Trade [%]                               -9.701273
Avg Winning Trade [%]                          5.445408
Avg Losing Trade [%]                          -4.740956
Avg Winning Trade Duration    8 days 19:25:42.857142857
Avg Losing Trade Duration               9 days 07:00:00
Profit Factor                                  2.186957
Expectancy                                     2.105364
Sharpe Ratio                                   1.165695
Calmar Ratio                                   3.541079
Omega Ratio                                    1.331624
Sortino Ratio                                  2.084565
Name: agg_func_mean, dtype: object
```

Here, the Sharpe ratio of 0.445231 (column=10) and 1.88616 (column=20) lead to the avarage of 1.16569.

We can also return a DataFrame with statistics per column/group by passing `agg_func=None`:

```pycon
>>> pf.stats(agg_func=None)
                           Start                       End   Period  ...  Sortino Ratio
rand_n                                                               ...
10     2020-01-01 00:00:00+00:00 2020-09-01 00:00:00+00:00 244 days  ...       0.706986
20     2020-01-01 00:00:00+00:00 2020-09-01 00:00:00+00:00 244 days  ...       3.462144

[2 rows x 25 columns]
```

### Metric selection

To select metrics, use the `metrics` argument (see `Portfolio.metrics` for supported metrics):

```pycon
>>> pf.stats(metrics=['sharpe_ratio', 'sortino_ratio'], column=10)
Sharpe Ratio     0.445231
Sortino Ratio    0.706986
Name: 10, dtype: float64
```

We can also select specific tags (see any metric from `Portfolio.metrics` that has the `tag` key):

```pycon
>>> pf.stats(column=10, tags=['trades'])
Total Trades                                10
Total Open Trades                            0
Open Trade PnL                               0
Long Trades [%]                            100
Win Rate [%]                                60
Best Trade [%]                         15.3196
Worst Trade [%]                       -9.90422
Avg Winning Trade [%]                  4.67196
Avg Winning Trade Duration    11 days 08:00:00
Avg Losing Trade [%]                   -4.8512
Avg Losing Trade Duration     14 days 06:00:00
Profit Factor                          1.34746
Expectancy                            0.672158
Name: 10, dtype: object
```

Or provide a boolean expression:

```pycon
>>> pf.stats(column=10, tags='trades and open and not closed')
Total Open Trades    0.0
Open Trade PnL       0.0
Name: 10, dtype: float64
```

The reason why we included "not closed" along with "open" is because some metrics such as the win rate
have both tags attached since they are based upon both open and closed trades/positions
(to see this, pass `settings=dict(incl_open=True)` and `tags='trades and open'`).

### Passing parameters

We can use `settings` to pass parameters used across multiple metrics.
For example, let's pass required and risk-free return to all return metrics:

```pycon
>>> pf.stats(column=10, settings=dict(required_return=0.1, risk_free=0.01))
Start                         2020-01-01 00:00:00+00:00
End                           2020-09-01 00:00:00+00:00
Period                                244 days 00:00:00
Start Value                                       100.0
End Value                                    106.721585
Total Return [%]                               6.721585
Benchmark Return [%]                          66.252621
Max Gross Exposure [%]                            100.0
Total Fees Paid                                     0.0
Max Drawdown [%]                              22.190944
Max Drawdown Duration                 101 days 00:00:00
Total Trades                                         10
Total Closed Trades                                  10
Total Open Trades                                     0
Open Trade PnL                                      0.0
Win Rate [%]                                       60.0
Best Trade [%]                                 15.31962
Worst Trade [%]                               -9.904223
Avg Winning Trade [%]                          4.671959
Avg Losing Trade [%]                          -4.851205
Avg Winning Trade Duration             11 days 08:00:00
Avg Losing Trade Duration              14 days 06:00:00
Profit Factor                                  1.347457
Expectancy                                     0.672158
Sharpe Ratio                                  -9.504742  << here
Calmar Ratio                                   0.460573  << here
Omega Ratio                                    0.233279  << here
Sortino Ratio                                -18.763407  << here
Name: 10, dtype: object
```

Passing any argument inside of `settings` either overrides an existing default, or acts as
an optional argument that is passed to the calculation function upon resolution (see below).
Both `required_return` and `risk_free` can be found in the signature of the 4 ratio methods,
so vectorbt knows exactly it has to pass them.

Let's imagine that the signature of `vectorbt.returns.accessors.ReturnsAccessor.sharpe_ratio`
doesn't list those arguments: vectorbt would simply call this method without passing those two arguments.
In such case, we have two options:

1) Set parameters globally using `settings` and set `pass_{arg}=True` individually using `metric_settings`:

```pycon
>>> pf.stats(
...     column=10,
...     settings=dict(required_return=0.1, risk_free=0.01),
...     metric_settings=dict(
...         sharpe_ratio=dict(pass_risk_free=True),
...         omega_ratio=dict(pass_required_return=True, pass_risk_free=True),
...         sortino_ratio=dict(pass_required_return=True)
...     )
... )
```

2) Set parameters individually using `metric_settings`:

```pycon
>>> pf.stats(
...     column=10,
...     metric_settings=dict(
...         sharpe_ratio=dict(risk_free=0.01),
...         omega_ratio=dict(required_return=0.1, risk_free=0.01),
...         sortino_ratio=dict(required_return=0.1)
...     )
... )
```

### Custom metrics

To calculate a custom metric, we need to provide at least two things: short name and a settings
dict with the title and calculation function (see arguments in `vectorbt.generic.stats_builder.StatsBuilderMixin`):

```pycon
>>> max_winning_streak = (
...     'max_winning_streak',
...     dict(
...         title='Max Winning Streak',
...         calc_func=lambda trades: trades.winning_streak.max(),
...         resolve_trades=True
...     )
... )
>>> pf.stats(metrics=max_winning_streak, column=10)
Max Winning Streak    3.0
Name: 10, dtype: float64
```

You might wonder how vectorbt knows which arguments to pass to `calc_func`?
In the example above, the calculation function expects two arguments: `trades` and `group_by`.
To automatically pass any of the them, vectorbt searches for each in the current settings.
As `trades` cannot be found, it either throws an error or tries to resolve this argument if
`resolve_{arg}=True` was passed. Argument resolution is the process of searching for property/method with
the same name (also with prefix `get_`) in the attributes of the current portfolio, automatically passing the
current settings such as `group_by` if they are present in the method's signature
(a similar resolution procedure), and calling the method/property. The result of the resolution
process is then passed as `arg` (or `trades` in our example).

Here's an example without resolution of arguments:

```pycon
>>> max_winning_streak = (
...     'max_winning_streak',
...     dict(
...         title='Max Winning Streak',
...         calc_func=lambda self, group_by:
...         self.get_trades(group_by=group_by).winning_streak.max()
...     )
... )
>>> pf.stats(metrics=max_winning_streak, column=10)
Max Winning Streak    3.0
Name: 10, dtype: float64
```

And here's an example without resolution of the calculation function:

```pycon
>>> max_winning_streak = (
...     'max_winning_streak',
...     dict(
...         title='Max Winning Streak',
...         calc_func=lambda self, settings:
...         self.get_trades(group_by=settings['group_by']).winning_streak.max(),
...         resolve_calc_func=False
...     )
... )
>>> pf.stats(metrics=max_winning_streak, column=10)
Max Winning Streak    3.0
Name: 10, dtype: float64
```

Since `max_winning_streak` method can be expressed as a path from this portfolio, we can simply write:

```pycon
>>> max_winning_streak = (
...     'max_winning_streak',
...     dict(
...         title='Max Winning Streak',
...         calc_func='trades.winning_streak.max'
...     )
... )
```

In this case, we don't have to pass `resolve_trades=True` any more as vectorbt does it automatically.
Another advantage is that vectorbt can access the signature of the last method in the path
(`vectorbt.records.mapped_array.MappedArray.max` in our case) and resolve its arguments.

To switch between entry trades, exit trades, and positions, use the `trades_type` setting.
Additionally, you can pass `incl_open=True` to also include open trades.

```pycon
>>> pf.stats(column=10, settings=dict(trades_type='positions', incl_open=True))
Start                         2020-01-01 00:00:00+00:00
End                           2020-09-01 00:00:00+00:00
Period                                244 days 00:00:00
Start Value                                       100.0
End Value                                    106.721585
Total Return [%]                               6.721585
Benchmark Return [%]                          66.252621
Max Gross Exposure [%]                            100.0
Total Fees Paid                                     0.0
Max Drawdown [%]                              22.190944
Max Drawdown Duration                 100 days 00:00:00
Total Trades                                         10
Total Closed Trades                                  10
Total Open Trades                                     0
Open Trade PnL                                      0.0
Win Rate [%]                                       60.0
Best Trade [%]                                 15.31962
Worst Trade [%]                               -9.904223
Avg Winning Trade [%]                          4.671959
Avg Losing Trade [%]                          -4.851205
Avg Winning Trade Duration             11 days 08:00:00
Avg Losing Trade Duration              14 days 06:00:00
Profit Factor                                  1.347457
Expectancy                                     0.672158
Sharpe Ratio                                   0.445231
Calmar Ratio                                   0.460573
Omega Ratio                                    1.099192
Sortino Ratio                                  0.706986
Name: 10, dtype: object
```

Any default metric setting or even global setting can be overridden by the user using metric-specific
keyword arguments. Here, we override the global aggregation function for `max_dd_duration`:

```pycon
>>> pf.stats(agg_func=lambda sr: sr.mean(),
...     metric_settings=dict(
...         max_dd_duration=dict(agg_func=lambda sr: sr.max())
...     )
... )
UserWarning: Object has multiple columns. Aggregating using <function <lambda> at 0x7fbf6e77b268>.
Pass column to select a single column/group.

Start                         2020-01-01 00:00:00+00:00
End                           2020-09-01 00:00:00+00:00
Period                                244 days 00:00:00
Start Value                                       100.0
End Value                                    138.746495
Total Return [%]                              38.746495
Benchmark Return [%]                          66.252621
Max Gross Exposure [%]                            100.0
Total Fees Paid                                     0.0
Max Drawdown [%]                               20.35869
Max Drawdown Duration                 101 days 00:00:00  << here
Total Trades                                       15.0
Total Closed Trades                                15.0
Total Open Trades                                   0.0
Open Trade PnL                                      0.0
Win Rate [%]                                       65.0
Best Trade [%]                                 16.82609
Worst Trade [%]                               -9.701273
Avg Winning Trade [%]                          5.445408
Avg Losing Trade [%]                          -4.740956
Avg Winning Trade Duration    8 days 19:25:42.857142857
Avg Losing Trade Duration               9 days 07:00:00
Profit Factor                                  2.186957
Expectancy                                     2.105364
Sharpe Ratio                                   1.165695
Calmar Ratio                                   3.541079
Omega Ratio                                    1.331624
Sortino Ratio                                  2.084565
Name: agg_func_<lambda>, dtype: object
```

Let's create a simple metric that returns a passed value to demonstrate how vectorbt overrides settings,
from least to most important:

```pycon
>>> # vbt.settings.portfolio.stats
>>> vbt.settings.portfolio.stats['settings']['my_arg'] = 100
>>> my_arg_metric = ('my_arg_metric', dict(title='My Arg', calc_func=lambda my_arg: my_arg))
>>> pf.stats(my_arg_metric, column=10)
My Arg    100
Name: 10, dtype: int64

>>> # settings >>> vbt.settings.portfolio.stats
>>> pf.stats(my_arg_metric, column=10, settings=dict(my_arg=200))
My Arg    200
Name: 10, dtype: int64

>>> # metric settings >>> settings
>>> my_arg_metric = ('my_arg_metric', dict(title='My Arg', my_arg=300, calc_func=lambda my_arg: my_arg))
>>> pf.stats(my_arg_metric, column=10, settings=dict(my_arg=200))
My Arg    300
Name: 10, dtype: int64

>>> # metric_settings >>> metric settings
>>> pf.stats(my_arg_metric, column=10, settings=dict(my_arg=200),
...     metric_settings=dict(my_arg_metric=dict(my_arg=400)))
My Arg    400
Name: 10, dtype: int64
```

Here's an example of a parametrized metric. Let's get the number of trades with PnL over some amount:

```pycon
>>> trade_min_pnl_cnt = (
...     'trade_min_pnl_cnt',
...     dict(
...         title=vbt.Sub('Trades with PnL over $$${min_pnl}'),
...         calc_func=lambda trades, min_pnl: trades.apply_mask(
...             trades.pnl.values >= min_pnl).count(),
...         resolve_trades=True
...     )
... )
>>> pf.stats(
...     metrics=trade_min_pnl_cnt, column=10,
...     metric_settings=dict(trade_min_pnl_cnt=dict(min_pnl=0)))
Trades with PnL over $0    6
Name: stats, dtype: int64

>>> pf.stats(
...     metrics=trade_min_pnl_cnt, column=10,
...     metric_settings=dict(trade_min_pnl_cnt=dict(min_pnl=10)))
Trades with PnL over $10    1
Name: stats, dtype: int64
```

If the same metric name was encountered more than once, vectorbt automatically appends an
underscore and its position, so we can pass keyword arguments to each metric separately:

```pycon
>>> pf.stats(
...     metrics=[
...         trade_min_pnl_cnt,
...         trade_min_pnl_cnt,
...         trade_min_pnl_cnt
...     ],
...     column=10,
...     metric_settings=dict(
...         trade_min_pnl_cnt_0=dict(min_pnl=0),
...         trade_min_pnl_cnt_1=dict(min_pnl=10),
...         trade_min_pnl_cnt_2=dict(min_pnl=20))
...     )
Trades with PnL over $0     6
Trades with PnL over $10    1
Trades with PnL over $20    0
Name: stats, dtype: int64
```

To add a custom metric to the list of all metrics, we have three options.

The first option is to change the `Portfolio.metrics` dict in-place (this will append to the end):

```pycon
>>> pf.metrics['max_winning_streak'] = max_winning_streak[1]
>>> pf.stats(column=10)
Start                         2020-01-01 00:00:00+00:00
End                           2020-09-01 00:00:00+00:00
Period                                244 days 00:00:00
Start Value                                       100.0
End Value                                    106.721585
Total Return [%]                               6.721585
Benchmark Return [%]                          66.252621
Max Gross Exposure [%]                            100.0
Total Fees Paid                                     0.0
Max Drawdown [%]                              22.190944
Max Drawdown Duration                 101 days 00:00:00
Total Trades                                         10
Total Closed Trades                                  10
Total Open Trades                                     0
Open Trade PnL                                      0.0
Win Rate [%]                                       60.0
Best Trade [%]                                 15.31962
Worst Trade [%]                               -9.904223
Avg Winning Trade [%]                          4.671959
Avg Losing Trade [%]                          -4.851205
Avg Winning Trade Duration             11 days 08:00:00
Avg Losing Trade Duration              14 days 06:00:00
Profit Factor                                  1.347457
Expectancy                                     0.672158
Sharpe Ratio                                   0.445231
Calmar Ratio                                   0.460573
Omega Ratio                                    1.099192
Sortino Ratio                                  0.706986
Max Winning Streak                                  3.0  << here
Name: 10, dtype: object
```

Since `Portfolio.metrics` is of type `vectorbt.utils.config.Config`, we can reset it at any time
to get default metrics:

```pycon
>>> pf.metrics.reset()
```

The second option is to copy `Portfolio.metrics`, append our metric, and pass as `metrics` argument:

```pycon
>>> my_metrics = list(pf.metrics.items()) + [max_winning_streak]
>>> pf.stats(metrics=my_metrics, column=10)
```

The third option is to set `metrics` globally under `portfolio.stats` in `vectorbt._settings.settings`.

```pycon
>>> vbt.settings.portfolio['stats']['metrics'] = my_metrics
>>> pf.stats(column=10)
```

## Returns stats

We can compute the stats solely based on the portfolio's returns using `Portfolio.returns_stats`,
which calls `vectorbt.returns.accessors.ReturnsAccessor.stats`.

```pycon
>>> pf.returns_stats(column=10)
Start                        2020-01-01 00:00:00+00:00
End                          2020-09-01 00:00:00+00:00
Period                               244 days 00:00:00
Total Return [%]                              6.721585
Benchmark Return [%]                         66.252621
Annualized Return [%]                         10.22056
Annualized Volatility [%]                    36.683518
Max Drawdown [%]                             22.190944
Max Drawdown Duration                100 days 00:00:00
Sharpe Ratio                                  0.445231
Calmar Ratio                                  0.460573
Omega Ratio                                   1.099192
Sortino Ratio                                 0.706986
Skew                                          1.328259
Kurtosis                                      10.80246
Tail Ratio                                    1.057913
Common Sense Ratio                            1.166037
Value at Risk                                -0.031011
Alpha                                        -0.075109
Beta                                          0.220351
Name: 10, dtype: object
```

Most metrics defined in `vectorbt.returns.accessors.ReturnsAccessor` are also available
as attributes of `Portfolio`:

```pycon
>>> pf.sharpe_ratio()
randnx_n
10    0.445231
20    1.886158
Name: sharpe_ratio, dtype: float64
```

Moreover, we can access quantstats functions using `vectorbt.returns.qs_adapter.QSAdapter`:

```pycon
>>> pf.qs.sharpe()
randnx_n
10    0.445231
20    1.886158
dtype: float64

>>> pf[10].qs.plot_snapshot()
```

![](/assets/images/portfolio_plot_snapshot.png)

## Plots

!!! hint
    See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots`.

    The features implemented in this method are very similar to `Portfolio.stats`.
    See also the examples under `Portfolio.stats`.

Plot portfolio of a random strategy:

```pycon
>>> pf.plot(column=10)
```

![](/assets/images/portfolio_plot.svg)

You can choose any of the subplots in `Portfolio.subplots`, in any order, and
control their appearance using keyword arguments:

```pycon
>>> pf.plot(
...     subplots=['drawdowns', 'underwater'],
...     column=10,
...     subplot_settings=dict(
...         drawdowns=dict(top_n=3),
...         underwater=dict(
...             trace_kwargs=dict(
...                 line=dict(color='#FF6F00'),
...                 fillcolor=adjust_opacity('#FF6F00', 0.3)
...             )
...         )
...     )
... )
```

![](/assets/images/portfolio_plot_drawdowns.svg)

To create a new subplot, a preferred way is to pass a plotting function:

```pycon
>>> def plot_order_size(pf, size, column=None, add_trace_kwargs=None, fig=None):
...     size = pf.select_one_from_obj(size, pf.wrapper.regroup(False), column=column)
...     size.rename('Order Size').vbt.barplot(
...         add_trace_kwargs=add_trace_kwargs, fig=fig)

>>> order_size = pf.orders.size.to_pd(fill_value=0.)
>>> pf.plot(subplots=[
...     'orders',
...     ('order_size', dict(
...         title='Order Size',
...         yaxis_kwargs=dict(title='Order size'),
...         check_is_not_grouped=True,
...         plot_func=plot_order_size
...     ))
... ],
...     column=10,
...     subplot_settings=dict(
...         order_size=dict(
...             size=order_size
...         )
...     )
... )
```

Alternatively, you can create a placeholder and overwrite it manually later:

```pycon
>>> fig = pf.plot(subplots=[
...     'orders',
...     ('order_size', dict(
...         title='Order Size',
...         yaxis_kwargs=dict(title='Order size'),
...         check_is_not_grouped=True
...     ))  # placeholder
... ], column=10)
>>> order_size[10].rename('Order Size').vbt.barplot(
...     add_trace_kwargs=dict(row=2, col=1),
...     fig=fig
... )
```

![](/assets/images/portfolio_plot_custom.svg)

If a plotting function can in any way be accessed from the current portfolio, you can pass
the path to this function (see `vectorbt.utils.attr_.deep_getattr` for the path format).
You can additionally use templates to make some parameters to depend upon passed keyword arguments:

```pycon
>>> subplots = [
...     ('cumulative_returns', dict(
...         title='Cumulative Returns',
...         yaxis_kwargs=dict(title='Cumulative returns'),
...         plot_func='returns.vbt.returns.cumulative.vbt.plot',
...         pass_add_trace_kwargs=True
...     )),
...     ('rolling_drawdown', dict(
...         title='Rolling Drawdown',
...         yaxis_kwargs=dict(title='Rolling drawdown'),
...         plot_func=[
...             'returns.vbt.returns',  # returns accessor
...             (
...                 'rolling_max_drawdown',  # function name
...                 (vbt.Rep('window'),)),  # positional arguments
...             'vbt.plot'  # plotting function
...         ],
...         pass_add_trace_kwargs=True,
...         trace_names=[vbt.Sub('rolling_drawdown(${window})')],  # add window to the trace name
...     ))
... ]
>>> pf.plot(
...     subplots,
...     column=10,
...     subplot_settings=dict(
...         rolling_drawdown=dict(
...             template_mapping=dict(
...                 window=10
...             )
...         )
...     )
... )
```

You can also replace templates across all subplots by using the global template mapping:

```pycon
>>> pf.plot(subplots, column=10, template_mapping=dict(window=10))
```

![](/assets/images/portfolio_plot_path.svg)
"""
import warnings

import numpy as np
import pandas as pd

from vectorbt import _typing as tp
from vectorbt.base.array_wrapper import ArrayWrapper, Wrapping
from vectorbt.base.reshape_fns import to_1d_array, to_2d_array, broadcast, broadcast_to, to_pd_array
from vectorbt.generic.drawdowns import Drawdowns
from vectorbt.generic.plots_builder import PlotsBuilderMixin
from vectorbt.generic.stats_builder import StatsBuilderMixin
from vectorbt.portfolio import nb
from vectorbt.portfolio.decorators import attach_returns_acc_methods
from vectorbt.portfolio.enums import *
from vectorbt.portfolio.logs import Logs
from vectorbt.portfolio.orders import Orders
from vectorbt.portfolio.trades import Trades, EntryTrades, ExitTrades, Positions
from vectorbt.returns import nb as returns_nb
from vectorbt.returns.accessors import ReturnsAccessor
from vectorbt.signals.generators import RANDNX, RPROBNX
from vectorbt.utils import checks
from vectorbt.utils.colors import adjust_opacity
from vectorbt.utils.config import merge_dicts, Config
from vectorbt.utils.decorators import cached_property, cached_method
from vectorbt.utils.enum_ import map_enum_fields
from vectorbt.utils.figure import get_domain
from vectorbt.utils.random_ import set_seed
from vectorbt.utils.template import RepEval, deep_substitute

try:
    import quantstats as qs
except ImportError:
    QSAdapterT = tp.Any
else:
    from vectorbt.returns.qs_adapter import QSAdapter as QSAdapterT

__pdoc__ = {}

returns_acc_config = Config(
    {
        'daily_returns': dict(source_name='daily'),
        'annual_returns': dict(source_name='annual'),
        'cumulative_returns': dict(source_name='cumulative'),
        'annualized_return': dict(source_name='annualized'),
        'annualized_volatility': dict(),
        'calmar_ratio': dict(),
        'omega_ratio': dict(),
        'sharpe_ratio': dict(),
        'deflated_sharpe_ratio': dict(),
        'downside_risk': dict(),
        'sortino_ratio': dict(),
        'information_ratio': dict(),
        'beta': dict(),
        'alpha': dict(),
        'tail_ratio': dict(),
        'value_at_risk': dict(),
        'cond_value_at_risk': dict(),
        'capture': dict(),
        'up_capture': dict(),
        'down_capture': dict(),
        'drawdown': dict(),
        'max_drawdown': dict()
    },
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['returns_acc_config'] = f"""Config of returns accessor methods to be added to `Portfolio`.

```json
{returns_acc_config.to_doc()}
```
"""

PortfolioT = tp.TypeVar("PortfolioT", bound="Portfolio")


class MetaPortfolio(type(StatsBuilderMixin), type(PlotsBuilderMixin)):
    pass


@attach_returns_acc_methods(returns_acc_config)
class Portfolio(Wrapping, StatsBuilderMixin, PlotsBuilderMixin, metaclass=MetaPortfolio):
    """Class for modeling portfolio and measuring its performance.

    Args:
        wrapper (ArrayWrapper): Array wrapper.

            See `vectorbt.base.array_wrapper.ArrayWrapper`.
        close (array_like): Last asset price at each time step.
        order_records (array_like): A structured NumPy array of order records.
        log_records (array_like): A structured NumPy array of log records.
        init_cash (InitCashMode, float or array_like of float): Initial capital.
        cash_sharing (bool): Whether to share cash within the same group.
        call_seq (array_like of int): Sequence of calls per row and group. Defaults to None.
        fillna_close (bool): Whether to forward and backward fill NaN values in `close`.

            Applied after the simulation to avoid NaNs in asset value.

            See `Portfolio.get_filled_close`.
        trades_type (str or int): Default `vectorbt.portfolio.trades.Trades` to use across `Portfolio`.

            See `vectorbt.portfolio.enums.TradesType`.

    For defaults, see `portfolio` in `vectorbt._settings.settings`.

    !!! note
        Use class methods with `from_` prefix to build a portfolio.
        The `__init__` method is reserved for indexing purposes.

    !!! note
        This class is meant to be immutable. To change any attribute, use `Portfolio.replace`."""

    def __init__(self,
                 wrapper: ArrayWrapper,
                 close: tp.ArrayLike,
                 order_records: tp.RecordArray,
                 log_records: tp.RecordArray,
                 init_cash: tp.ArrayLike,
                 cash_sharing: bool,
                 call_seq: tp.Optional[tp.Array2d] = None,
                 fillna_close: tp.Optional[bool] = None,
                 trades_type: tp.Optional[tp.Union[int, str]] = None) -> None:
        Wrapping.__init__(
            self,
            wrapper,
            close=close,
            order_records=order_records,
            log_records=log_records,
            init_cash=init_cash,
            cash_sharing=cash_sharing,
            call_seq=call_seq,
            fillna_close=fillna_close,
            trades_type=trades_type
        )
        StatsBuilderMixin.__init__(self)
        PlotsBuilderMixin.__init__(self)

        # Get defaults
        from vectorbt._settings import settings
        portfolio_cfg = settings['portfolio']

        if fillna_close is None:
            fillna_close = portfolio_cfg['fillna_close']
        if trades_type is None:
            trades_type = portfolio_cfg['trades_type']
        if isinstance(trades_type, str):
            trades_type = map_enum_fields(trades_type, TradesType)

        # Store passed arguments
        self._close = broadcast_to(close, wrapper.dummy(group_by=False))
        self._order_records = order_records
        self._log_records = log_records
        self._init_cash = init_cash
        self._cash_sharing = cash_sharing
        self._call_seq = call_seq
        self._fillna_close = fillna_close
        self._trades_type = trades_type

    def indexing_func(self: PortfolioT, pd_indexing_func: tp.PandasIndexingFunc, **kwargs) -> PortfolioT:
        """Perform indexing on `Portfolio`."""
        new_wrapper, _, group_idxs, col_idxs = \
            self.wrapper.indexing_func_meta(pd_indexing_func, column_only_select=True, **kwargs)
        new_close = new_wrapper.wrap(to_2d_array(self.close)[:, col_idxs], group_by=False)
        new_order_records = self.orders.get_by_col_idxs(col_idxs)
        new_log_records = self.logs.get_by_col_idxs(col_idxs)
        if isinstance(self._init_cash, int):
            new_init_cash = self._init_cash
        else:
            new_init_cash = to_1d_array(self._init_cash)[group_idxs if self.cash_sharing else col_idxs]
        if self.call_seq is not None:
            new_call_seq = self.call_seq.values[:, col_idxs]
        else:
            new_call_seq = None

        return self.replace(
            wrapper=new_wrapper,
            close=new_close,
            order_records=new_order_records,
            log_records=new_log_records,
            init_cash=new_init_cash,
            call_seq=new_call_seq
        )

    # ############# Class methods ############# #

    @classmethod
    def from_orders(cls: tp.Type[PortfolioT],
                    close: tp.ArrayLike,
                    size: tp.Optional[tp.ArrayLike] = None,
                    size_type: tp.Optional[tp.ArrayLike] = None,
                    direction: tp.Optional[tp.ArrayLike] = None,
                    price: tp.Optional[tp.ArrayLike] = None,
                    fees: tp.Optional[tp.ArrayLike] = None,
                    fixed_fees: tp.Optional[tp.ArrayLike] = None,
                    slippage: tp.Optional[tp.ArrayLike] = None,
                    min_size: tp.Optional[tp.ArrayLike] = None,
                    max_size: tp.Optional[tp.ArrayLike] = None,
                    size_granularity: tp.Optional[tp.ArrayLike] = None,
                    reject_prob: tp.Optional[tp.ArrayLike] = None,
                    lock_cash: tp.Optional[tp.ArrayLike] = None,
                    allow_partial: tp.Optional[tp.ArrayLike] = None,
                    raise_reject: tp.Optional[tp.ArrayLike] = None,
                    log: tp.Optional[tp.ArrayLike] = None,
                    val_price: tp.Optional[tp.ArrayLike] = None,
                    init_cash: tp.Optional[tp.ArrayLike] = None,
                    cash_sharing: tp.Optional[bool] = None,
                    call_seq: tp.Optional[tp.ArrayLike] = None,
                    ffill_val_price: tp.Optional[bool] = None,
                    update_value: tp.Optional[bool] = None,
                    max_orders: tp.Optional[int] = None,
                    max_logs: tp.Optional[int] = None,
                    seed: tp.Optional[int] = None,
                    group_by: tp.GroupByLike = None,
                    broadcast_kwargs: tp.KwargsLike = None,
                    wrapper_kwargs: tp.KwargsLike = None,
                    freq: tp.Optional[tp.FrequencyLike] = None,
                    attach_call_seq: tp.Optional[bool] = None,
                    **kwargs) -> PortfolioT:
        """Simulate portfolio from orders - size, price, fees, and other information.

        Args:
            close (array_like): Last asset price at each time step.
                Will broadcast.

                Used for calculating unrealized PnL and portfolio value.
            size (float or array_like): Size to order.
                See `vectorbt.portfolio.enums.Order.size`. Will broadcast.
            size_type (SizeType or array_like): See `vectorbt.portfolio.enums.SizeType`.
                See `vectorbt.portfolio.enums.Order.size_type`. Will broadcast.

                !!! note
                    `SizeType.Percent` does not support position reversal. Switch to a single direction.

                !!! warning
                    Be cautious using `SizeType.Percent` with `call_seq` set to 'auto'.
                    To execute sell orders before buy orders, the value of each order in the group
                    needs to be approximated in advance. But since `SizeType.Percent` depends
                    upon the cash balance, which cannot be calculated in advance since it may change
                    after each order, this can yield a non-optimal call sequence.
            direction (Direction or array_like): See `vectorbt.portfolio.enums.Direction`.
                See `vectorbt.portfolio.enums.Order.direction`. Will broadcast.
            price (array_like of float): Order price.
                See `vectorbt.portfolio.enums.Order.price`. Defaults to `np.inf`. Will broadcast.

                !!! note
                    Make sure to use the same timestamp for all order prices in the group with cash sharing
                    and `call_seq` set to `CallSeqType.Auto`.
            fees (float or array_like): Fees in percentage of the order value.
                See `vectorbt.portfolio.enums.Order.fees`. Will broadcast.
            fixed_fees (float or array_like): Fixed amount of fees to pay per order.
                See `vectorbt.portfolio.enums.Order.fixed_fees`. Will broadcast.
            slippage (float or array_like): Slippage in percentage of price.
                See `vectorbt.portfolio.enums.Order.slippage`. Will broadcast.
            min_size (float or array_like): Minimum size for an order to be accepted.
                See `vectorbt.portfolio.enums.Order.min_size`. Will broadcast.
            max_size (float or array_like): Maximum size for an order.
                See `vectorbt.portfolio.enums.Order.max_size`. Will broadcast.

                Will be partially filled if exceeded.
            size_granularity (float or array_like): Granularity of the size.
                See `vectorbt.portfolio.enums.Order.size_granularity`. Will broadcast.
            reject_prob (float or array_like): Order rejection probability.
                See `vectorbt.portfolio.enums.Order.reject_prob`. Will broadcast.
            lock_cash (bool or array_like): Whether to lock cash when shorting.
                See `vectorbt.portfolio.enums.Order.lock_cash`. Will broadcast.
            allow_partial (bool or array_like): Whether to allow partial fills.
                See `vectorbt.portfolio.enums.Order.allow_partial`. Will broadcast.

                Does not apply when size is `np.inf`.
            raise_reject (bool or array_like): Whether to raise an exception if order gets rejected.
                See `vectorbt.portfolio.enums.Order.raise_reject`. Will broadcast.
            log (bool or array_like): Whether to log orders.
                See `vectorbt.portfolio.enums.Order.log`. Will broadcast.
            val_price (array_like of float): Asset valuation price.
                Will broadcast.

                * Any `-np.inf` element is replaced by the latest valuation price (the previous `close` or
                    the latest known valuation price if `ffill_val_price`).
                * Any `np.inf` element is replaced by the current order price.

                Used at the time of decision making to calculate value of each asset in the group,
                for example, to convert target value into target amount.

                !!! note
                    In contrast to `Portfolio.from_order_func`, order price is known beforehand (kind of),
                    thus `val_price` is set to the current order price (using `np.inf`) by default.
                    To valuate using previous close, set it in the settings to `-np.inf`.

                !!! note
                    Make sure to use timestamp for `val_price` that comes before timestamps of
                    all orders in the group with cash sharing (previous `close` for example),
                    otherwise you're cheating yourself.
            init_cash (InitCashMode, float or array_like of float): Initial capital.

                By default, will broadcast to the number of columns.
                If cash sharing is enabled, will broadcast to the number of groups.
                See `vectorbt.portfolio.enums.InitCashMode` to find optimal initial cash.

                !!! note
                    Mode `InitCashMode.AutoAlign` is applied after the portfolio is initialized
                    to set the same initial cash for all columns/groups. Changing grouping
                    will change the initial cash, so be aware when indexing.
            cash_sharing (bool): Whether to share cash within the same group.

                If `group_by` is None, `group_by` becomes True to form a single group with cash sharing.

                !!! warning
                    Introduces cross-asset dependencies.

                    This method presumes that in a group of assets that share the same capital all
                    orders will be executed within the same tick and retain their price regardless
                    of their position in the queue, even though they depend upon each other and thus
                    cannot be executed in parallel.
            call_seq (CallSeqType or array_like): Default sequence of calls per row and group.

                Each value in this sequence should indicate the position of column in the group to
                call next. Processing of `call_seq` goes always from left to right.
                For example, `[2, 0, 1]` would first call column 'c', then 'a', and finally 'b'.

                * Use `vectorbt.portfolio.enums.CallSeqType` to select a sequence type.
                * Set to array to specify custom sequence. Will not broadcast.

                If `CallSeqType.Auto` selected, rearranges calls dynamically based on order value.
                Calculates value of all orders per row and group, and sorts them by this value.
                Sell orders will be executed first to release funds for buy orders.

                !!! warning
                    `CallSeqType.Auto` should be used with caution:

                    * It not only presumes that order prices are known beforehand, but also that
                        orders can be executed in arbitrary order and still retain their price.
                        In reality, this is hardly the case: after processing one asset, some time
                        has passed and the price for other assets might have already changed.
                    * Even if you're able to specify a slippage large enough to compensate for
                        this behavior, slippage itself should depend upon execution order.
                        This method doesn't let you do that.
                    * If one order is rejected, it still may execute next orders and possibly
                        leave them without required funds.

                    For more control, use `Portfolio.from_order_func`.
            ffill_val_price (bool): Whether to track valuation price only if it's known.

                Otherwise, unknown `close` will lead to NaN in valuation price at the next timestamp.
            update_value (bool): Whether to update group value after each filled order.
            max_orders (int): Size of the order records array.
                Defaults to the number of elements in the broadcasted shape.

                Set to a lower number if you run out of memory.
            max_logs (int): Size of the log records array.
                Defaults to the number of elements in the broadcasted shape if any of the `log` is True,
                otherwise to 1.

                Set to a lower number if you run out of memory.
            seed (int): Seed to be set for both `call_seq` and at the beginning of the simulation.
            group_by (any): Group columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            broadcast_kwargs (dict): Keyword arguments passed to `vectorbt.base.reshape_fns.broadcast`.
            wrapper_kwargs (dict): Keyword arguments passed to `vectorbt.base.array_wrapper.ArrayWrapper`.
            freq (any): Index frequency in case it cannot be parsed from `close`.
            attach_call_seq (bool): Whether to pass `call_seq` to the constructor.

                Makes sense if you want to analyze some metrics in the simulation order.
                Otherwise, just takes memory.
            **kwargs: Keyword arguments passed to the `__init__` method.

        All broadcastable arguments will broadcast using `vectorbt.base.reshape_fns.broadcast`
        but keep original shape to utilize flexible indexing and to save memory.

        For defaults, see `portfolio` in `vectorbt._settings.settings`.

        !!! note
            When `call_seq` is not `CallSeqType.Auto`, at each timestamp, processing of the assets in
            a group goes strictly in order defined in `call_seq`. This order can't be changed dynamically.

            This has one big implication for this particular method: the last asset in the call stack
            cannot be processed until other assets are processed. This is the reason why rebalancing
            cannot work properly in this setting: one has to specify percentages for all assets beforehand
            and then tweak the processing order to sell to-be-sold assets first in order to release funds
            for to-be-bought assets. This can be automatically done by using `CallSeqType.Auto`.

        !!! hint
            All broadcastable arguments can be set per frame, series, row, column, or element.

        Usage:
            * Buy 10 units each tick:

            ```pycon
            >>> close = pd.Series([1, 2, 3, 4, 5])
            >>> pf = vbt.Portfolio.from_orders(close, 10)

            >>> pf.assets()
            0    10.0
            1    20.0
            2    30.0
            3    40.0
            4    40.0
            dtype: float64
            >>> pf.cash()
            0    90.0
            1    70.0
            2    40.0
            3     0.0
            4     0.0
            dtype: float64
            ```

            * Reverse each position by first closing it:

            ```pycon
            >>> size = [1, 0, -1, 0, 1]
            >>> pf = vbt.Portfolio.from_orders(close, size, size_type='targetpercent')

            >>> pf.assets()
            0    100.000000
            1      0.000000
            2    -66.666667
            3      0.000000
            4     26.666667
            dtype: float64
            >>> pf.cash()
            0      0.000000
            1    200.000000
            2    400.000000
            3    133.333333
            4      0.000000
            dtype: float64
            ```

            * Equal-weighted portfolio as in `vectorbt.portfolio.nb.simulate_nb` example
            (it's more compact but has less control over execution):

            ```pycon
            >>> np.random.seed(42)
            >>> close = pd.DataFrame(np.random.uniform(1, 10, size=(5, 3)))
            >>> size = pd.Series(np.full(5, 1/3))  # each column 33.3%
            >>> size[1::2] = np.nan  # skip every second tick

            >>> pf = vbt.Portfolio.from_orders(
            ...     close,  # acts both as reference and order price here
            ...     size,
            ...     size_type='targetpercent',
            ...     call_seq='auto',  # first sell then buy
            ...     group_by=True,  # one group
            ...     cash_sharing=True,  # assets share the same cash
            ...     fees=0.001, fixed_fees=1., slippage=0.001  # costs
            ... )

            >>> pf.asset_value(group_by=False).vbt.plot()
            ```

            ![](/assets/images/simulate_nb.svg)
        """
        # Get defaults
        from vectorbt._settings import settings
        portfolio_cfg = settings['portfolio']

        if size is None:
            size = portfolio_cfg['size']
        if size_type is None:
            size_type = portfolio_cfg['size_type']
        size_type = map_enum_fields(size_type, SizeType)
        if direction is None:
            direction = portfolio_cfg['order_direction']
        direction = map_enum_fields(direction, Direction)
        if price is None:
            price = np.inf
        if size is None:
            size = portfolio_cfg['size']
        if fees is None:
            fees = portfolio_cfg['fees']
        if fixed_fees is None:
            fixed_fees = portfolio_cfg['fixed_fees']
        if slippage is None:
            slippage = portfolio_cfg['slippage']
        if min_size is None:
            min_size = portfolio_cfg['min_size']
        if max_size is None:
            max_size = portfolio_cfg['max_size']
        if size_granularity is None:
            size_granularity = portfolio_cfg['size_granularity']
        if reject_prob is None:
            reject_prob = portfolio_cfg['reject_prob']
        if lock_cash is None:
            lock_cash = portfolio_cfg['lock_cash']
        if allow_partial is None:
            allow_partial = portfolio_cfg['allow_partial']
        if raise_reject is None:
            raise_reject = portfolio_cfg['raise_reject']
        if log is None:
            log = portfolio_cfg['log']
        if val_price is None:
            val_price = portfolio_cfg['val_price']
        if init_cash is None:
            init_cash = portfolio_cfg['init_cash']
        if isinstance(init_cash, str):
            init_cash = map_enum_fields(init_cash, InitCashMode)
        if isinstance(init_cash, int) and init_cash in InitCashMode:
            init_cash_mode = init_cash
            init_cash = np.inf
        else:
            init_cash_mode = None
        if cash_sharing is None:
            cash_sharing = portfolio_cfg['cash_sharing']
        if cash_sharing and group_by is None:
            group_by = True
        if call_seq is None:
            call_seq = portfolio_cfg['call_seq']
        auto_call_seq = False
        if isinstance(call_seq, str):
            call_seq = map_enum_fields(call_seq, CallSeqType)
        if isinstance(call_seq, int):
            if call_seq == CallSeqType.Auto:
                call_seq = CallSeqType.Default
                auto_call_seq = True
        if ffill_val_price is None:
            ffill_val_price = portfolio_cfg['ffill_val_price']
        if update_value is None:
            update_value = portfolio_cfg['update_value']
        if seed is None:
            seed = portfolio_cfg['seed']
        if seed is not None:
            set_seed(seed)
        if freq is None:
            freq = portfolio_cfg['freq']
        if attach_call_seq is None:
            attach_call_seq = portfolio_cfg['attach_call_seq']
        if broadcast_kwargs is None:
            broadcast_kwargs = {}
        if wrapper_kwargs is None:
            wrapper_kwargs = {}
        if not wrapper_kwargs.get('group_select', True) and cash_sharing:
            raise ValueError("group_select cannot be disabled if cash_sharing=True")

        # Prepare the simulation
        # Only close is broadcast, others can remain unchanged thanks to flexible indexing
        broadcastable_args = (
            size,
            price,
            size_type,
            direction,
            fees,
            fixed_fees,
            slippage,
            min_size,
            max_size,
            size_granularity,
            reject_prob,
            lock_cash,
            allow_partial,
            raise_reject,
            log,
            val_price,
            close
        )
        keep_raw = [True] * len(broadcastable_args)
        keep_raw[-1] = False
        broadcast_kwargs = merge_dicts(dict(
            keep_raw=keep_raw,
            require_kwargs=dict(requirements='W')
        ), broadcast_kwargs)
        broadcasted_args = broadcast(*broadcastable_args, **broadcast_kwargs)
        close = broadcasted_args[-1]
        if not checks.is_pandas(close):
            close = pd.Series(close) if close.ndim == 1 else pd.DataFrame(close)
        target_shape_2d = (close.shape[0], close.shape[1] if close.ndim > 1 else 1)
        wrapper = ArrayWrapper.from_obj(close, freq=freq, group_by=group_by, **wrapper_kwargs)
        cs_group_lens = wrapper.grouper.get_group_lens(group_by=None if cash_sharing else False)
        init_cash = np.require(np.broadcast_to(init_cash, (len(cs_group_lens),)), dtype=np.float64)
        group_lens = wrapper.grouper.get_group_lens(group_by=group_by)
        if checks.is_any_array(call_seq):
            call_seq = nb.require_call_seq(broadcast(call_seq, to_shape=target_shape_2d, to_pd=False))
        else:
            call_seq = nb.build_call_seq(target_shape_2d, group_lens, call_seq_type=call_seq)
        if max_orders is None:
            max_orders = target_shape_2d[0] * target_shape_2d[1]
        if max_logs is None:
            max_logs = target_shape_2d[0] * target_shape_2d[1]
        if not np.any(log):
            max_logs = 1

        # Perform the simulation
        order_records, log_records = nb.simulate_from_orders_nb(
            target_shape_2d,
            cs_group_lens,  # group only if cash sharing is enabled to speed up
            init_cash,
            call_seq,
            *map(np.asarray, broadcasted_args),
            auto_call_seq,
            ffill_val_price,
            update_value,
            max_orders,
            max_logs,
            close.ndim == 2
        )

        # Create an instance
        return cls(
            wrapper,
            close,
            order_records,
            log_records,
            init_cash if init_cash_mode is None else init_cash_mode,
            cash_sharing,
            call_seq=call_seq if attach_call_seq else None,
            **kwargs
        )

    @classmethod
    def from_signals(cls: tp.Type[PortfolioT],
                     close: tp.ArrayLike,
                     entries: tp.Optional[tp.ArrayLike] = None,
                     exits: tp.Optional[tp.ArrayLike] = None,
                     short_entries: tp.Optional[tp.ArrayLike] = None,
                     short_exits: tp.Optional[tp.ArrayLike] = None,
                     signal_func_nb: nb.SignalFuncT = nb.no_signal_func_nb,
                     signal_args: tp.ArgsLike = (),
                     size: tp.Optional[tp.ArrayLike] = None,
                     size_type: tp.Optional[tp.ArrayLike] = None,
                     price: tp.Optional[tp.ArrayLike] = None,
                     fees: tp.Optional[tp.ArrayLike] = None,
                     fixed_fees: tp.Optional[tp.ArrayLike] = None,
                     slippage: tp.Optional[tp.ArrayLike] = None,
                     min_size: tp.Optional[tp.ArrayLike] = None,
                     max_size: tp.Optional[tp.ArrayLike] = None,
                     size_granularity: tp.Optional[tp.ArrayLike] = None,
                     reject_prob: tp.Optional[tp.ArrayLike] = None,
                     lock_cash: tp.Optional[tp.ArrayLike] = None,
                     allow_partial: tp.Optional[tp.ArrayLike] = None,
                     raise_reject: tp.Optional[tp.ArrayLike] = None,
                     log: tp.Optional[tp.ArrayLike] = None,
                     accumulate: tp.Optional[tp.ArrayLike] = None,
                     upon_long_conflict: tp.Optional[tp.ArrayLike] = None,
                     upon_short_conflict: tp.Optional[tp.ArrayLike] = None,
                     upon_dir_conflict: tp.Optional[tp.ArrayLike] = None,
                     upon_opposite_entry: tp.Optional[tp.ArrayLike] = None,
                     direction: tp.Optional[tp.ArrayLike] = None,
                     val_price: tp.Optional[tp.ArrayLike] = None,
                     open: tp.Optional[tp.ArrayLike] = None,
                     high: tp.Optional[tp.ArrayLike] = None,
                     low: tp.Optional[tp.ArrayLike] = None,
                     sl_stop: tp.Optional[tp.ArrayLike] = None,
                     sl_trail: tp.Optional[tp.ArrayLike] = None,
                     tp_stop: tp.Optional[tp.ArrayLike] = None,
                     stop_entry_price: tp.Optional[tp.ArrayLike] = None,
                     stop_exit_price: tp.Optional[tp.ArrayLike] = None,
                     upon_stop_exit: tp.Optional[tp.ArrayLike] = None,
                     upon_stop_update: tp.Optional[tp.ArrayLike] = None,
                     adjust_sl_func_nb: nb.AdjustSLFuncT = nb.no_adjust_sl_func_nb,
                     adjust_sl_args: tp.Args = (),
                     adjust_tp_func_nb: nb.AdjustTPFuncT = nb.no_adjust_tp_func_nb,
                     adjust_tp_args: tp.Args = (),
                     use_stops: tp.Optional[bool] = None,
                     init_cash: tp.Optional[tp.ArrayLike] = None,
                     cash_sharing: tp.Optional[bool] = None,
                     call_seq: tp.Optional[tp.ArrayLike] = None,
                     ffill_val_price: tp.Optional[bool] = None,
                     update_value: tp.Optional[bool] = None,
                     max_orders: tp.Optional[int] = None,
                     max_logs: tp.Optional[int] = None,
                     seed: tp.Optional[int] = None,
                     group_by: tp.GroupByLike = None,
                     broadcast_named_args: tp.KwargsLike = None,
                     broadcast_kwargs: tp.KwargsLike = None,
                     template_mapping: tp.Optional[tp.Mapping] = None,
                     wrapper_kwargs: tp.KwargsLike = None,
                     freq: tp.Optional[tp.FrequencyLike] = None,
                     attach_call_seq: tp.Optional[bool] = None,
                     **kwargs) -> PortfolioT:
        """Simulate portfolio from entry and exit signals.

        See `vectorbt.portfolio.nb.simulate_from_signal_func_nb`.

        You have three options to provide signals:

        * `entries` and `exits`: The direction of each pair of signals is taken from `direction` argument.
            Best to use when the direction doesn't change throughout time.

            Uses `vectorbt.portfolio.nb.dir_enex_signal_func_nb` as `signal_func_nb`.

            !!! hint
                `entries` and `exits` can be easily translated to direction-aware signals:

                * (True, True, 'longonly') -> True, True, False, False
                * (True, True, 'shortonly') -> False, False, True, True
                * (True, True, 'both') -> True, False, True, False

        * `entries` (acting as long), `exits` (acting as long), `short_entries`, and `short_exits`:
            The direction is already built into the arrays. Best to use when the direction changes frequently
            (for example, if you have one indicator providing long signals and one providing short signals).

            Uses `vectorbt.portfolio.nb.ls_enex_signal_func_nb` as `signal_func_nb`.

        * `signal_func_nb` and `signal_args`: Custom signal function that returns direction-aware signals.
            Best to use when signals should be placed dynamically based on custom conditions.

        Args:
            close (array_like): See `Portfolio.from_orders`.
            entries (array_like of bool): Boolean array of entry signals.
                Defaults to True if all other signal arrays are not set, otherwise False. Will broadcast.

                * If `short_entries` and `short_exits` are not set: Acts as a long signal if `direction`
                    is `all` or `longonly`, otherwise short.
                * If `short_entries` or `short_exits` are set: Acts as `long_entries`.
            exits (array_like of bool): Boolean array of exit signals.
                Defaults to False. Will broadcast.

                * If `short_entries` and `short_exits` are not set: Acts as a short signal if `direction`
                    is `all` or `longonly`, otherwise long.
                * If `short_entries` or `short_exits` are set: Acts as `long_exits`.
            short_entries (array_like of bool): Boolean array of short entry signals.
                Defaults to False. Will broadcast.
            short_exits (array_like of bool): Boolean array of short exit signals.
                Defaults to False. Will broadcast.
            signal_func_nb (callable): Function called to generate signals.

                Should accept `vectorbt.portfolio.enums.SignalContext` and `*signal_args`.
                Should return long entry signal, long exit signal, short entry signal, and short exit signal.

                !!! note
                    Stop signal has priority: `signal_func_nb` is executed only if there is no stop signal.
            signal_args (tuple): Packed arguments passed to `signal_func_nb`.
                Defaults to `()`.
            size (float or array_like): See `Portfolio.from_orders`.

                !!! note
                    Negative size is not allowed. You should express direction using signals.
            size_type (SizeType or array_like): See `Portfolio.from_orders`.

                Only `SizeType.Amount`, `SizeType.Value`, and `SizeType.Percent` are supported.
                Other modes such as target percentage are not compatible with signals since
                their logic may contradict the direction of the signal.

                !!! note
                    `SizeType.Percent` does not support position reversal. Switch to a single
                    direction or use `vectorbt.portfolio.enums.OppositeEntryMode.Close` to close the position first.

                See warning in `Portfolio.from_orders`.
            price (array_like of float): See `Portfolio.from_orders`.
            fees (float or array_like): See `Portfolio.from_orders`.
            fixed_fees (float or array_like): See `Portfolio.from_orders`.
            slippage (float or array_like): See `Portfolio.from_orders`.
            min_size (float or array_like): See `Portfolio.from_orders`.
            max_size (float or array_like): See `Portfolio.from_orders`.

                Will be partially filled if exceeded. You might not be able to properly close
                the position if accumulation is enabled and `max_size` is too low.
            size_granularity (float or array_like): See `Portfolio.from_orders`.
            reject_prob (float or array_like): See `Portfolio.from_orders`.
            lock_cash (bool or array_like): See `Portfolio.from_orders`.
            allow_partial (bool or array_like): See `Portfolio.from_orders`.
            raise_reject (bool or array_like): See `Portfolio.from_orders`.
            log (bool or array_like): See `Portfolio.from_orders`.
            accumulate (bool, AccumulationMode or array_like): See `vectorbt.portfolio.enums.AccumulationMode`.
                If True, becomes 'both'. If False, becomes 'disabled'. Will broadcast.

                When enabled, `Portfolio.from_signals` behaves similarly to `Portfolio.from_orders`.
            upon_long_conflict (ConflictMode or array_like): Conflict mode for long signals.
                See `vectorbt.portfolio.enums.ConflictMode`. Will broadcast.
            upon_short_conflict (ConflictMode or array_like): Conflict mode for short signals.
                See `vectorbt.portfolio.enums.ConflictMode`. Will broadcast.
            upon_dir_conflict (DirectionConflictMode or array_like): See `vectorbt.portfolio.enums.DirectionConflictMode`. Will broadcast.
            upon_opposite_entry (OppositeEntryMode or array_like): See `vectorbt.portfolio.enums.OppositeEntryMode`. Will broadcast.
            direction (Direction or array_like): See `Portfolio.from_orders`.

                Takes only effect if `short_entries` and `short_exits` are not set.
            val_price (array_like of float): See `Portfolio.from_orders`.
            open (array_like of float): First asset price at each time step.
                Defaults to `np.nan`, which gets replaced by `close`. Will broadcast.

                Used solely for stop signals.
            high (array_like of float): Highest asset price at each time step.
                Defaults to `np.nan`, which gets replaced by the maximum out of `open` and `close`. Will broadcast.

                Used solely for stop signals.
            low (array_like of float): Lowest asset price at each time step.
                Defaults to `np.nan`, which gets replaced by the minimum out of `open` and `close`. Will broadcast.

                Used solely for stop signals.
            sl_stop (array_like of float): Stop loss.
                Will broadcast.

                A percentage below/above the acquisition price for long/short position.
                Note that 0.01 = 1%.
            sl_trail (array_like of bool): Whether `sl_stop` should be trailing.
                Will broadcast.
            tp_stop (array_like of float): Take profit.
                Will broadcast.

                A percentage above/below the acquisition price for long/short position.
                Note that 0.01 = 1%.
            stop_entry_price (StopEntryPrice or array_like): See `vectorbt.portfolio.enums.StopEntryPrice`.
                Will broadcast.

                If provided on per-element basis, gets applied upon entry.
            stop_exit_price (StopExitPrice or array_like): See `vectorbt.portfolio.enums.StopExitPrice`.
                Will broadcast.

                If provided on per-element basis, gets applied upon exit.
            upon_stop_exit (StopExitMode or array_like): See `vectorbt.portfolio.enums.StopExitMode`.
                Will broadcast.

                If provided on per-element basis, gets applied upon exit.
            upon_stop_update (StopUpdateMode or array_like): See `vectorbt.portfolio.enums.StopUpdateMode`.
                Will broadcast.

                Only has effect if accumulation is enabled.

                If provided on per-element basis, gets applied upon repeated entry.
            adjust_sl_func_nb (callable): Function to adjust stop loss.
                Defaults to `vectorbt.portfolio.nb.no_adjust_sl_func_nb`.

                Called for each element before each row.

                Should accept `vectorbt.portfolio.enums.AdjustSLContext` and `*adjust_sl_args`.
                Should return a tuple of a new stop value and trailing flag.
            adjust_sl_args (tuple): Packed arguments passed to `adjust_sl_func_nb`.
                Defaults to `()`.
            adjust_tp_func_nb (callable): Function to adjust take profit.
                Defaults to `vectorbt.portfolio.nb.no_adjust_tp_func_nb`.

                Called for each element before each row.

                Should accept `vectorbt.portfolio.enums.AdjustTPContext` and `*adjust_tp_args`.
                of the stop, and `*adjust_tp_args`. Should return a new stop value.
            adjust_tp_args (tuple): Packed arguments passed to `adjust_tp_func_nb`.
                Defaults to `()`.
            use_stops (bool): Whether to use stops.
                Defaults to None, which becomes True if any of the stops are not NaN or
                any of the adjustment functions are custom.

                Disable this to make simulation a bit faster for simple use cases.
            init_cash (InitCashMode, float or array_like of float): See `Portfolio.from_orders`.
            cash_sharing (bool): See `Portfolio.from_orders`.
            call_seq (CallSeqType or array_like): See `Portfolio.from_orders`.
            ffill_val_price (bool): See `Portfolio.from_orders`.
            update_value (bool): See `Portfolio.from_orders`.
            max_orders (int): See `Portfolio.from_orders`.
            max_logs (int): See `Portfolio.from_orders`.
            seed (int): See `Portfolio.from_orders`.
            group_by (any): See `Portfolio.from_orders`.
            broadcast_named_args (dict): Dictionary with named arguments to broadcast.

                You can then pass argument names to the functions and this method will substitute
                them by their corresponding broadcasted objects.
            broadcast_kwargs (dict): See `Portfolio.from_orders`.
            template_mapping (mapping): Mapping to replace templates in arguments.
            wrapper_kwargs (dict): See `Portfolio.from_orders`.
            freq (any): See `Portfolio.from_orders`.
            attach_call_seq (bool): See `Portfolio.from_orders`.
            **kwargs: Keyword arguments passed to the `__init__` method.

        All broadcastable arguments will broadcast using `vectorbt.base.reshape_fns.broadcast`
        but keep original shape to utilize flexible indexing and to save memory.

        For defaults, see `portfolio` in `vectorbt._settings.settings`.

        !!! note
            Stop signal has priority - it's executed before other signals within the same bar.
            That is, if a stop signal is present, no other signals are generated and executed
            since there is a limit of one order per symbol and bar.

        !!! hint
            If you generated signals using close price, don't forget to shift your signals by one tick
            forward, for example, with `signals.vbt.fshift(1)`. In general, make sure to use a price
            that comes after the signal.

        Also see notes and hints for `Portfolio.from_orders`.

        Usage:
            * By default, if all signal arrays are None, `entries` becomes True,
            which opens a position at the very first tick and does nothing else:

            ```pycon
            >>> close = pd.Series([1, 2, 3, 4, 5])
            >>> pf = vbt.Portfolio.from_signals(close, size=1)
            >>> pf.asset_flow()
            0    1.0
            1    0.0
            2    0.0
            3    0.0
            4    0.0
            dtype: float64
            ```

            * Entry opens long, exit closes long:

            ```pycon
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=pd.Series([True, True, True, False, False]),
            ...     exits=pd.Series([False, False, True, True, True]),
            ...     size=1,
            ...     direction='longonly'
            ... )
            >>> pf.asset_flow()
            0    1.0
            1    0.0
            2    0.0
            3   -1.0
            4    0.0
            dtype: float64

            >>> # Using direction-aware arrays instead of `direction`
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=pd.Series([True, True, True, False, False]),  # long_entries
            ...     exits=pd.Series([False, False, True, True, True]),  # long_exits
            ...     short_entries=False,
            ...     short_exits=False,
            ...     size=1
            ... )
            >>> pf.asset_flow()
            0    1.0
            1    0.0
            2    0.0
            3   -1.0
            4    0.0
            dtype: float64
            ```

            Notice how both `short_entries` and `short_exits` are provided as constants - as any other
            broadcastable argument, they are treated as arrays where each element is False.

            * Entry opens short, exit closes short:

            ```pycon
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=pd.Series([True, True, True, False, False]),
            ...     exits=pd.Series([False, False, True, True, True]),
            ...     size=1,
            ...     direction='shortonly'
            ... )
            >>> pf.asset_flow()
            0   -1.0
            1    0.0
            2    0.0
            3    1.0
            4    0.0
            dtype: float64

            >>> # Using direction-aware arrays instead of `direction`
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=False,  # long_entries
            ...     exits=False,  # long_exits
            ...     short_entries=pd.Series([True, True, True, False, False]),
            ...     short_exits=pd.Series([False, False, True, True, True]),
            ...     size=1
            ... )
            >>> pf.asset_flow()
            0   -1.0
            1    0.0
            2    0.0
            3    1.0
            4    0.0
            dtype: float64
            ```

            * Entry opens long and closes short, exit closes long and opens short:

            ```pycon
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=pd.Series([True, True, True, False, False]),
            ...     exits=pd.Series([False, False, True, True, True]),
            ...     size=1,
            ...     direction='both'
            ... )
            >>> pf.asset_flow()
            0    1.0
            1    0.0
            2    0.0
            3   -2.0
            4    0.0
            dtype: float64

            >>> # Using direction-aware arrays instead of `direction`
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=pd.Series([True, True, True, False, False]),  # long_entries
            ...     exits=False,  # long_exits
            ...     short_entries=pd.Series([False, False, True, True, True]),
            ...     short_exits=False,
            ...     size=1
            ... )
            >>> pf.asset_flow()
            0    1.0
            1    0.0
            2    0.0
            3   -2.0
            4    0.0
            dtype: float64
            ```

            * More complex signal combinations are best expressed using direction-aware arrays.
            For example, ignore opposite signals as long as the current position is open:

            ```pycon
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries      =pd.Series([True, False, False, False, False]),  # long_entries
            ...     exits        =pd.Series([False, False, True, False, False]),  # long_exits
            ...     short_entries=pd.Series([False, True, False, True, False]),
            ...     short_exits  =pd.Series([False, False, False, False, True]),
            ...     size=1,
            ...     upon_opposite_entry='ignore'
            ... )
            >>> pf.asset_flow()
            0    1.0
            1    0.0
            2   -1.0
            3   -1.0
            4    1.0
            dtype: float64
            ```

            * First opposite signal closes the position, second one opens a new position:

            ```pycon
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=pd.Series([True, True, True, False, False]),
            ...     exits=pd.Series([False, False, True, True, True]),
            ...     size=1,
            ...     direction='both',
            ...     upon_opposite_entry='close'
            ... )
            >>> pf.asset_flow()
            0    1.0
            1    0.0
            2    0.0
            3   -1.0
            4   -1.0
            dtype: float64
            ```

            * If both long entry and exit signals are True (a signal conflict), choose exit:

            ```pycon
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=pd.Series([True, True, True, False, False]),
            ...     exits=pd.Series([False, False, True, True, True]),
            ...     size=1.,
            ...     direction='longonly',
            ...     upon_long_conflict='exit')
            >>> pf.asset_flow()
            0    1.0
            1    0.0
            2   -1.0
            3    0.0
            4    0.0
            dtype: float64
            ```

            * If both long entry and short entry signal are True (a direction conflict), choose short:

            ```pycon
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=pd.Series([True, True, True, False, False]),
            ...     exits=pd.Series([False, False, True, True, True]),
            ...     size=1.,
            ...     direction='both',
            ...     upon_dir_conflict='short')
            >>> pf.asset_flow()
            0    1.0
            1    0.0
            2   -2.0
            3    0.0
            4    0.0
            dtype: float64
            ```

            !!! note
                Remember that when direction is set to 'both', entries become `long_entries` and exits become
                `short_entries`, so this becomes a conflict of directions rather than signals.

            * If there are both signal and direction conflicts:

            ```pycon
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=True,  # long_entries
            ...     exits=True,  # long_exits
            ...     short_entries=True,
            ...     short_exits=True,
            ...     size=1,
            ...     upon_long_conflict='entry',
            ...     upon_short_conflict='entry',
            ...     upon_dir_conflict='short'
            ... )
            >>> pf.asset_flow()
            0   -1.0
            1    0.0
            2    0.0
            3    0.0
            4    0.0
            dtype: float64
            ```

            * Turn on accumulation of signals. Entry means long order, exit means short order
            (acts similar to `from_orders`):

            ```pycon
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=pd.Series([True, True, True, False, False]),
            ...     exits=pd.Series([False, False, True, True, True]),
            ...     size=1.,
            ...     direction='both',
            ...     accumulate=True)
            >>> pf.asset_flow()
            0    1.0
            1    1.0
            2    0.0
            3   -1.0
            4   -1.0
            dtype: float64
            ```

            * Allow increasing a position (of any direction), deny decreasing a position:

            ```pycon
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=pd.Series([True, True, True, False, False]),
            ...     exits=pd.Series([False, False, True, True, True]),
            ...     size=1.,
            ...     direction='both',
            ...     accumulate='addonly')
            >>> pf.asset_flow()
            0    1.0  << open a long position
            1    1.0  << add to the position
            2    0.0
            3   -3.0  << close and open a short position
            4   -1.0  << add to the position
            dtype: float64
            ```

            * Testing multiple parameters (via broadcasting):

            ```pycon
            >>> pf = vbt.Portfolio.from_signals(
            ...     close,
            ...     entries=pd.Series([True, True, True, False, False]),
            ...     exits=pd.Series([False, False, True, True, True]),
            ...     direction=[list(Direction)],
            ...     broadcast_kwargs=dict(columns_from=Direction._fields))
            >>> pf.asset_flow()
                Long  Short    All
            0  100.0 -100.0  100.0
            1    0.0    0.0    0.0
            2    0.0    0.0    0.0
            3 -100.0   50.0 -200.0
            4    0.0    0.0    0.0
            ```

            * Set risk/reward ratio by passing trailing stop loss and take profit thresholds:

            ```pycon
            >>> close = pd.Series([10, 11, 12, 11, 10, 9])
            >>> entries = pd.Series([True, False, False, False, False, False])
            >>> exits = pd.Series([False, False, False, False, False, True])
            >>> pf = vbt.Portfolio.from_signals(
            ...     close, entries, exits,
            ...     sl_stop=0.1, sl_trail=True, tp_stop=0.2)  # take profit hit
            >>> pf.asset_flow()
            0    10.0
            1     0.0
            2   -10.0
            3     0.0
            4     0.0
            5     0.0
            dtype: float64

            >>> pf = vbt.Portfolio.from_signals(
            ...     close, entries, exits,
            ...     sl_stop=0.1, sl_trail=True, tp_stop=0.3)  # stop loss hit
            >>> pf.asset_flow()
            0    10.0
            1     0.0
            2     0.0
            3     0.0
            4   -10.0
            5     0.0
            dtype: float64

            >>> pf = vbt.Portfolio.from_signals(
            ...     close, entries, exits,
            ...     sl_stop=np.inf, sl_trail=True, tp_stop=np.inf)  # nothing hit, exit as usual
            >>> pf.asset_flow()
            0    10.0
            1     0.0
            2     0.0
            3     0.0
            4     0.0
            5   -10.0
            dtype: float64
            ```

            !!! note
                When the stop price is hit, the stop signal invalidates any other signal defined for this bar.
                Thus, make sure that your signaling logic happens at the very end of the bar
                (for example, by using the closing price), otherwise you may expose yourself to a look-ahead bias.

                See `vectorbt.portfolio.enums.StopExitPrice` for more details.

            * We can implement our own stop loss or take profit, or adjust the existing one at each time step.
            Let's implement [stepped stop-loss](https://www.freqtrade.io/en/stable/strategy-advanced/#stepped-stoploss):

            ```pycon
            >>> @njit
            ... def adjust_sl_func_nb(c):
            ...     current_profit = (c.val_price_now - c.init_price) / c.init_price
            ...     if current_profit >= 0.40:
            ...         return 0.25, True
            ...     elif current_profit >= 0.25:
            ...         return 0.15, True
            ...     elif current_profit >= 0.20:
            ...         return 0.07, True
            ...     return c.curr_stop, c.curr_trail

            >>> close = pd.Series([10, 11, 12, 11, 10])
            >>> pf = vbt.Portfolio.from_signals(close, adjust_sl_func_nb=adjust_sl_func_nb)
            >>> pf.asset_flow()
            0    10.0
            1     0.0
            2     0.0
            3   -10.0  # 7% from 12 hit
            4    11.0
            dtype: float64
            ```

            * Sometimes there is a need to provide or transform signals dynamically. For this, we can implement
            a custom signal function `signal_func_nb`. For example, let's implement a signal function that
            takes two numerical arrays - long and short one - and transforms them into 4 direction-aware boolean
            arrays that vectorbt understands:

            ```pycon
            >>> @njit
            ... def signal_func_nb(c, long_num_arr, short_num_arr):
            ...     long_num = nb.get_elem_nb(c, long_num_arr)
            ...     short_num = nb.get_elem_nb(c, short_num_arr)
            ...     is_long_entry = long_num > 0
            ...     is_long_exit = long_num < 0
            ...     is_short_entry = short_num > 0
            ...     is_short_exit = short_num < 0
            ...     return is_long_entry, is_long_exit, is_short_entry, is_short_exit

            >>> pf = vbt.Portfolio.from_signals(
            ...     pd.Series([1, 2, 3, 4, 5]),
            ...     signal_func_nb=signal_func_nb,
            ...     signal_args=(vbt.Rep('long_num_arr'), vbt.Rep('short_num_arr')),
            ...     broadcast_named_args=dict(
            ...         long_num_arr=pd.Series([1, 0, -1, 0, 0]),
            ...         short_num_arr=pd.Series([0, 1, 0, 1, -1])
            ...     ),
            ...     size=1,
            ...     upon_opposite_entry='ignore'
            ... )
            >>> pf.asset_flow()
            0    1.0
            1    0.0
            2   -1.0
            3   -1.0
            4    1.0
            dtype: float64
            ```

            Passing both arrays as `broadcast_named_args` broadcasts them internally as any other array,
            so we don't have to worry about their dimensions every time we change our data.
        """
        # Get defaults
        from vectorbt._settings import settings
        portfolio_cfg = settings['portfolio']

        ls_mode = short_entries is not None or short_exits is not None
        signal_func_mode = signal_func_nb is not nb.no_signal_func_nb
        if (entries is not None or exits is not None or ls_mode) and signal_func_mode:
            raise ValueError("Either any of the signal arrays or signal_func_nb should be set, not both")
        if entries is None:
            if exits is None and not ls_mode:
                entries = True
            else:
                entries = False
        if exits is None:
            exits = False
        if short_entries is None:
            short_entries = False
        if short_exits is None:
            short_exits = False
        if signal_func_nb is nb.no_signal_func_nb:
            if ls_mode:
                signal_func_nb = nb.ls_enex_signal_func_nb
            else:
                signal_func_nb = nb.dir_enex_signal_func_nb
        if size is None:
            size = portfolio_cfg['size']
        if size_type is None:
            size_type = portfolio_cfg['size_type']
        size_type = map_enum_fields(size_type, SizeType)
        if price is None:
            price = np.inf
        if fees is None:
            fees = portfolio_cfg['fees']
        if fixed_fees is None:
            fixed_fees = portfolio_cfg['fixed_fees']
        if slippage is None:
            slippage = portfolio_cfg['slippage']
        if min_size is None:
            min_size = portfolio_cfg['min_size']
        if max_size is None:
            max_size = portfolio_cfg['max_size']
        if size_granularity is None:
            size_granularity = portfolio_cfg['size_granularity']
        if reject_prob is None:
            reject_prob = portfolio_cfg['reject_prob']
        if lock_cash is None:
            lock_cash = portfolio_cfg['lock_cash']
        if allow_partial is None:
            allow_partial = portfolio_cfg['allow_partial']
        if raise_reject is None:
            raise_reject = portfolio_cfg['raise_reject']
        if log is None:
            log = portfolio_cfg['log']
        if accumulate is None:
            accumulate = portfolio_cfg['accumulate']
        accumulate = map_enum_fields(accumulate, AccumulationMode, ignore_type=(int, bool))
        if upon_long_conflict is None:
            upon_long_conflict = portfolio_cfg['upon_long_conflict']
        upon_long_conflict = map_enum_fields(upon_long_conflict, ConflictMode)
        if upon_short_conflict is None:
            upon_short_conflict = portfolio_cfg['upon_short_conflict']
        upon_short_conflict = map_enum_fields(upon_short_conflict, ConflictMode)
        if upon_dir_conflict is None:
            upon_dir_conflict = portfolio_cfg['upon_dir_conflict']
        upon_dir_conflict = map_enum_fields(upon_dir_conflict, DirectionConflictMode)
        if upon_opposite_entry is None:
            upon_opposite_entry = portfolio_cfg['upon_opposite_entry']
        upon_opposite_entry = map_enum_fields(upon_opposite_entry, OppositeEntryMode)
        if direction is not None and ls_mode:
            warnings.warn("direction has no effect if short_entries and short_exits are set", stacklevel=2)
        if direction is None:
            direction = portfolio_cfg['signal_direction']
        direction = map_enum_fields(direction, Direction)
        if val_price is None:
            val_price = portfolio_cfg['val_price']
        if open is None:
            open = np.nan
        if high is None:
            high = np.nan
        if low is None:
            low = np.nan
        if sl_stop is None:
            sl_stop = portfolio_cfg['sl_stop']
        if sl_trail is None:
            sl_trail = portfolio_cfg['sl_trail']
        if tp_stop is None:
            tp_stop = portfolio_cfg['tp_stop']
        if stop_entry_price is None:
            stop_entry_price = portfolio_cfg['stop_entry_price']
        stop_entry_price = map_enum_fields(stop_entry_price, StopEntryPrice)
        if stop_exit_price is None:
            stop_exit_price = portfolio_cfg['stop_exit_price']
        stop_exit_price = map_enum_fields(stop_exit_price, StopExitPrice)
        if upon_stop_exit is None:
            upon_stop_exit = portfolio_cfg['upon_stop_exit']
        upon_stop_exit = map_enum_fields(upon_stop_exit, StopExitMode)
        if upon_stop_update is None:
            upon_stop_update = portfolio_cfg['upon_stop_update']
        upon_stop_update = map_enum_fields(upon_stop_update, StopUpdateMode)
        if use_stops is None:
            use_stops = portfolio_cfg['use_stops']
        if use_stops is None:
            if isinstance(sl_stop, float) and \
                    np.isnan(sl_stop) and \
                    isinstance(tp_stop, float) and \
                    np.isnan(tp_stop) and \
                    adjust_sl_func_nb == nb.no_adjust_sl_func_nb and \
                    adjust_tp_func_nb == nb.no_adjust_tp_func_nb:
                use_stops = False
            else:
                use_stops = True

        if init_cash is None:
            init_cash = portfolio_cfg['init_cash']
        if isinstance(init_cash, str):
            init_cash = map_enum_fields(init_cash, InitCashMode)
        if isinstance(init_cash, int) and init_cash in InitCashMode:
            init_cash_mode = init_cash
            init_cash = np.inf
        else:
            init_cash_mode = None
        if cash_sharing is None:
            cash_sharing = portfolio_cfg['cash_sharing']
        if cash_sharing and group_by is None:
            group_by = True
        if call_seq is None:
            call_seq = portfolio_cfg['call_seq']
        auto_call_seq = False
        if isinstance(call_seq, str):
            call_seq = map_enum_fields(call_seq, CallSeqType)
        if isinstance(call_seq, int):
            if call_seq == CallSeqType.Auto:
                call_seq = CallSeqType.Default
                auto_call_seq = True
        if ffill_val_price is None:
            ffill_val_price = portfolio_cfg['ffill_val_price']
        if update_value is None:
            update_value = portfolio_cfg['update_value']
        if seed is None:
            seed = portfolio_cfg['seed']
        if seed is not None:
            set_seed(seed)
        if freq is None:
            freq = portfolio_cfg['freq']
        if attach_call_seq is None:
            attach_call_seq = portfolio_cfg['attach_call_seq']
        if broadcast_named_args is None:
            broadcast_named_args = {}
        if broadcast_kwargs is None:
            broadcast_kwargs = {}
        if template_mapping is None:
            template_mapping = {}
        if wrapper_kwargs is None:
            wrapper_kwargs = {}
        if not wrapper_kwargs.get('group_select', True) and cash_sharing:
            raise ValueError("group_select cannot be disabled if cash_sharing=True")

        # Prepare the simulation
        broadcastable_args = dict(
            size=size,
            price=price,
            size_type=size_type,
            fees=fees,
            fixed_fees=fixed_fees,
            slippage=slippage,
            min_size=min_size,
            max_size=max_size,
            size_granularity=size_granularity,
            reject_prob=reject_prob,
            lock_cash=lock_cash,
            allow_partial=allow_partial,
            raise_reject=raise_reject,
            log=log,
            accumulate=accumulate,
            upon_long_conflict=upon_long_conflict,
            upon_short_conflict=upon_short_conflict,
            upon_dir_conflict=upon_dir_conflict,
            upon_opposite_entry=upon_opposite_entry,
            val_price=val_price,
            open=open,
            high=high,
            low=low,
            close=close,
            sl_stop=sl_stop,
            sl_trail=sl_trail,
            tp_stop=tp_stop,
            stop_entry_price=stop_entry_price,
            stop_exit_price=stop_exit_price,
            upon_stop_exit=upon_stop_exit,
            upon_stop_update=upon_stop_update
        )
        if not signal_func_mode:
            if ls_mode:
                broadcastable_args['entries'] = entries
                broadcastable_args['exits'] = exits
                broadcastable_args['short_entries'] = short_entries
                broadcastable_args['short_exits'] = short_exits
            else:
                broadcastable_args['entries'] = entries
                broadcastable_args['exits'] = exits
                broadcastable_args['direction'] = direction
        broadcastable_args = {**broadcastable_args, **broadcast_named_args}
        # Only close is broadcast, others can remain unchanged thanks to flexible indexing
        close_idx = list(broadcastable_args.keys()).index('close')
        keep_raw = [True] * len(broadcastable_args)
        keep_raw[close_idx] = False
        broadcast_kwargs = merge_dicts(dict(
            keep_raw=keep_raw,
            require_kwargs=dict(requirements='W')
        ), broadcast_kwargs)
        broadcasted_args = broadcast(*broadcastable_args.values(), **broadcast_kwargs)
        broadcasted_args = dict(zip(broadcastable_args.keys(), broadcasted_args))
        close = broadcasted_args['close']
        if not checks.is_pandas(close):
            close = pd.Series(close) if close.ndim == 1 else pd.DataFrame(close)
        broadcasted_args['close'] = to_2d_array(close)
        target_shape_2d = (close.shape[0], close.shape[1] if close.ndim > 1 else 1)
        wrapper = ArrayWrapper.from_obj(close, freq=freq, group_by=group_by, **wrapper_kwargs)
        cs_group_lens = wrapper.grouper.get_group_lens(group_by=None if cash_sharing else False)
        init_cash = np.require(np.broadcast_to(init_cash, (len(cs_group_lens),)), dtype=np.float64)
        group_lens = wrapper.grouper.get_group_lens(group_by=group_by)
        if checks.is_any_array(call_seq):
            call_seq = nb.require_call_seq(broadcast(call_seq, to_shape=target_shape_2d, to_pd=False))
        else:
            call_seq = nb.build_call_seq(target_shape_2d, group_lens, call_seq_type=call_seq)
        if max_orders is None:
            max_orders = target_shape_2d[0] * target_shape_2d[1]
        if max_logs is None:
            max_logs = target_shape_2d[0] * target_shape_2d[1]
        if not np.any(log):
            max_logs = 1
        template_mapping = {**broadcasted_args, **dict(
            target_shape=target_shape_2d,
            group_lens=cs_group_lens,
            init_cash=init_cash,
            call_seq=call_seq,
            adjust_sl_func_nb=adjust_sl_func_nb,
            adjust_sl_args=adjust_sl_args,
            adjust_tp_func_nb=adjust_tp_func_nb,
            adjust_tp_args=adjust_tp_args,
            use_stops=use_stops,
            auto_call_seq=auto_call_seq,
            ffill_val_price=ffill_val_price,
            update_value=update_value,
            max_orders=max_orders,
            max_logs=max_logs,
            flex_2d=close.ndim == 2,
            wrapper=wrapper
        ), **template_mapping}
        adjust_sl_args = deep_substitute(adjust_sl_args, template_mapping)
        adjust_tp_args = deep_substitute(adjust_tp_args, template_mapping)
        if signal_func_mode:
            signal_args = deep_substitute(signal_args, template_mapping)
        else:
            if ls_mode:
                signal_args = (
                    broadcasted_args['entries'],
                    broadcasted_args['exits'],
                    broadcasted_args['short_entries'],
                    broadcasted_args['short_exits']
                )
            else:
                signal_args = (
                    broadcasted_args['entries'],
                    broadcasted_args['exits'],
                    broadcasted_args['direction']
                )
        checks.assert_numba_func(signal_func_nb)
        checks.assert_numba_func(adjust_sl_func_nb)
        checks.assert_numba_func(adjust_tp_func_nb)

        # Perform the simulation
        order_records, log_records = nb.simulate_from_signal_func_nb(
            target_shape_2d,
            cs_group_lens,  # group only if cash sharing is enabled to speed up
            init_cash,
            call_seq,
            signal_func_nb=signal_func_nb,
            signal_args=signal_args,
            size=broadcasted_args['size'],
            price=broadcasted_args['price'],
            size_type=broadcasted_args['size_type'],
            fees=broadcasted_args['fees'],
            fixed_fees=broadcasted_args['fixed_fees'],
            slippage=broadcasted_args['slippage'],
            min_size=broadcasted_args['min_size'],
            max_size=broadcasted_args['max_size'],
            size_granularity=broadcasted_args['size_granularity'],
            reject_prob=broadcasted_args['reject_prob'],
            lock_cash=broadcasted_args['lock_cash'],
            allow_partial=broadcasted_args['allow_partial'],
            raise_reject=broadcasted_args['raise_reject'],
            log=broadcasted_args['log'],
            accumulate=broadcasted_args['accumulate'],
            upon_long_conflict=broadcasted_args['upon_long_conflict'],
            upon_short_conflict=broadcasted_args['upon_short_conflict'],
            upon_dir_conflict=broadcasted_args['upon_dir_conflict'],
            upon_opposite_entry=broadcasted_args['upon_opposite_entry'],
            val_price=broadcasted_args['val_price'],
            open=broadcasted_args['open'],
            high=broadcasted_args['high'],
            low=broadcasted_args['low'],
            close=broadcasted_args['close'],
            sl_stop=broadcasted_args['sl_stop'],
            sl_trail=broadcasted_args['sl_trail'],
            tp_stop=broadcasted_args['tp_stop'],
            stop_entry_price=broadcasted_args['stop_entry_price'],
            stop_exit_price=broadcasted_args['stop_exit_price'],
            upon_stop_exit=broadcasted_args['upon_stop_exit'],
            upon_stop_update=broadcasted_args['upon_stop_update'],
            adjust_sl_func_nb=adjust_sl_func_nb,
            adjust_sl_args=adjust_sl_args,
            adjust_tp_func_nb=adjust_tp_func_nb,
            adjust_tp_args=adjust_tp_args,
            use_stops=use_stops,
            auto_call_seq=auto_call_seq,
            ffill_val_price=ffill_val_price,
            update_value=update_value,
            max_orders=max_orders,
            max_logs=max_logs,
            flex_2d=close.ndim == 2
        )

        # Create an instance
        return cls(
            wrapper,
            close,
            order_records,
            log_records,
            init_cash if init_cash_mode is None else init_cash_mode,
            cash_sharing,
            call_seq=call_seq if attach_call_seq else None,
            **kwargs
        )

    @classmethod
    def from_holding(cls: tp.Type[PortfolioT], close: tp.ArrayLike, **kwargs) -> PortfolioT:
        """Simulate portfolio from holding.

        Based on `Portfolio.from_signals`.

        ```pycon
        >>> close = pd.Series([1, 2, 3, 4, 5])
        >>> pf = vbt.Portfolio.from_holding(close)
        >>> pf.final_value()
        500.0
        ```"""
        return cls.from_signals(close, entries=True, exits=False, **kwargs)

    @classmethod
    def from_random_signals(cls: tp.Type[PortfolioT],
                            close: tp.ArrayLike,
                            n: tp.Optional[tp.ArrayLike] = None,
                            prob: tp.Optional[tp.ArrayLike] = None,
                            entry_prob: tp.Optional[tp.ArrayLike] = None,
                            exit_prob: tp.Optional[tp.ArrayLike] = None,
                            param_product: bool = False,
                            seed: tp.Optional[int] = None,
                            run_kwargs: tp.KwargsLike = None,
                            **kwargs) -> PortfolioT:
        """Simulate portfolio from random entry and exit signals.

        Generates signals based either on the number of signals `n` or the probability
        of encountering a signal `prob`.

        * If `n` is set, see `vectorbt.signals.generators.RANDNX`.
        * If `prob` is set, see `vectorbt.signals.generators.RPROBNX`.

        Based on `Portfolio.from_signals`.

        !!! note
            To generate random signals, the shape of `close` is used. Broadcasting with other
            arrays happens after the generation.

        Usage:
            * Test multiple combinations of random entries and exits:

            ```pycon
            >>> close = pd.Series([1, 2, 3, 4, 5])
            >>> pf = vbt.Portfolio.from_random_signals(close, n=[2, 1, 0], seed=42)
            >>> pf.orders.count()
            randnx_n
            2    4
            1    2
            0    0
            Name: count, dtype: int64
            ```

            * Test the Cartesian product of entry and exit encounter probabilities:

            ```pycon
            >>> pf = vbt.Portfolio.from_random_signals(
            ...     close,
            ...     entry_prob=[0, 0.5, 1],
            ...     exit_prob=[0, 0.5, 1],
            ...     param_product=True,
            ...     seed=42)
            >>> pf.orders.count()
            rprobnx_entry_prob  rprobnx_exit_prob
            0.0                 0.0                  0
                                0.5                  0
                                1.0                  0
            0.5                 0.0                  1
                                0.5                  4
                                1.0                  3
            1.0                 0.0                  1
                                0.5                  4
                                1.0                  5
            Name: count, dtype: int64
            ```
        """
        from vectorbt._settings import settings
        portfolio_cfg = settings['portfolio']

        close = to_pd_array(close)
        close_wrapper = ArrayWrapper.from_obj(close)
        if entry_prob is None:
            entry_prob = prob
        if exit_prob is None:
            exit_prob = prob
        if seed is None:
            seed = portfolio_cfg['seed']
        if run_kwargs is None:
            run_kwargs = {}

        if n is not None and (entry_prob is not None or exit_prob is not None):
            raise ValueError("Either n or entry_prob and exit_prob should be set")
        if n is not None:
            rand = RANDNX.run(
                n=n,
                input_shape=close.shape,
                input_index=close_wrapper.index,
                input_columns=close_wrapper.columns,
                seed=seed,
                **run_kwargs
            )
            entries = rand.entries
            exits = rand.exits
        elif entry_prob is not None and exit_prob is not None:
            rprobnx = RPROBNX.run(
                entry_prob=entry_prob,
                exit_prob=exit_prob,
                param_product=param_product,
                input_shape=close.shape,
                input_index=close_wrapper.index,
                input_columns=close_wrapper.columns,
                seed=seed,
                **run_kwargs
            )
            entries = rprobnx.entries
            exits = rprobnx.exits
        else:
            raise ValueError("At least n or entry_prob and exit_prob should be set")

        return cls.from_signals(close, entries, exits, seed=seed, **kwargs)

    @classmethod
    def from_order_func(cls: tp.Type[PortfolioT],
                        close: tp.ArrayLike,
                        order_func_nb: tp.Union[nb.OrderFuncT, nb.FlexOrderFuncT],
                        *order_args,
                        flexible: tp.Optional[bool] = None,
                        init_cash: tp.Optional[tp.ArrayLike] = None,
                        cash_sharing: tp.Optional[bool] = None,
                        call_seq: tp.Optional[tp.ArrayLike] = None,
                        segment_mask: tp.Optional[tp.ArrayLike] = None,
                        call_pre_segment: tp.Optional[bool] = None,
                        call_post_segment: tp.Optional[bool] = None,
                        pre_sim_func_nb: nb.PreSimFuncT = nb.no_pre_func_nb,
                        pre_sim_args: tp.Args = (),
                        post_sim_func_nb: nb.PostSimFuncT = nb.no_post_func_nb,
                        post_sim_args: tp.Args = (),
                        pre_group_func_nb: nb.PreGroupFuncT = nb.no_pre_func_nb,
                        pre_group_args: tp.Args = (),
                        post_group_func_nb: nb.PostGroupFuncT = nb.no_post_func_nb,
                        post_group_args: tp.Args = (),
                        pre_row_func_nb: nb.PreRowFuncT = nb.no_pre_func_nb,
                        pre_row_args: tp.Args = (),
                        post_row_func_nb: nb.PostRowFuncT = nb.no_post_func_nb,
                        post_row_args: tp.Args = (),
                        pre_segment_func_nb: nb.PreSegmentFuncT = nb.no_pre_func_nb,
                        pre_segment_args: tp.Args = (),
                        post_segment_func_nb: nb.PostSegmentFuncT = nb.no_post_func_nb,
                        post_segment_args: tp.Args = (),
                        post_order_func_nb: nb.PostOrderFuncT = nb.no_post_func_nb,
                        post_order_args: tp.Args = (),
                        ffill_val_price: tp.Optional[bool] = None,
                        update_value: tp.Optional[bool] = None,
                        fill_pos_record: tp.Optional[bool] = None,
                        row_wise: tp.Optional[bool] = None,
                        use_numba: tp.Optional[bool] = None,
                        max_orders: tp.Optional[int] = None,
                        max_logs: tp.Optional[int] = None,
                        seed: tp.Optional[int] = None,
                        group_by: tp.GroupByLike = None,
                        broadcast_named_args: tp.KwargsLike = None,
                        broadcast_kwargs: tp.KwargsLike = None,
                        template_mapping: tp.Optional[tp.Mapping] = None,
                        wrapper_kwargs: tp.KwargsLike = None,
                        freq: tp.Optional[tp.FrequencyLike] = None,
                        attach_call_seq: tp.Optional[bool] = None,
                        **kwargs) -> PortfolioT:
        """Build portfolio from a custom order function.

        !!! hint
            See `vectorbt.portfolio.nb.simulate_nb` for illustrations and argument definitions.

        For more details on individual simulation functions:

        * not `row_wise` and not `flexible`: See `vectorbt.portfolio.nb.simulate_nb`
        * not `row_wise` and `flexible`: See `vectorbt.portfolio.nb.flex_simulate_nb`
        * `row_wise` and not `flexible`: See `vectorbt.portfolio.nb.simulate_row_wise_nb`
        * `row_wise` and `flexible`: See `vectorbt.portfolio.nb.flex_simulate_row_wise_nb`

        Args:
            close (array_like): Last asset price at each time step.
                Will broadcast to `target_shape`.

                Used for calculating unrealized PnL and portfolio value.
            order_func_nb (callable): Order generation function.
            *order_args: Arguments passed to `order_func_nb`.
            flexible (bool): Whether to simulate using a flexible order function.

                This lifts the limit of one order per tick and symbol.
            init_cash (InitCashMode, float or array_like of float): Initial capital.

                See `init_cash` in `Portfolio.from_orders`.
            cash_sharing (bool): Whether to share cash within the same group.

                If `group_by` is None, `group_by` becomes True to form a single group with cash sharing.
            call_seq (CallSeqType or array_like): Default sequence of calls per row and group.

                * Use `vectorbt.portfolio.enums.CallSeqType` to select a sequence type.
                * Set to array to specify custom sequence. Will not broadcast.

                !!! note
                    CallSeqType.Auto should be implemented manually.
                    Use `vectorbt.portfolio.nb.sort_call_seq_nb` or `vectorbt.portfolio.nb.sort_call_seq_out_nb`
                    in `pre_segment_func_nb`.
            segment_mask (int or array_like of bool): Mask of whether a particular segment should be executed.

                Supplying an integer will activate every n-th row.
                Supplying a boolean or an array of boolean will broadcast to the number of rows and groups.

                Does not broadcast together with `close` and `broadcast_named_args`, only against the final shape.
            call_pre_segment (bool): Whether to call `pre_segment_func_nb` regardless of `segment_mask`.
            call_post_segment (bool): Whether to call `post_segment_func_nb` regardless of `segment_mask`.
            pre_sim_func_nb (callable): Function called before simulation.
                Defaults to `vectorbt.portfolio.nb.no_pre_func_nb`.
            pre_sim_args (tuple): Packed arguments passed to `pre_sim_func_nb`.
                Defaults to `()`.
            post_sim_func_nb (callable): Function called after simulation.
                Defaults to `vectorbt.portfolio.nb.no_post_func_nb`.
            post_sim_args (tuple): Packed arguments passed to `post_sim_func_nb`.
                Defaults to `()`.
            pre_group_func_nb (callable): Function called before each group.
                Defaults to `vectorbt.portfolio.nb.no_pre_func_nb`.

                Called only if `row_wise` is False.
            pre_group_args (tuple): Packed arguments passed to `pre_group_func_nb`.
                Defaults to `()`.
            post_group_func_nb (callable): Function called after each group.
                Defaults to `vectorbt.portfolio.nb.no_post_func_nb`.

                Called only if `row_wise` is False.
            post_group_args (tuple): Packed arguments passed to `post_group_func_nb`.
                Defaults to `()`.
            pre_row_func_nb (callable): Function called before each row.
                Defaults to `vectorbt.portfolio.nb.no_pre_func_nb`.

                Called only if `row_wise` is True.
            pre_row_args (tuple): Packed arguments passed to `pre_row_func_nb`.
                Defaults to `()`.
            post_row_func_nb (callable): Function called after each row.
                Defaults to `vectorbt.portfolio.nb.no_post_func_nb`.

                Called only if `row_wise` is True.
            post_row_args (tuple): Packed arguments passed to `post_row_func_nb`.
                Defaults to `()`.
            pre_segment_func_nb (callable): Function called before each segment.
                Defaults to `vectorbt.portfolio.nb.no_pre_func_nb`.
            pre_segment_args (tuple): Packed arguments passed to `pre_segment_func_nb`.
                Defaults to `()`.
            post_segment_func_nb (callable): Function called after each segment.
                Defaults to `vectorbt.portfolio.nb.no_post_func_nb`.
            post_segment_args (tuple): Packed arguments passed to `post_segment_func_nb`.
                Defaults to `()`.
            post_order_func_nb (callable): Callback that is called after the order has been processed.
            post_order_args (tuple): Packed arguments passed to `post_order_func_nb`.
                Defaults to `()`.
            ffill_val_price (bool): Whether to track valuation price only if it's known.

                Otherwise, unknown `close` will lead to NaN in valuation price at the next timestamp.
            update_value (bool): Whether to update group value after each filled order.
            fill_pos_record (bool): Whether to fill position record.

                Disable this to make simulation a bit faster for simple use cases.
            row_wise (bool): Whether to iterate over rows rather than columns/groups.
            use_numba (bool): Whether to run the main simulation function using Numba.

                !!! note
                    Disabling it does not disable Numba for other functions.
                    If necessary, you should ensure that every other function does not uses Numba as well.
                    You can do this by using the `py_func` attribute of that function.
                    Or, you could disable Numba globally by doing `os.environ['NUMBA_DISABLE_JIT'] = '1'`.
            max_orders (int): Size of the order records array.
                Defaults to the number of elements in the broadcasted shape.

                Set to a lower number if you run out of memory.
            max_logs (int): Size of the log records array.
                Defaults to the number of elements in the broadcasted shape.

                Set to a lower number if you run out of memory.
            seed (int): See `Portfolio.from_orders`.
            group_by (any): See `Portfolio.from_orders`.
            broadcast_named_args (dict): See `Portfolio.from_signals`.
            broadcast_kwargs (dict): See `Portfolio.from_orders`.
            template_mapping (mapping): See `Portfolio.from_signals`.
            wrapper_kwargs (dict): See `Portfolio.from_orders`.
            freq (any): See `Portfolio.from_orders`.
            attach_call_seq (bool): See `Portfolio.from_orders`.
            **kwargs: Keyword arguments passed to the `__init__` method.

        For defaults, see `portfolio` in `vectorbt._settings.settings`.

        !!! note
            All passed functions should be Numba-compiled if Numba is enabled.

            Also see notes on `Portfolio.from_orders`.

        !!! note
            In contrast to other methods, the valuation price is previous `close` instead of the order price
            since the price of an order is unknown before the call (which is more realistic by the way).
            You can still override the valuation price in `pre_segment_func_nb`.

        Usage:
            * Buy 10 units each tick using closing price:

            ```pycon
            >>> @njit
            ... def order_func_nb(c, size):
            ...     return nb.order_nb(size=size)

            >>> close = pd.Series([1, 2, 3, 4, 5])
            >>> pf = vbt.Portfolio.from_order_func(close, order_func_nb, 10)

            >>> pf.assets()
            0    10.0
            1    20.0
            2    30.0
            3    40.0
            4    40.0
            dtype: float64
            >>> pf.cash()
            0    90.0
            1    70.0
            2    40.0
            3     0.0
            4     0.0
            dtype: float64
            ```

            * Reverse each position by first closing it. Keep state of last position to determine
            which position to open next (just as an example, there are easier ways to do this):

            ```pycon
            >>> @njit
            ... def pre_group_func_nb(c):
            ...     last_pos_state = np.array([-1])
            ...     return (last_pos_state,)

            >>> @njit
            ... def order_func_nb(c, last_pos_state):
            ...     if c.position_now != 0:
            ...         return nb.close_position_nb()
            ...
            ...     if last_pos_state[0] == 1:
            ...         size = -np.inf  # open short
            ...         last_pos_state[0] = -1
            ...     else:
            ...         size = np.inf  # open long
            ...         last_pos_state[0] = 1
            ...     return nb.order_nb(size=size)

            >>> pf = vbt.Portfolio.from_order_func(
            ...     close,
            ...     order_func_nb,
            ...     pre_group_func_nb=pre_group_func_nb
            ... )

            >>> pf.assets()
            0    100.000000
            1      0.000000
            2    -66.666667
            3      0.000000
            4     26.666667
            dtype: float64
            >>> pf.cash()
            0      0.000000
            1    200.000000
            2    400.000000
            3    133.333333
            4      0.000000
            dtype: float64
            ```

            * Equal-weighted portfolio as in the example under `vectorbt.portfolio.nb.simulate_nb`:

            ```pycon
            >>> @njit
            ... def pre_group_func_nb(c):
            ...     order_value_out = np.empty(c.group_len, dtype=np.float64)
            ...     return (order_value_out,)

            >>> @njit
            ... def pre_segment_func_nb(c, order_value_out, size, price, size_type, direction):
            ...     for col in range(c.from_col, c.to_col):
            ...         c.last_val_price[col] = nb.get_col_elem_nb(c, col, price)
            ...     nb.sort_call_seq_nb(c, size, size_type, direction, order_value_out)
            ...     return ()

            >>> @njit
            ... def order_func_nb(c, size, price, size_type, direction, fees, fixed_fees, slippage):
            ...     return nb.order_nb(
            ...         size=nb.get_elem_nb(c, size),
            ...         price=nb.get_elem_nb(c, price),
            ...         size_type=nb.get_elem_nb(c, size_type),
            ...         direction=nb.get_elem_nb(c, direction),
            ...         fees=nb.get_elem_nb(c, fees),
            ...         fixed_fees=nb.get_elem_nb(c, fixed_fees),
            ...         slippage=nb.get_elem_nb(c, slippage)
            ...     )

            >>> np.random.seed(42)
            >>> close = np.random.uniform(1, 10, size=(5, 3))
            >>> size_template = vbt.RepEval('np.asarray(1 / group_lens[0])')

            >>> pf = vbt.Portfolio.from_order_func(
            ...     close,
            ...     order_func_nb,
            ...     size_template,  # order_args as *args
            ...     vbt.Rep('price'),
            ...     vbt.Rep('size_type'),
            ...     vbt.Rep('direction'),
            ...     vbt.Rep('fees'),
            ...     vbt.Rep('fixed_fees'),
            ...     vbt.Rep('slippage'),
            ...     segment_mask=2,  # rebalance every second tick
            ...     pre_group_func_nb=pre_group_func_nb,
            ...     pre_segment_func_nb=pre_segment_func_nb,
            ...     pre_segment_args=(
            ...         size_template,
            ...         vbt.Rep('price'),
            ...         vbt.Rep('size_type'),
            ...         vbt.Rep('direction')
            ...     ),
            ...     broadcast_named_args=dict(  # broadcast against each other
            ...         price=close,
            ...         size_type=SizeType.TargetPercent,
            ...         direction=Direction.LongOnly,
            ...         fees=0.001,
            ...         fixed_fees=1.,
            ...         slippage=0.001
            ...     ),
            ...     template_mapping=dict(np=np),  # required by size_template
            ...     cash_sharing=True, group_by=True,  # one group with cash sharing
            ... )

            >>> pf.asset_value(group_by=False).vbt.plot()
            ```

            ![](/assets/images/simulate_nb.svg)

            Templates are a very powerful tool to prepare any custom arguments after they are broadcast and
            before they are passed to the simulation function. In the example above, we use `broadcast_named_args`
            to broadcast some arguments against each other and templates to pass those objects to callbacks.
            Additionally, we used an evaluation template to compute the size based on the number of assets in each group.

            You may ask: why should we bother using broadcasting and templates if we could just pass `size=1/3`?
            Because of flexibility those features provide: we can now pass whatever parameter combinations we want
            and it will work flawlessly. For example, to create two groups of equally-allocated positions,
            we need to change only two parameters:

            ```pycon
            >>> close = np.random.uniform(1, 10, size=(5, 6))  # 6 columns instead of 3
            >>> group_by = ['g1', 'g1', 'g1', 'g2', 'g2', 'g2']  # 2 groups instead of 1

            >>> pf['g1'].asset_value(group_by=False).vbt.plot()
            >>> pf['g2'].asset_value(group_by=False).vbt.plot()
            ```

            ![](/assets/images/from_order_func_g1.svg)

            ![](/assets/images/from_order_func_g2.svg)

            * Combine multiple exit conditions. Exit early if the price hits some threshold before an actual exit:

            ```pycon
            >>> @njit
            ... def pre_sim_func_nb(c):
            ...     # We need to define stop price per column once
            ...     stop_price = np.full(c.target_shape[1], np.nan, dtype=np.float64)
            ...     return (stop_price,)

            >>> @njit
            ... def order_func_nb(c, stop_price, entries, exits, size):
            ...     # Select info related to this order
            ...     entry_now = nb.get_elem_nb(c, entries)
            ...     exit_now = nb.get_elem_nb(c, exits)
            ...     size_now = nb.get_elem_nb(c, size)
            ...     price_now = nb.get_elem_nb(c, c.close)
            ...     stop_price_now = stop_price[c.col]
            ...
            ...     # Our logic
            ...     if entry_now:
            ...         if c.position_now == 0:
            ...             return nb.order_nb(
            ...                 size=size_now,
            ...                 price=price_now,
            ...                 direction=Direction.LongOnly)
            ...     elif exit_now or price_now >= stop_price_now:
            ...         if c.position_now > 0:
            ...             return nb.order_nb(
            ...                 size=-size_now,
            ...                 price=price_now,
            ...                 direction=Direction.LongOnly)
            ...     return NoOrder

            >>> @njit
            ... def post_order_func_nb(c, stop_price, stop):
            ...     # Same broadcasting as for size
            ...     stop_now = nb.get_elem_nb(c, stop)
            ...
            ...     if c.order_result.status == OrderStatus.Filled:
            ...         if c.order_result.side == OrderSide.Buy:
            ...             # Position entered: Set stop condition
            ...             stop_price[c.col] = (1 + stop_now) * c.order_result.price
            ...         else:
            ...             # Position exited: Remove stop condition
            ...             stop_price[c.col] = np.nan

            >>> def simulate(close, entries, exits, size, threshold):
            ...     return vbt.Portfolio.from_order_func(
            ...         close,
            ...         order_func_nb,
            ...         vbt.Rep('entries'), vbt.Rep('exits'), vbt.Rep('size'),  # order_args
            ...         pre_sim_func_nb=pre_sim_func_nb,
            ...         post_order_func_nb=post_order_func_nb,
            ...         post_order_args=(vbt.Rep('threshold'),),
            ...         broadcast_named_args=dict(  # broadcast against each other
            ...             entries=entries,
            ...             exits=exits,
            ...             size=size,
            ...             threshold=threshold
            ...         )
            ...     )

            >>> close = pd.Series([10, 11, 12, 13, 14])
            >>> entries = pd.Series([True, True, False, False, False])
            >>> exits = pd.Series([False, False, False, True, True])
            >>> simulate(close, entries, exits, np.inf, 0.1).asset_flow()
            0    10.0
            1     0.0
            2   -10.0
            3     0.0
            4     0.0
            dtype: float64

            >>> simulate(close, entries, exits, np.inf, 0.2).asset_flow()
            0    10.0
            1     0.0
            2   -10.0
            3     0.0
            4     0.0
            dtype: float64

            >>> simulate(close, entries, exits, np.nan).asset_flow()
            0    10.0
            1     0.0
            2     0.0
            3   -10.0
            4     0.0
            dtype: float64
            ```

            The reason why stop of 10% does not result in an order at the second time step is because
            it comes at the same time as entry, so it must wait until no entry is present.
            This can be changed by replacing the statement "elif" with "if", which would execute
            an exit regardless if an entry is present (similar to using `ConflictMode.Opposite` in
            `Portfolio.from_signals`).

            We can also test the parameter combinations above all at once (thanks to broadcasting):

            ```pycon
            >>> size = pd.DataFrame(
            ...     [[0.1, 0.2, np.nan]],
            ...     columns=pd.Index(['0.1', '0.2', 'nan'], name='size')
            ... )
            >>> simulate(close, entries, exits, np.inf, size).asset_flow()
            size   0.1   0.2   nan
            0     10.0  10.0  10.0
            1      0.0   0.0   0.0
            2    -10.0 -10.0   0.0
            3      0.0   0.0 -10.0
            4      0.0   0.0   0.0
            ```

            * Let's illustrate how to generate multiple orders per symbol and bar.
            For each bar, buy at open and sell at close:

            ```pycon
            >>> @njit
            ... def flex_order_func_nb(c, open, size):
            ...     if c.call_idx == 0:
            ...         return c.from_col, nb.order_nb(size=size, price=open[c.i, c.from_col])
            ...     if c.call_idx == 1:
            ...         return c.from_col, nb.close_position_nb(price=c.close[c.i, c.from_col])
            ...     return -1, NoOrder

            >>> open = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
            >>> close = pd.DataFrame({'a': [2, 3, 4], 'b': [3, 4, 5]})
            >>> size = 1
            >>> pf = vbt.Portfolio.from_order_func(
            ...     close,
            ...     flex_order_func_nb,
            ...     to_2d_array(open), size,
            ...     flexible=True, max_orders=close.shape[0] * close.shape[1] * 2)

            >>> pf.orders.records_readable
                Order Id  Timestamp Column  Size  Price  Fees  Side
            0          0          0      a   1.0    1.0   0.0   Buy
            1          1          0      a   1.0    2.0   0.0  Sell
            2          2          1      a   1.0    2.0   0.0   Buy
            3          3          1      a   1.0    3.0   0.0  Sell
            4          4          2      a   1.0    3.0   0.0   Buy
            5          5          2      a   1.0    4.0   0.0  Sell
            6          6          0      b   1.0    4.0   0.0   Buy
            7          7          0      b   1.0    3.0   0.0  Sell
            8          8          1      b   1.0    5.0   0.0   Buy
            9          9          1      b   1.0    4.0   0.0  Sell
            10        10          2      b   1.0    6.0   0.0   Buy
            11        11          2      b   1.0    5.0   0.0  Sell
            ```

            !!! warning
                Each bar is effectively a black box - we don't know how the price moves inside.
                Since trades must come in an order that replicates that of the real world, the only reliable
                pieces of information are the opening and the closing price.
        """
        # Get defaults
        from vectorbt._settings import settings
        portfolio_cfg = settings['portfolio']

        close = to_pd_array(close)
        if flexible is None:
            flexible = portfolio_cfg['flexible']
        if init_cash is None:
            init_cash = portfolio_cfg['init_cash']
        if isinstance(init_cash, str):
            init_cash = map_enum_fields(init_cash, InitCashMode)
        if isinstance(init_cash, int) and init_cash in InitCashMode:
            init_cash_mode = init_cash
            init_cash = np.inf
        else:
            init_cash_mode = None
        if cash_sharing is None:
            cash_sharing = portfolio_cfg['cash_sharing']
        if cash_sharing and group_by is None:
            group_by = True
        if not flexible:
            if call_seq is None:
                call_seq = portfolio_cfg['call_seq']
            call_seq = map_enum_fields(call_seq, CallSeqType)
            if isinstance(call_seq, int):
                if call_seq == CallSeqType.Auto:
                    raise ValueError("CallSeqType.Auto must be implemented manually. "
                                     "Use sort_call_seq_nb in pre_segment_func_nb.")
        if segment_mask is None:
            segment_mask = True
        if call_pre_segment is None:
            call_pre_segment = portfolio_cfg['call_pre_segment']
        if call_post_segment is None:
            call_post_segment = portfolio_cfg['call_post_segment']
        if ffill_val_price is None:
            ffill_val_price = portfolio_cfg['ffill_val_price']
        if update_value is None:
            update_value = portfolio_cfg['update_value']
        if fill_pos_record is None:
            fill_pos_record = portfolio_cfg['fill_pos_record']
        if row_wise is None:
            row_wise = portfolio_cfg['row_wise']
        if use_numba is None:
            use_numba = portfolio_cfg['use_numba']
        if seed is None:
            seed = portfolio_cfg['seed']
        if seed is not None:
            set_seed(seed)
        if freq is None:
            freq = portfolio_cfg['freq']
        if attach_call_seq is None:
            attach_call_seq = portfolio_cfg['attach_call_seq']
        if broadcast_named_args is None:
            broadcast_named_args = {}
        if broadcast_kwargs is None:
            broadcast_kwargs = {}
        require_kwargs = dict(require_kwargs=dict(requirements='W'))
        broadcast_kwargs = merge_dicts(require_kwargs, broadcast_kwargs)
        if template_mapping is None:
            template_mapping = {}
        if wrapper_kwargs is None:
            wrapper_kwargs = {}
        if not wrapper_kwargs.get('group_select', True) and cash_sharing:
            raise ValueError("group_select cannot be disabled if cash_sharing=True")

        # Prepare the simulation
        broadcastable_args = {**dict(close=close), **broadcast_named_args}
        if len(broadcastable_args) > 1:
            close_idx = list(broadcastable_args.keys()).index('close')
            keep_raw = [True] * len(broadcastable_args)
            keep_raw[close_idx] = False
            broadcast_kwargs = merge_dicts(dict(
                keep_raw=keep_raw,
                require_kwargs=dict(requirements='W')
            ), broadcast_kwargs)
            broadcasted_args = broadcast(*broadcastable_args.values(), **broadcast_kwargs)
            broadcasted_args = dict(zip(broadcastable_args.keys(), broadcasted_args))
            close = broadcasted_args['close']
            if not checks.is_pandas(close):
                close = pd.Series(close) if close.ndim == 1 else pd.DataFrame(close)
        else:
            broadcasted_args = broadcastable_args
        broadcasted_args['close'] = to_2d_array(close)
        target_shape_2d = (close.shape[0], close.shape[1] if close.ndim > 1 else 1)
        wrapper = ArrayWrapper.from_obj(close, freq=freq, group_by=group_by, **wrapper_kwargs)
        cs_group_lens = wrapper.grouper.get_group_lens(group_by=None if cash_sharing else False)
        init_cash = np.require(np.broadcast_to(init_cash, (len(cs_group_lens),)), dtype=np.float64)
        group_lens = wrapper.grouper.get_group_lens(group_by=group_by)
        if isinstance(segment_mask, int):
            _segment_mask = np.full((target_shape_2d[0], len(group_lens)), False)
            _segment_mask[0::segment_mask] = True
            segment_mask = _segment_mask
        else:
            segment_mask = broadcast(
                segment_mask,
                to_shape=(target_shape_2d[0], len(group_lens)),
                to_pd=False,
                **require_kwargs
            )
        if not flexible:
            if checks.is_any_array(call_seq):
                call_seq = nb.require_call_seq(broadcast(call_seq, to_shape=target_shape_2d, to_pd=False))
            else:
                call_seq = nb.build_call_seq(target_shape_2d, group_lens, call_seq_type=call_seq)
        if max_orders is None:
            max_orders = target_shape_2d[0] * target_shape_2d[1]
        if max_logs is None:
            max_logs = target_shape_2d[0] * target_shape_2d[1]
        template_mapping = {**broadcasted_args, **dict(
            target_shape=target_shape_2d,
            group_lens=group_lens,
            init_cash=init_cash,
            cash_sharing=cash_sharing,
            segment_mask=segment_mask,
            call_pre_segment=call_pre_segment,
            call_post_segment=call_post_segment,
            pre_sim_func_nb=pre_sim_func_nb,
            pre_sim_args=pre_sim_args,
            post_sim_func_nb=post_sim_func_nb,
            post_sim_args=post_sim_args,
            pre_group_func_nb=pre_group_func_nb,
            pre_group_args=pre_group_args,
            post_group_func_nb=post_group_func_nb,
            post_group_args=post_group_args,
            pre_row_func_nb=pre_row_func_nb,
            pre_row_args=pre_row_args,
            post_row_func_nb=post_row_func_nb,
            post_row_args=post_row_args,
            pre_segment_func_nb=pre_segment_func_nb,
            pre_segment_args=pre_segment_args,
            post_segment_func_nb=post_segment_func_nb,
            post_segment_args=post_segment_args,
            flex_order_func_nb=order_func_nb,
            flex_order_args=order_args,
            post_order_func_nb=post_order_func_nb,
            post_order_args=post_order_args,
            ffill_val_price=ffill_val_price,
            update_value=update_value,
            fill_pos_record=fill_pos_record,
            max_orders=max_orders,
            max_logs=max_logs,
            flex_2d=close.ndim == 2,
            wrapper=wrapper
        ), **template_mapping}
        pre_sim_args = deep_substitute(pre_sim_args, template_mapping)
        post_sim_args = deep_substitute(post_sim_args, template_mapping)
        pre_group_args = deep_substitute(pre_group_args, template_mapping)
        post_group_args = deep_substitute(post_group_args, template_mapping)
        pre_row_args = deep_substitute(pre_row_args, template_mapping)
        post_row_args = deep_substitute(post_row_args, template_mapping)
        pre_segment_args = deep_substitute(pre_segment_args, template_mapping)
        post_segment_args = deep_substitute(post_segment_args, template_mapping)
        order_args = deep_substitute(order_args, template_mapping)
        post_order_args = deep_substitute(post_order_args, template_mapping)
        if use_numba:
            checks.assert_numba_func(pre_sim_func_nb)
            checks.assert_numba_func(post_sim_func_nb)
            checks.assert_numba_func(pre_group_func_nb)
            checks.assert_numba_func(post_group_func_nb)
            checks.assert_numba_func(pre_row_func_nb)
            checks.assert_numba_func(post_row_func_nb)
            checks.assert_numba_func(pre_segment_func_nb)
            checks.assert_numba_func(post_segment_func_nb)
            checks.assert_numba_func(order_func_nb)
            checks.assert_numba_func(post_order_func_nb)

        # Perform the simulation
        if row_wise:
            if flexible:
                simulate_func = nb.flex_simulate_row_wise_nb
                if not use_numba and hasattr(simulate_func, 'py_func'):
                    simulate_func = simulate_func.py_func
                order_records, log_records = simulate_func(
                    target_shape=target_shape_2d,
                    group_lens=group_lens,
                    init_cash=init_cash,
                    cash_sharing=cash_sharing,
                    segment_mask=segment_mask,
                    call_pre_segment=call_pre_segment,
                    call_post_segment=call_post_segment,
                    pre_sim_func_nb=pre_sim_func_nb,
                    pre_sim_args=pre_sim_args,
                    post_sim_func_nb=post_sim_func_nb,
                    post_sim_args=post_sim_args,
                    pre_row_func_nb=pre_row_func_nb,
                    pre_row_args=pre_row_args,
                    post_row_func_nb=post_row_func_nb,
                    post_row_args=post_row_args,
                    pre_segment_func_nb=pre_segment_func_nb,
                    pre_segment_args=pre_segment_args,
                    post_segment_func_nb=post_segment_func_nb,
                    post_segment_args=post_segment_args,
                    flex_order_func_nb=order_func_nb,
                    flex_order_args=order_args,
                    post_order_func_nb=post_order_func_nb,
                    post_order_args=post_order_args,
                    close=broadcasted_args['close'],
                    ffill_val_price=ffill_val_price,
                    update_value=update_value,
                    fill_pos_record=fill_pos_record,
                    max_orders=max_orders,
                    max_logs=max_logs,
                    flex_2d=close.ndim == 2
                )
            else:
                simulate_func = nb.simulate_row_wise_nb
                if not use_numba and hasattr(simulate_func, 'py_func'):
                    simulate_func = simulate_func.py_func
                order_records, log_records = simulate_func(
                    target_shape=target_shape_2d,
                    group_lens=group_lens,
                    init_cash=init_cash,
                    cash_sharing=cash_sharing,
                    call_seq=call_seq,
                    segment_mask=segment_mask,
                    call_pre_segment=call_pre_segment,
                    call_post_segment=call_post_segment,
                    pre_sim_func_nb=pre_sim_func_nb,
                    pre_sim_args=pre_sim_args,
                    post_sim_func_nb=post_sim_func_nb,
                    post_sim_args=post_sim_args,
                    pre_row_func_nb=pre_row_func_nb,
                    pre_row_args=pre_row_args,
                    post_row_func_nb=post_row_func_nb,
                    post_row_args=post_row_args,
                    pre_segment_func_nb=pre_segment_func_nb,
                    pre_segment_args=pre_segment_args,
                    post_segment_func_nb=post_segment_func_nb,
                    post_segment_args=post_segment_args,
                    order_func_nb=order_func_nb,
                    order_args=order_args,
                    post_order_func_nb=post_order_func_nb,
                    post_order_args=post_order_args,
                    close=broadcasted_args['close'],
                    ffill_val_price=ffill_val_price,
                    update_value=update_value,
                    fill_pos_record=fill_pos_record,
                    max_orders=max_orders,
                    max_logs=max_logs,
                    flex_2d=close.ndim == 2
                )
        else:
            if flexible:
                simulate_func = nb.flex_simulate_nb
                if not use_numba and hasattr(simulate_func, 'py_func'):
                    simulate_func = simulate_func.py_func
                order_records, log_records = simulate_func(
                    target_shape=target_shape_2d,
                    group_lens=group_lens,
                    init_cash=init_cash,
                    cash_sharing=cash_sharing,
                    segment_mask=segment_mask,
                    call_pre_segment=call_pre_segment,
                    call_post_segment=call_post_segment,
                    pre_sim_func_nb=pre_sim_func_nb,
                    pre_sim_args=pre_sim_args,
                    post_sim_func_nb=post_sim_func_nb,
                    post_sim_args=post_sim_args,
                    pre_group_func_nb=pre_group_func_nb,
                    pre_group_args=pre_group_args,
                    post_group_func_nb=post_group_func_nb,
                    post_group_args=post_group_args,
                    pre_segment_func_nb=pre_segment_func_nb,
                    pre_segment_args=pre_segment_args,
                    post_segment_func_nb=post_segment_func_nb,
                    post_segment_args=post_segment_args,
                    flex_order_func_nb=order_func_nb,
                    flex_order_args=order_args,
                    post_order_func_nb=post_order_func_nb,
                    post_order_args=post_order_args,
                    close=broadcasted_args['close'],
                    ffill_val_price=ffill_val_price,
                    update_value=update_value,
                    fill_pos_record=fill_pos_record,
                    max_orders=max_orders,
                    max_logs=max_logs,
                    flex_2d=close.ndim == 2
                )
            else:
                simulate_func = nb.simulate_nb
                if not use_numba and hasattr(simulate_func, 'py_func'):
                    simulate_func = simulate_func.py_func
                order_records, log_records = simulate_func(
                    target_shape=target_shape_2d,
                    group_lens=group_lens,
                    init_cash=init_cash,
                    cash_sharing=cash_sharing,
                    call_seq=call_seq,
                    segment_mask=segment_mask,
                    call_pre_segment=call_pre_segment,
                    call_post_segment=call_post_segment,
                    pre_sim_func_nb=pre_sim_func_nb,
                    pre_sim_args=pre_sim_args,
                    post_sim_func_nb=post_sim_func_nb,
                    post_sim_args=post_sim_args,
                    pre_group_func_nb=pre_group_func_nb,
                    pre_group_args=pre_group_args,
                    post_group_func_nb=post_group_func_nb,
                    post_group_args=post_group_args,
                    pre_segment_func_nb=pre_segment_func_nb,
                    pre_segment_args=pre_segment_args,
                    post_segment_func_nb=post_segment_func_nb,
                    post_segment_args=post_segment_args,
                    order_func_nb=order_func_nb,
                    order_args=order_args,
                    post_order_func_nb=post_order_func_nb,
                    post_order_args=post_order_args,
                    close=broadcasted_args['close'],
                    ffill_val_price=ffill_val_price,
                    update_value=update_value,
                    fill_pos_record=fill_pos_record,
                    max_orders=max_orders,
                    max_logs=max_logs,
                    flex_2d=close.ndim == 2
                )

        # Create an instance
        return cls(
            wrapper,
            close,
            order_records,
            log_records,
            init_cash if init_cash_mode is None else init_cash_mode,
            cash_sharing,
            call_seq=call_seq if not flexible and attach_call_seq else None,
            **kwargs
        )

    # ############# Properties ############# #

    @property
    def wrapper(self) -> ArrayWrapper:
        """Array wrapper."""
        if self.cash_sharing:
            # Allow only disabling grouping when needed (but not globally, see regroup)
            return self._wrapper.replace(
                allow_enable=False,
                allow_modify=False
            )
        return self._wrapper

    def regroup(self: PortfolioT, group_by: tp.GroupByLike, **kwargs) -> PortfolioT:
        """Regroup this object.

        See `vectorbt.base.array_wrapper.Wrapping.regroup`.

        !!! note
            All cached objects will be lost."""
        if self.cash_sharing:
            if self.wrapper.grouper.is_grouping_modified(group_by=group_by):
                raise ValueError("Cannot modify grouping globally when cash_sharing=True")
        return Wrapping.regroup(self, group_by, **kwargs)

    @property
    def cash_sharing(self) -> bool:
        """Whether to share cash within the same group."""
        return self._cash_sharing

    @property
    def call_seq(self, wrap_kwargs: tp.KwargsLike = None) -> tp.Optional[tp.SeriesFrame]:
        """Sequence of calls per row and group."""
        if self._call_seq is None:
            return None
        return self.wrapper.wrap(self._call_seq, group_by=False, **merge_dicts({}, wrap_kwargs))

    @property
    def fillna_close(self) -> bool:
        """Whether to forward-backward fill NaN values in `Portfolio.close`."""
        return self._fillna_close

    @property
    def trades_type(self) -> int:
        """Default `vectorbt.portfolio.trades.Trades` to use across `Portfolio`."""
        return self._trades_type

    # ############# Reference price ############# #

    @property
    def close(self) -> tp.SeriesFrame:
        """Price per unit series."""
        return self._close

    @cached_method
    def get_filled_close(self, wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Forward-backward-fill NaN values in `Portfolio.close`"""
        close = to_2d_array(self.close.ffill().bfill())
        return self.wrapper.wrap(close, group_by=False, **merge_dicts({}, wrap_kwargs))

    # ############# Records ############# #

    @property
    def order_records(self) -> tp.RecordArray:
        """A structured NumPy array of order records."""
        return self._order_records

    @cached_property
    def orders(self) -> Orders:
        """`Portfolio.get_orders` with default arguments."""
        return self.get_orders()

    @cached_method
    def get_orders(self, group_by: tp.GroupByLike = None, **kwargs) -> Orders:
        """Get order records.

        See `vectorbt.portfolio.orders.Orders`."""
        return Orders(self.wrapper, self.order_records, close=self.close, **kwargs).regroup(group_by)

    @property
    def log_records(self) -> tp.RecordArray:
        """A structured NumPy array of log records."""
        return self._log_records

    @cached_property
    def logs(self) -> Logs:
        """`Portfolio.get_logs` with default arguments."""
        return self.get_logs()

    @cached_method
    def get_logs(self, group_by: tp.GroupByLike = None, **kwargs) -> Logs:
        """Get log records.

        See `vectorbt.portfolio.logs.Logs`."""
        return Logs(self.wrapper, self.log_records, **kwargs).regroup(group_by)

    @cached_property
    def entry_trades(self) -> EntryTrades:
        """`Portfolio.get_entry_trades` with default arguments."""
        return self.get_entry_trades()

    @cached_method
    def get_entry_trades(self, group_by: tp.GroupByLike = None, **kwargs) -> EntryTrades:
        """Get entry trade records.

        See `vectorbt.portfolio.trades.EntryTrades`."""
        return EntryTrades.from_orders(self.orders, **kwargs).regroup(group_by)

    @cached_property
    def exit_trades(self) -> ExitTrades:
        """`Portfolio.get_exit_trades` with default arguments."""
        return self.get_exit_trades()

    @cached_method
    def get_exit_trades(self, group_by: tp.GroupByLike = None, **kwargs) -> ExitTrades:
        """Get exit trade records.

        See `vectorbt.portfolio.trades.ExitTrades`."""
        return ExitTrades.from_orders(self.orders, **kwargs).regroup(group_by)

    @cached_property
    def trades(self) -> Trades:
        """`Portfolio.get_trades` with default arguments."""
        return self.get_trades()

    @cached_property
    def positions(self) -> Positions:
        """`Portfolio.get_positions` with default arguments."""
        return self.get_positions()

    @cached_method
    def get_positions(self, group_by: tp.GroupByLike = None, **kwargs) -> Positions:
        """Get position records.

        See `vectorbt.portfolio.trades.Positions`."""
        return Positions.from_trades(self.exit_trades, **kwargs).regroup(group_by)

    @cached_method
    def get_trades(self, group_by: tp.GroupByLike = None, **kwargs) -> Trades:
        """Get trade/position records depending upon `Portfolio.trades_type`."""
        if self.trades_type == TradesType.EntryTrades:
            return self.get_entry_trades(group_by=group_by, **kwargs)
        elif self.trades_type == TradesType.ExitTrades:
            return self.get_exit_trades(group_by=group_by, **kwargs)
        return self.get_positions(group_by=group_by, **kwargs)

    @cached_property
    def drawdowns(self) -> Drawdowns:
        """`Portfolio.get_drawdowns` with default arguments."""
        return self.get_drawdowns()

    @cached_method
    def get_drawdowns(self, group_by: tp.GroupByLike = None, wrap_kwargs: tp.KwargsLike = None,
                      wrapper_kwargs: tp.KwargsLike = None, **kwargs) -> Drawdowns:
        """Get drawdown records from `Portfolio.value`.

        See `vectorbt.generic.drawdowns.Drawdowns`."""
        value = self.value(group_by=group_by, wrap_kwargs=wrap_kwargs)
        wrapper_kwargs = merge_dicts(self.orders.wrapper.config, wrapper_kwargs, dict(group_by=None))
        return Drawdowns.from_ts(value, wrapper_kwargs=wrapper_kwargs, **kwargs)

    # ############# Assets ############# #

    @cached_method
    def asset_flow(self, direction: str = 'both', wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get asset flow series per column.

        Returns the total transacted amount of assets at each time step."""
        direction = map_enum_fields(direction, Direction)
        asset_flow = nb.asset_flow_nb(
            self.wrapper.shape_2d,
            self.orders.values,
            self.orders.col_mapper.col_map,
            direction
        )
        return self.wrapper.wrap(asset_flow, group_by=False, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def assets(self, direction: str = 'both', wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get asset series per column.

        Returns the current position at each time step."""
        direction = map_enum_fields(direction, Direction)
        asset_flow = to_2d_array(self.asset_flow(direction='both'))
        assets = nb.assets_nb(asset_flow)
        if direction == Direction.LongOnly:
            assets = np.where(assets > 0, assets, 0.)
        if direction == Direction.ShortOnly:
            assets = np.where(assets < 0, -assets, 0.)
        return self.wrapper.wrap(assets, group_by=False, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def position_mask(self, direction: str = 'both', group_by: tp.GroupByLike = None,
                      wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get position mask per column/group.

        An element is True if the asset is in the market at this tick."""
        direction = map_enum_fields(direction, Direction)
        assets = to_2d_array(self.assets(direction=direction))
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            position_mask = to_2d_array(self.position_mask(direction=direction, group_by=False))
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            position_mask = nb.position_mask_grouped_nb(position_mask, group_lens)
        else:
            position_mask = assets != 0
        return self.wrapper.wrap(position_mask, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def position_coverage(self, direction: str = 'both', group_by: tp.GroupByLike = None,
                          wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get position coverage per column/group."""
        direction = map_enum_fields(direction, Direction)
        assets = to_2d_array(self.assets(direction=direction))
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            position_mask = to_2d_array(self.position_mask(direction=direction, group_by=False))
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            position_coverage = nb.position_coverage_grouped_nb(position_mask, group_lens)
        else:
            position_coverage = np.mean(assets != 0, axis=0)
        wrap_kwargs = merge_dicts(dict(name_or_index='position_coverage'), wrap_kwargs)
        return self.wrapper.wrap_reduced(position_coverage, group_by=group_by, **wrap_kwargs)

    # ############# Cash ############# #

    @cached_method
    def cash_flow(self, group_by: tp.GroupByLike = None, free: bool = False,
                  wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get cash flow series per column/group.

        Use `free` to return the flow of the free cash, which never goes above the initial level,
        because an operation always costs money."""
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            cash_flow = to_2d_array(self.cash_flow(group_by=False, free=free))
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            cash_flow = nb.cash_flow_grouped_nb(cash_flow, group_lens)
        else:
            cash_flow = nb.cash_flow_nb(
                self.wrapper.shape_2d,
                self.orders.values,
                self.orders.col_mapper.col_map,
                free
            )
        return self.wrapper.wrap(cash_flow, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_property
    def init_cash(self) -> tp.MaybeSeries:
        """`Portfolio.get_init_cash` with default arguments."""
        return self.get_init_cash()

    @cached_method
    def get_init_cash(self, group_by: tp.GroupByLike = None,
                      wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Initial amount of cash per column/group with default arguments.

        !!! note
            If the initial cash balance was found automatically and no own cash is used throughout
            the simulation (for example, when shorting), it will be set to 1 instead of 0 to enable
            smooth calculation of returns."""
        if isinstance(self._init_cash, int):
            cash_flow = to_2d_array(self.cash_flow(group_by=group_by))
            cash_min = np.min(np.cumsum(cash_flow, axis=0), axis=0)
            init_cash = np.where(cash_min < 0, np.abs(cash_min), 1.)
            if self._init_cash == InitCashMode.AutoAlign:
                init_cash = np.full(init_cash.shape, np.max(init_cash))
        else:
            init_cash = to_1d_array(self._init_cash)
            if self.wrapper.grouper.is_grouped(group_by=group_by):
                group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
                init_cash = nb.init_cash_grouped_nb(init_cash, group_lens, self.cash_sharing)
            else:
                group_lens = self.wrapper.grouper.get_group_lens()
                init_cash = nb.init_cash_nb(init_cash, group_lens, self.cash_sharing)
        wrap_kwargs = merge_dicts(dict(name_or_index='init_cash'), wrap_kwargs)
        return self.wrapper.wrap_reduced(init_cash, group_by=group_by, **wrap_kwargs)

    @cached_method
    def cash(self, group_by: tp.GroupByLike = None, in_sim_order: bool = False, free: bool = False,
             wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get cash balance series per column/group.

        See the explanation on `in_sim_order` in `Portfolio.value`.
        For `free`, see `Portfolio.cash_flow`."""
        if in_sim_order and not self.cash_sharing:
            raise ValueError("Cash sharing must be enabled for in_sim_order=True")

        cash_flow = to_2d_array(self.cash_flow(group_by=group_by, free=free))
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            init_cash = to_1d_array(self.get_init_cash(group_by=group_by))
            cash = nb.cash_grouped_nb(
                self.wrapper.shape_2d,
                cash_flow,
                group_lens,
                init_cash
            )
        else:
            if self.wrapper.grouper.is_grouping_disabled(group_by=group_by) and in_sim_order:
                if self.call_seq is None:
                    raise ValueError("No call sequence attached. "
                                     "Pass `attach_call_seq=True` to the class method "
                                     "(flexible simulations are not supported)")
                group_lens = self.wrapper.grouper.get_group_lens()
                init_cash = to_1d_array(self.init_cash)
                call_seq = to_2d_array(self.call_seq)
                cash = nb.cash_in_sim_order_nb(cash_flow, group_lens, init_cash, call_seq)
            else:
                init_cash = to_1d_array(self.get_init_cash(group_by=False))
                cash = nb.cash_nb(cash_flow, init_cash)
        return self.wrapper.wrap(cash, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    # ############# Performance ############# #

    @cached_method
    def asset_value(self, direction: str = 'both', group_by: tp.GroupByLike = None,
                    wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get asset value series per column/group."""
        direction = map_enum_fields(direction, Direction)
        if self.fillna_close:
            close = to_2d_array(self.get_filled_close()).copy()
        else:
            close = to_2d_array(self.close).copy()
        assets = to_2d_array(self.assets(direction=direction))
        close[assets == 0] = 0.  # for price being NaN
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            asset_value = to_2d_array(self.asset_value(direction=direction, group_by=False))
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            asset_value = nb.asset_value_grouped_nb(asset_value, group_lens)
        else:
            asset_value = nb.asset_value_nb(close, assets)
        return self.wrapper.wrap(asset_value, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def gross_exposure(self, direction: str = 'both', group_by: tp.GroupByLike = None,
                       wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get gross exposure."""
        asset_value = to_2d_array(self.asset_value(group_by=group_by, direction=direction))
        cash = to_2d_array(self.cash(group_by=group_by, free=True))
        gross_exposure = nb.gross_exposure_nb(asset_value, cash)
        return self.wrapper.wrap(gross_exposure, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def net_exposure(self, group_by: tp.GroupByLike = None,
                     wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get net exposure."""
        long_exposure = to_2d_array(self.gross_exposure(direction='longonly', group_by=group_by))
        short_exposure = to_2d_array(self.gross_exposure(direction='shortonly', group_by=group_by))
        net_exposure = long_exposure - short_exposure
        return self.wrapper.wrap(net_exposure, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def value(self, group_by: tp.GroupByLike = None, in_sim_order: bool = False,
              wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get portfolio value series per column/group.

        By default, will generate portfolio value for each asset based on cash flows and thus
        independent from other assets, with the initial cash balance and position being that of the
        entire group. Useful for generating returns and comparing assets within the same group.

        When `group_by` is False and `in_sim_order` is True, returns value generated in
        simulation order (see [row-major order](https://en.wikipedia.org/wiki/Row-_and_column-major_order).
        This value cannot be used for generating returns as-is. Useful to analyze how value
        evolved throughout simulation."""
        cash = to_2d_array(self.cash(group_by=group_by, in_sim_order=in_sim_order))
        asset_value = to_2d_array(self.asset_value(group_by=group_by))
        if self.wrapper.grouper.is_grouping_disabled(group_by=group_by) and in_sim_order:
            if self.call_seq is None:
                raise ValueError("No call sequence attached. "
                                 "Pass `attach_call_seq=True` to the class method "
                                 "(flexible simulations are not supported)")
            group_lens = self.wrapper.grouper.get_group_lens()
            call_seq = to_2d_array(self.call_seq)
            value = nb.value_in_sim_order_nb(cash, asset_value, group_lens, call_seq)
            # price of NaN is already addressed by ungrouped_value_nb
        else:
            value = nb.value_nb(cash, asset_value)
        return self.wrapper.wrap(value, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def total_profit(self, group_by: tp.GroupByLike = None,
                     wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Get total profit per column/group.

        Calculated directly from order records (fast)."""
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            total_profit = to_1d_array(self.total_profit(group_by=False))
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            total_profit = nb.total_profit_grouped_nb(
                total_profit,
                group_lens
            )
        else:
            if self.fillna_close:
                close = to_2d_array(self.get_filled_close())
            else:
                close = to_2d_array(self.close)
            total_profit = nb.total_profit_nb(
                self.wrapper.shape_2d,
                close,
                self.orders.values,
                self.orders.col_mapper.col_map
            )
        wrap_kwargs = merge_dicts(dict(name_or_index='total_profit'), wrap_kwargs)
        return self.wrapper.wrap_reduced(total_profit, group_by=group_by, **wrap_kwargs)

    @cached_method
    def final_value(self, group_by: tp.GroupByLike = None,
                    wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Get total profit per column/group."""
        init_cash = to_1d_array(self.get_init_cash(group_by=group_by))
        total_profit = to_1d_array(self.total_profit(group_by=group_by))
        final_value = nb.final_value_nb(total_profit, init_cash)
        wrap_kwargs = merge_dicts(dict(name_or_index='final_value'), wrap_kwargs)
        return self.wrapper.wrap_reduced(final_value, group_by=group_by, **wrap_kwargs)

    @cached_method
    def total_return(self, group_by: tp.GroupByLike = None,
                     wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Get total profit per column/group."""
        init_cash = to_1d_array(self.get_init_cash(group_by=group_by))
        total_profit = to_1d_array(self.total_profit(group_by=group_by))
        total_return = nb.total_return_nb(total_profit, init_cash)
        wrap_kwargs = merge_dicts(dict(name_or_index='total_return'), wrap_kwargs)
        return self.wrapper.wrap_reduced(total_return, group_by=group_by, **wrap_kwargs)

    @cached_method
    def returns(self, group_by: tp.GroupByLike = None, in_sim_order=False,
                wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get return series per column/group based on portfolio value."""
        value = to_2d_array(self.value(group_by=group_by, in_sim_order=in_sim_order))
        if self.wrapper.grouper.is_grouping_disabled(group_by=group_by) and in_sim_order:
            if self.call_seq is None:
                raise ValueError("No call sequence attached. "
                                 "Pass `attach_call_seq=True` to the class method "
                                 "(flexible simulations are not supported)")
            group_lens = self.wrapper.grouper.get_group_lens()
            init_cash_grouped = to_1d_array(self.init_cash)
            call_seq = to_2d_array(self.call_seq)
            returns = nb.returns_in_sim_order_nb(value, group_lens, init_cash_grouped, call_seq)
        else:
            init_cash = to_1d_array(self.get_init_cash(group_by=group_by))
            returns = returns_nb.returns_nb(value, init_cash)
        return self.wrapper.wrap(returns, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def asset_returns(self, group_by: tp.GroupByLike = None,
                      wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get asset return series per column/group.

        This type of returns is based solely on cash flows and asset value rather than portfolio
        value. It ignores passive cash and thus it will return the same numbers irrespective of the amount of
        cash currently available, even `np.inf`. The scale of returns is comparable to that of going
        all in and keeping available cash at zero."""
        cash_flow = to_2d_array(self.cash_flow(group_by=group_by))
        asset_value = to_2d_array(self.asset_value(group_by=group_by))
        asset_returns = nb.asset_returns_nb(cash_flow, asset_value)
        return self.wrapper.wrap(asset_returns, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @property
    def returns_acc(self) -> ReturnsAccessor:
        """`Portfolio.get_returns_acc` with default arguments."""
        return self.get_returns_acc()

    @cached_method
    def get_returns_acc(self,
                        group_by: tp.GroupByLike = None,
                        benchmark_rets: tp.Optional[tp.ArrayLike] = None,
                        freq: tp.Optional[tp.FrequencyLike] = None,
                        year_freq: tp.Optional[tp.FrequencyLike] = None,
                        use_asset_returns: bool = False,
                        defaults: tp.KwargsLike = None,
                        **kwargs) -> ReturnsAccessor:
        """Get returns accessor of type `vectorbt.returns.accessors.ReturnsAccessor`.

        !!! hint
            You can find most methods of this accessor as (cacheable) attributes of this portfolio."""
        if freq is None:
            freq = self.wrapper.freq
        if use_asset_returns:
            returns = self.asset_returns(group_by=group_by)
        else:
            returns = self.returns(group_by=group_by)
        if benchmark_rets is None:
            benchmark_rets = self.benchmark_returns(group_by=group_by)
        return returns.vbt.returns(
            benchmark_rets=benchmark_rets,
            freq=freq,
            year_freq=year_freq,
            defaults=defaults,
            **kwargs
        )

    @cached_property
    def qs(self) -> QSAdapterT:
        """`Portfolio.get_qs` with default arguments."""
        return self.get_qs()

    @cached_method
    def get_qs(self,
               group_by: tp.GroupByLike = None,
               benchmark_rets: tp.Optional[tp.ArrayLike] = None,
               freq: tp.Optional[tp.FrequencyLike] = None,
               year_freq: tp.Optional[tp.FrequencyLike] = None,
               use_asset_returns: bool = False,
               **kwargs) -> QSAdapterT:
        """Get quantstats adapter of type `vectorbt.returns.qs_adapter.QSAdapter`.

        `**kwargs` are passed to the adapter constructor."""
        from vectorbt.returns.qs_adapter import QSAdapter

        returns_acc = self.get_returns_acc(
            group_by=group_by,
            benchmark_rets=benchmark_rets,
            freq=freq,
            year_freq=year_freq,
            use_asset_returns=use_asset_returns
        )
        return QSAdapter(returns_acc, **kwargs)

    @cached_method
    def benchmark_value(self, group_by: tp.GroupByLike = None,
                        wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get market benchmark value series per column/group.

        If grouped, evenly distributes the initial cash among assets in the group.

        !!! note
            Does not take into account fees and slippage. For this, create a separate portfolio."""
        if self.fillna_close:
            close = to_2d_array(self.get_filled_close())
        else:
            close = to_2d_array(self.close)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            init_cash_grouped = to_1d_array(self.get_init_cash(group_by=group_by))
            benchmark_value = nb.benchmark_value_grouped_nb(close, group_lens, init_cash_grouped)
        else:
            init_cash = to_1d_array(self.get_init_cash(group_by=False))
            benchmark_value = nb.benchmark_value_nb(close, init_cash)
        return self.wrapper.wrap(benchmark_value, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def benchmark_returns(self, group_by: tp.GroupByLike = None,
                          wrap_kwargs: tp.KwargsLike = None) -> tp.SeriesFrame:
        """Get return series per column/group based on benchmark value."""
        benchmark_value = to_2d_array(self.benchmark_value(group_by=group_by))
        init_cash = to_1d_array(self.get_init_cash(group_by=group_by))
        benchmark_returns = returns_nb.returns_nb(benchmark_value, init_cash)
        return self.wrapper.wrap(benchmark_returns, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    benchmark_rets = benchmark_returns

    @cached_method
    def total_benchmark_return(self, group_by: tp.GroupByLike = None,
                               wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Get total benchmark return."""
        benchmark_value = to_2d_array(self.benchmark_value(group_by=group_by))
        total_benchmark_return = nb.total_benchmark_return_nb(benchmark_value)
        wrap_kwargs = merge_dicts(dict(name_or_index='total_benchmark_return'), wrap_kwargs)
        return self.wrapper.wrap_reduced(total_benchmark_return, group_by=group_by, **wrap_kwargs)

    # ############# Resolution ############# #

    @property
    def self_aliases(self) -> tp.Set[str]:
        """Names to associate with this object."""
        return {'self', 'portfolio', 'pf'}

    def pre_resolve_attr(self, attr: str, final_kwargs: tp.KwargsLike = None) -> str:
        """Pre-process an attribute before resolution.

        Uses the following keys:

        * `use_asset_returns`: Whether to use `Portfolio.asset_returns` when resolving `returns` argument.
        * `trades_type`: Which trade type to use when resolving `trades` argument."""
        if 'use_asset_returns' in final_kwargs:
            if attr == 'returns' and final_kwargs['use_asset_returns']:
                attr = 'asset_returns'
        if 'trades_type' in final_kwargs:
            trades_type = final_kwargs['trades_type']
            if isinstance(final_kwargs['trades_type'], str):
                trades_type = map_enum_fields(trades_type, TradesType)
            if attr == 'trades' and trades_type != self.trades_type:
                if trades_type == TradesType.EntryTrades:
                    attr = 'entry_trades'
                elif trades_type == TradesType.ExitTrades:
                    attr = 'exit_trades'
                else:
                    attr = 'positions'
        return attr

    def post_resolve_attr(self, attr: str, out: tp.Any, final_kwargs: tp.KwargsLike = None) -> str:
        """Post-process an object after resolution.

        Uses the following keys:

        * `incl_open`: Whether to include open trades/positions when resolving an argument
            that is an instance of `vectorbt.portfolio.trades.Trades`."""
        if 'incl_open' in final_kwargs:
            if isinstance(out, Trades) and not final_kwargs['incl_open']:
                out = out.closed
        return out

    # ############# Stats ############# #

    @property
    def stats_defaults(self) -> tp.Kwargs:
        """Defaults for `Portfolio.stats`.

        Merges `vectorbt.generic.stats_builder.StatsBuilderMixin.stats_defaults` and
        `portfolio.stats` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        returns_cfg = settings['returns']
        portfolio_stats_cfg = settings['portfolio']['stats']

        return merge_dicts(
            StatsBuilderMixin.stats_defaults.__get__(self),
            dict(
                settings=dict(
                    year_freq=returns_cfg['year_freq'],
                    trades_type=self.trades_type
                )
            ),
            portfolio_stats_cfg
        )

    _metrics: tp.ClassVar[Config] = Config(
        dict(
            start=dict(
                title='Start',
                calc_func=lambda self: self.wrapper.index[0],
                agg_func=None,
                tags='wrapper'
            ),
            end=dict(
                title='End',
                calc_func=lambda self: self.wrapper.index[-1],
                agg_func=None,
                tags='wrapper'
            ),
            period=dict(
                title='Period',
                calc_func=lambda self: len(self.wrapper.index),
                apply_to_timedelta=True,
                agg_func=None,
                tags='wrapper'
            ),
            start_value=dict(
                title='Start Value',
                calc_func='get_init_cash',
                tags='portfolio'
            ),
            end_value=dict(
                title='End Value',
                calc_func='final_value',
                tags='portfolio'
            ),
            total_return=dict(
                title='Total Return [%]',
                calc_func='total_return',
                post_calc_func=lambda self, out, settings: out * 100,
                tags='portfolio'
            ),
            benchmark_return=dict(
                title='Benchmark Return [%]',
                calc_func='benchmark_rets.vbt.returns.total',
                post_calc_func=lambda self, out, settings: out * 100,
                tags='portfolio'
            ),
            max_gross_exposure=dict(
                title='Max Gross Exposure [%]',
                calc_func='gross_exposure.vbt.max',
                post_calc_func=lambda self, out, settings: out * 100,
                tags='portfolio'
            ),
            total_fees_paid=dict(
                title='Total Fees Paid',
                calc_func='orders.fees.sum',
                tags=['portfolio', 'orders']
            ),
            max_dd=dict(
                title='Max Drawdown [%]',
                calc_func='drawdowns.max_drawdown',
                post_calc_func=lambda self, out, settings: -out * 100,
                tags=['portfolio', 'drawdowns']
            ),
            max_dd_duration=dict(
                title='Max Drawdown Duration',
                calc_func='drawdowns.max_duration',
                fill_wrap_kwargs=True,
                tags=['portfolio', 'drawdowns', 'duration']
            ),
            total_trades=dict(
                title='Total Trades',
                calc_func='trades.count',
                incl_open=True,
                tags=['portfolio', 'trades']
            ),
            total_closed_trades=dict(
                title='Total Closed Trades',
                calc_func='trades.closed.count',
                tags=['portfolio', 'trades', 'closed']
            ),
            total_open_trades=dict(
                title='Total Open Trades',
                calc_func='trades.open.count',
                incl_open=True,
                tags=['portfolio', 'trades', 'open']
            ),
            open_trade_pnl=dict(
                title='Open Trade PnL',
                calc_func='trades.open.pnl.sum',
                incl_open=True,
                tags=['portfolio', 'trades', 'open']
            ),
            win_rate=dict(
                title='Win Rate [%]',
                calc_func='trades.win_rate',
                post_calc_func=lambda self, out, settings: out * 100,
                tags=RepEval("['portfolio', 'trades', *incl_open_tags]")
            ),
            best_trade=dict(
                title='Best Trade [%]',
                calc_func='trades.returns.max',
                post_calc_func=lambda self, out, settings: out * 100,
                tags=RepEval("['portfolio', 'trades', *incl_open_tags]")
            ),
            worst_trade=dict(
                title='Worst Trade [%]',
                calc_func='trades.returns.min',
                post_calc_func=lambda self, out, settings: out * 100,
                tags=RepEval("['portfolio', 'trades', *incl_open_tags]")
            ),
            avg_winning_trade=dict(
                title='Avg Winning Trade [%]',
                calc_func='trades.winning.returns.mean',
                post_calc_func=lambda self, out, settings: out * 100,
                tags=RepEval("['portfolio', 'trades', *incl_open_tags, 'winning']")
            ),
            avg_losing_trade=dict(
                title='Avg Losing Trade [%]',
                calc_func='trades.losing.returns.mean',
                post_calc_func=lambda self, out, settings: out * 100,
                tags=RepEval("['portfolio', 'trades', *incl_open_tags, 'losing']")
            ),
            avg_winning_trade_duration=dict(
                title='Avg Winning Trade Duration',
                calc_func='trades.winning.duration.mean',
                apply_to_timedelta=True,
                tags=RepEval("['portfolio', 'trades', *incl_open_tags, 'winning', 'duration']")
            ),
            avg_losing_trade_duration=dict(
                title='Avg Losing Trade Duration',
                calc_func='trades.losing.duration.mean',
                apply_to_timedelta=True,
                tags=RepEval("['portfolio', 'trades', *incl_open_tags, 'losing', 'duration']")
            ),
            profit_factor=dict(
                title='Profit Factor',
                calc_func='trades.profit_factor',
                tags=RepEval("['portfolio', 'trades', *incl_open_tags]")
            ),
            expectancy=dict(
                title='Expectancy',
                calc_func='trades.expectancy',
                tags=RepEval("['portfolio', 'trades', *incl_open_tags]")
            ),
            sharpe_ratio=dict(
                title='Sharpe Ratio',
                calc_func='returns_acc.sharpe_ratio',
                check_has_freq=True,
                check_has_year_freq=True,
                tags=['portfolio', 'returns']
            ),
            calmar_ratio=dict(
                title='Calmar Ratio',
                calc_func='returns_acc.calmar_ratio',
                check_has_freq=True,
                check_has_year_freq=True,
                tags=['portfolio', 'returns']
            ),
            omega_ratio=dict(
                title='Omega Ratio',
                calc_func='returns_acc.omega_ratio',
                check_has_freq=True,
                check_has_year_freq=True,
                tags=['portfolio', 'returns']
            ),
            sortino_ratio=dict(
                title='Sortino Ratio',
                calc_func='returns_acc.sortino_ratio',
                check_has_freq=True,
                check_has_year_freq=True,
                tags=['portfolio', 'returns']
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def metrics(self) -> Config:
        return self._metrics

    def returns_stats(self,
                      group_by: tp.GroupByLike = None,
                      benchmark_rets: tp.Optional[tp.ArrayLike] = None,
                      freq: tp.Optional[tp.FrequencyLike] = None,
                      year_freq: tp.Optional[tp.FrequencyLike] = None,
                      use_asset_returns: bool = False,
                      defaults: tp.KwargsLike = None,
                      **kwargs) -> tp.SeriesFrame:
        """Compute various statistics on returns of this portfolio.

        See `Portfolio.returns_acc` and `vectorbt.returns.accessors.ReturnsAccessor.metrics`.

        `kwargs` will be passed to `vectorbt.returns.accessors.ReturnsAccessor.stats` method.
        If `benchmark_rets` is not set, uses `Portfolio.benchmark_returns`."""
        returns_acc = self.get_returns_acc(
            group_by=group_by,
            benchmark_rets=benchmark_rets,
            freq=freq,
            year_freq=year_freq,
            use_asset_returns=use_asset_returns,
            defaults=defaults
        )
        return getattr(returns_acc, 'stats')(**kwargs)

    # ############# Plotting ############# #

    def plot_orders(self, column: tp.Optional[tp.Label] = None, **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of orders."""
        kwargs = merge_dicts(dict(close_trace_kwargs=dict(name='Close')), kwargs)
        return self.orders.regroup(False).plot(column=column, **kwargs)

    def plot_trades(self, column: tp.Optional[tp.Label] = None, **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of trades."""
        kwargs = merge_dicts(dict(close_trace_kwargs=dict(name='Close')), kwargs)
        return self.trades.regroup(False).plot(column=column, **kwargs)

    def plot_trade_pnl(self, column: tp.Optional[tp.Label] = None, **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of trade PnL."""
        return self.trades.regroup(False).plot_pnl(column=column, **kwargs)

    def plot_positions(self, column: tp.Optional[tp.Label] = None, **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of positions."""
        kwargs = merge_dicts(dict(close_trace_kwargs=dict(name='Close')), kwargs)
        return self.positions.regroup(False).plot(column=column, **kwargs)

    def plot_position_pnl(self, column: tp.Optional[tp.Label] = None, **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of position PnL."""
        return self.positions.regroup(False).plot_pnl(column=column, **kwargs)

    def plot_asset_flow(self,
                        column: tp.Optional[tp.Label] = None,
                        direction: str = 'both',
                        xref: str = 'x',
                        yref: str = 'y',
                        hline_shape_kwargs: tp.KwargsLike = None,
                        **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column of asset flow.

        Args:
            column (str): Name of the column to plot.
            direction (Direction): See `vectorbt.portfolio.enums.Direction`.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            hline_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for zeroline.
            **kwargs: Keyword arguments passed to `vectorbt.generic.accessors.GenericAccessor.plot`.
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        kwargs = merge_dicts(dict(
            trace_kwargs=dict(
                line=dict(
                    color=plotting_cfg['color_schema']['brown']
                ),
                name='Assets'
            )
        ), kwargs)
        asset_flow = self.asset_flow(direction=direction)
        asset_flow = self.select_one_from_obj(asset_flow, self.wrapper.regroup(False), column=column)
        fig = asset_flow.vbt.plot(**kwargs)
        x_domain = get_domain(xref, fig)
        fig.add_shape(**merge_dicts(dict(
            type='line',
            line=dict(
                color='gray',
                dash="dash",
            ),
            xref="paper",
            yref=yref,
            x0=x_domain[0],
            y0=0,
            x1=x_domain[1],
            y1=0
        ), hline_shape_kwargs))
        return fig

    def plot_cash_flow(self,
                       column: tp.Optional[tp.Label] = None,
                       group_by: tp.GroupByLike = None,
                       free: bool = False,
                       xref: str = 'x',
                       yref: str = 'y',
                       hline_shape_kwargs: tp.KwargsLike = None,
                       **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of cash flow.

        Args:
            column (str): Name of the column/group to plot.
            group_by (any): Group or ungroup columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            free (bool): Whether to plot the flow of the free cash.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            hline_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for zeroline.
            **kwargs: Keyword arguments passed to `vectorbt.generic.accessors.GenericAccessor.plot`.
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        kwargs = merge_dicts(dict(
            trace_kwargs=dict(
                line=dict(
                    color=plotting_cfg['color_schema']['green']
                ),
                name='Cash'
            )
        ), kwargs)
        cash_flow = self.cash_flow(group_by=group_by, free=free)
        cash_flow = self.select_one_from_obj(cash_flow, self.wrapper.regroup(group_by), column=column)
        fig = cash_flow.vbt.plot(**kwargs)
        x_domain = get_domain(xref, fig)
        fig.add_shape(**merge_dicts(dict(
            type='line',
            line=dict(
                color='gray',
                dash="dash",
            ),
            xref="paper",
            yref=yref,
            x0=x_domain[0],
            y0=0.,
            x1=x_domain[1],
            y1=0.
        ), hline_shape_kwargs))
        return fig

    def plot_assets(self,
                    column: tp.Optional[tp.Label] = None,
                    direction: str = 'both',
                    xref: str = 'x',
                    yref: str = 'y',
                    hline_shape_kwargs: tp.KwargsLike = None,
                    **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column of assets.

        Args:
            column (str): Name of the column to plot.
            direction (Direction): See `vectorbt.portfolio.enums.Direction`.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            hline_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for zeroline.
            **kwargs: Keyword arguments passed to `vectorbt.generic.accessors.GenericSRAccessor.plot_against`.
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        kwargs = merge_dicts(dict(
            trace_kwargs=dict(
                line=dict(
                    color=plotting_cfg['color_schema']['brown']
                ),
                name='Assets'
            ),
            pos_trace_kwargs=dict(
                fillcolor=adjust_opacity(plotting_cfg['color_schema']['brown'], 0.3)
            ),
            neg_trace_kwargs=dict(
                fillcolor=adjust_opacity(plotting_cfg['color_schema']['orange'], 0.3)
            ),
            other_trace_kwargs='hidden'
        ), kwargs)
        assets = self.assets(direction=direction)
        assets = self.select_one_from_obj(assets, self.wrapper.regroup(False), column=column)
        fig = assets.vbt.plot_against(0, **kwargs)
        x_domain = get_domain(xref, fig)
        fig.add_shape(**merge_dicts(dict(
            type='line',
            line=dict(
                color='gray',
                dash="dash",
            ),
            xref="paper",
            yref=yref,
            x0=x_domain[0],
            y0=0.,
            x1=x_domain[1],
            y1=0.
        ), hline_shape_kwargs))
        return fig

    def plot_cash(self,
                  column: tp.Optional[tp.Label] = None,
                  group_by: tp.GroupByLike = None,
                  free: bool = False,
                  xref: str = 'x',
                  yref: str = 'y',
                  hline_shape_kwargs: tp.KwargsLike = None,
                  **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of cash balance.

        Args:
            column (str): Name of the column/group to plot.
            group_by (any): Group or ungroup columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            free (bool): Whether to plot the flow of the free cash.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            hline_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for zeroline.
            **kwargs: Keyword arguments passed to `vectorbt.generic.accessors.GenericSRAccessor.plot_against`.
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        kwargs = merge_dicts(dict(
            trace_kwargs=dict(
                line=dict(
                    color=plotting_cfg['color_schema']['green']
                ),
                name='Cash'
            ),
            pos_trace_kwargs=dict(
                fillcolor=adjust_opacity(plotting_cfg['color_schema']['green'], 0.3)
            ),
            neg_trace_kwargs=dict(
                fillcolor=adjust_opacity(plotting_cfg['color_schema']['red'], 0.3)
            ),
            other_trace_kwargs='hidden'
        ), kwargs)
        init_cash = self.get_init_cash(group_by=group_by)
        init_cash = self.select_one_from_obj(init_cash, self.wrapper.regroup(group_by), column=column)
        cash = self.cash(group_by=group_by, free=free)
        cash = self.select_one_from_obj(cash, self.wrapper.regroup(group_by), column=column)
        fig = cash.vbt.plot_against(init_cash, **kwargs)
        x_domain = get_domain(xref, fig)
        fig.add_shape(**merge_dicts(dict(
            type='line',
            line=dict(
                color='gray',
                dash="dash",
            ),
            xref="paper",
            yref=yref,
            x0=x_domain[0],
            y0=init_cash,
            x1=x_domain[1],
            y1=init_cash
        ), hline_shape_kwargs))
        return fig

    def plot_asset_value(self,
                         column: tp.Optional[tp.Label] = None,
                         group_by: tp.GroupByLike = None,
                         direction: str = 'both',
                         xref: str = 'x',
                         yref: str = 'y',
                         hline_shape_kwargs: tp.KwargsLike = None,
                         **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of asset value.

        Args:
            column (str): Name of the column/group to plot.
            group_by (any): Group or ungroup columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            direction (Direction): See `vectorbt.portfolio.enums.Direction`.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            hline_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for zeroline.
            **kwargs: Keyword arguments passed to `vectorbt.generic.accessors.GenericSRAccessor.plot_against`.
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        kwargs = merge_dicts(dict(
            trace_kwargs=dict(
                line=dict(
                    color=plotting_cfg['color_schema']['cyan']
                ),
                name='Asset Value'
            ),
            pos_trace_kwargs=dict(
                fillcolor=adjust_opacity(plotting_cfg['color_schema']['cyan'], 0.3)
            ),
            neg_trace_kwargs=dict(
                fillcolor=adjust_opacity(plotting_cfg['color_schema']['orange'], 0.3)
            ),
            other_trace_kwargs='hidden'
        ), kwargs)
        asset_value = self.asset_value(direction=direction, group_by=group_by)
        asset_value = self.select_one_from_obj(asset_value, self.wrapper.regroup(group_by), column=column)
        fig = asset_value.vbt.plot_against(0, **kwargs)
        x_domain = get_domain(xref, fig)
        fig.add_shape(**merge_dicts(dict(
            type='line',
            line=dict(
                color='gray',
                dash="dash",
            ),
            xref="paper",
            yref=yref,
            x0=x_domain[0],
            y0=0.,
            x1=x_domain[1],
            y1=0.
        ), hline_shape_kwargs))
        return fig

    def plot_value(self,
                   column: tp.Optional[tp.Label] = None,
                   group_by: tp.GroupByLike = None,
                   xref: str = 'x',
                   yref: str = 'y',
                   hline_shape_kwargs: tp.KwargsLike = None,
                   **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of value.

        Args:
            column (str): Name of the column/group to plot.
            group_by (any): Group or ungroup columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            free (bool): Whether to plot free cash flow.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            hline_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for zeroline.
            **kwargs: Keyword arguments passed to `vectorbt.generic.accessors.GenericSRAccessor.plot_against`.
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        kwargs = merge_dicts(dict(
            trace_kwargs=dict(
                line=dict(
                    color=plotting_cfg['color_schema']['purple']
                ),
                name='Value'
            ),
            other_trace_kwargs='hidden'
        ), kwargs)
        init_cash = self.get_init_cash(group_by=group_by)
        init_cash = self.select_one_from_obj(init_cash, self.wrapper.regroup(group_by), column=column)
        value = self.value(group_by=group_by)
        value = self.select_one_from_obj(value, self.wrapper.regroup(group_by), column=column)
        fig = value.vbt.plot_against(init_cash, **kwargs)
        x_domain = get_domain(xref, fig)
        fig.add_shape(**merge_dicts(dict(
            type='line',
            line=dict(
                color='gray',
                dash="dash",
            ),
            xref="paper",
            yref=yref,
            x0=x_domain[0],
            y0=init_cash,
            x1=x_domain[1],
            y1=init_cash
        ), hline_shape_kwargs))
        return fig

    def plot_cum_returns(self,
                         column: tp.Optional[tp.Label] = None,
                         group_by: tp.GroupByLike = None,
                         benchmark_rets: tp.Optional[tp.ArrayLike] = None,
                         use_asset_returns: bool = False,
                         **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of cumulative returns.

        Args:
            column (str): Name of the column/group to plot.
            group_by (any): Group or ungroup columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            benchmark_rets (array_like): Benchmark returns.

                If None, will use `Portfolio.benchmark_returns`.
            use_asset_returns (bool): Whether to plot asset returns.
            **kwargs: Keyword arguments passed to `vectorbt.returns.accessors.ReturnsSRAccessor.plot_cumulative`.
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        if benchmark_rets is None:
            benchmark_rets = self.benchmark_returns(group_by=group_by)
        else:
            benchmark_rets = broadcast_to(benchmark_rets, self.obj)
        benchmark_rets = self.select_one_from_obj(benchmark_rets, self.wrapper.regroup(group_by), column=column)
        kwargs = merge_dicts(dict(
            benchmark_rets=benchmark_rets,
            main_kwargs=dict(
                trace_kwargs=dict(
                    line=dict(
                        color=plotting_cfg['color_schema']['purple']
                    ),
                    name='Value'
                )
            ),
            hline_shape_kwargs=dict(
                type='line',
                line=dict(
                    color='gray',
                    dash="dash",
                )
            )
        ), kwargs)
        if use_asset_returns:
            returns = self.asset_returns(group_by=group_by)
        else:
            returns = self.returns(group_by=group_by)
        returns = self.select_one_from_obj(returns, self.wrapper.regroup(group_by), column=column)
        return returns.vbt.returns.plot_cumulative(**kwargs)

    def plot_drawdowns(self,
                       column: tp.Optional[tp.Label] = None,
                       group_by: tp.GroupByLike = None,
                       **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of drawdowns.

        Args:
            column (str): Name of the column/group to plot.
            group_by (any): Group or ungroup columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            **kwargs: Keyword arguments passed to `vectorbt.generic.drawdowns.Drawdowns.plot`.
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        kwargs = merge_dicts(dict(
            ts_trace_kwargs=dict(
                line=dict(
                    color=plotting_cfg['color_schema']['purple']
                ),
                name='Value'
            )
        ), kwargs)
        return self.get_drawdowns(group_by=group_by).plot(column=column, **kwargs)

    def plot_underwater(self,
                        column: tp.Optional[tp.Label] = None,
                        group_by: tp.GroupByLike = None,
                        xref: str = 'x',
                        yref: str = 'y',
                        hline_shape_kwargs: tp.KwargsLike = None,
                        **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of underwater.

        Args:
            column (str): Name of the column/group to plot.
            group_by (any): Group or ungroup columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            hline_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for zeroline.
            **kwargs: Keyword arguments passed to `vectorbt.generic.accessors.GenericAccessor.plot`.
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        kwargs = merge_dicts(dict(
            trace_kwargs=dict(
                line=dict(
                    color=plotting_cfg['color_schema']['red']
                ),
                fillcolor=adjust_opacity(plotting_cfg['color_schema']['red'], 0.3),
                fill='tozeroy',
                name='Drawdown'
            )
        ), kwargs)
        drawdown = self.drawdown(group_by=group_by)
        drawdown = self.select_one_from_obj(drawdown, self.wrapper.regroup(group_by), column=column)
        fig = drawdown.vbt.plot(**kwargs)
        x_domain = get_domain(xref, fig)
        fig.add_shape(**merge_dicts(dict(
            type='line',
            line=dict(
                color='gray',
                dash="dash",
            ),
            xref="paper",
            yref=yref,
            x0=x_domain[0],
            y0=0,
            x1=x_domain[1],
            y1=0
        ), hline_shape_kwargs))
        yaxis = 'yaxis' + yref[1:]
        fig.layout[yaxis]['tickformat'] = '%'
        return fig

    def plot_gross_exposure(self,
                            column: tp.Optional[tp.Label] = None,
                            group_by: tp.GroupByLike = None,
                            direction: str = 'both',
                            xref: str = 'x',
                            yref: str = 'y',
                            hline_shape_kwargs: tp.KwargsLike = None,
                            **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of gross exposure.

        Args:
            column (str): Name of the column/group to plot.
            group_by (any): Group or ungroup columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            direction (Direction): See `vectorbt.portfolio.enums.Direction`.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            hline_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for zeroline.
            **kwargs: Keyword arguments passed to `vectorbt.generic.accessors.GenericSRAccessor.plot_against`.
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        kwargs = merge_dicts(dict(
            trace_kwargs=dict(
                line=dict(
                    color=plotting_cfg['color_schema']['pink']
                ),
                name='Exposure'
            ),
            pos_trace_kwargs=dict(
                fillcolor=adjust_opacity(plotting_cfg['color_schema']['orange'], 0.3)
            ),
            neg_trace_kwargs=dict(
                fillcolor=adjust_opacity(plotting_cfg['color_schema']['pink'], 0.3)
            ),
            other_trace_kwargs='hidden'
        ), kwargs)
        gross_exposure = self.gross_exposure(direction=direction, group_by=group_by)
        gross_exposure = self.select_one_from_obj(gross_exposure, self.wrapper.regroup(group_by), column=column)
        fig = gross_exposure.vbt.plot_against(1, **kwargs)
        x_domain = get_domain(xref, fig)
        fig.add_shape(**merge_dicts(dict(
            type='line',
            line=dict(
                color='gray',
                dash="dash",
            ),
            xref="paper",
            yref=yref,
            x0=x_domain[0],
            y0=1,
            x1=x_domain[1],
            y1=1
        ), hline_shape_kwargs))
        return fig

    def plot_net_exposure(self,
                          column: tp.Optional[tp.Label] = None,
                          group_by: tp.GroupByLike = None,
                          xref: str = 'x',
                          yref: str = 'y',
                          hline_shape_kwargs: tp.KwargsLike = None,
                          **kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot one column/group of net exposure.

        Args:
            column (str): Name of the column/group to plot.
            group_by (any): Group or ungroup columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            hline_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for zeroline.
            **kwargs: Keyword arguments passed to `vectorbt.generic.accessors.GenericSRAccessor.plot_against`.
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        kwargs = merge_dicts(dict(
            trace_kwargs=dict(
                line=dict(
                    color=plotting_cfg['color_schema']['pink']
                ),
                name='Exposure'
            ),
            pos_trace_kwargs=dict(
                fillcolor=adjust_opacity(plotting_cfg['color_schema']['pink'], 0.3)
            ),
            neg_trace_kwargs=dict(
                fillcolor=adjust_opacity(plotting_cfg['color_schema']['orange'], 0.3)
            ),
            other_trace_kwargs='hidden'
        ), kwargs)
        net_exposure = self.net_exposure(group_by=group_by)
        net_exposure = self.select_one_from_obj(net_exposure, self.wrapper.regroup(group_by), column=column)
        fig = net_exposure.vbt.plot_against(0, **kwargs)
        x_domain = get_domain(xref, fig)
        fig.add_shape(**merge_dicts(dict(
            type='line',
            line=dict(
                color='gray',
                dash="dash",
            ),
            xref="paper",
            yref=yref,
            x0=x_domain[0],
            y0=0,
            x1=x_domain[1],
            y1=0
        ), hline_shape_kwargs))
        return fig

    @property
    def plots_defaults(self) -> tp.Kwargs:
        """Defaults for `Portfolio.plot`.

        Merges `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots_defaults` and
        `portfolio.plots` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        returns_cfg = settings['returns']
        portfolio_plots_cfg = settings['portfolio']['plots']

        return merge_dicts(
            PlotsBuilderMixin.plots_defaults.__get__(self),
            dict(
                settings=dict(
                    year_freq=returns_cfg['year_freq'],
                    trades_type=self.trades_type
                )
            ),
            portfolio_plots_cfg
        )

    _subplots: tp.ClassVar[Config] = Config(
        dict(
            orders=dict(
                title="Orders",
                yaxis_kwargs=dict(title="Price"),
                check_is_not_grouped=True,
                plot_func='orders.plot',
                tags=['portfolio', 'orders']
            ),
            trades=dict(
                title="Trades",
                yaxis_kwargs=dict(title="Price"),
                check_is_not_grouped=True,
                plot_func='trades.plot',
                tags=['portfolio', 'trades']
            ),
            trade_pnl=dict(
                title="Trade PnL",
                yaxis_kwargs=dict(title="Trade PnL"),
                check_is_not_grouped=True,
                plot_func='trades.plot_pnl',
                tags=['portfolio', 'trades']
            ),
            asset_flow=dict(
                title="Asset Flow",
                yaxis_kwargs=dict(title="Asset flow"),
                check_is_not_grouped=True,
                plot_func='plot_asset_flow',
                pass_add_trace_kwargs=True,
                tags=['portfolio', 'assets']
            ),
            cash_flow=dict(
                title="Cash Flow",
                yaxis_kwargs=dict(title="Cash flow"),
                plot_func='plot_cash_flow',
                pass_add_trace_kwargs=True,
                tags=['portfolio', 'cash']
            ),
            assets=dict(
                title="Assets",
                yaxis_kwargs=dict(title="Assets"),
                check_is_not_grouped=True,
                plot_func='plot_assets',
                pass_add_trace_kwargs=True,
                tags=['portfolio', 'assets']
            ),
            cash=dict(
                title="Cash",
                yaxis_kwargs=dict(title="Cash"),
                plot_func='plot_cash',
                pass_add_trace_kwargs=True,
                tags=['portfolio', 'cash']
            ),
            asset_value=dict(
                title="Asset Value",
                yaxis_kwargs=dict(title="Asset value"),
                plot_func='plot_asset_value',
                pass_add_trace_kwargs=True,
                tags=['portfolio', 'assets', 'value']
            ),
            value=dict(
                title="Value",
                yaxis_kwargs=dict(title="Value"),
                plot_func='plot_value',
                pass_add_trace_kwargs=True,
                tags=['portfolio', 'value']
            ),
            cum_returns=dict(
                title="Cumulative Returns",
                yaxis_kwargs=dict(title="Cumulative returns"),
                plot_func='plot_cum_returns',
                pass_hline_shape_kwargs=True,
                pass_add_trace_kwargs=True,
                pass_xref=True,
                pass_yref=True,
                tags=['portfolio', 'returns']
            ),
            drawdowns=dict(
                title="Drawdowns",
                yaxis_kwargs=dict(title="Value"),
                plot_func='plot_drawdowns',
                pass_add_trace_kwargs=True,
                pass_xref=True,
                pass_yref=True,
                tags=['portfolio', 'value', 'drawdowns']
            ),
            underwater=dict(
                title="Underwater",
                yaxis_kwargs=dict(title="Drawdown"),
                plot_func='plot_underwater',
                pass_add_trace_kwargs=True,
                tags=['portfolio', 'value', 'drawdowns']
            ),
            gross_exposure=dict(
                title="Gross Exposure",
                yaxis_kwargs=dict(title="Gross exposure"),
                plot_func='plot_gross_exposure',
                pass_add_trace_kwargs=True,
                tags=['portfolio', 'exposure']
            ),
            net_exposure=dict(
                title="Net Exposure",
                yaxis_kwargs=dict(title="Net exposure"),
                plot_func='plot_net_exposure',
                pass_add_trace_kwargs=True,
                tags=['portfolio', 'exposure']
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    plot = PlotsBuilderMixin.plots

    @property
    def subplots(self) -> Config:
        return self._subplots


Portfolio.override_metrics_doc(__pdoc__)
Portfolio.override_subplots_doc(__pdoc__)

__pdoc__['Portfolio.plot'] = "See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots`."
