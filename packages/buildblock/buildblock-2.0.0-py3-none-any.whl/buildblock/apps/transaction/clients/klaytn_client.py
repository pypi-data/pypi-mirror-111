from buildblock.apps.transaction import constants
from buildblock.apps.transaction.clients.transaction_client import TransactionClient
from buildblock.apps.transaction.helper import to_checksum
from buildblock.settings import KLAYTN_RPC_PATH


class KlaytnClient(TransactionClient):
    """
    This client is only used for shadowing the Ethereum client when a request is made.
    Note that EthereumClient is a KlaytnClient in development environment.
    Therefore, this client does not have functions such as deeploy contract
    """
    def __init__(self):
        super().__init__(rpc_path_override=KLAYTN_RPC_PATH)

    def _get_correct_nonce(self, from_address, last_tx_hash_override=None):
        return self.web3.eth.getTransactionCount(from_address, 'pending')

    def transfer_token(self, tx_type, contract, fromAddr, toAddr, amount, invest_contract_addr=None, gasPrice=None):
        amount = int(float(amount)*constants.UNIT_MULTIPLIER)
        args = (to_checksum(fromAddr), to_checksum(toAddr), amount)

        self._transfer_token_base_operation(
            *args,
            contract_function=contract.functions.transferByOwner,
            gasPrice=gasPrice
        )
