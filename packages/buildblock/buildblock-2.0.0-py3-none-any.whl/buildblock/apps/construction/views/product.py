import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.construction.models import ConstructionWork
from buildblock.apps.construction.views.base import ConstructionTemplateView
from buildblock.decorators import catch_errors, require_post
from buildblock.services.product import ProductService
from buildblock.utils import get_required_post_data

logger = logging.getLogger(__name__)


@catch_errors
@require_post('construction')
def add_zone(request):
    return_url = get_required_post_data(request, 'return_url')
    product_code = get_required_post_data(request, 'product_code')
    zone_name = get_required_post_data(request, 'zone_name')

    ProductService.add_zone(product_code, zone_name)
    messages.success(request, _("A zone has been registered."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def edit_zone(request):
    return_url = get_required_post_data(request, 'return_url')
    product_code = get_required_post_data(request, 'product_code')
    zone_id = get_required_post_data(request, 'zone_id')
    zone_name = get_required_post_data(request, 'zone_name')

    ProductService.edit_zone(product_code, zone_id, zone_name)
    messages.success(request, _("The zone has been updated."))
    return redirect(return_url)


@catch_errors
@require_post('construction')
def delete_zone(request):
    return_url = get_required_post_data(request, 'return_url')
    product_code = get_required_post_data(request, 'product_code')
    zone_id = get_required_post_data(request, 'zone_id')

    # Validation: Work에서 해당 영역이 없는지 확인
    works = ConstructionWork.objects.filter(
        construction__product__code=product_code,
        zone_ids__in=zone_id
    )
    if works:
        messages.error(request, _("Please delete the zone after removing it from the work that contains the zone."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    ProductService.delete_zone(product_code, zone_id)
    messages.success(request, _("The zone has been deleted."))
    return redirect(return_url)


class ProductZoneView(ConstructionTemplateView):
    page_title = "Product Zone Update"
    template_name = 'construction/product_zone.html'
