# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Enum utilities.

In vectorbt, enums are represented by instances of named tuples to be easily used in Numba.
Their values start with 0, while -1 means there is no value."""

from vectorbt import _typing as tp
from vectorbt.utils.mapping import to_mapping, apply_mapping


def map_enum_fields(field: tp.Any, enum: tp.Enum, ignore_type=int, **kwargs) -> tp.Any:
    """Map fields to values.

    See `vectorbt.utils.mapping.apply_mapping`."""
    mapping = to_mapping(enum, reverse=True)

    return apply_mapping(field, mapping, ignore_type=ignore_type, **kwargs)


def map_enum_values(value: tp.Any, enum: tp.Enum, ignore_type=str, **kwargs) -> tp.Any:
    """Map values to fields.

    See `vectorbt.utils.mapping.apply_mapping`."""
    mapping = to_mapping(enum, reverse=False)

    return apply_mapping(value, mapping, ignore_type=ignore_type, **kwargs)
