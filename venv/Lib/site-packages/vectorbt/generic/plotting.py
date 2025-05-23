# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Base plotting functions.

Provides functions for visualizing data in an efficient and convenient way.
Each creates a figure widget that is compatible with ipywidgets and enables interactive
data visualization in Jupyter Notebook and JupyterLab environments. For more details
on using Plotly, see [Getting Started with Plotly in Python](https://plotly.com/python/getting-started/).

The module can be accessed directly via `vbt.plotting`.

!!! warning
    In case of errors, it won't be visible in the notebook cell, but in the logs."""

import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.basedatatypes import BaseTraceType

from vectorbt import _typing as tp
from vectorbt.base import reshape_fns
from vectorbt.utils import checks
from vectorbt.utils.array_ import renormalize
from vectorbt.utils.colors import rgb_from_cmap
from vectorbt.utils.config import Configured, resolve_dict
from vectorbt.utils.figure import make_figure


def clean_labels(labels: tp.ArrayLikeSequence) -> tp.ArrayLikeSequence:
    """Clean labels.

    Plotly doesn't support multi-indexes."""
    if isinstance(labels, pd.MultiIndex):
        labels = labels.to_flat_index()
    if len(labels) > 0 and isinstance(labels[0], tuple):
        labels = list(map(str, labels))
    return labels


class TraceUpdater:
    def __init__(self, fig: tp.BaseFigure, traces: tp.Tuple[BaseTraceType, ...]) -> None:
        """Base trace updating class."""
        self._fig = fig
        self._traces = traces

    @property
    def fig(self) -> tp.BaseFigure:
        """Figure."""
        return self._fig

    @property
    def traces(self) -> tp.Tuple[BaseTraceType, ...]:
        """Traces to update."""
        return self._traces

    def update(self, *args, **kwargs) -> None:
        """Update the trace data."""
        raise NotImplementedError


class Gauge(Configured, TraceUpdater):
    def __init__(self,
                 value: tp.Optional[float] = None,
                 label: tp.Optional[str] = None,
                 value_range: tp.Optional[tp.Tuple[float, float]] = None,
                 cmap_name: str = 'Spectral',
                 trace_kwargs: tp.KwargsLike = None,
                 add_trace_kwargs: tp.KwargsLike = None,
                 fig: tp.Optional[tp.BaseFigure] = None,
                 **layout_kwargs) -> None:
        """Create a gauge plot.

        Args:
            value (float): The value to be displayed.
            label (str): The label to be displayed.
            value_range (tuple of float): The value range of the gauge.
            cmap_name (str): A matplotlib-compatible colormap name.

                See the [list of available colormaps](https://matplotlib.org/tutorials/colors/colormaps.html).
            trace_kwargs (dict): Keyword arguments passed to the `plotly.graph_objects.Indicator`.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> import vectorbt as vbt

            >>> gauge = vbt.plotting.Gauge(
            ...     value=2,
            ...     value_range=(1, 3),
            ...     label='My Gauge'
            ... )
            >>> gauge.fig
            ```

            ![](/assets/images/Gauge.svg)
        """
        Configured.__init__(
            self,
            value=value,
            label=label,
            value_range=value_range,
            cmap_name=cmap_name,
            trace_kwargs=trace_kwargs,
            add_trace_kwargs=add_trace_kwargs,
            fig=fig,
            **layout_kwargs
        )

        from vectorbt._settings import settings
        layout_cfg = settings['plotting']['layout']

        if trace_kwargs is None:
            trace_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}

        if fig is None:
            fig = make_figure()
            if 'width' in layout_cfg:
                # Calculate nice width and height
                fig.update_layout(
                    width=layout_cfg['width'] * 0.7,
                    height=layout_cfg['width'] * 0.5,
                    margin=dict(t=80)
                )
        fig.update_layout(**layout_kwargs)

        indicator = go.Indicator(
            domain=dict(x=[0, 1], y=[0, 1]),
            mode="gauge+number+delta",
            title=dict(text=label)
        )
        indicator.update(**trace_kwargs)
        fig.add_trace(indicator, **add_trace_kwargs)

        TraceUpdater.__init__(self, fig, (fig.data[-1],))
        self._value_range = value_range
        self._cmap_name = cmap_name

        if value is not None:
            self.update(value)

    @property
    def value_range(self) -> tp.Tuple[float, float]:
        """The value range of the gauge."""
        return self._value_range

    @property
    def cmap_name(self) -> str:
        """A matplotlib-compatible colormap name."""
        return self._cmap_name

    def update(self, value: float) -> None:
        """Update the trace data."""
        if self.value_range is None:
            self._value_range = value, value
        else:
            self._value_range = min(self.value_range[0], value), max(self.value_range[1], value)

        with self.fig.batch_update():
            if self.value_range is not None:
                self.traces[0].gauge.axis.range = self.value_range
                if self.cmap_name is not None:
                    self.traces[0].gauge.bar.color = rgb_from_cmap(self.cmap_name, value, self.value_range)
            self.traces[0].delta.reference = self.traces[0].value
            self.traces[0].value = value


class Bar(Configured, TraceUpdater):
    def __init__(self,
                 data: tp.Optional[tp.ArrayLike] = None,
                 trace_names: tp.TraceNames = None,
                 x_labels: tp.Optional[tp.Labels] = None,
                 trace_kwargs: tp.KwargsLikeSequence = None,
                 add_trace_kwargs: tp.KwargsLike = None,
                 fig: tp.Optional[tp.BaseFigure] = None,
                 **layout_kwargs) -> None:
        """Create a bar plot.

        Args:
            data (array_like): Data in any format that can be converted to NumPy.

                Must be of shape (`x_labels`, `trace_names`).
            trace_names (str or list of str): Trace names, corresponding to columns in pandas.
            x_labels (array_like): X-axis labels, corresponding to index in pandas.
            trace_kwargs (dict or list of dict): Keyword arguments passed to `plotly.graph_objects.Bar`.

                Can be specified per trace as a sequence of dicts.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> import vectorbt as vbt

            >>> bar = vbt.plotting.Bar(
            ...     data=[[1, 2], [3, 4]],
            ...     trace_names=['a', 'b'],
            ...     x_labels=['x', 'y']
            ... )
            >>> bar.fig
            ```

            ![](/assets/images/Bar.svg)
        """
        Configured.__init__(
            self,
            data=data,
            trace_names=trace_names,
            x_labels=x_labels,
            trace_kwargs=trace_kwargs,
            add_trace_kwargs=add_trace_kwargs,
            fig=fig,
            **layout_kwargs
        )

        if trace_kwargs is None:
            trace_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}
        if data is not None:
            data = reshape_fns.to_2d_array(data)
            if trace_names is not None:
                checks.assert_shape_equal(data, trace_names, (1, 0))
        else:
            if trace_names is None:
                raise ValueError("At least data or trace_names must be passed")
        if trace_names is None:
            trace_names = [None] * data.shape[1]
        if isinstance(trace_names, str):
            trace_names = [trace_names]
        if x_labels is not None:
            x_labels = clean_labels(x_labels)

        if fig is None:
            fig = make_figure()
        fig.update_layout(**layout_kwargs)

        for i, trace_name in enumerate(trace_names):
            _trace_kwargs = resolve_dict(trace_kwargs, i=i)
            trace_name = _trace_kwargs.pop('name', trace_name)
            if trace_name is not None:
                trace_name = str(trace_name)
            bar = go.Bar(
                x=x_labels,
                name=trace_name,
                showlegend=trace_name is not None
            )
            bar.update(**_trace_kwargs)
            fig.add_trace(bar, **add_trace_kwargs)

        TraceUpdater.__init__(self, fig, fig.data[-len(trace_names):])

        if data is not None:
            self.update(data)

    def update(self, data: tp.ArrayLike) -> None:
        """Update the trace data.

        Usage:
            ```pycon
            >>> bar.update([[2, 1], [4, 3]])
            >>> bar.fig
            ```

            ![](/assets/images/Bar_updated.svg)
        """
        data = reshape_fns.to_2d_array(data)
        with self.fig.batch_update():
            for i, bar in enumerate(self.traces):
                bar.y = data[:, i]
                if bar.marker.colorscale is not None:
                    bar.marker.color = data[:, i]


class Scatter(Configured, TraceUpdater):
    def __init__(self,
                 data: tp.Optional[tp.ArrayLike] = None,
                 trace_names: tp.TraceNames = None,
                 x_labels: tp.Optional[tp.Labels] = None,
                 trace_kwargs: tp.KwargsLikeSequence = None,
                 add_trace_kwargs: tp.KwargsLike = None,
                 fig: tp.Optional[tp.BaseFigure] = None,
                 **layout_kwargs) -> None:
        """Create a scatter plot.

        Args:
            data (array_like): Data in any format that can be converted to NumPy.

                Must be of shape (`x_labels`, `trace_names`).
            trace_names (str or list of str): Trace names, corresponding to columns in pandas.
            x_labels (array_like): X-axis labels, corresponding to index in pandas.
            trace_kwargs (dict or list of dict): Keyword arguments passed to `plotly.graph_objects.Scatter`.

                Can be specified per trace as a sequence of dicts.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> import vectorbt as vbt

            >>> scatter = vbt.plotting.Scatter(
            ...     data=[[1, 2], [3, 4]],
            ...     trace_names=['a', 'b'],
            ...     x_labels=['x', 'y']
            ... )
            >>> scatter.fig
            ```

            ![](/assets/images/Scatter.svg)
        """
        Configured.__init__(
            self,
            data=data,
            trace_names=trace_names,
            x_labels=x_labels,
            trace_kwargs=trace_kwargs,
            add_trace_kwargs=add_trace_kwargs,
            fig=fig,
            **layout_kwargs
        )

        if trace_kwargs is None:
            trace_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}
        if data is not None:
            data = reshape_fns.to_2d_array(data)
            if trace_names is not None:
                checks.assert_shape_equal(data, trace_names, (1, 0))
        else:
            if trace_names is None:
                raise ValueError("At least data or trace_names must be passed")
        if trace_names is None:
            trace_names = [None] * data.shape[1]
        if isinstance(trace_names, str):
            trace_names = [trace_names]
        if x_labels is not None:
            x_labels = clean_labels(x_labels)

        if fig is None:
            fig = make_figure()
        fig.update_layout(**layout_kwargs)

        for i, trace_name in enumerate(trace_names):
            _trace_kwargs = resolve_dict(trace_kwargs, i=i)
            trace_name = _trace_kwargs.pop('name', trace_name)
            if trace_name is not None:
                trace_name = str(trace_name)
            scatter = go.Scatter(
                x=x_labels,
                name=trace_name,
                showlegend=trace_name is not None
            )
            scatter.update(**_trace_kwargs)
            fig.add_trace(scatter, **add_trace_kwargs)

        TraceUpdater.__init__(self, fig, fig.data[-len(trace_names):])

        if data is not None:
            self.update(data)

    def update(self, data: tp.ArrayLike) -> None:
        """Update the trace data."""
        data = reshape_fns.to_2d_array(data)

        with self.fig.batch_update():
            for i, trace in enumerate(self.traces):
                trace.y = data[:, i]


class Histogram(Configured, TraceUpdater):
    def __init__(self,
                 data: tp.Optional[tp.ArrayLike] = None,
                 trace_names: tp.TraceNames = None,
                 horizontal: bool = False,
                 remove_nan: bool = True,
                 from_quantile: tp.Optional[float] = None,
                 to_quantile: tp.Optional[float] = None,
                 trace_kwargs: tp.KwargsLikeSequence = None,
                 add_trace_kwargs: tp.KwargsLike = None,
                 fig: tp.Optional[tp.BaseFigure] = None,
                 **layout_kwargs) -> None:
        """Create a histogram plot.

        Args:
            data (array_like): Data in any format that can be converted to NumPy.

                Must be of shape (any, `trace_names`).
            trace_names (str or list of str): Trace names, corresponding to columns in pandas.
            horizontal (bool): Whether to plot horizontally.
            remove_nan (bool): Whether to remove NaN values.
            from_quantile (float): Filter out data points before this quantile.

                Should be in range `[0, 1]`.
            to_quantile (float): Filter out data points after this quantile.

                Should be in range `[0, 1]`.
            trace_kwargs (dict or list of dict): Keyword arguments passed to `plotly.graph_objects.Histogram`.

                Can be specified per trace as a sequence of dicts.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> import vectorbt as vbt

            >>> hist = vbt.plotting.Histogram(
            ...     data=[[1, 2], [3, 4], [2, 1]],
            ...     trace_names=['a', 'b']
            ... )
            >>> hist.fig
            ```

            ![](/assets/images/Histogram.svg)
        """
        Configured.__init__(
            self,
            data=data,
            trace_names=trace_names,
            horizontal=horizontal,
            remove_nan=remove_nan,
            from_quantile=from_quantile,
            to_quantile=to_quantile,
            trace_kwargs=trace_kwargs,
            add_trace_kwargs=add_trace_kwargs,
            fig=fig,
            **layout_kwargs
        )

        if trace_kwargs is None:
            trace_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}
        if data is not None:
            data = reshape_fns.to_2d_array(data)
            if trace_names is not None:
                checks.assert_shape_equal(data, trace_names, (1, 0))
        else:
            if trace_names is None:
                raise ValueError("At least data or trace_names must be passed")
        if trace_names is None:
            trace_names = [None] * data.shape[1]
        if isinstance(trace_names, str):
            trace_names = [trace_names]

        if fig is None:
            fig = make_figure()
            fig.update_layout(barmode='overlay')
        fig.update_layout(**layout_kwargs)

        for i, trace_name in enumerate(trace_names):
            _trace_kwargs = resolve_dict(trace_kwargs, i=i)
            trace_name = _trace_kwargs.pop('name', trace_name)
            if trace_name is not None:
                trace_name = str(trace_name)
            hist = go.Histogram(
                opacity=0.75 if len(trace_names) > 1 else 1,
                name=trace_name,
                showlegend=trace_name is not None
            )
            hist.update(**_trace_kwargs)
            fig.add_trace(hist, **add_trace_kwargs)

        TraceUpdater.__init__(self, fig, fig.data[-len(trace_names):])
        self._horizontal = horizontal
        self._remove_nan = remove_nan
        self._from_quantile = from_quantile
        self._to_quantile = to_quantile

        if data is not None:
            self.update(data)

    @property
    def horizontal(self):
        """Whether to plot horizontally."""
        return self._horizontal

    @property
    def remove_nan(self):
        """Whether to remove NaN values."""
        return self._remove_nan

    @property
    def from_quantile(self):
        """Filter out data points before this quantile."""
        return self._from_quantile

    @property
    def to_quantile(self):
        """Filter out data points after this quantile."""
        return self._to_quantile

    def update(self, data: tp.ArrayLike) -> None:
        """Update the trace data."""
        data = reshape_fns.to_2d_array(data)

        with self.fig.batch_update():
            for i, trace in enumerate(self.traces):
                d = data[:, i]
                if self.remove_nan:
                    d = d[~np.isnan(d)]
                mask = np.full(d.shape, True)
                if self.from_quantile is not None:
                    mask &= d >= np.quantile(d, self.from_quantile)
                if self.to_quantile is not None:
                    mask &= d <= np.quantile(d, self.to_quantile)
                d = d[mask]
                if self.horizontal:
                    trace.x = None
                    trace.y = d
                else:
                    trace.x = d
                    trace.y = None


class Box(Configured, TraceUpdater):
    def __init__(self,
                 data: tp.Optional[tp.ArrayLike] = None,
                 trace_names: tp.TraceNames = None,
                 horizontal: bool = False,
                 remove_nan: bool = True,
                 from_quantile: tp.Optional[float] = None,
                 to_quantile: tp.Optional[float] = None,
                 trace_kwargs: tp.KwargsLikeSequence = None,
                 add_trace_kwargs: tp.KwargsLike = None,
                 fig: tp.Optional[tp.BaseFigure] = None,
                 **layout_kwargs) -> None:
        """Create a box plot.

        For keyword arguments, see `Histogram`.

        Usage:
            ```pycon
            >>> import vectorbt as vbt

            >>> box = vbt.plotting.Box(
            ...     data=[[1, 2], [3, 4], [2, 1]],
            ...     trace_names=['a', 'b']
            ... )
            >>> box.fig
            ```

            ![](/assets/images/Box.svg)
        """
        Configured.__init__(
            self,
            data=data,
            trace_names=trace_names,
            horizontal=horizontal,
            remove_nan=remove_nan,
            from_quantile=from_quantile,
            to_quantile=to_quantile,
            trace_kwargs=trace_kwargs,
            add_trace_kwargs=add_trace_kwargs,
            fig=fig,
            **layout_kwargs
        )

        if trace_kwargs is None:
            trace_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}
        if data is not None:
            data = reshape_fns.to_2d_array(data)
            if trace_names is not None:
                checks.assert_shape_equal(data, trace_names, (1, 0))
        else:
            if trace_names is None:
                raise ValueError("At least data or trace_names must be passed")
        if trace_names is None:
            trace_names = [None] * data.shape[1]
        if isinstance(trace_names, str):
            trace_names = [trace_names]

        if fig is None:
            fig = make_figure()
        fig.update_layout(**layout_kwargs)

        for i, trace_name in enumerate(trace_names):
            _trace_kwargs = resolve_dict(trace_kwargs, i=i)
            trace_name = _trace_kwargs.pop('name', trace_name)
            if trace_name is not None:
                trace_name = str(trace_name)
            box = go.Box(
                name=trace_name,
                showlegend=trace_name is not None
            )
            box.update(**_trace_kwargs)
            fig.add_trace(box, **add_trace_kwargs)

        TraceUpdater.__init__(self, fig, fig.data[-len(trace_names):])
        self._horizontal = horizontal
        self._remove_nan = remove_nan
        self._from_quantile = from_quantile
        self._to_quantile = to_quantile

        if data is not None:
            self.update(data)

    @property
    def horizontal(self):
        """Whether to plot horizontally."""
        return self._horizontal

    @property
    def remove_nan(self):
        """Whether to remove NaN values."""
        return self._remove_nan

    @property
    def from_quantile(self):
        """Filter out data points before this quantile."""
        return self._from_quantile

    @property
    def to_quantile(self):
        """Filter out data points after this quantile."""
        return self._to_quantile

    def update(self, data: tp.ArrayLike) -> None:
        """Update the trace data."""
        data = reshape_fns.to_2d_array(data)

        with self.fig.batch_update():
            for i, trace in enumerate(self.traces):
                d = data[:, i]
                if self.remove_nan:
                    d = d[~np.isnan(d)]
                mask = np.full(d.shape, True)
                if self.from_quantile is not None:
                    mask &= d >= np.quantile(d, self.from_quantile)
                if self.to_quantile is not None:
                    mask &= d <= np.quantile(d, self.to_quantile)
                d = d[mask]
                if self.horizontal:
                    trace.x = d
                    trace.y = None
                else:
                    trace.x = None
                    trace.y = d


class Heatmap(Configured, TraceUpdater):
    def __init__(self,
                 data: tp.Optional[tp.ArrayLike] = None,
                 x_labels: tp.Optional[tp.Labels] = None,
                 y_labels: tp.Optional[tp.Labels] = None,
                 is_x_category: bool = False,
                 is_y_category: bool = False,
                 trace_kwargs: tp.KwargsLike = None,
                 add_trace_kwargs: tp.KwargsLike = None,
                 fig: tp.Optional[tp.BaseFigure] = None,
                 **layout_kwargs) -> None:
        """Create a heatmap plot.

        Args:
            data (array_like): Data in any format that can be converted to NumPy.

                Must be of shape (`y_labels`, `x_labels`).
            x_labels (array_like): X-axis labels, corresponding to columns in pandas.
            y_labels (array_like): Y-axis labels, corresponding to index in pandas.
            is_x_category (bool): Whether X-axis is a categorical axis.
            is_y_category (bool): Whether Y-axis is a categorical axis.
            trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Heatmap`.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        Usage:
            ```pycon
            >>> import vectorbt as vbt

            >>> heatmap = vbt.plotting.Heatmap(
            ...     data=[[1, 2], [3, 4]],
            ...     x_labels=['a', 'b'],
            ...     y_labels=['x', 'y']
            ... )
            >>> heatmap.fig
            ```

            ![](/assets/images/Heatmap.svg)
        """
        Configured.__init__(
            self,
            data=data,
            x_labels=x_labels,
            y_labels=y_labels,
            trace_kwargs=trace_kwargs,
            add_trace_kwargs=add_trace_kwargs,
            fig=fig,
            **layout_kwargs
        )

        from vectorbt._settings import settings
        layout_cfg = settings['plotting']['layout']

        if trace_kwargs is None:
            trace_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}
        if data is not None:
            data = reshape_fns.to_2d_array(data)
            if x_labels is not None:
                checks.assert_shape_equal(data, x_labels, (1, 0))
            if y_labels is not None:
                checks.assert_shape_equal(data, y_labels, (0, 0))
        else:
            if x_labels is None or y_labels is None:
                raise ValueError("At least data, or x_labels and y_labels must be passed")
        if x_labels is not None:
            x_labels = clean_labels(x_labels)
        if y_labels is not None:
            y_labels = clean_labels(y_labels)

        if fig is None:
            fig = make_figure()
            if 'width' in layout_cfg:
                # Calculate nice width and height
                max_width = layout_cfg['width']
                if data is not None:
                    x_len = data.shape[1]
                    y_len = data.shape[0]
                else:
                    x_len = len(x_labels)
                    y_len = len(y_labels)
                width = math.ceil(renormalize(
                    x_len / (x_len + y_len),
                    (0, 1),
                    (0.3 * max_width, max_width)
                ))
                width = min(width + 150, max_width)  # account for colorbar
                height = math.ceil(renormalize(
                    y_len / (x_len + y_len),
                    (0, 1),
                    (0.3 * max_width, max_width)
                ))
                height = min(height, max_width * 0.7)  # limit height
                fig.update_layout(
                    width=width,
                    height=height
                )

        heatmap = go.Heatmap(
            hoverongaps=False,
            colorscale='Plasma',
            x=x_labels,
            y=y_labels
        )
        heatmap.update(**trace_kwargs)
        fig.add_trace(heatmap, **add_trace_kwargs)

        axis_kwargs = dict()
        if is_x_category:
            if fig.data[-1]['xaxis'] is not None:
                axis_kwargs['xaxis' + fig.data[-1]['xaxis'][1:]] = dict(type='category')
            else:
                axis_kwargs['xaxis'] = dict(type='category')
        if is_y_category:
            if fig.data[-1]['yaxis'] is not None:
                axis_kwargs['yaxis' + fig.data[-1]['yaxis'][1:]] = dict(type='category')
            else:
                axis_kwargs['yaxis'] = dict(type='category')
        fig.update_layout(**axis_kwargs)
        fig.update_layout(**layout_kwargs)

        TraceUpdater.__init__(self, fig, (fig.data[-1],))

        if data is not None:
            self.update(data)

    def update(self, data: tp.ArrayLike) -> None:
        """Update the trace data."""
        data = reshape_fns.to_2d_array(data)

        with self.fig.batch_update():
            self.traces[0].z = data


class Volume(Configured, TraceUpdater):
    def __init__(self,
                 data: tp.Optional[tp.ArrayLike] = None,
                 x_labels: tp.Optional[tp.Labels] = None,
                 y_labels: tp.Optional[tp.Labels] = None,
                 z_labels: tp.Optional[tp.Labels] = None,
                 trace_kwargs: tp.KwargsLike = None,
                 add_trace_kwargs: tp.KwargsLike = None,
                 scene_name: str = 'scene',
                 fig: tp.Optional[tp.BaseFigure] = None,
                 **layout_kwargs) -> None:
        """Create a volume plot.

        Args:
            data (array_like): Data in any format that can be converted to NumPy.

                Must be a 3-dim array.
            x_labels (array_like): X-axis labels.
            y_labels (array_like): Y-axis labels.
            z_labels (array_like): Z-axis labels.
            trace_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Volume`.
            add_trace_kwargs (dict): Keyword arguments passed to `add_trace`.
            scene_name (str): Reference to the 3D scene.
            fig (Figure or FigureWidget): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        !!! note
            Figure widgets have currently problems displaying NaNs.
            Use `.show()` method for rendering.

        Usage:
            ```pycon
            >>> import vectorbt as vbt
            >>> import numpy as np

            >>> volume = vbt.plotting.Volume(
            ...     data=np.random.randint(1, 10, size=(3, 3, 3)),
            ...     x_labels=['a', 'b', 'c'],
            ...     y_labels=['d', 'e', 'f'],
            ...     z_labels=['g', 'h', 'i']
            ... )
            >>> volume.fig
            ```

            ![](/assets/images/Volume.svg)
        """
        Configured.__init__(
            self,
            data=data,
            x_labels=x_labels,
            y_labels=y_labels,
            z_labels=z_labels,
            trace_kwargs=trace_kwargs,
            add_trace_kwargs=add_trace_kwargs,
            scene_name=scene_name,
            fig=fig,
            **layout_kwargs
        )

        from vectorbt._settings import settings
        layout_cfg = settings['plotting']['layout']

        if trace_kwargs is None:
            trace_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}
        if data is not None:
            checks.assert_ndim(data, 3)
            data = np.asarray(data)
            x_len, y_len, z_len = data.shape
            if x_labels is not None:
                checks.assert_shape_equal(data, x_labels, (0, 0))
            if y_labels is not None:
                checks.assert_shape_equal(data, y_labels, (1, 0))
            if z_labels is not None:
                checks.assert_shape_equal(data, z_labels, (2, 0))
        else:
            if x_labels is None or y_labels is None or z_labels is None:
                raise ValueError("At least data, or x_labels, y_labels and z_labels must be passed")
            x_len = len(x_labels)
            y_len = len(y_labels)
            z_len = len(z_labels)
        if x_labels is None:
            x_labels = np.arange(x_len)
        else:
            x_labels = clean_labels(x_labels)
        if y_labels is None:
            y_labels = np.arange(y_len)
        else:
            y_labels = clean_labels(y_labels)
        if z_labels is None:
            z_labels = np.arange(z_len)
        else:
            z_labels = clean_labels(z_labels)
        x_labels = np.asarray(x_labels)
        y_labels = np.asarray(y_labels)
        z_labels = np.asarray(z_labels)

        if fig is None:
            fig = make_figure()
            if 'width' in layout_cfg:
                # Calculate nice width and height
                fig.update_layout(
                    width=layout_cfg['width'],
                    height=0.7 * layout_cfg['width']
                )

        # Non-numeric data types are not supported by go.Volume, so use ticktext
        # Note: Currently plotly displays the entire tick array, in future versions it will be more sensible
        more_layout = dict()
        if not np.issubdtype(x_labels.dtype, np.number):
            x_ticktext = x_labels
            x_labels = np.arange(x_len)
            more_layout[scene_name] = dict(
                xaxis=dict(
                    ticktext=x_ticktext,
                    tickvals=x_labels,
                    tickmode='array'
                )
            )
        if not np.issubdtype(y_labels.dtype, np.number):
            y_ticktext = y_labels
            y_labels = np.arange(y_len)
            more_layout[scene_name] = dict(
                yaxis=dict(
                    ticktext=y_ticktext,
                    tickvals=y_labels,
                    tickmode='array'
                )
            )
        if not np.issubdtype(z_labels.dtype, np.number):
            z_ticktext = z_labels
            z_labels = np.arange(z_len)
            more_layout[scene_name] = dict(
                zaxis=dict(
                    ticktext=z_ticktext,
                    tickvals=z_labels,
                    tickmode='array'
                )
            )
        fig.update_layout(**more_layout)
        fig.update_layout(**layout_kwargs)

        # Arrays must have the same length as the flattened data array
        x = np.repeat(x_labels, len(y_labels) * len(z_labels))
        y = np.tile(np.repeat(y_labels, len(z_labels)), len(x_labels))
        z = np.tile(z_labels, len(x_labels) * len(y_labels))

        volume = go.Volume(
            x=x,
            y=y,
            z=z,
            opacity=0.2,
            surface_count=15,  # keep low for big data
            colorscale='Plasma'
        )
        volume.update(**trace_kwargs)
        fig.add_trace(volume, **add_trace_kwargs)

        TraceUpdater.__init__(self, fig, (fig.data[-1],))

        if data is not None:
            self.update(data)

    def update(self, data: tp.ArrayLike) -> None:
        """Update the trace data."""
        data = np.asarray(data).flatten()

        with self.fig.batch_update():
            self.traces[0].value = data
