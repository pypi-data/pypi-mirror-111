import hashlib
import re
from datetime import timedelta

import langdetect
from django.db.models import Sum
from django.http import JsonResponse
from easy_thumbnails.files import get_thumbnailer
from langdetect.lang_detect_exception import LangDetectException

from buildblock.apps.core.constants import COMPLETE, CREDIT_CARD, CREDIT_CARD_CHARGE_RATE, DEBIT_CARD, IN_PROGRESS
from buildblock.errors import RequiredPostDataError


def calculate_payment_fee(payment_method, amount):
    if payment_method in [CREDIT_CARD, DEBIT_CARD]:
        return int(amount * CREDIT_CARD_CHARGE_RATE)
    else:
        return 0


def hash_sha256(value):
    if isinstance(value, str):
        value = value.encode()
    return hashlib.sha256(value).hexdigest()


def safe_money_read_from_db(value):
    if value:
        return int(value)/100
    return 0


def safe_money_save_from_dollar(value):
    if value:
        return int(value * 100)
    return 0


def change_dollar_to_won(value):
    if value:
        # 실시간으로 가져오지 않고 고정값을 사용 (현재 적용 환율 : 1150원)
        return value*11.5
    return 0


def convert_meters_to_feet(value):
    if value:
        return int(value * 3.28084)
    return 0


def convert_feet_to_miles(value):
    if value:
        return round(int(value) / 5280, 1)
    return 0


def convert_second_to_minute(value):
    if value:
        return int(int(value) / 60)
    return 0


def sum_field(query_set, field_name):
    return query_set.aggregate(sum=Sum(field_name))['sum'] or 0


def detect_language(text):
    try:
        language = langdetect.detect(text)
    except LangDetectException:
        language = None
    return language


def get_required_post_data(request, data_name):
    request_data = request.POST.get(data_name) or request.FILES.get(data_name)
    if not request_data:
        raise RequiredPostDataError
    return request_data


def get_input_dict_data(query_dict, param):
    dictionary = {}
    regex = re.compile('%s\[([\w\d_]+)\]' % param)  # noqa
    for key, value in query_dict.items():
        match = regex.match(key)
        if match:
            inner_key = match.group(1)
            dictionary[inner_key] = value
    return dictionary


def daterange(start_date, end_date):
    return [
        start_date + timedelta(n)
        for n in range(int((end_date - start_date).days) + 1)
    ]


def get_investment_progress_percentage(steps):
    progress_steps_count = steps.filter(status=COMPLETE).count() + \
                           steps.filter(status=IN_PROGRESS).count() * 0.5
    return int(progress_steps_count / steps.count() * 100)


def set_initial_value_field(initial, field, value):
    if value:
        initial[field] = value
    return initial


def json_error_response(message):
    return JsonResponse({"error": message})


def make_thumbnail_url(image):
    try:
        url = get_thumbnailer(image).get_thumbnail({'size': (600, 400), 'crop': True}).url
    except Exception:
        return ''
    else:
        return url
