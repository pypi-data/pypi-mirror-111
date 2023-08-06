import os

from config.settings.base import APPS_DIR, env


def is_local_environment():
    return os.environ.get('DJANGO_SETTINGS_MODULE') in \
        ['config.settings.local', 'config.settings.test']


def is_dev_environment():
    return os.environ.get('DJANGO_SETTINGS_MODULE') in \
        ['config.settings.local', 'config.settings.development', 'config.settings.test']


def is_prod_environment():
    return os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production'


# Ethereum Client settings
KLAYTN_RPC_PATH = 'http://13.125.65.89:8551'
KLAYTN_BAOBAB_CHAINID = 1001
ETHEREUM_RPC_PATH = env('RPC_PATH')

if is_dev_environment():
    # Connect to Klaytn for testing
    RPC_PATH = KLAYTN_RPC_PATH
else:
    # Connect to Ethereum main net for prod
    RPC_PATH = ETHEREUM_RPC_PATH

RPC_PATH_TO_NETWORK_MAPPING = {
    ETHEREUM_RPC_PATH: 'ethereum',
    KLAYTN_RPC_PATH: 'klaytn',
}

ETHEREUM_ENABLED = False

# Contract Settings
CONTRACT_PATH = str(APPS_DIR) + '/apps/transaction/contracts'

# AWS
BLOCKCHAIN_KEY_ARN = env('BLOCKCHAIN_KEY_ARN')
BLOCKCHAIN_KEY_BUCKET = env('BLOCKCHAIN_KEY_BUCKET')
