from allauth.account.models import EmailAddress
from django.contrib.auth.models import Group

from buildblock.apps.core.constants import AGENT_ROLE, CONSTRUCTOR_ROLE, OWNER_ROLE, TENANT_ROLE
from buildblock.apps.users.models import (
    Coupon,
    CouponRegister,
    CustromEmailConfirmationHMAC,
    ExitRequest,
    ProfileTenant,
    User
)
from buildblock.errors import CouponAlreadyRegisteredError, CouponDoesNotExistError
from buildblock.helper import db_update
from buildblock.services.aws import AwsService
from buildblock.utils import hash_sha256


class UserService:
    """High level interface for dealing with the Users database."""

    @classmethod
    def check_validation(cls, **kwargs):
        errors = []

        unique_user_list = ['username', 'email']
        unique_user_data = {key: kwargs.get(key) for key in unique_user_list}

        for key, value in unique_user_data.items():
            if User.objects.filter(**{key: value}).exists():
                errors.append({
                    "field": key,
                    "reason": "AlreadyExist"
                })

        return errors

    @classmethod
    def create_user(cls, username, name, password, email,
                    country, telecom, phone, ssn, address,
                    is_staff=False, is_active=True):
        user = User.objects.create_user(
            username=username,
            name=name,
            password=password,
            email=email,
            country=country,
            telecom=telecom,
            phone=phone,
            ssn=ssn,
            address=address,
            is_staff=is_staff,
            is_active=is_active,
        )
        return user

    @classmethod
    def add_user(cls, user, **kwargs):
        user_model_field_list = [
            'first_name',
            'last_name',
            'residence',
            'nationality',
            'telecom',
            'phone',
            'agree_marketing_email',
            'agree_marketing_phone',
        ]
        for attr in user_model_field_list:
            setattr(user, attr, kwargs.get(attr))
        db_update(user)

    @classmethod
    def get_user(cls, id):
        return User.objects.get(id=id)

    @staticmethod
    def get_groups_by_category(category):
        return Group.objects.filter(detail__category=category)

    @classmethod
    def check_coupon_validate(cls, coupon_number):
        for coupon in Coupon.objects.all():
            if not coupon.coupon_number_all:
                continue
            coupon_number_list = coupon.coupon_number_all.split(",")
            if coupon_number in coupon_number_list:
                if CouponRegister.objects.filter(coupon_number=coupon_number).exists():
                    raise CouponAlreadyRegisteredError
                return coupon

        raise CouponDoesNotExistError

    @classmethod
    def make_exit_request(cls, user):
        if ExitRequest.objects.filter(user=user).exists():
            return False

        ExitRequest.objects.create(user=user, name=user.name, email=user.email)
        db_update(user, dict(is_active=False))
        return True

    @classmethod
    def same_ssn_tenant_exists(cls, ssn):
        ssn_last4_hashed = hash_sha256(ssn[-4:])
        tenants = ProfileTenant.objects.filter(ssn_last4_hashed=ssn_last4_hashed)
        for tenant in tenants:
            if ssn == AwsService.decrypt_personal_info(tenant.ssn):
                return True
        return False

    @classmethod
    def get_ssn_last4_hashed_from_encrypted_ssn(cls, encrypted_ssn):
        ssn = AwsService.decrypt_personal_info(encrypted_ssn)
        ssn_last4_hashed = hash_sha256(ssn[-4:])
        return ssn_last4_hashed

    @classmethod
    def get_profile_by_role(cls, user, role):
        if role == TENANT_ROLE:
            return user.profile_tenant
        elif role == OWNER_ROLE:
            return user.profile_owner
        elif role == AGENT_ROLE:
            return user.profile_agent
        elif role == CONSTRUCTOR_ROLE:
            return user.profile_constructor
        else:
            return None

    @classmethod
    def create_email_address(cls, user, email, primary=False, verified=False):
        email_address = EmailAddress.objects.add_email(None, user, email)
        db_update(email_address, dict(
            primary=primary,
            verified=verified,
        ))
        return email_address

    # https://github.com/pennersr/django-allauth/blob/5b9b85593e683da28897635e9179b41f7db95ee1/allauth/account/models.py#L53
    @classmethod
    def send_verification_email_for_invited_user(cls, email, password):
        email_address = EmailAddress.objects.get(email=email)

        confirmation = CustromEmailConfirmationHMAC(email_address)
        confirmation.send(password)
