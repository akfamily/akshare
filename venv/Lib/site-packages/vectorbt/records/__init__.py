# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Modules for working with records.

Records are the second form of data representation in vectorbt. They allow storing sparse event data
such as drawdowns, orders, trades, and positions, without converting them back to the matrix form and
occupying the user's memory."""

from vectorbt.records.base import Records
from vectorbt.records.mapped_array import MappedArray

__all__ = [
    'MappedArray',
    'Records'
]

__pdoc__ = {k: False for k in __all__}
