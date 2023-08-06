from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import ETC, MESSAGING_TEMPLATE_CATEGORY_CHOICES
from buildblock.apps.core.models import HistoricalRecordModel
from buildblock.apps.users.models import User


def get_default_creator():
    return User.objects.filter(is_superuser=True).first().id


class MessagingTemplates(HistoricalRecordModel):
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name="messaging_template_creator",
                                default=get_default_creator)
    title = models.CharField(_("Title"), max_length=120)
    category = models.CharField(_("Category"), max_length=50, choices=MESSAGING_TEMPLATE_CATEGORY_CHOICES, default=ETC)
    # This field controls whether this email can be sent out to people
    is_active = models.BooleanField(_("Is Active"), default=False)
    description = models.TextField(_("Description"), blank=True)


class MessagingRequests(HistoricalRecordModel):
    title = models.CharField(_("Title"), max_length=200)
    content = models.TextField(_("Content"))
    sender = models.EmailField(_("Sender"), max_length=254)
    receivers = ArrayField(models.EmailField(_("receiver"), max_length=254))
    sent_at = models.DateTimeField(_("Sent at Date"), null=True, blank=True)
