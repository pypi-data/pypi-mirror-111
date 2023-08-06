from datetime import datetime

from buildblock.apps.construction.models import (
    Construction,
    ConstructionExpense,
    ConstructionOutsourcingContract,
    ConstructionOutsourcingExpense,
    ConstructionPersonnelExpense,
    ConstructionPicture,
    ConstructionReport,
    ConstructionWork,
    Worker,
    WorkType
)
from buildblock.helper import db_update


class ConstructionService:
    """High level interface for dealing with the Construction database."""

    @classmethod
    def get_construction(cls, id):
        return Construction.objects.get(id=id)

    @classmethod
    def get_construction_work(cls, id):
        return ConstructionWork.objects.get(id=id)

    @classmethod
    def get_construction_work_by_date_range(cls, construction_id, date_range):
        return ConstructionWork.objects.filter(
            construction__id=construction_id,
            work_date__overlap=date_range
        ).order_by('-id')

    @classmethod
    def get_work_type(cls, id):
        return WorkType.objects.get(id=id)

    @classmethod
    def get_worker(cls, id):
        return Worker.objects.get(id=id)

    @classmethod
    def get_picture(cls, id):
        return ConstructionPicture.objects.get(id=id)

    @classmethod
    def get_worker_by_role(cls, role):
        return Worker.objects.filter(role=role)

    @classmethod
    def get_personnel_expense(cls, id):
        return ConstructionPersonnelExpense.objects.get(id=id)

    @classmethod
    def get_personnel_expense_by_date_range(cls, construction_id, date_range):
        return ConstructionPersonnelExpense.objects.filter(
            construction__id=construction_id,
            date__in=date_range
        )

    @classmethod
    def get_personnel_expense_by_worker(cls, worker_id):
        return ConstructionPersonnelExpense.objects.filter(
            worker__id=worker_id
        )

    @classmethod
    def get_personnel_expense_by_worker_and_date_range(
        cls, worker_id, construction_id, date_range
    ):
        return ConstructionPersonnelExpense.objects.filter(
            worker__id=worker_id,
            construction__id=construction_id,
            date__in=date_range
        )

    @classmethod
    def get_expense(cls, id):
        return ConstructionExpense.objects.get(id=id)

    @classmethod
    def get_expense_by_date_range(cls, construction_id, date_range):
        return ConstructionExpense.objects.filter(
            construction__id=construction_id,
            date__in=date_range
        )

    @classmethod
    def add_picture(cls, work_id, picture, data_dict: dict):
        ConstructionPicture.objects.create(
            construction_work_id=work_id,
            picture=picture,
            **data_dict
        )

    @classmethod
    def edit_picture(cls, picture_id, data_dict: dict):
        picture = cls.get_picture(picture_id)
        db_update(picture, data_dict)

    @classmethod
    def delete_picture(cls, picture_id):
        cls.get_picture(picture_id).delete()

    @classmethod
    def add_work(
        cls, construction_id, type_id, data_dict: dict
    ):
        ConstructionWork.objects.create(
            construction_id=construction_id,
            type_id=type_id,
            **data_dict
        )

    @classmethod
    def edit_work(cls, work_id, data_dict: dict):
        work = cls.get_construction_work(work_id)
        db_update(work, data_dict)

    @classmethod
    def delete_work(cls, work_id):
        cls.get_construction_work(work_id).delete()

    @classmethod
    def add_worker(cls, name, role, data_dict: dict):
        Worker.objects.create(
            name=name,
            role=role,
            **data_dict
        )

    @classmethod
    def edit_worker(cls, worker_id, data_dict: dict):
        worker = cls.get_worker(worker_id)
        db_update(worker, data_dict)

    @classmethod
    def delete_worker(cls, worker_id):
        cls.get_worker(worker_id).delete()

    @classmethod
    def add_personnel_expense(cls, construction_id, worker_id, data_dict: dict):
        ConstructionPersonnelExpense.objects.create(
            construction_id=construction_id,
            worker_id=worker_id,
            **data_dict
        )

    @classmethod
    def edit_personnel_expense(
        cls, expense_id, attachment, delete_attach, data_dict: dict
    ):
        personnel_expense = cls.get_personnel_expense(expense_id)
        if attachment:
            personnel_expense.attachment = attachment
        elif delete_attach:
            personnel_expense.attachment.delete()
        db_update(personnel_expense, data_dict)

    @classmethod
    def edit_or_add_personnel_expense(
        cls, construction_id, worker_id, date, expense_data
    ):
        ConstructionPersonnelExpense.objects.update_or_create(
            construction_id=construction_id,
            worker_id=worker_id,
            date=date,
            defaults=expense_data
        )

    @classmethod
    def delete_personnel_expense(cls, expense_id):
        cls.get_personnel_expense(expense_id).delete()

    @classmethod
    def add_expense(cls, construction_id, expense_data):
        construction = cls.get_construction(id=construction_id)
        ConstructionExpense.objects.create(
            construction=construction,
            **expense_data
        )

    @classmethod
    def edit_expense(
        cls, expense_id, attachment, delete_attach, data_dict: dict
    ):
        expense = cls.get_expense(expense_id)
        if attachment:
            expense.attachment = attachment
        elif delete_attach:
            expense.attachment.delete()
        db_update(expense, data_dict)

    @classmethod
    def delete_expense(cls, expense_id):
        cls.get_expense(expense_id).delete()

    @classmethod
    def get_outsourcing_contract(cls, id):
        return ConstructionOutsourcingContract.objects.get(id=id)

    @classmethod
    def add_outsourcing_contract(
        cls, construction_id, contractor_id, data_dict: dict
    ):
        ConstructionOutsourcingContract.objects.create(
            construction_id=construction_id,
            contractor_id=contractor_id,
            **data_dict
        )

    @classmethod
    def edit_outsourcing_contract(
        cls, contract_id, attachment, delete_attach, data_dict: dict
    ):
        contract = cls.get_outsourcing_contract(contract_id)
        if attachment:
            contract.attachment = attachment
        elif delete_attach:
            contract.attachment.delete()
        db_update(contract, data_dict)

    @classmethod
    def delete_outsourcing_contract(cls, contract_id):
        cls.get_outsourcing_contract(contract_id).delete()

    @classmethod
    def get_outsourcing_expense(cls, id):
        return ConstructionOutsourcingExpense.objects.get(id=id)

    @classmethod
    def get_outsourcing_expenses_by_contract(cls, contract_id):
        return ConstructionOutsourcingExpense.objects.filter(
            outsourcing_contract__id=contract_id
        )

    @classmethod
    def add_outsourcing_expense(cls, contract_id, data_dict: dict):
        ConstructionOutsourcingExpense.objects.create(
            outsourcing_contract_id=contract_id,
            **data_dict
        )

    @classmethod
    def edit_outsourcing_expense(
        cls, expense_id, attachment, delete_attach, data_dict: dict
    ):
        expense = cls.get_outsourcing_expense(expense_id)
        expense.payment_date = datetime.utcnow() \
            if data_dict.get('paid_amount', 0) > 0 else None
        if attachment:
            expense.attachment = attachment
        elif delete_attach:
            expense.attachment.delete()
        db_update(expense, data_dict)

    @classmethod
    def delete_outsourcing_expense(cls, expense_id):
        cls.get_outsourcing_expense(expense_id).delete()

    @classmethod
    def get_daily_report_by_date_range(cls, construction_id, date_range):
        return ConstructionReport.objects.filter(
            construction__id=construction_id,
            start_date__in=date_range,
            type='DAILY'
        )

    @classmethod
    def add_weekly_report(cls, construction_id, type, start_date, end_date):
        return ConstructionReport.objects.create(
            construction_id=construction_id,
            type=type,
            start_date=start_date,
            end_date=end_date
        )

    @classmethod
    def get_report_by_type(cls, construction_id, report_type):
        return ConstructionReport.objects.filter(
            construction__id=construction_id,
            type=report_type
        )
