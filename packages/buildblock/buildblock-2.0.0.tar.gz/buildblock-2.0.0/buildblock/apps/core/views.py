from allauth.account.views import LoginView, PasswordChangeView, SignupView
from django.views import generic
from hitcount.views import HitCountDetailView


class ViewSetupMixin:
    page_title = "BuildBlock"
    service_role_set = set()
    service_app_name = None
    paginate_by = 20
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['service_role_set'] = self.service_role_set
        context['service_app_name'] = self.service_app_name
        return context


class TemplateView(ViewSetupMixin, generic.TemplateView):
    pass


class DetailView(ViewSetupMixin, generic.DetailView):
    pass


class HitCountDetailView(ViewSetupMixin, HitCountDetailView):
    pass


class CreateView(ViewSetupMixin, generic.CreateView):
    pass


class UpdateView(ViewSetupMixin, generic.UpdateView):
    pass


class FormView(ViewSetupMixin, generic.FormView):
    pass


class ListView(ViewSetupMixin, generic.ListView):
    pass


class DeleteView(ViewSetupMixin, generic.DeleteView):
    pass


class RedirectView(ViewSetupMixin, generic.RedirectView):
    pass


class SignupView(ViewSetupMixin, SignupView):
    pass


class LoginView(ViewSetupMixin, LoginView):
    pass


class PasswordChangeView(ViewSetupMixin, PasswordChangeView):
    pass
