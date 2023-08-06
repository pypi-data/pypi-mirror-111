import copy

from django import forms

from buildblock.apps.construction.models import Construction, ConstructionReport
from buildblock.apps.core.constants import EXPENSE_CATEGORY_CHOICES
from buildblock.apps.product.models import Product
from buildblock.forms import BaseModelForm, StartEndDateFormValidation


class ConstructionBaseForm(BaseModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get('construction'):
            self.fields['construction'].label_from_instance = lambda obj: obj.title
        if self.fields.get('construction_work'):
            self.fields['construction_work'].label_from_instance = lambda obj: obj.title
        if self.fields.get('type'):
            self.fields['type'].label_from_instance = lambda obj: obj.title
        if self.fields.get('product'):
            self.fields['product'].label_from_instance = lambda obj: obj.full_address
        if self.fields.get('constructor'):
            self.fields['constructor'].label_from_instance = \
                lambda obj: "%s (%s)" % (obj.name, obj.email)


class ConstructionForm(ConstructionBaseForm, StartEndDateFormValidation):
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = Construction
        fields = "__all__"


class ProductForm(BaseModelForm):
    class Meta:
        model = Product
        fields = [
            'main_image',
            'plan_image',
            'address_1',
            'address_2',
            'city',
            'state',
            'zip_code',
            'property_type',
            'built_year',
            'sqft',
            'num_people',
            'num_bedroom',
            'num_bathroom',
            'num_parking',
            'washer_dryer',
        ]


class ConstructionUpdateForm(ConstructionForm):
    class Meta:
        model = Construction
        fields = (
            'type',
            'constructor',
            'status',
            'method',
            'title',
            'budget',
            'start_date',
            'end_date',
            'description'
        )

    def __init__(self, *args, **kwargs):
        self.product = kwargs['instance'].product
        product_kwargs = copy.deepcopy(kwargs)
        product_kwargs['instance'] = product_kwargs['instance'].product
        self.product = ProductForm(*args, **product_kwargs)

        super().__init__(*args, **kwargs)

        self.fields.update(self.product.fields)
        self.initial.update(self.product.initial)

    def save(self, *args, **kwargs):
        # save both forms
        self.product.save(*args, **kwargs)
        return super().save(*args, **kwargs)


class ValidationForm(forms.Form):
    return_url = forms.CharField()


class AddWorkValForm(ValidationForm):
    construction_id = forms.IntegerField()
    title = forms.CharField()
    work_type = forms.IntegerField()


class EditWorkValForm(ValidationForm):
    work_id = forms.IntegerField()
    title = forms.CharField()
    work_type = forms.IntegerField()


class AddWorkDateValForm(ValidationForm):
    work_id = forms.IntegerField()
    work_date = forms.DateField()


class AddWorkerValForm(ValidationForm):
    name = forms.CharField()
    phone = forms.CharField(required=False)
    role = forms.CharField()


class EditWorkerValForm(ValidationForm):
    worker_id = forms.IntegerField()
    name = forms.CharField()
    phone = forms.CharField(required=False)
    role = forms.CharField()


class ExpenseValForm(ValidationForm):
    amount = forms.IntegerField(min_value=1)
    date = forms.DateField()
    attachment = forms.FileField(required=False)
    description = forms.CharField(required=False)


class PersonnelExpenseValForm(ExpenseValForm):
    work_hours = forms.IntegerField(min_value=1)


class AddPersonnelExpenseValForm(PersonnelExpenseValForm):
    construction_id = forms.IntegerField()
    worker_id = forms.IntegerField()


class UpdatePersonnelExpenseValForm(PersonnelExpenseValForm):
    expense_id = forms.IntegerField()


class ConstructionExpenseValForm(ExpenseValForm):
    category = forms.ChoiceField(choices=EXPENSE_CATEGORY_CHOICES)
    item = forms.CharField()
    quantity = forms.IntegerField(min_value=0)


class AddConstructionExpenseValForm(ConstructionExpenseValForm):
    construction_id = forms.IntegerField()


class UpdateConstructionExpenseValForm(ConstructionExpenseValForm):
    expense_id = forms.IntegerField()


class OutsourcingContractValForm(ValidationForm):
    contractor_id = forms.IntegerField()
    title = forms.CharField()
    amount = forms.IntegerField(min_value=1)
    start_date = forms.DateField()
    end_date = forms.DateField()
    attachment = forms.FileField(required=False)


class AddOutsourcingContractValForm(OutsourcingContractValForm):
    construction_id = forms.IntegerField()


class UpdateOutsourcingContractValForm(OutsourcingContractValForm):
    contract_id = forms.IntegerField()


class OutsourcingExpenseValForm(ExpenseValForm):
    title = forms.CharField()
    paid_amount = forms.IntegerField(required=False, min_value=0)
    payment_date = forms.DateField(required=False)


class AddOutsourcingExpenseValForm(OutsourcingExpenseValForm):
    contract_id = forms.IntegerField()


class UpdateOutsourcingExpenseValForm(OutsourcingExpenseValForm):
    expense_id = forms.IntegerField()


class ReportForm(BaseModelForm):
    class Meta:
        model = ConstructionReport
        fields = "__all__"


class AddWeeklyReportValForm(forms.Form):
    construction_id = forms.IntegerField()
    end_date = forms.DateField()
