import logging
from datetime import datetime

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.construction.models import ConstructionPicture
from buildblock.apps.construction.views.base import ConstructionListView
from buildblock.decorators import catch_errors, require_post
from buildblock.services.construction import ConstructionService
from buildblock.utils import get_required_post_data

logger = logging.getLogger(__name__)


@catch_errors
@require_post('construction')
def add_picture(request):
    work_id = get_required_post_data(request, 'work_id')
    picture = get_required_post_data(request, 'picture')
    return_url = get_required_post_data(request, 'return_url')
    status = get_required_post_data(request, 'status')

    data_dict = dict(status=status)
    ConstructionService.add_picture(
        work_id=work_id,
        picture=picture,
        data_dict=data_dict
    )
    messages.success(request, _("A construction photo has been registered."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def delete_picture(request):
    return_url = get_required_post_data(request, 'return_url')
    picture_id = get_required_post_data(request, 'picture_id')

    ConstructionService.delete_picture(picture_id)
    messages.success(request, _("A construction photo has been deleted."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def edit_picture(request):
    return_url = get_required_post_data(request, 'return_url')
    picture_id = get_required_post_data(request, 'picture_id')
    status = get_required_post_data(request, 'status')
    description = request.POST.get('description')

    data_dict = dict(
        status=status,
        description=description
    )
    ConstructionService.edit_picture(picture_id, data_dict)
    messages.success(request, _("A construction photo has been updated."))
    return redirect(return_url)


class PictureView:
    model = ConstructionPicture
    context_object_name = 'pictures'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            construction_work__construction__id=self.kwargs['construction_id']
        )
        return queryset


class PictureListView(PictureView, ConstructionListView):
    template_name = "construction/picture_list.html"
    page_title = "PICTURE LIST"
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Date Range Filter
        if self.request.GET.get('start_date') and self.request.GET.get('end_date'):
            start_date = datetime.fromtimestamp(float(self.request.GET.get('start_date')))
            end_date = datetime.fromtimestamp(float(self.request.GET.get('end_date')))
            queryset = queryset.filter(created_at__range=[start_date, end_date])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pictures = context["pictures"]
        context["pictures"] = [
            self._make_construction_picture_context(picture)
            for picture in pictures
        ]
        return context
