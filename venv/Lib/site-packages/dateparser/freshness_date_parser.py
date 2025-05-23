from datetime import datetime, time, timezone

import regex as re
from dateutil.relativedelta import relativedelta
from tzlocal import get_localzone

from dateparser.utils import apply_timezone, localize_timezone, strip_braces

from .parser import time_parser
from .timezone_parser import pop_tz_offset_from_string

_UNITS = r"decade|year|month|week|day|hour|minute|second"
PATTERN = re.compile(r"(\d+[.,]?\d*)\s*(%s)\b" % _UNITS, re.I | re.S | re.U)


class FreshnessDateDataParser:
    """Parses date string like "1 year, 2 months ago" and "3 hours, 50 minutes ago" """

    def _are_all_words_units(self, date_string):
        skip = [_UNITS, r"ago|in|\d+", r":|[ap]m"]

        date_string = re.sub(r"\s+", " ", date_string.strip())

        words = [x for x in re.split(r"\W", date_string) if x]
        words = [x for x in words if not re.match(r"%s" % "|".join(skip), x)]
        return not words

    def _parse_time(self, date_string, settings):
        """Attempts to parse time part of date strings like '1 day ago, 2 PM'"""
        date_string = PATTERN.sub("", date_string)
        date_string = re.sub(r"\b(?:ago|in)\b", "", date_string)
        try:
            return time_parser(date_string)
        except Exception:
            pass

    def get_local_tz(self):
        return get_localzone()

    def parse(self, date_string, settings):
        date_string = strip_braces(date_string)
        date_string, ptz = pop_tz_offset_from_string(date_string)
        _time = self._parse_time(date_string, settings)

        _settings_tz = settings.TIMEZONE.lower()

        def apply_time(dateobj, timeobj):
            if not isinstance(_time, time):
                return dateobj

            return dateobj.replace(
                hour=timeobj.hour,
                minute=timeobj.minute,
                second=timeobj.second,
                microsecond=timeobj.microsecond,
            )

        if settings.RELATIVE_BASE:
            now = settings.RELATIVE_BASE

            if "local" not in _settings_tz:
                now = localize_timezone(now, settings.TIMEZONE)

            if ptz:
                if now.tzinfo:
                    now = now.astimezone(ptz)
                else:
                    if hasattr(ptz, "localize"):
                        now = ptz.localize(now)
                    else:
                        now = now.replace(tzinfo=ptz)

            if not now.tzinfo:
                now = now.replace(tzinfo=self.get_local_tz())

        elif ptz:
            localized_now = datetime.now(ptz)

            if "local" in _settings_tz:
                now = localized_now
            else:
                now = apply_timezone(localized_now, settings.TIMEZONE)

        else:
            if "local" not in _settings_tz:
                utc_dt = datetime.now(tz=timezone.utc)
                now = apply_timezone(utc_dt, settings.TIMEZONE)
            else:
                now = datetime.now(self.get_local_tz())

        date, period = self._parse_date(date_string, now, settings.PREFER_DATES_FROM)

        if date:
            old_date = date
            date = apply_time(date, _time)
            if settings.RETURN_TIME_AS_PERIOD and old_date != date:
                period = "time"

            if settings.TO_TIMEZONE:
                date = apply_timezone(date, settings.TO_TIMEZONE)

            if not settings.RETURN_AS_TIMEZONE_AWARE or (
                settings.RETURN_AS_TIMEZONE_AWARE
                and "default" == settings.RETURN_AS_TIMEZONE_AWARE
                and not ptz
            ):
                date = date.replace(tzinfo=None)

        return date, period

    def _parse_date(self, date_string, now, prefer_dates_from):
        if not self._are_all_words_units(date_string):
            return None, None

        kwargs = self.get_kwargs(date_string)
        if not kwargs:
            return None, None
        period = "day"
        if "days" not in kwargs:
            for k in ["weeks", "months", "years"]:
                if k in kwargs:
                    period = k[:-1]
                    break
        td = relativedelta(**kwargs)

        if (
            re.search(r"\bin\b", date_string)
            or re.search(r"\bfuture\b", prefer_dates_from)
            and not re.search(r"\bago\b", date_string)
        ):
            date = now + td
        else:
            date = now - td
        return date, period

    def get_kwargs(self, date_string):
        m = PATTERN.findall(date_string)
        if not m:
            return {}

        kwargs = {}
        for num, unit in m:
            kwargs[unit + "s"] = float(num.replace(",", "."))
        if "decades" in kwargs:
            kwargs["years"] = 10 * kwargs["decades"] + kwargs.get("years", 0)
            del kwargs["decades"]
        return kwargs

    def get_date_data(self, date_string, settings=None):
        from dateparser.date import DateData

        date, period = self.parse(date_string, settings)
        return DateData(date_obj=date, period=period)


freshness_date_parser = FreshnessDateDataParser()
