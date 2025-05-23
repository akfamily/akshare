# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Modules for building and running indicators.

Technical indicators are used to see past trends and anticipate future moves.
See [Using Technical Indicators to Develop Trading Strategies](https://www.investopedia.com/articles/trading/11/indicators-and-strategies-explained.asp)."""

from vectorbt import _typing as tp
from vectorbt.indicators.basic import (
    MA,
    MSTD,
    BBANDS,
    RSI,
    STOCH,
    MACD,
    ATR,
    OBV
)
from vectorbt.indicators.factory import IndicatorFactory, IndicatorBase


def talib(*args, **kwargs) -> tp.Type[IndicatorBase]:
    """Shortcut for `vectorbt.indicators.factory.IndicatorFactory.from_talib`."""
    return IndicatorFactory.from_talib(*args, **kwargs)


def pandas_ta(*args, **kwargs) -> tp.Type[IndicatorBase]:
    """Shortcut for `vectorbt.indicators.factory.IndicatorFactory.from_pandas_ta`."""
    return IndicatorFactory.from_pandas_ta(*args, **kwargs)


def ta(*args, **kwargs) -> tp.Type[IndicatorBase]:
    """Shortcut for `vectorbt.indicators.factory.IndicatorFactory.from_ta`."""
    return IndicatorFactory.from_ta(*args, **kwargs)


__all__ = [
    'IndicatorFactory',
    'talib',
    'pandas_ta',
    'ta',
    'MA',
    'MSTD',
    'BBANDS',
    'RSI',
    'STOCH',
    'MACD',
    'ATR',
    'OBV'
]
__whitelist__ = [
    'talib',
    'pandas_ta',
    'ta'
]

__pdoc__ = {k: k in __whitelist__ for k in __all__}
