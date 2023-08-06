from django.db import models
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import AGREEMENTS_TYPE, LANGUAGE_CHOICES, SERVICE_TYPE
from buildblock.apps.core.models import TimeStampedModel


class Faq(TimeStampedModel):

    num = models.PositiveIntegerField(_("Number"), default=1)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    question = models.TextField(_("Question"))
    answer = models.TextField(_("Answer"))


class Agreement(TimeStampedModel):

    service_type = models.CharField(_("Service Type"), max_length=100, choices=SERVICE_TYPE)
    agreement_type = models.CharField(_("Agreements Type"), max_length=100, choices=AGREEMENTS_TYPE)
    language = models.CharField(_("Language"), max_length=10, choices=LANGUAGE_CHOICES)
    title = models.CharField(_("Title"), max_length=100)
    content = models.TextField(_("Content"))
