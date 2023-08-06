from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _


class ServiceSetupMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check Class Property
        if not self.service_app_name and self.service_role_set:
            messages.warning(self.request, _('Please select the correct service.'))
            return redirect("home")
        # Setup Path
        self.select_role_path = f"{self.service_app_name}:select-role"
        self.signup_choice_path = f"{self.service_app_name}:signup-choice"
        return super().dispatch(request, *args, **kwargs)


class AlreadySignedupCheck:
    '''Check already registered for this role.'''
    def dispatch(self, request, *args, **kwargs):
        application_role = self.kwargs.get('application_role')
        if application_role in self.request.user.user_role:
            messages.warning(self.request, _('You have already signed up for the role.'))
            return redirect(self.get_success_url())
        if application_role not in self.service_role_set:
            messages.warning(self.request, _('Invalid Access'))
            return redirect(self.signup_choice_path)
        return super().dispatch(request, *args, **kwargs)


class AlreadySignedupCheckMixin(ServiceSetupMixin, LoginRequiredMixin, AlreadySignedupCheck):
    pass


class ServiceSignupCheck:
    '''Check that user has the role of this service and the role argument is set.'''
    def dispatch(self, request, *args, **kwargs):
        if not self.service_app_name:
            messages.warning(self.request, _('Please select the correct service.'))
            return redirect("home")

        self.active_role = self.request.session.get('active_role')
        common_role = set(self.request.user.user_role).intersection(self.service_role_set)
        if len(common_role) < 1:
            messages.warning(self.request, _('Please submit your application to use the service.'))
            return redirect(self.signup_choice_path)
        if self.active_role in common_role or len(common_role) == 1:
            self.request.session['active_role'] = self.active_role = self.active_role or next(iter(common_role))
            return super().dispatch(request, *args, **kwargs)

        return redirect(self.select_role_path)


class ServiceSignupCheckMixin(ServiceSetupMixin, LoginRequiredMixin, ServiceSignupCheck):
    pass


class ViewPermissionCheck:
    '''Check that the role is registered.'''
    permitted_role_list = list()

    def dispatch(self, request, *args, **kwargs):
        if not self.active_role:
            return redirect(self.select_role_path)

        if self.active_role not in self.permitted_role_list:
            messages.warning(self.request, _('This page cannot be accessed with the current role.'))
            # 접속 가능한 Role과 유저가 가입한 Role 중에 중복 되는 것이 없다면 Role 등록 페이지로
            if set(self.request.user.user_role).isdisjoint(self.permitted_role_list):
                return redirect(self.signup_choice_path)
            return redirect(self.select_role_path)
        return super().dispatch(request, *args, **kwargs)


class ViewPermissionCheckMixin(ServiceSignupCheckMixin, ViewPermissionCheck):
    pass
