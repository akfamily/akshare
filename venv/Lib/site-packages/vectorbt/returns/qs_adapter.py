# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Adapter class for quantstats.

!!! note
    Accessors do not utilize caching.

We can access the adapter from `ReturnsAccessor`:

```pycon
>>> import numpy as np
>>> import pandas as pd
>>> import vectorbt as vbt
>>> import quantstats as qs

>>> np.random.seed(42)
>>> rets = pd.Series(np.random.uniform(-0.1, 0.1, size=(100,)))
>>> benchmark_rets = pd.Series(np.random.uniform(-0.1, 0.1, size=(100,)))

>>> rets.vbt.returns.qs.r_squared(benchmark=benchmark_rets)
0.0011582111228735541
```

Which is the same as:

```pycon
>>> qs.stats.r_squared(rets, benchmark_rets)
```

So why not just using `qs.stats`?

First, we can define all parameters such as benchmark returns once and avoid passing them repeatedly
to every function. Second, vectorbt automatically translates parameters passed to `ReturnsAccessor`
for the use in quantstats.

```pycon
>>> # Defaults that vectorbt understands
>>> ret_acc = rets.vbt.returns(
...     benchmark_rets=benchmark_rets,
...     freq='d',
...     year_freq='365d',
...     defaults=dict(risk_free=0.001)
... )

>>> ret_acc.qs.r_squared()
0.0011582111228735541

>>> ret_acc.qs.sharpe()
-1.9158923252075455

>>> # Defaults that only quantstats understands
>>> qs_defaults = dict(
...     benchmark=benchmark_rets,
...     periods=365,
...     periods_per_year=365,
...     rf=0.001
... )
>>> ret_acc_qs = rets.vbt.returns.qs(defaults=qs_defaults)

>>> ret_acc_qs.r_squared()
0.0011582111228735541

>>> ret_acc_qs.sharpe()
-1.9158923252075455
```

The adapter automatically passes the returns to the particular function.
It also merges the defaults defined in the settings, the defaults passed to `ReturnsAccessor`,
and the defaults passed to `QSAdapter` itself, and matches them with the argument names listed
in the function's signature.

For example, the `periods` and `periods_per_year` arguments default to the annualization factor
`ReturnsAccessor.ann_factor`, which itself is based on the `freq` argument. This makes the results
produced by quantstats and vectorbt at least somewhat similar.

```pycon
>>> vbt.settings.array_wrapper['freq'] = 'h'
>>> vbt.settings.returns['year_freq'] = '365d'

>>> rets.vbt.returns.sharpe_ratio()  # ReturnsAccessor
-9.38160953971508

>>> rets.vbt.returns.qs.sharpe()  # quantstats via QSAdapter
-9.38160953971508
```

We can still override any argument by overriding its default or by passing it directly to the function:

```pycon
>>> rets.vbt.returns.qs(defaults=dict(periods=252)).sharpe()
-1.5912029345745982

>>> rets.vbt.returns.qs.sharpe(periods=252)
-1.5912029345745982

>>> qs.stats.sharpe(rets)
-1.5912029345745982
```
"""
from inspect import getmembers, isfunction, signature, Parameter

import pandas as pd
import quantstats as qs

from vectorbt import _typing as tp
from vectorbt.returns.accessors import ReturnsAccessor
from vectorbt.utils import checks
from vectorbt.utils.config import merge_dicts, get_func_arg_names, Configured


def attach_qs_methods(cls: tp.Type[tp.T], replace_signature: bool = True) -> tp.Type[tp.T]:
    """Class decorator to attach quantstats methods."""

    checks.assert_subclass_of(cls, "QSAdapter")

    for module_name in ['utils', 'stats', 'plots', 'reports']:
        for qs_func_name, qs_func in getmembers(getattr(qs, module_name), isfunction):
            if not qs_func_name.startswith('_') and checks.func_accepts_arg(qs_func, 'returns'):
                if module_name == 'plots':
                    new_method_name = 'plot_' + qs_func_name
                elif module_name == 'reports':
                    new_method_name = qs_func_name + '_report'
                else:
                    new_method_name = qs_func_name

                def new_method(self, *, _func: tp.Callable = qs_func, **kwargs) -> tp.Any:
                    returns = self.returns_accessor.obj
                    if isinstance(returns, pd.DataFrame):
                        null_mask = returns.isnull().any(axis=1)
                    else:
                        null_mask = returns.isnull()
                    func_arg_names = get_func_arg_names(_func)
                    defaults = self.defaults

                    pass_kwargs = dict()
                    for arg_name in func_arg_names:
                        if arg_name not in kwargs:
                            if arg_name in defaults:
                                pass_kwargs[arg_name] = defaults[arg_name]
                            elif arg_name == 'benchmark':
                                if self.returns_accessor.benchmark_rets is not None:
                                    pass_kwargs['benchmark'] = self.returns_accessor.benchmark_rets
                            elif arg_name == 'periods':
                                pass_kwargs['periods'] = int(self.returns_accessor.ann_factor)
                            elif arg_name == 'periods_per_year':
                                pass_kwargs['periods_per_year'] = int(self.returns_accessor.ann_factor)
                        else:
                            pass_kwargs[arg_name] = kwargs[arg_name]

                    if 'benchmark' in pass_kwargs:
                        if isinstance(pass_kwargs['benchmark'], pd.DataFrame):
                            bm_null_mask = pass_kwargs['benchmark'].isnull().any(axis=1)
                        else:
                            bm_null_mask = pass_kwargs['benchmark'].isnull()
                        null_mask = null_mask | bm_null_mask
                        pass_kwargs['benchmark'] = pass_kwargs['benchmark'].loc[~null_mask]
                    returns = returns.loc[~null_mask]

                    signature(_func).bind(returns=returns, **pass_kwargs)
                    return _func(returns=returns, **pass_kwargs)

                if replace_signature:
                    # Replace the function's signature with the original one
                    source_sig = signature(qs_func)
                    new_method_params = tuple(signature(new_method).parameters.values())
                    self_arg = new_method_params[0]
                    other_args = [
                        p.replace(kind=Parameter.KEYWORD_ONLY)
                        if p.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
                        else p
                        for p in list(source_sig.parameters.values())[1:]
                    ]
                    source_sig = source_sig.replace(parameters=(self_arg,) + tuple(other_args))
                    new_method.__signature__ = source_sig

                new_method.__doc__ = f"See `quantstats.{module_name}.{qs_func_name}`."
                new_method.__qualname__ = f"{cls.__name__}.{new_method_name}"
                new_method.__name__ = new_method_name
                setattr(cls, new_method_name, new_method)
    return cls


QSAdapterT = tp.TypeVar("QSAdapterT", bound="QSAdapter")


@attach_qs_methods
class QSAdapter(Configured):
    """Adapter class for quantstats."""

    def __init__(self, returns_accessor: ReturnsAccessor, defaults: tp.KwargsLike = None, **kwargs) -> None:
        checks.assert_instance_of(returns_accessor, ReturnsAccessor)

        Configured.__init__(self, returns_accessor=returns_accessor, defaults=defaults, **kwargs)

        self._returns_accessor = returns_accessor
        self._defaults = defaults

    def __call__(self: QSAdapterT, **kwargs) -> QSAdapterT:
        """Allows passing arguments to the initializer."""

        return self.replace(**kwargs)

    @property
    def returns_accessor(self) -> ReturnsAccessor:
        """Returns accessor."""
        return self._returns_accessor

    @property
    def defaults_mapping(self) -> tp.Dict:
        """Common argument names in quantstats mapped to `ReturnsAccessor.defaults`."""
        return dict(rf='risk_free')

    @property
    def defaults(self) -> tp.Kwargs:
        """Defaults for `QSAdapter`.

        Merges `qs_adapter.defaults` from `vectorbt._settings.settings`, `returns_accessor.defaults`
        (with adapted naming), and `defaults` from `QSAdapter.__init__`."""
        from vectorbt._settings import settings
        qs_adapter_defaults_cfg = settings['qs_adapter']['defaults']

        mapped_defaults = dict()
        for k, v in self.defaults_mapping.items():
            if v in self.returns_accessor.defaults:
                mapped_defaults[k] = self.returns_accessor.defaults[v]
        return merge_dicts(
            qs_adapter_defaults_cfg,
            mapped_defaults,
            self._defaults
        )
