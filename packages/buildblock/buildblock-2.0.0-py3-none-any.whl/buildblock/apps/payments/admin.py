from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from buildblock.apps.payments.models import PaymentTransfers, RentPayment


@admin.register(RentPayment)
class RentPaymentAdmin(SimpleHistoryAdmin):
    list_display = ['tenant', 'product', 'amount', 'status', 'payment_type', 'due_date', 'identifier']
    search_fields = ['tenant', 'product', 'amount', 'status', 'payment_type', 'due_date', 'identifier']


@admin.register(PaymentTransfers)
class PaymentTransfersAdmin(SimpleHistoryAdmin):
    list_display = ['tenant', 'owner', 'product', 'amount', 'currency', 'destination_account', 'account_type',
                    'identifier', 'status']
    search_fields = ['tenant', 'owner', 'product', 'amount', 'currency', 'destination_account', 'account_type',
                     'identifier', 'status']
