from buildblock.apps.core.constants import INVESTMENT_APP_NAME, INVESTMENT_ROLE_SET
from buildblock.apps.investment.contexts import InvestmentContext
from buildblock.apps.users.mixin import ServiceSignupCheckMixin
from buildblock.mixins import Loggable


class InvestmentAccountMixin(Loggable):
    service_role_set = INVESTMENT_ROLE_SET
    service_app_name = INVESTMENT_APP_NAME


class InvestmentServiceMixin(InvestmentAccountMixin, ServiceSignupCheckMixin, InvestmentContext):
    pass
