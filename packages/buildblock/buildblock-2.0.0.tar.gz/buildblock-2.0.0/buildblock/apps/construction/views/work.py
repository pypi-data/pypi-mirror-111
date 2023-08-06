import logging

from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.construction.forms import (
    AddWorkDateValForm,
    AddWorkerValForm,
    AddWorkValForm,
    EditWorkerValForm,
    EditWorkValForm
)
from buildblock.apps.construction.models import ConstructionWork, Worker
from buildblock.apps.construction.views.base import ConstructionDetailView, ConstructionListView
from buildblock.decorators import catch_errors, require_post
from buildblock.helper import db_update
from buildblock.services.construction import ConstructionService
from buildblock.utils import get_required_post_data

logger = logging.getLogger(__name__)


def _worker_sum_data(model):
    total = model.aggregate(total_times=Coalesce(Sum('work_hours'), 0), total_payment=Coalesce(Sum('amount'), 0))
    return {
        'total_times': total['total_times'],
        'total_payment': total['total_payment']
    }


@catch_errors
@require_post('construction')
def add_work(request):
    form = AddWorkValForm(request.POST, request.FILES)
    # TODO zone_validation은 함수로 따로 체크
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return_url = get_required_post_data(request, 'return_url')
    construction_id = get_required_post_data(request, 'construction_id')
    work_type_id = get_required_post_data(request, 'work_type')
    title = get_required_post_data(request, 'title')
    zone_ids = request.POST.getlist('zone[]')

    data_dict = dict(
        zone_ids=zone_ids,
        title=title
    )
    ConstructionService.add_work(
        construction_id=construction_id,
        type_id=work_type_id,
        data_dict=data_dict
    )
    messages.success(request, _("A construction work has been registered."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def edit_work(request):
    form = EditWorkValForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return_url = get_required_post_data(request, 'return_url')
    work_id = get_required_post_data(request, 'work_id')
    work_type_id = get_required_post_data(request, 'work_type')
    title = get_required_post_data(request, 'title')
    zone_ids = request.POST.getlist('zone[]')

    data_dict = dict(
        type_id=work_type_id,
        zone_ids=zone_ids,
        title=title
    )
    ConstructionService.edit_work(work_id, data_dict)
    messages.success(request, _("A construction work has been edited."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def delete_work(request):
    work_id = get_required_post_data(request, 'work_id')
    construction_id = get_required_post_data(request, 'construction_id')

    ConstructionService.delete_work(work_id)
    messages.success(request, _("A construction work has been deleted."))
    return redirect(reverse('construction:work-list', kwargs={'construction_id': construction_id}))


@catch_errors
@require_post('construction')
def add_worker(request):
    form = AddWorkerValForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return_url = get_required_post_data(request, 'return_url')
    name = get_required_post_data(request, 'name')
    role = get_required_post_data(request, 'role')
    phone_number = request.POST.get('phone')
    speciality = request.POST.getlist('speciality[]')
    description = request.POST.get('description')

    data_dict = dict(
        phone_number=phone_number,
        speciality=speciality,
        description=description,
    )
    ConstructionService.add_worker(name, role, data_dict)
    messages.success(request, _("A worker has been registered."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def edit_worker(request):
    form = EditWorkerValForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return_url = get_required_post_data(request, 'return_url')
    worker_id = get_required_post_data(request, 'worker_id')
    name = get_required_post_data(request, 'name')
    role = get_required_post_data(request, 'role')
    phone_number = request.POST.get('phone')
    speciality = request.POST.getlist('speciality[]')
    description = request.POST.get('description')

    ConstructionService.edit_worker(worker_id, dict(
        name=name,
        phone_number=phone_number,
        role=role,
        speciality=speciality,
        description=description
    ))
    messages.success(request, _("A worker information has been edited."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def delete_worker(request):
    return_url = get_required_post_data(request, 'return_url')
    worker_id = get_required_post_data(request, 'worker_id')

    ConstructionService.delete_worker(worker_id)
    messages.success(request, _("A worker has been deleted."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def add_work_date(request):
    form = AddWorkDateValForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return_url = form.cleaned_data['return_url']
    work_id = form.cleaned_data['work_id']
    work_date = form.cleaned_data['work_date']

    work = ConstructionWork.objects.get(id=work_id)
    if work_date in work.work_date:
        messages.warning(request, _("Already registered."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    work.work_date.append(work_date)
    db_update(work)
    messages.success(request, _("A construction work has been edited."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def delete_work_date(request):
    form = AddWorkDateValForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.warning(request, _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return_url = form.cleaned_data['return_url']
    work_id = form.cleaned_data['work_id']
    work_date = form.cleaned_data['work_date']

    work = ConstructionWork.objects.get(id=work_id)
    if work_date not in work.work_date:
        messages.warning(request, _("Already deleted."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    work.work_date.remove(work_date)
    db_update(work)
    messages.success(request, _("A work has been deleted from this report."))
    return redirect(return_url)


class WorkView:
    model = ConstructionWork
    context_object_name = 'works'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(construction__id=self.kwargs['construction_id'])


class WorkListView(WorkView, ConstructionListView):
    template_name = "construction/work_list.html"
    page_title = "WORK LIST"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(construction__id=self.kwargs['construction_id'])
        if self.request.GET.get('zone'):
            zone_id = int(self.request.GET.get('zone'))
            queryset = queryset.filter(zone_ids__contains=[zone_id])
        if self.request.GET.get('work_type'):
            queryset = queryset.filter(type=self.request.GET.get('work_type'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self._make_all_construction_works_context(
            works=context[self.context_object_name]
        )
        return context


class WorkDetailView(WorkView, ConstructionDetailView):
    page_title = "WORK INFO"
    template_name = 'construction/work_detail.html'
    context_object_name = 'work'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work = self.object
        context['work'] = self._make_construction_work_context(work)
        context['pictures'] = self._make_all_work_pictures_context(work)
        return context


class WorkerListView(ConstructionListView):
    template_name = "construction/worker_list.html"
    page_title = "WORKER LIST"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workers = Worker.objects.all()
        worker_data = []

        for worker in workers:
            personnel_expense_data = ConstructionService.get_personnel_expense_by_worker(worker.id)
            data_list = {
                'data': ConstructionService.get_worker(worker.id),
                'sum': _worker_sum_data(personnel_expense_data)
            }
            worker_data.append(data_list)

        context['worker_data'] = worker_data

        return context
