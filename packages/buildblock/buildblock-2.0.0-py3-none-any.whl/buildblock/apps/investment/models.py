import logging

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from marshmallow import Schema, fields, validate
from private_storage.fields import PrivateFileField

from buildblock.apps.core.constants import (
    ATTACHMENT,
    CONTRACT_STATUS_TYPE,
    CONTRACT_TEMPLATE_TYPE,
    INVESTMENT_ROLES,
    INVESTMENT_STEP_STATUS_TYPE,
    INVESTMENT_WORKFLOW_TYPE,
    MANAGER_ROLE,
    PENDING
)
from buildblock.apps.core.enums import AccountTransactionCategoryEnum, AccountTransactionEntityTypeEnum, BankEnum
from buildblock.apps.core.models import HistoricalRecordModel, TimeStampedModel
from buildblock.apps.users.models import User
from buildblock.decorators import memoized_property
from buildblock.models.investment import InvestmentTransactionEntityModel

logger = logging.getLogger(__name__)


class WorkflowStageListSchema(Schema):
    """
    [
        {"id": "1", "title": "투자시작", "description": ""},
    ]
    """
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str()


class WorkflowStepListSchema(Schema):
    """
    [
        {"id": "1", "stage": "1", "title": "서비스 용역 계약서", "description": "", "metadata": ["amount",]},
    ]
    """
    id = fields.Str(required=True)
    stage = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    actor_role = fields.Str(validate=validate.OneOf(dict(INVESTMENT_ROLES)))
    metadata = fields.List(fields.Str())


class RelatedWorkflowTemplateListSchema(Schema):
    """
    [
        {"template": "{InvestmentWorkflowTemplate.id}", "stage": "{stage.id}", "step": "{step.id}"},
    ]
    """
    template = fields.Int(required=True)
    stage = fields.Str(required=True)
    step = fields.Str(required=True)


def investment_contract_document_path(instance, filename):
    return f"contract/document/{instance.investment.user.uuid}/{filename}"


def investment_product_plan_path(instance, filename):
    return f"investment_product/plan/{instance.id}/{filename}"


class InvestmentCompany(HistoricalRecordModel):
    title = models.CharField(_("Title"), max_length=200)
    established_at = models.DateField()
    users = models.ManyToManyField(User, blank=True, related_name='owned_companies')


class InvestmentCompanyBankAccount(HistoricalRecordModel):
    bank_name = models.CharField(_("Bank Name"), choices=BankEnum.choices(), max_length=24)
    bank_routing_number = models.CharField(_("Bank Routing Number"), max_length=9)
    bank_account_number = models.CharField(_("Bank Account Number"), max_length=20)
    name = models.CharField(_("Account Name"), max_length=200)
    company = models.ForeignKey(InvestmentCompany, on_delete=models.CASCADE, related_name='accounts')
    balance = models.PositiveIntegerField(default=0)
    opened_at = models.DateField()


class InvestmentProduct(HistoricalRecordModel):
    '''고객들이 투자하는 상품 - Product: Building information / InvestmentProduct: Investment Information'''
    title = models.CharField(_("Investment Title"), max_length=200, unique=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investment_manager')
    start_date = models.DateField(_("Start Date"), null=True, blank=True)
    end_date = models.DateField(_("End Date"), null=True, blank=True)
    plan = models.FileField(_("Investment Plan file"), upload_to=investment_product_plan_path, blank=True)
    description = RichTextUploadingField(_("Investment description"), blank=True)


class InvestmentWorkflowTemplate(TimeStampedModel):
    type = models.CharField(_("Workflow Type"), choices=INVESTMENT_WORKFLOW_TYPE, max_length=50)
    title = models.CharField(_("Title"), max_length=200, unique=True)
    description = RichTextUploadingField(_("Investment description"), blank=True)
    stage_list = models.JSONField(default=list)
    step_list = models.JSONField(default=list)

    def clean(self):
        if not self._has_valid_stage_list:
            raise Exception('Invalid schema for the stage list field')
        if not self._has_valid_step_list:
            raise Exception('Invalid schema for the step list field')

    @property
    def _has_valid_stage_list(self):
        return self.schema_list_valid(WorkflowStageListSchema, "stage_list")

    @property
    def _has_valid_step_list(self):
        return self.schema_list_valid(WorkflowStepListSchema, "step_list")


class Investment(HistoricalRecordModel):
    # TODO: Company 이전 작업 완료 후 User 부분 삭제 예정
    investment_product = models.ForeignKey(InvestmentProduct,
                                           on_delete=models.CASCADE,
                                           related_name='investments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investor_investments')
    company = models.ForeignKey(InvestmentCompany,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name='company_investments')
    workflow_template = models.ForeignKey(InvestmentWorkflowTemplate,
                                          on_delete=models.CASCADE,
                                          null=True,
                                          blank=True,
                                          related_name='workflow_investments')
    amount = models.IntegerField(_("Amount"))
    metadata = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        unique_together = (("investment_product", "company"))


class ContractTemplate(TimeStampedModel):
    type = models.CharField(_("Template Type"), choices=CONTRACT_TEMPLATE_TYPE, default=ATTACHMENT, max_length=20)
    title = models.CharField(_("Template Title"), max_length=200, unique=True)
    description = models.CharField(_("Template Description"), max_length=30, null=True, blank=True)
    identifier = models.CharField(null=True, blank=True, max_length=100)
    related_workflow_templates = models.JSONField(default=list)
    metadata = models.JSONField(default=dict, null=True, blank=True)

    def clean(self):
        if not self._has_valid_related_workflow_template_list:
            raise Exception('Invalid schema for the related workflow template list field')

    @property
    def _has_valid_related_workflow_template_list(self):
        return self.schema_list_valid(RelatedWorkflowTemplateListSchema, "related_workflow_template")


class InvestmentContract(HistoricalRecordModel):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, related_name='investment_contracts')
    title = models.CharField(_("Contract Title"), max_length=200)
    identifier = models.CharField(null=True, blank=True, max_length=100)
    document_file = PrivateFileField(_("Document file"), upload_to=investment_contract_document_path, blank=True)
    records = models.JSONField(default=dict, null=True, blank=True)
    template = models.ForeignKey(ContractTemplate, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(_("Contract Status"), choices=CONTRACT_STATUS_TYPE, max_length=40)
    due_date = models.DateField(_("Due Date"), null=True, blank=True)


class InvestmentStep(HistoricalRecordModel):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, related_name='investment_steps')
    title = models.CharField(_("Step Title"), max_length=200)
    stage_id = models.CharField(_("Stage ID"), max_length=20)
    step_id = models.CharField(_("Step ID"), max_length=20, null=True, blank=True)
    status = models.CharField(_("Status"), max_length=100, choices=INVESTMENT_STEP_STATUS_TYPE, default=PENDING)
    actor_role = models.CharField(_("Actor Role"), max_length=100, choices=INVESTMENT_ROLES, default=MANAGER_ROLE)
    description = RichTextUploadingField(_("Description"), blank=True)
    contract = models.ManyToManyField(InvestmentContract, blank=True)
    metadata = models.JSONField(default=dict, null=True, blank=True)


def transaction_entity(entity_type, entity_id):
    try:
        if entity_type == AccountTransactionEntityTypeEnum.USER.name:
            user = User.objects.get(id=entity_id)
            return InvestmentTransactionEntityModel(
                id=entity_id,
                type=AccountTransactionEntityTypeEnum.USER.value,
                name=user.name,
                bank_name=None,
                bank_account_number=None
            )
        elif entity_type == AccountTransactionEntityTypeEnum.COMPANY.name:
            account = InvestmentCompanyBankAccount.objects.get(id=entity_id)
            return InvestmentTransactionEntityModel(
                id=entity_id,
                type=AccountTransactionEntityTypeEnum.USER.value,
                name=account.company.title,
                bank_name=account.bank_name,
                bank_account_number=account.bank_account_number
            )
        else:
            return InvestmentTransactionEntityModel(
                id=entity_id,
                type=AccountTransactionEntityTypeEnum.UNKNOWN.value,
                name=entity_type,
                bank_name=None,
                bank_account_number=None
            )
    except Exception as e:
        logger.error(f'Invalid Transaction Entity Data.: {str(e)}')


class InvestmentCompanyBankTransaction(HistoricalRecordModel):
    to_entity_type = models.CharField(_("To Type"),
                                      max_length=20,
                                      choices=AccountTransactionEntityTypeEnum.choices())
    to_entity_id = models.IntegerField(_("To ID"))
    from_entity_type = models.CharField(_("From Type"),
                                        max_length=20,
                                        choices=AccountTransactionEntityTypeEnum.choices())
    from_entity_id = models.IntegerField(_("From ID"))
    investment = models.ForeignKey(Investment,
                                   on_delete=models.CASCADE,
                                   related_name='investment_transactions',
                                   null=True, blank=True)
    category = models.CharField(max_length=20, choices=AccountTransactionCategoryEnum.choices())
    amount = models.IntegerField(_("Amount"), null=True, blank=True)
    description = models.CharField(max_length=500)
    event_at = models.DateTimeField()

    @memoized_property
    def to_entity(self):
        return transaction_entity(self.to_entity_type, self.to_entity_id)

    @memoized_property
    def from_entity(self):
        return transaction_entity(self.from_entity_type, self.from_entity_id)
