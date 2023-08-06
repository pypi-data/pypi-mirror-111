import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import FAILED, IN_PROGRESS, PENDING, TENANT_ROLE
from buildblock.apps.management.views.base import ManagementPaymentView, ManagementTemplateView
from buildblock.apps.payments.models import RentPayment
from buildblock.apps.users.mixin import ViewPermissionCheckMixin
from buildblock.decorators import catch_errors, require_post
from buildblock.helper import db_update
from buildblock.utils import get_required_post_data, safe_money_read_from_db, sum_field

logger = logging.getLogger(__name__)


class ManagementHouseView(ViewPermissionCheckMixin, ManagementPaymentView):
    permitted_role_list = [TENANT_ROLE]
    template_name = "management/house.html"


class PaymentStatusView(ManagementTemplateView):
    template_name = "management/payment_status.html"

    def _get_payments_status(self, payments):
        submitted_payments = any(payment.status == PENDING for payment in payments)
        failed_payments = any(payment.status == FAILED for payment in payments)
        if not payments:
            return 'not found'
        if failed_payments:
            return 'failed'
        if submitted_payments:
            return 'submitted'
        return 'success'

    def get_context_data(self, *args, **kwargs):
        get_request = self.request.GET
        user_id = get_request.get('userId')
        product_id = get_request.get('productId')
        identifier = get_request.get('identifier')
        action = get_request.get('action')

        payments = RentPayment.objects.filter(
            tenant__id=user_id,
            product__id=product_id,
            identifier=identifier,
        )
        if action == 'posted':
            pending_payments = payments.filter(status=PENDING)
            db_update(pending_payments, dict(
                status=IN_PROGRESS,
                payment_made_datetime=datetime.utcnow(),
            ))
        context = super().get_context_data(**kwargs)
        context['status'] = self._get_payments_status(payments)
        context['date'] = payments[0].payment_made_datetime \
            if payments and payments[0].payment_made_datetime else datetime.utcnow()
        context['amount'] = safe_money_read_from_db(sum_field(payments, 'amount'))
        return context


@catch_errors
@require_post('management')
@login_required
def register_auto_payment(request):
    return_url = get_required_post_data(request, 'return_url')
    bank_id = get_required_post_data(request, 'bank_id')
    lease_id = get_required_post_data(request, 'lease_id')
    user = request.user
    profile = request.user.profile_tenant

    if not bank_id or not profile:
        messages.warning(request, _("Request Failed. Please contact us (info@buildblock.io)."))
        return redirect("management:house")

    lease = user.lease_tenant.filter(id=lease_id)
    db_update(lease, dict(is_auto_paid=True))
    db_update(profile, dict(auto_payment_account_id=bank_id))

    logger.info(f'Auto payment has successfully been setup for {user}')
    messages.success(request, _("Auto payment has been setup."))
    return redirect(return_url)


@catch_errors
@require_post('management')
@login_required
def unregister_auto_payment(request):
    return_url = get_required_post_data(request, 'return_url')
    lease_id = get_required_post_data(request, 'lease_id')
    user = request.user

    if not lease_id:
        messages.warning(request, _("Request Failed. Please contact us (info@buildblock.io)."))
        return redirect("management:house")

    lease = user.lease_tenant.filter(id=lease_id)
    db_update(lease, dict(is_auto_paid=False))

    logger.info(f'Auto payment has successfully been disabled for {user}')
    messages.success(request, _("Auto payment has been disabled."))
    return redirect(return_url)
