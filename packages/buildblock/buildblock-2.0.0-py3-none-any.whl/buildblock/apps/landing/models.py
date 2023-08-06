from datetime import date

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db.models import JSONField
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_better_admin_arrayfield.models.fields import ArrayField
from marshmallow import Schema, ValidationError, fields

from buildblock.apps.core.constants import AFTER, BEFORE, ENGLISH, LANGUAGE_CHOICES, PENDING
from buildblock.apps.core.enums import TeamMemberDepartment
from buildblock.apps.core.models import HistoricalRecordModel, TimeStampedModel
from buildblock.apps.landing import paths
from buildblock.apps.landing.constants import (
    CASE_STUDY_CATEGORY,
    LANDING_NEWS_CATEGORY,
    SURVEY_AMOUNT_CHOICE,
    SURVEY_PURPOSE_CHOICE
)
from buildblock.utils import make_thumbnail_url

CASE_STUDY_CKEDITOR_EXTERNAL_PLUGIN_RESOURCE = [
    ('youtube', settings.STATIC_URL + 'ckeditor/ckeditor/plugins/youtube/youtube/', 'plugin.js')
]


class InformationEmailSchema(Schema):
    category = fields.Str(required=True)
    email = fields.Str(required=True)


class InformationTelephoneSchema(Schema):
    title = fields.Str(required=True)
    telephone = fields.Str(required=True)


class InformationAddressSchema(Schema):
    location = fields.Str(required=True)
    address = fields.Str(required=True)


class InformationSnsSchema(Schema):
    name = fields.Str(required=True)
    url = fields.Str(required=True)


class Inquiry(TimeStampedModel):
    """This model represents the investment Survey"""
    survey_amount = models.CharField(_("Survey Amount"), choices=SURVEY_AMOUNT_CHOICE, max_length=100)
    survey_purpose = models.CharField(_("Survey Purpose"), choices=SURVEY_PURPOSE_CHOICE, max_length=100)
    message = models.TextField(_("Question"))
    name = models.CharField(_("Name"), max_length=100, default='')
    email = models.CharField(_("Email"), max_length=100, default='')
    phone = models.CharField(_("Phone"), max_length=100, default='')


class News(HistoricalRecordModel):
    """This model represents the news in landing page"""
    news_category = models.CharField(_("Category"), choices=LANDING_NEWS_CATEGORY, max_length=20)
    language = models.CharField(_("Language"), choices=LANGUAGE_CHOICES, max_length=50)
    title = models.CharField(_("Title"), max_length=200)
    writer = models.CharField(_("Writer"), max_length=100, null=True, blank=True)
    content = RichTextUploadingField(_("Content"), max_length=30000)
    thumbnail = models.ImageField(_("Thumbnail"), upload_to=paths.news_thumbnail_path, null=True, blank=True)
    report_date = models.DateField(_("Report Date"), default=date.today)
    headline = models.BooleanField(_("Headline"), default=False)

    @property
    def news_thumbnail_url(self):
        return make_thumbnail_url(self.thumbnail)


class CaseStudy(HistoricalRecordModel):
    status = models.CharField(_("Status"),
                              choices=CASE_STUDY_CATEGORY,
                              default=PENDING,
                              max_length=16)     # 모집예정(Pending), 모집중(Open), 진행중(Active), 투자완료(Complete)
    language = models.CharField(_("Language"), choices=LANGUAGE_CHOICES, max_length=50)
    title = models.CharField(_("Title"), max_length=200)
    thumbnail = models.ImageField(_("Thumbnail"), upload_to=paths.case_study_thumbnail_path, null=True, blank=True)
    purchase_price = models.PositiveIntegerField(_("Purchase Price"), blank=True, null=True)
    selling_price = models.PositiveIntegerField(_("Selling Price"), blank=True, null=True)
    content = RichTextUploadingField(_("Content"))
    map_url = models.CharField(_("Google Map Url"), max_length=500, blank=True)
    report_date = models.DateField(_("Report Date"), default=date.today)
    headline = models.BooleanField(_("Headline"), default=False)
    is_private = models.BooleanField(default=False)

    @property
    def news_thumbnail_url(self):
        return make_thumbnail_url(self.thumbnail)


class CaseStudyPhoto(TimeStampedModel):
    """CaseStudy Before/After Photos"""
    case_product = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name='photos')
    status = models.CharField(_("Status"),
                              choices=((BEFORE, _('BEFORE')), (AFTER, _('AFTER'))),
                              default=BEFORE,
                              max_length=16)
    photo = models.ImageField(_("photo"), upload_to=paths.case_study_photo_path)

    @property
    def thumbnail_image_url(self):
        return make_thumbnail_url(self.photo)


class CaseStudyVideo(TimeStampedModel):
    """CaseStudy Youtube Videos"""
    case_product = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name='videos')
    url = models.CharField(_("Video Url"), max_length=500, blank=True)


class History(TimeStampedModel):
    year = models.IntegerField(_('Year'), validators=[MinValueValidator(2017)])
    quarter = models.IntegerField(_('Quarter'), choices=((q, q) for q in range(1, 5)))
    title = models.CharField(_("Title"), max_length=200)
    subtitle = models.CharField(_("Sub Title"), max_length=200, blank=True, null=True)
    ordering = models.CharField(_("Ordering"), max_length=200, default=1)

    @property
    def date_display(self):
        year_str = str(self.year)
        quarter_str = str(self.quarter)
        return year_str + "-" + quarter_str + "Q"


class Team(TimeStampedModel):
    department = models.CharField(_("Department"), choices=TeamMemberDepartment.choices(), max_length=50)
    profile_image = models.ImageField(_("Profile Image"),
                                      upload_to=paths.team_profile_image_path,
                                      null=True,
                                      blank=True)
    name = models.CharField(_("Name"), max_length=30)
    position = models.CharField(_("Position"), max_length=100)
    work_experience = ArrayField(
        models.CharField(_("Work Experience"), max_length=200), blank=True, default=list
    )
    education = ArrayField(
        models.CharField(_("Education"), max_length=200), blank=True, default=list
    )
    description = models.TextField(_("Description"), blank=True, null=True)
    ordering = models.CharField(_("Ordering"), max_length=100, default=1)


# 회사 정보
class LandingInformation(TimeStampedModel):
    language = models.CharField(_("Language"), choices=LANGUAGE_CHOICES, max_length=50, default=ENGLISH)
    email = JSONField(default=list)
    telephone = JSONField(default=list)
    address = JSONField(default=list)
    sns = JSONField(default=list)

    @property
    def _has_valid_email(self):
        """
        [
            {"category": (category or purpose), "email": (email)},
            ...
        ]
        """
        try:
            InformationEmailSchema(many=True).load(self.address)
        except ValidationError:
            return False
        return True

    @property
    def _has_valid_telephone(self):
        """
        [
            {"title": (title or location), "telephone": (telephone)},
            ...
        ]
        """
        try:
            InformationTelephoneSchema(many=True).load(self.address)
        except ValidationError:
            return False
        return True

    @property
    def _has_valid_address(self):
        """
        [
            {"location": (city, country), "address": (address)},
            ...
        ]
        """
        try:
            InformationAddressSchema(many=True).load(self.address)
        except ValidationError:
            return False
        return True

    @property
    def _has_valid_sns(self):
        """
        [
            {"name": (channel name), "url": (sns url)},
            ...
        ]
        """
        try:
            InformationSnsSchema(many=True).load(self.sns)
        except ValidationError:
            return False
        return True


# 카탈로그 등 다운로드 파일
class LandingDocument(TimeStampedModel):
    language = models.CharField(_("Language"), choices=LANGUAGE_CHOICES, max_length=50)
    document = models.FileField(_("Document"), upload_to=paths.landing_document_path)
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"), blank=True, null=True)


# 랜딩페이지에 보여줄 유튜브 비디오 슬라이드, 각 코너별로 대표 동영상 하나를 노출
class LandingVideo(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=200)                                        # 코너명
    description = models.TextField(_("Description"), blank=True, null=True)                     # 코너 설명
    playlist_url = models.CharField(_("Playlist Url"), max_length=500, blank=True, null=True)   # 코너 재생목록 페이지 링크
    video_url = models.CharField(_("Video Url"), max_length=500)                                # 해당 코너의 대표 비디오 링크
    ordering = models.CharField(_("Ordering"), max_length=100, default=1)                       # 슬라이드 순서


# 랜딩페이지 메인 슬라이드
class LandingCarousel(TimeStampedModel):
    ordering = models.CharField(_("Ordering"), max_length=100, default=1)
    start_date = models.DateField(_("From"))
    end_date = models.DateField(_("To"))
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"), blank=True, null=True)
    button_title = models.CharField(_("Button Title"), max_length=50, blank=True, null=True)
    button_url = models.CharField(_("Button Url"), max_length=500, blank=True, null=True)
    image = models.ImageField(_("Banner Image"), upload_to=paths.landing_carousel_path)
    image_mobile = models.ImageField(_("Banner Mobile Image"),
                                     upload_to=paths.landing_carousel_path,
                                     blank=True,
                                     null=True)
    is_active = models.BooleanField(_("Is Active"), default=False)


# 랜딩페이지 메뉴바 위에 띠배너
class LandingThinBanner(TimeStampedModel):
    start_date = models.DateField(_("From"))
    end_date = models.DateField(_("To"))
    title = models.CharField(_("Title"), max_length=200)
    url = models.CharField(_("Url"), max_length=500, blank=True, null=True)
    image = models.ImageField(_("Banner Image"), upload_to=paths.landing_thin_banner_path)
    image_mobile = models.ImageField(_("Banner Mobile Image"),
                                     upload_to=paths.landing_thin_banner_path,
                                     blank=True,
                                     null=True)
    is_active = models.BooleanField(_("Is Active"), default=False)


# 랜딩페이지 팝업
class LandingPopup(TimeStampedModel):
    start_date = models.DateField(_("From"))
    end_date = models.DateField(_("To"))
    title = models.CharField(_("Title"), max_length=200)
    url = models.CharField(_("Url"), max_length=500, blank=True, null=True)
    image = models.ImageField(_("Popup Image"), upload_to=paths.landing_popup_path)
    image_mobile = models.ImageField(_("Popup Mobile Image"), upload_to=paths.landing_popup_path, blank=True, null=True)
    is_active = models.BooleanField(_("Is Active"), default=False)
