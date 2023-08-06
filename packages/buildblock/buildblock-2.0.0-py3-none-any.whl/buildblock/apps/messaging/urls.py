from django.urls import path

from buildblock.apps.messaging import views

app_name = "messaging"

urlpatterns = [
    path("template/list",
         view=views.MessagingListView.as_view(),
         name="template-list"),
    path('template/create/view',
         view=views.MessagingFormView.as_view(),
         name='template-create-view'),
    path('template/update/view/<int:pk>',
         view=views.MessagingFormView.as_view(),
         name='template-update-view'),
    path('template/upsert',
         view=views.messaging_upsert,
         name='template-upsert'),
    path('template/render/<int:pk>/',
         view=views.MessagingSendView.as_view(),
         name='render-message'),
    path('template/send',
         view=views.messaging_send,
         name='send-message'),
]
