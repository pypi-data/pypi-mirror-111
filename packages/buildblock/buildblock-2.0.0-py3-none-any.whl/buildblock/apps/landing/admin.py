from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from simple_history.admin import SimpleHistoryAdmin

from buildblock.apps.landing import models


class CaseStudyVideoInline(admin.TabularInline):
    model = models.CaseStudyVideo
    extra = 2


class CaseStudyPhotoInline(admin.TabularInline):
    model = models.CaseStudyPhoto
    extra = 10


@admin.register(models.LandingInformation)
class LandingInformationAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['language', 'email', 'telephone', 'address', 'sns']
    search_fields = ['language', 'email', 'telephone', 'address', 'sns']


@admin.register(models.LandingCarousel)
class LandingCarouselAdmin(admin.ModelAdmin):
    list_display = ['title', 'ordering', 'start_date', 'end_date', 'is_active']
    list_editable = ['ordering', 'start_date', 'end_date', 'is_active']
    search_fields = ['title', 'ordering', 'start_date', 'end_date', 'is_active']


@admin.register(models.LandingVideo)
class LandingVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'playlist_url', 'video_url', 'ordering']
    list_editable = ['playlist_url', 'video_url', 'ordering']
    search_fields = ['title', 'playlist_url', 'video_url', 'ordering']


@admin.register(models.News)
class NewsAdmin(SimpleHistoryAdmin):
    list_display = ['title', 'language', 'news_category', 'report_date', 'headline']
    list_editable = ['language', 'news_category', 'report_date', 'headline']
    search_fields = ['title', 'language', 'news_category', 'report_date', 'headline']


@admin.register(models.CaseStudy)
class CaseStudyAdmin(SimpleHistoryAdmin):
    list_display = ['title',
                    'language',
                    'status',
                    'purchase_price',
                    'selling_price',
                    'report_date',
                    'headline',
                    'is_private']
    list_editable = ['language', 'status', 'purchase_price', 'selling_price', 'report_date', 'headline', 'is_private']
    search_fields = ['title', 'language', 'status', 'headline', 'is_private']
    inlines = [CaseStudyVideoInline, CaseStudyPhotoInline]


@admin.register(models.History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'year', 'quarter', 'ordering']
    list_editable = ['year', 'quarter', 'ordering']
    search_fields = ['title', 'subtitle', 'year', 'quarter', 'ordering']


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['name', 'department', 'position', 'ordering']
    list_editable = ['department', 'position', 'ordering']
    search_fields = ['name', 'department', 'position', 'ordering']


@admin.register(models.LandingPopup)
class LandingPopupAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'start_date', 'end_date', 'is_active']
    list_editable = ['url', 'start_date', 'end_date', 'is_active']
    search_fields = ['title', 'url', 'start_date', 'end_date', 'is_active']


@admin.register(models.LandingThinBanner)
class LandingThinBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'start_date', 'end_date', 'is_active']
    list_editable = ['url', 'start_date', 'end_date', 'is_active']
    search_fields = ['title', 'url', 'start_date', 'end_date', 'is_active']


@admin.register(models.LandingDocument)
class LandingDocumentAdmin(admin.ModelAdmin):
    list_display = ['language', 'title', 'document']
    list_display_links = ['title']
    search_fields = ['language', 'title', 'document']


@admin.register(models.Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'survey_amount', 'survey_purpose', 'message']
    search_fields = ['name', 'email', 'phone', 'survey_amount', 'survey_purpose', 'message']
