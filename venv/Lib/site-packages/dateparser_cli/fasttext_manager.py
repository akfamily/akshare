import logging
import os
import urllib.request
from pathlib import Path

from .exceptions import FastTextModelNotFoundException
from .utils import create_data_model_home, dateparser_model_home


def fasttext_downloader(model_name):
    create_data_model_home()
    models = {
        "small": "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz",
        "large": "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin",
    }
    if model_name not in models:
        message = 'dateparser-download: Couldn\'t find a model called "{}". Supported models are: {}'.format(
            model_name, ", ".join(models.keys())
        )
        raise FastTextModelNotFoundException(message)

    models_directory_path = os.path.join(dateparser_model_home, (model_name + ".bin"))

    if not Path(models_directory_path).is_file():
        model_url = models[model_name]
        logging.info(
            'dateparser-download: Downloading model "{}" from "{}"...'.format(
                model_name, model_url
            )
        )
        try:
            urllib.request.urlretrieve(model_url, models_directory_path)
        except urllib.error.HTTPError as e:
            raise Exception(
                "dateparser-download: Fasttext model cannot be downloaded due to HTTP error"
            ) from e
    else:
        logging.info(
            'dateparser-download: The model "{}" is already downloaded'.format(
                model_name
            )
        )
