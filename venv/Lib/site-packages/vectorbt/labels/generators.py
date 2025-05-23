# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Basic look-ahead indicators and label generators.

You can access all the indicators either by `vbt.*` or `vbt.labels.*`."""

from vectorbt import _typing as tp
from vectorbt.indicators.configs import flex_elem_param_config
from vectorbt.indicators.factory import IndicatorFactory
from vectorbt.labels import nb
from vectorbt.labels.enums import TrendMode

# ############# Look-ahead indicators ############# #

FMEAN = IndicatorFactory(
    class_name='FMEAN',
    module_name=__name__,
    input_names=['close'],
    param_names=['window', 'ewm'],
    output_names=['fmean']
).from_apply_func(
    nb.future_mean_apply_nb,
    kwargs_to_args=['wait', 'adjust'],
    ewm=False,
    wait=1,
    adjust=False
)

FMEAN.__doc__ = """Look-ahead indicator based on `vectorbt.labels.nb.future_mean_apply_nb`."""

FSTD = IndicatorFactory(
    class_name='FSTD',
    module_name=__name__,
    input_names=['close'],
    param_names=['window', 'ewm'],
    output_names=['fstd']
).from_apply_func(
    nb.future_std_apply_nb,
    kwargs_to_args=['wait', 'adjust', 'ddof'],
    ewm=False,
    wait=1,
    adjust=False,
    ddof=0
)

FSTD.__doc__ = """Look-ahead indicator based on `vectorbt.labels.nb.future_std_apply_nb`."""

FMIN = IndicatorFactory(
    class_name='FMIN',
    module_name=__name__,
    input_names=['close'],
    param_names=['window'],
    output_names=['fmin']
).from_apply_func(
    nb.future_min_apply_nb,
    kwargs_to_args=['wait'],
    wait=1
)

FMIN.__doc__ = """Look-ahead indicator based on `vectorbt.labels.nb.future_min_apply_nb`."""

FMAX = IndicatorFactory(
    class_name='FMAX',
    module_name=__name__,
    input_names=['close'],
    param_names=['window'],
    output_names=['fmax']
).from_apply_func(
    nb.future_max_apply_nb,
    kwargs_to_args=['wait'],
    wait=1
)

FMAX.__doc__ = """Look-ahead indicator based on `vectorbt.labels.nb.future_max_apply_nb`."""


# ############# Label generators ############# #


def _plot(self, column: tp.Optional[tp.Label] = None, **kwargs) -> tp.BaseFigure:  # pragma: no cover
    """Plot `close` and overlay it with the heatmap of `labels`.

    `**kwargs` are passed to `vectorbt.generic.accessors.GenericSRAccessor.overlay_with_heatmap`."""
    self_col = self.select_one(column=column, group_by=False)

    return self_col.close.rename('close').vbt.overlay_with_heatmap(self_col.labels.rename('labels'), **kwargs)


FIXLB = IndicatorFactory(
    class_name='FIXLB',
    module_name=__name__,
    input_names=['close'],
    param_names=['n'],
    output_names=['labels']
).from_apply_func(
    nb.fixed_labels_apply_nb
)


class _FIXLB(FIXLB):
    """Label generator based on `vectorbt.labels.nb.fixed_labels_apply_nb`."""

    plot = _plot


setattr(FIXLB, '__doc__', _FIXLB.__doc__)
setattr(FIXLB, 'plot', _FIXLB.plot)

MEANLB = IndicatorFactory(
    class_name='MEANLB',
    module_name=__name__,
    input_names=['close'],
    param_names=['window', 'ewm'],
    output_names=['labels']
).from_apply_func(
    nb.mean_labels_apply_nb,
    kwargs_to_args=['wait', 'adjust'],
    ewm=False,
    wait=1,
    adjust=False
)


class _MEANLB(MEANLB):
    """Label generator based on `vectorbt.labels.nb.mean_labels_apply_nb`."""

    plot = _plot


setattr(MEANLB, '__doc__', _MEANLB.__doc__)
setattr(MEANLB, 'plot', _MEANLB.plot)

LEXLB = IndicatorFactory(
    class_name='LEXLB',
    module_name=__name__,
    input_names=['close'],
    param_names=['pos_th', 'neg_th'],
    output_names=['labels']
).from_apply_func(
    nb.local_extrema_apply_nb,
    param_settings=dict(
        pos_th=flex_elem_param_config,
        neg_th=flex_elem_param_config
    ),
    pass_flex_2d=True
)


class _LEXLB(LEXLB):
    """Label generator based on `vectorbt.labels.nb.local_extrema_apply_nb`."""

    plot = _plot


setattr(LEXLB, '__doc__', _LEXLB.__doc__)
setattr(LEXLB, 'plot', _LEXLB.plot)

TRENDLB = IndicatorFactory(
    class_name='TRENDLB',
    module_name=__name__,
    input_names=['close'],
    param_names=['pos_th', 'neg_th', 'mode'],
    output_names=['labels']
).from_apply_func(
    nb.trend_labels_apply_nb,
    param_settings=dict(
        pos_th=flex_elem_param_config,
        neg_th=flex_elem_param_config,
        mode=dict(dtype=TrendMode)
    ),
    pass_flex_2d=True,
    mode=TrendMode.Binary
)


class _TRENDLB(TRENDLB):
    """Label generator based on `vectorbt.labels.nb.trend_labels_apply_nb`."""

    plot = _plot


setattr(TRENDLB, '__doc__', _TRENDLB.__doc__)
setattr(TRENDLB, 'plot', _TRENDLB.plot)

BOLB = IndicatorFactory(
    class_name='BOLB',
    module_name=__name__,
    input_names=['close'],
    param_names=['window', 'pos_th', 'neg_th'],
    output_names=['labels']
).from_apply_func(
    nb.breakout_labels_nb,
    param_settings=dict(
        pos_th=flex_elem_param_config,
        neg_th=flex_elem_param_config
    ),
    pass_flex_2d=True,
    kwargs_to_args=['wait'],
    pos_th=0.,
    neg_th=0.,
    wait=1
)


class _BOLB(BOLB):
    """Label generator based on `vectorbt.labels.nb.breakout_labels_nb`."""

    plot = _plot


setattr(BOLB, '__doc__', _BOLB.__doc__)
setattr(BOLB, 'plot', _BOLB.plot)
