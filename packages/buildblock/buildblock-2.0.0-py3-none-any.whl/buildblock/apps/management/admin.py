from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from buildblock.apps.management.models import Invoice, Lease, LeaseDocs, Maintenance


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['product', 'tenant', 'status', 'title', 'content', 'comments']
    search_fields = ['product', 'tenant', 'status', 'title', 'content', 'comments']


class LeaseDocsInline(admin.TabularInline):
    model = LeaseDocs
    extra = 3


@admin.register(Lease)
class LeaseAdmin(SimpleHistoryAdmin):
    list_display = ['room_num', 'owner', 'tenant', 'product', 'status',
                    'start_date', 'end_date', 'deposit', 'move_in_date', 'move_out_date', 'is_auto_paid']
    search_fields = ['room_num', 'owner', 'tenant', 'product', 'status',
                     'start_date', 'end_date', 'deposit', 'move_in_date', 'move_out_date']
    inlines = [LeaseDocsInline]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["product", "owner", "tenant", "period", "amount"]
    search_fields = ["product", "owner", "tenant", "period"]
