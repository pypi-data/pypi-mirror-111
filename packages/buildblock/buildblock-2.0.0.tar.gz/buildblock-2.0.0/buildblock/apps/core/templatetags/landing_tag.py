from django import template

from buildblock.apps.core.constants import ENGLISH, KOREAN
from buildblock.apps.core.templatetags.base_tag import badge_format
from buildblock.apps.landing import constants

register = template.Library()


CASE_STUDY_STATUS_TEXT_MAPPING = {
    constants.PENDING: {
        ENGLISH: 'PENDING',
        KOREAN: '모집예정'
    },
    constants.OPEN: {
        ENGLISH: 'OPEN',
        KOREAN: '모집중'
    },
    constants.ACTIVE: {
        ENGLISH: 'ACTIVE',
        KOREAN: '진행중'
    },
    constants.COMPLETE: {
        ENGLISH: 'COMPLETE',
        KOREAN: '투자완료'
    }
}

NEWS_CATEGORY_BADGE = {
    constants.NEWS: "dark",
    constants.BLOG: "info",
    constants.NOTICE: "light",
    constants.EVENT: "warning",
    constants.INTERVIEW: "success",
}


@register.simple_tag
def get_news_category_badge(news_category):
    return badge_format(
        style=NEWS_CATEGORY_BADGE.get(news_category, "info"),
        text=news_category
    )


@register.simple_tag
def get_case_study_status_badge(status, language):
    status_mapping = CASE_STUDY_STATUS_TEXT_MAPPING.get(status, {})
    text = status_mapping.get(language)
    assert text, 'Text is not exist.'
    if status == constants.PENDING:
        return badge_format(style="light", text=text)
    if status == constants.OPEN:
        return badge_format(style="success", text=text)
    elif status == constants.ACTIVE:
        return badge_format(style="primary", text=text)
    elif status == constants.COMPLETE:
        return badge_format(style="dark", text=text)


@register.simple_tag
def get_case_study_type_list():
    return constants.CASE_STUDY_CATEGORY
