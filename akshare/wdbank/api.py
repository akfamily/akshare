# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2020/3/17 22:11
Desc: world bank interface
"""
import collections
import datetime
import re
import warnings

import pandas as pd
import tabulate
from decorator import decorator

from . import fetcher

BASE_URL = "https://api.worldbank.org/v2"
COUNTRIES_URL = f"{BASE_URL}/countries"
ILEVEL_URL = f"{BASE_URL}/incomeLevels"
INDICATOR_URL = f"{BASE_URL}/indicators"
LTYPE_URL = f"{BASE_URL}/lendingTypes"
SOURCES_URL = f"{BASE_URL}/sources"
TOPIC_URL = f"{BASE_URL}/topics"
INDIC_ERROR = "Cannot specify more than one of indicator, source, and topic"


class WBSearchResult(list):
    """
    A list that prints out a user-friendly table when printed or returned on the
    command line


    Items are expected to be dict-like and have an "id" key and a "name" or
    "value" key
    """

    def __repr__(self):
        try:
            return tabulate.tabulate(
                [[o["id"], o["name"]] for o in self],
                headers=["id", "name"],
                tablefmt="simple",
            )
        except KeyError:
            return tabulate.tabulate(
                [[o["id"], o["value"]] for o in self],
                headers=["id", "value"],
                tablefmt="simple",
            )


if pd:

    class WBSeries(pd.Series):
        """
        A pandas Series with a last_updated attribute
        """

        _metadata = ["last_updated"]

        @property
        def _constructor(self):
            return WBSeries

    class WBDataFrame(pd.DataFrame):
        """
        A pandas DataFrame with a last_updated attribute
        """

        _metadata = ["last_updated"]

        @property
        def _constructor(self):
            return WBDataFrame


@decorator
def uses_pandas(f, *args, **kwargs):
    """Raise ValueError if pandas is not loaded"""
    if not pd:
        raise ValueError("Pandas must be installed to be used")
    return f(*args, **kwargs)


def parse_value_or_iterable(arg):
    """
    If arg is a single value, return it as a string; if an iterable, return a
    ;-joined string of all values
    """
    if str(arg) == arg:
        return arg
    if type(arg) == int:
        return str(arg)
    return ";".join(arg)


def convert_year_to_datetime(yearstr):
    """return datetime.datetime object from %Y formatted string"""
    return datetime.datetime.strptime(yearstr, "%Y")


def convert_month_to_datetime(monthstr):
    """return datetime.datetime object from %YM%m formatted string"""
    split = monthstr.split("M")
    return datetime.datetime(int(split[0]), int(split[1]), 1)


def convert_quarter_to_datetime(quarterstr):
    """
    return datetime.datetime object from %YQ%# formatted string, where # is
    the desired quarter
    """
    split = quarterstr.split("Q")
    quarter = int(split[1])
    month = quarter * 3 - 2
    return datetime.datetime(int(split[0]), month, 1)


def convert_dates_to_datetime(data):
    """
    Return a datetime.datetime object from a date string as provided by the
    World Bank
    """
    first = data[0]["date"]
    if isinstance(first, datetime.datetime):
        return data
    if "M" in first:
        converter = convert_month_to_datetime
    elif "Q" in first:
        converter = convert_quarter_to_datetime
    else:
        converter = convert_year_to_datetime
    for datum in data:
        datum_date = datum["date"]
        if "MRV" in datum_date:
            continue
        if "-" in datum_date:
            continue
        datum["date"] = converter(datum_date)
    return data


def cast_float(value):
    """
    Return a floated value or none
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def get_series(
    indicator,
    country="all",
    data_date=None,
    source=None,
    convert_date=False,
    column_name="value",
    keep_levels=False,
    cache=True,
):
    """
    Retrieve indicators for given countries and years

    :indicator: the desired indicator code
    :country: a country code, sequence of country codes, or "all" (default)
    :data_date: the desired date as a datetime object or a 2-tuple with start
        and end dates
    :source: the specific source to retrieve data from (defaults on API to 2,
        World Development Indicators)
    :convert_date: if True, convert date field to a datetime.datetime object.
    :column_name: the desired name for the pandas column
    :keep_levels: if True and pandas is True, don't reduce the number of index
        levels returned if only getting one date or country
    :cache: use the cache
    :returns: WBSeries
    """
    raw_data = get_data(
        indicator=indicator,
        country=country,
        data_date=data_date,
        source=source,
        convert_date=convert_date,
        cache=cache,
    )
    df = pd.DataFrame(
        [[i["country"]["value"], i["date"], i["value"]] for i in raw_data],
        columns=["country", "date", column_name],
    )
    df[column_name] = df[column_name].map(cast_float)
    if not keep_levels and len(df["country"].unique()) == 1:
        df = df.set_index("date")
    elif not keep_levels and len(df["date"].unique()) == 1:
        df = df.set_index("country")
    else:
        df = df.set_index(["country", "date"])
    series = WBSeries(df[column_name])
    series.last_updated = raw_data.last_updated
    return series


def get_data(
    indicator,
    country="all",
    data_date=None,
    source=None,
    convert_date=False,
    pandas=False,
    column_name="value",
    keep_levels=False,
    cache=True,
):
    """
    Retrieve indicators for given countries and years

    :indicator: the desired indicator code
    :country: a country code, sequence of country codes, or "all" (default)
    :data_date: the desired date as a datetime object or a 2-tuple with start
        and end dates
    :source: the specific source to retrieve data from (defaults on API to 2,
        World Development Indicators)
    :convert_date: if True, convert date field to a datetime.datetime object.
    :cache: use the cache
    :returns: list of dictionaries or pandas Series
    """
    if pandas:
        warnings.warn(
            (
                "Argument 'pandas' is deprecated and will be removed in a "
                "future version. Use get_series or get_dataframe instead."
            ),
            PendingDeprecationWarning,
        )
        return get_series(
            indicator=indicator,
            country=country,
            data_date=data_date,
            source=source,
            convert_date=convert_date,
            column_name=column_name,
            keep_levels=keep_levels,
            cache=cache,
        )
    query_url = COUNTRIES_URL
    try:
        c_part = parse_value_or_iterable(country)
    except TypeError:
        raise TypeError("'country' must be a string or iterable'")
    query_url = "/".join((query_url, c_part, "indicators", indicator))
    args = {}
    if data_date:
        if isinstance(data_date, collections.Sequence):
            data_date_str = ":".join((i.strftime("%Y") for i in data_date))
            args["date"] = data_date_str
        else:
            args["date"] = data_date.strftime("%Y")
    if source:
        args["source"] = source
    data = fetcher.fetch(query_url, args, cache=cache)
    if convert_date:
        data = convert_dates_to_datetime(data)
    return data


def id_only_query(query_url, query_id, cache):
    """
    Retrieve information when ids are the only arguments

    :query_url: the base url to use for the query
    :query_id: an id or sequence of ids
    :cache: use the cache
    :returns: WBSearchResult containing dictionary objects describing results
    """
    if query_id:
        query_url = "/".join((query_url, parse_value_or_iterable(query_id)))
    return WBSearchResult(fetcher.fetch(query_url))


def get_source(source_id=None, cache=True):
    """
    Retrieve information on a source

    :source_id: a source id or sequence thereof.  None returns all sources
    :cache: use the cache
    :returns: WBSearchResult containing dictionary objects describing selected
        sources
    """
    return id_only_query(SOURCES_URL, source_id, cache=cache)


def get_incomelevel(level_id=None, cache=True):
    """
    Retrieve information on an income level aggregate

    :level_id: a level id or sequence thereof.  None returns all income level
        aggregates
    :cache: use the cache
    :returns: WBSearchResult containing dictionary objects describing selected
        income level aggregates
    """
    return id_only_query(ILEVEL_URL, level_id, cache=cache)


def get_topic(topic_id=None, cache=True):
    """
    Retrieve information on a topic

    :topic_id: a topic id or sequence thereof.  None returns all topics
    :cache: use the cache
    :returns: WBSearchResult containing dictionary objects describing selected
        topic aggregates
    """
    return id_only_query(TOPIC_URL, topic_id, cache=cache)


def get_lendingtype(type_id=None, cache=True):
    """
    Retrieve information on an income level aggregate

    :level_id: lending type id or sequence thereof.  None returns all lending
        type aggregates
    :cache: use the cache
    :returns: WBSearchResult containing dictionary objects describing selected
        topic aggregates
    """
    return id_only_query(LTYPE_URL, type_id, cache=cache)


def get_country(country_id=None, incomelevel=None, lendingtype=None, cache=True):
    """
    Retrieve information on a country or regional aggregate.  Can specify
    either country_id, or the aggregates, but not both

    :country_id: a country id or sequence thereof. None returns all countries
        and aggregates.
    :incomelevel: desired incomelevel id or ids.
    :lendingtype: desired lendingtype id or ids.
    :cache: use the cache
    :returns: WBSearchResult containing dictionary objects representing each
        country
    """
    if country_id:
        if incomelevel or lendingtype:
            raise ValueError("Can't specify country_id and aggregates")
        return id_only_query(COUNTRIES_URL, country_id, cache=cache)
    args = {}
    if incomelevel:
        args["incomeLevel"] = parse_value_or_iterable(incomelevel)
    if lendingtype:
        args["lendingType"] = parse_value_or_iterable(lendingtype)
    return WBSearchResult(fetcher.fetch(COUNTRIES_URL, args, cache=cache))


def get_indicator(indicator=None, source=None, topic=None, cache=True):
    """
    Retrieve information about an indicator or indicators.  Only one of
    indicator, source, and topic can be specified.  Specifying none of the
    three will return all indicators.

    :indicator: an indicator code or sequence thereof
    :source: a source id or sequence thereof
    :topic: a topic id or sequence thereof
    :cache: use the cache
    :returns: WBSearchResult containing dictionary objects representing
        indicators
    """
    if indicator:
        if source or topic:
            raise ValueError(INDIC_ERROR)
        query_url = "/".join((INDICATOR_URL, parse_value_or_iterable(indicator)))
    elif source:
        if topic:
            raise ValueError(INDIC_ERROR)
        query_url = "/".join(
            (SOURCES_URL, parse_value_or_iterable(source), "indicators")
        )
    elif topic:
        query_url = "/".join((TOPIC_URL, parse_value_or_iterable(topic), "indicators"))
    else:
        query_url = INDICATOR_URL
    return WBSearchResult(fetcher.fetch(query_url, cache=cache))


def search_indicators(query, source=None, topic=None, cache=True):
    """
    Search indicators for a certain regular expression.  Only one of source or
    topic can be specified. In interactive mode, will return None and print ids
    and names unless suppress_printing is True.

    :query: the term to match against indicator names
    :source: if present, id of desired source
    :topic: if present, id of desired topic
    :cache: use the cache
    :returns: WBSearchResult containing dictionary objects representing search
        indicators
    """
    indicators = get_indicator(source=source, topic=topic, cache=cache)
    pattern = re.compile(query, re.IGNORECASE)
    return WBSearchResult(i for i in indicators if pattern.search(i["name"]))


def search_countries(query, incomelevel=None, lendingtype=None, cache=True):
    """
    Search countries by name.  Very simple search.

    :query: the string to match against country names
    :incomelevel: if present, search only the matching incomelevel
    :lendingtype: if present, search only the matching lendingtype
    :cache: use the cache
    :returns: WBSearchResult containing dictionary objects representing
        countries
    """
    countries = get_country(
        incomelevel=incomelevel, lendingtype=lendingtype, cache=cache
    )
    pattern = re.compile(query, re.IGNORECASE)
    return WBSearchResult(i for i in countries if pattern.search(i["name"]))


@uses_pandas
def get_dataframe(
    indicators,
    country="all",
    data_date=None,
    source=None,
    convert_date=False,
    keep_levels=False,
    cache=True,
):
    """
    Convenience function to download a set of indicators and  merge them into a
        pandas DataFrame.  The index will be the same as if calls were made to
        get_data separately.

    :indicators: An dictionary where the keys are desired indicators and the
        values are the desired column names
    :country: a country code, sequence of country codes, or "all" (default)
    :data_date: the desired date as a datetime object or a 2-sequence with
        start and end dates
    :source: the specific source to retrieve data from (defaults on API to 2,
        World Development Indicators)
    :convert_date: if True, convert date field to a datetime.datetime object.
    :keep_levels: if True don't reduce the number of index levels returned if
        only getting one date or country
    :cache: use the cache
    :returns: a pandas DataFrame
    """
    serieses = [
        (
            get_series(
                indicator=indicator,
                country=country,
                data_date=data_date,
                source=source,
                convert_date=convert_date,
                keep_levels=keep_levels,
                cache=cache,
            ).rename(name)
        )
        for indicator, name in indicators.items()
    ]
    print(type(serieses[0]))
    result = None
    for series in serieses:
        if result is None:
            result = series.to_frame()
        else:
            result = result.join(series.to_frame(), how="outer")
    result = WBDataFrame(result)
    result.last_updated = {i.name: i.last_updated for i in serieses}
    return result
