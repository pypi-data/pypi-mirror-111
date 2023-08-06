from django.utils.translation import ugettext_lazy as _

NEWS = 'NEWS'
BLOG = 'BLOG'
NOTICE = 'NOTICE'
EVENT = 'EVENT'
INTERVIEW = "INTERVIEW"
CAREER = "CAREER"
PENDING = 'PENDING'
OPEN = 'OPEN'
ACTIVE = 'ACTIVE'
COMPLETE = 'COMPLETE'

# News Category
LANDING_NEWS_CATEGORY = (
    (NEWS, _("News")),
    (BLOG, _("Blog")),
    (NOTICE, _("Notice")),
    (EVENT, _("Event")),
    (INTERVIEW, _("Interview")),
    (CAREER, _("Career"))
)

# Case Study Category
CASE_STUDY_CATEGORY = (
    (PENDING, _('Pending')),
    (OPEN, _('Open')),
    (ACTIVE, _('Active')),
    (COMPLETE, _('Complete')),
)

# Inquiry Choices
SURVEY_AMOUNT_CHOICE = (
    ('less_than_100000', _('less than $100,000')),
    ('100000_500000', _('$100,000~$500,000')),
    ('500000_1M', _('$500,000~$1M')),
    ('more_than_1M', _('more than $1M')),
    ('undecided', _('undecided'))
)

SURVEY_PURPOSE_CHOICE = (
    ('long-term', _('long-term investment')),
    ('short-term', _('short-term investment')),
    ('migration', _('investment migration')),
    ('undecided', _('undecided'))
)