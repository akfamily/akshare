# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Base class for working with drawdown records.

Drawdown records capture information on drawdowns. Since drawdowns are ranges,
they subclass `vectorbt.generic.ranges.Ranges`.

!!! warning
    `Drawdowns` return both recovered AND active drawdowns, which may skew your performance results.
    To only consider recovered drawdowns, you should explicitly query `recovered` attribute.

Using `Drawdowns.from_ts`, you can generate drawdown records for any time series and analyze them right away.

```pycon
>>> import vectorbt as vbt
>>> import numpy as np
>>> import pandas as pd

>>> start = '2019-10-01 UTC'  # crypto is in UTC
>>> end = '2020-01-01 UTC'
>>> price = vbt.YFData.download('BTC-USD', start=start, end=end).get('Close')
>>> price = price.rename(None)

>>> drawdowns = vbt.Drawdowns.from_ts(price, wrapper_kwargs=dict(freq='d'))

>>> drawdowns.records_readable
   Drawdown Id  Column            Peak Timestamp           Start Timestamp  \\
0            0       0 2019-10-02 00:00:00+00:00 2019-10-03 00:00:00+00:00
1            1       0 2019-10-09 00:00:00+00:00 2019-10-10 00:00:00+00:00
2            2       0 2019-10-27 00:00:00+00:00 2019-10-28 00:00:00+00:00

           Valley Timestamp             End Timestamp   Peak Value  \\
0 2019-10-06 00:00:00+00:00 2019-10-09 00:00:00+00:00  8393.041992
1 2019-10-24 00:00:00+00:00 2019-10-25 00:00:00+00:00  8595.740234
2 2019-12-17 00:00:00+00:00 2020-01-01 00:00:00+00:00  9551.714844

   Valley Value    End Value     Status
0   7988.155762  8595.740234  Recovered
1   7493.488770  8660.700195  Recovered
2   6640.515137  7200.174316     Active

>>> drawdowns.duration.max(wrap_kwargs=dict(to_timedelta=True))
Timedelta('66 days 00:00:00')
```

## From accessors

Moreover, all generic accessors have a property `drawdowns` and a method `get_drawdowns`:

```pycon
>>> # vectorbt.generic.accessors.GenericAccessor.drawdowns.coverage
>>> price.vbt.drawdowns.coverage()
0.9354838709677419
```

## Stats

!!! hint
    See `vectorbt.generic.stats_builder.StatsBuilderMixin.stats` and `Drawdowns.metrics`.

```pycon
>>> df = pd.DataFrame({
...     'a': [1, 2, 1, 3, 2],
...     'b': [2, 3, 1, 2, 1]
... })

>>> drawdowns = df.vbt(freq='d').drawdowns

>>> drawdowns['a'].stats()
Start                                        0
End                                          4
Period                         5 days 00:00:00
Coverage [%]                              40.0
Total Records                                2
Total Recovered Drawdowns                    1
Total Active Drawdowns                       1
Active Drawdown [%]                  33.333333
Active Duration                1 days 00:00:00
Active Recovery [%]                        0.0
Active Recovery Return [%]                 0.0
Active Recovery Duration       0 days 00:00:00
Max Drawdown [%]                          50.0
Avg Drawdown [%]                          50.0
Max Drawdown Duration          1 days 00:00:00
Avg Drawdown Duration          1 days 00:00:00
Max Recovery Return [%]                  200.0
Avg Recovery Return [%]                  200.0
Max Recovery Duration          1 days 00:00:00
Avg Recovery Duration          1 days 00:00:00
Avg Recovery Duration Ratio                1.0
Name: a, dtype: object
```

By default, the metrics `max_dd`, `avg_dd`, `max_dd_duration`, and `avg_dd_duration` do
not include active drawdowns. To change that, pass `incl_active=True`:

```pycon
>>> drawdowns['a'].stats(settings=dict(incl_active=True))
Start                                        0
End                                          4
Period                         5 days 00:00:00
Coverage [%]                              40.0
Total Records                                2
Total Recovered Drawdowns                    1
Total Active Drawdowns                       1
Active Drawdown [%]                  33.333333
Active Duration                1 days 00:00:00
Active Recovery [%]                        0.0
Active Recovery Return [%]                 0.0
Active Recovery Duration       0 days 00:00:00
Max Drawdown [%]                          50.0
Avg Drawdown [%]                     41.666667
Max Drawdown Duration          1 days 00:00:00
Avg Drawdown Duration          1 days 00:00:00
Max Recovery Return [%]                  200.0
Avg Recovery Return [%]                  200.0
Max Recovery Duration          1 days 00:00:00
Avg Recovery Duration          1 days 00:00:00
Avg Recovery Duration Ratio                1.0
Name: a, dtype: object
```

`Drawdowns.stats` also supports (re-)grouping:

```pycon
>>> drawdowns['a'].stats(group_by=True)
UserWarning: Metric 'active_dd' does not support grouped data
UserWarning: Metric 'active_duration' does not support grouped data
UserWarning: Metric 'active_recovery' does not support grouped data
UserWarning: Metric 'active_recovery_return' does not support grouped data
UserWarning: Metric 'active_recovery_duration' does not support grouped data

Start                                        0
End                                          4
Period                         5 days 00:00:00
Coverage [%]                              40.0
Total Records                                2
Total Recovered Drawdowns                    1
Total Active Drawdowns                       1
Max Drawdown [%]                          50.0
Avg Drawdown [%]                          50.0
Max Drawdown Duration          1 days 00:00:00
Avg Drawdown Duration          1 days 00:00:00
Max Recovery Return [%]                  200.0
Avg Recovery Return [%]                  200.0
Max Recovery Duration          1 days 00:00:00
Avg Recovery Duration          1 days 00:00:00
Avg Recovery Duration Ratio                1.0
Name: group, dtype: object
```

## Plots

!!! hint
    See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots` and `Drawdowns.subplots`.

`Drawdowns` class has a single subplot based on `Drawdowns.plot`:

```pycon
>>> drawdowns['a'].plots()
```

![](/assets/images/drawdowns_plots.svg)
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from vectorbt import _typing as tp
from vectorbt.base.array_wrapper import ArrayWrapper
from vectorbt.base.reshape_fns import to_2d_array, to_pd_array
from vectorbt.generic import nb
from vectorbt.generic.enums import DrawdownStatus, drawdown_dt
from vectorbt.generic.ranges import Ranges
from vectorbt.records.decorators import override_field_config, attach_fields
from vectorbt.records.mapped_array import MappedArray
from vectorbt.utils.colors import adjust_lightness
from vectorbt.utils.config import merge_dicts, Config
from vectorbt.utils.decorators import cached_property, cached_method
from vectorbt.utils.figure import make_figure, get_domain
from vectorbt.utils.template import RepEval

__pdoc__ = {}

dd_field_config = Config(
    dict(
        dtype=drawdown_dt,
        settings=dict(
            id=dict(
                title='Drawdown Id'
            ),
            peak_idx=dict(
                title='Peak Timestamp',
                mapping='index'
            ),
            valley_idx=dict(
                title='Valley Timestamp',
                mapping='index'
            ),
            peak_val=dict(
                title='Peak Value',
            ),
            valley_val=dict(
                title='Valley Value',
            ),
            end_val=dict(
                title='End Value',
            ),
            status=dict(
                mapping=DrawdownStatus
            )
        )
    ),
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['dd_field_config'] = f"""Field config for `Drawdowns`.

```json
{dd_field_config.to_doc()}
```
"""

dd_attach_field_config = Config(
    dict(
        status=dict(
            attach_filters=True
        )
    ),
    readonly=True,
    as_attrs=False
)
"""_"""

__pdoc__['dd_attach_field_config'] = f"""Config of fields to be attached to `Drawdowns`.

```json
{dd_attach_field_config.to_doc()}
```
"""

DrawdownsT = tp.TypeVar("DrawdownsT", bound="Drawdowns")


@attach_fields(dd_attach_field_config)
@override_field_config(dd_field_config)
class Drawdowns(Ranges):
    """Extends `vectorbt.generic.ranges.Ranges` for working with drawdown records.

    Requires `records_arr` to have all fields defined in `vectorbt.generic.enums.drawdown_dt`."""

    @property
    def field_config(self) -> Config:
        return self._field_config

    def __init__(self,
                 wrapper: ArrayWrapper,
                 records_arr: tp.RecordArray,
                 ts: tp.Optional[tp.ArrayLike] = None,
                 **kwargs) -> None:
        Ranges.__init__(
            self,
            wrapper,
            records_arr,
            ts=ts,
            **kwargs
        )
        self._ts = ts

    def indexing_func(self: DrawdownsT, pd_indexing_func: tp.PandasIndexingFunc, **kwargs) -> DrawdownsT:
        """Perform indexing on `Drawdowns`."""
        new_wrapper, new_records_arr, _, col_idxs = \
            Ranges.indexing_func_meta(self, pd_indexing_func, **kwargs)
        if self.ts is not None:
            new_ts = new_wrapper.wrap(self.ts.values[:, col_idxs], group_by=False)
        else:
            new_ts = None
        return self.replace(
            wrapper=new_wrapper,
            records_arr=new_records_arr,
            ts=new_ts
        )

    @classmethod
    def from_ts(cls: tp.Type[DrawdownsT],
                ts: tp.ArrayLike,
                attach_ts: bool = True,
                wrapper_kwargs: tp.KwargsLike = None,
                **kwargs) -> DrawdownsT:
        """Build `Drawdowns` from time series `ts`.

        `**kwargs` will be passed to `Drawdowns.__init__`."""
        ts_pd = to_pd_array(ts)
        records_arr = nb.get_drawdowns_nb(to_2d_array(ts_pd))
        wrapper = ArrayWrapper.from_obj(ts_pd, **merge_dicts({}, wrapper_kwargs))
        return cls(wrapper, records_arr, ts=ts_pd if attach_ts else None, **kwargs)

    @property
    def ts(self) -> tp.Optional[tp.SeriesFrame]:
        """Original time series that records are built from (optional)."""
        return self._ts

    # ############# Drawdown ############# #

    @cached_property
    def drawdown(self) -> MappedArray:
        """See `vectorbt.generic.nb.dd_drawdown_nb`.

        Takes into account both recovered and active drawdowns."""
        drawdown = nb.dd_drawdown_nb(
            self.get_field_arr('peak_val'),
            self.get_field_arr('valley_val')
        )
        return self.map_array(drawdown)

    @cached_method
    def avg_drawdown(self, group_by: tp.GroupByLike = None,
                     wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Average drawdown (ADD).

        Based on `Drawdowns.drawdown`."""
        wrap_kwargs = merge_dicts(dict(name_or_index='avg_drawdown'), wrap_kwargs)
        return self.drawdown.mean(group_by=group_by, wrap_kwargs=wrap_kwargs, **kwargs)

    @cached_method
    def max_drawdown(self, group_by: tp.GroupByLike = None,
                     wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Maximum drawdown (MDD).

        Based on `Drawdowns.drawdown`."""
        wrap_kwargs = merge_dicts(dict(name_or_index='max_drawdown'), wrap_kwargs)
        return self.drawdown.min(group_by=group_by, wrap_kwargs=wrap_kwargs, **kwargs)

    # ############# Recovery ############# #

    @cached_property
    def recovery_return(self) -> MappedArray:
        """See `vectorbt.generic.nb.dd_recovery_return_nb`.

        Takes into account both recovered and active drawdowns."""
        recovery_return = nb.dd_recovery_return_nb(
            self.get_field_arr('valley_val'),
            self.get_field_arr('end_val')
        )
        return self.map_array(recovery_return)

    @cached_method
    def avg_recovery_return(self, group_by: tp.GroupByLike = None,
                            wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Average recovery return.

        Based on `Drawdowns.recovery_return`."""
        wrap_kwargs = merge_dicts(dict(name_or_index='avg_recovery_return'), wrap_kwargs)
        return self.recovery_return.mean(group_by=group_by, wrap_kwargs=wrap_kwargs, **kwargs)

    @cached_method
    def max_recovery_return(self, group_by: tp.GroupByLike = None,
                            wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Maximum recovery return.

        Based on `Drawdowns.recovery_return`."""
        wrap_kwargs = merge_dicts(dict(name_or_index='max_recovery_return'), wrap_kwargs)
        return self.recovery_return.max(group_by=group_by, wrap_kwargs=wrap_kwargs, **kwargs)

    # ############# Duration ############# #

    @cached_property
    def decline_duration(self) -> MappedArray:
        """See `vectorbt.generic.nb.dd_decline_duration_nb`.

        Takes into account both recovered and active drawdowns."""
        decline_duration = nb.dd_decline_duration_nb(
            self.get_field_arr('start_idx'),
            self.get_field_arr('valley_idx')
        )
        return self.map_array(decline_duration)

    @cached_property
    def recovery_duration(self) -> MappedArray:
        """See `vectorbt.generic.nb.dd_recovery_duration_nb`.

        A value higher than 1 means the recovery was slower than the decline.

        Takes into account both recovered and active drawdowns."""
        recovery_duration = nb.dd_recovery_duration_nb(
            self.get_field_arr('valley_idx'),
            self.get_field_arr('end_idx')
        )
        return self.map_array(recovery_duration)

    @cached_property
    def recovery_duration_ratio(self) -> MappedArray:
        """See `vectorbt.generic.nb.dd_recovery_duration_ratio_nb`.

        Takes into account both recovered and active drawdowns."""
        recovery_duration_ratio = nb.dd_recovery_duration_ratio_nb(
            self.get_field_arr('start_idx'),
            self.get_field_arr('valley_idx'),
            self.get_field_arr('end_idx')
        )
        return self.map_array(recovery_duration_ratio)

    # ############# Status: Active ############# #

    @cached_method
    def active_drawdown(self, group_by: tp.GroupByLike = None,
                        wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Drawdown of the last active drawdown only.

        Does not support grouping."""
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            raise ValueError("Grouping is not supported by this method")
        wrap_kwargs = merge_dicts(dict(name_or_index='active_drawdown'), wrap_kwargs)
        active = self.active
        curr_end_val = active.end_val.nth(-1, group_by=group_by)
        curr_peak_val = active.peak_val.nth(-1, group_by=group_by)
        curr_drawdown = (curr_end_val - curr_peak_val) / curr_peak_val
        return self.wrapper.wrap_reduced(curr_drawdown, group_by=group_by, **wrap_kwargs)

    @cached_method
    def active_duration(self, group_by: tp.GroupByLike = None,
                        wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Duration of the last active drawdown only.

        Does not support grouping."""
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            raise ValueError("Grouping is not supported by this method")
        wrap_kwargs = merge_dicts(dict(to_timedelta=True, name_or_index='active_duration'), wrap_kwargs)
        return self.active.duration.nth(-1, group_by=group_by, wrap_kwargs=wrap_kwargs, **kwargs)

    @cached_method
    def active_recovery(self, group_by: tp.GroupByLike = None,
                        wrap_kwargs: tp.KwargsLike = None) -> tp.MaybeSeries:
        """Recovery of the last active drawdown only.

        Does not support grouping."""
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            raise ValueError("Grouping is not supported by this method")
        wrap_kwargs = merge_dicts(dict(name_or_index='active_recovery'), wrap_kwargs)
        active = self.active
        curr_peak_val = active.peak_val.nth(-1, group_by=group_by)
        curr_end_val = active.end_val.nth(-1, group_by=group_by)
        curr_valley_val = active.valley_val.nth(-1, group_by=group_by)
        curr_recovery = (curr_end_val - curr_valley_val) / (curr_peak_val - curr_valley_val)
        return self.wrapper.wrap_reduced(curr_recovery, group_by=group_by, **wrap_kwargs)

    @cached_method
    def active_recovery_return(self, group_by: tp.GroupByLike = None,
                               wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Recovery return of the last active drawdown only.

        Does not support grouping."""
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            raise ValueError("Grouping is not supported by this method")
        wrap_kwargs = merge_dicts(dict(name_or_index='active_recovery_return'), wrap_kwargs)
        return self.active.recovery_return.nth(-1, group_by=group_by, wrap_kwargs=wrap_kwargs, **kwargs)

    @cached_method
    def active_recovery_duration(self, group_by: tp.GroupByLike = None,
                                 wrap_kwargs: tp.KwargsLike = None, **kwargs) -> tp.MaybeSeries:
        """Recovery duration of the last active drawdown only.

        Does not support grouping."""
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            raise ValueError("Grouping is not supported by this method")
        wrap_kwargs = merge_dicts(dict(to_timedelta=True, name_or_index='active_recovery_duration'), wrap_kwargs)
        return self.active.recovery_duration.nth(-1, group_by=group_by, wrap_kwargs=wrap_kwargs, **kwargs)

    # ############# Stats ############# #

    @property
    def stats_defaults(self) -> tp.Kwargs:
        """Defaults for `Drawdowns.stats`.

        Merges `vectorbt.generic.ranges.Ranges.stats_defaults` and
        `drawdowns.stats` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        drawdowns_stats_cfg = settings['drawdowns']['stats']

        return merge_dicts(
            Ranges.stats_defaults.__get__(self),
            drawdowns_stats_cfg
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
            coverage=dict(
                title='Coverage [%]',
                calc_func='coverage',
                post_calc_func=lambda self, out, settings: out * 100,
                tags=['ranges', 'duration']
            ),
            total_records=dict(
                title='Total Records',
                calc_func='count',
                tags='records'
            ),
            total_recovered=dict(
                title='Total Recovered Drawdowns',
                calc_func='recovered.count',
                tags='drawdowns'
            ),
            total_active=dict(
                title='Total Active Drawdowns',
                calc_func='active.count',
                tags='drawdowns'
            ),
            active_dd=dict(
                title='Active Drawdown [%]',
                calc_func='active_drawdown',
                post_calc_func=lambda self, out, settings: -out * 100,
                check_is_not_grouped=True,
                tags=['drawdowns', 'active']
            ),
            active_duration=dict(
                title='Active Duration',
                calc_func='active_duration',
                fill_wrap_kwargs=True,
                check_is_not_grouped=True,
                tags=['drawdowns', 'active', 'duration']
            ),
            active_recovery=dict(
                title='Active Recovery [%]',
                calc_func='active_recovery',
                post_calc_func=lambda self, out, settings: out * 100,
                check_is_not_grouped=True,
                tags=['drawdowns', 'active']
            ),
            active_recovery_return=dict(
                title='Active Recovery Return [%]',
                calc_func='active_recovery_return',
                post_calc_func=lambda self, out, settings: out * 100,
                check_is_not_grouped=True,
                tags=['drawdowns', 'active']
            ),
            active_recovery_duration=dict(
                title='Active Recovery Duration',
                calc_func='active_recovery_duration',
                fill_wrap_kwargs=True,
                check_is_not_grouped=True,
                tags=['drawdowns', 'active', 'duration']
            ),
            max_dd=dict(
                title='Max Drawdown [%]',
                calc_func=RepEval("'max_drawdown' if incl_active else 'recovered.max_drawdown'"),
                post_calc_func=lambda self, out, settings: -out * 100,
                tags=RepEval("['drawdowns'] if incl_active else ['drawdowns', 'recovered']")
            ),
            avg_dd=dict(
                title='Avg Drawdown [%]',
                calc_func=RepEval("'avg_drawdown' if incl_active else 'recovered.avg_drawdown'"),
                post_calc_func=lambda self, out, settings: -out * 100,
                tags=RepEval("['drawdowns'] if incl_active else ['drawdowns', 'recovered']")
            ),
            max_dd_duration=dict(
                title='Max Drawdown Duration',
                calc_func=RepEval("'max_duration' if incl_active else 'recovered.max_duration'"),
                fill_wrap_kwargs=True,
                tags=RepEval("['drawdowns', 'duration'] if incl_active else ['drawdowns', 'recovered', 'duration']")
            ),
            avg_dd_duration=dict(
                title='Avg Drawdown Duration',
                calc_func=RepEval("'avg_duration' if incl_active else 'recovered.avg_duration'"),
                fill_wrap_kwargs=True,
                tags=RepEval("['drawdowns', 'duration'] if incl_active else ['drawdowns', 'recovered', 'duration']")
            ),
            max_return=dict(
                title='Max Recovery Return [%]',
                calc_func='recovered.recovery_return.max',
                post_calc_func=lambda self, out, settings: out * 100,
                tags=['drawdowns', 'recovered']
            ),
            avg_return=dict(
                title='Avg Recovery Return [%]',
                calc_func='recovered.recovery_return.mean',
                post_calc_func=lambda self, out, settings: out * 100,
                tags=['drawdowns', 'recovered']
            ),
            max_recovery_duration=dict(
                title='Max Recovery Duration',
                calc_func='recovered.recovery_duration.max',
                apply_to_timedelta=True,
                tags=['drawdowns', 'recovered', 'duration']
            ),
            avg_recovery_duration=dict(
                title='Avg Recovery Duration',
                calc_func='recovered.recovery_duration.mean',
                apply_to_timedelta=True,
                tags=['drawdowns', 'recovered', 'duration']
            ),
            recovery_duration_ratio=dict(
                title='Avg Recovery Duration Ratio',
                calc_func='recovered.recovery_duration_ratio.mean',
                tags=['drawdowns', 'recovered']
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def metrics(self) -> Config:
        return self._metrics

    # ############# Plotting ############# #

    def plot(self,
             column: tp.Optional[tp.Label] = None,
             top_n: int = 5,
             plot_zones: bool = True,
             ts_trace_kwargs: tp.KwargsLike = None,
             peak_trace_kwargs: tp.KwargsLike = None,
             valley_trace_kwargs: tp.KwargsLike = None,
             recovery_trace_kwargs: tp.KwargsLike = None,
             active_trace_kwargs: tp.KwargsLike = None,
             decline_shape_kwargs: tp.KwargsLike = None,
             recovery_shape_kwargs: tp.KwargsLike = None,
             active_shape_kwargs: tp.KwargsLike = None,
             add_trace_kwargs: tp.KwargsLike = None,
             xref: str = 'x',
             yref: str = 'y',
             fig: tp.Optional[tp.BaseFigure] = None,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot drawdowns.

        Args:
            column (str): Name of the column to plot.
            top_n (int): Filter top N drawdown records by maximum drawdown.
            plot_zones (bool): Whether to plot zones.
            ts_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `Drawdowns.ts`.
            peak_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for peak values.
            valley_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for valley values.
            recovery_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for recovery values.
            active_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for active recovery values.
            decline_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for decline zones.
            recovery_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for recovery zones.
            active_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for active recovery zones.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> import vectorbt as vbt
            >>> from datetime import datetime, timedelta
            >>> import pandas as pd

            >>> price = pd.Series([1, 2, 1, 2, 3, 2, 1, 2], name='Price')
            >>> price.index = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(len(price))]
            >>> vbt.Drawdowns.from_ts(price, wrapper_kwargs=dict(freq='1 day')).plot()
            ```

            ![](/assets/images/drawdowns_plot.svg)
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        self_col = self.select_one(column=column, group_by=False)
        if top_n is not None:
            # Drawdowns is negative, thus top_n becomes bottom_n
            self_col = self_col.apply_mask(self_col.drawdown.bottom_n_mask(top_n))

        if ts_trace_kwargs is None:
            ts_trace_kwargs = {}
        ts_trace_kwargs = merge_dicts(dict(
            line=dict(
                color=plotting_cfg['color_schema']['blue']
            )
        ), ts_trace_kwargs)
        if peak_trace_kwargs is None:
            peak_trace_kwargs = {}
        if valley_trace_kwargs is None:
            valley_trace_kwargs = {}
        if recovery_trace_kwargs is None:
            recovery_trace_kwargs = {}
        if active_trace_kwargs is None:
            active_trace_kwargs = {}
        if decline_shape_kwargs is None:
            decline_shape_kwargs = {}
        if recovery_shape_kwargs is None:
            recovery_shape_kwargs = {}
        if active_shape_kwargs is None:
            active_shape_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}

        if fig is None:
            fig = make_figure()
        fig.update_layout(**layout_kwargs)
        y_domain = get_domain(yref, fig)

        if self_col.ts is not None:
            fig = self_col.ts.vbt.plot(trace_kwargs=ts_trace_kwargs, add_trace_kwargs=add_trace_kwargs, fig=fig)

        if self_col.count() > 0:
            # Extract information
            id_ = self_col.get_field_arr('id')
            id_title = self_col.get_field_title('id')

            peak_idx = self_col.get_map_field_to_index('peak_idx')
            peak_idx_title = self_col.get_field_title('peak_idx')

            if self_col.ts is not None:
                peak_val = self_col.ts.loc[peak_idx]
            else:
                peak_val = self_col.get_field_arr('peak_val')
            peak_val_title = self_col.get_field_title('peak_val')

            valley_idx = self_col.get_map_field_to_index('valley_idx')
            valley_idx_title = self_col.get_field_title('valley_idx')

            if self_col.ts is not None:
                valley_val = self_col.ts.loc[valley_idx]
            else:
                valley_val = self_col.get_field_arr('valley_val')
            valley_val_title = self_col.get_field_title('valley_val')

            end_idx = self_col.get_map_field_to_index('end_idx')
            end_idx_title = self_col.get_field_title('end_idx')

            if self_col.ts is not None:
                end_val = self_col.ts.loc[end_idx]
            else:
                end_val = self_col.get_field_arr('end_val')
            end_val_title = self_col.get_field_title('end_val')

            drawdown = self_col.drawdown.values
            recovery_return = self_col.recovery_return.values
            decline_duration = np.vectorize(str)(self_col.wrapper.to_timedelta(
                self_col.decline_duration.values, to_pd=True, silence_warnings=True))
            recovery_duration = np.vectorize(str)(self_col.wrapper.to_timedelta(
                self_col.recovery_duration.values, to_pd=True, silence_warnings=True))
            duration = np.vectorize(str)(self_col.wrapper.to_timedelta(
                self_col.duration.values, to_pd=True, silence_warnings=True))

            status = self_col.get_field_arr('status')

            peak_mask = peak_idx != np.roll(end_idx, 1)  # peak and recovery at same time -> recovery wins
            if peak_mask.any():
                # Plot peak markers
                peak_customdata = id_[peak_mask][:, None]
                peak_scatter = go.Scatter(
                    x=peak_idx[peak_mask],
                    y=peak_val[peak_mask],
                    mode='markers',
                    marker=dict(
                        symbol='diamond',
                        color=plotting_cfg['contrast_color_schema']['blue'],
                        size=7,
                        line=dict(
                            width=1,
                            color=adjust_lightness(plotting_cfg['contrast_color_schema']['blue'])
                        )
                    ),
                    name='Peak',
                    customdata=peak_customdata,
                    hovertemplate=f"{id_title}: %{{customdata[0]}}"
                                  f"<br>{peak_idx_title}: %{{x}}"
                                  f"<br>{peak_val_title}: %{{y}}"
                )
                peak_scatter.update(**peak_trace_kwargs)
                fig.add_trace(peak_scatter, **add_trace_kwargs)

            recovered_mask = status == DrawdownStatus.Recovered
            if recovered_mask.any():
                # Plot valley markers
                valley_customdata = np.stack((
                    id_[recovered_mask],
                    drawdown[recovered_mask],
                    decline_duration[recovered_mask]
                ), axis=1)
                valley_scatter = go.Scatter(
                    x=valley_idx[recovered_mask],
                    y=valley_val[recovered_mask],
                    mode='markers',
                    marker=dict(
                        symbol='diamond',
                        color=plotting_cfg['contrast_color_schema']['red'],
                        size=7,
                        line=dict(
                            width=1,
                            color=adjust_lightness(plotting_cfg['contrast_color_schema']['red'])
                        )
                    ),
                    name='Valley',
                    customdata=valley_customdata,
                    hovertemplate=f"{id_title}: %{{customdata[0]}}"
                                  f"<br>{valley_idx_title}: %{{x}}"
                                  f"<br>{valley_val_title}: %{{y}}"
                                  f"<br>Drawdown: %{{customdata[1]:.2%}}"
                                  f"<br>Duration: %{{customdata[2]}}"
                )
                valley_scatter.update(**valley_trace_kwargs)
                fig.add_trace(valley_scatter, **add_trace_kwargs)

                if plot_zones:
                    # Plot drawdown zones
                    for i in range(len(id_[recovered_mask])):
                        fig.add_shape(**merge_dicts(dict(
                            type="rect",
                            xref=xref,
                            yref="paper",
                            x0=peak_idx[recovered_mask][i],
                            y0=y_domain[0],
                            x1=valley_idx[recovered_mask][i],
                            y1=y_domain[1],
                            fillcolor='red',
                            opacity=0.2,
                            layer="below",
                            line_width=0,
                        ), decline_shape_kwargs))

                # Plot recovery markers
                recovery_customdata = np.stack((
                    id_[recovered_mask],
                    recovery_return[recovered_mask],
                    recovery_duration[recovered_mask]
                ), axis=1)
                recovery_scatter = go.Scatter(
                    x=end_idx[recovered_mask],
                    y=end_val[recovered_mask],
                    mode='markers',
                    marker=dict(
                        symbol='diamond',
                        color=plotting_cfg['contrast_color_schema']['green'],
                        size=7,
                        line=dict(
                            width=1,
                            color=adjust_lightness(plotting_cfg['contrast_color_schema']['green'])
                        )
                    ),
                    name='Recovery/Peak',
                    customdata=recovery_customdata,
                    hovertemplate=f"{id_title}: %{{customdata[0]}}"
                                  f"<br>{end_idx_title}: %{{x}}"
                                  f"<br>{end_val_title}: %{{y}}"
                                  f"<br>Return: %{{customdata[1]:.2%}}"
                                  f"<br>Duration: %{{customdata[2]}}"
                )
                recovery_scatter.update(**recovery_trace_kwargs)
                fig.add_trace(recovery_scatter, **add_trace_kwargs)

                if plot_zones:
                    # Plot recovery zones
                    for i in range(len(id_[recovered_mask])):
                        fig.add_shape(**merge_dicts(dict(
                            type="rect",
                            xref=xref,
                            yref="paper",
                            x0=valley_idx[recovered_mask][i],
                            y0=y_domain[0],
                            x1=end_idx[recovered_mask][i],
                            y1=y_domain[1],
                            fillcolor='green',
                            opacity=0.2,
                            layer="below",
                            line_width=0,
                        ), recovery_shape_kwargs))

            # Plot active markers
            active_mask = status == DrawdownStatus.Active
            if active_mask.any():
                active_customdata = np.stack((
                    id_[active_mask],
                    drawdown[active_mask],
                    duration[active_mask]
                ), axis=1)
                active_scatter = go.Scatter(
                    x=end_idx[active_mask],
                    y=end_val[active_mask],
                    mode='markers',
                    marker=dict(
                        symbol='diamond',
                        color=plotting_cfg['contrast_color_schema']['orange'],
                        size=7,
                        line=dict(
                            width=1,
                            color=adjust_lightness(plotting_cfg['contrast_color_schema']['orange'])
                        )
                    ),
                    name='Active',
                    customdata=active_customdata,
                    hovertemplate=f"{id_title}: %{{customdata[0]}}"
                                  f"<br>{end_idx_title}: %{{x}}"
                                  f"<br>{end_val_title}: %{{y}}"
                                  f"<br>Return: %{{customdata[1]:.2%}}"
                                  f"<br>Duration: %{{customdata[2]}}"
                )
                active_scatter.update(**active_trace_kwargs)
                fig.add_trace(active_scatter, **add_trace_kwargs)

                if plot_zones:
                    # Plot active drawdown zones
                    for i in range(len(id_[active_mask])):
                        fig.add_shape(**merge_dicts(dict(
                            type="rect",
                            xref=xref,
                            yref="paper",
                            x0=peak_idx[active_mask][i],
                            y0=y_domain[0],
                            x1=end_idx[active_mask][i],
                            y1=y_domain[1],
                            fillcolor='orange',
                            opacity=0.2,
                            layer="below",
                            line_width=0,
                        ), active_shape_kwargs))

        return fig

    @property
    def plots_defaults(self) -> tp.Kwargs:
        """Defaults for `Drawdowns.plots`.

        Merges `vectorbt.generic.ranges.Ranges.plots_defaults` and
        `drawdowns.plots` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        drawdowns_plots_cfg = settings['drawdowns']['plots']

        return merge_dicts(
            Ranges.plots_defaults.__get__(self),
            drawdowns_plots_cfg
        )

    _subplots: tp.ClassVar[Config] = Config(
        dict(
            plot=dict(
                title="Drawdowns",
                check_is_not_grouped=True,
                plot_func='plot',
                tags='drawdowns'
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def subplots(self) -> Config:
        return self._subplots


Drawdowns.override_field_config_doc(__pdoc__)
Drawdowns.override_metrics_doc(__pdoc__)
Drawdowns.override_subplots_doc(__pdoc__)
