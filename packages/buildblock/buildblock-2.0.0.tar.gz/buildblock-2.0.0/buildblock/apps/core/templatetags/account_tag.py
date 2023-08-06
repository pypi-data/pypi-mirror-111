import logging

from django import template

from buildblock.apps.core import constants

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def get_service_user_roles():
    return dict((x, x) for x, y in constants.USER_ROLES)


@register.simple_tag
def get_user_role_title(role):
    return dict(constants.USER_ROLES).get(role, 'User')


@register.simple_tag
def has_all_roles(service_role_set, user_roles):
    return service_role_set.issubset(set(user_roles))
