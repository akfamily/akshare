import regex as re

from dateparser.utils import get_logger


class LanguageValidator:
    logger = None

    VALID_KEYS = [
        "name",
        "skip",
        "pertain",
        "simplifications",
        "no_word_spacing",
        "ago",
        "in",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
        "year",
        "month",
        "week",
        "day",
        "hour",
        "minute",
        "second",
        "sentence_splitter_group",
    ]

    @classmethod
    def get_logger(cls):
        if cls.logger is None:
            cls.logger = get_logger()
        return cls.logger

    @classmethod
    def validate_info(cls, language_id, info):
        result = True

        result &= cls._validate_type(language_id, info)
        if not result:
            return False

        result &= cls._validate_name(language_id, info)
        result &= cls._validate_word_spacing(language_id, info)
        result &= cls._validate_skip_list(language_id, info)
        result &= cls._validate_pertain_list(language_id, info)
        result &= cls._validate_weekdays(language_id, info)
        result &= cls._validate_months(language_id, info)
        result &= cls._validate_units(language_id, info)
        result &= cls._validate_other_words(language_id, info)
        result &= cls._validate_simplifications(language_id, info)
        result &= cls._validate_extra_keys(language_id, info)
        return result

    @classmethod
    def _validate_type(cls, language_id, info):
        result = True

        if not isinstance(info, dict):
            cls.get_logger().error(
                "Language '%(id)s' info expected to be dict, but have got %(type)s",
                {"id": language_id, "type": type(info).__name__},
            )
            result = False

        return result

    @classmethod
    def _validate_name(cls, language_id, info):
        result = True

        if "name" not in info or not isinstance(info["name"], str) or not info["name"]:
            cls.get_logger().error(
                "Language '%(id)s' does not have a name", {"id": language_id}
            )
            result = False

        return result

    @classmethod
    def _validate_word_spacing(cls, language_id, info):
        if "no_word_spacing" not in info:
            return True  # Optional key

        result = True

        value = info["no_word_spacing"]
        if value not in [True, False]:
            cls.get_logger().error(
                "Invalid 'no_word_spacing' value %(value)r for '%(id)s' language: "
                "expected boolean",
                {"value": value, "id": language_id},
            )
            result = False

        return result

    @classmethod
    def _validate_sentence_splitter_group(cls, language_id, info):
        if "sentence_splitter_group" not in info:
            return True  # Optional key

        result = True

        group = info["sentence_splitter_group"]
        if isinstance(group, int) or not group:
            if group < 1 or group > 6:
                cls.get_logger().error(
                    "Invalid 'sentence_splitter_group' number %(number)r for '%(id)s' language: "
                    "expected number from 1 to 6",
                    {"number": group, "id": language_id},
                )
                result = False
        else:
            cls.get_logger().error(
                "Invalid 'sentence_splitter_group' for '%(id)s' language: "
                "expected int type but have got %(type)s",
                {"id": language_id, "type": type(group).__name__},
            )
            result = False

        return result

    @classmethod
    def _validate_skip_list(cls, language_id, info):
        if "skip" not in info:
            return True  # Optional key

        result = True

        skip_tokens_list = info["skip"]
        if isinstance(skip_tokens_list, list):
            for token in skip_tokens_list:
                if not isinstance(token, str) or not token:
                    cls.get_logger().error(
                        "Invalid 'skip' token %(token)r for '%(id)s' language: "
                        "expected not empty string",
                        {"token": token, "id": language_id},
                    )
                    result = False
        else:
            cls.get_logger().error(
                "Invalid 'skip' list for '%(id)s' language: "
                "expected list type but have got %(type)s",
                {"id": language_id, "type": type(skip_tokens_list).__name__},
            )
            result = False

        return result

    @classmethod
    def _validate_pertain_list(cls, language_id, info):
        if "pertain" not in info:
            return True  # Optional key

        result = True

        pertain_tokens_list = info["skip"]
        if isinstance(pertain_tokens_list, list):
            for token in pertain_tokens_list:
                if not isinstance(token, str) or not token:
                    cls.get_logger().error(
                        "Invalid 'pertain' token %(token)r for '%(id)s' language: "
                        "expected not empty string",
                        {"token": token, "id": language_id},
                    )
                    result = False
        else:
            cls.get_logger().error(
                "Invalid 'pertain' list for '%(id)s' language: "
                "expected list type but have got %(type)s",
                {"id": language_id, "type": type(pertain_tokens_list).__name__},
            )
            result = False

        return result

    @classmethod
    def _validate_weekdays(cls, language_id, info):
        result = True

        for weekday in (
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ):
            if weekday not in info or not info[weekday]:
                cls.get_logger().error(
                    "No translations for '%(weekday)s' provided for '%(id)s' language",
                    {"weekday": weekday, "id": language_id},
                )
                result = False
                continue

            translations_list = info[weekday]
            if isinstance(translations_list, list):
                for token in translations_list:
                    if not isinstance(token, str) or not token:
                        cls.get_logger().error(
                            "Invalid '%(weekday)s' translation %(token)r for '%(id)s' language: "
                            "expected not empty string",
                            {"weekday": weekday, "token": token, "id": language_id},
                        )
                        result = False
            else:
                cls.get_logger().error(
                    "Invalid '%(weekday)s' translations list for '%(id)s' language: "
                    "expected list type but have got %(type)s",
                    {
                        "weekday": weekday,
                        "id": language_id,
                        "type": type(translations_list).__name__,
                    },
                )
                result = False

        return result

    @classmethod
    def _validate_months(cls, language_id, info):
        result = True

        for month in (
            "january",
            "february",
            "march",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",
        ):
            if month not in info or not info[month]:
                cls.get_logger().error(
                    "No translations for '%(month)s' provided for '%(id)s' language",
                    {"month": month, "id": language_id},
                )
                result = False
                continue

            translations_list = info[month]
            if isinstance(translations_list, list):
                for token in translations_list:
                    if not isinstance(token, str) or not token:
                        cls.get_logger().error(
                            "Invalid '%(month)s' translation %(token)r for '%(id)s' language: "
                            "expected not empty string",
                            {"month": month, "token": token, "id": language_id},
                        )
                        result = False
            else:
                cls.get_logger().error(
                    "Invalid '%(month)s' translations list for '%(id)s' language: "
                    "expected list type but have got %(type)s",
                    {
                        "month": month,
                        "id": language_id,
                        "type": type(translations_list).__name__,
                    },
                )
                result = False

        return result

    @classmethod
    def _validate_units(cls, language_id, info):
        result = True

        for unit in "year", "month", "week", "day", "hour", "minute", "second":
            if unit not in info or not info[unit]:
                cls.get_logger().error(
                    "No translations for '%(unit)s' provided for '%(id)s' language",
                    {"unit": unit, "id": language_id},
                )
                result = False
                continue

            translations_list = info[unit]
            if isinstance(translations_list, list):
                for token in translations_list:
                    if not isinstance(token, str) or not token:
                        cls.get_logger().error(
                            "Invalid '%(unit)s' translation %(token)r for '%(id)s' language: "
                            "expected not empty string",
                            {"unit": unit, "token": token, "id": language_id},
                        )
                        result = False
            else:
                cls.get_logger().error(
                    "Invalid '%(unit)s' translations list for '%(id)s' language: "
                    "expected list type but have got %(type)s",
                    {
                        "unit": unit,
                        "id": language_id,
                        "type": type(translations_list).__name__,
                    },
                )
                result = False

        return result

    @classmethod
    def _validate_other_words(cls, language_id, info):
        result = True

        for word in ("ago",):
            if word not in info or not info[word]:
                cls.get_logger().error(
                    "No translations for '%(word)s' provided for '%(id)s' language",
                    {"word": word, "id": language_id},
                )
                result = False
                continue

            translations_list = info[word]
            if isinstance(translations_list, list):
                for token in translations_list:
                    if not isinstance(token, str) or not token:
                        cls.get_logger().error(
                            "Invalid '%(word)s' translation %(token)r for '%(id)s' language: "
                            "expected not empty string",
                            {"word": word, "token": token, "id": language_id},
                        )
                        result = False
            else:
                cls.get_logger().error(
                    "Invalid '%(word)s' translations list for '%(id)s' language: "
                    "expected list type but have got %(type)s",
                    {
                        "word": word,
                        "id": language_id,
                        "type": type(translations_list).__name__,
                    },
                )
                result = False

        return result

    @classmethod
    def _validate_simplifications(cls, language_id, info):
        if "simplifications" not in info:
            return True  # Optional key

        result = True

        simplifications_list = info["simplifications"]
        if isinstance(simplifications_list, list):
            for simplification in simplifications_list:
                if not isinstance(simplification, dict) or len(simplification) != 1:
                    cls.get_logger().error(
                        "Invalid simplification %(simplification)r for '%(id)s' language: "
                        "eash simplification suppose to be one-to-one mapping",
                        {"simplification": simplification, "id": language_id},
                    )
                    result = False
                    continue

                key, value = list(simplification.items())[0]
                if not isinstance(key, str) or not isinstance(value, (str, int)):
                    cls.get_logger().error(
                        "Invalid simplification %(simplification)r for '%(id)s' language: "
                        "each simplification suppose to be string-to-string-or-int mapping",
                        {"simplification": simplification, "id": language_id},
                    )
                    result = False
                    continue

                compiled_key = re.compile(key)
                value = str(value)
                replacements = re.findall(r"\\(\d+)", value)
                replacements.extend(re.findall(r"\\g<(.+?)>", value))

                groups = []
                for group in replacements:
                    if group.isdigit():
                        groups.append(int(group))
                    elif group in compiled_key.groupindex:
                        groups.append(compiled_key.groupindex[group])
                    else:
                        cls.get_logger().error(
                            "Invalid simplification %(simplification)r for '%(id)s' language: "
                            "unknown group %(group)s",
                            {
                                "simplification": simplification,
                                "id": language_id,
                                "group": group,
                            },
                        )
                        result = False

                used_groups = set(map(int, groups))
                expected_groups = set(range(0, compiled_key.groups + 1))
                extra_groups = used_groups - expected_groups
                not_used_groups = expected_groups - used_groups
                not_used_groups -= {0}  # Entire substring is not required to be used

                if extra_groups:
                    cls.get_logger().error(
                        "Invalid simplification %(simplification)r for '%(id)s' language: "
                        "unknown groups %(groups)s",
                        {
                            "simplification": simplification,
                            "id": language_id,
                            "groups": ", ".join(map(str, sorted(extra_groups))),
                        },
                    )
                    result = False

                if not_used_groups:
                    cls.get_logger().error(
                        "Invalid simplification %(simplification)r for '%(id)s' language: "
                        "groups %(groups)s were not used",
                        {
                            "simplification": simplification,
                            "id": language_id,
                            "groups": ", ".join(map(str, sorted(not_used_groups))),
                        },
                    )
                    result = False
        else:
            cls.get_logger().error(
                "Invalid 'simplifications' list for '%(id)s' language: "
                "expected list type but have got %(type)s",
                {"id": language_id, "type": type(simplifications_list).__name__},
            )
            result = False

        return result

    @classmethod
    def _validate_extra_keys(cls, language_id, info):
        result = True

        extra_keys = set(info.keys()) - set(cls.VALID_KEYS)
        if extra_keys:
            cls.get_logger().error(
                "Extra keys found for '%(id)s' language: %(keys)s",
                {"id": language_id, "keys": ", ".join(map(repr, extra_keys))},
            )
            result = False

        return result
