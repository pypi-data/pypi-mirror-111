import random
import string
from datetime import date

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from private_storage.views import PrivateStorageDetailView

from buildblock.apps.core import views
from buildblock.apps.core.constants import (
    ACTIVE,
    AGENCY,
    AGENT_ROLE,
    MANAGEMENT_APP_NAME,
    MANAGEMENT_ROLE_SET,
    OWNER_ROLE,
    PENDING,
    TENANT_ROLE
)
from buildblock.apps.management.contexts import ManagementContext
from buildblock.apps.payments.models import RentPayment
from buildblock.apps.product.models import Product
from buildblock.apps.users.mixin import ServiceSignupCheckMixin
from buildblock.mixins import Loggable
from buildblock.services.stripe import StripeService

ALLOWED_DAYS_TO_DISABLE_AUTOPAY = 3


class ManagementAccountMixin(Loggable):
    page_title = "Management Service"
    service_role_set = MANAGEMENT_ROLE_SET
    service_app_name = MANAGEMENT_APP_NAME


class ManagementServiceSetUp:
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if self.active_role == OWNER_ROLE:
            self.products = user.owned_products.all()
        elif self.active_role == AGENT_ROLE:
            self.groups = user.groups.filter(detail__category=AGENCY)
            self.products = Product.objects.filter(agency__in=self.groups)
        elif self.active_role == TENANT_ROLE:
            self.lease = user.lease_tenant.filter(status=ACTIVE).first()
        return super().dispatch(request, *args, **kwargs)


class ManagementServiceMixin(
    ManagementAccountMixin,
    ManagementContext,
    ServiceSignupCheckMixin,
    ManagementServiceSetUp
):
    def _error_message_and_redirect(self, context, error_message, redirect_url):
        messages.warning(self.request, error_message)
        context['redirect_url'] = redirect_url
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.active_role in [OWNER_ROLE, AGENT_ROLE]:
            context['products'] = [
                self._make_product_context(product)
                for product in self.products
            ]
        elif self.active_role == TENANT_ROLE:
            lease = self.request.user.lease_tenant.filter(status=ACTIVE).first()
            context['residence'] = {
                'lease': self._make_lease_context(lease),
                'product': self._make_product_context(lease.product),
                'payments': self._make_payments_context(lease.product),
            } if lease else None

        return context

    def render_to_response(self, context, **response_kwargs):
        if context.get('redirect_url'):
            return redirect(context['redirect_url'])
        return super().render_to_response(context, **response_kwargs)


class ManagementTemplateView(ManagementServiceMixin, views.TemplateView):
    pass


class ManagementListView(ManagementServiceMixin, views.ListView):
    paginate_by = 10


class ManagementDetailView(ManagementServiceMixin, views.DetailView):
    pass


class ManagementCreateView(ManagementServiceMixin, views.CreateView):
    pass


class ManagementUpdateView(ManagementServiceMixin, views.UpdateView):
    pass


class ManagementDeleteView(ManagementServiceMixin, views.DeleteView):
    pass


class ManagementPrivateStorageDetailView(ManagementServiceMixin, PrivateStorageDetailView):
    pass


class ManagementMainPageView(ManagementServiceMixin, views.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.active_role == TENANT_ROLE:
            return reverse('management:house')
        elif self.active_role == OWNER_ROLE:
            return reverse('management:overview')
        elif self.active_role == AGENT_ROLE:
            return reverse('management:product-list')
        else:
            return reverse('management:profile')


class ManagementPaymentView(ManagementTemplateView):
    def _generate_payment_identifier(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_pubkey'] = settings.STRIPE_PUBLISHABLE_KEY
        context['payment_identifier'] = self._generate_payment_identifier()
        context['payment_product_name'] = "Total rent due"

        residence = context.get('residence')
        if residence and self.active_role == TENANT_ROLE:
            # Payment D-day
            payment_dday = 0
            if residence['payments'].unpaid_amount > 0:
                # pay due date
                last_pending_payment = RentPayment.objects.filter(
                    tenant=self.request.user,
                    product__id=residence['product'].id,
                    status=PENDING,
                    due_date__isnull=False
                ).order_by('due_date').first()
                if last_pending_payment:
                    payment_dday = (last_pending_payment.due_date - date.today()).days

            context['payment_dday'] = payment_dday

            # Bank list for ACH payment
            if self.request.user.profile_tenant.stripe_customer_id:
                bank_accounts = StripeService.get_customer_bank_account_list(
                    customer_id=self.request.user.profile_tenant.stripe_customer_id
                )
                context['bank_accounts'] = bank_accounts
                context['has_verified_bank_account'] = \
                    any(bank_account.status == 'verified' for bank_account in bank_accounts)

                # Only allow disabling autopay if we have at least 3 days to process and the user
                # has setup autopay for the given lease
                context['allowed_to_disable_autopay'] = bool(
                    residence['lease'].is_auto_paid and
                    payment_dday > ALLOWED_DAYS_TO_DISABLE_AUTOPAY
                )

        return context
