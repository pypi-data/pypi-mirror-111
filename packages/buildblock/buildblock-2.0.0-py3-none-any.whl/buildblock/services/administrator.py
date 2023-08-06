from buildblock.apps.landing.models import CaseStudy, CaseStudyPhoto, CaseStudyVideo
from buildblock.helper import db_update


class LandingService:
    @classmethod
    def get_case_study(cls, id):
        return CaseStudy.objects.get(id=id)

    @classmethod
    def create_case_study(cls, data_dict: dict, thumbnail):
        return CaseStudy.objects.create(
            **data_dict,
            thumbnail=thumbnail
        )

    @classmethod
    def edit_case_study(cls, case_study_id, data_dict: dict, thumbnail, delete_thumbnail):
        case_study = cls.get_case_study(case_study_id)
        if thumbnail:
            case_study.thumbnail = thumbnail
        elif delete_thumbnail:
            case_study.thumbnail.delete()
        db_update(case_study, data_dict)
        return case_study

    @classmethod
    def get_case_study_photo(cls, id):
        return CaseStudyPhoto.objects.get(id=id)

    @classmethod
    def get_case_study_photos_by_product_id(cls, case_study_id):
        return CaseStudyPhoto.objects.filter(case_product__id=case_study_id)

    @classmethod
    def create_case_study_photo(cls, case_study_id, status, photo):
        CaseStudyPhoto.objects.create(
            case_product_id=case_study_id,
            status=status,
            photo=photo
        )

    @classmethod
    def delete_case_study_photo(cls, id):
        cls.get_case_study_photo(id).delete()

    @classmethod
    def get_case_study_video(cls, id):
        return CaseStudyVideo.objects.get(id=id)

    @classmethod
    def get_case_study_videos_by_product_id(cls, case_study_id):
        return CaseStudyVideo.objects.filter(case_product__id=case_study_id)

    @classmethod
    def create_case_study_video(cls, case_study_id, url):
        CaseStudyVideo.objects.create(
            case_product_id=case_study_id,
            url=url
        )

    @classmethod
    def delete_case_study_video(cls, id):
        cls.get_case_study_video(id).delete()
