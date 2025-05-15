"""times module

This module provides some Date and Time classes for dealing with MySQL data.

Use Python datetime module to handle date and time columns.
"""
from time import localtime
from datetime import date, datetime, time, timedelta
from MySQLdb._mysql import string_literal

Date = date
Time = time
TimeDelta = timedelta
Timestamp = datetime

DateTimeDeltaType = timedelta
DateTimeType = datetime


def DateFromTicks(ticks):
    """Convert UNIX ticks into a date instance."""
    return date(*localtime(ticks)[:3])


def TimeFromTicks(ticks):
    """Convert UNIX ticks into a time instance."""
    return time(*localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    """Convert UNIX ticks into a datetime instance."""
    return datetime(*localtime(ticks)[:6])


format_TIME = format_DATE = str


def format_TIMEDELTA(v):
    seconds = int(v.seconds) % 60
    minutes = int(v.seconds // 60) % 60
    hours = int(v.seconds // 3600) % 24
    return "%d %d:%d:%d" % (v.days, hours, minutes, seconds)


def format_TIMESTAMP(d):
    """
    :type d: datetime.datetime
    """
    if d.microsecond:
        fmt = " ".join(
            [
                "{0.year:04}-{0.month:02}-{0.day:02}",
                "{0.hour:02}:{0.minute:02}:{0.second:02}.{0.microsecond:06}",
            ]
        )
    else:
        fmt = " ".join(
            [
                "{0.year:04}-{0.month:02}-{0.day:02}",
                "{0.hour:02}:{0.minute:02}:{0.second:02}",
            ]
        )
    return fmt.format(d)


def DateTime_or_None(s):
    try:
        if len(s) < 11:
            return Date_or_None(s)

        micros = s[20:]

        if len(micros) == 0:
            # 12:00:00
            micros = 0
        elif len(micros) < 7:
            # 12:00:00.123456
            micros = int(micros) * 10 ** (6 - len(micros))
        else:
            return None

        return datetime(
            int(s[:4]),  # year
            int(s[5:7]),  # month
            int(s[8:10]),  # day
            int(s[11:13] or 0),  # hour
            int(s[14:16] or 0),  # minute
            int(s[17:19] or 0),  # second
            micros,  # microsecond
        )
    except ValueError:
        return None


def TimeDelta_or_None(s):
    try:
        h, m, s = s.split(":")
        if "." in s:
            s, ms = s.split(".")
            ms = ms.ljust(6, "0")
        else:
            ms = 0
        if h[0] == "-":
            negative = True
        else:
            negative = False
        h, m, s, ms = abs(int(h)), int(m), int(s), int(ms)
        td = timedelta(hours=h, minutes=m, seconds=s, microseconds=ms)
        if negative:
            return -td
        else:
            return td
    except ValueError:
        # unpacking or int/float conversion failed
        return None


def Time_or_None(s):
    try:
        h, m, s = s.split(":")
        if "." in s:
            s, ms = s.split(".")
            ms = ms.ljust(6, "0")
        else:
            ms = 0
        h, m, s, ms = int(h), int(m), int(s), int(ms)
        return time(hour=h, minute=m, second=s, microsecond=ms)
    except ValueError:
        return None


def Date_or_None(s):
    try:
        return date(
            int(s[:4]),
            int(s[5:7]),
            int(s[8:10]),
        )  # year  # month  # day
    except ValueError:
        return None


def DateTime2literal(d, c):
    """Format a DateTime object as an ISO timestamp."""
    return string_literal(format_TIMESTAMP(d))


def DateTimeDelta2literal(d, c):
    """Format a DateTimeDelta object as a time."""
    return string_literal(format_TIMEDELTA(d))
