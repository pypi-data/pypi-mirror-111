from django import forms

from buildblock.apps.core.constants import MESSAGING_TEMPLATE_CATEGORY_CHOICES
from buildblock.apps.messaging.models import MessagingTemplates
from buildblock.forms import BaseModelForm


class TemplateForm(BaseModelForm):

    class Meta:
        model = MessagingTemplates
        fields = '__all__'


class MessagingCreateValForm(forms.Form):
    title = forms.CharField()
    category = forms.ChoiceField(choices=MESSAGING_TEMPLATE_CATEGORY_CHOICES)
    is_active = forms.BooleanField(required=False)
    description = forms.CharField(required=False)


class MessagingSendValForm(forms.Form):
    message_title = forms.CharField()
    sender_id = forms.IntegerField()
    receiver_id = forms.IntegerField()
