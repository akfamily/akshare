# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Base class for working with trade records.

Trade records capture information on trades.

In vectorbt, a trade is a sequence of orders that starts with an opening order and optionally ends
with a closing order. Every pair of opposite orders can be represented by a trade. Each trade has a PnL
info attached to quickly assess its performance. An interesting effect of this representation
is the ability to aggregate trades: if two or more trades are happening one after another in time,
they can be aggregated into a bigger trade. This way, for example, single-order trades can be aggregated
into positions; but also multiple positions can be aggregated into a single blob that reflects the performance
of the entire symbol.

!!! warning
    All classes return both closed AND open trades/positions, which may skew your performance results.
    To only consider closed trades/positions, you should explicitly query the `closed` attribute.

## Trade types

There are three main types of trades.

### Entry trades

An entry trade is created from each order that opens or adds to a position.

For example, if we have a single large buy order and 100 smaller sell orders, we will see
a single trade with the entry information copied from the buy order and the exit information being
a size-weighted average over the exit information of all sell orders. On the other hand,
if we have 100 smaller buy orders and a single sell order, we will see 100 trades,
each with the entry information copied from the buy order and the exit information being
a size-based fraction of the exit information of the sell order.

Use `vectorbt.portfolio.trades.EntryTrades.from_orders` to build entry trades from orders.
Also available as `vectorbt.portfolio.base.Portfolio.entry_trades`.

### Exit trades

An exit trade is created from each order that closes or removes from a position.

Use `vectorbt.portfolio.trades.ExitTrades.from_orders` to build exit trades from orders.
Also available as `vectorbt.portfolio.base.Portfolio.exit_trades`.

### Positions

A position is created from a sequence of entry or exit trades.

Use `vectorbt.portfolio.trades.Positions.from_trades` to build positions from entry or exit trades.
Also available as `vectorbt.portfolio.base.Portfolio.positions`.

## Example

* Increasing position:

```pycon
>>> import pandas as pd
>>> import numpy as np
>>> from datetime import datetime, timedelta
>>> import vectorbt as vbt

>>> # Entry trades
>>> pf_kwargs = dict(
...     close=pd.Series([1., 2., 3., 4., 5.]),
...     size=pd.Series([1., 1., 1., 1., -4.]),
...     fixed_fees=1.
... )
>>> entry_trades = vbt.Portfolio.from_orders(**pf_kwargs).entry_trades
>>> entry_trades.records_readable
   Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \\
0         0       0   1.0                0              1.0         1.0
1         1       0   1.0                1              2.0         1.0
2         2       0   1.0                2              3.0         1.0
3         3       0   1.0                3              4.0         1.0

   Exit Timestamp  Avg Exit Price  Exit Fees   PnL  Return Direction  Status  \\
0               4             5.0       0.25  2.75  2.7500      Long  Closed
1               4             5.0       0.25  1.75  0.8750      Long  Closed
2               4             5.0       0.25  0.75  0.2500      Long  Closed
3               4             5.0       0.25 -0.25 -0.0625      Long  Closed

   Parent Id
0          0
1          0
2          0
3          0

>>> # Exit trades
>>> exit_trades = vbt.Portfolio.from_orders(**pf_kwargs).exit_trades
>>> exit_trades.records_readable
   Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \\
0         0       0   4.0                0              2.5         4.0

   Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \\
0               4             5.0        1.0  5.0     0.5      Long  Closed

   Parent Id
0          0

>>> # Positions
>>> positions = vbt.Portfolio.from_orders(**pf_kwargs).positions
>>> positions.records_readable
   Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \\
0         0       0   4.0                0              2.5         4.0

   Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \\
0               4             5.0        1.0  5.0     0.5      Long  Closed

   Parent Id
0          0

>>> entry_trades.pnl.sum() == exit_trades.pnl.sum() == positions.pnl.sum()
True
```

* Decreasing position:

```pycon
>>> # Entry trades
>>> pf_kwargs = dict(
...     close=pd.Series([1., 2., 3., 4., 5.]),
...     size=pd.Series([4., -1., -1., -1., -1.]),
...     fixed_fees=1.
... )
>>> entry_trades = vbt.Portfolio.from_orders(**pf_kwargs).entry_trades
>>> entry_trades.records_readable
   Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \\
0         0       0   4.0                0              1.0         1.0

   Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \\
0               4             3.5        4.0  5.0    1.25      Long  Closed

   Parent Id
0          0

>>> # Exit trades
>>> exit_trades = vbt.Portfolio.from_orders(**pf_kwargs).exit_trades
>>> exit_trades.records_readable
   Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \\
0         0       0   1.0                0              1.0        0.25
1         1       0   1.0                0              1.0        0.25
2         2       0   1.0                0              1.0        0.25
3         3       0   1.0                0              1.0        0.25

   Exit Timestamp  Avg Exit Price  Exit Fees   PnL  Return Direction  Status  \\
0               1             2.0        1.0 -0.25   -0.25      Long  Closed
1               2             3.0        1.0  0.75    0.75      Long  Closed
2               3             4.0        1.0  1.75    1.75      Long  Closed
3               4             5.0        1.0  2.75    2.75      Long  Closed

   Parent Id
0          0
1          0
2          0
3          0

>>> # Positions
>>> positions = vbt.Portfolio.from_orders(**pf_kwargs).positions
>>> positions.records_readable
   Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \\
0         0       0   4.0                0              1.0         1.0

   Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \\
0               4             3.5        4.0  5.0    1.25      Long  Closed

   Parent Id
0          0

>>> entry_trades.pnl.sum() == exit_trades.pnl.sum() == positions.pnl.sum()
True
```

* Multiple reversing positions:

```pycon
>>> # Entry trades
>>> pf_kwargs = dict(
...     close=pd.Series([1., 2., 3., 4., 5.]),
...     size=pd.Series([1., -2., 2., -2., 1.]),
...     fixed_fees=1.
... )
>>> entry_trades = vbt.Portfolio.from_orders(**pf_kwargs).entry_trades
>>> entry_trades.records_readable
   Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \\
0         0       0   1.0                0              1.0         1.0
1         1       0   1.0                1              2.0         0.5
2         2       0   1.0                2              3.0         0.5
3         3       0   1.0                3              4.0         0.5

   Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \\
0               1             2.0        0.5 -0.5  -0.500      Long  Closed
1               2             3.0        0.5 -2.0  -1.000     Short  Closed
2               3             4.0        0.5  0.0   0.000      Long  Closed
3               4             5.0        1.0 -2.5  -0.625     Short  Closed

   Parent Id
0          0
1          1
2          2
3          3

>>> # Exit trades
>>> exit_trades = vbt.Portfolio.from_orders(**pf_kwargs).exit_trades
>>> exit_trades.records_readable
   Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \\
0         0       0   1.0                0              1.0         1.0
1         1       0   1.0                1              2.0         0.5
2         2       0   1.0                2              3.0         0.5
3         3       0   1.0                3              4.0         0.5

   Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \\
0               1             2.0        0.5 -0.5  -0.500      Long  Closed
1               2             3.0        0.5 -2.0  -1.000     Short  Closed
2               3             4.0        0.5  0.0   0.000      Long  Closed
3               4             5.0        1.0 -2.5  -0.625     Short  Closed

   Parent Id
0          0
1          1
2          2
3          3

>>> # Positions
>>> positions = vbt.Portfolio.from_orders(**pf_kwargs).positions
>>> positions.records_readable
   Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \\
0         0       0   1.0                0              1.0         1.0
1         1       0   1.0                1              2.0         0.5
2         2       0   1.0                2              3.0         0.5
3         3       0   1.0                3              4.0         0.5

   Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction  Status  \\
0               1             2.0        0.5 -0.5  -0.500      Long  Closed
1               2             3.0        0.5 -2.0  -1.000     Short  Closed
2               3             4.0        0.5  0.0   0.000      Long  Closed
3               4             5.0        1.0 -2.5  -0.625     Short  Closed

   Parent Id
0          0
1          1
2          2
3          3

>>> entry_trades.pnl.sum() == exit_trades.pnl.sum() == positions.pnl.sum()
True
```

* Open position:

```pycon
>>> # Entry trades
>>> pf_kwargs = dict(
...     close=pd.Series([1., 2., 3., 4., 5.]),
...     size=pd.Series([1., 0., 0., 0., 0.]),
...     fixed_fees=1.
... )
>>> entry_trades = vbt.Portfolio.from_orders(**pf_kwargs).entry_trades
>>> entry_trades.records_readable
   Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \\
0         0       0   1.0                0              1.0         1.0

   Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction Status  \\
0               4             5.0        0.0  3.0     3.0      Long   Open

   Parent Id
0          0

>>> # Exit trades
>>> exit_trades = vbt.Portfolio.from_orders(**pf_kwargs).exit_trades
>>> exit_trades.records_readable
   Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \\
0         0       0   1.0                0              1.0         1.0

   Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction Status  \\
0               4             5.0        0.0  3.0     3.0      Long   Open

   Parent Id
0          0

>>> # Positions
>>> positions = vbt.Portfolio.from_orders(**pf_kwargs).positions
>>> positions.records_readable
   Trade Id  Column  Size  Entry Timestamp  Avg Entry Price  Entry Fees  \\
0         0       0   1.0                0              1.0         1.0

   Exit Timestamp  Avg Exit Price  Exit Fees  PnL  Return Direction Status  \\
0               4             5.0        0.0  3.0     3.0      Long   Open

   Parent Id
0          0

>>> entry_trades.pnl.sum() == exit_trades.pnl.sum() == positions.pnl.sum()
True
```

Get trade count, trade PnL, and winning trade PnL:

```pycon
>>> price = pd.Series([1., 2., 3., 4., 3., 2., 1.])
>>> size = pd.Series([1., -0.5, -0.5, 2., -0.5, -0.5, -0.5])
>>> trades = vbt.Portfolio.from_orders(price, size).trades

>>> trades.count()
6

>>> trades.pnl.sum()
-3.0

>>> trades.winning.count()
2

>>> trades.winning.pnl.sum()
1.5
```

Get count and PnL of trades with duration of more than 2 days:

```pycon
>>> mask = (trades.records['exit_idx'] - trades.records['entry_idx']) > 2
>>> trades_filtered = trades.apply_mask(mask)
>>> trades_filtered.count()
2

>>> trades_filtered.pnl.sum()
-3.0
```

## Stats

!!! hint
    See `vectorbt.generic.stats_builder.StatsBuilderMixin.stats` and `Trades.metrics`.

```pycon
>>> np.random.seed(42)
>>> price = pd.DataFrame({
...     'a': np.random.uniform(1, 2, size=100),
...     'b': np.random.uniform(1, 2, size=100)
... }, index=[datetime(2020, 1, 1) + timedelta(days=i) for i in range(100)])
>>> size = pd.DataFrame({
...     'a': np.random.uniform(-1, 1, size=100),
...     'b': np.random.uniform(-1, 1, size=100),
... }, index=[datetime(2020, 1, 1) + timedelta(days=i) for i in range(100)])
>>> pf = vbt.Portfolio.from_orders(price, size, fees=0.01, freq='d')

>>> pf.trades['a'].stats()
Start                                2020-01-01 00:00:00
End                                  2020-04-09 00:00:00
Period                                 100 days 00:00:00
First Trade Start                    2020-01-01 00:00:00
Last Trade End                       2020-04-09 00:00:00
Coverage                               100 days 00:00:00
Overlap Coverage                        97 days 00:00:00
Total Records                                         48
Total Long Trades                                     22
Total Short Trades                                    26
Total Closed Trades                                   47
Total Open Trades                                      1
Open Trade PnL                                 -1.290981
Win Rate [%]                                    51.06383
Max Win Streak                                         3
Max Loss Streak                                        3
Best Trade [%]                                 43.326077
Worst Trade [%]                               -59.478304
Avg Winning Trade [%]                          21.418522
Avg Losing Trade [%]                          -18.856792
Avg Winning Trade Duration              22 days 22:00:00
Avg Losing Trade Duration     29 days 01:02:36.521739130
Profit Factor                                   0.976634
Expectancy                                     -0.001569
SQN                                            -0.064929
Name: a, dtype: object
```

Positions share almost identical metrics with trades:

```pycon
>>> pf.positions['a'].stats()
Start                            2020-01-01 00:00:00
End                              2020-04-09 00:00:00
Period                             100 days 00:00:00
Coverage [%]                                   100.0
First Position Start             2020-01-01 00:00:00
Last Position End                2020-04-09 00:00:00
Total Records                                      3
Total Long Positions                               2
Total Short Positions                              1
Total Closed Positions                             2
Total Open Positions                               1
Open Position PnL                          -0.929746
Win Rate [%]                                    50.0
Max Win Streak                                     1
Max Loss Streak                                    1
Best Position [%]                          39.498421
Worst Position [%]                          -3.32533
Avg Winning Position [%]                   39.498421
Avg Losing Position [%]                     -3.32533
Avg Winning Position Duration        1 days 00:00:00
Avg Losing Position Duration        47 days 00:00:00
Profit Factor                               0.261748
Expectancy                                 -0.217492
SQN                                        -0.585103
Name: a, dtype: object
```

To also include open trades/positions when calculating metrics such as win rate, pass `incl_open=True`:

```pycon
>>> pf.trades['a'].stats(settings=dict(incl_open=True))
Start                         2020-01-01 00:00:00
End                           2020-04-09 00:00:00
Period                          100 days 00:00:00
First Trade Start             2020-01-01 00:00:00
Last Trade End                2020-04-09 00:00:00
Coverage                        100 days 00:00:00
Overlap Coverage                 97 days 00:00:00
Total Records                                  48
Total Long Trades                              22
Total Short Trades                             26
Total Closed Trades                            47
Total Open Trades                               1
Open Trade PnL                          -1.290981
Win Rate [%]                             51.06383
Max Win Streak                                  3
Max Loss Streak                                 3
Best Trade [%]                          43.326077
Worst Trade [%]                        -59.478304
Avg Winning Trade [%]                   21.418522
Avg Losing Trade [%]                   -19.117677
Avg Winning Trade Duration       22 days 22:00:00
Avg Losing Trade Duration        30 days 00:00:00
Profit Factor                            0.693135
Expectancy                              -0.028432
SQN                                     -0.794284
Name: a, dtype: object
```

`Trades.stats` also supports (re-)grouping:

```pycon
>>> pf.trades.stats(group_by=True)
Start                                2020-01-01 00:00:00
End                                  2020-04-09 00:00:00
Period                                 100 days 00:00:00
First Trade Start                    2020-01-01 00:00:00
Last Trade End                       2020-04-09 00:00:00
Coverage                               100 days 00:00:00
Overlap Coverage                       100 days 00:00:00
Total Records                                        104
Total Long Trades                                     32
Total Short Trades                                    72
Total Closed Trades                                  102
Total Open Trades                                      2
Open Trade PnL                                 -1.790938
Win Rate [%]                                   46.078431
Max Win Streak                                         5
Max Loss Streak                                        5
Best Trade [%]                                 43.326077
Worst Trade [%]                               -87.793448
Avg Winning Trade [%]                          19.023926
Avg Losing Trade [%]                          -20.605892
Avg Winning Trade Duration    24 days 08:40:51.063829787
Avg Losing Trade Duration     25 days 11:20:43.636363636
Profit Factor                                   0.909581
Expectancy                                     -0.006035
SQN                                            -0.365593
Name: group, dtype: object
```

## Plots

!!! hint
    See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots` and `Trades.subplots`.

`Trades` class has two subplots based on `Trades.plot` and `Trades.plot_pnl`:

```pycon
>>> pf.trades['a'].plots(settings=dict(plot_zones=False)).show_svg()
```

![](/assets/images/trades_plots.svg)
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from vectorbt import _typing as tp
from vectorbt.base.array_wrapper import ArrayWrapper
from vectorbt.base.reshape_fns import to_1d_array, to_2d_array
from vectorbt.generic.ranges import Ranges
from vectorbt.portfolio import nb
from vectorbt.portfolio.enums import TradeDirection, TradeStatus, trade_dt
from vectorbt.portfolio.orders import Orders
from vectorbt.records.decorators import attach_fields, override_field_config
from vectorbt.records.mapped_array import MappedArray
from vectorbt.utils.array_ import min_rel_rescale, max_rel_rescale
from vectorbt.utils.colors import adjust_lightness
from vectorbt.utils.config import merge_dicts, Config
from vectorbt.utils.decorators import cached_method, cached_property
from vectorbt.utils.figure import make_figure, get_domain
from vectorbt.utils.template import RepEval

__pdoc__ = {}

# ############# Trades ############# #

trades_field_config = Config(
    dict(
        dtype=trade_dt,
        settings={
            'id': dict(
                title='Trade Id'
            ),
            'idx': dict(
                name='exit_idx'  # remap field of Records
            ),
            'start_idx': dict(
                name='entry_idx'  # remap field of Ranges
            ),
            'end_idx': dict(
                name='exit_idx'  # remap field of Ranges
            ),
            'size': dict(
                title='Size'
            ),
            'entry_idx': dict(
                title='Entry Timestamp',
                mapping='index'
            ),
            'entry_price': dict(
                title='Avg Entry Price'
            ),
            'entry_fees': dict(
                title='Entry Fees'
            ),
            'exit_idx': dict(
                title='Exit Timestamp',
                mapping='index'
            ),
            'exit_price': dict(
                title='Avg Exit Price'
            ),
            'exit_fees': dict(
                title='Exit Fees'
            ),
            'pnl': dict(
                title='PnL'
            ),
            'return': dict(
                title='Return'
            ),
            'direction': dict(
                title='Direction',
                mapping=TradeDirection
            ),
            'status': dict(
                title='Status',
                mapping=TradeStatus
            ),
            'parent_id': dict(
                title='Position Id'
            )
        }
    ),
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['trades_field_config'] = f"""Field config for `Trades`.

```json
{trades_field_config.to_doc()}
```
"""

trades_attach_field_config = Config(
    {
        'return': dict(
            attach='returns'
        ),
        'direction': dict(
            attach_filters=True
        ),
        'status': dict(
            attach_filters=True,
            on_conflict='ignore'
        )
    },
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['trades_attach_field_config'] = f"""Config of fields to be attached to `Trades`.

```json
{trades_attach_field_config.to_doc()}
```
"""

TradesT = tp.TypeVar("TradesT", bound="Trades")


@attach_fields(trades_attach_field_config)
@override_field_config(trades_field_config)
class Trades(Ranges):
    """Extends `vectorbt.generic.ranges.Ranges` for working with trade-like records, such as
    entry trades, exit trades, and positions."""

    @property
    def field_config(self) -> Config:
        return self._field_config

    def __init__(self,
                 wrapper: ArrayWrapper,
                 records_arr: tp.RecordArray,
                 close: tp.ArrayLike,
                 **kwargs) -> None:
        Ranges.__init__(
            self,
            wrapper,
            records_arr,
            close=close,
            **kwargs
        )
        self._close = close

    def indexing_func(self: TradesT, pd_indexing_func: tp.PandasIndexingFunc, **kwargs) -> TradesT:
        """Perform indexing on `Trades`."""
        new_wrapper, new_records_arr, group_idxs, col_idxs = \
            Ranges.indexing_func_meta(self, pd_indexing_func, **kwargs)
        if self.close is not None:
            new_close = new_wrapper.wrap(to_2d_array(self.close)[:, col_idxs], group_by=False)
        else:
            new_close = None
        return self.replace(
            wrapper=new_wrapper,
            records_arr=new_records_arr,
            close=new_close
        )

    @property
    def close(self) -> tp.Optional[tp.SeriesFrame]:
        """Reference price such as close (optional)."""
        return self._close

    @classmethod
    def from_ts(cls: tp.Type[TradesT], *args, **kwargs) -> TradesT:
        raise NotImplementedError

    @cached_property
    def winning(self: TradesT) -> TradesT:
        """Winning trades."""
        filter_mask = self.values['pnl'] > 0.
        return self.apply_mask(filter_mask)

    @cached_property
    def losing(self: TradesT) -> TradesT:
        """Losing trades."""
        filter_mask = self.values['pnl'] < 0.
        return self.apply_mask(filter_mask)

    @cached_property
    def winning_streak(self) -> MappedArray:
        """Winning streak at each trade in the current column.

        See `vectorbt.portfolio.nb.trade_winning_streak_nb`."""
        return self.apply(nb.trade_winning_streak_nb, dtype=np.int64)

    @cached_property
    def losing_streak(self) -> MappedArray:
        """Losing streak at each trade in the current column.

        See `vectorbt.portfolio.nb.trade_losing_streak_nb`."""
        return self.apply(nb.trade_losing_streak_nb, dtype=np.int64)

    @cached_method
    def win_rate(self, group_by: tp.GroupByLike = None,
                 wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Rate of winning trades."""
        win_count = to_1d_array(self.winning.count(group_by=group_by))
        total_count = to_1d_array(self.count(group_by=group_by))
        with np.errstate(divide='ignore', invalid='ignore'):
            win_rate = win_count / total_count
        wrap_kwargs = merge_dicts(dict(name_or_index='win_rate'), wrap_kwargs)
        return self.wrapper.wrap_reduced(win_rate, group_by=group_by, **wrap_kwargs)

    @cached_method
    def profit_factor(self, group_by: tp.GroupByLike = None,
                      wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Profit factor."""
        total_win = to_1d_array(self.winning.pnl.sum(group_by=group_by))
        total_loss = to_1d_array(self.losing.pnl.sum(group_by=group_by))

        # Otherwise columns with only wins or losses will become NaNs
        has_values = to_1d_array(self.count(group_by=group_by)) > 0
        total_win[np.isnan(total_win) & has_values] = 0.
        total_loss[np.isnan(total_loss) & has_values] = 0.

        with np.errstate(divide='ignore', invalid='ignore'):
            profit_factor = total_win / np.abs(total_loss)
        wrap_kwargs = merge_dicts(dict(name_or_index='profit_factor'), wrap_kwargs)
        return self.wrapper.wrap_reduced(profit_factor, group_by=group_by, **wrap_kwargs)

    @cached_method
    def expectancy(self, group_by: tp.GroupByLike = None,
                   wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Average profitability."""
        win_rate = to_1d_array(self.win_rate(group_by=group_by))
        avg_win = to_1d_array(self.winning.pnl.mean(group_by=group_by))
        avg_loss = to_1d_array(self.losing.pnl.mean(group_by=group_by))

        # Otherwise columns with only wins or losses will become NaNs
        has_values = to_1d_array(self.count(group_by=group_by)) > 0
        avg_win[np.isnan(avg_win) & has_values] = 0.
        avg_loss[np.isnan(avg_loss) & has_values] = 0.

        expectancy = win_rate * avg_win - (1 - win_rate) * np.abs(avg_loss)
        wrap_kwargs = merge_dicts(dict(name_or_index='expectancy'), wrap_kwargs)
        return self.wrapper.wrap_reduced(expectancy, group_by=group_by, **wrap_kwargs)

    @cached_method
    def sqn(self, group_by: tp.GroupByLike = None,
            wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """System Quality Number (SQN)."""
        count = to_1d_array(self.count(group_by=group_by))
        pnl_mean = to_1d_array(self.pnl.mean(group_by=group_by))
        pnl_std = to_1d_array(self.pnl.std(group_by=group_by))
        sqn = np.sqrt(count) * pnl_mean / pnl_std
        wrap_kwargs = merge_dicts(dict(name_or_index='sqn'), wrap_kwargs)
        return self.wrapper.wrap_reduced(sqn, group_by=group_by, **wrap_kwargs)

    # ############# Stats ############# #

    @property
    def stats_defaults(self) -> tp.Kwargs:
        """Defaults for `Trades.stats`.

        Merges `vectorbt.generic.ranges.Ranges.stats_defaults` and
        `trades.stats` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        trades_stats_cfg = settings['trades']['stats']

        return merge_dicts(
            Ranges.stats_defaults.__get__(self),
            trades_stats_cfg
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
            first_trade_start=dict(
                title='First Trade Start',
                calc_func='entry_idx.nth',
                n=0,
                wrap_kwargs=dict(to_index=True),
                tags=['trades', 'index']
            ),
            last_trade_end=dict(
                title='Last Trade End',
                calc_func='exit_idx.nth',
                n=-1,
                wrap_kwargs=dict(to_index=True),
                tags=['trades', 'index']
            ),
            coverage=dict(
                title='Coverage',
                calc_func='coverage',
                overlapping=False,
                normalize=False,
                apply_to_timedelta=True,
                tags=['ranges', 'coverage']
            ),
            overlap_coverage=dict(
                title='Overlap Coverage',
                calc_func='coverage',
                overlapping=True,
                normalize=False,
                apply_to_timedelta=True,
                tags=['ranges', 'coverage']
            ),
            total_records=dict(
                title='Total Records',
                calc_func='count',
                tags='records'
            ),
            total_long_trades=dict(
                title='Total Long Trades',
                calc_func='long.count',
                tags=['trades', 'long']
            ),
            total_short_trades=dict(
                title='Total Short Trades',
                calc_func='short.count',
                tags=['trades', 'short']
            ),
            total_closed_trades=dict(
                title='Total Closed Trades',
                calc_func='closed.count',
                tags=['trades', 'closed']
            ),
            total_open_trades=dict(
                title='Total Open Trades',
                calc_func='open.count',
                tags=['trades', 'open']
            ),
            open_trade_pnl=dict(
                title='Open Trade PnL',
                calc_func='open.pnl.sum',
                tags=['trades', 'open']
            ),
            win_rate=dict(
                title='Win Rate [%]',
                calc_func='closed.win_rate',
                post_calc_func=lambda self, out, settings: out * 100,
                tags=RepEval("['trades', *incl_open_tags]")
            ),
            winning_streak=dict(
                title='Max Win Streak',
                calc_func=RepEval("'winning_streak.max' if incl_open else 'closed.winning_streak.max'"),
                wrap_kwargs=dict(dtype=pd.Int64Dtype()),
                tags=RepEval("['trades', *incl_open_tags, 'streak']")
            ),
            losing_streak=dict(
                title='Max Loss Streak',
                calc_func=RepEval("'losing_streak.max' if incl_open else 'closed.losing_streak.max'"),
                wrap_kwargs=dict(dtype=pd.Int64Dtype()),
                tags=RepEval("['trades', *incl_open_tags, 'streak']")
            ),
            best_trade=dict(
                title='Best Trade [%]',
                calc_func=RepEval("'returns.max' if incl_open else 'closed.returns.max'"),
                post_calc_func=lambda self, out, settings: out * 100,
                tags=RepEval("['trades', *incl_open_tags]")
            ),
            worst_trade=dict(
                title='Worst Trade [%]',
                calc_func=RepEval("'returns.min' if incl_open else 'closed.returns.min'"),
                post_calc_func=lambda self, out, settings: out * 100,
                tags=RepEval("['trades', *incl_open_tags]")
            ),
            avg_winning_trade=dict(
                title='Avg Winning Trade [%]',
                calc_func=RepEval("'winning.returns.mean' if incl_open else 'closed.winning.returns.mean'"),
                post_calc_func=lambda self, out, settings: out * 100,
                tags=RepEval("['trades', *incl_open_tags, 'winning']")
            ),
            avg_losing_trade=dict(
                title='Avg Losing Trade [%]',
                calc_func=RepEval("'losing.returns.mean' if incl_open else 'closed.losing.returns.mean'"),
                post_calc_func=lambda self, out, settings: out * 100,
                tags=RepEval("['trades', *incl_open_tags, 'losing']")
            ),
            avg_winning_trade_duration=dict(
                title='Avg Winning Trade Duration',
                calc_func=RepEval("'winning.avg_duration' if incl_open else 'closed.winning.avg_duration'"),
                fill_wrap_kwargs=True,
                tags=RepEval("['trades', *incl_open_tags, 'winning', 'duration']")
            ),
            avg_losing_trade_duration=dict(
                title='Avg Losing Trade Duration',
                calc_func=RepEval("'losing.avg_duration' if incl_open else 'closed.losing.avg_duration'"),
                fill_wrap_kwargs=True,
                tags=RepEval("['trades', *incl_open_tags, 'losing', 'duration']")
            ),
            profit_factor=dict(
                title='Profit Factor',
                calc_func=RepEval("'profit_factor' if incl_open else 'closed.profit_factor'"),
                tags=RepEval("['trades', *incl_open_tags]")
            ),
            expectancy=dict(
                title='Expectancy',
                calc_func=RepEval("'expectancy' if incl_open else 'closed.expectancy'"),
                tags=RepEval("['trades', *incl_open_tags]")
            ),
            sqn=dict(
                title='SQN',
                calc_func=RepEval("'sqn' if incl_open else 'closed.sqn'"),
                tags=RepEval("['trades', *incl_open_tags]")
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def metrics(self) -> Config:
        return self._metrics

    # ############# Plotting ############# #

    def plot_pnl(self,
                 column: tp.Optional[tp.Label] = None,
                 pct_scale: bool = True,
                 marker_size_range: tp.Tuple[float, float] = (7, 14),
                 opacity_range: tp.Tuple[float, float] = (0.75, 0.9),
                 closed_profit_trace_kwargs: tp.KwargsLike = None,
                 closed_loss_trace_kwargs: tp.KwargsLike = None,
                 open_trace_kwargs: tp.KwargsLike = None,
                 hline_shape_kwargs: tp.KwargsLike = None,
                 add_trace_kwargs: tp.KwargsLike = None,
                 xref: str = 'x',
                 yref: str = 'y',
                 fig: tp.Optional[tp.BaseFigure] = None,
                 **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot trade PnL and returns.

        Args:
            column (str): Name of the column to plot.
            pct_scale (bool): Whether to set y-axis to `Trades.returns`, otherwise to `Trades.pnl`.
            marker_size_range (tuple): Range of marker size.
            opacity_range (tuple): Range of marker opacity.
            closed_profit_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for "Closed - Profit" markers.
            closed_loss_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for "Closed - Loss" markers.
            open_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for "Open" markers.
            hline_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for zeroline.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> import pandas as pd
            >>> from datetime import datetime, timedelta
            >>> import vectorbt as vbt

            >>> price = pd.Series([1., 2., 3., 4., 3., 2., 1.])
            >>> price.index = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(len(price))]
            >>> orders = pd.Series([1., -0.5, -0.5, 2., -0.5, -0.5, -0.5])
            >>> pf = vbt.Portfolio.from_orders(price, orders)
            >>> pf.trades.plot_pnl()
            ```

            ![](/assets/images/trades_plot_pnl.svg)
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        self_col = self.select_one(column=column, group_by=False)

        if closed_profit_trace_kwargs is None:
            closed_profit_trace_kwargs = {}
        if closed_loss_trace_kwargs is None:
            closed_loss_trace_kwargs = {}
        if open_trace_kwargs is None:
            open_trace_kwargs = {}
        if hline_shape_kwargs is None:
            hline_shape_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}
        marker_size_range = tuple(marker_size_range)
        xaxis = 'xaxis' + xref[1:]
        yaxis = 'yaxis' + yref[1:]

        if fig is None:
            fig = make_figure()
        if pct_scale:
            _layout_kwargs = dict()
            _layout_kwargs[yaxis] = dict(tickformat='.2%')
            fig.update_layout(**_layout_kwargs)
        fig.update_layout(**layout_kwargs)
        x_domain = get_domain(xref, fig)

        if self_col.count() > 0:
            # Extract information
            id_ = self_col.get_field_arr('id')
            id_title = self_col.get_field_title('id')

            exit_idx = self_col.get_map_field_to_index('exit_idx')
            exit_idx_title = self_col.get_field_title('exit_idx')

            pnl = self_col.get_field_arr('pnl')
            pnl_title = self_col.get_field_title('pnl')

            returns = self_col.get_field_arr('return')
            return_title = self_col.get_field_title('return')

            status = self_col.get_field_arr('status')

            neutral_mask = pnl == 0
            profit_mask = pnl > 0
            loss_mask = pnl < 0

            marker_size = min_rel_rescale(np.abs(returns), marker_size_range)
            opacity = max_rel_rescale(np.abs(returns), opacity_range)

            open_mask = status == TradeStatus.Open
            closed_profit_mask = (~open_mask) & profit_mask
            closed_loss_mask = (~open_mask) & loss_mask
            open_mask &= ~neutral_mask

            def _plot_scatter(mask: tp.Array1d, name: tp.TraceName, color: tp.Any, kwargs: tp.Kwargs) -> None:
                if np.any(mask):
                    if self_col.get_field_setting('parent_id', 'ignore', False):
                        customdata = np.stack((
                            id_[mask],
                            pnl[mask],
                            returns[mask]
                        ), axis=1)
                        hovertemplate = f"{id_title}: %{{customdata[0]}}" \
                                        f"<br>{exit_idx_title}: %{{x}}" \
                                        f"<br>{pnl_title}: %{{customdata[1]:.6f}}" \
                                        f"<br>{return_title}: %{{customdata[2]:.2%}}"
                    else:
                        parent_id = self_col.get_field_arr('parent_id')
                        parent_id_title = self_col.get_field_title('parent_id')
                        customdata = np.stack((
                            id_[mask],
                            parent_id[mask],
                            pnl[mask],
                            returns[mask]
                        ), axis=1)
                        hovertemplate = f"{id_title}: %{{customdata[0]}}" \
                                        f"<br>{parent_id_title}: %{{customdata[1]}}" \
                                        f"<br>{exit_idx_title}: %{{x}}" \
                                        f"<br>{pnl_title}: %{{customdata[2]:.6f}}" \
                                        f"<br>{return_title}: %{{customdata[3]:.2%}}"
                    scatter = go.Scatter(
                        x=exit_idx[mask],
                        y=returns[mask] if pct_scale else pnl[mask],
                        mode='markers',
                        marker=dict(
                            symbol='circle',
                            color=color,
                            size=marker_size[mask],
                            opacity=opacity[mask],
                            line=dict(
                                width=1,
                                color=adjust_lightness(color)
                            ),
                        ),
                        name=name,
                        customdata=customdata,
                        hovertemplate=hovertemplate
                    )
                    scatter.update(**kwargs)
                    fig.add_trace(scatter, **add_trace_kwargs)

            # Plot Closed - Profit scatter
            _plot_scatter(
                closed_profit_mask,
                'Closed - Profit',
                plotting_cfg['contrast_color_schema']['green'],
                closed_profit_trace_kwargs
            )

            # Plot Closed - Profit scatter
            _plot_scatter(
                closed_loss_mask,
                'Closed - Loss',
                plotting_cfg['contrast_color_schema']['red'],
                closed_loss_trace_kwargs
            )

            # Plot Open scatter
            _plot_scatter(
                open_mask,
                'Open',
                plotting_cfg['contrast_color_schema']['orange'],
                open_trace_kwargs
            )

        # Plot zeroline
        fig.add_shape(**merge_dicts(dict(
            type='line',
            xref="paper",
            yref=yref,
            x0=x_domain[0],
            y0=0,
            x1=x_domain[1],
            y1=0,
            line=dict(
                color="gray",
                dash="dash",
            )
        ), hline_shape_kwargs))
        return fig

    def plot(self,
             column: tp.Optional[tp.Label] = None,
             plot_zones: bool = True,
             close_trace_kwargs: tp.KwargsLike = None,
             entry_trace_kwargs: tp.KwargsLike = None,
             exit_trace_kwargs: tp.KwargsLike = None,
             exit_profit_trace_kwargs: tp.KwargsLike = None,
             exit_loss_trace_kwargs: tp.KwargsLike = None,
             active_trace_kwargs: tp.KwargsLike = None,
             profit_shape_kwargs: tp.KwargsLike = None,
             loss_shape_kwargs: tp.KwargsLike = None,
             add_trace_kwargs: tp.KwargsLike = None,
             xref: str = 'x',
             yref: str = 'y',
             fig: tp.Optional[tp.BaseFigure] = None,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot orders.

        Args:
            column (str): Name of the column to plot.
            plot_zones (bool): Whether to plot zones.

                Set to False if there are many trades within one position.
            close_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `Trades.close`.
            entry_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for "Entry" markers.
            exit_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for "Exit" markers.
            exit_profit_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for "Exit - Profit" markers.
            exit_loss_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for "Exit - Loss" markers.
            active_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for "Active" markers.
            profit_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for profit zones.
            loss_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for loss zones.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> import pandas as pd
            >>> from datetime import datetime, timedelta
            >>> import vectorbt as vbt

            >>> price = pd.Series([1., 2., 3., 4., 3., 2., 1.], name='Price')
            >>> price.index = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(len(price))]
            >>> orders = pd.Series([1., -0.5, -0.5, 2., -0.5, -0.5, -0.5])
            >>> pf = vbt.Portfolio.from_orders(price, orders)
            >>> pf.trades.plot()
            ```

            ![](/assets/images/trades_plot.svg)
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        self_col = self.select_one(column=column, group_by=False)

        if close_trace_kwargs is None:
            close_trace_kwargs = {}
        close_trace_kwargs = merge_dicts(dict(
            line=dict(
                color=plotting_cfg['color_schema']['blue']
            ),
            name='Close'
        ), close_trace_kwargs)
        if entry_trace_kwargs is None:
            entry_trace_kwargs = {}
        if exit_trace_kwargs is None:
            exit_trace_kwargs = {}
        if exit_profit_trace_kwargs is None:
            exit_profit_trace_kwargs = {}
        if exit_loss_trace_kwargs is None:
            exit_loss_trace_kwargs = {}
        if active_trace_kwargs is None:
            active_trace_kwargs = {}
        if profit_shape_kwargs is None:
            profit_shape_kwargs = {}
        if loss_shape_kwargs is None:
            loss_shape_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}

        if fig is None:
            fig = make_figure()
        fig.update_layout(**layout_kwargs)

        # Plot close
        if self_col.close is not None:
            fig = self_col.close.vbt.plot(trace_kwargs=close_trace_kwargs, add_trace_kwargs=add_trace_kwargs, fig=fig)

        if self_col.count() > 0:
            # Extract information
            id_ = self_col.get_field_arr('id')
            id_title = self_col.get_field_title('id')

            size = self_col.get_field_arr('size')
            size_title = self_col.get_field_title('size')

            entry_idx = self_col.get_map_field_to_index('entry_idx')
            entry_idx_title = self_col.get_field_title('entry_idx')

            entry_price = self_col.get_field_arr('entry_price')
            entry_price_title = self_col.get_field_title('entry_price')

            entry_fees = self_col.get_field_arr('entry_fees')
            entry_fees_title = self_col.get_field_title('entry_fees')

            exit_idx = self_col.get_map_field_to_index('exit_idx')
            exit_idx_title = self_col.get_field_title('exit_idx')

            exit_price = self_col.get_field_arr('exit_price')
            exit_price_title = self_col.get_field_title('exit_price')

            exit_fees = self_col.get_field_arr('exit_fees')
            exit_fees_title = self_col.get_field_title('exit_fees')

            direction = self_col.get_apply_mapping_arr('direction')
            direction_title = self_col.get_field_title('direction')

            pnl = self_col.get_field_arr('pnl')
            pnl_title = self_col.get_field_title('pnl')

            returns = self_col.get_field_arr('return')
            return_title = self_col.get_field_title('return')

            status = self_col.get_field_arr('status')

            duration = np.vectorize(str)(self_col.wrapper.to_timedelta(
                self_col.duration.values, to_pd=True, silence_warnings=True))

            # Plot Entry markers
            if self_col.get_field_setting('parent_id', 'ignore', False):
                entry_customdata = np.stack((
                    id_,
                    size,
                    entry_fees,
                    direction
                ), axis=1)
                entry_hovertemplate = f"{id_title}: %{{customdata[0]}}" \
                                      f"<br>{size_title}: %{{customdata[1]:.6f}}" \
                                      f"<br>{entry_idx_title}: %{{x}}" \
                                      f"<br>{entry_price_title}: %{{y}}" \
                                      f"<br>{entry_fees_title}: %{{customdata[2]:.6f}}" \
                                      f"<br>{direction_title}: %{{customdata[3]}}"
            else:
                parent_id = self_col.get_field_arr('parent_id')
                parent_id_title = self_col.get_field_title('parent_id')
                entry_customdata = np.stack((
                    id_,
                    parent_id,
                    size,
                    entry_fees,
                    direction
                ), axis=1)
                entry_hovertemplate = f"{id_title}: %{{customdata[0]}}" \
                                      f"<br>{parent_id_title}: %{{customdata[1]}}" \
                                      f"<br>{size_title}: %{{customdata[2]:.6f}}" \
                                      f"<br>{entry_idx_title}: %{{x}}" \
                                      f"<br>{entry_price_title}: %{{y}}" \
                                      f"<br>{entry_fees_title}: %{{customdata[3]:.6f}}" \
                                      f"<br>{direction_title}: %{{customdata[4]}}"
            entry_scatter = go.Scatter(
                x=entry_idx,
                y=entry_price,
                mode='markers',
                marker=dict(
                    symbol='square',
                    color=plotting_cfg['contrast_color_schema']['blue'],
                    size=7,
                    line=dict(
                        width=1,
                        color=adjust_lightness(plotting_cfg['contrast_color_schema']['blue'])
                    )
                ),
                name='Entry',
                customdata=entry_customdata,
                hovertemplate=entry_hovertemplate
            )
            entry_scatter.update(**entry_trace_kwargs)
            fig.add_trace(entry_scatter, **add_trace_kwargs)

            # Plot end markers
            def _plot_end_markers(mask: tp.Array1d, name: tp.TraceName, color: tp.Any, kwargs: tp.Kwargs) -> None:
                if np.any(mask):
                    if self_col.get_field_setting('parent_id', 'ignore', False):
                        exit_customdata = np.stack((
                            id_[mask],
                            size[mask],
                            exit_fees[mask],
                            pnl[mask],
                            returns[mask],
                            direction[mask],
                            duration[mask]
                        ), axis=1)
                        exit_hovertemplate = f"{id_title}: %{{customdata[0]}}" \
                                             f"<br>{size_title}: %{{customdata[1]:.6f}}" \
                                             f"<br>{exit_idx_title}: %{{x}}" \
                                             f"<br>{exit_price_title}: %{{y}}" \
                                             f"<br>{exit_fees_title}: %{{customdata[2]:.6f}}" \
                                             f"<br>{pnl_title}: %{{customdata[3]:.6f}}" \
                                             f"<br>{return_title}: %{{customdata[4]:.2%}}" \
                                             f"<br>{direction_title}: %{{customdata[5]}}" \
                                             f"<br>Duration: %{{customdata[6]}}"
                    else:
                        parent_id = self_col.get_field_arr('parent_id')
                        parent_id_title = self_col.get_field_title('parent_id')
                        exit_customdata = np.stack((
                            id_[mask],
                            parent_id[mask],
                            size[mask],
                            exit_fees[mask],
                            pnl[mask],
                            returns[mask],
                            direction[mask],
                            duration[mask]
                        ), axis=1)
                        exit_hovertemplate = f"{id_title}: %{{customdata[0]}}" \
                                             f"<br>{parent_id_title}: %{{customdata[1]}}" \
                                             f"<br>{size_title}: %{{customdata[2]:.6f}}" \
                                             f"<br>{exit_idx_title}: %{{x}}" \
                                             f"<br>{exit_price_title}: %{{y}}" \
                                             f"<br>{exit_fees_title}: %{{customdata[3]:.6f}}" \
                                             f"<br>{pnl_title}: %{{customdata[4]:.6f}}" \
                                             f"<br>{return_title}: %{{customdata[5]:.2%}}" \
                                             f"<br>{direction_title}: %{{customdata[6]}}" \
                                             f"<br>Duration: %{{customdata[7]}}"
                    scatter = go.Scatter(
                        x=exit_idx[mask],
                        y=exit_price[mask],
                        mode='markers',
                        marker=dict(
                            symbol='square',
                            color=color,
                            size=7,
                            line=dict(
                                width=1,
                                color=adjust_lightness(color)
                            )
                        ),
                        name=name,
                        customdata=exit_customdata,
                        hovertemplate=exit_hovertemplate
                    )
                    scatter.update(**kwargs)
                    fig.add_trace(scatter, **add_trace_kwargs)

            # Plot Exit markers
            _plot_end_markers(
                (status == TradeStatus.Closed) & (pnl == 0.),
                'Exit',
                plotting_cfg['contrast_color_schema']['gray'],
                exit_trace_kwargs
            )

            # Plot Exit - Profit markers
            _plot_end_markers(
                (status == TradeStatus.Closed) & (pnl > 0.),
                'Exit - Profit',
                plotting_cfg['contrast_color_schema']['green'],
                exit_profit_trace_kwargs
            )

            # Plot Exit - Loss markers
            _plot_end_markers(
                (status == TradeStatus.Closed) & (pnl < 0.),
                'Exit - Loss',
                plotting_cfg['contrast_color_schema']['red'],
                exit_loss_trace_kwargs
            )

            # Plot Active markers
            _plot_end_markers(
                status == TradeStatus.Open,
                'Active',
                plotting_cfg['contrast_color_schema']['orange'],
                active_trace_kwargs
            )

            if plot_zones:
                profit_mask = pnl > 0.
                if np.any(profit_mask):
                    # Plot profit zones
                    for i in np.flatnonzero(profit_mask):
                        fig.add_shape(**merge_dicts(dict(
                            type="rect",
                            xref=xref,
                            yref=yref,
                            x0=entry_idx[i],
                            y0=entry_price[i],
                            x1=exit_idx[i],
                            y1=exit_price[i],
                            fillcolor='green',
                            opacity=0.2,
                            layer="below",
                            line_width=0,
                        ), profit_shape_kwargs))

                loss_mask = pnl < 0.
                if np.any(loss_mask):
                    # Plot loss zones
                    for i in np.flatnonzero(loss_mask):
                        fig.add_shape(**merge_dicts(dict(
                            type="rect",
                            xref=xref,
                            yref=yref,
                            x0=entry_idx[i],
                            y0=entry_price[i],
                            x1=exit_idx[i],
                            y1=exit_price[i],
                            fillcolor='red',
                            opacity=0.2,
                            layer="below",
                            line_width=0,
                        ), loss_shape_kwargs))

        return fig

    @property
    def plots_defaults(self) -> tp.Kwargs:
        """Defaults for `Trades.plots`.

        Merges `vectorbt.generic.ranges.Ranges.plots_defaults` and
        `trades.plots` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        trades_plots_cfg = settings['trades']['plots']

        return merge_dicts(
            Ranges.plots_defaults.__get__(self),
            trades_plots_cfg
        )

    _subplots: tp.ClassVar[Config] = Config(
        dict(
            plot=dict(
                title="Trades",
                yaxis_kwargs=dict(title="Price"),
                check_is_not_grouped=True,
                plot_func='plot',
                tags='trades'
            ),
            plot_pnl=dict(
                title="Trade PnL",
                yaxis_kwargs=dict(title="Trade PnL"),
                check_is_not_grouped=True,
                plot_func='plot_pnl',
                tags='trades'
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def subplots(self) -> Config:
        return self._subplots


Trades.override_field_config_doc(__pdoc__)
Trades.override_metrics_doc(__pdoc__)
Trades.override_subplots_doc(__pdoc__)

# ############# EntryTrades ############# #

entry_trades_field_config = Config(
    dict(
        settings={
            'id': dict(
                title='Entry Trade Id'
            ),
            'idx': dict(
                name='entry_idx'
            )
        }
    ),
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['entry_trades_field_config'] = f"""Field config for `EntryTrades`.

```json
{entry_trades_field_config.to_doc()}
```
"""

EntryTradesT = tp.TypeVar("EntryTradesT", bound="EntryTrades")


@override_field_config(entry_trades_field_config)
class EntryTrades(Trades):
    """Extends `Trades` for working with entry trade records."""

    @classmethod
    def from_orders(cls: tp.Type[EntryTradesT],
                    orders: Orders,
                    close: tp.Optional[tp.ArrayLike] = None,
                    attach_close: bool = True,
                    **kwargs) -> EntryTradesT:
        """Build `EntryTrades` from `vectorbt.portfolio.orders.Orders`."""
        if close is None:
            close = orders.close
        trade_records_arr = nb.get_entry_trades_nb(
            orders.values,
            to_2d_array(close),
            orders.col_mapper.col_map
        )
        return cls(orders.wrapper, trade_records_arr, close=close if attach_close else None, **kwargs)


# ############# ExitTrades ############# #

exit_trades_field_config = Config(
    dict(
        settings={
            'id': dict(
                title='Exit Trade Id'
            )
        }
    ),
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['exit_trades_field_config'] = f"""Field config for `ExitTrades`.

```json
{exit_trades_field_config.to_doc()}
```
"""

ExitTradesT = tp.TypeVar("ExitTradesT", bound="ExitTrades")


@override_field_config(exit_trades_field_config)
class ExitTrades(Trades):
    """Extends `Trades` for working with exit trade records."""

    @classmethod
    def from_orders(cls: tp.Type[ExitTradesT],
                    orders: Orders,
                    close: tp.Optional[tp.ArrayLike] = None,
                    attach_close: bool = True,
                    **kwargs) -> ExitTradesT:
        """Build `ExitTrades` from `vectorbt.portfolio.orders.Orders`."""
        if close is None:
            close = orders.close
        trade_records_arr = nb.get_exit_trades_nb(
            orders.values,
            to_2d_array(close),
            orders.col_mapper.col_map
        )
        return cls(orders.wrapper, trade_records_arr, close=close if attach_close else None, **kwargs)


# ############# Positions ############# #

positions_field_config = Config(
    dict(
        settings={
            'id': dict(
                title='Position Id'
            ),
            'parent_id': dict(
                title='Parent Id',
                ignore=True
            )
        }
    ),
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['positions_field_config'] = f"""Field config for `Positions`.

```json
{positions_field_config.to_doc()}
```
"""

PositionsT = tp.TypeVar("PositionsT", bound="Positions")


@override_field_config(positions_field_config)
class Positions(Trades):
    """Extends `Trades` for working with position records."""

    @property
    def field_config(self) -> Config:
        return self._field_config

    @classmethod
    def from_trades(cls: tp.Type[PositionsT],
                    trades: Trades,
                    close: tp.Optional[tp.ArrayLike] = None,
                    attach_close: bool = True,
                    **kwargs) -> PositionsT:
        """Build `Positions` from `Trades`."""
        if close is None:
            close = trades.close
        position_records_arr = nb.get_positions_nb(trades.values, trades.col_mapper.col_map)
        return cls(trades.wrapper, position_records_arr, close=close if attach_close else None, **kwargs)
