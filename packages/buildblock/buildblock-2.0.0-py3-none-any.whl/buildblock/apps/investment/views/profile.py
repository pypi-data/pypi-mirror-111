from buildblock.apps.core.constants import INVESTOR_ROLE, MANAGER_ROLE
from buildblock.apps.core.views import TemplateView
from buildblock.apps.investment.views.base import InvestmentServiceMixin
from buildblock.apps.users.mixin import ViewPermissionCheckMixin


class InvestmentProfileView(InvestmentServiceMixin, ViewPermissionCheckMixin, TemplateView):
    permitted_role_list = [INVESTOR_ROLE, MANAGER_ROLE]
    template_name = "investment/profile.html"
