import logging
import time

from buildblock.apps.core.constants import BB_MAIN_WALLET, POCKET_WALLET
from buildblock.apps.transaction import constants
from buildblock.apps.transaction.clients.transaction_client import TransactionClient
from buildblock.apps.transaction.helper import to_checksum
from buildblock.errors import NotEnoughEtherError
from buildblock.services.transaction import TxService

logger = logging.getLogger(__name__)

DEFAULT_PROCESS_DELAY_TIME = 60 * 30    # 30 minutes
JOB_TYPE_TO_TX_SERVICE_FUNC_MAPPING = {
    'token': TxService.get_waiting_token_job,
    'ether': TxService.get_waiting_ether_job,
    'vote': TxService.get_waiting_vote_job,
}


class EthereumClient(TransactionClient):

    def _get_correct_nonce(self, from_address=BB_MAIN_WALLET, last_tx_hash_override=None):
        if last_tx_hash_override:
            last_tx_hash = last_tx_hash_override
        else:
            last_tx_hash = TxService.get_last_tx_hash(from_address)

        if last_tx_hash:
            # We derive the nonce from two different perspectives to be sure
            tx = self.web3.eth.getTransaction(last_tx_hash)
            tx_count = self.web3.eth.getTransactionCount(from_address, 'pending')
            nonce = max(tx_count, tx.nonce+1) if tx else tx_count
        else:
            nonce = self.web3.eth.getTransactionCount(from_address, 'pending')

        return nonce

    def register_valid_contract(self, project_contract_addr, tx_hash, main_contract_address):
        """
        Registers the project token contract to be valid.
        MUST be run for all newly deployed project token contracts.
        Allows to call the transferbyOwnerRemote function in the contract.
        """
        tx_data = self._get_transaction_data(last_tx_hash_override=tx_hash)
        main_contract = self.get_contract('BuildToken', main_contract_address)
        transaction = main_contract.functions. \
            registerValidContract(project_contract_addr). \
            buildTransaction(tx_data)
        self._update_gas_limit(transaction)
        self._sign_and_send_transaction(transaction)

    def _wait_for_receipt(self, tx_hash, poll_interval, max_trials):
        for _ in range(max_trials):
            tx_receipt = self.web3.eth.getTransactionReceipt(tx_hash)
            # Got the receipt!
            if tx_receipt:
                logger.info(f"Found the receipt tx_hash: {tx_hash}")
                return tx_receipt
            time.sleep(poll_interval)

        logger.info(f"Wasn't able to find the receipt with max_trials for tx_hash: {tx_hash}")
        return None

    def _finish_transaction(self, job_type, tx_hash, tx_database_object, poll_interval=None, max_trials=None):
        """
        Depending on the tx_receipt value, act differently.
        1. If tx_receipt is None, that means the transaction was not mined yet
        2. If tx_receipt.status is 0, this means the transaction failed for some reason
        3. If tx_receipt.status is 1, this means the transaction succeeded
        """
        tx_receipt = self._wait_for_receipt(tx_hash, poll_interval, max_trials)

        if tx_receipt is None:
            tx_database_object.process_priority += DEFAULT_PROCESS_DELAY_TIME
            tx_database_object.save()
            return
        elif tx_receipt.status == 0:
            logger.warning(f"The contract execution was not successful, check your transaction!")
            # We should at least keep track of this in our PendingTransaction as an invalid
            # so that we can actually retry later
        else:
            block_number = tx_receipt.get('blockNumber')
            block_hash = str(tx_receipt.get('blockHash').hex())
            current_time = int(time.time())

            TxService.mark_tx_complete(tx_database_object, block_hash, block_number, current_time)
            logger.info(f'Tx succeeded for tx_hash={tx_hash} with Block number: {block_number} at time {current_time}')
            if job_type == 'vote':
                # Return early since the vote tx does not have the tx_type field as others
                return
            if job_type == 'token':
                self._final_balance_update(tx_database_object)

    def _final_balance_update(self, tx_database_object):
        if tx_database_object.contract_addr is None:
            # Ether transfer
            return
        self.get_balance(tx_database_object.from_address, tx_database_object.contract_addr, update=True)
        self.get_balance(tx_database_object.to_address, tx_database_object.contract_addr, update=True)

    def transfer_token(self, tx_type, contract, fromAddr, toAddr, amount, invest_contract_addr=None, gasPrice=None):
        """
        Used only for transferring Tokens.
        """
        tx_database_object = TxService.new_token_tx(
            tx_type, contract.address, fromAddr, toAddr, amount, invest_contract_addr
        )

        # we should use integers (multiplied by the UNIT_MULTIPLIER) when making the actual transactions
        amount = int(float(amount)*constants.UNIT_MULTIPLIER)
        args = (to_checksum(fromAddr), to_checksum(toAddr), amount)
        try:
            tx_hash = self._transfer_token_base_operation(
                *args,
                tx_database_object=tx_database_object,
                contract_function=contract.functions.transferByOwner,
                gasPrice=gasPrice
            )
        except Exception:
            # Delete the new entry since we experienced an error
            # We still will have a pending job error description in the database
            tx_database_object.delete()
            raise
        else:
            TxService.mark_tx_waiting(tx_database_object, tx_hash)

    def return_investment(self, tx_type, contract, investors_list, amount_list, gasPrice=None):
        """
        Return investment
        """
        # This is a special case where we set the sender as BB_MAIN_WALLET and rxer as POCKET_WALLET
        # It should NOT really be displayed to the user. We delete this entry later after processing.
        tx_database_object = TxService.new_token_tx(
            tx_type, contract.address, BB_MAIN_WALLET, POCKET_WALLET, sum(amount_list)
        )

        for index in range(len(amount_list)):
            amount_list[index] = int(float(amount_list[index])*constants.UNIT_MULTIPLIER)

        args = (investors_list, amount_list)
        self._transfer_token_base_operation(
            *args,
            tx_database_object=tx_database_object,
            contract_function=contract.functions.returnInvestment,
            gasPrice=gasPrice
        )

    def transfer_ether(self, tx_type, fromAddr, toAddr, amount, gasPrice=None):
        """
        Used only for transferring Ether (NOT tokens)
        """
        transaction = self._get_transaction_data(
            fromAddr=fromAddr,
            toAddr=toAddr,
            amount=amount,
            gasPrice_override=gasPrice,
        )
        # Update the gas limit to the exact amount we get to use
        self._update_gas_limit(transaction)
        # For ether transfer, we check the validity here!
        gas_price = transaction.get('gasPrice')
        gas_limit = transaction.get('gas')
        min_balance = gas_limit * gas_price + amount
        actual_balance = self.get_balance(fromAddr)
        if amount == 0:
            # This is when we transfer after PAYIN. Condition met when we add this
            # as a pending job in the background job. This will leave user's wallet with 0 eth
            logger.info(f'Transfer all ether after payin is verified for user: {fromAddr}')
            amount = actual_balance - gas_limit * gas_price
            if amount <= 0:
                raise NotEnoughEtherError(
                    min_balance=min_balance,
                    balance=actual_balance
                )
            transaction.update(value=amount)
        elif min_balance > actual_balance:
            raise NotEnoughEtherError(
                min_balance=min_balance,
                balance=actual_balance
            )

        logger.info(f'Transfer ether {fromAddr} -> {toAddr}: {amount} Wei')
        tx_database_object = TxService.new_ether_tx(tx_type, fromAddr, toAddr, amount)
        # Here, we specify the sender since this is an Ether transfer
        tx_hash = self._sign_and_send_transaction(transaction, sender=fromAddr)
        TxService.mark_tx_waiting(tx_database_object, tx_hash)

    def get_balance(self, account_address, contract_address=None, update=False):
        balance = super().get_balance(account_address, contract_address)
        return balance

    def _base_complete_waiting_jobs(self, job_type, max_round, poll_interval, max_trials):
        """ Background jobs used by the worker """
        waiting_function = JOB_TYPE_TO_TX_SERVICE_FUNC_MAPPING[job_type]
        for _ in range(max_round):
            incomplete_job = waiting_function()
            if not incomplete_job:
                break
            self._finish_transaction(
                job_type,
                incomplete_job.tx_hash,
                incomplete_job,
                poll_interval=poll_interval,
                max_trials=max_trials,
            )

    def complete_waiting_jobs(self, max_round, poll_interval, max_trials):
        self._base_complete_waiting_jobs('token', max_round, poll_interval, max_trials)
        self._base_complete_waiting_jobs('ether', max_round, poll_interval, max_trials)
        self._base_complete_waiting_jobs('vote', max_round, poll_interval, max_trials)

    def destroy_contract(self, contract_addr):
        contract = self.get_contract('ProjectToken', contract_addr)
        tx_data = self._get_transaction_data()
        transaction = contract.functions.destroy().buildTransaction(tx_data)
        self._update_gas_limit(transaction)
        tx_hash = self._sign_and_send_transaction(transaction)
        logger.info("Waiting until the contract gets DESTROYED")
        self.web3.eth.waitForTransactionReceipt(tx_hash, timeout=300)
        logger.info(f"Contract {contract_addr} has been successfully destroyed.")
