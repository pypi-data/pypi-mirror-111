from collections import defaultdict

from buildblock.apps.core.constants import ACTIVE, OWNER_ROLE, PENDING
from buildblock.apps.management.models import Lease
from buildblock.apps.management.views.base import ManagementTemplateView
from buildblock.apps.users.mixin import ViewPermissionCheckMixin
from buildblock.services.stripe import StripeService
from buildblock.utils import safe_money_read_from_db


class ManagementOverviewView(ViewPermissionCheckMixin, ManagementTemplateView):
    permitted_role_list = [OWNER_ROLE]
    template_name = "management/overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']

        # Products Overview
        products_overview = defaultdict(lambda: 0)
        for product in products:
            products_overview['num_people_under_lease'] += product.num_people_under_lease
            products_overview['max_num_people'] += product.max_num_people
            products_overview['rent_under_lease'] += product.rent_under_lease
            products_overview['deposit_under_lease'] += product.deposit_under_lease
        context.update(products_overview=dict(products_overview))

        # Tenant List
        leases = Lease.objects.filter(
            owner=self.request.user,
            status__in=[PENDING, ACTIVE]
        ).order_by("-created_at").all()
        context.update(leases=[self._make_lease_context(lease) for lease in leases])

        # Stripe Account Information
        stripe_account_id = self.request.user.profile_owner.stripe_account
        if stripe_account_id:
            # Payout Schedule (daily or manual)
            stripe_account_data = StripeService.get_account(
                stripe_account=stripe_account_id
            )

            # Balance
            stripe_balance = StripeService.get_account_balance(
                stripe_account=stripe_account_id
            )
            for key, value in stripe_balance.items():
                stripe_balance[key] = safe_money_read_from_db(value)
            context.update(
                stripe_account_data=stripe_account_data,
                stripe_balance=stripe_balance
            )

        return context
