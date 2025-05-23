import os

import fasttext

from dateparser_cli.exceptions import FastTextModelNotFoundException
from dateparser_cli.fasttext_manager import fasttext_downloader
from dateparser_cli.utils import create_data_model_home, dateparser_model_home

_supported_models = ["large.bin", "small.bin"]
_DEFAULT_MODEL = "small"


class _FastTextCache:
    model = None


def _load_fasttext_model():
    if _FastTextCache.model:
        return _FastTextCache.model
    create_data_model_home()
    downloaded_models = [
        file for file in os.listdir(dateparser_model_home) if file in _supported_models
    ]
    if not downloaded_models:
        fasttext_downloader(_DEFAULT_MODEL)
        return _load_fasttext_model()
    model_path = os.path.join(dateparser_model_home, downloaded_models[0])
    if not os.path.isfile(model_path):
        raise FastTextModelNotFoundException("Fasttext model file not found")
    _FastTextCache.model = fasttext.load_model(model_path)
    return _FastTextCache.model


def detect_languages(text, confidence_threshold):
    _language_parser = _load_fasttext_model()
    text = text.replace("\n", " ").replace("\r", "")
    language_codes = []
    parser_data = _language_parser.predict(text)
    for idx, language_probability in enumerate(parser_data[1]):
        if language_probability > confidence_threshold:
            language_code = parser_data[0][idx].replace("__label__", "")
            language_codes.append(language_code)
    return language_codes
