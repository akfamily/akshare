# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""A factory for building new signal generators with ease.

The signal factory class `SignalFactory` extends `vectorbt.indicators.factory.IndicatorFactory`
to offer a convenient way to create signal generators of any complexity. By providing it with information
such as entry and exit functions and the names of inputs, parameters, and outputs, it will create a
stand-alone class capable of generating signals for an arbitrary combination of inputs and parameters.
"""

import inspect

import numpy as np
from numba import njit

from vectorbt import _typing as tp
from vectorbt.base import combine_fns
from vectorbt.indicators.factory import IndicatorFactory, IndicatorBase, CacheOutputT
from vectorbt.signals.enums import FactoryMode
from vectorbt.signals.nb import (
    generate_nb,
    generate_ex_nb,
    generate_enex_nb,
    first_choice_nb
)
from vectorbt.utils import checks
from vectorbt.utils.config import merge_dicts
from vectorbt.utils.enum_ import map_enum_fields
from vectorbt.utils.params import to_typed_list


class SignalFactory(IndicatorFactory):
    """A factory for building signal generators.

    Extends `vectorbt.indicators.factory.IndicatorFactory` with choice functions.

    Generates a fixed number of outputs (depending upon `mode`).
    If you need to generate other outputs, use in-place outputs (via `in_output_names`).

    See `vectorbt.signals.enums.FactoryMode` for supported generation modes.

    Other arguments are passed to `vectorbt.indicators.factory.IndicatorFactory`.
    ```"""

    def __init__(self,
                 *args,
                 mode: tp.Union[str, int] = FactoryMode.Both,
                 input_names: tp.Optional[tp.Sequence[str]] = None,
                 attr_settings: tp.KwargsLike = None,
                 **kwargs) -> None:
        mode = map_enum_fields(mode, FactoryMode)
        if input_names is None:
            input_names = []
        else:
            input_names = list(input_names)
        if attr_settings is None:
            attr_settings = {}

        if 'entries' in input_names:
            raise ValueError("entries cannot be used in input_names")
        if 'exits' in input_names:
            raise ValueError("exits cannot be used in input_names")
        if mode == FactoryMode.Entries:
            output_names = ['entries']
        elif mode == FactoryMode.Exits:
            input_names = ['entries'] + input_names
            output_names = ['exits']
        elif mode == FactoryMode.Both:
            output_names = ['entries', 'exits']
        else:
            input_names = ['entries'] + input_names
            output_names = ['new_entries', 'exits']
        if 'entries' in input_names:
            attr_settings['entries'] = dict(dtype=np.bool_)
        for output_name in output_names:
            attr_settings[output_name] = dict(dtype=np.bool_)

        IndicatorFactory.__init__(
            self,
            *args,
            input_names=input_names,
            output_names=output_names,
            attr_settings=attr_settings,
            **kwargs
        )
        self.mode = mode

        def plot(_self,
                 entry_y: tp.Optional[tp.ArrayLike] = None,
                 exit_y: tp.Optional[tp.ArrayLike] = None,
                 entry_types: tp.Optional[tp.ArrayLikeSequence] = None,
                 exit_types: tp.Optional[tp.ArrayLikeSequence] = None,
                 entry_trace_kwargs: tp.KwargsLike = None,
                 exit_trace_kwargs: tp.KwargsLike = None,
                 fig: tp.Optional[tp.BaseFigure] = None,
                 **kwargs) -> tp.BaseFigure:  # pragma: no cover
            if _self.wrapper.ndim > 1:
                raise TypeError("Select a column first. Use indexing.")

            if entry_trace_kwargs is None:
                entry_trace_kwargs = {}
            if exit_trace_kwargs is None:
                exit_trace_kwargs = {}
            entry_trace_kwargs = merge_dicts(
                dict(name="New Entry" if mode == FactoryMode.Chain else "Entry"),
                entry_trace_kwargs
            )
            exit_trace_kwargs = merge_dicts(
                dict(name="Exit"),
                exit_trace_kwargs
            )
            if entry_types is not None:
                entry_types = np.asarray(entry_types)
                entry_trace_kwargs = merge_dicts(dict(
                    customdata=entry_types,
                    hovertemplate="(%{x}, %{y})<br>Type: %{customdata}"
                ), entry_trace_kwargs)
            if exit_types is not None:
                exit_types = np.asarray(exit_types)
                exit_trace_kwargs = merge_dicts(dict(
                    customdata=exit_types,
                    hovertemplate="(%{x}, %{y})<br>Type: %{customdata}"
                ), exit_trace_kwargs)
            if mode == FactoryMode.Entries:
                fig = _self.entries.vbt.signals.plot_as_entry_markers(
                    y=entry_y, trace_kwargs=entry_trace_kwargs, fig=fig, **kwargs)
            elif mode == FactoryMode.Exits:
                fig = _self.entries.vbt.signals.plot_as_entry_markers(
                    y=entry_y, trace_kwargs=entry_trace_kwargs, fig=fig, **kwargs)
                fig = _self.exits.vbt.signals.plot_as_exit_markers(
                    y=exit_y, trace_kwargs=exit_trace_kwargs, fig=fig, **kwargs)
            elif mode == FactoryMode.Both:
                fig = _self.entries.vbt.signals.plot_as_entry_markers(
                    y=entry_y, trace_kwargs=entry_trace_kwargs, fig=fig, **kwargs)
                fig = _self.exits.vbt.signals.plot_as_exit_markers(
                    y=exit_y, trace_kwargs=exit_trace_kwargs, fig=fig, **kwargs)
            else:
                fig = _self.new_entries.vbt.signals.plot_as_entry_markers(
                    y=entry_y, trace_kwargs=entry_trace_kwargs, fig=fig, **kwargs)
                fig = _self.exits.vbt.signals.plot_as_exit_markers(
                    y=exit_y, trace_kwargs=exit_trace_kwargs, fig=fig, **kwargs)

            return fig

        plot.__doc__ = """Plot `{0}.{1}` and `{0}.exits`.

        Args:
            entry_y (array_like): Y-axis values to plot entry markers on.
            exit_y (array_like): Y-axis values to plot exit markers on.
            entry_types (array_like): Entry types in string format.
            exit_types (array_like): Exit types in string format.
            entry_trace_kwargs (dict): Keyword arguments passed to \
            `vectorbt.signals.accessors.SignalsSRAccessor.plot_as_entry_markers` for `{0}.{1}`.
            exit_trace_kwargs (dict): Keyword arguments passed to \
            `vectorbt.signals.accessors.SignalsSRAccessor.plot_as_exit_markers` for `{0}.exits`.
            fig (Figure or FigureWidget): Figure to add traces to.
            **kwargs: Keyword arguments passed to `vectorbt.signals.accessors.SignalsSRAccessor.plot_as_markers`.
        """.format(
            self.class_name, 'new_entries' if mode == FactoryMode.Chain else 'entries'
        )

        setattr(self.Indicator, 'plot', plot)

    def from_choice_func(
            self,
            entry_choice_func: tp.Optional[tp.ChoiceFunc] = None,
            exit_choice_func: tp.Optional[tp.ChoiceFunc] = None,
            generate_func: tp.Callable = generate_nb,
            generate_ex_func: tp.Callable = generate_ex_nb,
            generate_enex_func: tp.Callable = generate_enex_nb,
            cache_func: tp.Callable = None,
            entry_settings: tp.KwargsLike = None,
            exit_settings: tp.KwargsLike = None,
            cache_settings: tp.KwargsLike = None,
            numba_loop: bool = False,
            **kwargs) -> tp.Type[IndicatorBase]:
        """Build signal generator class around entry and exit choice functions.

        A choice function is simply a function that returns indices of signals.
        There are two types of it: entry choice function and exit choice function.
        Each choice function takes broadcast time series, broadcast in-place output time series,
        broadcast parameter arrays, and other arguments, and returns an array of indices
        corresponding to chosen signals. See `vectorbt.signals.nb.generate_nb`.

        Args:
            entry_choice_func (callable): `choice_func_nb` that returns indices of entries.

                Defaults to `vectorbt.signals.nb.first_choice_nb` for `FactoryMode.Chain`.
            exit_choice_func (callable): `choice_func_nb` that returns indices of exits.
            generate_func (callable): Entry generation function.

                Defaults to `vectorbt.signals.nb.generate_nb`.
            generate_ex_func (callable): Exit generation function.

                Defaults to `vectorbt.signals.nb.generate_ex_nb`.
            generate_enex_func (callable): Entry and exit generation function.

                Defaults to `vectorbt.signals.nb.generate_enex_nb`.
            cache_func (callable): A caching function to preprocess data beforehand.

                All returned objects will be passed as last arguments to choice functions.
            entry_settings (dict): Settings dict for `entry_choice_func`.
            exit_settings (dict): Settings dict for `exit_choice_func`.
            cache_settings (dict): Settings dict for `cache_func`.
            numba_loop (bool): Whether to loop using Numba.

                Set to True when iterating large number of times over small input.
            **kwargs: Keyword arguments passed to `IndicatorFactory.from_custom_func`.

        !!! note
            Choice functions should be Numba-compiled.

            Which inputs, parameters and arguments to pass to each function should be
            explicitly indicated in the function's settings dict. By default, nothing is passed.

            Passing keyword arguments directly to the choice functions is not supported.
            Use `pass_kwargs` in a settings dict to pass keyword arguments as positional.

        Settings dict of each function can have the following keys:

        Attributes:
            pass_inputs (list of str): Input names to pass to the choice function.

                Defaults to []. Order matters. Each name must be in `input_names`.
            pass_in_outputs (list of str): In-place output names to pass to the choice function.

                Defaults to []. Order matters. Each name must be in `in_output_names`.
            pass_params (list of str): Parameter names to pass to the choice function.

                Defaults to []. Order matters. Each name must be in `param_names`.
            pass_kwargs (dict, list of str or list of tuple): Keyword arguments from `kwargs` dict to
                pass as positional arguments to the choice function.

                Defaults to []. Order matters.

                If any element is a tuple, should contain the name and the default value.
                If any element is a string, the default value is None.

                Built-in keys include:

                * `input_shape`: Input shape if no input time series passed.
                    Default is provided by the pipeline if `pass_input_shape` is True.
                * `wait`: Number of ticks to wait before placing signals.
                    Default is 1.
                * `until_next`: Whether to place signals up to the next entry signal.
                    Default is True.

                    Applied in `generate_ex_func` only.
                * `skip_until_exit`: Whether to skip processing entry signals until the next exit.
                    Default is False.

                    Applied in `generate_ex_func` only.
                * `pick_first`: Whether to stop as soon as the first exit signal is found.
                    Default is False with `FactoryMode.Entries`, otherwise is True.
                * `temp_idx_arr`: Empty integer array used to temporarily store indices.
                    Default is an automatically generated array of shape `input_shape[0]`.

                    You can also pass `temp_idx_arr1`, `temp_idx_arr2`, etc. to generate multiple.
                * `flex_2d`: See `vectorbt.base.reshape_fns.flex_select_auto_nb`.
                    Default is provided by the pipeline if `pass_flex_2d` is True.
            pass_cache (bool): Whether to pass cache from `cache_func` to the choice function.

                Defaults to False. Cache is passed unpacked.

        The following arguments can be passed to `run` and `run_combs` methods:

        Args:
            *args: Should be used instead of `entry_args` with `FactoryMode.Entries` and instead of
                `exit_args` with `FactoryMode.Exits` and `FactoryMode.Chain` with default `entry_choice_func`.
            entry_args (tuple): Arguments passed to the entry choice function.
            exit_args (tuple): Arguments passed to the exit choice function.
            cache_args (tuple): Arguments passed to the cache function.
            entry_kwargs (tuple): Settings for the entry choice function. Also contains arguments
                passed as positional if in `pass_kwargs`.
            exit_kwargs (tuple): Settings for the exit choice function. Also contains arguments
                passed as positional if in `pass_kwargs`.
            cache_kwargs (tuple): Settings for the cache function. Also contains arguments
                passed as positional if in `pass_kwargs`.
            return_cache (bool): Whether to return only cache.
            use_cache (any): Cache to use.
            **kwargs: Should be used instead of `entry_kwargs` with `FactoryMode.Entries` and instead of
                `exit_kwargs` with `FactoryMode.Exits` and `FactoryMode.Chain` with default `entry_choice_func`.

        For more arguments, see `vectorbt.indicators.factory.run_pipeline`.

        Usage:
            * The simplest signal indicator that places True at the very first index:

            ```pycon
            >>> from numba import njit
            >>> import vectorbt as vbt
            >>> import numpy as np

            >>> @njit
            ... def entry_choice_func(from_i, to_i, col):
            ...     return np.array([from_i])

            >>> @njit
            ... def exit_choice_func(from_i, to_i, col):
            ...     return np.array([from_i])

            >>> MySignals = vbt.SignalFactory().from_choice_func(
            ...     entry_choice_func=entry_choice_func,
            ...     exit_choice_func=exit_choice_func,
            ...     entry_kwargs=dict(wait=1),
            ...     exit_kwargs=dict(wait=1)
            ... )

            >>> my_sig = MySignals.run(input_shape=(3, 3))
            >>> my_sig.entries
                   0      1      2
            0   True   True   True
            1  False  False  False
            2   True   True   True
            >>> my_sig.exits
                   0      1      2
            0  False  False  False
            1   True   True   True
            2  False  False  False
            ```

            * Take the first entry and place an exit after waiting `n` ticks. Find the next entry and repeat.
            Test three different `n` values.

            ```pycon
            >>> from numba import njit
            >>> from vectorbt.signals.factory import SignalFactory

            >>> @njit
            ... def wait_choice_nb(from_i, to_i, col, n, temp_idx_arr):
            ...     temp_idx_arr[0] = from_i + n  # index of next exit
            ...     if temp_idx_arr[0] < to_i:
            ...         return temp_idx_arr[:1]
            ...     return temp_idx_arr[:0]  # must return array anyway

            >>> # Build signal generator
            >>> MySignals = SignalFactory(
            ...     mode='chain',
            ...     param_names=['n']
            ... ).from_choice_func(
            ...     exit_choice_func=wait_choice_nb,
            ...     exit_settings=dict(
            ...         pass_params=['n'],
            ...         pass_kwargs=['temp_idx_arr']  # built-in kwarg
            ...     )
            ... )

            >>> # Run signal generator
            >>> entries = [True, True, True, True, True]
            >>> my_sig = MySignals.run(entries, [0, 1, 2])

            >>> my_sig.entries  # input entries
            custom_n     0     1     2
            0         True  True  True
            1         True  True  True
            2         True  True  True
            3         True  True  True
            4         True  True  True

            >>> my_sig.new_entries  # output entries
            custom_n      0      1      2
            0          True   True   True
            1         False  False  False
            2          True  False  False
            3         False   True  False
            4          True  False   True

            >>> my_sig.exits  # output exits
            custom_n      0      1      2
            0         False  False  False
            1          True  False  False
            2         False   True  False
            3          True  False   True
            4         False  False  False
            ```

            * To combine multiple iterative signals, you would need to create a custom choice function.
            Here is an example of combining two random generators using "OR" rule (the first signal wins):

            ```pycon
            >>> from numba import njit
            >>> from collections import namedtuple
            >>> from vectorbt.indicators.configs import flex_elem_param_config
            >>> from vectorbt.signals.factory import SignalFactory
            >>> from vectorbt.signals.nb import rand_by_prob_choice_nb

            >>> # Enum to distinguish random generators
            >>> RandType = namedtuple('RandType', ['R1', 'R2'])(0, 1)

            >>> # Define exit choice function
            >>> @njit
            ... def rand_exit_choice_nb(from_i, to_i, col, rand_type, prob1,
            ...                         prob2, temp_idx_arr1, temp_idx_arr2, flex_2d):
            ...     idxs1 = rand_by_prob_choice_nb(from_i, to_i, col, prob1, True, temp_idx_arr1, flex_2d)
            ...     if len(idxs1) > 0:
            ...         to_i = idxs1[0]  # no need to go beyond first the first found signal
            ...     idxs2 = rand_by_prob_choice_nb(from_i, to_i, col, prob2, True, temp_idx_arr2, flex_2d)
            ...     if len(idxs2) > 0:
            ...         rand_type[idxs2[0], col] = RandType.R2
            ...         return idxs2
            ...     if len(idxs1) > 0:
            ...         rand_type[idxs1[0], col] = RandType.R1
            ...         return idxs1
            ...     return temp_idx_arr1[:0]

            >>> # Build signal generator
            >>> MySignals = SignalFactory(
            ...     mode='chain',
            ...     in_output_names=['rand_type'],
            ...     param_names=['prob1', 'prob2'],
            ...     attr_settings=dict(
            ...         rand_type=dict(dtype=RandType)  # creates rand_type_readable
            ...     )
            ... ).from_choice_func(
            ...     exit_choice_func=rand_exit_choice_nb,
            ...     exit_settings=dict(
            ...         pass_in_outputs=['rand_type'],
            ...         pass_params=['prob1', 'prob2'],
            ...         pass_kwargs=['temp_idx_arr1', 'temp_idx_arr2', 'flex_2d']
            ...     ),
            ...     param_settings=dict(
            ...         prob1=flex_elem_param_config,  # param per frame/row/col/element
            ...         prob2=flex_elem_param_config
            ...     ),
            ...     pass_flex_2d=True,
            ...     rand_type=-1  # fill with this value
            ... )

            >>> # Run signal generator
            >>> entries = [True, True, True, True, True]
            >>> my_sig = MySignals.run(entries, [0., 1.], [0., 1.], param_product=True)

            >>> my_sig.new_entries
            custom_prob1           0.0           1.0
            custom_prob2    0.0    1.0    0.0    1.0
            0              True   True   True   True
            1             False  False  False  False
            2             False   True   True   True
            3             False  False  False  False
            4             False   True   True   True

            >>> my_sig.exits
            custom_prob1           0.0           1.0
            custom_prob2    0.0    1.0    0.0    1.0
            0             False  False  False  False
            1             False   True   True   True
            2             False  False  False  False
            3             False   True   True   True
            4             False  False  False  False

            >>> my_sig.rand_type_readable
            custom_prob1     0.0     1.0
            custom_prob2 0.0 1.0 0.0 1.0
            0
            1                 R2  R1  R1
            2
            3                 R2  R1  R1
            4
            ```
        """

        mode = self.mode
        input_names = self.input_names
        param_names = self.param_names
        in_output_names = self.in_output_names

        if mode == FactoryMode.Entries:
            require_input_shape = True
            checks.assert_not_none(entry_choice_func)
            checks.assert_numba_func(entry_choice_func)
            if exit_choice_func is not None:
                raise ValueError("exit_choice_func cannot be used with FactoryMode.Entries")
        elif mode == FactoryMode.Exits:
            require_input_shape = False
            if entry_choice_func is not None:
                raise ValueError("entry_choice_func cannot be used with FactoryMode.Exits")
            checks.assert_not_none(exit_choice_func)
            checks.assert_numba_func(exit_choice_func)
        elif mode == FactoryMode.Both:
            require_input_shape = True
            checks.assert_not_none(entry_choice_func)
            checks.assert_numba_func(entry_choice_func)
            checks.assert_not_none(exit_choice_func)
            checks.assert_numba_func(exit_choice_func)
        else:
            require_input_shape = False
            if entry_choice_func is None:
                entry_choice_func = first_choice_nb
            if entry_settings is None:
                entry_settings = {}
            entry_settings = merge_dicts(dict(
                pass_inputs=['entries']
            ), entry_settings)
            checks.assert_not_none(entry_choice_func)
            checks.assert_numba_func(entry_choice_func)
            checks.assert_not_none(exit_choice_func)
            checks.assert_numba_func(exit_choice_func)
        require_input_shape = kwargs.pop('require_input_shape', require_input_shape)

        if entry_settings is None:
            entry_settings = {}
        if exit_settings is None:
            exit_settings = {}
        if cache_settings is None:
            cache_settings = {}

        valid_keys = [
            'pass_inputs',
            'pass_in_outputs',
            'pass_params',
            'pass_kwargs',
            'pass_cache'
        ]
        checks.assert_dict_valid(entry_settings, valid_keys)
        checks.assert_dict_valid(exit_settings, valid_keys)
        checks.assert_dict_valid(cache_settings, valid_keys)

        # Get input names for each function
        def _get_func_names(func_settings: tp.Kwargs, setting: str, all_names: tp.Sequence[str]) -> tp.List[str]:
            func_input_names = func_settings.get(setting, None)
            if func_input_names is None:
                return []
            else:
                for name in func_input_names:
                    checks.assert_in(name, all_names)
            return func_input_names

        entry_input_names = _get_func_names(entry_settings, 'pass_inputs', input_names)
        exit_input_names = _get_func_names(exit_settings, 'pass_inputs', input_names)
        cache_input_names = _get_func_names(cache_settings, 'pass_inputs', input_names)

        entry_in_output_names = _get_func_names(entry_settings, 'pass_in_outputs', in_output_names)
        exit_in_output_names = _get_func_names(exit_settings, 'pass_in_outputs', in_output_names)
        cache_in_output_names = _get_func_names(cache_settings, 'pass_in_outputs', in_output_names)

        entry_param_names = _get_func_names(entry_settings, 'pass_params', param_names)
        exit_param_names = _get_func_names(exit_settings, 'pass_params', param_names)
        cache_param_names = _get_func_names(cache_settings, 'pass_params', param_names)

        # Build a function that selects a parameter tuple
        if mode == FactoryMode.Entries:
            _0 = "i"
            _0 += ", shape"
            _0 += ", entry_pick_first"
            _0 += ", entry_input_tuple"
            if len(entry_in_output_names) > 0:
                _0 += ", entry_in_output_tuples"
            if len(entry_param_names) > 0:
                _0 += ", entry_param_tuples"
            _0 += ", entry_args"
            _1 = "shape"
            _1 += ", entry_pick_first"
            _1 += ", entry_choice_func"
            _1 += ", *entry_input_tuple"
            if len(entry_in_output_names) > 0:
                _1 += ", *entry_in_output_tuples[i]"
            if len(entry_param_names) > 0:
                _1 += ", *entry_param_tuples[i]"
            _1 += ", *entry_args"
            func_str = "def apply_func({0}):\n   return generate_func({1})".format(_0, _1)
            scope = {
                'generate_func': generate_func,
                'entry_choice_func': entry_choice_func
            }
            filename = inspect.getfile(lambda: None)
            code = compile(func_str, filename, 'single')
            exec(code, scope)
            apply_func = scope['apply_func']
            if numba_loop:
                apply_func = njit(apply_func)
                apply_and_concat_func = combine_fns.apply_and_concat_one_nb
            else:
                apply_and_concat_func = combine_fns.apply_and_concat_one

        elif mode == FactoryMode.Exits:
            _0 = "i"
            _0 += ", entries"
            _0 += ", exit_wait"
            _0 += ", until_next"
            _0 += ", skip_until_exit"
            _0 += ", exit_pick_first"
            _0 += ", exit_input_tuple"
            if len(exit_in_output_names) > 0:
                _0 += ", exit_in_output_tuples"
            if len(exit_param_names) > 0:
                _0 += ", exit_param_tuples"
            _0 += ", exit_args"
            _1 = "entries"
            _1 += ", exit_wait"
            _1 += ", until_next"
            _1 += ", skip_until_exit"
            _1 += ", exit_pick_first"
            _1 += ", exit_choice_func"
            _1 += ", *exit_input_tuple"
            if len(exit_in_output_names) > 0:
                _1 += ", *exit_in_output_tuples[i]"
            if len(exit_param_names) > 0:
                _1 += ", *exit_param_tuples[i]"
            _1 += ", *exit_args"
            func_str = "def apply_func({0}):\n   return generate_ex_func({1})".format(_0, _1)
            scope = {
                'generate_ex_func': generate_ex_func,
                'exit_choice_func': exit_choice_func
            }
            filename = inspect.getfile(lambda: None)
            code = compile(func_str, filename, 'single')
            exec(code, scope)
            apply_func = scope['apply_func']
            if numba_loop:
                apply_func = njit(apply_func)
                apply_and_concat_func = combine_fns.apply_and_concat_one_nb
            else:
                apply_and_concat_func = combine_fns.apply_and_concat_one

        else:
            _0 = "i"
            _0 += ", shape"
            _0 += ", entry_wait"
            _0 += ", exit_wait"
            _0 += ", entry_pick_first"
            _0 += ", exit_pick_first"
            _0 += ", entry_input_tuple"
            _0 += ", exit_input_tuple"
            if len(entry_in_output_names) > 0:
                _0 += ", entry_in_output_tuples"
            if len(exit_in_output_names) > 0:
                _0 += ", exit_in_output_tuples"
            if len(entry_param_names) > 0:
                _0 += ", entry_param_tuples"
            if len(exit_param_names) > 0:
                _0 += ", exit_param_tuples"
            _0 += ", entry_args"
            _0 += ", exit_args"
            _1 = "shape"
            _1 += ", entry_wait"
            _1 += ", exit_wait"
            _1 += ", entry_pick_first"
            _1 += ", exit_pick_first"
            _1 += ", entry_choice_func"
            _1 += ", (*entry_input_tuple"
            if len(entry_in_output_names) > 0:
                _1 += ", *entry_in_output_tuples[i]"
            if len(entry_param_names) > 0:
                _1 += ", *entry_param_tuples[i]"
            _1 += ", *entry_args)"
            _1 += ", exit_choice_func"
            _1 += ", (*exit_input_tuple"
            if len(exit_in_output_names) > 0:
                _1 += ", *exit_in_output_tuples[i]"
            if len(exit_param_names) > 0:
                _1 += ", *exit_param_tuples[i]"
            _1 += ", *exit_args)"
            func_str = "def apply_func({0}):\n   return generate_enex_func({1})".format(_0, _1)
            scope = {
                'generate_enex_func': generate_enex_func,
                'entry_choice_func': entry_choice_func,
                'exit_choice_func': exit_choice_func
            }
            filename = inspect.getfile(lambda: None)
            code = compile(func_str, filename, 'single')
            exec(code, scope)
            apply_func = scope['apply_func']
            if numba_loop:
                apply_func = njit(apply_func)
                apply_and_concat_func = combine_fns.apply_and_concat_multiple_nb
            else:
                apply_and_concat_func = combine_fns.apply_and_concat_multiple

        def custom_func(input_list: tp.List[tp.AnyArray],
                        in_output_list: tp.List[tp.List[tp.AnyArray]],
                        param_list: tp.List[tp.List[tp.Param]],
                        *args,
                        input_shape: tp.Optional[tp.Shape] = None,
                        flex_2d: tp.Optional[bool] = None,
                        entry_args: tp.Optional[tp.Args] = None,
                        exit_args: tp.Optional[tp.Args] = None,
                        cache_args: tp.Optional[tp.Args] = None,
                        entry_kwargs: tp.KwargsLike = None,
                        exit_kwargs: tp.KwargsLike = None,
                        cache_kwargs: tp.KwargsLike = None,
                        return_cache: bool = False,
                        use_cache: tp.Optional[CacheOutputT] = None,
                        **_kwargs) -> tp.Union[CacheOutputT, tp.Array2d, tp.List[tp.Array2d]]:
            # Get arguments
            if len(input_list) == 0:
                if input_shape is None:
                    raise ValueError("Pass input_shape if no input time series were passed")
            else:
                input_shape = input_list[0].shape

            if entry_args is None:
                entry_args = ()
            if exit_args is None:
                exit_args = ()
            if cache_args is None:
                cache_args = ()
            if mode == FactoryMode.Entries:
                if len(entry_args) > 0:
                    raise ValueError("Use *args instead of entry_args with FactoryMode.Entries")
                entry_args = args
            elif mode == FactoryMode.Exits or (mode == FactoryMode.Chain and entry_choice_func == first_choice_nb):
                if len(exit_args) > 0:
                    raise ValueError("Use *args instead of exit_args "
                                     "with FactoryMode.Exits or FactoryMode.Chain")
                exit_args = args
            else:
                if len(args) > 0:
                    raise ValueError("*args cannot be used with FactoryMode.Both")

            if entry_kwargs is None:
                entry_kwargs = {}
            if exit_kwargs is None:
                exit_kwargs = {}
            if cache_kwargs is None:
                cache_kwargs = {}
            if mode == FactoryMode.Entries:
                if len(entry_kwargs) > 0:
                    raise ValueError("Use **kwargs instead of entry_kwargs with FactoryMode.Entries")
                entry_kwargs = _kwargs
            elif mode == FactoryMode.Exits or (mode == FactoryMode.Chain and entry_choice_func == first_choice_nb):
                if len(exit_kwargs) > 0:
                    raise ValueError("Use **kwargs instead of exit_kwargs "
                                     "with FactoryMode.Exits or FactoryMode.Chain")
                exit_kwargs = _kwargs
            else:
                if len(_kwargs) > 0:
                    raise ValueError("*args cannot be used with FactoryMode.Both")

            kwargs_defaults = dict(
                input_shape=input_shape,
                wait=1,
                until_next=True,
                skip_until_exit=False,
                pick_first=True,
                flex_2d=flex_2d,
            )
            if mode == FactoryMode.Entries:
                kwargs_defaults['pick_first'] = False
            entry_kwargs = merge_dicts(kwargs_defaults, entry_kwargs)
            exit_kwargs = merge_dicts(kwargs_defaults, exit_kwargs)
            cache_kwargs = merge_dicts(kwargs_defaults, cache_kwargs)
            entry_wait = entry_kwargs['wait']
            exit_wait = exit_kwargs['wait']
            entry_pick_first = entry_kwargs['pick_first']
            exit_pick_first = exit_kwargs['pick_first']
            until_next = exit_kwargs['until_next']
            skip_until_exit = exit_kwargs['skip_until_exit']

            # Distribute arguments across functions
            entry_input_tuple = ()
            exit_input_tuple = ()
            cache_input_tuple = ()
            for input_name in entry_input_names:
                entry_input_tuple += (input_list[input_names.index(input_name)],)
            for input_name in exit_input_names:
                exit_input_tuple += (input_list[input_names.index(input_name)],)
            for input_name in cache_input_names:
                cache_input_tuple += (input_list[input_names.index(input_name)],)

            entry_in_output_list = []
            exit_in_output_list = []
            cache_in_output_list = []
            for in_output_name in entry_in_output_names:
                entry_in_output_list.append(in_output_list[in_output_names.index(in_output_name)])
            for in_output_name in exit_in_output_names:
                exit_in_output_list.append(in_output_list[in_output_names.index(in_output_name)])
            for in_output_name in cache_in_output_names:
                cache_in_output_list.append(in_output_list[in_output_names.index(in_output_name)])

            entry_param_list = []
            exit_param_list = []
            cache_param_list = []
            for param_name in entry_param_names:
                entry_param_list.append(param_list[param_names.index(param_name)])
            for param_name in exit_param_names:
                exit_param_list.append(param_list[param_names.index(param_name)])
            for param_name in cache_param_names:
                cache_param_list.append(param_list[param_names.index(param_name)])

            n_params = len(param_list[0]) if len(param_list) > 0 else 1
            entry_in_output_tuples = list(zip(*entry_in_output_list))
            exit_in_output_tuples = list(zip(*exit_in_output_list))
            entry_param_tuples = list(zip(*entry_param_list))
            exit_param_tuples = list(zip(*exit_param_list))

            def _build_more_args(func_settings: tp.Kwargs, func_kwargs: tp.Kwargs) -> tp.Args:
                pass_kwargs = func_settings.get('pass_kwargs', [])
                if isinstance(pass_kwargs, dict):
                    pass_kwargs = list(pass_kwargs.items())
                more_args = ()
                for key in pass_kwargs:
                    value = None
                    if isinstance(key, tuple):
                        key, value = key
                    else:
                        if key.startswith('temp_idx_arr'):
                            value = np.empty((input_shape[0],), dtype=np.int64)
                    value = func_kwargs.get(key, value)
                    more_args += (value,)
                return more_args

            entry_more_args = _build_more_args(entry_settings, entry_kwargs)
            exit_more_args = _build_more_args(exit_settings, exit_kwargs)
            cache_more_args = _build_more_args(cache_settings, cache_kwargs)

            # Caching
            cache = use_cache
            if cache is None and cache_func is not None:
                _cache_in_output_list = cache_in_output_list
                _cache_param_list = cache_param_list
                if checks.is_numba_func(cache_func):
                    if len(_cache_in_output_list) > 0:
                        _cache_in_output_list = [to_typed_list(in_outputs) for in_outputs in _cache_in_output_list]
                    if len(_cache_param_list) > 0:
                        _cache_param_list = [to_typed_list(params) for params in _cache_param_list]

                cache = cache_func(
                    *cache_input_tuple,
                    *_cache_in_output_list,
                    *_cache_param_list,
                    *cache_args,
                    *cache_more_args
                )
            if return_cache:
                return cache
            if cache is None:
                cache = ()
            if not isinstance(cache, tuple):
                cache = (cache,)

            entry_cache = ()
            exit_cache = ()
            if entry_settings.get('pass_cache', False):
                entry_cache = cache
            if exit_settings.get('pass_cache', False):
                exit_cache = cache

            # Apply and concatenate
            if mode == FactoryMode.Entries:
                if len(entry_in_output_names) > 0:
                    if numba_loop:
                        _entry_in_output_tuples = (to_typed_list(entry_in_output_tuples),)
                    else:
                        _entry_in_output_tuples = (entry_in_output_tuples,)
                else:
                    _entry_in_output_tuples = ()
                if len(entry_param_names) > 0:
                    if numba_loop:
                        _entry_param_tuples = (to_typed_list(entry_param_tuples),)
                    else:
                        _entry_param_tuples = (entry_param_tuples,)
                else:
                    _entry_param_tuples = ()

                return apply_and_concat_func(
                    n_params,
                    apply_func,
                    input_shape,
                    entry_pick_first,
                    entry_input_tuple,
                    *_entry_in_output_tuples,
                    *_entry_param_tuples,
                    entry_args + entry_more_args + entry_cache
                )

            elif mode == FactoryMode.Exits:
                if len(exit_in_output_names) > 0:
                    if numba_loop:
                        _exit_in_output_tuples = (to_typed_list(exit_in_output_tuples),)
                    else:
                        _exit_in_output_tuples = (exit_in_output_tuples,)
                else:
                    _exit_in_output_tuples = ()
                if len(exit_param_names) > 0:
                    if numba_loop:
                        _exit_param_tuples = (to_typed_list(exit_param_tuples),)
                    else:
                        _exit_param_tuples = (exit_param_tuples,)
                else:
                    _exit_param_tuples = ()

                return apply_and_concat_func(
                    n_params,
                    apply_func,
                    input_list[0],
                    exit_wait,
                    until_next,
                    skip_until_exit,
                    exit_pick_first,
                    exit_input_tuple,
                    *_exit_in_output_tuples,
                    *_exit_param_tuples,
                    exit_args + exit_more_args + exit_cache
                )

            else:
                if len(entry_in_output_names) > 0:
                    if numba_loop:
                        _entry_in_output_tuples = (to_typed_list(entry_in_output_tuples),)
                    else:
                        _entry_in_output_tuples = (entry_in_output_tuples,)
                else:
                    _entry_in_output_tuples = ()
                if len(entry_param_names) > 0:
                    if numba_loop:
                        _entry_param_tuples = (to_typed_list(entry_param_tuples),)
                    else:
                        _entry_param_tuples = (entry_param_tuples,)
                else:
                    _entry_param_tuples = ()
                if len(exit_in_output_names) > 0:
                    if numba_loop:
                        _exit_in_output_tuples = (to_typed_list(exit_in_output_tuples),)
                    else:
                        _exit_in_output_tuples = (exit_in_output_tuples,)
                else:
                    _exit_in_output_tuples = ()
                if len(exit_param_names) > 0:
                    if numba_loop:
                        _exit_param_tuples = (to_typed_list(exit_param_tuples),)
                    else:
                        _exit_param_tuples = (exit_param_tuples,)
                else:
                    _exit_param_tuples = ()

                return apply_and_concat_func(
                    n_params,
                    apply_func,
                    input_shape,
                    entry_wait,
                    exit_wait,
                    entry_pick_first,
                    exit_pick_first,
                    entry_input_tuple,
                    exit_input_tuple,
                    *_entry_in_output_tuples,
                    *_exit_in_output_tuples,
                    *_entry_param_tuples,
                    *_exit_param_tuples,
                    entry_args + entry_more_args + entry_cache,
                    exit_args + exit_more_args + exit_cache
                )

        return self.from_custom_func(
            custom_func,
            as_lists=True,
            require_input_shape=require_input_shape,
            **kwargs
        )
