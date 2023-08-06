from buildblock.apps.core.constants import AGENT_ROLE
from buildblock.apps.management.views.base import ManagementDetailView, ManagementListView
from buildblock.apps.users.mixin import ViewPermissionCheckMixin
from buildblock.apps.users.models import User


class ManagementOwnerMixin(ViewPermissionCheckMixin):
    permitted_role_list = [AGENT_ROLE]
    model = User
    page_title = 'Owners'
    context_object_name = "owners"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            owned_products__in=self.products
        )
        return queryset


class ManagementOwnerListView(ManagementOwnerMixin, ManagementListView):
    template_name = "management/owner-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self._make_all_owners_context(
            owners=context[self.context_object_name]
        )
        return context


class ManagementOwnerDetailView(ManagementOwnerMixin, ManagementDetailView):
    template_name = "management/owner-detail.html"
    context_object_name = "owner"
    page_title = 'Owner Profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self._make_owner_context(
            owner=context[self.context_object_name]
        )
        return context
