import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import ACTIVE, AGENT_ROLE, TENANT_ROLE
from buildblock.apps.core.views import TemplateView
from buildblock.apps.management.views.base import ManagementAccountMixin, ManagementUpdateView
from buildblock.apps.users.forms import UpdateGroupDetailForm
from buildblock.apps.users.mixin import ViewPermissionCheckMixin
from buildblock.apps.users.models import GroupDetail
from buildblock.apps.users.views import (
    ServiceRoleSelectView,
    ServiceRoleSignupSelectView,
    ServiceRoleSignupView,
    ServiceRoleUpdateView
)
from buildblock.helper import db_update
from buildblock.services.stripe import StripeService

logger = logging.getLogger(__name__)


# Signup Role
class ManagementRoleSignupView(ManagementAccountMixin, ServiceRoleSignupView):
    pass


# Update User Base Information
class ManagementRoleUpdateView(ManagementAccountMixin, ServiceRoleUpdateView):
    pass


# Signup Service Select
class ManagementRoleSignupSelectView(ManagementAccountMixin, ServiceRoleSignupSelectView):
    pass


# Select Role
class ManagementRoleSelectView(ManagementAccountMixin, ServiceRoleSelectView):
    pass


# Update User Base Information
class ManagementBankAccountRegistrationView(ManagementAccountMixin, ViewPermissionCheckMixin, TemplateView):
    permitted_role_list = [TENANT_ROLE]
    template_name = "account/bank_account_registration.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_pubkey'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


# Update Agency Group Info
class ManagementGroupUpdateView(ManagementUpdateView):
    permitted_role_list = [AGENT_ROLE]
    model = GroupDetail
    form_class = UpdateGroupDetailForm
    template_name = 'management/group-update.html'
    page_title = 'Edit Group Info.'

    def get_success_url(self):
        return reverse('management:profile')


# Create Stripe Customer by Bank Account
@login_required
def bank_account_register(request):
    token_id = request.GET.get('token_id')
    if not token_id:
        logger.error(f'Error has occurred while creating stripe bank token: {request.user.id}')
        messages.warning(request, _("Request Failed. Please try again."))
        return redirect("management:bank-account-registration")

    # Create stripe customer id by bank account token
    profile = request.user.profile_tenant
    if not profile:
        messages.warning(request, _('Please apply for the Tenant role.'))
        return redirect("management:signup-role", user_role=TENANT_ROLE)

    try:
        if profile.stripe_customer_id:
            StripeService.add_customer_bank_account(
                customer_id=profile.stripe_customer_id,
                token_id=token_id,
            )
        else:
            customer = StripeService.create_customer_with_bank_account(
                email=request.user.email,
                description=request.user.name,
                token_id=token_id,
            )
            logger.info(f'Stripe customer Created: customer- {customer.id}')
            db_update(profile, dict(stripe_customer_id=customer.id))
    except Exception as err:
        # TODO: 에러 구분하여 처리
        action = 'adding bank account' if profile.stripe_customer_id else 'creating customer'
        logger.error(f'Error has occurred while {action}: {str(err)}')
        messages.warning(request, _("Request Failed. Please try again."))
        return redirect("management:bank-account-registration")

    messages.success(request, _("Bank account registration completed."))
    return redirect("management:profile")


# Delete Stripe Bank Account
@login_required
def bank_account_unlink(request):
    bank_id = request.POST.get('bank_id')
    customer_id = request.user.profile_tenant.stripe_customer_id

    if not bank_id or not customer_id:
        messages.warning(request, _("Request Failed. Please contact us (info@buildblock.io)."))
        return redirect("management:profile")

    auto_paid_active_leases = request.user.lease_tenant.filter(status=ACTIVE, is_auto_paid=True)
    if request.user.profile_tenant.auto_payment_account_id == bank_id and auto_paid_active_leases:
        messages.warning(request, _("You cannot unlink an account that is being used for auto payment"))
        return redirect("management:profile")

    try:
        StripeService.bank_account_unlink(
            customer_id=customer_id,
            bank_id=bank_id,
        )
    except stripe.error.CardError as e:
        error = e.json_body.get('error')
        error_message = error.get('message')
        error_type = error.get('type')
        logger.error(f'Error has occurred while unlinking the bank account: detail - {error_type}')
        messages.warning(request, error_message)
    except Exception as e:
        logger.error(f'Error has occurred while unlinking the bank account: {e}')
        messages.warning(request, _("Request Failed. Please try again."))
    else:
        messages.success(request, _("Bank account has been unlinked."))

    return redirect("management:profile")


# Verify Stripe Bank Account
@login_required
def bank_account_verify(request):
    bank_id = request.POST.get('bank_id')
    customer_id = request.user.profile_tenant.stripe_customer_id

    if not bank_id or not customer_id:
        messages.warning(request, _("Request Failed. Please contact us (info@buildblock.io)."))
        return redirect("management:profile")

    first_amount = int(float(request.POST.get('first_amount', 0)) * 100)
    second_amount = int(float(request.POST.get('second_amount', 0)) * 100)

    try:
        StripeService.bank_account_verify(
            customer_id=customer_id,
            bank_id=bank_id,
            first_amount=first_amount,
            second_amount=second_amount
        )
    except stripe.error.CardError as e:
        error = e.json_body.get('error')
        error_message = error.get('message')
        error_type = error.get('type')
        logger.error(f'Error has occurred while verifying the bank account: detail - {error_type}')
        messages.warning(request, error_message)
    except Exception as e:
        logger.error(f'Error has occurred while verifying the bank account: {e}')
        messages.warning(request, _("Request Failed. Please try again."))
    else:
        messages.success(request, _("Bank account has been verified."))

    return redirect("management:profile")
