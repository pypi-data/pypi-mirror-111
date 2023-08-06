from django.urls import path

from buildblock.apps.core.constants import INVESTMENT_APP_NAME
from buildblock.apps.investment import views
from buildblock.apps.users.views import active_role_change

app_name = INVESTMENT_APP_NAME

urlpatterns = [
    # TODO: Overview 페이지 작업 후 변경
    path("",
         view=views.InvestmentListView.as_view(),
         name="home"),

    # Account
    path("signup/",
         view=views.InvestmentRoleSignupSelectView.as_view(),
         name="signup-choice"),
    path("signup/<str:application_role>/",
         view=views.InvestmentRoleSignupView.as_view(),
         name="signup-role"),
    path("select/",
         view=views.InvestmentRoleSelectView.as_view(),
         name="select-role"),
    path("role_change/<str:user_role>/",
         view=active_role_change,
         name="change-role"),
    path("profile_update/",
         view=views.InvestmentRoleUpdateView.as_view(),
         name="profile-update"),

    path("list",
         view=views.InvestmentListView.as_view(),
         name="list"),
    path("detail/<int:pk>",
         view=views.InvestmentDetailView.as_view(),
         name="detail"),
    path("document/list",
         view=views.DocumentListView.as_view(),
         name="document-list"),
    path("document/download/<int:pk>",
         view=views.DocumentDownloadView.as_view(),
         name="document-download"),
    path("profile",
         view=views.InvestmentProfileView.as_view(),
         name="profile"),
]
