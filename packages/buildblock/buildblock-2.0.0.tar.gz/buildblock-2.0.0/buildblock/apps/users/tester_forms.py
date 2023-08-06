"""
Circular Impeor 문제로 파일을 분리
https://stackoverflow.com/q/20784848
"""

from allauth.account.forms import LoginForm
from django.conf import settings
from django.contrib.auth import get_user_model


def _is_tester_email(email):
    return email.startswith(settings.TESTER_EMAIL_PREFIX) and email.endswith(settings.TESTER_EMAIL_DOMAIN)


class LoginFormWithTester(LoginForm):

    def clean_password(self):
        email = self.cleaned_data.get('login', '')

        user = get_user_model().objects.filter(email=email)
        if user.exists() and _is_tester_email(email):
            return settings.TESTER_PASSWORD

        # Normal User
        return self.cleaned_data['password']
