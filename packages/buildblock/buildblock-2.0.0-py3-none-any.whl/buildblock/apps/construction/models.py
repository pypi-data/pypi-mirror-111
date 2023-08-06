from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import (
    CONSTRUCTION_METHOD_CHOICES,
    CONSTRUCTION_PICTURE_STATUS_CHOICES,
    CONSTRUCTION_STATUS_CHOICES,
    CONSTRUCTION_TYPE_CHOICES,
    DIRECT_MANAGEMENT,
    EXPENSE_CATEGORY_CHOICES,
    IN_PROGRESS,
    OUTSOURCING_INCLUDED_CHOICES,
    PENDING,
    REPORT_TYPE_CHOICES,
    WORKER,
    WORKER_ROLE_CHOICES,
    WORKER_SPECIALITY_CHOICES
)
from buildblock.apps.core.models import ExpenseModel, HistoricalRecordModel, TimeStampedModel
from buildblock.apps.product.models import Product
from buildblock.apps.users.models import User
from buildblock.utils import make_thumbnail_url


def _construction_file_path(construction, filename, detail_path):
    product_code = construction.product.code
    return f"product/{product_code}/construction/{construction.id}/{detail_path}/{filename}"


def construction_picture_path(instance, filename):
    return _construction_file_path(instance.construction_work.construction, filename, "picture")


def construction_personnel_expense_path(instance, filename):
    return _construction_file_path(instance.construction, filename, "personnel_expense")


def construction_expense_path(instance, filename):
    return _construction_file_path(instance.construction, filename, "expense")


def construction_outsourcing_contract_path(instance, filename):
    return _construction_file_path(instance.construction, filename, "outsourcing_contract")


def construction_outsourcing_expense_path(instance, filename):
    return _construction_file_path(instance.outsourcing_contract.construction, filename, "outsourcing_expense")


class WorkType(TimeStampedModel):
    title = models.CharField(_("Work Type title"), max_length=100)
    description = RichTextUploadingField(_("Work Type description"), blank=True)


class Worker(TimeStampedModel):
    """Worker for Constructor"""
    name = models.CharField(_("Name"), max_length=200)
    phone_number = models.CharField(_("Phone"), max_length=20, blank=True, null=True)
    speciality = ArrayField(models.CharField(_("Speciality"),
                                             max_length=30,
                                             choices=WORKER_SPECIALITY_CHOICES), default=list)
    role = models.CharField(_("Role"),
                            choices=WORKER_ROLE_CHOICES,
                            default=WORKER,
                            max_length=20)  # worker, leader, contractor 중 택1
    description = models.TextField(_("Description"), blank=True)


class Construction(HistoricalRecordModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='constructions')
    type = models.CharField(_("Construction Type"), choices=CONSTRUCTION_TYPE_CHOICES, max_length=32)
    method = models.CharField(_("Construction Method"),
                              choices=CONSTRUCTION_METHOD_CHOICES,
                              default=DIRECT_MANAGEMENT,
                              max_length=32)
    constructor = models.ManyToManyField(User, related_name='related_constructions', blank=True)
    status = models.CharField(_("Construction Status"),
                              choices=CONSTRUCTION_STATUS_CHOICES,
                              default=PENDING,
                              max_length=16)
    title = models.CharField(_("Construction title"), max_length=100)
    budget = models.PositiveIntegerField(_("Budget (cent)"))
    start_date = models.DateField(_("Construction Start Date"))
    end_date = models.DateField(_("Construction End Date"))
    description = RichTextUploadingField(_("Product description"), blank=True)
    favorite_workers = models.ManyToManyField(Worker, related_name='favorite_constructions', blank=True)


class ConstructionWork(HistoricalRecordModel):
    """Construction Work Process"""
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE, related_name='work_process')
    title = models.CharField(_("Work title"), max_length=100)
    type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    zone_ids = ArrayField(models.IntegerField(), blank=True, default=list)
    work_date = ArrayField(models.DateField(), blank=True, default=list)

    def clean(self):
        if not self._has_valid_zone:
            raise Exception('Invalid data for the zone field')

    @property
    def _has_valid_zone(self):
        """
        Product zone필드에 데이터가 있는지 검사
        """
        zones = [zone.get('id') for zone in self.construction.product.zone]
        return set(self.zone_ids).issubset(zones)


class ConstructionPicture(TimeStampedModel):
    construction_work = models.ForeignKey(ConstructionWork, on_delete=models.CASCADE, related_name='work_picture')
    picture = models.ImageField(_("Picture"), upload_to=construction_picture_path)
    status = models.CharField(_("Status"),
                              choices=CONSTRUCTION_PICTURE_STATUS_CHOICES,
                              default=IN_PROGRESS,
                              max_length=16)
    description = models.TextField(_("Description"), blank=True)

    @property
    def construction_picture_thumb_url(self):
        return make_thumbnail_url(self.picture)


class ConstructionExpense(ExpenseModel):
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE)
    category = models.CharField(_("Category"), max_length=50, choices=EXPENSE_CATEGORY_CHOICES)
    item = models.CharField(_("Item"), max_length=200)
    quantity = models.PositiveIntegerField(_("Quantity"), blank=True, null=True)
    attachment = models.FileField(_("Attachment"), blank=True, upload_to=construction_expense_path)


class ConstructionPersonnelExpense(ExpenseModel):
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    work_hours = models.PositiveIntegerField(_("Hour"), blank=True, null=True)
    attachment = models.FileField(_("Attachment"), blank=True, upload_to=construction_personnel_expense_path)
    payment_date = models.DateField(_("Payment Date"), null=True, blank=True)

    class Meta:
        unique_together = (("construction", "worker", "date"))


class ConstructionOutsourcingContract(HistoricalRecordModel):
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Worker, on_delete=models.CASCADE)  # Worker에서 role contractor 리스트만 불러옴
    title = models.CharField(_("Title"), max_length=200)
    amount = models.PositiveIntegerField(_("Amount"), blank=True, null=True)
    attachment = models.FileField(_("Attachment"), blank=True, upload_to=construction_outsourcing_contract_path)
    included_details = ArrayField(models.CharField(_("Included Details"),
                                  max_length=30,
                                  choices=OUTSOURCING_INCLUDED_CHOICES),
                                  default=list)  # amount에 포함되는 항목 (labor, material, etc)
    start_date = models.DateField(_("From"))
    end_date = models.DateField(_("To"))


class ConstructionOutsourcingExpense(ExpenseModel):
    outsourcing_contract = models.ForeignKey(ConstructionOutsourcingContract, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=200)
    ordering = models.CharField(_("Ordering"), max_length=200)
    paid_amount = models.PositiveIntegerField(_("Paid Amount"), default=0)  # 계약한 금액과 실제 지급 금액이 다를 수 있음
    payment_date = models.DateField(_("Payment Date"), blank=True, null=True)
    attachment = models.FileField(_("Attachment"), blank=True, upload_to=construction_outsourcing_expense_path)

    class Meta:
        unique_together = (("outsourcing_contract", "ordering"))


class ConstructionReport(HistoricalRecordModel):
    """Product Construction Reports"""
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE, related_name='reports')
    type = models.CharField(_("Type"),
                            choices=REPORT_TYPE_CHOICES,
                            max_length=20)  # Daily, Weekly, Final 중 택1
    start_date = models.DateField(_("From"))
    end_date = models.DateField(_("To"))
    content = RichTextUploadingField(_("Content"), blank=True)

    class Meta:
        unique_together = (("construction", "start_date", "end_date"))


# TODO ConstructionCustomReport
