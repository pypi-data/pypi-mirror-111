from typing import List, NamedTuple

import stripe
from django.conf import settings

from buildblock.apps.payments.constants import TRANSFER_SOURCE_TYPES
from buildblock.apps.payments.helpers import construct_transfer_group
from buildblock.decorators import memoized_classproperty


class StripeBankModel(NamedTuple):
    '''
    THE BANK ACCOUNT OBJECT
    https://stripe.com/docs/api/customer_bank_accounts/object
    '''
    object: str
    bank_id: str
    account_holder_name: str
    account_holder_type: str
    routing_number: str
    bank_name: str
    account_last4: str
    status: str


class StripeCardModel(NamedTuple):
    '''
    THE BANK ACCOUNT OBJECT
    https://stripe.com/docs/api/customer_bank_accounts/object
    '''
    object: str
    card_id: str
    brand: str
    funding: str
    number_last4: str
    exp_year: int
    exp_month: int
    cvc_check: str


class StripeAccountModel(NamedTuple):
    '''
    THE ACCOUNT OBJECT
    https://stripe.com/docs/api/accounts/object
    details_submitted : Whether account details have been submitted.
    payouts_enabled: Whether Stripe can send payouts to this account.
    payout_schedule: How frequently funds will be paid out. One of manual, daily, weekly, or monthly.
    default_currency: Three-letter ISO currency code representing the default currency.
    external_accounts: External accounts (bank accounts and debit cards) currently attached.
    '''
    account_id: str
    default_currency: str
    details_submitted: bool
    payouts_enabled: bool
    payout_schedule: str
    external_accounts: List


def _get_amount_from_balance_data(balance_object, key, source_type=None):
    # For now, we default to USD balance
    balance_data = [balance for balance in balance_object.get(key) if balance.get("currency") == "usd"]
    if not balance_data:
        return 0
    return balance_data[0].get("amount") if not source_type else balance_data[0].get("source_types").get(source_type, 0)


def _make_external_account_context(external_account):
    if external_account.object == "card":
        return StripeCardModel(
            object=external_account.object,
            card_id=external_account.id,
            brand=external_account.brand,
            funding=external_account.funding,
            number_last4=external_account.last4,
            exp_year=external_account.exp_year,
            exp_month=external_account.exp_month,
            cvc_check=external_account.cvc_check,
        )
    elif external_account.object == "bank_account":
        return StripeBankModel(
            object=external_account.object,
            bank_id=external_account.id,
            account_holder_name=external_account.account_holder_name,
            account_holder_type=external_account.account_holder_type,
            routing_number=external_account.routing_number,
            bank_name=external_account.bank_name,
            account_last4=external_account.last4,
            status=external_account.status
        )
    else:
        return None


class StripeService:

    @memoized_classproperty
    def _client(cls):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        return stripe

    @classmethod
    def add_customer_bank_account(cls, *, customer_id, token_id):
        return cls._client.Customer.create_source(
            customer_id,
            source=token_id,
        )

    @classmethod
    def authorize_oauth_token(cls, *, grant_type, code):
        return cls._client.OAuth.token(
            grant_type=grant_type,
            code=code,
        )

    @classmethod
    def account_modify(cls, *, stripe_account, update_data):
        # https://stripe.com/docs/api/accounts/update
        return cls._client.Account.modify(
            stripe_account,
            **update_data
        )

    @classmethod
    def bank_account_unlink(cls, *, customer_id, bank_id):
        # https://stripe.com/docs/api/customer_bank_accounts/verify
        return cls._client.Customer.delete_source(
            customer_id,
            bank_id,
        )

    @classmethod
    def bank_account_verify(cls, *, customer_id, bank_id, first_amount, second_amount):
        # https://stripe.com/docs/api/customer_bank_accounts/verify
        bank_account = cls._client.Customer.retrieve_source(
            customer_id,
            bank_id,
        )
        return bank_account.verify(amounts=[first_amount, second_amount])

    @classmethod
    def construct_webhook_event(cls, *, payload, signature):
        return cls._client.Webhook.construct_event(
            payload=payload,
            sig_header=signature,
            secret=settings.STRIPE_WEBHOOK_SECRET_KEY,
        )

    @classmethod
    def create_charge_by_bank_account(cls, *, user_model, product_id,
                                      amount, currency, bank_id, payment_identifier=None):
        metadata = dict(user_id=user_model.id, product_id=product_id)
        transfer_group = construct_transfer_group(**metadata, payment_identifier=payment_identifier)
        return cls._client.Charge.create(
            amount=amount,
            currency=currency,
            customer=user_model.profile_tenant.stripe_customer_id,
            source=bank_id,
            metadata=metadata,
            transfer_group=transfer_group,
        )

    @classmethod
    def create_top_up(cls, *, user_model, product_id,
                                        amount, currency, payment_identifier=None):
        metadata = dict(user_id=user_model.id, product_id=product_id)
        transfer_group = construct_transfer_group(**metadata, payment_identifier=payment_identifier)
        return cls._client.Topup.create(
            amount=amount,
            currency=currency,
            metadata=metadata,
            transfer_group=transfer_group,
        )

    @classmethod
    def create_customer_with_bank_account(cls, *, email, description, token_id):
        return cls._client.Customer.create(
            email=email,
            description=description,
            source=token_id
        )

    @classmethod
    def create_dashboard_link(cls, *, account_id):
        return cls._client.Account.create_login_link(
            account_id
        )

    @classmethod
    def create_payment_intent(cls, *, amount, currency, metadata, transfer_group):
        return cls._client.PaymentIntent.create(
            amount=amount,
            currency=currency,
            metadata=metadata,
            transfer_group=transfer_group,
        )

    @classmethod
    def get_account(cls, *, stripe_account):
        account = cls._client.Account.retrieve(stripe_account)
        external_accounts = [
            _make_external_account_context(external_account)
            for external_account in account.external_accounts.data
        ]
        return StripeAccountModel(
            account_id=account.id,
            default_currency=account.default_currency,
            details_submitted=account.details_submitted,
            payouts_enabled=account.payouts_enabled,
            payout_schedule=account.settings.payouts.schedule.interval,
            external_accounts=external_accounts,
        )

    @classmethod
    def get_account_balance(cls, *, stripe_account):
        # https://stripe.com/docs/connect/account-balances#accounting-for-negative-balances
        balance_object = cls._client.Balance.retrieve(
            stripe_account=stripe_account
        )
        # Available: Funds that are available to be transferred or paid out.
        usd_available_balance_amount = _get_amount_from_balance_data(balance_object, "available")
        # Pending: Funds that are not yet available in the balance, due to the 7-day rolling pay cycle.
        usd_pending_balance_amount = _get_amount_from_balance_data(balance_object, "pending")

        return {
            'available_balance_amount': usd_available_balance_amount,
            'pending_balance_amount': usd_pending_balance_amount,
            'total_balance_amount': usd_available_balance_amount + usd_pending_balance_amount
        }

    @classmethod
    def get_balance(cls, source_type=None):
        balance_object = cls._client.Balance.retrieve()
        return _get_amount_from_balance_data(balance_object, "available", source_type)

    @classmethod
    def get_customer_bank_account(cls, *, customer_id, bank_id):
        bank_account = cls._client.Customer.retrieve_source(
            customer_id,
            bank_id,
        )
        return StripeBankModel(
            object=bank_account.object,
            bank_id=bank_account.id,
            account_holder_name=bank_account.account_holder_name,
            account_holder_type=bank_account.account_holder_type,
            routing_number=bank_account.routing_number,
            bank_name=bank_account.bank_name,
            account_last4=bank_account.last4,
            status=bank_account.status
        )

    @classmethod
    def get_customer_bank_account_list(cls, *, customer_id):
        bank_account_list = cls._client.Customer.list_sources(
            customer_id,
            object="bank_account",
        )
        return [
            StripeBankModel(
                object=bank_account.object,
                bank_id=bank_account.id,
                account_holder_name=bank_account.account_holder_name,
                account_holder_type=bank_account.account_holder_type,
                routing_number=bank_account.routing_number,
                bank_name=bank_account.bank_name,
                account_last4=bank_account.last4,
                status=bank_account.status
            )
            for bank_account in bank_account_list.data
        ]

    @classmethod
    def payout(cls, *, amount, currency, stripe_account, destination):
        # https://stripe.com/docs/connect/payouts#regular-payouts
        balance_object = cls._client.Balance.retrieve(
            stripe_account=stripe_account
        )
        remaining_amount = amount
        for source_type in dict(TRANSFER_SOURCE_TYPES):
            source_type_balance = _get_amount_from_balance_data(
                balance_object=balance_object,
                key="available",
                source_type=source_type,
            )
            if source_type_balance <= 0:
                continue

            request_amount = min(remaining_amount, source_type_balance)

            cls._client.Payout.create(
                amount=request_amount,
                currency=currency,
                stripe_account=stripe_account,
                destination=destination,
                source_type=source_type,
            )

            remaining_amount -= request_amount
            if remaining_amount <= 0:
                break

    @classmethod
    def transfer(cls, *, amount, currency, stripe_account, source_type, transfer_group):
        return cls._client.Transfer.create(
            amount=amount,
            currency=currency,
            destination=stripe_account,
            source_type=source_type,
            transfer_group=transfer_group,
        )
