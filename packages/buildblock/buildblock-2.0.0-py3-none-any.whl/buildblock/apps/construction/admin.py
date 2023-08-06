from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from buildblock.apps.construction import models


@admin.register(models.WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ["title"]


class ConstructionPicturesInline(admin.TabularInline):
    model = models.ConstructionPicture
    extra = 3


@admin.register(models.ConstructionWork)
class ConstructionWorkAdmin(SimpleHistoryAdmin):
    list_display = ["construction", "title", "type", "work_date"]
    inlines = [ConstructionPicturesInline]


class ConstructionWorkInline(admin.TabularInline):
    model = models.ConstructionWork
    extra = 3


@admin.register(models.Construction)
class ConstructionAdmin(SimpleHistoryAdmin):
    list_display = ("title", "status", "type", "product", "budget", "created_at")
    search_fields = ["title", "product"]
    inlines = [ConstructionWorkInline]


@admin.register(models.ConstructionExpense)
class ConstructionExpenseAdmin(SimpleHistoryAdmin):
    list_display = ["date", "category", "item", "amount", "quantity", "construction"]


@admin.register(models.ConstructionPersonnelExpense)
class ConstructionPersonnelExpenseAdmin(SimpleHistoryAdmin):
    list_display = ["date", "worker", "amount", "work_hours", "construction"]


@admin.register(models.ConstructionOutsourcingContract)
class ConstructionOutsourcingContractAdmin(SimpleHistoryAdmin):
    list_display = ["construction", "contractor", "title", "amount", "included_details", "start_date", "end_date"]


@admin.register(models.ConstructionOutsourcingExpense)
class ConstructionOutsourcingExpenseAdmin(SimpleHistoryAdmin):
    list_display = ["outsourcing_contract", "title", "amount", "paid_amount", "payment_date"]


@admin.register(models.Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ["name", "role", "speciality", "phone_number"]


@admin.register(models.ConstructionReport)
class ConstructionReportAdmin(SimpleHistoryAdmin):
    list_display = ["type", "start_date", "end_date", "construction"]
