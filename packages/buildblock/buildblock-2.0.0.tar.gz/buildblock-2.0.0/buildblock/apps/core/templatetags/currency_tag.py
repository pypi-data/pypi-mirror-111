from decimal import Decimal

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.translation import get_language

from buildblock.apps.core.constants import DISPLAY_UNIT_SYMBOL

register = template.Library()


@register.filter
def unit_floatformat(value, unit):
    ''' Decimal by Currency Unit (USD: 2, else: 0) '''
    return round(Decimal(value), 2 if unit == 'USD' else 0)


@register.simple_tag
def get_money_string(amount, unit, exchange_rate):
    if not amount:
        return "0"

    unit = get_display_unit(unit)
    rate = 0
    for x in exchange_rate:
        if unit == x.unit:
            rate = x.rate
            break
    exchanged_amount = rate * Decimal(amount)

    if unit == "KRW" and exchanged_amount >= 10000:
        # 120,000,000 -> 1억 2,000만 원
        #  75,000,000 -> 7천 500만 원
        #      35,000 -> 3만 원
        result = ""
        amount_in_hundered_millions = int(exchanged_amount // 100000000)
        if amount_in_hundered_millions:
            result += str(amount_in_hundered_millions) + "억"

        exchanged_amount %= 100000000
        amount_in_ten_thousands = int(exchanged_amount // 10000)
        if amount_in_ten_thousands:
            result += " " + str(amount_in_ten_thousands) + "만"

        return result.strip()

    return intcomma(round(exchanged_amount, 0))


@register.simple_tag
def get_display_unit(unit=""):
    if unit:
        return unit
    if get_language() == "en":
        return "USD"
    if get_language() == "ko":
        return "KRW"
    return ""


@register.simple_tag
def get_display_unit_symbol(unit=""):
    display_unit = get_display_unit(unit)
    return DISPLAY_UNIT_SYMBOL.get(display_unit, "")
