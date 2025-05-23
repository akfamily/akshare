import calendar
import logging
import types
import unicodedata
from collections import OrderedDict
from datetime import datetime

import regex as re
from pytz import UTC, UnknownTimeZoneError, timezone
from tzlocal import get_localzone

from dateparser.timezone_parser import StaticTzInfo, _tz_offsets


def strip_braces(date_string):
    return re.sub(r"[{}()<>\[\]]+", "", date_string)


def normalize_unicode(string, form="NFKD"):
    return "".join(
        c
        for c in unicodedata.normalize(form, string)
        if unicodedata.category(c) != "Mn"
    )


def combine_dicts(primary_dict, supplementary_dict):
    combined_dict = OrderedDict()
    for key, value in primary_dict.items():
        if key in supplementary_dict:
            if isinstance(value, list):
                combined_dict[key] = value + supplementary_dict[key]
            elif isinstance(value, dict):
                combined_dict[key] = combine_dicts(value, supplementary_dict[key])
            else:
                combined_dict[key] = supplementary_dict[key]
        else:
            combined_dict[key] = primary_dict[key]
    remaining_keys = [
        key for key in supplementary_dict.keys() if key not in primary_dict.keys()
    ]
    for key in remaining_keys:
        combined_dict[key] = supplementary_dict[key]
    return combined_dict


def find_date_separator(format):
    m = re.search(r"(?:(?:%[dbBmaA])(\W))+", format)
    if m:
        return m.group(1)


def _get_missing_parts(fmt):
    """
    Return a list containing missing parts (day, month, year)
    from a date format checking its directives
    """
    directive_mapping = {
        "day": ["%d", "%-d", "%j", "%-j"],
        "month": ["%b", "%B", "%m", "%-m"],
        "year": ["%y", "%-y", "%Y"],
    }

    missing = [
        field
        for field in ("day", "month", "year")
        if not any(directive in fmt for directive in directive_mapping[field])
    ]
    return missing


def get_timezone_from_tz_string(tz_string):
    try:
        return timezone(tz_string)
    except UnknownTimeZoneError as e:
        for name, info in _tz_offsets:
            if info["regex"].search(" %s" % tz_string):
                return StaticTzInfo(name, info["offset"])
        else:
            raise e


def localize_timezone(date_time, tz_string):
    if date_time.tzinfo:
        return date_time

    tz = get_timezone_from_tz_string(tz_string)

    if hasattr(tz, "localize"):
        date_time = tz.localize(date_time)
    else:
        date_time = date_time.replace(tzinfo=tz)

    return date_time


def apply_tzdatabase_timezone(date_time, pytz_string):
    usr_timezone = timezone(pytz_string)

    if date_time.tzinfo != usr_timezone:
        date_time = date_time.astimezone(usr_timezone)

    return date_time


def apply_dateparser_timezone(utc_datetime, offset_or_timezone_abb):
    for name, info in _tz_offsets:
        if info["regex"].search(" %s" % offset_or_timezone_abb):
            tz = StaticTzInfo(name, info["offset"])
            return utc_datetime.astimezone(tz)


def apply_timezone(date_time, tz_string):
    if not date_time.tzinfo:
        if hasattr(UTC, "localize"):
            date_time = UTC.localize(date_time)
        else:
            date_time = date_time.replace(tzinfo=UTC)

    new_datetime = apply_dateparser_timezone(date_time, tz_string)

    if not new_datetime:
        new_datetime = apply_tzdatabase_timezone(date_time, tz_string)

    return new_datetime


def apply_timezone_from_settings(date_obj, settings):
    tz = get_localzone()
    if settings is None:
        return date_obj

    if "local" in settings.TIMEZONE.lower():
        if hasattr(tz, "localize"):
            date_obj = tz.localize(date_obj)
        else:
            date_obj = date_obj.replace(tzinfo=tz)
    else:
        date_obj = localize_timezone(date_obj, settings.TIMEZONE)

    if settings.TO_TIMEZONE:
        date_obj = apply_timezone(date_obj, settings.TO_TIMEZONE)

    if settings.RETURN_AS_TIMEZONE_AWARE is not True:
        date_obj = date_obj.replace(tzinfo=None)

    return date_obj


def get_last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]


def get_previous_leap_year(year):
    return _get_leap_year(year, future=False)


def get_next_leap_year(year):
    return _get_leap_year(year, future=True)


def _get_leap_year(year, future):
    """
    Iterate through previous or next years until it gets a valid leap year
    This is performed to avoid missing or including centurial leap years
    """
    step = 1 if future else -1
    leap_year = year + step
    while not calendar.isleap(leap_year):
        leap_year += step
    return leap_year


def set_correct_day_from_settings(date_obj, settings, current_day=None):
    """Set correct day attending the `PREFER_DAY_OF_MONTH` setting."""
    options = {
        "first": 1,
        "last": get_last_day_of_month(date_obj.year, date_obj.month),
        "current": current_day or datetime.now().day,
    }

    try:
        return date_obj.replace(day=options[settings.PREFER_DAY_OF_MONTH])
    except ValueError:
        return date_obj.replace(day=options["last"])


def set_correct_month_from_settings(date_obj, settings, current_month=None):
    """Set correct month attending the `PREFER_MONTH_OF_YEAR` setting."""
    options = {"first": 1, "last": 12, "current": current_month or datetime.now().month}

    try:
        return date_obj.replace(month=options[settings.PREFER_MONTH_OF_YEAR])
    except ValueError:
        return date_obj.replace(month=options["last"])


def registry(cls):
    def choose(creator):
        def constructor(cls, *args, **kwargs):
            key = cls.get_key(*args, **kwargs)

            if not hasattr(cls, "__registry_dict"):
                setattr(cls, "__registry_dict", {})
            registry_dict = getattr(cls, "__registry_dict")

            if key not in registry_dict:
                registry_dict[key] = creator(cls, *args)
                setattr(registry_dict[key], "registry_key", key)
            return registry_dict[key]

        return staticmethod(constructor)

    if not (
        hasattr(cls, "get_key")
        and isinstance(cls.get_key, types.MethodType)
        and cls.get_key.__self__ is cls
    ):
        raise NotImplementedError(
            "Registry classes require to implement class method get_key"
        )

    setattr(cls, "__new__", choose(cls.__new__))
    return cls


def get_logger():
    setup_logging()
    return logging.getLogger("dateparser")


def setup_logging():
    if len(logging.root.handlers):
        return

    config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "console": {
                "format": "%(asctime)s %(levelname)s: [%(name)s] %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": logging.DEBUG,
                "class": "logging.StreamHandler",
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": logging.DEBUG,
            "handlers": ["console"],
        },
    }
    logging.config.dictConfig(config)
