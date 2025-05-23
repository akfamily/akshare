import os
import shutil
from collections import OrderedDict

from git import Repo


def get_raw_data():
    cldr_version = "31.0.1"
    raw_data_directory = "../raw_data"

    cldr_data = {
        "dates_full": {
            "url": "https://github.com/unicode-cldr/cldr-dates-full.git",
            "dir": "{}/cldr_dates_full/".format(raw_data_directory),
        },
        "core": {
            "url": "https://github.com/unicode-cldr/cldr-core.git",
            "dir": "{}/cldr_core/".format(raw_data_directory),
        },
        "rbnf": {
            "url": "https://github.com/unicode-cldr/cldr-rbnf.git",
            "dir": "{}/cldr_rbnf/".format(raw_data_directory),
        },
    }

    if os.path.isdir(raw_data_directory):
        # remove current raw data
        shutil.rmtree(raw_data_directory)
    os.mkdir(raw_data_directory)

    for name, data in cldr_data.items():
        print('Clonning "{}" from: {}'.format(name, data["url"]))
        repo = Repo.clone_from(data["url"], data["dir"], branch="master")
        repo.git.co(cldr_version)


def get_dict_difference(parent_dict, child_dict):
    difference_dict = OrderedDict()
    for key, child_value in child_dict.items():
        parent_value = parent_dict.get(key)
        child_specific_value = None
        if not parent_value:
            child_specific_value = child_value
        elif isinstance(child_value, list):
            child_specific_value = sorted(set(child_value) - set(parent_value))
        elif isinstance(child_value, dict):
            child_specific_value = get_dict_difference(parent_value, child_value)
        elif child_value != parent_value:
            child_specific_value = child_value
        if child_specific_value:
            difference_dict[key] = child_specific_value
    return difference_dict


def combine_dicts(primary_dict, supplementary_dict):
    combined_dict = OrderedDict()
    for key, value in primary_dict.items():
        if key in supplementary_dict:
            if isinstance(value, list):
                combined_dict[key] = value + supplementary_dict[key]
            elif isinstance(value, dict):
                combined_dict[key] = combine_dicts(value, supplementary_dict[key])
            else:
                combined_dict[key] = supplementary_dict[key]
        else:
            combined_dict[key] = primary_dict[key]
    remaining_keys = [
        key for key in supplementary_dict.keys() if key not in primary_dict.keys()
    ]
    for key in remaining_keys:
        combined_dict[key] = supplementary_dict[key]
    return combined_dict
