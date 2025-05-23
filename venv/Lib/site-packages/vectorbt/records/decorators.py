# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Class and function decorators."""

import keyword
import re
from functools import partial

from vectorbt import _typing as tp
from vectorbt.records.mapped_array import MappedArray
from vectorbt.utils import checks
from vectorbt.utils.config import merge_dicts, Config
from vectorbt.utils.decorators import cached_property
from vectorbt.utils.mapping import to_mapping

WrapperFuncT = tp.Callable[[tp.Type[tp.T]], tp.Type[tp.T]]


def override_field_config(*args, merge_configs: bool = True) -> tp.Union[WrapperFuncT, tp.Type[tp.T]]:
    """Class decorator to override field configs of all base classes in MRO that subclass
    `vectorbt.records.base.Records`.
    
    Instead of overriding `_field_config` class attribute, you can pass `config` directly to this decorator.

    Disable `merge_configs` to not merge, which will effectively disable field inheritance."""

    def wrapper(cls: tp.Type[tp.T], config: tp.DictLike = None) -> tp.Type[tp.T]:
        checks.assert_subclass_of(cls, "Records")

        if config is None:
            config = cls.field_config
        if not isinstance(config, Config):
            config = Config(config, readonly=True, as_attrs=False)
        if merge_configs:
            configs = []
            for base_cls in cls.mro()[::-1]:
                if base_cls is not cls:
                    if checks.is_subclass_of(base_cls, "Records"):
                        configs.append(base_cls.field_config)
            configs.append(config)
            config = merge_dicts(*configs, to_dict=False)

        setattr(cls, "_field_config", config)
        return cls

    if len(args) == 0:
        return wrapper
    elif len(args) == 1:
        if isinstance(args[0], type):
            return wrapper(args[0])
        return partial(wrapper, config=args[0])
    elif len(args) == 2:
        return wrapper(args[0], config=args[1])
    raise ValueError("Either class, config, class and config, or keyword arguments must be passed")


def attach_fields(*args, on_conflict: str = 'raise') -> tp.Union[WrapperFuncT, tp.Type[tp.T]]:
    """Class decorator to attach field properties in a `vectorbt.records.base.Records` class.

    Will extract `dtype` and other relevant information from `vectorbt.records.base.Records.field_config`
    and map its fields as properties. This behavior can be changed by using `config`.

    !!! note
        Make sure to run `attach_fields` after `override_field_config`.

    `config` should contain fields (keys) and dictionaries (values) with the following keys:

    * `attach`: Whether to attach the field property. Can be provided as a string to be used
        as a target attribute name. Defaults to True.
    * `defaults`: Dictionary with default keyword arguments for `vectorbt.records.base.Records.map_field`.
        Defaults to an empty dict.
    * `attach_filters`: Whether to attach filters based on the field's values. Can be provided as a dict
        to be used instead of the mapping (filter value -> target filter name). Defaults to False.
        If True, defaults to `mapping` in `vectorbt.records.base.Records.field_config`.
    * `filter_defaults`: Dictionary with default keyword arguments for `vectorbt.records.base.Records.apply_mask`.
        Can be provided by target filter name. Defaults to an empty dict.
    * `on_conflict`: Overrides global `on_conflict` for both field and filter properties.

    Any potential attribute name is prepared by placing underscores between capital letters and
    converting to the lower case.

    If an attribute with the same name already exists in the class but the name is not listed in the field config:

    * it will be overridden if `on_conflict` is 'override'
    * it will be ignored if `on_conflict` is 'ignore'
    * an error will be raised if `on_conflict` is 'raise'
    """

    def wrapper(cls: tp.Type[tp.T], config: tp.DictLike = None) -> tp.Type[tp.T]:
        checks.assert_subclass_of(cls, "Records")

        dtype = cls.field_config.get('dtype', None)
        checks.assert_not_none(dtype.fields)

        if config is None:
            config = {}

        def _prepare_attr_name(attr_name: str) -> str:
            checks.assert_instance_of(attr_name, str)
            attr_name = attr_name.replace('NaN', 'Nan')
            startswith_ = attr_name.startswith('_')
            attr_name = re.sub(r"([A-Z])", r"_\1", attr_name)
            if not startswith_ and attr_name.startswith('_'):
                attr_name = attr_name[1:]
            attr_name = attr_name.lower()
            if keyword.iskeyword(attr_name):
                attr_name += '_'
            return attr_name

        def _check_attr_name(attr_name, _on_conflict: str = on_conflict) -> None:
            if attr_name not in cls.field_config.get('settings', {}):
                # Consider only attributes that are not listed in the field config
                if hasattr(cls, attr_name):
                    if _on_conflict.lower() == 'raise':
                        raise ValueError(f"An attribute with the name '{attr_name}' already exists in {cls}")
                    if _on_conflict.lower() == 'ignore':
                        return
                    if _on_conflict.lower() == 'override':
                        return
                    raise ValueError(f"Value '{_on_conflict}' is invalid for on_conflict")
                if keyword.iskeyword(attr_name):
                    raise ValueError(f"Name '{attr_name}' is a keyword and cannot be used as an attribute name")

        if dtype is not None:
            for field_name in dtype.names:
                settings = config.get(field_name, {})
                attach = settings.get('attach', True)
                if not isinstance(attach, bool):
                    target_name = attach
                    attach = True
                else:
                    target_name = field_name
                defaults = settings.get('defaults', None)
                if defaults is None:
                    defaults = {}
                attach_filters = settings.get('attach_filters', False)
                filter_defaults = settings.get('filter_defaults', None)
                if filter_defaults is None:
                    filter_defaults = {}
                _on_conflict = settings.get('on_conflict', on_conflict)

                if attach:
                    target_name = _prepare_attr_name(target_name)
                    _check_attr_name(target_name, _on_conflict)

                    def new_prop(self,
                                 _field_name: str = field_name,
                                 _defaults: tp.KwargsLike = defaults) -> MappedArray:
                        return self.get_map_field(_field_name, **_defaults)

                    new_prop.__doc__ = f"Mapped array of the field `{field_name}`."
                    new_prop.__name__ = target_name
                    setattr(cls, target_name, cached_property(new_prop))

                if attach_filters:
                    if isinstance(attach_filters, bool):
                        if not attach_filters:
                            continue
                        mapping = cls.field_config \
                            .get('settings', {}) \
                            .get(field_name, {}) \
                            .get('mapping', None)
                    else:
                        mapping = attach_filters
                    if mapping is None:
                        raise ValueError(f"Field '{field_name}': Mapping is required to attach filters")
                    mapping = to_mapping(mapping)

                    for filter_value, target_filter_name in mapping.items():
                        if target_filter_name is None:
                            continue
                        target_filter_name = _prepare_attr_name(target_filter_name)
                        _check_attr_name(target_filter_name, _on_conflict)
                        if target_filter_name in filter_defaults:
                            __filter_defaults = filter_defaults[target_filter_name]
                        else:
                            __filter_defaults = filter_defaults

                        def new_filter_prop(self,
                                            _field_name: str = field_name,
                                            _filter_value: tp.Any = filter_value,
                                            _filter_defaults: tp.KwargsLike = __filter_defaults) -> MappedArray:
                            filter_mask = self.get_field_arr(_field_name) == _filter_value
                            return self.apply_mask(filter_mask, **_filter_defaults)

                        new_filter_prop.__doc__ = f"Records filtered by `{field_name} == {filter_value}`."
                        new_filter_prop.__name__ = target_filter_name
                        setattr(cls, target_filter_name, cached_property(new_filter_prop))

        return cls

    if len(args) == 0:
        return wrapper
    elif len(args) == 1:
        if isinstance(args[0], type):
            return wrapper(args[0])
        return partial(wrapper, config=args[0])
    elif len(args) == 2:
        return wrapper(args[0], config=args[1])
    raise ValueError("Either class, config, class and config, or keyword arguments must be passed")
