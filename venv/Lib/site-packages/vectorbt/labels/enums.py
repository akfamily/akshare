# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Named tuples and enumerated types.

Defines enums and other schemas for `vectorbt.labels`."""

from vectorbt import _typing as tp
from vectorbt.utils.docs import to_doc

__all__ = [
    'TrendMode'
]

__pdoc__ = {}


class TrendModeT(tp.NamedTuple):
    Binary: int = 0
    BinaryCont: int = 1
    BinaryContSat: int = 2
    PctChange: int = 3
    PctChangeNorm: int = 4


TrendMode = TrendModeT()
"""_"""

__pdoc__['TrendMode'] = f"""Trend mode.

```json
{to_doc(TrendMode)}
```

Attributes:
    Binary: See `vectorbt.labels.nb.bn_trend_labels_nb`.
    BinaryCont: See `vectorbt.labels.nb.bn_cont_trend_labels_nb`.
    BinaryContSat: See `vectorbt.labels.nb.bn_cont_sat_trend_labels_nb`.
    PctChange: See `vectorbt.labels.nb.pct_trend_labels_nb`.
    PctChangeNorm: See `vectorbt.labels.nb.pct_trend_labels_nb` with `normalize` set to True.
"""
