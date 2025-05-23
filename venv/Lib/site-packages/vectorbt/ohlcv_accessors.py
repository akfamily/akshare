# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Custom pandas accessors for OHLC(V) data.

Methods can be accessed as follows:

* `OHLCVDFAccessor` -> `pd.DataFrame.vbt.ohlc.*`
* `OHLCVDFAccessor` -> `pd.DataFrame.vbt.ohlcv.*`

The accessors inherit `vectorbt.generic.accessors`.

!!! note
    Accessors do not utilize caching.

## Column names

By default, vectorbt searches for columns with names 'open', 'high', 'low', 'close', and 'volume'
(case doesn't matter). You can change the naming either using `ohlcv.column_names` in
`vectorbt._settings.settings`, or by providing `column_names` directly to the accessor.

```pycon
>>> import pandas as pd
>>> import vectorbt as vbt

>>> df = pd.DataFrame({
...     'my_open1': [2, 3, 4, 3.5, 2.5],
...     'my_high2': [3, 4, 4.5, 4, 3],
...     'my_low3': [1.5, 2.5, 3.5, 2.5, 1.5],
...     'my_close4': [2.5, 3.5, 4, 3, 2],
...     'my_volume5': [10, 11, 10, 9, 10]
... })

>>> # vectorbt can't find columns
>>> df.vbt.ohlcv.get_column('open')
None

>>> my_column_names = dict(
...     open='my_open1',
...     high='my_high2',
...     low='my_low3',
...     close='my_close4',
...     volume='my_volume5',
... )
>>> ohlcv_acc = df.vbt.ohlcv(freq='d', column_names=my_column_names)
>>> ohlcv_acc.get_column('open')
0    2.0
1    3.0
2    4.0
3    3.5
4    2.5
Name: my_open1, dtype: float64
```

## Stats

!!! hint
    See `vectorbt.generic.stats_builder.StatsBuilderMixin.stats` and `OHLCVDFAccessor.metrics`.

```pycon
>>> ohlcv_acc.stats()
Start                           0
End                             4
Period            5 days 00:00:00
First Price                   2.0
Lowest Price                  1.5
Highest Price                 4.5
Last Price                    2.0
First Volume                   10
Lowest Volume                   9
Highest Volume                 11
Last Volume                    10
Name: agg_func_mean, dtype: object
```

## Plots

!!! hint
    See `vectorbt.generic.plots_builder.PlotsBuilderMixin.plots` and `OHLCVDFAccessor.subplots`.

`OHLCVDFAccessor` class has a single subplot based on `OHLCVDFAccessor.plot` (without volume):

```pycon
>>> ohlcv_acc.plots(settings=dict(plot_type='candlestick'))
```

![](/assets/images/ohlcv_plots.svg)
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from vectorbt import _typing as tp
from vectorbt.generic import nb
from vectorbt.generic.accessors import GenericAccessor, GenericDFAccessor
from vectorbt.root_accessors import register_dataframe_vbt_accessor
from vectorbt.utils.config import merge_dicts, Config
from vectorbt.utils.figure import make_figure, make_subplots

__pdoc__ = {}


@register_dataframe_vbt_accessor('ohlc')
@register_dataframe_vbt_accessor('ohlcv')
class OHLCVDFAccessor(GenericDFAccessor):  # pragma: no cover
    """Accessor on top of OHLCV data. For DataFrames only.

    Accessible through `pd.DataFrame.vbt.ohlcv`."""

    def __init__(self, obj: tp.Frame, column_names: tp.KwargsLike = None, **kwargs) -> None:
        self._column_names = column_names

        GenericDFAccessor.__init__(self, obj, column_names=column_names, **kwargs)

    @property
    def column_names(self) -> tp.Kwargs:
        """Column names."""
        from vectorbt._settings import settings
        ohlcv_cfg = settings['ohlcv']

        return merge_dicts(ohlcv_cfg['column_names'], self._column_names)

    def get_column(self, col_name: str) -> tp.Optional[tp.Series]:
        """Get column from `OHLCVDFAccessor.column_names`."""
        df_column_names = self.obj.columns.str.lower().tolist()
        col_name = self.column_names[col_name].lower()
        if col_name not in df_column_names:
            return None
        return self.obj.iloc[:, df_column_names.index(col_name)]

    @property
    def open(self) -> tp.Optional[tp.Series]:
        """Open series."""
        return self.get_column('open')

    @property
    def high(self) -> tp.Optional[tp.Series]:
        """High series."""
        return self.get_column('high')

    @property
    def low(self) -> tp.Optional[tp.Series]:
        """Low series."""
        return self.get_column('low')

    @property
    def close(self) -> tp.Optional[tp.Series]:
        """Close series."""
        return self.get_column('close')

    @property
    def ohlc(self) -> tp.Optional[tp.Frame]:
        """Open, high, low, and close series."""
        to_concat = []
        if self.open is not None:
            to_concat.append(self.open)
        if self.high is not None:
            to_concat.append(self.high)
        if self.low is not None:
            to_concat.append(self.low)
        if self.close is not None:
            to_concat.append(self.close)
        if len(to_concat) == 0:
            return None
        return pd.concat(to_concat, axis=1)

    @property
    def volume(self) -> tp.Optional[tp.Series]:
        """Volume series."""
        return self.get_column('volume')

    # ############# Stats ############# #

    @property
    def stats_defaults(self) -> tp.Kwargs:
        """Defaults for `OHLCVDFAccessor.stats`.

        Merges `vectorbt.generic.accessors.GenericAccessor.stats_defaults` and
        `ohlcv.stats` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        ohlcv_stats_cfg = settings['ohlcv']['stats']

        return merge_dicts(
            GenericAccessor.stats_defaults.__get__(self),
            ohlcv_stats_cfg
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
            first_price=dict(
                title='First Price',
                calc_func=lambda ohlc: nb.bfill_1d_nb(ohlc.values.flatten())[0],
                resolve_ohlc=True,
                tags=['ohlcv', 'ohlc']
            ),
            lowest_price=dict(
                title='Lowest Price',
                calc_func=lambda ohlc: ohlc.values.min(),
                resolve_ohlc=True,
                tags=['ohlcv', 'ohlc']
            ),
            highest_price=dict(
                title='Highest Price',
                calc_func=lambda ohlc: ohlc.values.max(),
                resolve_ohlc=True,
                tags=['ohlcv', 'ohlc']
            ),
            last_price=dict(
                title='Last Price',
                calc_func=lambda ohlc: nb.ffill_1d_nb(ohlc.values.flatten())[-1],
                resolve_ohlc=True,
                tags=['ohlcv', 'ohlc']
            ),
            first_volume=dict(
                title='First Volume',
                calc_func=lambda volume: nb.bfill_1d_nb(volume.values)[0],
                resolve_volume=True,
                tags=['ohlcv', 'volume']
            ),
            lowest_volume=dict(
                title='Lowest Volume',
                calc_func=lambda volume: volume.values.min(),
                resolve_volume=True,
                tags=['ohlcv', 'volume']
            ),
            highest_volume=dict(
                title='Highest Volume',
                calc_func=lambda volume: volume.values.max(),
                resolve_volume=True,
                tags=['ohlcv', 'volume']
            ),
            last_volume=dict(
                title='Last Volume',
                calc_func=lambda volume: nb.ffill_1d_nb(volume.values)[-1],
                resolve_volume=True,
                tags=['ohlcv', 'volume']
            ),
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def metrics(self) -> Config:
        return self._metrics

    # ############# Plotting ############# #

    def plot(self,
             plot_type: tp.Union[None, str, tp.BaseTraceType] = None,
             show_volume: tp.Optional[bool] = None,
             ohlc_kwargs: tp.KwargsLike = None,
             volume_kwargs: tp.KwargsLike = None,
             ohlc_add_trace_kwargs: tp.KwargsLike = None,
             volume_add_trace_kwargs: tp.KwargsLike = None,
             fig: tp.Optional[tp.BaseFigure] = None,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot OHLCV data.

        Args:
            plot_type: Either 'OHLC', 'Candlestick' or Plotly trace.

                Pass None to use the default.
            show_volume (bool): If True, shows volume as bar chart.
            ohlc_kwargs (dict): Keyword arguments passed to `plot_type`.
            volume_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Bar`.
            ohlc_add_trace_kwargs (dict): Keyword arguments passed to `add_trace` for OHLC.
            volume_add_trace_kwargs (dict): Keyword arguments passed to `add_trace` for volume.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> import vectorbt as vbt

            >>> vbt.YFData.download("BTC-USD").get().vbt.ohlcv.plot()
            ```

            ![](/assets/images/ohlcv_plot.svg)
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']
        ohlcv_cfg = settings['ohlcv']

        if ohlc_kwargs is None:
            ohlc_kwargs = {}
        if volume_kwargs is None:
            volume_kwargs = {}
        if ohlc_add_trace_kwargs is None:
            ohlc_add_trace_kwargs = {}
        if volume_add_trace_kwargs is None:
            volume_add_trace_kwargs = {}
        if show_volume is None:
            show_volume = self.volume is not None
        if show_volume:
            ohlc_add_trace_kwargs = merge_dicts(dict(row=1, col=1), ohlc_add_trace_kwargs)
            volume_add_trace_kwargs = merge_dicts(dict(row=2, col=1), volume_add_trace_kwargs)

        # Set up figure
        if fig is None:
            if show_volume:
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0, row_heights=[0.7, 0.3])
            else:
                fig = make_figure()
            fig.update_layout(
                showlegend=True,
                xaxis=dict(
                    rangeslider_visible=False,
                    showgrid=True
                ),
                yaxis=dict(
                    showgrid=True
                )
            )
            if show_volume:
                fig.update_layout(
                    xaxis2=dict(
                        showgrid=True
                    ),
                    yaxis2=dict(
                        showgrid=True
                    ),
                    bargap=0
                )
        fig.update_layout(**layout_kwargs)
        if plot_type is None:
            plot_type = ohlcv_cfg['plot_type']
        if isinstance(plot_type, str):
            if plot_type.lower() == 'ohlc':
                plot_type = 'OHLC'
                plot_obj = go.Ohlc
            elif plot_type.lower() == 'candlestick':
                plot_type = 'Candlestick'
                plot_obj = go.Candlestick
            else:
                raise ValueError("Plot type can be either 'OHLC' or 'Candlestick'")
        else:
            plot_obj = plot_type
        ohlc = plot_obj(
            x=self.wrapper.index,
            open=self.open,
            high=self.high,
            low=self.low,
            close=self.close,
            name=plot_type,
            increasing=dict(
                line=dict(
                    color=plotting_cfg['color_schema']['increasing']
                )
            ),
            decreasing=dict(
                line=dict(
                    color=plotting_cfg['color_schema']['decreasing']
                )
            )
        )
        ohlc.update(**ohlc_kwargs)
        fig.add_trace(ohlc, **ohlc_add_trace_kwargs)

        if show_volume:
            marker_colors = np.empty(self.volume.shape, dtype=object)
            marker_colors[(self.close.values - self.open.values) > 0] = plotting_cfg['color_schema']['increasing']
            marker_colors[(self.close.values - self.open.values) == 0] = plotting_cfg['color_schema']['gray']
            marker_colors[(self.close.values - self.open.values) < 0] = plotting_cfg['color_schema']['decreasing']
            volume_bar = go.Bar(
                x=self.wrapper.index,
                y=self.volume,
                marker=dict(
                    color=marker_colors,
                    line_width=0
                ),
                opacity=0.5,
                name='Volume'
            )
            volume_bar.update(**volume_kwargs)
            fig.add_trace(volume_bar, **volume_add_trace_kwargs)

        return fig

    @property
    def plots_defaults(self) -> tp.Kwargs:
        """Defaults for `OHLCVDFAccessor.plots`.

        Merges `vectorbt.generic.accessors.GenericAccessor.plots_defaults` and
        `ohlcv.plots` from `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        ohlcv_plots_cfg = settings['ohlcv']['plots']

        return merge_dicts(
            GenericAccessor.plots_defaults.__get__(self),
            ohlcv_plots_cfg
        )

    _subplots: tp.ClassVar[Config] = Config(
        dict(
            plot=dict(
                title='OHLC',
                xaxis_kwargs=dict(
                    showgrid=True,
                    rangeslider_visible=False
                ),
                yaxis_kwargs=dict(
                    showgrid=True
                ),
                check_is_not_grouped=True,
                plot_func='plot',
                show_volume=False,
                tags='ohlcv'
            )
        ),
        copy_kwargs=dict(copy_mode='deep')
    )

    @property
    def subplots(self) -> Config:
        return self._subplots


OHLCVDFAccessor.override_metrics_doc(__pdoc__)
OHLCVDFAccessor.override_subplots_doc(__pdoc__)
