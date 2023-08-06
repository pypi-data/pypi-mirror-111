from django import forms


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control mb-2"
            if hasattr(visible.field.widget, 'input_type'):
                if visible.field.widget.input_type == 'select':
                    visible.field.widget.attrs["class"] = "form-select mb-2"
                elif visible.field.widget.input_type == 'checkbox' or visible.field.widget.input_type == 'radio':
                    visible.field.widget.attrs["class"] = "form-control-check"

    def _user_select_label_from_instance(self, field):
        if self.fields.get(field):
            self.fields[field].label_from_instance = \
                lambda obj: "%s (%s)" % (obj.name, obj.email)

    def _product_select_label_from_instance(self, field):
        if self.fields.get(field):
            self.fields[field].label_from_instance = \
                lambda obj: "%s (%s)" % (obj.code, obj.full_address)


class BaseModelForm(BaseForm, forms.ModelForm):
    pass


class StartEndDateFormValidation:

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        if end_date and start_date and end_date <= start_date:
            raise forms.ValidationError("End date must be later than start date")
        return end_date


def form_max_min_validation(data, param_name):
    max_value = data.get(param_name + '_max')
    min_value = data.get(param_name + '_min')
    if max_value and min_value and float(min_value) > float(max_value):
        raise forms.ValidationError(
            "The " + param_name + " max value must be bigger than the " + param_name + " min value"
        )
