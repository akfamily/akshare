from collections import OrderedDict
from copy import deepcopy
from importlib import import_module
from itertools import zip_longest

import regex as re

from ..data import language_locale_dict, language_order
from .locale import Locale

LOCALE_SPLIT_PATTERN = re.compile(r"-(?=[A-Z0-9]+$)")


def _isvalidlocale(locale):
    language = LOCALE_SPLIT_PATTERN.split(locale)[0]
    if language not in language_order:
        return False
    else:
        locales_list = language_locale_dict[language]
        if locale == language or locale in locales_list:
            return True
        else:
            return False


def _filter_valid_locales(locales):
    return [locale for locale in locales if _isvalidlocale(locale)]


def _construct_locales(languages, region):
    if region:
        possible_locales = [language + "-" + region for language in languages]
        locales = _filter_valid_locales(possible_locales)
    else:
        locales = languages
    return locales


class LocaleDataLoader:
    """Class that handles loading of locale instances."""

    _loaded_languages = {}
    _loaded_locales = {}

    def get_locale_map(
        self,
        languages=None,
        locales=None,
        region=None,
        use_given_order=False,
        allow_conflicting_locales=False,
    ):
        """
        Get an ordered mapping with locale codes as keys
        and corresponding locale instances as values.

        :param languages:
            A list of language codes, e.g. ['en', 'es', 'zh-Hant'].
            If locales are not given, languages and region are
            used to construct locales to load.
        :type languages: list

        :param locales:
            A list of codes of locales which are to be loaded,
            e.g. ['fr-PF', 'qu-EC', 'af-NA']
        :type locales: list

        :param region:
            A region code, e.g. 'IN', '001', 'NE'.
            If locales are not given, languages and region are
            used to construct locales to load.
        :type region: str

        :param use_given_order:
            If True, the returned mapping is ordered in the order locales are given.
        :type use_given_order: bool

        :param allow_conflicting_locales:
            if True, locales with same language and different region can be loaded.
        :type allow_conflicting_locales: bool

        :return: ordered locale code to locale instance mapping
        """
        return OrderedDict(
            self._load_data(
                languages=languages,
                locales=locales,
                region=region,
                use_given_order=use_given_order,
                allow_conflicting_locales=allow_conflicting_locales,
            )
        )

    def get_locales(
        self,
        languages=None,
        locales=None,
        region=None,
        use_given_order=False,
        allow_conflicting_locales=False,
    ):
        """
        Yield locale instances.

        :param languages:
            A list of language codes, e.g. ['en', 'es', 'zh-Hant'].
            If locales are not given, languages and region are
            used to construct locales to load.
        :type languages: list

        :param locales:
            A list of codes of locales which are to be loaded,
            e.g. ['fr-PF', 'qu-EC', 'af-NA']
        :type locales: list

        :param region:
            A region code, e.g. 'IN', '001', 'NE'.
            If locales are not given, languages and region are
            used to construct locales to load.
        :type region: str

        :param use_given_order:
            If True, the returned mapping is ordered in the order locales are given.
        :type use_given_order: bool

        :param allow_conflicting_locales:
            if True, locales with same language and different region can be loaded.
        :type allow_conflicting_locales: bool

        :yield: locale instances
        """
        for _, locale in self._load_data(
            languages=languages,
            locales=locales,
            region=region,
            use_given_order=use_given_order,
            allow_conflicting_locales=allow_conflicting_locales,
        ):
            yield locale

    def get_locale(self, shortname):
        """
        Get a locale instance.

        :param shortname:
            A locale code, e.g. 'fr-PF', 'qu-EC', 'af-NA'.
        :type shortname: str

        :return: locale instance
        """
        return list(self.get_locales(locales=[shortname]))[0]

    def _load_data(
        self,
        languages=None,
        locales=None,
        region=None,
        use_given_order=False,
        allow_conflicting_locales=False,
    ):
        locale_dict = OrderedDict()
        if locales:
            invalid_locales = []
            for locale in locales:
                lang_reg = LOCALE_SPLIT_PATTERN.split(locale)
                if len(lang_reg) == 1:
                    lang_reg.append("")
                locale_dict[locale] = tuple(lang_reg)
                if not _isvalidlocale(locale):
                    invalid_locales.append(locale)
            if invalid_locales:
                raise ValueError(
                    "Unknown locale(s): %s" % ", ".join(map(repr, invalid_locales))
                )

            if not allow_conflicting_locales:
                if len(set(locales)) > len({t[0] for t in locale_dict.values()}):
                    raise ValueError(
                        "Locales should not have same language and different region"
                    )

        else:
            if languages is None:
                languages = language_order
            unsupported_languages = set(languages) - set(language_order)
            if unsupported_languages:
                raise ValueError(
                    "Unknown language(s): %s"
                    % ", ".join(map(repr, unsupported_languages))
                )
            if region is None:
                region = ""
            locales = _construct_locales(languages, region)
            locale_dict.update(
                zip_longest(
                    locales, tuple(zip_longest(languages, [], fillvalue=region))
                )
            )

        if not use_given_order:
            locale_dict = OrderedDict(
                sorted(locale_dict.items(), key=lambda x: language_order.index(x[1][0]))
            )

        for shortname, lang_reg in locale_dict.items():
            if shortname not in self._loaded_locales:
                lang, reg = lang_reg
                if lang in self._loaded_languages:
                    locale = Locale(
                        shortname, language_info=deepcopy(self._loaded_languages[lang])
                    )
                    self._loaded_locales[shortname] = locale
                else:
                    language_info = getattr(
                        import_module("dateparser.data.date_translation_data." + lang),
                        "info",
                    )
                    locale = Locale(shortname, language_info=deepcopy(language_info))
                    self._loaded_languages[lang] = language_info
                    self._loaded_locales[shortname] = locale
            yield shortname, self._loaded_locales[shortname]


default_loader = LocaleDataLoader()
