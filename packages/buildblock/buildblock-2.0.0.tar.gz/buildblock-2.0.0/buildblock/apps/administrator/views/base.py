from django.contrib.auth.mixins import LoginRequiredMixin

from buildblock.apps.access_control import require_admin_access
from buildblock.apps.core.views import TemplateView
from buildblock.apps.property.constants import PropertyInfoOriginEnum


class AdministratorServiceMixin(LoginRequiredMixin):
    page_title = "Administrator Page"
    info_origin = PropertyInfoOriginEnum.ZILLOW.value

    @require_admin_access
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info_origin'] = self.info_origin
        return context


class AdministratorTemplateView(AdministratorServiceMixin, TemplateView):
    pass
