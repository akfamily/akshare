#!/usr/bin/env python3

import os
from tempfile import TemporaryFile

from dateparser.data.languages_info import language_locale_dict


def to_string(data):
    result = ""
    language_column_width = 18
    for language in sorted(data):
        result += language
        locales = data[language]
        if locales:
            result += " " * (language_column_width - len(language))
            result += ", ".join("'{}'".format(locale) for locale in sorted(locales))
        result += "\n"
    return result


def main():
    readme_path = os.path.join(
        os.path.dirname(__file__), "..", "docs", "supported_locales.rst"
    )
    new_data = to_string(language_locale_dict)
    temporary_file = TemporaryFile("w+")
    with open(readme_path) as readme_file:
        delimiter = "============    ================================================================\n"
        delimiters_seen = 0
        is_inside_table = False
        for line in readme_file:
            if line == delimiter:
                delimiters_seen += 1
                is_inside_table = delimiters_seen == 2
            elif is_inside_table:
                continue
            temporary_file.write(line)
            if is_inside_table:
                temporary_file.write(new_data)
    temporary_file.seek(0)
    with open(readme_path, "w") as readme_file:
        readme_file.write(temporary_file.read())
    temporary_file.close()


if __name__ == "__main__":
    main()
