from collections import OrderedDict
from itertools import chain

import regex as re
from dateutil import parser

from dateparser.timezone_parser import pop_tz_offset_from_string, word_is_tz
from dateparser.utils import combine_dicts, normalize_unicode

from .dictionary import ALWAYS_KEEP_TOKENS, Dictionary, NormalizedDictionary

NUMERAL_PATTERN = re.compile(r"(\d+)", re.U)


class Locale:
    """
    Class that deals with applicability and translation from a locale.

    :param shortname:
        A locale code, e.g. 'fr-PF', 'qu-EC', 'af-NA'.
    :type shortname: str

    :param language_info:
        Language info (translation data) of the language the locale belongs to.
    :type language_info: dict

    :return: A Locale instance
    """

    _dictionary = None
    _normalized_dictionary = None
    _simplifications = None
    _normalized_simplifications = None
    _splitters = None
    _wordchars = None
    _relative_translations = None
    _normalized_relative_translations = None
    _abbreviations = None
    _split_dictionary = None
    _wordchars_for_detection = None

    def __init__(self, shortname, language_info):
        self.shortname = shortname
        locale_specific_info = language_info.get("locale_specific", {}).get(
            shortname, {}
        )
        self.info = combine_dicts(language_info, locale_specific_info)
        self.info.pop("locale_specific", None)

    def is_applicable(self, date_string, strip_timezone=False, settings=None):
        """
        Check if the locale is applicable to translate date string.

        :param date_string:
            A string representing date and/or time in a recognizably valid format.
        :type date_string: str

        :param strip_timezone:
            If True, timezone is stripped from date string.
        :type strip_timezone: bool

        :return: boolean value representing if the locale is applicable for the date string or not.
        """
        if strip_timezone:
            date_string, _ = pop_tz_offset_from_string(date_string, as_offset=False)

        date_string = self._translate_numerals(date_string)
        if settings.NORMALIZE:
            date_string = normalize_unicode(date_string)
        date_string = self._simplify(date_string, settings=settings)
        dictionary = self._get_dictionary(settings)
        date_tokens = dictionary.split(date_string)
        return dictionary.are_tokens_valid(date_tokens)

    def count_applicability(self, text, strip_timezone=False, settings=None):
        if strip_timezone:
            text, _ = pop_tz_offset_from_string(text, as_offset=False)

        text = self._simplify(text, settings=settings)
        sentences = self._sentence_split(text, settings=settings)
        tokens = []
        for sent in sentences:
            tokens.extend(self._split(sent, keep_formatting=False, settings=settings))
        return self._count_words_present_in_the_dictionary(tokens, settings)

    def _count_words_present_in_the_dictionary(self, words, settings=None):
        dictionary = self.clean_dictionary(
            self._get_split_dictionary(settings=settings)
        )
        dict_cnt = 0
        skip_cnt = 0
        for word in set(words):
            if word in dictionary:
                if dictionary[word]:
                    dict_cnt += 1
                else:
                    skip_cnt += 1
            elif word.isdigit():
                skip_cnt += 1
        return [dict_cnt, skip_cnt]

    @staticmethod
    def clean_dictionary(dictionary, threshold=2):
        del_keys = []
        for key in dictionary:
            if len(key) < threshold:
                del_keys.append(key)
        for del_key in del_keys:
            del dictionary[del_key]
        return dictionary

    def translate(self, date_string, keep_formatting=False, settings=None):
        """
        Translate the date string to its English equivalent.

        :param date_string:
            A string representing date and/or time in a recognizably valid format.
        :type date_string: str

        :param keep_formatting:
            If True, retain formatting of the date string after translation.
        :type keep_formatting: bool

        :return: translated date string.
        """
        date_string = self._translate_numerals(date_string)
        if settings.NORMALIZE:
            date_string = normalize_unicode(date_string)
        date_string = self._simplify(date_string, settings=settings)
        dictionary = self._get_dictionary(settings)
        date_string_tokens = dictionary.split(date_string, keep_formatting)

        relative_translations = self._get_relative_translations(settings=settings)

        for i, word in enumerate(date_string_tokens):
            word = word.lower()
            for pattern, replacement in relative_translations.items():
                if pattern.match(word):
                    date_string_tokens[i] = pattern.sub(replacement, word)
                    break
            else:
                if word in dictionary:
                    fallback = word if keep_formatting and not word.isalpha() else ""
                    date_string_tokens[i] = dictionary[word] or fallback
        if "in" in date_string_tokens:
            date_string_tokens = self._clear_future_words(date_string_tokens)

        return self._join(
            list(filter(bool, date_string_tokens)),
            separator="" if keep_formatting else " ",
            settings=settings,
        )

    def _translate_numerals(self, date_string):
        date_string_tokens = NUMERAL_PATTERN.split(date_string)
        for i, token in enumerate(date_string_tokens):
            if token.isdecimal():
                date_string_tokens[i] = str(int(token)).zfill(len(token))
        return "".join(date_string_tokens)

    def _get_relative_translations(self, settings=None):
        if settings.NORMALIZE:
            if self._normalized_relative_translations is None:
                self._normalized_relative_translations = (
                    self._generate_relative_translations(normalize=True)
                )
            return self._normalized_relative_translations
        else:
            if self._relative_translations is None:
                self._relative_translations = self._generate_relative_translations(
                    normalize=False
                )
            return self._relative_translations

    def _generate_relative_translations(self, normalize=False):
        relative_translations = self.info.get("relative-type-regex", {})
        relative_dictionary = OrderedDict()
        for key, value in relative_translations.items():
            if normalize:
                value = list(map(normalize_unicode, value))
            pattern = "|".join(sorted(value, key=len, reverse=True))
            pattern = pattern.replace(r"(\d+", r"(?P<n>\d+")
            pattern = re.compile(
                r"^(?:{})$".format(pattern), re.UNICODE | re.IGNORECASE
            )
            relative_dictionary[pattern] = key
        return relative_dictionary

    def translate_search(self, search_string, settings=None):
        dashes = ["-", "——", "—", "～"]
        word_joint_unsupported_languages = ["zh", "ja"]
        sentences = self._sentence_split(search_string, settings=settings)
        dictionary = self._get_dictionary(settings=settings)
        translated = []
        original = []
        for sentence in sentences:
            original_tokens, simplified_tokens = self._simplify_split_align(
                sentence, settings=settings
            )
            translated_chunk = []
            original_chunk = []
            last_token_index = len(simplified_tokens) - 1
            skip_next_token = False
            for i, word in enumerate(simplified_tokens):
                next_word = simplified_tokens[i + 1] if i < last_token_index else ""
                current_and_next_joined = self._join_chunk(
                    [word, next_word], settings=settings
                )
                if skip_next_token:
                    skip_next_token = False
                    continue

                if word == "" or word == " ":
                    translated_chunk.append(word)
                    original_chunk.append(original_tokens[i])
                elif (
                    current_and_next_joined in dictionary
                    and word not in dashes
                    and self.shortname not in word_joint_unsupported_languages
                ):
                    translated_chunk.append(dictionary[current_and_next_joined])
                    original_chunk.append(
                        self._join_chunk(
                            [original_tokens[i], original_tokens[i + 1]],
                            settings=settings,
                        )
                    )
                    skip_next_token = True
                elif word in dictionary and word not in dashes:
                    translated_chunk.append(dictionary[word])
                    original_chunk.append(original_tokens[i])
                elif word.strip("()\"'{}[],.،") in dictionary and word not in dashes:
                    punct = word[len(word.strip("()\"'{}[],.،")) :]
                    if punct and dictionary[word.strip("()\"'{}[],.،")]:
                        translated_chunk.append(
                            dictionary[word.strip("()\"'{}[],.،")] + punct
                        )
                    else:
                        translated_chunk.append(dictionary[word.strip("()\"'{}[],.،")])
                    original_chunk.append(original_tokens[i])
                elif self._token_with_digits_is_ok(word):
                    translated_chunk.append(word)
                    original_chunk.append(original_tokens[i])
                # Use original token because word_is_tz is case sensitive
                elif translated_chunk and word_is_tz(original_tokens[i]):
                    translated_chunk.append(word)
                    original_chunk.append(original_tokens[i])
                else:
                    if translated_chunk:
                        translated.append(translated_chunk)
                        translated_chunk = []
                        original.append(original_chunk)
                        original_chunk = []
            if translated_chunk:
                translated.append(translated_chunk)
                original.append(original_chunk)
        for i in range(len(translated)):
            if "in" in translated[i]:
                translated[i] = self._clear_future_words(translated[i])
            translated[i] = self._join_chunk(
                list(filter(bool, translated[i])), settings=settings
            )
            original[i] = self._join_chunk(
                list(filter(bool, original[i])), settings=settings
            )
        return translated, original

    def _get_abbreviations(self, settings):
        dictionary = self._get_dictionary(settings=settings)
        abbreviations = []
        if self._abbreviations is None:
            for item in dictionary:
                if item.endswith(".") and len(item) > 1:
                    abbreviations.append(item)
            self._abbreviations = abbreviations
        return self._abbreviations

    def _sentence_split(self, string, settings):
        abbreviations = self._get_abbreviations(settings=settings)
        digit_abbreviations = ["[0-9]"]  # numeric date with full stop
        abbreviation_string = ""

        for abbreviation in abbreviations:
            abbreviation_string += (
                "(?<! " + abbreviation[:-1] + ")"
            )  # negative lookbehind
        if self.shortname in ["fi", "cs", "hu", "de", "da"]:
            for digit_abbreviation in digit_abbreviations:
                abbreviation_string += (
                    "(?<!" + digit_abbreviation + ")"
                )  # negative lookbehind

        splitters_dict = {
            1: r"[\.!?;…\r\n]+(?:\s|$)*",  # most European, Tagalog, Hebrew, Georgian,
            # Indonesian, Vietnamese
            2: r"[\.!?;…\r\n]+(\s*[¡¿]*|$)|[¡¿]+",  # Spanish
            3: r"[|!?;\r\n]+(?:\s|$)+",  # Hindi and Bangla
            4: r"[。…‥\.!?？！;\r\n]+(?:\s|$)+",  # Japanese and Chinese
            5: r"[\r\n]+",  # Thai
            6: r"[\r\n؟!\.…]+(?:\s|$)+",
        }  # Arabic and Farsi
        if "sentence_splitter_group" not in self.info:
            split_reg = abbreviation_string + splitters_dict[1]
            sentences = re.split(split_reg, string)
        else:
            split_reg = (
                abbreviation_string
                + splitters_dict[self.info["sentence_splitter_group"]]
            )
            sentences = re.split(split_reg, string)

        sentences = filter(None, sentences)
        return sentences

    def _simplify_split_align(self, original, settings):
        # TODO: Switch to new split method.
        original_tokens = self._word_split(original, settings=settings)
        simplified_tokens = self._word_split(
            self._simplify(normalize_unicode(original), settings=settings),
            settings=settings,
        )
        if len(original_tokens) == len(simplified_tokens):
            return original_tokens, simplified_tokens

        elif len(original_tokens) < len(simplified_tokens):
            add_empty = False
            for i, token in enumerate(simplified_tokens):
                if i < len(original_tokens):
                    if token == normalize_unicode(original_tokens[i].lower()):
                        add_empty = False
                    else:
                        if not add_empty:
                            add_empty = True
                            continue
                        else:
                            original_tokens.insert(i, "")
                else:
                    original_tokens.insert(i, "")
        else:
            add_empty = False
            for i, token in enumerate(original_tokens):
                if i < len(simplified_tokens):
                    if normalize_unicode(token.lower()) == simplified_tokens[i]:
                        add_empty = False
                    else:
                        if not add_empty:
                            add_empty = True
                            continue
                        else:
                            simplified_tokens.insert(i, "")
                else:
                    simplified_tokens.insert(i, "")

        while len(original_tokens) != len(simplified_tokens):
            if len(original_tokens) > len(simplified_tokens):
                original_tokens.remove("")
            else:
                simplified_tokens.remove("")
        return original_tokens, simplified_tokens

    def _get_split_dictionary(self, settings):
        if self._split_dictionary is None:
            settings.NORMALIZE = True
            dictionary = self._get_dictionary(settings=settings)
            self._split_dictionary = self._split_dict(dictionary)
        return self._split_dictionary

    def _split_dict(self, dictionary):
        newdict = {}
        for item in dictionary:
            if " " in item:
                items = item.split()
                for i in items:
                    newdict[i] = dictionary[item]
            else:
                newdict[item] = dictionary[item]
        return newdict

    def _word_split(self, string, settings):
        if "no_word_spacing" in self.info:
            return self._split(string, keep_formatting=True, settings=settings)
        else:
            return string.split()

    def _split(self, date_string, keep_formatting, settings=None):
        tokens = [date_string]
        tokens = list(self._split_tokens_with_regex(tokens, r"(\d+)"))
        tokens = list(
            self._split_tokens_by_known_words(
                tokens, keep_formatting, settings=settings
            )
        )
        return tokens

    def _split_tokens_with_regex(self, tokens, regex):
        tokens = tokens[:]
        for i, token in enumerate(tokens):
            tokens[i] = re.split(regex, token)
        return filter(bool, chain.from_iterable(tokens))

    def _split_tokens_by_known_words(self, tokens, keep_formatting, settings=None):
        dictionary = self._get_dictionary(settings)
        for i, token in enumerate(tokens):
            tokens[i] = dictionary.split(token, keep_formatting)
        return list(chain.from_iterable(tokens))

    def _join_chunk(self, chunk, settings):
        if "no_word_spacing" in self.info:
            return self._join(chunk, separator="", settings=settings)
        else:
            return re.sub(r"\s{2,}", " ", " ".join(chunk))

    def _token_with_digits_is_ok(self, token):
        if "no_word_spacing" in self.info:
            if re.search(r"[\d\.:\-/]+", token) is not None:
                return True
            else:
                return False

        else:
            if re.search(r"\d+", token) is not None:
                return True
            else:
                return False

    def _simplify(self, date_string, settings=None):
        date_string = date_string.lower()
        simplifications = self._get_simplifications(settings=settings)
        for simplification in simplifications:
            pattern, replacement = list(simplification.items())[0]
            date_string = pattern.sub(replacement, date_string).lower()
        return date_string

    def _get_simplifications(self, settings=None):
        no_word_spacing = eval(self.info.get("no_word_spacing", "False"))
        if settings.NORMALIZE:
            if self._normalized_simplifications is None:
                self._normalized_simplifications = []
                simplifications = self._generate_simplifications(normalize=True)
                for simplification in simplifications:
                    pattern, replacement = list(simplification.items())[0]
                    if not no_word_spacing:
                        pattern = r"(?<=\A|\W|_)%s(?=\Z|\W|_)" % pattern
                    pattern = re.compile(pattern, flags=re.I | re.U)
                    self._normalized_simplifications.append({pattern: replacement})
            return self._normalized_simplifications

        else:
            if self._simplifications is None:
                self._simplifications = []
                simplifications = self._generate_simplifications(normalize=False)
                for simplification in simplifications:
                    pattern, replacement = list(simplification.items())[0]
                    if not no_word_spacing:
                        pattern = r"(?<=\A|\W|_)%s(?=\Z|\W|_)" % pattern
                    pattern = re.compile(pattern, flags=re.I | re.U)
                    self._simplifications.append({pattern: replacement})
            return self._simplifications

    def _generate_simplifications(self, normalize=False):
        simplifications = []
        for simplification in self.info.get("simplifications", []):
            c_simplification = {}
            key, value = list(simplification.items())[0]
            if normalize:
                key = normalize_unicode(key)

            if isinstance(value, int):
                c_simplification[key] = str(value)
            else:
                c_simplification[key] = normalize_unicode(value) if normalize else value

            simplifications.append(c_simplification)
        return simplifications

    def _clear_future_words(self, words):
        freshness_words = {"day", "week", "month", "year", "hour", "minute", "second"}
        if set(words).isdisjoint(freshness_words):
            words.remove("in")
        return words

    def _join(self, tokens, separator=" ", settings=None):
        if not tokens:
            return ""

        capturing_splitters = self._get_splitters(settings)["capturing"]
        joined = tokens[0]
        for i in range(1, len(tokens)):
            left, right = tokens[i - 1], tokens[i]
            if left not in capturing_splitters and right not in capturing_splitters:
                joined += separator
            joined += right

        return joined

    def _get_dictionary(self, settings=None):
        if not settings.NORMALIZE:
            if self._dictionary is None:
                self._generate_dictionary()
            self._dictionary._settings = settings
            return self._dictionary
        else:
            if self._normalized_dictionary is None:
                self._generate_normalized_dictionary()
            self._normalized_dictionary._settings = settings
            return self._normalized_dictionary

    def _get_wordchars(self, settings=None):
        if self._wordchars is None:
            self._set_wordchars(settings)
        return self._wordchars

    def _get_splitters(self, settings=None):
        if self._splitters is None:
            self._set_splitters(settings)
        return self._splitters

    def _set_splitters(self, settings=None):
        splitters = {
            # The ones that split string only if they are not surrounded by letters from both sides:
            "wordchars": set(),
            # The ones that are not filtered out from tokens after split:
            "capturing": set(),
        }
        splitters["capturing"] |= set(ALWAYS_KEEP_TOKENS)

        wordchars = self._get_wordchars(settings)
        skip = set(self.info.get("skip", [])) | splitters["capturing"]
        for token in skip:
            if not re.match(r"^\W+$", token, re.UNICODE):
                continue
            if token in wordchars:
                splitters["wordchars"].add(token)

        self._splitters = splitters

    def _set_wordchars(self, settings=None):
        wordchars = set()
        for word in self._get_dictionary(settings):
            if re.match(r"^[\W\d_]+$", word, re.UNICODE):
                continue
            for char in word:
                wordchars.add(char.lower())

        self._wordchars = wordchars - {" "} | {
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        }

    def get_wordchars_for_detection(self, settings):
        if self._wordchars_for_detection is None:
            wordchars = set()
            for word in self._get_dictionary(settings):
                if re.match(r"^[\W\d_]+$", word, re.UNICODE):
                    continue
                for char in word:
                    wordchars.add(char.lower())
            self._wordchars_for_detection = wordchars - {
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                ":",
                "(",
                ")",
                "'",
                "q",
                "a",
                "m",
                "p",
                " ",
            }
        return self._wordchars_for_detection

    def _generate_dictionary(self, settings=None):
        self._dictionary = Dictionary(self.info, settings=settings)

    def _generate_normalized_dictionary(self, settings=None):
        self._normalized_dictionary = NormalizedDictionary(self.info, settings=settings)

    def to_parserinfo(self, base_cls=parser.parserinfo):
        attributes = {
            "JUMP": self.info.get("skip", []),
            "PERTAIN": self.info.get("pertain", []),
            "WEEKDAYS": [
                self.info["monday"],
                self.info["tuesday"],
                self.info["wednesday"],
                self.info["thursday"],
                self.info["friday"],
                self.info["saturday"],
                self.info["sunday"],
            ],
            "MONTHS": [
                self.info["january"],
                self.info["february"],
                self.info["march"],
                self.info["april"],
                self.info["may"],
                self.info["june"],
                self.info["july"],
                self.info["august"],
                self.info["september"],
                self.info["october"],
                self.info["november"],
                self.info["december"],
            ],
            "HMS": [self.info["hour"], self.info["minute"], self.info["second"]],
        }
        name = "{language}ParserInfo".format(language=self.info["name"])
        return type(name, bases=[base_cls], dict=attributes)
