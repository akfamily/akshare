from dateparser.search.search import DateSearchWithDetection

_search_with_detection = DateSearchWithDetection()


def search_dates(
    text,
    languages=None,
    settings=None,
    add_detected_language=False,
    detect_languages_function=None,
):
    """Find all substrings of the given string which represent date and/or time and parse them.

    :param text:
        A string in a natural language which may contain date and/or time expressions.
    :type text: str

    :param languages:
        A list of two letters language codes.e.g. ['en', 'es']. If languages are given, it will
        not attempt to detect the language.
    :type languages: list

    :param settings:
        Configure customized behavior using settings defined in :mod:`dateparser.conf.Settings`.
    :type settings: dict

    :param add_detected_language:
        Indicates if we want the detected language returned in the tuple.
    :type add_detected_language: bool

    :param detect_languages_function:
        A function for language detection that takes as input a `text` and a `confidence_threshold`,
        and returns a list of detected language codes.
        Note: detect_languages_function is only uses if `languages` are not provided.
    :type detect_languages_function: function

    :return: Returns list of tuples containing:
        substrings representing date and/or time, corresponding :mod:`datetime.datetime`
        object and detected language if *add_detected_language* is True.
        Returns None if no dates that can be parsed are found.
    :rtype: list
    :raises: ValueError - Unknown Language

    >>> from dateparser.search import search_dates
    >>> search_dates('The first artificial Earth satellite was launched on 4 October 1957.')
    [('on 4 October 1957', datetime.datetime(1957, 10, 4, 0, 0))]

    >>> search_dates('The first artificial Earth satellite was launched on 4 October 1957.',
    >>>              add_detected_language=True)
    [('on 4 October 1957', datetime.datetime(1957, 10, 4, 0, 0), 'en')]

    >>> search_dates("The client arrived to the office for the first time in March 3rd, 2004 "
    >>>              "and got serviced, after a couple of months, on May 6th 2004, the customer "
    >>>              "returned indicating a defect on the part")
    [('in March 3rd, 2004 and', datetime.datetime(2004, 3, 3, 0, 0)),
     ('on May 6th 2004', datetime.datetime(2004, 5, 6, 0, 0))]

    """
    result = _search_with_detection.search_dates(
        text=text,
        languages=languages,
        settings=settings,
        detect_languages_function=detect_languages_function,
    )
    dates = result.get("Dates")
    if dates:
        if add_detected_language:
            language = result.get("Language")
            dates = [date + (language,) for date in dates]
        return dates
