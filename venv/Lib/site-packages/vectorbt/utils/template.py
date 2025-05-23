# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Utilities for working with templates."""

from copy import copy
from string import Template

from vectorbt import _typing as tp
from vectorbt.utils import checks
from vectorbt.utils.config import set_dict_item, get_func_arg_names, merge_dicts
from vectorbt.utils.docs import SafeToStr, prepare_for_doc


class Sub(SafeToStr):
    """Template to substitute parts of the string with the respective values from `mapping`.

    Returns a string."""

    def __init__(self, template: tp.Union[str, Template], mapping: tp.Optional[tp.Mapping] = None) -> None:
        self._template = template
        self._mapping = mapping

    @property
    def template(self) -> Template:
        """Template to be processed."""
        if not isinstance(self._template, Template):
            return Template(self._template)
        return self._template

    @property
    def mapping(self) -> tp.Mapping:
        """Mapping object passed to the initializer."""
        if self._mapping is None:
            return {}
        return self._mapping

    def substitute(self, mapping: tp.Optional[tp.Mapping] = None) -> str:
        """Substitute parts of `Sub.template` using `mapping`.

        Merges `mapping` and `Sub.mapping`.
        """
        mapping = merge_dicts(self.mapping, mapping)
        return self.template.substitute(mapping)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(" \
               f"template=\"{self.template.template}\", " \
               f"mapping={prepare_for_doc(self.mapping)})"


class Rep(SafeToStr):
    """Key to be replaced with the respective value from `mapping`."""

    def __init__(self, key: tp.Hashable, mapping: tp.Optional[tp.Mapping] = None) -> None:
        self._key = key
        self._mapping = mapping

    @property
    def key(self) -> tp.Hashable:
        """Key to be replaced."""
        return self._key

    @property
    def mapping(self) -> tp.Mapping:
        """Mapping object passed to the initializer."""
        if self._mapping is None:
            return {}
        return self._mapping

    def replace(self, mapping: tp.Optional[tp.Mapping] = None) -> tp.Any:
        """Replace `Rep.key` using `mapping`.

        Merges `mapping` and `Rep.mapping`."""
        mapping = merge_dicts(self.mapping, mapping)
        return mapping[self.key]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(" \
               f"key='{self.key}', " \
               f"mapping={prepare_for_doc(self.mapping)})"


class RepEval(SafeToStr):
    """Expression to be evaluated with `mapping` used as locals."""

    def __init__(self, expression: str, mapping: tp.Optional[tp.Mapping] = None) -> None:
        self._expression = expression
        self._mapping = mapping

    @property
    def expression(self) -> str:
        """Expression to be evaluated."""
        return self._expression

    @property
    def mapping(self) -> tp.Mapping:
        """Mapping object passed to the initializer."""
        if self._mapping is None:
            return {}
        return self._mapping

    def eval(self, mapping: tp.Optional[tp.Mapping] = None) -> tp.Any:
        """Evaluate `RepEval.expression` using `mapping`.

        Merges `mapping` and `RepEval.mapping`."""
        mapping = merge_dicts(self.mapping, mapping)
        return eval(self.expression, {}, mapping)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(" \
               f"expression=\"{self.expression}\", " \
               f"mapping={prepare_for_doc(self.mapping)})"


class RepFunc(SafeToStr):
    """Function to be called with argument names from `mapping`."""

    def __init__(self, func: tp.Callable, mapping: tp.Optional[tp.Mapping] = None) -> None:
        self._func = func
        self._mapping = mapping

    @property
    def func(self) -> tp.Callable:
        """Replacement function to be called."""
        return self._func

    @property
    def mapping(self) -> tp.Mapping:
        """Mapping object passed to the initializer."""
        if self._mapping is None:
            return {}
        return self._mapping

    def call(self, mapping: tp.Optional[tp.Mapping] = None) -> tp.Any:
        """Call `RepFunc.func` using `mapping`.

        Merges `mapping` and `RepFunc.mapping`."""
        mapping = merge_dicts(self.mapping, mapping)
        func_arg_names = get_func_arg_names(self.func)
        func_kwargs = dict()
        for k, v in mapping.items():
            if k in func_arg_names:
                func_kwargs[k] = v
        return self.func(**func_kwargs)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(" \
               f"func={self.func}, " \
               f"mapping={prepare_for_doc(self.mapping)})"


def has_templates(obj: tp.Any) -> tp.Any:
    """Check if the object has any templates."""
    if isinstance(obj, RepFunc):
        return True
    if isinstance(obj, RepEval):
        return True
    if isinstance(obj, Rep):
        return True
    if isinstance(obj, Sub):
        return True
    if isinstance(obj, Template):
        return True
    if isinstance(obj, dict):
        for k, v in obj.items():
            if has_templates(v):
                return True
    if isinstance(obj, (tuple, list, set, frozenset)):
        for v in obj:
            if has_templates(v):
                return True
    return False


def deep_substitute(obj: tp.Any,
                    mapping: tp.Optional[tp.Mapping] = None,
                    safe: bool = False,
                    make_copy: bool = True) -> tp.Any:
    """Traverses the object recursively and, if any template found, substitutes it using a mapping.

    Traverses tuples, lists, dicts and (frozen-)sets. Does not look for templates in keys.

    If `safe` is True, won't raise an error but return the original template.

    !!! note
        If the object is deep (such as a dict or a list), creates a copy of it if any template found inside,
        thus loosing the reference to the original. Make sure to do a deep or hybrid copy of the object
        before proceeding for consistent behavior, or disable `make_copy` to override the original in place.

    Usage:
        ```pycon
        >>> import vectorbt as vbt

        >>> vbt.deep_substitute(vbt.Sub('$key', {'key': 100}))
        100
        >>> vbt.deep_substitute(vbt.Sub('$key', {'key': 100}), {'key': 200})
        200
        >>> vbt.deep_substitute(vbt.Sub('$key$key'), {'key': 100})
        100100
        >>> vbt.deep_substitute(vbt.Rep('key'), {'key': 100})
        100
        >>> vbt.deep_substitute([vbt.Rep('key'), vbt.Sub('$key$key')], {'key': 100})
        [100, '100100']
        >>> vbt.deep_substitute(vbt.RepFunc(lambda key: key == 100), {'key': 100})
        True
        >>> vbt.deep_substitute(vbt.RepEval('key == 100'), {'key': 100})
        True
        >>> vbt.deep_substitute(vbt.RepEval('key == 100', safe=False))
        NameError: name 'key' is not defined
        >>> vbt.deep_substitute(vbt.RepEval('key == 100', safe=True))
        <vectorbt.utils.template.RepEval at 0x7fe3ad2ab668>
        ```
    """
    if mapping is None:
        mapping = {}
    if not has_templates(obj):
        return obj
    try:
        if isinstance(obj, RepFunc):
            return obj.call(mapping)
        if isinstance(obj, RepEval):
            return obj.eval(mapping)
        if isinstance(obj, Rep):
            return obj.replace(mapping)
        if isinstance(obj, Sub):
            return obj.substitute(mapping)
        if isinstance(obj, Template):
            return obj.substitute(mapping)
        if isinstance(obj, dict):
            if make_copy:
                obj = copy(obj)
            for k, v in obj.items():
                set_dict_item(obj, k, deep_substitute(v, mapping=mapping, safe=safe), force=True)
            return obj
        if isinstance(obj, list):
            if make_copy:
                obj = copy(obj)
            for i in range(len(obj)):
                obj[i] = deep_substitute(obj[i], mapping=mapping, safe=safe)
            return obj
        if isinstance(obj, (tuple, set, frozenset)):
            result = []
            for o in obj:
                result.append(deep_substitute(o, mapping=mapping, safe=safe))
            if checks.is_namedtuple(obj):
                return type(obj)(*result)
            return type(obj)(result)
    except Exception as e:
        if not safe:
            raise e
    return obj
