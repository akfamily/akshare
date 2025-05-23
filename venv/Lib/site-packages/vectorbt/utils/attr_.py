# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Utilities for working with class/instance attributes."""

import inspect
from collections.abc import Iterable

from vectorbt import _typing as tp
from vectorbt.utils import checks
from vectorbt.utils.config import merge_dicts, get_func_arg_names


def get_dict_attr(obj, attr):
    """Get attribute without invoking the attribute lookup machinery."""
    if inspect.isclass(obj):
        cls = obj
    else:
        cls = obj.__class__
    for obj in [obj] + cls.mro():
        if attr in obj.__dict__:
            return obj.__dict__[attr]
    raise AttributeError


def default_getattr_func(obj: tp.Any,
                         attr: str,
                         args: tp.Optional[tp.Args] = None,
                         kwargs: tp.Optional[tp.Kwargs] = None,
                         call_attr: bool = True) -> tp.Any:
    """Default `getattr_func`."""
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    out = getattr(obj, attr)
    if callable(out) and call_attr:
        return out(*args, **kwargs)
    return out


def deep_getattr(obj: tp.Any,
                 attr_chain: tp.Union[str, tuple, Iterable],
                 getattr_func: tp.Callable = default_getattr_func,
                 call_last_attr: bool = True) -> tp.Any:
    """Retrieve attribute consecutively.

    The attribute chain `attr_chain` can be:

    * string -> get variable/property or method without arguments
    * tuple of string -> call method without arguments
    * tuple of string and tuple -> call method and pass positional arguments (unpacked)
    * tuple of string, tuple, and dict -> call method and pass positional and keyword arguments (unpacked)
    * iterable of any of the above

    Use `getattr_func` to overwrite the default behavior of accessing an attribute (see `default_getattr_func`).

    !!! hint
        If your chain includes only attributes and functions without arguments,
        you can represent this chain as a single (but probably long) string.
    """
    checks.assert_instance_of(attr_chain, (str, tuple, Iterable))

    if isinstance(attr_chain, str):
        if '.' in attr_chain:
            return deep_getattr(
                obj,
                attr_chain.split('.'),
                getattr_func=getattr_func,
                call_last_attr=call_last_attr
            )
        return getattr_func(obj, attr_chain, call_attr=call_last_attr)
    if isinstance(attr_chain, tuple):
        if len(attr_chain) == 1 \
                and isinstance(attr_chain[0], str):
            return getattr_func(obj, attr_chain[0])
        if len(attr_chain) == 2 \
                and isinstance(attr_chain[0], str) \
                and isinstance(attr_chain[1], tuple):
            return getattr_func(obj, attr_chain[0], args=attr_chain[1])
        if len(attr_chain) == 3 \
                and isinstance(attr_chain[0], str) \
                and isinstance(attr_chain[1], tuple) \
                and isinstance(attr_chain[2], dict):
            return getattr_func(obj, attr_chain[0], args=attr_chain[1], kwargs=attr_chain[2])
    result = obj
    for i, attr in enumerate(attr_chain):
        if i < len(attr_chain) - 1:
            result = deep_getattr(
                result,
                attr,
                getattr_func=getattr_func,
                call_last_attr=True
            )
        else:
            result = deep_getattr(
                result,
                attr,
                getattr_func=getattr_func,
                call_last_attr=call_last_attr
            )
    return result


AttrResolverT = tp.TypeVar("AttrResolverT", bound="AttrResolver")


class AttrResolver:
    """Class that implements resolution of self and its attributes.

    Resolution is `getattr` that works for self, properties, and methods. It also utilizes built-in caching."""

    @property
    def self_aliases(self) -> tp.Set[str]:
        """Names to associate with this object."""
        return {'self'}

    def resolve_self(self: AttrResolverT,
                     cond_kwargs: tp.KwargsLike = None,
                     custom_arg_names: tp.Optional[tp.Set[str]] = None,
                     impacts_caching: bool = True,
                     silence_warnings: bool = False) -> AttrResolverT:
        """Resolve self.

        !!! note
            `cond_kwargs` can be modified in-place."""
        return self

    def pre_resolve_attr(self, attr: str, final_kwargs: tp.KwargsLike = None) -> str:
        """Pre-process an attribute before resolution.

        Should return an attribute."""
        return attr

    def post_resolve_attr(self, attr: str, out: tp.Any, final_kwargs: tp.KwargsLike = None) -> str:
        """Post-process an object after resolution.

        Should return an object."""
        return out

    def resolve_attr(self,
                     attr: str,
                     args: tp.ArgsLike = None,
                     cond_kwargs: tp.KwargsLike = None,
                     kwargs: tp.KwargsLike = None,
                     custom_arg_names: tp.Optional[tp.Container[str]] = None,
                     cache_dct: tp.KwargsLike = None,
                     use_caching: bool = True,
                     passed_kwargs_out: tp.KwargsLike = None) -> tp.Any:
        """Resolve an attribute using keyword arguments and built-in caching.

        * If `attr` is a property, returns its value.
        * If `attr` is a method, passes `*args`, `**kwargs`, and `**cond_kwargs` with keys found in the signature.
        * If `attr` is a property and there is a `get_{arg}` method, calls the `get_{arg}` method.

        Won't cache if `use_caching` is False or any passed argument is in `custom_arg_names`.

        Use `passed_kwargs_out` to get keyword arguments that were passed."""
        # Resolve defaults
        if custom_arg_names is None:
            custom_arg_names = list()
        if cache_dct is None:
            cache_dct = {}
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        if passed_kwargs_out is None:
            passed_kwargs_out = {}
        final_kwargs = merge_dicts(cond_kwargs, kwargs)

        # Resolve attribute
        cls = type(self)
        _attr = self.pre_resolve_attr(attr, final_kwargs=final_kwargs)
        if 'get_' + attr in dir(cls):
            _attr = 'get_' + attr
        if inspect.ismethod(getattr(cls, _attr)) or inspect.isfunction(getattr(cls, _attr)):
            attr_func = getattr(self, _attr)
            attr_func_kwargs = dict()
            attr_func_arg_names = get_func_arg_names(attr_func)
            custom_k = False
            for k, v in final_kwargs.items():
                if k in attr_func_arg_names or k in kwargs:
                    if k in custom_arg_names:
                        custom_k = True
                    attr_func_kwargs[k] = v
                    passed_kwargs_out[k] = v
            if use_caching and not custom_k and attr in cache_dct:
                out = cache_dct[attr]
            else:
                out = attr_func(*args, **attr_func_kwargs)
                if use_caching and not custom_k:
                    cache_dct[attr] = out
        else:
            if use_caching and attr in cache_dct:
                out = cache_dct[attr]
            else:
                out = getattr(self, _attr)
                if use_caching:
                    cache_dct[attr] = out
        out = self.post_resolve_attr(attr, out, final_kwargs=final_kwargs)
        return out

    def deep_getattr(self, *args, **kwargs) -> tp.Any:
        """See `vectorbt.utils.attr_.deep_getattr`."""
        return deep_getattr(self, *args, **kwargs)
