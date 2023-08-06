from django.urls import reverse

from buildblock.apps.administrator.forms import InvitedUserForm, UserForm
from buildblock.apps.administrator.views.base import AdministratorServiceMixin
from buildblock.apps.core.views import CreateView, DeleteView, ListView, UpdateView
from buildblock.apps.users.models import User


class UserView(AdministratorServiceMixin):
    model = User
    page_title = "User"
    context_object_name = "users"
    form_class = UserForm

    def get_success_url(self):
        return reverse('administrator:user-list')


class UserListView(UserView, ListView):
    page_title = "Users"
    template_name = "administrator/user_list.html"
    paginate_by = 50


class InvitedUserCreateView(UserView, CreateView):
    page_title = "Create User"
    template_name = "administrator/base_form.html"
    form_class = InvitedUserForm


class UserUpdateView(UserView, UpdateView):
    page_title = "Update User"
    template_name = "administrator/base_form.html"


class UserDeleteView(UserView, DeleteView):
    page_title = "Delete User"
    template_name = "administrator/base_confirm_delete.html"
