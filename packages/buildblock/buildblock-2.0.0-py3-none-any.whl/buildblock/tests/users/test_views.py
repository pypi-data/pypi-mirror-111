import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from buildblock.tests.users.factories import UserFactory

pytestmark = pytest.mark.django_db

TMP_PASSWORD = 'mypassword12@'


class TestUserSignupView:
    def test_sign_up(self, client):
        user = UserFactory.build()

        url = reverse("account_signup")

        response = client.post(url, {
                "email": user.email,
                "password1": user._password,
                "password2": user._password,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "nationality": user.nationality,
                "phone_number": user.phone_number,
                "agree_terms": True,
            },
        )

        assert response.status_code == 302
        assert response.url.endswith('accounts/confirm-email/')
        assert get_user_model().objects.count() == 1

    def test_disallow_same_email(self, client, user_kr):
        url = reverse("account_signup")

        response = client.post(url, {
                "email": user_kr.email,
                "password1": user_kr.password,
                "password2": user_kr.password,
                "first_name": user_kr.first_name,
                "last_name": user_kr.last_name,
                "nationality": user_kr.nationality,
                "phone_number": user_kr.phone_number,
                "agree_terms": True,
            },
        )

        # Already signed up
        assert response.status_code == 200
        assert 'account/signup.html' in response.template_name
        assert get_user_model().objects.count() == 1


class TestUserLoginView:

    def test_login(self, client, user_kr):
        user_kr.set_password(TMP_PASSWORD)
        user_kr.save()

        url = reverse("account_login")

        response = client.post(url, {
                "login": user_kr.email,
                "password": TMP_PASSWORD,
            },
            follow=True
        )

        assert 'account/verification_sent.html' in response.template_name

        WRONG_PASSWORD = 'wrong123123'
        response = client.post(url, {
                "login": user_kr.email,
                "password": WRONG_PASSWORD,
            },
            follow=True
        )

        assert 'account/login_fluid.html' in response.template_name

    def test_tester_login(self, client):
        tester_email = '{}0001@{}'.format(settings.TESTER_EMAIL_PREFIX, settings.TESTER_EMAIL_DOMAIN)
        tester = UserFactory(email=tester_email)

        tester.set_password(settings.TESTER_PASSWORD)
        tester.save()

        url = reverse("account_login")

        response = client.post(url, {
                "login": tester.email,
                "password": 'a',  # Any String
            },
            follow=True
        )

        assert 'account/verification_sent.html' in response.template_name


# TODO
class TestTenantSignupView:
    pass


class TestInvitedUser:

    def test_redirect_to_change_password_on_first_login(self, client, invited_user):
        invited_user.set_password(TMP_PASSWORD)
        invited_user.save()

        assert invited_user.is_invited is True
        assert invited_user.need_to_change_password is True

        url = reverse("account_login")

        response = client.post(url, {
                "login": invited_user.email,
                "password": TMP_PASSWORD,
            },
            follow=True
        )

        assert 'account/welcome_invited_user.html' in response.template_name
