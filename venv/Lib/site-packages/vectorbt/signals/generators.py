# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Signal generators built with `vectorbt.signals.factory.SignalFactory`."""

import numpy as np
import plotly.graph_objects as go

from vectorbt import _typing as tp
from vectorbt.indicators.configs import flex_col_param_config, flex_elem_param_config
from vectorbt.signals.enums import StopType
from vectorbt.signals.factory import SignalFactory
from vectorbt.signals.nb import (
    rand_enex_apply_nb,
    rand_by_prob_choice_nb,
    stop_choice_nb,
    ohlc_stop_choice_nb,
    rand_choice_nb
)
from vectorbt.utils.config import Config
from vectorbt.utils.figure import make_figure

# ############# RAND ############# #

RAND = SignalFactory(
    class_name='RAND',
    module_name=__name__,
    short_name='rand',
    mode='entries',
    param_names=['n']
).from_choice_func(
    entry_choice_func=rand_choice_nb,
    entry_settings=dict(
        pass_params=['n']
    ),
    param_settings=dict(
        n=flex_col_param_config
    ),
    seed=None
)


class _RAND(RAND):
    """Random entry signal generator based on the number of signals.

    Generates `entries` based on `vectorbt.signals.nb.rand_choice_nb`.

    !!! hint
        Parameter `n` can be either a single value (per frame) or a NumPy array (per column).
        To generate multiple combinations, pass it as a list.

    Usage:
        * Test three different entry counts values:

        ```pycon
        >>> import vectorbt as vbt

        >>> rand = vbt.RAND.run(input_shape=(6,), n=[1, 2, 3], seed=42)

        >>> rand.entries
        rand_n      1      2      3
        0        True   True   True
        1       False  False   True
        2       False  False  False
        3       False   True  False
        4       False  False   True
        5       False  False  False
        ```

        * Entry count can also be set per column:

        ```pycon
        >>> import numpy as np

        >>> rand = vbt.RAND.run(input_shape=(8, 2), n=[np.array([1, 2]), 3], seed=42)

        >>> rand.entries
        rand_n      1      2      3      3
                    0      1      0      1
        0       False  False   True  False
        1        True  False  False  False
        2       False  False  False   True
        3       False   True   True  False
        4       False  False  False  False
        5       False  False  False   True
        6       False  False   True  False
        7       False   True  False   True
        ```
    """
    pass


setattr(RAND, '__doc__', _RAND.__doc__)

RANDX = SignalFactory(
    class_name='RANDX',
    module_name=__name__,
    short_name='randx',
    mode='exits'
).from_choice_func(
    exit_choice_func=rand_choice_nb,
    exit_settings=dict(
        pass_kwargs=dict(n=1)
    ),
    seed=None
)


class _RANDX(RANDX):
    """Random exit signal generator based on the number of signals.

    Generates `exits` based on `entries` and `vectorbt.signals.nb.rand_choice_nb`.

    See `RAND` for notes on parameters.

    Usage:
        * Generate an exit for each entry:

        ```pycon
        >>> import vectorbt as vbt
        >>> import pandas as pd

        >>> entries = pd.Series([True, False, False, True, False, False])
        >>> randx = vbt.RANDX.run(entries, seed=42)

        >>> randx.exits
        0    False
        1    False
        2     True
        3    False
        4     True
        5    False
        dtype: bool
        ```
    """
    pass


setattr(RANDX, '__doc__', _RANDX.__doc__)

RANDNX = SignalFactory(
    class_name='RANDNX',
    module_name=__name__,
    short_name='randnx',
    mode='both',
    param_names=['n']
).from_apply_func(  # apply_func since function is (almost) vectorized
    rand_enex_apply_nb,
    require_input_shape=True,
    param_settings=dict(
        n=flex_col_param_config
    ),
    kwargs_to_args=['entry_wait', 'exit_wait'],
    entry_wait=1,
    exit_wait=1,
    seed=None
)


class _RANDNX(RANDNX):
    """Random entry and exit signal generator based on the number of signals.

    Generates `entries` and `exits` based on `vectorbt.signals.nb.rand_enex_apply_nb`.

    See `RAND` for notes on parameters.

    Usage:
        * Test three different entry and exit counts:

        ```pycon
        >>> import vectorbt as vbt

        >>> randnx = vbt.RANDNX.run(
        ...     input_shape=(6,),
        ...     n=[1, 2, 3],
        ...     seed=42)

        >>> randnx.entries
        randnx_n      1      2      3
        0          True   True   True
        1         False  False  False
        2         False   True   True
        3         False  False  False
        4         False  False   True
        5         False  False  False

        >>> randnx.exits
        randnx_n      1      2      3
        0         False  False  False
        1          True   True   True
        2         False  False  False
        3         False   True   True
        4         False  False  False
        5         False  False   True
        ```
    """
    pass


setattr(RANDNX, '__doc__', _RANDNX.__doc__)

# ############# RPROB ############# #

RPROB = SignalFactory(
    class_name='RPROB',
    module_name=__name__,
    short_name='rprob',
    mode='entries',
    param_names=['prob']
).from_choice_func(
    entry_choice_func=rand_by_prob_choice_nb,
    entry_settings=dict(
        pass_params=['prob'],
        pass_kwargs=['pick_first', 'temp_idx_arr', 'flex_2d']
    ),
    pass_flex_2d=True,
    param_settings=dict(
        prob=flex_elem_param_config,
    ),
    seed=None
)


class _RPROB(RPROB):
    """Random entry signal generator based on probabilities.

    Generates `entries` based on `vectorbt.signals.nb.rand_by_prob_choice_nb`.

    !!! hint
        All parameters can be either a single value (per frame) or a NumPy array (per row, column,
        or element). To generate multiple combinations, pass them as lists.

    Usage:
        * Generate three columns with different entry probabilities:

        ```pycon
        >>> import vectorbt as vbt

        >>> rprob = vbt.RPROB.run(input_shape=(5,), prob=[0., 0.5, 1.], seed=42)

        >>> rprob.entries
        rprob_prob    0.0    0.5   1.0
        0           False   True  True
        1           False   True  True
        2           False  False  True
        3           False  False  True
        4           False  False  True
        ```

        * Probability can also be set per row, column, or element:

        ```pycon
        >>> import numpy as np

        >>> rprob = vbt.RPROB.run(input_shape=(5,), prob=np.array([0., 0., 1., 1., 1.]), seed=42)

        >>> rprob.entries
        0    False
        1    False
        2     True
        3     True
        4     True
        Name: array_0, dtype: bool
        ```
    """
    pass


setattr(RPROB, '__doc__', _RPROB.__doc__)

rprobx_config = Config(
    dict(
        class_name='RPROBX',
        module_name=__name__,
        short_name='rprobx',
        mode='exits',
        param_names=['prob']
    )
)
"""Factory config for `RPROBX`."""

rprobx_func_config = Config(
    dict(
        exit_choice_func=rand_by_prob_choice_nb,
        exit_settings=dict(
            pass_params=['prob'],
            pass_kwargs=['pick_first', 'temp_idx_arr', 'flex_2d']
        ),
        pass_flex_2d=True,
        param_settings=dict(
            prob=flex_elem_param_config
        ),
        seed=None
    )
)
"""Exit function config for `RPROBX`."""

RPROBX = SignalFactory(
    **rprobx_config
).from_choice_func(
    **rprobx_func_config
)


class _RPROBX(RPROBX):
    """Random exit signal generator based on probabilities.

    Generates `exits` based on `entries` and `vectorbt.signals.nb.rand_by_prob_choice_nb`.

    See `RPROB` for notes on parameters."""
    pass


setattr(RPROBX, '__doc__', _RPROBX.__doc__)

RPROBCX = SignalFactory(
    **rprobx_config.merge_with(
        dict(
            class_name='RPROBCX',
            short_name='rprobcx',
            mode='chain'
        )
    )
).from_choice_func(
    **rprobx_func_config
)


class _RPROBCX(RPROBCX):
    """Random exit signal generator based on probabilities.

    Generates chain of `new_entries` and `exits` based on `entries` and
    `vectorbt.signals.nb.rand_by_prob_choice_nb`.

    See `RPROB` for notes on parameters."""
    pass


setattr(RPROBCX, '__doc__', _RPROBCX.__doc__)

RPROBNX = SignalFactory(
    class_name='RPROBNX',
    module_name=__name__,
    short_name='rprobnx',
    mode='both',
    param_names=['entry_prob', 'exit_prob']
).from_choice_func(
    entry_choice_func=rand_by_prob_choice_nb,
    entry_settings=dict(
        pass_params=['entry_prob'],
        pass_kwargs=['pick_first', 'temp_idx_arr', 'flex_2d']
    ),
    exit_choice_func=rand_by_prob_choice_nb,
    exit_settings=dict(
        pass_params=['exit_prob'],
        pass_kwargs=['pick_first', 'temp_idx_arr', 'flex_2d']
    ),
    pass_flex_2d=True,
    param_settings=dict(
        entry_prob=flex_elem_param_config,
        exit_prob=flex_elem_param_config
    ),
    seed=None
)


class _RPROBNX(RPROBNX):
    """Random entry and exit signal generator based on probabilities.

    Generates `entries` and `exits` based on `vectorbt.signals.nb.rand_by_prob_choice_nb`.

    See `RPROB` for notes on parameters.

    Usage:
        * Test all probability combinations:

        ```pycon
        >>> import vectorbt as vbt

        >>> rprobnx = vbt.RPROBNX.run(
        ...     input_shape=(5,),
        ...     entry_prob=[0.5, 1.],
        ...     exit_prob=[0.5, 1.],
        ...     param_product=True,
        ...     seed=42)

        >>> rprobnx.entries
        rprobnx_entry_prob    0.5    0.5    1.0    0.5
        rprobnx_exit_prob     0.5    1.0    0.5    1.0
        0                    True   True   True   True
        1                   False  False  False  False
        2                   False  False  False   True
        3                   False  False  False  False
        4                   False  False   True   True

        >>> rprobnx.exits
        rprobnx_entry_prob    0.5    0.5    1.0    1.0
        rprobnx_exit_prob     0.5    1.0    0.5    1.0
        0                   False  False  False  False
        1                   False   True  False   True
        2                   False  False  False  False
        3                   False  False   True   True
        4                    True  False  False  False
        ```

        * Probabilities can also be set per row, column, or element:

        ```pycon
        >>> import numpy as np

        >>> entry_prob1 = np.asarray([1., 0., 1., 0., 1.])
        >>> entry_prob2 = np.asarray([0., 1., 0., 1., 0.])
        >>> rprobnx = vbt.RPROBNX.run(
        ...     input_shape=(5,),
        ...     entry_prob=[entry_prob1, entry_prob2],
        ...     exit_prob=1.,
        ...     seed=42)

        >>> rprobnx.entries
        rprobnx_entry_prob array_0 array_1
        rprobnx_exit_prob      1.0     1.0
        0                     True   False
        1                    False    True
        2                     True   False
        3                    False    True
        4                     True   False

        >>> rprobnx.exits
        rprobnx_entry_prob array_0 array_1
        rprobnx_exit_prob      1.0     1.0
        0                    False   False
        1                     True   False
        2                    False    True
        3                     True   False
        4                    False    True
        ```
    """
    pass


setattr(RPROBNX, '__doc__', _RPROBNX.__doc__)

# ############# ST ############# #

stx_config = Config(
    dict(
        class_name='STX',
        module_name=__name__,
        short_name='stx',
        mode='exits',
        input_names=['ts'],
        param_names=['stop', 'trailing']
    )
)
"""Factory config for `STX`."""

stx_func_config = Config(
    dict(
        exit_choice_func=stop_choice_nb,
        exit_settings=dict(
            pass_inputs=['ts'],
            pass_params=['stop', 'trailing'],
            pass_kwargs=['wait', 'pick_first', 'temp_idx_arr', 'flex_2d']
        ),
        pass_flex_2d=True,
        param_settings=dict(
            stop=flex_elem_param_config,
            trailing=flex_elem_param_config
        ),
        trailing=False
    )
)
"""Exit function config for `STX`."""

STX = SignalFactory(
    **stx_config
).from_choice_func(
    **stx_func_config
)


class _STX(STX):
    """Exit signal generator based on stop values.

    Generates `exits` based on `entries` and `vectorbt.signals.nb.stop_choice_nb`.

    !!! hint
        All parameters can be either a single value (per frame) or a NumPy array (per row, column,
        or element). To generate multiple combinations, pass them as lists."""
    pass


setattr(STX, '__doc__', _STX.__doc__)

STCX = SignalFactory(
    **stx_config.merge_with(
        dict(
            class_name='STCX',
            short_name='stcx',
            mode='chain'
        )
    )
).from_choice_func(
    **stx_func_config
)


class _STCX(STCX):
    """Exit signal generator based on stop values.

    Generates chain of `new_entries` and `exits` based on `entries` and
    `vectorbt.signals.nb.stop_choice_nb`.

    See `STX` for notes on parameters."""
    pass


setattr(STCX, '__doc__', _STCX.__doc__)

# ############# OHLCST ############# #

ohlcstx_config = Config(
    dict(
        class_name='OHLCSTX',
        module_name=__name__,
        short_name='ohlcstx',
        mode='exits',
        input_names=['open', 'high', 'low', 'close'],
        in_output_names=['stop_price', 'stop_type'],
        param_names=['sl_stop', 'sl_trail', 'tp_stop', 'reverse'],
        attr_settings=dict(
            stop_type=dict(dtype=StopType)  # creates rand_type_readable
        )
    )
)
"""Factory config for `OHLCSTX`."""

ohlcstx_func_config = Config(
    dict(
        exit_choice_func=ohlc_stop_choice_nb,
        exit_settings=dict(
            pass_inputs=['open', 'high', 'low', 'close'],  # do not pass entries
            pass_in_outputs=['stop_price', 'stop_type'],
            pass_params=['sl_stop', 'sl_trail', 'tp_stop', 'reverse'],
            pass_kwargs=[('is_open_safe', True), 'wait', 'pick_first', 'temp_idx_arr', 'flex_2d'],
        ),
        pass_flex_2d=True,
        in_output_settings=dict(
            stop_price=dict(
                dtype=np.float64
            ),
            stop_type=dict(
                dtype=np.int64
            )
        ),
        param_settings=dict(
            sl_stop=flex_elem_param_config,
            sl_trail=flex_elem_param_config,
            tp_stop=flex_elem_param_config,
            reverse=flex_elem_param_config
        ),
        sl_stop=np.nan,
        sl_trail=False,
        tp_stop=np.nan,
        reverse=False,
        stop_price=np.nan,
        stop_type=-1
    )
)
"""Exit function config for `OHLCSTX`."""

OHLCSTX = SignalFactory(
    **ohlcstx_config
).from_choice_func(
    **ohlcstx_func_config
)


def _bind_ohlcstx_plot(base_cls: type, entries_attr: str) -> tp.Callable:  # pragma: no cover

    base_cls_plot = base_cls.plot

    def plot(self,
             plot_type: tp.Union[None, str, tp.BaseTraceType] = None,
             ohlc_kwargs: tp.KwargsLike = None,
             entry_trace_kwargs: tp.KwargsLike = None,
             exit_trace_kwargs: tp.KwargsLike = None,
             add_trace_kwargs: tp.KwargsLike = None,
             fig: tp.Optional[tp.BaseFigure] = None,
             _base_cls_plot: tp.Callable = base_cls_plot,
             **layout_kwargs) -> tp.BaseFigure:  # pragma: no cover
        from vectorbt._settings import settings
        ohlcv_cfg = settings['ohlcv']
        plotting_cfg = settings['plotting']

        if self.wrapper.ndim > 1:
            raise TypeError("Select a column first. Use indexing.")

        if ohlc_kwargs is None:
            ohlc_kwargs = {}
        if add_trace_kwargs is None:
            add_trace_kwargs = {}

        if fig is None:
            fig = make_figure()
            fig.update_layout(
                showlegend=True,
                xaxis_rangeslider_visible=False,
                xaxis_showgrid=True,
                yaxis_showgrid=True
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
        fig.add_trace(ohlc, **add_trace_kwargs)

        # Plot entry and exit markers
        _base_cls_plot(
            self,
            entry_y=self.open,
            exit_y=self.stop_price,
            exit_types=self.stop_type_readable,
            entry_trace_kwargs=entry_trace_kwargs,
            exit_trace_kwargs=exit_trace_kwargs,
            add_trace_kwargs=add_trace_kwargs,
            fig=fig
        )
        return fig

    plot.__doc__ = """Plot OHLC, `{0}.{1}` and `{0}.exits`.
    
    Args:
        plot_type: Either 'OHLC', 'Candlestick' or Plotly trace.
        ohlc_kwargs (dict): Keyword arguments passed to `plot_type`.
        entry_trace_kwargs (dict): Keyword arguments passed to \
        `vectorbt.signals.accessors.SignalsSRAccessor.plot_as_entry_markers` for `{0}.{1}`.
        exit_trace_kwargs (dict): Keyword arguments passed to \
        `vectorbt.signals.accessors.SignalsSRAccessor.plot_as_exit_markers` for `{0}.exits`.
        fig (Figure or FigureWidget): Figure to add traces to.
        **layout_kwargs: Keyword arguments for layout.""".format(base_cls.__name__, entries_attr)

    if entries_attr == 'entries':
        plot.__doc__ += """
    Usage:
        ```pycon
        >>> ohlcstx.iloc[:, 0].plot()
        ```
        
        ![](/assets/images/OHLCSTX.svg)
    """
    return plot


class _OHLCSTX(OHLCSTX):
    """Exit signal generator based on OHLC and stop values.

    Generates `exits` based on `entries` and `vectorbt.signals.nb.ohlc_stop_choice_nb`.

    !!! hint
        All parameters can be either a single value (per frame) or a NumPy array (per row, column,
        or element). To generate multiple combinations, pass them as lists.

    Usage:
        * Test each stop type:

        ```pycon
        >>> import vectorbt as vbt
        >>> import pandas as pd
        >>> import numpy as np

        >>> entries = pd.Series([True, False, False, False, False, False])
        >>> price = pd.DataFrame({
        ...     'open': [10, 11, 12, 11, 10, 9],
        ...     'high': [11, 12, 13, 12, 11, 10],
        ...     'low': [9, 10, 11, 10, 9, 8],
        ...     'close': [10, 11, 12, 11, 10, 9]
        ... })
        >>> ohlcstx = vbt.OHLCSTX.run(
        ...     entries,
        ...     price['open'], price['high'], price['low'], price['close'],
        ...     sl_stop=[0.1, 0.1, np.nan],
        ...     sl_trail=[False, True, False],
        ...     tp_stop=[np.nan, np.nan, 0.1])

        >>> ohlcstx.entries
        ohlcstx_sl_stop     0.1    0.1    NaN
        ohlcstx_sl_trail  False   True  False
        ohlcstx_tp_stop     NaN    NaN    0.1
        0                  True   True   True
        1                 False  False  False
        2                 False  False  False
        3                 False  False  False
        4                 False  False  False
        5                 False  False  False

        >>> ohlcstx.exits
        ohlcstx_sl_stop     0.1    0.1    NaN
        ohlcstx_sl_trail  False   True  False
        ohlcstx_tp_stop     NaN    NaN    0.1
        0                 False  False  False
        1                 False  False   True
        2                 False  False  False
        3                 False   True  False
        4                  True  False  False
        5                 False  False  False

        >>> ohlcstx.stop_price
        ohlcstx_sl_stop     0.1    0.1    NaN
        ohlcstx_sl_trail  False   True  False
        ohlcstx_tp_stop     NaN    NaN    0.1
        0                   NaN    NaN    NaN
        1                   NaN    NaN   11.0
        2                   NaN    NaN    NaN
        3                   NaN   11.7    NaN
        4                   9.0    NaN    NaN
        5                   NaN    NaN    NaN

        >>> ohlcstx.stop_type_readable
        ohlcstx_sl_stop        0.1        0.1         NaN
        ohlcstx_sl_trail     False       True       False
        ohlcstx_tp_stop        NaN        NaN         0.1
        0                     None       None        None
        1                     None       None  TakeProfit
        2                     None       None        None
        3                     None  TrailStop        None
        4                 StopLoss       None        None
        5                     None       None        None
        ```
    """

    plot = _bind_ohlcstx_plot(OHLCSTX, 'entries')


setattr(OHLCSTX, '__doc__', _OHLCSTX.__doc__)
setattr(OHLCSTX, 'plot', _OHLCSTX.plot)

OHLCSTCX = SignalFactory(
    **ohlcstx_config.merge_with(
        dict(
            class_name='OHLCSTCX',
            short_name='ohlcstcx',
            mode='chain'
        )
    )
).from_choice_func(
    **ohlcstx_func_config
)


class _OHLCSTCX(OHLCSTCX):
    """Exit signal generator based on OHLC and stop values.

    Generates chain of `new_entries` and `exits` based on `entries` and
    `vectorbt.signals.nb.ohlc_stop_choice_nb`.

    See `OHLCSTX` for notes on parameters."""

    plot = _bind_ohlcstx_plot(OHLCSTCX, 'new_entries')


setattr(OHLCSTCX, '__doc__', _OHLCSTCX.__doc__)
setattr(OHLCSTCX, 'plot', _OHLCSTCX.plot)
