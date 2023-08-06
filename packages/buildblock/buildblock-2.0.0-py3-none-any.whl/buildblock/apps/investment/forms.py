from django import forms

from buildblock.apps.investment.models import (
    ContractTemplate,
    Investment,
    InvestmentContract,
    InvestmentProduct,
    InvestmentStep
)
from buildblock.forms import BaseModelForm, StartEndDateFormValidation


class InvestmentProductForm(BaseModelForm, StartEndDateFormValidation):
    start_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    end_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)

    class Meta:
        model = InvestmentProduct
        fields = "__all__"


class InvestmentForm(BaseModelForm):
    class Meta:
        model = Investment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['investment_product'].label_from_instance = lambda obj: obj.title
        self.fields['user'].label_from_instance = lambda obj: "%s (%s)" % (obj.name, obj.email)
        self.fields['amount'].label_suffix = " (Unit: ₵ent)"

    def save(self, commit=True):
        investment = super().save(commit=commit)

        # Check whether Investment Steps are created
        if InvestmentStep.objects.filter(investment=investment):
            return investment

        # Step List of Workflow Template check and Create Steps
        if hasattr(investment, 'workflow_template') and investment.workflow_template.step_list:
            for step in investment.workflow_template.step_list:
                step_data = {
                    key: value for key, value in step.items()
                    if key in ['title', 'description', 'actor_role', 'metadata']
                }
                InvestmentStep.objects.create(
                    investment=investment,
                    stage_id=step['stage'],
                    **step_data
                )

        return investment


class InvestmentContractForm(BaseModelForm):
    class Meta:
        model = InvestmentContract
        fields = ['title', 'document_file', 'status', 'due_date', 'records']
        # TODO 'due_date'는 사인이 필요한 템플릿에서만 나오도록

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get('investment'):
            self.fields['investment'].label_from_instance = \
                lambda obj: "%s (investor: %s)" % (obj.investment_product.title, obj.user.name)


class ContractTemplateForm(BaseModelForm):
    class Meta:
        model = ContractTemplate
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].label_suffix = " (within 30 characters)"


class InvestmentStepForm(BaseModelForm):
    class Meta:
        model = InvestmentStep
        fields = ['investment', 'title', 'stage_id', 'status', 'actor_role', 'description', 'contract', 'metadata']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['investment'].widget = forms.HiddenInput()
