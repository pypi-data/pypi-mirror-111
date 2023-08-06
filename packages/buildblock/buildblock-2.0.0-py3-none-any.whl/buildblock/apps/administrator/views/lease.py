import logging
from datetime import datetime

from django.contrib import messages
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.administrator.forms import (
    ChargePaymentValidationForm,
    LeaseCreateForm,
    LeaseForm,
    PaymentTransfersForm,
    RentPaymentForm
)
from buildblock.apps.administrator.views.base import AdministratorServiceMixin
from buildblock.apps.core.constants import IN_PROGRESS, PENDING
from buildblock.apps.core.views import CreateView, DeleteView, DetailView, ListView, UpdateView
from buildblock.apps.management.contexts import ManagementContext
from buildblock.apps.management.models import Lease
from buildblock.apps.payments.constants import CURRENCY_USD
from buildblock.apps.payments.models import PaymentTransfers, RentPayment
from buildblock.decorators import catch_errors, require_post
from buildblock.helper import db_update
from buildblock.services.management import ManagementService
from buildblock.services.stripe import StripeService

logger = logging.getLogger(__name__)


@catch_errors
@require_post('administrator')
def charge_payment(request):
    form = ChargePaymentValidationForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return_url = form.cleaned_data.get('return_url')
    payment_id = form.cleaned_data.get('payment_id')
    method = form.cleaned_data.get('method')

    payment = RentPayment.objects.get(id=payment_id)
    if payment.status != PENDING:
        messages.warning(request, _("The payment is already in progress or has been completed."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Charge Stripe Balances
    result = StripeService.create_top_up(
        user_model=request.user,
        product_id=payment.product.id,
        amount=payment.amount,
        currency=CURRENCY_USD,
    )
    payment_identifier = result.transfer_group.split(':')[-1]

    # Change Payment
    data_dict = dict(
        payment_made_datetime=datetime.utcnow(),
        payment_method=method,
        status=IN_PROGRESS,
        identifier=payment_identifier,
    )
    db_update(payment, data_dict)

    messages.success(request, _("The payment has been paid."))
    return redirect(return_url)


class AdministratorLeaseView(AdministratorServiceMixin):
    model = Lease
    success_url = reverse_lazy('administrator:lease')

    def form_valid(self, form):
        # Create or Update Lease
        self.object = lease = form.save(commit=False)
        try:
            ManagementService.duplication_live_lease_validation(lease)
        except ValidationError as e:
            messages.error(self.request, e.message)
            return self.form_invalid(form)
        db_update(form)
        # Create Payment
        if form.cleaned_data.get('payment_deposit'):
            ManagementService.create_deposit_payment(lease)
        if form.cleaned_data.get('payment_rent'):
            ManagementService.create_first_rent_payment(lease)
        return super().form_valid(form)


class LeaseListView(AdministratorLeaseView, ManagementContext, ListView):
    page_title = "Leases"
    template_name = "administrator/lease_list.html"
    context_object_name = "leases"
    ordering = ['id']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        leases = context[self.context_object_name]
        context[self.context_object_name] = [
            self._make_lease_context(lease)
            for lease in leases
        ]
        return context


class LeaseDetailView(AdministratorLeaseView, DetailView):
    page_title = "Lease Info."
    template_name = "administrator/lease_detail.html"
    context_object_name = "lease"


class LeaseCreateView(AdministratorLeaseView, CreateView):
    page_title = "Create Lease"
    form_class = LeaseCreateForm
    template_name = 'administrator/lease_form.html'


class LeaseUpdateView(AdministratorLeaseView, UpdateView):
    page_title = "Update Lease"
    form_class = LeaseForm
    template_name = 'administrator/lease_form.html'


class LeaseDeleteView(AdministratorLeaseView, DeleteView):
    page_title = "Delete Lease"
    template_name = 'administrator/base_confirm_delete.html'


class AdministratorPaymentView(AdministratorServiceMixin):
    model = RentPayment
    success_url = reverse_lazy('administrator:payment')
    form_class = RentPaymentForm


class PaymentListView(AdministratorPaymentView, ManagementContext, ListView):
    page_title = "Payments"
    template_name = "administrator/payment_list.html"
    context_object_name = "payments"
    ordering = ['-id']
    paginate_by = 50


class PaymentDetailView(AdministratorPaymentView, DetailView):
    page_title = "Peyment Info."
    template_name = "administrator/payment_detail.html"
    context_object_name = "payment"


class PaymentCreateView(AdministratorPaymentView, CreateView):
    page_title = "Create Peyment"
    template_name = 'administrator/payment_form.html'


class PaymentUpdateView(AdministratorPaymentView, UpdateView):
    page_title = "Update Peyment"
    template_name = 'administrator/payment_form.html'


class PaymentDeleteView(AdministratorPaymentView, DeleteView):
    page_title = "Delete Peyment"
    template_name = 'administrator/base_confirm_delete.html'


# Payment Transfer
class AdministratorPaymentTransferView(AdministratorServiceMixin):
    model = PaymentTransfers
    success_url = reverse_lazy('administrator:payment-transfer')
    form_class = PaymentTransfersForm


class PaymentTransferListView(AdministratorPaymentTransferView, ManagementContext, ListView):
    page_title = "Transfer Payments"
    template_name = "administrator/payment_transfer_list.html"
    context_object_name = "transfers"
    ordering = ['-id']
    paginate_by = 50


class PaymentTransferDetailView(AdministratorPaymentTransferView, DetailView):
    page_title = "Transfer Payments Info."
    template_name = "administrator/payment_transfer_detail.html"
    context_object_name = "transfer"


class PaymentTransferCreateView(AdministratorPaymentTransferView, CreateView):
    page_title = "Create Transfer Payment"
    template_name = 'administrator/payment_transfer_form.html'


class PaymentTransferUpdateView(AdministratorPaymentTransferView, UpdateView):
    page_title = "Update Transfer Payment"
    template_name = 'administrator/payment_transfer_form.html'


class PaymentTransferDeleteView(AdministratorPaymentTransferView, DeleteView):
    page_title = "Delete Transfer Payment"
    template_name = 'administrator/base_confirm_delete.html'
