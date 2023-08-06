from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    # https://github.com/pennersr/django-allauth/blob/5b9b85593e683da28897635e9179b41f7db95ee1/allauth/account/adapter.py#L433
    def send_confirmation_mail_for_invited_user(self, emailconfirmation, password):
        current_site = get_current_site(None)
        activate_url = self.get_email_confirmation_url(
            request=None,  # FIXME: local test 시에도 buildblock.io 을 사용함
            emailconfirmation=emailconfirmation
        )
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
            "temp_password": password
        }
        email_template = 'account/email/email_confirmation_signup_for_invited_user'
        self.send_mail(email_template,
                       emailconfirmation.email_address.email,
                       ctx)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
