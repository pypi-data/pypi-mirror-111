from datetime import datetime
from typing import NamedTuple

from django.contrib import messages
from django.http import HttpResponse

from buildblock.apps.core.constants import (
    ACH_DEBIT,
    CANCELED,
    CASH,
    CHECKS,
    COMPLETE,
    CREDIT_CARD,
    DEBIT_CARD,
    DEPOSIT,
    FAILED,
    FAILED_NO_DESTINATION_ACCOUNT,
    PENDING,
    RENT,
    UNKNOWN
)
from buildblock.apps.payments.constants import (
    BANK_ACCOUNT,
    CARD,
    CHARGE_FAILED,
    CHARGE_SUCCEEDED,
    CURRENCY_USD,
    TOPUP_FAILED,
    TOPUP_SUCCEEDED,
    TRANSFER_CREATED,
    TRANSFER_FAILED
)
from buildblock.apps.payments.models import PaymentTransfers, RentPayment
from buildblock.helper import db_update
from buildblock.mixins import Loggable
from buildblock.utils import calculate_payment_fee

_STRIPE_EVENT_PAYMENT_METHOD_MAPPING = {
    'credit': CREDIT_CARD,
    'debit': DEBIT_CARD,
    'ach_debit': ACH_DEBIT,
    'topup': CASH,  # Cash or Cash Equivalents Method
}

CASH_EQUIVALENTS = [CASH, CHECKS]

_STRIPE_CHARGE_EVENT = frozenset([
    CHARGE_FAILED,
    CHARGE_SUCCEEDED,
    TOPUP_FAILED,
    TOPUP_SUCCEEDED,
])

_NON_FEE_PAYMENT_TYPE_LIST = frozenset([DEPOSIT])


def _get_payment_method(event_data):
    if event_data.object == 'charge':
        payment_method_details = event_data.payment_method_details
        payment_method = payment_method_details.card.funding \
            if payment_method_details.type == 'card' else payment_method_details.type
    else:
        payment_method = event_data.object
    return _STRIPE_EVENT_PAYMENT_METHOD_MAPPING.get(payment_method, UNKNOWN)


def _get_transfer_source_type(event_data):
    if event_data.object == 'charge':
        return CARD if event_data.payment_method_details.type == 'card' else BANK_ACCOUNT
    else:
        return BANK_ACCOUNT


def _get_application_fee(rent):
    return int(rent.product.application_fee_rate * rent.amount) \
        if rent.payment_type not in _NON_FEE_PAYMENT_TYPE_LIST else 0


def _create_transfers(rent, owners_list, transfer_group, transfer_source_type):
    num_owners = len(owners_list)
    currency = CURRENCY_USD
    individual_amount = int(rent.amount / float(num_owners))
    total_application_fee = _get_application_fee(rent)
    individual_application_fee = int(total_application_fee / float(num_owners))
    individual_transfer_amount = individual_amount - individual_application_fee

    for owner in owners_list:
        # TODO: profile_owner.stripe_account 생성 후 Transfer 처리
        stripe_account = owner.profile_owner.stripe_account \
            if hasattr(owner, 'profile_owner') else None
        # Create the payment transfer object. This will be run async via background jobs
        PaymentTransfers.objects.create(
            tenant=rent.tenant,
            owner=owner,
            product=rent.product,
            amount=individual_transfer_amount,
            application_fee=individual_application_fee,
            currency=currency,
            destination_account=stripe_account,
            account_type='stripe',
            identifier=transfer_group,
            status=PENDING if stripe_account else FAILED_NO_DESTINATION_ACCOUNT,
            source_type=transfer_source_type,
        )


class StripeChargeEventModel(NamedTuple):
    charge_id: str
    amount: int
    user_id: str
    product_id: str
    method: str
    transfer_group: str
    transfer_source_type: str


class StripePaymentHandler(Loggable):

    def _make_stripe_charge_context(self, event):
        return StripeChargeEventModel(
            charge_id=event.data.object.id,
            amount=event.data.object.amount,
            user_id=event.data.object.metadata.user_id,
            product_id=event.data.object.metadata.product_id,
            method=_get_payment_method(event.data.object),
            transfer_group=event.data.object.transfer_group,
            transfer_source_type=_get_transfer_source_type(event.data.object),
        )

    def __init__(self, request, event):
        self.request = request
        self.event = event
        self._event_type_to_execution_fn_mapping = {
            TRANSFER_CREATED: self._post_transfer_success,
            TRANSFER_FAILED: self._post_transfer_failed,
            TOPUP_FAILED: self._post_payment_failed,
            TOPUP_SUCCEEDED: self._post_payment_success,
            CHARGE_FAILED: self._post_payment_failed,
            CHARGE_SUCCEEDED: self._post_payment_success
        }
        if self.event.type in _STRIPE_CHARGE_EVENT:
            self.payment = self._make_stripe_charge_context(event)

    def run(self):
        execution_fn = self._event_type_to_execution_fn_mapping.get(self.event.type)
        if execution_fn:
            execution_fn(request=self.request, event=self.event)

    def with_rents(self):
        payment_identifier = self.payment.transfer_group.split(':')[-1]
        self.rents = RentPayment.objects.filter(identifier=payment_identifier)
        if self.payment.method == ACH_DEBIT:
            self.rents = self.rents.filter(payment_method=ACH_DEBIT)
        elif self.payment.method == CASH:
            self.rents = self.rents.filter(payment_method__in=CASH_EQUIVALENTS)
        return self

    def _process_transfers(self, rents):
        transfer_group = self.payment.transfer_group
        transfer_source_type = self.payment.transfer_source_type
        for rent in rents:
            owners_list = rent.product.owner.all()
            num_owners = len(owners_list)

            # For now, only allow transfers on a single owner product
            if num_owners != 1:
                self.logger.error(
                    'Multiple owner is not yet supported. Cancelling Transfer(s). '
                    f'Original payment event = {self.event.id}'
                )
                return

            self.logger.info(f'Start transferring money to {num_owners} owner(s)')
            _create_transfers(rent, owners_list, transfer_group, transfer_source_type)

    def _post_payment_failed(self, *, request, event):
        for rent in self.rents:
            # Change the status of an existing payment to 'FAILED'
            db_update(rent, dict(status=FAILED))
            # Check if there are any new payments made due to payment failure.
            linked_payments = RentPayment.objects.filter(
                status=PENDING,
                linked_payment=rent,
                linked_reason=FAILED,
            )
            if linked_payments:
                self.logger.info(
                    f'There are payments associated with {rent.id} payment failure.'
                    f'- event_id: {event.id}'
                )
                continue
            # Create a new payment
            RentPayment.objects.create(
                tenant=rent.tenant,
                product=rent.product,
                amount=rent.amount,
                status=PENDING,
                payment_type=RENT,
                due_date=rent.due_date,
                linked_payment=rent,
                linked_reason=FAILED,
            )
        # TODO: 다시 결제 메일 요청
        self.logger.info(f"Payment failure - event_id: {event.id}")

    def _post_payment_success(self, *, request, event):
        # Make sure the user is paying the full amount of unpaid rents, which we'll be updating upon success
        rent_amount = sum(rent.amount for rent in self.rents)
        payment_fee = calculate_payment_fee(self.payment.method, rent_amount)
        rents_id_list = self.rents.values_list('id', flat=True)
        if int(rent_amount + payment_fee) != self.payment.amount:
            self.logger.error(
                f'Payment amount mismatch - '
                f'payment event: {self.event.id}, '
                f'rent payment: {rents_id_list}, '
                f'payment_amount: {self.payment.amount/100}, '
                f'expected_amount: {(rent_amount+payment_fee)/100}'
            )
            messages.error(request, "Transaction Failed")
            return HttpResponse(status=200)

        uncompleted_rents = self.rents.exclude(status=COMPLETE)
        for rent in uncompleted_rents:
            rent.status = COMPLETE
            rent.payment_method = self.payment.method
            if not rent.payment_made_datetime:
                rent.payment_made_datetime = datetime.utcnow()
            db_update(rent)
            # If success is achieved through a payment retry,
            # cancel the payment made in case of failure.
            linked_rents = RentPayment.objects.filter(
                status=PENDING,
                linked_payment=rent,
                linked_reason=FAILED,
            )
            if linked_rents:
                db_update(linked_rents, dict(status=CANCELED))
        self.logger.info(f"Rent payment {rents_id_list} is successfully paid. event_id: {event.id}")
        # Transfer and fail open so that the user can still see payment success message, regardless
        # Note that all we need to do here is distribute the total amount to each owner based on their holdings
        # There is no need to go through each rent object since they are all for the same tenant and product
        self._process_transfers(uncompleted_rents)

    def _post_transfer_success(self, *, request, event):
        self.logger.info(f"Transfer has been successfully processed {event.id}")

    def _post_transfer_failed(self, *, request, event):
        self.logger.error(
            f'Transfer failed for {event.id}. Decline message: "{event.data.object.last_payment_error.message}"'
        )
