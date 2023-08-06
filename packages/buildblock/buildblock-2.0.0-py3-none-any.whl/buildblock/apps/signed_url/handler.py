import hashlib
import hmac
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse

USER_EMAIL = "email"
URL_TO_REDIRECT = "next_url"
EXPIRATION_DATE_TIMESTAMP = "exp"
SIGNATURE = "sig"


class SignedUrlHandler:
    REQUIRED_PARAMETERS = (
        USER_EMAIL,
        URL_TO_REDIRECT,
        EXPIRATION_DATE_TIMESTAMP,
        SIGNATURE,
    )

    @classmethod
    def has_required_parameters(cls, query_parameters: Dict[str, str]) -> bool:
        return all([
            required_parameter in query_parameters
            for required_parameter in cls.REQUIRED_PARAMETERS
        ])

    @classmethod
    def is_expired(cls, expiration_date_timestamp: str) -> bool:
        return int(expiration_date_timestamp) < time.time()

    @classmethod
    def is_valid_signature(cls, query_parameters: Dict[str, str]) -> bool:
        signature = cls.create_hex_signature(
            user_email=query_parameters[USER_EMAIL],
            redirect_url=query_parameters[URL_TO_REDIRECT],
            expiration_date_timestamp=query_parameters[EXPIRATION_DATE_TIMESTAMP],
        )
        return signature == query_parameters[SIGNATURE]

    @classmethod
    def create_hex_signature(cls, *, user_email: str, redirect_url: str, expiration_date_timestamp: str) -> str:
        """Create signature using given params
        """
        string_to_sign = ''.join([user_email, redirect_url, expiration_date_timestamp])
        return hmac.new(
            settings.SIGNED_URL_SECRET_KEY.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    @classmethod
    def create_signed_url(cls, *, user_email: str, redirect_url: str, expiration_days: Optional[int] = 1) -> str:
        """Return Full signed-url to use it in email template

        Default expiration_days is 1 (= 24 hours)

        Return example. "https://buildblock.io/signed-url?param=value&.."
        """
        expiration_date = datetime.fromtimestamp(time.time(), timezone.utc) + timedelta(days=expiration_days)
        expiration_date_timestamp = str(int(expiration_date.timestamp()))
        signature = cls.create_hex_signature(
            user_email=user_email,
            redirect_url=redirect_url,
            expiration_date_timestamp=expiration_date_timestamp,
        )

        query_parameters = {
            USER_EMAIL: user_email,
            URL_TO_REDIRECT: redirect_url,
            EXPIRATION_DATE_TIMESTAMP: expiration_date_timestamp,
            SIGNATURE: signature,
        }
        query_string = urlencode(query_parameters)

        url_path = reverse('signed-url')  # format: /{path}/

        return f"{settings.PRODUCTION_HOST_NAME}{url_path}?{query_string}"
