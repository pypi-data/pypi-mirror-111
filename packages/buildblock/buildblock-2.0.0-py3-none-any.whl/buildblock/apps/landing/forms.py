from django import forms

from buildblock.apps.landing.models import CaseStudy, Inquiry, News
from buildblock.forms import BaseForm, BaseModelForm


class InquiryForm(BaseModelForm):

    class Meta:
        model = Inquiry
        fields = ('survey_amount', 'survey_purpose', 'message', 'name', 'email', 'phone')
        widgets = {
          'message': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "survey_form bg-dark form-control mb-2"


class CaseStudyForm(BaseModelForm):

    class Meta:
        model = CaseStudy
        fields = '__all__'


class NewsForm(BaseModelForm):

    class Meta:
        model = News
        fields = '__all__'


class ContactEmailForm(BaseForm):
    name = forms.CharField()
    phone = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
