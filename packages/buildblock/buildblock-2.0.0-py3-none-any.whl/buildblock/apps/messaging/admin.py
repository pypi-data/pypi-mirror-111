from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from buildblock.apps.messaging.models import MessagingRequests, MessagingTemplates


@admin.register(MessagingTemplates)
class MessagingTemplatesAdmin(SimpleHistoryAdmin):
    list_display = ['title', 'category', 'creator', 'is_active']
    search_fields = ['title', 'category', 'creator', 'is_active']


@admin.register(MessagingRequests)
class MessagingRequestsAdmin(SimpleHistoryAdmin):
    list_display = ['title', 'sender', 'receivers', 'sent_at']
    search_fields = ['title', 'sender', 'receivers', 'sent_at']
