from datetime import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from marshmallow import ValidationError
from simple_history.models import HistoricalRecords

from buildblock.apps.core.constants import RECORD_DATETIME_FORMAT

PHONE_NUMBER_REGEX_VALIDATOR = RegexValidator(
    regex=r'^\d{9,15}$',
    message=_("Please enter only numbers. Up to 15 digits allowed."),
)


def get_full_address(instance):
    if not hasattr(instance, 'address_1') or not instance.address_1:
        return ''
    full_address = instance.address_1
    conv = lambda i: i or ''
    for attr in ['address_2', 'city', 'state', 'zip_code']:
        single_content = conv(getattr(instance, attr))
        if single_content:
            full_address += ", " + single_content
    return full_address


def add_read_data_at_record(records, user):
    records['read'] = records.get('read', [])
    read_data = {
        'reader': user.id,
        'datetime': datetime.utcnow().strftime(RECORD_DATETIME_FORMAT),
    }
    records['read'].append(read_data)
    return records


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def schema_list_valid(self, schema, list_name):
        try:
            list = getattr(self, list_name)
            if list:
                schema(many=True).load(list)
        except ValidationError:
            return False
        else:
            return True


class HistoricalRecordModel(TimeStampedModel):
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class ZipcodeField(models.CharField):
    description = "Zip Code"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 5
        kwargs['validators'] = [RegexValidator(
            regex=r'^[0-9]{5}$',
            message=_("Must be a valid Zipcode in format 12345"),
        )]
        super().__init__(*args, **kwargs)


class ExpenseModel(HistoricalRecordModel):
    amount = models.PositiveIntegerField(_("Amount"), blank=True, null=True)
    date = models.DateField(_("Date"))
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        abstract = True
