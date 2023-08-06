import pytest
from django.conf import settings
from django.test import RequestFactory

from buildblock.apps.core.constants import COUNTRY_KOREA, COUNTRY_UNITED_STATES
from buildblock.tests.users.factories import InvitedUserFactory, ProfileTenantFactory, UserFactory


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


@pytest.fixture
def user_kr() -> settings.AUTH_USER_MODEL:
    return UserFactory(country=COUNTRY_KOREA)


@pytest.fixture
def user_us() -> settings.AUTH_USER_MODEL:
    return UserFactory(country=COUNTRY_UNITED_STATES)


@pytest.fixture
def invited_user() -> settings.AUTH_USER_MODEL:
    return InvitedUserFactory()


@pytest.fixture
def tenant_kr() -> ProfileTenantFactory:
    return ProfileTenantFactory(country=COUNTRY_KOREA)


@pytest.fixture
def tenant_us() -> ProfileTenantFactory:
    return ProfileTenantFactory(country=COUNTRY_UNITED_STATES)
