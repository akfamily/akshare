from functools import wraps


def _restore_languages_on_generator_exit(method):
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        stored_languages = self.languages[:]
        for language in method(self, *args, **kwargs):
            yield language
        else:
            self.languages[:] = stored_languages

    return wrapped


class BaseLanguageDetector:
    def __init__(self, languages):
        self.languages = languages[:]

    @_restore_languages_on_generator_exit
    def iterate_applicable_languages(self, date_string, settings=None, modify=False):
        languages = self.languages if modify else self.languages[:]
        yield from self._filter_languages(date_string, languages, settings)

    @staticmethod
    def _filter_languages(date_string, languages, settings=None):
        while languages:
            language = languages[0]
            if language.is_applicable(
                date_string, strip_timezone=False, settings=settings
            ):
                yield language
            elif language.is_applicable(
                date_string, strip_timezone=True, settings=settings
            ):
                yield language

            languages.pop(0)


class AutoDetectLanguage(BaseLanguageDetector):
    def __init__(self, languages, allow_redetection=False):
        super().__init__(languages=languages[:])
        self.language_pool = languages[:]
        self.allow_redetection = allow_redetection

    @_restore_languages_on_generator_exit
    def iterate_applicable_languages(self, date_string, modify=False, settings=None):
        languages = self.languages if modify else self.languages[:]
        initial_languages = languages[:]
        yield from self._filter_languages(date_string, languages, settings=settings)

        if not self.allow_redetection:
            return

        # Try languages that was not tried before with this date_string
        languages = [
            language
            for language in self.language_pool
            if language not in initial_languages
        ]
        if modify:
            self.languages = languages

        yield from self._filter_languages(date_string, languages, settings=settings)


class ExactLanguages(BaseLanguageDetector):
    def __init__(self, languages):
        if languages is None:
            raise ValueError("language cannot be None for ExactLanguages")
        super().__init__(languages=languages)

    @_restore_languages_on_generator_exit
    def iterate_applicable_languages(self, date_string, modify=False, settings=None):
        yield from super().iterate_applicable_languages(
            date_string, modify=False, settings=settings
        )
