# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Modules for working with any time series.

In contrast to the `vectorbt.base` sub-package, focuses on the data itself."""

from vectorbt.generic.drawdowns import Drawdowns
from vectorbt.generic.enums import *
from vectorbt.generic.ranges import Ranges
from vectorbt.generic.splitters import RangeSplitter, RollingSplitter, ExpandingSplitter

__all__ = [
    'Ranges',
    'Drawdowns',
    'RangeSplitter',
    'RollingSplitter',
    'ExpandingSplitter'
]

__pdoc__ = {k: False for k in __all__}
