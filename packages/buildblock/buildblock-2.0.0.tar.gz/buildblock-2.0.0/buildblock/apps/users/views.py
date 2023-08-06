import csv
import logging
import random
import re
import string
from datetime import date, datetime
from io import StringIO

from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import resolve, reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import (
    AGENT_ROLE,
    CONSTRUCTOR_ROLE,
    INVESTOR_ROLE,
    MANAGER_ROLE,
    OWNER_ROLE,
    TENANT_ROLE
)
from buildblock.apps.core.views import FormView, PasswordChangeView, SignupView, TemplateView, UpdateView
from buildblock.apps.users import forms
from buildblock.apps.users.mixin import AlreadySignedupCheckMixin
from buildblock.apps.users.models import CouponRegister, User
from buildblock.apps.view_control import is_valid_post_request
from buildblock.errors import CouponAlreadyRegisteredError, CouponDoesNotExistError
from buildblock.helper import db_update
from buildblock.services import EmailService, UserService

logger = logging.getLogger(__name__)

EMAIL_PATTERN = re.compile(r'^.+@.+\..+$')
VALID_CHARS = string.ascii_letters + string.digits

_ROLE_TO_SIGNUP_FORM_MAPPING = {
    OWNER_ROLE: forms.SignupOwnerForm,
    TENANT_ROLE: forms.SignupTenantForm,
    AGENT_ROLE: forms.SignupAgentForm,
    INVESTOR_ROLE: forms.SignupInvestorForm,
    MANAGER_ROLE: forms.SignupManagerForm,
    CONSTRUCTOR_ROLE: forms.SignupConstructorForm,
}

_ROLE_TO_UPDATE_FORM_MAPPING = {
    OWNER_ROLE: forms.UpdateOwnerForm,
    TENANT_ROLE: forms.UpdateTenantForm,
    AGENT_ROLE: forms.UpdateAgentForm,
    INVESTOR_ROLE: forms.UpdateInvestorForm,
    MANAGER_ROLE: forms.UpdateManagerForm,
    CONSTRUCTOR_ROLE: forms.UpdateConstructorForm,
}


def _redact(value):
    if not isinstance(value, str) or len(value) == 0:
        return None
    # If the value is an email, we redact it slightly differently
    # e.g., abcd1234@buildblock.io -> abcdXXXX@buildblock.io
    if EMAIL_PATTERN.match(value):
        username, domain = value.split('@')
        half_length = len(username) // 2
        return (username[:half_length], 'x'*(len(username) - half_length), domain)

    return value[:int(len(value)/2)] + 'x'*int(len(value)/2 + 1)


def _generate_unique_identifier():
    return ''.join(random.choices(VALID_CHARS, k=80))


def _format_date_of_birth(value):
    if isinstance(value, str) and re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}').match(value):
        year, month, day = value.split('-')
        return year[-2:] + month + day


def _get_user_age(date_of_birth):
    born = datetime.strptime(date_of_birth, "%Y-%m-%d")
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


# DEPRECATED: but leaving this as a similar approach might be used (e.g., when we need to approve applicants)
def _store_requests_in_db_and_file(request_data):
    csvfile = StringIO()
    csvwriter = csv.writer(csvfile)
    request_unique_identifier = _generate_unique_identifier()
    csvwriter.writerow([f'{request_unique_identifier}'])
    csvwriter.writerow(['Investor address', 'Interest pre-tax', 'Interest tax', 'Amount'])
    for idx, investor_address in enumerate(request_data['investor_address_list']):
        interest_before_tax = request_data['interest_before_tax_list'][idx]
        interest_tax = request_data['interest_tax_list'][idx]
        actual_amount = interest_before_tax - interest_tax
        csvwriter.writerow([
            str(investor_address),
            str(interest_before_tax),
            str(interest_tax),
            str(actual_amount),
        ])
    logger.info(
        f'Sent email for payment interest and created InterestPayment item - request_id: {request_unique_identifier}'
    )


# Submit Function
def submit_contact_us(request):
    if not is_valid_post_request(request):
        return redirect('users:info')

    name = request.POST.get("name")
    email = request.POST.get("email")
    content = request.POST.get("content")

    if not name or not email or not content:
        messages.warning(request, _('Please fill in the blanks.'))
        return redirect('home')

    EmailService.send_to_admin_contact_us(name, email, content)
    messages.success(request, _('Email has successfully been sent.'))
    return redirect('home')


def submit_subscription(request):
    if not is_valid_post_request(request):
        return redirect('home')

    form = forms.SubscriptionForm(request.POST)
    if form.is_valid():
        db_update(form)
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        EmailService.send_to_admin(name, email)
        messages.success(request, _('Your subscription has been applied.'))
    else:
        messages.warning(request, _('Request Failed. Please try again.'))
    return redirect('home')


@login_required
def submit_coupon(request):
    if not is_valid_post_request(request):
        return redirect('users:info')

    form = forms.CouponRegisterForm(request.POST)
    if form.is_valid():
        coupon_register = form.save(commit=False)
        coupon_number = form.cleaned_data.get("coupon_number")
        kv = dict(user=request.user.username, coupon_number=coupon_number)
        try:
            coupon = UserService.check_coupon_validate(coupon_number)
        except CouponDoesNotExistError:
            messages.warning(request, _('The coupon does not exist.'))
            kv.update(reason='Not existent')
            logger.info(f'Invalid coupon - {kv}')
            return redirect('users:info')
        except CouponAlreadyRegisteredError:
            messages.warning(request, _('The coupon is already registered.'))
            kv.update(reason='Already registered')
            logger.info(f'Invalid coupon - {kv}')
            return redirect('users:info')

        if CouponRegister.objects.filter(coupon=coupon, user=request.user).exists():
            messages.warning(request, _('The coupon is already registered.'))
            kv.update(reason='Already registered same coupon')
            logger.info(f'Invalid coupon - {kv}')
            return redirect('users:info')

        db_update(coupon_register, dict(
            coupon=coupon,
            user=request.user
        ))
        logger.info(f'Successfully registered coupon: {kv}')
        messages.success(request, _('The coupon has been registered.'))
        return redirect('users:info')
    else:
        kv = dict(user=request.user.username, reason='invalid form')
        logger.info(f'Invalid coupon entered by user {kv}')
        messages.warning(request, _('Please enter the coupon numbers.'))
        return redirect('users:info')


@login_required
def submit_phone(request):
    if not is_valid_post_request(request):
        return redirect('users:info')

    phone = request.POST.get("phone")
    telecom = request.POST.get("telecom")
    kv = dict(user=request.user.username, phone=phone, telecom=telecom)

    if not phone or not telecom:
        kv.update(reason='Missing param')
        logger.info(f'Failed in changing phone number: {kv}')
        messages.warning(request, _('Please enter the numbers'))
        return redirect('users:info')

    if User.objects.filter(phone=phone).exists():
        kv.update(reason='Already existing phone number')
        logger.info(f'Failed in changing phone number: {kv}')
        messages.warning(request, _('The phone number is already registered.'))
        return redirect('users:info')

    phone_form = forms.PhoneForm(request.POST)
    if phone_form.is_valid():
        db_update(request.user, dict(
            telecom=phone_form.cleaned_data['telecom'],
            phone=phone_form.cleaned_data['phone'],
        ))
        logger.info(f'Successfully changed phone number: {kv}')
        messages.success(request, _('The phone number has changed.'))
    else:
        kv.update(reason='Invalid phone form')
        logger.info(f'Failed in changing phone number: {kv}')
        messages.warning(request, _('Request Failed. Please try again.'))

    return redirect('users:info')


@login_required
def submit_marketing(request):
    if not is_valid_post_request(request):
        return redirect('users:info')

    db_update(request.user, dict(
        agree_marketing_email=bool(request.POST.get("agree_marketing_email")),
        agree_marketing_phone=bool(request.POST.get("agree_marketing_phone")),
    ))

    messages.success(request, _('Marketing messaging has been unsubscribed.'))
    return redirect('users:info')


@login_required
def submit_exit(request):
    if not is_valid_post_request(request):
        return redirect('users:info')

    if not request.POST.get("agree"):
        messages.warning(request, _('Please accept the terms and conditions.'))
        return redirect('users:exit')

    # 탈퇴 조건 검사
    # 토큰이 남아있는가
    user = request.user

    # 탈퇴 처리
    if not UserService.make_exit_request(user):
        messages.warning(request, _('Already applied.'))
        return redirect('users:exit')

    EmailService.send_to_admin_exit_request(user.name, user.email)
    logout(request)
    messages.success(request, _('Your account has been deleted.'))
    return redirect('home')


# Role Change Function
@login_required
def active_role_change(request, user_role):
    app_name = resolve(request.path).app_name
    if user_role in request.user.user_role:
        request.session['active_role'] = user_role
        return redirect(reverse(app_name + ":home"))
    messages.warning(request, _('Please submit your application to use the service.'))
    return redirect(app_name + ":signup-role", user_role=user_role)


# Account View
class SignupView(SignupView):
    template_name = 'account/signup.html'
    form_class = forms.SignupForm


class AccountUpdateView(UpdateView):
    template_name = 'account/account_update.html'
    form_class = forms.AccountUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        db_update(self.request.user, dict(
            first_name=form.cleaned_data.get('first_name'),
            last_name=form.cleaned_data.get('last_name'),
            nationality=form.cleaned_data.get('nationality'),
            phone_number=form.cleaned_data.get('phone_number'),
        ))
        return super().form_valid(form)

    def get_success_url(self):
        # TODO: My Page 작업 후 마이페이지 링크로 이동
        return reverse("home")


class AccountFindView(FormView):
    template_name = "account/account_find.html"
    form_class = forms.AccountFindForm

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            phone = form.cleaned_data.get("phone")
            try:
                user = get_user_model().objects.get(
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone
                )
                (username_half, username_x, domain) = _redact(user.email)
                return render(request, 'account/account_find_result.html', {
                    'username_half': username_half,
                    'username_x': username_x,
                    'domain': domain
                })
            except get_user_model().DoesNotExist:
                messages.warning(request, _("No users match the information."))
        else:
            messages.warning(request, _("Please enter the information correctly."))
        return render(request, 'account/account_find.html', {'form': form})


class WelcomeInvitedUserView(PasswordChangeView):
    template_name = "account/welcome_invited_user.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        db_update(self.request.user, dict(
            need_to_change_password=False
        ))
        return response


class ServiceRoleSignupSelectView(TemplateView):
    template_name = "account/signup_user_role.html"


class ServiceRoleSignupView(AlreadySignedupCheckMixin, FormView):
    template_name = "account/signup_user_role.html"

    def dispatch(self, request, *args, **kwargs):
        self.application_role = self.kwargs.get('application_role')
        if self.application_role not in self.service_role_set:
            messages.warning(self.request, _('Invalid Access'))
            return redirect(reverse(self.service_app_name + ":signup-choice"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        context = super().get_context_data(**kwargs)
        context['application_role'] = self.application_role
        context['service_role_set'] = self.service_role_set
        context['service_app_name'] = self.service_app_name
        return context

    def get_form_class(self):
        return _ROLE_TO_SIGNUP_FORM_MAPPING.get(self.application_role)

    def form_valid(self, form):
        profile_form = form.save(commit=False)
        db_update(profile_form, dict(user_id=self.request.user.id))
        # User Role 추가
        if self.application_role not in self.request.user.user_role:
            user = self.request.user
            user.user_role.append(self.application_role)
            db_update(user)
        # Active Role change
        self.request.session['active_role'] = self.application_role
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(self.service_app_name + ":home")


# Update User Base Information
class ServiceRoleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "account/profile_update.html"
    model = None
    service_role_set = set()
    service_app_name = None

    def dispatch(self, request, *args, **kwargs):
        self.active_role = self.request.session.get('active_role')
        if self.active_role not in self.service_role_set:
            messages.warning(self.request, _('Invalid Access'))
            return redirect(reverse(self.service_app_name + ":profile"))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return UserService.get_profile_by_role(
            user=self.request.user,
            role=self.active_role,
        )

    def get_form_class(self):
        return _ROLE_TO_UPDATE_FORM_MAPPING.get(self.active_role)

    def get_success_url(self):
        return reverse(self.service_app_name + ":profile")


class ServiceRoleSelectView(TemplateView):
    template_name = "account/select_user_role.html"
