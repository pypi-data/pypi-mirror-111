from typing import List, NamedTuple, Optional


class Coordinate(NamedTuple):
    lng: float
    lat: float


class Address(NamedTuple):
    full: str
    state: str
    line: str
    city: str
    postal_code: str
    coordinate: Coordinate
    county: str
    fips_code: str                      # https://en.wikipedia.org/wiki/FIPS_county_code
    country: Optional[str]
    city_slug_id: Optional[str]
    direction_from_offices: List


class Direction(NamedTuple):
    destination: str
    origin: str
    distance: int   # Feet
    duration: int   # Seconds
    map_url: str
    embed_src: str


class DataSource(NamedTuple):
    name: str
    description: str
    group: str
    phone: str
    url: str


class School(NamedTuple):
    rating: int
    assigned: bool
    name: str
    funding_type: str
    parent_rating: int
    student_teacher_ratio: float
    education_levels: List
    link: str
    grades: List
    distance_in_miles: float


class Property(NamedTuple):
    id: str
    detail_link: str
    info_origin: str
    status: str
    full_address: str
    beds: Optional[float]
    baths: Optional[float]
    list_price: int
    list_date: str
    type: str


class PropertyDetail(NamedTuple):
    id: str
    detail_link: str
    info_origin: str
    status: str
    address: Address
    beds: Optional[float]
    baths: Optional[float]
    list_price: int
    list_date: str
    estimate_price: int
    images: List
    type: str
    listing_id: str                         # Data Source Listing ID와 차이가 있음
    tags: List                              # Property 특징
    garages: Optional[float]
    stories: Optional[float]
    year_built: Optional[int]
    sqft: Optional[int]
    lot_sqft: Optional[int]
    flags: List                             # Property 상황 체크
    community: Optional[str]                # TODO: 확인 되지 않음
    products_brand_name: str                # cf. basic_opt_in
    on_market_date: Optional[str]
    price_per_sqft: Optional[int]
    builder: Optional[str]
    description: str
    data_source: DataSource         # Data 출처 cf. mls
    hoa_fee: int                    # https://www.investopedia.com/terms/h/hoa.asp
    property_history: List          # Property 리스팅 등의 기록
    tax_history: List               # 세금 정보와 자산 평가 정보
    schools: List                   # 인근지역 학교 정보
    external_links: List


class PropertyExternalServiceLink(NamedTuple):
    title: str
    href: str


class PropertyHistory(NamedTuple):
    event_name: str
    date: str
    source_name: str
    price: int
    change_rate: float


class PropertyTaxHistory(NamedTuple):
    tax: int
    year: int
    assessment_value: int
