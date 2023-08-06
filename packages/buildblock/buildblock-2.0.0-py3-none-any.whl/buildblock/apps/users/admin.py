from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.users.models import (
    Coupon,
    CouponRegister,
    ExitRequest,
    GroupDetail,
    ProfileAgent,
    ProfileConstructor,
    ProfileManager,
    ProfileOwner,
    ProfileTenant,
    Subscription,
    User
)
from buildblock.helper import db_update
from buildblock.services.user import UserService


@admin.register(ProfileTenant)
class MyProfileTenantAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation", "credit_score", "auto_payment_account_id")


@admin.register(ProfileOwner)
class MyProfileOwnerAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(ProfileAgent)
class MyProfileAgentAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "position")


@admin.register(ProfileManager)
class MyProfileManagerAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "position")


@admin.register(ProfileConstructor)
class MyProfileConstructorAdmin(admin.ModelAdmin):
    list_display = ("user",)


class UserCreationForInvitedUser(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(label="Email", required=True,)

    def save(self, *args, **kwargs):
        user = super().save()
        db_update(user, dict(
            is_invited=True,
            need_to_change_password=True,
        ))

        UserService.create_email_address(user, user.email, primary=True, verified=False)

        password = self.cleaned_data.get('password1')
        UserService.send_verification_email_for_invited_user(user.email, password)

        return user


@admin.register(GroupDetail)
class MyGroupAdmin(admin.ModelAdmin):
    list_display = ("group", "category", "description")
    search_fields = ["group", "category", "description"]


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ("email", "name", "date_joined")
    search_fields = ["email", "first_name", "last_name"]

    # Change information of existing user
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'user_role')
        }),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email', 'nationality',
                'phone_number', 'date_of_birth',
                'is_invited', 'need_to_change_password'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Add new user
    add_form = UserCreationForInvitedUser
    add_fieldsets = (
        (None, {
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
            )
        }),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'nationality',
                'phone_number',
            )
        })
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at",)
    search_fields = ["first_name", "last_name", "email"]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("title", "description",)
    search_fields = ["title"]


@admin.register(CouponRegister)
class CouponRegisterAdmin(admin.ModelAdmin):
    list_display = ("user", "coupon", "coupon_number", "created_at",)
    search_fields = ["first_name", "last_name"]


@admin.register(ExitRequest)
class ExitRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "approval_date", "created_at",)
