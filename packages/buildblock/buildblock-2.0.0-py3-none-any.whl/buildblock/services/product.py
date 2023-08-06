from buildblock.apps.product.models import Product, ProductZoneSchema
from buildblock.helper import db_update


class ProductService:
    """High level interface for dealing with the Product database."""

    @classmethod
    def update_product_status(cls, product_code, new_status):
        product = cls.get_product_by_product_code(product_code)
        db_update(product, dict(status=new_status))

    @classmethod
    def get_product_by_product_code(cls, product_code):
        return Product.objects.get(code=product_code)

    @classmethod
    def get_product_by_id(cls, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None

    @classmethod
    def add_zone(cls, product_code, zone_name):
        product = cls.get_product_by_product_code(product_code)
        if not product.zone:
            product.zone = []
        zone_ids = [zone['id'] for zone in product.zone]
        new_zone_id = (max(zone_ids)+1) if product.zone else 1
        zone = ProductZoneSchema().load({
            "id": new_zone_id,
            "name": zone_name
        })
        product.zone.append(zone)
        db_update(product)

    @classmethod
    def edit_zone(cls, product_code, zone_id, zone_name):
        product = cls.get_product_by_product_code(product_code)
        for zone in product.zone:
            if int(zone['id']) == int(zone_id):
                zone['name'] = zone_name
                break
        db_update(product)

    @classmethod
    def delete_zone(cls, product_code, zone_id):
        product = cls.get_product_by_product_code(product_code)
        new_zones = []
        for zone in product.zone:
            if int(zone['id']) == int(zone_id):
                continue
            new_zones.append(zone)
        product.zone = new_zones
        db_update(product)
