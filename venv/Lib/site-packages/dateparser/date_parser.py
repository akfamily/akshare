import sys

from tzlocal import get_localzone

from .conf import apply_settings
from .timezone_parser import pop_tz_offset_from_string
from .utils import apply_timezone, localize_timezone, strip_braces


class DateParser:
    @apply_settings
    def parse(self, date_string, parse_method, settings=None):
        date_string = str(date_string)

        if not date_string.strip():
            raise ValueError("Empty string")

        date_string = strip_braces(date_string)
        date_string, ptz = pop_tz_offset_from_string(date_string)

        date_obj, period = parse_method(date_string, settings=settings, tz=ptz)

        _settings_tz = settings.TIMEZONE.lower()

        if ptz:
            if hasattr(ptz, "localize"):
                date_obj = ptz.localize(date_obj)
            else:
                date_obj = date_obj.replace(tzinfo=ptz)
            if "local" not in _settings_tz:
                date_obj = apply_timezone(date_obj, settings.TIMEZONE)
        else:
            if "local" in _settings_tz:
                stz = get_localzone()
                if hasattr(stz, "localize") and sys.version_info < (3, 6):
                    date_obj = stz.localize(date_obj)
                else:
                    date_obj = date_obj.replace(tzinfo=stz)
            else:
                date_obj = localize_timezone(date_obj, settings.TIMEZONE)

        if settings.TO_TIMEZONE:
            date_obj = apply_timezone(date_obj, settings.TO_TIMEZONE)

        if not settings.RETURN_AS_TIMEZONE_AWARE or (
            settings.RETURN_AS_TIMEZONE_AWARE
            and "default" == settings.RETURN_AS_TIMEZONE_AWARE
            and not ptz
        ):
            date_obj = date_obj.replace(tzinfo=None)

        return date_obj, period


date_parser = DateParser()
