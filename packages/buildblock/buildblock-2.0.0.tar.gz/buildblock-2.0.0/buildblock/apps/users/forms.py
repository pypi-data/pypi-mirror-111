import copy

from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import SUBSCRIPTION_INVEST_TYPE_SURVEY, TELECOM_CHOICES
from buildblock.apps.users import models
from buildblock.forms import BaseModelForm
from buildblock.helper import db_update
from buildblock.services.aws import AwsService
from buildblock.services.user import UserService


class SignupForm(BaseModelForm):
    agree_terms = forms.BooleanField(required=True)

    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "nationality",
            "phone_number",
        )

    def signup(self, request, user):
        db_update(user, dict(
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            nationality=self.cleaned_data.get('nationality'),
            phone_number=self.cleaned_data.get('phone_number'),
        ))
        return user


class AccountUpdateForm(BaseModelForm):

    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "nationality",
            "phone_number",
        )


class SignupOwnerForm(BaseModelForm):

    class Meta:
        model = models.ProfileOwner
        fields = (
            'address_1',
            'address_2',
            'city',
            'state',
            'zip_code'
        )


class SignupTenantForm(BaseModelForm):

    class Meta:
        model = models.ProfileTenant
        fields = ('emergency_contact', 'occupation', 'income', 'ssn', 'proof_of_income')

    def clean_ssn(self):
        ssn = self.cleaned_data['ssn']

        if not ssn.isdigit():
            raise ValidationError(_('Please enter only numbers'))

        if len(ssn) != 9:
            raise ValidationError(_('Please enter 9 numbers except the - marks.'))

        if UserService.same_ssn_tenant_exists(ssn):
            raise ValidationError(_('The SSN is already used.'))

        encrypted_ssn = AwsService.encrypt_personal_info(ssn)
        return encrypted_ssn

    def save(self, commit=True):
        profileTenant = super(SignupTenantForm, self).save(commit=False)
        profileTenant.ssn_last4_hashed = UserService.get_ssn_last4_hashed_from_encrypted_ssn(profileTenant.ssn)
        if commit:
            db_update(profileTenant)
        return profileTenant


class SignupConstructorForm(BaseModelForm):

    class Meta:
        model = models.ProfileConstructor
        fields = (
            'contact',
            'address_1',
            'address_2',
            'city',
            'state',
            'zip_code'
        )


class SignupAgentForm(BaseModelForm):

    class Meta:
        model = models.ProfileAgent
        fields = (
            'phone_number',
            'position',
        )


class SignupInvestorForm(BaseModelForm):

    class Meta:
        model = models.ProfileInvestor
        fields = (
            'account_bank',
            'account_number'
        )


class SignupManagerForm(BaseModelForm):

    class Meta:
        model = models.ProfileManager
        fields = (
            'phone_number',
            'position',
        )


class UpdateProfileForm(BaseModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs['instance'].user
        user_kwargs = copy.deepcopy(kwargs)
        user_kwargs['instance'] = user_kwargs['instance'].user
        self.account_form = AccountUpdateForm(*args, **user_kwargs)

        super(UpdateProfileForm, self).__init__(*args, **kwargs)

        self.fields.update(self.account_form.fields)
        self.initial.update(self.account_form.initial)

    def save(self, *args, **kwargs):
        # save both forms
        self.account_form.save(*args, **kwargs)
        return super(UpdateProfileForm, self).save(*args, **kwargs)


class UpdateOwnerForm(UpdateProfileForm):

    class Meta:
        model = models.ProfileOwner
        fields = (
            'address_1',
            'address_2',
            'city',
            'state',
            'zip_code'
        )


class UpdateTenantForm(UpdateProfileForm):

    class Meta:
        model = models.ProfileTenant
        fields = ('emergency_contact', 'occupation', 'income', 'proof_of_income')


class UpdateConstructorForm(UpdateProfileForm):

    class Meta:
        model = models.ProfileConstructor
        fields = (
            'contact',
            'address_1',
            'address_2',
            'city',
            'state',
            'zip_code'
        )


class UpdateAgentForm(UpdateProfileForm):

    class Meta:
        model = models.ProfileAgent
        fields = (
            'phone_number',
            'position',
        )


class UpdateInvestorForm(UpdateProfileForm):

    class Meta:
        model = models.ProfileInvestor
        fields = (
            'account_bank',
            'account_number'
        )


class UpdateManagerForm(UpdateProfileForm):

    class Meta:
        model = models.ProfileManager
        fields = (
            'phone_number',
            'position',
        )


class UpdateGroupForm(BaseModelForm):

    class Meta:
        model = Group
        fields = ('name',)


class UpdateGroupDetailForm(BaseModelForm):

    class Meta:
        model = models.GroupDetail
        fields = ('description',)

    def __init__(self, *args, **kwargs):
        self.group = kwargs['instance'].group
        group_kwargs = copy.deepcopy(kwargs)
        group_kwargs['instance'] = group_kwargs['instance'].group
        self.group_form = UpdateGroupForm(*args, **group_kwargs)

        super().__init__(*args, **kwargs)

        self.fields.update(self.group_form.fields)
        self.initial.update(self.group_form.initial)

    def save(self, *args, **kwargs):
        # save both forms
        self.group_form.save(*args, **kwargs)
        return super().save(*args, **kwargs)


class SubscriptionForm(BaseModelForm):

    email = forms.EmailField()
    name = forms.CharField(required=False)
    age = forms.IntegerField(required=False)
    occupation = forms.CharField(required=False)
    invest_survey = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=SUBSCRIPTION_INVEST_TYPE_SURVEY,
        required=False,
    )
    intention = forms.NullBooleanField(required=False)
    amount = forms.IntegerField(required=False)

    class Meta:
        model = models.Subscription
        fields = ("email", "name", "age", "occupation", "invest_survey", "intention", "amount", )


class PhoneForm(BaseModelForm):

    telecom = forms.ChoiceField(choices=TELECOM_CHOICES)

    class Meta:
        model = models.User
        fields = ("phone_number", "telecom",)


class AccountFindForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(AccountFindForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = pgettext_lazy("First Name", "이름")
        self.fields['last_name'].label = _("Last Name")
        self.fields['phone'].label = _("Phone")


class CouponRegisterForm(BaseModelForm):

    class Meta:
        model = models.CouponRegister
        fields = ("coupon_number",)
