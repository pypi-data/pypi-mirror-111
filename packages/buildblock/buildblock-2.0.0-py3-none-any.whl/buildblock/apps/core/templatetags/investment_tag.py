from django import template

from buildblock.apps.administrator.views.investment import get_investment_stage_list

register = template.Library()


@register.simple_tag
def get_investment_stage_list_tag(investment):
    return get_investment_stage_list(investment)
