from datetime import date

from django import template
from django.urls import reverse

from buildblock.apps.core.constants import (
    ACTIVE,
    FINISHED,
    INACTIVE,
    LANGUAGE_CHOICES,
    MESSAGING_TEMPLATE_CATEGORY_CHOICES,
    PENDING
)
from buildblock.apps.core.templatetags.base_tag import badge_format
from buildblock.apps.property.constants import PropertyInfoOriginEnum
from buildblock.apps.signed_url.handler import SignedUrlHandler

register = template.Library()


@register.simple_tag
def get_board_language_list():
    return LANGUAGE_CHOICES


@register.simple_tag
def get_template_category_list():
    return MESSAGING_TEMPLATE_CATEGORY_CHOICES


@register.simple_tag
def get_signed_url_for_zillow_property_details(email, property_id):
    info_origin = PropertyInfoOriginEnum.ZILLOW
    redirect_url = reverse(
        'administrator:property-detail',
        kwargs={'info_origin': info_origin.value,
                'property_id': property_id}
    )
    return SignedUrlHandler.create_signed_url(
        user_email=email,
        redirect_url=redirect_url,
        expiration_days=7,
    )


@register.simple_tag
def get_landing_asset_active_badge(start_date, end_date, is_active):
    if start_date <= date.today() and date.today() <= end_date:
        asset_status = ACTIVE
    elif start_date > date.today():
        asset_status = PENDING
    elif end_date < date.today():
        asset_status = FINISHED

    if not is_active:
        return badge_format(style="badge badge-secondary", text=INACTIVE)
    elif is_active and asset_status == 'active':
        return badge_format(style="badge badge-success", text=ACTIVE)
    elif is_active and asset_status == 'pending':
        return badge_format(style="badge badge-light", text=PENDING)
    elif is_active and asset_status == 'finished':
        return badge_format(style="badge badge-dark", text=FINISHED)
    else:
        return 'Incorrect Data'
