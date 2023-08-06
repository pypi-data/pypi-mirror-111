from enum import Enum
from urllib.parse import quote_plus, urlencode, urljoin

import googlemaps
from config.settings.base import GOOGLE_MAPS_KEY

from buildblock.decorators import memoized_classproperty
from buildblock.errors import InvalidParameterError

GOOGLE_MAP_HOST = "https://www.google.com/maps/"
GOOGLE_MAP_EMBED_HOST = urljoin(GOOGLE_MAP_HOST, "embed/v1/")
GOOGLE_MAP_TRAVEL_MODE_DRIVING = 'driving'

DISTANCE_UNIT = 'imperial'


class MapUrlApiEnum(Enum):
    URLS = 1    # https://developers.google.com/maps/documentation/urls/get-started
    EMBED = 2   # https://developers.google.com/maps/documentation/embed/embedding-map


class MapModeEnum(Enum):
    PLACE = 1       # a map pin at a particular place or address
    VIEW = 2        # with no markers or directions
    DIRECTIONS = 3  # the path between two or more specified points
    STREETVIEW = 4  # interactive panoramic views
    SEARCH = 5      # results for a search across the visible map region


MAP_LINK_MAPPING = {
    MapUrlApiEnum.URLS.value: {
        MapModeEnum.SEARCH.value: urljoin(GOOGLE_MAP_HOST, 'search/'),
        MapModeEnum.DIRECTIONS.value: urljoin(GOOGLE_MAP_HOST, 'dir/'),
    },
    MapUrlApiEnum.EMBED.value: {
        MapModeEnum.PLACE.value: urljoin(GOOGLE_MAP_EMBED_HOST, 'place'),
        MapModeEnum.VIEW.value: urljoin(GOOGLE_MAP_EMBED_HOST, 'view'),
        MapModeEnum.DIRECTIONS.value: urljoin(GOOGLE_MAP_EMBED_HOST, 'directions'),
        MapModeEnum.STREETVIEW.value: urljoin(GOOGLE_MAP_EMBED_HOST, 'streetview'),
        MapModeEnum.SEARCH.value: urljoin(GOOGLE_MAP_EMBED_HOST, 'search'),
    }
}


class GoogleMapService:
    @memoized_classproperty
    def _client(cls):
        return googlemaps.Client(key=GOOGLE_MAPS_KEY)

    @classmethod
    def _get_map_url(cls, map_api, mode, query: dict) -> str:
        mapping = MAP_LINK_MAPPING.get(map_api, {})
        map_link = mapping.get(mode)
        if not map_link:
            raise InvalidParameterError
        parameters = urlencode(query, quote_via=quote_plus)
        return f'{map_link}?{parameters}'

    @classmethod
    def get_directions(cls, destination: str, origin: str):
        return cls._client.directions(
            origin=origin,
            destination=destination,
            mode=GOOGLE_MAP_TRAVEL_MODE_DRIVING
        )

    @classmethod
    def get_recommended_direction(cls, destination: str, origin: str):
        directions = cls.get_directions(destination, origin)
        return next(iter(directions), {})

    @classmethod
    def get_recommended_direction_first_leg(cls, destination: str, origin: str):
        direction = cls.get_recommended_direction(destination, origin)
        return next(iter(direction.get('legs', [])))

    @classmethod
    def get_search_url(cls, address: str) -> str:
        query = {
            "api": 1,
            'query': address,
        }
        return cls._get_map_url(
            map_api=MapUrlApiEnum.URLS.value,
            mode=MapModeEnum.SEARCH.value,
            query=query
        )

    @classmethod
    def get_direction_url(cls, direction: dict) -> str:
        start_address = direction.get('start_address', '')
        end_address = direction.get('end_address', '')
        if not start_address or not end_address:
            raise InvalidParameterError
        query = {
            "api": 1,
            'origin': start_address,
            'destination': end_address,
            'travelmode': GOOGLE_MAP_TRAVEL_MODE_DRIVING
        }
        return cls._get_map_url(
            map_api=MapUrlApiEnum.URLS.value,
            mode=MapModeEnum.DIRECTIONS.value,
            query=query
        )

    @classmethod
    def get_direction_embed_src(cls, direction: dict) -> str:
        start_address = direction.get('start_address', '')
        end_address = direction.get('end_address', '')
        query = {
            "key": GOOGLE_MAPS_KEY,
            'origin': start_address,
            'destination': end_address,
            'mode': GOOGLE_MAP_TRAVEL_MODE_DRIVING,
            'units': DISTANCE_UNIT,
        }
        return cls._get_map_url(
            map_api=MapUrlApiEnum.EMBED.value,
            mode=MapModeEnum.DIRECTIONS.value,
            query=query
        )
