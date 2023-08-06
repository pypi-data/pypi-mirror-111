from datetime import datetime
from urllib.parse import urlencode

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from buildblock.apps.administrator.models import Agreement
from buildblock.apps.users.models import User
from buildblock.utils import (
    change_dollar_to_won,
    convert_feet_to_miles,
    convert_second_to_minute,
    safe_money_read_from_db,
    sum_field
)

register = template.Library()


@register.filter
def badge_format(style="success-lighten", text=""):
    return mark_safe("<span class=\"badge badge-" + style + "\">" + text + "</span>") \
        if text else mark_safe("")


@register.filter
def index(List, i):
    return List[int(i)]


@register.filter
def filter_sum_field(queryset, field):
    return sum_field(queryset, field)


@register.filter
def ord(n):
    if isinstance(n, str):
        return n
    return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


@register.simple_tag
def get_intersection_set(set1, set2):
    return list(set(set1) & set(set2))


@register.filter
def filter_safe_money_read_from_db(n):
    return safe_money_read_from_db(n)


@register.filter
def filter_change_dollar_to_won(n):
    return change_dollar_to_won(n)


@register.filter
def filter_change_dollar_to_100_m_won(n):
    return change_dollar_to_won(n)/10**8


@register.filter
def filter_convert_feet_to_miles(n):
    return convert_feet_to_miles(n)


@register.filter
def filter_convert_second_to_minute(n):
    return convert_second_to_minute(n)


@register.simple_tag(takes_context=True)
def get_param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    d.update(kwargs)
    return urlencode(d)


@register.simple_tag
def get_user_name_by_id(id):
    try:
        return User.objects.get(id=id).name
    except User.DoesNotExist:
        return "No Data"


@register.simple_tag
def get_agreement_by_type_language(service_type, agreement_type, language):
    return Agreement.objects.filter(
        service_type=service_type,
        agreement_type=agreement_type,
        language=language
    ).first()


@register.filter
def d_day_format(days):
    if days > 0:
        return "D-" + str(days)
    elif days < 0:
        return str(abs(days)) + " days overdue"
    else:
        return "D-Day"


@stringfilter
def parse_date(date_string):
    """
    Return a datetime corresponding to date_string, parsed according to format.
    For example, to re-display a date string in another format::
        {{ (timestamp)|parse_date|date:"(dateformat)" }}

        >> input: {{ 1567768207.260894|parse_date|date:"N j. Y. P" }}
        >> output: Sept. 6. 2019. 8:10 p.m.

    """
    try:
        return datetime.fromtimestamp(float(date_string))
    except ValueError:
        return None


register.filter(parse_date)
