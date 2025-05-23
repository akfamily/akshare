import re
from collections import OrderedDict
from functools import reduce

from convertdate import persian

from dateparser.calendars import non_gregorian_parser


class PersianDate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def weekday(self):
        for week in persian.monthcalendar(self.year, self.month):
            for idx, day in enumerate(week):
                if day == self.day:
                    return idx


class jalali_parser(non_gregorian_parser):
    calendar_converter = persian
    default_year = 1348
    default_month = 1
    default_day = 1
    non_gregorian_date_cls = PersianDate

    _digits = {
        "۰": 0,
        "۱": 1,
        "۲": 2,
        "۳": 3,
        "۴": 4,
        "۵": 5,
        "۶": 6,
        "۷": 7,
        "۸": 8,
        "۹": 9,
    }

    _months = OrderedDict(
        [
            # pinglish : (persian literals, month index, number of days)
            ("Farvardin", (1, 31, ["فروردین"])),
            ("Ordibehesht", (2, 31, ["اردیبهشت"])),
            ("Khordad", (3, 31, ["خرداد"])),
            ("Tir", (4, 31, ["تیر"])),
            ("Mordad", (5, 31, ["امرداد", "مرداد"])),
            ("Shahrivar", (6, 31, ["شهریور", "شهريور"])),
            ("Mehr", (7, 30, ["مهر"])),
            ("Aban", (8, 30, ["آبان"])),
            ("Azar", (9, 30, ["آذر"])),
            ("Dey", (10, 30, ["دی"])),
            ("Bahman", (11, 30, ["بهمن", "بهن"])),
            ("Esfand", (12, 29, ["اسفند"])),
        ]
    )

    _weekdays = OrderedDict(
        [
            ("Sunday", ["یکشنبه"]),
            ("Monday", ["دوشنبه"]),
            ("Tuesday", ["سهشنبه", "سه شنبه"]),
            ("Wednesday", ["چهارشنبه", "چهار شنبه"]),
            ("Thursday", ["پنجشنبه", "پنج شنبه"]),
            ("Friday", ["جمعه"]),
            ("Saturday", ["روز شنبه", "شنبه"]),
        ]
    )

    _number_letters = {
        0: ["صفر"],
        1: ["یک", "اول"],
        2: ["دو"],
        3: ["سه", "سو"],
        4: ["چهار"],
        5: ["پنج"],
        6: ["شش"],
        7: ["هفت"],
        8: ["هشت"],
        9: ["نه"],
        10: ["ده"],
        11: ["یازده"],
        12: ["دوازده"],
        13: ["سیزده"],
        14: ["چهارده"],
        15: ["پانزده"],
        16: ["شانزده"],
        17: ["هفده"],
        18: ["هجده"],
        19: ["نوزده"],
        20: ["بیست"],
        21: ["بیست و یک"],
        22: ["بیست و دو", "بیست ثانیه"],
        23: ["بیست و سه", "بیست و سو"],
        24: ["بیست و چهار"],
        25: ["بیست و پنج"],
        26: ["بیست و شش"],
        27: ["بیست و هفت"],
        28: ["بیست و هشت"],
        29: ["بیست و نه"],
        30: ["سی"],
        31: ["سی و یک"],
    }

    @classmethod
    def _replace_digits(cls, source):
        result = source
        for pers_digit, number in cls._digits.items():
            result = result.replace(pers_digit, str(number))
        return result

    @classmethod
    def _replace_months(cls, source):
        result = source
        for pers, latin in reduce(
            lambda a, b: a + b,
            [
                [(value, month) for value in repl[-1]]
                for month, repl in cls._months.items()
            ],
        ):
            result = result.replace(pers, latin)
        return result

    @classmethod
    def _replace_weekdays(cls, source):
        result = source
        for pers, latin in reduce(
            lambda a, b: a + b,
            [
                [(value, weekday) for value in repl]
                for weekday, repl in cls._weekdays.items()
            ],
        ):
            result = result.replace(pers, latin)
        return result

    @classmethod
    def _replace_time(cls, source):
        def only_numbers(match_obj):
            matched_string = match_obj.group()
            return re.sub(r"\D", " ", matched_string)

        hour_pattern = r"ساعت\s+\d{2}"
        minute_pattern = r"\d{2}\s+دقیقه"
        second_pattern = r"\d{2}\s+ثانیه"
        result = re.sub(hour_pattern, only_numbers, source)
        result = re.sub(minute_pattern, only_numbers, result)
        result = re.sub(second_pattern, only_numbers, result)
        result = re.sub(r"\s+و\s+", ":", result)
        result = result.replace("ساعت", "")
        return result

    @classmethod
    def _replace_days(cls, source):
        result = re.sub(
            r"ام|م|ین", "", source
        )  # removes persian variant of th/first/second/third
        day_pairs = list(cls._number_letters.items())

        def comp_key(tup):
            return tup[0]

        day_pairs.sort(key=comp_key, reverse=True)

        thirteen, thirty = day_pairs[-14], day_pairs[1]
        day_pairs[-14] = thirty
        day_pairs[1] = thirteen

        for persian_number, number in reduce(
            lambda a, b: a + b,
            [[(val, repl) for val in persian_word] for repl, persian_word in day_pairs],
        ):
            result = result.replace(persian_number, str(number))
        return result

    def handle_two_digit_year(self, year):
        if year > 60:
            return year + 1300
        else:
            return year + 1400
