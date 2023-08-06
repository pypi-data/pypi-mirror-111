from django.contrib import admin

from buildblock.apps.administrator.models import Agreement, Faq


@admin.register(Faq)
class FaqAdmin (admin.ModelAdmin):
    list_display = ["language", "question", "answer"]
    search_fields = ["language", "question", "answer"]


@admin.register(Agreement)
class AgreementAdmin (admin.ModelAdmin):
    list_display = ["service_type", "agreement_type", "language", "title"]
    search_fields = ["service_type", "agreement_type", "language", "title"]
