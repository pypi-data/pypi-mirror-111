import logging
from abc import ABC, abstractmethod

from buildblock.apps.core.constants import MAIN_CONTRACTS
from buildblock.apps.transaction.clients.base_client import BaseClient
from buildblock.apps.transaction.helper import to_checksum

logger = logging.getLogger(__name__)


class TransactionClient(BaseClient, ABC):

    @abstractmethod
    def transfer_token(self, tx_type, contract, fromAddr, toAddr, amount, invest_contract_addr=None, gasPrice=None):
        pass

    def _transfer_token_base_operation(self, *args, **kwargs):
        """
        Basic operation for all token transfers
        """
        gasPrice = kwargs.get('gasPrice')
        contract_function = kwargs.get('contract_function')
        try:
            tx_data = self._get_transaction_data(gasPrice_override=gasPrice)
            transaction = contract_function(*args).buildTransaction(tx_data)
            # Update the gas limit to the exact amount we get to use
            self._update_gas_limit(transaction)
            tx_hash = self._sign_and_send_transaction(transaction)
        except Exception:
            logger.error(f'Unhandled error while transferring token', exc_info=True)
            raise
        else:
            return tx_hash

    def get_balance(self, account_address, contract_address=None):
        # if the contract is not specified, we get the ETH (not token) balance of the address
        account_address = to_checksum(account_address)
        if contract_address is None:
            # Check ethereum balance
            balance = self.web3.eth.getBalance(account_address)
        else:
            contract_name = 'BuildToken' if contract_address in MAIN_CONTRACTS else 'ProjectToken'
            contract_instance = self.get_contract(contract_name, contract_address)
            # Check contract balances from the blockchain network (BBT, PJT)
            balance = contract_instance.functions.balanceOf(account_address).call()

        return balance
