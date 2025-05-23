# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Plotly Express pandas accessors.

!!! note
    Accessors do not utilize caching."""

from inspect import getmembers, isfunction

import pandas as pd
import plotly.express as px

from vectorbt import _typing as tp
from vectorbt.base.accessors import BaseAccessor, BaseDFAccessor, BaseSRAccessor
from vectorbt.base.reshape_fns import to_2d_array
from vectorbt.generic.plotting import clean_labels
from vectorbt.root_accessors import register_dataframe_vbt_accessor, register_series_vbt_accessor
from vectorbt.utils import checks
from vectorbt.utils.config import merge_dicts
from vectorbt.utils.figure import make_figure


def attach_px_methods(cls: tp.Type[tp.T]) -> tp.Type[tp.T]:
    """Class decorator to attach Plotly Express methods."""

    for px_func_name, px_func in getmembers(px, isfunction):
        if checks.func_accepts_arg(px_func, 'data_frame') or px_func_name == 'imshow':
            def plot_func(self, *args, _px_func_name: str = px_func_name,
                          _px_func: tp.Callable = px_func, **kwargs) -> tp.BaseFigure:
                from vectorbt._settings import settings
                layout_cfg = settings['plotting']['layout']

                layout_kwargs = dict(
                    template=kwargs.pop('template', layout_cfg['template']),
                    width=kwargs.pop('width', layout_cfg['width']),
                    height=kwargs.pop('height', layout_cfg['height'])
                )
                # Fix category_orders
                if 'color' in kwargs:
                    if isinstance(kwargs['color'], str):
                        if isinstance(self.obj, pd.DataFrame):
                            if kwargs['color'] in self.obj.columns:
                                category_orders = dict()
                                category_orders[kwargs['color']] = sorted(self.obj[kwargs['color']].unique())
                                kwargs = merge_dicts(dict(category_orders=category_orders), kwargs)

                # Fix Series name
                obj = self.obj.copy(deep=False)
                if isinstance(obj, pd.Series):
                    if obj.name is not None:
                        obj = obj.rename(str(obj.name))
                else:
                    obj.columns = clean_labels(obj.columns)
                obj.index = clean_labels(obj.index)

                if _px_func_name == 'imshow':
                    return make_figure(_px_func(
                        to_2d_array(obj), *args, **layout_kwargs, **kwargs
                    ), layout=layout_kwargs)
                return make_figure(_px_func(
                    obj, *args, **layout_kwargs, **kwargs
                ), layout=layout_kwargs)

            setattr(cls, px_func_name, plot_func)
    return cls


@attach_px_methods
class PXAccessor(BaseAccessor):
    """Accessor for running Plotly Express functions.

    Accessible through `pd.Series.vbt.px` and `pd.DataFrame.vbt.px`.

    Usage:
        ```pycon
        >>> import pandas as pd
        >>> import vectorbt as vbt

        >>> vbt.settings.set_theme('seaborn')

        >>> pd.Series([1, 2, 3]).vbt.px.bar()
        ```

        ![](/assets/images/px_bar.svg)
    """

    def __init__(self, obj: tp.SeriesFrame, **kwargs) -> None:
        BaseAccessor.__init__(self, obj, **kwargs)


@register_series_vbt_accessor('px')
class PXSRAccessor(PXAccessor, BaseSRAccessor):
    """Accessor for running Plotly Express functions. For Series only.

    Accessible through `pd.Series.vbt.px`."""

    def __init__(self, obj: tp.Series, **kwargs) -> None:
        BaseSRAccessor.__init__(self, obj, **kwargs)
        PXAccessor.__init__(self, obj, **kwargs)


@register_dataframe_vbt_accessor('px')
class PXDFAccessor(PXAccessor, BaseDFAccessor):
    """Accessor for running Plotly Express functions. For DataFrames only.

    Accessible through `pd.DataFrame.vbt.px`."""

    def __init__(self, obj: tp.Frame, **kwargs) -> None:
        BaseDFAccessor.__init__(self, obj, **kwargs)
        PXAccessor.__init__(self, obj, **kwargs)
