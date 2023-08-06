import logging

from django.conf import settings
from paypalcheckoutsdk.core import LiveEnvironment, PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest

from buildblock.decorators import memoized_classproperty
from buildblock.errors import PaypalInvalidResponseError
from buildblock.services.email import EmailService
from buildblock.settings import is_dev_environment

logger = logging.getLogger(__name__)


class PaypalService:

    @memoized_classproperty
    def _client(cls):
        environment = LiveEnvironment if not is_dev_environment() else SandboxEnvironment
        return PayPalHttpClient(
            environment(
                client_id=settings.PAYPAL_CLIENT_ID,
                client_secret=settings.PAYPAL_CLIENT_SECRET
            )
        )

    @classmethod
    def _is_primitive(cls, data):
        return isinstance(data, str) or isinstance(data, int)

    @classmethod
    def _object_to_json(cls, input_object):
        result = {}
        itr = input_object.__dict__.items()

        for key, value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = cls._list_to_json(value) if isinstance(value, list) else \
                cls._object_to_json(value) if not cls._is_primitive(value) else \
                value
        return result

    @classmethod
    def _list_to_json(cls, input_list):
        result = []
        if isinstance(input_list, list):
            for item in input_list:
                result.append(cls._object_to_json(item) if not cls._is_primitive(item) else
                              cls._list_to_json(item) if isinstance(item, list) else item)
        return result

    @classmethod
    def _response_to_json(cls, response):
        return cls._object_to_json(response)

    @classmethod
    def get_order(cls, order_id):
        return cls._client.execute(OrdersGetRequest(order_id))

    @classmethod
    def paypal_charge(cls, orderId, user):
        """
        결제 확인부터 코인 충전까지
        """
        kv = {
            'user': user.email,
            'orderId': orderId,
        }
        logger.info(f'Begin request for charge usd with paypal: {kv}')

        response = cls.get_order(orderId)
        if response.status_code != 200 or response.result.status != "COMPLETED":
            EmailService.send_paypal_error_alert_to_admin(user.email, orderId)
            kv.update(response=response)
            logger.error(f'Invalid Paypal response: {kv}', exc_info=True)
            raise PaypalInvalidResponseError
