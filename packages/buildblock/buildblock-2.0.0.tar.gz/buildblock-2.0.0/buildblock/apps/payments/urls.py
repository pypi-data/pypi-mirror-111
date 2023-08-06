from django.urls import path

from buildblock.apps.payments import views

app_name = "payments"

urlpatterns = [
    path("rent",
         view=views.stripe_payment_intents_view,
         name="stripe_payment_intents_view"),
    path("token",
         view=views.stripe_oauth_token_view,
         name="stripe_oauth_token_view"),
    path("webhook",
         view=views.stripe_webhook_view,
         name="stripe_webhook_view"),
    path("ach",
         view=views.stripe_ach_charge_view,
         name="stripe_ach_charge_view"),
    path("payout",
         view=views.stripe_payout_view,
         name="stripe_payout_view"),
    path("payout_schedule_change",
         view=views.stripe_payout_schedule_change_view,
         name="stripe_payout_schedule_change_view"),
]
