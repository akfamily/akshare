from dateparser.conf import apply_settings
from dateparser.search.detection import BaseLanguageDetector
from dateparser.utils import normalize_unicode


class FullTextLanguageDetector(BaseLanguageDetector):
    def __init__(self, languages):
        super(BaseLanguageDetector, self).__init__()
        self.languages = languages[:]
        self.language_unique_chars = []
        self.language_chars = []

    def get_unique_characters(self, settings):
        settings = settings.replace(NORMALIZE=False)

        for language in self.languages:
            chars = language.get_wordchars_for_detection(settings=settings)
            self.language_chars.append(chars)

        for char_set in self.language_chars:
            unique_chars = char_set
            for other_char_set in self.language_chars:
                if other_char_set != char_set:
                    unique_chars = unique_chars - other_char_set
            self.language_unique_chars.append(unique_chars)

    def character_check(self, date_string, settings):
        date_string_set = set(date_string.lower())
        symbol_set = {
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
            " ",
            "/",
            "-",
            ")",
            "(",
            ".",
            ":",
            "\\",
            ",",
            "'",
        }
        if date_string_set & symbol_set == date_string_set:
            self.languages = [self.languages[0]]
            return
        self.get_unique_characters(settings=settings)
        for i in range(len(self.languages)):
            for char in self.language_unique_chars[i]:
                if char.lower() in date_string.lower():
                    self.languages = [self.languages[i]]
                    return
        indices_to_pop = []
        for i in range(len(self.languages)):
            if len(date_string_set & self.language_chars[i]) == 0:
                indices_to_pop.append(i)
        self.languages = [
            i for j, i in enumerate(self.languages) if j not in indices_to_pop
        ]

    @apply_settings
    def _best_language(self, date_string, settings=None):
        self.character_check(date_string, settings)
        date_string = normalize_unicode(date_string.lower())
        if len(self.languages) == 1:
            return self.languages[0].shortname
        applicable_languages = []
        for language in self.languages:
            num_words = language.count_applicability(
                date_string, strip_timezone=False, settings=settings
            )
            if num_words[0] > 0 or num_words[1] > 0:
                applicable_languages.append((language.shortname, num_words))
            else:
                num_words = language.count_applicability(
                    date_string, strip_timezone=True, settings=settings
                )
                if num_words[0] > 0 or num_words[1] > 0:
                    applicable_languages.append((language.shortname, num_words))
        if not applicable_languages:
            return None
        return max(applicable_languages, key=lambda p: (p[1][0], p[1][1]))[0]
