# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Modules for building and running look-ahead indicators and label generators."""

from vectorbt.labels.enums import *
from vectorbt.labels.generators import (
    FMEAN,
    FSTD,
    FMIN,
    FMAX,
    FIXLB,
    MEANLB,
    LEXLB,
    TRENDLB,
    BOLB
)

__all__ = [
    'FMEAN',
    'FSTD',
    'FMIN',
    'FMAX',
    'FIXLB',
    'MEANLB',
    'LEXLB',
    'TRENDLB',
    'BOLB'
]

__pdoc__ = {k: False for k in __all__}
