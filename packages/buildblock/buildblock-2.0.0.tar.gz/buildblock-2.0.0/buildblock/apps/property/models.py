from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.models import TimeStampedModel
from buildblock.apps.messaging.models import MessagingTemplates
from buildblock.apps.property.constants import PROPERTY_SUBSCRIPTION_FILTER_CHOICES


class PropertySubscriptionFilter(TimeStampedModel):
    title = models.CharField(_("Filter Title"), max_length=200)
    status = models.CharField(_("Status"),
                              choices=PROPERTY_SUBSCRIPTION_FILTER_CHOICES,
                              max_length=50)
    emails = ArrayField(models.EmailField(_("Emails")), default=list)
    filter = models.JSONField(_("Filter"), default=dict)
    last_sent = models.DateTimeField(_("Last Sent"), blank=True, null=True)
    messaging_template = models.ForeignKey(MessagingTemplates,
                                           on_delete=models.SET_NULL,
                                           blank=True, null=True)
