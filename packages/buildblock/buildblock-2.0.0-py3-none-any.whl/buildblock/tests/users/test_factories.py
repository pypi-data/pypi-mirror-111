import pytest
from django.conf import settings

from buildblock.apps.core.constants import COUNTRY_KOREA, COUNTRY_UNITED_STATES, TENANT_ROLE
from buildblock.tests.users.factories import ProfileTenantFactory

pytestmark = pytest.mark.django_db


def test_user_kr(user_kr: settings.AUTH_USER_MODEL):
    assert user_kr.nationality == COUNTRY_KOREA
    assert user_kr.user_role == []


def test_user_us(user_us: settings.AUTH_USER_MODEL):
    assert user_us.nationality == COUNTRY_UNITED_STATES
    assert user_us.user_role == []


def test_tenant_kr(tenant_kr: ProfileTenantFactory):
    assert tenant_kr.user.nationality == COUNTRY_KOREA
    assert tenant_kr.user.user_role == [TENANT_ROLE]


def test_tenant_us(tenant_us: ProfileTenantFactory):
    assert tenant_us.user.nationality == COUNTRY_UNITED_STATES
    assert tenant_us.user.user_role == [TENANT_ROLE]
