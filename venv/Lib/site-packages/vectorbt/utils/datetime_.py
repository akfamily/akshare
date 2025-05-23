# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Utilities for working with dates and time."""

import copy
from datetime import datetime, timezone, timedelta, tzinfo, time

import dateparser
import numpy as np
import pandas as pd
import pytz

from vectorbt import _typing as tp

DatetimeIndexes = (pd.DatetimeIndex, pd.TimedeltaIndex, pd.PeriodIndex)


def freq_to_timedelta(arg: tp.FrequencyLike) -> pd.Timedelta:
    """`pd.to_timedelta` that uses unit abbreviation with number."""
    if isinstance(arg, str) and not arg[0].isdigit():
        # Otherwise "ValueError: unit abbreviation w/o a number"
        return pd.Timedelta(1, unit=arg)
    return pd.Timedelta(arg)


def get_utc_tz() -> timezone:
    """Get UTC timezone."""
    return timezone.utc


def get_local_tz() -> timezone:
    """Get local timezone."""
    return timezone(datetime.now(timezone.utc).astimezone().utcoffset())


def convert_tzaware_time(t: time, tz_out: tp.Optional[tzinfo]) -> time:
    """Return as non-naive time.

    `datetime.time` should have `tzinfo` set."""
    return datetime.combine(datetime.today(), t).astimezone(tz_out).timetz()


def tzaware_to_naive_time(t: time, tz_out: tp.Optional[tzinfo]) -> time:
    """Return as naive time.

    `datetime.time` should have `tzinfo` set."""
    return datetime.combine(datetime.today(), t).astimezone(tz_out).time()


def naive_to_tzaware_time(t: time, tz_out: tp.Optional[tzinfo]) -> time:
    """Return as non-naive time.

    `datetime.time` should not have `tzinfo` set."""
    return datetime.combine(datetime.today(), t).astimezone(tz_out).time().replace(tzinfo=tz_out)


def convert_naive_time(t: time, tz_out: tp.Optional[tzinfo]) -> time:
    """Return as naive time.

    `datetime.time` should not have `tzinfo` set."""
    return datetime.combine(datetime.today(), t).astimezone(tz_out).time()


def is_tz_aware(dt: tp.SupportsTZInfo) -> bool:
    """Whether datetime is timezone-aware."""
    tz = dt.tzinfo
    if tz is None:
        return False
    return tz.utcoffset(datetime.now()) is not None


def to_timezone(tz: tp.TimezoneLike, to_py_timezone: tp.Optional[bool] = None, **kwargs) -> tzinfo:
    """Parse the timezone.

    Strings are parsed by `pytz` and `dateparser`, while integers and floats are treated as hour offsets.

    If the timezone object can't be checked for equality based on its properties,
    it's automatically converted to `datetime.timezone`.

    If `to_py_timezone` is set to True, will convert to `datetime.timezone`.

    `**kwargs` are passed to `dateparser.parse`."""
    from vectorbt._settings import settings
    datetime_cfg = settings['datetime']

    if tz is None:
        return get_local_tz()
    if to_py_timezone is None:
        to_py_timezone = datetime_cfg['to_py_timezone']
    if isinstance(tz, str):
        try:
            tz = pytz.timezone(tz)
        except pytz.UnknownTimeZoneError:
            dt = dateparser.parse('now %s' % tz, **kwargs)
            if dt is not None:
                tz = dt.tzinfo
    if isinstance(tz, (int, float)):
        tz = timezone(timedelta(hours=tz))
    if isinstance(tz, timedelta):
        tz = timezone(tz)
    if isinstance(tz, tzinfo):
        if to_py_timezone:
            return timezone(tz.utcoffset(datetime.now()))
        return tz
    raise TypeError("Couldn't parse the timezone")


def to_tzaware_datetime(dt_like: tp.DatetimeLike,
                        naive_tz: tp.Optional[tp.TimezoneLike] = None,
                        tz: tp.Optional[tp.TimezoneLike] = None,
                        **kwargs) -> datetime:
    """Parse the datetime as a timezone-aware `datetime.datetime`.

    See [dateparser docs](http://dateparser.readthedocs.io/en/latest/) for valid string formats and `**kwargs`.

    Raw timestamps are localized to UTC, while naive datetime is localized to `naive_tz`.
    Set `naive_tz` to None to use the default value defined under `datetime` settings
    in `vectorbt._settings.settings`.
    To explicitly convert the datetime to a timezone, use `tz` (uses `to_timezone`)."""
    from vectorbt._settings import settings
    datetime_cfg = settings['datetime']

    if naive_tz is None:
        naive_tz = datetime_cfg['naive_tz']
    if isinstance(dt_like, float):
        dt = datetime.fromtimestamp(dt_like, timezone.utc)
    elif isinstance(dt_like, int):
        if len(str(dt_like)) > 10:
            dt = datetime.fromtimestamp(dt_like / 10 ** (len(str(dt_like)) - 10), timezone.utc)
        else:
            dt = datetime.fromtimestamp(dt_like, timezone.utc)
    elif isinstance(dt_like, str):
        dt = dateparser.parse(dt_like, **kwargs)
    elif isinstance(dt_like, pd.Timestamp):
        dt = dt_like.to_pydatetime()
    elif isinstance(dt_like, np.datetime64):
        dt = datetime.combine(dt_like.astype(datetime), time())
    else:
        dt = dt_like

    if dt is None:
        raise ValueError("Couldn't parse the datetime")

    if not is_tz_aware(dt):
        dt = dt.replace(tzinfo=to_timezone(naive_tz))
    else:
        dt = dt.replace(tzinfo=to_timezone(dt.tzinfo))
    if tz is not None:
        dt = dt.astimezone(to_timezone(tz))
    return dt


def datetime_to_ms(dt: datetime) -> int:
    """Convert a datetime to milliseconds."""
    epoch = datetime.fromtimestamp(0, dt.tzinfo)
    return int((dt - epoch).total_seconds() * 1000.0)


def interval_to_ms(interval: str) -> tp.Optional[int]:
    """Convert an interval string to milliseconds."""
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60,
    }
    try:
        return int(interval[:-1]) * seconds_per_unit[interval[-1]] * 1000
    except (ValueError, KeyError):
        return None
