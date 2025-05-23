from dateparser.data.languages_info import language_map


def map_languages(language_codes):
    """
    Returns the candidates from the supported languages codes.
    :param language_codes:
        A list of language codes, e.g. ['en', 'es'] in ISO 639 Standard.
    :type language_codes: list
    :return: Returns list[str] representing supported languages
    :rtype: list[str]
    """
    return [
        language_code
        for language in language_codes
        if language in language_map
        for language_code in language_map[language]
    ]
