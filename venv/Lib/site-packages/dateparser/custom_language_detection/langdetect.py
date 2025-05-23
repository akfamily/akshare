import langdetect

# The below _Factory is set to prevent setting global state of the library
# but still get consistent results.
# Refer : https://github.com/Mimino666/langdetect


class _Factory:
    data = None


def _init_factory():
    if _Factory.data is None:
        _Factory.data = langdetect.detector_factory.DetectorFactory()
        _Factory.data.load_profile(langdetect.detector_factory.PROFILES_DIRECTORY)
        _Factory.data.seed = 0


def _get_language_probablities(text):
    _init_factory()
    detector = _Factory.data.create()
    detector.append(text)
    return detector.get_probabilities()


def detect_languages(text, confidence_threshold):
    language_codes = []
    try:
        parser_data = _get_language_probablities(text)
        for language_candidate in parser_data:
            if language_candidate.prob > confidence_threshold:
                language_codes.append(language_candidate.lang)
    except langdetect.lang_detect_exception.LangDetectException:
        # This exception can be produced with empty strings or inputs without letters like `10-10-2021`.
        # As this could be really common, we ignore them.
        pass
    return language_codes
