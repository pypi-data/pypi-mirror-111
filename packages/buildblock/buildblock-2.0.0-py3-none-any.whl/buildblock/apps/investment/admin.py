from django.contrib import admin

from buildblock.apps.investment import models


class InvestmentCompanyBankAccountInline(admin.TabularInline):
    model = models.InvestmentCompanyBankAccount
    extra = 3


@admin.register(models.InvestmentCompany)
class InvestmentCompanyAdmin (admin.ModelAdmin):
    list_display = ["title", "established_at"]
    search_fields = ["title", "established_at"]
    inlines = [InvestmentCompanyBankAccountInline]


@admin.register(models.InvestmentProduct)
class InvestmentProductAdmin (admin.ModelAdmin):
    list_display = ["title", "manager", "start_date"]
    search_fields = ["title", "manager", "start_date"]


@admin.register(models.Investment)
class InvestmentAdmin (admin.ModelAdmin):
    list_display = ["investment_product", "company", "amount"]
    search_fields = ["investment_product", "company", "amount"]


@admin.register(models.ContractTemplate)
class ContractTemplateAdmin (admin.ModelAdmin):
    list_display = ["identifier", "title"]
    search_fields = ["identifier", "title"]


@admin.register(models.InvestmentContract)
class InvestmentContractAdmin (admin.ModelAdmin):
    list_display = ["investment", "title"]
    search_fields = ["investment", "title"]


@admin.register(models.InvestmentWorkflowTemplate)
class InvestmentWorkflowTemplateAdmin (admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


@admin.register(models.InvestmentStep)
class InvestmentStepAdmin (admin.ModelAdmin):
    list_display = ["investment", "stage_id", "title", "actor_role", "status"]
    search_fields = ["investment", "stage_id", "title", "actor_role", "status"]


@admin.register(models.InvestmentCompanyBankTransaction)
class InvestmentCompanyBankTransactionAdmin (admin.ModelAdmin):
    list_display = [
        "investment",
        "to_entity_type",
        "to_entity_id",
        "from_entity_type",
        "from_entity_id",
        "category"
    ]
    search_fields = list_display
