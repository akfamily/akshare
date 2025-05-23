# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Base class for working with order records.

Order records capture information on filled orders. Orders are mainly populated when simulating
a portfolio and can be accessed as `vectorbt.portfolio.base.Portfolio.orders`.

```pycon
>>> import pandas as pd
>>> import numpy as np
>>> from datetime import datetime, timedelta
>>> import vectorbt as vbt

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
>>> orders = pf.orders

>>> orders.buy.count()
a    58
b    51
Name: count, dtype: int64

>>> orders.sell.count()
a    42
b    49
Name: count, dtype: int64
```

## Stats

!!! hint
    See `vectorbt.generic.stats_builder.StatsBuilderMixin.stats` and `Orders.metrics`.

```pycon
>>> orders['a'].stats()
Start                2020-01-01 00:00:00
End                  2020-04-09 00:00:00
Period                 100 days 00:00:00
Total Records                        100
Total Buy Orders                      58
Total Sell Orders                     42
Min Size                        0.003033
Max Size                        0.989877
Avg Size                        0.508608
Avg Buy Size                    0.468802
Avg Sell Size                   0.563577
Avg Buy Price                   1.437037
Avg Sell Price                  1.515951
Total Fees                      0.740177
Min Fees                        0.000052
Max Fees                        0.016224
Avg Fees                        0.007402
Avg Buy Fees                    0.006771
Avg Sell Fees                   0.008273
Name: a, dtype: object
```

`Orders.stats` also supports (re-)grouping:

```pycon
>>> orders.stats(group_by=True)
Start                2020-01-01 00:00:00
End                  2020-04-09 00:00:00
Period                 100 days 00:00:00
Total Records                        200
Total Buy Orders                     109
Total Sell Orders                     91
Min Size                        0.003033
Max Size                        0.989877
Avg Size                        0.506279
Avg Buy Size                    0.472504
Avg Sell Size                   0.546735
Avg Buy Price                    1.47336
Avg Sell Price                  1.496759
Total Fees                      1.483343
Min Fees                        0.000052
Max Fees                        0.018319
Avg Fees                        0.007417
Avg Buy Fees                    0.006881
Avg Sell Fees                   0.008058
Name: group, dtype: object
```

## Plots

!!! hint
    See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots` and `Orders.subplots`.

`Orders` class has a single subplot based on `Orders.plot`:

```pycon
>>> orders['a'].plots()
```

![](/assets/images/orders_plots.svg)
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from vectorbt import _typing as tp
from vectorbt.base.array_wrapper import ArrayWrapper
from vectorbt.base.reshape_fns import to_2d_array
from vectorbt.portfolio.enums import order_dt, OrderSide
from vectorbt.records.base import Records
from vectorbt.records.decorators import attach_fields, override_field_config
from vectorbt.utils.colors import adjust_lightness
from vectorbt.utils.config import merge_dicts, Config
from vectorbt.utils.figure import make_figure

__pdoc__ = {}

orders_field_config = Config(
    dict(
        dtype=order_dt,
        settings=dict(
            id=dict(
                title='Order Id'
            ),
            size=dict(
                title='Size'
            ),
            price=dict(
                title='Price'
            ),
            fees=dict(
                title='Fees'
            ),
            side=dict(
                title='Side',
                mapping=OrderSide
            )
        )
    ),
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['orders_field_config'] = f"""Field config for `Orders`.

```json
{orders_field_config.to_doc()}
```
"""

orders_attach_field_config = Config(
    dict(
        side=dict(
            attach_filters=True
        )
    ),
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['orders_attach_field_config'] = f"""Config of fields to be attached to `Orders`.

```json
{orders_attach_field_config.to_doc()}
```
"""

OrdersT = tp.TypeVar("OrdersT", bound="Orders")


@attach_fields(orders_attach_field_config)
@override_field_config(orders_field_config)
class Orders(Records):
    """Extends `Records` for working with order records."""

    @property
    def field_config(self) -> Config:
        return self._field_config

    def __init__(self,
                 wrapper: ArrayWrapper,
                 records_arr: tp.RecordArray,
                 close: tp.Optional[tp.ArrayLike] = None,
                 **kwargs) -> None:
        Records.__init__(
            self,
            wrapper,
            records_arr,
            close=close,
            **kwargs
        )
        self._close = close

    def indexing_func(self: OrdersT, pd_indexing_func: tp.PandasIndexingFunc, **kwargs) -> OrdersT:
        """Perform indexing on `Orders`."""
        new_wrapper, new_records_arr, group_idxs, col_idxs = \
            Records.indexing_func_meta(self, pd_indexing_func, **kwargs)
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

    # ############# Stats ############# #

    @property
    def stats_defaults(self) -> tp.Kwargs:
        """Defaults for `Orders.stats`.

        Merges `vectorbt.records.base.Records.stats_defaults` and
        `orders.stats` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        orders_stats_cfg = settings['orders']['stats']

        return merge_dicts(
            Records.stats_defaults.__get__(self),
            orders_stats_cfg
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
            total_records=dict(
                title='Total Records',
                calc_func='count',
                tags='records'
            ),
            total_buy_orders=dict(
                title='Total Buy Orders',
                calc_func='buy.count',
                tags=['orders', 'buy']
            ),
            total_sell_orders=dict(
                title='Total Sell Orders',
                calc_func='sell.count',
                tags=['orders', 'sell']
            ),
            min_size=dict(
                title='Min Size',
                calc_func='size.min',
                tags=['orders', 'size']
            ),
            max_size=dict(
                title='Max Size',
                calc_func='size.max',
                tags=['orders', 'size']
            ),
            avg_size=dict(
                title='Avg Size',
                calc_func='size.mean',
                tags=['orders', 'size']
            ),
            avg_buy_size=dict(
                title='Avg Buy Size',
                calc_func='buy.size.mean',
                tags=['orders', 'buy', 'size']
            ),
            avg_sell_size=dict(
                title='Avg Sell Size',
                calc_func='sell.size.mean',
                tags=['orders', 'sell', 'size']
            ),
            avg_buy_price=dict(
                title='Avg Buy Price',
                calc_func='buy.price.mean',
                tags=['orders', 'buy', 'price']
            ),
            avg_sell_price=dict(
                title='Avg Sell Price',
                calc_func='sell.price.mean',
                tags=['orders', 'sell', 'price']
            ),
            total_fees=dict(
                title='Total Fees',
                calc_func='fees.sum',
                tags=['orders', 'fees']
            ),
            min_fees=dict(
                title='Min Fees',
                calc_func='fees.min',
                tags=['orders', 'fees']
            ),
            max_fees=dict(
                title='Max Fees',
                calc_func='fees.max',
                tags=['orders', 'fees']
            ),
            avg_fees=dict(
                title='Avg Fees',
                calc_func='fees.mean',
                tags=['orders', 'fees']
            ),
            avg_buy_fees=dict(
                title='Avg Buy Fees',
                calc_func='buy.fees.mean',
                tags=['orders', 'buy', 'fees']
            ),
            avg_sell_fees=dict(
                title='Avg Sell Fees',
                calc_func='sell.fees.mean',
                tags=['orders', 'sell', 'fees']
            ),
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def metrics(self) -> Config:
        return self._metrics

    # ############# Plotting ############# #

    def plot(self,
             column: tp.Optional[tp.Label] = None,
             close_trace_kwargs: tp.KwargsLike = None,
             buy_trace_kwargs: tp.KwargsLike = None,
             sell_trace_kwargs: tp.KwargsLike = None,
             add_trace_kwargs: tp.KwargsLike = None,
             fig: tp.Optional[tp.BaseFigure] = None,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot orders.

        Args:
            column (str): Name of the column to plot.
            close_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `Orders.close`.
            buy_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for "Buy" markers.
            sell_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for "Sell" markers.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> import pandas as pd
            >>> from datetime import datetime, timedelta
            >>> import vectorbt as vbt

            >>> price = pd.Series([1., 2., 3., 2., 1.], name='Price')
            >>> price.index = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(len(price))]
            >>> size = pd.Series([1., 1., 1., 1., -1.])
            >>> orders = vbt.Portfolio.from_orders(price, size).orders

            >>> orders.plot()
            ```

            ![](/assets/images/orders_plot.svg)
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
        if buy_trace_kwargs is None:
            buy_trace_kwargs = {}
        if sell_trace_kwargs is None:
            sell_trace_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}

        if fig is None:
            fig = make_figure()
        fig.update_layout(**layout_kwargs)

        # Plot price
        if self_col.close is not None:
            fig = self_col.close.vbt.plot(trace_kwargs=close_trace_kwargs, add_trace_kwargs=add_trace_kwargs, fig=fig)

        if self_col.count() > 0:
            # Extract information
            id_ = self_col.get_field_arr('id')
            id_title = self_col.get_field_title('id')

            idx = self_col.get_map_field_to_index('idx')
            idx_title = self_col.get_field_title('idx')

            size = self_col.get_field_arr('size')
            size_title = self_col.get_field_title('size')

            fees = self_col.get_field_arr('fees')
            fees_title = self_col.get_field_title('fees')

            price = self_col.get_field_arr('price')
            price_title = self_col.get_field_title('price')

            side = self_col.get_field_arr('side')

            buy_mask = side == OrderSide.Buy
            if buy_mask.any():
                # Plot buy markers
                buy_customdata = np.stack((
                    id_[buy_mask],
                    size[buy_mask],
                    fees[buy_mask]
                ), axis=1)
                buy_scatter = go.Scatter(
                    x=idx[buy_mask],
                    y=price[buy_mask],
                    mode='markers',
                    marker=dict(
                        symbol='triangle-up',
                        color=plotting_cfg['contrast_color_schema']['green'],
                        size=8,
                        line=dict(
                            width=1,
                            color=adjust_lightness(plotting_cfg['contrast_color_schema']['green'])
                        )
                    ),
                    name='Buy',
                    customdata=buy_customdata,
                    hovertemplate=f"{id_title}: %{{customdata[0]}}"
                                  f"<br>{idx_title}: %{{x}}"
                                  f"<br>{price_title}: %{{y}}"
                                  f"<br>{size_title}: %{{customdata[1]:.6f}}"
                                  f"<br>{fees_title}: %{{customdata[2]:.6f}}"
                )
                buy_scatter.update(**buy_trace_kwargs)
                fig.add_trace(buy_scatter, **add_trace_kwargs)

            sell_mask = side == OrderSide.Sell
            if sell_mask.any():
                # Plot sell markers
                sell_customdata = np.stack((
                    id_[sell_mask],
                    size[sell_mask],
                    fees[sell_mask]
                ), axis=1)
                sell_scatter = go.Scatter(
                    x=idx[sell_mask],
                    y=price[sell_mask],
                    mode='markers',
                    marker=dict(
                        symbol='triangle-down',
                        color=plotting_cfg['contrast_color_schema']['red'],
                        size=8,
                        line=dict(
                            width=1,
                            color=adjust_lightness(plotting_cfg['contrast_color_schema']['red'])
                        )
                    ),
                    name='Sell',
                    customdata=sell_customdata,
                    hovertemplate=f"{id_title}: %{{customdata[0]}}"
                                  f"<br>{idx_title}: %{{x}}"
                                  f"<br>{price_title}: %{{y}}"
                                  f"<br>{size_title}: %{{customdata[1]:.6f}}"
                                  f"<br>{fees_title}: %{{customdata[2]:.6f}}"
                )
                sell_scatter.update(**sell_trace_kwargs)
                fig.add_trace(sell_scatter, **add_trace_kwargs)

        return fig

    @property
    def plots_defaults(self) -> tp.Kwargs:
        """Defaults for `Orders.plots`.

        Merges `vectorbt.records.base.Records.plots_defaults` and
        `orders.plots` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        orders_plots_cfg = settings['orders']['plots']

        return merge_dicts(
            Records.plots_defaults.__get__(self),
            orders_plots_cfg
        )

    _subplots: tp.ClassVar[Config] = Config(
        dict(
            plot=dict(
                title="Orders",
                yaxis_kwargs=dict(title="Price"),
                check_is_not_grouped=True,
                plot_func='plot',
                tags='orders'
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def subplots(self) -> Config:
        return self._subplots


Orders.override_field_config_doc(__pdoc__)
Orders.override_metrics_doc(__pdoc__)
Orders.override_subplots_doc(__pdoc__)
