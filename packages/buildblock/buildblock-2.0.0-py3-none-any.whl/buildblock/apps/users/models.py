import uuid

from allauth.account import signals
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailConfirmationHMAC
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords

from buildblock.apps.core.constants import (
    COUNTRY_CHOICES,
    GROUP_CATEGORIES,
    LAST_FIRST_NAME_LANGUAGES,
    US_STATE_CHOICES,
    USER_ROLES
)
from buildblock.apps.core.models import PHONE_NUMBER_REGEX_VALIDATOR, TimeStampedModel, ZipcodeField, get_full_address
from buildblock.utils import detect_language


def tenant_file_path(instance, filename):
    return f"tenant/{instance.user.id}/{filename}"


class GroupDetail(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="detail")
    category = models.CharField(_("Category"), choices=GROUP_CATEGORIES, max_length=50)
    description = models.TextField(_("Description"), blank=True)


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user_role = ArrayField(models.CharField(max_length=200, choices=USER_ROLES), blank=True, default=list)
    first_name = models.CharField(_("First Name"), max_length=30)
    last_name = models.CharField(_("Last Name"), max_length=30)
    date_of_birth = models.CharField(_("Date of Birth"), max_length=1500, blank=True)
    nationality = models.CharField(_("Nationality"), choices=COUNTRY_CHOICES, max_length=15)
    # TODO: 휴대전화번호 형태 validator 다시 설정. "-"표시 제한
    phone_number = models.CharField(
        _("Phone Number"),
        max_length=15,
        validators=[PHONE_NUMBER_REGEX_VALIDATOR],
    )
    is_invited = models.BooleanField(_("초대 회원 여부"), default=False)
    need_to_change_password = models.BooleanField(_("비밀번호 재설정 필요 여부"), default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("users:account")

    @property
    def name(self):
        first_name_lang = detect_language(self.first_name)
        last_name_lang = detect_language(self.last_name)

        requires_last_name_before_first_name = (
            first_name_lang == last_name_lang and
            first_name_lang in LAST_FIRST_NAME_LANGUAGES
        )
        if requires_last_name_before_first_name:
            return self.last_name + self.first_name

        return self.first_name + " " + self.last_name

    @property
    def credit_score(self):
        # We only store the credit score for the tenant. Therefore retrieve it from their profile
        return self.profile_tenant.credit_score if hasattr(self, 'profile_tenant') else 'N/A'

    @property
    def is_first_visited_invited_user(self):
        return self.is_invited and self.need_to_change_password


class ProfileOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_owner")
    stripe_account = models.CharField(_("Stripe Account"), max_length=32, null=True, blank=True)

    # for Post (optional)
    address_1 = models.CharField(_("Address 1"), max_length=128, null=True, blank=True)
    address_2 = models.CharField(_("Address 2"), max_length=128, null=True, blank=True)
    city = models.CharField(_("City"), max_length=64, null=True, blank=True)
    state = models.CharField(_("State"), choices=US_STATE_CHOICES, max_length=16, null=True, blank=True)
    zip_code = ZipcodeField(null=True, blank=True)

    def __str__(self):
        return 'Owner -{}'.format(self.user.name)

    @property
    def full_address(self):
        return get_full_address(self)


class ProfileTenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_tenant")
    stripe_customer_id = models.CharField(_("Stripe Customer Id"), max_length=32, null=True, blank=True)
    emergency_contact = models.CharField(_("Emergency Contact"), max_length=300)

    # Proof of Payment
    occupation = models.CharField(_("Occupation"), max_length=300, default=None)
    income = models.PositiveIntegerField(_("Income"))
    ssn = models.CharField(_("SSN"), max_length=1500)
    ssn_last4_hashed = models.CharField(_("SSN last 4 hashed"), max_length=100)
    credit_score = models.CharField(_("Credit Score"), max_length=10, blank=True, null=True)
    proof_of_income = models.FileField(_("Proof of Income (option)"), upload_to=tenant_file_path, blank=True)
    auto_payment_account_id = models.CharField(_("Auto Payment Bank Account Id"), max_length=30, blank=True, null=True)

    def __str__(self):
        return 'Tenant -{}'.format(self.user.name)

    def clean(self):
        if self.proof_of_income and self.proof_of_income.size > 5242880:
            raise ValidationError({
                'proof_of_income': _("The maximum file size that can be uploaded is 5MB")
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ProfileConstructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_constructor")
    # Office Information
    contact = models.CharField(_("Contact"), max_length=300)
    address_1 = models.CharField(_("Address 1"), max_length=128)
    address_2 = models.CharField(_("Address 2"), max_length=128, blank=True)
    city = models.CharField(_("City"), max_length=64)
    state = models.CharField(_("State"), choices=US_STATE_CHOICES, max_length=16)
    zip_code = ZipcodeField()

    def __str__(self):
        return 'Constructor -{}'.format(self.user.name)

    @property
    def full_address(self):
        return get_full_address(self)


class ProfileAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_agent")
    phone_number = models.CharField(
        _("Phone Number"),
        max_length=15,
        validators=[PHONE_NUMBER_REGEX_VALIDATOR],
        blank=True,
        null=True,
    )
    position = models.CharField(
        _("Position"),
        max_length=100,
        blank=True,
        null=True,
    )

    def __str__(self):
        return 'Agent -{}'.format(self.user.name)


class ProfileManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_manager")
    phone_number = models.CharField(
        _("Phone Number"),
        max_length=15,
        validators=[PHONE_NUMBER_REGEX_VALIDATOR],
        blank=True,
        null=True,
    )
    position = models.CharField(
        _("Position"),
        max_length=100,
        blank=True,
        null=True,
    )

    def __str__(self):
        return 'Manager -{}'.format(self.user.name)


class ProfileInvestor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_investor")
    # Investment Profit Account
    account_bank = models.CharField(_("은행"), max_length=128, blank=True)
    account_number = models.CharField(_("계좌번호"), max_length=128, blank=True)


class Subscription(TimeStampedModel):

    email = models.CharField(_("Email"), max_length=100)
    name = models.CharField(_("Name"), max_length=30, blank=True, null=True, default=None)
    age = models.CharField(_("Age"), max_length=30, blank=True, null=True, default=None)
    occupation = models.CharField(_("Occupation"), max_length=300, blank=True, null=True, default=None)
    invest_survey = models.CharField(_("Familiar with Investment"), max_length=255, blank=True, null=True, default=None)
    intention = models.BooleanField(_("Would you invest"), blank=True, null=True, default=None,)
    amount = models.FloatField(_("If yes, how much?"), blank=True, null=True, default=None)

    def __str__(self):
        return self.email


class Coupon(TimeStampedModel):

    title = models.CharField(max_length=100)
    coupon_number_range = models.CharField(max_length=100, blank=True, null=True)
    coupon_number_all = models.TextField(blank=True, null=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class CouponRegister(TimeStampedModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="coupons")
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="registered")
    coupon_number = models.CharField(max_length=100)

    def __str__(self):
        return self.coupon_number


class ExitRequest(TimeStampedModel):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    approval_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email


# https://github.com/pennersr/django-allauth/blob/5b9b85593e683da28897635e9179b41f7db95ee1/allauth/account/models.py#L126
class CustromEmailConfirmationHMAC(EmailConfirmationHMAC):

    def send(self, password):
        get_adapter().send_confirmation_mail_for_invited_user(emailconfirmation=self, password=password)
        signals.email_confirmation_sent.send(sender=self.__class__,
                                             request=None,
                                             confirmation=self,
                                             signup=True)
