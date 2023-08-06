from django.utils.translation import ugettext_lazy as _


"""i18n
Note: No need to wrap non user-facing strings for translation!"""


# Base error class. We can use this to group all errors
class BaseError(Exception):
    pass


class NotEnoughEtherError(BaseError):
    def __init__(self, min_balance, balance):
        self.message = _("Not enough balance to make this transfer, please check the balance.")
        self.error_details = \
            "Not enough Ether to make this transfer - " + \
            f"Min. required balance: {min_balance} Balance: {balance}"


class NotEnoughTokenError(BaseError):
    def __init__(self, from_addr, contract_addr, amount, balance):
        self.message = _("Not enough balance to make this transfer, please check the balance.")
        self.error_details = \
            f"Not enough Tokens for {from_addr} to make this transfer in " + \
            f'contract {contract_addr} - Required balance: {amount} ' + \
            f'Actual balance: {balance}'


class InvalidParameterError(BaseError):
    def __init__(self):
        self.message = 'Invalid parameter'


class ServerError(BaseError):
    def __init__(self):
        self.message = _('Server error')


class CouponDoesNotExistError(BaseError):
    pass


class CouponAlreadyRegisteredError(BaseError):
    pass


class BlockscoreFieldDoesNotExistError(BaseError):
    def __init__(self, missing_field):
        self.message = _('Please enter the field.')


class PaypalInvalidResponseError(BaseError):
    def __init__(self):
        self.message = _('Request Failed. Please contact us.')


class PaypalTokenChargeError(BaseError):
    def __init__(self):
        self.message = _('Request Failed. Please contact us.')


class RequiredPostDataError(BaseError):
    pass
