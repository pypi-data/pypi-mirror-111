import json
import logging
import os

from config.settings.base import ROOT_DIR

from buildblock.settings import is_local_environment

LOGGING_SETUP_FILE = '/buildblock/logging_local.json' if is_local_environment() else '/buildblock/logging.json'


def setup_logging(
    default_path=str(ROOT_DIR) + LOGGING_SETUP_FILE,
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
