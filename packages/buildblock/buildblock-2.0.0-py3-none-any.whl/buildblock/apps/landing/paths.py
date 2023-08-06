def team_profile_image_path(instance, filename):
    return f"landing/team/{filename}"


def news_thumbnail_path(instance, filename):
    return f"landing/news/{instance.id}/{filename}"


def case_study_thumbnail_path(instance, filename):
    return f"landing/casestudy/{instance.id}/thumbnail/{filename}"


def case_study_photo_path(instance, filename):
    return f"landing/casestudy/{instance.case_product.id}/photos/{filename}"


def landing_document_path(instance, filename):
    return f"landing/document/{filename}"


def landing_carousel_path(instance, filename):
    return f"landing/event/carousel/{instance.id}/{filename}"


def landing_thin_banner_path(instance, filename):
    return f"landing/event/thin_banner/{instance.id}/{filename}"


def landing_popup_path(instance, filename):
    return f"landing/event/popup/{instance.id}/{filename}"
