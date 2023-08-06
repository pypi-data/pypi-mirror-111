from buildblock.apps.investment.views.base import InvestmentAccountMixin
from buildblock.apps.users.views import (
    ServiceRoleSelectView,
    ServiceRoleSignupSelectView,
    ServiceRoleSignupView,
    ServiceRoleUpdateView
)


# Signup Role
class InvestmentRoleSignupView(InvestmentAccountMixin, ServiceRoleSignupView):
    pass


# Update User Base Information
class InvestmentRoleUpdateView(InvestmentAccountMixin, ServiceRoleUpdateView):
    pass


# Signup Service Select
class InvestmentRoleSignupSelectView(InvestmentAccountMixin, ServiceRoleSignupSelectView):
    pass


# Select Role
class InvestmentRoleSelectView(InvestmentAccountMixin, ServiceRoleSelectView):
    pass
