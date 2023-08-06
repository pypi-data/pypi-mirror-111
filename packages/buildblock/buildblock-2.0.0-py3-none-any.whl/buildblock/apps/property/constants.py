from enum import Enum

from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import ACTIVE, INACTIVE


class PropertyCallEnum(Enum):
    PROPERTY_SALE_LIST = 1
    PROPERTY_DETAIL = 2
    PROPERTY_SOLD_LIST = 3


class PropertyInfoOriginEnum(Enum):
    ZILLOW = 'zillow'


# Property Filter
PROPERTY_SUBSCRIPTION_FILTER_CHOICES = (
    (ACTIVE, _("ACTIVE")),
    (INACTIVE, _("INACTIVE")),
)


PROPERTY_TYPE_FOR_FILTER_CHOICES = (
    ("single_family", _("Single Family")),
    ("multi_family", _("Multi Family")),
    ("apartments", _("Apartments")),
    ("town", _("Townhomes")),
    ("condo", _("Condo")),
    ("land", _("Land")),
    ("manufactured", _("Manufactured")),
)

PROPERTY_FILTER_SORT_CHOICES = (
    ("relevant", _("Relevant")),
    ("newest", _("Newest")),
    ("lowest_price", _("Lowest Price")),
    ("highest_price", _("Highest Price")),
    ("largest_sqft", _("Largest Sqft")),
    ("lot_size", _("Lot Size")),
)
