from typing import List, NamedTuple, Optional


class Amenities(NamedTuple):
    heater: Optional[str]
    cooling: Optional[str]


class Zone(NamedTuple):
    id: int
    name: str


class ProductImage(NamedTuple):
    title: str
    original_image_url: str
    thumbnail_image_url: str


class Product(NamedTuple):
    """Remote representation of how the product table looks like in the database.
    Instead of using the database object itself, this way we can tailor the representation"""
    id: int
    code: str
    description: str
    full_address: str
    main_image_url: str
    plan_image_url: Optional[str]
    max_num_people: int
    num_people_under_lease: int
    rent_under_lease: int
    deposit_under_lease: int
    status: str
    added_at: str
    num_bedroom: int
    num_bathroom: int
    num_parking: int
    map_url: str
    property_type: str
    sqft: float
    lot_sqft: float
    washer_dryer: str
    allowed_pets: str
    built_year: int
    amenities: Amenities
    product_images: List
    owners: List
    agency: Optional[str]
    active_constructions: List = []


class ConstructionWork(NamedTuple):
    id: int
    title: str
    type: str
    type_id: int
    zone_ids: str
    zone_list: Optional[list]
    work_date: str
    work_date_index: int
    pictures: List
    construction_id: int


class ConstructionPicture(NamedTuple):
    id: int
    image_url: str
    thumb_url: str
    work_id: int
    work_title: str
    status: str
    description: str
    created_at: str


class Construction(NamedTuple):
    id: int
    type: str
    method: str
    status: str
    title: str
    full_address: str
    main_image_url: str
    main_thumb_url: str
    plan_image_url: str
    product_code: str
    budget: Optional[float]
    period: Optional[int]
    description: Optional[str]
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    works: Optional[list] = None
    zones: Optional[list] = None
    constructor: Optional[list] = None
