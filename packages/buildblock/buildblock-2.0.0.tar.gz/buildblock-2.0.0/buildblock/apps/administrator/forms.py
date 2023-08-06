import datetime

from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.postgres.forms import SimpleArrayField

from buildblock.apps.administrator.models import Faq
from buildblock.apps.core import constants
from buildblock.apps.landing.models import (
    CaseStudy,
    CaseStudyPhoto,
    CaseStudyVideo,
    History,
    LandingCarousel,
    LandingDocument,
    LandingInformation,
    LandingPopup,
    LandingThinBanner,
    LandingVideo,
    News,
    Team
)
from buildblock.apps.management.models import Lease
from buildblock.apps.messaging.models import MessagingTemplates
from buildblock.apps.payments.models import PaymentTransfers, RentPayment
from buildblock.apps.product.models import Product
from buildblock.apps.property.constants import (
    PROPERTY_FILTER_SORT_CHOICES,
    PROPERTY_SUBSCRIPTION_FILTER_CHOICES,
    PROPERTY_TYPE_FOR_FILTER_CHOICES
)
from buildblock.apps.users.admin import UserCreationForInvitedUser
from buildblock.apps.users.models import User
from buildblock.forms import BaseModelForm, StartEndDateFormValidation, form_max_min_validation
from buildblock.utils import safe_money_save_from_dollar


class LandingInfoForm(BaseModelForm):

    class Meta:
        model = LandingInformation
        fields = '__all__'


class LandingDocumentForm(BaseModelForm):

    class Meta:
        model = LandingDocument
        fields = '__all__'


class HistoryForm(BaseModelForm):

    class Meta:
        model = History
        fields = '__all__'


class TeamForm(BaseModelForm):

    class Meta:
        model = Team
        fields = '__all__'


class CaseStudyForm(BaseModelForm):

    class Meta:
        model = CaseStudy
        fields = '__all__'


class CaseStudyVideoForm(BaseModelForm):

    class Meta:
        model = CaseStudyVideo
        fields = '__all__'


class CaseStudyPhotoForm(BaseModelForm):

    class Meta:
        model = CaseStudyPhoto
        fields = '__all__'


class NewsForm(BaseModelForm):

    class Meta:
        model = News
        fields = '__all__'


class LandingVideoForm(BaseModelForm):

    class Meta:
        model = LandingVideo
        fields = '__all__'


class LandingCarouselForm(BaseModelForm):
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = LandingCarousel
        fields = '__all__'


class LandingPopupForm(BaseModelForm):
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = LandingPopup
        fields = '__all__'


class LandingThinBannerForm(BaseModelForm):
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = LandingThinBanner
        fields = '__all__'


class FaqForm(BaseModelForm):
    question = forms.CharField()
    answer = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Faq
        fields = "__all__"


class RentPaymentForm(BaseModelForm):
    due_date = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = RentPayment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_select_label_from_instance('tenant')
        self._product_select_label_from_instance('product')

    def clean(self):
        cleaned_data = super().clean()
        # Unit Change
        cleaned_data['amount'] = safe_money_save_from_dollar(cleaned_data.get('amount'))
        return cleaned_data


class PaymentTransfersForm(BaseModelForm):
    class Meta:
        model = PaymentTransfers
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_select_label_from_instance('owner')
        self._user_select_label_from_instance('tenant')
        self._product_select_label_from_instance('product')

    def clean(self):
        cleaned_data = super().clean()
        # Unit Change
        cleaned_data['amount'] = safe_money_save_from_dollar(cleaned_data.get('amount'))
        cleaned_data['application_fee'] = safe_money_save_from_dollar(cleaned_data.get('application_fee'))
        return cleaned_data


class LeaseForm(BaseModelForm, StartEndDateFormValidation):
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())
    move_in_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    move_out_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)

    class Meta:
        model = Lease
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_select_label_from_instance('owner')
        self._user_select_label_from_instance('tenant')
        self._product_select_label_from_instance('product')
        # Date Initial
        start_date = datetime.date.today()
        end_date = start_date + relativedelta(years=1, days=-1)
        self.fields['start_date'].initial = start_date
        self.fields['end_date'].initial = end_date
        self.fields['move_in_date'].initial = start_date
        self.fields['move_out_date'].initial = end_date

    def clean(self):
        cleaned_data = super().clean()
        # Rent & Deposit Unit Change
        cleaned_data['rent'] = safe_money_save_from_dollar(cleaned_data.get('rent'))
        cleaned_data['deposit'] = safe_money_save_from_dollar(cleaned_data.get('deposit'))

        # Move in & out Date Validation
        move_out_date = cleaned_data.get('move_out_date')
        move_in_date = cleaned_data.get('move_in_date')
        if move_out_date and move_in_date and move_out_date <= move_in_date:
            raise forms.ValidationError("Move out date must be later than move in date")

        return cleaned_data


class LeaseCreateForm(LeaseForm):
    payment_deposit = forms.BooleanField(label="Create Deposit Payment", required=False)
    payment_rent = forms.BooleanField(label="Create Rent Payment", required=False)


class UserForm(BaseModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'nationality',
            'phone_number',
            'email',
        )


class InvitedUserForm(UserForm, UserCreationForInvitedUser):
    pass


class ProductForm(BaseModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class ChargePaymentValidationForm(forms.Form):
    return_url = forms.CharField()
    payment_id = forms.IntegerField()
    method = forms.ChoiceField(choices=constants.RENT_PAYMENT_METHOD_TYPE)


class PropertyFilterForm(forms.Form):
    city = forms.CharField()
    state_code = forms.ChoiceField(choices=constants.US_STATE_CHOICES, initial="CA")
    limit = forms.IntegerField(required=False, min_value=0, max_value=200)
    sort = forms.ChoiceField(choices=PROPERTY_FILTER_SORT_CHOICES, required=False)
    price_min = forms.IntegerField(min_value=0, required=False)
    price_max = forms.IntegerField(min_value=0, required=False)
    beds_min = forms.IntegerField(min_value=0, required=False)
    beds_max = forms.IntegerField(min_value=0, required=False)
    baths_min = forms.IntegerField(min_value=0, required=False)
    baths_max = forms.IntegerField(min_value=0, required=False)
    property_type = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=PROPERTY_TYPE_FOR_FILTER_CHOICES,
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        for param_name in ['price', 'beds', 'baths']:
            form_max_min_validation(cleaned_data, param_name)


class PropertyFilterCreateForm(PropertyFilterForm):
    title = forms.CharField()
    emails = SimpleArrayField(forms.CharField(max_length=100))
    status = forms.ChoiceField(choices=PROPERTY_SUBSCRIPTION_FILTER_CHOICES)
    messaging_template = forms.ModelChoiceField(
        queryset=MessagingTemplates.objects.filter(category=constants.PROPERTY)
    )
    field_order = ['title', 'emails', 'status', 'messaging_template']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['messaging_template'].label_from_instance = lambda obj: obj.title
