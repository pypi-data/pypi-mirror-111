import logging
from abc import ABC, abstractmethod
from urllib.parse import urlencode

from config.settings.base import LA_COUNTY_ASSESSOR_PORTAL_LINK, ZILLOW_LINK_MAPPING, ZIMAS_MAP_LINK

from buildblock.mixins import Loggable
from buildblock.models import property as model
from buildblock.services.googlemap import GoogleMapService
from buildblock.utils import convert_meters_to_feet

logger = logging.getLogger(__name__)

US_OFFICE_ADDRESS_LIST = ["2700 E 2nd St, Los Angeles, CA"]


class BasePropertyHandler(ABC, Loggable):

    def __init__(self, type, data: dict):
        self.type = type
        self.data = data

    @abstractmethod
    def info_origin(self):
        raise NotImplementedError

    @abstractmethod
    def _get_execution_fn_mapping(self) -> dict:
        pass

    @abstractmethod
    def _get_property_sale_list(self) -> dict:
        pass

    @abstractmethod
    def _get_property_detail(self) -> dict:
        pass

    def run(self):
        execution_fn = self._get_execution_fn_mapping().get(self.type)
        if not execution_fn:
            raise Exception('There is no function for the type you requested.')
        return execution_fn()

    def get_external_service_link_list(self, address) -> list:
        link_list = []
        # Real Estate Service
        zillow_detail_param = address.full.replace(" ", "_").replace(",", "") + "_rb"
        link_list.append(model.PropertyExternalServiceLink(
            title="Zillow",
            href=ZILLOW_LINK_MAPPING.get('detail') + zillow_detail_param
        ))
        # Map Service
        link_list.append(model.PropertyExternalServiceLink(
            title="Google Map",
            href=GoogleMapService.get_search_url(address.full)
        ))
        return link_list

    def get_assessor_link_list(self, address, assessor_parcel_number) -> list:
        link_list = []
        if address.county == "Los Angeles":
            link_list.append(model.PropertyExternalServiceLink(
                title="Assessor Portal",
                href=LA_COUNTY_ASSESSOR_PORTAL_LINK + assessor_parcel_number
            ))
            link_list.append(model.PropertyExternalServiceLink(
                title="ZIMAS",
                href=ZIMAS_MAP_LINK + urlencode([('apn', assessor_parcel_number)])
            ))
        # TODO: County 별로 추가 작업
        return link_list

    def get_direction_from_offices(self, full_address):
        direction_list = []
        for office in US_OFFICE_ADDRESS_LIST:
            try:
                direction = GoogleMapService.get_recommended_direction_first_leg(full_address, office)
            except Exception as e:
                direction = None
                logger.error(f'Error has occurred while getting dicrection: {str(e)}')
            if not direction:
                continue
            # TODO:Check offices less than (X) miles or in the same state.
            distance = direction.get('distance', {})
            direction['distance']['value'] = convert_meters_to_feet(distance.get('value'))
            direction_list.append({'office': office, 'data': direction})
        return [
            model.Direction(
                destination=full_address,
                origin=direction['office'],
                distance=direction['data'].get('distance', {}).get('value'),
                duration=direction['data'].get('duration', {}).get('value'),
                map_url=GoogleMapService.get_direction_url(direction['data']),
                embed_src=GoogleMapService.get_direction_embed_src(direction['data'])
            ) for direction in direction_list
        ]
