# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Root pandas accessors.

An accessor adds additional “namespace” to pandas objects.

The `vectorbt.root_accessors` registers a custom `vbt` accessor on top of each `pd.Series`
and `pd.DataFrame` object. It is the main entry point for all other accessors:

```plaintext
vbt.base.accessors.BaseSR/DFAccessor           -> pd.Series/DataFrame.vbt.*
vbt.generic.accessors.GenericSR/DFAccessor     -> pd.Series/DataFrame.vbt.*
vbt.signals.accessors.SignalsSR/DFAccessor     -> pd.Series/DataFrame.vbt.signals.*
vbt.returns.accessors.ReturnsSR/DFAccessor     -> pd.Series/DataFrame.vbt.returns.*
vbt.ohlcv.accessors.OHLCVDFAccessor            -> pd.DataFrame.vbt.ohlc.* and pd.DataFrame.vbt.ohlcv.*
vbt.px_accessors.PXAccessor                    -> pd.DataFrame.vbt.px.*
```

Additionally, some accessors subclass other accessors building the following inheritance hierarchy:

```plaintext
vbt.base.accessors.BaseSR/DFAccessor
    -> vbt.generic.accessors.GenericSR/DFAccessor
        -> vbt.cat_accessors.CatSR/DFAccessor
        -> vbt.signals.accessors.SignalsSR/DFAccessor
        -> vbt.returns.accessors.ReturnsSR/DFAccessor
        -> vbt.ohlcv_accessors.OHLCVDFAccessor
    -> vbt.px_accessors.PXSR/DFAccessor
```

So, for example, the method `pd.Series.vbt.to_2d_array` is also available as
`pd.Series.vbt.returns.to_2d_array`.

!!! note
    Accessors in vectorbt are not cached, so querying `df.vbt` twice will also call `Vbt_DFAccessor` twice."""

import warnings

import pandas as pd
from pandas.core.accessor import DirNamesMixin

from vectorbt import _typing as tp
from vectorbt.generic.accessors import GenericSRAccessor, GenericDFAccessor
from vectorbt.utils.config import Configured

ParentAccessorT = tp.TypeVar("ParentAccessorT", bound=object)
AccessorT = tp.TypeVar("AccessorT", bound=object)


class Accessor:
    """Custom property-like object.

    !!! note
        In contrast to other pandas accessors, this accessor is not cached!

        This prevents from using old data if the object has been changed in-place."""

    def __init__(self, name: str, accessor: tp.Type[AccessorT]) -> None:
        self._name = name
        self._accessor = accessor

    def __get__(self, obj: ParentAccessorT, cls: DirNamesMixin) -> AccessorT:
        if obj is None:
            return self._accessor
        if isinstance(obj, (pd.Series, pd.DataFrame)):
            accessor_obj = self._accessor(obj)
        elif isinstance(obj, Configured):
            accessor_obj = obj.replace(cls_=self._accessor)
        else:
            accessor_obj = self._accessor(obj.obj)
        return accessor_obj


def register_accessor(name: str, cls: tp.Type[DirNamesMixin]) -> tp.Callable:
    """Register a custom accessor.

    `cls` should subclass `pandas.core.accessor.DirNamesMixin`."""

    def decorator(accessor: tp.Type[AccessorT]) -> tp.Type[AccessorT]:
        if hasattr(cls, name):
            warnings.warn(
                f"registration of accessor {repr(accessor)} under name "
                f"{repr(name)} for type {repr(cls)} is overriding a preexisting "
                f"attribute with the same name.",
                UserWarning,
                stacklevel=2,
            )
        setattr(cls, name, Accessor(name, accessor))
        cls._accessors.add(name)
        return accessor

    return decorator


def register_series_accessor(name: str) -> tp.Callable:
    """Decorator to register a custom `pd.Series` accessor on top of the `pd.Series`."""
    return register_accessor(name, pd.Series)


def register_dataframe_accessor(name: str) -> tp.Callable:
    """Decorator to register a custom `pd.DataFrame` accessor on top of the `pd.DataFrame`."""
    return register_accessor(name, pd.DataFrame)


# By subclassing DirNamesMixin, we can build accessors on top of each other
@register_series_accessor("vbt")
class Vbt_SRAccessor(DirNamesMixin, GenericSRAccessor):
    """The main vectorbt accessor for `pd.Series`."""

    def __init__(self, obj: tp.Series, **kwargs) -> None:
        self._obj = obj

        DirNamesMixin.__init__(self)
        GenericSRAccessor.__init__(self, obj, **kwargs)


@register_dataframe_accessor("vbt")
class Vbt_DFAccessor(DirNamesMixin, GenericDFAccessor):
    """The main vectorbt accessor for `pd.DataFrame`."""

    def __init__(self, obj: tp.Frame, **kwargs) -> None:
        self._obj = obj

        DirNamesMixin.__init__(self)
        GenericDFAccessor.__init__(self, obj, **kwargs)


def register_series_vbt_accessor(name: str, parent: tp.Type[DirNamesMixin] = Vbt_SRAccessor) -> tp.Callable:
    """Decorator to register a `pd.Series` accessor on top of a parent accessor."""
    return register_accessor(name, parent)


def register_dataframe_vbt_accessor(name: str, parent: tp.Type[DirNamesMixin] = Vbt_DFAccessor) -> tp.Callable:
    """Decorator to register a `pd.DataFrame` accessor on top of a parent accessor."""
    return register_accessor(name, parent)
