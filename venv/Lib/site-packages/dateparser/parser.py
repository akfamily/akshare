import calendar
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from io import StringIO

import pytz
import regex as re

from dateparser.utils import (
    _get_missing_parts,
    get_last_day_of_month,
    get_next_leap_year,
    get_previous_leap_year,
    get_timezone_from_tz_string,
    set_correct_day_from_settings,
    set_correct_month_from_settings,
)
from dateparser.utils.strptime import strptime

NSP_COMPATIBLE = re.compile(r"\D+")
MERIDIAN = re.compile(r"am|pm")
MICROSECOND = re.compile(r"\d{1,6}")
EIGHT_DIGIT = re.compile(r"^\d{8}$")
HOUR_MINUTE_REGEX = re.compile(r"^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")


def no_space_parser_eligibile(datestring):
    src = NSP_COMPATIBLE.search(datestring)
    if not src or ":" == src.group():
        return True
    return False


def get_unresolved_attrs(parser_object):
    attrs = ["year", "month", "day"]
    seen = []
    unseen = []
    for attr in attrs:
        if getattr(parser_object, attr, None) is not None:
            seen.append(attr)
        else:
            unseen.append(attr)
    return seen, unseen


date_order_chart = {
    "DMY": "%d%m%y",
    "DYM": "%d%y%m",
    "MDY": "%m%d%y",
    "MYD": "%m%y%d",
    "YDM": "%y%d%m",
    "YMD": "%y%m%d",
}


def resolve_date_order(order, lst=None):
    chart_list = {
        "DMY": ["day", "month", "year"],
        "DYM": ["day", "year", "month"],
        "MDY": ["month", "day", "year"],
        "MYD": ["month", "year", "day"],
        "YDM": ["year", "day", "month"],
        "YMD": ["year", "month", "day"],
    }

    return chart_list[order] if lst else date_order_chart[order]


def _parse_absolute(datestring, settings, tz=None):
    return _parser.parse(datestring, settings, tz)


def _parse_nospaces(datestring, settings, tz=None):
    return _no_spaces_parser.parse(datestring, settings)


class _time_parser:
    time_directives = [
        "%H:%M:%S",
        "%I:%M:%S %p",
        "%H:%M",
        "%I:%M %p",
        "%I %p",
        "%H:%M:%S.%f",
        "%I:%M:%S.%f %p",
        "%H:%M %p",
    ]

    def __call__(self, timestring):
        _timestring = timestring
        for directive in self.time_directives:
            try:
                return strptime(timestring.strip(), directive).time()
            except ValueError:
                pass
        else:
            raise ValueError("%s does not seem to be a valid time string" % _timestring)


time_parser = _time_parser()


class _no_spaces_parser:
    _dateformats = [
        "%Y%m%d",
        "%Y%d%m",
        "%m%Y%d",
        "%m%d%Y",
        "%d%Y%m",
        "%d%m%Y",
        "%y%m%d",
        "%y%d%m",
        "%m%y%d",
        "%m%d%y",
        "%d%y%m",
        "%d%m%y",
    ]

    _preferred_formats = ["%Y%m%d%H%M", "%Y%m%d%H%M%S", "%Y%m%d%H%M%S.%f"]

    _preferred_formats_ordered_8_digit = [
        "%m%d%Y",
        "%d%m%Y",
        "%Y%m%d",
        "%Y%d%m",
        "%m%Y%d",
        "%d%Y%m",
    ]

    _timeformats = ["%H%M%S.%f", "%H%M%S", "%H%M", "%H"]

    period = {"day": ["%d", "%H", "%M", "%S"], "month": ["%m"]}

    _default_order = resolve_date_order("MDY")

    def __init__(self, *args, **kwargs):
        self._all = (
            self._dateformats
            + [x + y for x in self._dateformats for y in self._timeformats]
            + self._timeformats
        )

        self.date_formats = {
            "%m%d%y": (
                self._preferred_formats
                + sorted(
                    self._all,
                    key=lambda x: x.lower().startswith("%m%d%y"),
                    reverse=True,
                )
            ),
            "%m%y%d": sorted(
                self._all, key=lambda x: x.lower().startswith("%m%y%d"), reverse=True
            ),
            "%y%m%d": sorted(
                self._all, key=lambda x: x.lower().startswith("%y%m%d"), reverse=True
            ),
            "%y%d%m": sorted(
                self._all, key=lambda x: x.lower().startswith("%y%d%m"), reverse=True
            ),
            "%d%m%y": sorted(
                self._all, key=lambda x: x.lower().startswith("%d%m%y"), reverse=True
            ),
            "%d%y%m": sorted(
                self._all, key=lambda x: x.lower().startswith("%d%y%m"), reverse=True
            ),
        }

    @classmethod
    def _get_period(cls, format_string):
        for pname, pdrv in sorted(cls.period.items(), key=lambda x: x[0]):
            for drv in pdrv:
                if drv in format_string:
                    return pname
        else:
            return "year"

    @classmethod
    def _find_best_matching_date(cls, datestring):
        for fmt in cls._preferred_formats_ordered_8_digit:
            try:
                dt = strptime(datestring, fmt), cls._get_period(fmt)
                if len(str(dt[0].year)) == 4:
                    return dt
            except Exception:
                pass
        return None

    @classmethod
    def parse(cls, datestring, settings):
        if not no_space_parser_eligibile(datestring):
            raise ValueError("Unable to parse date from: %s" % datestring)

        datestring = datestring.replace(":", "")
        if not datestring:
            raise ValueError("Empty string")
        tokens = tokenizer(datestring)
        if settings.DATE_ORDER:
            order = resolve_date_order(settings.DATE_ORDER)
        else:
            order = cls._default_order
            if EIGHT_DIGIT.match(datestring):
                dt = cls._find_best_matching_date(datestring)
                if dt is not None:
                    return dt
        nsp = cls()
        ambiguous_date = None
        for token, _ in tokens.tokenize():
            for fmt in nsp.date_formats[order]:
                try:
                    dt = strptime(token, fmt), cls._get_period(fmt)
                    if len(str(dt[0].year)) < 4:
                        ambiguous_date = dt
                        continue

                    missing = _get_missing_parts(fmt)
                    _check_strict_parsing(missing, settings)
                    return dt
                except Exception:
                    pass
        else:
            if ambiguous_date:
                return ambiguous_date
            else:
                raise ValueError("Unable to parse date from: %s" % datestring)


def _get_missing_error(missing):
    return "Fields missing from the date string: {}".format(", ".join(missing))


def _check_strict_parsing(missing, settings):
    if settings.STRICT_PARSING and missing:
        raise ValueError(_get_missing_error(missing))
    elif settings.REQUIRE_PARTS and missing:
        errors = [part for part in settings.REQUIRE_PARTS if part in missing]
        if errors:
            raise ValueError(_get_missing_error(errors))


class _parser:
    alpha_directives = OrderedDict(
        [
            ("weekday", ["%A", "%a"]),
            ("month", ["%B", "%b"]),
        ]
    )

    num_directives = {
        "month": ["%m"],
        "day": ["%d"],
        "year": ["%y", "%Y"],
    }

    def __init__(self, tokens, settings):
        self.settings = settings
        self.tokens = [(t[0].strip(), t[1]) for t in list(tokens)]
        self.filtered_tokens = [
            (t[0], t[1], i) for i, t in enumerate(self.tokens) if t[1] <= 1
        ]

        self.unset_tokens = []

        self.day = None
        self.month = None
        self.year = None
        self.time = None

        self.auto_order = []

        self._token_day = None
        self._token_month = None
        self._token_year = None
        self._token_time = None

        self.ordered_num_directives = OrderedDict(
            (k, self.num_directives[k])
            for k in (resolve_date_order(settings.DATE_ORDER, lst=True))
        )

        skip_index = []
        skip_component = None
        skip_tokens = ["t", "year", "hour", "minute"]

        for index, token_type_original_index in enumerate(self.filtered_tokens):
            if index in skip_index:
                continue

            token, type, original_index = token_type_original_index

            if token in skip_tokens:
                continue

            if self.time is None:
                meridian_index = index + 1

                try:
                    # try case where hours and minutes are separated by a period. Example: 13.20.
                    _is_before_period = self.tokens[original_index + 1][0] == "."
                    _is_after_period = (
                        original_index != 0
                        and self.tokens[original_index - 1][0] == "."
                    )

                    if _is_before_period and not _is_after_period:
                        index_next_token = index + 1
                        next_token = self.filtered_tokens[index_next_token][0]
                        index_in_tokens_for_next_token = self.filtered_tokens[
                            index_next_token
                        ][2]

                        next_token_is_last = (
                            index_next_token == len(self.filtered_tokens) - 1
                        )
                        if (
                            next_token_is_last
                            or self.tokens[index_in_tokens_for_next_token + 1][0] != "."
                        ):
                            new_token = token + ":" + next_token
                            if re.match(HOUR_MINUTE_REGEX, new_token):
                                token = new_token
                                skip_index.append(index + 1)
                                meridian_index += 1
                except Exception:
                    pass

                try:
                    microsecond = MICROSECOND.search(
                        self.filtered_tokens[index + 1][0]
                    ).group()
                    # Is after time token? raise ValueError if ':' can't be found:
                    token.index(":")
                    # Is after period? raise ValueError if '.' can't be found:
                    self.tokens[self.tokens.index((token, 0)) + 1][0].index(".")
                except Exception:
                    microsecond = None

                if microsecond:
                    meridian_index += 1

                try:
                    meridian = MERIDIAN.search(
                        self.filtered_tokens[meridian_index][0]
                    ).group()
                except Exception:
                    meridian = None

                if any([":" in token, meridian, microsecond]):
                    if meridian and not microsecond:
                        self._token_time = "%s %s" % (token, meridian)
                        skip_index.append(meridian_index)
                    elif microsecond and not meridian:
                        self._token_time = "%s.%s" % (token, microsecond)
                        skip_index.append(index + 1)
                    elif meridian and microsecond:
                        self._token_time = "%s.%s %s" % (token, microsecond, meridian)
                        skip_index.append(index + 1)
                        skip_index.append(meridian_index)
                    else:
                        self._token_time = token
                    self.time = lambda: time_parser(self._token_time)
                    continue

            results = self._parse(type, token, skip_component=skip_component)
            for res in results:
                if len(token) == 4 and res[0] == "year":
                    skip_component = "year"
                setattr(self, *res)

        known, unknown = get_unresolved_attrs(self)
        params = {}
        for attr in known:
            params.update({attr: getattr(self, attr)})
        for attr in unknown:
            for token, type, _ in self.unset_tokens:
                if type == 0:
                    params.update({attr: int(token)})
                    setattr(self, "_token_%s" % attr, token)
                    setattr(self, attr, int(token))

    def _get_period(self):
        if self.settings.RETURN_TIME_AS_PERIOD:
            if getattr(self, "time", None):
                return "time"

        for period in ["time", "day"]:
            if getattr(self, period, None):
                return "day"

        for period in ["month", "year"]:
            if getattr(self, period, None):
                return period

        if self._results():
            return "day"

    def _get_datetime_obj(self, **params):
        try:
            return datetime(**params)
        except ValueError as e:
            error_text = e.__str__()
            error_msgs = ["day is out of range", "day must be in"]
            if error_msgs[0] in error_text or error_msgs[1] in error_text:
                if not (self._token_day or hasattr(self, "_token_weekday")):
                    # if day is not available put last day of the month
                    params["day"] = get_last_day_of_month(
                        params["year"], params["month"]
                    )
                    return datetime(**params)
                elif (
                    not self._token_year
                    and params["day"] == 29
                    and params["month"] == 2
                    and not calendar.isleap(params["year"])
                ):
                    # fix the year when year is not present and it is 29 of February
                    params["year"] = self._get_correct_leap_year(
                        self.settings.PREFER_DATES_FROM, params["year"]
                    )
                    return datetime(**params)
            raise e

    def _get_correct_leap_year(self, prefer_dates_from, current_year):
        if prefer_dates_from == "future":
            return get_next_leap_year(current_year)
        if prefer_dates_from == "past":
            return get_previous_leap_year(current_year)

        # Default case ('current_period'): return closer leap year
        next_leap_year = get_next_leap_year(current_year)
        previous_leap_year = get_previous_leap_year(current_year)
        next_leap_year_is_closer = (
            next_leap_year - current_year < current_year - previous_leap_year
        )
        return next_leap_year if next_leap_year_is_closer else previous_leap_year

    def _set_relative_base(self):
        self.now = self.settings.RELATIVE_BASE
        if not self.now:
            self.now = datetime.now(tz=timezone.utc).replace(tzinfo=None)

    def _get_datetime_obj_params(self):
        if not self.now:
            self._set_relative_base()

        params = {
            "day": self.day or self.now.day,
            "month": self.month or self.now.month,
            "year": self.year or self.now.year,
            "hour": 0,
            "minute": 0,
            "second": 0,
            "microsecond": 0,
        }
        return params

    def _get_date_obj(self, token, directive):
        return strptime(token, directive)

    def _results(self):
        missing = [
            field for field in ("day", "month", "year") if not getattr(self, field)
        ]
        _check_strict_parsing(missing, self.settings)
        self._set_relative_base()

        time = self.time() if self.time is not None else None
        params = self._get_datetime_obj_params()

        if time:
            params.update(
                dict(
                    hour=time.hour,
                    minute=time.minute,
                    second=time.second,
                    microsecond=time.microsecond,
                )
            )

        return self._get_datetime_obj(**params)

    def _correct_for_time_frame(self, dateobj, tz):
        days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

        token_weekday, _ = getattr(self, "_token_weekday", (None, None))

        if token_weekday and not (
            self._token_year or self._token_month or self._token_day
        ):
            day_index = calendar.weekday(dateobj.year, dateobj.month, dateobj.day)
            day = token_weekday[:3].lower()
            steps = 0
            if "future" in self.settings.PREFER_DATES_FROM:
                if days[day_index] == day:
                    steps = 7
                else:
                    while days[day_index] != day:
                        day_index = (day_index + 1) % 7
                        steps += 1
                delta = timedelta(days=steps)
            else:
                if days[day_index] == day:
                    if self.settings.PREFER_DATES_FROM == "past":
                        steps = 7
                    else:
                        steps = 0
                else:
                    while days[day_index] != day:
                        day_index -= 1
                        steps += 1
                delta = timedelta(days=-steps)

            dateobj = dateobj + delta

        # NOTE: If this assert fires, self.now needs to be made offset-aware in a similar
        # way that dateobj is temporarily made offset-aware.
        assert not (self.now.tzinfo is None and dateobj.tzinfo is not None), (
            "`self.now` doesn't have `tzinfo`. Review comment in code for details."
        )

        # Store the original dateobj values so that upon subsequent parsing everything is not
        # treated as offset-aware if offset awareness is changed.
        original_dateobj = dateobj

        # Since date comparisons must be either offset-naive or offset-aware, normalize dateobj
        # to be offset-aware if one or the other is already offset-aware.
        if self.now.tzinfo is not None and dateobj.tzinfo is None:
            dateobj = pytz.utc.localize(dateobj)

        if self.month and not self.year:
            try:
                if self.now < dateobj:
                    if self.settings.PREFER_DATES_FROM == "past":
                        dateobj = dateobj.replace(year=dateobj.year - 1)
                else:
                    if self.settings.PREFER_DATES_FROM == "future":
                        dateobj = dateobj.replace(year=dateobj.year + 1)
            except ValueError as e:
                if dateobj.day == 29 and dateobj.month == 2:
                    valid_year = self._get_correct_leap_year(
                        self.settings.PREFER_DATES_FROM, dateobj.year
                    )
                    dateobj = dateobj.replace(year=valid_year)
                else:
                    raise e

        if self._token_year and len(self._token_year[0]) == 2:
            if self.now < dateobj:
                if "past" in self.settings.PREFER_DATES_FROM:
                    dateobj = dateobj.replace(year=dateobj.year - 100)
            else:
                if "future" in self.settings.PREFER_DATES_FROM:
                    dateobj = dateobj.replace(year=dateobj.year + 100)

        if self._token_time and not any(
            [
                self._token_year,
                self._token_month,
                self._token_day,
                hasattr(self, "_token_weekday"),
            ]
        ):
            # Convert dateobj to utc time to compare with self.now
            try:
                tz = tz or get_timezone_from_tz_string(self.settings.TIMEZONE)
                tz_offset = tz.utcoffset(dateobj)
            except (pytz.UnknownTimeZoneError, pytz.NonExistentTimeError):
                tz_offset = timedelta(hours=0)

            if "past" in self.settings.PREFER_DATES_FROM:
                if self.now < dateobj - tz_offset:
                    dateobj = dateobj + timedelta(days=-1)
            if "future" in self.settings.PREFER_DATES_FROM:
                if self.now > dateobj - tz_offset:
                    dateobj = dateobj + timedelta(days=1)

        # Reset dateobj to the original value, thus removing any offset awareness that may
        # have been set earlier.
        dateobj = dateobj.replace(tzinfo=original_dateobj.tzinfo)

        return dateobj

    def _correct_for_day(self, dateobj):
        if (
            getattr(self, "_token_day", None)
            or getattr(self, "_token_weekday", None)
            or getattr(self, "_token_time", None)
        ):
            return dateobj

        dateobj = set_correct_day_from_settings(
            dateobj, self.settings, current_day=self.now.day
        )
        return dateobj

    def _correct_for_month(self, dateobj):
        relative_base = getattr(self.settings, "RELATIVE_BASE", None)
        relative_base_month = (
            relative_base.month if hasattr(relative_base, "month") else relative_base
        )

        if getattr(self, "_token_month", None):
            return dateobj

        dateobj = set_correct_month_from_settings(
            dateobj, self.settings, relative_base_month
        )
        return dateobj

    @classmethod
    def parse(cls, datestring, settings, tz=None):
        tokens = tokenizer(datestring)
        po = cls(tokens.tokenize(), settings)
        dateobj = po._results()

        # correction for past, future if applicable
        dateobj = po._correct_for_time_frame(dateobj, tz)

        # correction for preference of month: beginning, current, end
        # must happen before day so that day is derived from the correct month
        dateobj = po._correct_for_month(dateobj)

        # correction for preference of day: beginning, current, end
        dateobj = po._correct_for_day(dateobj)

        period = po._get_period()

        return dateobj, period

    def _parse(self, type, token, skip_component=None):
        def set_and_return(token, type, component, dateobj, skip_date_order=False):
            if not skip_date_order:
                self.auto_order.append(component)
            setattr(self, "_token_%s" % component, (token, type))
            return [(component, getattr(dateobj, component))]

        def parse_number(token, skip_component=None):
            type = 0

            for component, directives in self.ordered_num_directives.items():
                if skip_component == component:
                    continue
                for directive in directives:
                    try:
                        do = self._get_date_obj(token, directive)
                        prev_value = getattr(self, component, None)
                        if not prev_value:
                            return set_and_return(token, type, component, do)
                        else:
                            try:
                                prev_token, prev_type = getattr(
                                    self, "_token_%s" % component
                                )
                                if prev_type == type:
                                    do = self._get_date_obj(prev_token, directive)
                            except ValueError:
                                self.unset_tokens.append(
                                    (prev_token, prev_type, component)
                                )
                                return set_and_return(token, type, component, do)
                    except ValueError:
                        pass
            else:
                raise ValueError("Unable to parse: %s" % token)

        def parse_alpha(token, skip_component=None):
            type = 1

            for component, directives in self.alpha_directives.items():
                if skip_component == component:
                    continue
                for directive in directives:
                    try:
                        do = self._get_date_obj(token, directive)
                        prev_value = getattr(self, component, None)
                        if not prev_value:
                            return set_and_return(
                                token, type, component, do, skip_date_order=True
                            )
                        elif component == "month":
                            index = self.auto_order.index("month")
                            self.auto_order[index] = "day"
                            setattr(self, "_token_day", self._token_month)
                            setattr(self, "_token_month", (token, type))
                            return [
                                (component, getattr(do, component)),
                                ("day", prev_value),
                            ]
                    except Exception:
                        pass
            else:
                raise ValueError("Unable to parse: %s" % token)

        handlers = {0: parse_number, 1: parse_alpha}
        return handlers[type](token, skip_component)


class tokenizer:
    digits = "0123456789:"
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def _isletter(self, tkn):
        return tkn in self.letters

    def _isdigit(self, tkn):
        return tkn in self.digits

    def __init__(self, ds):
        self.instream = StringIO(ds)

    def _switch(self, chara, charb):
        if self._isdigit(chara):
            return 0, not self._isdigit(charb)

        if self._isletter(chara):
            return 1, not self._isletter(charb)

        return 2, self._isdigit(charb) or self._isletter(charb)

    def tokenize(self):
        token = ""
        EOF = False

        while not EOF:
            nextchar = self.instream.read(1)

            if not nextchar:
                EOF = True
                type, _ = self._switch(token[-1], nextchar)
                yield token, type
                return

            if token:
                type, switch = self._switch(token[-1], nextchar)

                if not switch:
                    token += nextchar
                else:
                    yield token, type
                    token = nextchar
            else:
                token += nextchar
