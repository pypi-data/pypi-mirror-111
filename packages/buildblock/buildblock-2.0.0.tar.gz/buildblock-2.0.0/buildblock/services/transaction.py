import logging
import time

from django.db.models import Q

from buildblock.apps.core.constants import BB_MAIN_WALLET, MAIN_CONTRACTS
from buildblock.apps.transaction import constants
from buildblock.apps.transaction.models import (
    Contract,
    EtherTransaction,
    Investment,
    TokenTransaction,
    VotingTransaction
)

logger = logging.getLogger(__name__)


class TxService:

    """
    Class Methods for token transfer - Interacts with TokenTransaction
    """
    @classmethod
    def new_token_tx(cls, tx_type, contract_addr, from_address, to_address, amount, invest_contract_addr=None):
        unit = constants.BBT if contract_addr in MAIN_CONTRACTS else constants.PJT
        tx = TokenTransaction.objects.create(
            tx_type=tx_type,
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            unit=unit,
            tx_hash=None,
            status=constants.PROCESSING,
            contract_addr=contract_addr,
            invest_contract_addr=invest_contract_addr,
        )
        logger.info(f'New TokenTransaction entry added in database: {locals()}')
        return tx

    @classmethod
    def new_ether_tx(cls, tx_type, from_address, to_address, amount):
        tx = EtherTransaction.objects.create(
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            tx_type=tx_type,
            status=constants.PROCESSING,
        )
        logger.info(f'New EtherTransaction entry added in database: {locals()}')
        return tx

    @classmethod
    def new_vote_tx(cls, voting_type, tx_hash, voter, contract_addr, voting_round, decision):
        """ For voting tx, we start from the WAITING state, only after we get the tx hash """
        tx = VotingTransaction.objects.create(
            voting_type=voting_type,
            voter=voter,
            contract_addr=contract_addr,
            voting_round=voting_round,
            decision=decision,
            status=constants.WAITING,
            tx_hash=tx_hash,
            process_priority=int(time.time()),
        )
        logger.info(f'New VotingTransaction entry added in database: {locals()}')
        return tx

    @classmethod
    def mark_tx_waiting(cls, tx, tx_hash):
        # Mark the transaction status to WAITING after making request to ether net
        if tx.status != constants.PROCESSING:
            return
        tx.process_priority = int(time.time())
        tx.status = constants.WAITING
        tx.tx_hash = tx_hash
        tx.save()
        logger.info(f'Mark transaction as WAITING for tx id: {tx.id}')

    @classmethod
    def mark_tx_complete(cls, tx, block_hash, block_number, tx_receipt_time):
        # Mark the transaction status to COMPLETE once we get tx receipt
        if tx.status != constants.WAITING:
            return
        tx.status = constants.COMPLETE
        tx.process_priority = None
        tx.block_hash = block_hash
        tx.block_number = block_number
        tx.tx_receipt_time = tx_receipt_time
        tx.save()
        logger.info(f'Mark transaction as COMPLETE for tx id: {tx.id}')

    @classmethod
    def get_waiting_token_job(cls):
        # Get the tx_hash of the transaction that has not been verified yet
        jobs = TokenTransaction.objects. \
               filter(status=constants.WAITING). \
               order_by('process_priority')
        return jobs[0] if jobs else None

    @classmethod
    def get_waiting_ether_job(cls):
        # Get the tx_hash of the transaction that has not been verified yet
        jobs = EtherTransaction.objects. \
               exclude(Q(tx_type=constants.PAYOUT) | Q(tx_type=constants.PAYIN)). \
               filter(status=constants.WAITING). \
               order_by('process_priority')
        return jobs[0] if jobs else None

    @classmethod
    def get_waiting_vote_job(cls):
        # Get the tx_hash of the transaction that has not been verified yet
        jobs = VotingTransaction.objects. \
               filter(status=constants.WAITING). \
               order_by('process_priority')
        return jobs[0] if jobs else None

    @classmethod
    def get_last_tx_hash(cls, from_address=BB_MAIN_WALLET):
        # We should always check both tables to get the latest Tx hash
        token_tx_instance = None
        if from_address == BB_MAIN_WALLET:
            # Only check this table when the sender is our main wallet
            token_tx_set = TokenTransaction.objects.exclude(status='PROCESSING')
            token_tx_instance = token_tx_set.latest('created_at') if token_tx_set else None

        ether_tx_set = EtherTransaction.objects.exclude(status='PROCESSING').filter(from_address=from_address)
        ether_tx_instance = ether_tx_set.latest('created_at') if ether_tx_set else None

        if from_address == BB_MAIN_WALLET:
            if not token_tx_instance and not ether_tx_instance:
                return None
            elif token_tx_instance and not ether_tx_instance:
                return token_tx_instance.tx_hash
            elif not token_tx_instance and ether_tx_instance:
                return ether_tx_instance.tx_hash
            else:
                return ether_tx_instance.tx_hash \
                    if ether_tx_instance.created_at > token_tx_instance.created_at \
                    else token_tx_instance.tx_hash
        else:
            return ether_tx_instance.tx_hash if ether_tx_instance else None

    """
    Class Methods for Investments - Interacts with Investments
    """
    @classmethod
    def make_investment(cls, contract_addr, borrower, investor, amount):
        try:
            # TODO: Assert that this contract_addr is indeed there!
            investment_instance = Investment.objects.get(
                contract_addr=contract_addr,
                borrower=borrower,
                investor=investor,
                status=constants.WAITING
            )
        except Investment.DoesNotExist:
            Investment.objects.create(
                contract_addr=contract_addr,
                borrower=borrower,
                investor=investor,
                amount=amount,
                status=constants.WAITING
            )
        except Exception:
            logger.error('Unhandled error', exc_info=True)
            raise
        else:
            investment_instance.amount += amount
            investment_instance.save()

    @classmethod
    def withdraw_investment(cls, contract_addr, borrower, investor, amount):
        # All validations are done when adding the pending job
        investment_instance = Investment.objects.get(
            contract_addr=contract_addr,
            borrower=borrower,
            investor=investor,
            status=constants.WAITING
        )
        investment_instance.amount -= amount
        if investment_instance.amount == 0:
            investment_instance.delete()
        else:
            investment_instance.save()

    """
    Class Methods for Contract - Interacts with Contract
    """
    @classmethod
    def is_contract_addr_valid(cls, contract_addr):
        for contract in Contract.objects.filter():
            if contract_addr in contract.contract_dict.values():
                return True
        return False
