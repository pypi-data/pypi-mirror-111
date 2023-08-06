from django import template

from buildblock.apps.construction.models import Worker, WorkType
from buildblock.apps.core import constants
from buildblock.apps.core.templatetags.base_tag import badge_format

register = template.Library()


@register.simple_tag
def get_picture_status_check_class(pictures, status):
    for picture in pictures:
        if picture.status == status:
            return "dripicons-checkmark text-success"
    return "dripicons-dot text-muted"


@register.simple_tag
def get_picture_status_badge(status):
    if status == constants.BEFORE:
        return badge_format(style="light", text="BEFORE")
    elif status == constants.IN_PROGRESS:
        return badge_format(style="warning", text="IN PROGRESS")
    elif status == constants.AFTER:
        return badge_format(style="success", text="AFTER")
    else:
        return badge_format(style="light", text=status)


@register.simple_tag
def get_construction_status_badge(status):
    if status == constants.IN_PROGRESS:
        return badge_format(style="warning", text="IN PROGRESS")
    elif status == constants.PENDING:
        return badge_format(style="dark", text="READY")
    elif status == constants.ACTIVE:
        return badge_format(style="light", text="COMPLETE")
    else:
        return badge_format(style="secondary", text=status)


@register.simple_tag
def get_construction_type_badge(type):
    if type == constants.FIX_AND_FLIP:
        return badge_format(style="info", text="FIX AND FLIP")
    elif type == constants.ADU:
        return badge_format(style="info-lighten", text="ADU")
    else:
        return badge_format(style="secondary", text=type)


@register.simple_tag
def get_worker_speciality_list():
    return constants.WORKER_SPECIALITY_CHOICES


@register.simple_tag
def get_worker_role_list():
    return constants.WORKER_ROLE_CHOICES


@register.simple_tag
def get_worker_role_badge(role):
    if role == constants.WORKER:
        return badge_format(style="light", text="WORKER")
    elif role == constants.LEADER:
        return badge_format(style="danger", text="LEADER")
    elif role == constants.CONTRACTOR:
        return badge_format(style="info", text="CONTRACTOR")
    else:
        return badge_format(style="light", text=role)


@register.simple_tag
def get_worker_speciality_shorttitle(speciality):
    if speciality == constants.NORMAL_WORKER:
        return "NORMAL WORKER"
    if speciality == constants.DEMOLITION_WORKER:
        return "DEMOLITION"
    if speciality == constants.ELECTRIC_WORKER:
        return "ELECTRIC"
    if speciality == constants.PAINTER:
        return "PAINTER"
    if speciality == constants.PLUMBER:
        return "PLUMBER"
    if speciality == constants.CARPENTER:
        return "CARPENTER"
    if speciality == constants.CLEANER:
        return "CLEANER"
    if speciality == constants.SPECIAL_WORKER:
        return "SPECIAL"
    else:
        return "NONE"


@register.simple_tag
def get_expense_category_list():
    return constants.EXPENSE_CATEGORY_CHOICES


@register.simple_tag
def get_outsourcing_contract_included_list():
    return constants.OUTSOURCING_INCLUDED_CHOICES


@register.simple_tag
def get_worker_list():
    return Worker.objects.all()


@register.simple_tag
def get_work_type_list():
    return WorkType.objects.all()


@register.simple_tag
def get_construction_method_display(method):
    if method == constants.DIRECT_MANAGEMENT:
        return "Direct Management"
    if method == constants.SEPARATE_ORDER:
        return "Separate Order"
    if method == constants.INTEGRATED_ORDER:
        return "Integrated Order"
    else:
        return "NONE"
