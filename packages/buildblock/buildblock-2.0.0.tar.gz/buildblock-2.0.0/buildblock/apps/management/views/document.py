from django.urls import reverse

from buildblock.apps.core.constants import AGENT_ROLE, OWNER_ROLE
from buildblock.apps.core.models import add_read_data_at_record
from buildblock.apps.management.forms import LeaseDocumentForm
from buildblock.apps.management.models import LeaseDocs
from buildblock.apps.management.views.base import (
    ManagementCreateView,
    ManagementListView,
    ManagementPrivateStorageDetailView,
    ManagementUpdateView
)
from buildblock.apps.users.mixin import ViewPermissionCheckMixin
from buildblock.helper import db_update
from buildblock.services.management import ManagementService
from buildblock.services.user import UserService


class ManagementDocumentMixin(ViewPermissionCheckMixin):
    page_title = "Lease Documents"
    context_object_name = 'documents'
    permitted_role_list = [OWNER_ROLE, AGENT_ROLE]
    model = LeaseDocs
    form_class = LeaseDocumentForm
    template_name = "management/document-form.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(lease__product__in=self.products)

    def get_success_url(self):
        return reverse("management:document-list")


class ManagementDocumentListView(ManagementDocumentMixin, ManagementListView):
    template_name = "management/document.html"

    def with_tenant_filter(self, queryset):
        tenant_id = self.request.GET.get('tenant')
        if tenant_id:
            queryset = queryset.filter(lease__tenant__id=tenant_id)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.with_tenant_filter(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tenants'] = ManagementService.get_live_tenants_by_products(self.products)
        tenant_id = self.request.GET.get('tenant')
        if tenant_id:
            tenant = UserService.get_user(self.request.GET.get('tenant'))
            context['selected_tenant_filter'] = tenant.name
        return context


class ManagementDocumentFormMixin(ManagementDocumentMixin):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['leases'] = ManagementService.get_live_leases_by_products(self.products)
        return kwargs


class ManagementDocumentCreateView(ManagementDocumentFormMixin, ManagementCreateView):
    page_title = "Lease Document Create"


class ManagementDocumentUpdateView(ManagementDocumentFormMixin, ManagementUpdateView):
    page_title = "Lease Document Update"


class ManagementDocumentDownloadView(ManagementDocumentMixin, ManagementPrivateStorageDetailView):
    model_file_field = 'document'

    def can_access_file(self, private_file):
        return private_file.request.user.is_authenticated

    def get(self, request, *args, **kwargs):
        self.object = document = self.get_object()
        # Append Read Data in Record
        document.records = add_read_data_at_record(document.records, self.request.user)
        db_update(document)
        return super().get(request, *args, **kwargs)
