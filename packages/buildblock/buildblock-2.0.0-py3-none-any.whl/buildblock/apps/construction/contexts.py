from operator import itemgetter

from buildblock.models.product import Construction, ConstructionPicture, ConstructionWork, Zone
from buildblock.utils import safe_money_read_from_db


class ConstructionContext:
    def _make_construction_context(self, construction):
        product = construction.product
        return Construction(
            id=construction.id,
            type=construction.type,
            method=construction.method,
            status=construction.status,
            title=construction.title,
            budget=safe_money_read_from_db(construction.budget),
            period=round((construction.end_date - construction.start_date).days / 7),
            description=construction.description,
            start_date=construction.start_date,
            end_date=construction.end_date,
            full_address=product.full_address,
            main_image_url=product.main_image.url,
            main_thumb_url=product.main_thumbnail_image_url,
            plan_image_url=product.plan_image.url if product.plan_image else None,
            product_code=product.code,
            works=self._make_all_construction_works_context(construction.work_process),
            zones=self._make_all_zones_context(product.zone),
            constructor=construction.constructor
        )

    def _make_all_constructions_context(self, constructions):
        return [
            self._make_construction_context(construction)
            for construction in constructions
        ]

    def _make_construction_work_context(self, work, report_date=None):
        product_zone = self._make_all_zones_context(
            work.construction.product.zone
        )
        zone_list = [
            zone for zone in product_zone
            if int(zone.id) in work.zone_ids
        ]
        work_date_index = (sorted(work.work_date).index(report_date) + 1) if report_date else None
        return ConstructionWork(
            id=work.id,
            title=work.title,
            type=work.type.title,
            type_id=work.type.id,
            zone_ids=work.zone_ids,
            zone_list=zone_list,
            work_date=work.work_date,
            work_date_index=work_date_index,
            construction_id=work.construction.id,
            pictures=self._make_all_work_pictures_context(work),
        )

    def _make_all_construction_works_context(self, works, report_date=None):
        return [
            self._make_construction_work_context(work, report_date)
            for work in works.all()
        ]

    def _make_construction_picture_context(self, construction_picture):
        return ConstructionPicture(
            id=construction_picture.id,
            image_url=construction_picture.picture.url,
            thumb_url=construction_picture.construction_picture_thumb_url,
            work_id=construction_picture.construction_work.id,
            work_title=construction_picture.construction_work.title,
            status=construction_picture.status,
            description=construction_picture.description,
            created_at=construction_picture.created_at,
        )

    def _make_all_work_pictures_context(self, construction_work):
        return [
            self._make_construction_picture_context(construction_picture)
            for construction_picture in construction_work.work_picture.all()
        ]

    def _make_zone_context(self, zone):
        return Zone(
            id=zone["id"],
            name=zone["name"],
        )

    def _make_all_zones_context(self, zones):
        zone_list = sorted(zones, key=itemgetter('name'))
        return [
            self._make_zone_context(zone)
            for zone in zone_list
        ]
