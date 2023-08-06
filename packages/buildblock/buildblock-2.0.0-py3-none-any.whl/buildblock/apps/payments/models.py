from django.db import models

from buildblock.apps.core.constants import (
    PAYMENT_LINKED_REASON_TYPE,
    PAYMENT_TRANSFER_DESTINATION_ACCOUNT_TYPES,
    PAYMENT_TRANSFER_STATUSES,
    RENT,
    RENT_PAYMENT_METHOD_TYPE,
    RENT_PAYMENT_STATUSES,
    RENT_PAYMENT_TYPE
)
from buildblock.apps.core.models import HistoricalRecordModel
from buildblock.apps.payments.constants import TRANSFER_SOURCE_TYPES
from buildblock.apps.product.models import Product
from buildblock.apps.users.models import User


class RentPayment(HistoricalRecordModel):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rent_payments_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="rent_payments_product")
    amount = models.PositiveIntegerField()
    status = models.CharField(choices=RENT_PAYMENT_STATUSES, max_length=30)
    payment_type = models.CharField(choices=RENT_PAYMENT_TYPE, default=RENT, max_length=30)
    payment_method = models.CharField(choices=RENT_PAYMENT_METHOD_TYPE, null=True, blank=True, max_length=30)
    payment_made_datetime = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    # Specifies a unique identifier for the transaction.
    identifier = models.CharField(null=True, blank=True, max_length=100)
    linked_payment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    linked_reason = models.CharField(choices=PAYMENT_LINKED_REASON_TYPE, max_length=30, null=True, blank=True)


class PaymentTransfers(HistoricalRecordModel):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_transfer_tenant")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_transfer_owner")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="payment_transfer_product")
    amount = models.PositiveIntegerField()
    application_fee = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=10)
    destination_account = models.CharField(null=True, blank=True, max_length=32)
    account_type = models.CharField(choices=PAYMENT_TRANSFER_DESTINATION_ACCOUNT_TYPES, max_length=32)
    identifier = models.CharField(max_length=60)
    status = models.CharField(choices=PAYMENT_TRANSFER_STATUSES, max_length=30)
    source_type = models.CharField(choices=TRANSFER_SOURCE_TYPES, max_length=30)
    transfer_datetime = models.DateTimeField(null=True, blank=True)
