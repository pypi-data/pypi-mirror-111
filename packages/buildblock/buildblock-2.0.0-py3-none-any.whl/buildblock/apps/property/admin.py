from django.contrib import admin

from buildblock.apps.property.models import PropertySubscriptionFilter


@admin.register(PropertySubscriptionFilter)
class PropertySubscriptionFilterAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'emails']
    list_editable = ['status', 'emails']
    search_fields = ['title', 'status', 'emails']
