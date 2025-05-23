import os
import sys
from pathlib import Path

DEFAULT_DIR_NAME = "dateparser_models"
DEFAULT_UNIX_CACHE_DIR = "~/.cache"

DEFAULT_WINDOWS_CACHE_DIR = os.path.join(Path.home(), "AppData", "Roaming")


if sys.platform.startswith("win"):
    # For Windows:
    _cache_dir = DEFAULT_WINDOWS_CACHE_DIR
else:
    # UNIX & OS X:
    _cache_dir = DEFAULT_UNIX_CACHE_DIR

dateparser_model_home = os.path.expanduser(os.path.join(_cache_dir, DEFAULT_DIR_NAME))


def create_data_model_home():
    os.makedirs(dateparser_model_home, exist_ok=True)


def clear_cache(*args):
    for path in Path(dateparser_model_home).rglob("*.*"):
        os.remove(path)
