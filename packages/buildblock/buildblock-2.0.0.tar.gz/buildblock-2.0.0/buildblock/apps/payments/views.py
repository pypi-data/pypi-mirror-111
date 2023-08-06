import json
import logging
from datetime import datetime

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from buildblock.apps.core.constants import ACH_DEBIT, CREDIT_CARD, DEBIT_CARD, IN_PROGRESS, PENDING
from buildblock.apps.payments.constants import (
    ACCOUNT_VERIFIED,
    AUTHORIZATION_CODE,
    CHARGE_FAILED,
    CHARGE_SUCCEEDED,
    PAYMENT_INTENT_PAYMENT_FAILED,
    TOPUP_FAILED,
    TOPUP_SUCCEEDED
)
from buildblock.apps.payments.handlers import StripePaymentHandler
from buildblock.apps.payments.helpers import construct_transfer_group
from buildblock.apps.payments.models import RentPayment
from buildblock.apps.users.models import ProfileOwner
from buildblock.apps.view_control import is_valid_post_request
from buildblock.helper import db_update
from buildblock.services.stripe import StripeService

logger = logging.getLogger(__name__)

_STRIPE_EVENT_PAYMENT_METHOD_MAPPING = {
    'credit': CREDIT_CARD,
    'debit': DEBIT_CARD,
}

_STRIPE_EVENT_WEBHOOK_HANDLER_SET = frozenset([
    CHARGE_FAILED,
    CHARGE_SUCCEEDED,
    TOPUP_FAILED,
    TOPUP_SUCCEEDED,
    PAYMENT_INTENT_PAYMENT_FAILED
])


def stripe_oauth_token_view(request):
    try:
        oauth_token = StripeService.authorize_oauth_token(
            grant_type=AUTHORIZATION_CODE,
            code=request.GET.get('code'),
        )
        stripe_user_id = oauth_token['stripe_user_id']
        profile = ProfileOwner.objects.filter(user=request.user)
        db_update(profile, dict(stripe_account=stripe_user_id))
    except Exception as err:
        logger.error(f'Error has occurred while generating stripe user: {err}')
    else:
        logger.info(
            f'User "{request.user}" has been successfully authorized. stripe_user_id={stripe_user_id}')

    return redirect('management:profile')


@csrf_exempt
@require_POST
def stripe_payment_intents_view(request):
    payment_modal_payload = json.loads(request.body)
    product_id = payment_modal_payload['productId']
    amount = payment_modal_payload['amount']
    outstanding_balance = payment_modal_payload['outstandingBalance']
    user_id = payment_modal_payload['userId']
    payment_identifier = payment_modal_payload.get('paymentIdentifier')
    if not amount:
        # If there is no rent to pay, no need to create an intent
        return HttpResponse(status=200)
    payment_intent = StripeService.create_payment_intent(
        amount=amount,
        currency=payment_modal_payload['currency'],
        metadata=dict(
            user_id=user_id,
            product_id=product_id,
            outstanding_balance=outstanding_balance,
        ),
        transfer_group=construct_transfer_group(user_id, product_id, payment_identifier),
    )
    rents = RentPayment.objects.filter(tenant__id=user_id, product__id=product_id, status=PENDING)
    db_update(rents, dict(identifier=payment_identifier))
    return JsonResponse(payment_intent)


@csrf_exempt
@require_POST
def stripe_webhook_view(request):
    try:
        event = StripeService.construct_webhook_event(
            payload=request.body,
            signature=request.META['HTTP_STRIPE_SIGNATURE']
        )
    except ValueError as err:
        # Invalid payload
        logger.error(f'Failed to create webhook event: {err}')
        return HttpResponse(status=400)
    except Exception as err:
        logger.error(f'Unhandled exception error occurred: {err}')
        return HttpResponse(status=500)

    logger.info(f'Webhook event received for {event.id}: {event.type}')

    handler = StripePaymentHandler(request, event)
    if event.type in _STRIPE_EVENT_WEBHOOK_HANDLER_SET:
        handler = handler.with_rents()

    handler.run()

    return HttpResponse(status=200)


@require_POST
def stripe_ach_charge_view(request):
    amount = request.POST.get('amount')
    currency = request.POST.get('currency')
    product_id = request.POST.get('product_id')
    payment_identifier = request.POST.get('payment_identifier')
    bank_id = request.POST.get('bank_id')
    customer_id = request.user.profile_tenant.stripe_customer_id

    # Bank account verification check
    try:
        bank_account = StripeService.get_customer_bank_account(
            customer_id=customer_id,
            bank_id=bank_id,
        )
        if bank_account.status != ACCOUNT_VERIFIED:
            messages.warning(request, _("Please try after your bank account is verified."))
            return redirect('management:profile')

        payment = StripeService.create_charge_by_bank_account(
            user_model=request.user,
            product_id=product_id,
            amount=amount,
            currency=currency,
            bank_id=bank_id,
            payment_identifier=payment_identifier,
        )
    except Exception as err:
        messages.warning(request, _("Please try again."))
        logger.error(f'Error has occurred while generating stripe user: {err}')
    else:
        rents = RentPayment.objects.filter(identifier=payment_identifier)
        db_update(rents, dict(
            status=IN_PROGRESS,
            payment_method=ACH_DEBIT,
            payment_made_datetime=datetime.utcnow(),
        ))
        messages.success(request, _("The ACH payment request has been completed."))
        logger.info(f'The ACH payment request has been completed: payment_id={payment.id}')

    return redirect('management:house')


def stripe_payout_view(request):
    if not is_valid_post_request(request):
        return redirect('management:home')

    request_amount = int(float(request.POST.get('payout_request_amount', 0)) * 100)
    destination = request.POST.get('destination')
    currency = request.POST.get('currency')

    # Request amount check: over $100
    if request_amount < 10000:
        messages.warning(request, _('The minimum payout amount is $100.'))
        return redirect('management:overview')

    # Balance check
    stripe_account = request.user.profile_owner.stripe_account
    stripe_balance = StripeService.get_account_balance(
        stripe_account=stripe_account
    )
    if request_amount > stripe_balance['available_balance_amount']:
        messages.warning(request, _('You do not have enough balance.'))
        return redirect('management:overview')

    # Payout
    try:
        StripeService.payout(
            amount=request_amount,
            currency=currency,
            stripe_account=stripe_account,
            destination=destination,
        )
    except Exception as e:
        messages.warning(request, _('Payout Request - Failed. Please try again.'))
        logger.warning(f'Failed Payout Request: Owner-{request.user.id}, Amount-{request_amount}. Details: {str(e)}')
    else:
        messages.success(request, _('Payout Request - Success. Will be paid in two days'))
        logger.info(f'Completed Payout Request: Owner-{request.user.id}, Amount-{request_amount}')

    return redirect('management:overview')


def stripe_payout_schedule_change_view(request):
    if not is_valid_post_request(request):
        return redirect('management:home')

    request_payout_schedule = request.POST.get('payout_schedule')
    if not request_payout_schedule:
        messages.warning(request, _('Please try again.'))
        return redirect('management:overview')

    try:
        update_data = {
            'settings': {
                'payouts': {
                    'schedule': {
                        "interval": request_payout_schedule
                    }
                }
            }
        }
        StripeService.account_modify(
            stripe_account=request.user.profile_owner.stripe_account,
            update_data=update_data
        )
    except Exception as e:
        messages.warning(request, _('Please try again.'))
        logger.warning(f'Failed payout schedule change: Owner-{request.user.id}. Details: {str(e)}')
    else:
        messages.success(request, _('Your payout schedule has been updated.'))
        logger.info(f'Updated payout schedule change: Owner-{request.user.id}')

    return redirect('management:overview')
