# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Indicators built with `vectorbt.indicators.factory.IndicatorFactory`.

You can access all the indicators either by `vbt.*` or `vbt.indicators.*`.

```pycon
>>> import pandas as pd
>>> import vectorbt as vbt

>>> # vectorbt.indicators.basic.MA
>>> vbt.MA.run(pd.Series([1, 2, 3]), [2, 3]).ma
ma_window     2     3
ma_ewm    False False
0           NaN   NaN
1           1.5   NaN
2           2.5   2.0
```

The advantage of these indicators over TA-Lib's is that they work primarily on 2-dimensional arrays
and utilize caching, which makes them faster for matrices with huge number of columns. They also
have plotting methods.

Run for the examples below:

```pycon
>>> import vectorbt as vbt
>>> from datetime import datetime

>>> start = '2019-03-01 UTC'  # crypto is in UTC
>>> end = '2019-09-01 UTC'
>>> cols = ['Open', 'High', 'Low', 'Close', 'Volume']
>>> ohlcv = vbt.YFData.download("BTC-USD", start=start, end=end).get(cols)
>>> ohlcv
                                   Open          High          Low  \\
Date
2019-03-01 00:00:00+00:00   3853.757080   3907.795410  3851.692383
2019-03-02 00:00:00+00:00   3855.318115   3874.607422  3832.127930
2019-03-03 00:00:00+00:00   3862.266113   3875.483643  3836.905762
...                                 ...           ...          ...
2019-08-30 00:00:00+00:00   9514.844727   9656.124023  9428.302734
2019-08-31 00:00:00+00:00   9597.539062   9673.220703  9531.799805
2019-09-01 00:00:00+00:00   9630.592773   9796.755859  9582.944336

                                 Close       Volume
Date
2019-03-01 00:00:00+00:00  3859.583740   7661247975
2019-03-02 00:00:00+00:00  3864.415039   7578786076
2019-03-03 00:00:00+00:00  3847.175781   7253558152
...                                ...          ...
2019-08-30 00:00:00+00:00  9598.173828  13595263986
2019-08-31 00:00:00+00:00  9630.664062  11454806419
2019-09-01 00:00:00+00:00  9757.970703  11445355859

[185 rows x 5 columns]

>>> ohlcv.vbt.ohlcv.plot()
```
![](/assets/images/basic_price.svg)"""

import numpy as np
import plotly.graph_objects as go

from vectorbt import _typing as tp
from vectorbt.generic import nb as generic_nb
from vectorbt.indicators import nb
from vectorbt.indicators.factory import IndicatorFactory
from vectorbt.utils.colors import adjust_opacity
from vectorbt.utils.config import merge_dicts
from vectorbt.utils.figure import make_figure

# ############# MA ############# #


MA = IndicatorFactory(
    class_name='MA',
    module_name=__name__,
    short_name='ma',
    input_names=['close'],
    param_names=['window', 'ewm'],
    output_names=['ma']
).from_apply_func(
    nb.ma_apply_nb,
    cache_func=nb.ma_cache_nb,
    kwargs_to_args=['adjust'],
    ewm=False,
    adjust=False
)


class _MA(MA):
    """Moving Average (MA).

    A moving average is a widely used indicator in technical analysis that helps smooth out
    price action by filtering out the “noise” from random short-term price fluctuations. 

    See [Moving Average (MA)](https://www.investopedia.com/terms/m/movingaverage.asp)."""

    def plot(self,
             column: tp.Optional[tp.Label] = None,
             plot_close: bool = True,
             close_trace_kwargs: tp.KwargsLike = None,
             ma_trace_kwargs: tp.KwargsLike = None,
             add_trace_kwargs: tp.KwargsLike = None,
             fig: tp.Optional[tp.BaseFigure] = None,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot `MA.ma` against `MA.close`.

        Args:
            column (str): Name of the column to plot.
            plot_close (bool): Whether to plot `MA.close`.
            close_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `MA.close`.
            ma_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `MA.ma`.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> vbt.MA.run(ohlcv['Close'], 10).plot()
            ```

            ![](/assets/images/MA.svg)
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        self_col = self.select_one(column=column)

        if fig is None:
            fig = make_figure()
        fig.update_layout(**layout_kwargs)

        if close_trace_kwargs is None:
            close_trace_kwargs = {}
        if ma_trace_kwargs is None:
            ma_trace_kwargs = {}
        close_trace_kwargs = merge_dicts(dict(
            name='Close',
            line=dict(
                color=plotting_cfg['color_schema']['blue']
            )
        ), close_trace_kwargs)
        ma_trace_kwargs = merge_dicts(dict(
            name='MA'
        ), ma_trace_kwargs)

        if plot_close:
            fig = self_col.close.vbt.plot(
                trace_kwargs=close_trace_kwargs,
                add_trace_kwargs=add_trace_kwargs, fig=fig)
        fig = self_col.ma.vbt.plot(
            trace_kwargs=ma_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)

        return fig


setattr(MA, '__doc__', _MA.__doc__)
setattr(MA, 'plot', _MA.plot)

# ############# MSTD ############# #


MSTD = IndicatorFactory(
    class_name='MSTD',
    module_name=__name__,
    short_name='mstd',
    input_names=['close'],
    param_names=['window', 'ewm'],
    output_names=['mstd']
).from_apply_func(
    nb.mstd_apply_nb,
    cache_func=nb.mstd_cache_nb,
    kwargs_to_args=['adjust', 'ddof'],
    ewm=False,
    adjust=False,
    ddof=0
)


class _MSTD(MSTD):
    """Moving Standard Deviation (MSTD).

    Standard deviation is an indicator that measures the size of an assets recent price moves
    in order to predict how volatile the price may be in the future."""

    def plot(self,
             column: tp.Optional[tp.Label] = None,
             mstd_trace_kwargs: tp.KwargsLike = None,
             add_trace_kwargs: tp.KwargsLike = None,
             fig: tp.Optional[tp.BaseFigure] = None,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot `MSTD.mstd`.

        Args:
            column (str): Name of the column to plot.
            mstd_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `MSTD.mstd`.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> vbt.MSTD.run(ohlcv['Close'], 10).plot()
            ```

            ![](/assets/images/MSTD.svg)
        """
        self_col = self.select_one(column=column)

        if fig is None:
            fig = make_figure()
        fig.update_layout(**layout_kwargs)

        if mstd_trace_kwargs is None:
            mstd_trace_kwargs = {}
        mstd_trace_kwargs = merge_dicts(dict(
            name='MSTD'
        ), mstd_trace_kwargs)

        fig = self_col.mstd.vbt.plot(
            trace_kwargs=mstd_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)

        return fig


setattr(MSTD, '__doc__', _MSTD.__doc__)
setattr(MSTD, 'plot', _MSTD.plot)

# ############# BBANDS ############# #


BBANDS = IndicatorFactory(
    class_name='BBANDS',
    module_name=__name__,
    short_name='bb',
    input_names=['close'],
    param_names=['window', 'ewm', 'alpha'],
    output_names=['middle', 'upper', 'lower'],
    custom_output_props=dict(
        percent_b=lambda self: self.wrapper.wrap(
            (self.close.values - self.lower.values) / (self.upper.values - self.lower.values)),
        bandwidth=lambda self: self.wrapper.wrap(
            (self.upper.values - self.lower.values) / self.middle.values)
    )
).from_apply_func(
    nb.bb_apply_nb,
    cache_func=nb.bb_cache_nb,
    kwargs_to_args=['adjust', 'ddof'],
    window=20,
    ewm=False,
    alpha=2,
    adjust=False,
    ddof=0
)


class _BBANDS(BBANDS):
    """Bollinger Bands (BBANDS).

    A Bollinger Band® is a technical analysis tool defined by a set of lines plotted two standard
    deviations (positively and negatively) away from a simple moving average (SMA) of the security's
    price, but can be adjusted to user preferences.

    See [Bollinger Band®](https://www.investopedia.com/terms/b/bollingerbands.asp)."""

    def plot(self,
             column: tp.Optional[tp.Label] = None,
             plot_close: bool = True,
             close_trace_kwargs: tp.KwargsLike = None,
             middle_trace_kwargs: tp.KwargsLike = None,
             upper_trace_kwargs: tp.KwargsLike = None,
             lower_trace_kwargs: tp.KwargsLike = None,
             add_trace_kwargs: tp.KwargsLike = None,
             fig: tp.Optional[tp.BaseFigure] = None,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot `BBANDS.middle`, `BBANDS.upper` and `BBANDS.lower` against
        `BBANDS.close`.

        Args:
            column (str): Name of the column to plot.
            plot_close (bool): Whether to plot `MA.close`.
            close_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `BBANDS.close`.
            middle_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `BBANDS.middle`.
            upper_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `BBANDS.upper`.
            lower_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `BBANDS.lower`.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> vbt.BBANDS.run(ohlcv['Close']).plot()
            ```

            ![](/assets/images/BBANDS.svg)
        """
        from vectorbt._settings import settings
        plotting_cfg = settings['plotting']

        self_col = self.select_one(column=column)

        if fig is None:
            fig = make_figure()
        fig.update_layout(**layout_kwargs)

        if close_trace_kwargs is None:
            close_trace_kwargs = {}
        if middle_trace_kwargs is None:
            middle_trace_kwargs = {}
        if upper_trace_kwargs is None:
            upper_trace_kwargs = {}
        if lower_trace_kwargs is None:
            lower_trace_kwargs = {}
        lower_trace_kwargs = merge_dicts(dict(
            name='Lower Band',
            line=dict(
                color=adjust_opacity(plotting_cfg['color_schema']['gray'], 0.75)
            ),
        ), lower_trace_kwargs)
        upper_trace_kwargs = merge_dicts(dict(
            name='Upper Band',
            line=dict(
                color=adjust_opacity(plotting_cfg['color_schema']['gray'], 0.75)
            ),
            fill='tonexty',
            fillcolor='rgba(128, 128, 128, 0.2)'
        ), upper_trace_kwargs)  # default kwargs
        middle_trace_kwargs = merge_dicts(dict(
            name='Middle Band'
        ), middle_trace_kwargs)
        close_trace_kwargs = merge_dicts(dict(
            name='Close',
            line=dict(color=plotting_cfg['color_schema']['blue'])
        ), close_trace_kwargs)

        fig = self_col.lower.vbt.plot(
            trace_kwargs=lower_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)
        fig = self_col.upper.vbt.plot(
            trace_kwargs=upper_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)
        fig = self_col.middle.vbt.plot(
            trace_kwargs=middle_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)
        if plot_close:
            fig = self_col.close.vbt.plot(
                trace_kwargs=close_trace_kwargs,
                add_trace_kwargs=add_trace_kwargs, fig=fig)

        return fig


setattr(BBANDS, '__doc__', _BBANDS.__doc__)
setattr(BBANDS, 'plot', _BBANDS.plot)

# ############# RSI ############# #


RSI = IndicatorFactory(
    class_name='RSI',
    module_name=__name__,
    short_name='rsi',
    input_names=['close'],
    param_names=['window', 'ewm'],
    output_names=['rsi']
).from_apply_func(
    nb.rsi_apply_nb,
    cache_func=nb.rsi_cache_nb,
    kwargs_to_args=['adjust'],
    window=14,
    ewm=False,
    adjust=False
)


class _RSI(RSI):
    """Relative Strength Index (RSI).

    Compares the magnitude of recent gains and losses over a specified time
    period to measure speed and change of price movements of a security. It is
    primarily used to attempt to identify overbought or oversold conditions in
    the trading of an asset.

    See [Relative Strength Index (RSI)](https://www.investopedia.com/terms/r/rsi.asp)."""

    def plot(self,
             column: tp.Optional[tp.Label] = None,
             levels: tp.Tuple[float, float] = (30, 70),
             rsi_trace_kwargs: tp.KwargsLike = None,
             add_trace_kwargs: tp.KwargsLike = None,
             xref: str = 'x',
             yref: str = 'y',
             fig: tp.Optional[tp.BaseFigure] = None,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot `RSI.rsi`.

        Args:
            column (str): Name of the column to plot.
            levels (tuple): Two extremes: bottom and top.
            rsi_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `RSI.rsi`.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> vbt.RSI.run(ohlcv['Close']).plot()
            ```

            ![](/assets/images/RSI.svg)
        """
        self_col = self.select_one(column=column)

        if fig is None:
            fig = make_figure()
        default_layout = dict()
        default_layout['yaxis' + yref[1:]] = dict(range=[-5, 105])
        fig.update_layout(**default_layout)
        fig.update_layout(**layout_kwargs)

        if rsi_trace_kwargs is None:
            rsi_trace_kwargs = {}
        rsi_trace_kwargs = merge_dicts(dict(
            name='RSI'
        ), rsi_trace_kwargs)

        fig = self_col.rsi.vbt.plot(
            trace_kwargs=rsi_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)

        # Fill void between levels
        fig.add_shape(
            type="rect",
            xref=xref,
            yref=yref,
            x0=self_col.rsi.index[0],
            y0=levels[0],
            x1=self_col.rsi.index[-1],
            y1=levels[1],
            fillcolor="purple",
            opacity=0.2,
            layer="below",
            line_width=0,
        )

        return fig


setattr(RSI, '__doc__', _RSI.__doc__)
setattr(RSI, 'plot', _RSI.plot)

# ############# STOCH ############# #


STOCH = IndicatorFactory(
    class_name='STOCH',
    module_name=__name__,
    short_name='stoch',
    input_names=['high', 'low', 'close'],
    param_names=['k_window', 'd_window', 'd_ewm'],
    output_names=['percent_k', 'percent_d']
).from_apply_func(
    nb.stoch_apply_nb,
    cache_func=nb.stoch_cache_nb,
    kwargs_to_args=['adjust'],
    k_window=14,
    d_window=3,
    d_ewm=False,
    adjust=False
)


class _STOCH(STOCH):
    """Stochastic Oscillator (STOCH).

    A stochastic oscillator is a momentum indicator comparing a particular closing price
    of a security to a range of its prices over a certain period of time. It is used to
    generate overbought and oversold trading signals, utilizing a 0-100 bounded range of values.

    See [Stochastic Oscillator](https://www.investopedia.com/terms/s/stochasticoscillator.asp)."""

    def plot(self,
             column: tp.Optional[tp.Label] = None,
             levels: tp.Tuple[float, float] = (30, 70),
             percent_k_trace_kwargs: tp.KwargsLike = None,
             percent_d_trace_kwargs: tp.KwargsLike = None,
             shape_kwargs: tp.KwargsLike = None,
             add_trace_kwargs: tp.KwargsLike = None,
             xref: str = 'x',
             yref: str = 'y',
             fig: tp.Optional[tp.BaseFigure] = None,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot `STOCH.percent_k` and `STOCH.percent_d`.

        Args:
            column (str): Name of the column to plot.
            levels (tuple): Two extremes: bottom and top.
            percent_k_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `STOCH.percent_k`.
            percent_d_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `STOCH.percent_d`.
            shape_kwargs (dict): Keyword arguments passed to `Figure or FigureWidget.add_shape` for zone between levels.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            xref (str): X coordinate axis.
            yref (str): Y coordinate axis.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> vbt.STOCH.run(ohlcv['High'], ohlcv['Low'], ohlcv['Close']).plot()
            ```

            ![](/assets/images/STOCH.svg)
        """
        self_col = self.select_one(column=column)

        if fig is None:
            fig = make_figure()
        default_layout = dict()
        default_layout['yaxis' + yref[1:]] = dict(range=[-5, 105])
        fig.update_layout(**default_layout)
        fig.update_layout(**layout_kwargs)

        if percent_k_trace_kwargs is None:
            percent_k_trace_kwargs = {}
        if percent_d_trace_kwargs is None:
            percent_d_trace_kwargs = {}
        if shape_kwargs is None:
            shape_kwargs = {}
        percent_k_trace_kwargs = merge_dicts(dict(
            name='%K'
        ), percent_k_trace_kwargs)
        percent_d_trace_kwargs = merge_dicts(dict(
            name='%D'
        ), percent_d_trace_kwargs)

        fig = self_col.percent_k.vbt.plot(
            trace_kwargs=percent_k_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)
        fig = self_col.percent_d.vbt.plot(
            trace_kwargs=percent_d_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)

        # Plot levels
        # Fill void between levels
        shape_kwargs = merge_dicts(dict(
            type="rect",
            xref=xref,
            yref=yref,
            x0=self_col.percent_k.index[0],
            y0=levels[0],
            x1=self_col.percent_k.index[-1],
            y1=levels[1],
            fillcolor="purple",
            opacity=0.2,
            layer="below",
            line_width=0,
        ), shape_kwargs)
        fig.add_shape(**shape_kwargs)

        return fig


setattr(STOCH, '__doc__', _STOCH.__doc__)
setattr(STOCH, 'plot', _STOCH.plot)

# ############# MACD ############# #


MACD = IndicatorFactory(
    class_name='MACD',
    module_name=__name__,
    short_name='macd',
    input_names=['close'],
    param_names=['fast_window', 'slow_window', 'signal_window', 'macd_ewm', 'signal_ewm'],
    output_names=['macd', 'signal'],
    custom_output_props=dict(
        hist=lambda self: self.wrapper.wrap(self.macd.values - self.signal.values),
    )
).from_apply_func(
    nb.macd_apply_nb,
    cache_func=nb.macd_cache_nb,
    kwargs_to_args=['adjust'],
    fast_window=12,
    slow_window=26,
    signal_window=9,
    macd_ewm=False,
    signal_ewm=False,
    adjust=False
)


class _MACD(MACD):
    """Moving Average Convergence Divergence (MACD).

    Is a trend-following momentum indicator that shows the relationship between
    two moving averages of prices.

    See [Moving Average Convergence Divergence – MACD](https://www.investopedia.com/terms/m/macd.asp)."""

    def plot(self,
             column: tp.Optional[tp.Label] = None,
             macd_trace_kwargs: tp.KwargsLike = None,
             signal_trace_kwargs: tp.KwargsLike = None,
             hist_trace_kwargs: tp.KwargsLike = None,
             add_trace_kwargs: tp.KwargsLike = None,
             fig: tp.Optional[tp.BaseFigure] = None,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot `MACD.macd`, `MACD.signal` and `MACD.hist`.

        Args:
            column (str): Name of the column to plot.
            macd_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `MACD.macd`.
            signal_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `MACD.signal`.
            hist_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Bar` for `MACD.hist`.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> vbt.MACD.run(ohlcv['Close']).plot()
            ```

            ![](/assets/images/MACD.svg)
        """
        self_col = self.select_one(column=column)

        if fig is None:
            fig = make_figure()
            fig.update_layout(bargap=0)
        fig.update_layout(**layout_kwargs)

        if macd_trace_kwargs is None:
            macd_trace_kwargs = {}
        if signal_trace_kwargs is None:
            signal_trace_kwargs = {}
        if hist_trace_kwargs is None:
            hist_trace_kwargs = {}
        macd_trace_kwargs = merge_dicts(dict(
            name='MACD'
        ), macd_trace_kwargs)
        signal_trace_kwargs = merge_dicts(dict(
            name='Signal'
        ), signal_trace_kwargs)
        hist_trace_kwargs = merge_dicts(dict(name='Histogram'), hist_trace_kwargs)

        fig = self_col.macd.vbt.plot(
            trace_kwargs=macd_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)
        fig = self_col.signal.vbt.plot(
            trace_kwargs=signal_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)

        # Plot hist
        hist = self_col.hist.values
        hist_diff = generic_nb.diff_1d_nb(hist)
        marker_colors = np.full(hist.shape, adjust_opacity('silver', 0.75), dtype=object)
        marker_colors[(hist > 0) & (hist_diff > 0)] = adjust_opacity('green', 0.75)
        marker_colors[(hist > 0) & (hist_diff <= 0)] = adjust_opacity('lightgreen', 0.75)
        marker_colors[(hist < 0) & (hist_diff < 0)] = adjust_opacity('red', 0.75)
        marker_colors[(hist < 0) & (hist_diff >= 0)] = adjust_opacity('lightcoral', 0.75)

        hist_bar = go.Bar(
            x=self_col.hist.index,
            y=self_col.hist.values,
            marker_color=marker_colors,
            marker_line_width=0
        )
        hist_bar.update(**hist_trace_kwargs)
        if add_trace_kwargs is None:
            add_trace_kwargs = {}
        fig.add_trace(hist_bar, **add_trace_kwargs)

        return fig


setattr(MACD, '__doc__', _MACD.__doc__)
setattr(MACD, 'plot', _MACD.plot)

# ############# ATR ############# #


ATR = IndicatorFactory(
    class_name='ATR',
    module_name=__name__,
    short_name='atr',
    input_names=['high', 'low', 'close'],
    param_names=['window', 'ewm'],
    output_names=['tr', 'atr']
).from_apply_func(
    nb.atr_apply_nb,
    cache_func=nb.atr_cache_nb,
    kwargs_to_args=['adjust'],
    window=14,
    ewm=True,
    adjust=False
)


class _ATR(ATR):
    """Average True Range (ATR).

    The indicator provide an indication of the degree of price volatility.
    Strong moves, in either direction, are often accompanied by large ranges,
    or large True Ranges.

    See [Average True Range - ATR](https://www.investopedia.com/terms/a/atr.asp).

    !!! note
        Uses Simple MA and Exponential MA as compared to Wilder.
    """

    def plot(self,
             column: tp.Optional[tp.Label] = None,
             tr_trace_kwargs: tp.KwargsLike = None,
             atr_trace_kwargs: tp.KwargsLike = None,
             add_trace_kwargs: tp.KwargsLike = None,
             fig: tp.Optional[tp.BaseFigure] = None,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot `ATR.tr` and `ATR.atr`.

        Args:
            column (str): Name of the column to plot.
            tr_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `ATR.tr`.
            atr_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `ATR.atr`.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> vbt.ATR.run(ohlcv['High'], ohlcv['Low'], ohlcv['Close'], 10).plot()
            ```

            ![](/assets/images/ATR.svg)
        """
        self_col = self.select_one(column=column)

        if fig is None:
            fig = make_figure()
        fig.update_layout(**layout_kwargs)

        if tr_trace_kwargs is None:
            tr_trace_kwargs = {}
        if atr_trace_kwargs is None:
            atr_trace_kwargs = {}
        tr_trace_kwargs = merge_dicts(dict(
            name='TR'
        ), tr_trace_kwargs)
        atr_trace_kwargs = merge_dicts(dict(
            name='ATR'
        ), atr_trace_kwargs)

        fig = self_col.tr.vbt.plot(
            trace_kwargs=tr_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)
        fig = self_col.atr.vbt.plot(
            trace_kwargs=atr_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)

        return fig


setattr(ATR, '__doc__', _ATR.__doc__)
setattr(ATR, 'plot', _ATR.plot)

# ############# OBV ############# #


OBV = IndicatorFactory(
    class_name='OBV',
    module_name=__name__,
    short_name='obv',
    input_names=['close', 'volume'],
    param_names=[],
    output_names=['obv'],
).from_custom_func(nb.obv_custom_nb)


class _OBV(OBV):
    """On-balance volume (OBV).

    It relates price and volume in the stock market. OBV is based on a cumulative total volume.

    See [On-Balance Volume (OBV)](https://www.investopedia.com/terms/o/onbalancevolume.asp)."""

    def plot(self,
             column: tp.Optional[tp.Label] = None,
             obv_trace_kwargs: tp.KwargsLike = None,
             add_trace_kwargs: tp.KwargsLike = None,
             fig: tp.Optional[tp.BaseFigure] = None,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        """Plot `OBV.obv`.

        Args:
            column (str): Name of the column to plot.
            obv_trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Scatter` for `OBV.obv`.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```py
            >>> vbt.OBV.run(ohlcv['Close'], ohlcv['Volume']).plot()
            ```

            ![](/assets/images/OBV.svg)
        """
        self_col = self.select_one(column=column)

        if fig is None:
            fig = make_figure()
        fig.update_layout(**layout_kwargs)

        if obv_trace_kwargs is None:
            obv_trace_kwargs = {}
        obv_trace_kwargs = merge_dicts(dict(
            name='OBV'
        ), obv_trace_kwargs)

        fig = self_col.obv.vbt.plot(
            trace_kwargs=obv_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs, fig=fig)

        return fig


setattr(OBV, '__doc__', _OBV.__doc__)
setattr(OBV, 'plot', _OBV.plot)
