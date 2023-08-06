import logging
from calendar import monthrange
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.construction.forms import AddWeeklyReportValForm, ReportForm
from buildblock.apps.construction.models import ConstructionReport, ConstructionWork
from buildblock.apps.construction.views.base import (
    ConstructionCreateView,
    ConstructionListView,
    ConstructionTemplateView,
    ConstructionUpdateView
)
from buildblock.apps.core.constants import WEEKLY
from buildblock.decorators import catch_errors, require_post
from buildblock.services.construction import ConstructionService
from buildblock.utils import daterange

logger = logging.getLogger(__name__)


def _expense_data(model, date):
    data = model.filter(date=date)
    total = data.aggregate(count=Count('date'), sum=Coalesce(Sum('amount'), 0))
    return {
        'data': data,
        'count': total['count'],
        'sum': total['sum']
    }


def _expense_data_by_range(model, date_range):
    data = model.filter(date__in=date_range)
    total = data.aggregate(count=Count('date'), sum=Coalesce(Sum('amount'), 0))
    return {
        'data': data,
        'count': total['count'],
        'sum': total['sum']
    }


@catch_errors
@require_post('construction')
def add_weekly_report(request):
    form = AddWeeklyReportValForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request,
                         _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    construction_id = form.cleaned_data.get('construction_id')
    end_date = form.cleaned_data.get('end_date')
    start_date = end_date - timedelta(days=6)
    date_range = [start_date, end_date]

    # 기존 주간보고서와 기간이 겹치지 않도록
    weekly_reports = ConstructionReport.objects\
                     .filter(construction_id=construction_id)\
                     .filter(Q(start_date__range=date_range) | Q(end_date__range=date_range))\
                     .distinct()
    if weekly_reports:
        messages.warning(request, _("Already registered."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    ConstructionService.add_weekly_report(
        construction_id=construction_id,
        type=WEEKLY,
        start_date=start_date,
        end_date=end_date
    )
    messages.success(request, _("The weekly report has been created."))
    return redirect(
        reverse('construction:weekly-report-list',
                kwargs={'construction_id': construction_id})
    )


class ReportView:
    model = ConstructionReport
    context_object_name = 'report'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(construction__id=self.kwargs['construction_id'])


class DailyReportListView(ConstructionTemplateView):
    template_name = "construction/daily_report_list.html"
    page_title = "Daily Report"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        construction_id = self.kwargs['construction_id']
        construction_end_date = ConstructionService.get_construction(construction_id).end_date
        if date.today() < construction_end_date:
            current_date = date.today()
        else:
            current_date = construction_end_date
        current_date = current_date.replace(
            year=int(self.request.GET.get('year', current_date.year)),
            month=int(self.request.GET.get('month', current_date.month)),
            day=1
        )
        _, current_month_last_day = monthrange(current_date.year, current_date.month)
        end_date = current_date.replace(day=current_month_last_day)
        start_date = current_date.replace(day=1)
        date_range = daterange(start_date, end_date)

        reports = []
        construction_work = ConstructionService.get_construction_work_by_date_range(construction_id, date_range)
        personnel_expense_data = ConstructionService.get_personnel_expense_by_date_range(construction_id, date_range)
        expense_data = ConstructionService.get_expense_by_date_range(construction_id, date_range)
        report_data = ConstructionService.get_daily_report_by_date_range(construction_id, date_range)

        for single_date in date_range:
            data_list = {
                'date': single_date,
                'works': construction_work.filter(work_date__contains=[single_date]),
                'personnel_expense': _expense_data(personnel_expense_data, single_date),
                'expense': _expense_data(expense_data, single_date),
                'report_data': report_data.filter(end_date=single_date)
            }

            reports.append(data_list)

        context['reports'] = reports
        context['current_year'] = current_date.year
        context['current_month'] = current_date.month

        return context


class DailyReportFormView(ReportView):
    form_class = ReportForm
    template_name = "construction/daily_report_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        construction_id = self.kwargs['construction_id']
        report_date = datetime.strptime(self.kwargs['report_date'], "%Y-%m-%d").date()
        all_works = ConstructionWork.objects \
            .filter(construction__id=construction_id) \
            .exclude(work_date__overlap=[report_date])
        works = ConstructionService.get_construction_work_by_date_range(construction_id, [report_date])
        personnel_expenses = ConstructionService.get_personnel_expense_by_date_range(construction_id, [report_date])
        personnel_expense_sum = personnel_expenses.aggregate(sum=Coalesce(Sum('amount'), 0))
        expenses = ConstructionService.get_expense_by_date_range(construction_id, [report_date])
        expense_sum = expenses.aggregate(sum=Coalesce(Sum('amount'), 0))

        context.update(
            all_works=all_works,
            personnel_expenses=personnel_expenses,
            personnel_expense_sum=personnel_expense_sum['sum'],
            expenses=expenses,
            expense_sum=expense_sum['sum'],
            works=self._make_all_construction_works_context(works, report_date),
            report_date=report_date
        )

        return context

    def get_success_url(self):
        construction_id = self.kwargs.get('construction_id')
        return reverse_lazy('construction:daily-report-list', kwargs={'construction_id': construction_id})


class DailyReportCreateView(DailyReportFormView, ConstructionCreateView):
    page_title = "WRITE DAILY REPORT"


class DailyReportUpdateView(DailyReportFormView, ConstructionUpdateView):
    page_title = "EDIT DAILY REPORT"


class WeeklyReportListView(ConstructionListView):
    model = ConstructionReport
    template_name = "construction/weekly_report_list.html"
    page_title = "WEEKLY REPORTS"
    context_object_name = "weekly_reports"
    ordering = ['start_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        construction_id = self.kwargs['construction_id']
        return queryset.filter(
            construction__id=construction_id,
            type=WEEKLY
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        construction_id = self.kwargs['construction_id']
        weekly_reports = context.get(self.context_object_name)

        reports = []
        for weekly_report in weekly_reports:
            start_date = weekly_report.start_date
            end_date = weekly_report.end_date
            date_range = daterange(start_date, end_date)

            construction_work = ConstructionService.get_construction_work_by_date_range(construction_id, date_range)
            personnel_expense_data = ConstructionService.get_personnel_expense_by_date_range(
                                        construction_id, date_range
                                     )
            expense_data = ConstructionService.get_expense_by_date_range(construction_id, date_range)

            data_list = {
                'works': construction_work,
                'personnel_expense': _expense_data_by_range(personnel_expense_data, date_range),
                'expense': _expense_data_by_range(expense_data, date_range),
                'report_data': weekly_report
            }
            reports.append(data_list)

        context['reports'] = reports

        return context


class WeeklyReportUpdateView(ReportView, ConstructionUpdateView):
    form_class = ReportForm
    template_name = "construction/weekly_report_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        construction_id = self.kwargs['construction_id']
        weekly_report = self.object
        start_date = weekly_report.start_date
        end_date = weekly_report.end_date
        date_range = daterange(start_date, end_date)

        works = ConstructionService.get_construction_work_by_date_range(construction_id, date_range)
        works_data = self._make_all_construction_works_context(works)
        personnel_expenses = ConstructionService.get_personnel_expense_by_date_range(construction_id, date_range)
        personnel_expense_sum = personnel_expenses.aggregate(sum=Coalesce(Sum('amount'), 0))
        expenses = ConstructionService.get_expense_by_date_range(construction_id, date_range)
        expense_sum = expenses.aggregate(sum=Coalesce(Sum('amount'), 0))

        expense_data_day = []
        for single_date in date_range:
            per_ex_day = personnel_expenses.filter(date=single_date)
            per_ex_sum_day = per_ex_day.aggregate(sum=Coalesce(Sum('amount'), 0))
            ex_day = expenses.filter(date=single_date)
            ex_sum_day = ex_day.aggregate(sum=Coalesce(Sum('amount'), 0))
            data_list = {
                'date': single_date,
                'per_ex_day': per_ex_day,
                'per_ex_sum': per_ex_sum_day['sum'],
                'ex_day': ex_day,
                'ex_sum': ex_sum_day['sum']
            }
            expense_data_day.append(data_list)

        context.update(
            works=works_data,
            expense_data_day=expense_data_day,
            personnel_expenses=personnel_expenses,
            personnel_expense_sum=personnel_expense_sum['sum'],
            expenses=expenses,
            expense_sum=expense_sum['sum'],
            date_range=date_range
        )

        return context

    def get_success_url(self):
        construction_id = self.kwargs.get('construction_id')
        return reverse_lazy('construction:weekly-report-list', kwargs={'construction_id': construction_id})
