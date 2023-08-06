from collections import defaultdict

from django.conf import settings

from buildblock.apps.core.constants import AGENT_ROLE, OWNER_ROLE, TENANT_ROLE
from buildblock.apps.management.models import Maintenance
from buildblock.apps.management.views.base import ManagementPaymentView
from buildblock.apps.users.mixin import ViewPermissionCheckMixin
from buildblock.apps.users.models import User
from buildblock.services.stripe import StripeService

_MAX_MAINTENANCE_LIST_SIZE = 10


class ManagementProfileView(ViewPermissionCheckMixin, ManagementPaymentView):
    permitted_role_list = [AGENT_ROLE, OWNER_ROLE, TENANT_ROLE]
    template_name = "management/profile.html"
    page_title = "Profile"

    def _generate_stripe_dashboard_url(self, user_account):
        if self.request.session['active_role'] != OWNER_ROLE:
            return None
        try:
            dashboard_url = StripeService.create_dashboard_link(
                account_id=user_account
            )['url']
            self.logger.info(f'dashboard url for the user "{self.request.user}" has been generated: {dashboard_url}')
        except Exception as err:
            self.logger.error(f'Error has occurred while creating dashboard link: {err}')
            dashboard_url = None
        return dashboard_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session['active_role'] == OWNER_ROLE:
            # TODO: Add CSRF validation at /token endpoint
            context['csrf_token'] = 'token'
            context['stripe_connect_client_id'] = settings.STRIPE_CONNECT_CLIENT_ID
            stripe_account = self.request.user.profile_owner.stripe_account
            if stripe_account:
                context['stripe_dashboard_url'] = self._generate_stripe_dashboard_url(stripe_account)
            products = context['products']
            products_overview = defaultdict(lambda: 0)
            for product in products:
                products_overview['num_people_under_lease'] += product.num_people_under_lease
                products_overview['max_num_people'] += product.max_num_people
                products_overview['rent_under_lease'] += product.rent_under_lease

            context.update(products_overview=dict(products_overview))

        if self.request.session['active_role'] == TENANT_ROLE:
            context['maintenances'] = Maintenance.objects.filter(
                tenant=self.request.user
            ).all().order_by('-created_at')[:_MAX_MAINTENANCE_LIST_SIZE]

        if self.request.session['active_role'] == AGENT_ROLE:
            # TODO 소속 agency는 하나만 노출할 예정, validation 작업 추후 진행
            context['agency'] = agency = self.request.user.groups.last()
            context['members'] = User.objects.filter(groups=agency)

        return context
