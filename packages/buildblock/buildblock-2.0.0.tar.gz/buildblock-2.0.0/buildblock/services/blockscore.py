
import logging

import blockscore
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from buildblock.errors import BlockscoreFieldDoesNotExistError

logger = logging.getLogger(__name__)

EXCEPTIONS_FOR_MISSING_FIELD = frozenset([
    "address_street2"
])

BLOCKSCORE_FIELDS_TO_NAME_MAPPING = {
    "name_first": _('First Name'),
    "name_last": _('Last Name'),
    "birth_date": _('Date of Birth'),   # To birth_day, birth_month, birth_year
    "document_value": _('SSN'),
    "address_street1": _('Address Line 1'),
    "address_street2": _('Address Line 2'),
    "address_city": _('City'),
    "address_subdivision": _('State'),
    "address_postal_code": _('Zip Code'),
}


class BlockscoreService:

    def __init__(self, *args, **kwargs):
        self.client = blockscore.Client({'api_key': settings.BLOCKSCORE_API_KEY})

    @classmethod
    def create_people(cls, post, kv):
        blockscore_form = {
            "document_type": "ssn",
            "address_country_code": "US",
        }

        for field, field_name in BLOCKSCORE_FIELDS_TO_NAME_MAPPING.items():
            field_input = post.get(field, '')
            if not field_input and field not in EXCEPTIONS_FOR_MISSING_FIELD:
                kv.update(reason='Wrong Input: field value is empty', field_name=field)
                logger.info(f'Failed while submitting ssn_cert: {kv}')
                raise BlockscoreFieldDoesNotExistError(field_name)
            else:
                blockscore_form[field] = field_input

        birth_date = blockscore_form.pop("birth_date")
        (year, month, day) = birth_date.split("-")
        blockscore_form["birth_day"] = day
        blockscore_form["birth_month"] = month
        blockscore_form["birth_year"] = year

        return cls().client.people.create(blockscore_form).body
