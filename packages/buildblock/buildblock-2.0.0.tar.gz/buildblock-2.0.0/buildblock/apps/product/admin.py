from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from buildblock.apps.product import models


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 3


class ProductDocsInline(admin.TabularInline):
    model = models.ProductDocs
    extra = 3


@admin.register(models.Product)
class ProductAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title", "full_address", "created_at")
    search_fields = ["title", "code"]
    inlines = [ProductImageInline, ProductDocsInline]
