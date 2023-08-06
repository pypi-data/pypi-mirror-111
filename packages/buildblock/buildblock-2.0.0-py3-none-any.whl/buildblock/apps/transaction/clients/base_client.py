import json
import logging
import time
from abc import ABC, abstractmethod

from web3 import Web3, middleware

from buildblock.apps.core.constants import BB_MAIN_WALLET
from buildblock.apps.transaction.helper import to_checksum
from buildblock.services.aws import AwsService
from buildblock.settings import CONTRACT_PATH, KLAYTN_BAOBAB_CHAINID, RPC_PATH, RPC_PATH_TO_NETWORK_MAPPING

logger = logging.getLogger(__name__)


class BaseClient(ABC):

    def __init__(self, rpc_path_override=None):
        web3, rpc_path = self._init_connection(rpc_path_override)
        self.web3 = web3
        # client type indicates to which blockchain network this client is connected to, regardless of env
        self.network = RPC_PATH_TO_NETWORK_MAPPING[rpc_path]

    @abstractmethod
    def _get_correct_nonce(self, from_address, last_tx_hash_override=None):
        pass

    def _init_connection(self, rpc_path_override):
        # Connect to Geth in AWS instance
        rpc_path = rpc_path_override or RPC_PATH
        web3 = Web3(Web3.HTTPProvider(rpc_path))
        web3.middleware_stack.inject(middleware.geth_poa_middleware, layer=0)

        # https://web3py.readthedocs.io/en/stable/gas_price.html
        # Due to the overhead of sampling the recent blocks it is recommended that a
        # caching solution be used to reduce the amount of chain data that needs to be
        # re-fetched for each request.
        web3.middleware_stack.add(middleware.time_based_cache_middleware)
        web3.middleware_stack.add(middleware.latest_block_based_cache_middleware)
        web3.middleware_stack.add(middleware.simple_cache_middleware)

        return web3, rpc_path

    def _get_private_key(self, account_address):
        return AwsService.get_user_key(account_address)

    def _get_contract_interface(self, file_name):
        json_data = open(file_name, 'r', encoding='utf-8').read()
        return json.loads(json_data)

    def _get_abi_with_filename(self, contract_name):
        contract_interface = self._get_contract_interface(
            CONTRACT_PATH + f'/{contract_name}.json'
        )
        return contract_interface['abi']

    def _get_transaction_data(self, fromAddr=BB_MAIN_WALLET, toAddr=None, amount=None,
                              gasPrice_override=None, last_tx_hash_override=None):
        transaction_data = {'from': fromAddr}

        try:
            gasPrice = self.web3.eth.gasPrice
        except Exception:
            gasPrice = 10000000000   # 10 Gwei

        transaction_data.update(
            nonce=self._get_correct_nonce(fromAddr, last_tx_hash_override),
            gasPrice=gasPrice,
        )

        if self.network == 'klaytn':
            # Chain ID needs to be specified in using Klaytn's Baobab TestNet
            transaction_data.update(chainId=KLAYTN_BAOBAB_CHAINID)
        if toAddr:
            transaction_data.update(to=toAddr)
        if amount:
            transaction_data.update(value=amount)
        # override gasPrice if present
        if gasPrice_override:
            transaction_data.update(gasPrice=gasPrice_override)
        return transaction_data

    def _update_gas_limit(self, transaction):
        transaction.update(gas=self.web3.eth.estimateGas(transaction))

    def _sign_and_send_transaction(self, transaction, sender=BB_MAIN_WALLET):
        signed = self.web3.eth.account.signTransaction(
            transaction,
            self._get_private_key(sender)
        )
        try:
            # Explicity sleep for 1 sec so that consecutive requests do not get considered as duplicates
            # e.g., ValueError: {'code': -32000, 'message': 'replacement transaction underpriced'}
            time.sleep(1)
            tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
        except Exception:
            logger.error(f'Unhandled error while sending transaction', exc_info=True)
            raise

        tx_hash = str(tx_hash.hex())
        logger.info(f'Sign and send transaction: {tx_hash}')
        return tx_hash

    def get_contract(self, contract_name, contract_address):
        contract_address = to_checksum(contract_address)
        abi = self._get_abi_with_filename(contract_name)
        try:
            contract = self.web3.eth.contract(address=to_checksum(contract_address), abi=abi)
            return contract
        except Exception:
            logger.info('Cannot retrieve the contract info')
            return None
