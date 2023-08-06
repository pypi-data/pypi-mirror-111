from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from marshmallow import Schema, ValidationError, fields

from buildblock.apps.core.constants import (
    ACTIVE,
    IN_PROGRESS,
    PENDING,
    PRODUCT_PROPERTY_TYPE_CHOICES,
    PRODUCT_STATUS_CHOICES,
    US_STATE_CHOICES
)
from buildblock.apps.core.models import HistoricalRecordModel, TimeStampedModel, ZipcodeField, get_full_address
from buildblock.apps.investment.models import InvestmentProduct
from buildblock.apps.users.models import Group, User
from buildblock.decorators import memoized_property
from buildblock.utils import make_thumbnail_url


class ProductZoneSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)


def product_main_path(instance, filename):
    return f"product/{instance.code}/main/{filename}"


def product_plan_path(instance, filename):
    return f"product/{instance.code}/plan/{filename}"


def product_detail_path(instance, filename):
    return f"product/{instance.product.code}/detail/{filename}"


def product_docs_path(instance, filename):
    return f"product/{instance.product.code}/docs/{filename}"


class Product(HistoricalRecordModel):
    # Main
    code = models.CharField(_("Product code"), max_length=100, unique=True)
    title = models.CharField(_("Product Title"), max_length=200)
    main_image = models.ImageField(_("Main Image"), upload_to=product_main_path)
    plan_image = models.ImageField(_("House Plan Image"), upload_to=product_plan_path, blank=True)
    description = RichTextUploadingField(_("Product description"), blank=True)
    owner = models.ManyToManyField(User, related_name='owned_products', blank=True)
    status = models.CharField(_("Product Status"), choices=PRODUCT_STATUS_CHOICES, default=ACTIVE, max_length=16)

    # Site Information
    address_1 = models.CharField(_("Address 1"), max_length=128)
    address_2 = models.CharField(_("Address 2"), max_length=128, blank=True)
    city = models.CharField(_("City"), max_length=64)
    state = models.CharField(_("State"), choices=US_STATE_CHOICES, max_length=16)
    zip_code = ZipcodeField()
    map_url = models.CharField(_("Product Google Map Url"), max_length=500, blank=True)

    # Building Information
    property_type = models.CharField(_("Product Property Type"), choices=PRODUCT_PROPERTY_TYPE_CHOICES, max_length=64)
    built_year = models.PositiveIntegerField(_("Building Built"))
    sqft = models.FloatField(_("Square Footage"))
    lot_sqft = models.FloatField(_("Lot Square Footage"), default=0)
    num_people = models.PositiveIntegerField(_("The Number of People"))
    num_bedroom = models.FloatField(_("The Number of Bedrooms"))
    num_bathroom = models.FloatField(_("The Number of Bathrooms"))
    num_parking = models.FloatField(_("The Number of Parking Spaces"))
    washer_dryer = models.CharField(_("Washer & Dryer"), max_length=100)
    allowed_pets = models.CharField(_("Allowed Pets"), max_length=100)
    amenities = models.JSONField(default=dict, null=True, blank=True)
    application_fee_rate = models.FloatField(_("Application Fee Rate"),
                                             default=0.05,
                                             validators=[MinValueValidator(0), MaxValueValidator(1)])
    zone = models.JSONField(default=list, null=True, blank=True)

    # Investment Product Information
    investment_product = models.ForeignKey(InvestmentProduct, on_delete=models.SET_NULL, blank=True, null=True)
    agency = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')

    def __str__(self):
        return self.code

    def clean(self):
        if not self._has_valid_amenities:
            raise Exception('Invalid schema for the amenities field')
        if not self._has_valid_zone:
            raise Exception('Invalid schema for the zone field')

    @property
    def _has_valid_amenities(self):
        """
        {
            "heater": (some description),
            "cooling": (some other description),
        }
        """
        _allowed_key_set = {'heater', 'cooling'}

        if not set(self.amenities).issubset(_allowed_key_set):
            return False
        return True

    @property
    def _has_valid_zone(self):
        """
        방 이름이 변경이 되었을 때 데이터 유실을 없애기 위해 키값 적용
        [
            {"id": 1, "name": (zone 1)},
            {"id": 2, "name": (zone 2)},
            ...
        ]
        """
        try:
            if self.zone:
                ProductZoneSchema(many=True).load(self.zone)
        except ValidationError:
            return False
        return True

    @property
    def full_address(self):
        return get_full_address(self)

    @memoized_property
    def active_leases(self):
        return self.lease_product.filter(
            status__in=[PENDING, ACTIVE]
        )

    @memoized_property
    def active_constructions(self):
        return self.constructions.filter(
            status__in=[PENDING, IN_PROGRESS]
        )

    @property
    def main_thumbnail_image_url(self):
        return make_thumbnail_url(self.main_image)


class ProductImage(TimeStampedModel):
    """Product Detail Image"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_("Detail Image"), upload_to=product_detail_path)
    title = models.CharField(_("Image title"), max_length=100)

    @property
    def thumbnail_image_url(self):
        return make_thumbnail_url(self.image)


class ProductDocs(TimeStampedModel):
    """Product Documents: cf.Business plan"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='docs')
    docs = models.FileField(_("Docs file"), upload_to=product_docs_path)
    title = models.CharField(_("Docs title"), max_length=100)
