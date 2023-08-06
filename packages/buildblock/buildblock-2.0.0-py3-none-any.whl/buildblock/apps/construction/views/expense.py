import logging
from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.construction.forms import (
    AddConstructionExpenseValForm,
    AddOutsourcingContractValForm,
    AddOutsourcingExpenseValForm,
    AddPersonnelExpenseValForm,
    UpdateConstructionExpenseValForm,
    UpdateOutsourcingContractValForm,
    UpdateOutsourcingExpenseValForm,
    UpdatePersonnelExpenseValForm
)
from buildblock.apps.construction.models import (
    ConstructionExpense,
    ConstructionOutsourcingContract,
    ConstructionOutsourcingExpense,
    ConstructionPersonnelExpense
)
from buildblock.apps.construction.views.base import ConstructionListView, ConstructionTemplateView
from buildblock.decorators import catch_errors, require_post
from buildblock.helper import db_update
from buildblock.services.construction import ConstructionService
from buildblock.utils import daterange, get_input_dict_data, get_required_post_data

logger = logging.getLogger(__name__)


@catch_errors
@require_post('construction')
def add_outsourcing_contract(request):
    form = AddOutsourcingContractValForm(request.POST, request.FILES)
    if not form.is_valid() or form.cleaned_data['start_date'] >= form.cleaned_data['end_date']:
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    data_dict = dict(
        title=form.cleaned_data['title'],
        amount=form.cleaned_data['amount'],
        included_details=request.POST.getlist('included_details[]'),
        start_date=form.cleaned_data['start_date'],
        end_date=form.cleaned_data['end_date'],
        attachment=form.cleaned_data['attachment']
    )
    ConstructionService.add_outsourcing_contract(
        construction_id=form.cleaned_data['construction_id'],
        contractor_id=form.cleaned_data['contractor_id'],
        data_dict=data_dict
    )
    messages.success(request, _("The outsourcing contract has been registered."))
    return redirect(form.cleaned_data['return_url'])


@catch_errors
@require_post('construction')
def edit_outsourcing_contract(request):
    form = UpdateOutsourcingContractValForm(request.POST, request.FILES)
    start_date = get_required_post_data(request, 'start_date')
    end_date = get_required_post_data(request, 'end_date')
    if not form.is_valid() or start_date >= end_date:
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return_url = get_required_post_data(request, 'return_url')
    contract_id = get_required_post_data(request, 'contract_id')
    contractor_id = get_required_post_data(request, 'contractor_id')
    title = get_required_post_data(request, 'title')
    amount = get_required_post_data(request, 'amount')
    included_details = request.POST.getlist('included_details[]')
    attachment = form.cleaned_data['attachment']
    delete_attach = request.POST.get('delete_attach')

    data_dict = dict(
        contractor_id=contractor_id,
        title=title,
        amount=amount,
        start_date=start_date,
        end_date=end_date,
        included_details=included_details,
    )
    ConstructionService.edit_outsourcing_contract(
        contract_id=contract_id,
        attachment=attachment,
        delete_attach=delete_attach,
        data_dict=data_dict
    )
    messages.success(request, _("The outsourcing contract has been edited."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def delete_outsourcing_contract(request):
    return_url = get_required_post_data(request, 'return_url')
    contract_id = get_required_post_data(request, 'contract_id')

    ConstructionService.delete_outsourcing_contract(contract_id)
    messages.success(request, _("The outsourcing contract has been deleted."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def add_outsourcing_expense(request):
    form = AddOutsourcingExpenseValForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    contract_id = form.cleaned_data['contract_id']
    paid_amount = form.cleaned_data['paid_amount']
    if paid_amount > 0:
        payment_date = datetime.utcnow()
    else:
        payment_date = None
    all_expenses = ConstructionService.get_outsourcing_expenses_by_contract(contract_id)
    if all_expenses:
        ordering = int(all_expenses.order_by('ordering').last().ordering) + 1
    else:
        ordering = 1

    data_dict = {
        'ordering': ordering,
        'title': form.cleaned_data['title'],
        'date': form.cleaned_data['date'],
        'payment_date': payment_date,
        'amount': form.cleaned_data['amount'],
        'paid_amount': paid_amount,
        'attachment': form.cleaned_data['attachment'],
        'description': form.cleaned_data['description']
    }

    ConstructionService.add_outsourcing_expense(
        contract_id=contract_id,
        data_dict=data_dict
    )
    messages.success(request, _("The outsourcing expense has been registered."))
    return redirect(form.cleaned_data['return_url'])


@catch_errors
@require_post('construction')
def edit_outsourcing_expense(request):
    form = UpdateOutsourcingExpenseValForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return_url = form.cleaned_data['return_url']
    expense_id = form.cleaned_data['expense_id']
    paid_amount = form.cleaned_data['paid_amount']
    title = form.cleaned_data['title']
    date = form.cleaned_data['date']
    amount = form.cleaned_data['amount']

    attachment = form.cleaned_data['attachment']
    delete_attach = request.POST.get('delete_attach')
    description = request.POST.get('description')

    data_dict = dict(
        title=title,
        date=date,
        amount=amount,
        paid_amount=paid_amount,
        description=description
    )
    ConstructionService.edit_outsourcing_expense(
        expense_id=expense_id,
        attachment=attachment,
        delete_attach=delete_attach,
        data_dict=data_dict
    )
    messages.success(request, _("The outsourcing expense has been edited."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def delete_outsourcing_expense(request):
    return_url = get_required_post_data(request, 'return_url')
    expense_id = get_required_post_data(request, 'expense_id')

    ConstructionService.delete_outsourcing_expense(expense_id)
    messages.success(request, _("The outsourcing expense has been deleted."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def add_personnel_expense(request):
    form = AddPersonnelExpenseValForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.POST.get('payment_check') == "paid":
        payment_date = datetime.utcnow()
    else:
        payment_date = None

    data_dict = dict(
        date=form.cleaned_data['date'],
        payment_date=payment_date,
        work_hours=form.cleaned_data['work_hours'],
        amount=form.cleaned_data['amount'],
        attachment=form.cleaned_data['attachment'],
        description=form.cleaned_data['description']
    )
    ConstructionService.add_personnel_expense(
        construction_id=form.cleaned_data['construction_id'],
        worker_id=form.cleaned_data['worker_id'],
        data_dict=data_dict
    )

    messages.success(request, _("A personnel expense has been registered."))
    return redirect(form.cleaned_data['return_url'])


@catch_errors
@require_post('construction')
def edit_personnel_expense(request):
    form = UpdatePersonnelExpenseValForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return_url = get_required_post_data(request, 'return_url')
    expense_id = get_required_post_data(request, 'expense_id')
    worker_id = get_required_post_data(request, 'worker_id')
    date = get_required_post_data(request, 'date')
    work_hours = get_required_post_data(request, 'work_hours')
    amount = get_required_post_data(request, 'amount')
    attachment = form.cleaned_data['attachment']
    description = request.POST.get('description')
    delete_attach = request.POST.get('delete_attach')

    if request.POST.get('payment_check') == "paid":
        payment_date = datetime.utcnow()
    else:
        payment_date = None

    data_dict = dict(
        worker_id=worker_id,
        date=date,
        payment_date=payment_date,
        work_hours=work_hours,
        amount=amount,
        description=description
    )
    ConstructionService.edit_personnel_expense(
        expense_id=expense_id,
        attachment=attachment,
        delete_attach=delete_attach,
        data_dict=data_dict
    )
    messages.success(request, _("The expense has been edited."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def add_expense(request):
    form = AddConstructionExpenseValForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    expense_data = {
        'category': form.cleaned_data['category'],
        'item': form.cleaned_data['item'],
        'date': form.cleaned_data['date'],
        'amount': form.cleaned_data['amount'],
        'quantity': form.cleaned_data['quantity'],
        'attachment': form.cleaned_data['attachment'],
        'description': form.cleaned_data['description']
    }

    ConstructionService.add_expense(
        construction_id=form.cleaned_data['construction_id'],
        expense_data=expense_data
    )
    messages.success(request, _("The expense has been registered."))
    return redirect(form.cleaned_data['return_url'])


@catch_errors
@require_post('construction')
def edit_expense(request):
    form = UpdateConstructionExpenseValForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return_url = get_required_post_data(request, 'return_url')
    expense_id = get_required_post_data(request, 'expense_id')
    item = get_required_post_data(request, 'item')
    category = get_required_post_data(request, 'category')
    date = get_required_post_data(request, 'date')
    quantity = get_required_post_data(request, 'quantity')
    amount = get_required_post_data(request, 'amount')
    attachment = form.cleaned_data['attachment']
    description = request.POST.get('description')
    delete_attach = request.POST.get('delete_attach')

    data_dict = dict(
        item=item,
        category=category,
        date=date,
        quantity=quantity,
        amount=amount,
        description=description
    )
    ConstructionService.edit_expense(
        expense_id=expense_id,
        attachment=attachment,
        delete_attach=delete_attach,
        data_dict=data_dict
    )
    messages.success(request, _("The expense has been edited."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def delete_expense(request):
    return_url = get_required_post_data(request, 'return_url')
    expense_id = get_required_post_data(request, 'expense_id')
    expense_type = get_required_post_data(request, 'expense_type')

    if expense_type == 'personnel_expense':
        ConstructionService.delete_personnel_expense(expense_id)
    elif expense_type == 'expense':
        ConstructionService.delete_expense(expense_id)
    messages.success(request, _("The expense has been deleted."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def edit_payment_date(request):
    return_url = get_required_post_data(request, 'return_url')
    expense_ids = request.POST.getlist('select_expense[]')

    expenses = ConstructionPersonnelExpense.objects.filter(id__in=expense_ids)
    db_update(expenses, dict(payment_date=datetime.utcnow()))

    messages.success(request, _("The expense's payment date has been edited."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def save_multiple_personnel_expenses(request):
    return_url = get_required_post_data(request, 'return_url')

    worker_id = get_required_post_data(request, 'worker_id')
    construction_id = get_required_post_data(request, 'construction_id')
    start_date = datetime.strptime(get_required_post_data(request, 'start_date'), "%Y-%m-%d")
    end_date = datetime.strptime(get_required_post_data(request, 'end_date'), "%Y-%m-%d")
    date_range = daterange(start_date, end_date)

    # TODO: 일정 시간 지난 후에 수정 불가능하게 하는 기능? 공사 상태에 따라?
    for single_date in date_range:
        single_data = get_input_dict_data(request.POST, single_date.strftime("%Y-%m-%d"))

        expense_id = single_data.get('expense_id')
        work_hours = single_data.get('work_hours') or None
        amount = single_data.get('amount') or None
        select_expense = single_data.get('select_expense')
        payment_date = datetime.utcnow() if select_expense == "paid" else None

        if work_hours and amount:
            expense_data = {
                'payment_date': payment_date,
                'work_hours': work_hours,
                'amount': amount
            }
            ConstructionService.edit_or_add_personnel_expense(
                construction_id=construction_id,
                worker_id=worker_id,
                date=single_date,
                expense_data=expense_data
            )
        elif expense_id:
            ConstructionService.delete_personnel_expense(expense_id)

    messages.success(request, _("The expense has been edited."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def save_multiple_expenses(request):
    return_url = get_required_post_data(request, 'return_url')
    construction_id = get_required_post_data(request, 'construction_id')
    expense_count = int(get_required_post_data(request, 'expense_count'))
    date = get_required_post_data(request, 'date')

    for i in range(expense_count):
        single_data = get_input_dict_data(request.POST, "expense_"+str(i))
        item = single_data.get('item')
        category = single_data.get('category')
        quantity = single_data.get('quantity')
        amount = single_data.get('amount')

        if not (item and category and quantity and amount):
            continue
        expense_data = {
            'date': date,
            'item': item,
            'category': category,
            'quantity': quantity,
            'amount': amount
        }
        ConstructionService.add_expense(
            construction_id=construction_id,
            expense_data=expense_data
        )

    messages.success(request, _("The expense has been edited."))
    return redirect(return_url)


class ExpenseView:
    model = ConstructionExpense
    context_object_name = 'expenses'
    ordering = ['-date']
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(construction__id=self.kwargs['construction_id'])


class PersonnelExpenseView:
    model = ConstructionPersonnelExpense
    context_object_name = 'personnel_expenses'
    ordering = ['-date']
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(construction__id=self.kwargs['construction_id'])


class OutsourcingExpenseView:
    model = ConstructionOutsourcingExpense
    context_object_name = 'outsourcing_expenses'
    ordering = ['ordering']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(outsourcing_contract__construction__id=self.kwargs['construction_id'])


class PersonnelExpenseListView(PersonnelExpenseView, ConstructionListView):
    template_name = "construction/personnel_expense_list.html"
    page_title = "PERSONNEL EXPENSES"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personnel_expenses = self.object_list
        context['expenses_not_paid'] = personnel_expenses.filter(payment_date__isnull=True)

        return context


class ExpenseListView(ExpenseView, ConstructionListView):
    template_name = "construction/expense_list.html"
    page_title = "MATERIALS & EXTRA EXPENSES"


class OutsourcingExpenseListView(OutsourcingExpenseView, ConstructionListView):
    template_name = "construction/outsourcing_expense_list.html"
    page_title = "OUTSOURCING EXPENSES"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        outsourcing_expenses = self.object_list
        context['expenses_not_paid'] = outsourcing_expenses.filter(payment_date__isnull=True)
        context['contractor_list'] = ConstructionService.get_worker_by_role(role='CONTRACTOR')
        outsourcing_contracts = ConstructionOutsourcingContract.objects.filter(
            construction_id=self.kwargs['construction_id']
        )
        contract_data = []

        for contract in outsourcing_contracts:
            expenses = outsourcing_expenses.filter(outsourcing_contract__id=contract.id)
            data_list = {
                'data': ConstructionService.get_outsourcing_contract(id=contract.id),
                'expenses': expenses,
                'paid_expenses': expenses.filter(payment_date__isnull=False)
            }
            contract_data.append(data_list)

        context['contract_data'] = contract_data

        return context


class MultiPersonnelExpenseFormView(PersonnelExpenseView, ConstructionTemplateView):
    template_name = "construction/multi_personnel_expense_form.html"
    page_title = "Add Multiple Personnel Expenses"

    def dispatch(self, request, *args, **kwargs):
        self.worker_id = self.request.GET.get('worker_id')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if not (self.worker_id and start_date and end_date):
            messages.warning(self.request, _("You have entered an invalid information. Please try again."))
            return redirect(reverse(
                'construction:personnel-expense-list',
                kwargs={'construction_id': self.kwargs['construction_id']}
            ))

        self.start_date = datetime.fromtimestamp(float(start_date))
        self.end_date = datetime.fromtimestamp(float(end_date))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_range = daterange(self.start_date, self.end_date)

        multi_expenses = []
        construction_id = self.kwargs['construction_id']
        personnel_expense_data = ConstructionService.get_personnel_expense_by_worker_and_date_range(
            worker_id=self.worker_id,
            construction_id=construction_id,
            date_range=date_range,
        )

        for single_date in date_range:
            data_list = {
                'date': single_date,
                'expense': personnel_expense_data.filter(date=single_date).first()
            }
            multi_expenses.append(data_list)

        context['multi_expenses'] = multi_expenses
        context['start_date'] = self.start_date
        context['end_date'] = self.end_date

        return context


class MultiExpenseFormView(ExpenseView, ConstructionTemplateView):
    template_name = "construction/multi_expense_form.html"
    page_title = "Add Multiple Expenses"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        date = self.request.GET.get('date')

        construction_id = self.kwargs['construction_id']
        expense_data = ConstructionService.get_expense_by_date_range(construction_id, [date])

        context['multi_expenses'] = expense_data

        return context
