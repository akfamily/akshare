from dateparser.calendars.jalali_parser import jalali_parser

from . import CalendarBase


class JalaliCalendar(CalendarBase):
    """Calendar class for Jalali calendar."""

    parser = jalali_parser
