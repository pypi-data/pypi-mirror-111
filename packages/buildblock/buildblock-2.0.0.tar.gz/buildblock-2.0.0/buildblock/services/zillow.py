'''
Zillow 기반의 RapidApi 서비스 이용
https://rapidapi.com/datascraper/api/Zillow.com%20Real%20Estate
'''

import json
from enum import Enum

import requests
from config.settings.base import RAPIDAPI_KEY, ZILLOW_API_HOST

ZILLOW_PROPERTY_TYPE_DICT = {
    "single_family": "Houses",
    "multi_family": "Multi-family",
    "manufactured": "Manufactured",
    "apartments": "Apartments",
    "condo": "Condos",
    "land": "LotsLand",
    "town": "Townhomes",
}

ZILLOW_PROPERTY_SORT_DICT = {
    "relevant": "Homes_for_You",
    "newest": "Newest",
    "lowest_price": "Price_Low_High",
    "highest_price": "Price_High_Low",
    "largest_sqft": "Square_Feet",
    "lot_size": "Lot_Size",
}


class ZillowPathEnum(Enum):
    '''Available Zillow Api Url Path'''
    IMAGES = "/images"
    PROPERTY_BY_COORDINATES = "/propertyByCoordinates"
    PROPERTY_SEARCH = "/propertyExtendedSearch"
    PROPERTY_DETAIL = "/property"


class ZillowService:
    @staticmethod
    def _get_data(path, params):
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': ZILLOW_API_HOST
        }
        url = f"https://{ZILLOW_API_HOST}{path}"
        response = json.loads(
            requests.request("GET", url, headers=headers, params=params).text
        )
        return response

    @staticmethod
    def _get_list(filter_dict: dict):
        params = dict()
        params['location'] = f"{filter_dict['city']}, {filter_dict['state_code']}"
        if filter_dict.get('property_type'):
            property_type_list = []
            for property_type in filter_dict.get('property_type'):
                property_type_list.append(ZILLOW_PROPERTY_TYPE_DICT.get(property_type))
            params['home_type'] = ",".join(property_type_list)
        if filter_dict.get('sort'):
            params['sort'] = ZILLOW_PROPERTY_SORT_DICT.get(filter_dict['sort'])
        if filter_dict.get('price_min'):
            params['minPrice'] = filter_dict['price_min']
        if filter_dict.get('price_max'):
            params['maxPrice'] = filter_dict['price_max']
        if filter_dict.get('baths_min'):
            params['bathsMin'] = filter_dict['baths_min']
        if filter_dict.get('baths_max'):
            params['bathsMax'] = filter_dict['baths_max']
        if filter_dict.get('beds_min'):
            params['bedsMin'] = filter_dict['beds_min']
        if filter_dict.get('beds_max'):
            params['bedsMax'] = filter_dict['beds_max']
        return ZillowService._get_data(
            path=ZillowPathEnum.PROPERTY_SEARCH.value,
            params=params
        )

    @staticmethod
    def get_for_sale(filter_dict: dict):
        filter_dict['status_type'] = "ForSale"
        return ZillowService._get_list(filter_dict=filter_dict)

    @staticmethod
    def get_sold_homes(filter_dict: dict):
        filter_dict['status_type'] = "RecentlySold"
        return ZillowService._get_list(filter_dict=filter_dict)

    @staticmethod
    def get_property_detail(property_id):
        return ZillowService._get_data(
            path=ZillowPathEnum.PROPERTY_DETAIL.value,
            params={"zpid": property_id}
        )

    @staticmethod
    def get_property_images(property_id):
        return ZillowService._get_data(
            path=ZillowPathEnum.IMAGES.value,
            params={"zpid": property_id}
        ).get('images')
