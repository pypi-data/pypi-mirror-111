from datetime import datetime

from django.urls import reverse

from buildblock.apps.property.constants import PropertyCallEnum, PropertyInfoOriginEnum
from buildblock.apps.property.handlers.base import BasePropertyHandler
from buildblock.models import property as model
from buildblock.services.zillow import ZillowService


def _reformat_zillow_datetime(value=0):
    return datetime.utcfromtimestamp(int(value)/1000) if value > 0 else value


class ZillowPropertyHandler(BasePropertyHandler):
    info_origin = PropertyInfoOriginEnum.ZILLOW

    def _get_execution_fn_mapping(self):
        return {
            PropertyCallEnum.PROPERTY_SALE_LIST: self._get_property_sale_list,
            PropertyCallEnum.PROPERTY_SOLD_LIST: self._get_property_sold_list,
            PropertyCallEnum.PROPERTY_DETAIL: self._get_property_detail,
        }

    def _get_property_list(self, response):
        properties = [
            self._make_property_context(property)
            for property in response.get('props')
        ]
        return dict(
            properties=properties,
            total=response.get('totalResultCount'),
            count=response.get('resultsPerPage'),
        )

    def _get_property_sale_list(self):
        response = ZillowService.get_for_sale(self.data)
        return self._get_property_list(response)

    def _get_property_sold_list(self):
        response = ZillowService.get_sold_homes(self.data)
        return self._get_property_list(response)

    def _get_property_detail(self):
        response = ZillowService.get_property_detail(self.data.get("property_id"))
        return dict(
            property=self._make_property_detail_context(response)
        )

    def _get_property_images(self, property_id):
        return ZillowService.get_property_images(property_id).get('images')

    def _make_address_context(self, property):
        address = property.get('address', {})
        full_address_list = []
        full_address_list.append(str(address.get('city', '')))
        full_address_list.append(str(address.get('state', '')))
        full_address_list.append(str(address.get('zipcode', '')))
        full_address = ', '.join(full_address_list)
        full_address = str(address.get('streetAddress', '')) + ' ' + full_address
        coordinate = model.Coordinate(
            lng=property.get('longitude'),
            lat=property.get('latitude')
        )
        direction_from_offices = self.get_direction_from_offices(full_address)
        return model.Address(
            full=full_address,
            state=address.get('state'),
            line=address.get('streetAddress'),
            city=address.get('city'),
            postal_code=address.get('zipcode'),
            coordinate=coordinate,
            county=property.get('county'),
            fips_code=property.get('countyFIPS'),
            country=property.get('country'),
            city_slug_id=property.get('cityId'),
            direction_from_offices=direction_from_offices,
        )

    def _make_data_source_context(self, data_source):
        return model.DataSource(
            name=data_source.get('agentName'),
            description=data_source.get('disclaimerText'),
            group=data_source.get('postingGroupName'),
            phone=data_source.get('phoneNumber'),
            url=data_source.get('postingWebsiteURL'),
        )

    def _make_property_image_list_context(self, property_id):
        return ZillowService.get_property_images(property_id) or []

    def _make_property_history_context(self, history):
        return model.PropertyHistory(
            event_name=history.get('event'),
            date=_reformat_zillow_datetime(history.get('time') or 0),
            source_name=history.get('source'),
            price=history.get('price'),
            change_rate=history.get('priceChangeRate'),
        )

    def _make_property_history_list_context(self, histories):
        return [
            self._make_property_history_context(history)
            for history in histories
        ] if histories else []

    def _make_tax_history_context(self, history):
        assessment = history.get('assessment') or {}
        return model.PropertyTaxHistory(
            tax=history.get('taxPaid'),
            year=history.get('time'),
            assessment_value=assessment.get('value'),
        )

    def _make_tax_history_list_context(self, histories):
        return [
            self._make_tax_history_context(history)
            for history in histories
        ] if histories else []

    def _make_school_context(self, school):
        return model.School(
            rating=school.get('rating'),
            assigned=school.get('isAssigned'),
            name=school.get('name'),
            funding_type=school.get('type'),
            parent_rating=school.get('rating'),
            student_teacher_ratio=school.get('studentsPerTeacher'),
            education_levels=school.get('level'),
            link=school.get('link'),
            grades=school.get('grades'),
            distance_in_miles=school.get('distance'),
        )

    def _make_school_list_context(self, schools):
        return [
            self._make_school_context(school)
            for school in schools
        ] if schools else []

    def _make_external_link_list_context(self, address, assessor_parcel_number=None) -> list:
        # Real Estate Service
        link_list = self.get_external_service_link_list(address)
        if assessor_parcel_number:
            link_list += self.get_assessor_link_list(address, assessor_parcel_number)
        return link_list

    def _make_property_context(self, property):
        property_id = property.get('zpid')
        detail_link = reverse(
            'administrator:property-detail',
            kwargs={'info_origin': self.info_origin.value, 'property_id': property_id}
        )
        return model.Property(
            id=property_id,
            detail_link=detail_link,
            info_origin=self.info_origin.value,
            status=property.get('listingStatus'),
            full_address=property.get('address'),
            beds=property.get('bedrooms'),
            baths=property.get('bathrooms'),
            list_price=property.get('price'),
            list_date=_reformat_zillow_datetime(property.get('listingDateTime') or 0),
            type=property.get('propertyType'),
        )

    def _make_property_detail_context(self, property):
        property_id = property.get('zpid')
        detail_link = reverse(
            'administrator:property-detail',
            kwargs={'info_origin': self.info_origin.value, 'property_id': property_id}
        )
        reso_facts = property.get('resoFacts')
        schools = property.get('schools', [])
        products = property.get('products') or {}
        address = self._make_address_context(property)
        # TODO: 추가 검토 필요
        assessor_parcel_number = None
        external_links = self._make_external_link_list_context(address, assessor_parcel_number)
        sqft = property.get('livingAreaValue') or 0
        price_per_sqft = property.get('price', 0) / sqft if sqft > 0 else 0
        return model.PropertyDetail(
            id=property_id,
            detail_link=detail_link,
            info_origin=self.info_origin.value,
            status=property.get('homeStatus'),
            address=address,
            beds=property.get('bedrooms'),
            baths=property.get('bathrooms'),
            list_price=property.get('price'),
            list_date=_reformat_zillow_datetime(property.get('datePosted') or 0),
            estimate_price=property.get('zestimate'),
            images=self._make_property_image_list_context(property_id),
            type=property.get('homeType'),
            listing_id=property.get('listingId'),
            tags=property.get('tags'),
            garages=reso_facts.get('garageSpaces'),
            stories=reso_facts.get('storiesTotal'),
            year_built=reso_facts.get('yearBuilt'),
            sqft=sqft,
            lot_sqft=reso_facts.get('lotSize'),
            flags=property.get('flags'),
            community=reso_facts.get('communityFeatures'),
            products_brand_name=products.get('brand_name') if products else None,
            on_market_date=_reformat_zillow_datetime(property.get('onMarketDate') or 0),
            price_per_sqft=price_per_sqft,
            builder=reso_facts.get('builderName'),
            description=property.get('description'),
            data_source=self._make_data_source_context(property.get('listingProvider') or {}),
            hoa_fee=property.get('hoaFee'),
            property_history=self._make_property_history_list_context(property.get('priceHistory')),
            tax_history=self._make_tax_history_list_context(property.get('taxHistory')),
            schools=self._make_school_list_context(schools),
            external_links=external_links
        )
