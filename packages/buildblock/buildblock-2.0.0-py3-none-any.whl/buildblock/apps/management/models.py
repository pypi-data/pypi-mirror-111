from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from private_storage.fields import PrivateFileField

from buildblock.apps.core import constants
from buildblock.apps.core.models import HistoricalRecordModel, TimeStampedModel
from buildblock.apps.payments.models import RentPayment
from buildblock.apps.product.models import Product
from buildblock.apps.users.models import User
from buildblock.decorators import memoized_property

INVOICE_PERIOD_REGEX_VALIDATOR = RegexValidator(
    r'^\d{4}-\d{2}$', "Period for invoice field should be in the format of YYYY-MM"
)


def lease_document_path(instance, filename):
    return f"lease/{instance.lease.id}/document/{filename}"


class Lease(HistoricalRecordModel):
    """This model represents the lease contract between the tenant and house owner"""
    room_num = models.CharField(_("Room Number"), max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lease_owner')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lease_tenant')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lease_product')
    status = models.CharField(_("Status"), choices=constants.LEASE_STATUS_CHOICES, max_length=20)
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"))
    rent = models.PositiveIntegerField(_("Rent"))
    deposit = models.PositiveIntegerField(_("Deposit"))
    payment_day = models.PositiveIntegerField(_("Payment Day"), default=1, validators=[MaxValueValidator(31)])
    move_in_date = models.DateTimeField(_("Move-in Date"), null=True, blank=True)
    move_out_date = models.DateTimeField(_("Move-out Date"), null=True, blank=True)
    is_auto_paid = models.BooleanField(_("Automatic Payment"), default=False)
    # TODO: Maybe add fields that append images

    @memoized_property
    def num_paid_rents(self):
        return RentPayment.objects.filter(
            tenant=self.tenant,
            product=self.product,
            payment_type=constants.RENT,
            status=constants.COMPLETE,
        ).count()


class LeaseDocs(HistoricalRecordModel):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='docs')
    title = models.CharField(_("Document title"), max_length=200)
    document = PrivateFileField(_("Document file"), upload_to=lease_document_path)
    records = models.JSONField(default=dict, null=True, blank=True)


class Invoice(TimeStampedModel):
    """This model represents the invoice that is generated for the least contract
    between the tenant and house owner"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='invoice_product')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoice_owner')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoice_tenant')
    period = models.CharField(_("Period"), validators=[INVOICE_PERIOD_REGEX_VALIDATOR], max_length=15)
    unit = models.CharField(choices=constants.BASE_UNIT_CHOICES, default='USD', max_length=20)
    detailed_amount = models.JSONField(default=dict)   # Breakdowns of invoice
    amount = models.PositiveIntegerField(_("Rent"))


class Maintenance(TimeStampedModel):
    """This model represents the list of maintenance requests and their status"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='maintenance_product')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maintenance_tenant')
    is_read = models.BooleanField(default=False)
    status = models.CharField(_("Status"),
                              choices=constants.MAINTENANCE_STATUS_CHOICES,
                              default=constants.PENDING,
                              max_length=20)
    title = models.CharField(_("Title"), max_length=100)
    content = RichTextUploadingField(_("Content"), max_length=400)
    comments = models.JSONField(default=dict)

    def clean(self):
        if not self._has_valid_comment:
            raise Exception('Invalid schema for the comments field')

    @property
    def _has_valid_comment(self):
        """
        {
            "(created_time_in_epoch|type:timestamp > 1567768207.260894)": {
                "writer": (user.id),
                "content": (comment),
            }
        }
        """
        _required_key_set = {'writer', 'content'}

        # Check if the key is in epoch and can be converted to a float
        for key_in_epoch in self.comments.keys():
            try:
                float(key_in_epoch)
            except Exception:
                return False

        if (len(self.comments) == 0):
            return True

        # Check if the required key fields are set
        comment_list = self.comments.values()  # [{'writer': 5, 'content': 'hello'}, {'writer': 7, 'content': 'world'}]
        return all([set(comment.keys()) == _required_key_set for comment in comment_list])
