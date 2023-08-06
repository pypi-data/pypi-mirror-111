from datetime import datetime

import pytz
import us
from dateutil.relativedelta import relativedelta
from django import forms
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import ACTIVE, CASH, CHECKS
from buildblock.apps.management.models import Lease, LeaseDocs, Maintenance
from buildblock.apps.payments.models import RentPayment
from buildblock.apps.product.models import Product
from buildblock.forms import BaseModelForm, StartEndDateFormValidation

_PAYMENT_METHOD_CHOICE = ((CASH, _('CASH')), (CHECKS, _('CHECKS')))
DATE_INPUT_FORMAT = '%Y-%m-%dT'
DATETIME_INPUT_FORMAT = '%Y-%m-%dT%H:%M'


class ProductForm(BaseModelForm):
    class Meta:
        model = Product
        fields = (
            'agency',
            'title',
            'address_1',
            'address_2',
            'city',
            'state',
            'zip_code',
            'main_image',
            'property_type',
            'sqft',
            'built_year',
            'num_bedroom',
            'num_bathroom',
            'num_parking',
            'num_people',
            'description'
        )

    def __init__(self, *args, **kwargs):
        agency_groups = kwargs.pop("agency_groups")
        super().__init__(*args, **kwargs)
        self.fields['agency'].queryset = agency_groups
        self.fields['agency'].initial = agency_groups.first()


class LeaseForm(BaseModelForm, StartEndDateFormValidation):
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())


class LeaseCreateForm(LeaseForm):
    payment_deposit = forms.BooleanField(label="Create Deposit Payment", required=False)
    payment_rent = forms.BooleanField(label="Create Rent Payment", required=False)

    class Meta:
        model = Lease
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        product_list = kwargs.pop("product_list")
        product = product_list.first()
        super().__init__(*args, **kwargs)
        self.fields['product'].label_from_instance = \
            lambda obj: "%s" % (obj.full_address)
        self.fields['owner'].label_from_instance = \
            lambda obj: "%s (%s)" % (obj.name, obj.email)
        self.fields['tenant'].label_from_instance = \
            lambda obj: "%s (%s)" % (obj.name, obj.email)

        self.fields['product'].queryset = product_list
        self.fields['product'].initial = product
        self.fields['product'].empty_label = None
        self.fields['owner'].queryset = product.owner
        self.fields['owner'].initial = product.owner.first()
        self.fields['owner'].empty_label = None
        self.fields['tenant'].empty_label = None
        self.fields['status'].initial = ACTIVE
        self.fields['status'].empty_label = None


class LeaseUpdateForm(LeaseForm):
    class Meta:
        model = Lease
        fields = (
            'room_num',
            'status',
            'rent',
            'payment_day',
            'start_date',
            'end_date',
        )


class LeaseDocumentForm(BaseModelForm):
    class Meta:
        model = LeaseDocs
        fields = ('lease', 'title', 'document')

    def __init__(self, *args, **kwargs):
        leases = kwargs.pop("leases")
        super().__init__(*args, **kwargs)
        self.fields['lease'].label_from_instance = \
            lambda obj: "%s (%s)" % (obj.tenant.name, obj.product.full_address)
        self.fields['lease'].queryset = leases


class RentPaymentCreateForm(BaseModelForm):
    amount = forms.FloatField()

    class Meta:
        model = RentPayment
        fields = (
            'payment_type',
            'due_date',
        )
        widgets = {
            'due_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        lease = kwargs.pop("lease")
        super().__init__(*args, **kwargs)
        product_state = lease.product.state
        state_info = getattr(us.states, product_state)
        self.today = datetime.now(pytz.timezone(state_info.capital_tz))
        due_date = self.today.replace(day=lease.payment_day)
        if int(self.today.day) >= lease.payment_day:
            due_date = due_date + relativedelta(months=1)
        self.fields['due_date'].initial = due_date

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if self.today.date() > due_date:
            raise forms.ValidationError("The due date must be later than today.")
        return due_date


class RentPaymentUpdateForm(BaseModelForm):
    # TODO: Agent의 현금 처리 방식 결정 후 진행
    # create_transfer = forms.BooleanField(label="Create Transfer", required=False)

    class Meta:
        model = RentPayment
        fields = ('payment_method', 'payment_made_datetime')
        widgets = {
            'payment_made_datetime': forms.DateTimeInput(
                format=DATETIME_INPUT_FORMAT,
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].choices = _PAYMENT_METHOD_CHOICE
        self.fields['payment_made_datetime'].input_formats = [DATETIME_INPUT_FORMAT]


class MaintenanceCreateForm(BaseModelForm):
    class Meta:
        model = Maintenance
        fields = ('product', 'tenant', 'title', 'content')

    def __init__(self, *args, **kwargs):
        product = kwargs.pop("product")
        tenant = kwargs.pop("tenant")
        super().__init__(*args, **kwargs)
        self.fields['product'].widget = forms.HiddenInput()
        self.fields['product'].initial = product
        self.fields['tenant'].widget = forms.HiddenInput()
        self.fields['tenant'].initial = tenant


class MaintenanceUpdateForm(BaseModelForm):
    class Meta:
        model = Maintenance
        fields = ('title', 'content')
