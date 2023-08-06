import logging
from datetime import date

from dateutil.relativedelta import relativedelta
from django import template
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core import constants
from buildblock.apps.core.templatetags.base_tag import badge_format
from buildblock.apps.investment.models import InvestmentProduct
from buildblock.services.stripe import StripeService

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def get_management_roles():
    return dict((x, x) for x, y in constants.MANAGEMENT_ROLES)


@register.simple_tag
def get_payment_method():
    return {
        (constants.CASH, _('CASH')),
        (constants.CHECKS, _('CHECKS')),
    }


@register.simple_tag
def get_lease_status_badge_class(status):
    if status == constants.ACTIVE:
        return "badge-success"
    elif status == constants.PENDING:
        return "badge-warning"
    else:
        return "badge-light"


@register.simple_tag
def get_payment_status_badge_class(status):
    if status == constants.PENDING:
        return "badge-warning"
    elif status == constants.IN_PROGRESS:
        return "badge-secondary"
    elif status == constants.COMPLETE:
        return "badge-success"
    elif status == constants.FAILED:
        return "badge-danger"
    else:
        return "badge-light"


@register.simple_tag
def get_payment_transfer_status_badge_class(status):
    if status == constants.PENDING:
        return "badge-secondary"
    elif status == constants.COMPLETE:
        return "badge-success"
    elif status == constants.FAILED_NO_DESTINATION_ACCOUNT:
        return "badge-danger"
    elif status == constants.FAILED_OTHER_REASON:
        return "badge-warning"
    else:
        return "badge-light"


@register.simple_tag
def get_maintenance_status_badge_class(status):
    if status in constants.MAINTENANCE_STATUS_LIST.get('resolved'):
        return "badge-success-lighten"
    elif status in constants.MAINTENANCE_STATUS_LIST.get('unresolved'):
        return "badge-warning"
    else:
        return "badge-light"


@register.simple_tag
def get_maintenance_resolved_button_text(status):
    return "Change to Unresolved" \
        if status in constants.MAINTENANCE_STATUS_LIST.get('resolved') else "Change to Resolved"


@register.simple_tag
def get_payment_overdue_badge(payment):
    is_overdue = False
    if not payment.due_date:
        return ""
    if payment.status in [constants.IN_PROGRESS, constants.COMPLETE] and payment.payment_made_datetime:
        is_overdue = payment.due_date and payment.due_date < payment.payment_made_datetime.date()
    elif payment.status == constants.PENDING:
        is_overdue = payment.due_date and payment.due_date < date.today()
    return badge_format(style="badge badge-danger", text="OVERDUE") if is_overdue else ""


@register.simple_tag
def get_product_status_badge(product):
    if product.status == constants.IN_PROGRESS:
        construction_type = product.active_constructions[0].type if product.active_constructions else None
        badge_text = str(dict(constants.CONSTRUCTION_TYPE_CHOICES).get(construction_type, "CONSTRUCTION")).upper()
        return badge_format(style="primary-lighten", text=badge_text)
    elif product.status == constants.PENDING:
        return badge_format("secondary-lighten", "UNDER REVIEW")
    elif product.status == constants.ACTIVE:
        if product.num_people_under_lease >= product.max_num_people:
            return badge_format(style="warning-lighten", text="FULL")
        return badge_format(style="success-lighten", text="AVAILABLE")
    elif product.status == constants.INVESTMENT:
        return badge_format(style="info-lighten", text="INVESTMENT")
    else:
        return badge_format(style="secondary-lighten", text=product.status)


@register.simple_tag
def get_lease_status_badge(status):
    if status == constants.ACTIVE:
        return badge_format(style="success", text="ACTIVE")
    elif status == constants.PENDING:
        return badge_format(style="warning", text="READY")
    elif status == constants.COMPLETE:
        return badge_format(style="secondary", text="TERMINATED")
    else:
        return badge_format(style="info", text=status)


@register.simple_tag
def get_construction_status_badge(status):
    if status == constants.IN_PROGRESS:
        return badge_format(style="primary-lighten", text="IN PROGRESS")
    elif status == constants.PENDING:
        return badge_format(style="secondary-lighten", text="READY")
    elif status == constants.ACTIVE:
        return badge_format(style="warning-lighten", text="COMPLETE")
    else:
        return badge_format(style="secondary-lighten", text=status)


@register.simple_tag
def get_contract_template_type_badge(type):
    if type == constants.ATTACHMENT:
        return badge_format(style="primary-lighten", text="ATTACHMENT")
    elif type == constants.SIGNATURE:
        return badge_format(style="warning-lighten", text="SIGNATURE")
    else:
        return badge_format(style="secondary-lighten", text=type)


@register.filter
def get_contract_status_badge(value):
    if value == constants.SIG_REQUIRED_PENDING:
        return badge_format(style="success-lighten", text="Need to Sign")
    elif value == constants.SIG_REQUIRED_COMPLETE:
        return badge_format(style="light", text="Completed")
    elif value == constants.SIG_REQUIRED_WAITING:
        return badge_format(style="warning-lighten", text="Waiting for Others")
    elif value == constants.SIG_NOT_REQUIRED_COMPLETE:
        return badge_format(style="light", text="Read")
    elif value == constants.SIG_NOT_REQUIRED_PENDING:
        return badge_format(style="primary-lighten", text="Unread")
    else:
        return badge_format(style="light", text=value)


@register.simple_tag
def get_payment_status_title(payment, role):
    if payment.status == constants.COMPLETE:
        return "RECEIVED" if role == constants.OWNER_ROLE else "SENT"
    elif payment.status == constants.IN_PROGRESS:
        return "IN PROGRESS"
    elif payment.status == constants.PENDING:
        return "CHARGED"
    return payment.status.upper()


@register.simple_tag
def get_payment_description(payment):
    if not payment.due_date or payment.payment_type == constants.DEPOSIT:
        return payment.payment_type.title()
    description_date = payment.due_date
    if payment.payment_type == constants.UTILITY:
        description_date -= relativedelta(months=1)
    return (description_date.strftime('%B %Y ') + payment.payment_type).title()


@register.simple_tag
def get_payment_status_url(payment):
    base_url = reverse("management:payment-status")
    query_param = '?userId=' + str(payment.tenant.id) + \
                  '&productId=' + str(payment.product.id) + \
                  '&identifier=' + str(payment.identifier)
    return base_url + query_param


@register.simple_tag
def get_investment_product_title_by_id(id):
    return InvestmentProduct.objects.get(id=id).title \
        if id and id != 'all' else 'All'


@register.simple_tag
def generate_stripe_dashboard_url(account_id):
    try:
        dashboard_url = StripeService.create_dashboard_link(
            account_id=account_id
        )['url']
        logger.info(f'dashboard url has been generated: account_id-{account_id} url-{dashboard_url}')
    except Exception as err:
        logger.error(f'Error has occurred while creating dashboard link: {err}')
        dashboard_url = None
    return dashboard_url


@register.filter
def get_contracts_by_status(contracts, status):
    return [contract for contract in contracts if contract.status == status]


@register.filter
def get_contracts_by_type(contracts, type):
    return [contract for contract in contracts if contract.template_type == type]


@register.filter
def get_email_verified_icon(user):
    email_set = user.emailaddress_set.filter(email=user.email).first()
    verified = email_set.verified if email_set else False
    return mark_safe(
        "<span class=\"text-success\"><i class=\"dripicons-checkmark\"></i></span>"
        if verified else "<span class=\"text-danger\"><i class=\"dripicons-cross\"></i></span>"
    )


@register.simple_tag
def get_class_investment_workflow_status(status):
    if status == constants.COMPLETE:
        return "complete"
    elif status == constants.IN_PROGRESS:
        return "in_progress"
    else:
        return "pending"


@register.simple_tag
def get_icon_investment_step_status(status, counter):
    if status == constants.COMPLETE:
        icon = "<i class=\"mdi mdi-check\"></i>"
    else:
        icon = counter
    return mark_safe(icon)


@register.simple_tag
def get_icon_investment_user_todo(role):
    return mark_safe("<i class=\"mdi mdi-circle text-warning\"></i>" if role == constants.INVESTOR_ROLE else "")


@register.simple_tag
def get_class_investment_user_todo(role):
    return "d-flex justify-content-between" if role == constants.INVESTOR_ROLE else ""


@register.simple_tag
def get_investment_complete_stage_count(list):
    return sum(x.status == constants.COMPLETE for x in list)


@register.simple_tag
def get_one_step_percentage_mobile(list):
    return int((100 / (len(list) - 1)) if len(list) > 1 else 100)


@register.simple_tag
def get_period_months(data):
    if not hasattr(data, 'start_date') or not hasattr(data, 'end_date'):
        return 0
    return (data.end_date.year - data.start_date.year) * 12 + \
           (data.end_date.month - data.start_date.month)
