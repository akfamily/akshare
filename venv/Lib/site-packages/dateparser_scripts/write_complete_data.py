import json
import os
import shutil
from collections import OrderedDict

import regex as re
from ruamel.yaml import RoundTripLoader

from dateparser_scripts.order_languages import avoid_languages
from dateparser_scripts.utils import combine_dicts

cldr_date_directory = "../dateparser_data/cldr_language_data/date_translation_data/"
supplementary_directory = "../dateparser_data/supplementary_language_data/"
supplementary_date_directory = (
    "../dateparser_data/supplementary_language_data/date_translation_data/"
)
translation_data_directory = "../dateparser/data/"
date_translation_directory = "../dateparser/data/date_translation_data/"

os.chdir(os.path.dirname(os.path.abspath(__file__)))

cldr_languages = list(
    set(map(lambda x: x[:-5], os.listdir(cldr_date_directory))) - avoid_languages
)
supplementary_languages = [x[:-5] for x in os.listdir(supplementary_date_directory)]
all_languages = set(cldr_languages).union(set(supplementary_languages))

RELATIVE_PATTERN = re.compile(r"\{0\}")


def _modify_relative_data(relative_data):
    modified_relative_data = OrderedDict()
    for key, value in relative_data.items():
        for i, string in enumerate(value):
            string = RELATIVE_PATTERN.sub(r"(\\d+[.,]?\\d*)", string)
            value[i] = string
        modified_relative_data[key] = value
    return modified_relative_data


def _modify_data(language_data):
    relative_data = language_data.get("relative-type-regex", {})
    relative_data = _modify_relative_data(relative_data)
    locale_specific_data = language_data.get("locale_specific", {})
    for _, info in locale_specific_data.items():
        locale_relative_data = info.get("relative-type-regex", {})
        locale_relative_data = _modify_relative_data(locale_relative_data)


def _get_complete_date_translation_data(language):
    cldr_data = {}
    supplementary_data = {}
    if language in cldr_languages:
        with open(cldr_date_directory + language + ".json") as f:
            cldr_data = json.load(f, object_pairs_hook=OrderedDict)
    if language in supplementary_languages:
        with open(supplementary_date_directory + language + ".yaml") as g:
            supplementary_data = OrderedDict(RoundTripLoader(g).get_data())
    complete_data = combine_dicts(cldr_data, supplementary_data)
    if "name" not in complete_data:
        complete_data["name"] = language
    return complete_data


def _write_file(filename, text, mode, in_memory, in_memory_result):
    if in_memory:
        in_memory_result[filename] = text
    else:
        with open(filename, mode) as out:
            out.write(text)


def write_complete_data(in_memory=False):
    """
    This function is responsible of generating the needed py files from the
    CLDR files (JSON format) and supplementary language data (YAML format).

    Use it with in_memory=True to avoid writing real files and getting a
    dictionary containing the file names and their content (used when testing).
    """
    in_memory_result = {}

    if not in_memory:
        if not os.path.isdir(translation_data_directory):
            os.mkdir(translation_data_directory)
        if os.path.isdir(date_translation_directory):
            shutil.rmtree(date_translation_directory)
        os.mkdir(date_translation_directory)

    with open(supplementary_directory + "base_data.yaml") as f:
        base_data = RoundTripLoader(f).get_data()

    for language in all_languages:
        date_translation_data = _get_complete_date_translation_data(language)
        date_translation_data = combine_dicts(date_translation_data, base_data)
        _modify_data(date_translation_data)
        translation_data = json.dumps(
            date_translation_data, indent=4, separators=(",", ": "), ensure_ascii=False
        )
        out_text = ("info = " + translation_data + "\n").encode("utf-8")
        _write_file(
            date_translation_directory + language + ".py",
            out_text,
            "wb",
            in_memory,
            in_memory_result,
        )

    init_text = (
        "from dateparser.data import date_translation_data\n"
        "from .languages_info import language_order, language_locale_dict\n"
    )

    _write_file(
        translation_data_directory + "__init__.py",
        init_text,
        "w",
        False,
        in_memory_result,
    )
    _write_file(
        date_translation_directory + "__init__.py", "", "w", False, in_memory_result
    )

    return in_memory_result


if __name__ == "__main__":
    write_complete_data()
