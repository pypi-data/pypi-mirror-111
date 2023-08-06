import logging
from datetime import datetime

from django.contrib import messages
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import AGENT_ROLE, COMPLETE, IN_PROGRESS, OWNER_ROLE, PENDING, TENANT_ROLE
from buildblock.apps.management.forms import RentPaymentCreateForm, RentPaymentUpdateForm
from buildblock.apps.management.views.base import (
    ManagementCreateView,
    ManagementDetailView,
    ManagementListView,
    ManagementUpdateView
)
from buildblock.apps.payments.constants import CURRENCY_USD, PAYMENT_PENDING
from buildblock.apps.payments.models import RentPayment
from buildblock.apps.users.mixin import ViewPermissionCheckMixin
from buildblock.services.management import ManagementService
from buildblock.services.product import ProductService
from buildblock.services.stripe import StripeService
from buildblock.utils import safe_money_save_from_dollar

logger = logging.getLogger(__name__)


class ManagementTransactionMixin:
    model = RentPayment
    page_title = 'Transaction'
    form_class = RentPaymentUpdateForm
    success_url = reverse_lazy('management:transaction')
    context_object_name = "transaction"


class ManagementTransactionListView(ManagementTransactionMixin, ManagementListView):
    template_name = "management/transaction.html"
    context_object_name = "transactions"
    paginate_by = 20

    def with_product_id_filter(self, queryset):
        product_id = self.request.GET.get('product')
        return queryset.filter(product__id=product_id) if product_id else queryset

    def with_status_filter(self, queryset):
        status = self.request.GET.get('status')
        return queryset.filter(status=status) if status else queryset

    def with_role_filter(self, queryset):
        if self.active_role == TENANT_ROLE:
            return queryset.filter(tenant=self.request.user)
        return queryset.filter(product__in=self.products)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.with_product_id_filter(queryset)
        queryset = self.with_status_filter(queryset)
        queryset = self.with_role_filter(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        outstanding_payments = self.object_list.filter(status=PENDING)
        context['outstanding_payments_total'] = outstanding_payments.aggregate(
            count=Count('id'),
            amount=Coalesce(Sum('amount'), 0)
        )
        product_id = self.request.GET.get('product')
        if product_id:
            product = ProductService.get_product_by_id(self.request.GET.get('product'))
            context['selected_product_filter'] = product.full_address
        return context


class ManagementTransactionDetailView(ManagementTransactionMixin, ManagementDetailView):
    template_name = "management/transaction-read.html"
    page_title = 'Transaction'


class ManagementTransactionFormMixin(ManagementTransactionMixin, ViewPermissionCheckMixin):
    permitted_role_list = [AGENT_ROLE, OWNER_ROLE]
    template_name = "management/transaction-write.html"
    page_title = 'Edit Transaction'


class ManagementTransactionUpdateView(ManagementTransactionFormMixin, ManagementUpdateView):
    template_name = "management/transaction-update.html"
    page_title = 'Change to Paid'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.payment_made_datetime:
            obj.payment_made_datetime = datetime.utcnow()
        return obj

    def form_valid(self, form):
        payment = form.save(commit=False)
        if payment.status != PENDING:
            messages.warning(self.request, _("The payment is already in progress or has been completed."))
            return self.form_invalid(form)
        payment.status = COMPLETE

        # Charge Stripe Balances
        if form.cleaned_data.get('create_transfer'):
            result = StripeService.create_top_up(
                user_model=self.request.user,
                product_id=payment.product.id,
                amount=payment.amount,
                currency=CURRENCY_USD,
            )
            if result.status != PAYMENT_PENDING:
                messages.warning(self.request, _("The payment transfer generation failed."))
                logger.error(
                    'The payment update failed.'
                    f'payment id - {payment.id}, stripe id - {result.id}'
                )
                return self.form_invalid(form)
            payment.payment_identifier = result.transfer_group.split(':')[-1]
            payment.status = IN_PROGRESS

        return super().form_valid(form)


class ManagementTransactionCreateView(ManagementTransactionFormMixin, ManagementCreateView):
    page_title = 'Create Payment'
    form_class = RentPaymentCreateForm
    template_name = "management/transaction-create.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            self.lease = ManagementService.get_lease_by_id(self.kwargs.get('lease_id'))
        except Exception:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['lease'] = self.lease
        return kwargs

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        payment = form.save(commit=False)
        payment.tenant = self.lease.tenant
        payment.product = self.lease.product
        payment.amount = safe_money_save_from_dollar(amount)
        payment.status = PENDING
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lease'] = self.lease
        return context

    def get_success_url(self):
        return reverse('management:tenant-detail', kwargs={'pk': self.lease.id})
