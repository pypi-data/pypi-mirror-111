import pytest

from buildblock.apps.signed_url.handler import (
    EXPIRATION_DATE_TIMESTAMP,
    SIGNATURE,
    URL_TO_REDIRECT,
    USER_EMAIL,
    SignedUrlHandler
)

pytestmark = pytest.mark.django_db


class TestSignedUrlHandler:
    def test_parameters(self):
        assert SignedUrlHandler.has_required_parameters({
            EXPIRATION_DATE_TIMESTAMP: '',
            SIGNATURE: '',
            URL_TO_REDIRECT: '',
            USER_EMAIL: '',
        }) is True

    def test_is_expired(self):
        assert SignedUrlHandler.is_expired('1598167097') is True

    def test_create_signature(self):
        signature = SignedUrlHandler.create_hex_signature(
            user_email='test@test.test',
            redirect_url='/',
            expiration_date_timestamp='1598167097',
        )
        assert len(signature) == 64
